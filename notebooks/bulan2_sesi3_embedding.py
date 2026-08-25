"""Bulan 2 Sesi 3 - representasi: dari kolom kata ke arah makna.

Jalankan:
    . .\\scripts\\activate.ps1
    python notebooks\\bulan2_sesi3_embedding.py

Sesi 2 berakhir dengan angka yang tidak enak dilihat, dan itu justru
kelebihannya. Model yang mencetak 100 persen di uji sintetis cuma mencetak
56,1 persen di 41 pesan nyatamu. Sebabnya sudah terukur: 55,2 persen kata di
pesan nyata tidak punya kolom di model, jadi kata itu menguap sebelum model
sempat melihatnya.

Malam ini kita serang sebab itu, bukan gejalanya.

Ada satu keterbatasan mendasar pada kantong kata yang belum pernah kita sebut
terang-terangan: `buka` dan `bukain` adalah dua kolom yang tidak saling
mengenal. Model tidak tahu keduanya berkerabat. Ia juga tidak tahu `berkas`
dan `file` menunjuk hal yang sama. Setiap kata adalah pulau. Itulah kenapa
satu kata baru langsung hilang tanpa jejak, bukan cuma berkurang bobotnya.

Yang akan kamu bangun malam ini semuanya menyerang keterpulauan itu:

    1  dasar mayoritas, supaya kamu tahu 56,1 persen itu sebenarnya seberapa
    2  kosinus, dan bukti terukur bahwa kolom kata buta terhadap kemiripan
    3  n-gram karakter, tambalan yang tidak butuh belajar sama sekali
    4  matriks ko-okurensi dari arsip tulisanmu sendiri
    5  PPMI, karena hitungan mentah didominasi kata yang sering saja
    6  SVD, dan kejujuran soal korpus 150 ribu kata
    7  lapisan embedding yang dilatih ujung ke ujung dengan Tensor buatanmu

Sekali lagi tidak ada kode autograd baru. `Tensor` dari Bulan 1 dipakai apa
adanya. Lapisan embedding ternyata cuma perkalian matriks, dan Bagian 7 akan
menunjukkan itu bukan penyederhanaan, melainkan definisinya.

Peringatan yang perlu kamu bawa sejak awal: sesi ini kemungkinan besar TIDAK
berakhir dengan lompatan akurasi. Himpunan ujimu 41 kalimat, dan 41 itu kecil
sekali. Bagian 1 menghitung seberapa kecil. Kalau akhirnya semua resep terlihat
sama, jawaban yang benar adalah mengatakannya, persis seperti Soal 3 Sesi 2.

Bagian bertanda TODO kamu yang isi.
"""

import re
import sys
import time
from collections import Counter
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from bulan1_sesi34_mnist import Tensor, maju  # noqa: E402
from bulan2_sesi2_intent import (  # noqa: E402
    bangun_kosakata, belah_tiga, bobot_idf, latih, muat_perintah, vektorkan)

GARIS = "=" * 66

AKAR = Path(__file__).resolve().parent.parent
DATA = AKAR / "data" / "bulan2"

# Folder yang TIDAK boleh masuk korpus. `data/` dibuang karena di dalamnya ada
# arsip percakapan sumber, dan 41 pesan ujimu diambil persis dari sana. Memakai
# arsip itu sebagai korpus berarti vektor katamu dibangun dari kalimat yang
# nanti dipakai menguji. Labelnya memang tidak ikut bocor, tapi kalimatnya
# bocor, dan Soal 5 membahas apakah itu masih boleh disebut curang.
KORPUS_BUANG = {".git", "node_modules", "__pycache__", "data", "knowladge",
                "figures", "video", "Contoh Video"}

KORPUS_KATA_MAKS = 2000     # batas kosakata matriks ko-okurensi
JENDELA = 5                 # berapa kata kiri-kanan dihitung bertetangga

# Batas kalimat latih sintetis yang dipakai Bagian 7. Lihat alasannya di
# `bagian7`; ringkasnya, sapuan porsi di Tuas B tidak sahih kalau data
# sintetisnya jauh lebih besar daripada yang bisa diimbangi 41 kalimat nyata.
ANGGARAN_LATIH = 1050
PORSI_TUAS_B = (0.03, 0.10, 0.30, 0.50)


# ══════════════════════════════════════════════════════════════
# BAGIAN 1 - 56,1 persen itu sebenarnya seberapa
# ══════════════════════════════════════════════════════════════

def dasar_mayoritas(pasang):
    """Akurasi kalau kamu selalu menebak kelas terbanyak. Disediakan.

    Ini lawan yang harus kamu kalahkan sebelum boleh senang. Model apa pun
    yang tidak melewati garis ini belum membuktikan bahwa ia belajar apa-apa.
    """
    hitung = Counter(l for _, l in pasang)
    kelas, n = hitung.most_common(1)[0]
    return kelas, n / len(pasang)


def selang_binomial(benar, n, z=1.96):
    """Selang kepercayaan untuk akurasi yang diukur dari n contoh.

    Kembalikan (p, bawah, atas) sebagai pecahan, bukan persen.

    Akurasi itu proporsi dari n percobaan Bernoulli, jadi simpangan bakunya

        sigma = sqrt( p (1 - p) / n )

    dan selang 95 persen kira-kira p plus minus 1,96 sigma. Potong di 0 dan 1,
    karena akurasi tidak bisa negatif atau lebih dari satu.

    Kamu sudah memakai rumus ini di Soal 1b Sesi 2 untuk menghitung BERAPA
    kalimat uji yang dibutuhkan. Sekarang arahnya dibalik: kamu sudah punya 41,
    dan mau tahu selangnya selebar apa.

    Ini ralat pengukuran, sama persis dengan yang kamu tulis di laporan
    praktikum. Melaporkan "56,1 persen" tanpa selang itu seperti melaporkan
    "9,7 m/s^2" tanpa menulis plus minus berapa.

    TODO 1
    """
    p = benar / n
    lebar = z * (p * (1 - p) / n) ** 0.5
    return p, max(0.0, p - lebar), min(1.0, p + lebar)


