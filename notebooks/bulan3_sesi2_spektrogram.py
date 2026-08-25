"""Bulan 3 Sesi 2 - suara jadi gambar: spektrogram dan MFCC dari nol.

Jalankan:
    . .\\scripts\\activate.ps1
    python notebooks\\bulan3_sesi2_spektrogram.py

Sesi 1 berhenti tepat sebelum suara. Malam ini suaranya masuk.

Satu detik audio pada 16.000 Hz adalah 16.000 angka berurutan, dan barisan
angka itu hampir tidak bisa dipakai apa adanya. Dua rekaman kata "yes" yang
diucapkan orang yang sama, digeser lima milidetik saja, menghasilkan dua
vektor 16.000 dimensi yang jaraknya jauh. Yang sama di antara keduanya bukan
nilai cuplikannya, melainkan bagaimana isi frekuensinya berubah terhadap
waktu.

Jadi seluruh isi malam ini satu kalimat: ubah sinyal satu dimensi jadi
gambar dua dimensi yang sumbunya waktu dan frekuensi, lalu Bulan 3 berubah
jadi soal penglihatan komputer yang sudah kamu punya alatnya sejak Sesi 1.

Tujuh bagian:

    1  berkas WAV dibaca dengan pustaka bawaan Python, tanpa librosa
    2  DFT dari definisinya, lalu bukti kenapa tidak ada yang memakainya
    3  bingkai dan jendela: kebocoran spektral, diukur dalam desibel
    4  STFT, spektrogram, dan pertukaran resolusi waktu lawan frekuensi
    5  bank tapis mel dari nol, dan kenapa sumbunya bukan linear
    6  MFCC: logaritma, DCT, dan dekorelasi yang bisa diukur
    7  delta dan normalisasi, lalu fiturnya dibekukan untuk Sesi 4

Pustaka baru: nol. `wave` bawaan Python untuk membaca WAV, numpy untuk
sisanya, scipy hanya sebagai pembanding. librosa sengaja tidak dipakai, dan
alasannya bukan kemurnian: fungsi yang kamu tulis malam ini akan dipasang ke
`synesis/suara.py` di Sesi 5, dan paket yang menyeret numba dan soundfile
tidak sepadan untuk tujuh puluh baris matematika.

Bagian bertanda TODO kamu yang isi.
"""

import sys
import time
import wave
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))

GARIS = "=" * 66
FIGUR = Path(__file__).resolve().parent.parent / "figures"
FIGUR.mkdir(exist_ok=True)
SUARA = Path(r"E:\SYNESIS\data\speech_commands")

# Tetapan yang dipakai sepanjang Bulan 3. Angkanya bukan selera.
LAJU = 16000            # Hz. Alasannya di Soal 7 Sesi 1.
BINGKAI = 400           # 25 ms. Cukup panjang untuk memuat satu periode
                        # nada dasar suara pria (80 Hz -> 12,5 ms), cukup
                        # pendek supaya isi frekuensinya belum sempat
                        # berubah banyak.
LONCAT = 160            # 10 ms. Bingkai bertumpang tindih 60 persen.
N_FFT = 512             # pangkat dua terdekat di atas BINGKAI.
N_MEL = 40              # jumlah tapis mel.
N_MFCC = 13             # koefisien yang disimpan, dari 40 yang dihasilkan.
PRA_TEKAN = 0.97        # koefisien pra-penekanan, Bagian 1.


def ribuan(n):
    """Pemisah ribuan gaya Indonesia: 16000 -> 16.000. Disediakan."""
    return f"{n:,.0f}".replace(",", ".")


def koma(x, n=1):
    """Koma desimal gaya Indonesia untuk prosa: 2.9 -> 2,9. Disediakan."""
    return f"{x:.{n}f}".replace(".", ",")


def bilah(i, n, label="", lebar=32, mulai=None):
    """Bilah kemajuan satu baris di terminal. Disediakan.

    Sengaja tidak memakai tqdm. Yang dibutuhkan cuma satu baris yang ditimpa
    ulang dengan carriage return, dan itu delapan baris kode; menambah
    dependensi untuk delapan baris tidak sepadan.

    mulai : nilai time.perf_counter() saat gelungnya dimulai. Kalau diisi,
            sisa waktunya ikut ditaksir dari laju rata-rata sejauh ini.
    """
    i = min(i, n)
    isi = int(lebar * i / max(1, n))
    sisa = ""
    if mulai is not None and i:
        lewat = time.perf_counter() - mulai
        taksir = lewat / i * (n - i)
        sisa = f"  {lewat:5.0f}s lewat, sisa ~{taksir:4.0f}s"
    akhir = "\n" if i >= n else ""
    print(f"\r  {label:<22}|{'#' * isi}{'.' * (lebar - isi)}| "
          f"{i:>7}/{n}{sisa}   ", end=akhir, flush=True)


# ══════════════════════════════════════════════════════════════
# BAGIAN 1 - membaca WAV tanpa pustaka pihak ketiga
# ══════════════════════════════════════════════════════════════

