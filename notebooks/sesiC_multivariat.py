"""Sesi C - multivariat, overfitting, regularisasi.

Jalankan:
    . .\\activate.ps1
    python notebooks\\sesiC_multivariat.py

Sampai sekarang modelmu punya dua kenop. Hari ini jadi banyak, dan seluruh
kode ditulis ulang dalam bentuk matriks supaya jumlah kenop berhenti jadi
urusan.

Lalu kamu akan melihat sendiri model menghafal derau, dan melihat satu suku
tambahan menyembuhkannya.

Fungsi yang sebenarnya membangkitkan data adalah kubik. Jadi derajat 3
adalah model yang benar, dan kamu punya pembanding jujur untuk menilai
derajat lainnya.

Bagian bertanda TODO kamu yang isi.
"""

from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

GARIS = "=" * 62
FIGUR = Path(__file__).resolve().parent.parent / "figures"
FIGUR.mkdir(exist_ok=True)

DERAU = 1.5


def f_asli(x):
    """Fungsi yang sebenarnya melahirkan data. Model tidak pernah melihat ini."""
    return 0.5 * x**3 - 2.0 * x + 1.0


def buat_data(n, seed):
    rng = np.random.default_rng(seed)
    x = np.sort(rng.uniform(-3, 3, n))
    return x, f_asli(x) + rng.normal(0, DERAU, n)


def bakukan(X, m=None, s=None):
    """Bakukan kolom 1 ke atas. Kolom 0 adalah kolom satuan, dibiarkan.

    Kalau m dan s diberikan, pakai itu. Ini penting: data uji WAJIB
    dibakukan memakai statistik data latih, bukan statistiknya sendiri.
    Memakai statistik data uji berarti model mengintip data uji, dan
    angka yang keluar jadi terlalu bagus untuk dipercaya.
    """
    Xb = X.copy().astype(float)
    if m is None:
        m = Xb[:, 1:].mean(axis=0)
        s = Xb[:, 1:].std(axis=0)
        s = np.where(s < 1e-12, 1.0, s)
    Xb[:, 1:] = (Xb[:, 1:] - m) / s
    return Xb, m, s


# ══════════════════════════════════════════════════════════════
# BAGIAN 1 - semuanya jadi matriks
# ══════════════════════════════════════════════════════════════

def desain_polinom(x, derajat):
    """Matriks desain untuk regresi polinomial.

    Baris ke-i berisi [1, x_i, x_i^2, ..., x_i^derajat].
    Bentuk keluaran (n, derajat + 1).

    Kolom pertama berisi angka satu semua. Itu bukan hiasan. Dengan kolom
    itu, geseran b berhenti jadi kasus khusus dan berubah jadi salah satu
    parameter biasa. Setelah ini tidak ada lagi w dan b terpisah, cuma
    satu vektor theta.

    TODO 1
    """
    raise NotImplementedError("desain_polinom")


def mse_matriks(X, y, theta):
    """MSE dalam bentuk matriks.

        residu = X @ theta - y
        MSE    = (1/n) * residu . residu

    Satu baris cukup. Perhatikan bahwa rumus ini tidak peduli berapa
    kolom X punya. Itu seluruh gunanya menulis ulang dalam bentuk matriks.

    TODO 2
    """
    raise NotImplementedError("mse_matriks")


def gradien_matriks(X, y, theta, lam=0.0):
    """Gradien MSE plus denda L2, dalam bentuk matriks.

        dL/dtheta = (2/n) * X^T @ (X @ theta - y) + 2 * lam * theta

    Turunkan sendiri di kertas dari bentuk skalar Sesi A, lalu cocokkan.
    Petunjuk: (2/n) * jumlah r_i * x_i adalah hasil kali dalam antara
    residu dan satu kolom X. Lakukan untuk semua kolom sekaligus, dan
    itulah X^T @ r.

    Satu jebakan yang harus kamu tangani sendiri. Kolom 0 adalah kolom
    satuan, dan parameter yang menyertainya adalah geseran. Geseran TIDAK
    boleh didenda. Mendendanya berarti memaksa garis lewat dekat titik
    asal, dan itu bukan yang kamu mau. Jadi jangan tambahkan suku denda
    pada theta[0].

    TODO 3
    """
    raise NotImplementedError("gradien_matriks")


