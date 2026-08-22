"""Bulan 1 Sesi 3+4 - MNIST, dua dinding, dan optimizer tulisan tangan.

Jalankan:
    . .\\scripts\\activate.ps1
    python notebooks\\bulan1_sesi34_mnist.py

Sesi 2 berhenti tepat di depan dua dinding yang sudah kamu hitung sendiri di
Soal 8: waktu, dan batas rekursi. Malam ini kamu menabrak keduanya sungguhan,
lalu menembusnya, lalu memakai yang tersisa untuk mengalahkan 95 persen di
MNIST.

Urutannya sengaja begini:

    1  entropi silang di atas Value        pakai exp dan log yang baru kamu tulis
    2  tabrak dinding waktu                784-32-10, diukur bukan ditebak
    3  tabrak dinding rekursi              784-256-10, pecah
    4  tembus dinding rekursi              backward iteratif
    5  tembus dinding waktu                Tensor numpy
    6  MNIST di atas 95 persen
    7  PyTorch, dan ukur rasionya
    8  momentum, RMSprop, Adam, tulis tangan

Bagian 8 menutup janji dari Soal 4e Sesi B, dan kamu sudah punya bahasanya
sejak Bukti 4 Sesi D: momentum itu osilator teredam.

Bagian bertanda TODO kamu yang isi.

Data MNIST dibaca dari E:\\SYNESIS\\data. Kalau belum ada, torchvision
mengunduhnya sekali (11 MB) lalu berkas ini menyimpan salinan npz supaya
jalan berikutnya tidak perlu jaringan.
"""

import math
import random
import sys
import time
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
from bulan1_sesi1_autograd import Value  # noqa: E402
from bulan1_sesi2_mlp import MLP  # noqa: E402

GARIS = "=" * 62
FIGUR = Path(__file__).resolve().parent.parent / "figures"
FIGUR.mkdir(exist_ok=True)
DATA = Path(r"E:\SYNESIS\data")


# ══════════════════════════════════════════════════════════════
# Data
# ══════════════════════════════════════════════════════════════

def muat_mnist():
    """Kembalikan enam array: latih, validasi, uji.

    Tiga cara, bukan dua. Bulan 0 cuma butuh dua karena tidak ada
    hyperparameter yang dipilih dari data. Sekarang ada: lebar lapisan, laju
    belajar, jumlah epoch. Kalau ketiganya dipilih dengan melihat himpunan
    uji, angka akhirmu bukan lagi ramalan untuk data baru.

    Disediakan, bukan TODO.
    """
    simpan = DATA / "mnist.npz"
    if simpan.exists():
        d = np.load(simpan)
        X, y, Xu, yu = d["X"], d["y"], d["Xu"], d["yu"]
    else:
        from torchvision import datasets            # cuma dipakai sekali
        a = datasets.MNIST(root=str(DATA), train=True, download=True)
        b = datasets.MNIST(root=str(DATA), train=False, download=True)
        X = a.data.numpy().reshape(-1, 784).astype(np.float64) / 255.0
        y = a.targets.numpy().astype(np.int64)
        Xu = b.data.numpy().reshape(-1, 784).astype(np.float64) / 255.0
        yu = b.targets.numpy().astype(np.int64)
        DATA.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(simpan, X=X, y=y, Xu=Xu, yu=yu)

    return X[:50000], y[:50000], X[50000:], y[50000:], Xu, yu


# ══════════════════════════════════════════════════════════════
# BAGIAN 1 - entropi silang di atas Value
# ══════════════════════════════════════════════════════════════

def softmax_silang_value(logit, kelas):
    """Rugi entropi silang untuk satu contoh, dibangun dari Value.

    logit : daftar 10 Value, keluaran mentah jaringan
    kelas : bilangan bulat 0..9, jawaban benarnya

    Rumusnya dua langkah:

        p_i  = exp(z_i) / sum_j exp(z_j)          <- softmax
        rugi = -log(p_kelas)                      <- entropi silang

    Satu jebakan angka. exp(z) meledak kalau z besar. Obatnya: kurangi semua
    z dengan bilangan tetap m sebelum di-exp. Hasil softmax-nya sama persis,
    karena faktor exp(-m) muncul di pembilang dan penyebut lalu saling
    menghapus. Ambil m = max(z) sebagai float biasa, bukan Value, supaya ia
    jadi konstanta dan gradiennya tidak terpengaruh.

    Kembalikan satu Value.

    TODO 1
    """
    raise NotImplementedError("softmax_silang_value")


