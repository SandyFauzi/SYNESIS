"""Pencarian ke knowledge/. Ini yang membuat SYNESIS menjawab dari catatanmu,
bukan mengarang dari ingatan model.

Kenapa TF-IDF dan bukan embedding.

Embedding lebih pintar. Ia paham "mobil" dan "kendaraan" itu mirip, TF-IDF
tidak. Tapi embedding butuh model tambahan diunduh, butuh VRAM saat dipakai,
dan kalau hasilnya aneh kamu tidak bisa melihat kenapa.

TF-IDF cuma menghitung kata mana yang jarang muncul di seluruh dokumen tapi
sering muncul di satu dokumen. Kamu bisa mencetak angkanya dan melihat persis
kenapa satu potongan terpilih. Untuk knowledge base berisi catatanmu sendiri,
yang istilahnya kamu tulis sendiri dan konsisten, ini sudah cukup.

Kalau nanti terasa kurang, ganti isi berkas ini saja. Yang lain tidak perlu
disentuh. Petunjuknya ada di otak.sematkan().
"""

import re
from dataclasses import dataclass

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from . import konfig


@dataclass
class Potongan:
    sumber: str        # nama berkas, supaya kamu bisa memeriksa sendiri
    judul: str         # heading terdekat di atas potongan ini
    teks: str
    skor: float = 0.0


def _pecah(teks, panjang):
    """Pecah dokumen jadi potongan, mengikuti paragraf dan heading.

    Dipotong per paragraf, bukan per sekian karakter, supaya kalimatnya tidak
    putus di tengah. Heading terdekat ikut dicatat karena itu petunjuk termurah
    tentang isi potongan.
    """
    hasil = []
    judul = ""
    buf = []
    panjang_buf = 0

    def buang():
        nonlocal buf, panjang_buf
        if buf:
            hasil.append((judul, "\n\n".join(buf).strip()))
            buf, panjang_buf = [], 0

    for blok in re.split(r"\n\s*\n", teks):
        blok = blok.strip()
        if not blok:
            continue
        if blok.startswith("#"):
            buang()
            judul = blok.lstrip("#").strip()
            continue
        if panjang_buf + len(blok) > panjang and buf:
            buang()
        buf.append(blok)
        panjang_buf += len(blok)
    buang()
    return [(j, t) for j, t in hasil if len(t) > 40]


class Ingatan:
    """Indeks seluruh isi knowledge/.

    Dibangun ulang tiap SYNESIS dinyalakan. Untuk ratusan berkas markdown itu
    hitungan sepersekian detik, jadi tidak perlu cache yang bisa basi.
    """

    def __init__(self, folder=None):
        self.folder = folder or konfig.KNOWLEDGE
        self.potongan = []
        self.vektor = None
        self.matriks = None
        self.muat()

    def muat(self):
        self.potongan = []
        berkas = sorted(self.folder.rglob("*.md"))
        for b in berkas:
            try:
                isi = b.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            for judul, teks in _pecah(isi, konfig.POTONGAN_PANJANG):
                self.potongan.append(
                    Potongan(sumber=str(b.relative_to(self.folder)),
                             judul=judul, teks=teks))

        if not self.potongan:
            self.vektor, self.matriks = None, None
            return

        # sublinear_tf meredam kata yang muncul berkali-kali dalam satu potongan,
        # supaya satu kata yang diulang tidak mendominasi skornya.
        self.vektor = TfidfVectorizer(
            lowercase=True, sublinear_tf=True,
            ngram_range=(1, 2), min_df=1, max_df=0.85,
        )
        self.matriks = self.vektor.fit_transform(
            [f"{p.judul} {p.teks}" for p in self.potongan])

    def cari(self, pertanyaan, n=None):
        """Kembalikan potongan paling mirip, sudah diurutkan dan disaring."""
        n = n or konfig.POTONGAN_DIAMBIL
        if self.matriks is None:
            return []

        q = self.vektor.transform([pertanyaan])
        # Matriks TF-IDF sklearn sudah dinormalkan L2, jadi hasil kali dalam
        # ini persis kemiripan kosinus. Tidak perlu dibagi apa-apa lagi.
        skor = (self.matriks @ q.T).toarray().ravel()

        urut = np.argsort(-skor)[:n]
        keluar = []
        for i in urut:
            if skor[i] < konfig.AMBANG_MIRIP:
                break
            p = self.potongan[i]
            keluar.append(Potongan(p.sumber, p.judul, p.teks, float(skor[i])))
        return keluar

    def catatan(self, pertanyaan):
        """Rakit blok CATATAN untuk diselipkan ke prompt.

        Nama berkas ikut ditulis. Itu bukan hiasan: kalau jawaban SYNESIS aneh,
        kamu bisa langsung membuka berkas yang disebut dan memeriksa sendiri.
        """
        potong = self.cari(pertanyaan)
        if not potong:
            return "", []
        bagian = []
        for p in potong:
            kepala = f"[{p.sumber}" + (f" · {p.judul}]" if p.judul else "]")
            bagian.append(f"{kepala}\n{p.teks}")
        return "CATATAN:\n\n" + "\n\n---\n\n".join(bagian), potong

    def ringkas(self):
        n_berkas = len({p.sumber for p in self.potongan})
        return f"{len(self.potongan)} potongan dari {n_berkas} berkas"
