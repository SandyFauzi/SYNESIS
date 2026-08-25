"""Bulan 3 Sesi 1 - konvolusi: satu operasi, tiga wajah.

Jalankan:
    . .\\scripts\\activate.ps1
    python notebooks\\bulan3_sesi1_konvolusi.py

Bulan 2 berakhir dengan kesimpulan yang tidak menyenangkan: yang paling
kurang bukan representasi teks, melainkan catatan pemakaian yang mewakili.
Sementara `audit.jsonl` terisi sendiri, Bulan 3 menyerang pintu masuk yang
lain. Bukan teks yang kamu ketik, melainkan suara yang kamu ucapkan.

Suara adalah sinyal satu dimensi. Sebelum ada model yang bisa mengenalinya,
sinyal itu harus diubah jadi sesuatu yang punya struktur lokal, dan di situ
konvolusi masuk. Malam ini kamu belum menyentuh suara sama sekali. Malam ini
kamu membereskan operasinya dulu.

Kamu sudah mengenal konvolusi dari Fisika Matematika III, dalam bentuk

    (f * g)(t) = integral f(tau) g(t - tau) d tau

dan kamu sudah memakai teorema konvolusi untuk menghindari integral itu.
Yang belum pernah kamu lakukan adalah menuliskannya sebagai kode, mengukur
ongkosnya, lalu menemukan bahwa lapisan konvolusi pada CNN ternyata bukan
konvolusi.

Tujuh bagian:

    1  konvolusi 1D dari definisinya, dan tiga mode yang membingungkan
    2  teorema konvolusi, dan titik silang tempat FFT mulai menang
    3  konvolusi 2D pada satu digit MNIST dari Bulan 1
    4  korelasi silang, pembalikan kernel, dan istilah yang dipakai salah
    5  keterpisahan: kenapa Gaussian 2D bisa dikerjakan dua kali 1D
    6  im2col: konvolusi diubah jadi satu perkalian matriks
    7  cuplikan dan aliasing, jembatan ke spektrogram di Sesi 2

Nol pustaka baru. numpy untuk array, scipy untuk pembanding, matplotlib
untuk satu gambar. Bagian bertanda TODO kamu yang isi.
"""

import sys
import time
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))

GARIS = "=" * 66
FIGUR = Path(__file__).resolve().parent.parent / "figures"
FIGUR.mkdir(exist_ok=True)
GUDANG = Path(r"E:\SYNESIS\data")


def ribuan(n):
    """Pemisah ribuan gaya Indonesia: 529984 -> 529.984. Disediakan."""
    return f"{n:,}".replace(",", ".")


# ══════════════════════════════════════════════════════════════
# BAGIAN 1 - konvolusi 1D dari definisinya
# ══════════════════════════════════════════════════════════════

def konvolusi1d(x, h, mode="full"):
    """Konvolusi diskret dua sinyal, ditulis dari definisinya.

        y[n] = sum_k x[k] h[n - k]

    Perhatikan tanda minus di dalam indeks h. Itulah pembalikan yang
    membedakan konvolusi dari korelasi silang, dan Bagian 4 akan menunjukkan
    bahwa hampir semua orang yang menulis "convolutional layer" sebenarnya
    tidak melakukannya.

    Tiga mode, dan bedanya cuma bagian mana dari hasil penuh yang diambil:

        full  panjang N + K - 1. Seluruh tumpang tindih, termasuk yang cuma
              menyentuh satu ujung. Ini definisinya yang utuh.
        same  panjang N. Potongan tengah, supaya keluaran sepanjang masukan.
        valid panjang N - K + 1. Hanya posisi ketika kernel tertutup penuh
              oleh sinyal, jadi tidak ada satu pun angka yang dihitung dari
              nol imajiner di luar sinyal.

    Pilihan mode bukan selera. `valid` menyusutkan keluaran tiap lapisan, dan
    itulah alasan CNN dalam memakai padding. `full` memanjangkan sinyal, dan
    itu yang benar untuk tanggapan impuls. Soal 1 menghitung penyusutannya
    untuk tumpukan lapisan.

    TODO 1
    """
    x = np.asarray(x, dtype=np.float64)
    h = np.asarray(h, dtype=np.float64)
    N, K = len(x), len(h)

    penuh = np.zeros(N + K - 1)
    for n in range(N + K - 1):
        # k dibatasi supaya kedua indeks tetap di dalam arraynya
        awal = max(0, n - K + 1)
        akhir = min(n, N - 1)
        for k in range(awal, akhir + 1):
            penuh[n] += x[k] * h[n - k]

    if mode == "full":
        return penuh
    if mode == "valid":
        if N < K:
            return np.zeros(0)
        return penuh[K - 1:N]
    if mode == "same":
        mulai = (K - 1) // 2
        return penuh[mulai:mulai + N]
    raise ValueError(f"mode tidak dikenal: {mode}")


