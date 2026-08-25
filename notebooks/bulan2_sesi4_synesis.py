"""Bulan 2 Sesi 4 - SYNESIS v0.1: tebakan jadi tindakan, dengan pagar.

Jalankan:
    . .\\scripts\\activate.ps1
    python notebooks\\bulan2_sesi4_synesis.py

Mode percakapan, sesudah semua TODO beres:
    python notebooks\\bulan2_sesi4_synesis.py --repl

Tiga sesi sebelumnya menghasilkan angka. Sesi ini menghasilkan sesuatu yang
BERTINDAK, dan itu jenis pekerjaan yang berbeda. Pengklasifikasi yang salah
menebak cuma memburukkan sebuah tabel. Asisten yang salah menebak menjalankan
perintah.

Perbedaan itu mengubah pertanyaan pokoknya. Sampai sekarang kamu bertanya
"berapa akurasinya". Mulai sekarang pertanyaannya "berapa ongkos totalnya",
dan kedua pertanyaan itu punya jawaban optimum yang berbeda.

Yang dibangun malam ini:

    1  peta intent ke alat, dan kelas risiko tiap alat
    2  ambang yang DITURUNKAN dari ongkos, bukan disetel tangan
    3  kebijakan dibandingkan dengan ongkos total, bukan akurasi
    4  slot jadi argumen, lalu diadu dengan pagar jalur
    5  catatan audit, karena asisten yang tidak bisa diulang tidak bisa diperbaiki
    6  pipa lengkap, diukur ujung ke ujung di 41 pesan nyata
    7  gerbang izin manusia, dan mode kering

Bagian 2 menutup utang paling lama di Bulan 2. Di Sesi 2 kamu menyetel
`AMBANG_INTENT` dengan tangan, lima belas angka yang dipilih karena terasa
pas. Malam ini kelima belas angka itu keluar sendiri dari dua tetapan ongkos,
dan kamu akan melihat mana yang kamu setel terlalu longgar.

Bagian bertanda TODO kamu yang isi.
"""

import json
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from bulan2_sesi2_intent import (  # noqa: E402
    AMBANG_INTENT, ekstrak_slot, muat_perintah, vektorkan)
from synesis import alat, konfig  # noqa: E402

GARIS = "=" * 66

AKAR = Path(__file__).resolve().parent.parent
DATA = AKAR / "data" / "bulan2"
MODEL = konfig.MODEL_INTENT
AUDIT = konfig.AUDIT


# ══════════════════════════════════════════════════════════════
# BAGIAN 1 - peta intent ke alat, dan kelas risiko
# ══════════════════════════════════════════════════════════════

# Empat kelas risiko. Yang membedakannya bukan seberapa rumit alatnya,
# melainkan seberapa mahal kalau alat itu dipanggil untuk perintah yang salah.
#
#   BACA    tidak mengubah apa pun. Salah panggil berarti kamu melihat isi
#           berkas yang bukan yang kamu maksud, lalu mengulang. Murah.
#   TULIS   mengubah disk, tapi bisa dibatalkan. Salah panggil berarti ada
#           berkas baru yang harus kamu bereskan.
#   MERUSAK tidak bisa dibatalkan, atau memasang sesuatu ke sistem. Salah
#           panggil bisa berarti berjam-jam membereskan.
#   BAHASA  tidak ada alatnya di v0.1. Butuh model bahasa, dan itu Bulan 6.
BACA, TULIS, MERUSAK, BAHASA = "BACA", "TULIS", "MERUSAK", "BAHASA"

# intent -> (nama alat di synesis/alat.py, kelas risiko)
# None berarti belum ada alatnya.
RUTE = {
    "buka_berkas":      ("baca_berkas", BACA),
    "cari_berkas":      ("cari_berkas", BACA),
    "info_sistem":      ("info_sistem", BACA),
    "hitung":           (None, BACA),
    "jadwal":           (None, TULIS),
    "kelola_repo":      ("jalankan", TULIS),
    "jalankan_program": ("jalankan", MERUSAK),
    "kontrol_sistem":   ("jalankan", MERUSAK),
    "pasang_paket":     ("jalankan", MERUSAK),
    "jelaskan_konsep":  (None, BAHASA),
    "lanjut_tugas":     (None, BAHASA),
    "obrol":            (None, BAHASA),
    "ringkas_catatan":  (None, BAHASA),
    "tanya_umum":       (None, BAHASA),
    "ubah_proyek":      (None, BAHASA),
}

# Ongkos satu tindakan SALAH dari tiap kelas, relatif terhadap ongkos menolak.
# Angkanya tidak perlu tepat; yang perlu tepat urutannya dan besar rasionya.
ONGKOS_TOLAK = 1.0
ONGKOS_SALAH = {BACA: 2.0, TULIS: 20.0, MERUSAK: 200.0, BAHASA: 3.0}


