"""Bab 2 - Lanskap dan Langkah. Isi Sesi B.

Pertanyaannya: seberapa besar langkah yang boleh diambil, dan kenapa ada
batas yang bisa dihitung sebelum satu iterasi pun dijalankan.

Angka kuncinya dihitung di berkas ini:
    lambda_max = 15.723272,  batas lr = 2/lambda_max = 0.127200

Render:
    S:\\Code\\manimations\\.venv\\Scripts\\python.exe -m manim -qh video\\bab2_lanskap.py Bab2
"""

import numpy as np

from sinema import (
    PALET, FONT_MONO, judul, kaki, kartu_angka, label_kecil, merek,
    pencacah, siapkan, subjudul,
)

siapkan()

from manim import *  # noqa: E402

# ══════════════════════════════════════════════════════════════
# Model dan lanskap
# ══════════════════════════════════════════════════════════════

W_ASLI, B_ASLI = 3.0, 2.0
rng = np.random.default_rng(42)
X = rng.uniform(-5, 5, 50)
Y = W_ASLI * X + B_ASLI + rng.normal(0, 1.5, 50)
N = len(X)

A = np.column_stack([X, np.ones_like(X)])
H = (2.0 / N) * (A.T @ A)
NILAI_EIGEN, VEKTOR_EIGEN = np.linalg.eigh(H)
LAM_MIN, LAM_MAKS = float(NILAI_EIGEN[0]), float(NILAI_EIGEN[1])
LR_BATAS = 2.0 / LAM_MAKS
KONDISI = LAM_MAKS / LAM_MIN

THETA_OPT = np.linalg.lstsq(A, Y, rcond=None)[0]
W_OPT, B_OPT = float(THETA_OPT[0]), float(THETA_OPT[1])


def rugi(w, b):
    return float(np.mean((w * X + b - Y) ** 2))


L_MIN = rugi(W_OPT, B_OPT)


def gradien(w, b):
    r = (w * X + b) - Y
    return (2.0 / N) * np.sum(r * X), (2.0 / N) * np.sum(r)


def lintasan(lr, n=60, w0=0.0, b0=0.0):
    jalan, w, b = [], w0, b0
    for _ in range(n):
        jalan.append((w, b, rugi(w, b)))
        dw, db = gradien(w, b)
        w -= lr * dw
        b -= lr * db
        if not np.isfinite(w) or abs(w) > 1e4:
            break
    return jalan


REZIM = [
    (0.15, "terlalu kecil", PALET["biru"]),
    (0.60, "pas", PALET["hijau"]),
    (0.95, "berayun, tapi sampai", PALET["kuning"]),
    (1.00, "tepat di batas", PALET["jingga"]),
    (1.02, "lewat batas", PALET["merah"]),
]

KODE = """
w = w - lr * dw
b = b - lr * db
"""