def bagian1(nyata):
    print(GARIS, "\nBAGIAN 1  56,1 persen itu sebenarnya seberapa\n",
          GARIS, sep="")

    kelas, dasar = dasar_mayoritas(nyata)
    n = len(nyata)
    hitung = Counter(l for _, l in nyata)

    print(f"  pesan nyata    : {n}")
    print(f"  intent terpakai: {len(hitung)}\n")
    print(f"  {'intent':<18}{'jumlah':>8}{'bagian':>9}")
    print("  " + "-" * 35)
    for label, c in hitung.most_common():
        print(f"  {label:<18}{c:>8}{c / n * 100:>8.1f}%")

    p_model = 23 / n
    _, b_m, a_m = selang_binomial(23, n)
    _, b_d, a_d = selang_binomial(hitung[kelas], n)
    lebar = 2 * 1.96 * (p_model * (1 - p_model) / n) ** 0.5 * 100

    print()
    print(f"  {'resep':<24}{'akurasi':>9}{'selang 95 persen':>22}")
    print("  " + "-" * 55)
    print(f"  {'tebak ' + kelas + ' terus':<24}{dasar * 100:>8.1f}%"
          f"{b_d * 100:>14.1f} .. {a_d * 100:.1f}")
    print(f"  {'model Sesi 2':<24}{p_model * 100:>8.1f}%"
          f"{b_m * 100:>14.1f} .. {a_m * 100:.1f}")

    print(f"""
  Baca dua baris itu berdampingan sebelum melanjutkan.

  Menebak "{kelas}" untuk SEMUA pesan, tanpa model, tanpa latihan, tanpa
  satu baris kode pun, sudah benar {dasar * 100:.1f} persen. Modelmu
  benar {p_model * 100:.1f} persen. Jaraknya {(p_model - dasar) * 100:.1f} poin.

  Dan selangnya tumpang tindih hampir seluruhnya. Batas bawah modelmu
  {b_m * 100:.1f} persen, cuma {b_m * 100 - dasar * 100:.1f} poin di atas dasar
  mayoritas. Dengan n = {n}, satu kalimat pindah kolom menggeser
  angkanya {1 / n * 100:.1f} poin, jadi selisih tiga kalimat saja sudah lebih
  besar daripada seluruh keunggulan yang kamu punya atas menebak buta.

  Ini bukan alasan menyerah. Ini alasan berhenti mempercayai selisih kecil di
  data sebesar ini. Sepanjang sesi malam ini akan muncul banyak tabel dengan
  akurasi berbeda-beda. Selang tiap barisnya selebar sekitar {lebar:.0f} poin,
  jadi hampir semua selisih antarbaris tidak akan terukur.

  Aturan yang dipakai sepanjang sesi: sebuah resep baru dianggap lebih baik
  hanya kalau selangnya tidak lagi memuat resep pembanding. Bukan kalau
  angkanya kebetulan lebih besar.

  Soal 1 memintamu menghitung n yang dibutuhkan supaya selisih 10 poin bisa
  dibedakan dari nol.""")

    return dasar


# ══════════════════════════════════════════════════════════════
# BAGIAN 2 - kolom kata buta terhadap kemiripan
# ══════════════════════════════════════════════════════════════

def kosinus(a, b):
    """Kemiripan kosinus dua vektor.

        cos(a, b) = (a . b) / (|a| |b|)

    Kembalikan 0.0 kalau salah satu vektor panjangnya nol, karena sudut
    terhadap vektor nol tidak terdefinisi dan melempar galat di tengah tabel
    itu tidak menolong siapa pun.

    Jembatan fisika, dan ini bukan analogi longgar melainkan operasi yang sama:
    ini hasil kali dalam ternormalkan. Di Fisika Kuantum kamu menulisnya
    <psi|phi> dengan |psi> dan |phi> sudah dinormalkan, dan nilainya menyatakan
    seberapa besar satu keadaan tumpang tindih dengan keadaan lain. Di sini
    keadaannya kalimat, dan basisnya kata.

    Yang membuat kantong kata lemah persis terlihat dari basisnya: tiap kata
    adalah satu sumbu ortogonal. Sumbu "buka" tegak lurus terhadap sumbu
    "bukain". Dua kata yang berkerabat erat punya tumpang tindih NOL menurut
    ukuran ini, dan tidak ada bobot apa pun yang bisa memperbaikinya, karena
    masalahnya di pilihan basis.

    TODO 2
    """
    panjang = np.linalg.norm(a) * np.linalg.norm(b)
    return 0.0 if panjang == 0 else float(np.dot(a, b) / panjang)


PASANGAN_KERABAT = [
    ("buka", "bukain"),
    ("buka", "bukakan"),
    ("cari", "cariin"),
    ("berkas", "file"),
    ("bikin", "buat"),
    ("jelaskan", "jelasin"),
    ("hapus", "menghapus"),
    ("install", "menginstal"),
]


def bagian2(sint, nyata):
    print("\n" + GARIS, "\nBAGIAN 2  kolom kata buta terhadap kemiripan\n",
          GARIS, sep="")

    kos = bangun_kosakata([k for k, _ in sint])
    print(f"  kosakata dari 1.080 kalimat sintetis : {len(kos)} kata\n")

    print(f"  {'kata A':<12}{'kata B':<14}{'kosinus':>9}   keterangan")
    print("  " + "-" * 58)
    for a, b in PASANGAN_KERABAT:
        va = vektorkan([a], kos)[0]
        vb = vektorkan([b], kos)[0]
        ada = ("ada" if a in kos else "A hilang") + ", " + \
              ("ada" if b in kos else "B hilang")
        print(f"  {a:<12}{b:<14}{kosinus(va, vb):>9.3f}   {ada}")

    tok = [w for k, _ in nyata for w in re.findall(r"[a-z0-9]+", k.lower())]
    oov = [w for w in tok if w not in kos]
    nol = [k for k, _ in nyata
           if not any(w in kos for w in re.findall(r"[a-z0-9]+", k.lower()))]

    print(f"""
  Seluruh kolom kosinus nol, dan itu bukan kebetulan melainkan definisi.
  Vektor "buka" cuma menyalakan sumbu ke-{kos.get('buka', -1)}, vektor "bukain"
  menyalakan sumbu lain. Hasil kali dalamnya nol karena tidak ada satu pun
  sumbu yang sama-sama menyala. Modelmu tidak "hampir tahu" keduanya
  berkerabat. Ia tidak punya cara untuk tahu.

  Akibatnya di data nyata:

    token pesan nyata          : {len(tok)}
    di luar kosakata           : {len(oov)} = {len(oov) / len(tok) * 100:.1f} persen
    kalimat yang vektornya NOL : {len(nol)} dari {len(nyata)}

  Baris terakhir itu yang paling perlu kamu resapi. Untuk {len(nol)} pesan,
  masukan ke jaringanmu adalah vektor nol utuh. Lapisan pertama menghasilkan
  geseran b1 saja, jadi keluarannya sama persis untuk ketiga kalimat itu,
  apa pun isinya. Model tidak menebak berdasarkan kalimat. Model mengeluarkan
  satu tebakan tetap yang sama untuk semua kalimat yang tidak ia kenali.

  Contohnya:""")
    for k in nol:
        print(f"    '{k[:64]}'")

    print("""
  Soal 2 memintamu menghitung kelas apa yang keluar untuk vektor nol, tanpa
  menjalankan model.""")

    return kos


# ══════════════════════════════════════════════════════════════
# BAGIAN 3 - n-gram karakter, tambalan yang tidak butuh belajar
# ══════════════════════════════════════════════════════════════

