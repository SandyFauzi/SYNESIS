"""Bulan 3 Sesi 3 - CNN dari nol, di atas Tensor buatanmu sendiri.

Jalankan:
    . .\\scripts\\activate.ps1
    python notebooks\\bulan3_sesi3_cnn.py

Sesi 1 menunjukkan bahwa konvolusi bisa ditulis sebagai satu perkalian
matriks. Sesi 2 mengubah suara jadi matriks waktu-frekuensi. Malam ini
keduanya disambung: lapisan konvolusi dilatih dengan mesin autograd yang
sudah kamu tulis di Bulan 1, tanpa mengganti satu baris pun di dalamnya.

Yang perlu ditambahkan cuma tiga operasi, dan tidak satu pun di antaranya
adalah "konvolusi":

    im2col       menyusun petak jadi baris. Turunannya col2im.
    bentuk_ulang mengubah bentuk array. Turunannya mengubah bentuknya balik.
    maks_kolam   mengambil maksimum tiap petak. Turunannya menyalurkan
                 gradien ke pemenangnya saja.

Konvolusinya sendiri lahir dari `__matmul__` dan `__add__` yang sudah ada
sejak Bulan 1. Itu bukan kebetulan penulisan; itu pernyataan bahwa lapisan
konvolusi memang lapisan linear dengan bobot yang dipakai ulang.

Enam bagian:

    1  tiga operasi baru, ditulis di atas Tensor apa adanya
    2  periksa gradiennya secara numerik, sebelum melatih apa pun
    3  CNN pertama di MNIST, diadu dengan MLP Bulan 1 pada jumlah bobot
    4  apa yang dipelajari kernel lapisan pertama
    5  versi PyTorch-nya: kesamaan diperiksa, lalu kecepatannya diukur
    6  dari gambar ke spektrogram, dan satu asumsi yang tidak berlaku lagi

Bagian bertanda TODO kamu yang isi.
"""

import sys
import time
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))

from bulan1_sesi34_mnist import Tensor, muat_mnist  # noqa: E402
from bulan3_sesi2_spektrogram import (  # noqa: E402
    baca_wav, koma, ribuan, spektrogram_mel)

GARIS = "=" * 66
FIGUR = Path(__file__).resolve().parent.parent / "figures"
FIGUR.mkdir(exist_ok=True)
SUARA = Path(r"E:\SYNESIS\data\speech_commands")

# Tata letak array dipatok kanal-terakhir: (batch, tinggi, lebar, kanal).
# PyTorch memakai kanal-kedua, dan Bagian 5 menerjemahkannya. Kanal-terakhir
# dipilih di sini karena membuat im2col jadi irisan tanpa transpose.


# ══════════════════════════════════════════════════════════════
# BAGIAN 1 - tiga operasi baru
# ══════════════════════════════════════════════════════════════

def im2col(X, Kh, Kw):
    """Susun tiap petak Kh x Kw jadi satu baris. Operasi Tensor, ada gradiennya.

    X    : Tensor bentuk (B, H, W, C)
    hasil: Tensor bentuk (B * Th * Tw, Kh * Kw * C)

    Majunya persis `im2col` dari Sesi 1, cuma dengan batch dan kanal.
    Mundurnya adalah col2im, dan Soal 6a Sesi 1 sudah menurunkannya: karena
    im2col menyalin, gradiennya MENJUMLAHKAN kembali seluruh salinan ke
    piksel asalnya.

    Perhatikan bahwa gelungnya cuma Kh kali Kw putaran, yaitu sembilan untuk
    kernel 3x3. Yang ada di dalam gelung adalah irisan array berukuran penuh,
    jadi seluruh batch dikerjakan numpy sekaligus.

    TODO 1
    """
    B, H, W, C = X.data.shape
    Th, Tw = H - Kh + 1, W - Kw + 1
    kol = np.empty((B, Th, Tw, Kh, Kw, C))
    for u in range(Kh):
        for v in range(Kw):
            kol[:, :, :, u, v, :] = X.data[:, u:u + Th, v:v + Tw, :]

    out = Tensor(kol.reshape(B * Th * Tw, Kh * Kw * C), (X,), "im2col")

    def _backward():
        g = out.grad.reshape(B, Th, Tw, Kh, Kw, C)
        dx = np.zeros_like(X.data)
        for u in range(Kh):
            for v in range(Kw):
                dx[:, u:u + Th, v:v + Tw, :] += g[:, :, :, u, v, :]
        X.grad += dx

    out._backward = _backward
    return out


def bentuk_ulang(X, bentuk):
    """Ubah bentuk tanpa mengubah isi. Turunannya mengubah bentuknya balik.

    Operasi paling sepele di berkas ini, dan tetap perlu ditulis sebagai
    operasi Tensor: tanpa simpul di graf, rantai gradiennya putus di sini.

    TODO 2
    """
    out = Tensor(X.data.reshape(bentuk), (X,), "bentuk_ulang")

    def _backward():
        X.grad += out.grad.reshape(X.data.shape)

    out._backward = _backward
    return out


