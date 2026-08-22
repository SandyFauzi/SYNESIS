"""Alat yang bisa dipanggil SYNESIS: baca berkas, cari berkas, lihat sistem.

Dua keputusan desain yang perlu kamu tahu, karena keduanya soal keamanan dan
bukan soal selera.

Pertama, protokolnya satu baris teks, bukan JSON. Model 3 miliar parameter
sering gagal mengeluarkan JSON yang sah. Kalau JSON-nya rusak, seluruh
pemanggilan gagal. Satu baris `[[ALAT nama|argumen]]` jauh lebih mudah
dikeluarkan model kecil dan jauh lebih mudah diperiksa mata manusia.

Kedua, ada pagar. Alat cuma boleh menyentuh folder di konfig.FOLDER_BOLEH, dan
apa pun yang mengubah disk berhenti dulu untuk minta izin. Tanpa pagar ini,
satu salah tafsir bisa membuat SYNESIS membaca atau menghapus apa saja. Model
kecil sering salah tafsir. Ini bukan paranoia, ini perhitungan.
"""

import os
import re
import shutil
import subprocess
from pathlib import Path

import psutil

from . import konfig

POLA = re.compile(r"\[\[ALAT\s+([a-z_]+)\s*\|?\s*([^\]]*)\]\]", re.IGNORECASE)


class DitolakPagar(PermissionError):
    pass


# ══════════════════════════════════════════════════════════════
# Pagar
# ══════════════════════════════════════════════════════════════

def _aman(p):
    """Pastikan jalur berada di dalam salah satu folder yang diizinkan.

    resolve() dipanggil dulu supaya '..' dan symlink tidak bisa dipakai
    menyelinap keluar. Tanpa resolve(), 'S:/Code/../../Windows' akan lolos.
    """
    p = Path(p).expanduser().resolve()
    for boleh in konfig.FOLDER_BOLEH:
        try:
            p.relative_to(Path(boleh).resolve())
            return p
        except ValueError:
            continue
    raise DitolakPagar(
        f"'{p}' di luar folder yang diizinkan.\n"
        f"  Yang boleh: {', '.join(str(b) for b in konfig.FOLDER_BOLEH)}\n"
        f"  Ubah daftarnya di synesis/konfig.py kalau memang perlu."
    )


# ══════════════════════════════════════════════════════════════
# Alat baca, tidak mengubah apa pun
# ══════════════════════════════════════════════════════════════

def baca_berkas(arg):
    """baca_berkas|S:/Code/Make A Jarvis/log.md"""
    p = _aman(arg.strip())
    if not p.is_file():
        return f"Tidak ada berkas di {p}"
    try:
        isi = p.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        return f"Gagal membaca {p}: {e}"
    if len(isi) > konfig.BERKAS_MAKS_BACA:
        isi = isi[:konfig.BERKAS_MAKS_BACA] + "\n\n[dipotong, berkas terlalu panjang]"
    return f"Isi {p.name}:\n{isi}"


def daftar_berkas(arg):
    """daftar_berkas|S:/Code/Make A Jarvis/notebooks"""
    p = _aman(arg.strip() or konfig.AKAR)
    if not p.is_dir():
        return f"Bukan folder: {p}"
    baris = []
    for anak in sorted(p.iterdir())[:120]:
        if anak.name.startswith("."):
            continue
        tanda = "/" if anak.is_dir() else ""
        ukuran = "" if anak.is_dir() else f"  {anak.stat().st_size // 1024} KB"
        baris.append(f"  {anak.name}{tanda}{ukuran}")
    return f"Isi {p}:\n" + ("\n".join(baris) if baris else "  (kosong)")


def cari_berkas(arg):
    """cari_berkas|*.py            atau     cari_berkas|sesiA*"""
    pola = arg.strip() or "*"
    if not any(c in pola for c in "*?"):
        pola = f"*{pola}*"
    hasil = []
    for akar in konfig.FOLDER_BOLEH:
        akar = Path(akar)
        if not akar.exists():
            continue
        for p in akar.rglob(pola):
            if any(bagian.startswith(".") for bagian in p.parts):
                continue
            hasil.append(str(p))
            if len(hasil) >= 40:
                break
        if len(hasil) >= 40:
            break
    return "Ketemu:\n" + "\n".join(f"  {h}" for h in hasil) if hasil else \
        f"Tidak ada berkas cocok dengan '{pola}'"


def info_sistem(arg=""):
    """info_sistem"""
    mem = psutil.virtual_memory()
    baris = [
        f"  CPU dipakai   : {psutil.cpu_percent(interval=0.4):.0f} persen",
        f"  RAM           : {mem.used / 2**30:.1f} dari {mem.total / 2**30:.1f} GB",
    ]
    for huruf in ("C:", "E:", "S:"):
        try:
            d = shutil.disk_usage(huruf + "\\")
            baris.append(f"  Disk {huruf}       : sisa {d.free / 2**30:.0f} GB "
                         f"dari {d.total / 2**30:.0f} GB")
        except OSError:
            pass
    try:
        keluaran = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,memory.used,memory.total",
             "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=8)
        if keluaran.returncode == 0 and keluaran.stdout.strip():
            nama, pakai, total = [x.strip() for x in
                                  keluaran.stdout.strip().split(",")]
            baris.append(f"  GPU           : {nama}, VRAM {pakai} dari {total} MB")
    except (OSError, subprocess.SubprocessError, ValueError):
        baris.append("  GPU           : nvidia-smi tidak terbaca")
    return "Keadaan sistem:\n" + "\n".join(baris)


