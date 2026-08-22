"""Kanvas tulis tangan, ditebak jaringan Bulan 1.

Jalankan:
    . .\\scripts\\activate.ps1
    python notebooks\\bulan1_kanvas.py

Tulis di kanvas kiri pakai mouse. Lepas tombol, panel kanan langsung menebak.

Modelnya jaringan 784-128-10 yang sama persis dari Sesi 3+4: kelas `Tensor`
tulisanmu, nol `torch.nn`. Latihan pertama kali sekitar setengah menit, lalu
bobotnya disimpan dan jalan berikutnya langsung buka.

Yang ditebak cuma ANGKA 0 sampai 9. MNIST memang cuma berisi itu. Huruf butuh
EMNIST, dan itu unduhan terpisah 562 MB.

Tulis besar-besar, hampir sepenuh kanvas. Letaknya bebas, karena coretanmu
dipotong ke kotak isinya lalu dipusatkan ulang. Yang tidak ikut diperbaiki
cuma tebal pena relatif: angka mungil yang ditulis dengan pena 22 piksel jadi
gumpalan sesudah dikecilkan ke 20 piksel.

Kotak "yang dilihat model" di kanan bukan hiasan. Kalau tebakannya meleset,
lihat kotak itu dulu sebelum menyalahkan jaringannya.
"""

import sys
import tkinter as tk
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageTk

sys.path.insert(0, str(Path(__file__).resolve().parent))

from bulan1_sesi34_mnist import (  # noqa: E402
    DATA, Tensor, akurasi, latih_mnist, maju, muat_mnist,
)

MODEL = DATA / "mnist_model_128.npz"
SISI = 336          # ukuran kanvas di layar
PENA = 22           # tebal coretan, kira-kira setara garis MNIST sesudah dikecilkan


# ══════════════════════════════════════════════════════════════
# Model
# ══════════════════════════════════════════════════════════════

def ambil_model():
    """Muat bobot kalau ada, kalau tidak latih sekali lalu simpan."""
    if MODEL.exists():
        d = np.load(MODEL)
        return [Tensor(d[f"p{i}"]) for i in range(4)], float(d["uji"])

    print("  bobot belum ada, melatih sekali. Sekitar setengah menit.\n")
    X, y, Xv, yv, Xu, yu = muat_mnist()
    param, riw, terbaik = latih_mnist(X, y, Xv, yv)
    for p, d in zip(param, terbaik[2]):
        p.data = d
    uji = akurasi(param, Xu, yu)
    print(f"\n  akurasi uji : {uji * 100:.2f} persen")
    np.savez_compressed(MODEL, uji=uji,
                        **{f"p{i}": p.data for i, p in enumerate(param)})
    print(f"  bobot disimpan : {MODEL}\n")
    return param, uji


def tebak(param, x784):
    z = maju(param, x784[None, :]).data[0]
    e = np.exp(z - z.max())
    return e / e.sum()


# ══════════════════════════════════════════════════════════════
# Coretan layar jadi masukan 784 angka
# ══════════════════════════════════════════════════════════════

