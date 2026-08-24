"""Buat data latihan sintetis dan kumpulkan pesan nyata untuk ditinjau.

Data sintetis hanya untuk latihan. Jangan pakai sebagai data uji.
"""

import re
from pathlib import Path


AKAR = Path(__file__).resolve().parent.parent
KELUAR = AKAR / "data" / "bulan2"
TARGET_PER_INTENT = 72

PEMBUNGKUS_PERINTAH = (
    ("", ""),
    ("tolong ", ""),
    ("coba ", ""),
    ("bisa ", " gak"),
    ("sera ", ""),
    ("", " dong"),
)
PEMBUNGKUS_OBROL = (
    ("", ""),
    ("sera, ", ""),
    ("eh, ", ""),
    ("", " ya"),
    ("", " dong"),
    ("hmm, ", ""),
)

CONTOH = {
    "buka_berkas": [
        "buka laporan praktikum", "bukain modul fisika komputasi",
        "buka log terakhir", "bukakan dokumen skripsi",
        "tampilkan file roadmap", "buka notebook sesi dua",
        "buka pdf nilai semester", "bukain folder video",
        "buka gambar hasil simulasi", "tampilkan readme proyek",
        "buka dataset mnist", "buka catatan kuliah kemarin",
    ],
    "cari_berkas": [
        "cari laporan praktikum", "cariin file python yang error",
        "temukan modul fisika statistik", "cari semua gambar plot",
        "cari file yang berubah hari ini", "lihat isi folder kuliah",
        "cari notebook bulan satu", "temukan folder make a jarvis",
        "cari file bernama roadmap", "cari semua pdf di drive s",
        "cari data mnist", "temukan catatan rapat terakhir",
    ],
    "ringkas_catatan": [
        "ringkas laporan praktikum", "rangkum isi log hari ini",
        "jelaskan isi dokumen ini secara singkat", "ringkasin catatan kuliah",
        "ambil poin penting dari roadmap", "rangkum hasil eksperimen",
        "ringkas isi pdf yang dibuka", "buat intisari readme proyek",
        "rangkum perubahan kode hari ini", "ringkas catatan rapat",
        "ambil kesimpulan laporan", "ringkas materi fisika statistik",
    ],
    "jalankan_program": [
        "buka vscode", "jalankan jupyter notebook", "buka terminal",
        "jalankan python", "buka blender", "jalankan matlab",
        "buka kalkulator", "jalankan ollama", "buka peramban",
        "jalankan julia", "buka spotify", "jalankan skrip latihan",
    ],
    "kontrol_sistem": [
        "kecilkan volume", "naikkan volume", "matikan wifi",
        "nyalakan bluetooth", "kunci layar", "matikan komputer",
        "mulai ulang laptop", "naikkan kecerahan", "matikan suara",
        "aktifkan mode pesawat", "tidurkan komputer", "matikan layar",
    ],
    "jadwal": [
        "ingatkan rapat jam tiga", "jadwalkan praktikum besok pagi",
        "lihat agenda hari ini", "buat pengingat minum obat",
        "tambah jadwal ujian minggu depan", "lihat jadwal kuliah besok",
        "setel alarm jam enam", "hapus jadwal hari sabtu",
        "ingatkan kirim laporan", "tunda pengingat sepuluh menit",
        "lihat kalender bulan depan", "buat jadwal belajar malam ini",
    ],
    "hitung": [
        "hitung akar dua ratus", "ubah lima meter ke kaki",
        "hitung dua puluh persen dari seratus ribu",
        "hitung tiga pangkat empat", "ubah celsius ke fahrenheit",
        "hitung rata rata data ini", "ubah dua jam ke menit",
        "hitung integral x kuadrat", "hitung lima faktorial",
        "hitung luas lingkaran", "ubah gigabyte ke megabyte",
        "hitung sepuluh dibagi tiga",
    ],
    "obrol": [
        "halo", "apa kabar", "makasih", "selamat pagi",
        "kamu siapa", "lagi apa", "oke siap", "bagus juga",
        "sampai jumpa", "aku capek", "wkwk lucu juga", "iya paham",
    ],
    "info_sistem": [
        "cek sisa disk", "lihat pemakaian ram", "cek penggunaan cpu",
        "lihat sisa vram", "cek suhu laptop", "lihat versi python",
        "cek library python yang terpasang", "lihat kondisi baterai",
        "cek koneksi internet", "lihat proses yang sedang jalan",
        "cek ruang drive s", "lihat spesifikasi laptop",
    ],
    "ubah_proyek": [
        "kerjain bagian c", "cek jawaban saya", "buat file log",
        "rapihkan folder ini", "perbaiki error di skrip",
        "tambahkan fitur ke program", "ubah isi roadmap",
        "lengkapi bagian yang kosong", "baca dan pahami folder ini",
        "kerjain notebook sesi dua", "buat grafik hasil latihan",
        "periksa kode lalu betulkan",
    ],
    "kelola_repo": [
        "cek git status", "commit perubahan terbaru", "push folder ini",
        "tarik perubahan dari github", "lihat riwayat commit",
        "buat branch baru", "rapihkan repo sebelum push",
        "cek file yang belum dilacak", "bandingkan perubahan lokal",
        "simpan keadaan terbaru ke repo", "lihat remote repository",
        "buat pesan commit",
    ],
    "pasang_paket": [
        "install library yang dibutuhkan", "pasang paket di drive e",
        "cek paket yang sudah terinstall", "verify instalasi python",
        "buat virtual environment", "pasang requirements proyek",
        "perbarui library numpy", "hapus cache paket",
        "cek apakah cuda terpasang", "siapkan lingkungan synesis",
        "install tanpa memakai drive c", "jangan install apa pun dulu",
    ],
    "jelaskan_konsep": [
        "jelaskan setiap plot yang terbentuk", "jelasin cara kerja neural network",
        "terangkan fungsi kode ini", "jelaskan kenapa model overfit",
        "ajarkan gradient descent", "jelaskan isi bulan dua",
        "terangkan perbedaan train dan test", "jelaskan softmax dengan sederhana",
        "ajarkan cara membaca matriks bingung", "jelaskan tf idf",
        "terangkan bagian a sampai d", "jelaskan hasil eksperimen ini",
    ],
    "tanya_umum": [
        "apakah saya bisa membuat ai sendiri", "menurutmu nama synesis bagaimana",
        "mana yang lebih baik ssd e atau x", "kenapa langit berwarna biru",
        "bantu saya memilih topik penelitian", "buat rencana belajar enam bulan",
        "kritik metode dalam makalah ini", "bandingkan dua desain sistem",
        "beri ide untuk proyek fisika", "kenapa hasil eksperimen ini aneh",
        "bagaimana strategi belajar machine learning", "apa risiko memberi ai akses laptop",
    ],
    "lanjut_tugas": [
        "lanjut", "lanjutkan pekerjaan tadi", "teruskan dari bagian terakhir",
        "lanjut sesi berikutnya", "kerjakan tahap selanjutnya",
        "lanjut dari tempat kamu berhenti", "teruskan bagian b",
        "lanjut bulan dua", "selesaikan sisanya", "lanjutkan prosesnya",
        "teruskan rencana yang tadi", "oke lanjut",
    ],
}


