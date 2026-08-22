"""Bab 4 - Mesin yang Menurunkan Sendiri. Isi Sesi D dan Bulan 1 Sesi 1.

Pertanyaannya: apa sebenarnya yang dikerjakan loss.backward(), dan kenapa
satu karakter di dalamnya menentukan benar atau salah.

Grafnya memakai angka bulat supaya bisa diikuti di kepala:
    w = 2.0,  x = 1.5,  b = 1.0,  y = 5.0
    u = w*x = 3.0,  v = u+b = 4.0,  r = v-y = -1.0,  L = r^2 = 1.0
    dL/dr = -2,  dL/dv = -2,  dL/du = -2,  dL/db = -2,  dL/dw = -3

Render:
    S:\\Code\\manimations\\.venv\\Scripts\\python.exe -m manim -qh video\\bab4_mesin.py Bab4
"""

import numpy as np

from sinema import (
    PALET, FONT_MONO, PanelKode, judul, kaki, kartu_angka, label_kecil,
    merek, pencacah, siapkan, subjudul,
)

siapkan()

from manim import *  # noqa: E402

# ══════════════════════════════════════════════════════════════
# Graf contoh, dihitung bukan diketik
# ══════════════════════════════════════════════════════════════

W, XX, B, YY = 2.0, 1.5, 1.0, 5.0
U = W * XX
V = U + B
R = V - YY
L = R ** 2

G_L = 1.0
G_R = 2 * R * G_L
G_V = G_R
G_U = G_V
G_B = G_V
G_W = XX * G_U
G_X = W * G_U

KODE_MUL = """
def __mul__(self, other):
    out = Value(self.data * other.data)

    def _backward():
        self.grad  += other.data * out.grad
        other.grad += self.data  * out.grad

    out._backward = _backward
    return out
"""

# angka hasil uji dari notebooks/bulan1_sesi1_autograd.py
UJI_ACAK = 300
GALAT_TERBURUK = "1.866e-08"
COCOK_TORCH = "0.000e+00"


def simpul(nama, nilai, pos, warna, lebar=1.55, tinggi=0.78):
    kotak = RoundedRectangle(
        width=lebar, height=tinggi, corner_radius=0.14,
        fill_color=PALET["kartu"], fill_opacity=1.0,
        stroke_color=warna, stroke_width=2.4,
    )
    tulisan = Text(nama, font=FONT_MONO, weight=BOLD, font_size=19, color=warna)
    angka = Text(f"{nilai:g}", font=FONT_MONO, font_size=17, color=PALET["teks"])
    tulisan.move_to(kotak.get_center() + UP * 0.155)
    angka.move_to(kotak.get_center() + DOWN * 0.165)
    g = VGroup(kotak, tulisan, angka)
    g.move_to(pos)
    return g


def panah(dari, ke, warna, lebar=2.6):
    return Arrow(dari.get_bottom(), ke.get_top(), buff=0.10,
                 stroke_width=lebar, max_tip_length_to_length_ratio=0.16,
                 color=warna)


