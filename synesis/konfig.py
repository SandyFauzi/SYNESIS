"""Semua tetapan SYNESIS di satu tempat.

Kalau ada yang perlu diubah, ubahnya di sini. Berkas lain tidak boleh punya
angka atau jalur yang ditulis langsung. Aturan ini penting karena mulai 27
Agustus kamu yang merawat sendiri, dan mencari satu angka di satu berkas jauh
lebih cepat daripada menyisir tujuh berkas.
"""

from pathlib import Path

# ══════════════════════════════════════════════════════════════
# Jalur
# ══════════════════════════════════════════════════════════════

AKAR = Path(__file__).resolve().parent.parent
KNOWLEDGE = AKAR / "knowledge"
RIWAYAT = AKAR / "riwayat"
GUDANG = Path("E:/SYNESIS")          # enclosure, di luar repo
SUARA_DIR = GUDANG / "suara"         # berkas model Piper

RIWAYAT.mkdir(exist_ok=True)
KNOWLEDGE.mkdir(exist_ok=True)


# ══════════════════════════════════════════════════════════════
# Model
# ══════════════════════════════════════════════════════════════

# Alamat Ollama. Ollama menyalakan server HTTP lokal di port ini.
OLLAMA = "http://127.0.0.1:11434"

# Model utama. Qwen2.5 3B dipilih karena paling patuh saat diminta
# mengeluarkan format tertentu, dan itu yang dibutuhkan untuk pemanggilan alat.
MODEL_UTAMA = "qwen2.5:3b"

# Model cadangan untuk penalaran dan matematika. Kosongkan kalau tidak dipakai,
# karena tiap pergantian model memaksa bongkar-pasang VRAM sekitar 5-15 detik.
MODEL_NALAR = ""          # contoh: "phi3:mini"

SUHU = 0.7                # makin tinggi makin liar, 0 berarti selalu sama
KONTEKS_MAKS = 4096       # token yang dimuat model sekaligus
BALASAN_MAKS = 800        # batas panjang jawaban


# ══════════════════════════════════════════════════════════════
# Ingatan dan pencarian
# ══════════════════════════════════════════════════════════════

# Berapa potongan knowledge/ yang diselipkan ke prompt tiap pertanyaan.
# Terlalu banyak membuat model bingung dan konteks penuh. Tiga cukup.
POTONGAN_DIAMBIL = 3

# Panjang satu potongan dalam karakter. Dipotong per paragraf, bukan per kata,
# supaya kalimatnya tidak terputus di tengah.
POTONGAN_PANJANG = 900

# Ambang kemiripan. Di bawah ini dianggap tidak relevan dan tidak diselipkan.
# Lebih baik tidak memberi konteks daripada memberi konteks yang salah.
AMBANG_MIRIP = 0.08

# Berapa giliran percakapan terakhir yang diingat dalam satu sesi.
INGAT_GILIRAN = 6


# ══════════════════════════════════════════════════════════════
# Alat
# ══════════════════════════════════════════════════════════════

# Folder yang boleh dibaca alat. Di luar ini ditolak. Ini pagar keamanan,
# bukan saran. Tanpa ini satu salah tafsir bisa membuat SYNESIS membaca
# atau menghapus apa pun di disk.
FOLDER_BOLEH = [
    AKAR,
    Path("S:/Code"),
    Path("E:/SYNESIS"),
]

# Perintah yang butuh konfirmasi manusia sebelum dijalankan.
BUTUH_IZIN = ("hapus", "tulis", "jalankan")

BERKAS_MAKS_BACA = 60_000     # karakter, biar tidak membanjiri konteks


# ══════════════════════════════════════════════════════════════
# Suara
# ══════════════════════════════════════════════════════════════

SUARA_AKTIF = False           # dinyalakan lewat perintah /suara
SUARA_MODEL = "en_US-amy-medium"   # nama berkas Piper tanpa ekstensi


# ══════════════════════════════════════════════════════════════
# Kepribadian
# ══════════════════════════════════════════════════════════════

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
