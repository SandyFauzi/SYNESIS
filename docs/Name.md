# SYNESIS & SEREN — Identitas Sistem

---

## SYNESIS — ekosistemnya

> **S**eeking **Y**et **N**ever-**E**nding Exploration of **S**cience & **I**ntelligence **S**ystem

SYNESIS adalah keseluruhan ekosistem: arsitektur, infrastruktur, perkakas, agen, sistem pengetahuan, dan jaringan intelijen yang melingkupi SEREN.

### Asal kata — dan kenapa ini pilihan yang kuat

**σύνεσις** *(synesis)* adalah kata Yunani Kuno yang benar-benar ada, artinya **"pemahaman"**, "daya tangkap", "kearifan menilai".

Etimologinya: dari **συνίημι** *(syniemi)* — **σύν** *(syn,* "bersama"*)* + **ἵημι** *(hiemi,* "menaruh, mengirim"*)*. Secara harfiah: **"menaruh bersama-sama"** — menyatukan hal-hal terpisah sampai menjadi mengerti.

Aristoteles membahasnya di *Nicomachean Ethics* Buku VI sebagai salah satu **keutamaan intelektual**. Di sana *synesis* adalah kemampuan **menilai dengan baik** — dibedakan dari *phronesis* (kebijaksanaan praktis yang memerintahkan) dan *sophia* (kebijaksanaan teoretis). Kata Aristoteles: *phronesis* memerintah, *synesis* menilai.

Tiga alasan nama ini pas secara luar biasa untuk proyekmu:

1. **Artinya persis tesis proyekmu.** Seluruh Roadmap v3 dibangun di atas satu prinsip: *bangun dari nol untuk **paham**, pakai pretrained untuk jalan*. Kamu menamai sistemmu dengan kata Yunani yang artinya "pemahaman". Itu bukan kebetulan yang buruk.

2. **"Menaruh bersama-sama" menggambarkan dua hal sekaligus.** Secara teknis: sistemmu menyatukan suara, penglihatan, berkas, dan penalaran. Secara intelektual: proyekmu menyatukan fisika dan machine learning — dan §11 Roadmap menunjukkan keduanya memang formalisme yang sama.

3. **Cocok dengan identitasmu sebagai mahasiswa Fisika.** Fisika penuh istilah Yunani. Mahasiswa fisika yang menamai AI-nya dengan keutamaan epistemik Yunani itu koheren — dengan cara yang "Jarvis" (pinjaman dari Marvel) tidak pernah bisa.

*Catatan tambahan:* dalam linguistik, *synesis* juga nama sebuah gejala tata bahasa — kesesuaian menurut **makna**, bukan bentuk formal. Kebetulan yang manis untuk sistem yang tugasnya menangkap maksud, bukan sekadar mencocokkan pola.

---

## SEREN — agennya

> **S**cientific **E**xploration & **R**easoning **E**ngine for **N**etworked **I**ntelligence

SEREN adalah AI personal dan pendamping digital di dalam sistem SYNESIS. Nama panggilannya: **Sera**.

**Asal kata:** *seren* dalam bahasa Wales berarti **"bintang"**. Padanan yang wajar untuk sesuatu yang memandu.

---

## Hubungan Keduanya

```text
SYNESIS  — ekosistem, arsitektur, infrastruktur
└── SEREN  — agen personal ("Sera")
    ├── Reasoning
    ├── Exploration
    ├── Knowledge
    ├── Computer Interaction
    ├── Tool Use
    └── Networked Intelligence
```

---

## Catatan Praktis

### 1. Definisikan "Networked" sekarang, sebelum jadi kontradiksi

Kendala mutlak proyek ini adalah **tanpa API sama sekali, sepenuhnya offline**. Tapi "Networked Intelligence" mudah dibaca sebagai "terhubung internet" — dan itu bertentangan dengan identitas yang sudah kamu tetapkan.

Solusinya cukup menyatakan maksudnya secara eksplisit:

> **"Networked"** merujuk pada **jaringan internal antar modul, agen, dan basis pengetahuan** di dalam SYNESIS — bukan konektivitas internet. SEREN berjalan sepenuhnya lokal.

Sekali ditulis, ambiguitasnya hilang selamanya.

### 2. Wake word — pertimbangan nyata untuk Bulan 3

Di Bulan 3 kamu akan **melatih wake word sendiri**. Pilihan nama berdampak langsung ke akurasinya:

| Kandidat | Suku kata | Penilaian |
|---|---|---|
| "Sera" | 2 | **Terlalu pendek** — rawan false trigger |
| "Hey Sera" | 3 | Bisa dipakai |
| "Hey Seren" | 3 | Lebih baik — konsonan akhir memperjelas batas kata |
| **"Hey Synesis"** | 4 | **Terbaik** — paling panjang dan paling khas |

Model wake word butuh 3–4 suku kata agar tidak sering salah picu. Satu catatan: *Synesis* kaya bunyi desis (s), yang sedikit lebih sulit dikenali di ruangan berisik dibanding bunyi letup. Uji keduanya di Bulan 3 dengan rekaman suaramu sendiri — keputusan ini sebaiknya diambil dari data, bukan selera.

Pengucapan Indonesia: **si-NE-sis** — luwes, tidak canggung di lidah.

### 3. Penamaan di kode

```text
synesis/          # paket utama
├── seren/        # agen: loop, memori, penalaran
├── senses/       # STT, TTS, wake word, wajah
├── tools/        # fs, metadata, log, sistem
└── safety/       # gate, audit, allowlist
```

⚠️ **Jangan biarkan pembagian dua tingkat ini menyetir struktur kode dulu.** Sampai Bulan 5 kamu belum punya alasan nyata untuk memisahkan "ekosistem" dari "agen" — pemisahan itu baru bermakna ketika benar-benar ada beberapa agen. Satu repo, satu paket, sampai pemisahannya dituntut oleh kode, bukan oleh diagram.

### 4. Penerapan nama — selesai

- [x] `Roadmap.md` — seluruh "Jarvis" → "SYNESIS" (termasuk `SYNESIS v0.1` … `v1.0`)
- [x] `Bulan-0-Harian.md` — sama, dan nama paket `jarvis/` → `synesis/`
- [x] Wake word Bulan 3 → *"Hey Synesis"*
- [x] Nama folder → `SYNESIS`

---

## Keputusan Final

**Ditetapkan 14 Agustus 2026.** Nama dan kepanjangannya dikunci sebagaimana ditulis pemiliknya:

| | Nama | Kepanjangan |
|---|---|---|
| Ekosistem | **SYNESIS** | Seeking Yet Never-Ending Exploration of Science & Intelligence System |
| Agen | **SEREN** | Scientific Exploration & Reasoning Engine for Networked Intelligence |
| Panggilan | **Sera** | — |

Tidak ada revisi lanjutan atas akronim. Etimologi Yunani di atas berfungsi sebagai **lapisan makna tambahan**, bukan pengganti kepanjangan — dipakai saat menjelaskan filosofi sistem, sementara kepanjangan resmi dipakai sebagai identitas formal.