def muat_model(berkas=MODEL):
    """Baca model_intent.npz hasil scripts/latih_bulan2.py. Disediakan."""
    if not berkas.exists():
        raise SystemExit(
            f"Model belum ada di {berkas}.\n"
            f"  Latih dulu: python scripts\\latih_bulan2.py"
        )
    d = np.load(berkas, allow_pickle=False)
    return {
        "resep": str(d["resep"]),
        "label": [str(x) for x in d["label"]],
        "kosakata": {str(w): i for i, w in enumerate(d["kosakata"])},
        "idf": d["idf"] if d["idf"].size else None,
        "W": d["W"],
        "b": d["b"],
    }


def ramal(model, kalimat):
    """Peluang tiap intent untuk daftar kalimat. Disediakan.

    Ini persis Sesi 1: satu perkalian matriks lalu softmax. Tidak ada lapisan
    tersembunyi, karena Sesi 2 sudah mengukur bahwa yang lebih rumit tidak
    lebih baik di data nyata, dan yang sederhana menang di seri.
    """
    X = vektorkan(kalimat, model["kosakata"], model["idf"])
    logit = X @ model["W"] + model["b"]
    e = np.exp(logit - logit.max(axis=1, keepdims=True))
    return e / e.sum(axis=1, keepdims=True)


def bagian1(nyata, model):
    print(GARIS, "\nBAGIAN 1  peta intent ke alat, dan kelas risiko\n",
          GARIS, sep="")

    print(f"  model  : {MODEL.name}, resep {model['resep']}")
    print(f"  kelas  : {len(model['label'])}")
    print(f"  kolom  : {len(model['kosakata'])}\n")

    print(f"  {'intent':<18}{'alat':<15}{'risiko'}")
    print("  " + "-" * 41)
    for intent in model["label"]:
        nama, risiko = RUTE[intent]
        print(f"  {intent:<18}{nama or '-':<15}{risiko}")

    hitung = Counter(RUTE[l][1] for _, l in nyata)
    n = len(nyata)
    bisa = n - hitung[BAHASA]

    print(f"\n  Komposisi {n} pesan nyata menurut kelas risiko LABEL BENARNYA:\n")
    for kelas in (BACA, TULIS, MERUSAK, BAHASA):
        print(f"    {kelas:<10}{hitung[kelas]:>4}{hitung[kelas] / n * 100:>8.1f}%")

    print(f"""
  Jadi {bisa} dari {n} pesan yang bisa dikerjakan v0.1 sama sekali, dan
  {hitung[BAHASA]} sisanya menunggu Bulan 6.

  Angka ini beda dari yang dilaporkan Bagian 7 Sesi 3, dan bedanya bukan bug.
  Daftar `PUNYA_ALAT` di Sesi 3 memasukkan `ringkas_catatan` dan `jadwal`;
  tabel `RUTE` di sini menilai ulang keduanya, karena meringkas catatan
  sebenarnya butuh model bahasa. Soal 1 memintamu memutuskan penilaian mana
  yang benar, dan mencatat bahwa satu keputusan taksonomi menggeser angka
  utamamu tanpa satu baris kode pun berubah.

  Perhatikan juga tiga baris MERUSAK di tabel atas. Ketiganya memanggil alat
  yang sama, `jalankan`, yaitu shell. Satu salah tebak di situ menjalankan
  perintah sungguhan di mesinmu. Itulah kenapa Bagian 2 ada.""")

    return bisa


# ══════════════════════════════════════════════════════════════
# BAGIAN 2 - ambang yang diturunkan, bukan disetel
# ══════════════════════════════════════════════════════════════

def ambang_dari_ongkos(risiko, ongkos_salah=None, ongkos_tolak=ONGKOS_TOLAK):
    """Ambang keyakinan minimum supaya bertindak lebih murah daripada menolak.

    Turunkan sendiri, jangan salin hasilnya. Jalannya begini.

    Misal model memberi peluang p untuk kelas k, dan kamu sedang menimbang dua
    pilihan: bertindak sesuai k, atau menolak dan bertanya balik ke manusia.

        ongkos bertindak = ongkos_salah[risiko(k)] * (1 - p)
        ongkos menolak   = ongkos_tolak

    Baris pertama itu nilai harapan: dengan peluang p tindakanmu benar dan
    ongkosnya nol, dengan peluang (1 - p) tindakanmu salah dan ongkosnya penuh.

    Bertindak layak hanya kalau ongkos harapannya lebih kecil. Selesaikan
    pertidaksamaannya untuk p, dan kamu dapat ambangnya. Kembalikan angka itu.

    Potong hasilnya ke selang [0, 1]. Kalau ongkos_tolak lebih besar daripada
    ongkos salah, hasil aljabarnya negatif, dan itu artinya "selalu bertindak".
    Kalau ongkos_tolak nol, hasilnya 1, artinya "tidak pernah bertindak".
    Keduanya benar, dan keduanya harus terwakili dengan sopan.

    Inilah yang menggantikan `AMBANG_INTENT` di Sesi 2. Di sana kamu menulis
    lima belas angka dengan tangan dan tidak bisa menjelaskan kenapa 0,85 dan
    bukan 0,8. Sekarang kelima belasnya keluar dari dua tetapan yang PUNYA
    satuan dan bisa didebat: seberapa mahal salah, seberapa mahal bertanya.

    TODO 1
    """
    tabel = ONGKOS_SALAH if ongkos_salah is None else ongkos_salah
    c_salah = tabel[risiko]
    if c_salah <= 0:
        return 1.0
    return min(1.0, max(0.0, 1 - ongkos_tolak / c_salah))