def ngram_karakter(kata, n_min=3, n_maks=5):
    """Pecah satu kata jadi himpunan potongan karakter.

    Bungkus katanya dengan penanda batas dulu: "buka" jadi "<buka>". Tanpa
    penanda itu, potongan "buk" dari "buka" dan dari "sebuka" tidak bisa
    dibedakan, padahal awalan kata membawa banyak informasi. Dengan penanda,
    "<bu" hanya muncul di kata yang MEMULAI dengan "bu".

    Lalu ambil semua potongan berurutan sepanjang n_min sampai n_maks.
    Kembalikan `set`, bukan `list`, karena yang dipedulikan adalah potongan apa
    yang hadir, bukan berapa kali.

    Contoh yang harus lolos:

        ngram_karakter("buka", 3, 3) == {"<bu", "buk", "uka", "ka>"}

    Kenapa ini menolong, dan kenapa tanpa satu langkah latihan pun: "bukain"
    membungkus jadi "<bukain>", dan potongan "<bu", "buk", "uka" muncul di
    kedua kata. Dua kata yang tadinya ortogonal sekarang berbagi sumbu.
    Kekerabatan yang tadi harus dipelajari sekarang jatuh gratis dari ejaan.

    TODO 3
    """
    s = f"<{kata}>"
    return {s[i:i + n] for n in range(n_min, n_maks + 1)
            for i in range(len(s) - n + 1)}


def kosakata_ngram(kalimat, n_min=3, n_maks=5):
    """Kumpulkan semua potongan karakter yang muncul di data latih. Disediakan."""
    potong = set()
    for k in kalimat:
        for w in re.findall(r"[a-z0-9]+", k.lower()):
            potong |= ngram_karakter(w, n_min, n_maks)
    return {t: i for i, t in enumerate(sorted(potong))}


def vektorkan_ngram(kalimat, kos, n_min=3, n_maks=5):
    """Ubah kalimat jadi matriks (n_kalimat, n_potongan), tiap baris panjang 1.

    Bentuknya sama persis dengan `vektorkan` di Sesi 2, cuma sumbunya potongan
    karakter, bukan kata. Hitung berapa kali tiap potongan muncul di kalimat,
    lalu normalkan tiap baris jadi panjang satu.

    Normalisasi baris di sini bahkan lebih penting daripada di Sesi 2. Satu
    kata sepanjang 12 huruf menghasilkan puluhan potongan, satu kata 3 huruf
    menghasilkan segelintir. Tanpa normalisasi, kalimat berkata panjang otomatis
    punya vektor jauh lebih besar.

    Potongan yang tidak ada di `kos` diabaikan, sama seperti kata OOV di Sesi 2.
    Bedanya, sekarang sebuah kata asing biasanya masih menyumbang SEBAGIAN
    potongannya. Ia tidak lagi menguap utuh.

    TODO 4
    """
    X = np.zeros((len(kalimat), len(kos)))
    for i, teks in enumerate(kalimat):
        for kata in re.findall(r"[a-z0-9]+", teks.lower()):
            for g in ngram_karakter(kata, n_min, n_maks):
                if g in kos:
                    X[i, kos[g]] += 1
    panjang = np.linalg.norm(X, axis=1, keepdims=True)
    np.divide(X, panjang, out=X, where=panjang != 0)
    return X


def bagian3(sint, nyata, kos_kata):
    print("\n" + GARIS,
          "\nBAGIAN 3  n-gram karakter: kekerabatan gratis dari ejaan\n",
          GARIS, sep="")

    print(f"  {'kata A':<12}{'kata B':<14}{'kata':>8}{'n-gram 3-5':>13}")
    print("  " + "-" * 47)
    kg = kosakata_ngram([k for k, _ in sint])
    for a, b in PASANGAN_KERABAT:
        k1 = kosinus(vektorkan([a], kos_kata)[0], vektorkan([b], kos_kata)[0])
        g1 = kosinus(vektorkan_ngram([a], kg)[0], vektorkan_ngram([b], kg)[0])
        print(f"  {a:<12}{b:<14}{k1:>8.3f}{g1:>13.3f}")

    tok = [w for k, _ in nyata for w in re.findall(r"[a-z0-9]+", k.lower())]
    oov_kata = [w for w in tok if w not in kos_kata]
    g_nyata = [g for w in tok for g in ngram_karakter(w)]
    g_oov = [g for g in g_nyata if g not in kg]
    punya = sum(1 for w in set(oov_kata) if ngram_karakter(w) & set(kg))

    print(f"""
  Kolom terakhir itu seluruh isi bagian ini. Tanpa melatih apa pun, tanpa
  korpus tambahan, cuma dengan memecah kata jadi potongan huruf.

  Ukuran yang sama di pesan nyata:

    {'satuan':<26}{'jumlah':>10}{'di luar latih':>16}
    {'-' * 52}
    {'kata':<26}{len(tok):>10}{len(oov_kata) / len(tok) * 100:>15.1f}%
    {'potongan karakter 3-5':<26}{len(g_nyata):>10}{len(g_oov) / len(g_nyata) * 100:>15.1f}%

    kata asing unik                 : {len(set(oov_kata))}
    yang punya minimal satu potongan
    dikenal                         : {punya} = {punya / len(set(oov_kata)) * 100:.1f} persen

  Baris terakhir itu janjinya. Dari {len(set(oov_kata))} kata yang tadinya
  menguap utuh, {punya} sekarang masih meninggalkan jejak. Bukan jejak yang
  lengkap, tapi bukan nol.

  Sekarang latih dan lihat apakah janji itu jadi akurasi. Perhatikan bahwa
  sapuan di bawah mengubah SATU hal saja: panjang potongan.""")

    label = sorted({l for _, l in sint})
    L = {l: i for i, l in enumerate(label)}
    tr, va, _ = belah_tiga(sint, seed=0)
    ytr = np.array([L[l] for _, l in tr])
    yva = np.array([L[l] for _, l in va])
    yny = np.array([L[l] for _, l in nyata])
    Kny = [k for k, _ in nyata]
    n = len(nyata)

    baris = []
    Xtr = vektorkan([k for k, _ in tr], kos_kata)
    Xva = vektorkan([k for k, _ in va], kos_kata)
    p, _ = latih(Xtr, ytr, Xva, yva, len(L), seed=0)
    a = (maju(p, vektorkan(Kny, kos_kata)).data.argmax(1) == yny).mean()
    baris.append(("kata (Sesi 2)", len(kos_kata), a))

    for lo, hi in ((2, 4), (3, 4), (3, 5), (4, 6)):
        k2 = kosakata_ngram([k for k, _ in tr], lo, hi)
        Xtr = vektorkan_ngram([k for k, _ in tr], k2, lo, hi)
        Xva = vektorkan_ngram([k for k, _ in va], k2, lo, hi)
        p, _ = latih(Xtr, ytr, Xva, yva, len(L), seed=0)
        a = (maju(p, vektorkan_ngram(Kny, k2, lo, hi)).data.argmax(1)
             == yny).mean()
        baris.append((f"n-gram {lo}-{hi}", len(k2), a))

    print(f"\n  {'fitur':<16}{'kolom':>8}{'pesan nyata':>14}{'selang 95 persen':>22}")
    print("  " + "-" * 60)
    for nama, kolom, a in baris:
        _, b, t = selang_binomial(round(a * n), n)
        print(f"  {nama:<16}{kolom:>8}{a * 100:>13.1f}%"
              f"{b * 100:>14.1f} .. {t * 100:.1f}")

    lebar = (max(a for _, _, a in baris) - min(a for _, _, a in baris)) * 100
    print(f"""
  Rentang seluruh tabel: {lebar:.1f} poin persen, dan yang berubah cuma pilihan
  panjang potongan. Bandingkan dengan lebar selang tiap barisnya, sekitar 30
  poin. Sapuan ini menunjukkan bahwa memilih baris terbaik lalu melaporkannya
  sebagai "hasil n-gram" adalah memilih derau.

  Ini bentuk yang sama dengan Soal 3 Sesi 2, tapi sumber derau yang berbeda.
  Di sana derau datang dari belahan mana yang kebetulan jadi uji. Di sini
  derau datang dari hiperparameter yang tidak punya alasan prinsipil.

  Soal 3 memintamu memutuskan panjang potongan mana yang dipakai, dan alasan
  yang boleh kamu pakai untuk itu.""")

    return baris


