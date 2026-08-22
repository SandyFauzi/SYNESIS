"""Bukti terukur untuk kunci Bulan 1 Sesi 3+4.

Jalankan:
    . .\\scripts\\activate.ps1
    python notebooks\\kunci_b1s34_bukti.py

Lima pengujian:
  A  m sebagai Value, dan jumlah gradien           -> Soal 1c, 1d
  B  apakah 0.000e+00 itu dijamin atau kebetulan   -> Soal 3a
  C  epoch 7 memburuk: overfit atau lr kebesaran   -> Soal 6a
  D  di batch berapa GPU menang                    -> Soal 5c
  E  lanskap kuartik, momentum lawan RMSprop       -> Soal 7d

Uji D paling lama, sekitar empat menit, karena tiap titik diulang tiga kali
plus sekali pemanasan. Pengulangan itu bukan kemewahan: satu pengukuran di
mesin ini bisa meleset dua kali lipat.
"""

import random
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

import bulan1_sesi34_mnist as S            # noqa: E402
from bulan1_sesi1_autograd import Value    # noqa: E402
from bulan1_sesi2_mlp import MLP           # noqa: E402

GARIS = "=" * 66


# ══════════════════════════════════════════════════════════════
# UJI A  m sebagai Value, dan jumlah gradien
# ══════════════════════════════════════════════════════════════

def silang_m_value(logit, kelas):
    """Varian TODO 1 dengan m dibuat Value, bukan float biasa."""
    puncak = max(v.data for v in logit)
    m = next(v for v in logit if v.data == puncak)
    eksponen = [(v - m).exp() for v in logit]
    return -(eksponen[kelas] / sum(eksponen, Value(0.0))).log()


def ujiA():
    print(GARIS, "\nUJI A  m sebagai Value, dan jumlah gradien  (Soal 1c, 1d)\n",
          GARIS, sep="")

    hasil = {}
    for nama, fn in (("m float", S.softmax_silang_value),
                     ("m Value", silang_m_value)):
        random.seed(0)
        z = [Value(random.gauss(0, 2)) for _ in range(10)]
        rugi = fn(z, 3)
        for v in z:
            v.grad = 0.0
        rugi.backward()
        hasil[nama] = (rugi.data, [v.grad for v in z])
        print(f"  {nama:<8} rugi {rugi.data!r}")
        print(f"  {'':<8} jumlah gradien {sum(v.grad for v in z):.3e}")

    beda = max(abs(a - b) for a, b in zip(hasil["m float"][1],
                                          hasil["m Value"][1]))
    print(f"\n  selisih rugi antara kedua versi    : "
          f"{abs(hasil['m float'][0] - hasil['m Value'][0]):.3e}")
    print(f"  selisih gradien antara kedua versi : {beda:.3e}")

    print("""
  Jawaban 1c benar. Rugi identik sampai bit terakhir, gradien beda di orde
  1e-16 saja. Membuat m jadi Value memberi logit terbesar satu jalur gradien
  tambahan, tapi sumbangan jalur itu saling menghapus karena softmax kebal
  terhadap pergeseran bersama. Yang tersisa cuma pembulatan.

  Jumlah gradien nol dalam batas float64, dan itu jawaban 1d. Aljabarnya
  sum(p) - sum(y) = 1 - 1 = 0.
""")


# ══════════════════════════════════════════════════════════════
# UJI B  apakah nol itu dijamin
# ══════════════════════════════════════════════════════════════

def iteratif(akar, balik):
    urutan, terlihat = [], set()
    tumpukan = [(akar, False)]
    while tumpukan:
        v, sudah = tumpukan.pop()
        if sudah:
            urutan.append(v)
        elif id(v) not in terlihat:
            terlihat.add(id(v))
            tumpukan.append((v, True))
            anak = tuple(v._prev)
            tumpukan.extend((a, False)
                            for a in (reversed(anak) if balik else anak))
    akar.grad = 1.0
    for v in reversed(urutan):
        v._backward()


def acak_urut(akar, seed):
    """Urutan topologis yang sah, tapi anaknya diacak. Tetap benar."""
    rng = random.Random(seed)
    urutan, terlihat = [], set()
    tumpukan = [(akar, False)]
    while tumpukan:
        v, sudah = tumpukan.pop()
        if sudah:
            urutan.append(v)
        elif id(v) not in terlihat:
            terlihat.add(id(v))
            tumpukan.append((v, True))
            anak = list(v._prev)
            rng.shuffle(anak)
            tumpukan.extend((a, False) for a in anak)
    akar.grad = 1.0
    for v in reversed(urutan):
        v._backward()


