"""Bab 3 - Menghafal atau Memahami. Isi Sesi C.

Pertanyaannya: kenapa model yang diberi lebih banyak kebebasan justru jadi
lebih buruk, dan kenapa obatnya ternyata Hukum Hooke.

Angka kuncinya, dihitung ulang di berkas ini:
    derajat 8 -> test 6.3470
    derajat 9 -> test 923.5812
    derajat 12 tanpa denda -> test 3833567, dengan lambda 0.1 -> test 5.0121

Render:
    S:\\Code\\manimations\\.venv\\Scripts\\python.exe -m manim -qh video\\bab3_menghafal.py Bab3
"""

import numpy as np

from sinema import (
    PALET, FONT_MONO, Y_PANGGUNG, judul, kaki, kartu_angka, label_kecil,
    merek, pencacah, siapkan, subjudul,
)

siapkan()

from manim import *  # noqa: E402

# ══════════════════════════════════════════════════════════════
# Data dan model, sama persis dengan notebooks/sesiC_multivariat.py
# ══════════════════════════════════════════════════════════════

DERAU = 1.5


def f_asli(x):
    return 0.5 * x ** 3 - 2.0 * x + 1.0


def buat_data(n, seed):
    rng = np.random.default_rng(seed)
    x = np.sort(rng.uniform(-3, 3, n))
    return x, f_asli(x) + rng.normal(0, DERAU, n)


def desain_polinom(x, derajat):
    X = np.ones((len(x), derajat + 1))
    for i in range(1, derajat + 1):
        X[:, i] = x ** i
    return X


def bakukan(X, m=None, s=None):
    Xb = X.copy().astype(float)
    if m is None:
        m = Xb[:, 1:].mean(axis=0)
        s = Xb[:, 1:].std(axis=0)
        s = np.where(s < 1e-12, 1.0, s)
    Xb[:, 1:] = (Xb[:, 1:] - m) / s
    return Xb, m, s


def ridge_tertutup(X, y, lam):
    n, d = X.shape
    R = np.eye(d)
    R[0, 0] = 0.0
    return np.linalg.solve(X.T @ X / n + lam * R, X.T @ y / n)


X_TR, Y_TR = buat_data(15, seed=7)
X_TE, Y_TE = buat_data(200, seed=99)

DERAJAT = list(range(1, 15))
KOEF, RUGI_TR, RUGI_TE, KONDISI = {}, {}, {}, {}
for d in DERAJAT:
    Xd = desain_polinom(X_TR, d)
    th, *_ = np.linalg.lstsq(Xd, Y_TR, rcond=None)
    KOEF[d] = th
    RUGI_TR[d] = float(np.mean((Xd @ th - Y_TR) ** 2))
    RUGI_TE[d] = float(np.mean((desain_polinom(X_TE, d) @ th - Y_TE) ** 2))
    KONDISI[d] = float(np.linalg.cond(Xd))

# Ridge di derajat 12
D_RIDGE = 12
_Xtr_b, _m, _s = bakukan(desain_polinom(X_TR, D_RIDGE))
_Xte_b, _, _ = bakukan(desain_polinom(X_TE, D_RIDGE), _m, _s)
TH_POLOS, *_ = np.linalg.lstsq(_Xtr_b, Y_TR, rcond=None)
TH_RIDGE = ridge_tertutup(_Xtr_b, Y_TR, 0.1)
TE_POLOS = float(np.mean((_Xte_b @ TH_POLOS - Y_TE) ** 2))
TE_RIDGE = float(np.mean((_Xte_b @ TH_RIDGE - Y_TE) ** 2))
NORMA_POLOS = float(np.linalg.norm(TH_POLOS[1:]))
NORMA_RIDGE = float(np.linalg.norm(TH_RIDGE[1:]))


def kurva_polinom(th, t):
    return float(sum(c * t ** i for i, c in enumerate(th)))


def kurva_baku(th, t):
    v = np.array([t ** i for i in range(1, D_RIDGE + 1)])
    v = (v - _m) / _s
    return float(th[0] + th[1:] @ v)