# ══════════════════════════════════════════════════════════════
# BAGIAN 4 - vektor kata dari arsip tulisanmu sendiri
# ══════════════════════════════════════════════════════════════

def kumpulkan_korpus(akar=AKAR, buang=KORPUS_BUANG):
    """Baca semua teks di repo jadi satu daftar token. Disediakan.

    Ini korpus tanpa label. Tidak ada satu pun intent di sini, dan memang itu
    intinya. Vektor kata dipelajari dari teks polos, lalu dipakai sebagai
    fitur untuk tugas berlabel. Namanya prapelatihan tanpa pengawasan, dan
    inilah gagasan yang melahirkan word2vec, GloVe, sampai BERT.

    Bedanya cuma skala. Korpusmu ratusan ribu kata. Korpus GloVe 6 miliar.
    Bagian 6 mengukur apa artinya selisih empat orde besaran itu.
    """
    teks = []
    for p in sorted(akar.rglob("*")):
        if not p.is_file() or p.suffix not in (".md", ".jsonl", ".py"):
            continue
        if any(b in p.relative_to(akar).parts for b in buang):
            continue
        try:
            teks.append(p.read_text(encoding="utf-8", errors="ignore").lower())
        except OSError:
            continue
    return re.findall(r"[a-z]{2,}", "\n".join(teks))


def matriks_kookurensi(token, kosakata, jendela=JENDELA):
    """Hitung berapa kali kata i muncul dekat kata j.

    token    : daftar kata berurutan, hasil `kumpulkan_korpus`
    kosakata : dict kata -> indeks; kata di luar ini dilewati
    jendela  : berapa kata ke kiri dan ke kanan dianggap bertetangga

    Kembalikan array (V, V) berisi hitungan.

    Hipotesis distribusional, dan seluruh bidang ini berdiri di atasnya: kata
    yang muncul di lingkungan yang mirip cenderung punya makna yang mirip.
    Kamu tidak pernah memberi tahu mesin bahwa "venv" dan "python" berkerabat.
    Mesin menyimpulkannya karena keduanya sama-sama muncul dekat "install",
    "scripts", "activate".

    Perhatikan bahwa kata di luar kosakata DILEWATI, bukan dihapus dari
    barisan. Kalau kamu menghapusnya, kata di kiri dan kanannya jadi bertetangga
    padahal aslinya terpisah. Soal 4 membahas mana yang lebih benar.

    Matriks ini simetris kalau jendelanya simetris, dan diagonalnya harus nol
    karena kata bukan tetangga dirinya sendiri.

    Ini akan jadi gelung Python atas ratusan ribu token. Lambat, dan itu tidak
    apa-apa. Kamu menulisnya sekali untuk paham; Bagian 6 menyimpan hasilnya.

    TODO 5
    """
    C = np.zeros((len(kosakata), len(kosakata)))
    indeks = [kosakata.get(w, -1) for w in token]
    for i, a in enumerate(indeks):
        if a < 0:
            continue
        for b in indeks[max(0, i - jendela):i] + indeks[i + 1:i + jendela + 1]:
            if b >= 0:
                C[a, b] += 1
    return C


def ppmi(C):
    """Ubah hitungan mentah jadi PPMI: positive pointwise mutual information.

        p(i,j) = C[i,j] / total
        p(i)   = jumlah baris i / total
        p(j)   = jumlah kolom j / total

        PMI(i,j)  = log2( p(i,j) / (p(i) p(j)) )
        PPMI(i,j) = max(0, PMI(i,j))

    Kenapa hitungan mentah tidak cukup. Kata "yang" bertetangga dengan segala
    hal ribuan kali. Kalau kamu memakai hitungan apa adanya, baris untuk setiap
    kata akan didominasi oleh kata-kata yang memang sering, dan semua kata jadi
    terlihat mirip satu sama lain. Yang mau kamu tangkap bukan "berapa kali i
    dan j bersebelahan", tapi "berapa kali LEBIH SERING daripada seharusnya
    kalau keduanya tidak berhubungan".

    Penyebut p(i) p(j) itu persis peluang gabungan seandainya i dan j saling
    bebas. Jadi PMI mengukur simpangan dari kebebasan. Nol berarti persis
    seperti kebetulan. Positif berarti lebih sering daripada kebetulan.

    Kenapa yang negatif dibuang. PMI negatif berarti "lebih jarang daripada
    kebetulan", dan untuk memperkirakan itu dengan andal kamu butuh korpus jauh
    lebih besar daripada punyamu. Dengan 150 ribu token, nilai negatif hampir
    seluruhnya derau pencacahan. Membuangnya juga membuat matriksnya jarang,
    dan itu menolong SVD.

    Hati-hati pada log nol. Pasangan yang tidak pernah bersebelahan memberi
    log(0) = -inf. Tangani sebelum `np.maximum`, jangan sesudah.

    TODO 6
    """
    total = C.sum()
    p_i = C.sum(axis=1, keepdims=True) / total
    p_j = C.sum(axis=0, keepdims=True) / total
    with np.errstate(divide="ignore", invalid="ignore"):
        pmi = np.log2(C / total / (p_i * p_j))
    return np.maximum(0.0, np.nan_to_num(pmi, nan=0.0, neginf=0.0))


