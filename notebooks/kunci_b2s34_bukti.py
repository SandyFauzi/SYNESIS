"""Bukti terukur untuk jawaban Soal Bulan 2 Sesi 3 dan Sesi 4.

Jalankan:
    . .\\scripts\\activate.ps1
    python notebooks\\kunci_b2s34_bukti.py

Berkas ini tidak mengajari apa-apa. Ia cuma menghitung angka yang dipakai
di `soal-bulan2-sesi3.md` dan `soal-bulan2-sesi4.md`, supaya tiap jawaban
yang menyebut angka bisa diulang, bukan dipercaya.

Satu peringatan yang harus dibaca lebih dulu. Tabel yang tercetak di dalam
kedua berkas soal dihitung waktu `perintah_train_generated.txt` masih 1.080
kalimat dan kosakatanya 353 kolom. Berkas itu sudah diganti jadi 15.000
kalimat, 402 kolom, dan `data/bulan2/README.md` mencatat pergantian itu.
Jadi angka Sesi 3 di sini TIDAK sama dengan yang tercetak di soal, dan
bedanya bukan kesalahan hitung. Angka Sesi 4 masih sama persis, karena Sesi 4
membaca `model_intent.npz` yang memang belum dilatih ulang.
"""

import re
import sys
import time
from collections import Counter
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from bulan1_sesi34_mnist import Tensor, maju                      # noqa: E402
from bulan2_sesi2_intent import (                                 # noqa: E402
    AMBANG_INTENT, bangun_kosakata, belah_tiga, ekstrak_slot,
    muat_perintah, vektorkan)
from bulan2_sesi3_embedding import (                              # noqa: E402
    KORPUS_KATA_MAKS, kosakata_ngram, kumpulkan_korpus, matriks_kookurensi,
    maju_embed, ngram_karakter, padatkan, peringkat_pasangan, ppmi,
    selang_binomial)
from bulan2_sesi4_synesis import (                                # noqa: E402
    BACA, BAHASA, MERUSAK, ONGKOS_SALAH, ONGKOS_TOLAK, RUTE, TULIS,
    SERANGAN_JALUR, ambang_dari_ongkos, muat_model, ramal)
from synesis import alat, konfig                                  # noqa: E402

GARIS = "=" * 70
AKAR = Path(__file__).resolve().parent.parent
DATA = AKAR / "data" / "bulan2"

# Korpus dan matriksnya mahal. Dibangun sekali, dipakai beberapa uji.
_TEMBOLOK = {}


def judul(teks):
    print(f"\n{GARIS}\n{teks}\n{GARIS}")


def korpus():
    if "token" not in _TEMBOLOK:
        _TEMBOLOK["token"] = kumpulkan_korpus()
    return _TEMBOLOK["token"]


# ══════════════════════════════════════════════════════════════
# Kebijakan, ditulis sekali dan dipakai Uji H sampai Uji K
# ══════════════════════════════════════════════════════════════

def ongkos_kelas(model, p, manfaat=0.0):
    """Ongkos harapan tiap kelas untuk satu baris peluang.

    `manfaat` nol berarti tindakan benar tidak dihargai, cuma tidak dihukum.
    Itu model ongkos Bagian 2, dan Soal 3e memberinya nilai negatif.
    """
    return [ONGKOS_SALAH[RUTE[l][1]] * (1 - q) + manfaat * q
            for l, q in zip(model["label"], p)]


def kebijakan_ongkos(model, manfaat=0.0):
    """Kebijakan ongkos harapan: fungsi(peluang) -> indeks kelas, atau -1."""
    def pilih(p):
        biaya = ongkos_kelas(model, p, manfaat)
        k = int(np.argmin(biaya))
        return k if biaya[k] < ONGKOS_TOLAK else -1
    return pilih


def kebijakan_tangan(model):
    """Kebijakan ambang tangan Sesi 2: argmax dulu, baru periksa ambang."""
    def pilih(p):
        k = int(p.argmax())
        return k if p[k] >= AMBANG_INTENT[model["label"][k]] else -1
    return pilih


def kebijakan_argmax(p):
    return int(p.argmax())


def kebijakan_tolak(p):
    return -1


def jalankan_kebijakan(model, P, benar, pilih, manfaat=0.0):
    """Adu satu kebijakan dengan seluruh himpunan uji.

    Kembalikan (hitungan, ongkos tiap pesan). Hitungan memuat benar, salah,
    tolak, ongkos total, dan `rincian`, yaitu kelas risiko tiap tindakan yang
    salah. Ongkos per pesan dikembalikan terpisah karena Uji J membutuhkan
    sebarannya, bukan cuma jumlahnya.
    """
    h = {"benar": 0, "salah": 0, "tolak": 0, "rincian": Counter()}
    ongkos = []
    for p, y in zip(P, benar):
        k = pilih(p)
        if k < 0:
            h["tolak"] += 1
            ongkos.append(ONGKOS_TOLAK)
        elif k == y:
            h["benar"] += 1
            ongkos.append(manfaat)
        else:
            risiko = RUTE[model["label"][k]][1]
            h["salah"] += 1
            h["rincian"][risiko] += 1
            ongkos.append(ONGKOS_SALAH[risiko])
    ongkos = np.array(ongkos, dtype=float)
    h["ongkos"] = float(ongkos.sum())
    return h, ongkos


