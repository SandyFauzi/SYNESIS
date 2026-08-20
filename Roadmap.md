# Roadmap: Belajar AI dari Nol → SYNESIS

**Sandy Fauzi Amrulloh** — Fisika UNPAD, NPM 140310240054
Status: Draft v3 — 13 Agustus 2026

**Tujuan 6 bulan (Agt 2026 – Feb 2027):** memahami cara kerja AI dari dasar, berjalan beriringan dengan mata kuliah Semester 5.
**Tujuan akhir:** SYNESIS dengan 5 spesifikasi yang diminta — **tanpa tenggat**, dikerjakan sampai selesai.
**Kendala mutlak:** biaya **Rp 0** · **tanpa API sama sekali** · semua jalan di laptop sendiri.

---

## 1. Pembingkaian Ulang

Dua draft sebelumnya keliru sasaran. Keduanya memperlakukan ini sebagai proyek produk dengan tenggat 6 bulan, lalu memampatkan pembelajaran ke sela-selanya. Hasilnya rencana yang defisit 8 jam dan penuh kompromi.

Dengan tujuan yang benar, tekanannya hilang:

| | v1 & v2 | **v3 (ini)** |
|---|---|---|
| Sasaran 6 bulan | Produk jadi | **Paham fondasinya** |
| Produk akhir | Tenggat Februari | **Tanpa tenggat — sampai kamu puas** |
| Model | Pakai pretrained saja | **Tulis sendiri dulu, baru pakai pretrained** |
| Otak | API / LLM lokal | **Tidak butuh LLM sampai Bulan 6** |
| Anggaran waktu | Defisit 8 jam | **Longgar** — tiap bulan berhenti secara wajar |
| Bila satu bulan meleset | Produk gagal rilis | Belajarnya melambat, tidak ada yang gagal |

Perubahan terpenting: **kalau satu bulan meleset, tidak ada yang rusak.** Kamu hanya belajar lebih pelan. Untuk mahasiswa dengan 22 SKS, ini bukan kenyamanan — ini yang membuat proyeknya bertahan sampai akhir.

---

## 2. Dua Arti "Dari Nol" — dan Keduanya Bisa Kamu Punya

Ini perlu diluruskan di depan, karena "bikin AI dari nol" bisa berarti dua hal, dan orang sering mencampurnya lalu menyerah.

**Arti A — dari nol untuk PAHAM.**
Kamu menulis sendiri algoritma intinya. Backpropagation kamu turunkan dan kode sendiri. Attention kamu bangun dari nol. Konvolusi kamu implementasikan manual. Tanpa PyTorch dulu, tanpa pustaka jadi. Tujuannya bukan menghasilkan model yang bagus — tujuannya **tidak ada lagi kotak hitam** buat kamu.

**Arti B — dari nol untuk SISTEM.**
Tidak ada API, tidak ada layanan luar, tidak ada tagihan. Semua berjalan di laptopmu, selamanya, milikmu sepenuhnya.

**Kamu bisa dapat keduanya.** Yang tidak bisa — dan tidak perlu — adalah menulis ulang Whisper atau ArcFace dari nol. Model-model itu butuh ribuan GPU-hour dan jutaan sampel. Tak seorang pun melakukannya sendirian, dan bukan begitu cara orang belajar.

Prinsip yang menyatukan keduanya:

> **Bangun dari nol untuk *paham*. Pakai pretrained untuk *jalan*.**
> Ini bukan kompromi — ini memang cara kerja setiap ML engineer.

Bedanya kamu dengan orang yang sekadar menempel pustaka: setelah 6 bulan ini, saat memanggil Whisper kamu tahu persis ada spektrogram dan transformer di dalamnya, karena **kamu sudah menulis keduanya sendiri**. Saat memanggil ArcFace, kamu tahu itu embedding di ruang vektor dengan cosine similarity — karena kamu sudah melatih embedding sendiri.

Soal "tanpa API": mengunduh model pretrained itu **unduhan sekali jalan**, bukan panggilan API. Setelah terunduh, laptopmu bisa dicabut dari internet selamanya dan SYNESIS tetap hidup. Kendala Rp 0 dan tanpa-API tetap utuh.

---

## 3. Prinsip Perancangan: Tidak Ada Latihan yang Terbuang

