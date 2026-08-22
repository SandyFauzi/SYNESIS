"""Bulan 1 Sesi 2 - Neuron, Layer, MLP di atas mesin buatanmu.

Jalankan:
    . .\\scripts\\activate.ps1
    python notebooks\\bulan1_sesi2_mlp.py

Sesi 1 kamu menulis mesin yang bisa menurunkan ekspresi apa pun. Malam ini
mesin itu dipakai untuk sesuatu yang bentuknya bukan rumus, tapi jaringan.

Tidak ada satu pun `import torch` di berkas ini. Semua gradien yang mengalir
di sini keluar dari kelas `Value` yang kamu tulis sendiri.

Satu hal yang berubah dan akibatnya berantai: mulai sekarang permukaan loss
berhenti jadi mangkuk tunggal. Titik awal yang berbeda mendarat di tempat yang
berbeda, dan itu bukan bug.

Bagian bertanda TODO kamu yang isi.
"""

import random
import time
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from bulan1_sesi1_autograd import Value  # noqa: E402

GARIS = "=" * 62
FIGUR = Path(__file__).resolve().parent.parent / "figures"
FIGUR.mkdir(exist_ok=True)


# ══════════════════════════════════════════════════════════════
# Data: dua cincin sepusat
# ══════════════════════════════════════════════════════════════

def cincin(n=120, derau=0.14, seed=3):
    """Satu kelompok di cincin dalam, satu di cincin luar.

    Bentuk ini dipilih karena membuat pertanyaannya tidak bisa diperdebatkan.
    Untuk dua bulan sabit, garis lurus masih bisa dapat sekitar 87 persen dan
    kamu bisa berargumen itu lumayan. Untuk dua cincin sepusat, garis lurus
    mentok di sekitar 65 persen, dan tidak ada sudut kemiringan mana pun yang
    menolongnya.

    Kenapa mustahil, itu Soal 4, dan buktinya satu paragraf.
    """
    rng = np.random.default_rng(seed)
    m = n // 2
    t_dalam = rng.uniform(0, 2 * np.pi, m)
    r_dalam = 0.8 + rng.normal(0, derau, m)
    t_luar = rng.uniform(0, 2 * np.pi, n - m)
    r_luar = 2.0 + rng.normal(0, derau, n - m)
    X = np.concatenate([
        np.stack([r_dalam * np.cos(t_dalam), r_dalam * np.sin(t_dalam)], 1),
        np.stack([r_luar * np.cos(t_luar), r_luar * np.sin(t_luar)], 1),
    ])
    y = np.concatenate([-np.ones(m), np.ones(n - m)])   # label -1 dan +1
    p = rng.permutation(n)
    return X[p], y[p]


# ══════════════════════════════════════════════════════════════
# BAGIAN 1 - satu neuron
# ══════════════════════════════════════════════════════════════

class Neuron:
    """Satu neuron. Isinya cuma dua hal: garis, lalu tekukan.

        keluaran = relu(w . x + b)

    Itu saja. Tidak ada yang lain. Seluruh kehebatan jaringan saraf datang
    dari menumpuk benda sesederhana ini, bukan dari kerumitan satuannya.
    """

    def __init__(self, n_masuk, tekuk=True):
        """Siapkan bobot dan geseran sebagai Value.

        Bobot diacak, geseran dimulai dari nol. Kenapa bobotnya tidak boleh
        nol semua adalah Soal 1, dan jawabannya menentukan apakah jaringanmu
        bisa belajar sama sekali.

        Skala acaknya pakai sqrt(2 / n_masuk). Namanya inisialisasi He, dan
        Soal 2 menanyakan dari mana angka itu datang.

        Simpan:
            self.w      daftar Value sepanjang n_masuk
            self.b      satu Value bernilai 0.0
            self.tekuk  bool, apakah relu dipasang di ujung

        TODO 1a
        """
        self.w = [Value(random.gauss(0.0, 1.0) * (2 / n_masuk)**0.5) for _ in range(n_masuk)]
        self.b = Value(0.0)
        self.tekuk = tekuk

    def __call__(self, x):
        """Hitung keluaran untuk satu contoh.

        `x` adalah daftar Value atau daftar angka biasa, panjangnya n_masuk.

        Langkahnya:
            1. jumlahkan wi * xi untuk semua i, mulai dari self.b
            2. kalau self.tekuk, kembalikan hasil.relu()
            3. kalau tidak, kembalikan hasilnya apa adanya

        Lapisan terakhir biasanya tanpa tekukan. Soal 3 menanyakan kenapa.

        TODO 1b
        """
        pra = sum((wi * xi for wi, xi in zip(self.w, x)), self.b)
        return pra.relu() if self.tekuk else pra

    def parameters(self):
        return self.w + [self.b]

    def __repr__(self):
        jenis = "relu" if self.tekuk else "linear"
        return f"Neuron({jenis}, {len(self.w)} masukan)"


