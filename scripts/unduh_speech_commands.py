"""Unduh Google Speech Commands v0.02, ambil hanya kata yang dipakai.

    python scripts\\unduh_speech_commands.py

Arsipnya 2,4 GB dan berisi 35 kata. Bulan 3 hanya memakai 10 kata inti
ditambah kolam kata asing dan derau latar, jadi sekitar 250 MB. Arsip dibaca
sebagai aliran (`r|gz`) dan tidak pernah mendarat utuh di disk: gzip tidak
bisa dilompati, jadi 2,4 GB tetap mengalir lewat kabel, tetapi yang ditulis
hanya yang dipakai.

Aman diulang. Berkas yang sudah ada dilewati, dan unduhan yang putus di
tengah tinggal dijalankan lagi.
"""

import sys
import tarfile
import time
import urllib.request
from pathlib import Path

URL = "http://download.tensorflow.org/data/speech_commands_v0.02.tar.gz"
TUJUAN = Path("E:/SYNESIS/data/speech_commands")

INTI = ("yes", "no", "up", "down", "left", "right", "on", "off", "stop", "go")
ASING = ("bed", "bird", "cat", "dog", "happy", "house", "marvin", "sheila",
         "tree", "wow")
DERAU = "_background_noise_"

# Dua berkas daftar milik dataset. Tanpa keduanya, belahan latih/valid/uji
# tidak bisa direproduksi, dan pembicara yang sama bisa jatuh di dua belahan.
DAFTAR = ("validation_list.txt", "testing_list.txt", "LICENSE", "README.md")

DIPAKAI = set(INTI) | set(ASING) | {DERAU}


def rapikan(nama):
    """Buang awalan './' yang dipakai arsip ini di setiap anggotanya."""
    return nama[2:] if nama.startswith("./") else nama


def dipilih(nama):
    """True kalau anggota tar ini termasuk yang kita simpan."""
    if nama in DAFTAR:
        return True
    bagian = nama.split("/")
    return len(bagian) == 2 and bagian[0] in DIPAKAI


def main():
    TUJUAN.mkdir(parents=True, exist_ok=True)
    print(f"sumber : {URL}\ntujuan : {TUJUAN}\n")

    n = lewat = 0
    mb = 0.0
    mulai = time.perf_counter()
    # Arsip penuhnya 2.429 MB dan seluruhnya tetap mengalir lewat kabel,
    # jadi bilahnya menakar byte yang diunduh, bukan berkas yang disimpan.
    TOTAL_MB = 2429.0
    with urllib.request.urlopen(URL, timeout=60) as aliran:
        # r|gz = mode aliran. tarfile tidak bisa mundur, jadi tiap anggota
        # diputuskan sekali saat lewat.
        with tarfile.open(fileobj=aliran, mode="r|gz") as tar:
            for anggota in tar:
                nama = rapikan(anggota.name)
                if not anggota.isfile() or not dipilih(nama):
                    continue
                keluar = TUJUAN / nama
                if keluar.exists():
                    lewat += 1
                    continue
                keluar.parent.mkdir(parents=True, exist_ok=True)
                isi = tar.extractfile(anggota).read()
                keluar.write_bytes(isi)
                n += 1
                mb += len(isi) / 1e6
                if n % 100 == 0:
                    lewat_detik = time.perf_counter() - mulai
                    laju = aliran.tell() / 1e6 / max(1e-9, lewat_detik)
                    unduh_mb = aliran.tell() / 1e6
                    isi = int(36 * min(1.0, unduh_mb / TOTAL_MB))
                    print(f"\r  |{'#' * isi}{'.' * (36 - isi)}| "
                          f"{unduh_mb:6.0f}/{TOTAL_MB:.0f} MB  "
                          f"{laju:4.2f} MB/s  sisa ~"
                          f"{(TOTAL_MB - unduh_mb) / max(0.01, laju) / 60:4.1f} menit  "
                          f"{n} berkas   ", end="", flush=True)

    print(f"\n\nselesai dalam {(time.perf_counter() - mulai) / 60:.1f} menit. "
          f"{n} berkas baru, {lewat} sudah ada, {mb:.1f} MB ditulis.")
    for kata in INTI:
        d = TUJUAN / kata
        print(f"  {kata:8s} {len(list(d.glob('*.wav'))) if d.exists() else 0:5d}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
