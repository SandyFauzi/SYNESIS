"""Bukti terukur untuk kunci Bulan 1 Sesi 2.

Jalankan:
    . .\\scripts\\activate.ps1
    python notebooks\\kunci_b1s2_bukti.py

Berkas ini tidak mengajarkan apa pun. Ia cuma mengukur, supaya tiap kalimat
di `kunci-bulan1-sesi2.md` punya angka yang bisa kamu ulang sendiri.

Enam pengujian:
  1  ragam bobot uniform lawan gauss             -> Soal 2d
  2  akibat ragam yang salah kalau ditumpuk      -> Soal 2d
  3  bobot nol: satu neuron efektif atau nol     -> Soal 1
  4  relu di lapisan terakhir                    -> Soal 3d
  5  cacah sudut di batas keputusan              -> Soal 7b, 7c
  6  ongkos dan kedalaman MNIST sungguhan        -> Soal 8

Waktu jalan sekitar tiga menit. Yang paling lama Uji 6, karena satu gambar
MNIST lewat mesin Value memang selambat itu, dan itu justru intinya.
"""

import random
import sys
import time
from collections import Counter
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt   # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))

from bulan1_sesi1_autograd import Value                        # noqa: E402
from bulan1_sesi2_mlp import MLP, cincin, latih, rugi_engsel    # noqa: E402

GARIS = "=" * 66


# ══════════════════════════════════════════════════════════════
# UJI 1  ragam bobot: uniform lawan gauss
# ══════════════════════════════════════════════════════════════

def uji1():
    print(GARIS, "\nUJI 1  ragam bobot: uniform lawan gauss  (Soal 2d)\n",
          GARIS, sep="")

    n = 50
    rng = np.random.default_rng(0)

    resep = {
        "uniform(-1,1) * sqrt(2/n)  <- yang kamu pakai":
            rng.uniform(-1, 1, (200, n)) * (2.0 / n) ** 0.5,
        "gauss(0,1)    * sqrt(2/n)  <- He gauss       ":
            rng.normal(0, 1, (200, n)) * (2.0 / n) ** 0.5,
        "gauss(0,1)    * sqrt(1/n)                    ":
            rng.normal(0, 1, (200, n)) * (1.0 / n) ** 0.5,
        "uniform(-1,1) * sqrt(6/n)  <- He uniform     ":
            rng.uniform(-1, 1, (200, n)) * (6.0 / n) ** 0.5,
    }
    x = rng.normal(0, 1, (4000, n))          # masukan ragam 1

    print(f"  {'resep':<47}{'ragam w':>10}{'ragam z':>10}{'E[a^2]':>9}")
    print("  " + "-" * 74)
    for nama, W in resep.items():
        z = x @ W.T
        a = np.maximum(z, 0)
        print(f"  {nama:<47}{W.var():>10.5f}{z.var():>10.4f}{(a ** 2).mean():>9.4f}")

    print(f"""
  Yang diincar He: ragam w = 2/n = {2 / n:.5f}, ragam z = 2, E[a^2] = 1.

  Ragam uniform(-1,1) bukan 1, tapi (b-a)^2/12 = 1/3. Jadi mengalikannya
  dengan sqrt(2/n) memberi ragam 2/(3n), tiga kali lebih kecil dari yang
  diturunkan di Soal 2b dan 2c.

  Kalau mau tetap memakai uniform, batasnya sqrt(6/n), bukan sqrt(2/n).
  Baris terakhir tabel membuktikannya: ragam w dan E[a^2] persis kena target.
""")


# ══════════════════════════════════════════════════════════════
# UJI 2  akibatnya kalau ditumpuk
# ══════════════════════════════════════════════════════════════