def bagian1():
    print(GARIS, "\nBAGIAN 1  satu neuron itu garis plus tekukan\n",
          GARIS, sep="")

    random.seed(0)
    n = Neuron(2)
    n.w[0].data, n.w[1].data, n.b.data = 1.0, -1.0, 0.5

    print("  w = [1, -1], b = 0.5, jadi pra-aktivasi = x0 - x1 + 0.5\n")
    print(f"  {'x0':>6}{'x1':>6}{'pra-aktivasi':>15}{'relu':>8}")
    print("  " + "-" * 36)
    for x0, x1 in [(0, 0), (1, 0), (0, 1), (2, 0), (0, 2)]:
        pra = x0 - x1 + 0.5
        keluar = n([Value(float(x0)), Value(float(x1))])
        print(f"  {x0:>6}{x1:>6}{pra:>15.2f}{keluar.data:>8.2f}")

    print("""
  Kolom terakhir sama dengan kolom ketiga, kecuali yang negatif jadi nol.

  Garis x0 - x1 + 0.5 = 0 membelah bidang jadi dua. Di satu sisi neuron
  meneruskan nilainya, di sisi lain ia diam. Satu neuron menyumbang satu
  lipatan, dan lipatannya lurus.

  Melengkungkan batas keputusan bukan pekerjaan satu neuron. Itu pekerjaan
  banyak lipatan lurus yang disusun.""")


# ══════════════════════════════════════════════════════════════
# BAGIAN 2 - lapisan dan jaringan
# ══════════════════════════════════════════════════════════════

class Layer:
    """Sekumpulan neuron yang menerima masukan yang sama.

    Tidak ada yang baru di sini. Ini cuma daftar Neuron dengan pemanggilan
    yang dirapikan.
    """

    def __init__(self, n_masuk, n_keluar, tekuk=True):
        """Buat n_keluar neuron, masing-masing menerima n_masuk masukan.

        TODO 2a
        """
        self.neuron = [Neuron(n_masuk, tekuk) for _ in range(n_keluar)]

    def __call__(self, x):
        """Kembalikan daftar keluaran. Kalau cuma satu, kembalikan Value-nya
        langsung, bukan daftar berisi satu. Itu membuat lapisan terakhir enak
        dipakai.

        TODO 2b
        """
        out = [n(x) for n in self.neuron]
        return out[0] if len(out) == 1 else out

    def parameters(self):
        return [p for n in self.neuron for p in n.parameters()]


