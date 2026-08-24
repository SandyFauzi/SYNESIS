"""Bulan 2 Sesi 2 - dari pengklasifikasi mainan ke intent classifier SYNESIS.

Jalankan:
    . .\\scripts\\activate.ps1
    python notebooks\\bulan2_sesi2_intent.py

Atau pakai berkas data lain:
    python notebooks\\bulan2_sesi2_intent.py data\\bulan2\\perintah_train_generated.txt

Sesi 1 berhenti di tempat yang enak dan menipu: akurasi 100 persen di enam
kelas, tanpa satu pun data uji. Soal 6c waktu itu memintamu menyebut kenapa
itu cacat. Malam ini cacatnya diperbaiki, dan gantinya kamu dapat angka yang
jauh lebih kecil tapi berarti.

Yang baru:

    1  data perintah sungguhan, yang kamu tulis sendiri
    2  belah tiga: latih, validasi, uji
    3  TF-IDF, dan apakah ia benar-benar menolong
    4  matriks bingung, presisi, recall
    5  ambang "tidak tahu", karena salah tebak itu mahal
    6  ekstraksi slot: perintah jadi argumen

Yang TIDAK baru, dan itu disengaja: mesin belajarnya. Kelas `Tensor` yang kamu
tulis untuk MNIST dipakai apa adanya di sini. Tidak ada satu baris pun kode
autograd baru. Gambar 784 piksel diganti kalimat, sisanya identik.

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

GARIS = "=" * 66


# ══════════════════════════════════════════════════════════════
# Data
# ══════════════════════════════════════════════════════════════

def muat_perintah(berkas=None):
    """Baca data bawaan atau berkas ``label | kalimat``."""
    sumber = Path(berkas).read_text(encoding="utf-8") if berkas else PERINTAH
    pasang = []
    for baris in sumber.strip().splitlines():
        baris = baris.strip()
        if not baris or baris.startswith("#"):
            continue
        label, kalimat = baris.split("|", 1)
        pasang.append((kalimat.strip().lower(), label.strip()))
    return pasang


def belah_tiga(pasang, seed=0, bagian=(0.7, 0.15, 0.15)):
    """Belah jadi latih, validasi, uji, dengan proporsi kelas dijaga.

    Kenapa proporsi kelas harus dijaga (namanya stratified): kalau kamu
    membelah acak begitu saja, kelas yang cuma punya 15 contoh bisa saja
    tidak kebagian satu pun di himpunan uji. Akurasi uji lalu melaporkan
    sesuatu tentang kelas yang tidak diujinya.

    Kembalikan tiga daftar berisi (kalimat, label).

    Petunjuknya: kelompokkan dulu per label, acak di dalam tiap kelompok,
    baru potong menurut proporsi. Pakai `np.random.default_rng(seed)` supaya
    hasilnya bisa diulang.

    TODO 1
    """
    if not np.isclose(sum(bagian), 1.0):
        raise ValueError("jumlah proporsi belahan harus 1")

    kelompok = {}
    for contoh in pasang:
        kelompok.setdefault(contoh[1], []).append(contoh)

    rng = np.random.default_rng(seed)
    latih, sah, uji = [], [], []
    for label in sorted(kelompok):
        contoh = kelompok[label]
        urut = rng.permutation(len(contoh))
        n_latih = int(len(contoh) * bagian[0])
        n_sah = int(len(contoh) * bagian[1])
        latih.extend(contoh[i] for i in urut[:n_latih])
        sah.extend(contoh[i] for i in urut[n_latih:n_latih + n_sah])
        uji.extend(contoh[i] for i in urut[n_latih + n_sah:])
    return latih, sah, uji


# ══════════════════════════════════════════════════════════════
# BAGIAN 1 - lihat datanya dulu
# ══════════════════════════════════════════════════════════════

def bagian1(pasang, latih, sah, uji):
    print(GARIS, "\nBAGIAN 1  datanya dulu, sebelum apa pun\n", GARIS, sep="")

    hitung = Counter(l for _, l in pasang)
    print(f"  total perintah : {len(pasang)}")
    print(f"  jumlah kelas   : {len(hitung)}")
    print(f"  belahan        : latih {len(latih)}, validasi {len(sah)}, "
          f"uji {len(uji)}\n")

    print(f"  {'intent':<18}{'semua':>7}{'latih':>7}{'sah':>6}{'uji':>6}")
    print("  " + "-" * 44)
    hl, hs, hu = (Counter(l for _, l in b) for b in (latih, sah, uji))
    for label in sorted(hitung):
        print(f"  {label:<18}{hitung[label]:>7}{hl[label]:>7}"
              f"{hs[label]:>6}{hu[label]:>6}")

    n_uji = len(uji)
    sigma = (0.9 * 0.1 / n_uji) ** 0.5
    print(f"""
  Sekarang bagian yang tidak enak.

  Himpunan ujimu berisi {n_uji} kalimat. Kalau akurasi sebenarnya 90 persen,
  simpangan baku hasil pengukuranmu adalah

      sqrt(0.9 * 0.1 / {n_uji}) = {sigma:.4f}, yaitu {sigma * 100:.1f} poin persen

  Selang kepercayaan 95 persennya kira-kira dua kali itu ke tiap arah, jadi
  {sigma * 200:.0f} poin persen. Artinya "akurasi 90 persen" yang kamu ukur
  di sini sebenarnya berarti "antara {90 - sigma * 200:.0f} dan
  {min(100, 90 + sigma * 200):.0f} persen".

  Itu bukan pengukuran, itu tebakan berpakaian rapi.

  Satu-satunya obatnya menambah data. Soal 1 memintamu menghitung berapa
  kalimat yang kamu butuhkan supaya selangnya menyempit jadi 5 poin persen,
  lalu menulis sebanyak itu. Rencana Bulan 2 menyebut angka 300 sampai 500,
  dan angka itu bukan diambil dari langit.""")


# ══════════════════════════════════════════════════════════════
# BAGIAN 2 - hitung kata lawan TF-IDF
# ══════════════════════════════════════════════════════════════

def bangun_kosakata(kalimat):
    """Kumpulkan semua kata unik, urut alfabet. Disediakan.

    Sama seperti Sesi 1, cuma sekarang membaca dari daftar kalimat latih saja.
    Membangunnya dari seluruh data termasuk uji itu kebocoran, dan Soal 2
    memintamu menjelaskan kebocoran macam apa.
    """
    kata = set()
    for k in kalimat:
        kata.update(re.findall(r"[a-z0-9]+", k))
    return {k: i for i, k in enumerate(sorted(kata))}


def bobot_idf(kalimat, kosakata):
    """Hitung bobot IDF tiap kata dari himpunan latih.

        idf(kata) = log( (1 + N) / (1 + df(kata)) ) + 1

    dengan N jumlah kalimat dan df jumlah kalimat yang memuat kata itu.
    Tambahan 1 di dua tempat itu penghalus, supaya kata yang muncul di semua
    kalimat tidak berbobot nol dan kata yang tak pernah muncul tidak membagi
    nol.

    Gagasannya satu kalimat: kata yang muncul di mana-mana tidak membedakan
    apa-apa, jadi bobotnya dikecilkan. Kata "buka" muncul di hampir semua
    perintah membuka berkas DAN membuka aplikasi, jadi ia hampir tidak
    berguna. Kata "volume" cuma muncul di satu kelas, jadi ia sangat berguna.

    Kembalikan array berbentuk (len(kosakata),).

    TODO 2
    """
    df = np.zeros(len(kosakata))
    for teks in kalimat:
        for kata in set(re.findall(r"[a-z0-9]+", teks.lower())):
            if kata in kosakata:
                df[kosakata[kata]] += 1
    return np.log((1 + len(kalimat)) / (1 + df)) + 1


def vektorkan(kalimat, kosakata, idf=None):
    """Ubah daftar kalimat jadi matriks (n_kalimat, n_kosakata).

    Kalau `idf` None, isinya hitung kata mentah, persis Sesi 1.
    Kalau `idf` diberikan, tiap hitungan dikalikan bobot IDF-nya, lalu tiap
    baris dinormalkan jadi panjang 1.

    Normalisasi baris itu penting dan gampang dilupakan. Tanpa itu, kalimat
    panjang otomatis punya vektor lebih besar, dan modelmu belajar bahwa
    "perintah panjang" itu sendiri sebuah petunjuk. Itu bukan yang kamu mau.

    Kata yang tidak ada di kosakata diabaikan begitu saja.

    TODO 3
    """
    X = np.zeros((len(kalimat), len(kosakata)))
    for i, teks in enumerate(kalimat):
        for kata in re.findall(r"[a-z0-9]+", teks.lower()):
            if kata in kosakata:
                X[i, kosakata[kata]] += 1

    if idf is not None:
        X *= idf
        panjang = np.linalg.norm(X, axis=1, keepdims=True)
        np.divide(X, panjang, out=X, where=panjang != 0)
    return X


def bagian2(latih, sah, kos, idf):
    print("\n" + GARIS, "\nBAGIAN 2  hitung kata lawan TF-IDF\n", GARIS, sep="")

    kal = [k for k, _ in latih]
    Xa = vektorkan(kal, kos)
    Xb = vektorkan(kal, kos, idf)

    urut = np.argsort(idf)
    balik = {i: k for k, i in kos.items()}
    print("  Sepuluh kata dengan IDF terendah, yaitu yang paling tidak berguna:")
    print("    " + ", ".join(f"{balik[i]} ({idf[i]:.2f})" for i in urut[:10]))
    print("\n  Sepuluh kata dengan IDF tertinggi:")
    print("    " + ", ".join(f"{balik[i]} ({idf[i]:.2f})" for i in urut[-10:]))

    print(f"""
  bentuk matriks       : {Xa.shape}
  persen nol           : {(Xa == 0).mean() * 100:.1f} persen
  nilai maks hitung    : {Xa.max():.2f}
  nilai maks TF-IDF    : {Xb.max():.2f}
  panjang baris TF-IDF : {np.linalg.norm(Xb, axis=1).min():.4f} sampai """
          f"""{np.linalg.norm(Xb, axis=1).max():.4f}

  Baris terakhir itu uji cepat untuk TODO 3-mu. Kalau normalisasinya benar,
  semua baris berpanjang tepat 1.

  Apakah TF-IDF benar-benar menolong di sini, itu diukur di Bagian 3, bukan
  diyakini. Sesi 1 sudah mengajarimu bahwa demonstrasi yang tidak bisa gagal
  itu tidak membuktikan apa-apa.""")
    return Xa, Xb


# ══════════════════════════════════════════════════════════════
# BAGIAN 3 - latih, pakai mesin MNIST yang sama
# ══════════════════════════════════════════════════════════════

def latih(Xtr, ytr, Xva, yva, n_kelas, n_h=48, lr=0.5, epoch=400, seed=0,
          kabar=0):
    """Latih MLP satu lapisan tersembunyi. Disediakan.

    Perhatikan apa yang TIDAK ada di sini: kelas model baru, aturan turunan
    baru, gelung backward baru. `Tensor` dan `maju` diimpor apa adanya dari
    Bulan 1 Sesi 3+4. Yang berubah cuma bentuk masukannya.
    """
    rng = np.random.default_rng(seed)
    n_f = Xtr.shape[1]
    param = [
        Tensor(rng.normal(0, 1, (n_f, n_h)) * (2 / n_f) ** 0.5),
        Tensor(np.zeros(n_h)),
        Tensor(rng.normal(0, 1, (n_h, n_kelas)) * (2 / n_h) ** 0.5),
        Tensor(np.zeros(n_kelas)),
    ]
    terbaik = None
    for e in range(epoch):
        rugi = maju(param, Xtr).entropi_silang(ytr)
        for p in param:
            p.grad = np.zeros_like(p.data)
        rugi.backward()
        for p in param:
            p.data -= lr * p.grad
        if e % 10 == 0 or e == epoch - 1:
            av = (maju(param, Xva).data.argmax(1) == yva).mean()
            if terbaik is None or av >= terbaik[0]:
                terbaik = (av, e, [p.data.copy() for p in param])
            if kabar and e % kabar == 0:
                print(f"    epoch {e:>4}   rugi {rugi.data:.4f}   "
                      f"validasi {av * 100:5.1f} persen")
    for p, d in zip(param, terbaik[2]):
        p.data = d
    return param, terbaik


def bagian3(pasang, kos_awal, label2i, n_seed=8):
    print("\n" + GARIS, "\nBAGIAN 3  dua resep fitur, diadu delapan kali\n",
          GARIS, sep="")

    n_k = len(label2i)
    kumpul = {"hitung kata": [], "TF-IDF": []}
    simpan = {}

    for seed in range(n_seed):
        tr, va, te = belah_tiga(pasang, seed=seed)
        kos = bangun_kosakata([k for k, _ in tr])
        idf = bobot_idf([k for k, _ in tr], kos)
        ytr = np.array([label2i[l] for _, l in tr])
        yva = np.array([label2i[l] for _, l in va])
        yte = np.array([label2i[l] for _, l in te])

        for nama, pakai in (("hitung kata", None), ("TF-IDF", idf)):
            Xtr = vektorkan([k for k, _ in tr], kos, pakai)
            Xva = vektorkan([k for k, _ in va], kos, pakai)
            Xte = vektorkan([k for k, _ in te], kos, pakai)
            param, _ = latih(Xtr, ytr, Xva, yva, n_k, seed=seed)
            kumpul[nama].append(
                ((maju(param, Xva).data.argmax(1) == yva).mean(),
                 (maju(param, Xte).data.argmax(1) == yte).mean()))
            if seed == 0:
                simpan[nama] = (param, pakai, kos, idf, (tr, va, te),
                                (ytr, yva, yte))

    print(f"  {'fitur':<12}{'validasi rata2':>17}{'uji rata2':>13}"
          f"{'uji terburuk':>15}{'uji terbaik':>14}")
    print("  " + "-" * 71)
    rerata = {}
    for nama, baris in kumpul.items():
        va = np.array([b[0] for b in baris])
        te = np.array([b[1] for b in baris])
        rerata[nama] = va.mean()
        print(f"  {nama:<12}{va.mean() * 100:>16.1f}%{te.mean() * 100:>12.1f}%"
              f"{te.min() * 100:>14.1f}%{te.max() * 100:>13.1f}%")

    pilih = max(rerata, key=rerata.get)
    selisih = abs(rerata['hitung kata'] - rerata['TF-IDF']) * 100
    lebar = max(np.ptp([b[1] for b in baris]) for baris in kumpul.values()) * 100
    print(f"""
  Delapan belahan, bukan satu. Lihat dua kolom terakhir: data dan kode sama
  persis, yang berubah cuma kalimat mana yang kebetulan masuk himpunan uji,
  dan hasilnya merentang sejauh {lebar:.0f} poin persen.

  Sekarang bandingkan dengan selisih antar-resep: {selisih:.1f} poin persen.

  Selisih yang mau kamu ukur jauh lebih kecil daripada derau alatmu. Artinya
  percobaan ini TIDAK BISA memutuskan resep mana yang lebih baik, dan jawaban
  yang benar untuk Soal 3 adalah mengatakan itu, bukan memilih yang angkanya
  kebetulan lebih besar.

  Ini bentuk yang sama dengan galat pengukuran di praktikum. Kalau ralatmu
  0,5 dan selisih dua bahan 0,1, kamu tidak menyimpulkan bahan mana yang
  lebih baik. Kamu menyimpulkan bahwa alatmu kurang teliti.

  Yang dipakai selanjutnya: {pilih}, dan alasannya bukan akurasi.
  Soal 3 memintamu menyebut alasan yang benar.""")

    param, pakai, kos, idf, belah, ys = simpan[pilih]
    return pilih, param, pakai, kos, idf, belah, ys


# ══════════════════════════════════════════════════════════════
# BAGIAN 4 - matriks bingung
# ══════════════════════════════════════════════════════════════

def matriks_bingung(benar, tebak, n_kelas):
    """Kembalikan matriks (n_kelas, n_kelas) dengan

        M[i, j] = berapa kali kelas sebenarnya i ditebak sebagai j

    Diagonalnya yang benar. Yang di luar diagonal itu daftar kesalahanmu,
    dan bentuk sebarannya jauh lebih berguna daripada satu angka akurasi.

    TODO 4
    """
    M = np.zeros((n_kelas, n_kelas), dtype=int)
    np.add.at(M, (benar, tebak), 1)
    return M


def presisi_recall(M):
    """Dari matriks bingung, hitung presisi dan recall tiap kelas.

        recall[i]  = M[i, i] / jumlah baris i      seberapa banyak yang
                                                   ketemu dari yang ada
        presisi[i] = M[i, i] / jumlah kolom i      seberapa banyak yang benar
                                                   dari yang diklaim

    Bedanya penting dan sering tertukar. Untuk SYNESIS, presisi kelas
    `kontrol_sistem` jauh lebih mahal daripada recall-nya: gagal mengenali
    "matikan komputer" cuma bikin kesal, salah mengira kalimat lain sebagai
    "matikan komputer" bikin pekerjaanmu hilang.

    Hati-hati pembagian nol untuk kelas yang tidak pernah ditebak sama sekali.

    Kembalikan (presisi, recall), dua array berpanjang n_kelas.

    TODO 5
    """
    benar = np.diag(M)
    presisi = np.divide(benar, M.sum(axis=0), out=np.zeros_like(benar, dtype=float),
                        where=M.sum(axis=0) != 0)
    recall = np.divide(benar, M.sum(axis=1), out=np.zeros_like(benar, dtype=float),
                       where=M.sum(axis=1) != 0)
    return presisi, recall


def bagian4(nama, param, pakai_idf, kos, label2i, uji_set, yte):
    print("\n" + GARIS, "\nBAGIAN 4  matriks bingung, presisi, recall\n",
          GARIS, sep="")

    Xte = vektorkan([k for k, _ in uji_set], kos, pakai_idf)
    tebak = maju(param, Xte).data.argmax(1)

    label = [l for l, _ in sorted(label2i.items(), key=lambda kv: kv[1])]
    M = matriks_bingung(yte, tebak, len(label))

    print(f"  fitur dipakai : {nama}, belahan seed 0\n")
    print("  baris = sebenarnya, kolom = tebakan\n")
    print(" " * 20 + "".join(f"{l[:6]:>8}" for l in label))
    for i, l in enumerate(label):
        print(f"  {l:<18}" + "".join(
            f"{M[i, j]:>8}" if i != j else f"{('[' + str(M[i, j]) + ']'):>8}"
            for j in range(len(label))))

    p, r = presisi_recall(M)
    print(f"\n  {'intent':<18}{'presisi':>10}{'recall':>10}{'dukungan':>11}")
    print("  " + "-" * 49)
    for i, l in enumerate(label):
        print(f"  {l:<18}{p[i] * 100:>9.1f}%{r[i] * 100:>9.1f}%"
              f"{M[i].sum():>11}")

    print("""
  Angka dalam kurung siku itu diagonalnya, yang benar. Selain itu kesalahan.

  Lihat pasangan mana yang paling sering tertukar. Biasanya bukan pasangan
  acak: ia dua kelas yang memang berbagi kata. Soal 4 memintamu menyebut
  pasangan terburuk di matriksmu, membuka kalimat-kalimatnya, dan memutuskan
  apakah itu masalah model atau masalah data.

  Kalau dua kelas hampir selalu tertukar dan kalimatnya memang mirip, model
  yang lebih besar tidak akan menolong. Yang menolong: tulis lebih banyak
  contoh yang membedakan keduanya, atau gabungkan keduanya jadi satu intent
  karena ternyata memang satu.""")
    return tebak, label


# ══════════════════════════════════════════════════════════════
# BAGIAN 5 - ambang tidak tahu
# ══════════════════════════════════════════════════════════════

AMBANG_INTENT = {
    "buka_berkas": 0.55,
    "cari_berkas": 0.40,
    "hitung": 0.60,
    "info_sistem": 0.50,
    "jadwal": 0.85,
    "jalankan_program": 0.85,
    "jelaskan_konsep": 0.40,
    "kelola_repo": 0.90,
    "kontrol_sistem": 0.90,
    "lanjut_tugas": 0.65,
    "obrol": 0.30,
    "pasang_paket": 0.90,
    "ringkas_catatan": 0.55,
    "tanya_umum": 0.30,
    "ubah_proyek": 0.85,
}


def tebak_dengan_ambang(param, X, ambang):
    """Kembalikan array indeks kelas, atau -1 kalau modelnya kurang yakin.

    Hitung softmax dari keluaran `maju`, ambil peluang tertinggi tiap baris.
    Kalau peluang tertinggi itu di bawah `ambang`, kembalikan -1 untuk baris
    tersebut, yang artinya "tidak tahu".

    Ini satu-satunya cara pengklasifikasi boleh menolak menjawab, dan tanpa
    itu ia akan menebak kelas terdekat untuk kalimat apa pun, termasuk
    kalimat yang tidak ada hubungannya dengan satu pun intentmu.

    TODO 6
    """
    logit = maju(param, X).data
    eksponen = np.exp(logit - logit.max(axis=1, keepdims=True))
    peluang = eksponen / eksponen.sum(axis=1, keepdims=True)
    tebak = peluang.argmax(axis=1)
    batas = np.asarray(ambang)
    if batas.ndim:
        batas = batas[tebak]
    tebak[peluang.max(axis=1) < batas] = -1
    return tebak


def bagian5(param, pakai_idf, kos, label2i, uji_set, yte):
    print("\n" + GARIS, "\nBAGIAN 5  ambang tidak tahu\n", GARIS, sep="")

    Xte = vektorkan([k for k, _ in uji_set], kos, pakai_idf)

    asing = ["fotosintesis pada tumbuhan hijau",
             "harga saham bank besok naik atau turun",
             "resep rendang padang yang enak",
             "siapa presiden pertama republik indonesia",
             "wkwkwk anjay mabar dulu gak"]
    Xas = vektorkan(asing, kos, pakai_idf)

    print(f"  {'ambang':>8}{'benar':>10}{'salah':>9}{'menolak':>10}"
          f"{'asing ditolak':>16}")
    print("  " + "-" * 53)
    for ambang in (0.0, 0.3, 0.5, 0.7, 0.9, 0.99):
        t = tebak_dengan_ambang(param, Xte, ambang)
        ta = tebak_dengan_ambang(param, Xas, ambang)
        benar = int((t == yte).sum())
        tolak = int((t == -1).sum())
        salah = len(yte) - benar - tolak
        print(f"  {ambang:>8.2f}{benar:>10}{salah:>9}{tolak:>10}"
              f"{f'{int((ta == -1).sum())} dari {len(asing)}':>16}")

    nama_label = [n for n, _ in sorted(label2i.items(), key=lambda kv: kv[1])]
    per_intent = np.array([AMBANG_INTENT.get(n, 0.60) for n in nama_label])
    t = tebak_dengan_ambang(param, Xte, per_intent)
    ta = tebak_dengan_ambang(param, Xas, per_intent)
    benar = int((t == yte).sum())
    tolak = int((t == -1).sum())
    salah = len(yte) - benar - tolak
    print(f"  {'per kelas':>8}{benar:>10}{salah:>9}{tolak:>10}"
          f"{f'{int((ta == -1).sum())} dari {len(asing)}':>16}")

    print("""
  Kolom terakhir kalimat yang sama sekali di luar semua intentmu. Model tanpa
  ambang akan memaksakan salah satu kelas untuk kelimanya, dengan keyakinan
  yang sering tinggi. Itu bukan bug, itu memang yang softmax lakukan: ia
  membagi peluang di antara kelas yang ADA, dan tidak punya cara menyatakan
  "bukan salah satu dari ini".

  Naikkan ambang dan penolakan bertambah, tapi jawaban benar ikut hilang.
  Tidak ada nilai yang benar untuk semua kelas. Soal 5 memintamu memilih
  ambang berbeda per intent, dan menjelaskan kenapa `kontrol_sistem` pantas
  dapat ambang lebih tinggi daripada `obrol`.""")


# ══════════════════════════════════════════════════════════════
# BAGIAN 6 - perintah jadi argumen
# ══════════════════════════════════════════════════════════════

WAKTU = {
    "hari ini": 0, "sekarang": 0, "kemarin": -1, "besok": 1, "lusa": 2,
    "minggu lalu": -7, "minggu depan": 7, "bulan lalu": -30, "bulan depan": 30,
    "tadi pagi": 0, "tadi malam": -1,
}


def ekstrak_slot(kalimat):
    """Ambil argumen dari kalimat perintah.

    Kembalikan dict yang boleh berisi kunci berikut, dan hanya yang ketemu:

        "waktu"  : geseran hari sebagai bilangan bulat, dari tabel WAKTU
        "jam"    : "03:00" dari "jam tiga" atau "jam 3", dan "15:00" dari
                   "jam 3 sore" atau "jam 15". Kalau tidak ada penanda
                   sore atau malam, JANGAN menebak. Soal 7 membahas
                   kenapa menebak di sini berbahaya.
        "objek"  : sisa kalimat sesudah kata kerja perintah dibuang

    Ini sengaja BUKAN pembelajaran mesin. Untuk slot sebanyak ini, aturan
    tangan lebih akurat, lebih cepat, dan bisa kamu perbaiki dalam sepuluh
    detik waktu ia salah. Menaruh jaringan saraf di sini akan terasa canggih
    dan bekerja lebih buruk.

    Kapan aturan tangan berhenti cukup, itu Soal 6.

    Mulai sederhana. Cocokkan frasa WAKTU yang terpanjang dulu, karena
    "minggu lalu" mengandung "lalu" dan kamu tidak mau yang pendek menang.

    TODO 7
    """
    teks = kalimat.lower().strip()
    slot = {}

    for frasa in sorted(WAKTU, key=len, reverse=True):
        pola = rf"\b{re.escape(frasa)}\b"
        if re.search(pola, teks):
            slot["waktu"] = WAKTU[frasa]
            teks = re.sub(pola, " ", teks, count=1)
            break

    angka = {
        "satu": 1, "dua": 2, "tiga": 3, "empat": 4, "lima": 5,
        "enam": 6, "tujuh": 7, "delapan": 8, "sembilan": 9,
        "sepuluh": 10, "sebelas": 11, "dua belas": 12,
    }
    cocok = re.search(
        r"\bjam\s+(dua belas|sebelas|sepuluh|sembilan|delapan|tujuh|enam|"
        r"lima|empat|tiga|dua|satu|[0-9]{1,2})(?:\s+(pagi|siang|sore|malam))?\b",
        teks,
    )
    if cocok:
        mentah, penanda = cocok.groups()
        jam = angka.get(mentah, int(mentah) if mentah.isdigit() else 0)
        if penanda in {"siang", "sore", "malam"} and 1 <= jam < 12:
            jam += 12
        if 0 <= jam <= 23:
            slot["jam"] = f"{jam:02d}:00"
        teks = teks[:cocok.start()] + " " + teks[cocok.end():]

    teks = re.sub(
        r"^(?:tolong\s+)?(?:buka(?:in|kan)?|tampilkan|cari(?:in|kan)?|temukan|"
        r"ingatkan(?:\s+aku)?|jadwalkan|setel)\b",
        "",
        teks,
    )
    objek = " ".join(teks.split())
    if objek:
        slot["objek"] = objek
    return slot


def bagian6():
    print("\n" + GARIS, "\nBAGIAN 6  perintah jadi argumen\n", GARIS, sep="")

    contoh = [
        "buka laporan praktikum minggu lalu",
        "ingatkan aku rapat jam tiga",
        "cari file tugas mekanika kemarin",
        "jadwalkan praktikum besok pagi",
        "buka vscode",
        "setel alarm jam 6",
    ]
    print(f"  {'kalimat':<40}{'slot yang terambil'}")
    print("  " + "-" * 70)
    for k in contoh:
        print(f"  {k:<40}{ekstrak_slot(k)}")

    print("""
  Intent memberi tahu FUNGSI mana yang dipanggil. Slot memberi tahu ARGUMEN
  apa yang dikirim. Tanpa keduanya kamu belum punya perintah, baru punya
  kategori.

  Perhatikan bahwa "buka vscode" tidak punya slot waktu, dan itu benar. Slot
  yang tidak ada tidak boleh ditebak. Mengarang nilai bawaan untuk slot yang
  tidak disebutkan pengguna adalah cara tercepat membuat asisten yang
  menakutkan.""")


# ══════════════════════════════════════════════════════════════
# BAGIAN 7 - ongkos
# ══════════════════════════════════════════════════════════════

def bagian7(param, pakai_idf, kos, uji_set):
    print("\n" + GARIS, "\nBAGIAN 7  ongkos satu perintah\n", GARIS, sep="")

    kal = [k for k, _ in uji_set] * 40

    t0 = time.perf_counter()
    X = vektorkan(kal, kos, pakai_idf)
    t1 = time.perf_counter()
    maju(param, X).data.argmax(1)
    t2 = time.perf_counter()

    n = len(kal)
    byte = sum(p.data.nbytes for p in param)
    print(f"  perintah diproses      : {n}")
    print(f"  vektorkan              : {(t1 - t0) / n * 1e6:.1f} mikrodetik "
          f"per perintah")
    print(f"  maju + argmax          : {(t2 - t1) / n * 1e6:.1f} mikrodetik "
          f"per perintah")
    print(f"  total                  : {(t2 - t0) / n * 1e3:.3f} milidetik "
          f"per perintah")
    print(f"  ukuran model           : {byte / 1024:.1f} KB")
    print(f"  parameter              : {sum(p.data.size for p in param):,}"
          .replace(",", "."))

    print(f"""
  Bandingkan dengan angka yang kamu ukur di Bagian 6 Sesi 1, dan dengan model
  bahasa 3B yang butuh sekitar 1.900.000 KB cuma untuk dimuat.

  Ini yang dimaksud rencana Bulan 2 waktu bilang SYNESIS v0.1 sudah berguna
  tanpa satu pun LLM. Perintah yang kamu ketik tiap hari bukan masalah
  penalaran bahasa. Ia masalah klasifikasi {param[-1].data.size} kelas dengan kosakata
  {len(kos)} kata, dan itu selesai dalam waktu di atas.

  Soal 8 memintamu memutuskan di mana batasnya: perintah macam apa yang
  BENAR-BENAR butuh LLM, dan kenapa memaksakannya ke pengklasifikasi ini akan
  gagal dengan cara yang tidak kelihatan.""")


# ══════════════════════════════════════════════════════════════
# Data perintah. Tambah barismu sendiri di sini.
#
# Format:  label | kalimat
#
# Rencana Bulan 2 menyebut 300 sampai 500 contoh. Yang ada di bawah ini 120,
# dan Bagian 1 akan menunjukkan padamu kenapa 120 tidak cukup. Menambahnya
# adalah pekerjaanmu, bukan pekerjaan saya, karena yang harus masuk ke sini
# adalah kalimat yang MEMANG kamu ucapkan, bukan kalimat yang saya bayangkan.
# ══════════════════════════════════════════════════════════════

PERINTAH = """
buka_berkas | buka laporan praktikum minggu lalu
buka_berkas | bukain file tugas fisika
buka_berkas | tolong buka dokumen skripsi
buka_berkas | buka folder unduhan
buka_berkas | bukakan catatan kuliah kemarin
buka_berkas | buka pdf modul dsp
buka_berkas | tampilkan berkas anggaran bulan ini
buka_berkas | buka gambar hasil simulasi
buka_berkas | bukain slide presentasi tadi pagi
buka_berkas | buka file excel jadwal
buka_berkas | buka readme proyek synesis
buka_berkas | tolong bukakan laporan mingguan
buka_berkas | buka dokumen yang aku edit kemarin
buka_berkas | buka folder video
buka_berkas | buka catatan rapat

