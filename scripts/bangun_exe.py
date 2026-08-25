"""Bangun SYNESIS.exe dari synesis/luncur.py.

    python scripts\\bangun_exe.py

Yang dikemas HANYA peluncurnya, bukan SYNESIS-nya. Peluncur itu memanggil
python di dalam `E:\\SYNESIS\\.venv`, jadi torch, onnxruntime, dan seluruh
bobot model tetap di tempatnya dan tidak ikut masuk ke dalam .exe.

Bedanya besar dan layak diukur:

    kemas peluncur saja   ~10 MB, dibangun dalam belasan detik
    kemas seluruh SYNESIS ~3 GB, dibangun dalam belasan menit, dan pecah tiap
                          kali torch atau onnxruntime menambah berkas data
                          yang tidak terdeteksi PyInstaller

Konsekuensinya: .exe ini TIDAK bisa dipindah ke komputer lain begitu saja.
Ia peluncur, bukan paket portabel. Untuk memindahkan SYNESIS, yang dipindah
repo dan `E:\\SYNESIS`.

PyInstaller hanya dibutuhkan untuk membangun ulang, tidak untuk menjalankan.
"""

import shutil
import subprocess
import sys
from pathlib import Path

AKAR = Path(__file__).resolve().parent.parent
SUMBER = AKAR / "synesis" / "luncur.py"
KELUAR = AKAR / "SYNESIS.exe"
KERJA = AKAR / "scratch" / "exe"


def main():
    if not SUMBER.exists():
        print(f"tidak ada {SUMBER}")
        return 1
    try:
        import PyInstaller  # noqa: F401
    except ImportError:
        print("PyInstaller belum terpasang. Pasang dulu:")
        print(f"  {sys.executable} -m pip install pyinstaller")
        return 1

    KERJA.mkdir(parents=True, exist_ok=True)
    perintah = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--console",
        "--name", "SYNESIS",
        "--distpath", str(KERJA / "dist"),
        "--workpath", str(KERJA / "build"),
        "--specpath", str(KERJA),
        # Tidak ada satu pun paket berat yang perlu ikut. Daftar ini menahan
        # PyInstaller kalau suatu saat luncur.py tidak sengaja mengimpornya.
        "--exclude-module", "numpy",
        "--exclude-module", "torch",
        "--exclude-module", "onnxruntime",
        "--exclude-module", "transformers",
        "--exclude-module", "matplotlib",
        "--exclude-module", "scipy",
        "--exclude-module", "tkinter",
        str(SUMBER),
    ]
    print("  " + " ".join(perintah[:6]) + " ...\n")
    kode = subprocess.call(perintah, cwd=str(AKAR))
    if kode != 0:
        return kode

    jadi = KERJA / "dist" / "SYNESIS.exe"
    shutil.copy2(jadi, KELUAR)
    print(f"\n  {KELUAR}  {KELUAR.stat().st_size / 1e6:.1f} MB")
    print("  Klik dua kali untuk memakainya.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
