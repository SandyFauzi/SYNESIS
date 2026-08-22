"""Bulan 1 Bab 1 - Garis Lurus Tidak Cukup. Isi Sesi 2.

Pertanyaannya: apa sebenarnya yang bertambah ketika satu lapisan tersembunyi
dipasang, dan kenapa satu tekukan sudah mengubah segalanya.

Angkanya dibaca dari video/data/bulan1.npz, hasil siapkan_data_bulan1.py.

Render:
    S:\\Code\\manimations\\.venv\\Scripts\\python.exe -m manim -ql --disable_caching -o b1bab1.mp4 b1_bab1_garis.py B1Bab1
"""

import numpy as np

from sinema import (
    PALET, FONT_MONO, Y_PANGGUNG, gambar_skala, judul, kaki, kartu_angka,
    label_kecil, merek, muat_data, pencacah, siapkan, subjudul,
)

siapkan()

from manim import *  # noqa: E402

NPZ, ANGKA = muat_data()
XM, YM = NPZ["moon_X"], NPZ["moon_y"]
GX, GY = NPZ["moon_gx"], NPZ["moon_gy"]
PETA_LIN, PETA_MLP = NPZ["moon_peta_lin"], NPZ["moon_peta_mlp"]
LIPAT = NPZ["moon_lipat"]
RUGI = NPZ["moon_rugi"]

AK_LIN = ANGKA["moon_akurasi_lin"]
AK_MLP = ANGKA["moon_akurasi_mlp"]
N_SEMBUNYI = ANGKA["moon_n_sembunyi"]
SEBARAN = ANGKA["moon_rugi_sebaran"]
AK_SURVEI = ANGKA["moon_akurasi_survei"]
MATI = ANGKA["moon_mati_survei"]