def bagian1():
    print(GARIS, "\nBAGIAN 1  konvolusi 1D dari definisinya\n", GARIS, sep="")

    rng = np.random.default_rng(0)
    x = rng.normal(size=12)
    h = np.array([0.25, 0.5, 0.25])          # penghalus tiga titik

    print("  Verifikasi terhadap numpy, tiga mode:\n")
    print(f"  {'mode':<8}{'panjang':>9}{'selisih maks':>16}")
    print("  " + "-" * 33)
    for mode in ("full", "same", "valid"):
        milikku = konvolusi1d(x, h, mode)
        numpy_ = np.convolve(x, h, mode)
        beda = np.abs(milikku - numpy_).max()
        print(f"  {mode:<8}{len(milikku):>9}{beda:>16.2e}")

    # Satu impuls masuk, kernel keluar. Ini bukan trik; ini definisi tanggapan
    # impuls, dan alasan kenapa sistem linear tak berubah waktu sepenuhnya
    # ditentukan oleh h.
    impuls = np.zeros(9)
    impuls[4] = 1.0
    keluar = konvolusi1d(impuls, h, "same")

    print(f"""
  Sifat yang perlu kamu pegang seumur hidup:

    impuls  {np.array2string(impuls, precision=2, separator=' ')}
    keluar  {np.array2string(keluar, precision=2, separator=' ')}

  Satu impuls masuk, kernelnya sendiri yang keluar. Itulah kenapa h disebut
  tanggapan impuls, dan kenapa mengukur tanggapan impuls sebuah ruangan sudah
  cukup untuk meramalkan bunyi apa pun di ruangan itu. Kamu akan memakai
  kenyataan ini lagi di Bulan 3 Sesi 4 waktu menambahkan derau ruangan ke
  data latih.

  Ongkosnya: dua gelung bersarang, jadi N kali K perkalian. Untuk N = 16.000
  cuplikan satu detik dan K = 400, itu 6,4 juta perkalian per detik audio.
  Bagian 2 menurunkannya.""")

    return x, h


# ══════════════════════════════════════════════════════════════
# BAGIAN 2 - teorema konvolusi
# ══════════════════════════════════════════════════════════════

def konvolusi_fft(x, h):
    """Konvolusi lewat ranah frekuensi. Kembalikan hasil mode 'full'.

    Teorema konvolusi yang kamu turunkan di Fisika Matematika III:

        F{f * g} = F{f} . F{g}

    Perkalian titik demi titik di ranah frekuensi sama dengan konvolusi di
    ranah waktu. Jadi: transformasikan keduanya, kalikan, kembalikan.

    Satu jebakan yang harus kamu sadari. DFT menganggap sinyalnya berulang
    selamanya, jadi perkalian di ranah frekuensi menghasilkan konvolusi
    MELINGKAR: ekor yang keluar di kanan masuk lagi dari kiri. Obatnya
    menambahkan nol sampai panjangnya paling sedikit N + K - 1, supaya ekor
    itu punya tempat mendarat dan tidak menabrak awal sinyal.

    Soal 2 memintamu menunjukkan kesalahan yang terjadi tanpa penambahan nol
    itu, dan menghitung berapa cuplikan pertama yang tercemar.

    TODO 2
    """
    x = np.asarray(x, dtype=np.float64)
    h = np.asarray(h, dtype=np.float64)
    n = len(x) + len(h) - 1
    # FFT paling cepat di panjang yang faktornya kecil. Naikkan ke pangkat 2
    # berikutnya; nol tambahan tidak mengubah hasil, cuma menambah ekor nol.
    n2 = 1 << (n - 1).bit_length()
    hasil = np.fft.irfft(np.fft.rfft(x, n2) * np.fft.rfft(h, n2), n2)
    return hasil[:n]


