"""Bangun timeline Remotion dari setiap baris nonkosong Sesi 1-4."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent / "src" / "storyboard.json"
FPS = 30
MANIM_FRAMES = {"sesi1": 281, "sesi2": 258, "sesi34": 251, "sesi4": 248}

SOURCES = (
    ("sesi1", "SESI 1 · MESIN AUTOGRAD", "notebooks/bulan1_sesi1_autograd.py", None),
    ("sesi2", "SESI 2 · JARINGAN SARAF", "notebooks/bulan1_sesi2_mlp.py", None),
    ("sesi34", "SESI 3 · MNIST & DUA DINDING", "notebooks/bulan1_sesi34_mnist.py", (1, 333)),
    ("sesi4", "SESI 4 · TENSOR & OPTIMIZER", "notebooks/bulan1_sesi34_mnist.py", (334, 10_000)),
)

KEY = re.compile(
    r"backward\(|_backward|\.grad|Value\(|Tensor\(|relu\(|entropi|softmax|"
    r"@|p\.data\s*-=|RecursionError|momentum|rmsprop|adam|akurasi|"
    r"beda_hingga|lstsq|eigvalsh|permutation|argmax"
)


def base_duration(text: str) -> int:
    s = text.strip()
    if s.startswith("#"):
        return 7
    if s.startswith(('"""', "'''")) or s.endswith(('"""', "'''")):
        return 8
    if s.startswith(("class ", "def ", "if __name__")):
        return 24
    if s.startswith(("for ", "while ", "if ", "elif ", "else:", "try:", "except ", "finally:")):
        return 16
    if KEY.search(s):
        return 34
    if s.startswith(("import ", "from ", "print(")):
        return 8
    if s in {"(", ")", "[", "]", "{", "}"}:
        return 5
    return 12


