"""SYNESIS v0.2 — asisten lokal. Nol API, nol internet, nol model bahasa.

Sejak Bulan 3 ia juga mendengar dan berbicara, dan itu pun tanpa internet:
wake word, VAD, Whisper, Piper, dan RVC semuanya berjalan dari berkas di
`E:\\SYNESIS\\models`.
"""

__version__ = "0.2.0"

from . import konfig  # noqa: F401

__all__ = ["konfig", "fitur", "niat", "alat", "cli", "jendela", "suara", "rvc"]
