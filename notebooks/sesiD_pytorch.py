"""Sesi D - pembanding, PyTorch, dan GPU. Penutup Bulan 0.

Jalankan:
    . .\\scripts\\activate.ps1
    python notebooks\\sesiD_pytorch.py

Tiga sesi terakhir kamu menulis semuanya sendiri. Hari ini kamu menghadapkan
tulisanmu dengan pustaka yang selama ini sengaja dihindari.

Urutannya penting dan tidak boleh dibalik. Kalau kamu memakai loss.backward()
lebih dulu, ia akan terasa gaib selamanya. Karena kamu sudah menulis gradiennya
sendiri, malam ini ia berhenti jadi gaib.

Berkas ini memakai ulang desain_polinom, mse_matriks, gradien_matriks, dan
latih_matriks dari Sesi C.

Bagian bertanda TODO kamu yang isi.
"""

import time
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import torch  # noqa: E402

from sesiC_multivariat import (  # noqa: E402
    bakukan, buat_data, desain_polinom, gradien_matriks, latih_matriks, mse_matriks,
)

GARIS = "=" * 62
FIGUR = Path(__file__).resolve().parent.parent / "figures"
FIGUR.mkdir(exist_ok=True)


# ══════════════════════════════════════════════════════════════
# BAGIAN 1 - hadapkan dengan scikit-learn
# ══════════════════════════════════════════════════════════════

def bagian1(x_tr, y_tr):
    print(GARIS, "\nBAGIAN 1  tulisanmu lawan scikit-learn\n", GARIS, sep="")

    from sklearn.linear_model import LinearRegression, Ridge

    X = desain_polinom(x_tr, 3)

    # milikmu, lewat solusi tertutup
    theta_lstsq, *_ = np.linalg.lstsq(X, y_tr, rcond=None)

    # sklearn. fit_intercept=False karena kolom satuan sudah ada di X.
    sk = LinearRegression(fit_intercept=False).fit(X, y_tr)

    print("  Regresi biasa, derajat 3:")
    print(f"  {'koef':>6} {'punyamu':>14} {'sklearn':>14} {'selisih':>12}")
    print("  " + "-" * 50)
    for i, (a, b) in enumerate(zip(theta_lstsq, sk.coef_)):
        print(f"  {i:6d} {a:14.9f} {b:14.9f} {abs(a - b):12.3e}")

    # Ridge. alpha sklearn mendenda jumlah kuadrat, bukan rata-rata, jadi
    # alpha = lam * n supaya setara dengan rumusmu di Sesi C.
    lam, n = 0.1, len(y_tr)
    Xb, m, s = bakukan(X)
    from sesiC_multivariat import ridge_tertutup
    theta_ridge = ridge_tertutup(Xb, y_tr, lam)
    sk_ridge = Ridge(alpha=lam * n, fit_intercept=False).fit(Xb, y_tr)

    print(f"\n  Ridge, lambda = {lam} (alpha sklearn = {lam * n}):")
    print(f"  {'koef':>6} {'punyamu':>14} {'sklearn':>14} {'selisih':>12}")
    print("  " + "-" * 50)
    for i, (a, b) in enumerate(zip(theta_ridge, sk_ridge.coef_)):
        print(f"  {i:6d} {a:14.9f} {b:14.9f} {abs(a - b):12.3e}")

    print("""
  Perhatikan baris koefisien 0 pada Ridge. Kamu tidak mendenda geseran, dan
  sklearn dengan fit_intercept=False juga tidak punya geseran terpisah untuk
  didenda. Kalau selisihnya besar di baris itu saja, kemungkinan konvensinya
  yang berbeda, bukan kodenya yang salah.

  Beda konvensi lebih sering jadi sumber kebingungan daripada beda algoritma.
  Kalau angkamu tidak cocok dengan pustaka, curigai definisi lebih dulu:
  apakah dendanya dibagi n, apakah geseran ikut didenda, apakah faktor 2 ada.""")


# ══════════════════════════════════════════════════════════════
# BAGIAN 2 - model yang sama, ditulis dalam PyTorch
# ══════════════════════════════════════════════════════════════

