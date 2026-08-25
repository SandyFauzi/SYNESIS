"""Kalimat -> intent -> tindakan. Ongkos yang memutuskan, bukan peluang."""

import inspect
import json
import re
from datetime import datetime, timezone

import numpy as np

from . import alat, konfig
from .fitur import bangun_fitur, dikenal, ekstrak_slot

BACA, TULIS, MERUSAK, BAHASA = "BACA", "TULIS", "MERUSAK", "BAHASA"

# intent -> (alat di alat.DAFTAR, kelas risiko). None = belum ada alatnya.
# Kelas ditentukan ongkos salah panggil, bukan kerumitan alatnya.
RUTE = {
    "buka_berkas":      ("baca_berkas", BACA),
    "cari_berkas":      ("cari_berkas", BACA),
    "info_sistem":      ("info_sistem", BACA),
    "hitung":           (None, BACA),
    "jadwal":           (None, TULIS),
    "kelola_repo":      ("jalankan", TULIS),
    "jalankan_program": ("jalankan", MERUSAK),
    "kontrol_sistem":   ("jalankan", MERUSAK),
    "pasang_paket":     ("jalankan", MERUSAK),
    "jelaskan_konsep":  (None, BAHASA),
    "lanjut_tugas":     (None, BAHASA),
    "obrol":            (None, BAHASA),
    "ringkas_catatan":  (None, BAHASA),
    "tanya_umum":       (None, BAHASA),
    "ubah_proyek":      (None, BAHASA),
}

KUNCI = ("kalimat", "intent", "yakin", "risiko", "alat", "argumen",
         "tindakan", "hasil")

# "buka berkas readme" -> objeknya "readme", bukan "berkas readme".
# Kata-kata ini menyebut JENIS bendanya, bukan namanya, jadi ia cuma
# meracuni pola glob.
PENGISI = re.compile(r"^(berkas|file|dokumen|folder|direktori)\b\s*", re.I)


class ModelHilang(SystemExit):
    pass


def muat_model(berkas=None):
    berkas = berkas or konfig.MODEL_INTENT
    if not berkas.exists():
        raise ModelHilang(f"No model at {berkas}.\n"
                          f"  Train first: python -m synesis.latih")
    d = np.load(berkas, allow_pickle=False)
    resep = str(d["resep"])
    # Model lama menyimpan nama resep versi notebook.
    if resep not in konfig.RESEP:
        resep = "kantong"
    return {
        "resep": resep,
        "label": [str(x) for x in d["label"]],
        "kosakata": {str(w): i for i, w in enumerate(d["kosakata"])},
        "idf": d["idf"] if d["idf"].size else None,
        "W": d["W"],
        "b": d["b"],
    }


def ramal(model, kalimat):
    X = bangun_fitur(kalimat, model["resep"], model["kosakata"], model["idf"])
    z = X @ model["W"] + model["b"]
    e = np.exp(z - z.max(axis=1, keepdims=True))
    return e / e.sum(axis=1, keepdims=True)


def ambang_dari_ongkos(risiko, ongkos_salah=None,
                       ongkos_tolak=konfig.ONGKOS_TOLAK):
    """c_salah (1 - p) < c_tolak  ->  p > 1 - c_tolak / c_salah"""
    c = (ongkos_salah or konfig.ONGKOS_SALAH)[risiko]
    if c <= 0:
        return 1.0
    return min(1.0, max(0.0, 1 - ongkos_tolak / c))


def putuskan(peluang, label, ongkos_salah=None,
             ongkos_tolak=konfig.ONGKOS_TOLAK):
    """(indeks, ongkos). -1 = menolak.

    Kelas termurah, bukan kelas terbesar peluangnya. p=0,55 kontrol_sistem
    kalah dari p=0,40 info_sistem karena 200*0,45 jauh di atas 2*0,60.
    """
    tabel = ongkos_salah or konfig.ONGKOS_SALAH
    ongkos = [tabel[RUTE[l][1]] * (1 - p) for l, p in zip(label, peluang)]
    k = int(np.argmin(ongkos))
    return (k, ongkos[k]) if ongkos[k] < ongkos_tolak else (-1, ongkos_tolak)


def slot_ke_argumen(intent, slot):
    """Argumen siap kirim, atau None. None menghentikan pipa, bukan menebak."""
    objek = PENGISI.sub("", slot.get("objek", "").strip()).strip()
    if intent == "info_sistem":
        return ""
    if intent == "buka_berkas":
        return objek or None
    if intent == "cari_berkas":
        if not objek:
            return None
        return objek if any(c in objek for c in "*?") else f"*{objek}*"
    return None


def catat_audit(baris, berkas=None):
    """JSONL, hanya menambah. Mati di tengah merusak satu baris, bukan semua."""
    berkas = berkas or konfig.AUDIT
    baris = {"waktu": datetime.now(timezone.utc).isoformat(), **baris}
    berkas.parent.mkdir(parents=True, exist_ok=True)
    with berkas.open("a", encoding="utf-8") as f:
        print(json.dumps(baris, ensure_ascii=False), file=f)


