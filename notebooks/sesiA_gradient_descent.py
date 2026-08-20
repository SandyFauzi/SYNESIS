"""Sesi A - gradient descent utuh.

Jalankan:
    . .\\activate.ps1
    python notebooks\\sesiA_gradient_descent.py

Hari 3 kamu membangun permukaannya. Hari ini kelerengnya menggelinding.

Berkas ini memakai ulang buat_data, prediksi, dan mse yang sudah kamu tulis
di hari03_data_loss.py. Kalau yang di sana benar, yang di sini ikut benar.

Bagian bertanda TODO kamu yang isi.
"""

from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from hari03_data_loss import B_ASLI, W_ASLI, buat_data, mse, prediksi  # noqa: E402

GARIS = "=" * 62
FIGUR = Path(__file__).resolve().parent.parent / "figures"
FIGUR.mkdir(exist_ok=True)


# ══════════════════════════════════════════════════════════════
# BAGIAN 1 - gradien analitik
# ══════════════════════════════════════════════════════════════

def gradien(x, y, w, b):
    n = len(x)
    r = (w * x + b) - y

    dw = (2.0 / n) * np.sum(r * x)
    
    db = (2.0 / n) * np.sum(r)
    
    return dw, db


# ══════════════════════════════════════════════════════════════
# BAGIAN 2 - gradien numerik sebagai pembanding
# ══════════════════════════════════════════════════════════════

def beda_hingga(x, y, w, b, h=1e-5):
    # --- Bagian nyari turunan parsial w (b diam) ---
    
    # 1. Hitung Loss kalau w maju sejauh h
    loss_w_maju   = mse(prediksi(x, w + h, b), y)
    
    # 2. Hitung Loss kalau w mundur sejauh h
    loss_w_mundur = mse(prediksi(x, w - h, b), y)
    
    # 3. Hitung selisihnya lalu bagi jarak lintasan (2h)
    dw = (loss_w_maju - loss_w_mundur) / (2 * h)

    # --- Bagian nyari turunan parsial b (w diam) ---
    
    # 4. Hitung Loss kalau b maju sejauh h
    loss_b_maju   = mse(prediksi(x, w, b + h), y)
    
    # 5. Hitung Loss kalau b mundur sejauh h
    loss_b_mundur = mse(prediksi(x, w, b - h), y)
    
    # 6. Hitung selisihnya lalu bagi jarak lintasan (2h)
    db = (loss_b_maju - loss_b_mundur) / (2 * h)
    
    # 7. Kembalikan 2 angkanya
    return dw, db


# ══════════════════════════════════════════════════════════════
# BAGIAN 3 - gradient check
# ══════════════════════════════════════════════════════════════

def galat_relatif(a, n):
    """Selisih relatif dua angka, aman terhadap pembagian nol."""
    return abs(a - n) / max(1e-12, abs(a) + abs(n))


def bagian3(x, y):
    print(GARIS, "\nBAGIAN 3  gradient check\n", GARIS, sep="")

    titik = [(0.0, 0.0), (1.0, 0.5), (3.0, 2.0), (5.0, -1.0), (2.9, 2.1)]

    print(f"  {'w':>6} {'b':>6}   {'rel dL/dw':>12}  {'rel dL/db':>12}   status")
    print("  " + "-" * 58)

    semua_lolos = True
    for w, b in titik:
        ga = gradien(x, y, w, b)
        gn = beda_hingga(x, y, w, b)
        rw = galat_relatif(ga[0], gn[0])
        rb = galat_relatif(ga[1], gn[1])
        lolos = rw < 1e-6 and rb < 1e-6
        semua_lolos = semua_lolos and lolos
        print(f"  {w:6.2f} {b:6.2f}   {rw:12.3e}  {rb:12.3e}   "
              f"{'lolos' if lolos else 'GAGAL'}")

    print(f"""
  Target selisih relatif di bawah 1e-6. Angka yang kamu lihat kemungkinan
  jauh lebih kecil dari itu, dan alasannya ada di Soal 3.

  Teknik ini akan menemanimu sampai Bulan 5. Di Bulan 1 ia jadi satu-satunya
  cara memverifikasi mesin autograd buatanmu, karena tidak ada pustaka yang
  bisa kamu percaya untuk memeriksa pustaka yang sedang kamu tulis sendiri.

  Semua lolos: {semua_lolos}""")
    return semua_lolos


