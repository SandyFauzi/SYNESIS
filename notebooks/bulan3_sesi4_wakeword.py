"""Bulan 3 Sesi 4 - keyword spotter, lalu wake word buatanmu sendiri.

Jalankan:
    . .\\scripts\\activate.ps1
    python scripts\\unduh_speech_commands.py      (sekali saja, sekitar 40 menit)
    python notebooks\\bulan3_sesi4_wakeword.py

Tiga sesi terakhir menyiapkan alatnya. Malam ini alat itu dipakai untuk
melatih model yang benar-benar mendengar.

Ada satu perbedaan besar dengan Bulan 2 yang perlu kamu sadari sejak awal.
Di Bulan 2, himpunan ujimu 41 kalimat, dan selang kepercayaannya 30 poin,
sehingga hampir semua selisih antarresep tidak bisa dibaca. Di sini himpunan
ujinya ribuan ucapan dari pembicara yang tidak pernah dilihat model. Untuk
pertama kalinya sejak Agustus, selisih dua poin benar-benar berarti dua poin.

Enam bagian:

    1  data: belahan menurut PEMBICARA, bukan menurut berkas
    2  fitur dihitung sekali lalu disimpan, dan alasannya diukur
    3  model dasar 12 kelas, lalu hipotesis log-mel lawan MFCC diuji
    4  augmentasi: geseran waktu dan derau latar, keduanya diukur
    5  wake word: dari 12 kelas jadi 2, dan ambangnya dikalibrasi ROC
    6  deteksi mengalir: jendela geser, penghalusan, dan latensinya

Bagian bertanda TODO kamu yang isi.
"""

import hashlib
import re
import sys
import time
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))

from bulan3_sesi2_spektrogram import (  # noqa: E402
    LAJU, LONCAT, N_MEL, N_MFCC, baca_wav, bilah, fitur_audio, koma,
    matriks_dct, ribuan)

GARIS = "=" * 66
FIGUR = Path(__file__).resolve().parent.parent / "figures"
FIGUR.mkdir(exist_ok=True)

SUARA = Path(r"E:\SYNESIS\data\speech_commands")
GUDANG = Path(r"E:\SYNESIS\data")
REKAMAN = Path(r"E:\SYNESIS\suara")          # rekaman suaramu sendiri, Sesi 5

INTI = ("yes", "no", "up", "down", "left", "right", "on", "off", "stop", "go")
ASING = ("bed", "bird", "cat", "dog", "happy", "house", "marvin", "sheila",
         "tree", "wow")
KELAS = ("_sunyi_", "_asing_") + INTI
ASING_MAKS = 400        # per kata asing, supaya kelas _asing_ tidak mendominasi
SUNYI_N = 2400          # potongan sunyi yang dibuat dari derau latar

N_BINGKAI = LAJU // LONCAT - 2               # 98 bingkai untuk 1 detik


# ══════════════════════════════════════════════════════════════
# BAGIAN 1 - belahan menurut pembicara
# ══════════════════════════════════════════════════════════════

def belahan(nama_berkas, persen_valid=10, persen_uji=10):
    """Tentukan belahan sebuah berkas: 'latih', 'valid', atau 'uji'.

    Ini fungsi resmi Speech Commands, ditulis ulang. Yang membuatnya penting
    bukan bahwa ia resmi, melainkan APA yang di-hash: bagian nama berkas
    SEBELUM `_nohash_`, yaitu identitas pembicara.

    Nama berkasnya berbentuk `<id_pembicara>_nohash_<n>.wav`. Satu pembicara
    biasanya menyumbang beberapa rekaman untuk kata yang sama. Kalau
    belahannya diacak per BERKAS, rekaman pembicara yang sama bisa jatuh di
    latih dan di uji sekaligus, dan model tinggal mengenali suaranya.
    Akurasi ujinya naik beberapa poin tanpa satu pun perbaikan nyata.

    Ini kesalahan yang sama dengan yang kamu hindari di Bulan 2 waktu
    memisahkan `perintah_eval_real.txt` dari data latih, cuma dengan sumber
    kebocoran yang berbeda.

    Hash dipakai, bukan pengacak, supaya keputusan tiap pembicara TETAP
    meskipun berkas ditambah atau dikurangi kemudian.

    TODO 1
    """
    dasar = Path(nama_berkas).name
    pembicara = re.sub(r"_nohash_.*$", "", dasar)
    maks = 2 ** 27 - 1
    nilai = int(hashlib.sha1(pembicara.encode()).hexdigest(), 16)
    persen = (nilai % (maks + 1)) * (100.0 / maks)
    if persen < persen_valid:
        return "valid"
    if persen < persen_valid + persen_uji:
        return "uji"
    return "latih"


def daftar_berkas():
    """Kumpulkan (jalur, indeks_kelas, belahan) untuk seluruh data. Disediakan."""
    baris = []
    for k, kata in enumerate(INTI):
        for w in sorted((SUARA / kata).glob("*.wav")):
            baris.append((w, KELAS.index(kata), belahan(w)))
    for kata in ASING:
        d = SUARA / kata
        if d.is_dir():
            for w in sorted(d.glob("*.wav"))[:ASING_MAKS]:
                baris.append((w, KELAS.index("_asing_"), belahan(w)))
    return baris


def derau_latar():
    """Muat seluruh berkas derau latar sebagai satu daftar sinyal. Disediakan."""
    d = SUARA / "_background_noise_"
    return [baca_wav(w)[0] for w in sorted(d.glob("*.wav"))] if d.is_dir() else []