Tiap bulan menghasilkan **komponen yang benar-benar masuk ke SYNESIS**. Tidak ada tugas latihan yang berakhir di folder sampah.

```text
Bulan 0 : Gradient descent dari nol   → intuisi optimasi
Bulan 1 : Backprop & MLP dari nol     → mesin autograd buatanmu
Bulan 2 : Embedding & classifier      → ✅ INTENT CLASSIFIER  (SYNESIS v0.1)
Bulan 3 : Konvolusi & sinyal          → ✅ WAKE WORD + VOICE  (SYNESIS v0.2)
Bulan 4 : Metric learning & visi      → ✅ FACE RECOGNITION   (SYNESIS v0.3)
Bulan 5 : Attention & transformer     → mini-GPT buatanmu sendiri
Bulan 6 : Integrasi + LLM lokal       → ✅ SYNESIS v1.0
```

Belajar dan membangun bukan dua kegiatan yang berebut waktu. Keduanya kegiatan yang sama.

---

## 4. Wawasan Kunci: SYNESIS Tidak Butuh LLM Sampai Bulan 6

Ini yang paling membebaskan dari seluruh rencana, dan yang paling sering tidak disadari orang.

Sebagian besar perintah harian ke asisten pribadi itu **sederhana dan bisa diklasifikasikan**:

- *"buka laporan praktikum minggu lalu"* → intent: `buka_file`
- *"berapa sisa disk"* → intent: `info_sistem`
- *"baca log error hari ini"* → intent: `baca_log`
- *"file apa yang berubah kemarin"* → intent: `cari_file`

Semua itu tidak butuh penalaran bahasa. Yang dibutuhkan hanyalah **klasifikasi intent + ekstraksi parameter** — dan itu persis masalah supervised learning klasik yang akan kamu kuasai di Bulan 2.

Konsekuensinya besar:

**SYNESIS v0.1 di Bulan 2 sudah benar-benar berguna, tanpa satu pun LLM.** Voice command di Bulan 3 juga tidak butuh LLM. Face recognition di Bulan 4 juga tidak.

LLM baru masuk di Bulan 6, dan **hanya untuk permintaan terbuka** yang tidak bisa diklasifikasikan — *"rangkum semua tugas yang deadline-nya minggu ini lalu buatkan jadwal"*. Itu porsi kecil dari pemakaian nyata.

Ini juga menyelesaikan kecemasan di draft v2 soal Qwen3-4B yang lemah: model itu tidak lagi memikul seluruh sistem. Dia hanya menangani sisa 10–20% yang sulit, sementara 80–90% ditangani classifier buatanmu yang **selalu benar dan instan**.

---

## 5. Peta Enam Bulan

Tiap bulan punya pola sama: satu konsep, sesuatu yang **kamu tulis sendiri dari nol**, satu komponen SYNESIS, dan sambungan ke mata kuliah yang sedang berjalan.

---

### Bulan 0 — Perkakas & Gradient Descent · 13–31 Agustus · ~24 jam

*Jendela emas: kuliah belum mulai.*

**Konsep:** optimasi. Belajar itu **mencari minimum**.

**Yang kamu tulis sendiri:**
- Regresi linear murni numpy — tanpa scikit-learn
- Gradient descent manual: hitung turunan sendiri, perbarui bobot sendiri
- Plot permukaan loss dalam 3D, animasikan penurunannya

**Perkakas:** struktur proyek Python, `venv`, git, type hints, numpy, matplotlib

**Jembatan fisika:** Loss adalah **energi potensial**. Gradient descent adalah bola menggelinding ke lembah. Learning rate adalah ukuran langkah — terlalu besar, melampaui minimum; terlalu kecil, tak sampai-sampai. Kamu sudah punya intuisi ini dari Mekanika.

**Selesai bila:** kamu bisa memasang garis pada data berisik **tanpa memanggil satu pun pustaka ML**, dan bisa menjelaskan tiap baris kodenya.

> **Gerbang kelayakan.** Kalau bulan ini terasa mustahil, itu sinyal untuk memperkuat Python dulu sebelum lanjut. Jauh lebih baik ketahuan sekarang.

---

### Bulan 1 — Backpropagation & Jaringan Saraf dari Nol · September · ~32 jam

