# SYNESIS

Asisten AI personal yang dibangun dari nol. Mahasiswa Fisika belajar machine
learning dengan menulis sendiri tiap lapisan sebelum memakai pustaka yang
menyembunyikannya.

| | Nama | Kepanjangan |
|---|---|---|
| Ekosistem | **SYNESIS** | Seeking Yet Never-Ending Exploration of Science & Intelligence System |
| Agen | **SEREN** | Scientific Exploration & Reasoning Engine for Networked Intelligence |
| Panggilan | **Sera** | |

**Pemilik:** Sandy Fauzi Amrulloh, Fisika UNPAD, NPM 140310240054
**Mulai:** Agustus 2026

---

## Deskripsi Proyek

Dua target dengan jadwal berbeda.

**Enam bulan (Agt 2026 sampai Feb 2027): memahami fondasinya.** Berjalan
beriringan dengan Semester 5. Tiap bulan menghasilkan satu komponen yang benar
benar masuk ke sistem, jadi tidak ada latihan yang terbuang.

**Produk akhir: tanpa tenggat.** Dikerjakan sampai pemiliknya puas.

### Lima spesifikasi yang dituju

1. Akses penuh ke laptop
2. Membuka file dan membaca log
3. Membaca metadata berkas
4. Pengenalan wajah
5. Perintah suara

### Prinsip yang mengikat semuanya

> Bangun dari nol untuk **paham**. Pakai pretrained untuk **jalan**.

Backpropagation, konvolusi, dan attention ditulis tangan lebih dulu. PyTorch
menyusul setelah pemiliknya tahu apa yang dikerjakan di baliknya.

### Peta enam bulan

```text
Bulan 0  Agt   Gradient descent dari nol      intuisi optimasi
Bulan 1  Sep   Backprop & MLP dari nol        mesin autograd sendiri
Bulan 2  Okt   Embedding & classifier         INTENT CLASSIFIER   v0.1
Bulan 3  Nov   Konvolusi & sinyal             WAKE WORD + VOICE   v0.2
Bulan 4  Des   Metric learning & visi         FACE RECOGNITION    v0.3
Bulan 5  Jan   Attention & transformer        mini-GPT sendiri
Bulan 6  Feb   Integrasi + LLM lokal          SYNESIS v1.0
```

### Kendala mutlak

| Kendala | Isi |
|---|---|
| Biaya | Rp 0 selamanya |
| API | Tidak ada, sama sekali |
| Jaringan | Berjalan penuh tanpa internet |
| Drive C: | Tidak kebagian satu byte pun. Lihat kebijakan di bawah |

---

## Kebijakan Drive

### Alasannya

SSD C: dipakai sistem dan kuliah. Proyek ini memuat pustaka dan model besar,
gabungannya belasan giga. C: tidak kebagian satu byte pun.

Pembagiannya dua tempat:

| Drive | Isi | Ukuran |
|---|---|---|
| `S:\Code\Make A Jarvis` | Workspace: kode, notebook, dokumen, repo git | beberapa MB |
| `E:\SYNESIS` | Gudang: venv, cache model, dataset | belasan GB |

Repo tetap ringan dan gampang di-backup. Barang berat tinggal di `E:`, SSD dalam
enclosure berlabel Sandzh BackUp.

### Aturan