def baris_kebijakan(nama, h, n, lebar=6):
    return (f"{' ' * lebar}{nama:<24}{h['benar']:>7}{h['salah']:>7}"
            f"{h['tolak']:>7}{h['ongkos']:>10.1f}{h['ongkos'] / n:>15.2f}")


def kepala_kebijakan(lebar=6):
    return (f"{' ' * lebar}{'kebijakan':<24}{'benar':>7}{'salah':>7}"
            f"{'tolak':>7}{'ongkos':>10}{'ongkos/pesan':>15}\n"
            + " " * lebar + "-" * 70)


# ══════════════════════════════════════════════════════════════
# UJI A - Sesi 3 Soal 1: berapa n supaya selisih 10 poin terbaca
# ══════════════════════════════════════════════════════════════

def uji_a():
    judul("UJI A  Sesi 3 Soal 1  lebar selang, dan n untuk selisih 10 poin")

    p = 0.56
    print("  1a  lebar(n) = 2 * 1,96 * sqrt(p(1-p)/n), p = 0,56\n")
    print(f"      {'n':>8}{'lebar (poin)':>16}")
    print("      " + "-" * 24)
    for n in (41, 100, 200, 400, 1000, 3840):
        print(f"      {n:>8}{2 * 1.96 * (p * (1 - p) / n) ** 0.5 * 100:>16.1f}")
    print(f"\n      pembilangnya tetap: 2*1,96*sqrt(0,56*0,44) = "
          f"{2 * 1.96 * (p * (1 - p)) ** 0.5:.4f}")
    print(f"      jadi lebar(n) = {2 * 1.96 * (p * (1 - p)) ** 0.5:.4f}/sqrt(n)")
    print(f"      lebar(41)     = {2 * 1.96 * (p * (1 - p)) ** 0.5:.4f}/"
          f"{41 ** 0.5:.3f} = {2 * 1.96 * (p * (1 - p) / 41) ** 0.5:.4f}")

    print("\n  1b  uji BERPASANGAN, dua model di kalimat yang SAMA.")
    print("      psi = porsi kalimat tempat kedua model BERBEDA.")
    print("      selisih delta = 10 poin, jadi psi >= 0,10 selalu.\n")
    delta = 0.10
    print(f"      {'psi':>8}{'n (selang 95%)':>18}{'n (95% + kuasa 80%)':>22}")
    print("      " + "-" * 48)
    for psi in (0.10, 0.15, 0.20, 0.30, 0.40, 0.55):
        n_ci = 1.96 ** 2 * psi / delta ** 2
        akar = psi - delta ** 2
        n_kuasa = ((1.96 * psi ** 0.5 + 0.84 * akar ** 0.5) / delta) ** 2
        print(f"      {psi:>8.2f}{n_ci:>18.0f}{n_kuasa:>22.0f}")

    n_tak = 2 * 1.96 ** 2 * 0.5 * 0.5 / delta ** 2
    print(f"\n      pembanding TAK berpasangan (p ~ 0,5, dua sampel bebas): "
          f"n = {n_tak:.0f} per model")

    print("\n  1c  angka 3.840 dari Sesi 2 Soal 1c:")
    print(f"      576 kalimat uji supaya lebar selang SATU model 5 poin, "
          f"dan 576/0,15 = {576 / 0.15:.0f} total.")

    print("\n  1d  komposisi 41 pesan nyata:")
    nyata = muat_perintah(DATA / "perintah_eval_real.txt")
    hit = Counter(l for _, l in nyata)
    n = len(nyata)
    p_maks, n_kelas = hit.most_common(1)[0][1] / n, len(hit)
    _, b, a = selang_binomial(hit.most_common(1)[0][1], n)
    print(f"      dasar mayoritas {p_maks * 100:.1f}%  selang "
          f"{b * 100:.1f} .. {a * 100:.1f}, dari {n_kelas} kelas terpakai")
    print(f"      lebar selangnya {a * 100 - b * 100:.1f} poin, jadi arah "
          f"geseran di 200 pesan tidak bisa ditebak dari sini.")


# ══════════════════════════════════════════════════════════════
# UJI B - Sesi 3 Soal 2: keluaran jaringan untuk vektor nol
# ══════════════════════════════════════════════════════════════