def putuskan(peluang, label, ongkos_salah=None, ongkos_tolak=ONGKOS_TOLAK):
    """Pilih tindakan berongkos harapan terkecil, atau menolak.

    peluang : array (n_kelas,) hasil softmax untuk SATU kalimat
    label   : daftar nama kelas, sepanjang peluang

    Kembalikan (indeks_kelas, ongkos_harapan). Indeks -1 berarti menolak.

    Bedanya dengan Sesi 2 halus tapi penting. Di sana kamu mengambil argmax
    dulu, baru memeriksa ambangnya. Di sini kamu membandingkan ONGKOS semua
    kelas, dan kelas berongkos terkecil belum tentu kelas berpeluang terbesar.

    Contoh yang membuat bedanya terasa: peluang 0,55 untuk `kontrol_sistem`
    dan 0,40 untuk `info_sistem`. Argmax memilih `kontrol_sistem`. Ongkos
    harapan memilih `info_sistem`, karena 2,0 * 0,60 jauh lebih kecil daripada
    200,0 * 0,45. Model lebih yakin pada yang pertama, dan tetap saja tindakan
    yang benar adalah yang kedua.

    Itu bukan kecurangan. Itu memang keputusan yang benar waktu ongkos salahnya
    tidak sama rata, dan ongkos salah memang tidak pernah sama rata.

    Sesudah kelas termurah ketemu, bandingkan ongkosnya dengan ongkos menolak.
    Kalau menolak lebih murah, tolak.

    TODO 2
    """
    tabel = ONGKOS_SALAH if ongkos_salah is None else ongkos_salah
    ongkos = [tabel[RUTE[l][1]] * (1 - p) for l, p in zip(label, peluang)]
    k = int(np.argmin(ongkos))
    return (k, ongkos[k]) if ongkos[k] < ongkos_tolak else (-1, ongkos_tolak)


def bagian2(model):
    print("\n" + GARIS,
          "\nBAGIAN 2  ambang yang diturunkan, bukan disetel tangan\n",
          GARIS, sep="")

    print(f"  ongkos menolak dan bertanya : {ONGKOS_TOLAK}")
    for kelas in (BACA, TULIS, MERUSAK, BAHASA):
        print(f"  ongkos satu tindakan {kelas:<8}: {ONGKOS_SALAH[kelas]}")

    print(f"\n  {'intent':<18}{'risiko':<10}{'ambang tangan':>15}"
          f"{'ambang ongkos':>15}{'selisih':>10}")
    print("  " + "-" * 68)
    for intent in model["label"]:
        _, risiko = RUTE[intent]
        a_tangan = AMBANG_INTENT[intent]
        a_ongkos = ambang_dari_ongkos(risiko)
        print(f"  {intent:<18}{risiko:<10}{a_tangan:>15.3f}"
              f"{a_ongkos:>15.3f}{a_ongkos - a_tangan:>+10.3f}")

    print("""
  Baca kolom selisih dari atas ke bawah, dan cari tanda yang berulang.

  Kolom ambang tangan itu tulisanmu di Sesi 2. Kolom ambang ongkos keluar dari
  empat angka di atas tabel, tanpa satu pun keputusan per intent. Soal 2
  memintamu membaca polanya, dan menyebut jenis kesalahan sistematis apa yang
  kamu buat waktu menyetelnya dengan tangan.

  Satu hal yang perlu diakui supaya jujur: dua tetapan ongkos itu juga saya
  yang menulis, dan saya juga tidak punya pengukuran untuk 200,0. Bedanya
  bukan bahwa yang satu terukur dan yang lain tidak. Bedanya, kalau kamu tidak
  setuju dengan 200,0 kamu tinggal mengubah SATU angka dan seluruh tabel ikut
  bergerak dengan konsisten. Kalau kamu tidak setuju dengan tabel tangan, kamu
  harus menyetel ulang lima belas angka dan berharap tetap konsisten.""")


