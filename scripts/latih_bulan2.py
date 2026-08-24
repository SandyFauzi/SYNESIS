"""Latih pengklasifikasi intent Bulan 2 dengan data sungguhan, lalu uji.

Jalankan lewat jendela sendiri:
    scripts\\latih_bulan2.cmd

Atau langsung:
    . .\\scripts\\activate.ps1
    python scripts\\latih_bulan2.py

Dua resep dilatih berdampingan:

    Sesi 1  regresi softmax satu lapis, numpy murni, hitung kata
    Sesi 2  MLP satu lapisan tersembunyi di atas Tensor, hitung kata dan TF-IDF

Keduanya dilatih pada 1.080 kalimat sintetis, lalu diuji dua kali:

    uji sintetis   belahan yang disisihkan dari data yang sama
    uji nyata      41 pesan asli dari arsip percakapan

Angka kedua yang berlaku. README di data/bulan2 sudah memperingatkan bahwa
pola pembungkus yang sama masuk ke beberapa belahan sintetis, jadi skor
sintetis terlalu mudah. Berkas ini menunjukkan seberapa terlalu mudahnya.
"""

import sys
import time
from collections import Counter
from pathlib import Path

import numpy as np

AKAR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AKAR / "notebooks"))

import bulan2_sesi1_kata as S1        # noqa: E402
import bulan2_sesi2_intent as S2      # noqa: E402

DATA = AKAR / "data" / "bulan2"
LATIH = DATA / "perintah_train_generated.txt"
NYATA = DATA / "perintah_eval_real.txt"
MODEL = DATA / "model_intent.npz"

GARIS = "=" * 70


LOG = DATA / "latihan_terakhir.log"


class Cabang:
    """Salin apa pun yang dicetak ke layar sekaligus ke berkas log.

    Dipasang ke sys.stdout supaya cetakan dari modul sesi ikut tertangkap,
    bukan cuma cetakan berkas ini.
    """

    def __init__(self, layar, berkas):
        self.layar, self.berkas = layar, berkas

    def write(self, teks):
        self.layar.write(teks)
        self.layar.flush()
        self.berkas.write(teks)
        self.berkas.flush()
        return len(teks)

    def flush(self):
        self.layar.flush()
        self.berkas.flush()


catat = print


def baca(berkas):
    pasang = []
    for baris in berkas.read_text(encoding="utf-8").strip().splitlines():
        baris = baris.strip()
        if not baris or baris.startswith("#"):
            continue
        label, kalimat = baris.split("|", 1)
        pasang.append((kalimat.strip().lower(), label.strip()))
    return pasang


# ══════════════════════════════════════════════════════════════
# BAGIAN 1 - data
# ══════════════════════════════════════════════════════════════

def bagian1():
    catat(GARIS, "\nBAGIAN 1  data\n", GARIS, sep="")

    latih_semua = baca(LATIH)
    nyata = baca(NYATA)

    tr, va, te = S2.belah_tiga(latih_semua, seed=0)
    catat(f"  sintetis  : {len(latih_semua)} kalimat, "
          f"{len(set(l for _, l in latih_semua))} intent")
    catat(f"  belahan   : latih {len(tr)}, validasi {len(va)}, uji {len(te)}")
    catat(f"  nyata     : {len(nyata)} pesan, "
          f"{len(set(l for _, l in nyata))} intent terpakai\n")

    hn = Counter(l for _, l in nyata)
    catat(f"  {'intent':<20}{'sintetis':>10}{'nyata':>8}")
    catat("  " + "-" * 38)
    hs = Counter(l for _, l in latih_semua)
    for label in sorted(hs):
        catat(f"  {label:<20}{hs[label]:>10}{hn.get(label, 0):>8}")

    kos = S2.bangun_kosakata([k for k, _ in tr])
    import re
    asing = tot = 0
    for kalimat, _ in nyata:
        for kata in re.findall(r"[a-z0-9]+", kalimat.lower()):
            tot += 1
            asing += kata not in kos
    catat(f"""
  kosakata dari latih sintetis  : {len(kos)} kata
  kata pesan nyata di luar itu  : {asing} dari {tot} = {asing / tot * 100:.1f} persen

  Angka terakhir itu ramalan paling jujur untuk apa yang akan terjadi nanti.
  Model tidak punya kolom untuk kata yang tidak pernah dilihatnya; kata itu
  hilang begitu saja dari vektor. Kalau {asing / tot * 100:.0f} persen kata di
  sebuah pesan menguap sebelum model melihatnya, sisa kalimatnya harus bekerja
  sangat keras.""")
    return tr, va, te, nyata


