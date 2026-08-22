"""Bulan 1 Bab 4 - Pegas, Gesekan, dan Adam. Isi Sesi 4.

Pertanyaannya: kenapa penurunan gradien polos kepayahan di lembah sempit,
dan kenapa obatnya persis osilator teredam dari Fisika Dasar.

Sambungannya ke Sesi D: lupa zero_() menghasilkan

    th[k+1] - 2 th[k] + th[k-1] = -lr g(th[k])

yaitu m a = F tanpa gesekan. Momentum adalah persamaan yang sama dengan
gesekan dipasang kembali, dan beta adalah koefisien redamannya.

Render:
    S:\\Code\\manimations\\.venv\\Scripts\\python.exe -m manim -ql --disable_caching -o b1bab4.mp4 b1_bab4_pegas.py B1Bab4
"""

import numpy as np

from sinema import (
    PALET, FONT_MONO, gambar_skala, judul, kaki, kartu_angka, label_kecil,
    merek, muat_data, pencacah, siapkan, subjudul,
)

siapkan()

from manim import *  # noqa: E402

NPZ, ANGKA = muat_data()

THETA_OPT = NPZ["opt_theta_opt"]
LAM_MIN = ANGKA["opt_lam_min"]
LAM_MAKS = ANGKA["opt_lam_maks"]
KONDISI = ANGKA["opt_kondisi"]
N_ITER = ANGKA["opt_n_iter"]

OPTIMIZER = [
    ("sgd", "SGD polos", PALET["merah"]),
    ("momentum", "momentum", PALET["kuning"]),
    ("rmsprop", "RMSprop", PALET["biru"]),
    ("adam", "Adam", PALET["hijau"]),
]

# vektor eigen dipakai untuk menggambar kontur eksak
_H = np.array([[LAM_MAKS, 0.0], [0.0, LAM_MIN]])