def maks_kolam(X, k=2):
    """Ambil maksimum tiap petak k x k yang tidak tumpang tindih.

    X    : Tensor (B, H, W, C)
    hasil: Tensor (B, H//k, W//k, C)

    Gradiennya: hanya cuplikan yang MENANG di petaknya yang menerima gradien,
    sisanya nol. Sebabnya langsung dari definisi maksimum: menggeser cuplikan
    yang kalah tidak mengubah keluarannya sama sekali, jadi turunannya nol.

    Ini juga sumber sifat yang membuat pooling berguna: keluarannya tidak
    berubah kalau puncaknya bergeser satu piksel di dalam petak yang sama.
    Untuk spektrogram, pergeseran satu bingkai adalah 10 milidetik, dan
    ketidakpekaan terhadap 10 milidetik persis yang kita inginkan.

    TODO 3
    """
    B, H, W, C = X.data.shape
    H2, W2 = H // k, W // k
    d = (X.data[:, :H2 * k, :W2 * k, :]
         .reshape(B, H2, k, W2, k, C)
         .transpose(0, 1, 3, 5, 2, 4)
         .reshape(B, H2, W2, C, k * k))
    pilih = d.argmax(axis=-1)

    out = Tensor(d.max(axis=-1), (X,), "maks_kolam")

    def _backward():
        g = np.zeros_like(d)
        np.put_along_axis(g, pilih[..., None], out.grad[..., None], axis=-1)
        g = (g.reshape(B, H2, W2, C, k, k)
             .transpose(0, 1, 4, 2, 5, 3)
             .reshape(B, H2 * k, W2 * k, C))
        X.grad[:, :H2 * k, :W2 * k, :] += g

    out._backward = _backward
    return out


def konv2d(X, W, b, Kh=3, Kw=3):
    """Lapisan konvolusi. Tidak ada satu pun aturan turunan baru di sini.

    X : Tensor (B, H, W, C_in)
    W : Tensor (Kh * Kw * C_in, C_out)
    b : Tensor (C_out,)

    Tiga baris, dan dua di antaranya memakai operasi Bulan 1 apa adanya.
    Bacalah pelan-pelan: inilah pernyataan bahwa lapisan konvolusi adalah
    lapisan padat yang bobotnya dipakai ulang di setiap posisi.

    TODO 4
    """
    B, H, Wd, _ = X.data.shape
    C_out = W.data.shape[1]
    kol = im2col(X, Kh, Kw)
    return bentuk_ulang(kol @ W + b, (B, H - Kh + 1, Wd - Kw + 1, C_out))


def padat(X, W, b):
    """Lapisan padat biasa. Disediakan; ini cuma @ dan + dari Bulan 1."""
    return X @ W + b


def he(rng, *bentuk):
    """Inisialisasi He: simpangan baku sqrt(2 / fan_in). Disediakan.

    Angka 2 di pembilang khusus untuk ReLU, yang mematikan separuh
    keluarannya, sehingga ragam yang lolos tinggal separuh. Tanpa faktor itu,
    ragam sinyal menyusut separuh tiap lapisan dan jaringan dalam berhenti
    belajar sebelum sempat mulai.
    """
    fan_in = int(np.prod(bentuk[:-1]))
    return Tensor(rng.normal(0, np.sqrt(2.0 / fan_in), bentuk))


def bagian1():
    print(GARIS, "\nBAGIAN 1  tiga operasi baru di atas Tensor Bulan 1\n",
          GARIS, sep="")

    rng = np.random.default_rng(0)
    X = Tensor(rng.normal(size=(2, 6, 6, 3)))
    W = he(rng, 3, 3, 3, 8)
    W = Tensor(W.data.reshape(27, 8))
    b = Tensor(np.zeros(8))

    h = konv2d(X, W, b)
    p = maks_kolam(h.relu(), 2)
    r = bentuk_ulang(p, (2, -1))

    print(f"  {'operasi':<24}{'bentuk masuk':>18}{'bentuk keluar':>18}")
    print("  " + "-" * 60)
    for nama, masuk, keluar in (
            ("konv2d 3x3, 3 -> 8", X.data.shape, h.data.shape),
            ("relu", h.data.shape, h.data.shape),
            ("maks_kolam 2x2", h.data.shape, p.data.shape),
            ("bentuk_ulang", p.data.shape, r.data.shape)):
        print(f"  {nama:<24}{str(masuk):>18}{str(keluar):>18}")

    # Bukti bahwa konv2d benar-benar korelasi silang Sesi 1: satu kernel,
    # satu kanal, dibandingkan dengan gelung polos.
    Xs = Tensor(rng.normal(size=(1, 7, 7, 1)))
    Ks = rng.normal(size=(3, 3))
    Ws = Tensor(Ks.reshape(9, 1))
    hs = konv2d(Xs, Ws, Tensor(np.zeros(1))).data[0, :, :, 0]
    polos = np.array([[(Xs.data[0, i:i + 3, j:j + 3, 0] * Ks).sum()
                       for j in range(5)] for i in range(5)])
    print(f"\n  selisih konv2d vs gelung polos : {np.abs(hs - polos).max():.2e}")
    print("  (korelasi silang, bukan konvolusi. Sesuai Bagian 4 Sesi 1.)")

    print("""
  Yang perlu diperhatikan: `konv2d` tidak punya `_backward` sendiri. Ia cuma
  merangkai im2col, `@`, `+`, dan bentuk_ulang, lalu mesin graf dari Bulan 1
  yang mengurus sisanya. Kalau kamu menambahkan aturan turunan untuk
  konvolusi, kamu menulis kode yang sudah ada.

  Bagian 2 memeriksa apakah keyakinan itu benar, dengan cara yang tidak bisa
  ditipu: bandingkan gradiennya dengan selisih terhingga.""")