def ujiB():
    print(GARIS, "\nUJI B  apakah 0.000e+00 itu dijamin atau kebetulan  (Soal 3a)\n",
          GARIS, sep="")

    asli = Value.backward

    for n_in, n_h, n_k, n_contoh in ((4, 3, 2, 2), (20, 12, 5, 4),
                                     (60, 40, 10, 8)):
        random.seed(0)
        m = MLP(n_in, [n_h, n_k])
        rng = np.random.default_rng(0)
        Xk = rng.normal(0, 1, (n_contoh, n_in))
        yk = list(rng.integers(0, n_k, n_contoh))
        rugi = S.rugi_batch_value(m, Xk, yk)      # satu graf, dipakai ulang

        lihat, tumpuk, simpul = set(), [rugi], []
        while tumpuk:
            v = tumpuk.pop()
            if id(v) not in lihat:
                lihat.add(id(v))
                simpul.append(v)
                tumpuk.extend(v._prev)

        def ambil(cara):
            for v in simpul:        # nolkan SELURUH graf, bukan cuma parameter
                v.grad = 0.0
            cara(rugi)
            return np.array([p.grad for p in m.parameters()])

        g_rek = ambil(lambda r: asli(r))
        print(f"\n  {n_in}-{n_h}-{n_k}, {n_contoh} contoh, "
              f"{len(m.parameters())} parameter, {len(simpul)} simpul")
        for nama, cara in (("iteratif + reversed", lambda r: iteratif(r, True)),
                           ("iteratif tanpa reversed", lambda r: iteratif(r, False)),
                           ("iteratif anak diacak", lambda r: acak_urut(r, 7))):
            g = ambil(cara)
            print(f"    {nama:<26} selisih {np.abs(g_rek - g).max():.3e}   "
                  f"beda bit {int((g_rek != g).sum()):>4} dari {len(g_rek)}")

    print("""
  Jawaban 3a benar, dan alasannya tepat sasaran.

  Perhatikan baris pertama tiap kelompok: dengan reversed(), selisihnya nol
  tepat di ketiga ukuran. Tanpa reversed(), urutan topologisnya tetap sah dan
  gradiennya tetap benar secara matematis, tapi penjumlahan titik-mengambang
  dikerjakan dengan urutan berbeda dan bit terakhirnya bergeser. Di jaringan
  terbesar, lebih dari separuh parameter berbeda bit. Cacah persisnya berubah
  tiap kali dijalankan, karena urutan iterasi set bergantung pada alamat objek
  dan alamat itu tidak sama antar proses.

  Jadi yang menjamin nol bukan "iteratif lawan rekursif", melainkan urutan
  topologis yang persis sama. reversed() yang menyamakannya, dan tanpa baris
  itu jawaban 3a jadi salah.

  Perhatikan juga jaringan 4-3-2: ketiga cara memberi nol. Grafnya terlalu
  kecil untuk membedakan apa pun. Itu ukuran yang dipakai Bagian 3 di berkas
  sesi waktu pertama ditulis, jadi uji di sana tidak bisa membuktikan
  klaimnya sendiri. Sudah diperbesar.
""")


# ══════════════════════════════════════════════════════════════
# UJI C  overfit atau lr kebesaran
# ══════════════════════════════════════════════════════════════