# ══════════════════════════════════════════════════════════════
# BAGIAN 3 - kebijakan diadu dengan ongkos, bukan akurasi
# ══════════════════════════════════════════════════════════════

def ongkos_kebijakan(peluang, benar, label, pilih):
    """Jalankan sebuah kebijakan atas seluruh himpunan uji, hitung ongkosnya.

    peluang : (n, n_kelas)
    benar   : (n,) indeks kelas sebenarnya
    label   : daftar nama kelas
    pilih   : fungsi(peluang_satu_baris) -> indeks kelas, atau -1 untuk menolak

    Kembalikan dict berisi, minimal:

        "benar"   jumlah tindakan yang kelasnya tepat
        "salah"   jumlah tindakan yang kelasnya meleset
        "tolak"   jumlah kali menolak
        "ongkos"  total ongkos, dijumlahkan pakai ONGKOS yang sama seperti
                  `putuskan`: tindakan benar 0, tindakan salah
                  ongkos_salah[risiko kelas YANG DIPILIH], menolak ongkos_tolak

    Perhatikan baik-baik kata "kelas YANG DIPILIH" di baris terakhir. Ongkos
    kesalahan ditanggung oleh tindakan yang KAMU AMBIL, bukan oleh maksud
    sebenarnya si pengguna. Kalau pengguna cuma mau bertanya dan kamu
    menjalankan perintah shell, yang meledak adalah shell-nya.

    Ini fungsi yang mengubah pertanyaannya. Akurasi memperlakukan semua
    kesalahan sama berat. Kolom ongkos tidak, dan kolom ongkos yang benar.

    TODO 3
    """
    h = {"benar": 0, "salah": 0, "tolak": 0, "ongkos": 0.0}
    for p, y in zip(peluang, benar):
        k = pilih(p)
        if k < 0:
            h["tolak"] += 1
            h["ongkos"] += ONGKOS_TOLAK
        elif k == y:
            h["benar"] += 1
        else:
            h["salah"] += 1
            h["ongkos"] += ONGKOS_SALAH[RUTE[label[k]][1]]
    return h


def bagian3(nyata, model):
    print("\n" + GARIS,
          "\nBAGIAN 3  tiga kebijakan, diadu dengan ongkos\n", GARIS, sep="")

    L = {l: i for i, l in enumerate(model["label"])}
    kalimat = [k for k, _ in nyata]
    benar = np.array([L[l] for _, l in nyata])
    P = ramal(model, kalimat)

    def argmax_polos(p):
        return int(p.argmax())

    def ambang_tangan(p):
        k = int(p.argmax())
        return k if p[k] >= AMBANG_INTENT[model["label"][k]] else -1

    def ambang_ongkos(p):
        return putuskan(p, model["label"])[0]

    kebijakan = [
        ("argmax polos", argmax_polos),
        ("ambang tangan Sesi 2", ambang_tangan),
        ("ongkos harapan", ambang_ongkos),
    ]

    print(f"  {'kebijakan':<24}{'benar':>7}{'salah':>7}{'tolak':>7}"
          f"{'ongkos':>10}{'ongkos/pesan':>15}")
    print("  " + "-" * 70)
    for nama, pilih in kebijakan:
        h = ongkos_kebijakan(P, benar, model["label"], pilih)
        print(f"  {nama:<24}{h['benar']:>7}{h['salah']:>7}{h['tolak']:>7}"
              f"{h['ongkos']:>10.1f}{h['ongkos'] / len(nyata):>15.2f}")

    print("""
  Sekarang baca tabelnya dua kali, dengan dua pertanyaan berbeda.

  Pertama, urutkan barisnya menurut kolom benar. Kedua, urutkan menurut kolom
  ongkos. Kalau kedua urutan itu berbeda, kamu baru saja melihat kenapa
  melaporkan akurasi untuk sistem yang bertindak itu menyesatkan.

  Soal 3 memintamu menyebut baris mana yang paling banyak benar, baris mana
  yang paling murah, dan mana yang akan kamu pasang di SYNESIS.""")

    return P, benar


# ══════════════════════════════════════════════════════════════
# BAGIAN 4 - slot jadi argumen, lalu diadu dengan pagar
# ══════════════════════════════════════════════════════════════