def latih_matriks(X, y, theta, lr, n_iter, lam=0.0):
    """Gradient descent versi matriks. Kembalikan (theta, riwayat_loss).

    Isinya sama persis dengan latih() di Sesi A. Yang berubah cuma
    theta jadi vektor, bukan dua angka terpisah.

    Hentikan lebih awal kalau theta sudah tidak berhingga.

    TODO 4
    """
    raise NotImplementedError("latih_matriks")


def ridge_tertutup(X, y, lam):
    """Solusi tertutup regresi ridge. Disediakan, bukan TODO.

        theta = (X^T X / n + lam * R)^(-1) (X^T y / n)

    dengan R matriks identitas yang elemen [0,0]-nya dinolkan, supaya
    geseran tidak ikut didenda.

    Ini dipakai di Bagian 5 dan 6, karena di derajat tinggi gradient
    descent butuh iterasi sebanyak bilangan kondisi, dan Bagian 3 akan
    menunjukkan angka itu menembus 1e20.
    """
    n, d = X.shape
    R = np.eye(d)
    R[0, 0] = 0.0
    return np.linalg.solve(X.T @ X / n + lam * R, X.T @ y / n)


# ══════════════════════════════════════════════════════════════
# BAGIAN 2 - verifikasi silang dengan Sesi A
# ══════════════════════════════════════════════════════════════

def bagian2():
    print(GARIS, "\nBAGIAN 2  apakah bentuk matriks setuju dengan Sesi A\n",
          GARIS, sep="")

    from hari03_data_loss import buat_data as data_hari3
    from sesiA_gradient_descent import beda_hingga, gradien

    x, y = data_hari3()
    X = desain_polinom(x, 1)

    print("  Derajat 1 harus identik dengan model dua kenop Sesi A.")
    print(f"  {'w':>6} {'b':>6}   {'sumber':>16}   {'dL/dw':>12} {'dL/db':>12}")
    print("  " + "-" * 62)

    for w, b in [(0.0, 0.0), (3.0, 2.0), (5.0, -1.0)]:
        theta = np.array([b, w])            # kolom 0 = satuan, kolom 1 = x
        g_mat = gradien_matriks(X, y, theta)
        g_ses = gradien(x, y, w, b)
        g_num = beda_hingga(x, y, w, b)
        print(f"  {w:6.2f} {b:6.2f}   {'matriks':>16}   {g_mat[1]:12.6f} {g_mat[0]:12.6f}")
        print(f"  {'':6} {'':6}   {'skalar Sesi A':>16}   {g_ses[0]:12.6f} {g_ses[1]:12.6f}")
        print(f"  {'':6} {'':6}   {'beda hingga':>16}   {g_num[0]:12.6f} {g_num[1]:12.6f}")
        selisih = max(abs(g_mat[1] - g_ses[0]), abs(g_mat[0] - g_ses[1]))
        print(f"  {'':6} {'':6}   {'selisih maks':>16}   {selisih:12.3e}")
        print()

    print("""  Tiga jalan yang berbeda mendarat di angka yang sama. Yang pertama
  memakai perkalian matriks, yang kedua memakai rumus skalar tulisanmu di
  Sesi A, yang ketiga tidak memakai kalkulus sama sekali.

  Kesepakatan tiga arah ini lebih kuat daripada kesepakatan dua arah, dan
  ini pola yang akan kamu pakai terus. Verifikasi butuh saksi yang tidak
  saling menyalin.""")


# ══════════════════════════════════════════════════════════════
# BAGIAN 3 - kenapa derajat tinggi menghancurkan gradient descent
# ══════════════════════════════════════════════════════════════

