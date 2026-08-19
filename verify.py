"""Audit lingkungan SYNESIS.

Jalankan tiap akhir bulan: python verify.py
Memastikan tidak ada yang bocor ke C: dan venv masih sehat.
"""
import os
import sys
from pathlib import Path

OK, BAD = "  OK   ", "  ALARM"


def cek_venv():
    prefix = Path(sys.prefix)
    benar = str(prefix).upper().startswith("E:\SYNESIS")
    print(f"{OK if benar else BAD} venv aktif : {prefix}")
    if not benar:
        print("         Jalankan dulu:  . .\activate.ps1")
    return benar


def cek_envvar():
    diharapkan = {
        "PIP_CACHE_DIR": r"E:\SYNESIS\.cache\pip",
        "HF_HOME": r"E:\SYNESIS\.cache\huggingface",
        "TORCH_HOME": r"E:\SYNESIS\.cache\torch",
        "OLLAMA_MODELS": r"E:\SYNESIS\.cache\ollama",
    }
    semua = True
    for nama, nilai in diharapkan.items():
        aktual = os.environ.get(nama)
        cocok = aktual == nilai
        semua &= cocok
        print(f"{OK if cocok else BAD} {nama:<14}: {aktual or '(tidak diset)'}")
    return semua


def ukuran(path):
    p = Path(path)
    if not p.exists():
        return 0
    return sum(f.stat().st_size for f in p.rglob("*") if f.is_file())


def cek_kebocoran_c():
    lokal = Path(os.environ.get("LOCALAPPDATA", ""))
    home = Path.home()
    titik = {
        "cache pip": lokal / "pip" / "Cache",
        "cache huggingface": home / ".cache" / "huggingface",
        "cache torch": home / ".cache" / "torch",
        "model insightface": home / ".insightface",
        "model ollama": home / ".ollama" / "models",
    }
    bersih = True
    total = 0
    for nama, p in titik.items():
        b = ukuran(p)
        total += b
        if b > 50 * 1024**2:
            bersih = False
            print(f"{BAD} {nama:<18}: {b / 1024**2:,.0f} MB di C:")
        elif b:
            print(f"{OK} {nama:<18}: {b / 1024**2:,.1f} MB (kecil, aman)")
    if total == 0:
        print(f"{OK} C: benar-benar bersih")
    return bersih


def cek_torch():
    try:
        import torch
    except ImportError:
        print(f"{BAD} torch belum terpasang")
        return False
    ada = torch.cuda.is_available()
    print(f"{OK} torch {torch.__version__}")
    print(f"{OK if ada else BAD} CUDA tersedia : {ada}")
    if ada:
        bebas, total = torch.cuda.mem_get_info()
        print(f"{OK} GPU : {torch.cuda.get_device_name(0)}")
        print(f"{OK} VRAM: {bebas / 1024**3:.1f} GB bebas / {total / 1024**3:.1f} GB")
    return ada


if __name__ == "__main__":
    print("=" * 58)
    print("AUDIT LINGKUNGAN SYNESIS")
    print("=" * 58)
    hasil = []
    for judul, fn in [
        ("VENV", cek_venv),
        ("VARIABEL LINGKUNGAN", cek_envvar),
        ("KEBOCORAN KE C:", cek_kebocoran_c),
        ("PYTORCH & CUDA", cek_torch),
    ]:
        print(f"\n[{judul}]")
        hasil.append(fn())
    print("\n" + "=" * 58)
    print("LULUS SEMUA" if all(hasil) else "ADA YANG PERLU DIBERESKAN")
    print("=" * 58)
    sys.exit(0 if all(hasil) else 1)