def baca_wav(berkas):
    """Baca WAV PCM 16 bit mono. Kembalikan (sinyal float64, laju cuplik).

    Modul `wave` sudah ada di Python sejak selamanya dan tidak perlu
    dipasang. Ia mengembalikan byte mentah, jadi tugas kita cuma
    menafsirkannya.

    Dua hal yang harus dikerjakan dan gampang dilupakan:

        1  int16 bertanda, jangkauannya -32768 sampai 32767. Bagi 32768
           supaya sinyalnya mendarat di [-1, 1). Membagi 32767 juga sering
           dilihat orang, dan bedanya di bawah ketelitian yang mana pun.
        2  kalau kanalnya lebih dari satu, cuplikannya berselang-seling
           kiri-kanan-kiri-kanan. Rata-ratakan jadi mono.

    TODO 1
    """
    with wave.open(str(berkas), "rb") as w:
        n_kanal = w.getnchannels()
        lebar = w.getsampwidth()
        laju = w.getframerate()
        mentah = w.readframes(w.getnframes())

    if lebar != 2:
        raise ValueError(f"cuma PCM 16 bit yang didukung, ini {lebar * 8} bit")

    x = np.frombuffer(mentah, dtype="<i2").astype(np.float64) / 32768.0
    if n_kanal > 1:
        x = x.reshape(-1, n_kanal).mean(axis=1)
    return x, laju