def bagian1():
    print(GARIS, "\nBAGIAN 1  entropi silang di atas mesinmu sendiri\n",
          GARIS, sep="")

    random.seed(0)
    z = [Value(random.gauss(0, 2)) for _ in range(10)]
    kelas = 3

    rugi = softmax_silang_value(z, kelas)
    for v in z:
        v.grad = 0.0
    rugi.backward()

    # softmax versi numpy, cuma sebagai pembanding
    zn = np.array([v.data for v in z])
    p = np.exp(zn - zn.max())
    p /= p.sum()
    sasaran = np.zeros(10)
    sasaran[kelas] = 1.0

    print(f"  rugi dari mesinmu     : {rugi.data:.6f}")
    print(f"  rugi dari numpy       : {-math.log(p[kelas]):.6f}")
    print(f"  peluang kelas benar   : {p[kelas]:.6f}\n")

    print(f"  {'i':>3}{'z_i':>11}{'p_i':>11}{'dL/dz_i':>13}"
          f"{'p_i - y_i':>13}{'selisih':>12}")
    print("  " + "-" * 63)
    galat = 0.0
    for i in range(10):
        beda = abs(z[i].grad - (p[i] - sasaran[i]))
        galat = max(galat, beda)
        print(f"  {i:>3}{z[i].data:>11.4f}{p[i]:>11.6f}{z[i].grad:>13.6f}"
              f"{p[i] - sasaran[i]:>13.6f}{beda:>12.2e}")

    print(f"""
  Selisih terbesar {galat:.2e}.

  Kolom keempat dan kelima sama, dan itu bukan kebetulan. Gradien entropi
  silang terhadap logit selalu

      dL/dz = p - y

  Satu pengurangan. Tidak ada exp, tidak ada log, tidak ada pembagian yang
  tersisa. Semua kerumitan softmax dan logaritma saling menghapus waktu
  diturunkan, dan yang tertinggal cuma "seberapa jauh peluangmu dari
  jawabannya".

  Turunkan sendiri di kertas, itu Soal 1. Sesudah itu kamu akan paham kenapa
  di Bagian 5 nanti gradiennya boleh ditulis langsung tanpa autograd.

  Perhatikan juga baris ke-{kelas}: gradiennya negatif, satu-satunya yang
  negatif. Itu kelas yang benar, dan gradien negatif berarti "naikkan logit
  ini". Sembilan lainnya positif, artinya turunkan.""")


# ══════════════════════════════════════════════════════════════
# BAGIAN 2 - dua dinding
# ══════════════════════════════════════════════════════════════

def rugi_batch_value(model, X, y):
    """Rugi entropi silang rata-rata untuk sekumpulan gambar. Disediakan."""
    total = Value(0.0)
    for xi, yi in zip(X, y):
        logit = model([Value(float(v)) for v in xi])
        total = total + softmax_silang_value(logit, int(yi))
    return total * (1.0 / len(y))


def bagian2(X, y):
    print("\n" + GARIS, "\nBAGIAN 2  dua dinding, diukur bukan ditebak\n",
          GARIS, sep="")

    print("  Dinding pertama: waktu.\n")
    random.seed(0)
    m = MLP(784, [32, 10])
    waktu = []
    for i in range(3):
        t0 = time.perf_counter()
        rugi = rugi_batch_value(m, X[i:i + 1], y[i:i + 1])
        m.nolkan()
        rugi.backward()
        waktu.append(time.perf_counter() - t0)

    per_gambar = sum(waktu) / len(waktu)
    n_par = f"{len(m.parameters()):,}".replace(",", ".")
    print(f"    arsitektur          : 784-32-10, {n_par} parameter")
    print("    tiga ukuran         : "
          + ", ".join(f"{t * 1000:.0f} ms" for t in sorted(waktu)))
    print(f"    satu epoch 50000    : {per_gambar * 50000 / 3600:.1f} jam")
    print(f"    sepuluh epoch       : {per_gambar * 50000 * 10 / 86400:.1f} hari\n")

    print("  Dinding kedua: rekursi.\n")
    random.seed(0)
    besar = MLP(784, [256, 10])
    try:
        rugi = rugi_batch_value(besar, X[:1], y[:1])
        besar.nolkan()
        rugi.backward()
        print("    784-256-10 : lolos, tidak seperti ramalanmu")
    except RecursionError as e:
        print(f"    784-256-10 : {type(e).__name__}: {e}")
        print(f"    kedalaman kira-kira 784 + 256 = 1040, batas "
              f"{sys.getrecursionlimit()}")

    print("""
  Dua dinding ini independen, dan itu yang bikin urutan perbaikan penting.
  Mempercepat kode tidak menaikkan batas rekursi. Menaikkan batas rekursi
  tidak mempercepat apa pun.

  Yang pecah dikerjakan dulu. Bagian 3.""")

    return per_gambar


# ══════════════════════════════════════════════════════════════
# BAGIAN 3 - tembus dinding rekursi
# ══════════════════════════════════════════════════════════════