# ══════════════════════════════════════════════════════════════
# BAGIAN 2 - resep Sesi 1
# ══════════════════════════════════════════════════════════════

def latih_sesi1(Xtr, ytr, Xva, yva, n_kelas, n_iter=3000, lr=0.5, kabar=300):
    """Regresi softmax satu lapis. Persis Bagian 5 Sesi 1, tanpa lapisan
    tersembunyi, memakai softmax tulisan pemilik."""
    rng = np.random.default_rng(0)
    W = rng.normal(0, 0.1, (Xtr.shape[1], n_kelas))
    b = np.zeros(n_kelas)
    T = np.zeros((len(ytr), n_kelas))
    T[np.arange(len(ytr)), ytr] = 1.0

    terbaik = None
    for i in range(n_iter):
        P = S1.softmax(Xtr @ W + b)
        dZ = (P - T) / len(ytr)
        W -= lr * (Xtr.T @ dZ)
        b -= lr * dZ.sum(0)
        if i % 50 == 0 or i == n_iter - 1:
            av = (S1.softmax(Xva @ W + b).argmax(1) == yva).mean()
            if terbaik is None or av >= terbaik[0]:
                terbaik = (av, i, W.copy(), b.copy())
            if kabar and i % kabar == 0:
                rugi = -np.log(np.clip(P[np.arange(len(ytr)), ytr], 1e-12, 1)).mean()
                catat(f"    iterasi {i:>5}   rugi {rugi:.4f}   "
                      f"validasi {av * 100:5.1f} persen")
    return terbaik[2], terbaik[3], terbaik[0], terbaik[1]


def bagian2(tr, va, te, label2i):
    catat("\n" + GARIS, "\nBAGIAN 2  resep Sesi 1, regresi softmax numpy murni\n",
          GARIS, sep="")

    kos = S2.bangun_kosakata([k for k, _ in tr])
    Xtr = S2.vektorkan([k for k, _ in tr], kos)
    Xva = S2.vektorkan([k for k, _ in va], kos)
    Xte = S2.vektorkan([k for k, _ in te], kos)
    ytr = np.array([label2i[l] for _, l in tr])
    yva = np.array([label2i[l] for _, l in va])
    yte = np.array([label2i[l] for _, l in te])

    catat(f"  {Xtr.shape[1]} kolom kosakata, {len(label2i)} kelas, "
          f"{Xtr.shape[1] * len(label2i) + len(label2i)} parameter\n")
    t0 = time.perf_counter()
    W, b, av, ep = latih_sesi1(Xtr, ytr, Xva, yva, len(label2i))
    dt = time.perf_counter() - t0

    ate = (S1.softmax(Xte @ W + b).argmax(1) == yte).mean()
    catat(f"\n  epoch terpilih : {ep}   validasi {av * 100:.1f} persen")
    catat(f"  uji sintetis   : {ate * 100:.1f} persen")
    catat(f"  waktu latih    : {dt:.1f} detik")
    return {"nama": "Sesi 1 softmax", "kos": kos, "idf": None,
            "ramal": lambda X: S1.softmax(X @ W + b), "uji_sintetis": ate,
            "simpan": {"W": W, "b": b}}


# ══════════════════════════════════════════════════════════════
# BAGIAN 3 - resep Sesi 2
# ══════════════════════════════════════════════════════════════