class B1Bab4(Scene):
    def construct(self):
        self.camera.background_color = PALET["latar"]

        jd = judul("Pegas dan Gesekan", 32)
        sj = subjudul(["Bulan 1 Sesi 4  ·  kenapa optimizer modern",
                       "semuanya osilator teredam"])
        mk, kk = merek(), kaki()

        self.play(FadeIn(mk, run_time=0.5), FadeIn(kk, run_time=0.5))
        self.play(Write(jd, run_time=1.0))
        self.play(FadeIn(sj, shift=UP * 0.15, run_time=0.6))
        self.wait(0.3)

        # ---------- sambungan ke Sesi D ----------
        r1 = MathTex(r"\theta_{k+1}-2\theta_k+\theta_{k-1}=-\eta\,g(\theta_k)",
                     font_size=27, color=PALET["teks"]).move_to([0, 3.65, 0])
        if r1.width > 8.2:
            r1.scale_to_fit_width(8.2)
        r1k = label_kecil("yang kamu temukan waktu lupa zero_()", PALET["redup"], 15)
        r1k.next_to(r1, DOWN, buff=0.20)

        self.play(Write(r1, run_time=1.2), FadeIn(r1k, run_time=0.5))
        self.wait(1.0)

        r2 = MathTex(r"m\,a = F", font_size=44, color=PALET["kuning"])
        r2.move_to([0, 2.15, 0])
        r2k = label_kecil("hukum Newton, tanpa gesekan", PALET["kuning"], 15)
        r2k.next_to(r2, DOWN, buff=0.18)
        self.play(Write(r2, run_time=0.8), FadeIn(r2k, run_time=0.4))
        self.wait(1.2)

        r3 = MathTex(r"v_{k+1}=\beta v_k-\eta\,g(\theta_k)",
                     font_size=28, color=PALET["hijau"]).move_to([0, 0.75, 0])
        r3b = MathTex(r"\theta_{k+1}=\theta_k+v_{k+1}",
                      font_size=28, color=PALET["hijau"]).move_to([0, 0.05, 0])
        r3k = label_kecil("momentum: persamaan yang sama, gesekan dipasang lagi",
                          PALET["hijau"], 15)
        r3k.next_to(r3b, DOWN, buff=0.20)
        self.play(Write(r3, run_time=0.8), Write(r3b, run_time=0.8))
        self.play(FadeIn(r3k, run_time=0.5))
        self.wait(1.0)

        skala = VGroup(
            Text("beta = 0", font=FONT_MONO, font_size=16, color=PALET["redup"]),
            Text("penurunan gradien biasa", font=FONT_MONO, font_size=14,
                 color=PALET["redup"]),
            Text("beta = 1", font=FONT_MONO, font_size=16, color=PALET["merah"]),
            Text("osilator tak teredam, bug zero_()", font=FONT_MONO,
                 font_size=14, color=PALET["merah"]),
        )
        skala[0].move_to([-2.15, -1.25, 0])
        skala[1].move_to([-2.15, -1.65, 0])
        skala[2].move_to([2.15, -1.25, 0])
        skala[3].move_to([2.15, -1.65, 0])
        batang = Line([-3.5, -0.75, 0], [3.5, -0.75, 0],
                      stroke_color=PALET["garis"], stroke_width=3)
        penanda = Dot([0.6, -0.75, 0], radius=0.09, color=PALET["kuning"])
        plabel = label_kecil("beta = 0.9, tempat hampir semua orang berada",
                             PALET["kuning"], 14)
        plabel.next_to(penanda, UP, buff=0.16)

        self.play(Create(batang, run_time=0.6), FadeIn(skala, run_time=0.7))
        self.play(FadeIn(penanda, scale=0.6, run_time=0.5),
                  FadeIn(plabel, run_time=0.5))
        self.wait(1.8)

        self.play(FadeOut(r1), FadeOut(r1k), FadeOut(r2), FadeOut(r2k),
                  FadeOut(r3), FadeOut(r3b), FadeOut(r3k), FadeOut(skala),
                  FadeOut(batang), FadeOut(penanda), FadeOut(plabel),
                  FadeOut(sj), run_time=0.7)

        # ---------- lembah sempit ----------
        sj2 = subjudul([f"lembah dengan bilangan kondisi {KONDISI:.0f}.",
                        "curam ke satu arah, hampir datar ke arah lain"])
        self.play(FadeIn(sj2, run_time=0.5))

        wo, bo = float(THETA_OPT[0]), float(THETA_OPT[1])
        sumbu = Axes(
            x_range=[-0.4, 3.6, 1], y_range=[-1.2, 4.2, 1],
            x_length=6.6, y_length=5.6,
            axis_config={"color": PALET["garis"], "stroke_width": 1.8,
                         "tip_length": 0.12, "font_size": 16},
        ).move_to([0, 0.95, 0])

        peta = gambar_skala(NPZ["opt_peta"], PALET["ungu"], PALET["latar"],
                            tinggi=sumbu.y_length, halus=True)
        peta.stretch_to_fit_width(sumbu.x_length)
        peta.move_to(sumbu.get_center())
        peta.set_opacity(0.55)
        tanda = Dot(sumbu.c2p(wo, bo), radius=0.075, color=PALET["hijau"])

        self.play(Create(sumbu, run_time=0.6))
        self.add(peta)
        self.bring_to_back(peta)
        self.play(FadeIn(peta, run_time=1.0))
        self.play(FadeIn(tanda, run_time=0.4))

        ket = label_kecil("ungu terang = dasar lembah. ngarainya nyaris "
                          "sempit tak terlihat.", PALET["redup"], 14)
        ket.next_to(sumbu, DOWN, buff=0.20)
        self.play(FadeIn(ket, run_time=0.5))
        self.wait(1.2)

        # ---------- empat lintasan ----------
        sj3 = subjudul(["empat cara melangkah,",
                        "masing-masing dengan lr terbaiknya sendiri"])
        self.play(FadeOut(sj2), FadeIn(sj3), run_time=0.5)

        terakhir = None
        for kunci, nama, warna in OPTIMIZER:
            j = NPZ[f"opt_{kunci}"]
            p = [sumbu.c2p(float(np.clip(a, -0.35, 3.55)),
                           float(np.clip(b, -1.15, 4.15))) for a, b in j]
            kurva = VMobject(stroke_color=warna, stroke_width=3.2)
            kurva.set_points_as_corners(p)

            it = ANGKA[f"opt_{kunci}_iterasi"]
            jarak = ANGKA[f"opt_{kunci}_jarak_akhir"]
            teks_it = "tidak sampai" if it < 0 else f"iterasi {it}"
            cacah = pencacah(f"{nama}   {teks_it}", warna, 20)

            if terakhir is None:
                self.play(FadeIn(cacah, run_time=0.3))
            else:
                self.play(FadeOut(terakhir[0]), ReplacementTransform(
                    terakhir[1], cacah), run_time=0.45)
            self.play(Create(kurva, run_time=1.7))
            self.wait(0.7)
            terakhir = (kurva, cacah)

        self.play(FadeOut(terakhir[0]), FadeOut(terakhir[1]), run_time=0.4)

        # ---------- angka ----------
        pasangan = []
        for kunci, nama, _ in OPTIMIZER:
            it = ANGKA[f"opt_{kunci}_iterasi"]
            pasangan.append((nama, "tidak sampai" if it < 0 else f"iterasi {it}"))
        kartu = kartu_angka(pasangan, ukuran=18,
                            warna_nilai=PALET["hijau"]).move_to([0, -3.55, 0])
        ket_k = label_kecil(f"sampai 2 persen dari optimum, dalam {N_ITER} iterasi",
                            PALET["redup"], 15)
        ket_k.next_to(kartu, DOWN, buff=0.20)

        self.play(FadeIn(kartu, shift=UP * 0.2, run_time=0.7),
                  FadeIn(ket_k, run_time=0.5))
        self.wait(2.0)

        tutup = Paragraph(
            "SGD polos tidak pernah sampai, sekencang apa pun boleh melangkah.",
            "Bukan karena kurang pintar, tapi karena lembahnya lonjong.",
            "Sisanya cuma soal berapa banyak gesekan yang dipasang.",
            font=FONT_MONO, font_size=15, color=PALET["teks"],
            line_spacing=0.75, alignment="center",
        ).move_to([0, -5.75, 0])
        self.play(FadeIn(tutup, run_time=0.9))
        self.wait(2.2)

        akhir = Text("SYNESIS", font=FONT_MONO, weight=BOLD, font_size=40,
                     color=PALET["hijau"]).move_to([0, -6.85, 0])
        self.play(FadeIn(akhir, scale=0.9, run_time=0.8))
        self.wait(1.4)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.3)