def uji2():
    print(GARIS, "\nUJI 2  akibat ragam yang salah, 10 lapis 50 neuron  (Soal 2d)\n",
          GARIS, sep="")

    def rambat(faktor, sebar, lapis=10, n=50, seed=1):
        r = np.random.default_rng(seed)
        a = r.normal(0, 1, (2000, n))
        keluar = []
        for _ in range(lapis):
            W = (r.uniform(-1, 1, (n, n)) if sebar == "uniform"
                 else r.normal(0, 1, (n, n))) * faktor
            a = np.maximum(a @ W.T, 0)
            keluar.append(a.std())
        return keluar

    baris = {
        "uniform * sqrt(2/n)": rambat((2 / 50) ** 0.5, "uniform"),
        "gauss   * sqrt(2/n)": rambat((2 / 50) ** 0.5, "gauss"),
        "gauss   * sqrt(1/n)": rambat((1 / 50) ** 0.5, "gauss"),
    }
    kolom = (0, 2, 4, 6, 9)
    print(f"  {'lapis ke':<21}" + "".join(f"{i + 1:>10}" for i in kolom))
    print("  " + "-" * 71)
    for nama, v in baris.items():
        print(f"  {nama:<21}" + "".join(f"{v[i]:>10.2e}" for i in kolom))

    print("""
  Angkanya simpangan baku aktivasi di lapis itu.

  Baris kedua bertahan di sekitar 1 sampai lapis kesepuluh. Itu yang dimaksud
  "inisialisasi yang benar": sinyalnya tidak mengecil dan tidak meledak.

  Baris pertama, yang dipakai di berkas jawabanmu, jatuh ke 1e-03. Perhatikan
  bahwa ia jatuh lebih cepat daripada baris ketiga, yaitu resep 1/n yang kamu
  sendiri kritik di jawaban 2d. Jadi kritikmu benar, dan kodemu kena kritik
  itu lebih keras daripada sasarannya.

  Di jaringan 2 lapis seperti Sesi 2, ini tidak terlihat. Di Sesi 3 dan
  seterusnya, terlihat.
""")


# ══════════════════════════════════════════════════════════════
# UJI 3  bobot nol
# ══════════════════════════════════════════════════════════════

def uji3(X, y):
    print(GARIS, "\nUJI 3  bobot nol: satu neuron efektif, atau nol?  (Soal 1)\n",
          GARIS, sep="")

    def paksa(m, nilai):
        for nrn in m.lapisan[0].neuron:
            for w in nrn.w:
                w.data = nilai
            nrn.b.data = 0.0

    for nilai, label in (
        (0.0, "bobot lapisan tersembunyi = 0 semua"),
        (0.5, "bobot lapisan tersembunyi = 0.5 semua (seragam, tapi tak nol)"),
    ):
        random.seed(1)
        m = MLP(2, [8, 1])
        paksa(m, nilai)
        rugi, _ = rugi_engsel(m, X, y)
        m.nolkan()
        rugi.backward()
        g = [abs(w.grad) for nrn in m.lapisan[0].neuron for w in nrn.w]

        riw = latih(m, X, y, lr=0.15, n_iter=200, kabar=0)
        w0 = [nrn.w[0].data for nrn in m.lapisan[0].neuron]

        print(f"\n  {label}")
        print(f"    |grad| terbesar di lapisan tersembunyi : {max(g):.3e}")
        print(f"    akurasi setelah 200 iterasi           : {riw[-1][1] * 100:.1f} persen")
        print(f"    w[0] tiap neuron sesudah latih        : "
              f"{min(w0):.4f} .. {max(w0):.4f}   (rentang {max(w0) - min(w0):.4f})")

    print("""
  Baris pertama: gradiennya bukan kecil, tapi nol tepat. Sebabnya relu.
  Kalau semua bobot dan geseran nol, pra-aktivasi tiap neuron nol, dan
  turunan relu di nol dipilih 0 di mesinmu. Tidak ada gradien yang mengalir
  balik, jadi bobotnya tidak pernah bergerak, satu iterasi pun.

  Jadi bukan 1 neuron efektif. Nol. Lapisannya mati sejak sebelum dilatih,
  dan matinya sama persis dengan kematian di lr = 8 pada Bagian 5B.

  Baris kedua: bobot seragam tapi tak nol, lapisan sesudahnya acak. Gradien
  tiap neuron langsung berbeda, dan setelah 200 iterasi bobotnya sudah
  menyebar sejauh 0.24. Simetrinya patah sendiri.

  Artinya cerita "8 kloningan selamanya" cuma berlaku kalau SELURUH jaringan
  seragam, bukan satu lapisan saja. Petunjuk yang saya tulis di soal terlalu
  ringkas soal ini, dan itu kesalahan saya.
""")


# ══════════════════════════════════════════════════════════════
# UJI 4  relu di lapisan terakhir
# ══════════════════════════════════════════════════════════════