def bagian4(token):
    print("\n" + GARIS,
          "\nBAGIAN 4  vektor kata dari arsip tulisanmu sendiri\n",
          GARIS, sep="")

    hit = Counter(token)
    sering = [w for w, _ in hit.most_common(KORPUS_KATA_MAKS)]
    V = {w: i for i, w in enumerate(sorted(sering))}

    print(f"  token korpus       : {len(token)}")
    print(f"  kata unik          : {len(hit)}")
    print(f"  dipakai (tersering): {len(V)}")
    print(f"  jendela            : {JENDELA} kata kiri dan kanan\n")

    mulai = time.perf_counter()
    C = matriks_kookurensi(token, V)
    M = ppmi(C)
    detik = time.perf_counter() - mulai

    isi_c, isi_m = (C > 0).mean(), (M > 0).mean()
    diag = np.diag(C)
    print(f"  matriks {C.shape[0]} x {C.shape[1]}, dibangun dalam {detik:.1f} detik")
    print(f"  sel taknol sebelum PPMI : {isi_c * 100:5.1f} persen")
    print(f"  sel taknol sesudah PPMI : {isi_m * 100:5.1f} persen")
    print(f"  simetris                : {np.allclose(C, C.T)}")
    print(f"  diagonal taknol         : {(diag > 0).sum()} kata, "
          f"terbesar {diag.max():.0f}")

    besar = sorted(V, key=lambda w: -C[V[w], V[w]])[:5]
    print(f"  diagonal terbesar       : {', '.join(besar)}")

    atas = [V[w] for w in sorted(V, key=lambda w: -C[V[w]].sum())[:5]]
    nama_atas = [w for w in sorted(V, key=lambda w: -C[V[w]].sum())[:5]]
    massa_c = C[atas].sum() / C.sum() * 100
    massa_m = M[atas].sum() / M.sum() * 100
    print(f"\n  lima kata tersering     : {', '.join(nama_atas)}")
    print(f"  porsi massa sebelum PPMI: {massa_c:5.1f} persen")
    print(f"  porsi massa sesudah PPMI: {massa_m:5.1f} persen")

    print(f"""
  Diagonal itu perlu dijelaskan, karena hampir semua orang menduga isinya nol.
  C[i][i] menghitung berapa kali kata i muncul di dekat kata i LAGI, dan itu
  memang terjadi: kata yang sering seperti "yang" atau "dan" muncul dua kali
  dalam satu jendela sepanjang {JENDELA} kata. Yang harus nol cuma pasangan kata
  dengan DIRINYA SENDIRI di posisi yang sama, dan itu sudah dicegah syarat
  j != i. Soal 4 menanyakan apakah diagonal ini sebaiknya dibiarkan atau
  dinolkan sebelum PPMI.

  Dua baris taknol menunjukkan berapa banyak sel yang dinolkan PPMI, yaitu
  sekitar {(1 - isi_m / isi_c) * 100:.0f} persen dari yang tadinya terisi.
  Yang dinolkan itu pasangan yang bersebelahan TIDAK lebih sering daripada
  kebetulan.

  Kalau kamu menduga PPMI akan memangkas separuh matriks, itu dugaan yang
  wajar dan ternyata keliru. Penyaringan terbesarnya ada di NILAI sel, bukan
  di jumlahnya, dan dua baris massa di atas menunjukkannya. Lima kata
  tersering memegang {massa_c:.1f} persen hitungan mentah, lalu tinggal
  {massa_m:.1f} persen sesudah PPMI. Bobotnya nyaris hilang tanpa satu pun
  selnya jadi nol.

  Tiap kata sekarang punya baris sepanjang {len(V)}, dan itu sudah vektor yang
  bisa dipakai. Tapi {len(V)} dimensi yang cuma {isi_m * 100:.0f} persen
  terisi itu boros dan berisik. Bagian 5 memampatkannya.""")

    return V, M


# ══════════════════════════════════════════════════════════════
# BAGIAN 5 - SVD, dan kejujuran soal korpus 150 ribu kata
# ══════════════════════════════════════════════════════════════

def padatkan(M, d=100):
    """Mampatkan matriks PPMI jadi vektor rapat d dimensi lewat SVD. Disediakan.

        M = U S V^T,  ambil d kolom pertama,  E = U[:, :d] * S[:d]

    SVD memberi basis ortogonal yang terurut menurut seberapa besar ragam yang
    dijelaskannya. Memotong di d berarti membuang arah yang paling sedikit
    menjelaskan, dan arah itu biasanya derau pencacahan.

    Ini persis analisis komponen utama yang kamu pakai di praktikum untuk
    memampatkan data pengukuran, diterapkan pada matriks kata. Tidak ada
    yang baru secara matematis.

    Barisnya dinormalkan jadi panjang satu di akhir, supaya `kosinus` di
    Bagian 2 tinggal jadi hasil kali dalam biasa.
    """
    U, S, _ = np.linalg.svd(M, full_matrices=False)
    E = U[:, :d] * S[:d]
    panjang = np.linalg.norm(E, axis=1, keepdims=True)
    return E / (panjang + 1e-12)


def tetangga(E, kosakata, kata, k=8):
    """Kembalikan k kata terdekat dari `kata` menurut kosinus.

    Kembalikan daftar (kata_tetangga, skor), terurut menurun. Kata itu sendiri
    tidak dihitung sebagai tetangganya sendiri. Kalau `kata` tidak ada di
    kosakata, kembalikan daftar kosong.

    Karena baris E sudah dinormalkan di `padatkan`, kosinus terhadap semua kata
    sekaligus cukup satu perkalian matriks-vektor: `E @ E[i]`. Tidak perlu
    gelung.

    Ini fungsi diagnostik, dan itu bukan hal sepele. Sampai sekarang kamu cuma
    bisa menilai representasi lewat akurasi hilir, yang di n = 41 hampir tidak
    bisa mengukur apa pun. `tetangga` membiarkanmu memeriksa representasinya
    LANGSUNG, tanpa lewat pengklasifikasi.

    TODO 7
    """
    i = kosakata.get(kata)
    if i is None:
        return []
    skor = E @ E[i]
    nama = {j: w for w, j in kosakata.items()}
    urut = [j for j in np.argsort(-skor)[:k + 1] if j != i][:k]
    return [(nama[j], float(skor[j])) for j in urut]


# Pasangan yang kamu tahu berkerabat di dunia proyekmu sendiri. Dipakai untuk
# menilai vektor kata dengan angka, bukan dengan kesan.
PASANGAN_UJI = [
    ("python", "venv"), ("python", "pip"), ("gpu", "vram"), ("gpu", "cuda"),
    ("install", "menginstal"), ("git", "commit"), ("gradient", "descent"),
    ("kuliah", "semester"), ("fisika", "matematika"), ("numpy", "matplotlib"),
    ("model", "latih"), ("berkas", "folder"), ("disk", "drive"),
    ("laptop", "ram"), ("epoch", "iterasi"), ("softmax", "logit"),
]


def peringkat_pasangan(E, V, pasangan=PASANGAN_UJI):
    """Nilai kualitas vektor kata dengan satu angka. Disediakan.

    Untuk tiap pasangan (a, b) yang keduanya ada di kosakata, cari peringkat b
    di dalam daftar tetangga a yang terurut. Peringkat 1 berarti b adalah
    tetangga terdekat a. Kembalikan (median peringkat, jumlah pasangan terpakai,
    ukuran kosakata).

    Kenapa peringkat, bukan kosinus. Kosinus mentah tidak punya skala yang bisa
    ditafsirkan; 0,42 itu bagus atau jelek tergantung sebaran seluruh kosakata.
    Peringkat punya pembanding nol yang jelas: kalau vektormu murni acak,
    peringkat median yang diharapkan adalah setengah ukuran kosakata.

    Jadi angka ini bisa dibaca langsung. Median peringkat 3 dari kosakata 2.000
    berarti sangat baik. Median 900 dari 2.000 berarti vektormu tidak lebih
    berguna daripada dadu.
    """
    peringkat = []
    for a, b in pasangan:
        if a not in V or b not in V:
            continue
        skor = E @ E[V[a]]
        urut = np.argsort(-skor)
        pos = int(np.where(urut == V[b])[0][0])
        peringkat.append(pos)          # pos 0 adalah a sendiri
    if not peringkat:
        return float("nan"), 0, len(V)
    return float(np.median(peringkat)), len(peringkat), len(V)


