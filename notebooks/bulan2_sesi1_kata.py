"""Bulan 2 Sesi 1 - Dari kata jadi angka, dari angka jadi keputusan.

Jalankan:
    . .\\scripts\\activate.ps1
    python notebooks\\bulan2_sesi1_kata.py

Bulan 1 kamu bikin mesin yang menurunkan apa saja. Sekarang mesin itu dipakai
untuk masalah yang bukan angka: kalimat.

Pertanyaan bulan ini satu. Komputer cuma bisa mengalikan angka. Kalimat bukan
angka. Jadi bagaimana caranya "buka laporan praktikum minggu lalu" berubah jadi
sesuatu yang bisa dikalikan?

Dan yang kamu tulis di sini bukan latihan yang dibuang. Ini otak perintah
rutin SYNESIS. Setelah jadi, "berapa sisa disk" tidak perlu lagi melewati
model 1,9 GB di VRAM. Ia dijawab dalam hitungan milidetik oleh bobot yang
muat di beberapa kilobyte.

Bagian bertanda TODO kamu yang isi.
"""

import re
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

GARIS = "=" * 62
FIGUR = Path(__file__).resolve().parent.parent / "figures"
FIGUR.mkdir(exist_ok=True)


# ══════════════════════════════════════════════════════════════
# Data. Perintah sungguhan, label sungguhan.
# ══════════════════════════════════════════════════════════════
#
# Ini benih. Tugas Sesi 2 nanti menambahkannya sampai 300 sampai 500 baris,
# semuanya perintah yang memang kamu ketik. Untuk sekarang 36 sudah cukup
# untuk melihat seluruh mesinnya bekerja.

DATA = [
    # buka_file
    ("buka laporan praktikum minggu lalu", "buka_file"),
    ("bukain modul fisika komputasi", "buka_file"),
    ("tolong buka file log terakhir", "buka_file"),
    ("buka dokumen skripsi", "buka_file"),
    ("bukakan catatan kuliah kemarin", "buka_file"),
    ("buka pdf yang tadi", "buka_file"),

    # cari_file
    ("cari file python di folder notebooks", "cari_file"),
    ("ada file apa aja di folder video", "cari_file"),
    ("cariin dokumen yang namanya sesiA", "cari_file"),
    ("file apa yang berubah kemarin", "cari_file"),
    ("cari semua gambar png", "cari_file"),
    ("liat isi folder scripts", "cari_file"),

    # info_sistem
    ("berapa sisa disk", "info_sistem"),
    ("cek ram yang kepake", "info_sistem"),
    ("vram nya masih sisa berapa", "info_sistem"),
    ("gimana kondisi laptop sekarang", "info_sistem"),
    ("suhu prosesor berapa", "info_sistem"),
    ("cek penggunaan cpu", "info_sistem"),

    # baca_log
    ("baca log error hari ini", "baca_log"),
    ("ada error apa tadi", "baca_log"),
    ("tunjukin log terakhir", "baca_log"),
    ("cek catatan kerja kemarin", "baca_log"),
    ("apa yang gagal di run terakhir", "baca_log"),
    ("liat riwayat error minggu ini", "baca_log"),

    # jalankan
    ("jalankan script sesiA", "jalankan"),
    ("run notebook bulan 1", "jalankan"),
    ("eksekusi verify.py", "jalankan"),
    ("coba jalanin tesnya", "jalankan"),
    ("render video bab 1", "jalankan"),
    ("jalankan git status", "jalankan"),

    # tanya_umum  -> yang ini dilempar ke LLM
    ("jelaskan apa itu gradient descent", "tanya_umum"),
    ("kenapa langit warnanya biru", "tanya_umum"),
    ("bantu aku mikir soal termodinamika", "tanya_umum"),
    ("menurutmu mana yang lebih baik", "tanya_umum"),
    ("ceritakan sesuatu yang menarik", "tanya_umum"),
    ("apa bedanya momentum sama adam", "tanya_umum"),
]

LABEL = sorted({lab for _, lab in DATA})


def belah(teks):
    """Pecah kalimat jadi kata. Huruf kecil semua, tanda baca dibuang.

    Sengaja sesederhana ini. Kamu akan melihat sendiri di Soal 3 kenapa
    kesederhanaan ini punya harga.
    """
    return re.findall(r"[a-z0-9]+", teks.lower())