def uji_b():
    judul("UJI B  Sesi 3 Soal 2  vektor nol, di atas kertas lalu diukur")

    sint = muat_perintah(DATA / "perintah_train_generated.txt")
    nyata = muat_perintah(DATA / "perintah_eval_real.txt")
    kos = bangun_kosakata([k for k, _ in sint])

    nol = [k for k, _ in nyata
           if not any(w in kos for w in re.findall(r"[a-z0-9]+", k.lower()))]
    print(f"  kosakata sintetis        : {len(kos)} kata")
    print(f"  kalimat bervektor nol    : {len(nol)} dari {len(nyata)}")
    for k in nol:
        print(f"    '{k}'")
    print("\n  Soal menyebut TIGA kalimat. Terukur di data sekarang: "
          f"{len(nol)}.")

    # Model dua lapis, persis baris pertama tabel Bagian 3.
    label = sorted({l for _, l in sint})
    L = {l: i for i, l in enumerate(label)}
    tr, va, _ = belah_tiga(sint, seed=0)
    from bulan2_sesi2_intent import latih
    t0 = time.perf_counter()
    param, _ = latih(vektorkan([k for k, _ in tr], kos),
                     np.array([L[l] for _, l in tr]),
                     vektorkan([k for k, _ in va], kos),
                     np.array([L[l] for _, l in va]), len(L), seed=0)
    print(f"\n  model dua lapis dilatih dalam {time.perf_counter() - t0:.0f} detik")

    W1, b1, W2, b2 = [p.data for p in param]
    logit_rumus = np.maximum(b1, 0) @ W2 + b2
    logit_jalan = maju(param, np.zeros((1, len(kos)))).data[0]
    print(f"  2a  logit = relu(b1) @ W2 + b2")
    print(f"      selisih rumus lawan jalan: "
          f"{np.abs(logit_rumus - logit_jalan).max():.3e}")

    e = np.exp(logit_jalan - logit_jalan.max())
    peluang = e / e.sum()
    k = int(peluang.argmax())
    print(f"  2b  kelas keluar : {label[k]}, sama untuk SEMUA kalimat nol")
    print(f"  2c  keyakinan    : {peluang[k]:.4f}")
    print(f"      ambang tangan {label[k]} = {AMBANG_INTENT[label[k]]:.2f} -> "
          f"{'DITOLAK' if peluang[k] < AMBANG_INTENT[label[k]] else 'LOLOS'}")
    print(f"      ambang ongkos {label[k]} = "
          f"{ambang_dari_ongkos(RUTE[label[k]][1]):.3f} -> "
          f"{'DITOLAK' if peluang[k] < ambang_dari_ongkos(RUTE[label[k]][1]) else 'LOLOS'}")

    # Model tersimpan, yaitu yang benar-benar dipakai SYNESIS.
    model = muat_model()
    p_simpan = ramal(model, [""])[0]
    ks = int(p_simpan.argmax())
    print(f"\n      model tersimpan (softmax satu lapis, {len(model['kosakata'])} kolom):")
    print(f"      kelas {model['label'][ks]}, yakin {p_simpan[ks]:.4f}, "
          f"ambang tangan {AMBANG_INTENT[model['label'][ks]]:.2f} -> "
          f"{'DITOLAK' if p_simpan[ks] < AMBANG_INTENT[model['label'][ks]] else 'LOLOS'}")
    return param, kos, label, L


# ══════════════════════════════════════════════════════════════
# UJI C - Sesi 3 Soal 3: kelebihan lapor, dan kenapa 2-gram jelek
# ══════════════════════════════════════════════════════════════

def uji_c():
    judul("UJI C  Sesi 3 Soal 3  kelebihan lapor, dan potongan 2 huruf")

    n = 41
    sigma = (0.55 * 0.45 / n) ** 0.5
    print(f"  3b  sigma satu baris = sqrt(p(1-p)/n) = {sigma * 100:.1f} poin")
    print(f"      {'k baris':>9}{'sqrt(2 ln k)':>15}{'kelebihan lapor':>19}")
    print("      " + "-" * 43)
    for k in (2, 3, 5, 10):
        lebih = sigma * (2 * np.log(k)) ** 0.5
        print(f"      {k:>9}{(2 * np.log(k)) ** 0.5:>15.3f}{lebih * 100:>18.1f}p")

    sint = muat_perintah(DATA / "perintah_train_generated.txt")
    kalimat = [k for k, _ in sint]
    print("\n  3d  berapa kalimat memuat tiap potongan (data latih penuh):\n")
    print(f"      {'panjang':>9}{'potongan unik':>16}{'median df':>12}"
          f"{'df > 50%':>11}{'df = 1':>9}")
    print("      " + "-" * 57)
    for panjang in (2, 3, 4, 5):
        kos = kosakata_ngram(kalimat, panjang, panjang)
        df = Counter()
        for teks in kalimat:
            hadir = set()
            for w in re.findall(r"[a-z0-9]+", teks.lower()):
                hadir |= ngram_karakter(w, panjang, panjang)
            df.update(hadir)
        nilai = np.array([df[g] for g in kos])
        print(f"      {panjang:>9}{len(kos):>16}{np.median(nilai):>12.0f}"
              f"{(nilai > len(kalimat) / 2).sum():>11}{(nilai == 1).sum():>9}")
    # Yang menentukan bukan cuma seberapa sering, tapi berapa besar porsi
    # panjang kuadrat vektor yang direbut potongan 2 huruf, karena tiap
    # baris dinormalkan jadi panjang satu.
    from bulan2_sesi3_embedding import vektorkan_ngram
    contoh = kalimat[:400]
    kos24 = kosakata_ngram(contoh, 2, 4)
    X = vektorkan_ngram(contoh, kos24, 2, 4)
    dua = np.array([len(g) == 2 for g in sorted(kos24)])
    porsi = (X[:, dua] ** 2).sum(axis=1)
    print(f"\n      di fitur n-gram 2-4, potongan 2 huruf memegang "
          f"{porsi.mean() * 100:.1f} persen")
    print(f"      panjang kuadrat tiap baris (median {np.median(porsi) * 100:.1f}%), "
          f"padahal cuma {dua.sum()} dari {len(kos24)} kolom.")
    print("      Itu mekanismenya: baris dinormalkan, jadi kolom yang ramai")
    print("      merebut norma dari kolom 3-4 huruf yang membedakan.")