cari_berkas | cari file laporan praktikum
cari_berkas | carikan dokumen yang ada kata gelombang
cari_berkas | cari semua pdf di folder kuliah
cari_berkas | di mana file tugas mekanika
cari_berkas | temukan berkas yang aku simpan minggu lalu
cari_berkas | cari foto praktikum
cari_berkas | cariin skrip python yang pakai numpy
cari_berkas | cari catatan tentang fourier
cari_berkas | daftar file yang berubah hari ini
cari_berkas | cari file berukuran lebih dari seratus mb
cari_berkas | temukan folder proyek synesis
cari_berkas | cari berkas bernama modul
cari_berkas | carikan semua csv di folder data
cari_berkas | cari file yang hilang kemarin
cari_berkas | di mana aku simpan laporan itu

ringkas_catatan | ringkas catatan kuliah fisika statistik
ringkas_catatan | rangkum isi laporan praktikum
ringkas_catatan | apa isi dokumen modul dsp
ringkas_catatan | ringkasin notulen rapat kemarin
ringkas_catatan | jelaskan isi catatan gelombang
ringkas_catatan | buat ringkasan bab tiga
ringkas_catatan | rangkumkan pdf yang barusan dibuka
ringkas_catatan | apa poin penting di catatan minggu ini
ringkas_catatan | ringkas semua catatan bulan ini
ringkas_catatan | tolong rangkum artikel yang aku simpan
ringkas_catatan | ringkas hasil eksperimen
ringkas_catatan | rangkum isi folder kuliah
ringkas_catatan | apa kesimpulan laporan itu
ringkas_catatan | ringkas catatan termodinamika
ringkas_catatan | buatkan intisari dokumen ini