def bagian5(token, V, M):
    print("\n" + GARIS,
          "\nBAGIAN 5  SVD, tetangga, dan kejujuran soal ukuran korpus\n",
          GARIS, sep="")

    E = padatkan(M, d=100)
    print(f"  {M.shape[0]} dimensi jarang  ->  {E.shape[1]} dimensi rapat\n")

    for kata in ("python", "gpu", "install", "berkas", "kuliah", "buka",
                 "roadmap"):
        hasil = tetangga(E, V, kata, k=7)
        if not hasil:
            print(f"  {kata:>10} -> tidak ada di kosakata korpus")
            continue
        print(f"  {kata:>10} -> " + ", ".join(w for w, _ in hasil))

    med, dipakai, ukuran = peringkat_pasangan(E, V)
    print(f"""
  Baca daftar itu jujur: cari baris yang MELESET, bukan baris yang kebetulan
  rapi. Mata manusia sangat pandai membaca pola dari daftar acak, dan itu
  sebabnya penilaian dengan mata tidak boleh jadi bukti.

  Jadi ini angkanya, bukan kesan:

    pasangan uji terpakai : {dipakai} dari {len(PASANGAN_UJI)}
    median peringkat      : {med:.0f} dari {ukuran} kata
    pembanding acak       : {ukuran / 2:.0f}

  Soal 5 memintamu menyimpulkan dari dua angka terakhir itu, lalu menjelaskan
  kenapa pasangan uji yang kamu susun sendiri punya cacat bawaan sebagai alat
  ukur.

  Sekarang sapuan ukuran korpus. Kosakatanya SENGAJA dipatok sama untuk semua
  baris, diambil dari korpus penuh, supaya yang berubah cuma satu hal: berapa
  banyak teks yang dibaca. Kalau kosakatanya ikut berubah, kamu tidak akan
  tahu mana yang menggerakkan angkanya.""")

    hit = Counter(token)
    besar = min(1200, len(hit))
    Vk = {w: i for i, w in enumerate(
        sorted(w for w, _ in hit.most_common(besar)))}

    print(f"\n  {'token dibaca':>14}{'pasangan':>10}{'median peringkat':>19}"
          f"{'acak':>8}")
    print("  " + "-" * 51)
    for bagian in (0.1, 0.25, 0.5, 1.0):
        n = int(len(token) * bagian)
        Ek = padatkan(ppmi(matriks_kookurensi(token[:n], Vk)), d=100)
        m, dp, u = peringkat_pasangan(Ek, Vk)
        print(f"  {n:>14}{dp:>10}{m:>19.0f}{u / 2:>8.0f}")

    print("""
  Kalau median peringkat masih turun di titik terakhir, korpusmu masih lapar
  dan menambah teks akan menolong. Kalau ia sudah mendatar, hambatanmu bukan
  jumlah teks.

  Angka pembanding yang perlu kamu tahu: GloVe dilatih pada 6 miliar token,
  word2vec asli pada 100 miliar. Korpusmu sekitar 150 ribu. Itu selisih empat
  sampai enam orde besaran, dan Soal 6 memintamu memperkirakan apa yang bisa
  dan tidak bisa ditebus oleh selisih sebesar itu.""")

    return E


# ══════════════════════════════════════════════════════════════
# BAGIAN 6 - lapisan embedding, dilatih ujung ke ujung
# ══════════════════════════════════════════════════════════════

def maju_embed(param, X):
    """Satu lintasan maju dengan lapisan embedding di depan.

    param : [E, W1, b1, W2, b2]
    X     : (B, V) vektor kantong kata, tiap baris sudah dinormalkan

    Susunannya:

        H0 = X @ E                 (B, d)   tanpa geseran, tanpa tekukan
        H1 = relu(H0 @ W1 + b1)    (B, n_h)
        out = H1 @ W2 + b2         (B, n_kelas)

    Baris pertama itu seluruh isi bagian ini, dan perlu kamu lihat pelan-pelan.

    Kalau X baris ke-i adalah vektor kantong kata untuk kalimat i, maka
    (X @ E)[i] = jumlah baris E untuk tiap kata yang hadir, ditimbang
    hitungannya. Kalau X sudah dinormalkan, itu rerata vektor kata. Jadi
    "lapisan embedding" yang terdengar canggih ternyata perkalian matriks
    biasa dengan vektor kantong.

    Pustaka sungguhan tidak menuliskannya sebagai perkalian matriks karena X
    hampir seluruhnya nol, dan mengambil baris langsung lewat indeks jauh lebih
    cepat. Tapi yang DIHITUNG sama persis. Tidak ada operasi baru, tidak ada
    aturan turunan baru. Kamu tidak perlu menambah apa pun ke `Tensor`.

    Kenapa H0 tidak pakai tekukan atau geseran: karena E memang cuma tabel
    pencarian. Menaruh relu di situ berarti separuh dimensi tiap vektor kata
    dipaksa nol, dan itu membuang informasi tanpa alasan.

    TODO 8
    """
    E, W1, b1, W2, b2 = param
    return ((Tensor(X) @ E @ W1 + b1).relu()) @ W2 + b2


def latih_embed(Xtr, ytr, Xva, yva, n_kelas, E0=None, d=100, n_h=48,
                lr=0.5, epoch=400, seed=0):
    """Latih model berembedding. Disediakan.

    `E0` adalah nilai awal matriks embedding. Kalau None, diisi acak. Kalau
    diberikan, itu vektor PPMI-SVD dari Bagian 5, dan inilah percobaan
    sesungguhnya di bagian ini: apakah memulai dari vektor yang sudah tahu
    sesuatu tentang bahasamu lebih baik daripada memulai dari acak.

    Inilah prapelatihan, dalam bentuknya yang paling telanjang. Yang dilakukan
    orang dengan BERT persis ini, cuma dengan korpus semiliar kali lebih besar
    dan arsitektur yang lebih rumit di atasnya.
    """
    rng = np.random.default_rng(seed)
    V = Xtr.shape[1]
    if E0 is None:
        E = rng.normal(0, 1, (V, d)) * (2 / V) ** 0.5
    else:
        E = E0.copy()
        d = E.shape[1]
    param = [
        Tensor(E),
        Tensor(rng.normal(0, 1, (d, n_h)) * (2 / d) ** 0.5),
        Tensor(np.zeros(n_h)),
        Tensor(rng.normal(0, 1, (n_h, n_kelas)) * (2 / n_h) ** 0.5),
        Tensor(np.zeros(n_kelas)),
    ]
    terbaik = None
    for e in range(epoch):
        rugi = maju_embed(param, Xtr).entropi_silang(ytr)
        for p in param:
            p.grad = np.zeros_like(p.data)
        rugi.backward()
        for p in param:
            p.data -= lr * p.grad
        if e % 10 == 0 or e == epoch - 1:
            av = (maju_embed(param, Xva).data.argmax(1) == yva).mean()
            if terbaik is None or av >= terbaik[0]:
                terbaik = (av, e, [p.data.copy() for p in param])
    for p, dd in zip(param, terbaik[2]):
        p.data = dd
    return param, terbaik