**1. Tidak ada paket Python proyek ini yang mendarat di C:.**
Semua masuk `E:\SYNESIS\.venv\`. Jangan pernah `pip install` di luar venv aktif.

**2. Tiap unduhan model mendarat di E:.**
Whisper, InsightFace, Piper, Qwen3. Tanpa pengecualian.

**3. Cache pip tinggal di E:.**
Ini yang paling sering luput. Wheel PyTorch 2,5 GB bisa tersimpan dua kali
tanpa terlihat.

**4. Periksa venv aktif sebelum memasang apa pun.**
Prompt harus menampilkan `(.venv)`. Kalau tidak, berhenti.

**5. venv itu barang sekali pakai.**
Dia menyimpan path absolut, jadi tidak portabel antar komputer. Yang portabel
adalah repo dan `requirements.txt`. Bangun ulang di mana pun.

### Variabel lingkungan

Empat pengalih ini menahan semua yang tadinya bocor ke C:.

| Variabel | Nilai | Menahan |
|---|---|---|
| `PIP_CACHE_DIR` | `E:\SYNESIS\.cache\pip` | Cache pip, 3 sampai 5 GB |
| `HF_HOME` | `E:\SYNESIS\.cache\huggingface` | Whisper dan model embedding, 1 sampai 3 GB |
| `TORCH_HOME` | `E:\SYNESIS\.cache\torch` | silero-vad dan torch.hub |
| `OLLAMA_MODELS` | `E:\SYNESIS\.cache\ollama` | Qwen3-4B, 2,5 GB |
| `TMP` | `E:\SYNESIS\.cache	mp` | Ruang kerja pip saat mengunduh |
| `TEMP` | `E:\SYNESIS\.cache	mp` | Sama, pip membaca keduanya |

> **`PIP_CACHE_DIR` saja tidak cukup.** pip mengunduh ke `%TEMP%` lebih dulu,
> lalu memindahkannya ke cache. Tanpa `TMP` dan `TEMP` diarahkan, wheel PyTorch
> 2,5 GB tetap transit di C:. Ini ketahuan di Hari 1 setelah 1,78 GB menumpuk
> di sana.

> **Jebakan yang sudah pernah kena.** Variabel lingkungan diwariskan saat proses
> dibuat. Menyetelnya secara permanen tidak mengubah terminal yang sudah terbuka,
> jadi `pip` di jendela lama tetap menulis cache ke C:. Tutup dan buka lagi
> terminalnya setelah menyetel, atau setel ulang di sesi berjalan:
>
> ```powershell
> $env:PIP_CACHE_DIR = "E:\SYNESIS\.cache\pip"
> ```
>
> Ini yang membuat 140 MB sempat mendarat di C: pada Hari 1.

InsightFace tidak memakai variabel lingkungan. Arahkan lewat parameter saat
inisialisasi:

```python
FaceAnalysis(name="buffalo_s", root=r"E:\SYNESIS\.cache\insightface")
```

### Letak berkas

```text
S:\Code\Make A Jarvis\        workspace, repo git
├── synesis\                  kode
├── notebooks\                eksplorasi
├── docs\                     dokumen
│   └── akademik\             KPA & KRS (di-gitignore)
├── activate.ps1              helper aktivasi venv
└── *.md                      README, Roadmap, Bulan-0, Name

E:\SYNESIS\                   gudang, tidak masuk git
├── .venv\                    paket Python, sekitar 5 GB
├── .cache\                   sekitar 8 GB
│   ├── pip│   ├── huggingface│   ├── torch│   ├── ollama│   └── insightface└── data\                     dataset, sekitar 3 GB
```

venv berada di luar repo, jadi aktifkan lewat helper:

```powershell
. .ctivate.ps1
```

Kalau enclosure `E:` tidak terpasang, venv tidak ada dan tidak ada yang jalan.
Helper itu akan bilang.

### Cara memastikan

```powershell
# venv aktif?
python -c "import sys; print(sys.prefix)"     # harus diawali E:\SYNESIS

# paket mendarat di mana?
python -c "import torch; print(torch.__file__)"

# pengalih terpasang?
Get-ChildItem Env: | Where-Object Name -match 'PIP_CACHE|HF_HOME|TORCH_HOME|OLLAMA'

# ada yang bocor ke C:?
Get-ChildItem "$env:LOCALAPPDATA\pip\Cache" -Recurse -EA 0 |
  Measure-Object Length -Sum
```

Jalankan pemeriksaan terakhir tiap akhir bulan. Kalau angkanya naik, ada yang
lolos.

### Satu pengecualian

Aplikasi Ollama, sekitar 1 GB, urusan Bulan 6. Installer Windows-nya memasang
ke `%LOCALAPPDATA%\Programs\Ollama` tanpa menawarkan lokasi lain. Model-modelnya,
bagian yang jauh lebih besar, tetap bisa diarahkan lewat `OLLAMA_MODELS`.

Kalau C: sempit saat itu, pindahkan foldernya lalu buat symlink.

### Yang harus memicu alarm

- Prompt tanpa `(.venv)` saat memasang paket
- `pip install` dijalankan dari PowerShell yang baru dibuka
- Pustaka baru yang mengunduh model tanpa parameter path
- Folder `.cache` muncul di `C:\Users\SANDY FAUZI\`

---

## Dokumen

| Berkas | Isi |
|---|---|
| `Roadmap.md` | Rencana enam bulan, arsitektur, jembatan fisika ke ML |
| `Bulan-0-Harian.md` | Diagnosa lingkungan dan rencana harian 13 sampai 31 Agustus |
| `Name.md` | Identitas, etimologi, konvensi penamaan |
| `README.md` | Berkas ini |

---

## Perangkat

```text
CPU    AMD Ryzen 5 4600H, 6 core 12 thread
RAM    15,4 GB
GPU    NVIDIA GTX 1650 Ti, 4 GB VRAM, compute capability 7.5
        sekitar 979 MB terpakai saat idle, sisa efektif 3,1 GB
Python 3.12.5
```

Tutup Wallpaper Engine dan launcher game sebelum sesi training di Bulan 5 dan 6.
Keduanya membebaskan 500 sampai 700 MB VRAM.