def siapkan(gambar):
    """Ubah coretan jadi vektor 784, mengikuti cara MNIST dibuat.

    Empat langkah, dan ketiganya yang pertama wajib. Tanpa itu jaringanmu
    akan menebak asal walaupun akurasi ujinya 97 persen, karena yang kamu
    berikan bukan benda yang sama dengan yang dilatihkan.

        1  potong ke kotak isi, buang pinggiran kosong
        2  skalakan sisi terpanjang jadi 20 piksel
        3  tempel ke bidang 28x28 sehingga pusat massanya di tengah
        4  bagi 255

    Kembalikan (vektor 784, gambar 28x28) atau (None, None) kalau kanvasnya
    masih kosong.
    """
    a = np.asarray(gambar, dtype=np.float64)
    if a.max() == 0:
        return None, None

    baris = np.nonzero(a.any(axis=1))[0]
    kolom = np.nonzero(a.any(axis=0))[0]
    potong = Image.fromarray(
        a[baris[0]:baris[-1] + 1, kolom[0]:kolom[-1] + 1].astype(np.uint8))

    lebar, tinggi = potong.size
    skala = 20.0 / max(lebar, tinggi)
    # BOX itu rata-rata luas, dan itu persis cara MNIST asli dibuat abu-abu.
    # Diukur pada 300 gambar uji lewat jalur ini: BOX 95.3 persen, LANCZOS 95.0,
    # BILINEAR 94.7. Selisihnya tipis, tapi BOX tidak bisa berdering sama sekali
    # dan itu yang penting untuk coretan bertepi keras.
    kecil = potong.resize((max(1, round(lebar * skala)),
                           max(1, round(tinggi * skala))), Image.BOX)

    bidang = Image.new("L", (28, 28), 0)
    bidang.paste(kecil, ((28 - kecil.size[0]) // 2, (28 - kecil.size[1]) // 2))

    # geser supaya pusat massa jatuh di tengah, seperti MNIST asli.
    # ponytail: geser bilangan bulat pakai np.roll. Selisihnya dengan
    # interpolasi subpiksel di bawah setengah piksel, tidak terasa di 28x28.
    b = np.asarray(bidang, dtype=np.float64)
    total = b.sum()
    if total > 0:
        cy = (b.sum(axis=1) @ np.arange(28)) / total
        cx = (b.sum(axis=0) @ np.arange(28)) / total
        b = np.roll(b, (round(13.5 - cy), round(13.5 - cx)), axis=(0, 1))

    return (b.ravel() / 255.0), b


# ══════════════════════════════════════════════════════════════
# Jendela
# ══════════════════════════════════════════════════════════════

class Aplikasi:
    def __init__(self, akar, param, uji):
        self.param = param
        akar.title("Kanvas Bulan 1 - jaringan 784-128-10 tulisan sendiri")
        akar.resizable(False, False)

        bingkai = tk.Frame(akar, padx=10, pady=10)
        bingkai.pack()

        # ---------- kiri: kanvas ----------
        kiri = tk.Frame(bingkai)
        kiri.grid(row=0, column=0, sticky="n")
        tk.Label(kiri, text="tulis di sini", font=("Segoe UI", 11)).pack()

        self.kanvas = tk.Canvas(kiri, width=SISI, height=SISI, bg="black",
                                highlightthickness=1, highlightbackground="#555",
                                cursor="crosshair")
        self.kanvas.pack()
        self.kanvas.bind("<Button-1>", self.turun)
        self.kanvas.bind("<B1-Motion>", self.seret)
        self.kanvas.bind("<ButtonRelease-1>", lambda e: self.ramal())

        self.gambar = Image.new("L", (SISI, SISI), 0)
        self.pena = ImageDraw.Draw(self.gambar)
        self.titik = None

        tombol = tk.Frame(kiri, pady=6)
        tombol.pack(fill="x")
        tk.Button(tombol, text="Bersihkan  (Esc)", command=self.bersih,
                  width=18).pack(side="left")
        tk.Label(tombol, text=f"akurasi uji {uji * 100:.2f}%",
                 fg="#777").pack(side="right")

        # ---------- kanan: hasil ----------
        kanan = tk.Frame(bingkai, padx=14)
        kanan.grid(row=0, column=1, sticky="n")

        self.jawab = tk.Label(kanan, text="-", font=("Segoe UI", 72, "bold"))
        self.jawab.pack()
        self.yakin = tk.Label(kanan, text="tulis sesuatu", font=("Segoe UI", 11),
                              fg="#777")
        self.yakin.pack()

        self.batang = tk.Canvas(kanan, width=250, height=250,
                                highlightthickness=0)
        self.batang.pack(pady=(10, 8))

        tk.Label(kanan, text="yang dilihat model, 28x28",
                 font=("Segoe UI", 9), fg="#777").pack()
        self.kotak = tk.Label(kanan, bd=1, relief="solid")
        self.kotak.pack()

        akar.bind("<Escape>", lambda e: self.bersih())
        self.gambar_batang(np.zeros(10))

    # ---------- menggambar ----------
    def turun(self, e):
        self.titik = (e.x, e.y)
        self.seret(e)

    def seret(self, e):
        x0, y0 = self.titik
        self.kanvas.create_line(x0, y0, e.x, e.y, fill="white", width=PENA,
                                capstyle=tk.ROUND, smooth=True)
        self.pena.line([x0, y0, e.x, e.y], fill=255, width=PENA)
        self.pena.ellipse([e.x - PENA // 2, e.y - PENA // 2,
                           e.x + PENA // 2, e.y + PENA // 2], fill=255)
        self.titik = (e.x, e.y)

    def bersih(self):
        self.kanvas.delete("all")
        self.pena.rectangle([0, 0, SISI, SISI], fill=0)
        self.jawab.config(text="-")
        self.yakin.config(text="tulis sesuatu")
        self.gambar_batang(np.zeros(10))
        self.kotak.config(image="")

    # ---------- menebak ----------
    def ramal(self):
        x, kecil = siapkan(self.gambar)
        if x is None:
            return
        p = tebak(self.param, x)
        self.jawab.config(text=str(int(p.argmax())))
        self.yakin.config(text=f"yakin {p.max() * 100:.1f} persen")
        self.gambar_batang(p)

        besar = Image.fromarray(kecil.astype(np.uint8)).resize(
            (140, 140), Image.NEAREST)
        self.foto = ImageTk.PhotoImage(besar)      # simpan, kalau tidak dibuang
        self.kotak.config(image=self.foto)

    def gambar_batang(self, p):
        self.batang.delete("all")
        urut = np.argsort(-p)
        for baris, k in enumerate(urut):
            y = baris * 25 + 4
            warna = "#2e7d32" if baris == 0 else "#9e9e9e"
            self.batang.create_text(12, y + 8, text=str(k),
                                    font=("Consolas", 12, "bold"))
            self.batang.create_rectangle(26, y + 2, 26 + 170, y + 15,
                                         outline="#ddd")
            if p[k] > 0:
                self.batang.create_rectangle(26, y + 2, 26 + 170 * p[k], y + 15,
                                             fill=warna, outline="")
            self.batang.create_text(228, y + 8, text=f"{p[k] * 100:4.1f}%",
                                    font=("Consolas", 9), fill="#555")


if __name__ == "__main__":
    param, uji = ambil_model()
    akar = tk.Tk()
    Aplikasi(akar, param, uji)
    akar.mainloop()