def uji4(X, y):
    print(GARIS, "\nUJI 4  relu dipasang di lapisan terakhir  (Soal 3d)\n",
          GARIS, sep="")

    random.seed(1)
    m = MLP(2, [8, 1])
    for nrn in m.lapisan[-1].neuron:
        nrn.tekuk = True
    riw = latih(m, X, y, lr=0.15, n_iter=200, kabar=0)
    ram = [m([Value(a), Value(b)]).data for a, b in X]
    nol = sum(1 for r in ram if r == 0.0)

    print(f"  akurasi                       : {riw[-1][1] * 100:.1f} persen")
    print(f"  rugi                          : {riw[-1][0]:.4f}")
    print(f"  ramalan terkecil              : {min(ram):.4f}")
    print(f"  ramalan negatif               : {sum(1 for r in ram if r < 0)} dari {len(ram)}")
    print(f"  ramalan tepat nol             : {nol} dari {len(ram)}")

    print("""
  Bagian pertama tebakanmu benar: keluaran negatif jadi mustahil, dan untuk
  titik berkelas -1 rugi engsel tidak pernah bisa turun di bawah 1.

  Bagian kedua meleset. Akurasinya tidak terkunci di 50 persen. Alasannya ada
  di baris `(s.data > 0) == (yi > 0)` di dalam `latih`: ramalan tepat nol
  dihitung sebagai kelas -1. Jadi model masih bisa membedakan dua kelas,
  lewat "nol lawan positif" dan bukan lewat "negatif lawan positif".

  Yang hilang bukan kemampuan memisahkan, tapi margin. Model tidak bisa lagi
  menyatakan seberapa yakin ia pada kelas negatif, dan gradien di seluruh
  daerah nol itu ikut mati.
""")


# ══════════════════════════════════════════════════════════════
# UJI 5  cacah sudut di batas keputusan
# ══════════════════════════════════════════════════════════════

def uji5(X, y):
    print(GARIS, "\nUJI 5  cacah sudut di batas keputusan  (Soal 7b, 7c)\n",
          GARIS, sep="")

    def analisa(h, kisi, seed=1, n_iter=200):
        random.seed(seed)
        m = MLP(2, [h, 1])
        latih(m, X, y, lr=0.15, n_iter=n_iter, kabar=0)
        W = np.array([[w.data for w in nrn.w] for nrn in m.lapisan[0].neuron])
        b = np.array([nrn.b.data for nrn in m.lapisan[0].neuron])
        v = np.array([w.data for w in m.lapisan[1].neuron[0].w])
        c = m.lapisan[1].neuron[0].b.data

        gx = np.linspace(X[:, 0].min() - .5, X[:, 0].max() + .5, kisi)
        gy = np.linspace(X[:, 1].min() - .5, X[:, 1].max() + .5, kisi)
        GX, GY = np.meshgrid(gx, gy)
        P = np.stack([GX.ravel(), GY.ravel()], 1)
        Z = (np.maximum(P @ W.T + b, 0) @ v + c).reshape(GY.shape)

        fig, ax = plt.subplots()
        cs = ax.contour(GX, GY, Z, levels=[0.0])
        try:
            jalur = cs.get_paths()
        except AttributeError:                     # matplotlib lama
            jalur = [p for k in cs.collections for p in k.get_paths()]
        plt.close(fig)

        per_neuron = Counter()
        for p in jalur:
            pola = (p.vertices @ W.T + b) > 0
            for i in range(1, len(pola)):
                for j in np.nonzero(pola[i] != pola[i - 1])[0]:
                    per_neuron[int(j)] += 1
        return per_neuron, len(jalur)

    print(f"  {'neuron':>7}{'kisi':>7}{'sudut':>8}{'ikut melipat':>15}"
          f"{'potongan':>10}{'seberang/neuron':>18}")
    print("  " + "-" * 73)
    for h in (8, 32):
        for kisi in (200, 400, 800, 1600):
            pn, nj = analisa(h, kisi)
            sebar = dict(sorted(Counter(pn.values()).items()))
            print(f"  {h:>7}{kisi:>7}{sum(pn.values()):>8}"
                  f"{f'{len(pn)} dari {h}':>15}{nj:>10}{str(sebar):>18}")

    print("""
  Tebakan "kurang dari 8" meleset ke arah yang berlawanan. Sudutnya 16, dua
  kali jumlah neuron, dan angkanya tidak berubah walau kisi dinaikkan delapan
  kali lipat. Jadi itu bukan artefak resolusi.

  Sebabnya geometri, dan sekali dilihat tidak bisa dilupakan. Tiap neuron
  menyumbang satu garis lipat lurus di bidang. Batas keputusannya satu kurva
  tertutup yang mengurung cincin dalam. Sebuah garis lurus yang memotong
  kurva tertutup harus masuk sekali dan keluar sekali. Dua penyeberangan,
  dua sudut, per neuron. Kolom terakhir menunjukkan tiap neuron kena persis 2.

  Untuk 32 neuron: 62 sudut, dan 31 dari 32 neuron ikut. Yang satu itu garis
  lipatnya lewat di luar kurva, jadi ia tidak menyumbang sudut sama sekali.
  Di situlah "kenapa bisa kurang" yang ditanyakan 7b, cuma tempatnya bukan di
  model 8 neuron melainkan di model 32.

  Ramalanmu untuk 7c, poligon bersisi 32, jadi meleset dua kali: sisinya 62,
  dan bukan 32.
""")


