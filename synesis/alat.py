"""Alat yang bisa dipanggil SYNESIS, dan pagar yang membatasinya.

Dua lapisan, keduanya lewat `_aman`:
  1. jalur  — harus di dalam konfig.FOLDER_BOLEH, sesudah resolve()
  2. isi    — nama berkas rahasia ditolak walau letaknya sah
"""

import re
import shutil
import subprocess
from pathlib import Path

import psutil

from . import konfig

POLA = re.compile(r"\[\[ALAT\s+([a-z_]+)\s*\|?\s*([^\]]*)\]\]", re.IGNORECASE)

# Lapisan 2. Pagar jalur meloloskan .git/config, .env, dan kunci SSH selama
# letaknya di dalam FOLDER_BOLEH.
POLA_RAHASIA = re.compile(
    r"^(\.env(\..*)?|\.git|\.ssh|\.aws|\.npmrc|id_[a-z0-9]+"
    r"|.*\.(key|pem|pfx|p12)|credentials(\..*)?|secrets?\..*)$",
    re.IGNORECASE)


class DitolakPagar(PermissionError):
    pass


def _bukan_rahasia(p):
    for bagian in p.parts[1:]:
        if ":" in bagian:
            raise DitolakPagar(f"'{p}' uses an NTFS alternate data stream.")
        if POLA_RAHASIA.match(bagian):
            raise DitolakPagar(
                f"'{p}' blocked by the secrets layer via '{bagian}'.\n"
                f"  Edit POLA_RAHASIA in synesis/alat.py if you really need it.")
    return p


def _aman(p):
    """resolve() dulu, supaya '..' dan symlink tidak bisa menyelinap keluar."""
    p = Path(p).expanduser().resolve()
    for boleh in konfig.FOLDER_BOLEH:
        try:
            p.relative_to(Path(boleh).resolve())
        except ValueError:
            continue
        return _bukan_rahasia(p)
    raise DitolakPagar(
        f"'{p}' is outside the allowed folders.\n"
        f"  Allowed: {', '.join(str(b) for b in konfig.FOLDER_BOLEH)}\n"
        f"  Edit the list in synesis/konfig.py if you really need it.")


# ── alat baca ────────────────────────────────────────────────────

# Daftar berkas terakhir yang ditawarkan ke pengguna, supaya ia bisa memilih
# dengan nomor. Keadaan global memang, dan itu sesuai sifatnya: yang dimaksud
# "nomor dua" selalu daftar yang barusan disebut, bukan daftar mana pun.
PILIHAN = []


def _temukan(pola, batas=40):
    """Semua berkas di FOLDER_BOLEH yang cocok pola glob."""
    if not any(c in pola for c in "*?"):
        pola = f"*{pola}*"
    hasil = []
    for akar in konfig.FOLDER_BOLEH:
        akar = Path(akar)
        if not akar.exists():
            continue
        for p in akar.rglob(pola):
            if any(b.startswith(".") for b in p.parts) or not p.is_file():
                continue
            hasil.append(p)
            if len(hasil) >= batas:
                return hasil
    return hasil


def baca_berkas(arg):
    """Terima jalur, nama, atau potongan nama.

    `ekstrak_slot` mengembalikan frasa manusia ("laporan praktikum"), bukan
    jalur. Kalau jalurnya tidak ada, dicari dulu. Satu yang cocok dibuka;
    beberapa yang cocok dilaporkan supaya kamu yang memilih, bukan ditebak.
    """
    arg = arg.strip()
    p = _aman(arg)
    if not p.is_file():
        cocok = _temukan(arg)
        if not cocok:
            return f"No file named '{arg}' in the allowed folders."
        if len(cocok) > 1:
            # Bernomor, bukan sekadar didaftar. Nomornya yang membuat daftar
            # ini bisa dibacakan lewat suara: "satu, dua, tiga" bisa
            # diucapkan, jalur absolut tidak.
            global PILIHAN
            PILIHAN = list(cocok[:12])
            daftar = "\n".join(
                f"  {i + 1:>2}  {x.name}   {x.parent.name}"
                for i, x in enumerate(PILIHAN))
            return (f"'{arg}' matches {len(cocok)} files. "
                    f"Say the number:\n{daftar}")
        p = _bukan_rahasia(cocok[0])
    try:
        isi = p.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        return f"Could not read {p}: {e}"
    if len(isi) > konfig.BERKAS_MAKS_BACA:
        isi = isi[:konfig.BERKAS_MAKS_BACA] + "\n\n[truncated]"
    return f"{p.name}:\n{isi}"


def daftar_berkas(arg):
    p = _aman(arg.strip() or konfig.AKAR)
    if not p.is_dir():
        return f"Not a folder: {p}"
    baris = []
    for anak in sorted(p.iterdir())[:120]:
        if anak.name.startswith("."):
            continue
        tanda = "/" if anak.is_dir() else ""
        ukuran = "" if anak.is_dir() else f"  {anak.stat().st_size // 1024} KB"
        baris.append(f"  {anak.name}{tanda}{ukuran}")
    return f"{p}:\n" + ("\n".join(baris) if baris else "  (empty)")