**Konsep:** aturan rantai pada graf komputasi. Inilah seluruh isi deep learning.

**Yang kamu tulis sendiri:**
- **Mesin autograd** bergaya micrograd — ~150 baris, kamu tulis sendiri dari kosong. Kelas `Value` yang melacak operasi dan menurunkan gradien otomatis
- MLP dari nol memakai mesin buatanmu itu
- Latih untuk klasifikasi MNIST
- **Lalu** tulis ulang dengan PyTorch, dan lihat hasilnya identik

Momen terakhir itu penting: kamu akan sadar PyTorch **tidak melakukan sihir apa pun** — dia hanya versi cepat dari yang barusan kamu tulis sendiri.

**Jembatan fisika:** Backpropagation **adalah** aturan rantai yang kamu pakai di Fisika Matematika I–III, diterapkan mundur menembus graf. Tidak ada yang baru secara matematis. Yang baru hanya nama dan cara mengorganisasinya.

**Sambungan matkul:** Machine Learning mulai berjalan — teori dari kelas, implementasi dari sini.

**Selesai bila:** MLP buatanmu sendiri mencapai akurasi >95% di MNIST, dan kamu bisa menjelaskan aliran gradien pada tiap lapisan.

---

### Bulan 2 — Embedding, Classifier & SYNESIS Pertama · Oktober · ~20 jam

*Bulan UTS — sengaja ringan.*

**Konsep:** representasi. Cara mengubah makna jadi vektor.

**Yang kamu tulis sendiri:**
- Klasifikasi teks dari nol: bag-of-words → regresi logistik, semuanya manual
- Cross-entropy loss diturunkan dan dikode sendiri
- Baru kemudian pakai embedding pretrained, dan bandingkan selisih akurasinya

**✅ Komponen SYNESIS — Intent Classifier:**
- Tulis sendiri **300–500 contoh perintah** yang memang kamu pakai sehari-hari, beri label intent
- Latih classifier · evaluasi dengan confusion matrix · pasang ke sistem
- Ekstraksi parameter (nama file, rentang waktu) dari perintah

**Ini menghasilkan SYNESIS v0.1: perintah teks → intent → eksekusi tool. Nol LLM, sudah berguna.**

Ditambah toolset filesystem dasar (baca, cari, buka file) dan **safety gate** — klasifikasi operasi `READ`/`WRITE`/`DESTRUCTIVE`, path allowlist, konfirmasi untuk yang merusak, audit log. Mulai dari sini, bukan ditambal belakangan.

**Jembatan fisika:** Embedding adalah vektor di ruang berdimensi tinggi; kemiripan adalah **hasil kali dalam**. Ini operasi `⟨ψ|φ⟩` yang sama persis dari Fisika Kuantum. Softmax adalah **distribusi Boltzmann** — parameter "temperature" memang dinamai dari suhu termodinamika. Cross-entropy adalah **entropi** dari Termodinamika dan Fisika Statistik.

**Sambungan matkul:** Ini kandidat terkuat untuk **tugas besar Machine Learning** — siklus supervised learning yang utuh: kumpulkan data, beri label, latih, evaluasi, deploy ke sistem nyata.

**Selesai bila:** kamu mengetik *"bukain laporan praktikum minggu lalu"* dan file-nya terbuka — lewat classifier yang kamu latih sendiri.

---

### Bulan 3 — Konvolusi, Sinyal & Suara · November · ~34 jam

**Konsep:** konvolusi dan representasi waktu-frekuensi.

**Yang kamu tulis sendiri:**
- Konvolusi 1D dan 2D manual, tanpa pustaka
- Spektrogram dari nol: framing → windowing → FFT
- MFCC dari nol
- CNN kecil dari nol, lalu versi PyTorch-nya
- **Latih keyword spotter sendiri** pada dataset Google Speech Commands (35 kata, model kecil, ~30 menit di GPU-mu)

**✅ Komponen SYNESIS — Voice:**
- **Wake word buatanmu sendiri**, dilatih dengan suaramu
- VAD (`silero-vad`), lalu Whisper untuk transkripsi umum — **sekarang kamu tahu persis apa isinya**
- Piper TTS untuk balasan suara
- Semua di CPU; GPU disimpan untuk Bulan 6

**Ini menghasilkan SYNESIS v0.2: perintah suara.**

