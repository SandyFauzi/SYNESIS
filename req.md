# Catatan Diskusi Antigravity: Strategi LLM Lokal & Knowledge Distillation
**Tanggal:** 22 Agustus 2026

## 1. Pilihan 3 Model Lokal Tersakti (untuk GTX 1650 Ti - 4GB VRAM)
Berdasarkan sisa VRAM (~3.1 GB), model terbaik yang bisa berjalan secara utuh dan maksimal di GPU adalah model berukuran 2B - 4B parameter.
- **Gemma-2-2B (Google Deepmind):** Super efisien dan sangat cerdas untuk ukuran sekecil ini. Cocok untuk obrolan santai dan general.
- **Phi-3 Mini 3.8B (Microsoft):** Unggul mutlak di bidang penalaran logis, matematika, dan *coding*.
- **Qwen2.5-3B (Alibaba):** Keseimbangan sempurna, stabil, dan sangat andal saat dipanggil lewat *script* Python.

*Catatan:* Ketiganya **100% Gratis (Open Weights)** dan hanya membutuhkan penyimpanan disk sekitar ~6 GB total.

## 2. Strategi Multi-Agent / Mixture of Experts (MoE)
Di Bulan 6, SYNESIS tidak harus bergantung pada satu model saja.
- **Eksekusi Bergantian:** Ollama memuat model ke GPU sesuai spesialisasi tugas (misal: panggil Phi-3 untuk matematika, lalu ganti Gemma untuk teks).
- **Eksekusi Bersamaan:** Jika dipaksa menyala bareng, 1 model akan masuk ke VRAM (ngebut), sedangkan 2 lainnya akan tumpah ke RAM CPU 15.4 GB (lebih lambat, tapi tetap aman tanpa *crash*).

## 3. Knowledge Distillation (Memerah Otak Claude)
Ide jenius dari pemilik: Mumpung langganan Claude masih aktif, kita akan mengekstrak pengetahuannya untuk tugas kreatif berat (seperti 3D Modeling di Blender atau Video Editing).
- **Aksi:** Perintahkan Claude untuk membuat **Dokumen Tutorial, SOP Terstruktur, atau Template Python API (`bpy`)** secara mendetail.
- **Penyimpanan:** Simpan hasil tersebut di folder *Knowledge Base* lokal (misal: `knowledge/blender_skills.md`).
- **Implementasi SYNESIS (RAG):** Di masa depan, saat SYNESIS disuruh nge-desain 3D, dia tidak akan ngoding dari memori (yang berisiko halusinasi). SYNESIS akan mencari contekan dari Claude tersebut, membacanya, dan meracik kodenya berdasarkan SOP akurat tersebut.

## 4. Ekspansi Integrasi dengan MCP (Model Context Protocol)
Untuk meningkatkan kapabilitas SYNESIS di Bulan 6, kita akan mengimplementasikan arsitektur MCP menggunakan standar JSON-RPC dari Anthropic. 
- **SYNESIS sebagai MCP Client:** Memungkinkan SYNESIS untuk menggunakan ratusan *tools* buatan komunitas secara instan (contoh: koneksi MCP Figma, GitHub, Google Drive, Database) tanpa harus koding integrasi eksternalnya satu-satu.
- **SYNESIS sebagai MCP Server:** Mengekspos *script/skill* Python buatanmu (misalnya pembaca sensor atau *scanner* PDF akademik) agar bisa digunakan oleh agen AI luar seperti Claude Desktop.
- **Dampak Utama:** Mengubah SYNESIS dari sekadar asisten terisolasi menjadi *Agent* fleksibel berstandar industri (*plug-and-play tools*).

## 5. Voice Cloning & TTS (Bulan 3)
SYNESIS akan dilengkapi dengan kemampuan berbicara (*Text-to-Speech*) menggunakan suara kustom secara 100% *offline* dan gratis untuk kebutuhan pribadi.
- **Teknologi Pilihan:** RVC (Retrieval-based Voice Conversion) atau XTTSv2 (Zero-Shot Voice Cloning).
- **Suara Target:** Menggunakan *open weights model* dari komunitas Hugging Face untuk meniru suara Seiyuu **Saori Hayami**, secara spesifik dengan *tone* dingin dan elegan ala karakter **Yukino Yukinoshita** (*Oregairu*).
- **Alur Eksekusi:** LLM lokal merumuskan teks balasan $\rightarrow$ dilempar ke *engine* TTS $\rightarrow$ difilter oleh model RVC Saori Hayami $\rightarrow$ diucapkan melalui *speaker* laptop.

## 6. Visi Akhir: Arsitektur "OpenJarvis" & DeepSeek Harness
Tujuan akhir (End Goal) dari seluruh proyek ini adalah merakit agen yang otonom sepenuhnya di OS lokal, berkiblat pada struktur seperti repositori **OpenJarvis**.
- **Integrasi Penuh:** Mesin LLM lokal, sistem memori (RAG), *voice interface* (Yukino), dan infrastruktur MCP tidak berdiri sendiri-sendiri, melainkan disatukan di bawah satu *framework agentic* (seperti mengadaptasi DeepSeek Harness atau menulis *agent loop* kustom).
- **Aksi Nyata:** SYNESIS pada akhirnya harus bisa menerima satu prompt lisan/teks kompleks (misal: "Analisis folder ini, jalankan *script*-nya, lalu perbaiki kalau ada error") dan mengerjakannya secara mandiri (otomasi PC sejati).