def bagian3(x, y):
    print("\n" + GARIS, "\nBAGIAN 3  bilangan kondisi meledak\n", GARIS, sep="")

    print(f"  {'derajat':>8} {'cond mentah':>14} {'cond baku':>12} "
          f"{'lambda_min mentah':>19} {'lr maks baku':>14}")
    print("  " + "-" * 76)

    for d in [1, 3, 5, 9, 14]:
        X = desain_polinom(x, d).astype(float)
        H = (2 / len(y)) * X.T @ X
        lam_min = np.linalg.eigvalsh(H)[0]

        Xb, _, _ = bakukan(X)
        Hb = (2 / len(y)) * Xb.T @ Xb
        lamb_maks = np.linalg.eigvalsh(Hb)[-1]

        print(f"  {d:8d} {np.linalg.cond(H):14.3e} {np.linalg.cond(Hb):12.3e} "
              f"{lam_min:19.3e} {2 / lamb_maks:14.3e}")

    print("""
  Ini Hessian yang sama dengan Sesi B, cuma sekarang berukuran lebih besar
  dari 2 kali 2. Bilangan kondisinya masih rasio nilai eigen terbesar
  terhadap terkecil, dan artinya masih sama: seberapa lonjong paritnya.

  Di Sesi B angkanya 8 dan lintasannya sudah menggergaji parah. Sekarang
  lihat kolom pertama di derajat 14.

  Ingat juga float64 cuma punya sekitar 16 angka penting. Bilangan kondisi
  yang melewati 1e16 berarti hasil hitungannya sudah kehilangan seluruh
  ketelitiannya. Bukan kurang teliti, tapi habis.

  Sekarang lihat kolom lambda_min. Matriks X^T X selalu semidefinit
  positif, jadi nilai eigen terkecilnya TIDAK MUNGKIN negatif. Itu
  teorema, bukan kebiasaan.

  Kalau di derajat tinggi kolom itu memberimu angka negatif, komputernya
  tidak menemukan sesuatu yang baru tentang aljabar linear. Ia sedang
  memberi tahu bahwa aritmetikanya sudah rusak. Angka yang mustahil
  adalah alarm paling jujur yang bisa kamu dapat, dan ia gratis.""")

    print("\n  Ongkosnya dalam iterasi, derajat 3:")
    print(f"  {'ragam':>12} {'cond':>12} {'iter sampai 1% dari optimum':>30}")
    print("  " + "-" * 58)

    for nama, pakai_baku in [("mentah", False), ("dibakukan", True)]:
        X = desain_polinom(x, 3).astype(float)
        if pakai_baku:
            X, _, _ = bakukan(X)
        H = (2 / len(y)) * X.T @ X
        lam = np.linalg.eigvalsh(H)
        theta_opt, *_ = np.linalg.lstsq(X, y, rcond=None)
        L_opt = mse_matriks(X, y, theta_opt)

        lr = 0.9 * 2 / lam[-1]
        theta = np.zeros(X.shape[1])
        hit = -1
        for i in range(400000):
            theta = theta - lr * gradien_matriks(X, y, theta)
            if not np.isfinite(theta).all():
                break
            if mse_matriks(X, y, theta) < L_opt * 1.01:
                hit = i
                break
        print(f"  {nama:>12} {lam[-1] / lam[0]:12.3e} {hit:30d}")

    print("""
  Bilangan kondisi turun, jumlah iterasi ikut turun, kira-kira sebanding.

  Itulah bayaran dari satu baris pembakuan fitur. Di Soal 5e Sesi B kamu
  sudah menduga arahnya benar. Sekarang kamu punya angkanya.""")


# ══════════════════════════════════════════════════════════════
# BAGIAN 4 - melihat model menghafal derau
# ══════════════════════════════════════════════════════════════

def bagian4(x_tr, y_tr, x_te, y_te):
    print("\n" + GARIS, "\nBAGIAN 4  empat derajat, satu data\n", GARIS, sep="")

    derajat = [1, 3, 9, 14]
    xs = np.linspace(-3.2, 3.2, 500)

    fig, sumbu = plt.subplots(1, 4, figsize=(18, 4.3), sharey=True)

    print(f"  {'derajat':>8} {'#param':>7} {'train':>10} {'test':>16}")
    print("  " + "-" * 45)

    for ax, d in zip(sumbu, derajat):
        X = desain_polinom(x_tr, d)
        theta, *_ = np.linalg.lstsq(X, y_tr, rcond=None)
        tr = mse_matriks(X, y_tr, theta)
        te = mse_matriks(desain_polinom(x_te, d), y_te, theta)
        print(f"  {d:8d} {d + 1:7d} {tr:10.6f} {te:16.4f}")

        ax.plot(xs, f_asli(xs), "g-", lw=2, alpha=0.7, label="fungsi asli")
        ax.plot(xs, desain_polinom(xs, d) @ theta, "r-", lw=1.8, label="model")
        ax.plot(x_tr, y_tr, "ko", ms=6, label="data latih")
        ax.set_ylim(-15, 15)
        ax.set_title(f"derajat {d}  ({d + 1} parameter)")
        ax.set_xlabel("x")
        ax.grid(alpha=0.25)

    sumbu[0].set_ylabel("y")
    sumbu[0].legend(fontsize=8, loc="upper left")
    plt.tight_layout()
    plt.savefig(FIGUR / "sesiC_derajat.png", dpi=110, bbox_inches="tight")
    plt.close()
    print(f"\n  plot disimpan : figures/sesiC_derajat.png")

    print(f"""
  Buka gambarnya. Empat panel, data yang sama persis di keempatnya.

  Panel pertama terlalu kaku untuk mengikuti lekuk kubiknya. Panel kedua
  memakai derajat yang benar dan hampir menempel pada kurva hijau.

  Panel keempat melewati SETIAP titik hitam, dan train loss-nya nol. Lalu
  lihat apa yang ia lakukan di antara titik-titik itu.

  Model itu tidak mempelajari kubiknya. Ia mempelajari 15 posisi derau
  tertentu, dan derau menurut definisinya tidak berulang. Test loss-nya
  {'':>0}menembus miliar.

  Lantai teoretisnya adalah ragam derau, yaitu {DERAU**2:.2f}. Model terbaik
  yang mungkin ada pun tidak bisa turun di bawah itu pada data baru.""")