# ══════════════════════════════════════════════════════════════
# UJI D - Sesi 3 Soal 4: melewati vs menghapus, diagonal, jendela
# ══════════════════════════════════════════════════════════════

def uji_d():
    judul("UJI D  Sesi 3 Soal 4  melewati vs menghapus, diagonal, jendela")

    kalimat = "saya install venv pakai python".split()
    V = {"install": 0, "python": 1}
    C_lewat = matriks_kookurensi(kalimat, V, jendela=2)
    C_hapus = matriks_kookurensi([w for w in kalimat if w in V], V, jendela=2)
    print(f"  4a  '{' '.join(kalimat)}', jendela 2, kosakata {list(V)}")
    print(f"      dilewati : C[install][python] = {C_lewat[0, 1]:.0f}")
    print(f"      dihapus  : C[install][python] = {C_hapus[0, 1]:.0f}")
    print("      Menghapus membuat dua kata yang terpisah tiga posisi jadi "
          "bersebelahan.")

    token = korpus()
    hit = Counter(token)
    Vk = {w: i for i, w in enumerate(
        sorted(w for w, _ in hit.most_common(KORPUS_KATA_MAKS)))}
    C = matriks_kookurensi(token, Vk)
    _TEMBOLOK["C"], _TEMBOLOK["Vk"] = C, Vk

    diag = np.diag(C).copy()
    print(f"\n  4b  diagonal taknol: {(diag > 0).sum()} kata, "
          f"jumlahnya {diag.sum():.0f} dari total {C.sum():.0f} "
          f"= {diag.sum() / C.sum() * 100:.2f} persen massa")
    C0 = C.copy()
    np.fill_diagonal(C0, 0)
    tepi = sorted(Vk, key=lambda w: -diag[Vk[w]])[:5]
    print(f"      diagonal terbesar: {', '.join(tepi)}")
    for w in tepi[:3]:
        i = Vk[w]
        print(f"      p({w}) turun {C[i].sum() / C.sum() * 100:.3f}% -> "
              f"{C0[i].sum() / C0.sum() * 100:.3f}% kalau diagonal dinolkan")
    m1 = peringkat_pasangan(padatkan(ppmi(C), d=100), Vk)
    m0 = peringkat_pasangan(padatkan(ppmi(C0), d=100), Vk)
    print(f"      median peringkat: diagonal dibiarkan {m1[0]:.0f}, "
          f"dinolkan {m0[0]:.0f}  ({m1[1]} pasangan)")

    print("\n  4c  ramalan sebelum diukur ada di jawaban Soal 4c.\n")
    print(f"      {'jendela':>9}{'taknol PPMI':>14}{'median peringkat':>19}"
          f"{'detik':>8}")
    print("      " + "-" * 50)
    for j in (2, 5, 15):
        t0 = time.perf_counter()
        Cj = C if j == 5 else matriks_kookurensi(token, Vk, jendela=j)
        Mj = ppmi(Cj)
        med, dipakai, ukuran = peringkat_pasangan(padatkan(Mj, d=100), Vk)
        print(f"      {j:>9}{(Mj > 0).mean() * 100:>13.1f}%{med:>19.0f}"
              f"{time.perf_counter() - t0:>8.0f}")

    print("\n  4d  ongkos memori matriks rapat float64:")
    for v in (2000, 50000):
        print(f"      {v} x {v} = {v * v * 8 / 2 ** 20:,.0f} MB "
              f"= {v * v * 8 / 2 ** 30:,.2f} GB")
    isi = (ppmi(C) > 0).mean()
    print(f"      taknol terukur {isi * 100:.1f}%, jadi COO 50.000 kira-kira "
          f"{50000 ** 2 * isi * 16 / 2 ** 30:.1f} GB")


# ══════════════════════════════════════════════════════════════
# UJI E - Sesi 3 Soal 6: kurva ukuran korpus, dan ambang hitungan
# ══════════════════════════════════════════════════════════════

def uji_e():
    judul("UJI E  Sesi 3 Soal 6  kurva ukuran korpus dan ambang hitungan")

    token = korpus()
    hit = Counter(token)
    besar = min(1200, len(hit))
    Vk = {w: i for i, w in enumerate(
        sorted(w for w, _ in hit.most_common(besar)))}

    print(f"  korpus {len(token)} token, {len(hit)} kata unik, "
          f"kosakata dipatok {len(Vk)}\n")
    print(f"  {'token dibaca':>14}{'pasangan':>10}{'median peringkat':>19}"
          f"{'acak':>8}{'median hitungan kata uji':>26}")
    print("  " + "-" * 77)
    from bulan2_sesi3_embedding import PASANGAN_UJI
    kata_uji = sorted({w for pas in PASANGAN_UJI for w in pas if w in Vk})
    for bagian in (0.1, 0.25, 0.5, 1.0):
        n = int(len(token) * bagian)
        potong = token[:n]
        h = Counter(potong)
        E = padatkan(ppmi(matriks_kookurensi(potong, Vk)), d=100)
        med, dp, u = peringkat_pasangan(E, Vk)
        med_hit = np.median([h[w] for w in kata_uji])
        print(f"  {n:>14}{dp:>10}{med:>19.0f}{u / 2:>8.0f}{med_hit:>26.0f}")

    print(f"\n  6c  GloVe 6e9 token / korpus {len(token)} = "
          f"{6e9 / len(token):,.0f} kali lebih besar")