jalankan_program | buka vscode
jalankan_program | jalankan blender
jalankan_program | nyalakan spotify
jalankan_program | buka peramban
jalankan_program | jalankan jupyter notebook
jalankan_program | buka terminal
jalankan_program | jalankan ollama
jalankan_program | jalankan simulasi python
jalankan_program | buka kalkulator
jalankan_program | nyalakan discord
jalankan_program | jalankan skrip latihan
jalankan_program | buka steam
jalankan_program | jalankan matlab
jalankan_program | buka aplikasi catatan
jalankan_program | jalankan minecraft

kontrol_sistem | kecilkan volume
kontrol_sistem | naikkan kecerahan layar
kontrol_sistem | matikan wifi
kontrol_sistem | nyalakan bluetooth
kontrol_sistem | kunci layar
kontrol_sistem | matikan komputer
kontrol_sistem | mulai ulang laptop
kontrol_sistem | besarkan suara
kontrol_sistem | aktifkan mode pesawat
kontrol_sistem | matikan suara
kontrol_sistem | ubah ke mode hemat baterai
kontrol_sistem | tutup semua aplikasi
kontrol_sistem | tidurkan komputer sekarang
kontrol_sistem | naikkan volume jadi lima puluh
kontrol_sistem | matikan layar

jadwal | ingatkan aku rapat jam tiga
jadwal | jadwalkan praktikum besok pagi
jadwal | apa agenda hari ini
jadwal | ingatkan minum obat tiap malam
jadwal | tambah acara ujian minggu depan
jadwal | jam berapa kelas fisika besok
jadwal | setel alarm jam enam
jadwal | hapus jadwal hari sabtu
jadwal | apa jadwal minggu ini
jadwal | ingatkan kirim laporan jumat
jadwal | tunda pengingat sepuluh menit
jadwal | buat pengingat belanja
jadwal | kapan tenggat tugas dsp
jadwal | jadwalkan rapat tim lusa
jadwal | lihat kalender bulan depan