def bagian1():
    print(GARIS, "\nBAGIAN 1  belahan menurut pembicara\n", GARIS, sep="")

    if not SUARA.is_dir():
        print("  Speech Commands belum ada. Jalankan dulu:")
        print("    python scripts\\unduh_speech_commands.py")
        raise SystemExit(1)

    baris = daftar_berkas()
    hitung = {"latih": 0, "valid": 0, "uji": 0}
    for _, _, b in baris:
        hitung[b] += 1
    n = len(baris)

    print(f"  berkas terpakai : {ribuan(n)}")
    print(f"  kelas           : {len(KELAS)}  {', '.join(KELAS)}\n")
    print(f"  {'belahan':<10}{'berkas':>10}{'persen':>10}")
    print("  " + "-" * 30)
    for b in ("latih", "valid", "uji"):
        print(f"  {b:<10}{ribuan(hitung[b]):>10}{hitung[b] / n * 100:>9.1f}%")

    # Bukti bahwa belahannya benar-benar terpisah menurut pembicara.
    milik = {}
    for w, _, b in baris:
        milik.setdefault(re.sub(r"_nohash_.*$", "", w.name), set()).add(b)
    bocor = sum(1 for s in milik.values() if len(s) > 1)
    print(f"\n  pembicara berbeda            : {ribuan(len(milik))}")
    print(f"  pembicara di lebih dari satu : {bocor}")

    print(f"""
  Baris terakhir harus nol, dan kalau ia tidak nol maka seluruh angka di sesi
  ini tidak berarti apa-apa.

  Cara mudah membuatnya tidak nol: ganti `belahan` dengan pengacak biasa atas
  daftar berkas. Akurasi ujinya akan naik beberapa poin, dan tidak ada satu
  pun tanda bahwa yang naik cuma kemampuan mengenali suara orang yang sudah
  pernah didengar.

  Di Bulan 2 kebocoran yang sama muncul dalam bentuk lain: kalimat uji yang
  ikut masuk korpus pembangun vektor kata. Sumbernya berbeda, akibatnya
  sama, dan pemeriksanya juga sama, yaitu satu baris yang menghitung irisan.""")

    return baris


# ══════════════════════════════════════════════════════════════
# BAGIAN 2 - fitur dihitung sekali
# ══════════════════════════════════════════════════════════════

def satu_detik(x, rng=None, geser=0):
    """Patok sinyal jadi tepat satu detik, dengan geseran opsional.

    geser : jumlah cuplikan maksimum untuk digeser acak. 0 berarti tidak
            digeser. Dipakai Bagian 4 sebagai augmentasi.

    Disediakan.
    """
    x = np.pad(x, (0, max(0, LAJU - len(x))))[:LAJU]
    if geser and rng is not None:
        d = int(rng.integers(-geser, geser + 1))
        x = np.roll(x, d)
        if d > 0:
            x[:d] = 0.0
        elif d < 0:
            x[d:] = 0.0
    return x


def bangun_fitur(baris, derau, berkas_cache=GUDANG / "kws_logmel.npz"):
    """Hitung log-mel untuk seluruh berkas, lalu simpan. Disediakan.

    Disimpan sebagai float16. Ketelitiannya sekitar tiga angka berarti, dan
    nilai log-mel berkisar puluhan desibel, jadi galat kuantisasinya di orde
    0,01 dB. Itu jauh di bawah selisih antarucapan mana pun, dan memotong
    ukuran berkasnya jadi separuh.
    """
    if berkas_cache.exists():
        d = np.load(berkas_cache)
        return d["X"], d["y"], d["b"]

    rng = np.random.default_rng(0)
    X = np.empty((len(baris) + SUNYI_N, N_BINGKAI, N_MEL), dtype=np.float16)
    y = np.empty(len(baris) + SUNYI_N, dtype=np.int64)
    b = np.empty(len(baris) + SUNYI_N, dtype="<U5")

    mulai = time.perf_counter()
    for i, (w, kelas, bagi) in enumerate(baris):
        X[i] = fitur_audio(satu_detik(baca_wav(w)[0]))
        y[i] = kelas
        b[i] = bagi
        if (i + 1) % 200 == 0 or i + 1 == len(baris):
            bilah(i + 1, len(baris), "fitur log-mel", mulai=mulai)

    # Kelas sunyi dibuat dari potongan derau latar. Belahannya diacak, dan
    # itu tidak melanggar aturan pembicara karena tidak ada pembicara di sini.
    mulai = time.perf_counter()
    for j in range(SUNYI_N):
        d = derau[int(rng.integers(len(derau)))]
        awal = int(rng.integers(0, len(d) - LAJU))
        keras = float(rng.uniform(0.0, 0.6))
        X[len(baris) + j] = fitur_audio(d[awal:awal + LAJU] * keras)
        y[len(baris) + j] = KELAS.index("_sunyi_")
        b[len(baris) + j] = ("latih", "valid", "uji")[
            int(rng.choice(3, p=[0.8, 0.1, 0.1]))]
        if (j + 1) % 200 == 0 or j + 1 == SUNYI_N:
            bilah(j + 1, SUNYI_N, "potongan sunyi", mulai=mulai)

    berkas_cache.parent.mkdir(parents=True, exist_ok=True)
    print("    menyimpan cache, ini memakan waktu sebentar ...", flush=True)
    np.savez_compressed(berkas_cache, X=X, y=y, b=b)
    print(f"    disimpan: {berkas_cache.name}  "
          f"{berkas_cache.stat().st_size / 1e6:.0f} MB")
    return X, y, b