def duration_frames(text: str) -> int:
    """Baris panjang mendapat waktu untuk digeser sampai ujung kanan."""
    base = base_duration(text)
    length = len(text.rstrip())
    if length <= 75:
        return base
    return max(base, min(48, 18 + (length - 75) // 3))


def visual_for(chapter: str, line: int, scope: str, text: str) -> str:
    t = f"{scope} {text}".lower()
    if chapter == "sesi1":
        if "beda_hingga" in t or "finite" in t:
            return "finite"
        if "torch" in t:
            return "gpu"
        if "latih" in t or "rugi" in t:
            return "training"
        return "graph"
    if chapter == "sesi2":
        if "mati" in t:
            return "dead"
        if "cincin" in t or "batas" in t:
            return "decision"
        if "relu" in t:
            return "relu"
        if "latih" in t or "rugi" in t:
            return "training"
        return "network"
    if chapter == "sesi34":
        if line <= 172:
            return "softmax"
        if line <= 231:
            return "wall"
        return "stack"
    if line <= 474:
        return "matrix"
    if line <= 529:
        return "finite"
    if line <= 644:
        return "mnist" if "latih" not in t else "training"
    if line <= 713:
        return "gpu"
    return "optimizer"


def caption_for(text: str, scope: str) -> str:
    s = text.strip()
    if s.startswith("#"):
        return s.lstrip("# -═").strip() or "Pemisah bagian kode."
    clean = s.strip('"\' ')
    if clean and s.startswith(('"""', "'''")):
        return clean.strip('"\' ')
    if s.startswith("from ") or s.startswith("import "):
        return "Muat alat yang dibutuhkan baris-baris berikutnya."
    if s.startswith("class "):
        return f"Bangun cetak biru {s.split()[1].split('(')[0].rstrip(':')}."
    if s.startswith("def "):
        return f"Definisikan fungsi {s[4:].split('(')[0]}."
    if s.startswith("return "):
        return "Kembalikan hasil ke pemanggil fungsi."
    if s.startswith("for "):
        return "Ulangi proses untuk setiap elemen."
    if s.startswith("while "):
        return "Ulangi selama syarat masih benar."
    if s.startswith(("if ", "elif ", "else:")):
        return "Pilih jalur eksekusi berdasarkan kondisi."
    if s.startswith(("try:", "except ", "finally:")):
        return "Jaga alur saat operasi berhasil maupun gagal."
    if "self.data" in s:
        return "Simpan nilai yang bergerak maju melalui graf."
    if "self.grad" in s or ".grad" in s:
        return "Simpan atau alirkan gradien menuju sumber operasi."
    if "_backward" in s:
        return "Pasang aturan turunan lokal untuk operasi ini."
    if ".backward()" in s:
        return "Mulai aliran gradien dari loss menuju parameter."
    if "p.data -=" in s:
        return "Geser parameter melawan arah gradien."
    if "relu" in s.lower():
        return "ReLU meneruskan nilai positif dan memotong nilai negatif."
    if "softmax" in s.lower() or "eksponen" in s or "peluang" in s:
        return "Ubah skor mentah menjadi peluang yang berjumlah satu."
    if "entropi" in s.lower() or "rugi" in s.lower() or "loss" in s.lower():
        return "Hitung seberapa jauh tebakan dari jawaban."
    if " @ " in s or "matmul" in s.lower():
        return "Kalikan matriks; bentuk array menentukan jalur data."
    if "time.perf_counter" in s:
        return "Mulai atau hentikan pengukuran waktu nyata."
    if "print(" in s:
        return "Tampilkan bukti hasil pengukuran."
    if "random.seed" in s or "default_rng" in s:
        return "Kunci sumber acak agar eksperimen bisa diulang."
    if "np.zeros" in s:
        return "Buat penampung nol dengan bentuk yang dibutuhkan."
    if "parameters" in s:
        return "Kumpulkan semua angka yang dapat dipelajari."
    if s:
        return f"Jalankan baris ini di {scope or 'program utama'}."
    return "Lanjut ke baris berikutnya."


def scope_map(lines: list[str]) -> list[str]:
    scopes: list[tuple[int, str]] = []
    result: list[str] = []
    for line in lines:
        stripped = line.lstrip()
        indent = len(line) - len(stripped)
        if stripped:
            while scopes and indent <= scopes[-1][0]:
                scopes.pop()
        name = scopes[-1][1] if scopes else "program utama"
        result.append(name)
        match = re.match(r"(?:async\s+)?def\s+([\w_]+)|class\s+([\w_]+)", stripped)
        if match:
            found = match.group(1) or match.group(2)
            scopes.append((indent, found))
    return result


def main() -> None:
    chapters = []
    segments = []
    cursor = 0
    seen_file_lines: set[tuple[str, int, str]] = set()

    for chapter_id, title, rel, bounds in SOURCES:
        path = ROOT / rel
        lines = path.read_text(encoding="utf-8").splitlines()
        scopes = scope_map(lines)
        start = cursor
        chapter_segments = []

        for i, raw in enumerate(lines, start=1):
            if bounds and not (bounds[0] <= i <= bounds[1]):
                continue
            if not raw.strip():
                continue
            dedupe = (rel, i, chapter_id)
            if dedupe in seen_file_lines:
                continue
            seen_file_lines.add(dedupe)
            duration = duration_frames(raw)
            lo = max(1, i - 4)
            hi = min(len(lines), lo + 8)
            lo = max(1, hi - 8)
            window = [{"no": n, "text": lines[n - 1]} for n in range(lo, hi + 1)]
            scope = scopes[i - 1]
            segment = {
                "start": cursor,
                "duration": duration,
                "chapter": chapter_id,
                "file": Path(rel).name,
                "line": i,
                "totalLines": len(lines),
                "window": window,
                "caption": caption_for(raw, scope),
                "scope": scope,
                "visual": visual_for(chapter_id, i, scope, raw),
            }
            segments.append(segment)
            chapter_segments.append(len(segments) - 1)
            cursor += duration

        chapters.append({
            "id": chapter_id,
            "title": title,
            "file": Path(rel).name,
            "start": start,
            "duration": cursor - start,
            "manim": f"manim/{chapter_id}.mp4",
            "manimFrames": MANIM_FRAMES[chapter_id],
            "segments": chapter_segments,
        })

    payload = {
        "fps": FPS,
        "width": 720,
        "height": 1280,
        "totalFrames": cursor + FPS * 3,
        "chapters": chapters,
        "segments": segments,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{len(segments)} baris, {payload['totalFrames'] / FPS:.1f} detik -> {OUT}")


if __name__ == "__main__":
    main()
