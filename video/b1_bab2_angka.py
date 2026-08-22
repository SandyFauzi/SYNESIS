"""Bulan 1 Bab 2 - Sepuluh Kemungkinan. Isi Sesi 3.

Pertanyaannya: apa yang berubah ketika keluarannya bukan lagi satu angka,
tapi sepuluh kemungkinan yang harus berjumlah satu.

Datanya angka tulisan tangan 8x8 dari sklearn, bukan MNIST 28x28. Dipilih
karena tidak perlu diunduh dan karena 8x8 masih terbaca di layar telepon.
Bentuk soalnya sama persis, cuma lebih kecil.

Render:
    S:\\Code\\manimations\\.venv\\Scripts\\python.exe -m manim -ql --disable_caching -o b1bab2.mp4 b1_bab2_angka.py B1Bab2
"""

import numpy as np

from sinema import (
    PALET, FONT_MONO, gambar_skala, judul, kaki, kartu_angka, label_kecil,
    merek, muat_data, pencacah, siapkan, subjudul,
)

siapkan()

from manim import *  # noqa: E402

NPZ, ANGKA = muat_data()
CONTOH = NPZ["angka_contoh"]
LABEL = NPZ["angka_label"]
RAMAL = NPZ["angka_ramal"]
RUGI = NPZ["angka_rugi"]
BOBOT1 = NPZ["angka_bobot1"]

AK_TR = ANGKA["angka_akurasi_tr"]
AK_TE = ANGKA["angka_akurasi_te"]
N_TR = ANGKA["angka_n_latih"]
N_TE = ANGKA["angka_n_uji"]
N_PIKSEL = ANGKA["angka_piksel"]
N_PARAM = ANGKA["angka_parameter"]


