"""Hari 3 - data dan loss.

Jalankan:
    . .\\scripts\\activate.ps1
    python notebooks\\hari03_data_loss.py

Hari ini kamu membangun permukaan yang akan dituruni di Hari 7.
Belum ada gradient descent. Yang dibangun dulu adalah lanskapnya.

Bagian bertanda TODO kamu yang isi.
"""

from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")          # simpan ke berkas, jangan buka jendela
import matplotlib.pyplot as plt  # noqa: E402

GARIS = "=" * 62
FIGUR = Path(__file__).resolve().parent.parent / "figures"
FIGUR.mkdir(exist_ok=True)

# Parameter yang sebenarnya. Data dibangkitkan dari sini, lalu kita pura-pura
# tidak tahu dan mencoba menemukannya kembali dari data. Persis seperti
# mengukur konstanta pegas dari data simpangan dan gaya.
W_ASLI = 3.0
B_ASLI = 2.0


# ══════════════════════════════════════════════════════════════
# BAGIAN 1 - bangkitkan data
# ══════════════════════════════════════════════════════════════

def buat_data(n=50, derau=1.5, seed=42):
    """y = W_ASLI * x + B_ASLI + derau gaussian."""
    rng = np.random.default_rng(seed)
    x = rng.uniform(-5, 5, n)
    y = W_ASLI * x + B_ASLI + rng.normal(0, derau, n)
    return x, y


def bagian1(x, y):
    print(GARIS, "\nBAGIAN 1  data sintetis\n", GARIS, sep="")
    print(f"  n           : {len(x)}")
    print(f"  x rentang   : [{x.min():.2f}, {x.max():.2f}]")
    print(f"  y rentang   : [{y.min():.2f}, {y.max():.2f}]")
    print(f"  parameter asli : w = {W_ASLI}, b = {B_ASLI}")

    plt.figure(figsize=(7, 5))
    plt.scatter(x, y, s=28, alpha=0.7, label="data terukur")
    xs = np.linspace(-5, 5, 100)
    plt.plot(xs, W_ASLI * xs + B_ASLI, "r-", lw=2,
             label=f"garis asli: y = {W_ASLI}x + {B_ASLI}")
    plt.xlabel("x"); plt.ylabel("y")
    plt.title("Data sintetis dengan derau gaussian")
    plt.legend(); plt.grid(alpha=0.3)
    plt.savefig(FIGUR / "hari03_data.png", dpi=110, bbox_inches="tight")
    plt.close()
    print(f"  plot disimpan  : figures/hari03_data.png")


# ══════════════════════════════════════════════════════════════
# BAGIAN 2 - yang kamu tulis
# ══════════════════════════════════════════════════════════════

def prediksi(x, w, b):
    """Ramalan model garis lurus: y_ramal = w * x + b.

    Terima x berupa array, kembalikan array dengan bentuk sama.
    Boleh memakai operasi vektor numpy di sini. Hari 2 sudah membuktikan
    kenapa loop tidak perlu.

    TODO 1
    """
    return w * x + b


def mse(y_ramal, y_asli):
    """Mean Squared Error.

        MSE = (1/n) * sum( (y_ramal[i] - y_asli[i])^2 )

    Kembalikan SATU angka.

    Dilarang: np.mean, np.square, sklearn. Boleh: pengurangan array,
    perkalian array, dan np.sum untuk penjumlahan akhir.

    TODO 2
    """
    diff = y_ramal - y_asli
    return np.sum(diff * diff) / len(y_asli)


def mae(y_ramal, y_asli):
    """Mean Absolute Error, pembanding untuk Soal 5.

        MAE = (1/n) * sum( |y_ramal[i] - y_asli[i]| )

    TODO 3
    """
    return np.sum(np.abs(y_ramal - y_asli)) / len(y_asli)


# ══════════════════════════════════════════════════════════════
# BAGIAN 3 - hitung loss untuk beberapa tebakan
# ══════════════════════════════════════════════════════════════

