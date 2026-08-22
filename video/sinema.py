"""Kit gaya bersama untuk seri video SYNESIS.

Semua bab memakai modul ini supaya tata letaknya konsisten: bingkai vertikal
720x1280, latar gelap, judul mono di atas, panggung visual di tengah, dan panel
kode dengan baris aktif disorot di bawah.

Angka yang muncul di layar dihitung dari kode yang sama dengan yang ada di
notebooks, bukan diketik manual. Itu aturan yang sama sejak Hari 1: kalau ada
angka di layar, ia harus bisa diproduksi ulang.

Jalankan lewat venv manimations:
    S:\\Code\\manimations\\.venv\\Scripts\\python.exe -m manim -qm video\\bab1_menuruni.py Bab1
"""

from manim import *
from manim import config

# ══════════════════════════════════════════════════════════════
# Bingkai vertikal 720 x 1280
# ══════════════════════════════════════════════════════════════

LEBAR_PIKSEL = 720
TINGGI_PIKSEL = 1280
LEBAR_BINGKAI = 9.0
TINGGI_BINGKAI = 16.0


def siapkan():
    """Panggil sekali di awal tiap berkas bab, sebelum kelas Scene dibaca."""
    config.pixel_width = LEBAR_PIKSEL
    config.pixel_height = TINGGI_PIKSEL
    config.frame_width = LEBAR_BINGKAI
    config.frame_height = TINGGI_BINGKAI
    config.background_color = PALET["latar"]
    config.frame_rate = 30


# ══════════════════════════════════════════════════════════════
# Palet
# ══════════════════════════════════════════════════════════════

PALET = {
    "latar": "#08080C",
    "kartu": "#0E1016",
    "garis": "#1C2230",
    "teks": "#E8EAF0",
    "redup": "#7C8698",
    "hijau": "#22C55E",
    "biru": "#60A5FA",
    "kuning": "#FBBF24",
    "merah": "#F87171",
    "ungu": "#A78BFA",
    "jingga": "#FB923C",
}

FONT_MONO = "Consolas"

# Tinggi acuan tata letak, dalam satuan bingkai (y dari -8 sampai 8)
Y_MEREK = 7.35
Y_JUDUL = 6.30
Y_SUBJUDUL = 5.35
Y_PENCACAH = 4.55
Y_PANGGUNG = 0.60
Y_KODE = -4.60
Y_KAKI = -7.45


# ══════════════════════════════════════════════════════════════
# Bagian bingkai
# ══════════════════════════════════════════════════════════════

def merek(teks="SYNESIS"):
    t = Text(teks, font=FONT_MONO, weight=BOLD, font_size=17, color=PALET["hijau"])
    t.move_to([LEBAR_BINGKAI / 2 - t.width / 2 - 0.35, Y_MEREK, 0])
    return t


def judul(teks, ukuran=40):
    """Judul utama, huruf besar berspasi lebar seperti pada contoh."""
    t = Text(teks.upper(), font=FONT_MONO, weight=BOLD, font_size=ukuran,
             color=PALET["teks"])
    # spasi antar huruf dilebarkan manual
    for i in range(1, len(t)):
        t[i].shift(RIGHT * 0.035 * i)
    t.move_to([0, Y_JUDUL, 0])
    if t.width > LEBAR_BINGKAI - 0.8:
        t.scale_to_fit_width(LEBAR_BINGKAI - 0.8)
        t.move_to([0, Y_JUDUL, 0])
    return t


def subjudul(baris, ukuran=19):
    """Satu atau dua baris penjelasan di bawah judul."""
    if isinstance(baris, str):
        baris = [baris]
    p = Paragraph(*baris, font=FONT_MONO, font_size=ukuran, color=PALET["redup"],
                  line_spacing=0.7, alignment="center")
    p.move_to([0, Y_SUBJUDUL, 0])
    if p.width > LEBAR_BINGKAI - 1.0:
        p.scale_to_fit_width(LEBAR_BINGKAI - 1.0)
        p.move_to([0, Y_SUBJUDUL, 0])
    return p


def pencacah(teks, warna=None, ukuran=23):
    """Baris angka berjalan, misal 'iterasi 12 / 60'."""
    t = Text(teks, font=FONT_MONO, weight=BOLD, font_size=ukuran,
             color=warna or PALET["hijau"])
    t.move_to([0, Y_PENCACAH, 0])
    return t


def kaki(teks="notebooks/  ·  github.com/SandyFauzi/SYNESIS"):
    t = Text(teks, font=FONT_MONO, font_size=14, color="#3A4252")
    t.move_to([0, Y_KAKI, 0])
    return t


# ══════════════════════════════════════════════════════════════
# Panel kode
# ══════════════════════════════════════════════════════════════

