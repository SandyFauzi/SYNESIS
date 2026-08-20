#!/usr/bin/env python3
"""Ubah transkrip Claude Code jadi JSONL berskema Codex untuk szh-ex.

Hanya pesan user dan assistant yang terlihat yang ikut. Yang dibuang:
blok thinking, tool_use, tool_result, sisipan <system-reminder>, dan
perancah perintah lokal. Ini mengikuti batas yang ditetapkan SKILL.md.
"""

import json
import re
import sys
from pathlib import Path

BUANG_TAG = re.compile(r"<system-reminder>.*?</system-reminder>", re.S)
BUANG_CMD = re.compile(
    r"<(command-name|command-message|command-args|local-command-stdout|"
    r"local-command-caveat|ide_selection)>.*?</\1>", re.S)
BUANG_KOSONG = re.compile(r"\n{3,}")

# Pesan yang memuat salah satu penanda ini bukan pesan yang terlihat.
# Isinya definisi skill, daftar alat, instruksi MCP, ringkasan sistem, atau
# keluaran hook. SKILL.md melarang mengekspor instruksi developer.
PENANDA_SISTEM = (
    "Base directory for this skill",
    "The following skills are available",
    "The following deferred tools",
    "Available agent types for the Agent tool",
    "# MCP Server Instructions",
    "This session is being continued from a previous conversation",
    "PostToolUse:",
    "<ide_diagnostics>",
    "Launching skill:",
)


def bukan_pesan_terlihat(teks: str) -> bool:
    return any(p in teks for p in PENANDA_SISTEM)


def bersihkan(teks: str) -> str:
    teks = BUANG_TAG.sub("", teks)
    teks = BUANG_CMD.sub("", teks)
    # Buang spasi di ujung baris. Exporter menjalankan git diff --cached --check
    # dan menolak commit kalau menemukannya.
    teks = "\n".join(baris.rstrip() for baris in teks.splitlines())
    teks = BUANG_KOSONG.sub("\n\n", teks)
    return teks.strip()


def teks_dari(isi) -> str:
    """Ambil hanya blok teks. Abaikan thinking, tool_use, tool_result, media."""
    if isinstance(isi, str):
        return bersihkan(isi)
    if not isinstance(isi, list):
        return ""
    bagian = []
    for blok in isi:
        if isinstance(blok, dict) and blok.get("type") == "text":
            nilai = blok.get("text")
            if isinstance(nilai, str):
                bersih = bersihkan(nilai)
                if bersih:
                    bagian.append(bersih)
    return "\n\n".join(bagian)


def main() -> int:
    sumber = Path(sys.argv[1])
    tujuan = Path(sys.argv[2])
    cwd = sys.argv[3] if len(sys.argv) > 3 else ""
    sesi = sumber.stem

    keluar = [{"type": "session_meta",
               "payload": {"session_id": sesi, "cwd": cwd, "source": "claude-code"}}]

    n_user = n_asst = n_lewat = n_sistem = 0
    for baris in sumber.open(encoding="utf-8"):
        baris = baris.strip()
        if not baris:
            continue
        rec = json.loads(baris)
        if rec.get("type") not in {"user", "assistant"}:
            continue
        pesan = rec.get("message")
        if not isinstance(pesan, dict):
            continue
        peran = pesan.get("role")
        if peran not in {"user", "assistant"}:
            continue
        teks = teks_dari(pesan.get("content"))
        if not teks:
            n_lewat += 1
            continue
        if bukan_pesan_terlihat(teks):
            n_sistem += 1
            continue
        jenis = "input_text" if peran == "user" else "output_text"
        keluar.append({"type": "response_item",
                       "payload": {"type": "message", "role": peran,
                                   "content": [{"type": jenis, "text": teks}]}})
        if peran == "user":
            n_user += 1
        else:
            n_asst += 1

    with tujuan.open("w", encoding="utf-8", newline="\n") as f:
        for rec in keluar:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    print(f"pesan user      : {n_user}")
    print(f"pesan assistant : {n_asst}")
    print(f"dilewati        : {n_lewat}  (thinking, tool, atau kosong setelah dibersihkan)")
    print(f"disaring sistem : {n_sistem}  (definisi skill, daftar alat, ringkasan sistem)")
    print(f"tujuan          : {tujuan}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
