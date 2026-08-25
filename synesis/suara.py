"""SYNESIS v0.2 - telinga dan mulut.

    python -m synesis.suara rekam 40      rekam contoh wake word
    python -m synesis.suara potong X.m4a  potong rekaman panjang jadi contoh
    python -m synesis.suara latih         latih model wake word
    python -m synesis.suara ambang        kalibrasi ambang dengan ROC
    python -m synesis.suara ucap "halo"   uji suara keluar
    python -m synesis.suara ucap en "hi"  bahasa lain: id, en, ja
    python -m synesis.suara dengar        jalankan loop penuh

Rantainya:

    mikrofon -> VAD -> wake word -> perekam -> Whisper -> pipa niat Bulan 2
             -> Piper -> RVC -> speaker

Fungsi DSP di bagian atas berkas ini adalah salinan dari
`notebooks/bulan3_sesi2_spektrogram.py`. Duplikasinya disengaja, dan
alasannya sama dengan `fitur.py` di Bulan 2: notebook adalah jawaban latihan
yang dibekukan dan tidak boleh berubah lagi, sedangkan berkas ini akan terus
berubah bersama SYNESIS. Yang tidak boleh berbeda cuma angkanya, dan `_demo`
di bawah memeriksanya.
"""

import json
import sys
import time
import wave
from pathlib import Path

import numpy as np

from . import konfig

LAJU = konfig.LAJU
BINGKAI = LAJU * konfig.BINGKAI_MS // 1000        # 400
LONCAT = LAJU * konfig.LONCAT_MS // 1000          # 160
N_FFT = 512
N_MEL = konfig.N_MEL
PRA_TEKAN = 0.97
N_BINGKAI = LAJU // LONCAT - 2                    # 98 bingkai untuk 1 detik

REKAMAN = konfig.SUARA_DIR                        # E:\SYNESIS\suara
BANGUN = REKAMAN / "bangun"
BUKAN = REKAMAN / "bukan"


def bilah(i, n, label="", lebar=32, mulai=None):
    """Bilah kemajuan satu baris. Salinan dari Bulan 3 Sesi 2."""
    i = min(i, n)
    isi = int(lebar * i / max(1, n))
    sisa = ""
    if mulai is not None and i:
        lewat = time.perf_counter() - mulai
        sisa = f"  {lewat:5.0f}s lewat, sisa ~{lewat / i * (n - i):4.0f}s"
    print(f"\r  {label:<22}|{'#' * isi}{'.' * (lebar - isi)}| "
          f"{i:>6}/{n}{sisa}   ", end="\n" if i >= n else "", flush=True)


# ══════════════════════════════════════════════════════════════
# DSP
# ══════════════════════════════════════════════════════════════

def baca_wav(berkas):
    """Baca WAV PCM 16 bit. Kembalikan (sinyal float64, laju)."""
    with wave.open(str(berkas), "rb") as w:
        kanal, lebar, laju = w.getnchannels(), w.getsampwidth(), w.getframerate()
        mentah = w.readframes(w.getnframes())
    if lebar != 2:
        raise ValueError(f"cuma PCM 16 bit, ini {lebar * 8} bit")
    x = np.frombuffer(mentah, dtype="<i2").astype(np.float64) / 32768.0
    return (x.reshape(-1, kanal).mean(axis=1) if kanal > 1 else x), laju