**Jembatan fisika:** Ini **praktikum DSP**. Transformasi Fourier, windowing, teorema konvolusi, aliasing — semuanya dari Gelombang dan DSP. Lapisan konvolusi pada CNN persis konvolusi yang kamu pelajari di Fisika Matematika III.

**Sambungan matkul:** Kandidat terkuat untuk **tugas DSP untuk Sensor dan Imaging**.

**Selesai bila:** kamu memanggil *"Hey Synesis"* dengan wake word buatanmu sendiri, dan dia menjawab.

---

### Bulan 4 — Metric Learning & Pengenalan Wajah · Desember · ~20 jam

*Bulan UAS — ringan, sebagian bisa didorong ke liburan.*

**Konsep:** metric learning. Melatih model agar jarak antar vektor **berarti** sesuatu.

**Yang kamu tulis sendiri:**
- Siamese network kecil dari nol dengan contrastive loss
- Latih di dataset wajah kecil, amati embedding-nya memisah
- Pahami mengapa ArcFace bekerja: memaksa pemisahan **sudut** di permukaan hiperbola satuan

**✅ Komponen SYNESIS — Face Recognition:**
- InsightFace `buffalo_s` di CPU untuk akurasi produksi
- Enrollment: ambil N gambar → rata-ratakan embedding → simpan
- **Kalibrasi threshold: kurva ROC, FAR/FRR** — ini ML sungguhan
- Kegunaan: buka kunci sesi, sapaan personal, autentikasi operasi sensitif

**Ini menghasilkan SYNESIS v0.3: wajah + suara.**

**Jembatan fisika:** Embedding wajah adalah vektor ternormalisasi di permukaan bola satuan berdimensi 512. Pengenalan adalah **proyeksi** — sekali lagi `⟨ψ|φ⟩`. ArcFace bekerja dengan memaksimalkan pemisahan sudut, dan itu geometri, bukan sihir.

**Sambungan matkul:** Kurva ROC dan kalibrasi threshold adalah materi laporan **Machine Learning** yang kuat.

**Selesai bila:** SYNESIS mengenalimu dari webcam dalam <1 detik, dengan false accept rate mendekati nol pada wajah asing — dan kamu bisa menjelaskan kenapa threshold-nya di angka itu.

---

### Bulan 5 — Attention & Transformer dari Nol · Januari · ~28 jam

**Konsep:** attention. Arsitektur yang mendasari semua LLM modern.

**Yang kamu tulis sendiri:**
- Self-attention dari nol dengan numpy: query, key, value — turunkan sendiri
- Multi-head attention
- Positional encoding *(sinusoidal — kamu akan langsung mengenalinya)*
- **Transformer utuh dari nol**, bergaya nanoGPT
- **Latih mini-GPT-mu sendiri** pada teks pilihanmu — catatan kuliah, tulisanmu sendiri. Beberapa juta parameter, latih 30–60 menit di GTX 1650 Ti

Modelnya akan payah. Itu wajar dan bukan masalah — **poinnya kamu sudah membangun LLM dari nol dan melatihnya sendiri.** Setelah bulan ini, Qwen3-4B bukan lagi kotak hitam.

**Jembatan fisika:** Attention adalah hasil kali dalam berbobot — sekali lagi ruang Hilbert. Positional encoding memakai sinus dan kosinus berbagai frekuensi; itu **deret Fourier**, langsung dari Gelombang. Sampling temperature adalah distribusi Boltzmann. Training adalah menuruni permukaan energi, dengan noise SGD berperan seperti fluktuasi termal yang membantu lolos dari minimum lokal — *simulated annealing* memang istilah dari mekanika statistik, dan itu materi Fisika Statistik yang sedang kamu ambil.

**Sambungan matkul:** Fisika Statistik memberi kerangka teoretisnya; Robotika Cerdas memberi arsitektur agent untuk bulan berikutnya.

**Selesai bila:** mini-GPT buatanmu menghasilkan teks yang menyerupai data latihnya, dan kamu bisa menjelaskan tiap komponen transformer tanpa membuka catatan.

---

### Bulan 6 — Integrasi & LLM Lokal · Februari · ~24 jam

**Konsep:** arsitektur agent — siklus *sense → plan → act*.