class MLP:
    """Rangkaian lapisan. Keluaran lapisan sebelumnya jadi masukan berikutnya."""

    def __init__(self, n_masuk, ukuran):
        """`ukuran` daftar lebar tiap lapisan, misalnya [8, 1].

        Lapisan terakhir dibuat tanpa tekukan, sisanya dengan tekukan.

        TODO 2c
        """
        sz = [n_masuk] + ukuran
        self.lapisan = [Layer(sz[i], sz[i+1], tekuk=(i != len(ukuran)-1)) for i in range(len(ukuran))]

    def __call__(self, x):
        """Lewatkan x melalui semua lapisan berurutan.

        TODO 2d
        """
        for layer in self.lapisan:
            x = layer(x)
        return x

    def parameters(self):
        return [p for l in self.lapisan for p in l.parameters()]

    def nolkan(self):
        """Nolkan semua gradien.

        Ini yang di Sesi D dikerjakan PyTorch lewat zero_(). Sekarang kamu
        yang memanggilnya, dan kalau lupa akibatnya persis sama: rekurensinya
        naik jadi orde dua dan modelmu berayun tanpa pernah mendarat.

        TODO 2e
        """
        for p in self.parameters():
            p.grad = 0.0

    def __repr__(self):
        return f"MLP({len(self.parameters())} parameter)"


def bagian2():
    print("\n" + GARIS, "\nBAGIAN 2  lapisan dan jaringan\n", GARIS, sep="")

    random.seed(1)
    m = MLP(2, [8, 1])
    print(f"  arsitektur : 2 -> 8 -> 1")
    print(f"  parameter  : {len(m.parameters())}")

    hitung = 2 * 8 + 8 + 8 * 1 + 1
    print(f"  hitung tangan : 2*8 + 8 + 8*1 + 1 = {hitung}")
    print(f"  cocok         : {len(m.parameters()) == hitung}")

    keluar = m([Value(0.5), Value(-0.3)])
    print(f"\n  keluaran untuk x = [0.5, -0.3] : {keluar.data:.6f}")
    print(f"  jenisnya                        : {type(keluar).__name__}")
    return m


# ══════════════════════════════════════════════════════════════
# BAGIAN 3 - gradien jaringan diadu dengan beda hingga
# ══════════════════════════════════════════════════════════════

def bagian3():
    print("\n" + GARIS, "\nBAGIAN 3  gradien jaringan lawan beda hingga\n",
          GARIS, sep="")

    random.seed(2)
    m = MLP(2, [4, 1])
    x = [Value(0.7), Value(-0.4)]

    m.nolkan()
    keluar = m(x)
    keluar.backward()
    analitik = [p.grad for p in m.parameters()]

    h = 1e-5
    numerik = []
    for p in m.parameters():
        asli = p.data
        p.data = asli + h
        maju = MLP.__call__(m, [Value(0.7), Value(-0.4)]).data
        p.data = asli - h
        mundur = MLP.__call__(m, [Value(0.7), Value(-0.4)]).data
        p.data = asli
        numerik.append((maju - mundur) / (2 * h))

    a = np.array(analitik)
    n = np.array(numerik)
    galat = np.abs(a - n).max() / max(1e-12, np.abs(n).max())

    print(f"  parameter diuji : {len(a)}")
    print(f"  galat relatif   : {galat:.3e}")
    print(f"  status          : {'lolos' if galat < 1e-5 else 'GAGAL'}")

    print("""
  Aturannya tidak berubah sejak Hari 1. Gradien tidak dipercaya sebelum diadu
  dengan beda hingga.

  Yang berubah: sekarang yang diuji bukan satu rumus, tapi 17 parameter yang
  gradiennya mengalir melalui jaringan bercabang. Kalau urutan topologis di
  Sesi 1 salah, atau kalau kamu memakai = alih-alih +=, baris ini yang akan
  menangkapnya.""")


# ══════════════════════════════════════════════════════════════
# BAGIAN 4 - latih pada dua bulan sabit
# ══════════════════════════════════════════════════════════════