# ══════════════════════════════════════════════════════════════
# BAGIAN 5 - kurva yang berpisah
# ══════════════════════════════════════════════════════════════

def bagian5(x_tr, y_tr, x_te, y_te):
    print("\n" + GARIS, "\nBAGIAN 5  titik tempat kedua kurva berpisah\n",
          GARIS, sep="")

    derajat = list(range(1, 15))
    tr_semua, te_semua = [], []

    print(f"  {'derajat':>8} {'train':>10} {'test':>16}")
    print("  " + "-" * 37)
    for d in derajat:
        X = desain_polinom(x_tr, d)
        theta, *_ = np.linalg.lstsq(X, y_tr, rcond=None)
        tr = mse_matriks(X, y_tr, theta)
        te = mse_matriks(desain_polinom(x_te, d), y_te, theta)
        tr_semua.append(tr)
        te_semua.append(te)
        print(f"  {d:8d} {tr:10.6f} {te:16.4f}")

    d_terbaik = derajat[int(np.argmin(te_semua))]

    plt.figure(figsize=(8, 5.2))
    plt.plot(derajat, tr_semua, "o-", lw=2, label="train loss")
    plt.plot(derajat, te_semua, "s-", lw=2, label="test loss")
    plt.axhline(DERAU**2, color="0.5", ls="--", label=f"lantai derau = {DERAU**2:.2f}")
    plt.axvline(3, color="g", ls=":", lw=2, label="derajat sebenarnya = 3")
    plt.axvline(d_terbaik, color="r", ls=":", lw=2,
                label=f"test terbaik = {d_terbaik}")
    plt.yscale("log")
    plt.xlabel("derajat polinomial")
    plt.ylabel("MSE (skala log)")
    plt.title("Train terus turun, test berbalik naik")
    plt.legend(fontsize=9)
    plt.grid(alpha=0.3)
    plt.savefig(FIGUR / "sesiC_train_test.png", dpi=110, bbox_inches="tight")
    plt.close()
    print(f"\n  plot disimpan : figures/sesiC_train_test.png")

    print(f"""
  Ini grafik yang kamu tunggu sejak Hari 3.

  Kurva train turun terus, tanpa pernah berbalik. Ia akan selalu begitu.
  Menambah parameter tidak pernah bisa memperburuk kecocokan pada data
  yang sedang dicocokkan.

  Kurva test punya dasar, lalu naik. Dasarnya di derajat {d_terbaik}, dan
  derajat sebenarnya adalah 3.

  Titik tempat kedua kurva mulai berpisah adalah batas antara memahami
  dan menghafal. Sebelum titik itu, parameter tambahan dipakai untuk
  menangkap pola. Sesudahnya, parameter tambahan dipakai untuk menghafal
  derau.

  Dan inilah masalah sebenarnya: kalau kamu cuma melihat kurva train,
  kedua wilayah itu tampak sama persis. Model yang overfit tidak
  menunjukkan gejala apa pun dari dalam.""")

    return d_terbaik


# ══════════════════════════════════════════════════════════════
# BAGIAN 6 - satu suku yang menyembuhkan
# ══════════════════════════════════════════════════════════════

