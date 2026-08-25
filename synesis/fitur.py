"""Kalimat -> vektor, kalimat -> slot.

Salinan kanonik untuk aplikasi. Versi latihan ada di
notebooks/bulan2_sesi2_intent.py dan sengaja dibiarkan terpisah; notebooks
itu jawaban ujian yang dibekukan, berkas ini yang dirawat.
"""

import importlib.util
import re

import numpy as np

from . import konfig

KATA = re.compile(r"[a-z0-9]+")

WAKTU = {
    "hari ini": 0, "sekarang": 0, "kemarin": -1, "besok": 1, "lusa": 2,
    "minggu lalu": -7, "minggu depan": 7, "bulan lalu": -30, "bulan depan": 30,
    "tadi pagi": 0, "tadi malam": -1,
}

ANGKA = {
    "satu": 1, "dua": 2, "tiga": 3, "empat": 4, "lima": 5, "enam": 6,
    "tujuh": 7, "delapan": 8, "sembilan": 9, "sepuluh": 10, "sebelas": 11,
    "dua belas": 12,
}

JAM = re.compile(
    r"\bjam\s+(dua belas|sebelas|sepuluh|sembilan|delapan|tujuh|enam|"
    r"lima|empat|tiga|dua|satu|[0-9]{1,2})(?:\s+(pagi|siang|sore|malam))?\b")

KERJA = re.compile(
    r"^(?:tolong\s+)?(?:buka(?:in|kan)?|tampilkan|cari(?:in|kan)?|temukan|"
    r"ingatkan(?:\s+aku)?|jadwalkan|setel)\b")

SORE = {"siang", "sore", "malam"}


def potong(teks):
    return KATA.findall(teks.lower())


def vektorkan(kalimat, kosakata, idf=None):
    """(n_kalimat, n_kosakata). idf None -> hitung kata mentah."""
    X = np.zeros((len(kalimat), len(kosakata)))
    for i, teks in enumerate(kalimat):
        for kata in potong(teks):
            j = kosakata.get(kata)
            if j is not None:
                X[i, j] += 1
    if idf is not None:
        X *= idf
        panjang = np.linalg.norm(X, axis=1, keepdims=True)
        np.divide(X, panjang, out=X, where=panjang != 0)
    return X


def dikenal(kalimat, kosakata):
    return any(w in kosakata for w in potong(kalimat))


# ── encoder pretrained, opsional ─────────────────────────────────
# sentence-transformers sengaja tidak diwajibkan. Tanpa dia SYNESIS tetap
# jalan penuh dengan resep "kantong"; yang hilang cuma dua resep lain.

_ENCODER = None


def encoder_ada():
    """Ada paketnya atau tidak, TANPA mengimpornya.

    Mengimpor sentence_transformers menarik torch dan transformers sekalian,
    sekitar sepuluh detik. Jendela memanggil ini saat dibangun, jadi cek yang
    mengimpor membuat jendelanya lambat dibuka tanpa alasan.
    """
    return importlib.util.find_spec("sentence_transformers") is not None


def muat_encoder():
    """Muat sekali, pakai berkali-kali. Muatnya sekitar 9 detik."""
    global _ENCODER
    if _ENCODER is None:
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as e:
            raise RuntimeError(
                "Resep ini butuh sentence-transformers.\n"
                "  pasang: pip install sentence-transformers\n"
                "  atau pakai resep 'kantong' yang tidak butuh apa-apa."
            ) from e
        _ENCODER = SentenceTransformer(konfig.ENCODER)
    return _ENCODER


def encode(kalimat, batch=128):
    """(n, 384), tiap baris sudah panjang 1."""
    v = muat_encoder().encode(list(kalimat), batch_size=batch,
                              show_progress_bar=False,
                              normalize_embeddings=True)
    return np.asarray(v, dtype=np.float64)


def encode_tercache(kalimat, berkas=None):
    """Sama seperti encode, tapi yang sudah pernah dihitung tidak diulang.

    Ini yang menjaga latih ulang tetap beberapa detik. Tanpa cache, tiap
    latihan mengencode ribuan kalimat yang sama dari nol.
    """
    berkas = berkas or konfig.EMBED_CACHE
    kalimat = list(kalimat)
    simpan = {}
    if berkas.exists():
        d = np.load(berkas, allow_pickle=False)
        simpan = dict(zip((str(t) for t in d["teks"]), d["vek"]))

    baru = [k for k in dict.fromkeys(kalimat) if k not in simpan]
    if baru:
        for k, v in zip(baru, encode(baru)):
            simpan[k] = v
        berkas.parent.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(
            berkas,
            teks=np.array(list(simpan), dtype=object).astype(str),
            vek=np.array(list(simpan.values())))
    return np.array([simpan[k] for k in kalimat]), len(baru)