# ══════════════════════════════════════════════════════════════
# UJI 6  ongkos dan kedalaman MNIST
# ══════════════════════════════════════════════════════════════

def uji6():
    print(GARIS, "\nUJI 6  ongkos dan kedalaman MNIST sungguhan  (Soal 8)\n",
          GARIS, sep="")

    def ukur(n_in, n_hid, n_out, ulang=3):
        cacah = {"n": 0}
        asli = Value.__init__

        def hitung(self, data, _anak=(), _op=""):
            cacah["n"] += 1
            asli(self, data, _anak, _op)

        Value.__init__ = hitung
        waktu = []
        try:
            random.seed(0)
            m = MLP(n_in, [n_hid, n_out])
            gambar = [Value(random.random()) for _ in range(n_in)]
            for _ in range(ulang):
                cacah["n"] = 0
                t0 = time.perf_counter()
                keluar = m(gambar)
                rugi = sum(k * k for k in keluar)
                m.nolkan()
                rugi.backward()
                waktu.append(time.perf_counter() - t0)
            return cacah["n"], waktu, None
        except RecursionError as e:
            return cacah["n"], waktu, f"{type(e).__name__}: {e}"
        finally:
            Value.__init__ = asli

    print(f"  batas rekursi mesin ini : {sys.getrecursionlimit()}\n")
    for arsi in ((784, 32, 10), (784, 256, 10)):
        n_val, waktu, salah = ukur(*arsi)
        nama = "-".join(map(str, arsi))
        dalam = arsi[0] + arsi[1]
        if salah:
            print(f"  {nama:<12} PECAH   {salah}")
            print(f"  {'':<12} kedalaman kira-kira {dalam} > {sys.getrecursionlimit()}")
        else:
            ms = sorted(t * 1000 for t in waktu)
            jam = [t * 60000 / 3600 for t in sorted(waktu)]
            print(f"  {nama:<12} {format(n_val, ',').replace(',', '.'):>7} Value per gambar")
            print(f"  {'':<12} {len(ms)} ukuran : "
                  + ", ".join(f"{t:.0f} ms" for t in ms))
            print(f"  {'':<12} satu epoch 60000 gambar = "
                  f"{jam[0]:.1f} sampai {jam[-1]:.1f} jam")
            print(f"  {'':<12} kedalaman kira-kira {dalam} < {sys.getrecursionlimit()}, aman")

    print("""
  Dua dinding itu nyata, dan letaknya persis seperti hitunganmu di 8b dan 8c.

  Yang meleset besarannya. Ramalanmu 29 hari per epoch datang dari menganggap
  49 ms itu ongkos satu gambar. Padahal 49 ms itu satu iterasi penuh atas 120
  titik, jadi ongkos satu titik sekitar 0.4 ms. Selisihnya 120 kali lipat.

  Perhatikan juga sebaran tiga ukuran di atas. Selisih antar ukuran bisa
  hampir dua kali lipat, karena mesin Value bergantung pada alokasi objek
  Python dan pemungut sampah, bukan pada aritmetika. Melaporkan satu angka
  tunggal untuk ongkos seperti ini menyesatkan.

  Berjam-jam per epoch tetap tidak bisa dipakai. Kesimpulanmu selamat, yang
  perlu diperbaiki cuma cara membaca angkanya.
""")


if __name__ == "__main__":
    X, y = cincin()
    uji1()
    uji2()
    uji3(X, y)
    uji4(X, y)
    uji5(X, y)
    uji6()