def gradien_torch(X_np, y_np, theta_np, lam=0.0):
    """Gradien yang sama, tapi dihitung PyTorch lewat loss.backward().

    Langkahnya:
      1. ubah X, y, theta jadi tensor float64 (torch.double)
      2. theta harus punya requires_grad=True, karena itu kenop yang dilacak
      3. hitung residu dan MSE memakai operasi tensor biasa
      4. tambahkan denda L2, dan JANGAN denda theta[0]
      5. panggil loss.backward()
      6. kembalikan theta.grad sebagai array numpy

    Pakai torch.double, bukan float32. Target kecocokannya 1e-6, dan float32
    cuma punya sekitar 7 angka penting.

    Untuk mendenda semua kecuali elemen 0, cara paling bersih adalah
    menghitung denda dari theta[1:] saja. Menulis ke theta[0] secara langsung
    akan membuat autograd protes, dan alasannya adalah Soal 3.

    Kembalikan array numpy berbentuk sama dengan theta_np.
    """
    X = torch.tensor(X_np, dtype=torch.double)
    y = torch.tensor(y_np, dtype=torch.double)
    theta = torch.tensor(theta_np, dtype=torch.double, requires_grad=True)

    residu = X @ theta - y
    loss = (residu ** 2).mean()

    if lam > 0.0:
        loss = loss + lam * (theta[1:] ** 2).sum()

    loss.backward()
    return theta.grad.numpy()


def latih_torch(X_np, y_np, theta_np, lr, n_iter, lam=0.0):
    """Training loop versi PyTorch, tanpa optimizer.

    Sengaja tanpa torch.optim, supaya kamu melihat bahwa isinya tetap empat
    baris yang sama dengan Sesi A.

    Tiap iterasi:
      1. catat loss SEKARANG ke riwayat, sebelum memperbarui
      2. hitung loss, panggil backward()
      3. perbarui theta di dalam blok with torch.no_grad()
      4. nolkan theta.grad, karena PyTorch MENUMPUK gradien, tidak menimpanya

    Langkah 4 itu jebakan paling terkenal bagi pemula PyTorch. Kalau lupa,
    gradienmu jadi jumlah kumulatif seluruh iterasi sebelumnya, dan modelmu
    melesat entah ke mana tanpa satu pun pesan error.

    Kembalikan (theta_akhir sebagai numpy, riwayat_loss sebagai list).
    """
    X = torch.tensor(X_np, dtype=torch.double)
    y = torch.tensor(y_np, dtype=torch.double)
    theta = torch.tensor(theta_np, dtype=torch.double, requires_grad=True)

    riwayat_loss = []
    for _ in range(n_iter):
        residu = X @ theta - y
        mse = (residu ** 2).mean()
        riwayat_loss.append(mse.item())

        if lam > 0.0:
            loss = mse + lam * (theta[1:] ** 2).sum()
        else:
            loss = mse

        loss.backward()

        with torch.no_grad():
            theta.sub_(lr * theta.grad)
            theta.grad.zero_()

    return theta.detach().numpy(), riwayat_loss


# ══════════════════════════════════════════════════════════════
# BAGIAN 3 - momen yang ditunggu
# ══════════════════════════════════════════════════════════════

def bagian3(x_tr, y_tr):
    print("\n" + GARIS, "\nBAGIAN 3  gradien tanganmu lawan loss.backward()\n",
          GARIS, sep="")

    X = desain_polinom(x_tr, 3)

    print(f"  {'lambda':>8} {'selisih maks':>16} {'selisih relatif':>18}   status")
    print("  " + "-" * 60)

    semua_lolos = True
    rng = np.random.default_rng(11)
    for lam in [0.0, 0.01, 0.1, 1.0]:
        theta = rng.normal(0, 1.5, X.shape[1])
        g_tangan = gradien_matriks(X, y_tr, theta.copy(), lam)
        g_torch = gradien_torch(X, y_tr, theta.copy(), lam)
        maks = np.abs(g_tangan - g_torch).max()
        rel = maks / max(1e-12, np.abs(g_tangan).max())
        lolos = rel < 1e-6
        semua_lolos = semua_lolos and lolos
        print(f"  {lam:8} {maks:16.3e} {rel:18.3e}   {'lolos' if lolos else 'GAGAL'}")

    print(f"""
  Semua lolos: {semua_lolos}

  Berhenti sebentar di sini.

  Angka di kolom itu adalah selisih antara turunan yang kamu kerjakan di
  kertas pada Sesi A, lalu kamu perluas jadi bentuk matriks di Sesi C, dengan
  turunan yang dihitung mesin autograd PyTorch.

  PyTorch tidak memakai rumusmu. Ia menyusun graf komputasi saat perhitungan
  maju berjalan, lalu menelusurinya mundur dengan aturan rantai. Jalan yang
  sepenuhnya berbeda, hasil yang sama sampai batas ketelitian mesin.

  Mulai sekarang loss.backward() bukan kotak hitam. Ia melakukan persis apa
  yang kamu lakukan di kertas, cuma otomatis dan untuk graf sebesar apa pun.

  Dan itulah pintu masuk Bulan 1: kamu akan membangun mesin itu sendiri.""")

    return semua_lolos


# ══════════════════════════════════════════════════════════════
# BAGIAN 4 - dua training loop, satu hasil
# ══════════════════════════════════════════════════════════════