def tulis_wav(berkas, x, laju=LAJU):
    """Kebalikan baca_wav. Dipakai Sesi 5 untuk menyimpan rekaman. Disediakan."""
    d = (np.clip(x, -1.0, 1.0) * 32767).astype("<i2")
    with wave.open(str(berkas), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(laju)
        w.writeframes(d.tobytes())


def pra_tekan(x, a=PRA_TEKAN):
    """Tapis lolos-tinggi satu tap: y[n] = x[n] - a x[n-1].

    Tenaga suara manusia turun kira-kira 6 dB per oktaf karena bentuk pulsa
    pita suara. Akibatnya frekuensi tinggi, tempat formant kedua dan ketiga
    berada, jauh lebih lemah daripada nada dasarnya, dan sesudah logaritma di
    Bagian 6 selisih itu berubah jadi selisih tetap yang membebani seluruh
    fitur.

    Tapis ini menaikkan sisi tinggi kira-kira 6 dB per oktaf, jadi ia
    membatalkan kemiringan itu. Ongkosnya satu pengurangan per cuplikan.

    Perhatikan bahwa ini konvolusi dengan kernel [1, -a], jadi seluruh isi
    Sesi 1 berlaku, termasuk pertanyaan tentang cuplikan pertama.

    TODO 2
    """
    return np.append(x[0], x[1:] - a * x[:-1])


def contoh_ucapan():
    """Satu rekaman kata dari Speech Commands, atau sintetis kalau belum ada.

    Disediakan. Sintetisnya bukan pengganti yang setara; ia cuma menjaga sesi
    ini tetap jalan sebelum unduhannya selesai.
    """
    for kata in ("yes", "no", "stop"):
        d = SUARA / kata
        if d.is_dir():
            wavs = sorted(d.glob("*.wav"))
            if wavs:
                x, laju = baca_wav(wavs[0])
                return x, laju, f"{kata}/{wavs[0].name}"

    # Vokal buatan: nada dasar 120 Hz plus tiga formant, diamplop.
    t = np.arange(LAJU) / LAJU
    x = np.zeros_like(t)
    for h in range(1, 30):
        x += np.sin(2 * np.pi * 120 * h * t) / h
    for f, g in ((700, 1.0), (1220, 0.5), (2600, 0.25)):
        x += g * np.sin(2 * np.pi * f * t) * np.exp(-((t - 0.5) / 0.2) ** 2)
    amplop = np.exp(-((t - 0.5) / 0.25) ** 2)
    return x * amplop / np.abs(x * amplop).max(), LAJU, "(sintetis)"


def bagian1():
    print(GARIS, "\nBAGIAN 1  WAV dibaca dengan pustaka bawaan\n", GARIS,
          sep="")

    x, laju, nama = contoh_ucapan()
    print(f"  sumber        : {nama}")
    print(f"  laju cuplik   : {ribuan(laju)} Hz")
    print(f"  jumlah cuplik : {ribuan(len(x))}")
    print(f"  durasi        : {len(x) / laju:.3f} detik")
    print(f"  jangkauan     : {x.min():+.4f} .. {x.max():+.4f}")
    print(f"  RMS           : {np.sqrt((x ** 2).mean()):.4f}")

    y = pra_tekan(x)
    # Ukur kemiringan spektrum sebelum dan sesudah: bandingkan tenaga di
    # separuh bawah pita dengan separuh atasnya.
    def miring(s):
        S = np.abs(np.fft.rfft(s)) ** 2
        tengah = len(S) // 2
        return 10 * np.log10(S[:tengah].sum() / S[tengah:].sum())

    print(f"\n  tenaga bawah dibanding atas, sebelum pra-penekanan : "
          f"{miring(x):+6.1f} dB")
    print(f"  tenaga bawah dibanding atas, sesudah pra-penekanan : "
          f"{miring(y):+6.1f} dB")

    print(f"""
  Selisih {koma(miring(x) - miring(y))} dB itulah yang dikerjakan satu baris
  pengurangan. Tanpa itu, seluruh koefisien MFCC di Bagian 6 didominasi
  kemiringan yang sama untuk setiap kata, dan yang sama untuk setiap kata
  tidak membantu membedakan kata.

  Perhatikan juga apa yang TIDAK dilakukan: sinyalnya tidak dinormalisasi ke
  amplitudo tetap. Kerasnya suara memang membawa informasi, dan Bagian 7
  menangani normalisasi di tempat yang lebih tepat, yaitu setelah logaritma.""")

    return x, laju


# ══════════════════════════════════════════════════════════════
# BAGIAN 2 - DFT dari definisinya
# ══════════════════════════════════════════════════════════════

def matriks_fourier(N):
    """Matriks DFT berukuran N x N.

        W[k, n] = exp(-2 pi i k n / N)

    Sesudah itu, DFT tinggal perkalian matriks: X = W x. Menuliskannya
    begini membuat satu hal jadi jelas dan sulit dilupakan: DFT adalah
    pemetaan LINEAR. Bukan algoritma, bukan trik, cuma satu matriks.

    Kolom ke-n matriks itu adalah satu vektor basis, dan barisnya
    ortogonal: W W^H = N I. Itu ruang Hilbert yang sama dengan yang kamu
    pakai di Fisika Kuantum, dan proyeksi ke basis Fourier adalah hasil kali
    dalam yang sama.

    TODO 3
    """
    n = np.arange(N)
    return np.exp(-2j * np.pi * np.outer(n, n) / N)


def bagian2():
    print("\n" + GARIS, "\nBAGIAN 2  DFT sebagai matriks, dan ongkosnya\n",
          GARIS, sep="")

    N = 256
    W = matriks_fourier(N)
    rng = np.random.default_rng(0)
    x = rng.normal(size=N)

    print(f"  selisih maks W @ x vs np.fft.fft : "
          f"{np.abs(W @ x - np.fft.fft(x)).max():.3e}")
    # Ortogonalitas: W W^H harus N kali matriks satuan.
    sisa = np.abs(W @ W.conj().T / N - np.eye(N)).max()
    print(f"  penyimpangan W W^H / N dari I    : {sisa:.3e}")
    print(f"  ukuran matriksnya                : {W.nbytes / 1e6:.1f} MB "
          f"untuk N = {N} saja\n")

    print(f"  {'N':>7}{'matriks (ms)':>15}{'FFT (ms)':>12}{'rasio':>10}"
          f"{'N/log2(N)':>12}")
    print("  " + "-" * 56)
    for N in (128, 256, 512, 1024, 2048):
        x = rng.normal(size=N)
        W = matriks_fourier(N)
        t0 = time.perf_counter()
        for _ in range(20):
            W @ x
        t_mat = (time.perf_counter() - t0) / 20 * 1000
        t0 = time.perf_counter()
        for _ in range(20):
            np.fft.fft(x)
        t_fft = (time.perf_counter() - t0) / 20 * 1000
        print(f"  {N:>7}{t_mat:>15.4f}{t_fft:>12.4f}{t_mat / t_fft:>10.1f}"
              f"{N / np.log2(N):>12.1f}")

    print(f"""
  Kolom terakhir adalah ramalan teoretisnya: DFT langsung butuh N^2 operasi,
  FFT butuh N log2 N, jadi rasionya seharusnya N / log2(N). Kolom rasio dan
  kolom ramalan tidak sama persis, dan arah selisihnya konsisten: perkalian
  matriks numpy memakai BLAS yang sangat cepat, sedangkan FFT membayar ongkos
  tetap penyusunan rencana. Untuk N kecil ongkos tetap itu belum tenggelam.

  Yang tidak terlihat di tabel waktu tetapi lebih menentukan adalah memori.
  Matriks Fourier untuk N = 512 saja sudah 4,2 MB. Spektrogram di Bagian 4
  menghitung {ribuan(LAJU // LONCAT)} DFT per detik audio, dan tidak ada
  satu pun yang perlu menyimpan matriks.

  Jadi matriks Fourier bukan alat kerja. Ia alat pikir, dan gunanya persis
  satu: mengingatkan bahwa sesuatu yang tampak rumit sebenarnya proyeksi ke
  basis ortogonal, sama seperti menguraikan keadaan kuantum ke basis energi.""")


# ══════════════════════════════════════════════════════════════
# BAGIAN 3 - bingkai dan jendela
# ══════════════════════════════════════════════════════════════

def jendela_hann(N):
    """Jendela Hann periodik, panjang N.

        w[n] = 0,5 - 0,5 cos(2 pi n / N)

    Perhatikan pembagi N, bukan N - 1. Yang memakai N - 1 adalah versi
    simetris, dan itu yang benar untuk merancang tapis. Untuk STFT yang
    benar versi periodik, karena bingkainya disambung berulang dan versi
    periodik yang menjumlah jadi konstan pada tumpang tindih 50 persen.
    `np.hanning` memberi versi simetris, jadi jangan dipakai di sini.

    TODO 4
    """
    n = np.arange(N)
    return 0.5 - 0.5 * np.cos(2 * np.pi * n / N)


def bingkaikan(x, panjang=BINGKAI, loncat=LONCAT):
    """Potong sinyal jadi bingkai tumpang tindih. Kembalikan (n_bingkai, panjang).

    Dikerjakan dengan `sliding_window_view` supaya tidak ada penyalinan:
    hasilnya cuma tampilan lain atas memori yang sama. Ini persis im2col
    dari Sesi 1 dalam satu dimensi, dan kesamaannya bukan kebetulan.

    TODO 5
    """
    from numpy.lib.stride_tricks import sliding_window_view
    if len(x) < panjang:
        x = np.pad(x, (0, panjang - len(x)))
    return sliding_window_view(x, panjang)[::loncat]


def bagian3():
    print("\n" + GARIS, "\nBAGIAN 3  kebocoran spektral, diukur\n", GARIS,
          sep="")

    N = 512
    HALUS = 64          # penambahan nol, supaya cupingnya benar-benar tercuplik
    jendela = (("kotak", np.ones(N)), ("hann", jendela_hann(N)))

    # Ukuran pertama: sifat jendelanya sendiri, lepas dari sinyal apa pun.
    # Spektrum jendela ditambahi nol 64 kali lipat, supaya puncak cuping
    # sampingnya tidak jatuh di antara dua titik cuplik dan terlewat.
    print("  Sifat jendela, diukur dari spektrumnya sendiri:\n")
    print(f"  {'jendela':<10}{'cuping samping (dB)':>21}"
          f"{'lebar cuping utama':>21}{'gain koheren':>15}")
    print("  " + "-" * 65)
    samping = {}
    for nama, w in jendela:
        S = np.abs(np.fft.rfft(w, N * HALUS))
        S_db = 20 * np.log10(S / S.max() + 1e-15)
        # Nol pertama: titik pertama tempat spektrumnya berhenti turun.
        i = 1
        while S_db[i] < S_db[i - 1]:
            i += 1
        samping[nama] = S_db[i:].max()
        lebar = 2 * i / HALUS                    # dua sisi, dalam satuan bin
        print(f"  {nama:<10}{samping[nama]:>21.1f}{lebar:>21.1f}"
              f"{w.mean():>15.3f}")

    # Ukuran kedua: akibatnya pada nada nyata. Dua nada, satu jatuh persis di
    # tengah bin dan satu jatuh di antara dua bin.
    print("\n  Kebocoran pada nada tunggal, tenaga di luar tiga bin puncak:\n")
    print(f"  {'nada':<26}{'jendela':>10}{'bocor (persen)':>18}"
          f"{'cuping tertinggi (dB)':>23}")
    print("  " + "-" * 77)
    bocor = {}
    for judul, k in (("tepat di bin (k = 40,0)", 40.0),
                     ("di antara bin (k = 40,5)", 40.5)):
        n = np.arange(N)
        x = np.sin(2 * np.pi * k * n / N)
        for nama, w in jendela:
            S = np.abs(np.fft.rfft(x * w)) ** 2
            puncak = int(np.argmax(S))
            luar = np.ones(len(S), bool)
            luar[max(0, puncak - 1):puncak + 2] = False
            bocor[(k, nama)] = S[luar].sum() / S.sum() * 100
            tertinggi = 10 * np.log10(S[luar].max() / S.max() + 1e-15)
            print(f"  {judul:<26}{nama:>10}{bocor[(k, nama)]:>18.2f}"
                  f"{tertinggi:>23.1f}")

    print(f"""
  Tabel pertama adalah sifat jendelanya, dan angka {koma(samping['kotak'])} dB
  itu tetapan yang layak kamu hafal: cuping samping tertinggi jendela kotak
  ada sekitar 13 dB di bawah puncaknya, apa pun panjang bingkainya. Hann
  menekannya jadi {koma(samping['hann'])} dB, dan harganya terbaca di kolom
  sebelahnya: cuping utamanya dua kali lebih lebar. Kamu membeli kebersihan
  dengan resolusi, dan pertukaran itu tidak bisa dihindari.

  Tabel kedua menunjukkan akibatnya pada sinyal. Baca dua baris kotak
  berdampingan: pada nada yang jatuh tepat di bin, kebocorannya
  {koma(bocor[(40.0, 'kotak')], 2)} persen; pada nada yang bergeser setengah
  bin saja, {koma(bocor[(40.5, 'kotak')], 1)} persen. Sinyalnya tidak berubah
  sifat; yang berubah cuma di mana frekuensinya mendarat relatif terhadap
  kisi bin.

  Sebabnya sudah kamu lihat di Soal 2 Sesi 1: DFT menganggap bingkainya
  berulang selamanya. Bingkai yang memuat bilangan bulat periode tersambung
  mulus dengan dirinya sendiri; bingkai yang memuat 40,5 periode punya
  lompatan di sambungannya. Lompatan itu diskontinu, dan diskontinu berisi
  seluruh frekuensi.

  Hann menekan kedua ujung bingkai jadi nol, jadi sambungannya selalu mulus
  berapa pun periodenya. Kebocorannya turun jadi
  {koma(bocor[(40.5, 'hann')], 1)} persen.

  Dan inilah jebakannya: pada k = 40,0 kedua jendela terlihat sama-sama baik.
  Nada uji di laboratorium biasanya disetel tepat di bin; suara manusia tidak
  pernah. Kalau kamu menguji pipa spektrum dengan nada yang tepat di bin,
  kamu tidak menguji apa pun.

  Soal 3 memintamu menurunkan tingkat cuping samping kotak secara analitik.""")


# ══════════════════════════════════════════════════════════════
# BAGIAN 4 - STFT dan spektrogram
# ══════════════════════════════════════════════════════════════

def stft(x, panjang=BINGKAI, loncat=LONCAT, n_fft=N_FFT):
    """Transformasi Fourier waktu-pendek. Kembalikan (n_bingkai, n_fft//2+1).

    Tiga baris: bingkaikan, kalikan jendela, FFT tiap baris. `np.fft.rfft`
    bekerja sepanjang sumbu terakhir, jadi seluruh bingkai dikerjakan
    sekaligus tanpa gelung Python.

    Nol tambahan sampai n_fft tidak menambah informasi apa pun. Yang
    ditambahkannya cuma titik interpolasi di antara bin yang sudah ada, dan
    panjang pangkat dua membuat FFT-nya lebih cepat.

    TODO 6
    """
    bingkai = bingkaikan(x, panjang, loncat) * jendela_hann(panjang)
    return np.fft.rfft(bingkai, n=n_fft, axis=-1)


def daya_db(S, lantai=-80.0):
    """Spektrum daya dalam desibel, dengan lantai. Disediakan."""
    daya = np.abs(S) ** 2
    db = 10 * np.log10(daya + 1e-10)
    return np.maximum(db, db.max() + lantai)


def bagian4(x, laju):
    print("\n" + GARIS, "\nBAGIAN 4  spektrogram dan pertukaran resolusi\n",
          GARIS, sep="")

    print(f"  {'bingkai':>9}{'ms':>7}{'loncat':>8}{'bingkai/dtk':>13}"
          f"{'df (Hz)':>10}{'dt (ms)':>10}{'df.dt':>9}")
    print("  " + "-" * 66)
    for panjang in (128, 256, 400, 800, 1600):
        loncat = panjang // 4
        df = laju / panjang            # jarak antar bin frekuensi
        dt = panjang / laju * 1000     # panjang bingkai dalam milidetik
        print(f"  {panjang:>9}{panjang / laju * 1000:>7.1f}{loncat:>8}"
              f"{laju / loncat:>13.0f}{df:>10.1f}{dt:>10.1f}"
              f"{df * dt / 1000:>9.2f}")

    print("""
  Kolom terakhir tetap 1,00 di setiap baris, dan itu bukan kebetulan
  aritmetika. df = fs/N dan dt = N/fs, jadi hasil kalinya persis 1 apa pun
  N-nya. Kamu tidak sedang memilih resolusi; kamu sedang memilih di sumbu
  mana resolusinya dibelanjakan.

  Ini prinsip ketakpastian yang sama dengan yang kamu turunkan di Fisika
  Kuantum. Di sana bentuknya delta_x delta_p >= hbar/2, dan turunannya
  memakai pertidaksamaan Cauchy-Schwarz atas pasangan Fourier posisi dan
  momentum. Di sini pasangannya waktu dan frekuensi, dan tetapan Planck
  tidak muncul karena tidak ada kuantisasi yang terlibat; yang tersisa cuma
  geometrinya. Bunyinya bukan analogi: keduanya teorema yang sama tentang
  pasangan Fourier.

  Pilihan 25 milidetik untuk suara berasal dari kompromi fisis, bukan dari
  optimasi. Lebih pendek dari itu, satu bingkai tidak memuat satu periode
  penuh nada dasar suara pria dan nada dasarnya tidak terukur. Lebih panjang
  dari itu, bibir dan lidah sudah sempat berpindah posisi di dalam satu
  bingkai, sehingga yang terukur campuran dua bunyi.""")

    X = stft(x)
    print(f"\n  spektrogram : {X.shape}  (bingkai, bin frekuensi)")
    print(f"  bin 0        : 0 Hz     bin terakhir : {laju / 2:.0f} Hz")
    print(f"  jarak bin    : {laju / N_FFT:.1f} Hz")
    return X


# ══════════════════════════════════════════════════════════════
# BAGIAN 5 - bank tapis mel
# ══════════════════════════════════════════════════════════════

def hz_ke_mel(f):
    """Skala mel O'Shaughnessy: m = 2595 log10(1 + f/700). TODO 7"""
    return 2595.0 * np.log10(1.0 + np.asarray(f, dtype=np.float64) / 700.0)


def mel_ke_hz(m):
    """Kebalikannya. TODO 7"""
    return 700.0 * (10.0 ** (np.asarray(m, dtype=np.float64) / 2595.0) - 1.0)


def bank_mel(n_mel=N_MEL, n_fft=N_FFT, laju=LAJU, f_min=20.0, f_max=None):
    """Bank tapis segitiga di skala mel. Kembalikan (n_mel, n_fft//2+1).

    Resepnya:

        1  ubah f_min dan f_max ke mel
        2  ambil n_mel + 2 titik berjarak SAMA di skala mel
        3  kembalikan ke Hz, lalu ke indeks bin FFT
        4  tapis ke-i naik lurus dari titik i ke titik i+1, lalu turun lurus
           ke titik i+2

    Titik puncak satu tapis adalah titik kaki tapis tetangganya, jadi
    tapisnya bertumpang tindih 50 persen dan tidak ada frekuensi yang jatuh
    di celah.

    Normalisasi: tiap tapis dibagi lebarnya, supaya tapis lebar di frekuensi
    tinggi tidak otomatis mengumpulkan tenaga lebih banyak hanya karena ia
    lebar. Tanpa ini, koefisien mel tertinggi selalu terbesar untuk apa pun.

    TODO 8
    """
    f_max = laju / 2 if f_max is None else f_max
    titik_mel = np.linspace(hz_ke_mel(f_min), hz_ke_mel(f_max), n_mel + 2)
    titik_hz = mel_ke_hz(titik_mel)

    freq = np.fft.rfftfreq(n_fft, 1.0 / laju)
    bank = np.zeros((n_mel, len(freq)))
    for i in range(n_mel):
        kiri, puncak, kanan = titik_hz[i], titik_hz[i + 1], titik_hz[i + 2]
        naik = (freq - kiri) / (puncak - kiri)
        turun = (kanan - freq) / (kanan - puncak)
        bank[i] = np.clip(np.minimum(naik, turun), 0.0, None)
        bank[i] *= 2.0 / (kanan - kiri)          # normalisasi luas
    return bank, titik_hz


def spektrogram_mel(x, n_mel=N_MEL):
    """Spektrogram mel dalam desibel. Kembalikan (n_bingkai, n_mel). Disediakan."""
    S = np.abs(stft(x)) ** 2
    bank, _ = bank_mel(n_mel)
    return 10 * np.log10(S @ bank.T + 1e-10)


def bagian5():
    print("\n" + GARIS, "\nBAGIAN 5  bank tapis mel: kenapa bukan linear\n",
          GARIS, sep="")

    bank, titik = bank_mel()
    print(f"  bank tapis : {bank.shape}")
    print(f"  tapis 0    : {titik[0]:7.1f} .. {titik[2]:7.1f} Hz  "
          f"(lebar {titik[2] - titik[0]:6.1f} Hz)")
    print(f"  tapis {N_MEL - 1}   : {titik[-3]:7.1f} .. {titik[-1]:7.1f} Hz  "
          f"(lebar {titik[-1] - titik[-3]:6.1f} Hz)")
    print(f"  rasio lebar: {(titik[-1] - titik[-3]) / (titik[2] - titik[0]):.1f}x\n")

    print(f"  {'oktaf (Hz)':<16}{'lebar pita':>12}{'jumlah tapis':>15}"
          f"{'tapis per kHz':>16}")
    print("  " + "-" * 59)
    batas = [125, 250, 500, 1000, 2000, 4000, 8000]
    pusat = titik[1:-1]
    for a, b in zip(batas[:-1], batas[1:]):
        n = int(((pusat >= a) & (pusat < b)).sum())
        print(f"  {f'{a} - {b}':<16}{b - a:>12}{n:>15}"
              f"{n / (b - a) * 1000:>16.1f}")

    print(f"""
  Tiap baris tabel itu satu oktaf, jadi tiap baris lebar pitanya dua kali
  baris di atasnya. Kalau sumbunya linear, jumlah tapis per baris akan
  berlipat dua ke bawah. Yang terukur justru hampir rata: oktaf 125-250 Hz
  dan oktaf 4000-8000 Hz mendapat jumlah tapis yang tidak jauh berbeda,
  padahal pitanya berbeda 32 kali lipat.

  Itulah seluruh isi skala mel. Ia meniru telinga, dan telinga memisahkan
  nada secara kira-kira logaritmik: selisih 100 Hz jelas terdengar di sekitar
  200 Hz dan hampir tidak terdengar di sekitar 5.000 Hz. Membelanjakan
  {N_MEL} tapis secara linear berarti membuang sebagian besarnya di wilayah
  yang telinga sendiri tidak bisa membedakan.

  Ada akibat kedua yang lebih langsung untuk kita: {N_FFT // 2 + 1} bin FFT
  diringkas jadi {N_MEL} angka. Itu penyusutan {koma((N_FFT // 2 + 1) / N_MEL)}
  kali lipat pada masukan model, dan model yang masukannya lebih kecil butuh
  contoh lebih sedikit. Di Sesi 4, dengan data latih yang jumlahnya tetap,
  penyusutan itulah yang menentukan apakah modelnya bisa dilatih sama sekali.

  Soal 5 memintamu memeriksa apakah bank tapis ini bisa dibalik, dan apa
  akibatnya untuk mengubah spektrogram kembali jadi suara.""")

    return bank


# ══════════════════════════════════════════════════════════════
# BAGIAN 6 - MFCC
# ══════════════════════════════════════════════════════════════

def matriks_dct(n_keluar, n_masuk):
    """Matriks DCT-II ortonormal, bentuk (n_keluar, n_masuk).

        C[k, n] = a_k cos(pi k (2n + 1) / (2 N))
        a_0 = sqrt(1/N),  a_k = sqrt(2/N) untuk k > 0

    DCT adalah kerabat DFT untuk sinyal real yang dicerminkan jadi genap.
    Karena pencerminan itu menghapus diskontinu di ujung, DCT memusatkan
    tenaga di koefisien pertama jauh lebih rapat daripada DFT. Sifat itulah
    yang dipakai JPEG, dan yang dipakai di sini.

    TODO 9
    """
    k = np.arange(n_keluar)[:, None]
    n = np.arange(n_masuk)[None, :]
    C = np.cos(np.pi * k * (2 * n + 1) / (2 * n_masuk))
    C *= np.sqrt(2.0 / n_masuk)
    C[0] *= np.sqrt(0.5)
    return C


def mfcc(x, n_mfcc=N_MFCC, n_mel=N_MEL):
    """MFCC lengkap: pra-tekan, STFT, mel, log, DCT. Kembalikan (bingkai, n_mfcc).

    TODO 10
    """
    mel_db = spektrogram_mel(pra_tekan(x), n_mel)
    return mel_db @ matriks_dct(n_mfcc, n_mel).T


def bagian6(x):
    print("\n" + GARIS, "\nBAGIAN 6  MFCC: logaritma, DCT, dan dekorelasi\n",
          GARIS, sep="")

    from scipy.fft import dct as dct_scipy
    C = matriks_dct(N_MEL, N_MEL)
    uji = np.random.default_rng(0).normal(size=N_MEL)
    print(f"  selisih matriks DCT vs scipy : "
          f"{np.abs(C @ uji - dct_scipy(uji, type=2, norm='ortho')).max():.3e}")
    print(f"  penyimpangan C C^T dari I    : "
          f"{np.abs(C @ C.T - np.eye(N_MEL)).max():.3e}")
    print("  (ortonormal, jadi DCT tidak menambah atau membuang tenaga)\n")

    mel_db = spektrogram_mel(pra_tekan(x))
    koef = mel_db @ matriks_dct(N_MEL, N_MEL).T

    def korelasi_rata(M):
        """Rerata |korelasi| antar pasangan kolom yang berbeda."""
        R = np.corrcoef(M.T)
        luar = ~np.eye(len(R), dtype=bool)
        return np.abs(R[luar]).mean()

    print(f"  {'representasi':<28}{'dimensi':>9}{'|korelasi| rerata':>20}")
    print("  " + "-" * 57)
    print(f"  {'log mel':<28}{mel_db.shape[1]:>9}{korelasi_rata(mel_db):>20.3f}")
    print(f"  {'MFCC penuh':<28}{koef.shape[1]:>9}{korelasi_rata(koef):>20.3f}")
    print(f"  {'MFCC dipotong ' + str(N_MFCC):<28}{N_MFCC:>9}"
          f"{korelasi_rata(koef[:, :N_MFCC]):>20.3f}")

    # Berapa banyak tenaga yang tersisa di 13 koefisien pertama.
    tenaga = (koef ** 2).sum(axis=0)
    porsi = tenaga[:N_MFCC].sum() / tenaga.sum()
    print(f"\n  tenaga di {N_MFCC} koefisien pertama : {porsi * 100:.1f} persen "
          f"dari {N_MEL}")

    print(f"""
  Dua angka itu adalah seluruh alasan MFCC ada.

  Angka pertama: tapis mel yang bersebelahan bertumpang tindih 50 persen, jadi
  keluarannya memang berkorelasi kuat, terukur {koma(korelasi_rata(mel_db), 3)}.
  Model yang masukannya berkorelasi kuat memboroskan kapasitas untuk
  mempelajari kembali korelasi yang sudah kita ketahui ada. DCT
  menghilangkannya sampai {koma(korelasi_rata(koef), 3)}, dan itu bukan hampiran
  melainkan akibat ortogonalitas.

  Angka kedua: {koma(porsi * 100)} persen tenaganya ada di {N_MFCC} koefisien
  pertama, jadi 27 sisanya bisa dibuang dengan kerugian kecil. Yang terbuang
  adalah pola log-mel yang berubah cepat sepanjang sumbu frekuensi, dan itu
  terutama struktur harmonik nada dasar, yaitu tinggi suara pembicara. Untuk
  mengenali KATA, membuang tinggi suara adalah keuntungan.

  Dan di situlah letak alasan MFCC mulai ditinggalkan sejak sekitar 2015.
  Dekorelasi berguna untuk model campuran Gaussian, yang mengasumsikan
  matriks kovarian diagonal. CNN tidak mengasumsikan itu, dan justru MEMBUTUHKAN
  struktur lokal di sumbu frekuensi supaya kernelnya punya sesuatu untuk
  disapu. DCT mengaduk sumbu itu, jadi kernel 3x3 di atas MFCC menyapu
  tetangga yang tidak lagi bertetangga.

  Ramalan yang akan diuji di Sesi 4: untuk CNN, log-mel mengalahkan MFCC.
  Untuk model linear seperti yang kamu latih di Bulan 2, MFCC yang menang.
  Soal 6 memintamu menyatakan ramalan itu sebagai hipotesis yang bisa gagal,
  lengkap dengan angka yang akan membantahnya.""")

    return mel_db, koef


# ══════════════════════════════════════════════════════════════
# BAGIAN 7 - delta, normalisasi, dan fitur yang dibekukan
# ══════════════════════════════════════════════════════════════

def delta(M, lebar=2):
    """Turunan terhadap waktu dengan regresi linear di jendela +-lebar.

        d[t] = sum_k k (M[t+k] - M[t-k]) / (2 sum_k k^2)

    Rumus ini bukan selisih maju M[t+1] - M[t], dan bedanya penting: selisih
    maju memperbesar derau, sedangkan kemiringan regresi merata-ratakan
    beberapa titik lebih dulu. Ini persoalan yang sama dengan menurunkan data
    terukur di praktikum, dan jawabannya sama.

    Tepi ditangani dengan mengulang bingkai pertama dan terakhir.

    TODO 11
    """
    bantalan = np.pad(M, ((lebar, lebar), (0, 0)), mode="edge")
    penyebut = 2 * sum(k * k for k in range(1, lebar + 1))
    d = np.zeros_like(M)
    for k in range(1, lebar + 1):
        d += k * (bantalan[lebar + k:len(M) + lebar + k]
                  - bantalan[lebar - k:len(M) + lebar - k])
    return d / penyebut


def normalkan(M):
    """Kurangi rerata tiap koefisien sepanjang ucapan. Disediakan.

    Namanya cepstral mean normalisation, dan gunanya membatalkan tanggapan
    tetap dari mikrofon dan ruangan. Konvolusi di ranah waktu jadi penjumlahan
    di ranah log, jadi apa pun yang tetap sepanjang rekaman jadi geseran tetap
    yang tinggal dikurangkan. Sekali lagi teorema konvolusi dari Sesi 1, kali
    ini dipakai untuk membuang sesuatu.
    """
    return M - M.mean(axis=0, keepdims=True)


def fitur_audio(x, n_mel=N_MEL, delta_juga=False):
    """Fitur baku Bulan 3: log-mel, dinormalkan. Kembalikan (bingkai, dim).

    Inilah yang dipakai Sesi 4 dan yang disalin ke `synesis/suara.py` di Sesi
    5. Bentuknya dibekukan di sini supaya tidak ada dua versi yang berbeda
    diam-diam.

    TODO 12
    """
    M = normalkan(spektrogram_mel(pra_tekan(x), n_mel))
    if not delta_juga:
        return M
    return np.concatenate([M, delta(M), delta(delta(M))], axis=1)


def bagian7(x, laju, mel_db, koef):
    print("\n" + GARIS, "\nBAGIAN 7  delta, normalisasi, dan fitur beku\n",
          GARIS, sep="")

    F = fitur_audio(x)
    F3 = fitur_audio(x, delta_juga=True)
    print(f"  {'fitur':<26}{'bentuk':>16}{'angka/detik':>14}")
    print("  " + "-" * 56)
    for nama, M in (("sinyal mentah", x[:, None]),
                    ("spektrogram linear", np.abs(stft(x))),
                    ("log-mel", mel_db),
                    (f"MFCC {N_MFCC}", koef[:, :N_MFCC]),
                    ("log-mel dinormalkan", F),
                    ("log-mel + delta + delta2", F3)):
        per_detik = M.size / (len(x) / laju)
        print(f"  {nama:<26}{str(M.shape):>16}{ribuan(per_detik):>14}")

    print(f"""
  Baris pertama dan baris kelima adalah seluruh cerita Bulan 3 sejauh ini:
  {ribuan(laju)} angka per detik jadi {ribuan(F.shape[1] * laju // LONCAT)} angka
  per detik, penyusutan {laju / (F.shape[1] * laju / LONCAT):.0f} kali lipat, dan
  yang dibuang justru bagian yang tidak membedakan kata.

  Baris terakhir menambahkan turunan pertama dan kedua terhadap waktu.
  Alasannya: satu bingkai log-mel menggambarkan bunyi saat itu, dan tidak
  memuat ke mana bunyi itu bergerak. Perbedaan antara /b/ dan /p/ hampir
  seluruhnya ada di kecepatan perubahan, bukan di keadaan sesaatnya.

  Untuk model yang membaca satu bingkai pada satu waktu, delta itu wajib.
  Untuk CNN yang membaca seluruh petak waktu-frekuensi sekaligus, delta
  sebagian besar mubazir: kernel yang menyapu sumbu waktu bisa MEMPELAJARI
  turunan itu sendiri, dan kernel [-1, 0, 1] yang kamu lihat di Sesi 1 persis
  itu bentuknya. Sesi 4 mengukur apakah menambahkannya masih membantu.""")

    fig, ax = plt.subplots(4, 1, figsize=(9, 9), sharex=False)
    t = np.arange(len(x)) / laju
    ax[0].plot(t, x, lw=0.4)
    ax[0].set_title("sinyal", fontsize=9)
    ax[0].set_xlim(0, t[-1])
    for a, (judul, M) in zip(ax[1:], [
            ("spektrogram daya (dB)", daya_db(stft(x)).T),
            (f"log-mel ({N_MEL} tapis)", mel_db.T),
            (f"MFCC ({N_MFCC} koefisien)", koef[:, :N_MFCC].T)]):
        a.imshow(M, aspect="auto", origin="lower", cmap="magma")
        a.set_title(judul, fontsize=9)
    fig.tight_layout()
    berkas = FIGUR / "b3s2_spektrogram.png"
    fig.savefig(berkas, dpi=110)
    plt.close(fig)
    print(f"\n  Gambar disimpan: {berkas.name}")

    print("""
  Lihat gambarnya sebelum menutup sesi. Panel kedua adalah spektrogram
  linear, dan garis-garis mendatar berjarak sama di bagian bawahnya adalah
  harmonik nada dasar. Panel ketiga meremas sumbu itu jadi 40 baris, dan
  harmoniknya sebagian besar hilang sementara pita formant yang lebar tetap
  terlihat. Panel keempat sudah tidak bisa dibaca mata sama sekali, dan itu
  wajar: DCT membuang tafsiran spasialnya demi dekorelasi.

  Sesi 3 mengambil panel ketiga dan memperlakukannya persis seperti gambar
  MNIST di Bulan 1: satu matriks yang disapu kernel. Semua yang kamu tulis
  di Sesi 1 berlaku apa adanya mulai titik itu.""")


# ══════════════════════════════════════════════════════════════
# Jalankan semuanya
# ══════════════════════════════════════════════════════════════

def main():
    mulai = time.perf_counter()

    x, laju = bagian1()
    bagian2()
    bagian3()
    bagian4(x, laju)
    bagian5()
    mel_db, koef = bagian6(x)
    bagian7(x, laju, mel_db, koef)

    print(f"\n{GARIS}")
    print(f"  selesai dalam {time.perf_counter() - mulai:.1f} detik")
    print(GARIS)


if __name__ == "__main__":
    main()