def bagian2():
    print("\n" + GARIS, "\nBAGIAN 2  teorema konvolusi dan titik silangnya\n",
          GARIS, sep="")

    rng = np.random.default_rng(1)
    x = rng.normal(size=1000)
    h = rng.normal(size=64)

    langsung = np.convolve(x, h, "full")
    lewat_fft = konvolusi_fft(x, h)
    print(f"  selisih maks langsung vs FFT : "
          f"{np.abs(langsung - lewat_fft).max():.3e}")
    print("  (bukan nol, karena FFT bekerja di bilangan pecahan, tapi sekitar\n"
          "   batas ketelitian float64. Ini kesamaan, bukan hampiran.)\n")

    # Konvolusi melingkar tanpa penambahan nol: buktinya, bukan ceritanya.
    n = len(x)
    melingkar = np.fft.irfft(np.fft.rfft(x, n) * np.fft.rfft(h, n), n)
    tercemar = np.abs(melingkar - langsung[:n]) > 1e-9
    print(f"  tanpa penambahan nol, cuplikan tercemar : "
          f"{tercemar.sum()} dari {n} pertama")
    print(f"  seharusnya persis K - 1                 : {len(h) - 1}\n")

    print(f"  {'N':>8}{'K':>6}{'langsung (ms)':>16}{'FFT (ms)':>12}"
          f"{'rasio':>9}")
    print("  " + "-" * 51)
    for N in (1024, 4096, 16384, 65536):
        for K in (16, 128, 1024):
            a = rng.normal(size=N)
            b = rng.normal(size=K)
            t0 = time.perf_counter()
            np.convolve(a, b, "full")
            t_langsung = (time.perf_counter() - t0) * 1000
            t0 = time.perf_counter()
            konvolusi_fft(a, b)
            t_fft = (time.perf_counter() - t0) * 1000
            print(f"  {N:>8}{K:>6}{t_langsung:>16.3f}{t_fft:>12.3f}"
                  f"{t_langsung / t_fft:>9.2f}")

    print("""
  Bacalah kolom rasio, bukan kolom waktu. Rasio di bawah 1 berarti cara
  langsung masih menang. Kernel pendek tetap murah dikerjakan langsung
  seberapa pun panjang sinyalnya, karena ongkosnya N kali K, dan K yang kecil
  membuat konstantanya kecil. FFT membayar N log N di muka untuk KEDUA
  sinyal, dan biaya di muka itu baru terbayar kalau K cukup besar.

  Konsekuensi untuk Bulan 3: kernel CNN kita nanti 3 sampai 9 titik. Sekecil
  itu, FFT tidak pernah menang, dan itulah kenapa tidak ada satu pun framework
  deep learning yang mengerjakan konvolusi lapisannya lewat FFT. Yang mereka
  pakai justru Bagian 6.

  Soal 2 memintamu menurunkan titik silangnya secara analitik dan membandingkan
  dengan tabel di atas.""")


# ══════════════════════════════════════════════════════════════
# BAGIAN 3 - konvolusi 2D pada digit MNIST
# ══════════════════════════════════════════════════════════════

def muat_digit():
    """Satu gambar MNIST 28x28. Disediakan.

    Dipakai lagi dari Bulan 1 Sesi 3+4, tanpa mengunduh apa pun. Kalau
    berkasnya belum ada, kembalikan kotak sintetis supaya sesi ini tetap
    jalan di mesin lain.
    """
    simpan = GUDANG / "mnist.npz"
    if simpan.exists():
        d = np.load(simpan)
        return d["X"][0].reshape(28, 28), int(d["y"][0])
    g = np.zeros((28, 28))
    g[8:20, 8:20] = 1.0
    g[11:17, 11:17] = 0.0
    return g, -1


