"""Bukti terukur untuk kunci Bulan 2 Sesi 1 dan Sesi 2.

Jalankan:
    . .\\scripts\\activate.ps1
    python notebooks\\kunci_b2_bukti.py

Empat pengujian:
  A  softmax tanpa pengurangan maksimum, dan di mana ambangnya  -> S1 Soal 7d
  B  MSE lawan entropi silang, gradien masing-masing            -> S1 Soal 4a
  C  kebocoran kosakata, tiga tingkat                           -> S2 Soal 2b
  D  ambang per intent dan lima perintah yang butuh LLM         -> S2 Soal 5c, 8c

Uji C paling lama, sekitar dua menit, karena melatih 8 seed kali 3 tingkat
kebocoran kali 2 resep fitur.
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

import bulan2_sesi1_kata as S1        # noqa: E402
import bulan2_sesi2_intent as S2      # noqa: E402

GARIS = "=" * 68


# ══════════════════════════════════════════════════════════════
# UJI A  softmax tanpa pengurangan maksimum
# ══════════════════════════════════════════════════════════════

def softmax_polos(Z):
    """Softmax tanpa pengurangan maksimum. Sengaja rapuh."""
    e = np.exp(Z)
    return e / e.sum(axis=-1, keepdims=True)


def bagian5_dengan(softmax_fn, kali, n_iter=4000):
    kos = S1.bangun_kosakata([t for t, _ in S1.DATA])
    X = np.array([S1.ke_vektor(t, kos) for t, _ in S1.DATA], dtype=float)
    indeks = {lab: i for i, lab in enumerate(S1.LABEL)}
    y = np.array([indeks[lab] for _, lab in S1.DATA])
    T = np.zeros((len(y), len(S1.LABEL)))
    T[np.arange(len(y)), y] = 1.0

    rng = np.random.default_rng(7)
    W = rng.normal(0, 0.1, (X.shape[1], len(S1.LABEL))) * kali
    b = np.zeros(len(S1.LABEL))

    logit_maks = np.abs(X @ W + b).max()
    with np.errstate(over="ignore", invalid="ignore"):
        for _ in range(n_iter):
            P = softmax_fn(X @ W + b)
            dZ = (P - T) / len(y)
            W -= 0.5 * (X.T @ dZ)
            b -= 0.5 * dZ.sum(0)
        P = softmax_fn(X @ W + b)

    ada_nan = bool(np.isnan(P).any())
    return logit_maks, ada_nan, (float("nan") if ada_nan
                                 else (P.argmax(1) == y).mean())


def ujiA():
    print(GARIS, "\nUJI A  softmax tanpa pengurangan maksimum  (S1 Soal 7d)\n",
          GARIS, sep="")

    print(f"  exp meluap di atas ln(1.8e308) = "
          f"{np.log(np.finfo(float).max):.2f}\n")
    print(f"  {'kali W awal':>12}{'logit maks':>13}{'nan':>7}{'akurasi':>10}"
          f"  softmax")
    print("  " + "-" * 62)
    for kali in (1, 1000, 1500):
        for nama, fn in (("polos", softmax_polos),
                         ("kurangi maks", S1.softmax)):
            lm, nan, ak = bagian5_dengan(fn, kali)
            ak_s = "nan" if np.isnan(ak) else f"{ak * 100:.1f}%"
            print(f"  {kali:>12}{lm:>13.2f}{str(nan):>7}{ak_s:>10}  {nama}")

    lo, hi = 1000, 1500
    for _ in range(22):
        tengah = (lo + hi) / 2
        _, nan, _ = bagian5_dengan(softmax_polos, tengah, n_iter=1)
        lo, hi = (lo, tengah) if nan else (tengah, hi)
    lm, _, _ = bagian5_dengan(softmax_polos, hi, n_iter=1)

    print(f"""
  ambang terukur: pengali {hi:.1f}, dan logit maks di situ {lm:.2f}

  Jawabanmu benar, dan soal saya yang kurang kalibrasi. Pengali 1000 memberi
  logit terbesar 496,17, dan exp(496) itu sekitar 1e215: besar sekali, tapi
  masih muat di float64. Yang meluap baru di atas ln(1.8e308) = 709,78, dan
  itu tercapai di pengali sekitar {hi:.0f}.

  Soal 7c benar sebagai pernyataan umum, tapi angka 1000 di Soal 7d tidak
  cukup untuk membuktikannya di data ini. Kamu mengukurnya, menemukan itu,
  dan melaporkan bahwa dugaan soalnya tidak terbukti. Itu jawaban yang lebih
  baik daripada menuliskan apa yang soalnya harapkan.

  Perhatikan juga baris terakhir tabel: di pengali 1500, versi yang mengurangi
  maksimum tetap hidup tapi akurasinya jatuh ke 72,2 persen. Jadi pengurangan
  maksimum menyelamatkan dari nan, bukan dari inisialisasi yang buruk.""")


# ══════════════════════════════════════════════════════════════
# UJI B  MSE lawan entropi silang
# ══════════════════════════════════════════════════════════════

def ujiB():
    print("\n" + GARIS, "\nUJI B  MSE lawan entropi silang  (S1 Soal 4a)\n",
          GARIS, sep="")

    kos = S1.bangun_kosakata([t for t, _ in S1.DATA])
    X = np.array([S1.ke_vektor(t, kos) for t, _ in S1.DATA], dtype=float)
    y = np.array([1.0 if lab == "info_sistem" else 0.0 for _, lab in S1.DATA])

    def latih_dengan(jenis, n_iter=400, lr=0.5):
        w, b, tiba = np.zeros(X.shape[1]), 0.0, None
        for i in range(n_iter):
            p = S1.sigmoid(X @ w + b)
            if tiba is None and ((p > 0.5).astype(float) == y).all():
                tiba = i
            dz = ((p - y) / len(y) if jenis == "silang"
                  else 2 * (p - y) * p * (1 - p) / len(y))
            w -= lr * (X.T @ dz)
            b -= lr * dz.sum()
        p = S1.sigmoid(X @ w + b)
        rugi = (S1.rugi_silang(p, y) if jenis == "silang"
                else float(np.mean((p - y) ** 2)))
        return rugi, ((p > 0.5).astype(float) == y).mean(), tiba

    print(f"  {'rugi':<10}{'rugi akhir':>14}{'akurasi':>10}"
          f"{'iterasi ke 100%':>18}")
    print("  " + "-" * 52)
    for jenis in ("silang", "mse"):
        r, a, t = latih_dengan(jenis)
        print(f"  {jenis:<10}{r:>14.6f}{a * 100:>9.1f}%"
              f"{(t if t is not None else 'tidak pernah'):>18}")

    print("""
  Iterasi 54 lawan 85, persis seperti laporanmu, dan cara mengujimu benar:
  MSE diadu dengan gradien MSE-nya sendiri, bukan gradien entropi silang.
  Percobaan yang mengganti rugi tapi menyisakan gradien lama tidak menguji
  apa pun.

  Satu koreksi angka. Rugi akhir MSE terukur 0,009026, sedangkan kamu menulis
  0,000926. Kelihatannya angkanya tertukar waktu disalin. Kesimpulannya tidak
  berubah, dan memang dua kolom rugi itu tidak boleh dibandingkan langsung
  karena rumusnya beda; yang membandingkan cuma kolom iterasi.""")


# ══════════════════════════════════════════════════════════════
# UJI C  kebocoran kosakata
# ══════════════════════════════════════════════════════════════

def ujiC():
    print("\n" + GARIS, "\nUJI C  kebocoran kosakata, tiga tingkat  (S2 Soal 2b)\n",
          GARIS, sep="")

    pasang = S2.muat_perintah()
    label2i = {l: i for i, l in enumerate(sorted({l for _, l in pasang}))}

    def jalan(sumber_kos, sumber_idf, n_seed=8):
        out = {"hitung kata": [], "TF-IDF": []}
        for seed in range(n_seed):
            tr, va, te = S2.belah_tiga(pasang, seed=seed)
            kos = S2.bangun_kosakata(
                [k for k, _ in (pasang if sumber_kos == "semua" else tr)])
            idf = S2.bobot_idf(
                [k for k, _ in (pasang if sumber_idf == "semua" else tr)], kos)
            ytr = np.array([label2i[l] for _, l in tr])
            yva = np.array([label2i[l] for _, l in va])
            yte = np.array([label2i[l] for _, l in te])
            for nama, pakai in (("hitung kata", None), ("TF-IDF", idf)):
                Xtr = S2.vektorkan([k for k, _ in tr], kos, pakai)
                Xva = S2.vektorkan([k for k, _ in va], kos, pakai)
                Xte = S2.vektorkan([k for k, _ in te], kos, pakai)
                par, _ = S2.latih(Xtr, ytr, Xva, yva, len(label2i), seed=seed)
                out[nama].append(
                    ((S2.maju(par, Xva).data.argmax(1) == yva).mean(),
                     (S2.maju(par, Xte).data.argmax(1) == yte).mean()))
        return out

    print(f"  {'tingkat':<28}{'fitur':<14}{'validasi':>11}{'uji':>9}")
    print("  " + "-" * 62)
    for sk, si, nama in (("latih", "latih", "bersih"),
                         ("semua", "latih", "kosakata bocor, IDF bersih"),
                         ("semua", "semua", "kosakata + IDF bocor")):
        hasil = jalan(sk, si)
        for fitur, baris in hasil.items():
            if fitur == "hitung kata" and si == "semua":
                continue          # hitung kata tidak memakai IDF, jadi sama
            va = np.mean([b[0] for b in baris]) * 100
            te = np.mean([b[1] for b in baris]) * 100
            print(f"  {nama:<28}{fitur:<14}{va:>10.1f}%{te:>8.1f}%")

    print("""
  Keempat angka yang kamu laporkan kena persis, termasuk 68,8 dan 66,1 untuk
  TF-IDF yang bocor.

  Waktu memeriksanya saya sempat mendapat 67,7, bukan 66,1, dan sempat mengira
  angkamu meleset. Ternyata saya yang salah: saya membocorkan kosakata DAN
  IDF, padahal Soal 2b cuma menyuruh mengubah satu baris, yaitu sumber
  kosakatanya. Baris tengah tabel di atas itu percobaan yang benar, dan itu
  yang kamu jalankan.

  Perhatikan arahnya. Validasi naik dari 65,6 ke 71,9 untuk hitung kata,
  sedangkan uji justru turun dari 68,2 ke 62,5. Kebocoran tidak selalu
  menaikkan angka. Yang pasti rusak: angkanya berhenti berarti, karena sistem
  yang dilaporkan tidak sama dengan sistem yang akan kamu jalankan.""")


# ══════════════════════════════════════════════════════════════
# UJI D  ambang per intent dan lima perintah LLM
# ══════════════════════════════════════════════════════════════

AMBANG = np.array([0.55, 0.40, 0.60, 0.85, 0.85, 0.90, 0.30, 0.55])

ASING = ["fotosintesis pada tumbuhan hijau",
         "harga saham bank besok naik atau turun",
         "resep rendang padang yang enak",
         "siapa presiden pertama republik indonesia",
         "wkwkwk anjay mabar dulu gak"]

BUTUH_LLM = [
    "bandingkan hasil eksperimen ini dan cari penyebab anomalinya",
    "jelaskan backpropagation dengan bahasa yang mudah saya pahami",
    "baca dua makalah ini lalu kritik metode keduanya",
    "rancang arsitektur synesis yang aman dan jelaskan pilihanmu",
    "kenapa model ini overfit dan bagaimana memperbaikinya",
]


def ujiD():
    print("\n" + GARIS, "\nUJI D  ambang per intent, dan lima perintah LLM"
          "  (S2 Soal 5c, 8c)\n", GARIS, sep="")

    pasang = S2.muat_perintah()
    label2i = {l: i for i, l in enumerate(sorted({l for _, l in pasang}))}
    label = [l for l, _ in sorted(label2i.items(), key=lambda kv: kv[1])]

    tr, va, te = S2.belah_tiga(pasang, seed=0)
    kos = S2.bangun_kosakata([k for k, _ in tr])
    ytr = np.array([label2i[l] for _, l in tr])
    yva = np.array([label2i[l] for _, l in va])
    yte = np.array([label2i[l] for _, l in te])
    param, _ = S2.latih(S2.vektorkan([k for k, _ in tr], kos), ytr,
                        S2.vektorkan([k for k, _ in va], kos), yva,
                        len(label2i), seed=0)

    def peluang(kalimat):
        z = S2.maju(param, S2.vektorkan(kalimat, kos)).data
        e = np.exp(z - z.max(axis=1, keepdims=True))
        return e / e.sum(axis=1, keepdims=True)

    p = peluang([k for k, _ in te])
    kelas = p.argmax(1)
    lolos = p.max(1) >= AMBANG[kelas]
    print(f"  ambang per intent : {int(((kelas == yte) & lolos).sum())} benar, "
          f"{int(((kelas != yte) & lolos).sum())} salah, "
          f"{int((~lolos).sum())} menolak")
    t = np.where(p.max(1) >= 0.5, kelas, -1)
    print(f"  ambang global 0,50: {int((t == yte).sum())} benar, "
          f"{int(((t != yte) & (t != -1)).sum())} salah, "
          f"{int((t == -1).sum())} menolak")

    pa = peluang(ASING)
    print(f"  asing ditolak ambang per intent : "
          f"{int((pa.max(1) < AMBANG[pa.argmax(1)]).sum())} dari {len(ASING)}")

    pl = peluang(BUTUH_LLM)
    print(f"\n  {'perintah yang butuh LLM':<50}{'kelas':>18}{'yakin':>9}")
    print("  " + "-" * 77)
    n_glob = n_int = 0
    for k, row in zip(BUTUH_LLM, pl):
        i = int(row.argmax())
        print(f"  {k[:48]:<50}{label[i]:>18}{row[i]:>9.4f}")
        n_glob += int(row[i] < 0.5)
        n_int += int(row[i] < AMBANG[i])
    print(f"\n  ditangkap ambang global 0,50 : {n_glob} dari 5")
    print(f"  ditangkap ambang per intent  : {n_int} dari 5")

    print("""
  Semua angka di dua blok ini sama persis dengan laporanmu, termasuk kelima
  nilai keyakinan sampai empat angka di belakang koma.

  Dan kesimpulan yang kamu tarik dari situ yang paling penting: ambang ongkos
  membuat kesalahan mahal berkurang, tapi ia BUKAN pendeteksi kalimat asing.
  Nol dari lima kalimat asing tertolak, karena kelas murah seperti `obrol`
  sengaja dibuat longgar dan kalimat asing cenderung mendarat di situ.

  Dua alat yang berbeda untuk dua masalah yang berbeda, dan kamu menyebutnya
  sendiri tanpa diminta.""")


if __name__ == "__main__":
    ujiA()
    ujiB()
    ujiC()
    ujiD()
