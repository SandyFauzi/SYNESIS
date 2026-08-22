"""Bab 1 - Menuruni Bukit. Isi Sesi A.

Pertanyaannya satu: bagaimana mesin menemukan garis terbaik tanpa pernah
diberi tahu garis yang benar.

Semua angka di layar dihitung ulang di berkas ini dengan generator dan seed
yang sama persis dengan notebooks/hari03_data_loss.py dan sesiA_gradient_descent.py,
jadi apa yang muncul di video adalah apa yang keluar dari terminalmu.

Render:
    S:\\Code\\manimations\\.venv\\Scripts\\python.exe -m manim -qh video\\bab1_menuruni.py Bab1
"""

import numpy as np

from sinema import (
    PALET, FONT_MONO, Y_PANGGUNG, PanelKode, judul, kaki, kartu_angka,
    label_kecil, merek, pencacah, siapkan, subjudul,
)

siapkan()

from manim import *  # noqa: E402

# ══════════════════════════════════════════════════════════════
# Data dan hitungan, sama persis dengan notebooks
# ══════════════════════════════════════════════════════════════

W_ASLI, B_ASLI = 3.0, 2.0


def buat_data(n=50, derau=1.5, seed=42):
    rng = np.random.default_rng(seed)
    x = rng.uniform(-5, 5, n)
    y = W_ASLI * x + B_ASLI + rng.normal(0, derau, n)
    return x, y


def mse(w, b, x, y):
    return float(np.mean((w * x + b - y) ** 2))


def gradien(w, b, x, y):
    n = len(x)
    r = (w * x + b) - y
    return (2.0 / n) * np.sum(r * x), (2.0 / n) * np.sum(r)


X, Y = buat_data()
N = len(X)

# lintasan gradient descent sungguhan, dari (0, 0)
LR, N_ITER = 0.02, 60
RIWAYAT = []
_w, _b = 0.0, 0.0
for _i in range(N_ITER):
    RIWAYAT.append((_i, _w, _b, mse(_w, _b, X, Y)))
    _dw, _db = gradien(_w, _b, X, Y)
    _w -= LR * _dw
    _b -= LR * _db

# jawaban tertutup sebagai pembanding
_A = np.column_stack([X, np.ones_like(X)])
(W_OPT, B_OPT), *_ = np.linalg.lstsq(_A, Y, rcond=None)
LOSS_OPT = mse(W_OPT, B_OPT, X, Y)

KODE = """
for i in range(n_iter):
    loss = mse(w, b, x, y)
    dw, db = gradien(w, b, x, y)
    w = w - lr * dw
    b = b - lr * db
"""