def slot_ke_argumen(intent, slot, kalimat):
    """Ubah hasil `ekstrak_slot` jadi argumen yang siap dikirim ke alat.

    Kembalikan string argumen, atau None kalau argumennya tidak bisa dibentuk.

    Aturan per intent:

        buka_berkas   objek dipakai sebagai pola nama berkas. Kalau tidak ada
                      slot "objek", kembalikan None; JANGAN membuka berkas
                      sembarang cuma karena intentnya sudah tertebak.
        cari_berkas   sama, tapi kalau objeknya tidak memuat * atau ?, bungkus
                      dengan bintang di kedua sisi.
        info_sistem   tidak butuh argumen, kembalikan string kosong.
        selain itu    kembalikan None.

    Baris "JANGAN membuka berkas sembarang" itu aturan yang paling gampang
    dilanggar tanpa sadar. Godaannya besar: intent sudah ketemu, keyakinan
    tinggi, sayang kalau berhenti. Tapi intent yang benar dengan argumen yang
    salah menghasilkan tindakan yang salah, dan tidak ada di lapisan mana pun
    sesudah ini yang bisa menangkapnya.

    Kembalikan None itu jawaban yang sah dan sering benar. Sesi 2 sudah
    mengajarimu itu untuk kelas; sekarang berlaku juga untuk argumen.

    TODO 4
    """
    objek = slot.get("objek", "").strip()
    if intent == "info_sistem":
        return ""
    if intent == "buka_berkas":
        return objek or None
    if intent == "cari_berkas":
        if not objek:
            return None
        return objek if any(c in objek for c in "*?") else f"*{objek}*"
    return None


SERANGAN_JALUR = [
    "S:/Code/Make A Jarvis/../../Windows/System32/config/SAM",
    "../../../../../../Windows/win.ini",
    "C:/Users/SANDY FAUZI/.ssh/id_rsa",
    "S:/Code/Make A Jarvis/../../../Users",
    "~/.bash_history",
    "\\\\?\\C:\\Windows\\System32\\drivers\\etc\\hosts",
    "S:/Code/Make A Jarvis/./../../boot.ini",
    "//localhost/C$/Windows",
    # Empat serangan tambahan milik pemilik. Ramalan ditulis lebih dulu,
    # sebelum satu pun dijalankan (Soal 5b):
    #   1 DITOLAK. relative_to() membandingkan komponen jalur, bukan awalan
    #     string, jadi "CodeRahasia" bukan anak dari "Code". Pagar yang
    #     memakai startswith() akan meloloskan baris ini.
    #   2 LOLOS, dan memang seharusnya. ".." yang keluar lalu masuk lagi
    #     berakhir di dalam pagar. Menolaknya berarti pagar menolak ".."
    #     sebagai token, bukan menolak tujuannya.
    #   3 LOLOS. Ada di dalam FOLDER_BOLEH, dan isinya alamat remote serta
    #     kadang kredensial. Pagar jalur memang tidak melihat isi. Soal 5e.
    #   4 LOLOS pagar. Aliran data alternatif NTFS: nama berkas induknya sah,
    #     jadi resolve() tetap menaruhnya di dalam S:/Code.
    "S:/CodeRahasia/rahasia.txt",
    "S:/Code/Make A Jarvis/../../Code/Make A Jarvis/log.md",
    "S:/Code/Make A Jarvis/.git/config",
    "S:/Code/Make A Jarvis/log.md:rahasia",
]


def uji_pagar(serangan=SERANGAN_JALUR):
    """Adu `alat._aman` dengan jalur yang seharusnya ditolak.

    Untuk tiap jalur di `serangan`, panggil `alat._aman(jalur)` dan catat
    apakah ia menolak. Kembalikan daftar (jalur, ditolak, keterangan) dengan
    `ditolak` bernilai True kalau `DitolakPagar` terlempar.

    Perhatikan bahwa lolos itu BUKAN berarti alatnya akan membaca berkasnya.
    `_aman` cuma memeriksa jalur ada di dalam FOLDER_BOLEH. Kalau ada jalur
    yang lolos padahal seharusnya tidak, laporkan sebagai lolos, jangan
    dilunakkan.

    Kenapa daftar ini ditulis sebagai serangan, bukan sebagai kasus uji biasa:
    karena cara berpikirnya berbeda. Kasus uji biasa menanyakan "apakah yang
    seharusnya jalan itu jalan". Uji pagar menanyakan "apakah yang seharusnya
    mustahil itu benar-benar mustahil", dan untuk menjawabnya kamu harus
    berusaha menembusnya sendiri.

    Tambahkan minimal tiga seranganmu sendiri sebelum menyatakan bagian ini
    selesai. Soal 5 menanyakan seranganmu apa dan kenapa kamu memilihnya.

    TODO 5
    """
    hasil = []
    for jalur in serangan:
        try:
            hasil.append((jalur, False, f"lolos jadi {alat._aman(jalur)}"))
        except alat.DitolakPagar:
            hasil.append((jalur, True, "DitolakPagar"))
        except OSError as e:            # jalur tidak bisa di-resolve sama sekali
            hasil.append((jalur, True, f"galat {type(e).__name__}"))
    return hasil