# ══════════════════════════════════════════════════════════════
# BAGIAN 1 - kalimat jadi vektor
# ══════════════════════════════════════════════════════════════

def bangun_kosakata(kalimat):
    """Kumpulkan semua kata unik, beri nomor urut.

    Kembalikan dict {kata: indeks}, diurutkan alfabet supaya hasilnya sama
    tiap kali dijalankan. Urutan yang tidak tetap membuat bug jadi mustahil
    dilacak.

    TODO 1a
    """
    raise NotImplementedError("bangun_kosakata")


def ke_vektor(teks, kosakata):
    """Ubah satu kalimat jadi vektor sepanjang kosakata.

    Elemen ke-i berisi berapa kali kata ke-i muncul di kalimat ini. Kata yang
    tidak ada di kosakata diabaikan.

    Inilah bag-of-words. Namanya jujur: ini benar-benar cuma karung berisi
    kata. Urutannya hilang. "anjing menggigit orang" dan "orang menggigit
    anjing" menghasilkan vektor yang identik.

    Itu terdengar seperti cacat fatal. Soal 2 menanyakan kenapa ternyata
    tidak, untuk masalah yang sedang kamu kerjakan.

    TODO 1b
    """
    raise NotImplementedError("ke_vektor")


def bagian1():
    print(GARIS, "\nBAGIAN 1  kalimat jadi vektor\n", GARIS, sep="")

    kal = [t for t, _ in DATA]
    kos = bangun_kosakata(kal)
    print(f"  kalimat        : {len(kal)}")
    print(f"  kata unik      : {len(kos)}")

    contoh = "berapa sisa disk"
    v = ke_vektor(contoh, kos)
    hidup = [(k, int(v[i])) for k, i in kos.items() if v[i] > 0]
    print(f"\n  '{contoh}'")
    print(f"  panjang vektor : {len(v)}")
    print(f"  yang tidak nol : {hidup}")
    print(f"  persen nol     : {100 * (v == 0).mean():.1f} persen")

    print("""
  Perhatikan baris terakhir. Hampir seluruh vektornya nol.

  Itu bukan pemborosan yang bisa dihindari, itu sifat bawaan bahasa. Satu
  kalimat cuma memakai segelintir kata dari seluruh kosakata. Vektor seperti
  ini disebut jarang, dan seluruh bidang temu-kembali informasi dibangun di
  atas kenyataan itu.""")
    return kos


# ══════════════════════════════════════════════════════════════
# BAGIAN 2 - kemiripan adalah hasil kali dalam
# ══════════════════════════════════════════════════════════════

def kemiripan(a, b):
    """Kemiripan kosinus antara dua vektor.

        mirip(a, b) = (a . b) / (|a| |b|)

    Kalau salah satu vektornya nol, kembalikan 0.0 dan jangan membagi nol.

    Kamu sudah pernah menulis operasi ini, dengan nama lain. Di Fisika Kuantum
    ia ditulis <psi|phi>. Di Sesi C Bulan 0 ia muncul sebagai X.T @ X. Di sini
    ia mengukur seberapa mirip dua perintah.

    Rumusnya sama. Yang berbeda cuma apa yang diwakili sumbunya.

    TODO 2
    """
    raise NotImplementedError("kemiripan")