class Bab2(ThreeDScene):
    def construct(self):
        self.camera.background_color = PALET["latar"]

        jd = judul("Lanskap dan Langkah", 36)
        sj = subjudul(["Sesi B  ·  ada batas langkah yang bisa",
                       "dihitung sebelum training dimulai"])
        mk, kk = merek(), kaki()
        self.add_fixed_in_frame_mobjects(jd, sj, mk, kk)
        self.remove(jd, sj, mk, kk)

        self.play(FadeIn(mk, run_time=0.5), FadeIn(kk, run_time=0.5))
        self.play(Write(jd, run_time=1.0))
        self.play(FadeIn(sj, shift=UP * 0.15, run_time=0.6))

        # ---------- mangkuk tiga dimensi ----------
        sumbu3d = ThreeDAxes(
            x_range=[-1.0, 7.0, 2], y_range=[-2.0, 5.5, 2], z_range=[0, 90, 30],
            x_length=5.6, y_length=5.25, z_length=3.4,
            axis_config={"color": PALET["garis"], "stroke_width": 2.0,
                         "tip_length": 0.14},
        )

        def permukaan_titik(u, v):
            return sumbu3d.c2p(u, v, min(rugi(u, v), 90.0))

        mangkuk = Surface(
            permukaan_titik, u_range=[-1.0, 7.0], v_range=[-2.0, 5.5],
            resolution=(28, 28), fill_opacity=0.72, stroke_width=0.6,
            stroke_color=PALET["garis"],
        )
        mangkuk.set_fill_by_value(
            axes=sumbu3d,
            colorscale=[(ManimColor(PALET["hijau"]), 0),
                        (ManimColor(PALET["kuning"]), 35),
                        (ManimColor(PALET["merah"]), 90)],
            axis=2,
        )

        self.set_camera_orientation(phi=66 * DEGREES, theta=-52 * DEGREES,
                                    zoom=0.95)
        self.play(Create(sumbu3d, run_time=1.0))
        self.play(Create(mangkuk, run_time=2.0))

        lbl = label_kecil("sumbu datar: w dan b   ·   tinggi: seberapa salah",
                          PALET["redup"], 16)
        lbl.move_to([0, -3.55, 0])
        self.add_fixed_in_frame_mobjects(lbl)
        self.play(FadeIn(lbl, run_time=0.5))

        self.begin_ambient_camera_rotation(rate=0.10)
        self.wait(2.0)

        # kelereng menuruni permukaan, lr yang pas
        jalan = lintasan(0.60 * LR_BATAS, n=45)
        titik3d = [sumbu3d.c2p(w, b, min(L, 90.0)) for w, b, L in jalan]

        bola = Dot3D(titik3d[0], radius=0.10, color=PALET["teks"])
        jejak = VMobject(stroke_color=PALET["teks"], stroke_width=4.0)
        jejak.set_points_as_corners([titik3d[0], titik3d[0]])
        self.play(FadeIn(bola, run_time=0.4))

        cacah = pencacah(f"loss {jalan[0][2]:.1f}")
        self.add_fixed_in_frame_mobjects(cacah)
        self.play(FadeIn(cacah, run_time=0.3))

        self.add(jejak)
        for k in range(1, len(titik3d)):
            baru = pencacah(f"loss {jalan[k][2]:.1f}")
            self.play(
                bola.animate.move_to(titik3d[k]),
                UpdateFromFunc(jejak, lambda m, k=k: m.set_points_as_corners(
                    titik3d[:k + 1])),
                Transform(cacah, baru),
                run_time=0.10 if k > 6 else 0.22,
            )
        self.stop_ambient_camera_rotation()
        self.wait(0.6)

        # ---------- naik ke atas: mangkuk jadi peta kontur ----------
        sj2 = subjudul(["dilihat dari atas, mangkuknya",
                        "jadi peta kontur"])
        self.add_fixed_in_frame_mobjects(sj2)
        self.remove(sj2)

        self.play(FadeOut(lbl), FadeOut(cacah), run_time=0.4)
        self.move_camera(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=1.05,
                         run_time=2.4)
        self.play(FadeOut(sj), FadeIn(sj2), run_time=0.5)
        self.play(FadeOut(mangkuk), FadeOut(sumbu3d.z_axis), run_time=0.7)

        # kontur eksak, karena lanskapnya benar-benar kuadratik
        def elips(taraf):
            titik = []
            for t in np.linspace(0, TAU, 90):
                z = np.array([np.cos(t) * np.sqrt(2 * taraf / LAM_MIN),
                              np.sin(t) * np.sqrt(2 * taraf / LAM_MAKS)])
                p = THETA_OPT + VEKTOR_EIGEN @ z
                titik.append(sumbu3d.c2p(p[0], p[1], 0.0))
            k = VMobject(stroke_color=PALET["ungu"], stroke_width=2.2,
                         stroke_opacity=0.75)
            k.set_points_as_corners(titik + [titik[0]])
            return k

        kontur = VGroup(*[elips(c) for c in [0.5, 1.5, 3.0, 5.5, 8.5, 12.5]])
        self.play(FadeOut(bola), FadeOut(jejak), run_time=0.4)
        self.play(LaggedStart(*[Create(k) for k in kontur],
                              lag_ratio=0.15, run_time=1.8))

        tanda = Dot(sumbu3d.c2p(W_OPT, B_OPT, 0.0), radius=0.09,
                    color=PALET["hijau"])
        self.play(FadeIn(tanda, run_time=0.4))
        self.wait(0.8)

        # ---------- lima nilai lr ----------
        sj3 = subjudul(["langkah yang sama, lima ukuran.",
                        "hanya satu yang salah arah"])
        self.add_fixed_in_frame_mobjects(sj3)
        self.remove(sj3)
        self.play(FadeOut(sj2), FadeIn(sj3), run_time=0.5)

        kartu_batas = kartu_angka([
            ("lambda maks Hessian", f"{LAM_MAKS:.4f}"),
            ("batas aman  2/lambda", f"{LR_BATAS:.6f}"),
        ], warna_nilai=PALET["kuning"]).move_to([0, -5.15, 0])
        self.add_fixed_in_frame_mobjects(kartu_batas)
        self.play(FadeIn(kartu_batas, run_time=0.6))

        garis_terakhir = None
        untuk_dihapus = []
        for faktor, nama, warna in REZIM:
            lr = faktor * LR_BATAS
            jln = lintasan(lr, n=60)
            titik2d = [sumbu3d.c2p(np.clip(w, -0.95, 6.95),
                                   np.clip(b, -1.95, 5.45), 0.0)
                       for w, b, _ in jln]

            kurva = VMobject(stroke_color=warna, stroke_width=3.4)
            kurva.set_points_as_corners(titik2d)
            simpul = VGroup(*[Dot(p, radius=0.045, color=warna)
                              for p in titik2d[:26]])

            keterangan = pencacah(
                f"lr = {lr:.4f}   {nama}", warna, 21)
            self.add_fixed_in_frame_mobjects(keterangan)
            self.remove(keterangan)

            if garis_terakhir is None:
                self.play(FadeIn(keterangan, run_time=0.3))
            else:
                self.play(FadeOut(garis_terakhir[0]), FadeOut(garis_terakhir[1]),
                          ReplacementTransform(garis_terakhir[2], keterangan),
                          run_time=0.4)
            self.play(Create(kurva, run_time=1.5),
                      LaggedStart(*[GrowFromCenter(d) for d in simpul],
                                  lag_ratio=0.04, run_time=1.5))
            self.wait(0.7)
            garis_terakhir = (kurva, simpul, keterangan)
            untuk_dihapus.append(keterangan)

        self.wait(0.5)
        self.play(FadeOut(garis_terakhir[0]), FadeOut(garis_terakhir[1]),
                  FadeOut(garis_terakhir[2]), FadeOut(kartu_batas), run_time=0.5)

        # ---------- angka penutup ----------
        sj4 = subjudul(["ambangnya bukan tebakan.",
                        "ia keluar dari nilai eigen Hessian"])
        self.add_fixed_in_frame_mobjects(sj4)
        self.remove(sj4)
        self.play(FadeOut(sj3), FadeIn(sj4), run_time=0.5)

        rms = MathTex(r"\eta < \frac{2}{\lambda_{\max}}",
                      font_size=46, color=PALET["kuning"])
        rms.move_to([0, -3.05, 0])
        self.add_fixed_in_frame_mobjects(rms)
        self.remove(rms)
        self.play(Write(rms, run_time=1.0))

        hasil = []
        for faktor, nama, _ in REZIM:
            jln = lintasan(faktor * LR_BATAS, n=60)
            hasil.append((f"lr = {faktor:.2f} x batas", f"{jln[-1][2]:.2f}"))
        kartu2 = kartu_angka(hasil, ukuran=18,
                             warna_nilai=PALET["teks"]).move_to([0, -5.55, 0])
        self.add_fixed_in_frame_mobjects(kartu2)
        self.remove(kartu2)
        self.play(FadeIn(kartu2, shift=UP * 0.2, run_time=0.7))
        self.wait(1.4)

        tutup = Paragraph(
            "Di batasnya tepat, ia berayun selamanya:",
            "tidak menurun, tidak meledak.",
            "Osilator tak teredam, di dalam kodemu.",
            font=FONT_MONO, font_size=18, color=PALET["teks"],
            line_spacing=0.75, alignment="center",
        ).move_to([0, -7.05, 0])
        self.add_fixed_in_frame_mobjects(tutup)
        self.remove(tutup)
        self.play(FadeIn(tutup, run_time=0.8))
        self.wait(1.8)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.9)
        self.wait(0.3)