def bagian4(model):
    print("\n" + GARIS,
          "\nBAGIAN 4  slot jadi argumen, lalu diadu dengan pagar\n",
          GARIS, sep="")

    contoh = ["buka laporan praktikum minggu lalu",
              "cariin file py yang berubah kemarin",
              "berapa sisa disk",
              "buka"]
    Pc = ramal(model, contoh)
    print(f"  {'kalimat':<38}{'intent':<19}{'argumen'}")
    print("  " + "-" * 75)
    for k, p in zip(contoh, Pc):
        i = int(p.argmax())
        intent = model["label"][i]
        arg = slot_ke_argumen(intent, ekstrak_slot(k), k)
        tampil = "(None, berhenti)" if arg is None else f"'{arg}'"
        print(f"  {k[:36]:<38}{intent:<19}{tampil}")

    print("\n  Pagar jalur:\n")
    hasil = uji_pagar()
    lolos = [h for h in hasil if not h[1]]
    for jalur, ditolak, ket in hasil:
        tanda = "ditolak" if ditolak else "LOLOS  "
        print(f"    {tanda}  {jalur[:52]}")

    print(f"""
  {len(hasil) - len(lolos)} dari {len(hasil)} serangan ditolak.

  Folder yang diizinkan sekarang: {', '.join(str(b) for b in konfig.FOLDER_BOLEH)}

  Kalau ada baris LOLOS di atas, berhenti di sini dan betulkan
  `synesis/alat._aman` sebelum melanjutkan ke Bagian 5. Bagian 5 mulai
  benar-benar memanggil alat.""")

    if lolos:
        print("\n  ADA SERANGAN YANG LOLOS. Jangan lanjut sebelum beres.")


# ══════════════════════════════════════════════════════════════
# BAGIAN 5 - catatan audit, lalu pipa lengkap
# ══════════════════════════════════════════════════════════════

def catat_audit(baris, berkas=AUDIT):
    """Tambahkan satu baris JSON ke berkas audit. Hanya menambah, tidak menimpa.

    `baris` dict. Tambahkan sendiri kunci "waktu" berisi cap waktu UTC format
    ISO kalau belum ada, lalu tulis sebagai satu baris JSON diakhiri newline.

    Pakai mode "a", dan pastikan foldernya ada. Pakai `ensure_ascii=False`
    supaya kalimat berbahasa Indonesia tetap terbaca mata manusia di dalam
    berkasnya.

    Kenapa JSONL dan bukan JSON biasa: berkas JSON harus utuh untuk bisa
    dibaca, jadi kalau proses mati di tengah penulisan seluruh riwayatmu
    rusak. JSONL rusak paling banter satu baris terakhir, dan baris-baris
    sebelumnya tetap terbaca.

    Kenapa hanya menambah: karena catatan audit yang bisa diubah bukan catatan
    audit. Kalau SYNESIS boleh menulis ulang riwayatnya sendiri, riwayat itu
    tidak bisa dipakai sebagai bukti tentang apa yang terjadi.

    Dan inilah alasan sebenarnya bagian ini ada, yang bukan soal keamanan
    sama sekali. Bagian 7 Sesi 3 menemukan bahwa kekurangan terbesar Bulan 2
    adalah catatan pemakaian yang mewakili. Berkas ini adalah alat pengumpul
    itu. Tiap kali kamu memakai SYNESIS, ia menambah satu baris data latih
    yang tidak dikarang siapa pun.

    TODO 6
    """
    baris = {"waktu": datetime.now(timezone.utc).isoformat(), **baris}
    berkas.parent.mkdir(parents=True, exist_ok=True)
    with berkas.open("a", encoding="utf-8") as f:
        print(json.dumps(baris, ensure_ascii=False), file=f)


# ══════════════════════════════════════════════════════════════
# Pipa lengkap, dan gerbang izinnya
# ══════════════════════════════════════════════════════════════

def izin_konsol(rencana):
    """Tanya manusia sebelum tindakan berisiko. Disediakan.

    Kembalikan True kalau dijawab 'y'. Apa pun selain itu, termasuk enter
    kosong, berarti tidak. Bawaannya menolak, dan itu memang harus.
    """
    print(f"\n  SYNESIS mau menjalankan: {rencana}")
    return input("  Izinkan? [y/T] ").strip().lower() == "y"