def bagian2(kos):
    print("\n" + GARIS, "\nBAGIAN 2  kemiripan itu hasil kali dalam\n",
          GARIS, sep="")

    uji = [
        ("berapa sisa disk", "vram nya masih sisa berapa"),
        ("buka laporan praktikum minggu lalu", "buka dokumen skripsi"),
        ("cari file python di folder notebooks", "cari semua gambar png"),
        ("berapa sisa disk", "buka dokumen skripsi"),
        ("jalankan script sesiA", "run notebook bulan 1"),
    ]

    print(f"  {'kalimat A':<38}{'kalimat B':<38}{'mirip':>7}")
    print("  " + "-" * 84)
    for a, b in uji:
        m = kemiripan(ke_vektor(a, kos), ke_vektor(b, kos))
        print(f"  {a:<38}{b:<38}{m:7.3f}")

    print("""
  Tiga baris pertama masuk akal. Yang berbagi kata dapat skor tinggi, dan
  makin banyak kata yang sama makin tinggi skornya. Baris keempat nol, dan
  itu juga benar: dua perintah itu memang tidak ada hubungannya.

  Sekarang lihat baris kelima. 'jalankan script sesiA' dan 'run notebook
  bulan 1' maksudnya sama persis, dan skornya nol. Tidak ada satu pun kata
  yang sama.

  Di situlah bag-of-words buta. Ia tidak tahu 'jalankan' dan 'run' itu satu
  arti, dan tidak tahu 'buka' dan 'bukain' itu kata yang sama. Ia cuma
  mencocokkan huruf.

  Soal 3 menanyakan apa yang akan kamu lakukan soal ini. Jawabannya bukan
  menyerah, dan ada tiga jalan dengan ongkos yang sangat berbeda.""")


# ══════════════════════════════════════════════════════════════
# BAGIAN 3 - regresi logistik, dua kelas dulu
# ══════════════════════════════════════════════════════════════

def sigmoid(z):
    """Peras bilangan apa pun ke rentang (0, 1).

        sigmoid(z) = 1 / (1 + exp(-z))

    Satu jebakan: exp(-z) meledak jadi inf kalau z sangat negatif, dan Python
    akan memberi peringatan overflow. Cegah dengan np.clip pada z sebelum
    dipangkatkan. Batas aman sekitar -60 sampai 60.

    Ini bukan kerapian, ini kebiasaan yang menyelamatkanmu nanti saat melatih
    di data sungguhan.

    TODO 3a
    """
    raise NotImplementedError("sigmoid")


def rugi_silang(p, y):
    """Entropi silang biner, dirata-ratakan.

        L = -(1/n) sum[ y log p + (1-y) log(1-p) ]

    Kenapa bukan MSE seperti Bulan 0? Soal 4 menanyakan itu, dan jawabannya
    bisa kamu turunkan sendiri.

    Jebakan kedua: log(0) itu -inf. Tambahkan epsilon kecil, misalnya 1e-12,
    ke dalam log.

    TODO 3b
    """
    raise NotImplementedError("rugi_silang")


def gradien_logistik(X, y, w, b):
    """Gradien rugi silang terhadap w dan b.

    Turunkan sendiri di kertas dulu. Petunjuknya: kamu sudah melihat hasil
    akhirnya di video Bulan 1 Bab 2, tertulis sebagai p - y. Sekarang buktikan
    dari mana bentuk sebersih itu datang.

    Yang harus dikembalikan:
        dL/dw  berbentuk sama dengan w
        dL/db  satu bilangan

    TODO 3c
    """
    raise NotImplementedError("gradien_logistik")


def bagian3(kos):
    print("\n" + GARIS, "\nBAGIAN 3  gradien tanganmu lawan beda hingga\n",
          GARIS, sep="")

    # masalah dua kelas: perintah sistem atau bukan
    X = np.array([ke_vektor(t, kos) for t, _ in DATA], dtype=float)
    y = np.array([1.0 if lab == "info_sistem" else 0.0 for _, lab in DATA])

    rng = np.random.default_rng(3)
    w = rng.normal(0, 0.3, X.shape[1])
    b = float(rng.normal(0, 0.3))

    dw, db = gradien_logistik(X, y, w, b)

    def rugi_di(w_, b_):
        return rugi_silang(sigmoid(X @ w_ + b_), y)

    h = 1e-5
    dw_num = np.zeros_like(w)
    for i in range(len(w)):
        maju, mundur = w.copy(), w.copy()
        maju[i] += h
        mundur[i] -= h
        dw_num[i] = (rugi_di(maju, b) - rugi_di(mundur, b)) / (2 * h)
    db_num = (rugi_di(w, b + h) - rugi_di(w, b - h)) / (2 * h)

    galat_w = np.abs(dw - dw_num).max() / max(1e-12, np.abs(dw_num).max())
    galat_b = abs(db - db_num) / max(1e-12, abs(db_num))

    print(f"  galat relatif dL/dw : {galat_w:.3e}")
    print(f"  galat relatif dL/db : {galat_b:.3e}")
    print(f"  status              : "
          f"{'lolos' if max(galat_w, galat_b) < 1e-6 else 'GAGAL'}")

    print("""
  Aturan yang sama sejak Hari 1: gradien tidak dipercaya sebelum diadu dengan
  beda hingga. Kali ini fungsinya bukan polinom, jadi beda pusat tidak lagi
  eksak. Galat 1e-9 sampai 1e-7 itu wajar dan bukan tanda salah.""")

    return X, y