def konvolusi2d(g, k, mode="valid"):
    """Konvolusi dua dimensi, dari definisinya.

        y[i, j] = sum_u sum_v g[u, v] k[i - u, j - v]

    Sama seperti 1D, cuma indeksnya dua. Tulis dengan empat gelung bersarang.
    Lambat, dan memang harus lambat: Bagian 5 dan 6 baru berarti kalau kamu
    sudah punya angka lambatnya sebagai pembanding.

    Mode 'valid' saja yang wajib. Mode 'same' boleh kamu tambahkan sendiri
    dengan menambahkan nol di keempat sisi.

    TODO 3
    """
    g = np.asarray(g, dtype=np.float64)
    k = np.asarray(k, dtype=np.float64)
    H, W = g.shape
    Kh, Kw = k.shape

    if mode == "same":
        g = np.pad(g, ((Kh // 2, Kh // 2), (Kw // 2, Kw // 2)))
        H, W = g.shape

    keluar = np.zeros((H - Kh + 1, W - Kw + 1))
    k_balik = k[::-1, ::-1]                  # pembalikan dua sumbu
    for i in range(keluar.shape[0]):
        for j in range(keluar.shape[1]):
            keluar[i, j] = (g[i:i + Kh, j:j + Kw] * k_balik).sum()
    return keluar


SOBEL_X = np.array([[-1.0, 0.0, 1.0],
                    [-2.0, 0.0, 2.0],
                    [-1.0, 0.0, 1.0]])
SOBEL_Y = SOBEL_X.T
KOTAK = np.ones((3, 3)) / 9.0
TAJAM = np.array([[0.0, -1.0, 0.0],
                  [-1.0, 5.0, -1.0],
                  [0.0, -1.0, 0.0]])


def bagian3():
    print("\n" + GARIS, "\nBAGIAN 3  konvolusi 2D pada satu digit MNIST\n",
          GARIS, sep="")

    g, label = muat_digit()
    print(f"  gambar : {g.shape}, label {label}\n")

    kernel = {"sobel_x": SOBEL_X, "sobel_y": SOBEL_Y,
              "kotak": KOTAK, "tajam": TAJAM}

    from scipy.signal import convolve2d      # pembanding, bukan alat kerja

    print(f"  {'kernel':<10}{'bentuk keluar':>16}{'selisih vs scipy':>20}"
          f"{'|tanggapan| maks':>20}")
    print("  " + "-" * 66)
    hasil = {}
    for nama, k in kernel.items():
        milikku = konvolusi2d(g, k, "valid")
        acuan = convolve2d(g, k, mode="valid")
        hasil[nama] = milikku
        print(f"  {nama:<10}{str(milikku.shape):>16}"
              f"{np.abs(milikku - acuan).max():>20.2e}"
              f"{np.abs(milikku).max():>20.3f}")

    tepi = np.hypot(hasil["sobel_x"], hasil["sobel_y"])

    fig, ax = plt.subplots(1, 6, figsize=(15, 2.8))
    for a, (judul, arr) in zip(ax, [("asli", g), ("sobel x", hasil["sobel_x"]),
                                    ("sobel y", hasil["sobel_y"]),
                                    ("besar tepi", tepi),
                                    ("kotak", hasil["kotak"]),
                                    ("tajam", hasil["tajam"])]):
        a.imshow(arr, cmap="gray")
        a.set_title(judul, fontsize=9)
        a.axis("off")
    fig.tight_layout()
    berkas = FIGUR / "b3s1_konvolusi2d.png"
    fig.savefig(berkas, dpi=110)
    plt.close(fig)

    print(f"""
  Gambar disimpan: {berkas.name}

  Empat kernel di atas ditulis tangan oleh manusia, dan tiga di antaranya
  punya nama karena seseorang di tahun 1968 memutuskan angkanya. Yang perlu
  kamu perhatikan: kernel sobel_x menyala di tepi tegak dan buta terhadap
  tepi datar, sedangkan sobel_y kebalikannya. Tidak ada yang memberi tahu
  mereka apa itu tepi. Yang membuatnya bekerja cuma susunan tanda: negatif
  di satu sisi, positif di sisi lain, jadi daerah rata saling menghapus dan
  hanya perubahan yang tersisa.

  Seluruh gagasan CNN adalah berhenti menulis angka itu tangan. Di Sesi 3,
  sembilan angka yang sama akan diturunkan dari gradien, dan kamu akan
  melihat model menemukan pendeteksi tepi sendiri tanpa pernah diberi tahu
  bahwa tepi itu ada.

  Ongkos berbagi bobot, sekali lagi dengan angka. Lapisan padat dari 28 kali
  28 ke 26 kali 26 butuh {ribuan(28 * 28 * 26 * 26)} bobot. Satu kernel 3 kali 3
  yang disapukan butuh 9. Perbandingannya {ribuan(28 * 28 * 26 * 26 // 9)} banding 1,
  dan model dengan bobot lebih sedikit butuh contoh lebih sedikit untuk
  dilatih. Itu bukan penghematan memori; itu penghematan data.""")

    return g


# ══════════════════════════════════════════════════════════════
# BAGIAN 4 - korelasi silang, dan istilah yang dipakai salah
# ══════════════════════════════════════════════════════════════

def korelasi2d(g, k):
    """Korelasi silang: kernel digeser tanpa dibalik.

        y[i, j] = sum_u sum_v g[i + u, j + v] k[u, v]

    Bandingkan dengan konvolusi2d. Satu-satunya beda adalah baris pembalikan
    yang tidak ada di sini. Tulis versi 'valid' saja.

    TODO 4
    """
    g = np.asarray(g, dtype=np.float64)
    k = np.asarray(k, dtype=np.float64)
    Kh, Kw = k.shape
    keluar = np.zeros((g.shape[0] - Kh + 1, g.shape[1] - Kw + 1))
    for i in range(keluar.shape[0]):
        for j in range(keluar.shape[1]):
            keluar[i, j] = (g[i:i + Kh, j:j + Kw] * k).sum()
    return keluar


def bagian4(g):
    print("\n" + GARIS, "\nBAGIAN 4  konvolusi bukan yang dipakai CNN\n",
          GARIS, sep="")

    print(f"  {'kernel':<10}{'simetris?':>12}{'konv == korel?':>17}"
          f"{'selisih maks':>16}")
    print("  " + "-" * 55)
    for nama, k in (("sobel_x", SOBEL_X), ("kotak", KOTAK), ("tajam", TAJAM)):
        simetris = np.allclose(k, k[::-1, ::-1])
        beda = np.abs(konvolusi2d(g, k) - korelasi2d(g, k)).max()
        print(f"  {nama:<10}{str(simetris):>12}{str(beda < 1e-12):>17}"
              f"{beda:>16.3f}")

    print(f"""
  Baris sobel_x adalah seluruh isi bagian ini. Kernelnya antisimetris, jadi
  membaliknya membalik tandanya, dan hasil korelasinya persis negatif hasil
  konvolusinya. Selisih {np.abs(konvolusi2d(g, SOBEL_X) - korelasi2d(g, SOBEL_X)).max():.2f}
  itu bukan galat; itu dua operasi yang memang berbeda.

  Sekarang bagian yang perlu dinyatakan terang-terangan, karena hampir semua
  tulisan mengenai deep learning melewatkannya. `nn.Conv2d` di PyTorch,
  `Conv2D` di Keras, dan lapisan yang akan kamu tulis di Sesi 3 semuanya
  mengerjakan KORELASI SILANG, bukan konvolusi. Pembalikannya tidak ada.

  Apakah itu masalah? Tidak, dan alasannya tepat satu kalimat: kernelnya
  dipelajari, jadi model tinggal mempelajari versi terbaliknya dan hasilnya
  identik. Yang dilanggar cuma penamaannya, dan penamaan yang keliru itu
  merugikan hanya kalau kamu mencoba menyambungkannya ke teorema konvolusi
  dari Fisika Matematika III. Di situ pembalikannya wajib, karena teorema
  itu tidak berlaku untuk korelasi apa adanya.

  Soal 4 memintamu menurunkan padanan teorema konvolusi untuk korelasi
  silang, dan menyebutkan di mana konjugat kompleksnya muncul.""")


# ══════════════════════════════════════════════════════════════
# BAGIAN 5 - keterpisahan
# ══════════════════════════════════════════════════════════════

def gaussian1d(sigma, radius=None):
    """Kernel Gaussian satu dimensi, ternormalisasi. Disediakan."""
    if radius is None:
        radius = int(3 * sigma)
    n = np.arange(-radius, radius + 1)
    k = np.exp(-(n ** 2) / (2 * sigma ** 2))
    return k / k.sum()


def bagian5(g):
    print("\n" + GARIS, "\nBAGIAN 5  keterpisahan: K^2 jadi 2K\n", GARIS,
          sep="")

    print(f"  {'sigma':>7}{'K':>5}{'2D (ms)':>11}{'dua kali 1D (ms)':>19}"
          f"{'selisih':>12}{'rasio':>9}")
    print("  " + "-" * 63)

    besar = np.pad(g, 40, mode="reflect")     # 108x108, supaya waktunya terukur
    for sigma in (1.0, 2.0, 4.0, 8.0):
        k1 = gaussian1d(sigma)
        K = len(k1)
        k2 = np.outer(k1, k1)                 # inilah keterpisahannya

        from scipy.signal import convolve2d
        t0 = time.perf_counter()
        a = convolve2d(besar, k2, mode="valid")
        t_2d = (time.perf_counter() - t0) * 1000

        t0 = time.perf_counter()
        # Baris dulu, lalu kolom. Dua sapuan 1D, bukan satu sapuan 2D.
        antara = convolve2d(besar, k1[None, :], mode="valid")
        b = convolve2d(antara, k1[:, None], mode="valid")
        t_1d = (time.perf_counter() - t0) * 1000

        print(f"  {sigma:>7.1f}{K:>5}{t_2d:>11.3f}{t_1d:>19.3f}"
              f"{np.abs(a - b).max():>12.2e}{t_2d / t_1d:>9.2f}")

    print("""
  Kolom selisih memastikan keduanya menghitung hal yang sama, dan kolom
  rasio menunjukkan harganya. Sebabnya aljabar, bukan trik pemrograman:
  kalau kernel 2D bisa ditulis sebagai hasil kali luar dua vektor,

      k2 = k1 (x) k1  ->  g * k2 = (g * k1_baris) * k1_kolom

  maka ongkos per piksel turun dari K^2 jadi 2K. Untuk K = 25 itu 625 jadi
  50. Syaratnya bisa diperiksa dengan satu perintah: kernel yang terpisah
  selalu berperingkat satu.

  Kenapa ini masuk ke Bulan 3 dan bukan sekadar catatan kaki: spektrogram
  yang kamu bangun di Sesi 2 berbentuk matriks waktu kali frekuensi, dan
  banyak kernel yang berguna di sana memang terpisah, karena struktur waktu
  dan struktur frekuensi tidak saling bergantung. Kernel 1 kali 7 di sumbu
  waktu dan 7 kali 1 di sumbu frekuensi mengerjakan pekerjaan yang berbeda,
  dan memisahkannya bukan cuma lebih murah, melainkan lebih mudah dibaca.

  Soal 5 memintamu memeriksa peringkat SOBEL_X dan memutuskan apakah ia
  terpisah.""")


# ══════════════════════════════════════════════════════════════
# BAGIAN 6 - im2col
# ══════════════════════════════════════════════════════════════

def im2col(g, Kh, Kw):
    """Susun setiap petak Kh x Kw jadi satu baris matriks.

    Kembalikan matriks berbentuk (jumlah_posisi, Kh * Kw).

    Ini gagasan yang membuat konvolusi cepat di perangkat keras nyata, dan
    gagasannya sederhana sampai terasa curang: kalau setiap posisi kernel
    cuma menghitung satu hasil kali dalam, maka menyusun semua petak jadi
    baris mengubah seluruh konvolusi jadi SATU perkalian matriks. Dan
    perkalian matriks adalah operasi yang sudah dioptimalkan orang selama
    lima puluh tahun.

    Harganya memori. Tiap piksel disalin sebanyak Kh kali Kw kali, jadi
    matriksnya jauh lebih besar daripada gambarnya. Soal 6 menghitung
    pelipatannya untuk masukan Sesi 4.

    Tulis dengan gelung yang mengisi kolom, bukan baris; ada Kh kali Kw
    kolom dan biasanya jauh lebih banyak posisi, jadi jumlah putaran
    gelungnya kecil.

    TODO 5
    """
    g = np.asarray(g, dtype=np.float64)
    H, W = g.shape
    Th, Tw = H - Kh + 1, W - Kw + 1
    kolom = np.empty((Th * Tw, Kh * Kw))
    for u in range(Kh):
        for v in range(Kw):
            kolom[:, u * Kw + v] = g[u:u + Th, v:v + Tw].reshape(-1)
    return kolom


def konvolusi_im2col(g, kernel_list):
    """Konvolusikan g dengan BANYAK kernel sekaligus, satu perkalian matriks.

    kernel_list : array (C, Kh, Kw)
    kembalikan  : array (C, Th, Tw)

    TODO 6
    """
    kernel_list = np.asarray(kernel_list, dtype=np.float64)
    C, Kh, Kw = kernel_list.shape
    Th, Tw = g.shape[0] - Kh + 1, g.shape[1] - Kw + 1
    kolom = im2col(g, Kh, Kw)                       # (Th*Tw, Kh*Kw)
    W = kernel_list.reshape(C, Kh * Kw).T           # (Kh*Kw, C)
    return (kolom @ W).T.reshape(C, Th, Tw)


def bagian6(g):
    print("\n" + GARIS, "\nBAGIAN 6  im2col: konvolusi jadi perkalian matriks\n",
          GARIS, sep="")

    bank = np.stack([SOBEL_X, SOBEL_Y, KOTAK, TAJAM])
    hasil = konvolusi_im2col(g, bank)
    acuan = np.stack([korelasi2d(g, k) for k in bank])
    print(f"  selisih vs korelasi bergelung : {np.abs(hasil - acuan).max():.2e}")
    print("  (im2col mengerjakan KORELASI, bukan konvolusi. Sesuai Bagian 4,\n"
          "   dan sesuai yang dilakukan setiap framework.)\n")

    besar = np.pad(g, 50, mode="reflect")
    C = 16
    rng = np.random.default_rng(2)
    bank_besar = rng.normal(size=(C, 3, 3))

    t0 = time.perf_counter()
    for k in bank_besar:
        korelasi2d(besar, k)
    t_gelung = (time.perf_counter() - t0) * 1000

    t0 = time.perf_counter()
    konvolusi_im2col(besar, bank_besar)
    t_im2col = (time.perf_counter() - t0) * 1000

    memori = im2col(besar, 3, 3).nbytes / besar.nbytes

    print(f"  masukan {besar.shape}, {C} kernel 3x3\n")
    print(f"  {'cara':<26}{'waktu (ms)':>13}")
    print("  " + "-" * 39)
    print(f"  {'gelung Python per kernel':<26}{t_gelung:>13.2f}")
    print(f"  {'im2col + satu matmul':<26}{t_im2col:>13.2f}")
    print(f"  {'percepatan':<26}{t_gelung / t_im2col:>12.1f}x")
    print(f"\n  harga memorinya: matriks kolom {memori:.1f}x lebih besar "
          f"daripada gambarnya\n  (persis Kh kali Kw = 9, dikurangi sedikit "
          f"karena tepi tidak ikut)")

    print("""
  Simpan bagian ini baik-baik, karena Sesi 3 berdiri seluruhnya di atasnya.
  Kelas `Tensor` dari Bulan 1 cuma punya empat operasi: perkalian matriks,
  penjumlahan, ReLU, dan entropi silang. Kalau konvolusi bisa ditulis sebagai
  perkalian matriks, maka lapisan konvolusi bisa dilatih dengan mesin autograd
  yang sudah kamu punya, tanpa satu pun aturan turunan baru untuk konvolusi
  itu sendiri.

  Yang perlu ditambahkan di Sesi 3 cuma jalan pulangnya, yaitu col2im, dan
  itu bukan aturan turunan baru melainkan penjumlahan salinan yang tadi
  dibuat oleh im2col. Soal 6 memintamu menurunkannya sekarang, di kertas,
  sebelum menulis kodenya minggu depan.""")


# ══════════════════════════════════════════════════════════════
# BAGIAN 7 - cuplikan dan aliasing
# ══════════════════════════════════════════════════════════════

def bagian7():
    print("\n" + GARIS, "\nBAGIAN 7  cuplikan, Nyquist, dan lipatan\n", GARIS,
          sep="")

    fs = 1000.0                      # laju cuplik, Hz
    n = np.arange(200)
    t = n / fs

    print(f"  laju cuplik {fs:.0f} Hz, jadi batas Nyquist "
          f"{fs / 2:.0f} Hz\n")
    print(f"  {'f asli (Hz)':>13}{'f terlihat (Hz)':>18}"
          f"{'selisih cuplikan':>19}")
    print("  " + "-" * 50)
    for f in (100.0, 400.0, 600.0, 900.0, 1100.0):
        # Frekuensi yang benar-benar terlihat setelah dicuplik: lipat ke
        # dalam selang [0, fs/2] dengan pantulan di 0 dan di fs/2.
        sisa = f % fs
        terlihat = sisa if sisa <= fs / 2 else fs - sisa
        beda = np.abs(np.sin(2 * np.pi * f * t)
                      - np.sin(2 * np.pi * terlihat * t)).max()
        # tanda ikut terbalik untuk lipatan di atas Nyquist
        beda_tanda = np.abs(np.sin(2 * np.pi * f * t)
                            + np.sin(2 * np.pi * terlihat * t)).max()
        print(f"  {f:>13.0f}{terlihat:>18.0f}"
              f"{min(beda, beda_tanda):>19.2e}")

    print(f"""
  Kolom terakhir nol sampai batas ketelitian float. Itu bukan hampiran: sinus
  600 Hz yang dicuplik pada 1000 Hz MENGHASILKAN barisan angka yang identik
  dengan sinus 400 Hz. Tidak ada algoritma, tidak ada model, dan tidak ada
  jumlah data yang bisa memisahkan keduanya sesudah pencuplikan, karena
  informasinya sudah tidak ada di dalam angkanya.

  Inilah alasan tapis anti-aliasing dipasang SEBELUM pengubah analog ke
  digital, bukan sesudah. Di praktikum, ini kesalahan yang sama dengan
  membaca osiloskop pada laju sapuan yang terlalu rendah lalu melaporkan
  frekuensi yang salah dengan yakin.

  Angka yang dipakai Bulan 3: mikrofon kita mencuplik 16.000 Hz, jadi batas
  Nyquistnya 8.000 Hz. Suara manusia menaruh hampir seluruh tenaga yang
  berguna untuk pengenalan kata di bawah 8.000 Hz, jadi 16 kHz cukup dan
  itulah kenapa hampir semua model pengenal suara memakai angka itu. Musik
  memakai 44.100 Hz karena telinga mendengar sampai sekitar 20 kHz.

  Sesi 2 mulai dari sini: sinyal 16 kHz dipotong jadi bingkai pendek, tiap
  bingkai ditransformasi Fourier, dan hasilnya ditumpuk jadi gambar
  waktu-frekuensi. Setelah itu suara jadi soal konvolusi 2D, dan seluruh isi
  malam ini berlaku apa adanya.""")


# ══════════════════════════════════════════════════════════════
# Jalankan semuanya
# ══════════════════════════════════════════════════════════════

def main():
    mulai = time.perf_counter()

    bagian1()
    bagian2()
    g = bagian3()
    bagian4(g)
    bagian5(g)
    bagian6(g)
    bagian7()

    print(f"\n{GARIS}")
    print(f"  selesai dalam {time.perf_counter() - mulai:.1f} detik")
    print(GARIS)


if __name__ == "__main__":
    main()