class Bab4(Scene):
    def construct(self):
        self.camera.background_color = PALET["latar"]

        jd = judul("The Slope Machine", 34)
        sj = subjudul(["Month 1  ·  what is actually inside",
                       "loss.backward(), written from scratch"])
        mk, kk = merek(), kaki()

        self.play(FadeIn(mk, run_time=0.5), FadeIn(kk, run_time=0.5))
        self.play(Write(jd, run_time=1.0))
        self.play(FadeIn(sj, shift=UP * 0.15, run_time=0.6))
        self.wait(0.4)

        # ---------- bangun grafnya ----------
        n_w = simpul("w", W, [-1.65, 3.45, 0], PALET["kuning"])
        n_x = simpul("x", XX, [1.65, 3.45, 0], PALET["biru"])
        n_u = simpul("u = w*x", U, [-0.55, 1.85, 0], PALET["teks"], lebar=2.5)
        n_b = simpul("b", B, [2.55, 1.85, 0], PALET["kuning"])
        n_v = simpul("v = u+b", V, [0.35, 0.30, 0], PALET["teks"], lebar=2.5)
        n_y = simpul("y", YY, [-2.45, 0.30, 0], PALET["biru"])
        n_r = simpul("r = v-y", R, [-0.55, -1.25, 0], PALET["teks"], lebar=2.5)
        n_L = simpul("L = r^2", L, [-0.55, -2.80, 0], PALET["hijau"], lebar=2.5)

        semua = [n_w, n_x, n_u, n_b, n_v, n_y, n_r, n_L]
        rusuk = [
            panah(n_w, n_u, PALET["garis"]), panah(n_x, n_u, PALET["garis"]),
            panah(n_u, n_v, PALET["garis"]), panah(n_b, n_v, PALET["garis"]),
            panah(n_v, n_r, PALET["garis"]), panah(n_y, n_r, PALET["garis"]),
            panah(n_r, n_L, PALET["garis"]),
        ]

        sj_maju = pencacah("FORWARD   ·   values flow downward",
                           PALET["biru"], 19)
        self.play(FadeIn(sj_maju, run_time=0.4))

        urut = [(n_w, None), (n_x, None), (n_u, [rusuk[0], rusuk[1]]),
                (n_b, None), (n_v, [rusuk[2], rusuk[3]]),
                (n_y, None), (n_r, [rusuk[4], rusuk[5]]),
                (n_L, [rusuk[6]])]
        for nd, rs in urut:
            anim = [FadeIn(nd, scale=0.85, run_time=0.35)]
            if rs:
                anim = [Create(r, run_time=0.30) for r in rs] + anim
            self.play(*anim)
        self.wait(0.8)

        ket_maju = label_kecil("every operation writes down who its parents were. "
                               "That is the whole graph.",
                               PALET["redup"], 14)
        ket_maju.move_to([0, -4.05, 0])
        self.play(FadeIn(ket_maju, run_time=0.5))
        self.wait(1.2)
        self.play(FadeOut(ket_maju), run_time=0.3)

        # ---------- mundur ----------
        sj_mundur = pencacah("BACKWARD   ·   slopes flow upward",
                            PALET["hijau"], 19)
        self.play(Transform(sj_maju, sj_mundur), run_time=0.5)

        def label_grad(nd, nilai, arah=RIGHT):
            t = Text(f"grad {nilai:g}", font=FONT_MONO, weight=BOLD,
                     font_size=16, color=PALET["hijau"])
            t.next_to(nd, arah, buff=0.14)
            return t

        mundur = [
            (n_L, G_L, RIGHT, None),
            (n_r, G_R, RIGHT, rusuk[6]),
            (n_v, G_V, RIGHT, rusuk[4]),
            (n_y, G_R * -1, LEFT, rusuk[5]),
            (n_u, G_U, LEFT, rusuk[2]),
            (n_b, G_B, RIGHT, rusuk[3]),
            (n_w, G_W, LEFT, rusuk[0]),
            (n_x, G_X, RIGHT, rusuk[1]),
        ]

        label_semua = VGroup()
        for nd, nilai, arah, rs in mundur:
            lg = label_grad(nd, nilai, arah)
            label_semua.add(lg)
            anim = [FadeIn(lg, run_time=0.30)]
            if rs is not None:
                anim.insert(0, rs.animate.set_color(PALET["hijau"]).set_stroke(width=4.0))
            self.play(*anim, run_time=0.42)
            self.wait(0.10)

        self.wait(0.7)

        r_rantai = MathTex(r"\frac{\partial L}{\partial w}"
                           r"=\frac{\partial L}{\partial r}\,"
                           r"\frac{\partial r}{\partial v}\,"
                           r"\frac{\partial v}{\partial u}\,"
                           r"\frac{\partial u}{\partial w}"
                           r"=-2\cdot 1\cdot 1\cdot 1.5=-3",
                           font_size=26, color=PALET["kuning"])
        r_rantai.move_to([0, -4.15, 0])
        if r_rantai.width > 8.2:
            r_rantai.scale_to_fit_width(8.2)
        self.play(Write(r_rantai, run_time=1.4))
        self.wait(1.0)

        ket_rantai = label_kecil("the chain rule. The same one from first year calculus.",
                                 PALET["redup"], 14)
        ket_rantai.move_to([0, -5.05, 0])
        self.play(FadeIn(ket_rantai, run_time=0.5))
        self.wait(1.6)

        # ---------- jebakan satu karakter ----------
        self.play(
            *[FadeOut(m) for m in semua], *[FadeOut(r) for r in rusuk],
            FadeOut(label_semua), FadeOut(r_rantai), FadeOut(ket_rantai),
            FadeOut(sj_maju), FadeOut(sj), run_time=0.7,
        )

        sj2 = subjudul(["One node used twice, and a single",
                        "character decides right from wrong"])
        self.play(FadeIn(sj2, run_time=0.5))

        a_nilai = 1.7
        n_a = simpul("a", a_nilai, [0, 2.75, 0], PALET["kuning"])
        n_p = simpul("a * a", a_nilai * a_nilai, [0, 0.75, 0], PALET["teks"],
                     lebar=2.3)
        kiri = Arrow(n_a.get_bottom() + LEFT * 0.35, n_p.get_top() + LEFT * 0.35,
                     buff=0.10, stroke_width=2.8, color=PALET["garis"],
                     max_tip_length_to_length_ratio=0.2)
        kanan = Arrow(n_a.get_bottom() + RIGHT * 0.35, n_p.get_top() + RIGHT * 0.35,
                      buff=0.10, stroke_width=2.8, color=PALET["garis"],
                      max_tip_length_to_length_ratio=0.2)

        self.play(FadeIn(n_a), FadeIn(n_p), Create(kiri), Create(kanan),
                  run_time=0.9)

        ket_dua = label_kecil("two paths, two slope contributions into the same node",
                              PALET["redup"], 14)
        ket_dua.move_to([0, -0.55, 0])
        self.play(FadeIn(ket_dua, run_time=0.5))
        self.wait(0.8)

        salah = VGroup(
            Text("self.grad  = ...", font=FONT_MONO, font_size=19,
                 color=PALET["merah"]),
            Text(f"dL/da = {a_nilai:g}", font=FONT_MONO, weight=BOLD,
                 font_size=21, color=PALET["merah"]),
            Text("FAILS", font=FONT_MONO, weight=BOLD, font_size=17,
                 color=PALET["merah"]),
        ).arrange(DOWN, buff=0.18).move_to([-2.05, -2.15, 0])

        benar = VGroup(
            Text("self.grad += ...", font=FONT_MONO, font_size=19,
                 color=PALET["hijau"]),
            Text(f"dL/da = {2 * a_nilai:g}", font=FONT_MONO, weight=BOLD,
                 font_size=21, color=PALET["hijau"]),
            Text("passes", font=FONT_MONO, weight=BOLD, font_size=17,
                 color=PALET["hijau"]),
        ).arrange(DOWN, buff=0.18).move_to([2.05, -2.15, 0])

        self.play(FadeIn(salah, shift=UP * 0.15, run_time=0.6))
        self.wait(0.7)
        self.play(FadeIn(benar, shift=UP * 0.15, run_time=0.6))
        self.wait(1.0)

        pk = PanelKode(KODE_MUL, keterangan="notebooks/bulan1_sesi1_autograd.py",
                       ukuran_font=15)
        self.play(FadeIn(pk, shift=UP * 0.2, run_time=0.7))
        self.play(pk.sorot(4))
        self.wait(0.5)
        self.play(pk.sorot(5))
        self.wait(1.2)

        # ---------- tiga saksi ----------
        self.play(FadeOut(n_a), FadeOut(n_p), FadeOut(kiri), FadeOut(kanan),
                  FadeOut(ket_dua), FadeOut(salah), FadeOut(benar),
                  FadeOut(pk), FadeOut(sj2), run_time=0.7)

        sj3 = subjudul(["Three witnesses that never copied",
                        "each other, and you wrote two of them"])
        self.play(FadeIn(sj3, run_time=0.5))

        saksi = VGroup()
        for nama, ket, warna in [
            ("NUDGE AND MEASURE", "just runs the function twice\nknows nothing about the chain rule", PALET["biru"]),
            ("YOUR OWN ENGINE", "a computation graph\n90 lines you wrote yourself", PALET["kuning"]),
            ("PYTORCH", "industrial autograd\nwritten by thousands of people", PALET["ungu"]),
        ]:
            kotak = RoundedRectangle(width=7.6, height=1.42, corner_radius=0.14,
                                     fill_color=PALET["kartu"], fill_opacity=1.0,
                                     stroke_color=warna, stroke_width=2.0)
            jt = Text(nama, font=FONT_MONO, weight=BOLD, font_size=19, color=warna)
            kt = Paragraph(*ket.split("\n"), font=FONT_MONO, font_size=14,
                           color=PALET["redup"], line_spacing=0.6,
                           alignment="center")
            jt.move_to(kotak.get_center() + UP * 0.34)
            kt.move_to(kotak.get_center() + DOWN * 0.24)
            saksi.add(VGroup(kotak, jt, kt))
        saksi.arrange(DOWN, buff=0.30).move_to([0, 1.55, 0])

        self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.15) for s in saksi],
                              lag_ratio=0.3, run_time=1.6))
        self.wait(0.8)

        kartu = kartu_angka([
            (f"{UJI_ACAK} random expressions, worst gap", GALAT_TERBURUK),
            ("agreement with PyTorch", COCOK_TORCH),
            ("failures", "0"),
        ], warna_nilai=PALET["hijau"]).move_to([0, -2.55, 0])
        self.play(FadeIn(kartu, shift=UP * 0.2, run_time=0.7))
        self.wait(1.6)

        tutup = Paragraph(
            "loss.backward() stopped being a black box",
            "not by reading the documentation,",
            "but by rewriting it and proving it agrees.",
            font=FONT_MONO, font_size=17, color=PALET["teks"],
            line_spacing=0.75, alignment="center",
        ).move_to([0, -4.75, 0])
        self.play(FadeIn(tutup, run_time=0.9))
        self.wait(2.0)

        akhir = Text("SYNESIS", font=FONT_MONO, weight=BOLD, font_size=42,
                     color=PALET["hijau"]).move_to([0, -6.35, 0])
        self.play(FadeIn(akhir, scale=0.9, run_time=0.8))
        self.wait(1.4)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.3)