# ══════════════════════════════════════════════════════════════
# BAGIAN 4 - latih, dua kelas
# ══════════════════════════════════════════════════════════════

def latih_biner(X, y, lr=0.5, n_iter=3000):
    """Gelung yang sama dengan Sesi A Bulan 0. Sengaja tidak berubah.

    Disediakan, bukan TODO. Perhatikan isinya cuma empat baris yang sama:
    hitung rugi, hitung gradien, melangkah, ulangi.
    """
    w = np.zeros(X.shape[1])
    b = 0.0
    riwayat = []
    for i in range(n_iter):
        p = sigmoid(X @ w + b)
        riwayat.append(rugi_silang(p, y))
        dw, db = gradien_logistik(X, y, w, b)
        w -= lr * dw
        b -= lr * db
    return w, b, np.array(riwayat)


def bagian4(X, y, kos):
    print("\n" + GARIS, "\nBAGIAN 4  melatih pemisah dua kelas\n", GARIS, sep="")

    w, b, riwayat = latih_biner(X, y)
    p = sigmoid(X @ w + b)
    tebak = (p > 0.5).astype(float)
    akurasi = (tebak == y).mean()

    print(f"  rugi awal   : {riwayat[0]:.6f}")
    print(f"  rugi akhir  : {riwayat[-1]:.6f}")
    print(f"  akurasi     : {akurasi * 100:.1f} persen "
          f"({int((tebak == y).sum())} dari {len(y)})")

    balik = {i: k for k, i in kos.items()}
    urut = np.argsort(-w)
    print("\n  Lima kata yang paling menarik ke 'info_sistem':")
    for i in urut[:5]:
        print(f"    {balik[i]:<14} bobot {w[i]:+.4f}")
    print("  Lima kata yang paling menolak:")
    for i in urut[-5:]:
        print(f"    {balik[i]:<14} bobot {w[i]:+.4f}")

    print("""
  Berhenti sebentar di sini.

  Tidak ada satu pun aturan tentang kata mana yang berarti apa yang kamu tulis
  ke dalam program ini. Daftar di atas muncul sendiri dari menuruni bukit.

  Dan bobot itu bisa kamu baca. Kamu bisa membuka isinya, melihat kata mana
  yang dipakai mengambil keputusan, dan tidak setuju kalau perlu. Model 3
  miliar parameter tidak memberimu itu.""")

    plt.figure(figsize=(7, 4))
    plt.plot(riwayat, lw=2, color="#22C55E")
    plt.xlabel("iterasi"); plt.ylabel("entropi silang")
    plt.title("Rugi selama latihan")
    plt.grid(alpha=0.3)
    plt.savefig(FIGUR / "bulan2_sesi1_rugi.png", dpi=110, bbox_inches="tight")
    plt.close()
    print("\n  plot disimpan : figures/bulan2_sesi1_rugi.png")


# ══════════════════════════════════════════════════════════════
# BAGIAN 5 - enam kelas sekaligus, dan hubungannya dengan Boltzmann
# ══════════════════════════════════════════════════════════════

def softmax(Z):
    """Ubah tiap baris Z jadi peluang yang berjumlah satu.

        p_k = exp(z_k) / sum_j exp(z_j)

    Wajib mengurangi maksimum tiap baris sebelum exp. Tanpa itu, exp(1000)
    langsung inf dan seluruh baris jadi nan. Menguranginya tidak mengubah
    hasil sama sekali, karena faktor yang sama muncul di pembilang dan
    penyebut lalu saling menghapus. Buktikan sendiri, satu baris aljabar.

    Kalau bentuk ini terasa akrab, memang. Ini distribusi Boltzmann dari
    Fisika Statistik, dengan z berperan sebagai minus energi dibagi kT.
    Parameter 'temperature' pada model bahasa dinamai dari situ, bukan
    kebetulan.

    TODO 5
    """
    raise NotImplementedError("softmax")