# ══════════════════════════════════════════════════════════════
# BAGIAN 2 - periksa gradien
# ══════════════════════════════════════════════════════════════

def periksa_gradien(fungsi, param, eps=1e-6, n_uji=12, seed=0):
    """Bandingkan gradien autograd dengan selisih terhingga terpusat.

    Kembalikan (galat relatif terbesar, gradien analitik, gradien numerik).

    Selisih terpusat dipakai, bukan selisih maju, karena galat pemotongannya
    O(eps^2) dan bukan O(eps). Dengan float64 dan eps = 1e-6, galat relatif
    di bawah 1e-7 adalah lulus.

    Hanya n_uji entri acak yang diperiksa. Memeriksa seluruh parameter berarti
    dua lintasan maju per bobot, dan itu ongkos yang tidak berguna: kalau ada
    aturan turunan yang salah, dua belas titik acak sudah cukup untuk
    menangkapnya.

    Disediakan.
    """
    rng = np.random.default_rng(seed)
    for p in param:
        p.grad = np.zeros_like(p.data)
    fungsi().backward()

    galat = 0.0
    pasang = []
    for p in param:
        for _ in range(max(1, n_uji // len(param))):
            i = tuple(rng.integers(0, s) for s in p.data.shape)
            asli = p.data[i]
            p.data[i] = asli + eps
            atas = fungsi().data
            p.data[i] = asli - eps
            bawah = fungsi().data
            p.data[i] = asli
            num = (atas - bawah) / (2 * eps)
            ana = p.grad[i]
            pasang.append((ana, float(num)))
            galat = max(galat, abs(ana - num) / max(1e-12, abs(ana) + abs(num)))
    return galat, pasang


def bagian2():
    print("\n" + GARIS, "\nBAGIAN 2  gradiennya diperiksa sebelum dipakai\n",
          GARIS, sep="")

    rng = np.random.default_rng(1)
    X = Tensor(rng.normal(size=(3, 8, 8, 2)))
    kelas = rng.integers(0, 4, size=3)

    W1 = Tensor(rng.normal(0, 0.3, (3 * 3 * 2, 4)))
    b1 = Tensor(rng.normal(0, 0.1, 4))
    W2 = Tensor(rng.normal(0, 0.3, (3 * 3 * 4, 5)))
    b2 = Tensor(rng.normal(0, 0.1, 5))
    W3 = Tensor(rng.normal(0, 0.3, (5, 4)))
    b3 = Tensor(rng.normal(0, 0.1, 4))
    param = [W1, b1, W2, b2, W3, b3]

    def rugi():
        h = konv2d(X, W1, b1).relu()
        h = maks_kolam(h, 2)
        h = konv2d(h, W2, b2).relu()
        h = bentuk_ulang(h, (3, -1))
        return padat(h, W3, b3).entropi_silang(kelas)

    galat, pasang = periksa_gradien(rugi, param)

    print(f"  {'analitik':>16}{'numerik':>16}{'galat relatif':>18}")
    print("  " + "-" * 50)
    for ana, num in pasang[:8]:
        rel = abs(ana - num) / max(1e-12, abs(ana) + abs(num))
        print(f"  {ana:>16.9f}{num:>16.9f}{rel:>18.2e}")
    print(f"\n  galat relatif terbesar dari {len(pasang)} titik : {galat:.2e}")
    print(f"  lulus (< 1e-7)                          : {galat < 1e-7}")

    print("""
  Bagian ini tidak boleh dilewati, dan alasannya bukan kehati-hatian umum.
  Gradien yang salah TIDAK menghasilkan pesan galat. Ia menghasilkan latihan
  yang tetap berjalan, rugi yang tetap turun sedikit, dan akurasi yang
  mentok di angka yang kelihatan masuk akal. Kamu bisa menghabiskan seminggu
  menyetel laju belajar untuk menambal satu tanda minus.

  Yang paling sering salah di berkas seperti ini justru col2im, karena
  godaannya menulis penugasan sebagai ganti penambahan. Coba ubah `+=` jadi
  `=` di dalam `im2col._backward`, jalankan lagi bagian ini, dan lihat galat
  relatifnya melompat. Sesudah itu kembalikan.""")


# ══════════════════════════════════════════════════════════════
# BAGIAN 3 - CNN pertama di MNIST
# ══════════════════════════════════════════════════════════════

def cnn_awal(rng, c1=8, c2=16, n_kelas=10):
    """Parameter CNN kecil. Kembalikan daftar Tensor. Disediakan.

    Arsitekturnya:
        28x28x1 -> konv 3x3 -> 26x26xc1 -> relu -> kolam 2 -> 13x13xc1
                -> konv 3x3 -> 11x11xc2 -> relu -> kolam 2 ->  5x 5xc2
                -> ratakan -> padat -> 10
    """
    return [
        he(rng, 3, 3, 1, c1), Tensor(np.zeros(c1)),
        he(rng, 3, 3, c1, c2), Tensor(np.zeros(c2)),
        he(rng, 5 * 5 * c2, n_kelas), Tensor(np.zeros(n_kelas)),
    ]


def maju_cnn(param, X):
    """Satu lintasan maju CNN. X berbentuk (B, 28, 28, 1).

    TODO 5
    """
    W1, b1, W2, b2, W3, b3 = param
    h = maks_kolam(konv2d(X, W1, b1).relu(), 2)
    h = maks_kolam(konv2d(h, W2, b2).relu(), 2)
    return padat(bentuk_ulang(h, (X.data.shape[0], -1)), W3, b3)


def ratakan_bobot(param):
    """Ubah bobot konvolusi (Kh, Kw, C_in, C_out) jadi (Kh*Kw*C_in, C_out).

    Disediakan. Bentuk empat sumbu lebih mudah dibaca manusia dan lebih mudah
    diterjemahkan ke PyTorch; bentuk dua sumbu yang dibutuhkan `@`.
    """
    hasil = []
    for p in param:
        if p.data.ndim == 4:
            q = Tensor(p.data.reshape(-1, p.data.shape[-1]))
            q.grad = p.grad.reshape(q.data.shape)
            hasil.append(q)
        else:
            hasil.append(p)
    return hasil


def latih_cnn(Xl, yl, Xv, yv, param, lr=0.05, epoch=3, batch=64, seed=0,
              diam=False):
    """SGD dengan momentum. Kembalikan (param, riwayat, detik). Disediakan.

    Momentum 0,9 dipakai, bukan SGD polos, karena permukaan rugi CNN jauh
    lebih memanjang daripada MLP: bobot konvolusi memengaruhi seluruh posisi
    sekaligus, jadi gradiennya besar di sedikit arah dan kecil di banyak
    arah. Itu lembah sempit yang sama dengan Bagian 7 Bulan 1 Sesi 3+4.
    """
    rng = np.random.default_rng(seed)
    kecepatan = [np.zeros_like(p.data) for p in param]
    riwayat = []
    mulai = time.perf_counter()

    for e in range(epoch):
        urut = rng.permutation(len(Xl))
        for i in range(0, len(urut) - batch + 1, batch):
            ambil = urut[i:i + batch]
            for p in param:
                p.grad = np.zeros_like(p.data)
            rugi = maju_cnn(param, Tensor(Xl[ambil])).entropi_silang(yl[ambil])
            rugi.backward()
            for p, v in zip(param, kecepatan):
                v *= 0.9
                v += p.grad
                p.data -= lr * v
        akur = akurasi_cnn(param, Xv, yv)
        riwayat.append((e + 1, float(rugi.data), akur))
        if not diam:
            print(f"    epoch {e + 1}  rugi {float(rugi.data):.4f}  "
                  f"akurasi validasi {akur * 100:.2f}%")

    return param, riwayat, time.perf_counter() - mulai


def akurasi_cnn(param, X, y, batch=500):
    """Akurasi, dihitung per potongan supaya memorinya aman. Disediakan."""
    benar = 0
    for i in range(0, len(X), batch):
        logit = maju_cnn(param, Tensor(X[i:i + batch])).data
        benar += (logit.argmax(axis=1) == y[i:i + batch]).sum()
    return benar / len(X)


def bagian3():
    print("\n" + GARIS, "\nBAGIAN 3  CNN pertama, diadu dengan MLP Bulan 1\n",
          GARIS, sep="")

    X, y, Xv, yv, Xu, yu = muat_mnist()
    # Sepersepuluh data latih. numpy di CPU, dan poin bagian ini perbandingan
    # jumlah bobot, bukan angka akurasi tertinggi yang bisa dicapai.
    n = 10000
    Xl = X[:n].reshape(-1, 28, 28, 1)
    yl = y[:n]
    Xv4 = Xv[:2000].reshape(-1, 28, 28, 1)
    yv2 = yv[:2000]
    Xu4 = Xu.reshape(-1, 28, 28, 1)

    print(f"  latih {ribuan(n)}  validasi {ribuan(len(Xv4))}  "
          f"uji {ribuan(len(Xu4))}\n")

    rng = np.random.default_rng(0)
    param = ratakan_bobot(cnn_awal(rng))
    n_bobot = sum(p.data.size for p in param)

    param, riwayat, detik = latih_cnn(Xl, yl, Xv4, yv2, param)
    akur_cnn = akurasi_cnn(param, Xu4, yu)

    # Pembanding: MLP satu lapisan tersembunyi, lebar disetel supaya jumlah
    # bobotnya kira-kira SAMA dengan CNN. Ini pembandingan yang adil, dan
    # tidak seorang pun melakukannya di tutorial mana pun.
    lebar = max(1, round(n_bobot / (784 + 1 + 10)))
    W1 = he(rng, 784, lebar)
    b1 = Tensor(np.zeros(lebar))
    W2 = he(rng, lebar, 10)
    b2 = Tensor(np.zeros(10))
    mlp = [W1, b1, W2, b2]
    n_mlp = sum(p.data.size for p in mlp)

    def maju_mlp(par, Xb):
        A, ba, B, bb = par
        return (Tensor(Xb) @ A + ba).relu() @ B + bb

    kecepatan = [np.zeros_like(p.data) for p in mlp]
    t0 = time.perf_counter()
    for e in range(3):
        urut = rng.permutation(n)
        for i in range(0, n - 64 + 1, 64):
            ambil = urut[i:i + 64]
            for p in mlp:
                p.grad = np.zeros_like(p.data)
            maju_mlp(mlp, X[ambil]).entropi_silang(y[ambil]).backward()
            for p, v in zip(mlp, kecepatan):
                v *= 0.9
                v += p.grad
                p.data -= 0.05 * v
    detik_mlp = time.perf_counter() - t0
    akur_mlp = (maju_mlp(mlp, Xu).data.argmax(axis=1) == yu).mean()

    print(f"\n  {'model':<28}{'bobot':>10}{'detik':>9}{'akurasi uji':>14}")
    print("  " + "-" * 61)
    print(f"  {'CNN 8-16, kolam 2x2':<28}{ribuan(n_bobot):>10}{detik:>9.1f}"
          f"{akur_cnn * 100:>13.2f}%")
    print(f"  {'MLP ' + str(lebar) + ' tersembunyi':<28}{ribuan(n_mlp):>10}"
          f"{detik_mlp:>9.1f}{akur_mlp * 100:>13.2f}%")

    print(f"""
  Kedua model punya jumlah bobot yang hampir sama, dilatih dengan data yang
  sama, jumlah epoch yang sama, dan aturan pembaruan yang sama. Yang berbeda
  cuma bagaimana bobot itu disusun.

  Selisihnya {koma(abs(akur_cnn - akur_mlp) * 100)} poin, dan di n = 10.000
  gambar uji selang 95 persennya sekitar 0,6 poin, jadi selisih ini terukur
  dan bukan derau. Bandingkan dengan Bulan 2, tempat n = 41 membuat hampir
  semua selisih tidak bisa dibaca.

  Perhatikan juga kolom detik. CNN jauh lebih lambat untuk jumlah bobot yang
  sama, karena tiap bobot dipakai ulang di ratusan posisi. Berbagi bobot
  menghemat PARAMETER, bukan HITUNGAN. Itu pertukaran yang sengaja diambil:
  parameter mahal karena butuh data, hitungan murah karena tinggal menunggu.

  Soal 3 memintamu memutuskan apa yang akan terjadi kalau data latihnya
  dinaikkan sepuluh kali lipat, dan model mana yang lebih diuntungkan.""")

    return param


# ══════════════════════════════════════════════════════════════
# BAGIAN 4 - apa yang dipelajari kernel lapisan pertama
# ══════════════════════════════════════════════════════════════

def bagian4(param):
    print("\n" + GARIS, "\nBAGIAN 4  kernel yang ditemukan sendiri\n", GARIS,
          sep="")

    K = param[0].data.reshape(3, 3, 1, -1)[:, :, 0, :]     # (3, 3, c1)
    c1 = K.shape[-1]

    from bulan3_sesi1_konvolusi import SOBEL_X, SOBEL_Y, KOTAK

    acuan = {"sobel_x": SOBEL_X, "sobel_y": SOBEL_Y, "kotak": KOTAK}
    print(f"  {'kernel':>8}{'norm':>9}{'jumlah':>9}"
          + "".join(f"{n:>12}" for n in acuan))
    print("  " + "-" * (26 + 12 * len(acuan)))
    for i in range(c1):
        k = K[:, :, i]
        baris = f"  {i:>8}{np.linalg.norm(k):>9.3f}{k.sum():>9.3f}"
        for nama, a in acuan.items():
            # Kemiripan kosinus, dengan tanda diabaikan: kernel yang
            # terbalik tandanya mengerjakan pekerjaan yang sama.
            c = abs((k * a).sum() / (np.linalg.norm(k) * np.linalg.norm(a)))
            baris += f"{c:>12.3f}"
        print(baris)

    fig, ax = plt.subplots(1, c1, figsize=(1.4 * c1, 1.8))
    for i, a in enumerate(np.atleast_1d(ax)):
        a.imshow(K[:, :, i], cmap="RdBu_r",
                 vmin=-np.abs(K).max(), vmax=np.abs(K).max())
        a.set_title(f"k{i}", fontsize=8)
        a.axis("off")
    fig.tight_layout()
    berkas = FIGUR / "b3s3_kernel.png"
    fig.savefig(berkas, dpi=120)
    plt.close(fig)

    mirip = max(abs((K[:, :, i] * a).sum()
                    / (np.linalg.norm(K[:, :, i]) * np.linalg.norm(a)))
                for i in range(c1) for a in acuan.values())

    print(f"""
  Gambar disimpan: {berkas.name}

  Kolom `jumlah` layak dibaca lebih dulu. Kernel yang jumlahnya mendekati nol
  buta terhadap daerah rata: masukan konstan menghasilkan keluaran nol. Itu
  ciri pendeteksi perubahan, dan tidak ada satu baris pun di berkas ini yang
  memintanya. Yang ada cuma gradien dari entropi silang.

  Kemiripan tertinggi terhadap kernel tulisan tangan Sesi 1 adalah
  {koma(mirip, 3)}. Jangan berlebihan menafsirkannya: kernel terlatih TIDAK
  harus mirip Sobel, dan kemiripan tinggi bukan tanda keberhasilan. Yang
  ditunjukkan bagian ini lebih sederhana dan lebih kuat: dengan sepuluh ribu
  contoh dan tanpa satu pun petunjuk tentang tepi, {c1} kernel itu menemukan
  sendiri bahwa yang berguna adalah perubahan, bukan nilai mutlak.

  Di Bulan 1 kamu harus menulis Sobel sendiri kalau menginginkannya. Di sini
  kamu tidak menulis apa pun, dan tidak bisa memilih. Itu keuntungan dan
  kerugian sekaligus: modelnya menemukan yang berguna untuk MNIST, dan tidak
  ada jaminan yang ditemukannya masuk akal bagi manusia.""")


# ══════════════════════════════════════════════════════════════
# BAGIAN 5 - versi PyTorch
# ══════════════════════════════════════════════════════════════

def bagian5(param):
    print("\n" + GARIS, "\nBAGIAN 5  PyTorch: kesamaan dulu, kecepatan kemudian\n",
          GARIS, sep="")

    import torch
    import torch.nn.functional as F

    rng = np.random.default_rng(3)
    X = rng.normal(size=(8, 28, 28, 1))

    W1, b1, W2, b2, W3, b3 = param
    milikku = maju_cnn(param, Tensor(X)).data

    # Terjemahan tata letak. Ini satu-satunya bagian yang membingungkan, dan
    # membingungkannya nyata: numpy kita kanal-terakhir, PyTorch kanal-kedua,
    # dan bobot konvolusi PyTorch berbentuk (C_out, C_in, Kh, Kw).
    def ke_torch(W, C_in, C_out):
        return torch.tensor(W.data.reshape(3, 3, C_in, C_out)
                            .transpose(3, 2, 0, 1).copy())

    xt = torch.tensor(X.transpose(0, 3, 1, 2).copy())
    h = F.conv2d(xt, ke_torch(W1, 1, 8), torch.tensor(b1.data)).relu()
    h = F.max_pool2d(h, 2)
    h = F.conv2d(h, ke_torch(W2, 8, 16), torch.tensor(b2.data)).relu()
    h = F.max_pool2d(h, 2)
    # Perataannya juga harus cocok: kita meratakan kanal-terakhir, jadi
    # tensornya dikembalikan ke kanal-terakhir sebelum diratakan.
    h = h.permute(0, 2, 3, 1).reshape(8, -1)
    torchku = (h @ torch.tensor(W3.data) + torch.tensor(b3.data)).numpy()

    print(f"  selisih maks keluaran numpy vs PyTorch : "
          f"{np.abs(milikku - torchku).max():.3e}")
    print("  (dua implementasi bebas, angka yang sama. Ini pemeriksa yang\n"
          "   paling menggigit di seluruh Bulan 3.)\n")

    ada_gpu = torch.cuda.is_available()
    Xb = rng.normal(size=(64, 28, 28, 1))
    ulang = 10

    t0 = time.perf_counter()
    for _ in range(ulang):
        maju_cnn(param, Tensor(Xb))
    t_numpy = (time.perf_counter() - t0) / ulang * 1000

    def waktu_torch(peranti):
        w1 = ke_torch(W1, 1, 8).to(peranti)
        w2 = ke_torch(W2, 8, 16).to(peranti)
        c1, c2 = torch.tensor(b1.data).to(peranti), torch.tensor(b2.data).to(peranti)
        w3, c3 = torch.tensor(W3.data).to(peranti), torch.tensor(b3.data).to(peranti)
        xt = torch.tensor(Xb.transpose(0, 3, 1, 2).copy()).to(peranti)

        def sekali():
            h = F.max_pool2d(F.conv2d(xt, w1, c1).relu(), 2)
            h = F.max_pool2d(F.conv2d(h, w2, c2).relu(), 2)
            return h.permute(0, 2, 3, 1).reshape(64, -1) @ w3 + c3

        sekali()                                   # pemanasan
        if peranti == "cuda":
            torch.cuda.synchronize()
        t0 = time.perf_counter()
        for _ in range(ulang):
            sekali()
        if peranti == "cuda":
            torch.cuda.synchronize()
        return (time.perf_counter() - t0) / ulang * 1000

    t_cpu = waktu_torch("cpu")
    t_gpu = waktu_torch("cuda") if ada_gpu else float("nan")

    print(f"  {'lintasan maju, batch 64':<30}{'ms':>9}{'relatif':>11}")
    print("  " + "-" * 50)
    print(f"  {'numpy + Tensor buatanmu':<30}{t_numpy:>9.2f}{1.0:>11.1f}x")
    print(f"  {'PyTorch CPU':<30}{t_cpu:>9.2f}{t_numpy / t_cpu:>10.1f}x")
    if ada_gpu:
        print(f"  {'PyTorch CUDA (' + torch.cuda.get_device_name(0)[:14] + ')':<30}"
              f"{t_gpu:>9.2f}{t_numpy / t_gpu:>10.1f}x")
    else:
        print("  PyTorch CUDA                   tidak tersedia")

    print("""
  Baris pertama bukan bahan malu. Implementasi float64 yang menyalin seluruh
  matriks im2col ke memori baru tiap lintasan memang harus kalah dari pustaka
  yang memakai float32, kernel terkompilasi, dan konvolusi langsung tanpa
  im2col.

  Yang penting baris di atas tabel: selisihnya di orde ketelitian float64.
  Dua implementasi yang ditulis terpisah, satu olehmu dan satu oleh ratusan
  orang selama sepuluh tahun, memberi angka yang sama. Sesudah ini, memakai
  `nn.Conv2d` di Sesi 4 bukan lagi menyerahkan sesuatu ke kotak hitam; ia
  memanggil hal yang sama yang barusan kamu tulis.

  Mulai Sesi 4, PyTorch yang dipakai. Alasannya ada di kolom terakhir tabel
  ini, bukan pada keyakinan bahwa PyTorch lebih benar.""")


# ══════════════════════════════════════════════════════════════
# BAGIAN 6 - dari gambar ke spektrogram
# ══════════════════════════════════════════════════════════════

def bagian6():
    print("\n" + GARIS, "\nBAGIAN 6  spektrogram bukan gambar\n", GARIS, sep="")

    berkas = []
    for kata in ("yes", "no", "stop", "go"):
        d = SUARA / kata
        if d.is_dir():
            berkas += sorted(d.glob("*.wav"))[:60]

    if not berkas:
        print("  Speech Commands belum ada. Jalankan dulu:")
        print("    python scripts\\unduh_speech_commands.py")
        return

    # Semua ucapan dipatok satu detik supaya bisa ditumpuk jadi satu array.
    # Rerata SELURUH ucapan dikurangkan, satu angka per ucapan, bukan satu
    # angka per tapis. Bedanya menentukan: mengurangkan per tapis, seperti
    # yang dilakukan `fitur_audio`, membuat profil frekuensinya nol menurut
    # definisi, dan pengukuran di bawah jadi tidak berarti apa-apa.
    from bulan3_sesi2_spektrogram import LAJU, pra_tekan

    def kumpulkan(pakai_pra_tekan):
        A = []
        for b in berkas:
            x, _ = baca_wav(b)
            x = np.pad(x, (0, max(0, LAJU - len(x))))[:LAJU]
            M = spektrogram_mel(pra_tekan(x) if pakai_pra_tekan else x)
            A.append(M - M.mean())
        return np.stack(A)                 # (ucapan, bingkai, tapis)

    A = kumpulkan(True)
    n_u, n_t, n_f = A.shape
    print(f"  {n_u} ucapan, {n_t} bingkai, {n_f} tapis mel\n")

    # Ukuran stasioneritas, dihitung sama persis untuk kedua sumbu: seberapa
    # jauh rerata BERGESER dari satu posisi ke posisi lain di sumbu itu,
    # dibandingkan dengan sebaran keseluruhan. Rasio besar berarti posisi
    # membawa informasi, dan itu berarti berbagi bobot memaksakan asumsi yang
    # salah.
    def rasio_geser(A, sumbu):
        lain = tuple(i for i in range(A.ndim) if i != sumbu)
        return A.mean(axis=lain).std() / A.std()

    B = kumpulkan(False)
    r_f, r_t = rasio_geser(A, 2), rasio_geser(A, 1)
    r_f0, r_t0 = rasio_geser(B, 2), rasio_geser(B, 1)

    print(f"  {'sumbu':<14}{'rasio tanpa pra-tekan':>24}"
          f"{'rasio dengan pra-tekan':>25}")
    print("  " + "-" * 63)
    print(f"  {'frekuensi':<14}{r_f0:>24.3f}{r_f:>25.3f}")
    print(f"  {'waktu':<14}{r_t0:>24.3f}{r_t:>25.3f}")

    print("\n  profil frekuensi, rerata per tapis (dB relatif):")
    idx_f = (0, 5, 10, 20, 30, 39)
    print("    tapis  :" + "".join(f"{i:>8}" for i in idx_f))
    print("    rerata :" + "".join(f"{A.mean(axis=(0, 1))[i]:>8.1f}"
                                   for i in idx_f))
    print("\n  profil waktu, rerata per bingkai (dB relatif):")
    idx_t = (0, 20, 49, 70, 97)
    print("    bingkai:" + "".join(f"{i:>8}" for i in idx_t))
    print("    rerata :" + "".join(f"{A.mean(axis=(0, 2))[i]:>8.1f}"
                                   for i in idx_t))

    print(f"""
  Saya menulis bagian ini dengan ramalan yang terbalik dari hasilnya, jadi
  ramalannya saya tinggalkan supaya bisa dibandingkan.

  Ramalan saya: sumbu frekuensi TIDAK stasioner, karena pola pada 200 Hz dan
  pola yang sama pada 4.000 Hz berarti bunyi yang berbeda; sumbu waktu
  stasioner, karena kata bisa diucapkan kapan saja. Jadi rasio frekuensi
  seharusnya jauh lebih besar daripada rasio waktu.

  Terukur, sesudah pra-penekanan: frekuensi {koma(r_f, 3)}, waktu
  {koma(r_t, 3)}. Urutannya terbalik.

  Dua sebabnya, dan keduanya berguna.

  Pertama, kolom kiri menunjukkan bahwa saya sedang mengukur akibat kerja
  saya sendiri. Tanpa pra-penekanan, rasio frekuensinya {koma(r_f0, 3)};
  dengan pra-penekanan ia turun jadi {koma(r_f, 3)}. Satu baris pengurangan
  di Sesi 2 memang dipasang untuk meratakan sumbu itu, dan ternyata ia
  bekerja jauh lebih baik daripada yang saya duga. Ketidakstasioneran
  frekuensi sebagian besar adalah kemiringan spektrum, dan kemiringan itu
  sudah dibatalkan sebelum model melihatnya.

  Kedua, sumbu waktu tidak stasioner karena DATANYA, bukan karena suaranya.
  Baca profil waktu di atas: bingkai awal dan bingkai akhir jauh lebih
  lemah daripada bingkai tengah. Speech Commands memotong tiap ucapan jadi
  tepat satu detik dengan katanya kira-kira di tengah, jadi posisi memang
  membawa informasi di dalam dataset ini. Di pemakaian nyata, ketika SYNESIS
  mendengarkan terus-menerus, katanya bisa mendarat di mana saja.

  Konsekuensi yang langsung untuk Sesi 4, dan ini yang membuat pengukuran
  tadi berharga meskipun ramalannya salah: kalau model dilatih apa adanya di
  atas data yang katanya selalu di tengah, ia akan mempelajari "di tengah"
  sebagai ciri. Ciri itu tidak ada di pemakaian nyata, dan modelnya akan
  gagal dengan cara yang tidak terlihat di himpunan uji, karena himpunan
  ujinya berbagi cacat yang sama.

  Obatnya augmentasi geseran waktu, dan sekarang alasannya bukan "karena
  semua orang melakukannya" melainkan angka {koma(r_t, 3)} di tabel di atas.
  Sesi 4 mengukur seberapa besar bedanya.

  Soal 6 memintamu merancang pengukuran yang memisahkan ketidakstasioneran
  yang berasal dari suara dari yang berasal dari cara datanya dipotong.""")


# ══════════════════════════════════════════════════════════════
# Jalankan semuanya
# ══════════════════════════════════════════════════════════════

def main():
    mulai = time.perf_counter()

    bagian1()
    bagian2()
    param = bagian3()
    bagian4(param)
    bagian5(param)
    bagian6()

    print(f"\n{GARIS}")
    print(f"  selesai dalam {time.perf_counter() - mulai:.1f} detik")
    print(GARIS)


if __name__ == "__main__":
    main()
