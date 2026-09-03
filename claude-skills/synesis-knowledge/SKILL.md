---
name: synesis-knowledge
description: "Search, retrieve, and apply curated code snippets, solutions, and design patterns from the SYNESIS Knowledge Base at 'S:\\Code\\Make A Jarvis\\synesis-knowledge'. Use when the user asks to query knowledge, find code examples, or solve problems in Blender 3D, Manim, FFmpeg, Remotion video, Figma design, frontend web, document conversion, or scientific physics computing."
---

# SYNESIS Knowledge Base Assistant

Query and retrieve vetted code chunks and domain knowledge from the fixed knowledge base located at:
`S:\Code\Make A Jarvis\synesis-knowledge`

## Supported Knowledge Domains

| Domain | Scope & Topic |
|---|---|
| `coding_general` | Python, C++, standard library algorithms, debugging, automation |
| `design_figma` | Figma design system tokens, UI components, vector assets |
| `web_frontend` | React, Next.js, Tailwind CSS, TypeScript, modern frontend |
| `video_remotion` | Programmatic video generation with Remotion, React animations |
| `docs_convert` | PDF, Markdown, DOCX processing, PyPDF, text normalization |
| `fisika_sci` | Computational physics, math derivations, signal processing, FFT |
| `video_ffmpeg` | FFmpeg command pipelines, audio/video filters, stream extraction |
| `manim` | Mathematical and scientific 3Blue1Brown animations |
| `blender_3d` | Blender Python scripting (`bpy`), procedural materials, shader nodes |

---

## Workflow

### 1. Searching Knowledge

Run `query.py` located at `S:\Code\Make A Jarvis\synesis-knowledge\query.py`:

```powershell
python "S:\Code\Make A Jarvis\synesis-knowledge\query.py" --domain <domain> "<search query>"
```

*Example for FFmpeg:*
```powershell
python "S:\Code\Make A Jarvis\synesis-knowledge\query.py" --domain video_ffmpeg "gabung klip audio dan video"
```

*Example for Blender 3D:*
```powershell
python "S:\Code\Make A Jarvis\synesis-knowledge\query.py" --domain blender_3d "material emisi neon"
```

*Global search across all domains:*
```powershell
python "S:\Code\Make A Jarvis\synesis-knowledge\query.py" "<search query>"
```

### 2. Applying Retrieved Solutions
- Examine the retrieved `code`, `target`, and `intent` fields from `chunks.jsonl`.
- Adopt the exact patterns, APIs, and idioms proven in the retrieved chunks.
- Ensure all solutions remain aligned with Sandy's local-first and performance-oriented standards.

### 3. Re-indexing / Ingesting Knowledge
When new authored markdown guides are added to `S:\Code\Make A Jarvis\synesis-knowledge\blender\`:

```powershell
python "S:\Code\Make A Jarvis\synesis-knowledge\ingest_blender.py"
```

---

## Boundaries & Constraints
- The knowledge base path is **fixed** at `S:\Code\Make A Jarvis\synesis-knowledge`. Do not look for it in temporary paths.
- `chunks.jsonl` is the primary dataset; do not corrupt or delete it.