# ══════════════════════════════════════════════════════════════
# BAGIAN 4 - training loop
# ══════════════════════════════════════════════════════════════

def latih(x, y, w, b, lr, n_iter):
    """Gradient descent. Lima baris yang melatih semua model di dunia.

    Tiap iterasi:
        1. hitung loss dengan w dan b sekarang
        2. hitung gradien
        3. w = w - lr * dL_dw
           b = b - lr * dL_db
        4. simpan (iterasi, w, b, loss) ke riwayat

    Catat dulu SEBELUM memperbarui, supaya riwayat baris pertama adalah
    kondisi awal.

    Kembalikan (w_akhir, b_akhir, riwayat) dengan riwayat berupa list
    of tuple (i, w, b, loss).

    Satu hal yang perlu dijaga. Kalau lr kebesaran, w dan b akan meledak
    jadi inf lalu nan, dan program akan terus berputar tanpa guna sampai
    n_iter habis. Berhenti lebih awal kalau np.isfinite(w) sudah False.

    TODO 3
    """
    riwayat = []
    
    for i in range(n_iter):
        loss_skrg = mse(prediksi(x, w, b), y)
        riwayat.append((i, w, b, loss_skrg))
        
        dw, db = gradien(x, y, w, b)
        
        w = w - (lr * dw)
        b = b - (lr * db)
        
        if not np.isfinite(w):
            break
            
    return w, b, riwayat


def bagian4(x, y):
    print("\n" + GARIS, "\nBAGIAN 4  konvergensi dari berbagai titik awal\n",
          GARIS, sep="")

    awal = [(0.0, 0.0), (-5.0, 10.0), (100.0, -100.0)]
    print(f"  {'w awal':>8} {'b awal':>9}   {'w akhir':>10} {'b akhir':>10} {'loss':>10}")
    print("  " + "-" * 56)

    hasil = []
    for w0, b0 in awal:
        w, b, _ = latih(x, y, w0, b0, lr=0.02, n_iter=2000)
        loss = mse(prediksi(x, w, b), y)
        hasil.append((w, b))
        print(f"  {w0:8.1f} {b0:9.1f}   {w:10.6f} {b:10.6f} {loss:10.6f}")

    print(f"""
  Ketiganya mendarat di titik yang sama, sampai enam angka di belakang koma.
  Itu bukan keberuntungan. Permukaan loss model linear cuma punya satu dasar,
  jadi dari mana pun kamu melepas kelerengnya, ia berakhir di lubang yang sama.

  Sifat ini akan hilang mulai Bulan 1. Jaringan berlapis punya banyak lembah,
  dan titik awal yang berbeda mendarat di tempat yang berbeda. Nikmati
  kepastian ini selagi masih ada.

  Parameter asli: w = {W_ASLI}, b = {B_ASLI}
  Hasil training: w = {hasil[0][0]:.6f}, b = {hasil[0][1]:.6f}

  b meleset lumayan jauh. Itu bukan bug, dan Soal 4 membahasnya.""")


# ══════════════════════════════════════════════════════════════
# BAGIAN 5 - sapuan learning rate
# ══════════════════════════════════════════════════════════════

