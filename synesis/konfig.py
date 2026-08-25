"""Tetapan SYNESIS. Berkas lain tidak menulis angka atau jalur langsung."""

import os
from pathlib import Path

# ── jalur ────────────────────────────────────────────────────────
AKAR = Path(__file__).resolve().parent.parent
DATA = AKAR / "data" / "bulan2"
KNOWLEDGE = AKAR / "knowledge"
RIWAYAT = AKAR / "riwayat"
GUDANG = Path("E:/SYNESIS")
SUARA_DIR = GUDANG / "suara"

# Cache HuggingFace dipatok ke enclosure. Disetel sebelum modul apa pun
# mengimpor transformers, supaya C: tidak kebagian gigabyte diam-diam.
#
# `setdefault`, bukan penugasan: kalau HF_HOME sudah disetel di lingkungan,
# setelan itu yang menang. Menimpanya berarti mengunduh ulang model yang
# sudah ada di cache lain, dan ContentVec saja 378 MB.
#
# Jalur cadangannya HARUS sama dengan yang dipakai `luncur.py` dan
# `SYNESIS.cmd`. Dua jalur berbeda menghasilkan dua cache kembar, dan itu
# pernah terjadi: 1,2 GB terunduh dua kali.
HF_CACHE = GUDANG / ".cache" / "huggingface"
os.environ.setdefault("HF_HOME", str(HF_CACHE))

# Barang yang SYNESIS baca/tulis saat jalan, di dalam paketnya sendiri.
# Korpus latih tetap di DATA: itu bahan trainer, bukan bahan aplikasi.
GUDANG_MODEL = Path(__file__).resolve().parent / "model"
MODEL_INTENT = GUDANG_MODEL / "model_intent.npz"
# SYNESIS_AUDIT mengalihkan catatan ke berkas lain. Dipakai waktu uji,
# supaya jalannya pengujian tidak mengotori data latih yang sesungguhnya.
AUDIT = Path(os.environ.get("SYNESIS_AUDIT")
             or GUDANG_MODEL / "audit.jsonl")
KOREKSI = Path(os.environ.get("SYNESIS_KOREKSI")
               or GUDANG_MODEL / "koreksi.jsonl")

# Bahan trainer. UJI_NYATA tidak pernah masuk latihan.
LATIH_SINTETIS = DATA / "perintah_train_generated.txt"
UJI_NYATA = DATA / "perintah_eval_real.txt"

# Terukur: kosakata sintetis jenuh di sekitar 3.000 kalimat. Di atas itu
# latihannya makin lama tanpa satu kata baru pun.
SINTETIS_MAKS = 3000

# Porsi koreksi di dalam data latih. Tanpa pengulangan, belasan kalimat
# nyata tenggelam di antara ribuan sintetis.
PORSI_KOREKSI = 0.30

# Batas pengulangan. Tanpa ini, 3 koreksi diulang 429x masing-masing, jadi
# satu label salah berubah jadi 429 contoh latih salah. Pengulangan
# memperbesar kesalahan sekuat sinyal. Batas ini cuma menggigit waktu
# koreksinya masih sedikit; di atas 60 koreksi ia tidak berpengaruh.
ULANG_MAKS = 25

# ── resep fitur ──────────────────────────────────────────────────
# kantong  hitung kata. Nol dependensi, muat instan.
# encoder  MiniLM multibahasa. Butuh sentence-transformers.
# gabung   keduanya disambung. Titik ukur tertinggi sejauh ini, tapi
#          selisihnya masih di dalam derau di n = 41.
RESEP = ("kantong", "encoder", "gabung")
RESEP_BAWAAN = "gabung"
ENCODER = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
EMBED_CACHE = GUDANG_MODEL / "embed_cache.npz"

RIWAYAT.mkdir(exist_ok=True)
KNOWLEDGE.mkdir(exist_ok=True)

# ── niat: ongkos salah tebak ─────────────────────────────────────
# Dari dua tetapan ini keluar 15 ambang keyakinan, satu per intent, tanpa
# satu pun disetel tangan. Yang perlu tepat urutan dan rasionya.
ONGKOS_TOLAK = 1.0
ONGKOS_SALAH = {"BACA": 2.0, "TULIS": 20.0, "MERUSAK": 200.0, "BAHASA": 3.0}