def bagian2(baris, derau):
    print("\n" + GARIS, "\nBAGIAN 2  fitur dihitung sekali, bukan tiap epoch\n",
          GARIS, sep="")

    # Ongkos menghitung fitur satu berkas, diukur sebelum memutuskan.
    contoh = baris[0][0]
    x = satu_detik(baca_wav(contoh)[0])
    t0 = time.perf_counter()
    for _ in range(50):
        fitur_audio(x)
    per_berkas = (time.perf_counter() - t0) / 50 * 1000

    n_total = len(baris) + SUNYI_N
    print(f"  waktu fitur per berkas      : {per_berkas:.2f} ms")
    print(f"  berkas                      : {ribuan(n_total)}")
    print(f"  sekali hitung               : {per_berkas * n_total / 1000:.0f} detik")
    print(f"  dihitung ulang tiap epoch   : "
          f"{per_berkas * n_total / 1000 * 12:.0f} detik untuk 12 epoch\n")

    X, y, b = bangun_fitur(baris, derau)
    print(f"  X {X.shape} {X.dtype}  = {X.nbytes / 1e6:.0f} MB di memori")

    print(f"\n  {'kelas':<10}{'latih':>9}{'valid':>9}{'uji':>9}{'total':>9}")
    print("  " + "-" * 46)
    for k, nama in enumerate(KELAS):
        r = [(y == k) & (b == s) for s in ("latih", "valid", "uji")]
        print(f"  {nama:<10}" + "".join(f"{int(t.sum()):>9}" for t in r)
              + f"{int((y == k).sum()):>9}")

    print("""
  Menyimpan fitur adalah keputusan yang perlu dibela, dan pembelaannya bukan
  cuma kecepatan. Ada dua akibat yang berlawanan arah:

    untung  fiturnya dihitung sekali, bukan dua belas kali. Waktu yang hemat
            terbaca di tabel atas.
    rugi    augmentasi jadi tidak mungkin dilakukan di ranah waktu, karena
            sinyalnya sudah hilang. Geseran waktu masih bisa dikerjakan di
            ranah bingkai, tetapi penambahan derau tidak.

  Bagian 4 menabrak batas itu secara langsung, dan menyelesaikannya dengan
  cara yang jujur: augmentasi derau dikerjakan di ranah waktu untuk sebagian
  kecil data, dan hasilnya diukur terhadap yang tanpa augmentasi.

  Aturan yang layak dibawa: cache mempercepat percobaan dan mempersempit
  ruang percobaan yang bisa kamu lakukan. Keduanya nyata.""")

    return X, y, b


# ══════════════════════════════════════════════════════════════
# BAGIAN 3 - model dasar 12 kelas
# ══════════════════════════════════════════════════════════════

def bikin_model(n_kelas, n_masuk=N_MEL, kanal=(32, 48, 64), seed=0):
    """CNN kecil untuk spektrogram. Kembalikan nn.Module. Disediakan.

    Seed dipatok DI SINI, bukan di `latih_torch`. Bedanya menentukan: bobot
    awal ditentukan saat model dibangun, jadi menyetel seed sesudahnya tidak
    mengubah apa pun. Tanpa baris ini, dua baris tabel yang seharusnya cuma
    berbeda pada fiturnya juga berbeda pada bobot awalnya, dan seluruh
    perbandingan di Bagian 3 dan 4 kehilangan pengendaliannya.

    Rancangannya membawa dua keputusan dari Sesi 3:

      * pooling ASIMETRIS. Sumbu waktu dipooling 2, sumbu frekuensi 2 di dua
        lapisan pertama lalu dibiarkan. Alasannya Soal 2b Sesi 3: pergeseran
        10 milidetik tidak berarti, pergeseran satu tapis mel berarti.
      * rerata global di sumbu waktu di ujungnya, bukan perataan. Akibatnya
        model menerima masukan sepanjang apa pun, dan itulah yang membuat
        Bagian 6 bisa memakai model yang sama untuk aliran kontinu.
    """
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
        nn.AdaptiveAvgPool2d((1, None)),        # rerata sepanjang WAKTU
        nn.Flatten(),
        nn.Linear(c3 * (n_masuk // 4), n_kelas),
    )


def ke_torch(X, y, b, belah, peranti, mfcc=None):
    """Ubah potongan belahan jadi tensor di peranti. Disediakan.

    mfcc : kalau bukan None, log-mel diubah jadi MFCC sebanyak itu lebih
           dulu. Dipakai Bagian 3 untuk menguji hipotesis Soal 6b Sesi 2.
    """
    import torch
    pilih = b == belah
    Xs = X[pilih].astype(np.float32)
    if mfcc:
        Xs = Xs @ matriks_dct(mfcc, Xs.shape[-1]).T.astype(np.float32)
    return (torch.from_numpy(Xs).unsqueeze(1).to(peranti),
            torch.from_numpy(y[pilih]).to(peranti))


def latih_torch(model, Xl, yl, Xv, yv, epoch=12, batch=128, lr=3e-3, seed=0,
                diam=False):
    """Latih dengan AdamW dan jadwal kosinus. Kembalikan (akurasi valid, detik).

    Disediakan. Yang perlu kamu perhatikan cuma dua hal: seed dipatok supaya
    perbandingan antarbaris di Bagian 3 dan 4 sahih, dan model dikembalikan
    ke keadaan validasi TERBAIK, bukan keadaan epoch terakhir.
    """
    import torch
    import torch.nn as nn

    torch.manual_seed(seed)
    opt = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-4)
    jadwal = torch.optim.lr_scheduler.CosineAnnealingLR(opt, epoch)
    rugi_fn = nn.CrossEntropyLoss()
    terbaik, bobot_terbaik = 0.0, None
    mulai = time.perf_counter()

    for e in range(epoch):
        model.train()
        urut = torch.randperm(len(Xl), device=Xl.device)
        for i in range(0, len(urut) - batch + 1, batch):
            ambil = urut[i:i + batch]
            opt.zero_grad(set_to_none=True)
            rugi_fn(model(Xl[ambil]), yl[ambil]).backward()
            opt.step()
        jadwal.step()
        a = akurasi_torch(model, Xv, yv)
        if a > terbaik:
            terbaik = a
            bobot_terbaik = {k: v.clone() for k, v in model.state_dict().items()}
        if diam:
            bilah(e + 1, epoch, f"latih (valid {a * 100:.1f}%)", mulai=mulai)
        else:
            print(f"    epoch {e + 1:2d}  akurasi validasi {a * 100:5.2f}%")

    model.load_state_dict(bobot_terbaik)
    return terbaik, time.perf_counter() - mulai