class Bab1(Scene):
    def construct(self):
        self.camera.background_color = PALET["latar"]

        # ---------- pembuka ----------
        jd = judul("Walking Downhill")
        sj = subjudul(["Session A  ·  how a machine finds the",
                       "best line without being told the answer"])
        mk, kk = merek(), kaki()

        self.play(FadeIn(mk, run_time=0.5), FadeIn(kk, run_time=0.5))
        self.play(Write(jd, run_time=1.1))
        self.play(FadeIn(sj, shift=UP * 0.15, run_time=0.7))
        self.wait(0.5)

        # ---------- panggung 1: data dan garis yang salah ----------
        sumbu = Axes(
            x_range=[-5.6, 5.6, 2], y_range=[-16, 20, 8],
            x_length=7.6, y_length=6.4,
            axis_config={"color": PALET["garis"], "stroke_width": 2.2,
                         "include_ticks": True, "tip_length": 0.16,
                         "font_size": 20},
        ).move_to([0, Y_PANGGUNG - 0.25, 0])

        titik = VGroup(*[
            Dot(sumbu.c2p(xi, yi), radius=0.052, color=PALET["biru"],
                fill_opacity=0.85)
            for xi, yi in zip(X, Y)
        ])

        ket_data = label_kecil(f"{N} measurements, noise and all",
                               PALET["redup"]).next_to(sumbu, DOWN, buff=0.22)

        self.play(Create(sumbu, run_time=0.9))
        self.play(LaggedStart(*[GrowFromCenter(d) for d in titik],
                              lag_ratio=0.012, run_time=1.3))
        self.play(FadeIn(ket_data, run_time=0.4))
        self.wait(0.4)

        # tebakan awal w = 0, b = 0
        w_t = ValueTracker(0.0)
        b_t = ValueTracker(0.0)

        garis = always_redraw(lambda: sumbu.plot(
            lambda t: w_t.get_value() * t + b_t.get_value(),
            x_range=[-5.4, 5.4], color=PALET["kuning"], stroke_width=4.5,
        ))

        def buat_sisa():
            g = VGroup()
            w, b = w_t.get_value(), b_t.get_value()
            for xi, yi in zip(X, Y):
                g.add(Line(sumbu.c2p(xi, yi), sumbu.c2p(xi, w * xi + b),
                           stroke_color=PALET["merah"], stroke_width=2.0,
                           stroke_opacity=0.55))
            return g

        sisa = always_redraw(buat_sisa)

        self.play(Create(garis, run_time=0.7))
        self.play(FadeIn(sisa, run_time=0.6))

        cacah = pencacah(f"loss = {RIWAYAT[0][3]:.2f}", PALET["merah"])
        self.play(FadeIn(cacah, run_time=0.4))
        self.wait(0.6)

        ket2 = label_kecil("A wrong line. Every red bar is one mistake.",
                           PALET["merah"], 16).next_to(sumbu, DOWN, buff=0.22)
        self.play(ReplacementTransform(ket_data, ket2), run_time=0.5)
        self.wait(0.8)

        # ---------- rumus loss ----------
        rms = MathTex(
            r"L(w,b)=\frac{1}{n}\sum_{i=1}^{n}\bigl(wx_i+b-y_i\bigr)^2",
            font_size=30, color=PALET["teks"],
        ).move_to([0, -4.30, 0])
        rms_ket = label_kecil("We square it so that missing high hurts "
                              "exactly as much as missing low",
                              PALET["redup"], 15)
        rms_ket.next_to(rms, DOWN, buff=0.22)

        self.play(Write(rms, run_time=1.2))
        self.play(FadeIn(rms_ket, run_time=0.5))
        self.wait(1.2)
        self.play(FadeOut(rms), FadeOut(rms_ket), run_time=0.5)

        # ---------- panggung 2: lanskap loss ----------
        self.play(
            FadeOut(sisa), FadeOut(titik), FadeOut(garis), FadeOut(sumbu),
            FadeOut(ket2), FadeOut(cacah), FadeOut(sj), run_time=0.7,
        )

        sj2 = subjudul(["Slice the landscape along one axis",
                        "and you always get a bowl"])
        self.play(FadeIn(sj2, run_time=0.5))

        ws = np.linspace(-1.2, 7.2, 240)
        Ls = np.array([mse(w, B_OPT, X, Y) for w in ws])

        sumbu2 = Axes(
            x_range=[-1.2, 7.2, 2], y_range=[0, float(Ls.max()) * 1.08, 20],
            x_length=7.2, y_length=6.0,
            axis_config={"color": PALET["garis"], "stroke_width": 2.2,
                         "tip_length": 0.16, "font_size": 20},
        ).move_to([0, Y_PANGGUNG - 0.15, 0])

        lbl_w = label_kecil("w", PALET["redup"], 20).next_to(sumbu2.x_axis, RIGHT, buff=0.12)
        lbl_L = label_kecil("L", PALET["redup"], 20).next_to(sumbu2.y_axis, UP, buff=0.12)

        kurva = sumbu2.plot(lambda w: mse(w, B_OPT, X, Y),
                            x_range=[-1.2, 7.2], color=PALET["ungu"],
                            stroke_width=4.0)

        self.play(Create(sumbu2, run_time=0.8), FadeIn(lbl_w), FadeIn(lbl_L))
        self.play(Create(kurva, run_time=1.1))

        # kelereng di w = 0
        wk = ValueTracker(0.0)
        kelereng = always_redraw(lambda: Dot(
            sumbu2.c2p(wk.get_value(), mse(wk.get_value(), B_OPT, X, Y)),
            radius=0.11, color=PALET["kuning"],
        ))
        aura = always_redraw(lambda: Dot(
            sumbu2.c2p(wk.get_value(), mse(wk.get_value(), B_OPT, X, Y)),
            radius=0.22, color=PALET["kuning"], fill_opacity=0.22,
        ))
        self.play(FadeIn(aura), FadeIn(kelereng), run_time=0.5)

        # garis singgung = gradien
        def buat_singgung():
            w = wk.get_value()
            L = mse(w, B_OPT, X, Y)
            g, _ = gradien(w, B_OPT, X, Y)
            dw = 1.5
            p1 = sumbu2.c2p(w - dw, L - g * dw)
            p2 = sumbu2.c2p(w + dw, L + g * dw)
            return Line(p1, p2, stroke_color=PALET["hijau"], stroke_width=3.4)

        singgung = always_redraw(buat_singgung)
        self.play(Create(singgung, run_time=0.7))

        g0, _ = gradien(0.0, B_OPT, X, Y)
        ket_g = label_kecil(f"slope here = {g0:.2f}, so downhill is to the right",
                            PALET["hijau"], 16)
        ket_g.next_to(sumbu2, DOWN, buff=0.24)
        self.play(FadeIn(ket_g, run_time=0.5))
        self.wait(1.0)

        rms2 = MathTex(r"w \leftarrow w - \eta\,\frac{\partial L}{\partial w}",
                       font_size=32, color=PALET["kuning"]).move_to([0, -4.45, 0])
        self.play(Write(rms2, run_time=0.9))
        self.wait(0.7)

        # tiga langkah pelan supaya terlihat
        for tujuan in [1.1, 2.0, 2.6]:
            self.play(wk.animate.set_value(tujuan), run_time=0.55)
            self.wait(0.12)
        self.play(wk.animate.set_value(float(W_OPT)), run_time=0.7)
        self.wait(0.5)

        self.play(FadeOut(singgung), FadeOut(ket_g), FadeOut(rms2), run_time=0.5)

        # ---------- panggung 3: loop yang sebenarnya ----------
        self.play(FadeOut(sumbu2), FadeOut(kurva), FadeOut(kelereng),
                  FadeOut(aura), FadeOut(lbl_w), FadeOut(lbl_L),
                  FadeOut(sj2), run_time=0.6)

        sj3 = subjudul(["These four lines train almost",
                        "every model in the world"])
        self.play(FadeIn(sj3, run_time=0.5))

        sumbu3 = Axes(
            x_range=[-5.6, 5.6, 2], y_range=[-16, 20, 8],
            x_length=7.2, y_length=5.0,
            axis_config={"color": PALET["garis"], "stroke_width": 2.0,
                         "tip_length": 0.14, "font_size": 18},
        ).move_to([0, 1.15, 0])

        titik3 = VGroup(*[
            Dot(sumbu3.c2p(xi, yi), radius=0.045, color=PALET["biru"],
                fill_opacity=0.75)
            for xi, yi in zip(X, Y)
        ])

        w_t.set_value(0.0)
        b_t.set_value(0.0)
        garis3 = always_redraw(lambda: sumbu3.plot(
            lambda t: w_t.get_value() * t + b_t.get_value(),
            x_range=[-5.4, 5.4], color=PALET["kuning"], stroke_width=4.2,
        ))

        pk = PanelKode(KODE, keterangan="notebooks/sesiA_gradient_descent.py")

        self.play(Create(sumbu3, run_time=0.6),
                  LaggedStart(*[GrowFromCenter(d) for d in titik3],
                              lag_ratio=0.008, run_time=0.8))
        self.play(Create(garis3, run_time=0.5))
        self.play(FadeIn(pk, shift=UP * 0.2, run_time=0.7))

        cacah3 = pencacah("iteration 0 / 60   loss 100.00")
        self.play(FadeIn(cacah3, run_time=0.4))

        # satu putaran pelan, memperlihatkan tiap baris
        for baris, jeda in [(0, 0.30), (1, 0.45), (2, 0.45), (3, 0.40), (4, 0.40)]:
            self.play(pk.sorot(baris))
            self.wait(jeda)

        i1, w1, b1, l1 = RIWAYAT[1]
        self.play(w_t.animate.set_value(w1), b_t.animate.set_value(b1),
                  run_time=0.5)

        # sisanya berjalan cepat
        langkah = [2, 3, 5, 7, 10, 14, 18, 23, 29, 36, 44, 52, 59]
        for k in langkah:
            i, w, b, L = RIWAYAT[k]
            baru = pencacah(f"iteration {i} / {N_ITER}   loss {L:.2f}")
            self.play(
                w_t.animate.set_value(w), b_t.animate.set_value(b),
                Transform(cacah3, baru),
                pk.sorot(3 if k % 2 else 4),
                run_time=0.24,
            )

        self.play(pk.padam(), run_time=0.3)
        self.wait(0.5)

        # ---------- penutup: angka ----------
        self.play(FadeOut(pk), FadeOut(sj3), run_time=0.5)

        w_akhir, b_akhir = RIWAYAT[-1][1], RIWAYAT[-1][2]
        kartu = kartu_angka([
            ("w the machine found", f"{w_akhir:.6f}"),
            ("b the machine found", f"{b_akhir:.6f}"),
            ("w actually used", f"{W_ASLI:.6f}"),
            ("b actually used", f"{B_ASLI:.6f}"),
            ("gap to exact solution", f"{abs(w_akhir - W_OPT):.2e}"),
        ], warna_nilai=PALET["hijau"]).move_to([0, -3.9, 0])

        self.play(FadeIn(kartu, shift=UP * 0.2, run_time=0.7))
        self.wait(1.2)

        tutup = Paragraph(
            "Nobody handed the machine the answer.",
            "It measured how wrong it was, took one step",
            "downhill, and did that sixty times.",
            font=FONT_MONO, font_size=19, color=PALET["teks"],
            line_spacing=0.75, alignment="center",
        ).move_to([0, -6.45, 0])
        self.play(FadeIn(tutup, run_time=0.8))
        self.wait(1.6)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.9)
        self.wait(0.3)
