# Handoff

## Goal
Menyelesaikan migrasi dan optimalisasi model LLM lokal di Bulan 6 SYNESIS dengan mengunduh, memverifikasi, dan melakukan benchmark komparatif terhadap trio model generasi terbaru (`qwen3.5:4b`, `phi4-mini-reasoning`, `gemma4:e2b-it-qat`), mengatasi bottleneck mode thinking pada jalur produksi, serta menghapus model lama (`gemma2:2b` dan `phi3:mini`) guna menghemat ruang disk di enclosure `E:\SYNESIS`.

## Decisions and rationale
1. **Pilihan Model Pengganti**:
   - `qwen3.5:4b` (4.7B Q4_K_M) dipilih sebagai model utama karena mendukung Vision, Tools (function calling), dan penalaran terstruktur dengan kecepatan stabil 12,07 token/s (52% CPU / 48% GPU).
   - `phi4-mini-reasoning` (3.8B Q4_K_M) dipilih sebagai model nalar murni untuk penalaran logika/matematika pada kecepatan ~18 token/s.
   - `gemma4:e2b-it-qat` (4.6B Q4_0) dipilih sebagai model cepat dengan kecepatan inferensi luar biasa 50,63 token/s dan dukungan multimodal bawaan.
2. **Pembersihan Model Lama**:
   - Menghapus `gemma2:2b` dan `phi3:mini` setelah ketiga model baru terbukti lulus uji fungsional nyata di jalur SYNESIS, membebaskan ~3,8 GB di Drive E:.
3. **Penonaktifan Thinking pada Jalur Cepat/Utama**:
   - Qwen 3.5 secara bawaan mengaktifkan *thinking* yang tidak ditampilkan oleh UI SYNESIS, menyebabkan latensi semu 97,4 detik pada cold start.
   - Mengubah parameter `think: false` untuk model utama dan model cepat, menyisakan `think: true` hanya untuk `phi4-mini-reasoning`. Latensi giliran pertama terpangkas menjadi 39–43 detik (cold), dan giliran kedua menjadi hanya 3,1 detik (warm).

## Current state
- Seluruh model baru (`qwen3.5:4b`, `phi4-mini-reasoning`, `gemma4:e2b-it-qat`) terdaftar resmi di Ollama dan terverifikasi di `E:\SYNESIS\.cache\ollama`.
- `synesis.agen` berhasil mengeksekusi pipeline end-to-end melalui intent `jelaskan_konsep` dan integrasi RAG lokal `knowledge/`.
- Uji warm turn percakapan normal selesai dalam 3,1 detik pada spesifikasi laptop Ryzen 5 4600H + GTX 1650 Ti 4GB VRAM.
- Model lama `gemma2:2b` dan `phi3:mini` telah dibersihkan dari sistem.

## Important files and commands
- `synesis/agen.py`: Gelung orkestrasi agen Bulan 6.
- `synesis/konfig.py`: Konfigurasi model default (`MODEL_UTAMA`, `MODEL_CEPAT`, `MODEL_NALAR`).
- `E:\SYNESIS\.cache\ollama`: Direktori penyimpanan bobot model Ollama.
- Uji jalur produksi agen:
  ```powershell
  & 'E:\SYNESIS\.venv\Scripts\python.exe' -c "from synesis.agen import Agen; a=Agen(model_llm='qwen3.5:4b'); h=a.balas('Jelaskan dengan singkat apa fungsi VRAM pada komputer.', kering=True, audit=False); print(h)"
  ```
- Cek status model lokal:
  ```powershell
  ollama list
  ```

## Open items and risks
- Pengujian interaktif suara (TTS/STT) secara live dengan model Qwen 3.5 belum dicoba di antarmuka jendela utama (`synesis.jendela`).
- Menjaga VRAM tetap steril sebelum menjalankan model dengan memastikan tidak ada beban grafis berat di latar belakang.
- Penyesuaian batas token output jika model penalaran (`phi4-mini-reasoning`) digunakan untuk soal multi-langkah agar tidak terpotong.

## Suggested next prompt
"Uji SYNESIS live lewat antarmuka terminal `python -m synesis --teks` atau jendela `python -m synesis` untuk mencoba interaksi percakapan dengan Qwen 3.5 dan tool calling."