def backward_iteratif(akar):
    """Ganti `Value.backward` dengan versi tanpa rekursi.

    Yang rekursif di Sesi 1 cuma satu hal: fungsi `bangun` yang menyusun
    urutan topologis. Tumpukan panggilannya sedalam graf, dan graf MNIST
    sedalam 1040.

    Tulis ulang penyusunan urutan itu memakai daftar sebagai tumpukan sendiri,
    bukan tumpukan panggilan Python. Sesudah urutannya jadi, sisanya sama
    persis dengan Sesi 1: pasang grad akar 1.0, lalu panggil _backward tiap
    simpul dari belakang ke depan.

    Pola yang paling ringkas namanya iterative post-order. Satu tumpukan
    berisi pasangan (simpul, sudah_ditelusuri):

        - ambil satu dari tumpukan
        - kalau belum ditelusuri, kembalikan ke tumpukan dengan tanda sudah,
          lalu dorong semua anaknya
        - kalau sudah ditelusuri, catat ke urutan

    Simpul yang sudah pernah dilihat jangan didorong dua kali. Pakai `set`,
    yang menyimpan berdasarkan identitas objek, sama seperti di Sesi 1.

    TODO 2
    """
    raise NotImplementedError("backward_iteratif")


def bagian3(X, y):
    print("\n" + GARIS, "\nBAGIAN 3  tembus dinding rekursi\n", GARIS, sep="")

    asli = Value.backward
    Value.backward = backward_iteratif
    try:
        random.seed(0)
        kecil = MLP(4, [3, 2])
        r = rugi_batch_value(kecil, np.random.default_rng(0).normal(0, 1, (2, 4)),
                             [0, 1])
        kecil.nolkan()
        r.backward()
        g_iter = [p.grad for p in kecil.parameters()]

        Value.backward = asli
        random.seed(0)
        kecil2 = MLP(4, [3, 2])
        r2 = rugi_batch_value(kecil2, np.random.default_rng(0).normal(0, 1, (2, 4)),
                              [0, 1])
        kecil2.nolkan()
        r2.backward()
        g_rek = [p.grad for p in kecil2.parameters()]

        beda = max(abs(a - b) for a, b in zip(g_iter, g_rek))
        print(f"  dulu diadu dengan versi rekursif di jaringan kecil")
        print(f"    parameter dibandingkan : {len(g_iter)}")
        print(f"    selisih gradien maks   : {beda:.3e}")
        print(f"    status                 : {'lolos' if beda < 1e-12 else 'GAGAL'}\n")

        Value.backward = backward_iteratif
        random.seed(0)
        besar = MLP(784, [256, 10])
        t0 = time.perf_counter()
        rugi = rugi_batch_value(besar, X[:1], y[:1])
        besar.nolkan()
        rugi.backward()
        dt = time.perf_counter() - t0
        n_grad = sum(1 for p in besar.parameters() if p.grad != 0.0)
        print(f"  784-256-10 sekarang    : lolos, {dt * 1000:.0f} ms")
        print(f"    parameter bergradien : {n_grad:,} dari "
              f"{len(besar.parameters()):,}".replace(",", "."))
    finally:
        Value.backward = asli

    print("""
  Dinding kedua jatuh, dan perhatikan yang TIDAK terjadi: waktunya tidak
  membaik sedikit pun. Memang begitu. Rekursi bukan sumber lambatnya.

  Perhatikan juga apa yang tidak dipakai: sys.setrecursionlimit. Menaikkan
  batas itu memindahkan masalah ke tumpukan sistem operasi, dan waktu ia
  habis kamu tidak dapat RecursionError yang sopan, kamu dapat proses mati
  tanpa pesan. Soal 2 memintamu menjelaskan bedanya.""")


# ══════════════════════════════════════════════════════════════
# BAGIAN 4 - tembus dinding waktu
# ══════════════════════════════════════════════════════════════