def bagian3(tr, va, te, label2i):
    catat("\n" + GARIS, "\nBAGIAN 3  resep Sesi 2, MLP di atas Tensor\n",
          GARIS, sep="")

    kos = S2.bangun_kosakata([k for k, _ in tr])
    idf = S2.bobot_idf([k for k, _ in tr], kos)
    ytr = np.array([label2i[l] for _, l in tr])
    yva = np.array([label2i[l] for _, l in va])
    yte = np.array([label2i[l] for _, l in te])

    keluar = []
    for nama, pakai in (("hitung kata", None), ("TF-IDF", idf)):
        catat(f"\n  {nama}")
        Xtr = S2.vektorkan([k for k, _ in tr], kos, pakai)
        Xva = S2.vektorkan([k for k, _ in va], kos, pakai)
        Xte = S2.vektorkan([k for k, _ in te], kos, pakai)
        t0 = time.perf_counter()
        param, terbaik = S2.latih(Xtr, ytr, Xva, yva, len(label2i),
                                  n_h=96, epoch=600, kabar=100)
        dt = time.perf_counter() - t0
        ate = (S2.maju(param, Xte).data.argmax(1) == yte).mean()
        catat(f"    epoch terpilih {terbaik[1]}, validasi "
              f"{terbaik[0] * 100:.1f} persen, uji sintetis {ate * 100:.1f} "
              f"persen, {dt:.1f} detik")

        def buat(param=param, pakai=pakai):
            def ramal(X):
                z = S2.maju(param, X).data
                e = np.exp(z - z.max(axis=1, keepdims=True))
                return e / e.sum(axis=1, keepdims=True)
            return ramal

        keluar.append({"nama": f"Sesi 2 {nama}", "kos": kos, "idf": pakai,
                       "ramal": buat(), "uji_sintetis": ate,
                       "simpan": {f"p{i}": p.data
                                  for i, p in enumerate(param)}})
    return keluar


# ══════════════════════════════════════════════════════════════
# BAGIAN 4 - ujian sebenarnya
# ══════════════════════════════════════════════════════════════

def bagian4(model, nyata, label2i):
    catat("\n" + GARIS, "\nBAGIAN 4  ujian sebenarnya, 41 pesan nyata\n",
          GARIS, sep="")

    ynyata = np.array([label2i[l] for _, l in nyata])
    kalimat = [k for k, _ in nyata]

    catat(f"  {'resep':<22}{'uji sintetis':>15}{'pesan nyata':>14}{'jatuh':>9}")
    catat("  " + "-" * 60)
    for m in model:
        X = S2.vektorkan(kalimat, m["kos"], m["idf"])
        a = (m["ramal"](X).argmax(1) == ynyata).mean()
        m["nyata"] = a
        catat(f"  {m['nama']:<22}{m['uji_sintetis'] * 100:>14.1f}%"
              f"{a * 100:>13.1f}%{(m['uji_sintetis'] - a) * 100:>8.1f}")

    catat("""
  Kolom terakhir itu inti seluruh berkas ini.

  Data sintetis dibuat dari sejumlah kecil pola pembungkus yang dipasangkan
  ke sejumlah kecil objek. Model tidak perlu memahami perintahnya; cukup
  menghafal pembungkusnya. Karena pembungkus yang sama muncul di belahan
  latih dan belahan uji, uji sintetis mengukur hafalan itu dan menyebutnya
  akurasi.

  Pesan nyata tidak punya pembungkus itu. Di situ angkanya jatuh.""")

    puncak = max(m["nyata"] for m in model)
    seri = [m["nama"] for m in model if m["nyata"] == puncak]
    terbaik = next(m for m in model if m["nyata"] == puncak)
    catat(f"\n  Resep terbaik di pesan nyata: {terbaik['nama']}")
    if len(seri) > 1:
        catat(f"  Seri dengan {len(seri)} resep: {', '.join(seri)}.")
        catat("  Seri dimenangkan yang paling sederhana, bukan yang paling "
              "canggih.")
    catat("")

    X = S2.vektorkan(kalimat, terbaik["kos"], terbaik["idf"])
    p = terbaik["ramal"](X)
    tebak = p.argmax(1)
    label = [l for l, _ in sorted(label2i.items(), key=lambda kv: kv[1])]

    catat("  Yang salah, beserta keyakinannya:\n")
    for i in np.nonzero(tebak != ynyata)[0]:
        catat(f"    '{kalimat[i][:52]}'")
        catat(f"      benar {label[ynyata[i]]:<18} ditebak "
              f"{label[tebak[i]]:<18} yakin {p[i].max():.3f}")
    return terbaik, p, tebak, ynyata, label


