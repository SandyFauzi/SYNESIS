"""Bukti terukur untuk seluruh Bulan 3.

Jalankan:
    . .\\scripts\\activate.ps1
    python notebooks\\kunci_b3_bukti.py

Setiap angka yang dikutip di berkas soal Bulan 3 punya satu uji di sini.
Gunanya bukan mengulang notebooknya, melainkan memisahkan KLAIM dari
PENJELASAN: kalau salah satu uji di bawah gagal, ada kalimat di berkas soal
yang harus diperbaiki, dan berkas ini menyebut yang mana.

Uji yang butuh model besar dilewati dengan pesan, bukan dengan kegagalan,
supaya berkas ini tetap bisa dijalankan di mesin yang baru dikloning.
"""

import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

GARIS = "=" * 66
LULUS, GAGAL, LEWAT = [], [], []


def periksa(nama, syarat, catatan=""):
    """Catat satu klaim. Disediakan."""
    (LULUS if syarat else GAGAL).append(nama)
    tanda = "lulus" if syarat else "GAGAL"
    print(f"  [{tanda}] {nama}" + (f"   {catatan}" if catatan else ""))
    return syarat


def lewati(nama, alasan):
    LEWAT.append(nama)
    print(f"  [lewat] {nama}   {alasan}")


# ══════════════════════════════════════════════════════════════
# UJI A - Sesi 1: konvolusi
# ══════════════════════════════════════════════════════════════

def uji_a():
    print(GARIS, "\nUJI A  Sesi 1, konvolusi\n", GARIS, sep="")
    from bulan3_sesi1_konvolusi import (KOTAK, SOBEL_X, TAJAM, im2col,
                                        konvolusi1d, konvolusi_fft,
                                        konvolusi2d, korelasi2d)

    rng = np.random.default_rng(0)
    x, h = rng.normal(size=200), rng.normal(size=9)

    for mode in ("full", "same", "valid"):
        periksa(f"konvolusi1d cocok numpy, mode {mode}",
                np.allclose(konvolusi1d(x, h, mode), np.convolve(x, h, mode)))

    periksa("teorema konvolusi, FFT == langsung",
            np.abs(konvolusi_fft(x, h) - np.convolve(x, h)).max() < 1e-10)

    # Soal 2b: tanpa penambahan nol, tepat K-1 cuplikan pertama tercemar.
    K = 64
    hh = rng.normal(size=K)
    xx = rng.normal(size=1000)
    ling = np.fft.irfft(np.fft.rfft(xx, 1000) * np.fft.rfft(hh, 1000), 1000)
    tercemar = int((np.abs(ling - np.convolve(xx, hh)[:1000]) > 1e-9).sum())
    periksa("konvolusi melingkar mencemari tepat K-1 cuplikan",
            tercemar == K - 1, f"{tercemar} vs {K - 1}")

    # Soal 4b: sobel antisimetris, selisih konv-korel = 2x tanggapan maks.
    g = rng.normal(size=(28, 28))
    beda = np.abs(konvolusi2d(g, SOBEL_X) - korelasi2d(g, SOBEL_X)).max()
    dua = 2 * np.abs(konvolusi2d(g, SOBEL_X)).max()
    periksa("selisih konvolusi-korelasi sobel = 2x tanggapan maks",
            abs(beda - dua) / dua < 1e-9, f"{beda:.3f} vs {dua:.3f}")
    for nama, k in (("kotak", KOTAK), ("tajam", TAJAM)):
        periksa(f"kernel {nama} simetris, konvolusi == korelasi",
                np.abs(konvolusi2d(g, k) - korelasi2d(g, k)).max() < 1e-12)

    # Soal 5a: peringkat kernel.
    periksa("SOBEL_X berperingkat 1, jadi terpisah",
            np.linalg.matrix_rank(SOBEL_X) == 1)
    periksa("SOBEL_X = [1,2,1] kali [-1,0,1]",
            np.allclose(np.outer([1, 2, 1], [-1, 0, 1]), SOBEL_X))
    periksa("TAJAM berperingkat 2, tidak terpisah",
            np.linalg.matrix_rank(TAJAM) == 2)

    # Soal 6c: pelipatan memori im2col.
    kol = im2col(np.zeros((40, 101)), 3, 3)
    lipat = kol.nbytes / np.zeros((40, 101)).nbytes
    periksa("im2col melipatkan memori mendekati Kh*Kw = 9",
            8.0 < lipat < 9.0, f"{lipat:.2f}x")

    # Soal 7a: lipatan aliasing.
    fs, n = 1000.0, np.arange(200)
    a = np.sin(2 * np.pi * 600 * n / fs)
    b = -np.sin(2 * np.pi * 400 * n / fs)
    periksa("600 Hz pada 1 kHz identik dengan -400 Hz",
            np.abs(a - b).max() < 1e-10)