def rugi_engsel(model, X, y, denda=1e-4):
    """Rugi engsel, plus denda L2 kecil.

        rugi = rata-rata( max(0, 1 - y * ramalan) ) + lam * sum(p^2)

    Kenapa engsel dan bukan entropi silang? Karena engsel cuma butuh relu
    dan perkalian, yang dua-duanya sudah ada di mesinmu. Entropi silang butuh
    exp dan log, yang belum kamu tulis. Menambahkannya adalah Soal 6.

    Disediakan, bukan TODO.
    """
    skor = [model([Value(float(a)), Value(float(b))]) for a, b in X]
    kerugian = [(1 + -yi * s).relu() for yi, s in zip(y, skor)]
    total = sum(kerugian, Value(0.0)) * (1.0 / len(kerugian))
    reg = sum((p * p for p in model.parameters()), Value(0.0)) * denda
    return total + reg, skor


def latih(model, X, y, lr=0.05, n_iter=120, kabar=20):
    """Gelung yang sama sejak Sesi A. Empat baris, tidak berubah.

    Disediakan, bukan TODO. Perhatikan `model.nolkan()` di dalamnya, dan
    ingat apa yang terjadi kalau baris itu hilang.
    """
    riwayat = []
    for i in range(n_iter):
        rugi, skor = rugi_engsel(model, X, y)
        benar = sum(1 for yi, s in zip(y, skor) if (s.data > 0) == (yi > 0))
        riwayat.append((rugi.data, benar / len(y)))

        model.nolkan()
        rugi.backward()

        laju = lr * (1 - 0.9 * i / n_iter)      # dikecilkan pelan-pelan
        for p in model.parameters():
            p.data -= laju * p.grad

        if kabar and (i % kabar == 0 or i == n_iter - 1):
            print(f"    iterasi {i:4d}   rugi {rugi.data:.4f}   "
                  f"akurasi {benar / len(y) * 100:5.1f} persen")
    return riwayat


def bagian4(X, y):
    print("\n" + GARIS, "\nBAGIAN 4  melatih di dua cincin sepusat\n",
          GARIS, sep="")

    print(f"  data : {len(y)} titik, cincin dalam lawan cincin luar\n")

    print("  Model tanpa lapisan tersembunyi, jadi cuma satu garis lurus:")
    random.seed(1)
    lurus = MLP(2, [1])
    t0 = time.perf_counter()
    riw_lurus = latih(lurus, X, y, lr=0.15, n_iter=120, kabar=60)
    print(f"    waktu : {time.perf_counter() - t0:.1f} detik\n")

    print("  Model dengan 8 neuron tersembunyi:")
    random.seed(1)
    dalam = MLP(2, [8, 1])
    t0 = time.perf_counter()
    riw_dalam = latih(dalam, X, y, lr=0.15, n_iter=200, kabar=50)
    print(f"    waktu : {time.perf_counter() - t0:.1f} detik")

    print(f"""
  Akurasi akhir garis lurus : {riw_lurus[-1][1] * 100:.1f} persen
  Akurasi akhir 8 neuron    : {riw_dalam[-1][1] * 100:.1f} persen

  Selisih itu seluruhnya datang dari satu hal: relu. Tanpa tekukan, menumpuk
  berapa lapis pun tetap menghasilkan satu garis lurus, dan Soal 3 memintamu
  membuktikan itu di kertas dalam tiga baris.

  Perhatikan juga bahwa garis lurus tidak gagal karena kurang dilatih. Ia
  gagal karena tidak ada garis lurus yang bisa memisahkan lingkaran dalam
  dari lingkaran luar. Melatihnya seribu kali lebih lama tidak akan menolong.""")

    return dalam, riw_dalam


# ══════════════════════════════════════════════════════════════
# BAGIAN 5 - neuron mati, dan titik awal yang menentukan
# ══════════════════════════════════════════════════════════════

def hitung_mati(model, X):
    """Berapa neuron di lapisan pertama yang tidak pernah menyala."""
    lapis = model.lapisan[0]
    pernah = [False] * len(lapis.neuron)
    for a, b in X:
        xin = [Value(float(a)), Value(float(b))]
        for j, n in enumerate(lapis.neuron):
            if n(xin).data > 0:
                pernah[j] = True
    return sum(1 for p in pernah if not p), len(pernah)