class Tensor:
    """Value, tapi satu objek memuat seluruh array, bukan satu angka.

    Itu seluruh idenya. Grafnya sama, urutan topologisnya sama, aturan
    rantainya sama. Yang berubah cuma berapa banyak angka yang diurus satu
    objek Python.

    Di Bagian 2 satu gambar MNIST butuh 50.869 objek Value. Di sini satu
    batch 64 gambar butuh belasan objek Tensor.

    Mesin grafnya disediakan. Yang jadi TODO cuma aturan turunan lokalnya.
    """

    def __init__(self, data, _anak=(), _op=""):
        self.data = np.asarray(data, dtype=np.float64)
        self.grad = np.zeros_like(self.data)
        self._prev = set(_anak)
        self._backward = lambda: None
        self._op = _op

    def __repr__(self):
        return f"Tensor(bentuk={self.data.shape}, op={self._op!r})"

    def __matmul__(self, other):
        """Perkalian matriks. out = self @ other

        Turunan lokalnya dua baris, dan bentuknya bisa kamu tebak dari
        aturan "bentuk gradien selalu sama dengan bentuk datanya".

        Kalau self berbentuk (B, n) dan other (n, m), maka out (B, m) dan
        out.grad juga (B, m). Susun perkalian yang menghasilkan (B, n) untuk
        self.grad, dan (n, m) untuk other.grad. Cuma ada satu susunan yang
        bentuknya cocok untuk masing-masing.

        TODO 3
        """
        out = Tensor(self.data @ other.data, (self, other), "@")

        def _backward():
            raise NotImplementedError("Tensor.__matmul__ backward")

        out._backward = _backward
        return out

    def __add__(self, other):
        """Penjumlahan dengan siaran. out = self + other

        Dipakai untuk menambahkan geseran: self (B, n) plus other (n,).

        Di sinilah orang paling sering salah. Karena other disiarkan ke B
        baris, ia ikut memengaruhi B keluaran, jadi gradiennya adalah JUMLAH
        gradien dari seluruh baris. Bukan rata-rata, dan bukan satu baris saja.

        Kalau bentuk keduanya sama persis, tidak ada siaran, dan gradiennya
        lewat apa adanya.

        TODO 4
        """
        out = Tensor(self.data + other.data, (self, other), "+")

        def _backward():
            raise NotImplementedError("Tensor.__add__ backward")

        out._backward = _backward
        return out

    def relu(self):
        """Tekukan, elemen demi elemen.

        TODO 5
        """
        out = Tensor(np.maximum(self.data, 0), (self,), "relu")

        def _backward():
            raise NotImplementedError("Tensor.relu backward")

        out._backward = _backward
        return out

    def entropi_silang(self, kelas):
        """Softmax dan entropi silang sekaligus, dirata-rata atas batch.

        self  : logit, bentuk (B, 10)
        kelas : bentuk (B,), bilangan bulat 0..9

        Sengaja digabung jadi satu operasi, bukan dua. Alasannya persis apa
        yang kamu lihat di Bagian 1: turunan gabungannya `p - y`, bersih dan
        murah. Dipisah jadi softmax lalu log, kamu membangun graf yang jauh
        lebih besar untuk mendapat jawaban yang sama.

        Maju: kurangi max tiap baris, exp, bagi jumlahnya, ambil -log di
        kolom kelas yang benar, rata-ratakan.

        Mundur: (p - y) / B. Ingat pembagi B, karena rugi ini rata-rata.

        TODO 6
        """
        raise NotImplementedError("Tensor.entropi_silang")

    def backward(self):
        """Sama seperti Value, tapi urutannya sudah iteratif sejak awal.

        Disediakan. Bandingkan dengan yang kamu tulis di TODO 2.
        """
        urutan, terlihat, tumpukan = [], set(), [(self, False)]
        while tumpukan:
            v, sudah = tumpukan.pop()
            if sudah:
                urutan.append(v)
            elif id(v) not in terlihat:
                terlihat.add(id(v))
                tumpukan.append((v, True))
                for a in v._prev:
                    tumpukan.append((a, False))

        self.grad = np.ones_like(self.data)
        for v in reversed(urutan):
            v._backward()


def maju(param, X):
    """Satu lintasan maju. param daftar [W1, b1, W2, b2]. Disediakan."""
    W1, b1, W2, b2 = param
    return ((Tensor(X) @ W1 + b1).relu()) @ W2 + b2


def bagian4(X, y):
    print("\n" + GARIS, "\nBAGIAN 4  Tensor: satu objek untuk seluruh array\n",
          GARIS, sep="")

    rng = np.random.default_rng(0)
    n_in, n_h, n_k, B = 6, 5, 4, 3
    param = [
        Tensor(rng.normal(0, 1, (n_in, n_h)) * (2 / n_in) ** 0.5),
        Tensor(np.zeros(n_h)),
        Tensor(rng.normal(0, 1, (n_h, n_k)) * (2 / n_h) ** 0.5),
        Tensor(np.zeros(n_k)),
    ]
    Xk = rng.normal(0, 1, (B, n_in))
    yk = rng.integers(0, n_k, B)

    rugi = maju(param, Xk).entropi_silang(yk)
    rugi.backward()

    def rugi_saja(vektor):
        salin = [Tensor(p.data.copy()) for p in param]
        i = 0
        for p in salin:
            n = p.data.size
            p.data = vektor[i:i + n].reshape(p.data.shape).copy()
            i += n
        return maju(salin, Xk).entropi_silang(yk).data

    datar = np.concatenate([p.data.ravel() for p in param])
    g_auto = np.concatenate([p.grad.ravel() for p in param])
    h = 1e-6
    g_beda = np.zeros_like(datar)
    for i in range(len(datar)):
        maju_i, mundur_i = datar.copy(), datar.copy()
        maju_i[i] += h
        mundur_i[i] -= h
        g_beda[i] = (rugi_saja(maju_i) - rugi_saja(mundur_i)) / (2 * h)

    galat = np.abs(g_auto - g_beda).max() / (np.abs(g_beda).max() + 1e-12)
    print(f"  parameter diuji : {len(datar)}")
    print(f"  rugi            : {rugi.data:.6f}")
    print(f"  galat relatif   : {galat:.3e}")
    print(f"  status          : {'lolos' if galat < 1e-5 else 'GAGAL'}")

    print("""
  Aturannya tetap sama sejak Hari 1. Gradien tidak dipercaya sebelum diadu
  dengan beda hingga, tak peduli seberapa yakin kamu waktu menulisnya.

  Yang berubah cuma ongkosnya. Angkanya ada di Bagian 5.""")


