"""Semua pemeriksa jalan sendiri. python -m synesis.uji

Catatan audit dialihkan ke berkas sementara selama uji, supaya jalannya
pengujian tidak pernah masuk ke data latih yang sesungguhnya.
"""

import sys
import tempfile
from pathlib import Path

from . import konfig

konfig.AUDIT = Path(tempfile.gettempdir()) / "synesis_uji_audit.jsonl"
konfig.KOREKSI = Path(tempfile.gettempdir()) / "synesis_uji_koreksi.jsonl"

from . import alat, fitur, jendela, latih, niat, rvc, suara  # noqa: E402


def main():
    gagal = 0
    # rvc dan suara ikut sejak Bulan 3. Keduanya tidak menyentuh mikrofon,
    # speaker, atau jaringan; yang diperiksa cuma DSP, bentuk tensor, dan
    # kecocokan kunci model kalau berkasnya kebetulan ada.
    for modul in (fitur, alat, niat, latih, jendela, suara, rvc):
        try:
            modul._demo()
        except Exception as e:                       # noqa: BLE001
            gagal += 1
            print(f"{modul.__name__.split('.')[-1]}: GAGAL "
                  f"{type(e).__name__}: {e}")
    konfig.AUDIT.unlink(missing_ok=True)
    konfig.KOREKSI.unlink(missing_ok=True)
    print("semua lulus" if not gagal else f"{gagal} modul gagal")
    return 1 if gagal else 0


if __name__ == "__main__":
    sys.exit(main())