hitung | berapa akar dua ratus
hitung | konversi lima meter ke kaki
hitung | hitung dua puluh persen dari seratus ribu
hitung | berapa hasil tiga pangkat empat
hitung | ubah seratus derajat celsius ke fahrenheit
hitung | hitung rata rata dari data itu
hitung | berapa detik dalam satu hari
hitung | konversi satu gigabyte ke megabyte
hitung | hitung integral x kuadrat
hitung | berapa lima faktorial
hitung | ubah dua jam ke menit
hitung | hitung luas lingkaran jari jari tiga
hitung | berapa kecepatan cahaya
hitung | konversi kilogram ke pon
hitung | hitung sepuluh dibagi tiga

obrol | halo
obrol | apa kabar
obrol | kamu siapa
obrol | terima kasih
obrol | selamat pagi
obrol | lagi apa
obrol | kamu bisa apa saja
obrol | ceritakan sesuatu yang lucu
obrol | aku capek hari ini
obrol | oke siap
obrol | bagus sekali
obrol | sampai jumpa
obrol | kamu pintar juga ya
obrol | hmm begitu ya
obrol | lanjut saja
"""


if __name__ == "__main__":
    pasang = muat_perintah(sys.argv[1] if len(sys.argv) > 1 else None)
    try:
        latih_set, sah_set, uji_set = belah_tiga(pasang)
        bagian1(pasang, latih_set, sah_set, uji_set)

        kos = bangun_kosakata([k for k, _ in latih_set])
        idf = bobot_idf([k for k, _ in latih_set], kos)
        bagian2(latih_set, sah_set, kos, idf)

        label2i = {l: i for i, l in enumerate(sorted({l for _, l in pasang}))}
        nama, param, pakai, kos, idf, belah, ys = bagian3(pasang, kos, label2i)
        latih_set, sah_set, uji_set = belah
        yte = ys[2]

        bagian4(nama, param, pakai, kos, label2i, uji_set, yte)
        bagian5(param, pakai, kos, label2i, uji_set, yte)
        bagian6()
        bagian7(param, pakai, kos, uji_set)
    except NotImplementedError as e:
        print(f"\n  {e} belum diisi. Kerjakan TODO dulu.")