# ══════════════════════════════════════════════════════════════
# UJI F - Sesi 3 Soal 7c: nasib kata bervektor nol
# ══════════════════════════════════════════════════════════════

def uji_f():
    judul("UJI F  Sesi 3 Soal 7c  gradien baris E untuk kata yang tak muncul")

    sint = muat_perintah(DATA / "perintah_train_generated.txt")
    kos = bangun_kosakata([k for k, _ in sint])
    label = sorted({l for _, l in sint})
    L = {l: i for i, l in enumerate(label)}
    tr, _, _ = belah_tiga(sint, seed=0)

    # Data latih penuh memakai SETIAP kata, jadi tidak ada kolom nol untuk
    # ditunjukkan. Dipotong 200 kalimat supaya kasusnya benar-benar ada.
    for n_tr in (200, len(tr)):
        X = vektorkan([k for k, _ in tr[:n_tr]], kos)
        panjang = X.sum(axis=1, keepdims=True)
        np.divide(X, panjang, out=X, where=panjang != 0)
        y = np.array([L[l] for _, l in tr[:n_tr]])
        kolom_nol = np.flatnonzero(X.sum(axis=0) == 0)

        rng = np.random.default_rng(0)
        d, n_h = 100, 48
        param = [
            Tensor(rng.normal(0, 1, (len(kos), d)) * (2 / len(kos)) ** 0.5),
            Tensor(rng.normal(0, 1, (d, n_h)) * (2 / d) ** 0.5),
            Tensor(np.zeros(n_h)),
            Tensor(rng.normal(0, 1, (n_h, len(L))) * (2 / n_h) ** 0.5),
            Tensor(np.zeros(len(L)))]
        rugi = maju_embed(param, X).entropi_silang(y)
        for p in param:
            p.grad = np.zeros_like(p.data)
        rugi.backward()
        g = param[0].grad
        ada = np.setdiff1d(np.arange(len(kos)), kolom_nol)
        print(f"  {n_tr:>5} kalimat latih, kosakata {len(kos)}, "
              f"kolom NOL di data latih: {len(kolom_nol)}")
        if len(kolom_nol):
            print(f"        |grad E| terbesar di baris kolom nol   : "
                  f"{np.abs(g[kolom_nol]).max():.3e}")
        print(f"        |grad E| terbesar di baris kata yang ada: "
              f"{np.abs(g[ada]).max():.3e}")

    # Kasus kedua: E awal nol tapi katanya MUNCUL di data latih.
    E0 = np.zeros((len(kos), d))
    param[0] = Tensor(E0)
    rugi = maju_embed(param, X).entropi_silang(y)
    for p in param:
        p.grad = np.zeros_like(p.data)
    rugi.backward()
    print(f"\n  E awal NOL seluruhnya: |grad E| terbesar "
          f"{np.abs(param[0].grad).max():.3e}")
    print("  H0 = X @ 0 = 0, lalu relu(0 @ W1 + 0) = 0, dan turunan relu di")
    print("  nol bernilai nol, jadi gradiennya mati di tekukan, bukan di X.")

    print("\n  grad E = X.T @ (dL/dH0). Kolom i dari X nol -> baris i dari")
    print("  X.T nol -> baris i dari grad E nol, berapa pun epochnya.")
    print("  Baris nol yang tak pernah dapat gradien tetap nol selamanya.")


# ══════════════════════════════════════════════════════════════
# UJI G - Sesi 4 Soal 5: mekanisme mana yang menolak
# ══════════════════════════════════════════════════════════════

def uji_g():
    judul("UJI G  Sesi 4 Soal 5  mekanisme mana yang menolak tiap serangan")

    boleh = [Path(b).resolve() for b in konfig.FOLDER_BOLEH]

    def di_dalam(p):
        for b in boleh:
            try:
                p.relative_to(b)
                return True
            except ValueError:
                continue
        return False

    print(f"  {'jalur':<46}{'mentah':>8}{'resolve':>9}{'putusan':>10}"
          f"   penolak")
    print("  " + "-" * 105)
    for jalur in SERANGAN_JALUR:
        mentah = Path(jalur).expanduser()
        sebelum, sesudah = di_dalam(mentah), di_dalam(mentah.resolve())
        try:
            alat._aman(jalur)
            putusan = "LOLOS"
        except alat.DitolakPagar:
            putusan = "ditolak"
        if putusan == "LOLOS":
            penolak = "-"
        elif sebelum and not sesudah:
            penolak = "resolve() lalu relative_to()"
        elif not sebelum and not sesudah:
            penolak = "relative_to() saja, resolve() tak perlu"
        else:
            penolak = "lapisan isi (_bukan_rahasia)"
        print(f"  {jalur[:44]:<46}{str(sebelum):>8}{str(sesudah):>9}"
              f"{putusan:>10}  {penolak}")

    print("\n  5d  kalau urutannya dibalik (relative_to dulu, resolve sesudah):")
    for jalur in SERANGAN_JALUR:
        mentah = Path(jalur).expanduser()
        if di_dalam(mentah) and not di_dalam(mentah.resolve()):
            print(f"      LOLOS: {jalur}")
            print(f"             sesungguhnya menunjuk {mentah.resolve()}")