def akurasi_torch(model, X, y, batch=1024):
    """Akurasi, tanpa gradien. Disediakan."""
    import torch
    model.eval()
    benar = 0
    with torch.no_grad():
        for i in range(0, len(X), batch):
            benar += (model(X[i:i + batch]).argmax(1) == y[i:i + batch]).sum().item()
    return benar / len(X)


def bagian3(X, y, b):
    print("\n" + GARIS, "\nBAGIAN 3  model dasar, dan hipotesis Sesi 2 diuji\n",
          GARIS, sep="")

    import torch
    peranti = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"  peranti : {peranti}"
          + (f"  ({torch.cuda.get_device_name(0)})" if peranti == "cuda" else ""))

    # Dasar mayoritas, sama seperti Bagian 1 Bulan 2 Sesi 3. Tidak ada model
    # yang boleh dianggap belajar sebelum melewati garis ini.
    uji = y[b == "uji"]
    dasar = np.bincount(uji, minlength=len(KELAS)).max() / len(uji)
    print(f"  dasar mayoritas uji : {dasar * 100:.2f}%")
    print(f"  ucapan uji          : {ribuan(len(uji))}")
    lebar = 2 * 1.96 * np.sqrt(0.9 * 0.1 / len(uji)) * 100
    print(f"  lebar selang 95%    : {lebar:.2f} poin  "
          f"(pada akurasi sekitar 90 persen)\n")

    hasil = []
    for nama, mfcc in (("log-mel 40", None), ("MFCC 13", N_MFCC),
                       ("MFCC 40", N_MEL)):
        Xl, yl = ke_torch(X, y, b, "latih", peranti, mfcc)
        Xv, yv = ke_torch(X, y, b, "valid", peranti, mfcc)
        Xu, yu = ke_torch(X, y, b, "uji", peranti, mfcc)
        model = bikin_model(len(KELAS), Xl.shape[-1]).to(peranti)
        n_par = sum(p.numel() for p in model.parameters())
        print(f"  {nama}  ({ribuan(n_par)} parameter)")
        _, detik = latih_torch(model, Xl, yl, Xv, yv, diam=True)
        a_uji = akurasi_torch(model, Xu, yu)
        hasil.append((nama, n_par, detik, a_uji))
        print(f"    akurasi uji {a_uji * 100:.2f}%   {detik:.0f} detik")
        if nama == "log-mel 40":
            simpan = (model, Xu, yu)

    print(f"\n  {'fitur':<14}{'dimensi':>9}{'parameter':>12}{'detik':>8}"
          f"{'akurasi uji':>14}")
    print("  " + "-" * 57)
    for (nama, n_par, detik, a) in hasil:
        dim = {"log-mel 40": 40, "MFCC 13": 13, "MFCC 40": 40}[nama]
        print(f"  {nama:<14}{dim:>9}{ribuan(n_par):>12}{detik:>8.0f}"
              f"{a * 100:>13.2f}%")

    a_mel = hasil[0][3] * 100
    a_m13 = hasil[1][3] * 100
    a_m40 = hasil[2][3] * 100
    menang = "log-mel" if a_mel > a_m40 else "MFCC 40"
    terukur = abs(a_mel - a_m40) > lebar

    print(f"""
  Hipotesis dari Soal 6b Sesi 2 berbunyi: untuk CNN, log-mel mengalahkan
  MFCC, dan selisihnya melampaui selang {koma(lebar, 1)} poin.

  Terukur: log-mel {koma(a_mel, 2)} persen, MFCC 13 {koma(a_m13, 2)} persen,
  MFCC 40 {koma(a_m40, 2)} persen.

  Baris MFCC 40 adalah pengendaliannya, dan ia yang memisahkan dua penjelasan
  yang berbeda. Kalau log-mel menang atas MFCC 13 tetapi kalah atau seri
  terhadap MFCC 40, maka yang berperan JUMLAH DIMENSI, bukan struktur
  lokalnya. Kalau log-mel menang atas keduanya, barulah klaim tentang
  struktur lokal punya dukungan.

  Yang menang di antara keduanya: {menang}. Selisihnya
  {koma(abs(a_mel - a_m40), 2)} poin, dan itu {'MELAMPAUI' if terukur else 'DI DALAM'}
  selang kepercayaan, jadi hipotesisnya {'didukung' if terukur and menang == 'log-mel' else 'belum terbukti dari pengukuran ini'}.

  Perhatikan bahwa jawaban ini bisa saja tidak seperti yang saya harapkan
  waktu menulis Sesi 2, dan itu memang gunanya menuliskan ramalan lebih dulu.
  Soal 3 memintamu menuliskan kesimpulan yang keluar dari angka di atas, apa
  pun angkanya.""")

    return simpan, peranti


# ══════════════════════════════════════════════════════════════
# BAGIAN 4 - augmentasi
# ══════════════════════════════════════════════════════════════

def geser_bingkai(X, rng, maks=10):
    """Geser spektrogram di sumbu waktu, dalam satuan bingkai. Disediakan.

    Satu bingkai 10 milidetik, jadi maks=10 berarti sampai 100 milidetik.
    Dikerjakan di ranah bingkai karena sinyal waktunya sudah tidak ada di
    dalam cache. Bagian 2 sudah menyebutkan batas ini; di sini ia digigit.
    """
    hasil = np.empty_like(X)
    for i in range(len(X)):
        d = int(rng.integers(-maks, maks + 1))
        hasil[i] = np.roll(X[i], d, axis=0)
        if d > 0:
            hasil[i, :d] = X[i, 0]
        elif d < 0:
            hasil[i, d:] = X[i, -1]
    return hasil