# ══════════════════════════════════════════════════════════════
# UJI B - Sesi 2: spektrogram dan MFCC
# ══════════════════════════════════════════════════════════════

def uji_b():
    print("\n" + GARIS, "\nUJI B  Sesi 2, spektrogram dan MFCC\n", GARIS, sep="")
    from bulan3_sesi2_spektrogram import (N_FFT, N_MEL, bank_mel, hz_ke_mel,
                                          jendela_hann, matriks_dct,
                                          matriks_fourier, mel_ke_hz,
                                          spektrogram_mel, stft)

    N = 256
    W = matriks_fourier(N)
    rng = np.random.default_rng(0)
    x = rng.normal(size=N)
    periksa("matriks Fourier == np.fft.fft",
            np.abs(W @ x - np.fft.fft(x)).max() < 1e-9)
    periksa("basis Fourier ortogonal, W W^H = N I",
            np.abs(W @ W.conj().T / N - np.eye(N)).max() < 1e-12)

    # Soal 3a: cuping samping kotak -13,46 dB secara analitik.
    for nama, w, harap in (("kotak", np.ones(512), -13.46),
                           ("hann", jendela_hann(512), -31.5)):
        S = np.abs(np.fft.rfft(w, 512 * 64))
        db = 20 * np.log10(S / S.max() + 1e-15)
        i = 1
        while db[i] < db[i - 1]:
            i += 1
        ukur = db[i:].max()
        periksa(f"cuping samping {nama} sekitar {harap} dB",
                abs(ukur - harap) < 0.5, f"terukur {ukur:.2f} dB")

    # Soal 4a: hasil kali resolusi selalu 1.
    hasil = {16000 / n * (n / 16000) for n in (128, 256, 400, 800, 1600)}
    periksa("df kali dt = 1 untuk semua panjang bingkai",
            all(abs(v - 1.0) < 1e-12 for v in hasil))

    # mel bolak-balik.
    f = np.array([20.0, 700.0, 4000.0, 8000.0])
    periksa("hz_ke_mel dan mel_ke_hz saling membalik",
            np.abs(mel_ke_hz(hz_ke_mel(f)) - f).max() < 1e-9)

    bank, titik = bank_mel()
    periksa("bank mel menutup pita tanpa celah",
            (bank.sum(axis=0) > 0).mean() > 0.98)
    lebar_bawah = titik[2] - titik[0]
    lebar_atas = titik[-1] - titik[-3]
    periksa("tapis mel teratas jauh lebih lebar daripada terbawah",
            lebar_atas / lebar_bawah > 8,
            f"{lebar_atas / lebar_bawah:.1f}x")

    # DCT ortonormal, dan dibandingkan scipy.
    from scipy.fft import dct as dct_scipy
    C = matriks_dct(N_MEL, N_MEL)
    u = rng.normal(size=N_MEL)
    periksa("matriks DCT-II == scipy norm='ortho'",
            np.abs(C @ u - dct_scipy(u, type=2, norm="ortho")).max() < 1e-12)
    periksa("DCT ortonormal, C C^T = I",
            np.abs(C @ C.T - np.eye(N_MEL)).max() < 1e-12)

    # Bentuk STFT.
    S = stft(np.zeros(16000))
    periksa("STFT satu detik berbentuk (98, 257)", S.shape == (98, N_FFT // 2 + 1),
            str(S.shape))
    periksa("spektrogram mel berbentuk (98, 40)",
            spektrogram_mel(np.zeros(16000)).shape == (98, N_MEL))


# ══════════════════════════════════════════════════════════════
# UJI C - Sesi 3: CNN dari nol
# ══════════════════════════════════════════════════════════════

def uji_c():
    print("\n" + GARIS, "\nUJI C  Sesi 3, CNN dari nol\n", GARIS, sep="")
    from bulan1_sesi34_mnist import Tensor
    from bulan3_sesi1_konvolusi import korelasi2d
    from bulan3_sesi3_cnn import (bentuk_ulang, konv2d, maks_kolam, padat,
                                  periksa_gradien)

    rng = np.random.default_rng(1)
    X = Tensor(rng.normal(size=(3, 8, 8, 2)))
    kelas = rng.integers(0, 4, size=3)
    par = [Tensor(rng.normal(0, 0.3, (3 * 3 * 2, 4))), Tensor(rng.normal(0, 0.1, 4)),
           Tensor(rng.normal(0, 0.3, (3 * 3 * 4, 5))), Tensor(rng.normal(0, 0.1, 5)),
           Tensor(rng.normal(0, 0.3, (5, 4))), Tensor(rng.normal(0, 0.1, 4))]

    def rugi():
        W1, b1, W2, b2, W3, b3 = par
        h = maks_kolam(konv2d(X, W1, b1).relu(), 2)
        h = konv2d(h, W2, b2).relu()
        return padat(bentuk_ulang(h, (3, -1)), W3, b3).entropi_silang(kelas)

    galat, _ = periksa_gradien(rugi, par)
    periksa("gradien konv2d, maks_kolam, bentuk_ulang cocok selisih terhingga",
            galat < 1e-7, f"galat relatif {galat:.2e}")

    # Konv2d benar-benar korelasi silang, bukan konvolusi.
    Xs = Tensor(rng.normal(size=(1, 7, 7, 1)))
    Ks = rng.normal(size=(3, 3))
    hs = konv2d(Xs, Tensor(Ks.reshape(9, 1)), Tensor(np.zeros(1)))
    polos = korelasi2d(Xs.data[0, :, :, 0], Ks)
    periksa("konv2d == korelasi silang bergelung",
            np.abs(hs.data[0, :, :, 0] - polos).max() < 1e-12)

    # Gradien yang SALAH harus tertangkap. Ini uji atas ujinya sendiri.
    import bulan3_sesi3_cnn as b3s3
    asli = b3s3.im2col

    def im2col_rusak(Xt, Kh, Kw):
        keluar = asli(Xt, Kh, Kw)
        lama = keluar._backward

        def _backward():
            simpan = Xt.grad.copy()
            lama()
            Xt.grad = (Xt.grad - simpan) * 0.3 + simpan      # gradien dikecilkan

        keluar._backward = _backward
        return keluar

    b3s3.im2col = im2col_rusak
    galat_rusak, _ = periksa_gradien(rugi, par)
    b3s3.im2col = asli
    periksa("pemeriksa gradien menangkap col2im yang dirusak",
            galat_rusak > 1e-3, f"galat relatif {galat_rusak:.2e}")


# ══════════════════════════════════════════════════════════════
# UJI D - Sesi 4: data dan belahan
# ══════════════════════════════════════════════════════════════

def uji_d():
    print("\n" + GARIS, "\nUJI D  Sesi 4, data dan belahan\n", GARIS, sep="")
    from bulan3_sesi4_wakeword import SUARA, belahan, daftar_berkas, roc

    # ROC di skor yang sempurna terpisah harus memberi AUC = 1.
    ambang, far, frr, auc = roc(np.array([0.9, 0.95, 1.0]),
                                np.array([0.0, 0.1, 0.2]))
    periksa("AUC = 1 untuk dua kelompok yang terpisah sempurna", auc == 1.0)
    ambang, far, frr, auc = roc(np.array([0.4, 0.5]), np.array([0.4, 0.5]))
    periksa("AUC = 0,5 untuk dua kelompok yang identik", abs(auc - 0.5) < 1e-9,
            f"{auc:.3f}")

    # Belahan menurut pembicara: nama pembicara sama harus jatuh sama.
    a = belahan("E:/x/yes/004ae714_nohash_0.wav")
    b = belahan("E:/x/no/004ae714_nohash_3.wav")
    periksa("pembicara yang sama selalu jatuh di belahan yang sama", a == b,
            f"{a} == {b}")
    periksa("belahan hanya bernilai latih, valid, atau uji",
            a in ("latih", "valid", "uji"))

    if not SUARA.is_dir():
        lewati("kebocoran pembicara di data nyata",
               "Speech Commands belum diunduh")
        return

    import re
    baris = daftar_berkas()
    milik = {}
    for w, _, s in baris:
        milik.setdefault(re.sub(r"_nohash_.*$", "", w.name), set()).add(s)
    bocor = sum(1 for v in milik.values() if len(v) > 1)
    periksa("nol pembicara muncul di lebih dari satu belahan", bocor == 0,
            f"{len(milik)} pembicara, {bocor} bocor")


# ══════════════════════════════════════════════════════════════
# UJI E - Sesi 5: paket dan notebook tidak boleh berbeda angka
# ══════════════════════════════════════════════════════════════

def uji_e():
    print("\n" + GARIS, "\nUJI E  Sesi 5, duplikasi yang disengaja\n", GARIS,
          sep="")
    import bulan3_sesi2_spektrogram as nb
    from synesis import suara as pk

    for nama, a, b in (("LAJU", nb.LAJU, pk.LAJU),
                       ("BINGKAI", nb.BINGKAI, pk.BINGKAI),
                       ("LONCAT", nb.LONCAT, pk.LONCAT),
                       ("N_FFT", nb.N_FFT, pk.N_FFT),
                       ("N_MEL", nb.N_MEL, pk.N_MEL),
                       ("PRA_TEKAN", nb.PRA_TEKAN, pk.PRA_TEKAN)):
        periksa(f"tetapan {nama} sama di notebook dan paket", a == b,
                f"{a} == {b}")

    rng = np.random.default_rng(0)
    x = rng.normal(0, 0.05, 16000)
    beda = np.abs(nb.fitur_audio(x) - pk.fitur_audio(x)).max()
    periksa("fitur_audio notebook == fitur_audio paket", beda < 1e-9,
            f"selisih maks {beda:.2e}")

    beda_j = np.abs(nb.jendela_hann(400) - pk.jendela_hann(400)).max()
    periksa("jendela Hann sama", beda_j < 1e-15)
    beda_b = np.abs(nb.bank_mel()[0] - pk.BANK).max()
    periksa("bank tapis mel sama", beda_b < 1e-12, f"selisih maks {beda_b:.2e}")

    # Pemilih ambang harus condong ke sisi aman.
    periksa("ambang dipilih dari ongkos, bukan dari titik kesalahan setara",
            pk.pilih_ambang(np.array([0.1, 0.5, 0.9]),
                            np.array([0.50, 0.10, 0.001]),
                            np.array([0.00, 0.05, 0.300])) == 0.9)


# ══════════════════════════════════════════════════════════════
# UJI F - Sesi 5: RVC
# ══════════════════════════════════════════════════════════════

def uji_f():
    print("\n" + GARIS, "\nUJI F  Sesi 5, RVC yang ditulis ulang\n", GARIS,
          sep="")
    from synesis import konfig, rvc

    # YIN pada nada yang diketahui.
    t = np.arange(16000) / 16000
    for f in (110.0, 220.0, 440.0):
        x = np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t)
        ukur = float(np.median(rvc.f0_yin(x)[5:-5]))
        periksa(f"YIN menemukan {f:.0f} Hz", abs(ukur - f) / f < 0.02,
                f"{ukur:.1f} Hz")
    periksa("YIN menyebut sunyi sebagai tak bersuara",
            rvc.f0_yin(np.zeros(16000)).max() == 0.0)

    kasar = rvc.nada_kasar(np.array([0.0, 50.0, 200.0, 1100.0, 2000.0]))
    periksa("kuantisasi nada monoton dan di dalam 1..255",
            kasar[0] == 1 and kasar[-1] == 255 and (np.diff(kasar) >= 0).all(),
            str(kasar.tolist()))

    if not Path(konfig.RVC_MODEL).exists():
        lewati("kunci model RVC", f"{konfig.RVC_MODEL} tidak ada")
        return

    import torch
    titik = torch.load(konfig.RVC_MODEL, map_location="cpu", weights_only=False)
    net = rvc.SynthesizerTrnMs768NSFsid(titik["config"])
    sd = rvc._lepas_weight_norm(titik["weight"])
    punya, datang = set(net.state_dict()), set(sd)
    periksa("himpunan kunci model == himpunan kunci berkas .pth",
            punya == datang,
            f"{len(punya)} kunci, {len(punya - datang)} hilang, "
            f"{len(datang - punya)} berlebih")
    bentuk_cocok = all(net.state_dict()[k].shape == sd[k].shape
                       for k in punya & datang)
    periksa("bentuk setiap tensor cocok", bentuk_cocok)


