"""Bulan 1 Bab 3 - Dinding yang Menunggu.

Mesin autograd buatan sendiri benar, dan itu sudah dibuktikan. Bab ini soal
hal lain: ongkosnya, dan dinding yang akan ditabrak di Sesi 3.

Tiga angka yang jadi tulang punggungnya, semuanya diukur:
    258 objek Value per iterasi regresi kubik
    996 operasi berantai sebelum backward menyerah
    MLP 784 -> 256 -> 1 sudah melewatinya

Render:
    S:\\Code\\manimations\\.venv\\Scripts\\python.exe -m manim -ql --disable_caching -o b1bab3.mp4 b1_bab3_dinding.py B1Bab3
"""

import numpy as np

from sinema import (
    PALET, FONT_MONO, judul, kaki, kartu_angka, label_kecil, merek,
    muat_data, pencacah, siapkan, subjudul,
)

siapkan()

from manim import *  # noqa: E402

NPZ, ANGKA = muat_data()

VAL_PER_ITER = ANGKA["value_per_iterasi"]
VAL_TOTAL = ANGKA["value_total"]
VAL_MNIST = ANGKA["value_mnist_satu_maju"]
WAKTU_VALUE = ANGKA["waktu_value_ms"]
WAKTU_NUMPY = ANGKA["waktu_numpy_ms"]
REK_BATAS = ANGKA["rekursi_batas"]
REK_LIMIT = ANGKA["rekursi_limit_python"]
REK_TABEL = ANGKA["rekursi_tabel"]


def ribuan(n):
    return f"{int(n):,}".replace(",", ".")