def cari_berkas(arg):
    hasil = _temukan(arg.strip() or "*")
    return "Found:\n" + "\n".join(f"  {h}" for h in hasil) if hasil else \
        f"No file matches '{arg.strip() or '*'}'"


def cari_isi(arg):
    kata = arg.strip()
    if len(kata) < 3:
        return "Keyword too short, three letters minimum."
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
    return f"'{kata}' found in:\n" + "\n".join(hasil) if hasil else \
        f"'{kata}' not found."


def info_sistem(arg=""):
    mem = psutil.virtual_memory()
    baris = [
        f"  CPU      : {psutil.cpu_percent(interval=0.4):.0f} percent",
        f"  RAM      : {mem.used / 2**30:.1f} of {mem.total / 2**30:.1f} GB",
    ]
    for huruf in ("C:", "E:", "S:"):
        try:
            d = shutil.disk_usage(huruf + "\\")
            baris.append(f"  Disk {huruf}  : {d.free / 2**30:.0f} GB free "
                         f"of {d.total / 2**30:.0f} GB")
        except OSError:
            pass
    try:
        keluaran = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,memory.used,memory.total",
             "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=8)
        if keluaran.returncode == 0 and keluaran.stdout.strip():
            nama, pakai_, total = [x.strip() for x in
                                   keluaran.stdout.strip().split(",")]
            baris.append(f"  GPU      : {nama}, VRAM {pakai_} of {total} MB")
    except (OSError, subprocess.SubprocessError, ValueError):
        baris.append("  GPU      : nvidia-smi unavailable")
    return "System:\n" + "\n".join(baris)


# ── alat yang mengubah sesuatu ───────────────────────────────────

def jalankan(arg, izin=None):
    """`izin` fungsi(teks) -> bool. Tanpa itu, tidak pernah jalan."""
    perintah = arg.strip()
    if not perintah:
        return "Empty command."
    if izin is None or not izin(perintah):
        return f"Cancelled. Command not run: {perintah}"
    try:
        hasil = subprocess.run(perintah, shell=True, capture_output=True,
                               text=True, timeout=60, cwd=str(konfig.AKAR))
    except subprocess.TimeoutExpired:
        return "Command killed after 60 seconds."
    keluar = ((hasil.stdout or "") + (hasil.stderr or "")).strip()[:4000]
    return f"Exit code {hasil.returncode}:\n{keluar or '(no output)'}"


# ── daftar dan pengurai ──────────────────────────────────────────

DAFTAR = {
    "baca_berkas": (baca_berkas, "baca isi satu berkas", False),
    "daftar_berkas": (daftar_berkas, "lihat isi folder", False),
    "cari_berkas": (cari_berkas, "cari berkas berdasarkan nama", False),
    "cari_isi": (cari_isi, "cari teks di dalam berkas", False),
    "info_sistem": (info_sistem, "CPU, RAM, disk, VRAM", False),
    "jalankan": (jalankan, "jalankan perintah shell, minta izin dulu", True),
}


def keterangan_untuk_model():
    """Teks untuk prompt LLM di Bulan 6. Belum dipakai v0.1."""
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
        "Pakai alat hanya kalau memang perlu.")


def temukan(teks):
    m = POLA.search(teks or "")
    if not m:
        return None
    nama, arg = m.group(1).lower().strip(), m.group(2).strip()
    return (nama, arg) if nama in DAFTAR else None


def pakai(nama, arg, izin=None):
    if nama not in DAFTAR:
        return f"No such tool: '{nama}'."
    fungsi, _, berbahaya = DAFTAR[nama]
    try:
        return fungsi(arg, izin) if berbahaya else fungsi(arg)
    except DitolakPagar as e:
        return f"Blocked by the safety gate.\n{e}"
    except Exception as e:                       # noqa: BLE001
        return f"Tool '{nama}' failed: {type(e).__name__}: {e}"


def _demo():
    for jalur in ["../../../../Windows/win.ini", "C:/Users", "~/.bashrc",
                  "//localhost/C$/Windows"]:
        try:
            _aman(jalur)
            raise AssertionError(f"lolos: {jalur}")
        except (DitolakPagar, OSError):
            pass

    for jalur in [konfig.AKAR / ".git" / "config", konfig.AKAR / ".env",
                  "S:/Code/apa.key", konfig.AKAR / "log.md:ads"]:
        try:
            _aman(jalur)
            raise AssertionError(f"lolos: {jalur}")
        except DitolakPagar:
            pass

    assert _aman(konfig.AKAR / "log.md").name == "log.md"

    # nama telanjang, bukan jalur: dicari, bukan langsung gagal
    assert "log.md" in baca_berkas("log.md")
    assert "No file named" in baca_berkas("zzzqqqwww")
    assert _temukan("log.md") and all(p.is_file() for p in _temukan("*.py", 5))
    assert temukan("[[ALAT info_sistem|]]") == ("info_sistem", "")
    assert temukan("[[ALAT tidak_ada|x]]") is None
    assert temukan("bukan alat") is None
    assert "no such tool" in pakai("tidak_ada", "").lower()
    assert "Cancelled" in jalankan("echo hai")           # izin None
    assert "Cancelled" in jalankan("echo hai", lambda _: False)
    print("alat: lulus")


if __name__ == "__main__":
    _demo()