def ujiC(X, y, Xv, yv):
    print(GARIS, "\nUJI C  epoch 7 memburuk. overfit, atau lr kebesaran?  (Soal 6a)\n",
          GARIS, sep="")

    rng = np.random.default_rng(0)
    param = [S.Tensor(rng.normal(0, 1, (784, 128)) * (2 / 784) ** 0.5),
             S.Tensor(np.zeros(128)),
             S.Tensor(rng.normal(0, 1, (128, 10)) * (2 / 128) ** 0.5),
             S.Tensor(np.zeros(10))]

    print(f"  {'epoch':>6}{'akurasi latih':>16}{'akurasi validasi':>19}")
    print("  " + "-" * 42)
    for e in range(8):
        urut = rng.permutation(len(y))
        for i in range(0, len(urut), 64):
            k = urut[i:i + 64]
            rugi = S.maju(param, X[k]).entropi_silang(y[k])
            for p in param:
                p.grad = np.zeros_like(p.data)
            rugi.backward()
            for p in param:
                p.data -= 0.1 * p.grad
        print(f"  {e:>6}{S.akurasi(param, X, y) * 100:>15.2f}%"
              f"{S.akurasi(param, Xv, yv) * 100:>18.2f}%")

    print("""
  Jawaban 6a salah, dan ini satu-satunya yang salah.

  Overfitting punya tanda tangan yang khas: akurasi latih terus naik sementara
  validasi mulai turun. Yang terjadi di sini bukan itu. Akurasi latih ikut
  jatuh, dari 98,10 ke 97,11, di epoch yang sama waktu validasi jatuh dari
  97,32 ke 96,37. Keduanya turun bersama.

  Model yang overfit tidak melupakan data latihnya. Yang terjadi: laju belajar
  0,1 tetap sampai akhir, dan langkah terakhir mendarat di tempat yang lebih
  buruk untuk kedua himpunan sekaligus. Itu derau SGD, bukan hafalan.

  Cara memisahkan keduanya di masa depan sederhana: selalu catat akurasi
  latih di samping validasi. Tanpa kolom itu, kedua sebab kelihatan sama.
""")


# ══════════════════════════════════════════════════════════════
# UJI D  di batch berapa GPU menang
# ══════════════════════════════════════════════════════════════

def ujiD(X, y):
    print(GARIS, "\nUJI D  di batch berapa GPU menang, tiga ulangan  (Soal 5c)\n",
          GARIS, sep="")

    try:
        import torch
        import torch.nn as nn
    except ImportError:
        print("  torch tidak ada, uji ini dilewati")
        return

    def epoch_numpy(batch):
        rng = np.random.default_rng(0)
        p = [S.Tensor(rng.normal(0, 1, (784, 128)) * (2 / 784) ** 0.5),
             S.Tensor(np.zeros(128)),
             S.Tensor(rng.normal(0, 1, (128, 10)) * (2 / 128) ** 0.5),
             S.Tensor(np.zeros(10))]
        urut = rng.permutation(len(y))
        t0 = time.perf_counter()
        for i in range(0, len(urut), batch):
            k = urut[i:i + batch]
            rugi = S.maju(p, X[k]).entropi_silang(y[k])
            for q in p:
                q.grad = np.zeros_like(q.data)
            rugi.backward()
            for q in p:
                q.data -= 0.1 * q.grad
        return time.perf_counter() - t0

    Xt = torch.tensor(X, dtype=torch.float32)
    yt = torch.tensor(y)

    def epoch_torch(batch, alat):
        torch.manual_seed(0)
        jar = nn.Sequential(nn.Linear(784, 128), nn.ReLU(),
                            nn.Linear(128, 10)).to(alat)
        opt = torch.optim.SGD(jar.parameters(), lr=0.1)
        fn = nn.CrossEntropyLoss()
        Xa, ya = Xt.to(alat), yt.to(alat)
        urut = torch.randperm(len(ya), device=alat)
        if alat == "cuda":
            torch.cuda.synchronize()
        t0 = time.perf_counter()
        for i in range(0, len(urut), batch):
            k = urut[i:i + batch]
            opt.zero_grad()
            fn(jar(Xa[k]), ya[k]).backward()
            opt.step()
        if alat == "cuda":
            torch.cuda.synchronize()
        return time.perf_counter() - t0

    ada_gpu = torch.cuda.is_available()
    kolom = [("numpy f64", None), ("torch CPU", "cpu")]
    if ada_gpu:
        kolom.append(("torch GPU", "cuda"))

    print(f"  {'batch':>6}" + "".join(f"{n:>22}" for n, _ in kolom))
    print("  " + "-" * (6 + 22 * len(kolom)))
    for batch in (64, 128, 256, 512, 1024):
        baris = f"  {batch:>6}"
        for _, alat in kolom:
            def sekali(b=batch, a=alat):
                return epoch_numpy(b) if a is None else epoch_torch(b, a)
            sekali()                                   # pemanasan
            w = sorted(sekali() for _ in range(3))
            baris += f"{w[0]:.3f}/{w[1]:.3f}/{w[2]:.3f}".rjust(22)
        print(baris)

    print("""
  format tiap sel: tercepat / tengah / terlambat dari tiga ulangan.

  Jawaban 5c benar. Titik baliknya batch 256, dan sesudah itu GPU menang
  makin jauh: di batch 1024 ia hampir tiga kali lebih cepat dari CPU.

  Satu catatan cara mengukur. Angka yang kamu laporkan punya enam angka di
  belakang koma tapi berasal dari satu kali jalan. Kolom di atas menunjukkan
  ulangan ketiga bisa 15 persen lebih lambat dari yang pertama, jadi angka
  keenam itu tidak berarti apa-apa. Ini keluhan yang sama dengan waktu epoch
  di Bagian 5, dan sekarang giliranmu yang kena.
""")