class B1Bab2(Scene):
    def construct(self):
        self.camera.background_color = PALET["latar"]

        jd = judul("Ten Possible Answers", 30)
        sj = subjudul(["Month 1 Session 3  ·  the output stops being",
                       "one number and becomes ten possibilities"])
        mk, kk = merek(), kaki()

        self.play(FadeIn(mk, run_time=0.5), FadeIn(kk, run_time=0.5))
        self.play(Write(jd, run_time=1.0))
        self.play(FadeIn(sj, shift=UP * 0.15, run_time=0.6))

        # ---------- satu gambar adalah 64 angka ----------
        satu = gambar_skala(CONTOH[3], PALET["latar"], PALET["teks"],
                            tinggi=3.0)
        satu.move_to([-1.85, 2.55, 0])
        bingkai = SurroundingRectangle(satu, color=PALET["garis"],
                                       stroke_width=1.6, buff=0.0)

        kisi_teks = VGroup()
        for i in range(8):
            baris = " ".join(f"{int(v * 16):2d}" for v in CONTOH[3][i])
            kisi_teks.add(Text(baris, font=FONT_MONO, font_size=13,
                               color=PALET["redup"]))
        kisi_teks.arrange(DOWN, buff=0.09).move_to([1.95, 2.55, 0])

        self.play(FadeIn(satu, run_time=0.7), Create(bingkai, run_time=0.5))
        self.play(FadeIn(kisi_teks, run_time=0.8))

        panah_k = Arrow(satu.get_right(), kisi_teks.get_left(), buff=0.18,
                        stroke_width=2.6, color=PALET["garis"],
                        max_tip_length_to_length_ratio=0.18)
        self.play(Create(panah_k, run_time=0.4))

        ket = label_kecil(f"one image is {N_PIKSEL} numbers. Nothing more.",
                          PALET["redup"], 16).move_to([0, 0.75, 0])
        self.play(FadeIn(ket, run_time=0.5))
        self.wait(1.4)

        # ---------- softmax ----------
        r1 = MathTex(r"p_k=\frac{e^{z_k}}{\sum_j e^{z_j}}",
                     font_size=34, color=PALET["kuning"]).move_to([0, -0.55, 0])
        r1k = label_kecil("ten outputs forced to be positive and to add up to one",
                          PALET["redup"], 15)
        r1k.next_to(r1, DOWN, buff=0.22)
        self.play(Write(r1, run_time=1.0), FadeIn(r1k, run_time=0.5))
        self.wait(1.2)

        r2 = MathTex(r"\frac{\partial L}{\partial z} = p - y",
                     font_size=38, color=PALET["hijau"]).move_to([0, -2.35, 0])
        r2k = label_kecil("pair it with cross entropy and the slope comes out this clean",
                          PALET["hijau"], 15)
        r2k.next_to(r2, DOWN, buff=0.22)
        self.play(Write(r2, run_time=0.9), FadeIn(r2k, run_time=0.5))
        self.wait(0.8)

        r2j = label_kecil("guess minus truth. That is the entire gradient.",
                          PALET["redup"], 15)
        r2j.next_to(r2k, DOWN, buff=0.18)
        self.play(FadeIn(r2j, run_time=0.5))
        self.wait(1.6)

        self.play(FadeOut(satu), FadeOut(bingkai), FadeOut(kisi_teks),
                  FadeOut(panah_k), FadeOut(ket), FadeOut(r1), FadeOut(r1k),
                  FadeOut(r2), FadeOut(r2k), FadeOut(r2j), run_time=0.7)

        # ---------- sepuluh angka, dan tebakannya ----------
        sj2 = subjudul([f"{N_TR} images to study from,",
                        f"{N_TE} locked away and never shown"])
        self.play(FadeOut(sj), FadeIn(sj2), run_time=0.5)

        petak = Group()
        for i in range(10):
            g = gambar_skala(CONTOH[i], PALET["latar"], PALET["teks"],
                             tinggi=1.28)
            bk = SurroundingRectangle(
                g, buff=0.0, stroke_width=1.6,
                color=PALET["hijau"] if RAMAL[i] == LABEL[i] else PALET["merah"])
            tk = Text(f"{int(RAMAL[i])}", font=FONT_MONO, weight=BOLD,
                      font_size=19,
                      color=PALET["hijau"] if RAMAL[i] == LABEL[i]
                      else PALET["merah"])
            tk.next_to(bk, DOWN, buff=0.10)
            petak.add(Group(g, bk, tk))
        petak.arrange_in_grid(rows=4, cols=3, buff=(0.42, 0.40))
        petak.move_to([0, 1.55, 0])

        self.play(LaggedStart(*[FadeIn(p, scale=0.85) for p in petak],
                              lag_ratio=0.09, run_time=2.0))
        ket2 = label_kecil("the digit under each tile is the machine guess",
                           PALET["redup"], 15).next_to(petak, DOWN, buff=0.24)
        self.play(FadeIn(ket2, run_time=0.5))
        self.wait(1.4)

        kartu = kartu_angka([
            ("on images it studied", f"{AK_TR * 100:.2f} percent"),
            ("on images it never saw", f"{AK_TE * 100:.2f} percent"),
            ("knobs it tuned", f"{N_PARAM:,}"),
        ], ukuran=18, warna_nilai=PALET["hijau"]).move_to([0, -4.35, 0])
        self.play(FadeIn(kartu, shift=UP * 0.2, run_time=0.7))
        self.wait(1.6)

        # ---------- apa yang dipelajari lapisan pertama ----------
        self.play(FadeOut(petak), FadeOut(ket2), FadeOut(kartu),
                  FadeOut(sj2), run_time=0.6)

        sj3 = subjudul(["What the first layer learned",
                        "can be looked at directly"])
        self.play(FadeIn(sj3, run_time=0.5))

        b = BOBOT1
        b = (b - b.min()) / (b.max() - b.min() + 1e-12)
        filter_petak = Group()
        for i in range(8):
            g = gambar_skala(b[i], PALET["jingga"], PALET["biru"], tinggi=1.55)
            bk = SurroundingRectangle(g, buff=0.0, stroke_width=1.4,
                                      color=PALET["garis"])
            filter_petak.add(Group(g, bk))
        filter_petak.arrange_in_grid(rows=2, cols=4, buff=(0.36, 0.36))
        filter_petak.move_to([0, 1.85, 0])

        self.play(LaggedStart(*[FadeIn(f, scale=0.85) for f in filter_petak],
                              lag_ratio=0.10, run_time=1.6))
        ket3 = label_kecil("eight of 32 neurons. Blue hunts for ink, "
                           "orange votes against it.", PALET["redup"], 14)
        ket3.next_to(filter_petak, DOWN, buff=0.26)
        self.play(FadeIn(ket3, run_time=0.5))
        self.wait(1.8)

        # ---------- kurva rugi ----------
        sumbu = Axes(
            x_range=[0, len(RUGI), 60], y_range=[0, float(RUGI.max()) * 1.05, 1],
            x_length=6.8, y_length=3.0,
            axis_config={"color": PALET["garis"], "stroke_width": 1.8,
                         "tip_length": 0.12, "font_size": 16},
        ).move_to([0, -2.55, 0])
        kurva = VMobject(stroke_color=PALET["hijau"], stroke_width=3.4)
        kurva.set_points_as_corners(
            [sumbu.c2p(i, float(v)) for i, v in enumerate(RUGI)])
        lbl = label_kecil("cross entropy during training", PALET["redup"], 15)
        lbl.next_to(sumbu, DOWN, buff=0.18)

        self.play(Create(sumbu, run_time=0.6))
        self.play(Create(kurva, run_time=1.4), FadeIn(lbl, run_time=0.5))
        self.wait(1.2)

        tutup = Paragraph(
            "Not one rule about the shape of a digit",
            "was written into this program by a human.",
            "It all came from walking downhill, over and over.",
            font=FONT_MONO, font_size=16, color=PALET["teks"],
            line_spacing=0.75, alignment="center",
        ).move_to([0, -5.6, 0])
        self.play(FadeIn(tutup, run_time=0.9))
        self.wait(2.2)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.9)
        self.wait(0.3)