def bagian6(sint, nyata, kos_kata, V_korpus, E_korpus):
    print("\n" + GARIS,
          "\nBAGIAN 6  lapisan embedding, dilatih ujung ke ujung\n",
          GARIS, sep="")

    label = sorted({l for _, l in sint})
    L = {l: i for i, l in enumerate(label)}
    tr, va, _ = belah_tiga(sint, seed=0)
    ytr = np.array([L[l] for _, l in tr])
    yva = np.array([L[l] for _, l in va])
    yny = np.array([L[l] for _, l in nyata])

    Xtr = vektorkan([k for k, _ in tr], kos_kata)
    Xva = vektorkan([k for k, _ in va], kos_kata)
    Xny = vektorkan([k for k, _ in nyata], kos_kata)
    for X in (Xtr, Xva, Xny):
        panjang = X.sum(axis=1, keepdims=True)
        np.divide(X, panjang, out=X, where=panjang != 0)

    # Vektor awal untuk kata yang dikenal kosakata sintetis. Kata yang tidak
    # ada di korpus diisi nol, artinya "belum tahu apa-apa tentang kata ini".
    d = E_korpus.shape[1]
    E0 = np.zeros((len(kos_kata), d))
    ketemu = 0
    for kata, i in kos_kata.items():
        if kata in V_korpus:
            E0[i] = E_korpus[V_korpus[kata]]
            ketemu += 1
    print(f"  kosakata sintetis      : {len(kos_kata)}")
    print(f"  punya vektor dari korpus: {ketemu} = "
          f"{ketemu / len(kos_kata) * 100:.1f} persen\n")

    n = len(nyata)
    hasil = []
    for nama, awal in (("embedding acak", None),
                       ("embedding PPMI-SVD", E0)):
        p, t = latih_embed(Xtr, ytr, Xva, yva, len(L), E0=awal, seed=0)
        a = (maju_embed(p, Xny).data.argmax(1) == yny).mean()
        hasil.append((nama, t[0], a))

    print(f"  {'model':<22}{'validasi sintetis':>19}{'pesan nyata':>14}"
          f"{'selang 95 persen':>22}")
    print("  " + "-" * 76)
    for nama, av, a in hasil:
        _, b, t = selang_binomial(round(a * n), n)
        print(f"  {nama:<22}{av * 100:>18.1f}%{a * 100:>13.1f}%"
              f"{b * 100:>14.1f} .. {t * 100:.1f}")

    print("""
  Soal 7 memintamu menjelaskan kenapa kolom validasi sintetis nyaris tidak
  membedakan apa-apa antara dua baris ini, padahal keduanya berangkat dari
  titik yang sangat berbeda.""")

    return hasil


# ══════════════════════════════════════════════════════════════
# BAGIAN 7 - kalau bukan representasi, lalu apa
# ══════════════════════════════════════════════════════════════

# Intent yang benar-benar punya alat di synesis/alat.py, atau bisa dibuatkan
# alat tanpa model bahasa. Sisanya permintaan terbuka yang baru bisa dilayani
# LLM lokal di Bulan 6.
PUNYA_ALAT = {
    "buka_berkas", "cari_berkas", "info_sistem", "hitung", "jadwal",
    "jalankan_program", "kelola_repo", "kontrol_sistem", "pasang_paket",
    "ringkas_catatan",
}


def _siapkan(tr, va, te, L):
    """Kosakata dari latih saja, lalu vektorkan ketiganya. Disediakan."""
    kos = bangun_kosakata([x for x, _ in tr])
    X = [vektorkan([x for x, _ in b], kos) for b in (tr, va, te)]
    y = [np.array([L[l] for _, l in b]) for b in (tr, va, te)]
    return X, y