**Yang kamu bangun:**
- Ollama + Qwen3-4B lokal, **hanya untuk permintaan terbuka** yang tidak tertangkap intent classifier
- Agent loop dengan tool calling; grammar GBNF untuk menjamin JSON valid
- Orkestrator: state machine `idle → listening → thinking → speaking`
- Ekstraktor metadata (PDF, EXIF, media, Office) dan pembaca log
- **Safety gate v2**: rate limiting, kill switch, pembatasan jangkauan filesystem
- Uji ketahanan: nyalakan seharian, catat semua yang rusak

**Ini menghasilkan SYNESIS v1.0.**

**Jembatan fisika:** Siklus agent adalah lingkar kendali dengan umpan balik — persis kerangka **Robotika Cerdas dan Otomasi Sistem Fisik**.

**Selesai bila:** perintah suara → dikenali → dieksekusi → dijawab dengan suara, sepenuhnya offline, menyala 8 jam tanpa crash.

---

## 5b. Kecepatan yang Direvisi

> **Direvisi 20 Agustus 2026**, setelah Hari 1 sampai 3 selesai dalam satu hari
> dengan seluruh jawaban benar, termasuk penurunan `w* = -B/2A` dan ramalan
> perilaku divergensi sebelum melihat datanya. Ditambah 5 tahun pengalaman C
> dan Python, kecepatan aslinya terlalu lambat.

Urutan bulannya tidak berubah. Yang berubah durasinya.

| Bulan | Semula | Jadi | Alasan |
|---|---|---|---|
| 0 · fondasi | 19 hari | **4 sesi** | keterampilan Python sudah menutupinya |
| 1 · backprop & autograd | 4 minggu | **2 minggu** | matematikanya sudah kamu kuasai |
| 2 · embedding & classifier | 4 minggu | **2 minggu** | mayoritas rekayasa, bukan konsep baru |
| 3 · konvolusi & suara | 4 minggu | **3 minggu** | **ditahan** — lihat catatan di bawah |
| 4 · metric learning & wajah | 4 minggu | **2 minggu** | mayoritas pemanggilan pustaka |
| 5 · attention & transformer | 4 minggu | **3–4 minggu** | **ditahan** — bagian tersulit |
| 6 · integrasi & LLM lokal | 4 minggu | **4 minggu** | **ditahan** — integrasi selalu molor |

Total kira-kira **4 bulan**, bukan 6. Dua bulan yang terbebas jatuh ke produk,
yang memang tanpa tenggat.

### Yang tidak dipadatkan, dan kenapa

Tiga bulan sengaja ditahan pada durasi aslinya. Bukan karena meragukan
kecepatanmu, tapi karena hambatannya bukan kecepatan belajar.

**Bulan 3, suara.** Di sinilah kenyataan menggigit. Latensi, kuirk perangkat
audio, ambang VAD yang meleset, wake word yang salah picu di ruangan berisik.
Semua itu perlu waktu berjam-jam yang tidak bisa dipercepat dengan membaca
lebih cepat. Ini debugging perangkat keras, bukan belajar konsep.

**Bulan 5, transformer.** Attention benar-benar sulit, bahkan bagi programmer
berpengalaman. Bug di sini tidak melempar error, ia menghasilkan model yang
melatih diri tanpa pernah membaik. Menemukannya butuh kesabaran, bukan
kecepatan.

**Bulan 6, integrasi.** Menyatukan enam modul yang masing-masing jalan sendiri
selalu memakan waktu lebih lama dari perkiraan siapa pun. Ini hukum, bukan
dugaan.

### Batas sebenarnya bukan kemampuanmu

Kamu punya sekitar 8 jam per minggu dengan beban 22 SKS. Belajar tiga kali
lebih cepat tidak menambah jam dalam seminggu.

Jadi akselerasi ini berarti **lebih sedikit sesi untuk cakupan yang sama**,
bukan lebih banyak jam. Kalender tetap yang memegang kendali.

### Satu risiko yang naik

Yang paling sering menjatuhkan pembelajar cepat adalah melompati bagian yang
terasa lambat padahal justru di situ intuisinya dibangun.

Dua hal berikut wajib dikerjakan utuh meski terasa remeh:

- **Sesi B Bulan 0**, animasi lintasan di permukaan loss
- **Sesi C Bulan 0**, melihat sendiri test loss naik saat train loss turun