def jalankan_pipa(kalimat, model, izin=None, kering=True):
    """Satu perintah, dari teks sampai tindakan.

    Kembalikan dict berisi minimal kunci: "kalimat", "intent", "yakin",
    "risiko", "alat", "argumen", "tindakan", "hasil".

    "tindakan" salah satu dari: "jalan", "tolak_yakin", "tolak_argumen",
    "tolak_izin", "belum_ada_alat".

    Urutannya, dan tiap langkah boleh menghentikan yang berikutnya:

        1  ramal peluang
        2  `putuskan` -> kalau -1, tindakan "tolak_yakin", berhenti
        3  cari rutenya. Kalau alatnya None, "belum_ada_alat", berhenti
        4  `ekstrak_slot` lalu `slot_ke_argumen`. Kalau None,
           "tolak_argumen", berhenti
        5  kalau risikonya bukan BACA, minta izin lewat `izin`. Kalau tidak
           ada fungsi izin atau jawabannya tidak, "tolak_izin", berhenti
        6  kalau `kering` True, jangan panggil alatnya; isi hasil dengan
           keterangan bahwa ini mode kering. Kalau False, panggil
           `alat.pakai(nama, argumen, izin)`
        7  catat semuanya lewat `catat_audit`, apa pun tindakannya

    Perhatikan langkah 7. Yang dicatat BUKAN cuma yang jalan. Yang ditolak
    justru yang paling berharga, karena baris itulah yang memberitahumu
    kalimat apa yang SYNESIS belum bisa tangani, dan itu daftar pekerjaan
    berikutnya yang tidak dikarang siapa pun.

    Perhatikan juga bahwa `kering` bawaannya True. Alat yang bisa menjalankan
    shell tidak boleh punya bawaan yang menjalankan shell.

    TODO 7
    """
    peluang = ramal(model, [kalimat])[0]
    k, _ = putuskan(peluang, model["label"])
    # Waktu menolak, yang dicatat tetap tebakan terkuat model, supaya baris
    # audit bisa dibaca sebagai "ini yang model kira, dan ini kenapa ditahan".
    i = k if k >= 0 else int(peluang.argmax())
    intent = model["label"][i]
    nama, risiko = RUTE[intent]
    h = {"kalimat": kalimat, "intent": intent, "yakin": float(peluang[i]),
         "risiko": risiko, "alat": nama, "argumen": None,
         "tindakan": "jalan", "hasil": ""}

    if k < 0:
        h["tindakan"] = "tolak_yakin"
    elif nama is None:
        h["tindakan"] = "belum_ada_alat"
    else:
        h["argumen"] = slot_ke_argumen(intent, ekstrak_slot(kalimat), kalimat)
        if h["argumen"] is None:
            h["tindakan"] = "tolak_argumen"
        elif risiko != BACA and not (izin and izin(f"{nama}|{h['argumen']}")):
            h["tindakan"] = "tolak_izin"
        elif kering:
            h["hasil"] = f"(kering) {nama}|{h['argumen']} tidak dipanggil"
        else:
            h["hasil"] = alat.pakai(nama, h["argumen"], izin)

    catat_audit(h)
    return h


def bagian5(nyata, model):
    print("\n" + GARIS,
          "\nBAGIAN 5  pipa lengkap, dan catatannya\n", GARIS, sep="")

    print("""  Semua dijalankan dalam mode kering. Tidak ada berkas dibuka, tidak ada
  perintah shell jalan. Yang diukur keputusannya, bukan akibatnya.
""")

    hasil = [jalankan_pipa(k, model, izin=None, kering=True) for k, _ in nyata]
    hitung = Counter(h["tindakan"] for h in hasil)
    n = len(nyata)

    print(f"  {'tindakan':<20}{'jumlah':>8}{'bagian':>9}")
    print("  " + "-" * 37)
    for t in ("jalan", "tolak_yakin", "tolak_argumen", "tolak_izin",
              "belum_ada_alat"):
        print(f"  {t:<20}{hitung[t]:>8}{hitung[t] / n * 100:>8.1f}%")

    jalan = [(h, l) for h, (_, l) in zip(hasil, nyata) if h["tindakan"] == "jalan"]
    tepat = sum(1 for h, l in jalan if h["intent"] == l)

    meleset = hitung["jalan"] - tepat
    print(f"""
  Dari {n} pesan nyata, hanya {hitung['jalan']} yang sampai ke tahap
  bertindak, dan {tepat} di antaranya intentnya memang tepat.

  Tapi angka yang perlu kamu bawa keluar dari sini bukan yang tepat. Yang
  perlu kamu bawa adalah yang meleset, yaitu {meleset}: berapa kali SYNESIS
  akan bertindak berdasarkan intent yang salah. Kalau angka itu nol, pagarnya
  bekerja. Kalau tidak, Soal 6 memintamu menelusuri kalimat mana dan lapisan
  mana yang gagal menahannya.

  Dan angka terpenting untuk Bulan 3 adalah yang berhenti karena intentnya
  belum punya alat sama sekali, yaitu {hitung['belum_ada_alat']} pesan. Itu
  bukan kesalahan model. Itu daftar pekerjaan.

  Keempat puluh satu keputusan di atas sudah tercatat sebagai baris di
  {AUDIT.name}, termasuk yang ditolak. Berkas itulah yang akan tumbuh jadi
  data latih nyatamu.""")

    if jalan:
        print("\n  Yang sampai bertindak:\n")
        for h, l in jalan:
            tanda = "tepat" if h["intent"] == l else "MELESET"
            print(f"    {tanda:<8}{h['intent']:<16}yakin {h['yakin']:.3f}  "
                  f"'{h['kalimat'][:40]}'")

    return hasil