def tulis_wav(berkas, x, laju=LAJU):
    """Tulis WAV PCM 16 bit mono."""
    Path(berkas).parent.mkdir(parents=True, exist_ok=True)
    d = (np.clip(x, -1.0, 1.0) * 32767).astype("<i2")
    with wave.open(str(berkas), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(laju)
        w.writeframes(d.tobytes())


def baca_audio(berkas):
    """Baca berkas audio apa pun jadi mono 16 kHz. Kembalikan (sinyal, LAJU).

    WAV lewat `wave` bawaan Python; sisanya lewat `av`, yang sudah terpasang
    sebagai dependensi faster-whisper. Jadi m4a dari Perekam Suara Windows
    bisa dipakai langsung tanpa memasang ffmpeg.
    """
    berkas = Path(berkas)
    if berkas.suffix.lower() == ".wav":
        x, laju = baca_wav(berkas)
        return cuplik_ulang(x, laju, LAJU), LAJU

    import av
    wadah = av.open(str(berkas))
    ubah = av.audio.resampler.AudioResampler(format="s16", layout="mono",
                                             rate=LAJU)
    blok = []
    for bingkai in wadah.decode(audio=0):
        for hasil in ubah.resample(bingkai):
            blok.append(hasil.to_ndarray().reshape(-1))
    wadah.close()
    if not blok:
        raise ValueError(f"tidak ada audio di {berkas}")
    return np.concatenate(blok).astype(np.float64) / 32768.0, LAJU


def potong_rekaman(berkas, label="bangun", bantal_ms=150):
    """Potong satu rekaman panjang jadi berkas-berkas satu ucapan.

    Dipakai kalau kamu merekam dengan Perekam Suara Windows, bukan dengan
    `python -m synesis.suara rekam`. Batas tiap ucapan dicari VAD, jadi yang
    menentukan bukan hitungan melainkan jeda di antaranya: berhenti sekitar
    satu detik sesudah tiap ucapan dan potongannya jatuh sendiri.

    bantal_ms : audio tambahan di kedua ujung tiap potongan. Tanpa bantalan,
                konsonan awal yang lemah seperti /h/ ikut terpotong VAD.
    """
    x, laju = baca_audio(berkas)
    tujuan = REKAMAN / label
    tujuan.mkdir(parents=True, exist_ok=True)
    sudah = len(list(tujuan.glob("*.wav")))
    bantal = bantal_ms * laju // 1000

    seg = Vad().segmen(x)
    print(f"  sumber  : {Path(berkas).name}  {len(x) / laju:.1f} detik")
    print(f"  tujuan  : {tujuan}  (sudah ada {sudah})")
    print(f"  potongan: {len(seg)}\n")
    print(f"  {'no':>4}{'mulai':>9}{'durasi':>9}{'puncak':>9}  catatan")
    print("  " + "-" * 50)

    ditulis = 0
    for i, (a, b) in enumerate(seg):
        potong = x[max(0, a - bantal):b + bantal]
        lama = len(potong) / laju
        puncak = float(np.abs(potong).max())
        catatan = []
        if lama > 2.5:
            catatan.append("terlalu panjang, mungkin dua ucapan menyatu")
        if lama < 0.35:
            catatan.append("terlalu pendek, dilewati")
        if puncak > 0.99:
            catatan.append("terpotong di puncak, kecilkan volume")
        elif puncak < 0.05:
            catatan.append("terlalu pelan")

        print(f"  {i + 1:>4}{a / laju:>8.2f}s{lama:>8.2f}s{puncak:>9.3f}  "
              f"{'; '.join(catatan)}")
        if lama < 0.35:
            continue
        tulis_wav(tujuan / f"{label}_{sudah + ditulis:03d}.wav", potong, laju)
        ditulis += 1

    print(f"\n  {ditulis} berkas ditulis. Total sekarang {sudah + ditulis}.")
    return ditulis


def cuplik_ulang(x, dari, ke):
    """Ubah laju cuplik. Menapis dulu, baru mencuplik ulang.

    Mengambil satu dari sekian tanpa menapis membuat isi di atas Nyquist yang
    baru MELIPAT ke bawah, dan Bagian 7 Bulan 3 Sesi 1 mengukur bahwa
    lipatan itu tidak bisa dibedakan dari sinyal aslinya sesudah terjadi.
    """
    if dari == ke:
        return np.asarray(x, dtype=np.float64)
    from math import gcd
    from scipy.signal import resample_poly
    g = gcd(int(dari), int(ke))
    return resample_poly(np.asarray(x, dtype=np.float64), ke // g, dari // g)


def pra_tekan(x, a=PRA_TEKAN):
    """Tapis lolos-tinggi satu tap, meratakan kemiringan spektrum suara."""
    return np.append(x[0], x[1:] - a * x[:-1])


def jendela_hann(N):
    """Hann periodik. Pembagi N, bukan N-1; lihat Sesi 2."""
    return 0.5 - 0.5 * np.cos(2 * np.pi * np.arange(N) / N)


def _hz_ke_mel(f):
    return 2595.0 * np.log10(1.0 + np.asarray(f, dtype=np.float64) / 700.0)


def _mel_ke_hz(m):
    return 700.0 * (10.0 ** (np.asarray(m, dtype=np.float64) / 2595.0) - 1.0)


def _bank_mel(n_mel=N_MEL, n_fft=N_FFT, laju=LAJU, f_min=20.0):
    titik = _mel_ke_hz(np.linspace(_hz_ke_mel(f_min), _hz_ke_mel(laju / 2),
                                   n_mel + 2))
    freq = np.fft.rfftfreq(n_fft, 1.0 / laju)
    bank = np.zeros((n_mel, len(freq)))
    for i in range(n_mel):
        kiri, puncak, kanan = titik[i], titik[i + 1], titik[i + 2]
        bank[i] = np.clip(np.minimum((freq - kiri) / (puncak - kiri),
                                     (kanan - freq) / (kanan - puncak)),
                          0.0, None) * (2.0 / (kanan - kiri))
    return bank


BANK = _bank_mel()          # dihitung sekali saat impor
JENDELA = jendela_hann(BINGKAI)


def fitur_audio(x):
    """Log-mel dinormalkan. Kembalikan (bingkai, N_MEL).

    Inilah bentuk yang dilihat model wake word, dan ia harus identik dengan
    yang dipakai saat melatih. Kalau salah satu berubah, yang lain harus ikut.
    """
    from numpy.lib.stride_tricks import sliding_window_view
    y = pra_tekan(np.asarray(x, dtype=np.float64))
    if len(y) < BINGKAI:
        y = np.pad(y, (0, BINGKAI - len(y)))
    bingkai = sliding_window_view(y, BINGKAI)[::LONCAT] * JENDELA
    daya = np.abs(np.fft.rfft(bingkai, n=N_FFT, axis=-1)) ** 2
    mel = 10 * np.log10(daya @ BANK.T + 1e-10)
    return mel - mel.mean(axis=0, keepdims=True)


def satu_detik(x):
    """Patok sinyal jadi tepat satu detik."""
    x = np.asarray(x, dtype=np.float64)
    return np.pad(x, (0, max(0, LAJU - len(x))))[:LAJU]


# ══════════════════════════════════════════════════════════════
# Mikrofon
# ══════════════════════════════════════════════════════════════

def peranti_masuk():
    """Nama peranti masukan bawaan, atau None kalau tidak ada."""
    try:
        import sounddevice as sd
        i = sd.default.device[0]
        return sd.query_devices(i)["name"] if i is not None else None
    except Exception:                                        # noqa: BLE001
        return None


def rekam(detik, laju=LAJU):
    """Rekam dari mikrofon dan kembalikan sinyal mono float64."""
    import sounddevice as sd
    n = int(detik * laju)
    buf = sd.rec(n, samplerate=laju, channels=1, dtype="float32", blocking=True)
    return buf[:, 0].astype(np.float64)


def mainkan(x, laju=LAJU, tunggu=True):
    """Bunyikan sinyal ke speaker."""
    import sounddevice as sd
    sd.play(np.asarray(x, dtype=np.float32), laju)
    if tunggu:
        sd.wait()


# ══════════════════════════════════════════════════════════════
# Deteksi aktivitas suara
# ══════════════════════════════════════════════════════════════

def tenaga_db(x, panjang=LONCAT):
    """Tenaga tiap potongan dalam desibel. Satu angka per 10 milidetik."""
    n = len(x) // panjang
    if n == 0:
        return np.zeros(0)
    p = np.asarray(x[:n * panjang], dtype=np.float64).reshape(n, panjang)
    return 10 * np.log10((p ** 2).mean(axis=1) + 1e-12)


class Vad:
    """Pemisah suara dari sunyi, berdasarkan tenaga relatif lantai derau.

    Ambang mutlak tidak bekerja: lantai derau kamar berbeda-beda sampai 20 dB,
    dan penguatan mikrofon ikut berubah sendiri di Windows. Yang dipakai di
    sini persentil ke-20 dari tenaga yang sudah lewat, jadi ambangnya
    mengikuti ruangan tanpa perlu disetel.

    Histeresis dua ambang dipakai supaya satu potongan lemah di tengah kata
    tidak langsung dianggap akhir ucapan. Bunyi letup /p/ memang berhenti
    total selama 30 sampai 60 milidetik sebelum meledak.
    """

    def __init__(self, atas_db=None, diam_ms=None):
        self.atas = konfig.VAD_ATAS_DB if atas_db is None else atas_db
        self.diam = ((konfig.VAD_DIAM_MS if diam_ms is None else diam_ms)
                     // konfig.LONCAT_MS)
        self.riwayat = []
        self.lantai = None

    def perbarui_lantai(self, db):
        self.riwayat.extend(db.tolist())
        del self.riwayat[:-300]                  # tiga detik terakhir
        self.lantai = float(np.percentile(self.riwayat, 20))
        return self.lantai

    def segmen(self, x):
        """Kembalikan daftar (awal, akhir) dalam cuplikan untuk tiap ucapan."""
        db = tenaga_db(x)
        if len(db) == 0:
            return []
        lantai = self.perbarui_lantai(db)
        naik, turun = lantai + self.atas, lantai + self.atas / 2

        hasil, mulai, diam = [], None, 0
        for i, nilai in enumerate(db):
            if mulai is None:
                if nilai > naik:
                    mulai, diam = i, 0
            elif nilai > turun:
                diam = 0
            else:
                diam += 1
                if diam >= self.diam:
                    hasil.append((mulai, i - diam))
                    mulai = None
        if mulai is not None:
            hasil.append((mulai, len(db)))

        minimal = konfig.VAD_MIN_MS // konfig.LONCAT_MS
        return [(a * LONCAT, b * LONCAT) for a, b in hasil if b - a >= minimal]


# ══════════════════════════════════════════════════════════════
# Wake word
# ══════════════════════════════════════════════════════════════

def bikin_model(n_kelas=2, n_masuk=N_MEL, kanal=(32, 48, 64), seed=0):
    """CNN kecil untuk spektrogram. Sama persis dengan Bulan 3 Sesi 4."""
    import torch
    import torch.nn as nn
    torch.manual_seed(seed)
    c1, c2, c3 = kanal
    return nn.Sequential(
        nn.Conv2d(1, c1, 3, padding=1), nn.BatchNorm2d(c1), nn.ReLU(),
        nn.MaxPool2d((2, 2)),
        nn.Conv2d(c1, c2, 3, padding=1), nn.BatchNorm2d(c2), nn.ReLU(),
        nn.MaxPool2d((2, 2)),
        nn.Conv2d(c2, c3, 3, padding=1), nn.BatchNorm2d(c3), nn.ReLU(),
        nn.AdaptiveAvgPool2d((1, None)),
        nn.Flatten(),
        nn.Linear(c3 * (n_masuk // 4), n_kelas),
    )


class Wake:
    """Pendeteksi kata bangun. Muat sekali, panggil tiap jendela."""

    def __init__(self, berkas=None, ambang=None):
        self.berkas = Path(berkas or konfig.WAKE_MODEL)
        self.ambang = konfig.WAKE_AMBANG if ambang is None else ambang
        self.model = None
        self.skor_lalu = []

    def ada(self):
        return self.berkas.exists()

    def muat(self):
        if self.model is not None:
            return self
        import torch
        if not self.ada():
            raise FileNotFoundError(
                f"model wake word belum ada: {self.berkas}\n"
                "  rekam dulu: python -m synesis.suara rekam 40\n"
                "  lalu latih: python -m synesis.suara latih")
        titik = torch.load(self.berkas, map_location="cpu", weights_only=False)
        self.model = bikin_model()
        self.model.load_state_dict(titik["bobot"])
        self.model.eval()
        if "ambang" in titik:
            self.ambang = float(titik["ambang"])
        return self

    def skor(self, x):
        """Peluang bahwa potongan satu detik ini memuat kata bangun."""
        import torch
        self.muat()
        f = fitur_audio(satu_detik(x)).astype(np.float32)[None, None]
        with torch.no_grad():
            return float(torch.softmax(self.model(torch.from_numpy(f)), 1)[0, 1])

    def skor_banyak(self, potongan):
        """Skor beberapa potongan sekaligus. Jauh lebih murah daripada satu-satu."""
        import torch
        self.muat()
        f = np.stack([fitur_audio(satu_detik(p)) for p in potongan])
        with torch.no_grad():
            keluar = self.model(torch.from_numpy(f.astype(np.float32)[:, None]))
            return torch.softmax(keluar, 1)[:, 1].numpy()

    def lewat(self, skor):
        """Terapkan penghalusan lalu bandingkan dengan ambang."""
        self.skor_lalu.append(skor)
        del self.skor_lalu[:-konfig.WAKE_HALUS]
        return float(np.mean(self.skor_lalu)) >= self.ambang


def _kumpulkan_latih():
    """Susun (X, y) dari rekaman sendiri plus negatif seadanya."""
    positif = sorted(BANGUN.glob("*.wav")) if BANGUN.is_dir() else []
    if not positif:
        raise SystemExit(
            f"tidak ada rekaman di {BANGUN}\n"
            "  rekam dulu: python -m synesis.suara rekam 40")

    negatif = sorted(BUKAN.glob("*.wav")) if BUKAN.is_dir() else []
    sc = konfig.GUDANG / "data" / "speech_commands"
    if sc.is_dir():
        # Kata apa pun dari Speech Commands adalah contoh negatif yang bagus:
        # ia ucapan manusia, bukan sunyi, jadi model dipaksa membedakan KATA
        # dan bukan sekadar membedakan ada-suara dari tidak-ada-suara.
        rng = np.random.default_rng(0)
        semua = sorted(sc.glob("*/*.wav"))
        ambil = rng.choice(len(semua), size=min(len(semua), 30 * len(positif)),
                           replace=False)
        negatif += [semua[i] for i in ambil]

    X, y = [], []
    total = len(positif) + len(negatif)
    mulai = time.perf_counter()
    for daftar, label in ((positif, 1), (negatif, 0)):
        for w in daftar:
            x, laju = baca_wav(w)
            X.append(fitur_audio(satu_detik(cuplik_ulang(x, laju, LAJU))))
            y.append(label)
            if len(X) % 100 == 0 or len(X) == total:
                bilah(len(X), total, "fitur", mulai=mulai)
    return np.stack(X).astype(np.float32), np.array(y), len(positif), len(negatif)


def latih_wake(epoch=25, seed=0):
    """Latih model wake word dari rekaman sendiri. Simpan ke konfig.WAKE_MODEL."""
    import torch
    import torch.nn as nn

    X, y, n_pos, n_neg = _kumpulkan_latih()
    print(f"  positif {n_pos}  negatif {n_neg}")

    rng = np.random.default_rng(seed)
    urut = rng.permutation(len(X))
    potong = int(0.8 * len(X))
    latih, uji = urut[:potong], urut[potong:]

    Xl = torch.from_numpy(X[latih]).unsqueeze(1)
    yl = torch.from_numpy(y[latih])
    Xu = torch.from_numpy(X[uji]).unsqueeze(1)
    yu = torch.from_numpy(y[uji])

    torch.manual_seed(seed)
    model = bikin_model()
    opt = torch.optim.AdamW(model.parameters(), lr=3e-3, weight_decay=1e-4)
    jadwal = torch.optim.lr_scheduler.CosineAnnealingLR(opt, epoch)
    # Kelas positif jauh lebih sedikit, jadi bobotnya dinaikkan. Tanpa ini
    # model belajar menjawab "bukan" untuk apa pun dan tetap 97 persen benar.
    rugi_fn = nn.CrossEntropyLoss(
        weight=torch.tensor([1.0, float(n_neg) / max(1, n_pos)]))

    mulai = time.perf_counter()
    for e in range(epoch):
        model.train()
        acak = torch.randperm(len(Xl))
        for i in range(0, len(acak), 32):
            ambil = acak[i:i + 32]
            opt.zero_grad(set_to_none=True)
            rugi_fn(model(Xl[ambil]), yl[ambil]).backward()
            opt.step()
        jadwal.step()
        bilah(e + 1, epoch, "latih wake word", mulai=mulai)

    model.eval()
    with torch.no_grad():
        skor = torch.softmax(model(Xu), 1)[:, 1].numpy()
    ambang, far, frr, auc = roc(skor[yu.numpy() == 1], skor[yu.numpy() == 0])
    pilih = pilih_ambang(ambang, far, frr)

    konfig.WAKE_MODEL.parent.mkdir(parents=True, exist_ok=True)
    torch.save({"bobot": model.state_dict(), "ambang": float(pilih),
                "auc": float(auc), "n_pos": n_pos, "n_neg": n_neg},
               konfig.WAKE_MODEL)
    print(f"  AUC {auc:.4f}  ambang {pilih:.3f}  -> {konfig.WAKE_MODEL}")
    return auc, pilih


def roc(positif, negatif):
    """Kurva ROC. Kembalikan (ambang, FAR, FRR, AUC).

    `rankdata` dipakai, bukan `argsort().argsort()`, supaya skor yang SERI
    mendapat peringkat rerata. Model yang yakin menghasilkan banyak skor
    yang jenuh tepat di 0,0 dan 1,0, dan tanpa penanganan seri, AUC-nya
    ditentukan oleh urutan kebetulan.
    """
    from scipy.stats import rankdata

    p, n = np.sort(np.asarray(positif)), np.sort(np.asarray(negatif))
    if len(p) == 0 or len(n) == 0:
        return np.array([0.5]), np.array([1.0]), np.array([1.0]), 0.5
    ambang = np.unique(np.concatenate([p, n]))
    far = np.array([(n >= t).mean() for t in ambang])
    frr = np.array([(p < t).mean() for t in ambang])
    peringkat = rankdata(np.concatenate([p, n]))
    auc = ((peringkat[:len(p)].sum() - len(p) * (len(p) + 1) / 2)
           / (len(p) * len(n)))
    return ambang, far, frr, float(auc)


def pilih_ambang(ambang, far, frr, ongkos_salah_terima=100.0):
    """Pilih ambang yang meminimalkan ongkos, bukan yang menyamakan kesalahan.

    Kerangkanya sama dengan `niat.ambang_dari_ongkos` di Bulan 2: kedua
    kesalahan tidak sama mahal, jadi titik kesalahan setara bukan jawabannya.

    Salah menolak  : kamu mengulang sekali. Ongkos 1.
    Salah menerima : SYNESIS menyala di tengah percakapan, merekam, lalu
                     melempar apa pun yang terdengar ke pipa niat. Ongkos 100.
    """
    ongkos = ongkos_salah_terima * far + 1.0 * frr
    return float(ambang[int(np.argmin(ongkos))])


# ══════════════════════════════════════════════════════════════
# Pengenal ucapan
# ══════════════════════════════════════════════════════════════

_whisper = None


def _panaskan_cudnn():
    """Paksa torch memuat cuDNN-nya sendiri sebelum ctranslate2 memuat miliknya.

    Terukur: kalau faster-whisper dipanggil lebih dulu, panggilan RVC
    berikutnya mati dengan `Could not load symbol cudnnGetLibConfig.
    Error code 127`. Dua pustaka membawa cuDNN sendiri-sendiri, dan yang
    memuat belakangan menemukan simbol milik yang duluan.

    ponytail: satu konvolusi 3x3 di atas tensor 8x8 sudah cukup untuk
    mengunci urutannya. Kalau nanti ctranslate2 dan torch memakai cuDNN yang
    sama, baris ini boleh dihapus.
    """
    try:
        import torch
        import torch.nn.functional as F
        if not torch.cuda.is_available():
            return
        F.conv2d(torch.zeros(1, 1, 8, 8, device="cuda"),
                 torch.zeros(1, 1, 3, 3, device="cuda"))
        torch.cuda.synchronize()
    except Exception:                                        # noqa: BLE001
        pass                                                 # CPU saja, aman


def transkrip(x, laju=LAJU, bahasa=None):
    """Ubah sinyal jadi teks. Kembalikan string, mungkin kosong.

    bahasa : kode dua huruf. Kosong berarti `konfig.STT_BAHASA`. Dipatok,
             bukan dideteksi otomatis, karena deteksi bahasa Whisper sering
             meleset pada ucapan pendek dan sekali meleset seluruh
             transkripsinya ikut salah.
    """
    global _whisper
    if _whisper is None:
        _panaskan_cudnn()
        from faster_whisper import WhisperModel
        _whisper = WhisperModel(konfig.STT_MODEL, device=konfig.STT_PERANTI,
                                compute_type=konfig.STT_TIPE,
                                download_root=str(konfig.GUDANG / "models" / "stt"))
    x = cuplik_ulang(np.asarray(x, dtype=np.float32), laju, 16000)
    # ponytail: transkripsi baru dimulai sesudah ucapannya selesai. Terukur
    # RTF 0,77, jadi tahap ini memakan 55 persen anggaran latensi 3 detik.
    # Upgrade path kalau anggarannya mulai terlewati: mulai mentranskripsi
    # sambil merekam, lalu buang hasilnya kalau penuturnya melanjutkan.
    segmen, _ = _whisper.transcribe(x.astype(np.float32),
                                    language=bahasa or konfig.STT_BAHASA,
                                    vad_filter=True, beam_size=1)
    return " ".join(s.text.strip() for s in segmen).strip()


# ══════════════════════════════════════════════════════════════
# Suara keluar
# ══════════════════════════════════════════════════════════════

_piper = {}
_yukino = None


def sintesis(teks, model=None):
    """Ucapkan teks lewat Piper. Kembalikan (sinyal, laju).

    model : jalur berkas .onnx Piper. Kosong berarti `konfig.PIPER_MODEL`,
            yaitu suara bahasa Indonesia.

    Tiap model dimuat sekali lalu disimpan, jadi berganti bahasa di tengah
    jalan tidak membayar ongkos muat dua kali. Warna suaranya toh diganti RVC
    sesudah ini; yang ditentukan model Piper cuma bahasa dan iramanya.
    """
    if isinstance(model, str) and model in konfig.PIPER_SUARA:
        model = konfig.PIPER_SUARA[model]        # "id", "en", "ja"
    jalur = str(model or konfig.PIPER_MODEL)
    if jalur not in _piper:
        from piper import PiperVoice
        _piper[jalur] = PiperVoice.load(jalur)
    suara_piper = _piper[jalur]
    potong = list(suara_piper.synthesize(teks))
    if not potong:
        return np.zeros(0), suara_piper.config.sample_rate
    x = np.concatenate([np.frombuffer(c.audio_int16_bytes, dtype="<i2")
                        for c in potong]).astype(np.float64) / 32768.0
    return x, suara_piper.config.sample_rate


def warnai(x, laju):
    """Ganti warna suara dengan model RVC. Kembalikan (sinyal, laju baru)."""
    global _yukino
    from . import rvc
    if _yukino is None:
        _yukino = rvc.Yukino()
    return _yukino.ubah(cuplik_ulang(x, laju, LAJU), nada=konfig.RVC_NADA)


def ucap(teks, mainkan_juga=True, simpan=None, model=None):
    """Rantai penuh suara keluar: Piper, lalu RVC, lalu speaker."""
    x, laju = sintesis(teks, model)
    if konfig.RVC_AKTIF and Path(konfig.RVC_MODEL).exists() and len(x):
        x, laju = warnai(x, laju)
    if simpan:
        tulis_wav(simpan, x, laju)
    if mainkan_juga and len(x):
        mainkan(x, laju)
    return x, laju


# ══════════════════════════════════════════════════════════════
# Loop
# ══════════════════════════════════════════════════════════════

def rekam_contoh(jumlah, jeda=2.0, panjang=1.5):
    """Rekam contoh kata bangun satu per satu, dengan hitungan mundur."""
    BANGUN.mkdir(parents=True, exist_ok=True)
    sudah = len(list(BANGUN.glob("*.wav")))
    print(f"  peranti : {peranti_masuk()}")
    print(f"  simpan  : {BANGUN}  (sudah ada {sudah})")
    print(f"\n  Ucapkan \"hey synesis\" tiap kali muncul REKAM.")
    print("  Ubah-ubah jaraknya, nada bicaranya, dan arah kepalamu. Contoh yang")
    print("  seragam menghasilkan model yang cuma bekerja pada satu keadaan.\n")
    for i in range(jumlah):
        for sisa in range(int(jeda), 0, -1):
            print(f"    {i + 1}/{jumlah}  bersiap {sisa}   ", end="\r", flush=True)
            time.sleep(1)
        print(f"    {i + 1}/{jumlah}  REKAM         ", end="\r", flush=True)
        x = rekam(panjang)
        berkas = BANGUN / f"bangun_{sudah + i:03d}.wav"
        tulis_wav(berkas, x)
        print(f"    {i + 1}/{jumlah}  tersimpan {berkas.name}  "
              f"puncak {np.abs(x).max():.3f}")
    print(f"\n  selesai. Latih dengan: python -m synesis.suara latih")


def panaskan(diam=False):
    """Muat ketiga model besar sebelum loop dimulai. Kembalikan detik terpakai.

    Tanpa ini, ongkos muat dibayar di tengah perintah PERTAMA, dan terukur
    23,3 detik: 2,4 untuk wake word, 8,2 untuk Whisper, 12,7 untuk Piper
    ditambah ContentVec ditambah RVC. Perintah kedua dan seterusnya cuma 2,6
    detik.

    Ongkosnya tidak hilang, cuma dipindah ke tempat yang benar. Menunggu 23
    detik di layar pembuka dengan bilah kemajuan adalah hal yang berbeda dari
    menunggu 23 detik sesudah mengucapkan perintah dan mengira SYNESIS
    menggantung.
    """
    mulai = time.perf_counter()
    tahap = [
        ("wake word", lambda: Wake().muat()),
        ("Whisper", lambda: transkrip(np.zeros(LAJU))),
        ("Piper dan RVC", lambda: ucap("Siap.", mainkan_juga=False)),
    ]
    for i, (nama, kerja) in enumerate(tahap):
        if not diam:
            bilah(i, len(tahap), f"memuat {nama}", mulai=mulai)
        try:
            kerja()
        except Exception as e:                                # noqa: BLE001
            if not diam:
                print(f"\n  {nama} gagal dimuat: {type(e).__name__}: {e}")
    if not diam:
        bilah(len(tahap), len(tahap), "siap", mulai=mulai)
    return time.perf_counter() - mulai


def dengar(kering=True, batas=None):
    """Loop utama: dengar, bangun, rekam, transkrip, jalankan, jawab."""
    import sounddevice as sd

    from . import niat

    panaskan()
    wake = Wake().muat()
    model = niat.muat_model()
    vad = Vad()

    jendela = LAJU                                   # satu detik
    loncat = LAJU * konfig.WAKE_LONCAT_MS // 1000    # 100 ms
    sabuk = np.zeros(jendela)
    n_bangun = 0

    print(f"  peranti : {peranti_masuk()}")
    print(f"  ambang  : {wake.ambang:.3f}   mode: "
          f"{'DRY RUN' if kering else 'LIVE'}")
    print("  Katakan \"hey synesis\". Ctrl+C untuk berhenti.\n")

    with sd.InputStream(samplerate=LAJU, channels=1, dtype="float32",
                        blocksize=loncat) as aliran:
        try:
            while batas is None or n_bangun < batas:
                blok, _ = aliran.read(loncat)
                sabuk = np.concatenate([sabuk[loncat:], blok[:, 0]])

                db = tenaga_db(sabuk[-loncat:])
                lantai = vad.perbarui_lantai(db)
                if db.max() < lantai + konfig.VAD_ATAS_DB / 2:
                    wake.skor_lalu.clear()          # ruangan sunyi, lewati
                    continue

                if not wake.lewat(wake.skor(sabuk)):
                    continue

                n_bangun += 1
                print(f"  [bangun] skor {np.mean(wake.skor_lalu):.3f}")
                wake.skor_lalu.clear()

                # Pra-gulung: 300 milidetik terakhir dari sabuk ikut direkam.
                # Tanpa ini, kata pertama perintah hilang untuk orang yang
                # tidak berhenti sesudah "hey synesis". Ongkosnya nol, karena
                # audionya memang sudah ada di memori.
                ucapan = rekam_sampai_diam(aliran, vad,
                                           awalan=sabuk[-3 * LAJU // 10:])
                sabuk[:] = 0.0
                if len(ucapan) < konfig.VAD_MIN_MS * LAJU // 1000:
                    print("  (tidak ada yang terdengar)")
                    continue

                teks = transkrip(ucapan)
                print(f"  kamu > {teks or '(kosong)'}")
                if not teks:
                    continue

                h = niat.jalankan_pipa(teks, model, izin=niat.izin_konsol,
                                       kering=kering)
                print(f"  {h['intent'] or '(tak dikenal)'}  "
                      f"conf {h['yakin']:.3f}  -> {h['tindakan']}")
                jawab = ringkas_jawaban(h)
                print(f"  synesis > {jawab}")
                ucap(jawab)
        except KeyboardInterrupt:
            print("\n  berhenti.")
    return n_bangun


def rekam_sampai_diam(aliran, vad, maks=None, awalan=None):
    """Rekam dari aliran yang sedang terbuka sampai penuturnya berhenti.

    awalan : audio yang sudah terlanjur lewat, ditempel di depan hasilnya.
    """
    maks = maks or konfig.VAD_MAKS_DETIK
    loncat = LAJU * konfig.LONCAT_MS // 1000
    butuh = konfig.VAD_DIAM_MS // konfig.LONCAT_MS
    kumpul = [np.asarray(awalan, dtype=np.float64)] if awalan is not None else []
    diam = 0
    while sum(len(k) for k in kumpul) < maks * LAJU:
        blok, _ = aliran.read(loncat)
        kumpul.append(blok[:, 0].astype(np.float64))
        db = tenaga_db(kumpul[-1])
        if len(db) and db.max() > vad.lantai + konfig.VAD_ATAS_DB / 2:
            diam = 0
        else:
            diam += 1
            if diam >= butuh and len(kumpul) > butuh:
                break
    return np.concatenate(kumpul) if kumpul else np.zeros(0)


ANGKA = {"satu": 1, "dua": 2, "tiga": 3, "empat": 4, "lima": 5, "enam": 6,
         "tujuh": 7, "delapan": 8, "sembilan": 9, "sepuluh": 10,
         "sebelas": 11, "dua belas": 12,
         "pertama": 1, "kedua": 2, "ketiga": 3, "keempat": 4, "kelima": 5,
         "keenam": 6, "ketujuh": 7, "kedelapan": 8, "kesembilan": 9,
         "kesepuluh": 10}


def nomor_pilihan(teks, batas):
    """Baca "nomor dua", "yang ketiga", atau "2" jadi indeks. None kalau bukan.

    Dipanggil hanya ketika ada daftar pilihan yang sedang menunggu, jadi
    kalimat biasa yang kebetulan memuat angka tidak akan tertafsir sebagai
    pilihan di saat yang salah.
    """
    import re
    t = " " + teks.lower().strip().strip(".!?") + " "
    for kata, n in sorted(ANGKA.items(), key=lambda kv: -len(kv[0])):
        if f" {kata} " in t:
            return n if 1 <= n <= batas else None
    angka = re.findall(r"\b(\d{1,2})\b", t)
    if angka:
        n = int(angka[0])
        return n if 1 <= n <= batas else None
    return None


def ringkas_jawaban(h, maks_baca=5):
    """Ubah hasil pipa niat jadi kalimat yang enak didengar.

    Layar boleh menampilkan dua puluh baris; telinga tidak. Tetapi memotongnya
    jadi "ada 13 baris lagi di layar" salah untuk kanal suara: kalau kamu
    sedang memakai SYNESIS lewat mikrofon, kamu belum tentu sedang melihat
    layar. Jadi daftar pilihan DIBACAKAN, bukan dirujuk.

    maks_baca : berapa pilihan yang diucapkan sebelum menyuruh melihat layar.
                Lima dipilih karena itu batas ingatan pendengaran orang untuk
                daftar yang tidak bisa diulang.
    """
    if not h.get("intent"):
        return "Maaf, saya belum yakin maksudnya."
    if h.get("tindakan") == "tolak":
        return "Saya belum cukup yakin. Coba ulangi dengan kalimat lain."
    hasil = str(h.get("hasil") or "").strip()
    if not hasil:
        return "Sudah."

    baris = [b for b in hasil.splitlines() if b.strip()]

    # Daftar pilihan bernomor: bacakan isinya, bukan jumlahnya.
    from . import alat
    if alat.PILIHAN and "Say the number" in baris[0]:
        n = len(alat.PILIHAN)
        nama = [p.name for p in alat.PILIHAN[:maks_baca]]
        urut = ". ".join(f"{i + 1}, {a}" for i, a in enumerate(nama))
        ekor = (f" Ada {n - maks_baca} lagi." if n > maks_baca else "")
        return (f"Ketemu {n} berkas. {urut}.{ekor} "
                f"Sebutkan nomornya.")

    # Daftar hasil pencarian: bacakan nama berkasnya saja, tanpa jalur.
    if baris[0].startswith(("Found:", "Ditemukan:")):
        nama = [b.strip().split("\\")[-1].split("/")[-1]
                for b in baris[1:maks_baca + 1]]
        sisa = len(baris) - 1 - len(nama)
        ekor = f" Ada {sisa} lagi." if sisa > 0 else ""
        return f"Ketemu {len(baris) - 1} berkas. " + ". ".join(nama) + "." + ekor

    if len(baris) == 1:
        return baris[0][:200]
    return f"{baris[0][:160]} Ada {len(baris) - 1} baris lagi di layar."


# ══════════════════════════════════════════════════════════════
# CLI dan pemeriksa
# ══════════════════════════════════════════════════════════════

def _demo():
    """Pemeriksa yang jalan tanpa mikrofon, tanpa model, tanpa speaker."""
    # Bentuk fitur harus persis yang diharapkan model.
    x = np.random.default_rng(0).normal(0, 0.05, LAJU)
    f = fitur_audio(satu_detik(x))
    assert f.shape == (N_BINGKAI, N_MEL), f.shape
    # Normalisasi rerata: tiap kolom harus berpusat di nol.
    assert np.abs(f.mean(axis=0)).max() < 1e-9

    # Bank mel harus menutup seluruh pita tanpa celah.
    assert BANK.shape == (N_MEL, N_FFT // 2 + 1)
    assert (BANK.sum(axis=0) > 0).mean() > 0.98

    # Pencuplikan ulang harus mengubah panjang sesuai rasionya.
    y = cuplik_ulang(np.zeros(22050), 22050, 16000)
    assert abs(len(y) - 16000) <= 1, len(y)

    # VAD harus menemukan satu ucapan dan bukan dua.
    rng = np.random.default_rng(1)
    sunyi = rng.normal(0, 1e-3, LAJU)
    kata = rng.normal(0, 0.1, LAJU // 2)
    uji = np.concatenate([sunyi, kata, sunyi])
    seg = Vad().segmen(uji)
    assert len(seg) == 1, seg
    assert abs(seg[0][0] - LAJU) < 0.15 * LAJU, seg

    # Ambang harus condong ke sisi aman waktu salah terima jauh lebih mahal.
    ambang = np.array([0.1, 0.5, 0.9])
    far = np.array([0.50, 0.10, 0.001])
    frr = np.array([0.00, 0.05, 0.300])
    assert pilih_ambang(ambang, far, frr) == 0.9

    # WAV pulang pergi tanpa berubah lebih dari satu bit.
    import tempfile
    berkas = Path(tempfile.gettempdir()) / "synesis_uji_suara.wav"
    asli = np.sin(2 * np.pi * 220 * np.arange(LAJU) / LAJU) * 0.5
    tulis_wav(berkas, asli)
    balik, laju = baca_wav(berkas)
    assert laju == LAJU and np.abs(balik - asli).max() < 2e-4
    berkas.unlink(missing_ok=True)

    # Ringkasan jawaban tidak boleh melempar untuk bentuk hasil apa pun.
    for h in ({}, {"intent": "baca_berkas", "tindakan": "tolak"},
              {"intent": "x", "tindakan": "jalan", "hasil": "a\nb\nc"}):
        assert isinstance(ringkas_jawaban(h), str)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    perintah = argv[0] if argv else "bantuan"

    if perintah == "rekam":
        rekam_contoh(int(argv[1]) if len(argv) > 1 else 40)
    elif perintah == "potong":
        if len(argv) < 2:
            print("  pakai: python -m synesis.suara potong <berkas> [label]")
            return 1
        potong_rekaman(argv[1], argv[2] if len(argv) > 2 else "bangun")
    elif perintah == "latih":
        latih_wake()
    elif perintah == "ambang":
        import torch
        titik = torch.load(konfig.WAKE_MODEL, map_location="cpu",
                           weights_only=False)
        print(json.dumps({k: v for k, v in titik.items() if k != "bobot"},
                         indent=2))
    elif perintah == "ucap":
        # python -m synesis.suara ucap [id|en|ja] "teks"
        sisa = argv[1:]
        bahasa = sisa.pop(0) if sisa and sisa[0] in konfig.PIPER_SUARA else None
        teks = " ".join(sisa) or "Halo, saya SYNESIS."
        t0 = time.perf_counter()
        x, laju = ucap(teks, model=bahasa)
        print(f"  {len(x) / laju:.2f} detik audio dalam "
              f"{time.perf_counter() - t0:.2f} detik, laju {laju}")
    elif perintah == "panaskan":
        print(f"  siap dalam {panaskan():.1f} detik")
    elif perintah == "dengar":
        dengar(kering="--sungguhan" not in argv)
    elif perintah == "uji":
        _demo()
        print("suara: semua lulus")
    else:
        print(__doc__)
    return 0


if __name__ == "__main__":
    sys.exit(main())