class PanelKode(VGroup):
    """Kartu kode gelap dengan nomor baris dan penyorot baris aktif.

    Pemakaian:
        pk = PanelKode(kode, keterangan="gradient descent, empat baris")
        self.add(pk)
        self.play(pk.sorot(3))       # sorot baris ke-4 (indeks mulai 0)
    """

    def __init__(self, kode, keterangan=None, lebar=7.9, ukuran_font=17, **kw):
        super().__init__(**kw)

        self.kode = Code(
            code_string=kode.strip("\n"),
            language="python",
            formatter_style="material",
            background="rectangle",
            add_line_numbers=True,
            paragraph_config={"font": FONT_MONO, "font_size": ukuran_font,
                              "line_spacing": 0.62},
            background_config={"fill_color": PALET["kartu"], "fill_opacity": 1.0,
                               "stroke_color": PALET["garis"], "stroke_width": 1.6,
                               "corner_radius": 0.10, "buff": 0.26},
        )
        if self.kode.width > lebar:
            self.kode.scale_to_fit_width(lebar)

        self.penyorot = None
        self.add(self.kode)

        if keterangan:
            self.keterangan = Text(keterangan, font=FONT_MONO, font_size=15,
                                   color=PALET["hijau"])
            self.keterangan.next_to(self.kode, UP, buff=0.20)
            self.add(self.keterangan)

        self.move_to([0, Y_KODE, 0])

    def _kotak(self, i):
        baris = self.kode.code_lines[i]
        lebar_dalam = self.kode.background.width - 0.30
        k = Rectangle(
            width=lebar_dalam, height=baris.height + 0.14,
            fill_color=PALET["hijau"], fill_opacity=0.16,
            stroke_color=PALET["hijau"], stroke_width=0, stroke_opacity=0.0,
        )
        k.move_to([self.kode.background.get_center()[0], baris.get_center()[1], 0])
        # garis penanda di tepi kiri
        tepi = Line(k.get_corner(UL), k.get_corner(DL),
                    stroke_color=PALET["hijau"], stroke_width=3.2)
        return VGroup(k, tepi)

    def sorot(self, i):
        """Kembalikan animasi yang memindahkan penyorot ke baris ke-i."""
        baru = self._kotak(i)
        if self.penyorot is None:
            self.penyorot = baru
            self.add_to_back(self.penyorot)
            return FadeIn(self.penyorot, run_time=0.25)
        lama = self.penyorot
        self.penyorot = baru
        self.remove(lama)
        self.add_to_back(self.penyorot)
        return ReplacementTransform(lama, baru, run_time=0.30)

    def padam(self):
        if self.penyorot is None:
            return Wait(0)
        a = FadeOut(self.penyorot, run_time=0.25)
        self.penyorot = None
        return a


# ══════════════════════════════════════════════════════════════
# Kartu angka, dipakai untuk menampilkan hasil ukur
# ══════════════════════════════════════════════════════════════

def kartu_angka(pasangan, lebar=7.4, ukuran=20, warna_nilai=None):
    """pasangan: daftar (label, nilai). Mengembalikan VGroup berisi kartu."""
    baris = VGroup()
    for label, nilai in pasangan:
        kiri = Text(label, font=FONT_MONO, font_size=ukuran, color=PALET["redup"])
        kanan = Text(str(nilai), font=FONT_MONO, weight=BOLD, font_size=ukuran,
                     color=warna_nilai or PALET["teks"])
        baris.add(VGroup(kiri, kanan))

    lebar_dalam = lebar - 0.7
    for b in baris:
        b[0].move_to([-lebar_dalam / 2 + b[0].width / 2, 0, 0])
        b[1].move_to([lebar_dalam / 2 - b[1].width / 2, 0, 0])
    baris.arrange(DOWN, buff=0.26, aligned_edge=LEFT)
    for b in baris:
        b[0].align_to(baris, LEFT)
        b[1].align_to(baris, RIGHT)

    kotak = RoundedRectangle(
        width=lebar, height=baris.height + 0.62, corner_radius=0.12,
        fill_color=PALET["kartu"], fill_opacity=1.0,
        stroke_color=PALET["garis"], stroke_width=1.6,
    )
    baris.move_to(kotak.get_center())
    return VGroup(kotak, baris)


def label_kecil(teks, warna=None, ukuran=17):
    return Text(teks, font=FONT_MONO, font_size=ukuran, color=warna or PALET["redup"])


def rumus(tex, ukuran=34, warna=None):
    m = MathTex(tex, font_size=ukuran, color=warna or PALET["teks"])
    return m


# ══════════════════════════════════════════════════════════════
# Data hasil pra-hitung, dipakai seri Bulan 1
# ══════════════════════════════════════════════════════════════

def muat_data(nama="bulan1"):
    """Baca hasil siapkan_data_bulan1.py. Kembalikan (npz, dict angka)."""
    import json
    from pathlib import Path

    import numpy as np

    d = Path(__file__).resolve().parent / "data"
    npz = np.load(d / f"{nama}.npz")
    angka = json.loads((d / f"{nama}.json").read_text(encoding="utf-8"))
    return npz, angka


def _hex_ke_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def gambar_skala(nilai, warna_rendah, warna_tinggi, tinggi=4.6, halus=False):
    """Ubah larik 2D 0..1 jadi ImageMobject dua warna.

    Dipakai untuk peta keputusan dan citra angka. Lebih cepat ribuan kali
    daripada menyusun satu Square per piksel.
    """
    import numpy as np

    a = np.clip(np.asarray(nilai, dtype=float), 0.0, 1.0)
    c0 = np.array(_hex_ke_rgb(warna_rendah), dtype=float)
    c1 = np.array(_hex_ke_rgb(warna_tinggi), dtype=float)
    rgb = c0[None, None, :] + (c1 - c0)[None, None, :] * a[:, :, None]
    img = ImageMobject(rgb.astype(np.uint8))
    if not halus:
        img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    img.height = tinggi
    return img


def garis_data(pasangan, warna, tebal=3.6):
    """VMobject dari daftar titik layar."""
    g = VMobject(stroke_color=warna, stroke_width=tebal)
    g.set_points_as_corners(list(pasangan))
    return g
