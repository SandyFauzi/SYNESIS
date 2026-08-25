"""Peluncur SYNESIS. Isi dari SYNESIS.exe dan SYNESIS.cmd.

Berkas ini SENGAJA tidak mengimpor apa pun dari luar pustaka bawaan Python.
Alasannya bukan gaya: ia dikemas jadi .exe oleh PyInstaller, dan tiap impor
yang ditambahkan di sini ikut masuk ke dalam .exe itu. Mengimpor numpy saja
menaikkan ukurannya dari belasan megabyte jadi ratusan, dan mengimpor torch
menaikkannya jadi gigabyte.

Jadi yang dikerjakan .exe cuma satu: mencari python di dalam venv, lalu
memanggilnya. Seluruh SYNESIS tetap berjalan dari venv itu, bukan dari dalam
.exe. Model, bobot, dan data juga tetap di tempatnya masing-masing.

Bangun ulang .exe-nya:

    python scripts\\bangun_exe.py
"""

import os
import subprocess
import sys
from pathlib import Path

VENV = Path(r"E:\SYNESIS\.venv\Scripts\python.exe")
GARIS = "=" * 60

MENU = [
    ("1", "Suara, dry run", "Dengarkan dan jawab, tapi tidak ada alat dipanggil",
     ["-m", "synesis.suara", "dengar"]),
    ("2", "Suara, LIVE", "Alat benar-benar dipanggil. Berkas bisa terbuka",
     ["-m", "synesis.suara", "dengar", "--sungguhan"]),
    ("3", "Jendela, dry run", "Antarmuka tkinter, aman",
     ["-m", "synesis"]),
    ("4", "Jendela, LIVE", "Antarmuka tkinter, alat aktif",
     ["-m", "synesis", "--sungguhan"]),
    ("5", "Terminal", "Ketik perintah, tanpa jendela",
     ["-m", "synesis", "--teks"]),
    ("6", "Rekam wake word", "Rekam contoh 'hey synesis' dengan hitungan mundur",
     ["-m", "synesis.suara", "rekam", "20"]),
    ("7", "Latih wake word", "Latih ulang dari rekaman yang ada",
     ["-m", "synesis.suara", "latih"]),
    ("8", "Uji suara keluar", "Ucapkan satu kalimat dengan suara Yukino",
     ["-m", "synesis.suara", "ucap", "Halo Sandy. Saya SYNESIS."]),
    ("9", "Periksa semua", "Jalankan seluruh pemeriksa modul",
     ["-m", "synesis.uji"]),
]


def akar_repo():
    """Folder repo, baik saat dijalankan sebagai .exe maupun sebagai skrip."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent.parent


def python_venv():
    """Jalur python di dalam venv, atau None kalau tidak ada."""
    return VENV if VENV.exists() else None


def jalankan(argumen, akar):
    """Panggil python venv dengan argumen yang diberikan."""
    py = python_venv()
    if py is None:
        print(f"\n  venv tidak ditemukan di {VENV}")
        print("  Enclosure E: terpasang? Bangun ulang dengan:")
        print("    python -m venv E:\\SYNESIS\\.venv")
        print("    E:\\SYNESIS\\.venv\\Scripts\\python.exe -m pip install "
              "-r requirements.txt")
        return 1

    lingkungan = dict(os.environ)
    # Cache HuggingFace diarahkan ke enclosure supaya C: tidak kebagian
    # gigabyte diam-diam. `setdefault`, bukan penugasan: kalau kamu sudah
    # menyetel HF_HOME sendiri, setelanmu yang menang. Menimpanya berarti
    # mengunduh ulang model yang sudah ada di cache-mu, dan ContentVec saja
    # 378 MB.
    # Jalur ini harus sama dengan `konfig.HF_CACHE` dan `SYNESIS.cmd`.
    lingkungan.setdefault("HF_HOME", r"E:\SYNESIS\.cache\huggingface")
    # Keluaran Python dipaksa UTF-8 supaya nama berkas dan teks Jepang tidak
    # memicu UnicodeEncodeError di konsol Windows.
    lingkungan["PYTHONIOENCODING"] = "utf-8"
    return subprocess.call([str(py), *argumen], cwd=str(akar), env=lingkungan)


def tampilkan(akar):
    print(f"\n{GARIS}")
    print("  SYNESIS v0.2   asisten lokal, tanpa internet")
    print(GARIS)
    print(f"  repo : {akar}")
    print(f"  venv : {VENV if python_venv() else 'TIDAK DITEMUKAN'}\n")
    for kunci, nama, jelas, _ in MENU:
        print(f"   {kunci}  {nama:<20} {jelas}")
    print("   0  Keluar\n")


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    akar = akar_repo()

    # Argumen diteruskan, jadi SYNESIS.exe bisa dipakai sebagai pengganti
    # python di dalam skrip lain. Dua bentuk yang didukung:
    #
    #   SYNESIS.exe --teks               -> python -m synesis --teks
    #   SYNESIS.exe -m synesis.suara ucap hai
    #                                    -> python -m synesis.suara ucap hai
    #
    # Bendera yang berdiri sendiri diartikan sebagai bendera `synesis`,
    # karena itu yang paling sering diketik. Selain itu diteruskan apa adanya.
    if argv:
        if argv[0] != "-m" and argv[0].startswith("-"):
            argv = ["-m", "synesis", *argv]
        return jalankan(argv, akar)

    while True:
        tampilkan(akar)
        try:
            pilih = input("  pilih > ").strip()
        except (EOFError, KeyboardInterrupt):
            return 0
        if pilih in ("0", "q", "keluar"):
            return 0
        cocok = [m for m in MENU if m[0] == pilih]
        if not cocok:
            print("  pilihan tidak ada.")
            continue
        _, nama, _, argumen = cocok[0]
        print(f"\n{GARIS}\n  {nama}\n{GARIS}")
        jalankan(argumen, akar)
        input("\n  selesai. Enter untuk kembali ke menu ")


if __name__ == "__main__":
    sys.exit(main())