def bagian5(x, y):
    print("\n" + GARIS, "\nBAGIAN 5  sapuan learning rate\n", GARIS, sep="")

    daftar_lr = [0.0001, 0.001, 0.01, 0.05, 0.1, 0.12, 0.13, 0.2]

    print(f"  {'lr':>8}   {'w akhir':>16} {'b akhir':>14}   status")
    print("  " + "-" * 58)

    kurva = {}
    for lr in daftar_lr:
        w, b, riwayat = latih(x, y, 0.0, 0.0, lr, 500)
        loss = mse(prediksi(x, w, b), y) if np.isfinite(w) and np.isfinite(b) else np.inf
        divergen = (not np.isfinite(loss)) or loss > 1e6
        kurva[lr] = [r[3] for r in riwayat]
        print(f"  {lr:8}   {w:16.6f} {b:14.6f}   "
              f"{'DIVERGEN' if divergen else 'konvergen'}")

    plt.figure(figsize=(8, 5))
    for lr, losses in kurva.items():
        losses = np.array(losses, dtype=float)
        tampak = losses[np.isfinite(losses) & (losses > 0)]
        plt.plot(range(len(tampak)), tampak, lw=1.6, label=f"lr = {lr}")
    plt.yscale("log")
    plt.xlabel("iterasi")
    plt.ylabel("MSE (skala log)")
    plt.title("Kurva loss untuk berbagai learning rate")
    plt.legend(fontsize=8)
    plt.grid(alpha=0.3)
    plt.savefig(FIGUR / "sesiA_sapuan_lr.png", dpi=110, bbox_inches="tight")
    plt.close()
    print("\n  plot disimpan : figures/sesiA_sapuan_lr.png")

    print("""
  Di suatu tempat antara dua nilai lr yang berdekatan, perilakunya berbalik
  dari konvergen jadi meledak. Peralihannya mendadak, bukan berangsur.

  Soal 5 memintamu meramalkan letak batas itu dari kelengkungan permukaan,
  sebelum melihat tabel di atas. Kalau kamu sudah terlanjur melihat, ramalkan
  saja untuk dataset dengan seed berbeda, lalu uji.""")


# ══════════════════════════════════════════════════════════════
# BAGIAN 6 - pembanding analitik
# ══════════════════════════════════════════════════════════════

def bagian6(x, y):
    print("\n" + GARIS, "\nBAGIAN 6  pembanding solusi tertutup\n", GARIS, sep="")

    n = len(x)
    M = np.vstack([x, np.ones(n)]).T
    sol, *_ = np.linalg.lstsq(M, y, rcond=None)
    w_ls, b_ls = sol

    w_gd, b_gd, _ = latih(x, y, 0.0, 0.0, lr=0.02, n_iter=5000)

    print(f"  gradient descent : w = {w_gd:.9f}   b = {b_gd:.9f}")
    print(f"  kuadrat terkecil : w = {w_ls:.9f}   b = {b_ls:.9f}")
    print(f"  selisih          : {abs(w_gd - w_ls):.2e}       {abs(b_gd - b_ls):.2e}")

    r = prediksi(x, w_ls, b_ls) - y
    print(f"\n  rata-rata residu di titik optimum : {np.sum(r) / n:.3e}")
    print(f"  x rata-rata : {x.mean():.6f}   y rata-rata : {y.mean():.6f}")
    print(f"  garis di x rata-rata : {w_ls * x.mean() + b_ls:.6f}")

    print("""
  Dua jalan yang sama sekali berbeda mendarat di angka yang sama. Yang satu
  merayap ribuan langkah, yang satu memakai rumus tertutup dari Soal 4c Hari 3.

  Dua baris terakhir bukan kebetulan juga. Menyamakan dMSE/db dengan nol
  berarti jumlah residu nol, dan itu memaksa garis melewati titik pusat massa
  data. Soal 4 memintamu membuktikan ini.""")


if __name__ == "__main__":
    x, y = buat_data()
    try:
        bagian3(x, y)
        bagian4(x, y)
        bagian5(x, y)
        bagian6(x, y)
    except NotImplementedError as e:
        print(f"\n  {e} belum diisi. Kerjakan TODO dulu.")