class B1Bab3(Scene):
    def construct(self):
        self.camera.background_color = PALET["latar"]

        jd = judul("Dinding di Depan", 34)
        sj = subjudul(["mesinmu benar, dan itu sudah dibuktikan.",
                       "yang belum: berapa ongkosnya"])
        mk, kk = merek(), kaki()

        self.play(FadeIn(mk, run_time=0.5), FadeIn(kk, run_time=0.5))
        self.play(Write(jd, run_time=1.0))
        self.play(FadeIn(sj, shift=UP * 0.15, run_time=0.6))
        self.wait(0.4)

        # ---------- satu objek per angka ----------
        kiri_judul = label_kecil("mesinmu", PALET["kuning"], 18)
        kanan_judul = label_kecil("PyTorch", PALET["ungu"], 18)
        kiri_judul.move_to([-2.15, 4.05, 0])
        kanan_judul.move_to([2.15, 4.05, 0])

        butir = VGroup()
        rng = np.random.default_rng(2)
        for i in range(36):
            c = Circle(radius=0.115, stroke_color=PALET["kuning"],
                       stroke_width=1.8, fill_color=PALET["kartu"],
                       fill_opacity=1.0)
            butir.add(c)
        butir.arrange_in_grid(rows=6, cols=6, buff=0.14).move_to([-2.15, 2.55, 0])

        tensor = RoundedRectangle(width=2.35, height=2.35, corner_radius=0.12,
                                  stroke_color=PALET["ungu"], stroke_width=2.2,
                                  fill_color=PALET["kartu"], fill_opacity=1.0)
        tensor.move_to([2.15, 2.55, 0])
        kisi_t = VGroup()
        for i in range(5):
            kisi_t.add(Line(tensor.get_left() + RIGHT * 0.39 * (i + 1) + UP * 1.175,
                            tensor.get_left() + RIGHT * 0.39 * (i + 1) + DOWN * 1.175,
                            stroke_color=PALET["ungu"], stroke_width=0.7,
                            stroke_opacity=0.4))
            kisi_t.add(Line(tensor.get_top() + DOWN * 0.39 * (i + 1) + LEFT * 1.175,
                            tensor.get_top() + DOWN * 0.39 * (i + 1) + RIGHT * 1.175,
                            stroke_color=PALET["ungu"], stroke_width=0.7,
                            stroke_opacity=0.4))

        kiri_ket = Paragraph("36 objek Python", "36 closure", "36 pointer",
                             font=FONT_MONO, font_size=14, color=PALET["redup"],
                             line_spacing=0.6, alignment="center")
        kanan_ket = Paragraph("1 objek", "1 blok memori", "1 panggilan BLAS",
                              font=FONT_MONO, font_size=14, color=PALET["redup"],
                              line_spacing=0.6, alignment="center")
        kiri_ket.next_to(butir, DOWN, buff=0.26)
        kanan_ket.next_to(tensor, DOWN, buff=0.26)

        self.play(FadeIn(kiri_judul), FadeIn(kanan_judul), run_time=0.4)
        self.play(LaggedStart(*[GrowFromCenter(c) for c in butir],
                              lag_ratio=0.012, run_time=1.2))
        self.play(Create(tensor, run_time=0.6), Create(kisi_t, run_time=0.6))
        self.play(FadeIn(kiri_ket), FadeIn(kanan_ket), run_time=0.6)
        self.wait(1.2)

        ket = label_kecil("angka yang disimpan sama banyak. ongkos mengurusnya tidak.",
                          PALET["redup"], 15).move_to([0, 0.35, 0])
        self.play(FadeIn(ket, run_time=0.5))
        self.wait(1.4)

        kartu1 = kartu_angka([
            ("objek Value per iterasi", ribuan(VAL_PER_ITER)),
            ("selama 4000 iterasi", ribuan(VAL_TOTAL)),
            ("satu maju MLP 784-32-10", ribuan(VAL_MNIST)),
        ], ukuran=17, warna_nilai=PALET["kuning"]).move_to([0, -1.85, 0])
        self.play(FadeIn(kartu1, shift=UP * 0.2, run_time=0.7))
        self.wait(1.6)

        kartu2 = kartu_angka([
            ("satu langkah, gaya Value", f"{WAKTU_VALUE:.2f} ms"),
            ("satu langkah, numpy", f"{WAKTU_NUMPY:.2f} ms"),
            ("selisihnya", f"{WAKTU_VALUE / max(WAKTU_NUMPY, 1e-9):.0f} kali"),
        ], ukuran=17, warna_nilai=PALET["ungu"]).move_to([0, -4.25, 0])
        self.play(FadeIn(kartu2, shift=UP * 0.2, run_time=0.7))
        self.wait(1.8)

        # ---------- dinding rekursi ----------
        self.play(FadeOut(butir), FadeOut(tensor), FadeOut(kisi_t),
                  FadeOut(kiri_judul), FadeOut(kanan_judul), FadeOut(kiri_ket),
                  FadeOut(kanan_ket), FadeOut(ket), FadeOut(kartu1),
                  FadeOut(kartu2), FadeOut(sj), run_time=0.7)

        sj2 = subjudul(["ada dinding kedua, dan ini",
                        "akan menghentikanmu di Sesi 3"])
        self.play(FadeIn(sj2, run_time=0.5))

        kode = Paragraph(
            "def bangun(v):",
            "    if v not in terlihat:",
            "        terlihat.add(v)",
            "        for anak in v._prev:",
            "            bangun(anak)          <-- memanggil dirinya",
            "        topo.append(v)",
            font=FONT_MONO, font_size=15, color=PALET["teks"],
            line_spacing=0.62, alignment="left",
        )
        kotak_kode = RoundedRectangle(
            width=kode.width + 0.6, height=kode.height + 0.5, corner_radius=0.10,
            fill_color=PALET["kartu"], fill_opacity=1.0,
            stroke_color=PALET["garis"], stroke_width=1.6)
        grup_kode = VGroup(kotak_kode, kode).move_to([0, 3.35, 0])
        kode.move_to(kotak_kode.get_center())

        self.play(FadeIn(grup_kode, run_time=0.8))
        ket_kode = label_kecil("rekursif. tiap simpul menambah satu bingkai tumpukan.",
                               PALET["redup"], 15)
        ket_kode.next_to(grup_kode, DOWN, buff=0.24)
        self.play(FadeIn(ket_kode, run_time=0.5))
        self.wait(1.2)

        kartu3 = kartu_angka([
            ("batas rekursi Python", ribuan(REK_LIMIT)),
            ("rantai terpanjang yang jalan", ribuan(REK_BATAS)),
        ], ukuran=18, warna_nilai=PALET["kuning"]).move_to([0, 0.55, 0])
        self.play(FadeIn(kartu3, shift=UP * 0.2, run_time=0.6))
        self.wait(1.2)

        # tabel arsitektur
        baris = VGroup()
        kepala = Text(f"{'arsitektur':<22}{'kedalaman':>11}   hasil",
                      font=FONT_MONO, font_size=15, color=PALET["redup"])
        baris.add(kepala)
        for masuk, sem, dalam, status in REK_TABEL:
            w = PALET["hijau"] if status == "lolos" else PALET["merah"]
            t = Text(f"{f'{masuk} -> {sem} -> 1':<22}{dalam:>11}   {status}",
                     font=FONT_MONO, font_size=15, color=w)
            baris.add(t)
        baris.arrange(DOWN, buff=0.16, aligned_edge=LEFT).move_to([0, -1.95, 0])

        self.play(FadeIn(baris[0], run_time=0.4))
        for t in baris[1:]:
            self.play(FadeIn(t, shift=RIGHT * 0.12, run_time=0.42))
            self.wait(0.12)
        self.wait(1.0)

        rumus = MathTex(r"\text{kedalaman} \approx n_{\text{masuk}} + n_{\text{sembunyi}}",
                        font_size=28, color=PALET["kuning"]).move_to([0, -3.85, 0])
        if rumus.width > 8.0:
            rumus.scale_to_fit_width(8.0)
        self.play(Write(rumus, run_time=1.0))
        rket = label_kecil("ramalan sederhana, dan tabelnya cocok",
                           PALET["redup"], 15)
        rket.next_to(rumus, DOWN, buff=0.20)
        self.play(FadeIn(rket, run_time=0.5))
        self.wait(1.6)

        tutup = Paragraph(
            "Jangan diperbaiki sekarang.",
            "Biarkan pecah dulu di Sesi 3, lihat pesan errornya,",
            "baru ganti telusur rekursif jadi tumpukan eksplisit.",
            font=FONT_MONO, font_size=16, color=PALET["teks"],
            line_spacing=0.75, alignment="center",
        ).move_to([0, -5.6, 0])
        self.play(FadeIn(tutup, run_time=0.9))
        self.wait(2.2)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.9)
        self.wait(0.3)