# ══════════════════════════════════════════════════════════════
# BAGIAN 5 - ambang di pesan nyata
# ══════════════════════════════════════════════════════════════

def bagian5(p, tebak, ynyata, label):
    catat("\n" + GARIS, "\nBAGIAN 5  ambang, diuji di pesan nyata\n",
          GARIS, sep="")

    catat(f"  {'ambang':>8}{'benar':>9}{'salah':>9}{'menolak':>10}"
          f"{'presisi yang dijawab':>23}")
    catat("  " + "-" * 59)
    for ambang in (0.0, 0.3, 0.5, 0.7, 0.9):
        lolos = p.max(1) >= ambang
        benar = int(((tebak == ynyata) & lolos).sum())
        salah = int(((tebak != ynyata) & lolos).sum())
        pres = benar / (benar + salah) if benar + salah else float("nan")
        catat(f"  {ambang:>8.2f}{benar:>9}{salah:>9}{int((~lolos).sum()):>10}"
              f"{pres * 100:>22.1f}%")

    catat("""
  Kolom terakhir yang menentukan apakah ini layak dipasang ke SYNESIS.

  Akurasi mentah menjawab "berapa persen pesan yang benar". Presisi
  yang-dijawab menjawab "kalau ia menjawab, berapa persen jawabannya benar".
  Untuk asisten yang menjalankan perintah, yang kedua jauh lebih penting,
  karena menolak itu murah dan salah jalan itu mahal.

  Cari baris di mana presisi cukup tinggi untuk dipercaya. Berapa banyak
  pesan yang harus ditolak untuk sampai ke situ adalah harga yang kamu bayar,
  dan harga itu turun hanya dengan menambah data nyata.""")


# ══════════════════════════════════════════════════════════════
# BAGIAN 6 - simpan
# ══════════════════════════════════════════════════════════════

def bagian6(terbaik, label2i):
    catat("\n" + GARIS, "\nBAGIAN 6  simpan model\n", GARIS, sep="")

    label = [l for l, _ in sorted(label2i.items(), key=lambda kv: kv[1])]
    np.savez_compressed(
        MODEL,
        resep=np.array(terbaik["nama"]),
        label=np.array(label),
        kosakata=np.array(sorted(terbaik["kos"], key=terbaik["kos"].get)),
        idf=(terbaik["idf"] if terbaik["idf"] is not None else np.zeros(0)),
        **terbaik["simpan"],
    )
    catat(f"  resep    : {terbaik['nama']}")
    catat(f"  disimpan : {MODEL}")
    catat(f"  ukuran   : {MODEL.stat().st_size / 1024:.1f} KB")
    catat("""
  Berkas ini yang nanti dibaca SYNESIS. Isinya nama resep, label, kosakata,
  bobot IDF kalau dipakai, dan larik parameternya. Tidak ada kode di
  dalamnya.""")


if __name__ == "__main__":
    DATA.mkdir(parents=True, exist_ok=True)
    sys.stdout = Cabang(sys.stdout, LOG.open("w", encoding="utf-8"))
    mulai = time.perf_counter()
    tr, va, te, nyata = bagian1()

    semua_label = sorted({l for _, l in tr + va + te + nyata})
    label2i = {l: i for i, l in enumerate(semua_label)}

    model = [bagian2(tr, va, te, label2i)]
    model += bagian3(tr, va, te, label2i)
    terbaik, p, tebak, ynyata, label = bagian4(model, nyata, label2i)
    bagian5(p, tebak, ynyata, label)
    bagian6(terbaik, label2i)

    catat(f"\n{GARIS}")
    catat(f"  selesai dalam {time.perf_counter() - mulai:.1f} detik")
    catat(f"  catatan lengkap : {LOG}")
    catat(GARIS)