def bagian5(X, y):
    print("\n" + GARIS, "\nBAGIAN 5  dua hal yang tidak ada di Bulan 0\n",
          GARIS, sep="")

    # ---------- A. titik awal menentukan ----------
    print("  A. Enam titik awal acak. Model 2-4-1, data sama persis.\n")
    print(f"  {'seed':>6}{'rugi akhir':>14}{'akurasi':>12}")
    print("  " + "-" * 34)

    akur = []
    for s in range(6):
        random.seed(s)
        m = MLP(2, [4, 1])
        riw = latih(m, X, y, lr=0.15, n_iter=150, kabar=0)
        akur.append(riw[-1][1])
        print(f"  {s:>6}{riw[-1][0]:>14.4f}{riw[-1][1] * 100:>11.1f}%")

    print(f"""
  Terbaik {max(akur) * 100:.1f} persen, terburuk {min(akur) * 100:.1f} persen.
  Yang berbeda cuma angka acak awalnya.

  Di Bulan 0 ini mustahil. Mangkuknya tunggal, jadi dari mana pun kamu mulai
  tiba di dasar yang sama. Sekarang permukaannya berbenjol, dan tiap titik
  awal jatuh ke lembah yang berbeda.

  Akibat praktisnya langsung: menjalankan sekali lalu melaporkan angkanya itu
  tidak jujur. Yang benar adalah menjalankan beberapa kali dan melaporkan
  sebarannya, persis seperti kamu melaporkan ralat pengukuran di praktikum.
""")

    # ---------- B. neuron mati ----------
    print("  B. Neuron mati. Model 2-8-1, seed tetap, cuma lr yang diubah.\n")
    print(f"  {'lr':>6}{'neuron mati':>14}{'akurasi':>12}")
    print("  " + "-" * 34)

    for lr in (0.15, 3.0, 8.0):
        random.seed(0)
        m = MLP(2, [8, 1])
        riw = latih(m, X, y, lr=lr, n_iter=80, kabar=0)
        mati, total = hitung_mati(m, X)
        print(f"  {lr:>6}{f'{mati} dari {total}':>14}{riw[-1][1] * 100:>11.1f}%")

    print("""
  Baris terakhir itu kematian massal.

  Langkah yang terlalu besar mendorong bobot sampai pra-aktivasi neuron
  negatif untuk SEMUA titik data. Setelah itu relu selalu mengeluarkan nol,
  gradiennya nol, dan bobotnya berhenti diperbarui selamanya. Neuron itu tidak
  akan hidup lagi, sekeras apa pun kamu melatihnya.

  Perhatikan bahwa di lr wajar tidak ada satu pun yang mati. Itu bukan
  kebetulan: inisialisasi sqrt(2/n_masuk) memang dirancang supaya pra-aktivasi
  tersebar di sekitar nol, jadi kira-kira separuh neuron menyala untuk tiap
  masukan. Soal 5 memintamu menurunkan dari mana angka 2 itu datang.""")

    return akur


# ══════════════════════════════════════════════════════════════
# BAGIAN 6 - batas keputusan, digambar
# ══════════════════════════════════════════════════════════════