def bagian3(x, y):
    print("\n" + GARIS, "\nBAGIAN 3  loss untuk beberapa tebakan\n", GARIS, sep="")

    tebakan = [
        (0.0, 0.0, "tebakan buta"),
        (1.0, 0.0, "kemiringan terlalu landai"),
        (3.0, 0.0, "kemiringan benar, geseran salah"),
        (5.0, 2.0, "kemiringan terlalu curam"),
        (3.0, 2.0, "parameter asli"),
        (2.9, 2.1, "sangat dekat"),
    ]

    print(f"  {'w':>6} {'b':>6}   {'MSE':>10}   keterangan")
    print("  " + "-" * 52)
    for w, b, ket in tebakan:
        loss = mse(prediksi(x, w, b), y)
        print(f"  {w:6.2f} {b:6.2f}   {loss:10.4f}   {ket}")

    print("""
  Perhatikan baris 'parameter asli'. Loss-nya TIDAK nol.

  Kenapa? Karena data memuat derau. Bahkan parameter yang benar-benar
  membangkitkan data pun tidak bisa melewati setiap titik. Loss sisa itu
  adalah derau yang tidak mungkin dihilangkan model mana pun.

  Ini batas bawah. Model yang loss-nya di bawah angka ini justru
  mencurigakan: dia menghafal derau, bukan menangkap polanya.""")


# ══════════════════════════════════════════════════════════════
# BAGIAN 4 - irisan pertama dari permukaan loss
# ══════════════════════════════════════════════════════════════

def bagian4(x, y):
    print("\n" + GARIS, "\nBAGIAN 4  irisan permukaan loss\n", GARIS, sep="")

    # Kunci b di nilai aslinya, sapu w saja. Ini irisan 1D dari permukaan
    # 2D yang akan kamu gambar utuh di Hari 9.
    ws = np.linspace(-2, 8, 200)
    losses = np.array([mse(prediksi(x, w, B_ASLI), y) for w in ws])

    w_min = ws[losses.argmin()]
    print(f"  w dengan loss terkecil : {w_min:.3f}")
    print(f"  w asli                  : {W_ASLI}")
    print(f"  loss di titik itu       : {losses.min():.4f}")

    plt.figure(figsize=(7, 5))
    plt.plot(ws, losses, lw=2)
    plt.axvline(W_ASLI, color="r", ls="--", alpha=0.7, label=f"w asli = {W_ASLI}")
    plt.scatter([w_min], [losses.min()], color="r", zorder=5, s=60)
    plt.xlabel("w"); plt.ylabel("MSE")
    plt.title(f"Irisan permukaan loss pada b = {B_ASLI}")
    plt.legend(); plt.grid(alpha=0.3)
    plt.savefig(FIGUR / "hari03_irisan_loss.png", dpi=110, bbox_inches="tight")
    plt.close()
    print(f"  plot disimpan           : figures/hari03_irisan_loss.png")

    print("""
  Bentuknya parabola. Itu bukan kebetulan.

  MSE memuat selisih yang dikuadratkan, jadi terhadap w ia polinomial
  derajat dua. Selalu. Untuk model linear, permukaan loss-nya selalu
  mangkuk, dan mangkuk hanya punya satu dasar.

  Kamu sudah kenal bentuk ini dari Mekanika:

      V(x) = (1/2) k x^2        potensial harmonik
      MSE(w) ~ a(w - w*)^2 + c  permukaan loss

  Persamaan yang sama. Karena itulah gradient descent pada model linear
  berperilaku seperti massa pada pegas, dan learning rate yang kebesaran
  membuatnya berosilasi lalu terlempar, persis seperti sistem teredam
  yang kekurangan redaman.""")


if __name__ == "__main__":
    x, y = buat_data()
    bagian1(x, y)
    try:
        bagian3(x, y)
        bagian4(x, y)
    except NotImplementedError as e:
        print(f"\n  {e} belum diisi. Kerjakan TODO dulu.")