def cari_isi(arg):
    """cari_isi|gradient descent      cari teks di dalam berkas .md dan .py"""
    kata = arg.strip()
    if len(kata) < 3:
        return "Kata kunci terlalu pendek, minimal tiga huruf."
    hasil = []
    for akar in konfig.FOLDER_BOLEH:
        akar = Path(akar)
        if not akar.exists():
            continue
        for p in list(akar.rglob("*.md")) + list(akar.rglob("*.py")):
            if any(b.startswith(".") for b in p.parts):
                continue
            try:
                isi = p.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            for i, baris in enumerate(isi.splitlines(), 1):
                if kata.lower() in baris.lower():
                    hasil.append(f"  {p.name}:{i}  {baris.strip()[:90]}")
                    break
            if len(hasil) >= 25:
                break
        if len(hasil) >= 25:
            break
    return f"'{kata}' ditemukan di:\n" + "\n".join(hasil) if hasil else \
        f"'{kata}' tidak ketemu."


# ══════════════════════════════════════════════════════════════
# Alat yang mengubah sesuatu. Semuanya minta izin dulu.
# ══════════════════════════════════════════════════════════════

def jalankan(arg, izin=None):
    """jalankan|python --version

    Tidak pernah dijalankan tanpa persetujuan manusia. `izin` adalah fungsi
    yang menerima teks perintah dan mengembalikan True atau False. cli.py yang
    menyediakannya.
    """
    perintah = arg.strip()
    if not perintah:
        return "Perintah kosong."
    if izin is None or not izin(perintah):
        return f"Dibatalkan. Perintah tidak dijalankan: {perintah}"
    try:
        hasil = subprocess.run(perintah, shell=True, capture_output=True,
                               text=True, timeout=60, cwd=str(konfig.AKAR))
    except subprocess.TimeoutExpired:
        return "Perintah dihentikan karena lewat 60 detik."
    keluar = (hasil.stdout or "") + (hasil.stderr or "")
    keluar = keluar.strip()[:4000] or "(tidak ada keluaran)"
    return f"Keluar dengan kode {hasil.returncode}:\n{keluar}"


# ══════════════════════════════════════════════════════════════
# Daftar dan pengurai
# ══════════════════════════════════════════════════════════════

DAFTAR = {
    "baca_berkas": (baca_berkas, "baca isi satu berkas", False),
    "daftar_berkas": (daftar_berkas, "lihat isi folder", False),
    "cari_berkas": (cari_berkas, "cari berkas berdasarkan nama", False),
    "cari_isi": (cari_isi, "cari teks di dalam berkas", False),
    "info_sistem": (info_sistem, "CPU, RAM, disk, VRAM", False),
    "jalankan": (jalankan, "jalankan perintah shell, minta izin dulu", True),
}


def keterangan_untuk_model():
    """Teks yang diselipkan ke prompt supaya model tahu alat apa yang ada."""
    baris = [f"- {nama}: {ket}" for nama, (_, ket, _) in DAFTAR.items()]
    return (
        "Kamu punya alat. Untuk memakainya, tulis SATU baris persis begini "
        "lalu berhenti:\n"
        "[[ALAT nama_alat|argumen]]\n\n"
        "Alat yang ada:\n" + "\n".join(baris) + "\n\n"
        "Contoh:\n"
        "[[ALAT info_sistem|]]\n"
        "[[ALAT cari_berkas|*.py]]\n"
        "[[ALAT baca_berkas|S:/Code/Make A Jarvis/log.md]]\n\n"
        "Pakai alat hanya kalau memang perlu. Kalau pertanyaannya bisa "
        "dijawab langsung, jawab langsung tanpa alat."
    )


def temukan(teks):
    """Cari pemanggilan alat di jawaban model. Kembalikan (nama, argumen) atau None."""
    m = POLA.search(teks or "")
    if not m:
        return None
    nama = m.group(1).lower().strip()
    arg = m.group(2).strip()
    return (nama, arg) if nama in DAFTAR else None


def pakai(nama, arg, izin=None):
    """Jalankan satu alat, kembalikan hasilnya sebagai teks."""
    if nama not in DAFTAR:
        return f"Alat '{nama}' tidak ada."
    fungsi, _, berbahaya = DAFTAR[nama]
    try:
        return fungsi(arg, izin) if berbahaya else fungsi(arg)
    except DitolakPagar as e:
        return f"Ditolak pagar keamanan.\n{e}"
    except Exception as e:                       # noqa: BLE001
        return f"Alat '{nama}' gagal: {type(e).__name__}: {e}"