# ── alat: pagar ──────────────────────────────────────────────────
FOLDER_BOLEH = [
    AKAR,
    Path("S:/Code"),
    Path("E:/SYNESIS"),
]
BUTUH_IZIN = ("hapus", "tulis", "jalankan")
BERKAS_MAKS_BACA = 60_000

# ── model bahasa (Bulan 6, belum dipakai v0.1) ───────────────────
OLLAMA = "http://127.0.0.1:11434"
MODEL_UTAMA = "qwen2.5:3b"
MODEL_NALAR = ""
SUHU = 0.7
KONTEKS_MAKS = 4096
BALASAN_MAKS = 800

POTONGAN_DIAMBIL = 3
POTONGAN_PANJANG = 900
AMBANG_MIRIP = 0.08
INGAT_GILIRAN = 6

# ── suara (Bulan 3) ──────────────────────────────────────────────
SUARA_AKTIF = True

# Pencuplikan. Alasan 16.000 ada di Soal 7 Sesi 1 Bulan 3: batas Nyquist
# 8.000 Hz menampung seluruh formant yang membedakan kata.
LAJU = 16000
BINGKAI_MS = 25            # panjang bingkai analisis
LONCAT_MS = 10             # jarak antarbingkai
N_MEL = 40                 # jumlah tapis mel

# Deteksi aktivitas suara. Ambangnya relatif terhadap lantai derau ruangan
# yang diukur sendiri saat mulai, bukan angka mutlak: kamar yang berbeda
# punya lantai derau yang berbeda sampai 20 dB.
VAD_ATAS_DB = 8.0          # berapa dB di atas lantai derau dianggap suara
VAD_DIAM_MS = 700          # sunyi selama ini dianggap ucapan sudah selesai
VAD_MIN_MS = 300           # ucapan lebih pendek dari ini diabaikan
VAD_MAKS_DETIK = 12.0      # batas atas satu ucapan

# Wake word. Model dilatih di Bulan 3 Sesi 4.
WAKE_MODEL = GUDANG / "models" / "wake" / "wake.pt"
WAKE_AMBANG = 0.90         # dikalibrasi ROC, lihat Bagian 5 Sesi 4
WAKE_HALUS = 3             # rerata bergerak atas skor, dalam jendela
WAKE_LONCAT_MS = 100       # jarak antarjendela deteksi

# Pengenal ucapan. faster-whisper, di CPU. GPU disimpan untuk Bulan 6.
STT_MODEL = "small"
STT_BAHASA = "id"
STT_PERANTI = "cpu"
STT_TIPE = "int8"

# Text-to-speech. Piper bahasa Indonesia, lalu warna suaranya diganti RVC.
# Model Piper menentukan BAHASA dan iramanya; warna suaranya ditentukan RVC.
# Jadi menambah bahasa cukup menambah satu berkas .onnx di sini.
PIPER_DIR = GUDANG / "models" / "voice" / "piper"
PIPER_SUARA = {
    "id": PIPER_DIR / "id_ID-news_tts-medium.onnx",
    "en": PIPER_DIR / "en_US-amy-medium.onnx",
    "ja": PIPER_DIR / "ja_JA-hi_fi_captain-medium.onnx",   # butuh pyopenjtalk
}
PIPER_MODEL = PIPER_SUARA["id"]
RVC_MODEL = GUDANG / "models" / "voice" / "yukino" / "Yukinoshita_Yukino.pth"
RVC_AKTIF = True
RVC_NADA = 0               # geseran semiton; sumber Piper sudah perempuan

# ── kepribadian ──────────────────────────────────────────────────
PEMILIK = "Sandy"

SISTEM = """Kamu SYNESIS, asisten pribadi lokal milik {pemilik}.

Aturan:
- Jawab ringkas. Kalau satu kalimat cukup, jangan tiga.
- Kalau tidak tahu, bilang tidak tahu. Jangan mengarang.
- Kalau ada bagian CATATAN di bawah, jawab berdasarkan itu dulu, bukan dari
  ingatanmu sendiri. Kalau CATATAN tidak menjawab, bilang begitu.
- Bahasa Indonesia, kecuali diminta lain.
- Kamu berjalan offline di laptop {pemilik}. Tidak ada internet.
""".format(pemilik=PEMILIK)