class Bab3(Scene):
    def construct(self):
        self.camera.background_color = PALET["latar"]

        jd = judul("Menghafal atau Paham", 34)
        sj = subjudul(["Sesi C  ·  kenapa model yang lebih bebas",
                       "justru jadi lebih bodoh"])
        mk, kk = merek(), kaki()

        self.play(FadeIn(mk, run_time=0.5), FadeIn(kk, run_time=0.5))
        self.play(Write(jd, run_time=1.0))
        self.play(FadeIn(sj, shift=UP * 0.15, run_time=0.6))

        # ---------- panggung: data dan kurva yang makin liar ----------
        sumbu = Axes(
            x_range=[-3.4, 3.4, 1], y_range=[-16, 16, 8],
            x_length=7.4, y_length=6.0,
            axis_config={"color": PALET["garis"], "stroke_width": 2.0,
                         "tip_length": 0.14, "font_size": 18},
        ).move_to([0, Y_PANGGUNG + 0.35, 0])

        titik_tr = VGroup(*[
            Dot(sumbu.c2p(xi, yi), radius=0.062, color=PALET["biru"])
            for xi, yi in zip(X_TR, Y_TR)
        ])
        sejati = DashedVMobject(
            sumbu.plot(f_asli, x_range=[-3.2, 3.2],
                       color=PALET["redup"], stroke_width=2.6),
            num_dashes=46, dashed_ratio=0.55)
        sejati_ket = label_kecil("garis putus: fungsi sebenarnya, "
                                 "yang model tidak pernah lihat",
                                 PALET["redup"], 14)
        sejati_ket.next_to(sumbu, DOWN, buff=0.18)

        self.play(Create(sumbu, run_time=0.8))
        self.play(LaggedStart(*[GrowFromCenter(d) for d in titik_tr],
                              lag_ratio=0.05, run_time=1.0))
        self.play(Create(sejati, run_time=0.9), FadeIn(sejati_ket, run_time=0.4))
        self.wait(0.6)

        d_awal = 1
        pas = sumbu.plot(lambda t: kurva_polinom(KOEF[d_awal], t),
                         x_range=[-3.2, 3.2], color=PALET["kuning"],
                         stroke_width=4.2)
        cacah = pencacah(f"derajat {d_awal}   train {RUGI_TR[d_awal]:.2f}"
                         f"   test {RUGI_TE[d_awal]:.2f}", PALET["hijau"], 19)
        self.play(Create(pas, run_time=0.8), FadeIn(cacah, run_time=0.4))
        self.wait(0.8)

        for d in DERAJAT[1:]:
            warna = PALET["hijau"] if RUGI_TE[d] < 10 else (
                PALET["kuning"] if RUGI_TE[d] < 1000 else PALET["merah"])
            te = f"{RUGI_TE[d]:.2f}" if RUGI_TE[d] < 1e4 else f"{RUGI_TE[d]:.1e}"
            baru_cacah = pencacah(
                f"derajat {d}   train {RUGI_TR[d]:.2f}   test {te}", warna, 19)
            baru_pas = sumbu.plot(
                lambda t, d=d: float(np.clip(kurva_polinom(KOEF[d], t), -16.4, 16.4)),
                x_range=[-3.2, 3.2, 0.02], color=PALET["kuning"],
                stroke_width=4.2)
            self.play(Transform(pas, baru_pas), Transform(cacah, baru_cacah),
                      run_time=0.55 if d < 9 else 0.75)
            if d in (8, 9):
                self.wait(1.0)

        self.wait(0.6)

        lonjak = kartu_angka([
            ("derajat 8, test", f"{RUGI_TE[8]:.4f}"),
            ("derajat 9, test", f"{RUGI_TE[9]:.4f}"),
        ], warna_nilai=PALET["merah"]).move_to([0, -5.4, 0])
        self.play(FadeIn(lonjak, run_time=0.6))
        self.wait(1.3)
        self.play(FadeOut(lonjak), run_time=0.4)

        # ---------- dua kurva rugi ----------
        self.play(FadeOut(pas), FadeOut(titik_tr), FadeOut(sejati),
                  FadeOut(sumbu), FadeOut(sejati_ket), FadeOut(cacah),
                  FadeOut(sj), run_time=0.7)

        sj2 = subjudul(["latih terus turun. uji berbalik naik.",
                        "di situlah menghafal dimulai"])
        self.play(FadeIn(sj2, run_time=0.5))

        sumbu2 = Axes(
            x_range=[1, 14, 2], y_range=[-1.2, 7.2, 2],
            x_length=7.0, y_length=5.8,
            axis_config={"color": PALET["garis"], "stroke_width": 2.0,
                         "tip_length": 0.14, "font_size": 18},
        ).move_to([0, Y_PANGGUNG + 0.35, 0])

        lbl_x = label_kecil("derajat polinom", PALET["redup"], 16)
        lbl_x.next_to(sumbu2, DOWN, buff=0.18)
        lbl_y = label_kecil("log10 rugi", PALET["redup"], 16)
        lbl_y.rotate(PI / 2).next_to(sumbu2, LEFT, buff=0.12)

        t_tr = [(d, np.log10(max(RUGI_TR[d], 1e-6))) for d in DERAJAT]
        t_te = [(d, np.log10(max(RUGI_TE[d], 1e-6))) for d in DERAJAT]

        def garis_dari(pasangan, warna):
            g = VMobject(stroke_color=warna, stroke_width=4.0)
            g.set_points_as_corners([sumbu2.c2p(a, b) for a, b in pasangan])
            return g

        gt = garis_dari(t_tr, PALET["biru"])
        ge = garis_dari(t_te, PALET["merah"])
        st = VGroup(*[Dot(sumbu2.c2p(a, b), radius=0.05, color=PALET["biru"])
                      for a, b in t_tr])
        se = VGroup(*[Dot(sumbu2.c2p(a, b), radius=0.05, color=PALET["merah"])
                      for a, b in t_te])

        ket_tr = label_kecil("data latih", PALET["biru"], 17)
        ket_te = label_kecil("data uji", PALET["merah"], 17)
        ket_tr.move_to(sumbu2.c2p(11.2, t_tr[-1][1] + 0.9))
        ket_te.move_to(sumbu2.c2p(4.6, t_te[3][1] + 1.4))

        self.play(Create(sumbu2, run_time=0.8), FadeIn(lbl_x), FadeIn(lbl_y))
        self.play(Create(gt, run_time=1.3), FadeIn(st, run_time=1.3),
                  FadeIn(ket_tr, run_time=0.8))
        self.play(Create(ge, run_time=1.6), FadeIn(se, run_time=1.6),
                  FadeIn(ket_te, run_time=0.8))

        pisah = DashedLine(sumbu2.c2p(8.5, -1.2), sumbu2.c2p(8.5, 7.2),
                           stroke_color=PALET["kuning"], stroke_width=2.4,
                           dash_length=0.09)
        ket_pisah = label_kecil("15 titik data, 10 parameter", PALET["kuning"], 15)
        ket_pisah.next_to(pisah, UP, buff=0.10)
        self.play(Create(pisah, run_time=0.6), FadeIn(ket_pisah, run_time=0.4))
        self.wait(1.6)

        # ---------- Hukum Hooke ----------
        self.play(FadeOut(sumbu2), FadeOut(gt), FadeOut(ge), FadeOut(st),
                  FadeOut(se), FadeOut(ket_tr), FadeOut(ket_te), FadeOut(pisah),
                  FadeOut(ket_pisah), FadeOut(lbl_x), FadeOut(lbl_y),
                  FadeOut(sj2), run_time=0.7)

        sj3 = subjudul(["obatnya sudah kamu pelajari",
                        "di Fisika Dasar: pegas"])
        self.play(FadeIn(sj3, run_time=0.5))

        r1 = MathTex(r"L = \mathrm{MSE} + \lambda \lVert \theta \rVert^2",
                     font_size=34, color=PALET["teks"]).move_to([0, 3.6, 0])
        r2 = MathTex(r"\frac{\partial}{\partial \theta}\,\lambda\lVert\theta\rVert^2"
                     r"= 2\lambda\theta",
                     font_size=32, color=PALET["kuning"]).move_to([0, 2.4, 0])
        r3 = MathTex(r"F = -k x \quad\Longrightarrow\quad k = 2\lambda",
                     font_size=32, color=PALET["hijau"]).move_to([0, 1.3, 0])

        self.play(Write(r1, run_time=1.0))
        self.play(Write(r2, run_time=0.9))
        self.play(Write(r3, run_time=0.9))
        self.wait(0.8)

        # pegas menarik theta ke nol
        pusat = np.array([0.0, -0.35, 0.0])
        dinding = Line(pusat + LEFT * 3.1 + UP * 0.55,
                       pusat + LEFT * 3.1 + DOWN * 0.55,
                       stroke_color=PALET["redup"], stroke_width=5)
        massa_x = ValueTracker(2.3)

        def buat_pegas():
            a = pusat + LEFT * 3.1
            b = pusat + RIGHT * massa_x.get_value()
            n_lilit, amp = 14, 0.24
            titik = []
            for i in range(n_lilit * 12 + 1):
                s = i / (n_lilit * 12)
                p = a + (b - a) * s
                p = p + UP * amp * np.sin(TAU * n_lilit * s)
                titik.append(p)
            m = VMobject(stroke_color=PALET["ungu"], stroke_width=3.0)
            m.set_points_as_corners(titik)
            return m

        pegas = always_redraw(buat_pegas)
        massa = always_redraw(lambda: Square(
            side_length=0.62, fill_color=PALET["kuning"], fill_opacity=1.0,
            stroke_width=0).move_to(pusat + RIGHT * massa_x.get_value()))
        titik_nol = DashedLine(pusat + UP * 0.9, pusat + DOWN * 0.9,
                               stroke_color=PALET["hijau"], stroke_width=2.0,
                               dash_length=0.08)
        lbl_nol = label_kecil("theta = 0", PALET["hijau"], 15)
        lbl_nol.next_to(titik_nol, DOWN, buff=0.12)

        self.play(FadeIn(dinding), Create(titik_nol), FadeIn(lbl_nol),
                  FadeIn(pegas), FadeIn(massa), run_time=0.8)
        ket_pegas = label_kecil("makin jauh theta dari nol, makin kuat ditarik balik",
                                PALET["redup"], 15)
        ket_pegas.move_to([0, -1.65, 0])
        self.play(FadeIn(ket_pegas, run_time=0.5))
        for tujuan in [0.7, 1.9, 0.35, 1.1, 0.55]:
            self.play(massa_x.animate.set_value(tujuan), run_time=0.45)
        self.wait(0.5)

        kartu_r = kartu_angka([
            (f"derajat {D_RIDGE}, tanpa denda", f"{TE_POLOS:.3e}"),
            (f"derajat {D_RIDGE}, lambda 0.1", f"{TE_RIDGE:.4f}"),
            ("norma theta tanpa denda", f"{NORMA_POLOS:.3e}"),
            ("norma theta dengan denda", f"{NORMA_RIDGE:.4f}"),
        ], ukuran=17, warna_nilai=PALET["hijau"]).move_to([0, -4.2, 0])
        self.play(FadeIn(kartu_r, shift=UP * 0.2, run_time=0.7))
        self.wait(1.8)

        tutup = Paragraph(
            "Model tidak dibuat lebih pintar.",
            "Ia cuma dilarang punya bobot raksasa,",
            "dan larangan itu bentuknya gaya pegas.",
            font=FONT_MONO, font_size=18, color=PALET["teks"],
            line_spacing=0.75, alignment="center",
        ).move_to([0, -6.5, 0])
        self.play(FadeIn(tutup, run_time=0.8))
        self.wait(1.8)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.9)
        self.wait(0.3)