def buat_sintetis():
    """Buat jumlah seimbang, tanpa kalimat duplikat."""
    baris = []
    for label, contoh in CONTOH.items():
        pembungkus = PEMBUNGKUS_OBROL if label == "obrol" else PEMBUNGKUS_PERINTAH
        variasi = {
            re.sub(r"\s+", " ", f"{awal}{teks}{akhir}".lower()).strip()
            for teks in contoh for awal, akhir in pembungkus
        }
        if len(variasi) < TARGET_PER_INTENT:
            raise ValueError(f"contoh {label} hanya {len(variasi)}")
        baris.extend(f"{label} | {teks}" for teks in sorted(variasi)[:TARGET_PER_INTENT])
    return baris


def ambil_pesan_nyata():
    """Ambil pesan pengguna pendek dari arsip, tanpa data pribadi mencolok."""
    hasil = []
    sumber = sorted((AKAR / "knowladge" / "sessions").glob("*/conversation.md"))
    rahasia = re.compile(
        r"(?i)(sk-[a-z0-9_-]{8,}|ghp_[a-z0-9]{8,}|api[_ -]?key\s*[:=]|"
        r"password\s*[:=]|bearer\s+[a-z0-9._-]{8,})"
    )
    for berkas in sumber:
        aktif = False
        isi = []
        for baris in berkas.read_text(encoding="utf-8").splitlines() + ["## selesai"]:
            if re.match(r"^##\s+\d+.*User\s*$", baris):
                aktif, isi = True, []
            elif baris.startswith("## "):
                if aktif and isi:
                    pesan = re.sub(r"\s+", " ", " ".join(isi)).strip()
                    pesan = re.sub(
                        r"<ide_opened_file>.*?</ide_opened_file>\s*", "", pesan,
                        flags=re.IGNORECASE,
                    )
                    pesan = re.sub(
                        r"[A-Za-z]:\\.*?\.(?:py|md|pdf|txt|jsonl?|csv|ps1)",
                        "<PATH>", pesan, flags=re.IGNORECASE,
                    )
                    if (3 <= len(pesan) <= 300 and "http" not in pesan.lower()
                            and not re.search(r"\d{6,}", pesan)
                            and not rahasia.search(pesan)
                            and "request interrupted" not in pesan.lower()):
                        hasil.append(pesan)
                aktif, isi = False, []
            elif aktif and baris.strip():
                isi.append(baris.strip())
    return sorted(set(hasil), key=str.lower)


def main():
    KELUAR.mkdir(parents=True, exist_ok=True)
    sintetis = buat_sintetis()
    pesan = ambil_pesan_nyata()

    (KELUAR / "perintah_train_generated.txt").write_text(
        "# Data sintetis untuk TRAIN saja. Jangan pakai sebagai data uji.\n"
        f"# {len(CONTOH)} intent x {TARGET_PER_INTENT} = {len(sintetis)} kalimat.\n"
        + "\n".join(sintetis) + "\n",
        encoding="utf-8",
    )
    (KELUAR / "pesan_nyata_kandidat.txt").write_text(
        "# Pesan pengguna nyata yang aman untuk ditinjau dan dilabeli manual.\n"
        "# Belum menjadi data train.\n" + "\n".join(pesan) + "\n",
        encoding="utf-8",
    )

    assert len(sintetis) == len(CONTOH) * TARGET_PER_INTENT
    assert len(sintetis) == len(set(sintetis))
    print(f"sintetis : {len(sintetis)} kalimat, {len(CONTOH)} intent")
    print(f"nyata    : {len(pesan)} kandidat aman, belum dilabeli")
    print(f"folder   : {KELUAR}")


if __name__ == "__main__":
    main()