# ══════════════════════════════════════════════════════════════
# Mode percakapan
# ══════════════════════════════════════════════════════════════

def repl(model, kering=True):
    """SYNESIS v0.1 tanpa LLM. Disediakan.

    Inilah kalimat "selesai bila" dari rencana Bulan 2: kamu mengetik perintah
    dan berkasnya terbuka, lewat pengklasifikasi yang kamu latih sendiri.
    """
    mode = "KERING" if kering else "SUNGGUHAN"
    print(f"\n{GARIS}\n  SYNESIS v0.1  mode {mode}  ketik /keluar untuk "
          f"berhenti\n{GARIS}")
    if not kering:
        print("  Mode sungguhan. Alat akan benar-benar dipanggil.\n")

    while True:
        try:
            teks = input("\n  kamu > ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not teks:
            continue
        if teks in ("/keluar", "/exit", "/quit"):
            break
        if teks == "/kering":
            kering = not kering
            print(f"  mode kering: {kering}")
            continue

        h = jalankan_pipa(teks, model, izin=izin_konsol, kering=kering)
        print(f"  intent  : {h['intent']}  (yakin {h['yakin']:.3f}, "
              f"risiko {h['risiko']})")
        print(f"  tindakan: {h['tindakan']}")
        if h["hasil"]:
            for baris in str(h["hasil"]).splitlines()[:20]:
                print(f"    {baris}")

    print(f"\n  Catatan tersimpan di {AUDIT}")


# ══════════════════════════════════════════════════════════════
# BAGIAN 6 - apa yang jadi, apa yang belum
# ══════════════════════════════════════════════════════════════

def bagian6(bisa, hasil, n):
    print("\n" + GARIS, "\nBAGIAN 6  apa yang jadi, apa yang belum\n",
          GARIS, sep="")

    hitung = Counter(h["tindakan"] for h in hasil)
    print(f"""  Yang jadi malam ini:

    - lima belas ambang diturunkan dari dua tetapan ongkos, bukan disetel
    - kebijakan dibandingkan dengan ongkos total, dan urutannya beda dari
      urutan menurut akurasi
    - pagar jalur diadu dengan serangan, bukan diasumsikan bekerja
    - catatan audit yang hanya bisa ditambah
    - pipa lengkap dengan mode kering sebagai bawaan

  Yang belum, dan angkanya:

    - {n - bisa} dari {n} pesan nyata butuh model bahasa. Itu Bulan 6.
    - {hitung['belum_ada_alat']} pesan berhenti karena intentnya belum punya
      alat sama sekali, dan sebagian di antaranya sebenarnya bisa dibuatkan
      alat tanpa LLM.
    - catatan audit masih kosong sampai kamu benar-benar memakainya.

  Baris terakhir itu pekerjaan rumah yang sesungguhnya, dan ia tidak selesai
  dengan mengetik kode. Ia selesai dengan memakai SYNESIS beberapa minggu
  sampai `audit.jsonl` cukup panjang untuk melatih ulang. Itu satu-satunya
  jalan keluar dari lingkaran yang diukur Sesi 3: data sintetis tidak mewakili
  cara kamu bicara, dan satu-satunya cara mendapat data yang mewakili adalah
  merekam pemakaian sungguhan.

  Soal 8 memintamu menyusun rencana pengumpulan itu, lengkap dengan kapan
  kamu berhenti mengumpulkan dan mulai melatih ulang.""")


# ══════════════════════════════════════════════════════════════

def main():
    mulai = time.perf_counter()
    model = muat_model()
    nyata = muat_perintah(DATA / "perintah_eval_real.txt")

    if "--repl" in sys.argv:
        repl(model, kering="--sungguhan" not in sys.argv)
        return

    bisa = bagian1(nyata, model)
    bagian2(model)
    bagian3(nyata, model)
    bagian4(model)
    hasil = bagian5(nyata, model)
    bagian6(bisa, hasil, len(nyata))

    print(f"\n{GARIS}")
    print(f"  selesai dalam {time.perf_counter() - mulai:.1f} detik")
    print(f"  mode percakapan: python notebooks\\bulan2_sesi4_synesis.py --repl")
    print(GARIS)


if __name__ == "__main__":
    main()