def bagian6(model, X, y, riwayat):
    print("\n" + GARIS, "\nBAGIAN 6  batas keputusan\n", GARIS, sep="")

    gx = np.linspace(X[:, 0].min() - 0.5, X[:, 0].max() + 0.5, 46)
    gy = np.linspace(X[:, 1].min() - 0.5, X[:, 1].max() + 0.5, 42)
    Z = np.zeros((len(gy), len(gx)))
    for i, b in enumerate(gy):
        for j, a in enumerate(gx):
            Z[i, j] = model([Value(float(a)), Value(float(b))]).data

    fig, ax = plt.subplots(1, 2, figsize=(11, 4.5))
    ax[0].contourf(gx, gy, Z, levels=[-99, 0, 99], colors=["#FB923C", "#60A5FA"],
                   alpha=0.25)
    ax[0].contour(gx, gy, Z, levels=[0], colors=["#22C55E"], linewidths=2)
    ax[0].scatter(X[y < 0, 0], X[y < 0, 1], s=22, c="#FB923C", edgecolors="k",
                  linewidths=0.3)
    ax[0].scatter(X[y > 0, 0], X[y > 0, 1], s=22, c="#60A5FA", edgecolors="k",
                  linewidths=0.3)
    ax[0].set_title("Batas keputusan, disusun dari lipatan lurus")

    ax[1].plot([r[0] for r in riwayat], lw=2, color="#22C55E", label="rugi")
    ax[1].plot([r[1] for r in riwayat], lw=2, color="#60A5FA", label="akurasi")
    ax[1].set_xlabel("iterasi"); ax[1].legend(); ax[1].grid(alpha=0.3)
    ax[1].set_title("Selama latihan")

    plt.tight_layout()
    plt.savefig(FIGUR / "bulan1_sesi2_batas.png", dpi=110, bbox_inches="tight")
    plt.close()
    print("  plot disimpan : figures/bulan1_sesi2_batas.png")
    print("""
  Buka gambarnya. Batas hijaunya melengkung, tapi kalau kamu ikuti pelan-pelan
  ia tersusun dari potongan-potongan lurus yang bertemu di sudut.

  Itu bukan pendekatan kasar dari kurva mulus. Itu memang bentuk sebenarnya
  dari jaringan relu: fungsi linear sepotong-sepotong. Tidak ada lengkungan
  di mana pun, cuma banyak patahan yang dari jauh terlihat melengkung.""")


# ══════════════════════════════════════════════════════════════
# BAGIAN 7 - ongkosnya
# ══════════════════════════════════════════════════════════════

def bagian7(X):
    print("\n" + GARIS, "\nBAGIAN 7  ongkos satu objek per angka\n",
          GARIS, sep="")

    cacah = {"n": 0}
    asli = Value.__init__

    def hitung(self, data, _anak=(), _op=""):
        cacah["n"] += 1
        asli(self, data, _anak, _op)

    Value.__init__ = hitung
    random.seed(1)
    m = MLP(2, [8, 1])
    cacah["n"] = 0
    t0 = time.perf_counter()
    rugi, _ = rugi_engsel(m, X, np.ones(len(X)))
    m.nolkan()
    rugi.backward()
    detik = time.perf_counter() - t0
    per_iter = cacah["n"]
    Value.__init__ = asli

    print(f"  titik data                 : {len(X)}")
    print(f"  objek Value satu iterasi   : {per_iter:,}".replace(",", "."))
    print(f"  waktu satu iterasi         : {detik * 1000:.0f} ms")
    print(f"  ramalan untuk 1000 iterasi : {detik * 1000:.0f} detik")

    print(f"""
  Sekarang kalikan ke MNIST: 60000 gambar, 784 piksel, ratusan neuron.

  Angka di atas naik ribuan kali. Itu Sesi 3, dan di situ kamu akan menabrak
  dua dinding sekaligus: waktu, dan batas rekursi 996 yang sudah terukur di
  mesinmu.

  Jangan diperbaiki sekarang. Biarkan pecah dulu supaya kamu melihat sendiri
  bentuk kegagalannya.""")


if __name__ == "__main__":
    X, y = cincin()
    try:
        bagian1()
        bagian2()
        bagian3()
        model, riw = bagian4(X, y)
        bagian5(X, y)
        bagian6(model, X, y, riw)
        bagian7(X)
    except NotImplementedError as e:
        print(f"\n  {e} belum diisi. Kerjakan TODO dulu.")