def bagian4(X, y, b, baris, derau, peranti):
    print("\n" + GARIS, "\nBAGIAN 4  augmentasi, dua-duanya diukur\n", GARIS,
          sep="")

    import torch

    Xv, yv = ke_torch(X, y, b, "valid", peranti)
    Xu, yu = ke_torch(X, y, b, "uji", peranti)
    pilih = b == "latih"
    Xl_np, yl_np = X[pilih].astype(np.float32), y[pilih]
    rng = np.random.default_rng(0)

    # Dua himpunan uji, bukan satu. Yang pertama himpunan uji resmi, yang
    # ucapannya sejajar seperti data latih. Yang kedua himpunan yang sama
    # tetapi SENGAJA digeser sampai 250 milidetik, menirukan pemakaian nyata
    # tempat katanya tidak pernah mendarat tepat di tengah.
    Xu_geser = torch.from_numpy(
        geser_bingkai(X[b == "uji"].astype(np.float32),
                      np.random.default_rng(1), maks=25)
    ).unsqueeze(1).to(peranti)

    print(f"  {'model':<26}{'uji sejajar':>14}{'uji digeser':>14}{'jatuh':>9}")
    print("  " + "-" * 63)
    ulang = []
    for nama, augmen in (("tanpa augmentasi", False),
                         ("geseran waktu +-100 ms", True)):
        Xa = geser_bingkai(Xl_np, rng) if augmen else Xl_np
        Xl = torch.from_numpy(Xa).unsqueeze(1).to(peranti)
        yl = torch.from_numpy(yl_np).to(peranti)
        model = bikin_model(len(KELAS)).to(peranti)
        latih_torch(model, Xl, yl, Xv, yv, diam=True)
        a1 = akurasi_torch(model, Xu, yu)
        a2 = akurasi_torch(model, Xu_geser, yu)
        ulang.append((nama, a1, a2))
        print(f"  {nama:<26}{a1 * 100:>13.2f}%{a2 * 100:>13.2f}%"
              f"{(a1 - a2) * 100:>8.2f}", flush=True)

    jatuh_tanpa = (ulang[0][1] - ulang[0][2]) * 100
    jatuh_dengan = (ulang[1][1] - ulang[1][2]) * 100

    print(f"""
  Kolom `jatuh` adalah seluruh isi bagian ini, dan kolom akurasi uji sejajar
  sengaja disisakan di sebelahnya untuk dibandingkan.

  Model tanpa augmentasi jatuh {koma(jatuh_tanpa, 2)} poin ketika ucapan
  ujinya digeser sampai 250 milidetik. Model dengan augmentasi jatuh
  {koma(jatuh_dengan, 2)} poin.

  Inilah ramalan Bagian 6 Sesi 3 yang diuji: rasio {koma(0.406, 3)} di sumbu
  waktu memang menandakan bahwa posisi membawa informasi di dalam dataset
  ini, dan model yang dilatih apa adanya memungutnya sebagai ciri. Ciri itu
  tidak ada di pemakaian nyata, tempat SYNESIS mendengarkan terus-menerus dan
  kata bisa mendarat di mana saja.

  Yang perlu dicatat dengan hati-hati: kalau kamu hanya membaca kolom akurasi
  uji sejajar, augmentasi terlihat tidak berguna atau bahkan merugikan.
  Himpunan uji resminya berbagi cacat yang sama dengan data latihnya, jadi ia
  buta terhadap masalah yang justru paling penting. Ini contoh nyata bahwa
  himpunan uji yang benar secara prosedur bisa tetap salah secara isi.

  Derau latar tidak diaugmentasikan di sini, dan alasannya jujur: cache di
  Bagian 2 menyimpan log-mel, bukan sinyal, dan menambahkan derau di ranah
  log-mel bukan penjumlahan. Bagian 5 mengerjakannya di ranah waktu untuk
  data wake word yang jauh lebih kecil, dan Soal 4 memintamu menghitung
  ongkos mengerjakannya untuk seluruh data.""")

    return ulang


# ══════════════════════════════════════════════════════════════
# BAGIAN 5 - wake word
# ══════════════════════════════════════════════════════════════

def data_wake(baris, derau, kata_bangun="marvin", n_derau=1200):
    """Susun data dua kelas: bangun lawan bukan-bangun. Disediakan.

    Kalau `E:\\SYNESIS\\suara\\bangun\\*.wav` ada, rekaman suaramu sendiri
    yang dipakai sebagai kelas positif. Kalau belum ada, kata `marvin` dari
    Speech Commands dipakai sebagai penggantinya.

    Penggantinya bukan sekadar penambal. `marvin` memang dipakai sebagai
    wake word tiruan di banyak makalah, karena ia dua suku kata dan tidak
    mirip kata lain di dataset. Yang hilang dari penggantian itu satu hal
    yang penting, dan Soal 5 membahasnya: model yang dilatih dari 1.700
    pembicara TIDAK sama dengan model yang dilatih dari satu pembicara.
    """
    milikku = sorted((REKAMAN / "bangun").glob("*.wav")) if REKAMAN.is_dir() else []
    if milikku:
        positif = [(w, 1, belahan(w)) for w in milikku]
        sumber = "rekaman sendiri"
    else:
        positif = [(w, 1, b) for w, k, b in baris
                   if w.parent.name == kata_bangun]
        sumber = f"{kata_bangun} (pengganti)"

    negatif = [(w, 0, b) for w, k, b in baris if w.parent.name != kata_bangun]
    return positif, negatif, sumber