def bagian7(sint, nyata):
    print("\n" + GARIS,
          "\nBAGIAN 7  kalau bukan representasi, lalu apa\n", GARIS, sep="")

    print("""  Enam bagian sebelumnya menyerang satu variabel: cara kalimat diubah jadi
  angka. Bagian ini menyerang dua variabel lain, supaya kamu punya tiga titik
  pembanding dan bukan satu.

  Tuas A: berapa kalimat NYATA yang ikut dilatih.
  Tuas B: seberapa besar PORSI kalimat nyata itu di dalam gradien.
  Tuas C: apakah 15 kelasnya sendiri yang terlalu halus.

  Perhatikan bahwa di Tuas A dan B himpunan ujinya MENGECIL waktu k membesar,
  jadi selangnya melebar. Itu bukan cacat percobaan, itu harga yang memang
  kamu bayar kalau data nyatamu cuma 41.
""")

    label = sorted({l for _, l in sint})
    L = {l: i for i, l in enumerate(label)}
    tr_s, va_s, _ = belah_tiga(sint, seed=0)

    # Anggaran latih dipatok. Dua alasannya, dan keduanya soal kesahihan
    # percobaan, bukan soal kecepatan.
    #
    # Pertama, kalau data sintetismu tumbuh, mengulang 20 kalimat nyata
    # empat puluh kali tidak lagi menaikkan porsinya ke mana-mana. Di 750
    # kalimat sintetis, 20 x 40 itu 51,6 persen. Di 10.500 kalimat, angka
    # yang sama persis cuma 7,1 persen, dan Tuas B berhenti menguji apa pun.
    #
    # Kedua, `latih` di sini penurunan gradien satu bets penuh. Waktunya naik
    # sebanding jumlah kalimat, dan sapuan ini melatih dua puluh kali.
    if len(tr_s) > ANGGARAN_LATIH:
        acak = np.random.default_rng(7).permutation(len(tr_s))
        tr_s = [tr_s[i] for i in acak[:ANGGARAN_LATIH]]
        print(f"  Data latih sintetis dipotong ke {len(tr_s)} kalimat untuk\n"
              f"  bagian ini saja, supaya porsi di Tuas B bisa dicapai.\n")

    def coba(k, ulangi=1, n_ulang=5, seed0=100):
        skor = []
        for u in range(n_ulang):
            rng = np.random.default_rng(seed0 + u)
            urut = rng.permutation(len(nyata))
            ambil = [nyata[i] for i in urut[:k]]
            sisa = [nyata[i] for i in urut[k:]]
            if not sisa:
                continue
            tr = tr_s + ambil * ulangi
            X, y = _siapkan(tr, va_s, sisa, L)
            p, _ = latih(X[0], y[0], X[1], y[1], len(L), seed=u)
            skor.append((maju(p, X[2]).data.argmax(1) == y[2]).mean())
        return np.array(skor), len(tr_s) + k * ulangi

    print("  TUAS A  tambah kalimat nyata\n")
    print(f"  {'k nyata':>9}{'n uji':>8}{'rerata':>10}{'terburuk':>11}"
          f"{'terbaik':>10}")
    print("  " + "-" * 48)
    for k in (0, 5, 10, 15, 20):
        s, _ = coba(k)
        print(f"  {k:>9}{len(nyata) - k:>8}{s.mean() * 100:>9.1f}%"
              f"{s.min() * 100:>10.1f}%{s.max() * 100:>9.1f}%")

    print("\n  TUAS B  ulangi kalimat nyata supaya porsinya naik\n")
    print(f"  {'k nyata':>9}{'diulang':>9}{'n latih':>9}{'porsi':>8}"
          f"{'rerata':>10}{'terbaik':>10}")
    print("  " + "-" * 55)

    # Yang disapu porsinya, bukan pengalinya. Pengali yang dipatok bikin
    # percobaannya bergantung pada besar data sintetis, dan itu variabel
    # yang justru tidak sedang diuji di sini.
    k = 20
    capai = []
    for porsi in PORSI_TUAS_B:
        ulangi = max(1, round(porsi * len(tr_s) / (k * (1 - porsi))))
        sk, n_tr = coba(k, ulangi=ulangi, n_ulang=3)
        nyata_porsi = k * ulangi / n_tr
        capai.append(nyata_porsi)
        print(f"  {k:>9}{ulangi:>9}{n_tr:>9}{nyata_porsi * 100:>7.1f}%"
              f"{sk.mean() * 100:>9.1f}%{sk.max() * 100:>9.1f}%")

    print(f"""
  Kalau Tuas B mendatar juga, itu menutup satu penjelasan yang masuk akal.
  Dugaan yang wajar tadinya: {k} kalimat nyata di antara {len(tr_s)} sintetis
  cuma {k / (len(tr_s) + k) * 100:.1f} persen dari gradien, jadi tenggelam.
  Baris terakhir menaikkannya ke {capai[-1] * 100:.0f} persen. Kalau hasilnya
  tetap tidak bergerak, penjelasan itu salah dan boleh kamu buang.

  Perhatikan bahwa kolom porsi yang DICAPAI belum tentu sama dengan yang
  diminta, karena pengali harus bilangan bulat. Yang dibaca kolom capaiannya,
  bukan niatnya.

  TUAS C  gabungkan kelasnya
""")

    n = len(nyata)
    X, y = _siapkan(tr_s, va_s, nyata, L)
    p, _ = latih(X[0], y[0], X[1], y[1], len(L), seed=0)
    tebak = maju(p, X[2]).data.argmax(1)
    inv = {i: l for l, i in L.items()}

    benar15 = (tebak == y[2]).mean()
    alat_benar = np.array([inv[i] in PUNYA_ALAT for i in y[2]])
    alat_tebak = np.array([inv[i] in PUNYA_ALAT for i in tebak])
    benar2 = (alat_benar == alat_tebak).mean()
    dasar2 = max(alat_benar.mean(), 1 - alat_benar.mean())

    _, b15, a15 = selang_binomial(round(benar15 * n), n)
    _, b2, a2 = selang_binomial(round(benar2 * n), n)
    _, bd, ad = selang_binomial(round(dasar2 * n), n)

    print(f"  {'tugas':<30}{'akurasi':>9}{'selang 95 persen':>22}")
    print("  " + "-" * 61)
    print(f"  {'15 intent':<30}{benar15 * 100:>8.1f}%"
          f"{b15 * 100:>14.1f} .. {a15 * 100:.1f}")
    print(f"  {'2 kelas: alat atau LLM':<30}{benar2 * 100:>8.1f}%"
          f"{b2 * 100:>14.1f} .. {a2 * 100:.1f}")
    print(f"  {'dasar mayoritas 2 kelas':<30}{dasar2 * 100:>8.1f}%"
          f"{bd * 100:>14.1f} .. {ad * 100:.1f}")

    print(f"""
  Sekarang lihat komposisi pesan nyatanya, karena di situ kejutannya:

    pesan yang intentnya PUNYA alat  : {alat_benar.sum()} dari {n}
    pesan yang butuh model bahasa    : {(~alat_benar).sum()} dari {n}

  Bandingkan dua baris terakhir tabel di atas sebelum menyimpulkan apa pun
  tentang Tuas C.

  Dan bandingkan {alat_benar.sum()} dari {n} itu dengan Bagian 4 docs/Roadmap.md,
  yang saya tulis sendiri, dan yang menyatakan bahwa 80 sampai 90 persen
  pemakaian harian bisa ditangani pengklasifikasi tanpa LLM. Di sampel ini
  angkanya {alat_benar.sum() / n * 100:.0f} persen.

  Sebelum kamu membuang roadmap-nya, dua keberatan yang harus kamu timbang:

    1  41 pesan ini semuanya dari satu arsip, yaitu percakapan merancang
       proyek ini bersama agen pemrograman. Itu memang percakapan terbuka
       dari ujung ke ujung. Ia bukan sampel dari cara kamu akan memakai
       SYNESIS untuk membuka berkas praktikum.

    2  tapi arsip itu satu-satunya rekaman pemakaian nyata yang kamu punya,
       dan sampai ada yang lain, dialah bukti terbaik yang ada.

  Dua kalimat itu tidak saling membatalkan. Keduanya menunjuk ke kesimpulan
  yang sama: yang paling kurang dari Bulan 2 bukan representasi, bukan
  arsitektur, dan bukan jumlah epoch. Yang kurang adalah catatan pemakaian
  yang mewakili.

  Sesi 4 membangun alat pencatat itu, dan menjadikannya bagian dari SYNESIS
  sendiri, bukan skrip terpisah yang akan kamu lupakan.

  Soal 8 memintamu memutuskan apa yang dikerjakan setelah ini, dengan angka
  dari ketiga tuas sebagai alasannya.""")


# ══════════════════════════════════════════════════════════════
# Jalankan semuanya
# ══════════════════════════════════════════════════════════════

def main():
    mulai = time.perf_counter()

    sint = muat_perintah(DATA / "perintah_train_generated.txt")
    nyata = muat_perintah(DATA / "perintah_eval_real.txt")

    bagian1(nyata)
    kos_kata = bagian2(sint, nyata)
    bagian3(sint, nyata, kos_kata)

    token = kumpulkan_korpus()
    V_korpus, M = bagian4(token)
    E_korpus = bagian5(token, V_korpus, M)
    bagian6(sint, nyata, kos_kata, V_korpus, E_korpus)
    bagian7(sint, nyata)

    print(f"\n{GARIS}")
    print(f"  selesai dalam {time.perf_counter() - mulai:.1f} detik")
    print(GARIS)


if __name__ == "__main__":
    main()