Keduanya pengalaman, bukan tugas. Kamu sudah menjelaskan overfitting dengan
benar di Soal 3b secara konsep. Melihatnya terjadi di layarmu sendiri adalah
hal yang berbeda, dan itulah yang menempel.

---

## 6. Posisi Kamu di Akhir Februari

**Yang akan kamu pahami — bukan sekadar pakai:**

- [ ] Gradient descent, karena kamu menulisnya sendiri
- [ ] Backpropagation, karena kamu membangun mesin autograd sendiri
- [ ] Jaringan saraf, karena kamu melatihnya tanpa pustaka
- [ ] Embedding dan metric learning, karena kamu melatihnya sendiri
- [ ] CNN dan pemrosesan sinyal, karena kamu menulis konvolusi dan spektrogram sendiri
- [ ] Attention dan transformer, karena kamu membangun serta melatih LLM sendiri
- [ ] Arsitektur agent, karena kamu merangkainya sendiri

**Yang akan berjalan di laptopmu:**

- [ ] Perintah suara dengan wake word buatanmu sendiri
- [ ] Pengenalan wajah dengan threshold yang kamu kalibrasi sendiri
- [ ] Intent classifier yang kamu latih dari data buatanmu sendiri
- [ ] Operasi file, metadata, dan pembacaan log
- [ ] LLM lokal untuk permintaan terbuka
- [ ] Sepenuhnya offline · Rp 0 · tanpa API · tanpa ketergantungan pada siapa pun

**Empat dari lima spesifikasi awal sudah berfungsi** — akses file, metadata, face recognition, voice command. Spesifikasi pertama (akses penuh dengan penalaran setara Claude) baru dimulai, dan memang wajar begitu: bagian itu bergantung pada kualitas LLM, dan di situlah pekerjaan setelah 6 bulan berada.

**Dan yang paling penting:** kamu punya fondasi untuk membangun apa pun setelahnya, bukan hanya SYNESIS.

---

## 7. Setelah Enam Bulan — Tanpa Tenggat

Fondasinya sudah berdiri. Sisanya perluasan, dikerjakan sesuai kecepatanmu:

| Arah | Isi |
|---|---|
| **Otak lebih kuat** | Qwen3-8B dengan offload · fine-tune LoRA untuk gaya bicaramu · model baru saat rilis |
| **Indra lebih tajam** | Fine-tune Whisper untuk bahasa Indonesia · speaker ID (autentikasi suara) · deteksi emosi |
| **Jangkauan lebih luas** | Otomasi browser · kalender & email · kendali IoT — **bersambung ke Fisika Instrumentasi** |
| **Memori lebih baik** | Memori jangka panjang · RAG di atas berkasmu · pengetahuan personal |
| **Jalur akademik** | Skripsi · publikasi · portofolio magang/riset |

Perluasan paling alami buatmu: **hubungkan ke perangkat keras.** Kamu ambil Fisika Instrumentasi dan Robotika semester ini. SYNESIS yang bisa membaca sensor, mengendalikan alat lab, dan mencatat data eksperimen adalah pertemuan langsung antara fisika dan AI — dan itu wilayah yang sangat sedikit orang kuasai keduanya.

---

## 8. Tumpukan Teknologi — Semua Gratis, Semua Lokal

| Kebutuhan | Pilihan | Lisensi | Biaya |
|---|---|---|---|
| Numerik | numpy, matplotlib | BSD | Rp 0 |
| Deep learning | PyTorch (CUDA 11.8+) | BSD | Rp 0 |
| ML klasik | scikit-learn | BSD | Rp 0 |
| Audio | librosa, sounddevice, silero-vad | ISC/MIT | Rp 0 |
| STT | faster-whisper (`small`, int8) | MIT | Rp 0 |
| TTS | Piper | MIT | Rp 0 |
| Wake word | openWakeWord *(+ model buatanmu)* | Apache 2.0 | Rp 0 |
| Wajah | InsightFace `buffalo_s` | kode MIT · **model non-komersial** | Rp 0 |
| Visi | opencv-python | Apache 2.0 | Rp 0 |
| LLM lokal | Ollama + Qwen3-4B | MIT / Apache 2.0 | Rp 0 |
| Data | SQLite | Public domain | Rp 0 |
| Dataset latih | MNIST, Google Speech Commands | terbuka | Rp 0 |