# ══════════════════════════════════════════════════════════════
# UJI H - Sesi 4 Soal 3: selalu menolak, dan tabel ongkos yang diperbaiki
# ══════════════════════════════════════════════════════════════

MANFAAT_BENAR = -2.0     # tindakan benar dihargai, bukan cuma tidak dihukum


def ambang_dengan_manfaat(risiko, manfaat=MANFAAT_BENAR,
                          c_tolak=ONGKOS_TOLAK):
    """p > (c_salah - c_tolak) / (c_salah - manfaat). Manfaat nol -> rumus lama."""
    c_salah = ONGKOS_SALAH[risiko]
    return min(1.0, max(0.0, (c_salah - c_tolak) / (c_salah - manfaat)))


def uji_h():
    judul("UJI H  Sesi 4 Soal 3  selalu menolak, lalu ongkos yang diperbaiki")

    model = muat_model()
    nyata = muat_perintah(DATA / "perintah_eval_real.txt")
    L = {l: i for i, l in enumerate(model["label"])}
    benar = np.array([L[l] for _, l in nyata])
    P = ramal(model, [k for k, _ in nyata])
    n = len(nyata)

    print("  3d  papan skor asli, dengan baris keempat yang soalnya sisakan\n")
    print(kepala_kebijakan())
    for nama, pilih in (("argmax polos", kebijakan_argmax),
                        ("ambang tangan Sesi 2", kebijakan_tangan(model)),
                        ("ongkos harapan", kebijakan_ongkos(model)),
                        ("selalu menolak", kebijakan_tolak)):
        h, _ = jalankan_kebijakan(model, P, benar, pilih)
        print(baris_kebijakan(nama, h, n))

    print(f"\n  3e  manfaat tindakan benar = {MANFAAT_BENAR}, ONGKOS_SALAH "
          f"dan ONGKOS_TOLAK tidak diubah\n")
    print(f"      {'risiko':<10}{'ambang lama':>13}{'ambang baru':>13}")
    print("      " + "-" * 36)
    for r in (BACA, TULIS, MERUSAK, BAHASA):
        print(f"      {r:<10}{ambang_dari_ongkos(r):>13.3f}"
              f"{ambang_dengan_manfaat(r):>13.3f}")

    print()
    print(kepala_kebijakan())
    for nama, pilih in (("argmax polos", kebijakan_argmax),
                        ("ambang tangan Sesi 2", kebijakan_tangan(model)),
                        ("ongkos + manfaat", kebijakan_ongkos(model, MANFAAT_BENAR)),
                        ("selalu menolak", kebijakan_tolak)):
        h, _ = jalankan_kebijakan(model, P, benar, pilih, MANFAAT_BENAR)
        print(baris_kebijakan(nama, h, n))
    return model, nyata, P, benar


# ══════════════════════════════════════════════════════════════
# UJI I - Sesi 4 Soal 2b, 4b, 6c
# ══════════════════════════════════════════════════════════════

def uji_i(model, nyata, P, benar):
    judul("UJI I  Sesi 4 Soal 2b, 4b, 6c  selisih ambang, slot, dan penolakan")

    selisih = {l: ambang_dari_ongkos(RUTE[l][1]) - AMBANG_INTENT[l]
               for l in model["label"]}
    positif = [l for l, s in selisih.items() if s > 1e-9]
    negatif = [l for l, s in selisih.items() if s < -1e-9]
    print(f"  2b  selisih positif {len(positif)}, negatif {len(negatif)}, "
          f"nol {len(selisih) - len(positif) - len(negatif)}")
    print(f"      terbesar positif: "
          f"{', '.join(f'{l} {selisih[l]:+.3f}' for l in sorted(positif, key=lambda x: -selisih[x])[:3])}")
    print(f"      terbesar negatif: "
          f"{', '.join(f'{l} {selisih[l]:+.3f}' for l in sorted(negatif, key=lambda x: selisih[x])[:3])}")

    kalimat = "buka laporan praktikum minggu lalu"
    slot = ekstrak_slot(kalimat)
    print(f"\n  4b  ekstrak_slot('{kalimat}') = {slot}")
    cocok = list((AKAR).glob(f"*{slot.get('objek', '')}*"))
    print(f"      berkas yang cocok dengan pola itu di akar repo: {len(cocok)}")
    print(f"      slot 'waktu' = {slot.get('waktu')}, dan tidak dipakai "
          f"sama sekali oleh slot_ke_argumen")

    print("\n  6c  tiga pesan pertama yang berakhir tolak_yakin:\n")
    pilih = kebijakan_ongkos(model)
    dicetak = 0
    for (k, l), p in zip(nyata, P):
        if pilih(p) >= 0:
            continue
        biaya = ongkos_kelas(model, p)
        km = int(np.argmin(biaya))
        top = int(p.argmax())
        print(f"      '{k[:52]}'")
        print(f"        label benar   : {l}")
        print(f"        tebakan model : {model['label'][top]} yakin {p[top]:.3f}")
        print(f"        kelas termurah: {model['label'][km]} ongkos "
              f"{biaya[km]:.2f} lawan ongkos menolak {ONGKOS_TOLAK}")
        print(f"        ambang {model['label'][top]} = "
              f"{ambang_dari_ongkos(RUTE[model['label'][top]][1]):.3f}")
        dicetak += 1
        if dicetak == 3:
            break