class B1Bab1(Scene):
    def construct(self):
        self.camera.background_color = PALET["latar"]

        jd = judul("A Line Is Not Enough", 30)
        sj = subjudul(["Month 1 Session 2  ·  what you gain",
                       "by adding one hidden layer"])
        mk, kk = merek(), kaki()

        self.play(FadeIn(mk, run_time=0.5), FadeIn(kk, run_time=0.5))
        self.play(Write(jd, run_time=1.0))
        self.play(FadeIn(sj, shift=UP * 0.15, run_time=0.6))

        # ---------- data yang saling mengunci ----------
        sumbu = Axes(
            x_range=[-2.0, 3.0, 1], y_range=[-1.6, 2.0, 1],
            x_length=7.0, y_length=5.05,
            axis_config={"color": PALET["garis"], "stroke_width": 1.8,
                         "tip_length": 0.12, "font_size": 16},
        ).move_to([0, Y_PANGGUNG + 0.55, 0])

        def titik_kelas(k, warna):
            return VGroup(*[
                Dot(sumbu.c2p(a, b), radius=0.048, color=warna,
                    fill_opacity=0.9)
                for (a, b), c in zip(XM, YM) if int(c) == k
            ])

        merah = titik_kelas(0, PALET["jingga"])
        biru = titik_kelas(1, PALET["biru"])

        self.play(Create(sumbu, run_time=0.7))
        self.play(LaggedStart(*[GrowFromCenter(d) for d in merah],
                              lag_ratio=0.006, run_time=0.9),
                  LaggedStart(*[GrowFromCenter(d) for d in biru],
                              lag_ratio=0.006, run_time=0.9))
        ket = label_kecil("two groups that interlock like fingers",
                          PALET["redup"], 16).next_to(sumbu, DOWN, buff=0.20)
        self.play(FadeIn(ket, run_time=0.4))
        self.wait(0.7)

        # ---------- garis lurus gagal ----------
        peta_l = gambar_skala(PETA_LIN, PALET["jingga"], PALET["biru"],
                              tinggi=sumbu.y_length)
        peta_l.stretch_to_fit_width(sumbu.x_length)
        peta_l.move_to(sumbu.get_center())
        peta_l.set_opacity(0.30)
        self.add(peta_l)
        self.bring_to_back(peta_l)
        self.play(FadeIn(peta_l, run_time=0.8))

        cacah = pencacah(f"one straight line   {AK_LIN * 100:.1f} percent correct",
                         PALET["jingga"], 19)
        self.play(FadeIn(cacah, run_time=0.4))
        ket2 = label_kecil("tilt it any way you like, some dots stay on the wrong side",
                           PALET["jingga"], 16).next_to(sumbu, DOWN, buff=0.20)
        self.play(ReplacementTransform(ket, ket2), run_time=0.5)
        self.wait(1.4)

        # ---------- pasang satu lapisan ----------
        sj2 = subjudul([f"Add {N_SEMBUNYI} ReLU neurons in the middle.",
                        "Each one contributes a single crease."])
        self.play(FadeOut(sj), FadeIn(sj2), run_time=0.5)

        garis_lipat = VGroup()
        for seg in LIPAT:
            (x1, y1), (x2, y2) = seg
            garis_lipat.add(Line(sumbu.c2p(x1, y1), sumbu.c2p(x2, y2),
                                 stroke_color=PALET["kuning"],
                                 stroke_width=2.0, stroke_opacity=0.65))
        self.play(FadeOut(peta_l), run_time=0.4)
        self.play(LaggedStart(*[Create(g) for g in garis_lipat],
                              lag_ratio=0.16, run_time=1.8))

        ket3 = label_kecil("each line marks where one neuron switches on or off",
                           PALET["kuning"], 15).next_to(sumbu, DOWN, buff=0.20)
        self.play(ReplacementTransform(ket2, ket3), run_time=0.5)
        self.wait(1.2)

        rumus = MathTex(r"\mathrm{relu}(w\cdot x + b)", font_size=32,
                        color=PALET["kuning"]).move_to([0, -3.55, 0])
        rket = label_kecil("one bend. Not a curve, just a single fold.",
                           PALET["redup"], 15)
        rket.next_to(rumus, DOWN, buff=0.20)
        self.play(Write(rumus, run_time=0.8), FadeIn(rket, run_time=0.5))
        self.wait(1.2)
        self.play(FadeOut(rumus), FadeOut(rket), run_time=0.4)

        # ---------- hasilnya ----------
        peta_m = gambar_skala(PETA_MLP, PALET["jingga"], PALET["biru"],
                              tinggi=sumbu.y_length)
        peta_m.stretch_to_fit_width(sumbu.x_length)
        peta_m.move_to(sumbu.get_center())
        peta_m.set_opacity(0.34)
        self.add(peta_m)
        self.bring_to_back(peta_m)

        cacah2 = pencacah(
            f"{N_SEMBUNYI} hidden neurons   {AK_MLP * 100:.1f} percent correct",
            PALET["hijau"], 19)
        self.play(FadeIn(peta_m, run_time=1.0),
                  garis_lipat.animate.set_stroke(opacity=0.22),
                  Transform(cacah, cacah2), run_time=1.0)

        ket4 = label_kecil("the boundary curves, because it is built from straight folds",
                           PALET["hijau"], 15).next_to(sumbu, DOWN, buff=0.20)
        self.play(ReplacementTransform(ket3, ket4), run_time=0.5)
        self.wait(1.6)

        kartu = kartu_angka([
            ("one straight line", f"{AK_LIN * 100:.2f} percent"),
            (f"{N_SEMBUNYI} ReLU neurons", f"{AK_MLP * 100:.2f} percent"),
        ], warna_nilai=PALET["hijau"]).move_to([0, -4.35, 0])
        self.play(FadeIn(kartu, shift=UP * 0.2, run_time=0.6))
        self.wait(1.5)

        # ---------- yang baru di Bulan 1 ----------
        self.play(FadeOut(peta_m), FadeOut(garis_lipat), FadeOut(merah),
                  FadeOut(biru), FadeOut(sumbu), FadeOut(ket4),
                  FadeOut(cacah), FadeOut(kartu), FadeOut(sj2), run_time=0.7)

        sj3 = subjudul(["The price: where you start now",
                        "decides where you end up"])
        self.play(FadeIn(sj3, run_time=0.5))

        sumbu2 = Axes(
            x_range=[0, 7, 1], y_range=[0.90, 1.005, 0.02],
            x_length=6.8, y_length=4.4,
            axis_config={"color": PALET["garis"], "stroke_width": 1.8,
                         "tip_length": 0.12, "font_size": 16},
        ).move_to([0, Y_PANGGUNG + 1.0, 0])

        batang = VGroup()
        terbaik = max(AK_SURVEI)
        for i, a in enumerate(AK_SURVEI):
            tinggi = (a - 0.90) / (1.005 - 0.90) * sumbu2.y_length
            w = PALET["ungu"] if a >= terbaik - 1e-9 else PALET["merah"]
            b = Rectangle(width=0.52, height=max(tinggi, 0.04),
                          fill_color=w, fill_opacity=0.85, stroke_width=0)
            b.move_to(sumbu2.c2p(i, 0.90), aligned_edge=DOWN)
            batang.add(b)

        lbl = label_kecil("accuracy from eight random starting points. "
                          "Same model, same data, every time.",
                          PALET["redup"], 13).next_to(sumbu2, DOWN, buff=0.20)
        self.play(Create(sumbu2, run_time=0.6))
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in batang],
                              lag_ratio=0.12, run_time=1.6), FadeIn(lbl))
        self.wait(1.0)

        n_gagal = sum(1 for a in AK_SURVEI if a < terbaik - 1e-9)
        kartu2 = kartu_angka([
            ("best run", f"{max(AK_SURVEI) * 100:.2f} percent"),
            ("worst run", f"{min(AK_SURVEI) * 100:.2f} percent"),
            ("runs that got stuck", f"{n_gagal} out of {len(AK_SURVEI)}"),
        ], ukuran=17, warna_nilai=PALET["ungu"]).move_to([0, -3.9, 0])
        self.play(FadeIn(kartu2, shift=UP * 0.2, run_time=0.6))
        self.wait(1.5)

        tutup = Paragraph(
            "In Month 0 there was one bowl, so every",
            "starting point reached the same bottom.",
            "From Month 1 on, that guarantee is gone.",
            font=FONT_MONO, font_size=16, color=PALET["teks"],
            line_spacing=0.75, alignment="center",
        ).move_to([0, -6.2, 0])
        self.play(FadeIn(tutup, run_time=0.8))
        self.wait(2.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.9)
        self.wait(0.3)