**Total: Rp 0. Tanpa API. Tanpa akun. Tanpa langganan.** Yang kamu bayar hanya listrik dan waktu.

> ⚠️ Model pretrained InsightFace berlisensi **non-komersial** (kodenya MIT). Untuk proyek pribadi dan tugas kuliah sepenuhnya aman. Bila kelak ingin dikomersialkan, ganti ke `face_recognition` (dlib, Boost License).

---

## 9. Perangkat Keras & Anggaran Waktu

```text
CPU   : AMD Ryzen 5 4600H — 6 core / 12 thread
RAM   : 15.4 GB
GPU   : NVIDIA GeForce GTX 1650 Ti — 4 GB VRAM (CUDA-capable)
Python: 3.12.5   |   Git: 2.48.1
```

Semua yang kamu latih di enam bulan ini **muat dengan lega**:

| Yang dilatih | VRAM | Waktu latih |
|---|---|---|
| MLP di MNIST | <0.5 GB | menit |
| Intent classifier | <0.5 GB *(CPU pun bisa)* | **detik** |
| CNN keyword spotting | ~1 GB | ~30 menit |
| Siamese network wajah | ~1.5 GB | ~1 jam |
| Mini-GPT (beberapa juta parameter) | ~2 GB | 30–60 menit |

GTX 1650 Ti sepenuhnya memadai untuk **semua** materi pembelajaran ini. Batasan 4 GB baru terasa saat menjalankan LLM besar di Bulan 6 — dan Qwen3-4B terkuantisasi pun masih muat.

> ⚠️ **Terverifikasi 13 Agt 2026:** saat idle, **979 MB VRAM sudah terpakai** (Wallpaper Engine, Chrome, launcher game), menyisakan ~3.1 GB. Untuk Bulan 0–4 tidak berpengaruh; di Bulan 5–6 tutup aplikasi tersebut sebelum sesi. Rincian di [Bulan-0-Harian.md](Bulan-0-Harian.md).

**Anggaran waktu:** 6–10 jam/minggu, turun saat UTS dan UAS.

```text
26 minggu − 2 (UTS) − 3 (UAS) − 1 (buffer) ≈ 20 minggu efektif
20 minggu × 8 jam ≈ 160 jam tersedia
Kebutuhan rencana ini  ≈ 148 jam
───────────────────────────────────
Kelonggaran            ≈  12 jam
```

Berbeda dengan v2 yang defisit 8 jam, rencana ini **punya kelonggaran**. Dan karena tiap bulan berdiri sendiri, bulan yang meleset hanya menggeser jadwal — tidak menggagalkan apa pun.

---

## 10. Cara Belajar yang Menentukan Hasil

Empat aturan. Yang pertama paling penting, dan paling sering dilanggar.

**1. Tulis dulu, baru pakai pustaka.**
Setiap konsep dikerjakan dua kali: sekali dari nol, sekali dengan pustaka. Urutannya tidak boleh dibalik. Menulis MLP dari nol lalu melihat `nn.Linear` melakukan hal yang sama akan **menghapus rasa gaib**-nya untuk selamanya. Langsung memakai `nn.Linear` justru mengabadikan rasa itu.

**2. Selalu ada yang berjalan.**
Tiap bulan berakhir dengan sesuatu yang bisa dijalankan dan ditunjukkan. Bukan catatan, bukan tutorial yang setengah ditonton — program yang hidup.

**3. Belajar tepat pada waktunya.**
Jangan habiskan Agustus menonton kursus ML. Kamu akan lupa semuanya sebelum sempat dipakai. Pelajari tiap konsep pada bulan ia benar-benar dibutuhkan.

**4. Terjemahkan ke bahasa fisika.**
Setiap konsep ML baru, tanyakan: *ini padanan apa di fisika?* Hampir selalu ada. Itu bukan trik menghafal — memang formalisme yang sama, dan kamu punya keunggulan yang tidak dimiliki mayoritas orang yang belajar ML.

---

## 11. Fisika Kamu Adalah Matematika ML

Bukan analogi. Persamaan yang sama, nama yang berbeda.