# ══════════════════════════════════════════════════════════════
# UJI J - Sesi 4 Soal 8a: berapa baris audit sebelum melatih ulang
# ══════════════════════════════════════════════════════════════

def uji_j(model, nyata, P, benar):
    judul("UJI J  Sesi 4 Soal 8a dan 8d  berapa baris audit, diukur dari ongkos")

    _, c = jalankan_kebijakan(model, P, benar, kebijakan_ongkos(model))
    print(f"  ongkos per pesan kebijakan sekarang: rerata {c.mean():.3f}, "
          f"simpangan baku {c.std(ddof=1):.3f}, maks {c.max():.1f}")

    print(f"\n  n supaya PERBAIKAN ongkos sebesar d bisa dibedakan dari nol,")
    print(f"  uji berpasangan, simpangan baku selisih diasumsikan s:\n")
    print(f"      {'perbaikan d':>13}{'s = 0,50':>12}{'s = 1,00':>12}"
          f"{'s = 1,50':>12}")
    print("      " + "-" * 49)
    for d in (0.10, 0.25, 0.50):
        baris = f"      {d:>13.2f}"
        for s in (0.5, 1.0, 1.5):
            baris += f"{(1.96 * s / d) ** 2:>12.0f}"
        print(baris)

    for uji in (115, 233):
        print(f"\n  kalau himpunan uji {uji} pesan dan belahan 70/15/15, "
              f"total baris audit = {uji / 0.15:,.0f}")


# ══════════════════════════════════════════════════════════════
# UJI K - lima angka pendek yang dipakai beberapa jawaban sekaligus
# ══════════════════════════════════════════════════════════════

def uji_k(model, nyata, P, benar):
    judul("UJI K  angka pendek: pagar izin, S:/Code, dan rincian ongkos")

    L = {l: i for i, l in enumerate(model["label"])}
    n = len(nyata)

    # Sesi 4 Soal 2e: seberapa yakin model pernah pada kelas MERUSAK
    kolom_rusak = [i for i, l in enumerate(model["label"])
                   if RUTE[l][1] == MERUSAK]
    maks_rusak = P[:, kolom_rusak].max()
    print(f"  2e  keyakinan MERUSAK tertinggi di 41 pesan: {maks_rusak:.3f}")
    for c in (50.0, 200.0, 1000.0):
        print(f"      ongkos {c:>6.0f} -> ambang {1 - ONGKOS_TOLAK / c:.3f} -> "
              f"{'tetap ditolak' if maks_rusak < 1 - ONGKOS_TOLAK / c else 'ADA yang lolos'}")

    # Sesi 4 Soal 3b: dari mana selisih 242 lawan 39 datang
    print("\n  3b  rincian ongkos dua kebijakan yang sama-sama benar 15 kali:")
    for nama, pilih in (("ambang tangan", kebijakan_tangan(model)),
                        ("ongkos harapan", kebijakan_ongkos(model))):
        h, _ = jalankan_kebijakan(model, P, benar, pilih)
        isi = ", ".join(f"{c} x {r} ({ONGKOS_SALAH[r]:.0f})"
                        for r, c in sorted(h["rincian"].items()))
        salah = sum(ONGKOS_SALAH[r] * c for r, c in h["rincian"].items())
        print(f"      {nama:<16} salah: {isi or 'tidak ada'} = {salah:.1f}"
              f", tolak: {h['tolak']} x {ONGKOS_TOLAK} = {h['tolak'] * ONGKOS_TOLAK:.1f}"
              f", total {h['ongkos']:.1f}")

    # Sesi 4 Soal 6a dan 6b: apakah pagar izin pernah dipakai.
    # Audit dimatikan sementara: jalannya uji ini bukan pemakaian pemilik,
    # dan audit.jsonl harus berisi pemakaian sungguhan saja.
    import bulan2_sesi4_synesis as S4
    asli, S4.catat_audit = S4.catat_audit, lambda baris, berkas=None: None
    try:
        hasil = [S4.jalankan_pipa(k, model, izin=None, kering=True)
                 for k, _ in nyata]
    finally:
        S4.catat_audit = asli
    hit = Counter(h["tindakan"] for h in hasil)
    print(f"\n  6a  {dict(hit)}")
    print(f"      tolak_izin = {hit['tolak_izin']}, dan itu BUKAN bukti "
          f"gerbangnya bekerja: tidak ada satu pun yang sampai ke sana.")

    # Bukti terpisah bahwa gerbang izin memang menahan, dengan peluang buatan
    buatan = np.zeros(len(model["label"]))
    buatan[L["pasang_paket"]] = 0.999
    from bulan2_sesi4_synesis import putuskan
    k, _ = putuskan(buatan, model["label"])
    print(f"      dipaksa: peluang pasang_paket 0,999 -> putuskan memilih "
          f"{model['label'][k] if k >= 0 else 'TOLAK'}")

    # Sesi 4 Soal 6b: kalau kebijakannya dipaksa selalu bertindak
    ha, _ = jalankan_kebijakan(model, P, benar, kebijakan_argmax)
    print(f"\n  6b  kalau kebijakannya argmax polos (selalu bertindak): "
          f"{ha['benar']} tepat, {ha['salah']} meleset dari {n}")
    print(f"      kebijakan sekarang bertindak {hit['jalan']} kali, jadi "
          f"'meleset 0' cuma menutup {hit['jalan']}/{n} kesempatan salah.")
    batas = min(1.0, 3 / max(hit['jalan'], 1))
    print(f"      aturan tiga: dari {hit['jalan']} tindakan tanpa satu pun "
          f"salah, batas atas laju salah {batas * 100:.0f} persen, "
          f"yaitu tidak membatasi apa pun")

    # Sesi 4 Soal 6c: berapa dari yang ditolak sebenarnya punya alat
    tolak = [(k, l) for (k, l), h in zip(nyata, hasil)
             if h["tindakan"] == "tolak_yakin"]
    punya = sum(1 for _, l in tolak if RUTE[l][0] is not None)
    print(f"\n  6c  dari {len(tolak)} pesan tolak_yakin, yang label BENARNYA "
          f"punya alat: {punya}")
    print(f"      sisanya akan berhenti di belum_ada_alat juga, jadi ambangnya "
          f"tidak mencegah apa-apa untuk mereka.")

    # Sesi 4 Soal 5c: apa yang terbuka karena S:/Code ada di FOLDER_BOLEH
    akar = Path("S:/Code")
    n_berkas = n_rahasia = 0
    proyek = set()
    for p in akar.rglob("*"):
        if not p.is_file():
            continue
        n_berkas += 1
        bagian = p.relative_to(akar).parts
        if bagian:
            proyek.add(bagian[0])
        if any(alat.POLA_RAHASIA.match(b) for b in p.parts[1:]):
            n_rahasia += 1
    print(f"\n  5c  S:/Code memuat {len(proyek)} entri tingkat atas, "
          f"{n_berkas} berkas")
    print(f"      yang cocok POLA_RAHASIA: {n_rahasia}")