def bagian4(x_tr, y_tr):
    print("\n" + GARIS, "\nBAGIAN 4  training loop numpy lawan PyTorch\n",
          GARIS, sep="")

    X = desain_polinom(x_tr, 3)
    Xb, _, _ = bakukan(X)
    theta0 = np.zeros(Xb.shape[1])
    lr, n_iter = 0.1, 400

    th_np, hist_np = latih_matriks(Xb, y_tr, theta0.copy(), lr, n_iter)
    th_pt, hist_pt = latih_torch(Xb, y_tr, theta0.copy(), lr, n_iter)

    print(f"  {'koef':>6} {'numpy':>14} {'pytorch':>14} {'selisih':>12}")
    print("  " + "-" * 50)
    for i, (a, b) in enumerate(zip(th_np, th_pt)):
        print(f"  {i:6d} {a:14.9f} {b:14.9f} {abs(a - b):12.3e}")

    hn, hp = np.array(hist_np), np.array(hist_pt)
    print(f"\n  loss akhir numpy   : {mse_matriks(Xb, y_tr, th_np):.9f}")
    print(f"  loss akhir pytorch : {mse_matriks(Xb, y_tr, th_pt):.9f}")

    langsung = np.abs(hn - hp).max()
    geser = np.abs(hn[:-1] - hp[1:]).max()
    print(f"\n  riwayat dibandingkan langsung   : selisih maks {langsung:.3e}")
    print(f"  riwayat digeser satu iterasi    : selisih maks {geser:.3e}")

    if geser < langsung * 1e-3:
        print("""
  Yang digeser jauh lebih cocok. Artinya kedua loop menghitung hal yang sama,
  tapi mencatatnya pada saat yang berbeda. Satu mencatat sebelum memperbarui,
  satu sesudah.

  Ini bukan bug yang merusak hasil, dan parameter akhirnya identik. Tapi ia
  akan menipumu saat membandingkan kurva loss, dan kamu sudah menjawab persis
  soal ini di Soal 6c Sesi A. Sekarang kamu melihat akibatnya.""")
    else:
        print("\n  Kedua riwayat memakai konvensi pencatatan yang sama.")

    plt.figure(figsize=(8, 5))
    plt.plot(hn, lw=2.4, alpha=0.8, label="numpy, gradien tanganmu")
    plt.plot(hp, lw=1.4, ls="--", label="pytorch, backward()")
    plt.yscale("log")
    plt.xlabel("iterasi"); plt.ylabel("MSE (skala log)")
    plt.title("Dua jalan, satu kurva")
    plt.legend(); plt.grid(alpha=0.3)
    plt.savefig(FIGUR / "sesiD_dua_loop.png", dpi=110, bbox_inches="tight")
    plt.close()
    print("\n  plot disimpan : figures/sesiD_dua_loop.png")


# ══════════════════════════════════════════════════════════════
# BAGIAN 5 - kapan GPU justru kalah
# ══════════════════════════════════════════════════════════════

def ukur(n, d, perangkat, n_iter=300):
    """Satu langkah training penuh: maju, mundur, perbarui. Satuan milidetik."""
    dev = torch.device(perangkat)
    X = torch.randn(n, d, device=dev, dtype=torch.float32)
    y = torch.randn(n, device=dev, dtype=torch.float32)
    th = torch.zeros(d, device=dev, requires_grad=True)

    def langkah():
        # th.grad = None dan th.sub_ dipakai supaya tidak ada penugasan ke
        # nama th di dalam fungsi ini. Menulis th -= ... akan membuat Python
        # menganggap th variabel lokal, lalu melempar UnboundLocalError.
        th.grad = None
        ((X @ th - y) ** 2).mean().backward()
        with torch.no_grad():
            th.sub_(1e-3 * th.grad)

    for _ in range(10):          # pemanasan, wajib untuk GPU
        langkah()
    if perangkat == "cuda":
        torch.cuda.synchronize()

    t0 = time.perf_counter()
    for _ in range(n_iter):
        langkah()
    if perangkat == "cuda":
        torch.cuda.synchronize()
    return (time.perf_counter() - t0) / n_iter * 1000