# ══════════════════════════════════════════════════════════════
# BAGIAN 5 - MNIST
# ══════════════════════════════════════════════════════════════

def akurasi(param, X, y, potong=10000):
    logit = maju(param, X[:potong]).data
    return (logit.argmax(1) == y[:potong]).mean()


def latih_mnist(X, y, Xv, yv, n_h=128, lr=0.1, epoch=8, batch=64, seed=0,
                kabar=True):
    """SGD polos, mini-batch.

    Menyimpan salinan parameter di epoch dengan validasi terbaik. Itulah
    gunanya himpunan validasi ada, dan kalau tidak dipakai memilih apa pun,
    membelahnya jadi tiga cuma upacara.

    Disediakan.
    """
    rng = np.random.default_rng(seed)
    param = [
        Tensor(rng.normal(0, 1, (784, n_h)) * (2 / 784) ** 0.5),
        Tensor(np.zeros(n_h)),
        Tensor(rng.normal(0, 1, (n_h, 10)) * (2 / n_h) ** 0.5),
        Tensor(np.zeros(10)),
    ]
    riwayat, terbaik = [], None
    for e in range(epoch):
        t0 = time.perf_counter()
        urut = rng.permutation(len(y))
        for i in range(0, len(urut), batch):
            k = urut[i:i + batch]
            rugi = maju(param, X[k]).entropi_silang(y[k])
            for p in param:
                p.grad = np.zeros_like(p.data)
            rugi.backward()
            for p in param:
                p.data -= lr * p.grad
        dt = time.perf_counter() - t0
        av = akurasi(param, Xv, yv)
        riwayat.append((e, rugi.data, av, dt))
        if terbaik is None or av > terbaik[0]:
            terbaik = (av, e, [p.data.copy() for p in param])
        if kabar:
            print(f"    epoch {e:>2}   rugi {rugi.data:.4f}   "
                  f"validasi {av * 100:5.2f} persen   {dt:.1f} detik")
    return param, riwayat, terbaik