def bangun_fitur(kalimat, resep, kosakata=None, idf=None, cache=False):
    """Satu-satunya tempat resep diterjemahkan jadi matriks.

    Dipakai trainer maupun peramal. Kalau keduanya membangun fitur sendiri,
    suatu hari mereka akan membangunnya berbeda dan tidak ada yang sadar.
    """
    if resep not in konfig.RESEP:
        raise ValueError(f"resep tak dikenal: {resep}")
    bagian = []
    if resep in ("kantong", "gabung"):
        bagian.append(vektorkan(kalimat, kosakata, idf))
    if resep in ("encoder", "gabung"):
        bagian.append(encode_tercache(kalimat)[0] if cache else encode(kalimat))
    return np.hstack(bagian) if len(bagian) > 1 else bagian[0]


def ekstrak_slot(kalimat):
    """Kunci yang mungkin muncul: waktu (geseran hari), jam, objek.

    Aturan tangan, bukan model. Slot yang tidak disebut tidak ditebak.
    """
    teks = kalimat.lower().strip()
    slot = {}

    # frasa terpanjang dulu: "minggu lalu" mengandung "lalu"
    for frasa in sorted(WAKTU, key=len, reverse=True):
        pola = rf"\b{re.escape(frasa)}\b"
        if re.search(pola, teks):
            slot["waktu"] = WAKTU[frasa]
            teks = re.sub(pola, " ", teks, count=1)
            break

    cocok = JAM.search(teks)
    if cocok:
        mentah, penanda = cocok.groups()
        jam = ANGKA.get(mentah, int(mentah) if mentah.isdigit() else 0)
        if penanda in SORE and 1 <= jam < 12:
            jam += 12
        if 0 <= jam <= 23:
            slot["jam"] = f"{jam:02d}:00"
        teks = teks[:cocok.start()] + " " + teks[cocok.end():]

    objek = " ".join(KERJA.sub("", teks).split())
    if objek:
        slot["objek"] = objek
    return slot


def _demo():
    kos = {"buka": 0, "berkas": 1, "disk": 2}
    X = vektorkan(["buka berkas", "disk disk"], kos)
    assert X.tolist() == [[1, 1, 0], [0, 0, 2]]

    idf = np.array([1.0, 2.0, 1.0])
    Y = vektorkan(["buka berkas"], kos, idf)
    assert abs(np.linalg.norm(Y[0]) - 1.0) < 1e-12
    assert vektorkan(["zzz"], kos, idf).tolist() == [[0, 0, 0]]

    assert dikenal("buka apa", kos) and not dikenal("zzz qqq", kos)

    s = ekstrak_slot("buka laporan praktikum minggu lalu")
    assert s == {"waktu": -7, "objek": "laporan praktikum"}, s
    assert ekstrak_slot("ingatkan aku jam 3 sore")["jam"] == "15:00"
    assert ekstrak_slot("ingatkan aku jam 3")["jam"] == "03:00"
    assert "jam" not in ekstrak_slot("buka berkas")
    assert ekstrak_slot("") == {}

    assert bangun_fitur(["buka berkas"], "kantong", kos).shape == (1, 3)
    try:
        bangun_fitur([], "ngawur", kos)
        raise AssertionError("resep ngawur harus ditolak")
    except ValueError:
        pass

    if encoder_ada():
        v = encode(["buka berkas laporan", "bukain file laporan",
                    "pasang numpy"])
        assert v.shape == (3, 384)
        assert abs(np.linalg.norm(v[0]) - 1) < 1e-5
        # yang sekerabat harus lebih dekat daripada yang tidak
        assert v[0] @ v[1] > v[0] @ v[2]
        assert bangun_fitur(["buka berkas"], "gabung", kos).shape == (1, 387)
        print("fitur: lulus (encoder ada)")
    else:
        print("fitur: lulus (tanpa encoder)")


if __name__ == "__main__":
    _demo()