def bagian6(x_tr, y_tr, x_te, y_te, d=14):
    print("\n" + GARIS, f"\nBAGIAN 6  L2 pada derajat {d}\n", GARIS, sep="")

    X = desain_polinom(x_tr, d)
    Xb, m, s = bakukan(X)
    Xtb, _, _ = bakukan(desain_polinom(x_te, d), m, s)

    lams = [0.0, 1e-6, 1e-4, 1e-2, 1e-1, 1.0, 10.0, 100.0]
    tr_semua, te_semua, norm_semua = [], [], []

    print(f"  {'lambda':>10} {'train':>10} {'test':>18} {'|theta|':>14}")
    print("  " + "-" * 56)
    for lam in lams:
        theta = ridge_tertutup(Xb, y_tr, lam)
        tr = mse_matriks(Xb, y_tr, theta)
        te = mse_matriks(Xtb, y_te, theta)
        tr_semua.append(tr)
        te_semua.append(te)
        norm_semua.append(np.linalg.norm(theta))
        print(f"  {lam:10} {tr:10.5f} {te:18.4f} {np.linalg.norm(theta):14.4f}")

    lam_terbaik = lams[int(np.argmin(te_semua))]

    fig, (kiri, kanan) = plt.subplots(1, 2, figsize=(13, 4.8))

    lams_plot = np.array(lams[1:])
    kiri.plot(lams_plot, tr_semua[1:], "o-", lw=2, label="train loss")
    kiri.plot(lams_plot, te_semua[1:], "s-", lw=2, label="test loss")
    kiri.axhline(DERAU**2, color="0.5", ls="--", label=f"lantai derau")
    kiri.set_xscale("log"); kiri.set_yscale("log")
    kiri.set_xlabel("lambda"); kiri.set_ylabel("MSE")
    kiri.set_title(f"derajat {d}, disapu lambda")
    kiri.legend(fontsize=9); kiri.grid(alpha=0.3)

    xs = np.linspace(-3.2, 3.2, 500)
    Xs, _, _ = bakukan(desain_polinom(xs, d), m, s)
    kanan.plot(xs, f_asli(xs), "g-", lw=2, alpha=0.7, label="fungsi asli")
    for lam, warna in [(0.0, "tab:red"), (lam_terbaik, "tab:blue"), (100.0, "tab:orange")]:
        theta = ridge_tertutup(Xb, y_tr, lam)
        kanan.plot(xs, Xs @ theta, lw=1.8, color=warna, label=f"lambda = {lam}")
    kanan.plot(x_tr, y_tr, "ko", ms=6, label="data latih")
    kanan.set_ylim(-15, 15)
    kanan.set_xlabel("x"); kanan.set_ylabel("y")
    kanan.set_title("bentuk model untuk tiga lambda")
    kanan.legend(fontsize=8); kanan.grid(alpha=0.25)

    plt.tight_layout()
    plt.savefig(FIGUR / "sesiC_regularisasi.png", dpi=110, bbox_inches="tight")
    plt.close()
    print(f"\n  plot disimpan : figures/sesiC_regularisasi.png")

    print(f"""
  Lihat kolom |theta| dari atas ke bawah. Tanpa denda, panjang vektor
  parameternya mencapai jutaan. Dengan lambda = {lam_terbaik}, ia turun jadi
  sekitar {norm_semua[int(np.argmin(te_semua))]:.2f}.

  Itu pegasnya bekerja. Suku lambda * |theta|^2 adalah energi potensial
  pegas, dan gradiennya 2 * lambda * theta adalah gaya pemulih yang
  sebanding dengan simpangan. Hukum Hooke, dengan lambda sebagai tetapan
  pegasnya.

  Sekarang bandingkan angkanya. Derajat {d} tanpa denda memberi test loss
  yang menembus miliar. Derajat {d} yang sama, dengan satu suku tambahan,
  memberi {min(te_semua):.2f}. Modelnya tidak diganti. Jumlah parameternya tidak
  dikurangi. Yang berubah cuma satu angka.

  Perhatikan juga kolom lambda punya bentuk U yang sama dengan kolom
  derajat di Bagian 5. Terlalu kecil, model menghafal. Terlalu besar,
  model jadi kaku dan tidak sanggup menangkap kubiknya. Dua kenop yang
  berbeda, satu bentuk yang sama, dan bentuk itu punya nama: pertukaran
  bias lawan ragam.""")


if __name__ == "__main__":
    x_tr, y_tr = buat_data(15, seed=7)
    x_te, y_te = buat_data(200, seed=99)
    try:
        bagian2()
        bagian3(x_tr, y_tr)
        bagian4(x_tr, y_tr, x_te, y_te)
        bagian5(x_tr, y_tr, x_te, y_te)
        bagian6(x_tr, y_tr, x_te, y_te)
    except NotImplementedError as e:
        print(f"\n  {e} belum diisi. Kerjakan TODO dulu.")