def bagian5(X, y, Xv, yv, Xu, yu, per_gambar_value):
    print("\n" + GARIS, "\nBAGIAN 5  MNIST\n", GARIS, sep="")

    print(f"  latih {len(y):,} | validasi {len(yv):,} | uji {len(yu):,}"
          .replace(",", "."))
    print("  arsitektur 784-128-10, SGD polos, batch 64\n")

    param, riw, terbaik = latih_mnist(X, y, Xv, yv)

    au_akhir = akurasi(param, Xu, yu)
    for pr, d in zip(param, terbaik[2]):
        pr.data = d
    au_pilih = akurasi(param, Xu, yu)

    waktu = sorted(r[3] for r in riw)
    detik = waktu[len(waktu) // 2]

    print(f"\n  akurasi uji, epoch terakhir : {au_akhir * 100:.2f} persen")
    print(f"  akurasi uji, epoch pilihan  : {au_pilih * 100:.2f} persen"
          f"   (epoch {terbaik[1]}, dipilih lewat validasi)")
    print("  target Bulan 1              : 95 persen")
    print(f"  status                      : "
          f"{'lolos' if au_pilih > 0.95 else 'BELUM'}\n")

    cepat = per_gambar_value * len(y) / detik
    print(f"  {'mesin':<18}{'per epoch':>14}{'rasio':>10}")
    print("  " + "-" * 42)
    print(f"  {'Value, sebutir':<18}{per_gambar_value * len(y) / 3600:>11.1f} jam"
          f"{1:>10.0f}x")
    print(f"  {'Tensor, numpy':<18}{detik:>11.1f} dtk{cepat:>10.0f}x")
    print(f"  waktu epoch dipakai nilai tengahnya. Sebaran "
          f"{waktu[0]:.1f} sampai {waktu[-1]:.1f} detik,")
    print("  dan epoch pertama selalu terlama karena 313 MB data baru "
          "disentuh")
    print("  untuk pertama kali.")

    # gambar yang salah tebak
    logit = maju(param, Xu[:2000]).data
    tebak = logit.argmax(1)
    salah = np.nonzero(tebak != yu[:2000])[0][:12]
    fig, sb = plt.subplots(2, 6, figsize=(9, 3.4))
    for ax, i in zip(sb.ravel(), salah):
        ax.imshow(Xu[i].reshape(28, 28), cmap="gray_r")
        ax.set_title(f"{yu[i]} -> {tebak[i]}", fontsize=9)
        ax.axis("off")
    fig.suptitle("dua belas yang masih salah")
    fig.tight_layout()
    fig.savefig(FIGUR / "bulan1_sesi34_salah.png", dpi=110)
    plt.close(fig)
    print(f"\n  gambar salah tebak : figures/bulan1_sesi34_salah.png")

    print("""
  Dinding pertama jatuh, dan besarannya ada di tabel di atas.

  Yang penting dipahami: tidak satu pun aritmetika berubah. Perkalian dan
  penjumlahan yang dikerjakan mesin persis sama banyaknya. Yang hilang cuma
  ongkos mengurus, satu objek Python plus satu penelusuran graf per angka.

  Itu jawaban lengkap untuk "kenapa PyTorch cepat", dan kamu sudah
  mengukurnya sendiri di Bukti 6 Sesi D. Bagian 6 cuma mengonfirmasi.""")

    return param, detik


# ══════════════════════════════════════════════════════════════
# BAGIAN 6 - PyTorch
# ══════════════════════════════════════════════════════════════

def bagian6(X, y, detik_numpy):
    print("\n" + GARIS, "\nBAGIAN 6  pembanding PyTorch\n", GARIS, sep="")

    try:
        import torch
        import torch.nn as nn
    except ImportError:
        print("  torch tidak ada di lingkungan ini, bagian ini dilewati")
        return

    torch.manual_seed(0)
    Xt = torch.tensor(X, dtype=torch.float32)
    yt = torch.tensor(y)

    def sekali(alat):
        jaring = nn.Sequential(nn.Linear(784, 128), nn.ReLU(),
                               nn.Linear(128, 10)).to(alat)
        opt = torch.optim.SGD(jaring.parameters(), lr=0.5)
        rugi_fn = nn.CrossEntropyLoss()
        Xa, ya = Xt.to(alat), yt.to(alat)
        urut = torch.randperm(len(ya), device=alat)
        if alat == "cuda":
            torch.cuda.synchronize()
        t0 = time.perf_counter()
        for i in range(0, len(urut), 64):
            k = urut[i:i + 64]
            opt.zero_grad()
            rugi_fn(jaring(Xa[k]), ya[k]).backward()
            opt.step()
        if alat == "cuda":
            torch.cuda.synchronize()
        return time.perf_counter() - t0

    alat = ["cpu"] + (["cuda"] if torch.cuda.is_available() else [])
    print(f"  {'mesin':<22}{'per epoch':>13}{'lawan numpy':>14}")
    print("  " + "-" * 49)
    print(f"  {'Tensor numpy sendiri':<22}{detik_numpy:>10.1f} dtk{1:>13.1f}x")
    for a in alat:
        sekali(a)                      # pemanasan, jangan diukur
        dt = sekali(a)
        nama = "PyTorch " + ("CPU" if a == "cpu" else
                             torch.cuda.get_device_name(0)[:12])
        print(f"  {nama:<22}{dt:>10.1f} dtk{detik_numpy / dt:>13.1f}x")

    print("""
  Selisih numpy lawan PyTorch CPU jauh lebih kecil daripada selisih Value
  lawan numpy. Itu penting, dan sering disalahpahami.

  Lompatan besar terjadi waktu kamu berhenti mengurus satu angka satu objek.
  Sesudah itu semua pustaka memanggil BLAS yang sama.

  Sisa selisihnya punya satu sebab yang bisa kamu hapus sendiri: Tensor kita
  memakai float64, PyTorch memakai float32. Dua kali lebar berarti dua kali
  lalu lintas memori, dan di perkalian matriks sebesar ini memorilah
  penyempitnya, bukan aritmetika. Sisanya lapisan Python yang masih tertinggal
  di jalur panas kita.

  Perhatikan juga baris GPU-nya. Kalau ia kalah dari CPU, itu bukan kesalahan
  pemasangan. Batch 64 di jaringan 784-128-10 terlalu kecil untuk menutup
  ongkos tetap tiap panggilan kernel, dan ongkos itu ada entah kamu mengalikan
  seratus angka atau seratus juta.

  Soal 5 memintamu mengukur bagian float32-nya, lalu memperkirakan di batch
  berapa GPU mulai menang.""")


# ══════════════════════════════════════════════════════════════
# BAGIAN 7 - optimizer tulisan tangan
# ══════════════════════════════════════════════════════════════

def lembah_sempit(n=60, seed=1):
    """Regresi linear tanpa distandarkan. Sengaja, supaya lembahnya sempit.

    Di Sesi B, x diambil dari [-5, 5] dan bilangan kondisinya cuma 8. Di
    lanskap selandai itu SGD polos justru menang, dan perbandingan optimizer
    jadi tidak ada artinya.

    Di sini x diambil dari [2, 12]. Yang berubah cuma pergeseran pusatnya,
    dan itu sudah cukup untuk menaikkan bilangan kondisi ratusan kali.
    Soal 6 memintamu menghitung kenapa.

    Disediakan.
    """
    rng = np.random.default_rng(seed)
    x = rng.uniform(2, 12, n)
    y = 3.0 * x + 2.0 + rng.normal(0, 1.5, n)
    A = np.stack([x, np.ones(n)], 1)
    return A, y


def rugi_grad(A, y, th):
    """MSE dan gradiennya. Disediakan."""
    sisa = A @ th - y
    return (sisa ** 2).mean(), 2.0 / len(y) * (A.T @ sisa)


def sgd(g, keadaan, lr):
    """Pembanding dasar. Disediakan sebagai contoh bentuk fungsinya."""
    return -lr * g, keadaan


def momentum(g, keadaan, lr, beta=0.9):
    """SGD dengan momentum.

        v = beta * v - lr * g
        langkah = v

    `keadaan` adalah dict yang boleh kamu isi bebas; ia dikembalikan ke kamu
    di panggilan berikutnya. Kembalikan (langkah, keadaan).

    Dari Bukti 4 Sesi D kamu sudah tahu bentuk ini. Lupa `zero_()` memberi

        th[k+1] - 2*th[k] + th[k-1] = -lr * g(th[k])

    yaitu osilator TANPA gesekan, dan itu sebabnya ia berayun selamanya.
    Momentum adalah persamaan yang sama dengan gesekan dikembalikan, dan
    beta itu koefisien redamannya. beta = 1 memberi kembali bug zero_(),
    beta = 0 memberi kembali SGD polos.

    TODO 7
    """
    raise NotImplementedError("momentum")


def rmsprop(g, keadaan, lr, beta=0.9, eps=1e-8):
    """RMSprop.

        s = beta * s + (1 - beta) * g^2
        langkah = -lr * g / (sqrt(s) + eps)

    Bacaan fisisnya: tiap sumbu dibagi akar rata-rata kuadrat gradiennya
    sendiri, jadi sumbu yang curam dikecilkan dan sumbu yang landai
    dibesarkan. Efeknya menyamakan skala, yang persis obat untuk bilangan
    kondisi besar.

    TODO 8
    """
    raise NotImplementedError("rmsprop")


def adam(g, keadaan, lr, b1=0.9, b2=0.999, eps=1e-8):
    """Adam. Momentum dan RMSprop dipakai bersamaan, plus koreksi bias.

        m = b1 * m + (1 - b1) * g
        s = b2 * s + (1 - b2) * g^2
        mh = m / (1 - b1^t)
        sh = s / (1 - b2^t)
        langkah = -lr * mh / (sqrt(sh) + eps)

    Koreksi bias itu perlu karena m dan s dimulai dari nol, jadi di
    langkah-langkah awal keduanya terlalu kecil. Pembagi (1 - b1^t) menebus
    itu, dan pengaruhnya lenyap sendiri waktu t membesar.

    Simpan t di dalam `keadaan`.

    TODO 9
    """
    raise NotImplementedError("adam")


def jalankan(A, y, aturan, lr, n_iter=300, th0=(0.0, 0.0)):
    """Jalankan satu optimizer, kembalikan lintasannya. Disediakan."""
    th = np.array(th0, dtype=float)
    keadaan, jejak = {}, [th.copy()]
    with np.errstate(over="ignore", invalid="ignore"):
        for _ in range(n_iter):
            _, g = rugi_grad(A, y, th)
            if not np.all(np.isfinite(g)):
                break
            langkah, keadaan = aturan(g, keadaan, lr)
            th = th + langkah
            if not np.all(np.isfinite(th)):
                break
            jejak.append(th.copy())
    return np.array(jejak)


def bagian7():
    print("\n" + GARIS, "\nBAGIAN 7  momentum, RMSprop, Adam, tulis tangan\n",
          GARIS, sep="")

    A, y = lembah_sempit()
    H = 2.0 / len(y) * (A.T @ A)
    lam = np.linalg.eigvalsh(H)
    th_ideal = np.linalg.lstsq(A, y, rcond=None)[0]
    rugi_ideal, _ = rugi_grad(A, y, th_ideal)

    print(f"  eigen Hessian    : {lam[0]:.4f} dan {lam[1]:.4f}")
    print(f"  bilangan kondisi : {lam[1] / lam[0]:.1f}")
    print(f"  ambang SGD, 2/lam_max : {2 / lam[1]:.6f}")
    print(f"  rugi minimum     : {rugi_ideal:.6f}\n")

    print("  Tiap optimizer dapat laju belajarnya sendiri, dipilih dari sapuan")
    print("  yang sama persis. Membandingkan di satu lr itu tidak jujur.\n")

    aturan = {"SGD polos": sgd, "momentum": momentum,
              "RMSprop": rmsprop, "Adam": adam}
    sapuan = np.logspace(-4, 1.5, 56)
    hasil = {}

    print(f"  {'optimizer':<12}{'lr terbaik':>12}{'rugi akhir':>13}"
          f"{'iterasi ke 1%':>16}")
    print("  " + "-" * 53)
    for nama, fn in aturan.items():
        terbaik = None
        with np.errstate(over="ignore", invalid="ignore"):
            for lr in sapuan:
                jejak = jalankan(A, y, fn, lr)
                r, _ = rugi_grad(A, y, jejak[-1])
                if not np.isfinite(r):
                    continue
                if terbaik is None or r < terbaik[1]:
                    terbaik = (lr, r, jejak)
            lr, r, jejak = terbaik
            batas = rugi_ideal * 1.01
            tiba = next((i for i, t in enumerate(jejak)
                         if rugi_grad(A, y, t)[0] <= batas), None)
        hasil[nama] = (lr, r, jejak, tiba)
        print(f"  {nama:<12}{lr:>12.5f}{r:>13.6f}"
              f"{(tiba if tiba is not None else '-'):>16}")

    # gambar: kiri lintasan, kanan konvergensi
    potong = 80
    semua = np.vstack([h[2][:potong] for h in hasil.values()])
    pad_w = 0.12 * (np.ptp(semua[:, 0]) + 1e-9)
    pad_b = 0.12 * (np.ptp(semua[:, 1]) + 1e-9)
    ws = np.linspace(semua[:, 0].min() - pad_w, semua[:, 0].max() + pad_w, 200)
    bs = np.linspace(semua[:, 1].min() - pad_b, semua[:, 1].max() + pad_b, 200)
    WS, BS = np.meshgrid(ws, bs)
    L = np.array([[rugi_grad(A, y, np.array([w, b]))[0] for w in ws]
                  for b in bs])

    fig, (kiri, kanan) = plt.subplots(1, 2, figsize=(12.5, 5.2))

    kiri.contour(WS, BS, np.log10(L - rugi_ideal + 1e-9), levels=24,
                 colors="0.8", linewidths=0.6)
    tebal = (2.6, 1.9, 1.3, 0.9)
    for (nama, (lr, r, jejak, tiba)), lw in zip(hasil.items(), tebal):
        kiri.plot(jejak[:potong, 0], jejak[:potong, 1], lw=lw, alpha=0.9,
                  label=f"{nama}  lr={lr:.4f}")
    kiri.plot(*th_ideal, "k*", ms=15, zorder=5)
    kiri.set_xlabel("w")
    kiri.set_ylabel("b")
    kiri.set_title(f"{potong} langkah pertama, "
                   f"bilangan kondisi {lam[1] / lam[0]:.0f}")
    kiri.legend(fontsize=8, loc="lower right")

    for nama, (lr, r, jejak, tiba) in hasil.items():
        kurva = np.array([rugi_grad(A, y, t)[0] for t in jejak]) - rugi_ideal
        kanan.semilogy(np.maximum(kurva, 1e-16), lw=1.6, label=nama)
    kanan.axhline(rugi_ideal * 0.01, color="0.4", ls="--", lw=1,
                  label="ambang 1 persen")
    kanan.set_xlabel("iterasi")
    kanan.set_ylabel("rugi dikurangi minimum")
    kanan.set_title("jarak ke dasar, sumbu tegak logaritmik")
    kanan.legend(fontsize=8)
    kanan.grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(FIGUR / "bulan1_sesi34_optimizer.png", dpi=120)
    plt.close(fig)

    print(f"\n  lintasan : figures/bulan1_sesi34_optimizer.png")

    print("""
  Buka gambarnya. Panel kiri bentuk lintasan, panel kanan yang menentukan:
  jarak ke dasar terhadap iterasi, sumbu tegak logaritmik. Garis yang turun
  lurus di sumbu logaritmik artinya galatnya mengecil dengan faktor tetap tiap
  langkah, dan kemiringannya itulah kecepatan sebenarnya.

  SGD polos harus memilih laju belajar yang aman untuk sumbu paling curam,
  dan sumbu itu 400 kali lebih curam dari yang landai. Akibatnya ia merangkak
  di sumbu landai. Ini persis ambang 2/lam_max yang kamu ukur di Sesi D, cuma
  sekarang kamu melihat harganya.

  Momentum menumpuk kecepatan di arah yang konsisten dan saling menghapus di
  arah yang bolak-balik. Gesekan beta yang menentukan seberapa banyak yang
  ditumpuk, dan itu osilator teredam dari Fisika Dasar, bukan analogi.

  RMSprop tidak menumpuk apa pun. Ia membagi tiap sumbu dengan skalanya
  sendiri, jadi lembah sempitnya berhenti sempit.

  Adam memakai keduanya. Soal 8 memintamu menyebutkan kondisi masing-masing
  menang, dan jawaban "Adam selalu" salah.""")


# ══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    X, y, Xv, yv, Xu, yu = muat_mnist()
    try:
        bagian1()
        per_gambar = bagian2(X, y)
        bagian3(X, y)
        bagian4(X, y)
        param, detik = bagian5(X, y, Xv, yv, Xu, yu, per_gambar)
        bagian6(X, y, detik)
        bagian7()
    except NotImplementedError as e:
        print(f"\n  {e} belum diisi. Kerjakan TODO dulu.")