def bagian5():
    print("\n" + GARIS, "\nBAGIAN 5  kapan GPU justru kalah\n", GARIS, sep="")

    if not torch.cuda.is_available():
        print("  CUDA tidak tersedia. Bagian ini dilewati.")
        return

    print(f"  perangkat : {torch.cuda.get_device_name(0)}\n")
    print(f"  {'n':>8} {'d':>6} {'CPU ms':>9} {'GPU ms':>9} {'rasio':>8}  pemenang")
    print("  " + "-" * 56)

    kasus = [(50, 2), (50, 10), (1000, 10), (1000, 1000),
             (10000, 100), (10000, 1000), (50000, 1000)]
    for n, d in kasus:
        c, g = ukur(n, d, "cpu"), ukur(n, d, "cuda")
        print(f"  {n:8} {d:6} {c:9.3f} {g:9.3f} {c / g:8.2f}  "
              f"{'GPU' if g < c else 'CPU'}")

    print("\n  Sapuan n pada d = 1000, mencari titik silang:")
    print(f"  {'n':>8} {'CPU ms':>9} {'GPU ms':>9}  pemenang")
    print("  " + "-" * 42)
    ns, cs, gs = [], [], []
    for n in [100, 300, 1000, 3000, 10000, 30000]:
        c, g = ukur(n, 1000, "cpu"), ukur(n, 1000, "cuda")
        ns.append(n); cs.append(c); gs.append(g)
        print(f"  {n:8} {c:9.3f} {g:9.3f}  {'GPU' if g < c else 'CPU'}")

    plt.figure(figsize=(8, 5))
    plt.plot(ns, cs, "o-", lw=2, label="CPU")
    plt.plot(ns, gs, "s-", lw=2, label="GPU")
    plt.xscale("log"); plt.yscale("log")
    plt.xlabel("n (jumlah baris data)"); plt.ylabel("milidetik per langkah")
    plt.title("CPU naik linear, GPU nyaris datar")
    plt.legend(); plt.grid(alpha=0.3, which="both")
    plt.savefig(FIGUR / "sesiD_cpu_gpu.png", dpi=110, bbox_inches="tight")
    plt.close()
    print("\n  plot disimpan : figures/sesiD_cpu_gpu.png")

    print(f"""
  Lihat kolom GPU pada sapuan terakhir. Dari n = 100 sampai n = 10000, data
  membesar seratus kali lipat, tapi waktunya nyaris tidak berubah.

  Itu bukan keajaiban. Itu tanda bahwa waktunya sama sekali bukan dihabiskan
  untuk menghitung. Yang dibayar adalah ongkos tetap: memerintahkan GPU
  memulai kernel, menunggu, lalu menyinkronkan. Perhitungannya sendiri
  tenggelam di bawah ongkos itu.

  CPU tidak punya ongkos tetap sebesar itu, tapi waktunya naik sebanding
  dengan jumlah pekerjaan.

  Jadi bentuknya {'ongkos tetap + ongkos per satuan'}, dan GPU baru menang
  setelah pekerjaannya cukup besar untuk menutup ongkos tetapnya.

  Sekarang lihat baris pertama tabel di atas, n = 50 dan d = 2. Itu model
  Sesi A sampai C. Memindahkannya ke GPU akan membuatnya lebih LAMBAT. Semua
  yang kamu kerjakan di Bulan 0 memang tempatnya di CPU.""")


# ══════════════════════════════════════════════════════════════
# BAGIAN 6 - penutup Bulan 0
# ══════════════════════════════════════════════════════════════

def bagian6():
    print("\n" + GARIS, "\nBAGIAN 6  yang sudah kamu bangun\n", GARIS, sep="")
    print("""
  Empat sesi lalu kamu belum pernah menurunkan satu pun gradien.

  Sekarang kamu punya, semuanya tulisan sendiri: fungsi loss, gradien
  analitik yang diverifikasi dengan beda hingga, training loop, permukaan
  loss beserta animasi lintasannya, kriteria kestabilan yang diramalkan dari
  nilai eigen Hessian lalu terbukti sampai empat angka, bentuk matriks yang
  tidak peduli berapa jumlah parameter, dan regularisasi L2 yang kamu pahami
  sebagai Hukum Hooke.

  Dan malam ini gradien tulisanmu bertemu loss.backward(), lalu keduanya
  sepakat.

  Yang berubah di Bulan 1 cuma satu hal: modelnya berhenti linear.

  Akibatnya berantai. Permukaan loss berhenti jadi mangkuk tunggal, jadi
  titik awal yang berbeda mendarat di tempat yang berbeda. Hessian mulai
  bergantung pada y, jadi lr aman tidak bisa lagi dihitung sebelum melihat
  label. Turunan ketiga berhenti nol, jadi h = 1e-5 kembali jadi anjuran
  yang benar untuk beda hingga.

  Yang tidak berubah: ukur seberapa salah, cari arah menurun, melangkah,
  ulangi. Itu tetap sama sampai Modul 6.

  Bulan 1 dimulai dengan menulis mesin autograd sendiri, sekitar 150 baris.
  Setelah malam ini, kamu sudah tahu persis apa yang harus dilakukan mesin
  itu, karena kamu baru saja membuktikan hasilnya cocok dengan hasilmu.""")


if __name__ == "__main__":
    x_tr, y_tr = buat_data(15, seed=7)
    try:
        bagian1(x_tr, y_tr)
        bagian3(x_tr, y_tr)
        bagian4(x_tr, y_tr)
        bagian5()
        bagian6()
    except NotImplementedError as e:
        print(f"\n  {e} belum diisi. Kerjakan TODO dulu.")