def bagian5(kos):
    print("\n" + GARIS, "\nBAGIAN 5  enam kelas, dan distribusi Boltzmann\n",
          GARIS, sep="")

    X = np.array([ke_vektor(t, kos) for t, _ in DATA], dtype=float)
    indeks = {lab: i for i, lab in enumerate(LABEL)}
    y = np.array([indeks[lab] for _, lab in DATA])
    T = np.zeros((len(y), len(LABEL)))
    T[np.arange(len(y)), y] = 1.0

    rng = np.random.default_rng(7)
    W = rng.normal(0, 0.1, (X.shape[1], len(LABEL)))
    bvec = np.zeros(len(LABEL))

    for _ in range(4000):
        P = softmax(X @ W + bvec)
        dZ = (P - T) / len(y)          # inilah p - y, sekarang untuk banyak kelas
        W -= 0.5 * (X.T @ dZ)
        bvec -= 0.5 * dZ.sum(0)

    P = softmax(X @ W + bvec)
    tebak = P.argmax(1)
    akurasi = (tebak == y).mean()
    print(f"  akurasi latih : {akurasi * 100:.1f} persen "
          f"({int((tebak == y).sum())} dari {len(y)})")

    print(f"\n  Matriks kebingungan, baris = sebenarnya, kolom = tebakan:\n")
    print("       " + "".join(f"{l[:8]:>10}" for l in LABEL))
    for i, lab in enumerate(LABEL):
        baris = [int(((y == i) & (tebak == j)).sum()) for j in range(len(LABEL))]
        print(f"  {lab[:10]:<10}" + "".join(f"{v:>10}" for v in baris))

    salah = [(DATA[i][0], LABEL[y[i]], LABEL[tebak[i]])
             for i in range(len(y)) if tebak[i] != y[i]]
    if salah:
        print("\n  Yang salah:")
        for kal, benar, keliru in salah:
            print(f"    '{kal}'\n      seharusnya {benar}, ditebak {keliru}")
    else:
        print("\n  Tidak ada yang salah di data latih. Soal 6 menjelaskan "
              "kenapa itu justru mencurigakan.")


# ══════════════════════════════════════════════════════════════
# BAGIAN 6 - ongkosnya, dan kenapa ini penting buat SYNESIS
# ══════════════════════════════════════════════════════════════

def bagian6(kos):
    print("\n" + GARIS, "\nBAGIAN 6  ongkos, dan kenapa ini penting\n",
          GARIS, sep="")

    n_kata = len(kos)
    n_kelas = len(LABEL)
    n_param = n_kata * n_kelas + n_kelas
    byte = n_param * 8

    print(f"  kosakata           : {n_kata}")
    print(f"  kelas              : {n_kelas}")
    print(f"  parameter          : {n_param}")
    print(f"  ukuran di memori   : {byte / 1024:.1f} KB")
    print(f"  VRAM yang dipakai  : 0")
    print()
    print(f"  Qwen2.5-3B Q4      : ~1.900.000 KB, dan butuh VRAM")
    print(f"  perbandingan       : {1_900_000 / (byte / 1024):,.0f} kali lebih besar"
          .replace(",", "."))

    print("""
  Angka terakhir itu alasan Bulan 2 ada di peta jalan SYNESIS.

  Tiap 'berapa sisa disk' yang lewat LLM harus memuat 1,9 GB ke VRAM,
  menghitung ratusan juta operasi, lalu mengarang kalimat. Pengklasifikasi
  di atas menjawab pertanyaan yang sama dengan satu perkalian matriks kecil,
  tanpa menyentuh GPU sama sekali.

  LLM tetap dipakai, tapi untuk yang memang butuh bahasa. Sisanya dikerjakan
  benda seberat beberapa kilobyte ini.

  Dan VRAM adalah sumber daya paling sempit di laptopmu.""")


if __name__ == "__main__":
    try:
        kos = bagian1()
        bagian2(kos)
        X, y = bagian3(kos)
        bagian4(X, y, kos)
        bagian5(kos)
        bagian6(kos)
    except NotImplementedError as e:
        print(f"\n  {e} belum diisi. Kerjakan TODO dulu.")
