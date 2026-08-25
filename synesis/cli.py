"""SYNESIS v0.2 di terminal.

    python -m synesis --teks
    python -m synesis --teks --sungguhan
"""

import sys

from . import konfig, latih, niat

GARIS = "=" * 66


def repl(model, kering=True):
    mode = "DRY RUN" if kering else "LIVE"
    print(f"\n{GARIS}\n  SYNESIS v0.2  {mode}  /quit to exit"
          f"\n{GARIS}")
    if not kering:
        print("  Tools will really be called.")
    print("  /wrong <intent> fixes the last answer, /train retrains, /dry toggles.")
    sebelumnya = None

    while True:
        try:
            teks = input("\n  kamu > ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not teks:
            continue
        if teks in ("/quit", "/exit", "/keluar"):
            break
        if teks in ("/dry", "/kering"):
            kering = not kering
            print(f"  dry run: {kering}")
            continue
        if teks in ("/train", "/latih"):
            r = latih.latih()
            model = niat.muat_model()
            continue
        if teks.startswith(("/wrong ", "/salah ")):
            intent = teks.split(" ", 1)[1].strip()
            if intent not in niat.RUTE:
                print(f"  unknown intent. Pick one of: {', '.join(sorted(niat.RUTE))}")
            elif not sebelumnya:
                print("  nothing to fix yet.")
            else:
                latih.catat_koreksi(sebelumnya, intent)
                print(f"  recorded: '{sebelumnya[:40]}' -> {intent}")
            continue

        h = niat.jalankan_pipa(teks, model, izin=niat.izin_konsol,
                               kering=kering)
        print(f"  {h['intent'] or '(unknown)'}  conf {h['yakin']:.3f}  "
              f"{h['risiko'] or '-'}  -> {h['tindakan']}")
        for baris in str(h["hasil"]).splitlines()[:20]:
            print(f"    {baris}")
        sebelumnya = teks

    print(f"\n  Log: {konfig.AUDIT}")


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    repl(niat.muat_model(), kering="--sungguhan" not in argv)


if __name__ == "__main__":
    main()