# ══════════════════════════════════════════════════════════════
# UJI G - anggaran latensi, diukur bukan ditebak
# ══════════════════════════════════════════════════════════════

def uji_g(cepat=True):
    print("\n" + GARIS, "\nUJI G  anggaran latensi\n", GARIS, sep="")
    from synesis import konfig, suara

    if cepat:
        lewati("RTF Piper, Whisper, dan RVC",
               "butuh memuat tiga model, jalankan dengan --penuh")
        return

    if not Path(konfig.PIPER_MODEL).exists():
        lewati("RTF ketiga model", "Piper belum diunduh")
        return

    kal = "Halo Sandy. Laporan praktikum minggu lalu sudah saya buka."
    suara.sintesis(kal)
    t0 = time.perf_counter()
    x, laju = suara.sintesis(kal)
    t_piper = time.perf_counter() - t0
    dur = len(x) / laju

    suara.transkrip(x, laju)
    t0 = time.perf_counter()
    teks = suara.transkrip(x, laju)
    t_stt = time.perf_counter() - t0

    t_rvc = float("nan")
    if konfig.RVC_AKTIF and Path(konfig.RVC_MODEL).exists():
        suara.warnai(x, laju)
        t0 = time.perf_counter()
        y, sr = suara.warnai(x, laju)
        t_rvc = time.perf_counter() - t0

    print(f"\n  {'tahap':<22}{'detik':>9}{'RTF':>8}")
    print("  " + "-" * 39)
    for nama, t in (("Piper", t_piper), ("RVC", t_rvc)):
        print(f"  {nama:<22}{t:>9.2f}{t / dur:>8.2f}")
    # Whisper tidak punya RTF yang berarti: ia membantali masukannya sampai
    # 30 detik, jadi ongkosnya tetap. Kolomnya sengaja dikosongkan.
    print(f"  {'Whisper':<22}{t_stt:>9.2f}{'-':>8}")

    # Whisper dihitung sebagai ongkos TETAP, bukan RTF dikali durasi:
    # ia membantali masukannya sampai 30 detik, jadi ucapan 1 detik dan
    # 8 detik memakan waktu yang sama.
    total = 0.7 + t_stt + 0.005 + (t_piper + t_rvc) / dur * 3
    print(f"\n  anggaran ujung ke ujung, perintah 2 detik, balasan 3 detik:")
    print(f"    {total * 1000:.0f} ms   (batas Modul.md: 3.000 ms)")
    # Klaim ini SEDANG GAGAL, dan sengaja dibiarkan gagal. Batas 3 detik
    # dijanjikan docs/Modul.md; anggaran sesungguhnya sekitar 3,8 detik
    # karena Whisper memakan waktu tetap 2,6 detik berapa pun panjang
    # ucapannya. Tercatat di TODO.md beserta dua jalan keluarnya. Jangan
    # tutup uji ini supaya angkanya kelihatan hijau.
    periksa("anggaran latensi di bawah 3 detik (janji docs/Modul.md)",
            total < 3.0, f"{total:.2f} detik, utang tercatat di TODO.md")
    periksa("transkripsi Piper mengandung kata kunci",
            "laporan" in teks.lower(), repr(teks))


# ══════════════════════════════════════════════════════════════

def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    mulai = time.perf_counter()

    uji_a()
    uji_b()
    uji_c()
    uji_d()
    uji_e()
    uji_f()
    uji_g(cepat="--penuh" not in argv)

    print(f"\n{GARIS}")
    print(f"  {len(LULUS)} lulus, {len(GAGAL)} gagal, {len(LEWAT)} dilewati, "
          f"{time.perf_counter() - mulai:.1f} detik")
    if GAGAL:
        print("\n  yang gagal:")
        for n in GAGAL:
            print(f"    - {n}")
    print(GARIS)
    return 1 if GAGAL else 0


if __name__ == "__main__":
    sys.exit(main())