# ══════════════════════════════════════════════════════════════
# UJI E  lanskap kuartik
# ══════════════════════════════════════════════════════════════

def rugi_grad_kuartik(th):
    x, y = th
    return x ** 4 / 4 + y ** 2 / 2, np.array([x ** 3, y])


def ujiE():
    print(GARIS, "\nUJI E  lanskap kuartik, momentum lawan RMSprop  (Soal 7d)\n",
          GARIS, sep="")

    def jalankan(aturan, lr, n_iter=1000, th0=(100.0, 100.0)):
        th = np.array(th0, dtype=float)
        keadaan, jejak = {}, [th.copy()]
        with np.errstate(over="ignore", invalid="ignore"):
            for _ in range(n_iter):
                _, g = rugi_grad_kuartik(th)
                if not np.all(np.isfinite(g)):
                    break
                langkah, keadaan = aturan(g, keadaan, lr)
                th = th + langkah
                if not np.all(np.isfinite(th)):
                    break
                jejak.append(th.copy())
        return np.array(jejak)

    print("  L(x, y) = x^4/4 + y^2/2, mulai dari (100, 100)")
    print(f"  kurvatur sumbu x di titik awal : 3 * 100^2 = {3 * 100 ** 2}")
    print("  kurvatur sumbu y              : 1 di mana pun\n")
    print(f"  {'optimizer':<12}{'lr terbaik':>14}{'rugi akhir':>14}"
          f"{'iterasi ke rugi 1':>20}")
    print("  " + "-" * 60)

    for nama, fn in (("SGD polos", S.sgd), ("momentum", S.momentum),
                     ("RMSprop", S.rmsprop), ("Adam", S.adam)):
        terbaik = None
        with np.errstate(over="ignore", invalid="ignore"):
            for lr in np.logspace(-8, 1, 60):
                jejak = jalankan(fn, lr)
                r = rugi_grad_kuartik(jejak[-1])[0]
                if np.isfinite(r) and (terbaik is None or r < terbaik[1]):
                    terbaik = (lr, r, jejak)
        lr, r, jejak = terbaik
        tiba = next((i for i, t in enumerate(jejak)
                     if rugi_grad_kuartik(t)[0] <= 1.0), None)
        print(f"  {nama:<12}{lr:>14.6g}{r:>14.6g}"
              f"{(tiba if tiba is not None else 'tidak pernah'):>20}")

    print("""
  Jawaban 7d benar. Lanskap yang kamu pilih memang membalik urutannya, dan
  alasan yang kamu tulis tepat.

  Kurvatur sumbu x bergerak dari 30000 di titik awal menuju nol di dasar.
  Satu laju belajar global harus cukup kecil untuk selamat di awal, dan
  sesudah itu ia terlalu kecil untuk sisanya. Momentum tidak menolong, karena
  yang dikumpulkannya kecepatan, bukan skala. RMSprop membagi tiap sumbu
  dengan akar rata-rata kuadrat gradiennya sendiri, jadi laju efektifnya ikut
  membesar waktu gradiennya mengecil.

  Angka pastinya beda tipis dengan punyamu karena kisi sapuannya beda, tapi
  kesimpulannya sama: RMSprop tiba, momentum tidak pernah.

  Baris Adam jangan dibaca sebagai hasil akhir. Laju belajar terbaiknya jatuh
  tepat di ujung atas sapuan, artinya sapuan ini belum melingkupinya. Kalau
  mau menyimpulkan sesuatu tentang Adam di lanskap ini, lebarkan dulu.
""")


if __name__ == "__main__":
    X, y, Xv, yv, Xu, yu = S.muat_mnist()
    ujiA()
    ujiB()
    ujiC(X, y, Xv, yv)
    ujiD(X, y)
    ujiE()