def roc(skor_positif, skor_negatif):
    """Kurva ROC dari dua kumpulan skor. Kembalikan (ambang, FAR, FRR, AUC).

    FAR (false accept rate)  : porsi negatif yang lolos ambang.
    FRR (false reject rate)  : porsi positif yang tertolak ambang.

    Dihitung dengan mengurutkan seluruh skor sekaligus, bukan dengan menyapu
    ambang berjarak tetap. Sapuan berjarak tetap melewatkan titik siku, dan
    titik siku itulah yang biasanya ingin kamu pakai.

    AUC dihitung dengan uji peringkat Mann-Whitney, yang identik dengan luas
    di bawah kurva ROC dan tidak memerlukan integrasi numerik sama sekali.

    Satu jebakan yang wajib ditutup: peringkat SERI. `argsort().argsort()`
    memberi peringkat berbeda kepada nilai yang sama persis, dan urutannya
    ditentukan kebetulan. Akibatnya dua kumpulan skor yang identik memberi
    AUC 0,25, bukan 0,5. Ini bukan kasus buatan: model yang yakin menghasilkan
    banyak skor yang jenuh tepat di 0,0 dan 1,0. `rankdata` memberi peringkat
    rerata untuk nilai yang seri, dan itu definisi yang benar.

    TODO 2
    """
    from scipy.stats import rankdata

    p = np.sort(np.asarray(skor_positif))
    n = np.sort(np.asarray(skor_negatif))
    ambang = np.unique(np.concatenate([p, n]))
    far = np.array([(n >= t).mean() for t in ambang])
    frr = np.array([(p < t).mean() for t in ambang])

    peringkat = rankdata(np.concatenate([p, n]))
    auc = ((peringkat[:len(p)].sum() - len(p) * (len(p) + 1) / 2)
           / (len(p) * len(n)))
    return ambang, far, frr, auc


def bagian5(baris, derau, peranti):
    print("\n" + GARIS, "\nBAGIAN 5  wake word, dan ambang yang dikalibrasi\n",
          GARIS, sep="")

    import torch

    positif, negatif, sumber = data_wake(baris, derau)
    rng = np.random.default_rng(0)
    # Negatif disubsampel supaya latihannya tidak didominasi satu kelas
    # sampai model belajar menjawab "bukan" untuk apa pun.
    ambil = rng.choice(len(negatif), size=min(len(negatif), 20 * len(positif)),
                       replace=False)
    negatif = [negatif[i] for i in ambil]

    print(f"  sumber kelas positif : {sumber}")
    print(f"  positif              : {len(positif)}")
    print(f"  negatif              : {len(negatif)}\n")

    def muat(daftar, augmen=False):
        Xs, ys = [], []
        for w, kelas, _ in daftar:
            x = satu_detik(baca_wav(w)[0], rng, geser=int(0.1 * LAJU) if augmen else 0)
            if augmen and derau and rng.random() < 0.5:
                d = derau[int(rng.integers(len(derau)))]
                a = int(rng.integers(0, len(d) - LAJU))
                x = x + d[a:a + LAJU] * float(rng.uniform(0.02, 0.25))
            Xs.append(fitur_audio(x))
            ys.append(kelas)
        return np.stack(Xs).astype(np.float32), np.array(ys)

    bagi = {s: [r for r in positif + negatif if r[2] == s]
            for s in ("latih", "valid", "uji")}

    Xl, yl = muat(bagi["latih"], augmen=True)
    Xv, yv = muat(bagi["valid"])
    Xu, yu = muat(bagi["uji"])
    print(f"  latih {len(Xl)}  valid {len(Xv)}  uji {len(Xu)}\n")

    def ke_t(A, c):
        return (torch.from_numpy(A).unsqueeze(1).to(peranti),
                torch.from_numpy(c).to(peranti))

    Xlt, ylt = ke_t(Xl, yl)
    Xvt, yvt = ke_t(Xv, yv)
    Xut, yut = ke_t(Xu, yu)

    model = bikin_model(2).to(peranti)
    latih_torch(model, Xlt, ylt, Xvt, yvt, epoch=20, diam=True)
    print(f"  akurasi uji : {akurasi_torch(model, Xut, yut) * 100:.2f}%")

    model.eval()
    with torch.no_grad():
        skor = torch.softmax(model(Xut), 1)[:, 1].cpu().numpy()
    ambang, far, frr, auc = roc(skor[yu == 1], skor[yu == 0])

    print(f"  AUC         : {auc:.4f}\n")
    print(f"  {'ambang':>9}{'FAR (persen)':>15}{'FRR (persen)':>15}"
          f"{'salah/jam*':>13}")
    print("  " + "-" * 52)
    # *Salah per jam: satu jendela per 100 milidetik, jadi 36.000 keputusan
    #  per jam kalau lingkungannya selalu berisi ucapan bukan-bangun. Ini
    #  batas ATAS yang pesimistis; Bagian 6 mengukur angka yang lebih jujur.
    for t in (0.5, 0.9, 0.95, 0.99, 0.995, 0.999):
        i = int(np.searchsorted(ambang, t))
        i = min(i, len(ambang) - 1)
        print(f"  {t:>9.3f}{far[i] * 100:>15.3f}{frr[i] * 100:>15.2f}"
              f"{far[i] * 36000:>13.0f}")

    # Titik siku: ambang tempat FAR dan FRR bertemu (equal error rate).
    j = int(np.argmin(np.abs(far - frr)))
    eer = (far[j] + frr[j]) / 2

    # Ambang yang benar-benar dipakai TIDAK diambil dari titik itu. Ia dipilih
    # dengan meminimalkan ongkos, persis seperti lima belas ambang intent di
    # Bulan 2 Sesi 4: salah menerima dianggap seratus kali lebih mahal
    # daripada salah menolak.
    ongkos = 100.0 * far + 1.0 * frr
    pakai = float(ambang[int(np.argmin(ongkos))])

    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    ax[0].plot(far * 100, (1 - frr) * 100, lw=1.5)
    ax[0].set_xlabel("FAR (persen)")
    ax[0].set_ylabel("terdeteksi benar (persen)")
    ax[0].set_title(f"ROC, AUC = {auc:.4f}", fontsize=9)
    ax[0].grid(alpha=0.3)
    ax[1].semilogy(ambang, far * 100 + 1e-3, label="FAR")
    ax[1].semilogy(ambang, frr * 100 + 1e-3, label="FRR")
    ax[1].axvline(ambang[j], color="k", ls="--", lw=0.8)
    ax[1].set_xlabel("ambang")
    ax[1].set_ylabel("persen")
    ax[1].set_title(f"EER = {eer * 100:.2f}% di ambang {ambang[j]:.3f}",
                    fontsize=9)
    ax[1].legend()
    ax[1].grid(alpha=0.3)
    fig.tight_layout()
    berkas = FIGUR / "b3s4_roc.png"
    fig.savefig(berkas, dpi=110)
    plt.close(fig)

    print(f"""
  Gambar disimpan: {berkas.name}
  Titik kesalahan setara (EER) : {koma(eer * 100, 2)} persen di ambang
  {koma(ambang[j], 3)}.
  Ambang yang dipakai Bagian 6   : {koma(pakai, 3)}, dari ongkos 100 banding 1.

  EER adalah angka yang enak dilaporkan dan hampir selalu keliru dipakai
  untuk memilih ambang, karena ia menganggap kedua kesalahan sama mahal.
  Untuk wake word keduanya sama sekali tidak sama mahal, dan kamu sudah punya
  kerangka untuk menyatakan alasannya: Bagian 3 Bulan 2 Sesi 4 menurunkan
  lima belas ambang intent dari ongkos salah, bukan dari akurasi.

  Kerangka yang sama, dipakai di sini:

    salah menolak  kamu mengulang "hey synesis" sekali. Ongkosnya satu
                   detik dan sedikit jengkel.
    salah menerima SYNESIS menyala di tengah percakapan, merekam, lalu
                   mengirim apa pun yang terdengar ke pipa niat. Ongkosnya
                   jauh lebih besar, dan sebagian di antaranya bukan
                   ongkos waktu.

  Dengan rasio ongkos 1 banding 100, ambang yang tepat adalah yang menahan
  FAR serendah mungkin sambil menjaga FRR tetap bisa ditoleransi, dan tabel
  di atas memberi angkanya. Soal 5 memintamu memilih satu, lalu menuliskan
  ongkos yang kamu asumsikan.

  Peringatan yang harus ikut, dan yang paling penting di seluruh bagian ini:
  angka FAR di atas diukur pada UCAPAN, yaitu satu detik audio yang memang
  berisi kata. Di pemakaian nyata, sebagian besar waktu tidak ada yang
  berbicara sama sekali, dan model ini tidak pernah melihat kesunyian ruangan
  kamarmu. Bagian 6 mengukur angka yang lebih dekat ke kenyataan.""")

    return model, pakai