def _catatan(kalimat, **isi):
    kosong = dict.fromkeys(KUNCI)
    kosong.update(kalimat=kalimat, yakin=0.0, tindakan="jalan", hasil="")
    kosong.update(isi)
    return kosong


def izin_konsol(rencana):
    print(f"\n  SYNESIS wants to run: {rencana}")
    return input("  Allow? [y/N] ").strip().lower() == "y"


def jalankan_pipa(kalimat, model, izin=None, kering=True, audit=None):
    """tindakan: jalan | tolak_kosong | tolak_yakin | tolak_argumen
    | tolak_izin | belum_ada_alat. Semua dicatat, termasuk yang ditolak."""
    # Vektor nol -> jaringan menjawab relu(b1) @ W2 + b2, satu tebakan tetap
    # yang tidak bergantung kalimatnya. Ditahan sebelum model dipanggil.
    if not dikenal(kalimat, model["kosakata"]):
        h = _catatan(kalimat, tindakan="tolak_kosong",
                     hasil="None of these words are in the model vocabulary.")
        catat_audit(h, audit)
        return h

    peluang = ramal(model, [kalimat])[0]
    k, _ = putuskan(peluang, model["label"])
    # Waktu menolak, tebakan terkuat tetap dicatat supaya barisnya bisa dibaca
    # sebagai "ini yang model kira, dan ini kenapa ditahan".
    i = k if k >= 0 else int(peluang.argmax())
    intent = model["label"][i]
    nama, risiko = RUTE[intent]
    h = _catatan(kalimat, intent=intent, yakin=float(peluang[i]),
                 risiko=risiko, alat=nama)

    if k < 0:
        h["tindakan"] = "tolak_yakin"
    elif nama is None:
        h["tindakan"] = "belum_ada_alat"
    else:
        h["argumen"] = slot_ke_argumen(intent, ekstrak_slot(kalimat))
        if h["argumen"] is None:
            h["tindakan"] = "tolak_argumen"
        elif risiko != BACA and not (izin and izin(f"{nama}|{h['argumen']}")):
            h["tindakan"] = "tolak_izin"
        elif kering:
            h["hasil"] = f"(dry run) {nama}|{h['argumen']} not called"
        else:
            h["hasil"] = alat.pakai(nama, h["argumen"], izin)

    catat_audit(h, audit)
    return h


def _demo():
    assert ambang_dari_ongkos(MERUSAK) == 0.995
    assert ambang_dari_ongkos(BACA) == 0.5
    assert ambang_dari_ongkos(BACA, {BACA: 0.5}) == 0.0
    assert ambang_dari_ongkos(BACA, ongkos_tolak=0.0) == 1.0

    label = ["kontrol_sistem", "info_sistem", "obrol"]
    p = np.array([0.55, 0.40, 0.05])
    o = [konfig.ONGKOS_SALAH[RUTE[l][1]] * (1 - q) for l, q in zip(label, p)]
    assert int(p.argmax()) == 0 and int(np.argmin(o)) == 1
    assert putuskan(p, label)[0] == -1
    assert putuskan(np.array([0.02, 0.96, 0.02]), label)[0] == 1   # BACA lewat
    assert putuskan(np.array([0.96, 0.02, 0.02]), label)[0] == -1  # MERUSAK tidak

    assert slot_ke_argumen("cari_berkas", {"objek": "laporan"}) == "*laporan*"
    assert slot_ke_argumen("cari_berkas", {"objek": "file py"}) == "*py*"
    assert slot_ke_argumen("buka_berkas", {"objek": "berkas readme"}) == "readme"
    assert slot_ke_argumen("buka_berkas", {"objek": "berkas"}) is None
    assert slot_ke_argumen("cari_berkas", {"objek": "*.py"}) == "*.py"
    assert slot_ke_argumen("buka_berkas", {}) is None
    assert slot_ke_argumen("info_sistem", {}) == ""
    assert slot_ke_argumen("pasang_paket", {"objek": "numpy"}) is None

    tmp = konfig.AUDIT.parent / "_demo.jsonl"
    tmp.unlink(missing_ok=True)
    catat_audit({"kalimat": "a"}, tmp)
    catat_audit({"kalimat": "b"}, tmp)
    baris = [json.loads(x) for x in tmp.read_text(encoding="utf-8").splitlines()]
    assert len(baris) == 2 and baris[0]["kalimat"] == "a" and "waktu" in baris[0]

    # Mode kering tetap bawaan. Diperiksa di tanda tangannya, bukan lewat
    # keluaran model, supaya tidak ikut goyah tiap kali dilatih ulang.
    assert inspect.signature(jalankan_pipa).parameters["kering"].default is True

    model = muat_model()
    assert jalankan_pipa("zzzqqq wwwxxx", model, audit=tmp)["tindakan"] \
        == "tolak_kosong"
    assert jalankan_pipa("berapa sisa disk", model, audit=tmp)["tindakan"] \
        != "tolak_kosong"
    tmp.unlink()
    print("niat: lulus")


if __name__ == "__main__":
    _demo()