| Yang sudah kamu kuasai | Namanya di ML | Dipakai di |
|---|---|---|
| Prinsip aksi minimum *(Mekanika, A−)* | Minimasi loss | Bulan 0 |
| Turun di permukaan energi potensial | Gradient descent | Bulan 0 |
| Aturan rantai *(Fismat I–III, A−/A/A)* | Backpropagation | Bulan 1 |
| Ruang Hilbert, `⟨ψ, φ⟩` *(Kuantum, A−)* | Embedding, cosine similarity | Bulan 2, 4, 5 |
| Nilai & vektor eigen | PCA, metode spektral | Bulan 2 |
| Distribusi Boltzmann `e^(−E/kT)` *(Fisstat)* | Softmax `e^(z/T)` — **identik** | Bulan 2, 5 |
| Fungsi partisi `Z` | Penyebut normalisasi softmax | Bulan 2 |
| Entropi *(Termodinamika, A−)* | Cross-entropy loss | Bulan 2 |
| Transformasi Fourier *(Gelombang, A−)* | Spektrogram, MFCC | Bulan 3 |
| Konvolusi *(Fismat III, A)* | Lapisan konvolusi CNN | Bulan 3 |
| Deret Fourier | Positional encoding | Bulan 5 |
| Simulated annealing *(Fisstat)* | Jadwal learning rate | Bulan 5 |
| Monte Carlo *(Komputasi & Simulasi, A)* | SGD, dropout | Bulan 1 |
| Iterasi relaksasi | Training loop | Bulan 0–1 |

**Empat mata kuliah semester ini memasok teori tepat waktu:**

| Mata Kuliah | SKS | Menopang |
|---|---|---|
| Machine Learning | 2 | Bulan 1–2, 4 — *ajukan intent classifier & kalibrasi ROC sebagai tugas besar* |
| DSP untuk Sensor & Imaging | 2 | Bulan 3 — *ajukan wake word sebagai tugas* |
| Fisika Statistik | 3 | Bulan 2 & 5 — Boltzmann, entropi, annealing |
| Robotika Cerdas & Otomasi | 2 | Bulan 6 — arsitektur agent |

**Aksi konkret, minggu pertama kuliah:** temui dosen Machine Learning dan DSP, ajukan modul-modul ini sebagai tugas besar. Kalau diterima, waktu kuliah dan waktu proyek melebur — dan kelonggaran 12 jam berubah jadi kelonggaran nyata.

Ajukan **sebelum** topik tugas ditetapkan.

---

## 12. Risiko

| Risiko | Dampak | Mitigasi |
|---|---|---|
| Terjebak *tutorial hell* | **Tinggi** | Aturan #1 dan #2 di §10 — selalu tulis dulu, selalu ada yang jalan |
| Perfeksionisme di Bulan 0–1 | Sedang | Definisi selesai tiap bulan. Cukup berjalan, tidak harus indah |
| Semester lebih berat dari perkiraan | Sedang | Bulan berdiri sendiri; geser jadwal, jangan potong pemahaman |
| Matematika terasa berat | **Rendah** | §11 — kamu sudah menguasai fondasinya |
| Mini-GPT mengecewakan | Rendah | Sudah diperkirakan. Tujuannya paham, bukan performa |
| Godaan melompat langsung ke LLM | Sedang | Bulan 5 sengaja ditaruh belakangan. Melompat berarti kembali ke kotak hitam |

Risiko terbesar bukan teknis. Ia adalah **melompati bagian "dari nol"** karena terasa lambat, lalu tanpa sadar kembali menjadi pengguna pustaka yang tidak paham isinya — persis yang ingin kamu hindari.

---

## 13. Langkah Berikutnya

Minggu ini, sebelum perkuliahan mulai:

1. Struktur repo + `venv` + `git init`
2. Pasang numpy, matplotlib, PyTorch — verifikasi CUDA mengenali GTX 1650 Ti
3. Regresi linear dari nol, gradient descent manual
4. Plot permukaan loss dan animasikan penurunannya
5. Susun pertanyaan untuk dosen ML dan DSP soal menjadikan modul sebagai tugas kuliah

Nomor 3 dan 4 adalah langkah pertama sungguhan. Semua yang datang setelahnya — backprop, CNN, attention — hanyalah gagasan yang sama dalam bentuk yang makin bertingkat.