# ══════════════════════════════════════════════════════════════
# BAGIAN 6 - deteksi mengalir
# ══════════════════════════════════════════════════════════════

def skor_mengalir(model, x, peranti, panjang=LAJU, loncat=LAJU // 10):
    """Jalankan model di sepanjang sinyal dengan jendela geser.

    Kembalikan (waktu_detik, skor). Satu skor tiap `loncat` cuplikan.

    Ini bentuk yang benar-benar dipakai SYNESIS: audio masuk terus-menerus,
    dan modelnya harus memberi keputusan berkala tanpa menunggu ucapan
    selesai.

    TODO 3
    """
    import torch
    potong = []
    for a in range(0, max(1, len(x) - panjang + 1), loncat):
        potong.append(fitur_audio(x[a:a + panjang]))
    if not potong:
        return np.zeros(0), np.zeros(0)
    Xb = torch.from_numpy(np.stack(potong).astype(np.float32))
    model.eval()
    with torch.no_grad():
        s = torch.softmax(model(Xb.unsqueeze(1).to(peranti)), 1)[:, 1]
    waktu = (np.arange(len(potong)) * loncat + panjang) / LAJU
    return waktu, s.cpu().numpy()


def haluskan(s, n=3):
    """Rerata bergerak n titik. Disediakan.

    Ini konvolusi 1D dengan kernel kotak, dan Sesi 1 sudah mengukur harganya:
    kernel kotak punya cuping samping -13 dB, jadi ia penghalus yang buruk
    secara spektral. Untuk penghalusan tiga titik atas skor keputusan, hal itu
    tidak menggigit. Soal 6 menanyakan kapan ia mulai menggigit.
    """
    if n <= 1 or len(s) < n:
        return s
    return np.convolve(s, np.ones(n) / n, mode="same")


def bagian6(model, ambang, baris, derau, peranti):
    print("\n" + GARIS, "\nBAGIAN 6  deteksi mengalir dan latensinya\n", GARIS,
          sep="")

    if not derau:
        print("  Derau latar tidak ada. Bagian ini dilewati.")
        return

    rng = np.random.default_rng(2)

    # Uji 1: berapa kali model menyala di derau latar murni, per jam.
    # Inilah angka yang menentukan apakah SYNESIS bisa dibiarkan menyala.
    total_detik = 0.0
    palsu = {t: 0 for t in (0.5, 0.9, 0.99, 0.999)}
    for d in derau:
        _, s = skor_mengalir(model, d, peranti)
        s = haluskan(s)
        total_detik += len(d) / LAJU
        for t in palsu:
            # Satu penyalaan dihitung sekali per lintasan naik, bukan sekali
            # per jendela. Tanpa itu, satu penyalaan sepanjang 1 detik
            # terhitung sepuluh kali.
            naik = np.diff((s >= t).astype(int)) == 1
            palsu[t] += int(naik.sum()) + int(s[0] >= t)

    print(f"  derau latar : {total_detik / 60:.1f} menit\n")
    print(f"  {'ambang':>9}{'penyalaan':>12}{'per jam':>11}")
    print("  " + "-" * 32)
    for t in sorted(palsu):
        print(f"  {t:>9.3f}{palsu[t]:>12}{palsu[t] / total_detik * 3600:>11.1f}")

    # Uji 2: latensi. Satu ucapan positif ditanam di posisi yang diketahui
    # di dalam derau, lalu diukur kapan skornya melewati ambang.
    kata_positif = [w for w, k, b in baris
                    if w.parent.name == "marvin" and b == "uji"][:40]
    if not kata_positif:
        print("\n  Tidak ada ucapan uji untuk mengukur latensi.")
        return

    def akhir_kata(u):
        """Detik ke berapa di dalam potongan satu detik itu katanya berhenti.

        Speech Commands memberi kliping satu detik dengan katanya di tengah,
        jadi kata yang sesungguhnya cuma menempati sekitar separuhnya.
        Mengukur latensi terhadap detik ke-3 berarti mengukur terhadap
        kesunyian di ekor kliping, dan itu menghasilkan angka negatif yang
        kelihatan mustahil. Yang benar: akhir tenaganya.
        """
        pot = u.reshape(-1, LONCAT)
        db = 10 * np.log10((pot ** 2).mean(axis=1) + 1e-12)
        aktif = np.where(db > db.max() - 25)[0]
        return (aktif[-1] + 1) * LONCAT / LAJU if len(aktif) else 1.0

    tunda = []
    for w in kata_positif:
        u = satu_detik(baca_wav(w)[0])
        d = derau[int(rng.integers(len(derau)))]
        a = int(rng.integers(0, len(d) - 5 * LAJU))
        lorong = d[a:a + 5 * LAJU] * 0.05
        mulai_kata = 2 * LAJU
        lorong[mulai_kata:mulai_kata + LAJU] += u
        t, s = skor_mengalir(model, lorong, peranti)
        s = haluskan(s)
        lewat = np.where(s >= ambang)[0]
        if len(lewat):
            tunda.append(t[lewat[0]] - (2.0 + akhir_kata(u)))

    if tunda:
        tunda = np.array(tunda)
        print(f"\n  ucapan ditanam di detik 2,0, {len(kata_positif)} percobaan")
        print("  latensi dihitung dari AKHIR TENAGA katanya, bukan dari akhir\n"
              "  potongan satu detiknya")
        print(f"  terdeteksi                : {len(tunda)} dari "
              f"{len(kata_positif)}")
        print(f"  latensi median            : {np.median(tunda) * 1000:+.0f} ms")
        print(f"  latensi persentil ke-90   : "
              f"{np.percentile(tunda, 90) * 1000:+.0f} ms")

    # Ongkos hitung: berapa lama satu jendela diproses, dan berapa porsi
    # anggaran waktu nyata yang dipakainya.
    x = np.zeros(LAJU)
    t0 = time.perf_counter()
    for _ in range(20):
        skor_mengalir(model, x, peranti, loncat=LAJU)
    per_jendela = (time.perf_counter() - t0) / 20 * 1000

    print(f"\n  waktu satu jendela        : {per_jendela:.1f} ms")
    print(f"  jendela per detik         : 10")
    print(f"  beban prosesor            : {per_jendela * 10 / 1000 * 100:.1f}%")

    print(f"""
  Tabel pertama adalah angka yang menentukan apakah SYNESIS layak dibiarkan
  menyala seharian, dan ia jauh lebih jujur daripada FAR di Bagian 5.
  Bedanya: FAR di Bagian 5 dihitung atas ucapan yang memang berisi kata,
  sedangkan tabel ini dihitung atas derau ruangan tanpa satu pun kata. Yang
  kedua persis keadaan SYNESIS selama 99 persen waktunya.

  Latensi diukur relatif terhadap akhir TENAGA katanya, dan titik acuan itu
  perlu disebut karena versi pertama bagian ini salah memilihnya. Semula ia
  diukur terhadap detik ke-3, yaitu ujung potongan satu detiknya, dan
  hasilnya minus 300 milidetik: model seolah-olah mendeteksi sebelum katanya
  selesai. Yang sebenarnya terjadi, kata di dalam kliping Speech Commands
  cuma menempati sekitar separuh potongan, jadi 300 milidetik terakhirnya
  memang kesunyian.

  Angka negatif tetap mungkin dan tetap masuk akal: jendela satu detik yang
  sudah memuat sebagian besar kata sudah cukup untuk melewati ambang, dan
  model tidak wajib menunggu suku kata terakhir. Yang tidak mungkin adalah
  mendeteksi sebelum katanya mulai.

  Dua sumbangan tetap yang tidak bisa dihapus: jendela satu detik harus
  terisi dulu, dan penghalusan tiga titik menambahkan 100 milidetik lagi.
  Keduanya keputusan yang bisa ditukar, dan Soal 6 memintamu menghitung
  pertukarannya.

  Beban prosesor adalah angka terakhir yang menentukan. Kalau ia di bawah
  lima persen, SYNESIS bisa mendengarkan terus-menerus tanpa terasa. Kalau
  di atas dua puluh persen, kipas laptopmu akan menyala sepanjang hari dan
  kamu akan mematikan fiturnya dalam seminggu.

  Sesi 5 memasang seluruh ini ke `synesis/suara.py`, menambahkan VAD supaya
  model tidak dijalankan waktu ruangan sunyi, lalu menyambungkannya ke pipa
  niat Bulan 2.""")


# ══════════════════════════════════════════════════════════════
# Jalankan semuanya
# ══════════════════════════════════════════════════════════════

def main():
    mulai = time.perf_counter()

    baris = bagian1()
    derau = derau_latar()
    X, y, b = bagian2(baris, derau)
    (model12, Xu, yu), peranti = bagian3(X, y, b)
    bagian4(X, y, b, baris, derau, peranti)
    model, ambang = bagian5(baris, derau, peranti)
    bagian6(model, ambang, baris, derau, peranti)

    print(f"\n{GARIS}")
    print(f"  selesai dalam {time.perf_counter() - mulai:.0f} detik")
    print(GARIS)


if __name__ == "__main__":
    main()