# ══════════════════════════════════════════════════════════════
# UJI L - Sesi 3 Soal 8b: Tuas B ditarik sampai porsinya lewat separuh
# ══════════════════════════════════════════════════════════════

def uji_l():
    judul("UJI L  Sesi 3 Soal 8b  Tuas B sampai porsi nyata lewat separuh")

    from bulan2_sesi2_intent import latih
    from bulan2_sesi3_embedding import _siapkan
    sint = muat_perintah(DATA / "perintah_train_generated.txt")
    nyata = muat_perintah(DATA / "perintah_eval_real.txt")
    label = sorted({l for _, l in sint})
    L = {l: i for i, l in enumerate(label)}
    tr_s, va_s, _ = belah_tiga(sint, seed=0)

    print(f"  data latih sintetis {len(tr_s)} kalimat. Sapuan Bagian 7 cuma")
    print(f"  sampai ulangi 40, yaitu porsi 7,1 persen, bukan lebih dari")
    print(f"  separuh seperti yang tertulis di soal. Ditarik lebih jauh:\n")
    print(f"  {'k nyata':>9}{'diulang':>9}{'n latih':>9}{'porsi':>8}"
          f"{'rerata':>10}{'terbaik':>10}{'detik':>8}")
    print("  " + "-" * 63)
    for ulangi in (40, 200, 600):
        t0 = time.perf_counter()
        skor = []
        for u in range(3):
            rng = np.random.default_rng(100 + u)
            urut = rng.permutation(len(nyata))
            ambil = [nyata[i] for i in urut[:20]]
            sisa = [nyata[i] for i in urut[20:]]
            X, y = _siapkan(tr_s + ambil * ulangi, va_s, sisa, L)
            p, _ = latih(X[0], y[0], X[1], y[1], len(L), seed=u)
            skor.append((maju(p, X[2]).data.argmax(1) == y[2]).mean())
        s = np.array(skor)
        n_tr = len(tr_s) + 20 * ulangi
        print(f"  {20:>9}{ulangi:>9}{n_tr:>9}{20 * ulangi / n_tr * 100:>7.1f}%"
              f"{s.mean() * 100:>9.1f}%{s.max() * 100:>9.1f}%"
              f"{time.perf_counter() - t0:>8.0f}")


# ══════════════════════════════════════════════════════════════

def main():
    mulai = time.perf_counter()
    uji_a()
    uji_b()
    uji_c()
    uji_d()
    uji_e()
    uji_f()
    uji_g()
    model, nyata, P, benar = uji_h()
    uji_i(model, nyata, P, benar)
    uji_j(model, nyata, P, benar)
    uji_k(model, nyata, P, benar)
    uji_l()
    print(f"\n{GARIS}\n  selesai dalam {time.perf_counter() - mulai:.0f} detik\n{GARIS}")


if __name__ == "__main__":
    main()
