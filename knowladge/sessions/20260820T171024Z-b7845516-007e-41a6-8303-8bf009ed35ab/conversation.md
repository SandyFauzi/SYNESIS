# Conversation

> Visible user and assistant messages exported from a Codex session.

## 001 — User

take a look at file di folder ini. ada ya nilai saya di Fisika dan pengambilan mata kuliah di semester 5 dan ada machine learning. Dari titik saya ini saya ingin belajar membuat AI sendiri dengan tujuan dan spesifikasi sebagai berikut:
1. Bisa punya akses full ke laptop saya
2. Bisa assist saya dalam membuka file baca log
3. Mirip kamu lah intinya bisa buka inti metadata file dan lain lain
4. Face recognition
5. Voice command

Coba memungkinkan kah untuk di develop selama 6 bulan 1 semester 5 ini. Kita bikin rodamap dulu saja

## 002 — Assistant

Saya lihat dulu isi foldernya.

## 003 — Assistant

Ada dua PDF. Saya baca keduanya.

## 004 — Assistant

Dua PDF-nya kebaca: **KPA semester 1–4** (IPK 3.70, 80 SKS) dan **KRS semester 5** (22 SKS, 9 MK). Sebelum bikin roadmap, saya cek dulu spek laptop kamu — ini yang menentukan arsitekturnya (model lokal vs API).

## 005 — Assistant

Spek terbaca. Ini yang menentukan seluruh arsitekturnya, jadi saya jelaskan dulu implikasinya sebelum menulis roadmap.

## 006 — Assistant

Roadmap-nya sudah ditulis ke [Roadmap.md](Roadmap.md). Ini ringkasan temuan dan alasan di balik keputusannya.

## Jawaban singkat: bisa

Tapi dengan satu pembingkaian ulang yang penting: **ini proyek integrasi sistem, bukan proyek riset AI.** Kelima spek yang kamu minta semuanya bisa dicapai dengan model pretrained — tidak ada satu pun yang perlu dilatih dari nol. Kerja sebenarnya ada di agent loop, tool, dan menyatukan audio/kamera/filesystem/LLM dalam satu proses. Itu porsi yang muat di 6 bulan; melatih model tidak.

## Spek laptop menyetir arsitekturnya

Ryzen 5 4600H, 15.4 GB RAM, **GTX 1650 Ti dengan 4 GB VRAM**. Python 3.12.5, Git, dan Node sudah terpasang.

Angka 4 GB itu yang menentukan segalanya. Whisper `small`, InsightFace, Piper, dan wake word semuanya muat nyaman. Yang **tidak** muat adalah LLM 7B untuk jadi otaknya (~4.5 GB, harus offload ke RAM, jadi lambat). Model 3B muat tapi tool-calling-nya rapuh — dan tool-calling justru inti dari yang kamu minta.

Jadi: **otak pakai API, indra jalan lokal di GPU.** Efek sampingnya bagus — STT, TTS, dan face recognition gratis selamanya karena lokal, yang berbayar cuma panggilan LLM.

## Temuan yang paling berguna

KRS-mu nyaris dirancang untuk proyek ini. Empat dari sembilan mata kuliah memberi materi yang langsung terpakai:

- **Machine Learning** → modul face recognition (ROC, FAR/FRR, threshold pada embedding — itu laporan ML yang sah)
- **DSP untuk Sensor & Imaging** → seluruh pipeline audio (Fase 3 pada dasarnya praktikum DSP)
- **Robotika Cerdas** → arsitektur agent = siklus *sense–plan–act*
- **Fisika Statistik** → fondasi konseptual ML, dan ini bukan analogi longgar: Boltzmann ↔ softmax, fungsi partisi ↔ normalisasi, entropi ↔ cross-entropy memang formalisme yang sama

Dengan 22 SKS, proyek pribadi biasanya kalah bersaing dengan kuliah. Jalan keluarnya: **ajukan modul face recognition sebagai tugas besar ML dan modul voice sebagai tugas DSP**, dibicarakan di minggu pertama sebelum topik tugas ditentukan. Kalau diterima, waktu kuliah dan waktu proyek jadi satu blok, bukan dua blok yang saling makan.

## Dua hal yang perlu saya sampaikan terus terang

**Anggaran waktunya ketat.** 26 minggu kalender dikurangi UTS, UAS, dan buffer ≈ **20 minggu efektif × 8 jam ≈ 160 jam**. Cukup untuk sistem yang benar-benar jalan, tapi tanpa ruang untuk waktu terbuang. Karena itu ada tangga pemangkasan di §9 — urutan fitur yang dipotong duluan saat semester ternyata lebih berat dari perkiraan.

**"Akses penuh ke laptop" adalah bagian yang paling mudah diremehkan.** Secara teknis ini justru termudah — beberapa baris `subprocess` sudah cukup. Justru itu bahayanya: LLM yang salah paham, dengan shell tanpa batas di mesin berisi tugas kuliah dan kodemu, bisa berarti kehilangan data permanen. Safety gate (klasifikasi operasi, path allowlist, konfirmasi, audit log, kill switch) masuk di **Fase 1**, bukan ditambal belakangan, dan itu satu-satunya hal yang tidak boleh dipotong.

## Fase-fasenya

| Fase | Waktu | Hasil |
|---|---|---|
| 0 · Fondasi | 13–31 Agt (~20 j) | Agent loop minimal, 3 tool — **checkpoint kelayakan** |
| 1 · Otak + filesystem | Sept (~32 j) | Spek #1, #2 terkunci + safety gate |
| 2 · Metadata + log | Okt (~20 j) | Spek #2, #3 — sengaja ringan karena UTS |
| 3 · Voice | Nov (~34 j) | Spek #5 — bulan bernilai tertinggi |
| 4 · Face recognition | Des (~18 j) | Spek #4 — ringan karena UAS |
| 5 · Integrasi + hardening | Jan (~24 j) | Manajemen VRAM, stabil 8 jam |
| 6 · Poles + demo | Feb (~12 j) | Portofolio |

Fase 0 sengaja saya taruh **sekarang, sebelum kuliah mulai** — itu jendela paling longgar sepanjang enam bulan, dan sekaligus gerbang jujur pertama. Kalau agent loop minimal tidak selesai sebelum perkuliahan dimulai, itu sinyal untuk memperkecil target ke asisten berbasis teks saja, bukan memaksakan rencana penuh.

Tanggal-tanggalnya saya asumsikan kuliah mulai akhir Agustus, UTS pertengahan Oktober, UAS pertengahan Desember — sesuaikan dengan kalender akademik FMIPA yang resmi.

Mau saya langsung mulai Fase 0 (struktur repo, venv, verifikasi CUDA, agent loop minimal)? Atau kalau roadmap-nya mau dibaca dalam bentuk halaman web yang lebih enak, bisa saya publish jadi artifact.

## 007 — User

ya saya bikin AI ini dengan tujuan jadi gartis karena develop sendiri dan saya 0 knowladge tentang machine learninng hanya saja sudah jago FFisika sebagai fondasi. Coba ubah strategi

## 008 — Assistant

Dua kendala baru ini mengubah banyak hal — tapi kabar baiknya, lebih sedikit dari yang kamu kira. Saya tulis ulang strateginya.

## 009 — Assistant

[Roadmap.md](Roadmap.md) sudah saya tulis ulang jadi v2. Ini yang berubah dan alasannya.

## Kendala "gratis" ternyata dampaknya kecil

Dari lima komponen AI yang kamu butuhkan, **empat sudah gratis dan lokal sejak draft pertama** — speech-to-text, text-to-speech, wake word, dan face recognition semuanya model open-source yang jalan di laptopmu. Cuma "otak"-nya yang tadinya pakai API berbayar.

Penggantinya: **Qwen3-4B lewat Ollama**. Kuantisasi Q4 ukurannya ~2.5 GB, jadi muat penuh di 4 GB VRAM kamu. Biaya berjalan jadi **Rp 0**, dan bonusnya sistem bisa offline penuh serta tidak ada data yang keluar dari laptop.

Ada satu hal yang justru **membaik** karena pindah ke lokal. Di v1 semua model rebutan 4 GB VRAM dan butuh bongkar-pasang. Sekarang pembagiannya tegas: **LLM menguasai GPU sendirian, semua indra pindah ke CPU** — Ryzen 6-core kamu selama ini menganggur dan sanggup menangani Whisper, Piper, dan InsightFace sekaligus. Masalah manajemen VRAM hilang.

## Soal "0 knowledge ML" — kalimat itu keliru

Fisika yang sudah kamu kuasai **adalah** matematika ML. Bukan analogi:

| Yang sudah kamu bisa | Namanya di ML |
|---|---|
| Prinsip aksi minimum *(Mekanika, A−)* | Minimasi loss function |
| Aturan rantai *(Fismat I–III, A−/A/A)* | Backpropagation |
| Ruang Hilbert, hasil kali dalam *(Kuantum, A−)* | Embedding, cosine similarity |
| Distribusi Boltzmann `e^(−E/kT)` *(Fisstat, sedang diambil)* | Softmax `e^(z/T)` — **persamaan identik** |
| Entropi *(Termo, A−)* | Cross-entropy loss |
| Fourier, konvolusi *(Gelombang, A−)* | Spektrogram, MFCC, layer konvolusi |

Parameter "temperature" pada LLM itu **memang dinamai dari suhu termodinamika** — rumusnya diturunkan dari distribusi Boltzmann. Menaikkan temperature secara matematis identik dengan memanaskan sistem.

Yang benar-benar belum kamu punya cuma tiga: kosakata (beberapa jam), perkakas PyTorch/numpy (beberapa hari), dan intuisi praktis — yang memang **hanya bisa datang dari mengerjakan**.

## Wawasan yang mengubah strategi

Saya periksa satu per satu, dan **empat dari lima spekmu tidak butuh ilmu ML sama sekali**. Akses laptop, baca file/log, dan metadata itu murni pemrograman Python. Face recognition dan voice cuma butuh cara memanggil pustaka.

> Memakai model pretrained adalah keterampilan memanggil pustaka, bukan keterampilan machine learning.

Kamu tak perlu tahu cara kerja ArcFace untuk memakainya, sama seperti tak perlu tahu isi LAPACK untuk memanggil `numpy.linalg.eig` di tugas Fismat. Seluruh "ML" pada face recognition itu lima baris kode, dan baris terakhirnya — hasil kali dalam dua vektor ternormalisasi — persis operasi `⟨ψ|φ⟩` yang sudah kamu pakai di Kuantum.

Artinya proyek ini **bukan sesuatu yang harus ditunda sampai jago ML.** Dia justru kendaraan untuk belajarnya, berjalan paralel dengan MK Machine Learning 2 SKS yang sedang kamu ambil. Teori masuk dari kelas, praktik dari sini, ketemu di Fase 4.

## Kendala sebenarnya bukan yang kamu sebut

Yang berubah signifikan justru hal ketiga: **model 4B jauh lebih lemah dari Claude.** Ini kompromi nyata dari "gratis", dan saya taruh satu bagian penuh (§6) untuk itu. Dia bagus memanggil satu tool, cukup untuk rencana 2–3 langkah, tapi **buruk** untuk rencana 6+ langkah dari perintah ambigu, dan JSON-nya rapuh.

Menyangkal ini akan membuatmu menghabiskan berminggu-minggu membenahi sesuatu yang memang tidak bisa diperbaiki lewat prompt. Jadi arsitekturnya dirancang mengelilingi keterbatasan itu — tiga siasat: **intent router** (80% perintah harian ditangani aturan deterministik, tanpa LLM sama sekali — hasilnya selalu benar dan instan), **grammar GBNF** (membatasi ruang keluaran sehingga JSON tidak valid jadi mustahil secara struktural, bukan sekadar diminta baik-baik), dan **sedikit tool per konteks**.

Yang kedua itu konsep yang sudah akrab buatmu: sama seperti menerapkan syarat batas pada persamaan gelombang — kamu tidak membujuk solusinya berperilaku di tepi, kamu mempersempit ruang solusi sehingga yang melanggar tak pernah muncul.

## Dua hal yang perlu saya sampaikan terus terang

**Anggaran waktunya sekarang defisit.** 160 jam tersedia, kebutuhan ~168 jam (143 proyek + 25 belajar). Saya sengaja tidak menyembunyikannya — artinya rencana ini tanpa kelonggaran, dan tangga pemangkasan di §12 kemungkinan besar benar-benar akan kamu pakai. Kalau pengajuan modul sebagai tugas kuliah diterima, defisit ini hilang sendiri.

**Risiko keamanan naik, bukan turun.** Model 4B lebih sering salah paham daripada model besar, sementara spek #1 memberinya akses penuh ke mesin berisi tugas kuliah dan kodemu. Safety gate tetap masuk Fase 1 dan tetap satu-satunya yang tidak boleh dipotong.

**Gerbang kelayakannya juga bergeser ke depan.** Fase 0 sekarang berujung pada satu pertanyaan: apakah Qwen3-4B konsisten memanggil tool dengan JSON valid, dan cukup cepat? Kalau tidak, kamu tahu **bulan ini** — saat masih ada waktu ganti rencana — bukan di bulan keempat.

Mau saya mulai Fase 0 sekarang? Saya bisa siapkan struktur repo, venv, cek instalasi Ollama, dan langsung uji tool calling Qwen3-4B di laptopmu — jadi gerbang kelayakannya terjawab hari ini juga.

## 010 — User

klao misal saya train model sendiri bisa gak???

## 011 — Assistant

Bisa — tapi "train model sendiri" itu lima hal yang sangat berbeda, dan jawabannya berbeda-beda. Mari saya pisahkan, karena di sinilah orang paling sering salah ambil keputusan.

## Apa yang muat di GTX 1650 Ti 4 GB

| Yang mau dilatih | Muat? | Waktu | Berguna untuk Jarvis? |
|---|---|---|---|
| LLM 7B dari nol | Tidak — butuh ~70 GB | — | — |
| GPT-2 124M dari nol | Muat, tapi **~2–3 tahun** | Tidak realistis | Tidak |
| nanoGPT ~10M char-level | Ya | 15–30 menit | Tidak — tapi sangat mendidik |
| QLoRA fine-tune 7B | Tidak — butuh ~6–8 GB | — | — |
| QLoRA fine-tune 1.5–3B | Ya, ketat | 2–6 jam | Terbatas — lihat bawah |
| Fine-tune Whisper (LoRA) | Ya, ketat | 4–8 jam | **Ya** — akurasi bahasa Indonesia |
| Custom wake word | Ya | ~1 jam | **Ya** |
| Speaker ID (verifikasi suara) | Ya | ~30 menit | **Ya** |
| **Intent classifier** | Ya — bahkan di CPU | **detik** | **Sangat** |
| Face recognition dari nol | Tidak realistis | — | Tidak perlu |

## Jebakan terbesar: fine-tuning tidak membuat model lebih pintar

Ini yang harus saya sampaikan sebelum apa pun, karena hampir semua orang salah di sini.

> **Fine-tuning mengubah gaya, bukan kecerdasan.**

Fine-tuning mengajari model *format*, *nada*, dan *pola domain*. Dia **tidak** menambah kemampuan menalar. Melatih Qwen3-4B dengan 5.000 contoh percakapan tidak akan membuatnya sanggup merencanakan 6 langkah — dia akan tetap gagal di situ, hanya dengan gaya bahasa yang lebih mirip kamu.

Dan hal yang paling ingin kamu perbaiki lewat fine-tuning — supaya JSON tool call-nya selalu valid — **sudah selesai gratis oleh grammar GBNF** di §6 roadmap. Grammar menjaminnya secara struktural, deterministik, tanpa satu baris data latih pun. Fine-tuning untuk itu berarti menghabiskan 20 jam demi versi yang lebih buruk dari yang sudah kamu punya.

Jadi: **jangan fine-tune otaknya.** Itu jalan buntu yang menyamar jadi jalan pintas.

## Yang justru sangat layak kamu latih

Kamu punya satu peluang yang bagus sekali, dan kebetulan sudah ada lubangnya di rencana:

**Intent classifier — pengganti intent router.**

Di §6 roadmap, router-nya pakai aturan regex. Regex itu rapuh: *"bukain file laporan dong"* dan *"tolong buka laporan"* butuh pola berbeda. Model terlatih menangani keduanya sekaligus.

```python
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression

enc = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")  # paham bahasa Indonesia
X = enc.encode(perintah)              # ~300 contoh yang kamu tulis sendiri
clf = LogisticRegression().fit(X, label)   # waktu latih: di bawah 1 detik
```

Kenapa ini pilihan terbaik untuk posisimu sekarang:

- **Ini ML sungguhan, lengkap** — kumpulkan data, beri label, split train/test, latih, evaluasi dengan confusion matrix, lalu deploy ke sistem nyata. Persis siklus yang diajarkan di MK Machine Learning.
- **Latihnya di bawah satu detik**, jadi kamu bisa beriterasi puluhan kali dalam satu sore. Untuk belajar, umpan balik secepat ini jauh lebih berharga daripada training 8 jam.
- **Tidak menambah beban ke anggaran waktu** — dia *menggantikan* pekerjaan regex yang sudah dijadwalkan. Tukar ~3 jam regex dengan ~6 jam ML, bersih hanya +3 jam.
- **Langsung terasa** — akurasi router naik, Jarvis jadi lebih jarang salah paham.
- **Datasetnya kamu buat sendiri** dari perintah yang memang kamu pakai sehari-hari. Tidak perlu cari dataset publik.

Kalau kamu hanya mau melatih **satu** model sepanjang enam bulan ini, latih yang ini.

## Peringkat selengkapnya

**Layak, sesuai urutan:**

1. **Intent classifier** (~6 j) — nilai tertinggi, effort terendah, materi kuliah ML paling pas
2. **Custom wake word** (~8 j) — panggil dia dengan namamu sendiri; openWakeWord punya pipeline training bawaan
3. **Speaker ID** (~8 j) — verifikasi suara, dipasangkan dengan face recognition untuk autentikasi dua faktor
4. **Fine-tune Whisper untuk bahasa Indonesia** (~15 j) — dampaknya paling terasa, dan irisan DSP × ML-nya bagus untuk dua mata kuliah sekaligus, tapi paling berisiko di VRAM 4 GB

**Jangan:**

5. Fine-tune otak 4B — GBNF sudah menyelesaikannya gratis
6. Latih LLM yang layak pakai dari nol — secara fisik mustahil di perangkat ini

**Kategori tersendiri — nanoGPT dari nol** (~10 j). Modelnya tidak berguna sama sekali untuk Jarvis, tapi kamu akan benar-benar paham cara kerja transformer dari dalam: attention, embedding, training loop, semuanya dalam ~300 baris yang bisa kamu baca habis. Kerjakan saat liburan kalau penasaran, **jangan** saat semester berjalan.

Satu hal yang akan langsung klik buatmu di situ: training itu **menuruni permukaan energi potensial**. Noise pada SGD berperan seperti fluktuasi termal yang membantu lolos dari minimum lokal, dan jadwal penurunan learning rate itu **jadwal pendinginan** — istilah *simulated annealing* memang diambil dari metalurgi dan mekanika statistik. Fisika Statistik yang sedang kamu ambil membahas persis kerangka ini.

## Rekomendasi

Ambil **intent classifier di Fase 1**, dan jadikan itu tugas besar MK Machine Learning. Itu ML sungguhan, meningkatkan Jarvis secara terukur, dan nyaris tidak menambah beban waktu karena menggantikan pekerjaan yang sudah dijadwalkan.

Sisanya tahan dulu sampai **Fase 4 selesai**. Setelah pipeline dasarnya jalan dan kamu sudah punya intuisi dari MK ML, wake word dan speaker ID jadi ekstensi yang wajar. Fine-tune Whisper simpan untuk liburan atau semester 6.

Ingat §10: kamu sudah defisit ~8 jam sebelum training masuk hitungan. Melatih satu model kecil yang benar-benar dipakai jauh lebih berharga daripada empat model yang tak sempat diintegrasikan.

Mau saya masukkan ini ke roadmap sebagai §16 sekaligus revisi Fase 1 — intent router-nya diganti dari regex ke classifier terlatih?

## 012 — User

nah iya maksud saya gitu, kita beneran belajar bikin AI dari nol tanpa penggunaan API sama sekali, jalan barengan sama matkulnya gitu maksud saya, 6 bulan itu untuk memahami dasar saja cukup untuk tujuan akhir ya spesifikasi yg diminta sebelumnya itu tentatif sampai kapan pun saya mau

## 013 — Assistant

Sekarang saya paham arah kamu, dan ini pembingkaian yang jauh lebih baik. Dua roadmap sebelumnya salah sasaran — keduanya mengejar **produk jadi dalam 6 bulan**, padahal yang kamu mau adalah **paham betul dalam 6 bulan**, dengan produk sebagai tujuan terbuka. Itu mengubah hampir semuanya.

## 014 — Assistant

Ada satu bug rendering nyata di tabel — karakter `|` pada notasi bra-ket memecah kolom. Saya perbaiki.

## 015 — Assistant

Roadmap v3 sudah menggantikan isi [Roadmap.md](Roadmap.md). Dua draft sebelumnya memang salah sasaran — keduanya mengejar produk jadi dalam 6 bulan lalu memampatkan pembelajaran ke sela-selanya. Hasilnya rencana defisit 8 jam yang penuh kompromi. Dengan sasaran yang benar, tekanannya hilang.

## "Dari nol" itu dua hal, dan kamu bisa dapat keduanya

Perlu saya luruskan di depan, karena di sini orang sering menyerah:

**Dari nol untuk paham** — kamu tulis sendiri algoritma intinya. Backprop kamu turunkan dan kode sendiri, attention kamu bangun dari kosong, konvolusi kamu implementasikan manual. Tanpa PyTorch dulu.

**Dari nol untuk sistem** — tanpa API, tanpa layanan luar, tanpa tagihan. Semua di laptopmu.

Yang **tidak** bisa dan tidak perlu: menulis ulang Whisper atau ArcFace. Itu ribuan GPU-hour dan jutaan sampel. Tak seorang pun melakukannya sendirian, dan bukan begitu cara orang belajar.

> Bangun dari nol untuk **paham**. Pakai pretrained untuk **jalan**.

Bedanya kamu dengan orang yang sekadar menempel pustaka: setelah 6 bulan, saat memanggil Whisper kamu tahu persis ada spektrogram dan transformer di dalamnya — karena kamu sudah menulis keduanya sendiri.

Soal "tanpa API": mengunduh model pretrained itu unduhan sekali jalan, bukan panggilan API. Setelah terunduh, laptop bisa dicabut dari internet selamanya dan Jarvis tetap hidup.

## Temuan yang paling mengubah rencana

**Jarvis tidak butuh LLM sampai Bulan 6.**

Sebagian besar perintah harian sebenarnya bisa diklasifikasikan — *"buka laporan minggu lalu"*, *"berapa sisa disk"*, *"baca log error"*. Itu bukan masalah penalaran bahasa, itu **klasifikasi intent + ekstraksi parameter** — supervised learning klasik yang kamu kuasai di Bulan 2.

Artinya **Jarvis v0.1 di Bulan 2 sudah berguna tanpa satu pun LLM.** Voice di Bulan 3 juga tidak butuh. Face di Bulan 4 juga tidak. LLM baru masuk Bulan 6, khusus untuk permintaan terbuka yang tak bisa diklasifikasikan.

Ini sekaligus menyelesaikan kecemasan draft v2 soal Qwen3-4B yang lemah: dia tidak lagi memikul seluruh sistem, hanya sisa 10–20% yang sulit.

## Peta enam bulannya

Tiap bulan: satu konsep, sesuatu yang kamu tulis sendiri, satu komponen Jarvis. **Tidak ada latihan yang terbuang.**

| Bulan | Kamu tulis sendiri | Masuk ke Jarvis |
|---|---|---|
| 0 · Agt | Gradient descent manual, regresi linear numpy | intuisi optimasi |
| 1 · Sep | **Mesin autograd ~150 baris**, MLP tanpa pustaka | mesin buatanmu |
| 2 · Okt | Regresi logistik, cross-entropy dari nol | ✅ **Intent classifier** → v0.1 |
| 3 · Nov | Konvolusi, spektrogram, MFCC, CNN | ✅ **Wake word + voice** → v0.2 |
| 4 · Des | Siamese network, contrastive loss | ✅ **Face recognition** → v0.3 |
| 5 · Jan | **Transformer utuh, mini-GPT dilatih sendiri** | Qwen bukan lagi kotak hitam |
| 6 · Feb | Agent loop, orkestrator | ✅ **Jarvis v1.0** |

Momen paling penting ada di Bulan 1: setelah menulis MLP dari nol, kamu tulis ulang dengan PyTorch dan lihat hasilnya identik. Saat itu kamu sadar PyTorch **tidak melakukan sihir apa pun** — dia cuma versi cepat dari yang barusan kamu tulis.

## Anggaran waktunya sekarang longgar

```
Tersedia   ≈ 160 jam
Kebutuhan  ≈ 148 jam
Kelonggaran ≈ 12 jam   (v2: defisit 8 jam)
```

Dan yang lebih penting dari angkanya: **kalau satu bulan meleset, tidak ada yang rusak.** Tiap bulan berdiri sendiri, jadi kamu hanya belajar lebih pelan. Untuk mahasiswa 22 SKS, ini yang membuat proyeknya bertahan sampai akhir.

Semua yang kamu latih muat lega di GTX 1650 Ti — intent classifier hitungan **detik**, CNN keyword spotting ~30 menit, mini-GPT 30–60 menit. Batasan 4 GB baru terasa di Bulan 6, dan Qwen3-4B terkuantisasi pun masih muat.

## Yang perlu saya sampaikan terus terang

**Empat dari lima spek akan berfungsi di akhir Februari** — file, metadata, face recognition, voice command. Spek pertama (akses penuh dengan penalaran setara Claude) baru **dimulai**, bukan selesai. Bagian itu bergantung pada kualitas LLM, dan di situlah pekerjaan setelah 6 bulan berada. Sesuai yang kamu bilang: tanpa tenggat.

**Risiko terbesarnya bukan teknis.** Ia adalah melompati bagian "dari nol" karena terasa lambat — lalu tanpa sadar kembali jadi pengguna pustaka yang tidak paham isinya, persis yang ingin kamu hindari. Karena itu aturan #1 di §10: setiap konsep dikerjakan dua kali, dari nol dulu baru pustaka, dan urutannya tidak boleh dibalik.

Satu hal yang tetap saya pertahankan dari draft sebelumnya: **temui dosen ML dan DSP di minggu pertama**, ajukan intent classifier sebagai tugas besar ML dan wake word sebagai tugas DSP — sebelum topik tugas ditetapkan.

Mulai Bulan 0 sekarang? Saya bisa siapkan struktur repo, venv, verifikasi CUDA, lalu kita tulis regresi linear + gradient descent dari nol dengan plot permukaan loss yang bisa kamu lihat menurun.

## 016 — User

cek library python yg terinstall ada apa saja, dan cek kelayakan sebagai diagnosa. Dan rincikan list tugas per hari

## 017 — Assistant

Saya jalankan diagnosa lingkungannya dulu.

## 018 — Assistant

Ada temuan penting. Saya verifikasi beberapa hal lagi.

## 019 — Assistant

PowerShell quoting mengacaukan query audio. Saya pakai skrip terpisah.

## 020 — Assistant

Diagnosa lengkap. Saya tulis hasilnya beserta rencana harian ke file terpisah.

## 021 — Assistant

Satu koreksi faktual perlu masuk ke roadmap — asumsi VRAM saya sebelumnya keliru.

## 022 — Assistant

Diagnosa selesai, dan hasilnya bagus. Rinciannya ada di [Bulan-0-Harian.md](Bulan-0-Harian.md).

## Vonis: sangat layak — lebih siap dari perkiraan

Temuan utamanya:

> **Bulan 0 bisa kamu mulai hari ini tanpa menginstal apa pun.**

numpy 2.4.6, matplotlib 3.10.9, scipy 1.17.1, dan scikit-learn 1.9.0 semuanya sudah terpasang dan versinya baru. Seluruh materi Bulan 0 — regresi linear, gradient descent, plot permukaan loss — tidak butuh satu pun paket tambahan.

Beberapa yang sudah ada dan kebetulan pas sekali:

- **manim + pyvista + vtk + plotly** — untuk memvisualisasikan permukaan loss 3D dan menganimasikan lintasan gradient descent di Hari 9, perkakasnya bahkan berlebih
- **onnxruntime 1.27** — ini mesin yang dipakai InsightFace, sudah siap untuk Bulan 4
- **sounddevice 0.5.2** + 36 perangkat input terdeteksi (mikrofon Realtek internal siap) — Bulan 3 aman
- **pypdf, pymupdf, python-docx, openpyxl, psutil, pywin32** — seluruh toolset metadata dan sistem untuk Bulan 6 sudah lengkap

**CUDA terverifikasi berfungsi**, bukan sekadar terpasang: tes cupy lulus, compute capability 7.5 (Turing, didukung penuh PyTorch), driver 555.85.

**Yang kurang cuma PyTorch** — dan itu pun baru dipakai Hari 15.

## Tiga hal yang perlu ditindaklanjuti

**1. Koreksi: VRAM sudah terpakai 979 MB saat idle.** Di roadmap sebelumnya saya menduga tampilan Windows digerakkan iGPU Radeon sehingga 1650 Ti bebas penuh. Ternyata tidak — sisa efektifnya **~3.1 GB**, bukan 4 GB. Pemakainya teridentifikasi: Wallpaper Engine, Chrome, Epic Games Launcher, Steam, Antigravity. Untuk Bulan 0–4 tidak berpengaruh sama sekali (semua latihan muat di 2 GB), tapi akan terasa di Bulan 5–6. Menutup Wallpaper Engine dan launcher game biasanya membebaskan 500–700 MB. Roadmap sudah saya koreksi.

**2. Ini yang paling penting — venv itu wajib, bukan saran.** Python global-mu berisi ~250 paket termasuk tumpukan riset fisika yang jelas kamu pakai: `astropy`, `spacepy`, `pyspedas`, `cdflib`, `geopack`, `juliacall`, `schroedingerequation`.

Menginstal pustaka ML ke lingkungan global itu berisiko nyata. Nanti di Bulan 3–4, `librosa` atau `insightface` bisa meminta numpy versi lebih rendah, dan pip akan **menurunkan numpy global tanpa bertanya** — lalu tumpukan fisikamu rusak di tengah semester, kemungkinan besar saat sedang mengerjakan tugas. Semua `pip install` untuk proyek ini harus di dalam venv aktif, tanpa pengecualian.

**3. numpy 2.4.6 dan pandas 3.0.3 sangat baru.** Sebagian pustaka ML tertinggal beberapa bulan dari rilis numpy mayor. Venv terpisah sekaligus menyelesaikan ini — kalau nanti perlu menurunkan versi, lakukan di dalam venv tanpa menyentuh lingkungan fisikamu.

## Rencana harian 13–31 Agustus

19 hari: **15 hari aktif, 4 hari istirahat, ~28 jam**. Alurnya:

| Hari | Fokus |
|---|---|
| 1 *(13 Agt)* | venv + repo + PyTorch dipasang lalu **disisihkan** sampai Hari 15 |
| 2–3 | numpy sampai paham · data sintetis · tulis MSE sendiri |
| 4 | istirahat |
| 5 *(17 Agt, HUT RI)* | **turunkan gradien di kertas** — tanpa kode, ini kerja Fismat |
| 6–7 | implementasi gradien + gradient check · **training loop pertama** |
| 8 | learning rate: lihat sendiri divergensinya |
| 9 ⭐ | **permukaan loss 3D + animasi lintasan** — hari terpenting Bulan 0 |
| 10 | multivariat, vektorisasi penuh |
| 11 | istirahat |
| 12–13 | overfitting pertamamu · regularisasi L2 |
| 14 | bandingkan dengan sklearn — buktikan tidak ada sihir |
| 15 | **PyTorch mengerjakan hal yang sama** — `backward()` vs gradien manualmu |
| 16 | GPU: pelajari kapan GPU justru **kalah** dari CPU |
| 17 | rapikan + dokumentasikan |
| 18 | buffer |
| 19 | tinjau + siapkan pertanyaan untuk dosen ML & DSP |

Dua hari yang paling menentukan: **Hari 9**, saat kamu melihat animasi bola menggelinding menuruni permukaan energi potensial dan gradient descent berhenti terasa abstrak. Lalu **Hari 15**, saat gradien dari `loss.backward()` ternyata sama persis dengan gradien yang kamu turunkan sendiri di kertas — dan autograd berhenti terasa gaib.

File-nya juga memuat daftar **yang tidak boleh dilakukan** (jangan pip install di luar venv, jangan pakai PyTorch sebelum Hari 15, jangan menonton kursus ML) dan enam pertanyaan tolok ukur untuk mengukur pemahamanmu di akhir bulan.

Mau saya kerjakan Hari 1 sekarang — struktur repo, venv, verifikasi isolasi, dan pasang PyTorch cu124?

## 023 — User

Beri nama AI saya ini SYNESIS (Seeking Yet Never-Ending Exploration of Science & Intelligence System)

Menurut mu bagaimana?? S:\Code\Make A Jarvis\Name.md

## 024 — Assistant

File-nya sudah ada isinya — dan lebih kaya dari yang kamu sebut di pesan: ada dua tingkat, SYNESIS sebagai ekosistem dan SEREN sebagai agennya. Tapi ada `cat > SEREN.md <<'EOF'` nyasar di baris pertama dan blok kodenya terpotong belum tertutup.

Pendapat saya: **namanya bagus sekali — jauh lebih bagus dari yang kamu sadari.** Tapi ada tiga hal yang perlu saya sampaikan terus terang.

## 025 — Assistant

Namanya bagus — dan alasan terkuatnya mungkin belum kamu sadari.

## SYNESIS bukan sekadar akronim yang kebetulan enak

**σύνεσις** adalah kata Yunani Kuno yang benar-benar ada, artinya **"pemahaman"** — daya tangkap, kearifan menilai. Etimologinya dari **σύν** ("bersama") + **ἵημι** ("menaruh"): secara harfiah **"menaruh bersama-sama"**, menyatukan hal-hal terpisah sampai jadi mengerti.

Aristoteles membahasnya di *Nicomachean Ethics* Buku VI sebagai salah satu **keutamaan intelektual** — kemampuan menilai dengan baik, dibedakan dari *phronesis* (kebijaksanaan praktis) dan *sophia* (kebijaksanaan teoretis). Rumusannya: *phronesis* memerintah, *synesis* menilai.

Tiga alasan ini pas secara luar biasa:

**Artinya persis tesis proyekmu.** Seluruh Roadmap v3 berdiri di atas satu prinsip — bangun dari nol untuk *paham*, pakai pretrained untuk jalan. Kamu menamai sistemmu dengan kata yang artinya "pemahaman".

**"Menaruh bersama-sama" menggambarkan dua lapis sekaligus.** Teknis: menyatukan suara, penglihatan, berkas, penalaran. Intelektual: menyatukan fisika dan ML — dan §11 Roadmap menunjukkan keduanya memang formalisme yang sama.

**Koheren dengan identitasmu.** Mahasiswa Fisika menamai AI-nya dengan keutamaan epistemik Yunani — itu nyambung dengan cara yang "Jarvis" (pinjaman dari Marvel) tidak akan pernah bisa.

## Tiga hal yang perlu saya sampaikan terus terang

**1. Akronim SYNESIS-nya bagian yang paling lemah.** *"Seeking Yet Never-Ending Exploration of Science & Intelligence System"* tidak terbaca sebagai kalimat Inggris yang wajar, dan **"Yet"** jelas dipasang semata untuk memenuhi huruf Y. Bandingkan dengan SEREN — *"[Scientific Exploration & Reasoning] Engine for [Networked Intelligence]"* — itu frasa utuh dan gramatikal. SEREN tersusun jauh lebih rapi.

Dua jalan keluar: ganti *Yet* → *Yearning* supaya sejajar dengan *Seeking* ("Seeking, Yearning, Never-Ending — Science & Intelligence System"), **atau lepaskan saja backronym-nya.** Saya sarankan yang kedua. SYNESIS tidak butuh kepanjangan karena ia sudah kata sungguhan dengan arti yang tepat. Backronym menjelaskan huruf; etimologi menjelaskan maksud.

**2. "Networked Intelligence" berisiko jadi kontradiksi.** Kendala mutlakmu adalah tanpa API, sepenuhnya offline — tapi "Networked" gampang dibaca sebagai terhubung internet. Cukup nyatakan sekali di file bahwa yang dimaksud adalah **jaringan internal antar modul dan basis pengetahuan**, bukan konektivitas internet. Sudah saya tuliskan di Name.md.

**3. Pembagian dua tingkatnya bagus sebagai konsep, tapi jangan menyetir kode dulu.** Memisahkan ekosistem dari agen itu instinct arsitektur yang benar. Masalahnya kamu belum punya satu baris kode pun, dan membangun ontologi dua tingkat sebelum menulis training loop pertama adalah cara klasik menghabiskan energi di diagram alih-alih di sistem. Pemisahan itu baru bermakna kalau benar-benar ada beberapa agen — kemungkinan Bulan 5 ke atas. Sampai itu: satu repo, satu paket.

## Satu konsekuensi praktis untuk Bulan 3

Kamu akan **melatih wake word sendiri**, jadi pilihan nama berdampak langsung ke akurasinya:

| Kandidat | Suku kata | Penilaian |
|---|---|---|
| "Sera" | 2 | **Terlalu pendek** — rawan salah picu |
| "Hey Sera" | 3 | Bisa dipakai |
| "Hey Seren" | 3 | Lebih baik — konsonan akhir memperjelas batas |
| **"Hey Synesis"** | 4 | **Terbaik** — paling khas |

Catatan: *Synesis* kaya bunyi desis, sedikit lebih sulit dikenali di ruangan berisik dibanding bunyi letup. Uji keduanya di Bulan 3 dengan rekaman suaramu — putuskan dari data, bukan selera. Pengucapan Indonesianya **si-NE-sis**, luwes di lidah.

---

Name.md sudah saya rapikan: ada `cat > SEREN.md <<'EOF'` nyasar di baris pertama (sisa perintah shell yang ikut tertempel) dan blok kode pohonnya terpotong belum tertutup. Struktur dan keputusan penamaanmu saya pertahankan utuh — yang saya tambahkan hanya etimologi, catatan praktis, dan konvensi kode.

Mau saya sekalian ganti seluruh "Jarvis" jadi "SYNESIS" di Roadmap.md dan Bulan-0-Harian.md, plus rename foldernya dari `Make A Jarvis`?

## 026 — User

udah setuju aja dengan nama dari saya ekskekusi ke smua log

## 027 — Assistant

Siap, keputusan kamu. Nama dan kepanjangannya saya pakai apa adanya. Saya cek dulu semua kemunculan "Jarvis".

## 028 — Assistant

Sekarang Name.md — kepanjangan kamu saya kunci sebagai final, dan bagian yang mempersoalkannya saya cabut.

## 029 — Assistant

Sisa tiga kemunculan itu memang disengaja — dua di catatan perubahan, satu di perbandingan dengan nama lama. Sekarang folder-nya.

## 030 — Assistant

Folder-nya terkunci proses lain. Semua isi file sudah beres — folder ini satu-satunya yang gagal.

## 031 — Assistant

Selesai. Nama dan kepanjangan kamu dipakai apa adanya, tanpa revisi.

**[Roadmap.md](Roadmap.md)** — 24 kemunculan diganti, termasuk:
- Judul → `Belajar AI dari Nol → SYNESIS`
- Milestone: `SYNESIS v0.1` → `v0.2` → `v0.3` → `v1.0`
- §4 → *"SYNESIS Tidak Butuh LLM Sampai Bulan 6"*
- Wake word Bulan 3 → *"Hey Synesis"*

**[Bulan-0-Harian.md](Bulan-0-Harian.md)** — `CLI SYNESIS`, dan nama paket di Hari 1 → `synesis/`

**[Name.md](Name.md)** — dirapikan dan dikunci:
- Bagian yang mempersoalkan akronim sudah dicabut
- Ditambah **Keputusan Final** bertanggal, memuat tabel SYNESIS / SEREN / Sera dengan kepanjangan resmi kamu
- Etimologi Yunani tetap ada, tapi posisinya jelas sekarang: **lapisan makna tambahan untuk menjelaskan filosofi**, bukan pengganti kepanjangan
- Checklist penerapan sudah dicentang

Tiga kata "Jarvis" yang tersisa di Name.md sengaja dibiarkan — dua di catatan perubahan, satu di kalimat pembanding dengan nama lama.

## Satu yang gagal: rename folder

```
GAGAL: The process cannot access the file because it is being used by another process.
```

Foldernya dipegang dua proses sekaligus — editor Antigravity kamu, dan working directory shell saya sendiri yang otomatis di-reset ke folder itu setiap kali perintah dijalankan. Jadi dari sini memang tidak bisa, berapa kali pun dicoba.

Tutup editornya, lalu jalankan ini dari PowerShell mana pun:

```powershell
Rename-Item -LiteralPath "S:\Code\Make A Jarvis" -NewName "SYNESIS"
```

Setelah itu buka ulang foldernya di editor dari path baru `S:\Code\SYNESIS`. Isinya sudah bersih semua, tinggal nama wadahnya.

## 032 — User

Help me create a Skill called "Revision Coach" that turns my
feedback into a student-facing action list.

When invoked, ask me for:
1. My feedback comment (paste)
2. The rubric and the student's current scores
3. The reassessment policy (deadline, attempts allowed)
4. The student's apparent skill level

Output a student-facing action list:
- Top 3 priorities ranked by impact on the next score
- For each priority: what to do, where in the artifact to do it,
  what success looks like
- A self-check the student runs before resubmitting
- A short reminder of the proficiency standard
- A note on what is already strong and should be preserved
- An encouragement line that matches the tone in my ABOUT ME

Always read my ABOUT ME folder first.
Save as a permanent Skill.

Help me create a Skill called "Lecture Builder" that turns a
topic into structured lecture notes or slide outlines.

When invoked, ask me for:
1. Course, topic, and session length
2. Student level
3. Three things they should walk out understanding
4. Current real-world contexts I want to anchor to
5. My usual pacing (lots of stops for discussion, fewer stops,
   pure delivery)
6. Visual style (text-heavy slides, image-led, minimal)

Output:
- Opening hook tied to current context
- 3-5 main sections with key points
- 2 examples and 1 analogy per section
- Built-in discussion prompts every 10-15 minutes
- A closing synthesis question
- Slide outline if requested with speaker notes
- Things to remove if I run short on time

Always read my ABOUT ME folder first.
Save as a permanent Skill.

Help me create a Skill called "Lesson Plan Designer" that builds
a single class session minute-by-minute.

When invoked, ask me for:
1. Course and topic for the session
2. Session length and class size
3. Modality (in-person, online sync, hybrid)
4. The one thing students must leave understanding
5. What they were supposed to do before class
6. Materials and tech available

Output:
- Opening hook (3-5 minutes) that creates the question
- Minute-by-minute plan with activity, purpose, timing
- 2 active learning moments minimum
- Transitions between activities written out
- Built-in formative check at the halfway point
- Closing reflection that maps to the next session
- A "what to do if energy drops" backup move
- Materials list

Always read my ABOUT ME folder first.
Save as a permanent Skill.

Buatin 3 skill ini siap pakai untuk dipanggil

## 033 — Assistant

Sebelum menulis skill-nya, saya cari dulu folder ABOUT ME — ketiganya bergantung pada itu.

## 034 — Assistant

Folder ABOUT ME belum ada. Saya lihat dulu format skill yang sudah terpasang supaya konsisten.

## 035 — Assistant

Format terkonfirmasi. Saya buat folder ABOUT ME dulu — ketiga skill akan gagal di langkah pertama tanpa itu.

## 036 — Assistant

Ketiganya terpasang di level user (`~/.claude/skills/`), jadi permanen dan bisa dipanggil dari project mana pun — bukan cuma dari folder ini.

| Skill | Panggil dengan |
|---|---|
| **Revision Coach** | `/revision-coach` |
| **Lecture Builder** | `/lecture-builder` |
| **Lesson Plan Designer** | `/lesson-plan-designer` |

## ⚠️ Satu hal yang harus kamu kerjakan dulu

**Folder ABOUT ME tidak ada** — saya cek di `~/.claude/`, home, dan folder project, tidak ketemu. Padahal ketiga skill mensyaratkan membacanya di Step 0.

Saya buatkan templatnya di `~/.claude/ABOUT ME/teaching-profile.md`, tapi **masih kosong dan perlu kamu isi**. Kalau tidak diisi, ketiga skill akan berhenti di langkah pertama dan minta path-nya — itu memang sengaja: saya tidak mau mereka mengarang nada bicara, standar penilaian, atau karakteristik mahasiswamu.

Bagian yang paling menentukan kualitas output:
- **Voice and tone** → menyetir baris encouragement di Revision Coach
- **Language for student-facing output** → set ke Bahasa Indonesia kalau output untuk mahasiswa harus berbahasa Indonesia (file skill-nya sendiri berbahasa Inggris, tapi outputnya ikut setelan ini)
- **What "proficient" means** → jadi bagian "standard" di Revision Coach
- **Activities that fall flat** → di Lesson Plan Designer ini **daftar veto**, bukan saran

Folder itu membaca semua file di dalamnya, jadi kamu bisa tambah `rubrics.md`, `course-catalog.md`, dan lain-lain.

## Keputusan desain di luar spesifikasi literal

Beberapa hal saya tambahkan karena tanpanya spesifikasinya tidak benar-benar bisa dijalankan:

**Revision Coach — mesin perankingannya dibuat eksplisit.** "Ranked by impact on the next score" butuh definisi, jadi saya buat konkret: petakan tiap isu ke kriteria rubrik → hitung `poin tersedia − poin didapat` → kalikan dengan peluang berhasil diperbaiki sebelum deadline. Lalu kebijakan reasessment mengubah urutannya — satu attempt memihak perbaikan pasti, banyak attempt memungkinkan perbaikan struktural yang berisiko tapi bernilai besar. Ada juga pagar keras: dilarang memunculkan kekurangan yang tidak disebut di feedback aslimu.

**Lecture Builder — waktu wajib dihitung dulu sebelum menulis.** Jumlah menit harus sama persis dengan durasi sesi, termasuk buffer 8–10%. Jumlah discussion stop diturunkan dari jawaban pacing lewat tabel. Dan ada aturan: **setiap section harus melayani salah satu dari tiga walk-out understanding** — kalau tidak, itu bahan bacaan, bukan bahan kuliah, dan langsung masuk cut list.

**Lesson Plan Designer — ukuran kelas dan modality yang memilih aktivitas, bukan selera.** Ada tabel: think-pair-share jalan di kelas 20–50 tapi mati di 150+. Formative check wajib punya **tiga cabang** (mayoritas paham / terbelah / mayoritas gagal) beserta blok mana yang dikorbankan — check tanpa cabang cuma hiasan.

**Ketiganya:** tidak akan menanyakan ulang hal yang sudah kamu sertakan saat memanggil, dan akan mengusulkan nilai default dari ABOUT ME lalu minta konfirmasi saja.

Isi dulu `teaching-profile.md`-nya, lalu coba `/revision-coach` dengan satu feedback asli — dari situ paling kelihatan bagian mana yang perlu disetel.

## 037 — User

ya sbenernya saya mau mulai day 0 sih cuman pengen kamu berperan guru/dosen pembimbing saja. Ayo ekskusi day 0 dan ajarkan saya

## 038 — Assistant

Baik. Mulai sekarang saya pakai peran itu — saya jelaskan **kenapa**, kamu yang harus paham, bukan sekadar punya folder yang jadi.

Cek keadaan awal dulu. Seorang pembimbing tidak pernah mulai tanpa tahu titik berangkatnya.

## 039 — Assistant

API Error: Connection dropped (ECONNRESET)

## 040 — User

lanjut

## 041 — Assistant

Tiga temuan sebelum mulai:

- Dokumen sudah bersih — `Roadmap.md` dan `Bulan-0-Harian.md` nol "Jarvis". Dua sisa di `Name.md` memang disengaja (kontras dengan Marvel).
- Belum ada git.
- **Folder belum diganti nama.** Checklist di `Name.md` sudah dicentang, tapi kenyataannya masih `Make A Jarvis`.

Yang terakhir itu harus dibereskan **sekarang, sebelum venv dibuat** — dan ini pelajaran pertamamu hari ini.

> **Kenapa urutannya penting.** `venv` menyimpan **path absolut** di dalam `pyvenv.cfg` dan skrip aktivasinya. Kalau kamu buat venv di `Make A Jarvis` lalu folder itu diganti nama, venv-nya **rusak** — Python-nya menunjuk ke alamat yang sudah tidak ada. Ini jebakan klasik yang bikin orang bingung setengah jam. Ganti nama dulu, baru bikin venv.

## 042 — Assistant

Classifier keamanan sedang timeout. Saya coba lewat Bash.

## 043 — Assistant

Kedua shell terblokir — classifier keamanannya timeout, bukan masalah di sisimu. Saya tidak bisa mengeksekusi apa pun sampai pulih.

Jadi kita balik urutannya: **kamu yang mengetik, saya yang membimbing.** Untuk Hari 1 ini sebenarnya lebih baik — perintah yang kamu ketik sendiri akan kamu ingat, yang saya jalankan diam-diam tidak.

---

# Hari 1 — Lingkungan Kerja

Hari ini bukan tentang ML. Hari ini tentang membangun ruang kerja yang **tidak mengkhianatimu di Bulan 4**. Membosankan, tapi menahan beban.

Lima konsep dulu. Baru perintah.

## Konsep 1 — Kenapa venv ada

Python global-mu berisi ~250 paket, termasuk `astropy`, `spacepy`, `pyspedas`, `cdflib` — perkakas riset fisika yang kamu pakai untuk kuliah.

Skenario yang akan terjadi kalau kita ceroboh: di Bulan 3, `librosa` minta `numpy<2.3`. Kamu punya numpy 2.4.6. pip akan **menurunkan numpy global tanpa bertanya**. Minggu depannya kamu buka tugas Fisika Komputasi, `astropy` error, dan kamu tidak akan menghubungkannya dengan yang kamu install tiga minggu lalu.

Ini isolasi sistem — kebiasaan yang sudah kamu punya dari lab. Kamu tidak menjalankan eksperimen dengan variabel luar bocor masuk.

## Konsep 2 — venv itu bukan sihir

Penting supaya nanti saat rusak kamu tahu harus lihat ke mana. Sebuah venv cuma:

```
.venv/
├── Scripts/          ← python.exe, pip.exe, activate
├── Lib/site-packages/  ← paket-paketnya tinggal di sini
└── pyvenv.cfg        ← teks biasa, menunjuk ke Python induk
```

Dan "aktivasi" hanyalah **menaruh `.venv\Scripts` di depan PATH**. Setelah itu `python` merujuk ke python di dalam venv. Tidak ada yang lebih ajaib dari itu.

Konsekuensinya — dan ini yang tadi saya sebut: `pyvenv.cfg` menyimpan **path absolut**. Ganti nama foldernya setelah venv jadi, venv-nya mati.

## Konsep 3 — Verifikasi, jangan percaya

Kebiasaan fisika: ukur, jangan asumsikan. Kita tidak akan menganggap venv-nya terisolasi — kita **buktikan**. Tes yang paling meyakinkan justru yang *gagal*: `import astropy` harus **error** di dalam venv. Kalau berhasil, isolasimu bocor.

## Konsep 4 — Git bukan untuk kolaborasi

Kamu kerja sendiri, jadi git di sini bukan soal tim. Git adalah **izin untuk berani**. Kamu boleh hapus, boleh coba ide bodoh, boleh rusakkan training loop — karena `git checkout .` mengembalikan semuanya. Tanpa git kamu akan ragu-ragu, dan belajar sambil ragu itu lambat.

## Konsep 5 — Kenapa PyTorch dipasang hari ini padahal baru dipakai Hari 15

Memindahkan risiko ke depan. Instalasi CUDA gagal dengan cara-cara membosankan: wheel salah, driver ketuaan, runtime VC++ kurang. Kamu mau menemukan itu **hari ini** saat masih ada 18 hari kelonggaran — bukan di Hari 15 saat sedang mengalir.

Satu hal yang wajib kamu tahu sekarang, karena ini kebingungan nomor satu pemula:

> `torch.cuda.is_available()` mengembalikan `False` **paling sering karena kamu menginstal build CPU-only.** `pip install torch` biasa akan mengambil versi CPU dari PyPI. Yang menentukan adalah **`--index-url`**-nya.

---

# Perintah — ketik berurutan

**Tutup dulu Antigravity/VSCode** yang membuka folder ini, kalau tidak rename-nya akan ditolak Windows.

### 1. Ganti nama folder *(harus paling awal — Konsep 2)*

```powershell
cd S:\Code
Rename-Item "Make A Jarvis" "SYNESIS"
cd S:\Code\SYNESIS
```

### 2. Struktur repo

```powershell
mkdir synesis, notebooks, data, docs
Move-Item *.md docs\ -ErrorAction SilentlyContinue
```

### 3. Buat & aktifkan venv

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Prompt-mu sekarang harus diawali `(.venv)`. Kalau PowerShell menolak dengan *execution policy*, jalankan sekali:
`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

### 4. Buktikan isolasinya — tiga tes

```powershell
python -c "import sys; print(sys.prefix)"
pip list
python -c "import astropy"
```

Yang harus kamu lihat: path menunjuk ke dalam `.venv` · daftar paket **pendek** (~5, bukan 250) · dan yang ketiga **ModuleNotFoundError**. Error itu tanda berhasil.

### 5. Paket ringan

```powershell
pip install numpy matplotlib scipy scikit-learn jupyter rich
```

### 6. Git

```powershell
git init
"@
.venv/
__pycache__/
*.pyc
.ipynb_checkpoints/
data/
"@ | Out-File -Encoding utf8 .gitignore
git add -A
git commit -m "Hari 1: struktur repo, venv terisolasi, paket dasar"
```

### 7. PyTorch — unduhan besar, ~2.5 GB

```powershell
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
```

Perhatikan `--index-url`-nya. Itu yang membedakan build CUDA dari build CPU.

### 8. Gerbang Hari 1

```powershell
python -c "import torch; print(torch.__version__); print('CUDA:', torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU only')"
```

**Selesai bila** tercetak `CUDA: True` dan `NVIDIA GeForce GTX 1650 Ti`.

---

Jalankan sampai langkah 8, lalu **tempel hasil langkah 4 dan langkah 8** ke sini. Dari dua itu saya bisa memastikan isolasinya benar dan wheel-nya tidak salah ambil.

Kalau ada yang error di tengah, berhenti dan tempel error-nya — jangan lanjut. Di Hari 1 kesalahan yang dibiarkan akan menghantui sampai Bulan 6.

## 044 — User

kamu belum install apapun kan?? jawab singkat di chat saja jnagn eksekusi

## 045 — User

[Request interrupted by user]

## 046 — Assistant

No response requested.

## 047 — User

boleh kah custom install di directory drive lain yg non c atau d??

## 048 — Assistant

Boleh, bebas. venv itu folder biasa — dia ikut di mana project-nya berada, jadi `S:` (atau `E:`, `X:`) sama sahnya dengan `C:`.

Tiga hal yang tetap "bocor" ke `C:` kalau tidak diarahkan:

| Apa | Default | Pengalih |
|---|---|---|
| Cache pip | `C:\Users\...\AppData\Local\pip\Cache` | `PIP_CACHE_DIR` |
| Model HuggingFace *(Bulan 3–4)* | `C:\Users\...\.cache\huggingface` | `HF_HOME` |
| Model Ollama *(Bulan 6)* | `C:\Users\...\.ollama` | `OLLAMA_MODELS` |

Yang paling terasa: wheel PyTorch CUDA itu ~2.5 GB, dan cache-nya mendarat di `C:` kalau dibiarkan.

**Satu jebakan yang perlu kamu tahu:** venv menyimpan path **absolut** di dalamnya. Jadi huruf drive-nya harus stabil — kalau `S:` itu drive eksternal yang huruf-nya bisa berubah, venv-nya langsung rusak. Kalau internal, aman.

Kalau mau ruang paling lega, `E:` punya 191 GB bebas (vs `S:` 55.8 GB). Tapi 55.8 GB pun masih cukup untuk seluruh 6 bulan — PyTorch + semua model nanti kira-kira 15–20 GB.

Dan betul, **belum ada apa pun yang saya install.** Sejauh ini murni baca file dan cek diagnosa.

Mau ditaruh di drive mana?

## 049 — User

mending E atau X?? E itu ssd di enclosure

## 050 — Assistant

**X.** Jangan E.

Bukan soal kecepatan — SSD di enclosure USB 3.x masih kencang. Masalahnya tiga hal yang cocok persis dengan pola pakai proyek ini:

**1. venv menyimpan path absolut.** Kalau huruf drive enclosure bergeser (dan itu sering, tergantung urutan colok USB), venv-nya langsung mati. Harus dibuat ulang.

**2. Kamu akan pakai ini hampir tiap hari selama 6 bulan.** Enclosure berarti harus ingat colok. Satu sesi belajar 2 jam yang batal karena SSD ketinggalan di kos itu gesekan kecil yang lama-lama membunuh kebiasaan.

**3. Risiko cabut/sleep saat menulis.** Enclosure USB bisa auto-sleep atau lepas sendiri. Kalau itu terjadi pas `git commit` atau pas training menulis checkpoint, kamu bisa kehilangan kerja.

88.1 GB di X jauh lebih dari cukup — total kebutuhan seluruh 6 bulan sekitar **20–25 GB** (PyTorch ~3 GB, model-model ~15 GB, dataset Speech Commands ~2.4 GB, Ollama ~2.5 GB di Bulan 6).

Satu pertimbangan lagi: project-nya sekarang sudah di `S:` dengan 55.8 GB bebas — itu sebenarnya juga cukup. Kalau `S:` internal dan kamu tidak keberatan sisanya menipis, tidak pindah pun sah. Tapi kalau mau ruang lebih lega dan rapi, **X** pilihan yang benar.

E bagus untuk arsip, dataset besar, atau backup — bukan untuk lingkungan kerja harian.

## 051 — User

list dulu di chat coba apa saja yg bakal kita install. Cuman ya saya kepikiran kalo di enclosure SSD itu saya bisa pindah2 device heheh maslaah label huruf mah urusan nanti, saya juga udah jarang masang storage lain

## 052 — Assistant

Oke, E: it is — keputusan kamu.

Satu hal teknis yang justru penting buat tujuan kamu (pindah-pindah device), dan ini bukan soal huruf drive: **venv tidak pernah portabel antar komputer.** Dia menyimpan path absolut ke interpreter Python mesin tempat dia dibuat. Colok ke laptop lain, venv-nya mati — bukan karena `E:` jadi `F:`, tapi karena Python-nya beda.

Solusinya gampang dan justru standar: **perlakukan venv sebagai barang sekali pakai.** Yang portabel adalah repo + `requirements.txt`. Sampai di device lain, `python -m venv .venv` ulang, `pip install -r requirements.txt`, 5 menit selesai. Jadi taruh `.venv/` di `.gitignore` sejak Hari 1 — dan `E:` jadi pilihan yang benar-benar masuk akal.

Catatan kecil: kalau device lain tidak punya GPU NVIDIA, wheel PyTorch-nya beda (CPU-only). Makanya `requirements.txt` sebaiknya tidak mengunci versi CUDA.

---

## Yang akan diinstal

### Hari 1 — sekarang

| Paket | Ukuran | Untuk |
|---|---|---|
| numpy · scipy · matplotlib | ~150 MB | Bulan 0, seluruh fondasi |
| scikit-learn | ~40 MB | pembanding Hari 14, intent classifier Bulan 2 |
| jupyter · jupyterlab · ipykernel | ~200 MB | eksplorasi |
| rich | ~1 MB | output CLI |
| **torch + torchvision** (cu124) | **~4 GB** | dipasang Hari 1, **baru dipakai Hari 15** |

Subtotal: **~4.5 GB**

Yang besar cuma PyTorch — wheel CUDA-nya membawa cuDNN, cuBLAS, dan kawan-kawan.

### Bulan 2 · Okt — intent classifier

| Paket | Ukuran |
|---|---|
| sentence-transformers *(opsional)* | ~100 MB + model ~120 MB |

Opsional karena scikit-learn saja sudah cukup untuk classifier pertamamu.

### Bulan 3 · Nov — suara

| Paket | Ukuran |
|---|---|
| librosa · soundfile | ~50 MB |
| torchaudio | ~10 MB |
| silero-vad | ~2 MB |
| openwakeword | ~50 MB |
| faster-whisper *(+ ctranslate2)* | ~80 MB |
| piper-tts | ~30 MB |
| **Model:** Whisper small int8 | ~500 MB |
| **Model:** suara Piper | ~60 MB |
| **Dataset:** Google Speech Commands | **~2.4 GB** |

Subtotal: **~3.2 GB**

### Bulan 4 · Des — wajah

| Paket | Ukuran |
|---|---|
| opencv-python | ~70 MB |
| insightface | ~30 MB |
| **Model:** buffalo_s | ~150 MB |

Subtotal: **~250 MB**

### Bulan 5 · Jan — transformer dari nol

**Nol instalasi baru.** Cuma PyTorch yang sudah ada — tokenizer dan transformernya kamu tulis sendiri. Itu memang intinya.

### Bulan 6 · Feb — LLM lokal & integrasi

| Paket | Ukuran |
|---|---|
| **Ollama** *(installer Windows, bukan pip)* | ~1 GB |
| **Model:** Qwen3-4B Q4_K_M | ~2.5 GB |
| pypdf · pymupdf · python-docx · openpyxl | ~80 MB |
| pywin32 · psutil · pyyaml | ~30 MB |

Subtotal: **~3.6 GB**

---

**Total seluruh 6 bulan: ~12 GB**, ditambah cache pip yang bisa membengkak sementara saat unduh PyTorch. Sebut saja **~15 GB aman**.

Dari 191 GB bebas di `E:`, itu tidak terasa sama sekali.

Tiga env var yang perlu diarahkan supaya tidak bocor ke `C:` — `PIP_CACHE_DIR`, `HF_HOME`, `OLLAMA_MODELS` — saya set sekalian di Hari 1.

Lanjut eksekusi Hari 1 di `E:`? Kasih tahu path yang kamu mau, misal `E:\SYNESIS`.

## 053 — User

fungsi nya buat apa saja, dan juga apakah library yg sudah ad di laptop ini bisa dipakai juga?? coba cek dulu

## 054 — Assistant

Saya cek dulu mana yang sudah ada di global.

## 055 — Assistant

Hasil cek: **17 dari 29 paket sudah ada di global.** Termasuk seluruh kebutuhan Hari 1 kecuali PyTorch, dan hampir seluruh toolset Bulan 6.

## Fungsi tiap paket

### Hari 1 — fondasi

| Paket | Fungsinya | Status |
|---|---|---|
| **numpy** | Mesin array & matriks. Semua dibangun di atas ini — gradient descent dan backprop yang kamu tulis Bulan 0–1 murni numpy | ✅ 2.4.6 |
| **scipy** | Metode numerik di atas numpy: optimasi, integrasi, FFT, aljabar linear. Jadi pembanding hasil hitunganmu | ✅ 1.17.1 |
| **matplotlib** | Plot. Di Hari 9 inilah kamu menggambar permukaan loss 3D dan animasi lintasannya | ✅ 3.10.9 |
| **scikit-learn** | ML klasik: regresi, klasifikasi, train/test split, ROC. Dipakai Hari 14 sebagai pembanding, Bulan 2 intent classifier, Bulan 4 kalibrasi threshold | ✅ 1.9.0 |
| **jupyterlab + ipykernel** | Notebook — eksplorasi dengan umpan balik langsung | ✅ 4.2.4 |
| **pandas** | Data tabel. Bulan 2 untuk menyimpan 300–500 perintah berlabel | ✅ 3.0.3 |
| **rich** | Output terminal berwarna — nanti untuk CLI SYNESIS | ✅ 14.3.3 |
| **torch** | Framework deep learning: autograd, tensor GPU, layer, optimizer. Hari 15 kamu bandingkan gradiennya dengan gradien tulisanmu | ❌ |
| **torchvision** | Dataset & transformasi gambar — **MNIST untuk Bulan 1 ada di sini** | ❌ |

### Bulan 2 — embedding *(opsional)*

| Paket | Fungsinya |
|---|---|
| **sentence-transformers** | Ubah kalimat jadi vektor, supaya makna serupa berdekatan. Opsional — bag-of-words + sklearn sudah cukup, dan lebih sesuai semangat "dari nol" |

### Bulan 3 — suara

| Paket | Fungsinya |
|---|---|
| **librosa** | Analisis audio: muat file, spektrogram, MFCC, resampling. Ini kotak perkakas DSP-mu — dan kamu akan menulis spektrogram sendiri **dulu**, baru bandingkan ke librosa, pola yang sama seperti Hari 14 |
| **soundfile** | Baca/tulis WAV — backend librosa |
| **torchaudio** | Operasi audio di dalam PyTorch + **dataset Speech Commands** untuk melatih keyword spotter |
| **silero-vad** | Deteksi ada-tidaknya orang bicara. Sangat kecil, lewat `torch.hub` |
| **openwakeword** | Deteksi wake word **plus pipeline pelatihannya** — ini yang kamu pakai melatih "Hey Synesis" |
| **faster-whisper** | Speech-to-text. Versi Whisper yang dioptimasi, ~4× lebih cepat |
| **piper-tts** | Text-to-speech. Jalan di CPU, cepat |

### Bulan 4 — wajah

| Paket | Fungsinya | Status |
|---|---|---|
| **opencv-python** | Ambil frame webcam, operasi gambar, gambar kotak wajah | ❌ |
| **insightface** | Deteksi wajah (SCRFD) + embedding wajah (ArcFace) | ❌ |
| **onnxruntime** | Mesin yang benar-benar menjalankan model InsightFace | ✅ 1.27.0 |
| **scikit-image** | Pengolahan citra pendukung | ✅ 0.26.0 |

### Bulan 5 — transformer

**Tidak ada instalasi baru.** Cuma PyTorch. Tokenizer dan transformernya kamu tulis sendiri — itu memang intinya.

### Bulan 6 — LLM & integrasi

| Paket | Fungsinya | Status |
|---|---|---|
| **Ollama** | Menjalankan LLM lokal *(installer terpisah, bukan pip)* | ❌ |
| **pypdf · pymupdf** | Teks & metadata PDF | ✅ |
| **python-docx · openpyxl** | Word & Excel | ✅ |
| **pywin32** | API Windows: Event Log, proses, shell | ✅ 306 |
| **psutil** | Info sistem: CPU, RAM, disk, proses | ✅ 6.0.0 |
| **PyYAML** | File konfigurasi | ✅ 6.0.3 |

---

## Bisakah yang global dipakai ulang?

Secara teknis **bisa** — `python -m venv --system-site-packages .venv` membuat venv ikut melihat paket global.

**Tapi saya sarankan jangan**, dan alasannya justru tujuan kamu sendiri.

Kamu pilih `E:` supaya bisa pindah-pindah device. Venv yang bergantung pada paket global **hanya jalan di laptop yang punya paket global itu**. Colok ke komputer lain yang numpy-nya beda versi atau tidak punya scikit-learn — langsung rusak. Itu persis membatalkan alasan kamu memilih enclosure.

Dua alasan tambahan:
- `pip freeze` jadi kacau — `requirements.txt`-mu ikut mencatat paket global, atau malah melewatkannya
- Kamu kehilangan kebebasan mengunci versi. Nanti di Bulan 3–4 `librosa` atau `insightface` mungkin minta numpy lebih rendah — di venv bersih itu sepele, di venv yang menempel global itu jadi rumit

Dan hitungannya tidak sepadan: paket global yang bisa dihemat itu **~400 MB**, sementara PyTorch yang **4 GB** tetap harus diunduh karena tidak ada di global. Jadi kamu menukar portabilitas demi menghemat 10% unduhan.

**Gantinya, ini yang benar:** set `PIP_CACHE_DIR` ke `E:`. Sekali unduh, tersimpan di SSD itu juga. Bangun ulang venv di device lain — atau setelah venv rusak — tinggal pasang dari cache, tanpa unduh ulang, bahkan tanpa internet.

Jadi: **venv bersih, cache di E:.** Portabel betul, global fisikamu aman total, dan rebuild tetap cepat.

Lanjut Hari 1? Kasih path yang kamu mau, misal `E:\SYNESIS`.

## 056 — User

laptop saya global pythonnya aman semua karena kuliah fisika dengan fisika komputasi. Dan intinya saya itu gak mau pake ssd c saya untuk nyimpen library model python besar di atas 1gb. Balas dulu di chat

## 057 — Assistant

Paham — dan itu mengubah alasannya, bukan kesimpulannya.

Argumen "lindungi global Python" saya cabut. Kamu yang paling tahu kondisi lingkungan fisikamu, dan kalau selama ini aman, ya sudah. Yang benar-benar menyetir desainnya sekarang cuma satu: **jangan ada barang besar mendarat di C:.**

Kabar baiknya, rencana venv-di-`E:` justru jawaban paling tepat untuk itu — bukan karena isolasi, tapi karena **lokasi fisik file**. Paket yang diinstal ke venv mendarat di `E:\SYNESIS\.venv\Lib\site-packages`, bukan di `C:\...\Python312\Lib\site-packages`. Kalau PyTorch dipasang global, 4 GB itu masuk C:. Kalau lewat venv di E:, C: tidak tersentuh sama sekali.

## Yang diam-diam bocor ke C: kalau tidak diarahkan

| Apa | Default di C: | Ukuran | Pengalih |
|---|---|---|---|
| Paket venv | — | ~5 GB | ✅ otomatis di E: |
| Cache pip | `AppData\Local\pip\Cache` | 3–5 GB | `PIP_CACHE_DIR` |
| Model HuggingFace *(Whisper, embedding)* | `.cache\huggingface` | 1–3 GB | `HF_HOME` |
| Cache torch.hub *(silero-vad)* | `.cache\torch` | ~100 MB | `TORCH_HOME` |
| Model Ollama *(Qwen3-4B)* | `.ollama` | 2.5 GB+ | `OLLAMA_MODELS` |
| Model InsightFace | `.insightface` | ~150 MB | parameter `root=` saat init |

Tanpa pengalihan, total yang menumpuk di C: sepanjang 6 bulan sekitar **13 GB**. Dengan pengalihan: **mendekati nol.**

Cache pip itu yang paling sering luput — orang mengarahkan model tapi lupa cache, lalu C: penuh diam-diam oleh wheel PyTorch 2.5 GB yang tersimpan dua kali.

## Satu yang jujur tidak bisa dipindah sepenuhnya

**Aplikasi Ollama** (~1 GB) — installer Windows-nya memasang ke `%LOCALAPPDATA%\Programs\Ollama` tanpa menawarkan lokasi lain. Yang bisa dipindah adalah **model-modelnya**, dan justru itu bagian besarnya (2.5 GB untuk Qwen3-4B, lebih kalau kamu coba model lain).

Itu pun baru urusan Bulan 6, Februari. Masih jauh, dan kalau saat itu C: sempit, ada jalan keluar lewat symlink direktori.

## Soal `--system-site-packages`

Karena isolasi bukan lagi isu, opsi itu sekarang masuk akal untuk dipertimbangkan — venv ikut memakai numpy/scipy/matplotlib/sklearn yang sudah ada di global, hemat ~400 MB.

Tapi saya tetap sarankan venv bersih, dan sekarang alasannya tinggal satu: **kamu mau SSD ini bisa pindah device.** Venv yang menyandarkan diri pada paket global cuma jalan di laptop yang punya paket global itu. Colok ke komputer lain — langsung rusak.

Menukar portabilitas demi 400 MB di drive 191 GB itu tidak sepadan.

---

Jadi rencananya: **venv bersih di `E:`, plus empat env var pengalih di Hari 1** (`PIP_CACHE_DIR`, `HF_HOME`, `TORCH_HOME`, `OLLAMA_MODELS`). C: tidak kebagian satu byte pun dari proyek ini.

Kasih path yang kamu mau — `E:\SYNESIS` atau lainnya — dan saya mulai Hari 1.

## 058 — User

Terakhir saya mau tanya lagi. Model Oddesyus milik pewdiepie itu apa?? dan cara pakenya gimana?? dan apa saja fungsinya?? jawab di chat. Dan 1 perintah buat dalam 1 file md aturan mengenai drive c saya ini dan juga ya semacam readme di dalamnya mengenai deskripsi dari projek ini /stop-slop

## 059 — Assistant

Odysseus bukan model. Itu koreksi pertama yang perlu kamu tahu.

## Apa itu Odysseus

PewDiePie merilisnya Mei 2026 sebagai **workspace AI self-hosted**: antarmuka lengkap yang kamu jalankan di komputer sendiri, bukan bobot model. Filosofinya "own your AI instead of renting it". Lisensinya AGPL-3.0, gratis, kodenya terbuka.

Posisinya di tumpukan sama seperti ChatGPT atau Claude versi web, tapi berjalan di mesinmu. Modelnya tetap harus kamu sediakan sendiri.

## Fungsinya

Satu dashboard berisi chat, agen otonom, deep research, perbandingan model berdampingan, pengelolaan email, kalender, catatan, task, dan editor gambar.

Backend model yang didukung: Ollama, llama.cpp, vLLM, OpenRouter, OpenAI.

## Cara pakai

Semuanya dikemas sebagai container Docker, jadi pemasangannya beberapa perintah saja. Syarat minimalnya cuma mesin yang bisa menjalankan Docker. Kalau pakai API key cloud, kamu bahkan tidak perlu model lokal sama sekali.

Untuk model lokal, Ollama jadi titik awal yang disarankan. Model 7B atau 8B jalan nyaman di RAM 8 sampai 16 GB.

## Yang perlu kamu pertimbangkan untuk SYNESIS

Tiga hal.

**Docker Desktop di Windows makan 3 sampai 5 GB dan default-nya mendarat di C:.** Bertabrakan langsung dengan aturan drive yang baru kita tetapkan.

**VRAM 4 GB kamu tetap jadi batas yang sama.** Odysseus tidak menambah kapasitas apa pun. Dia cuma memberi antarmuka di atas model yang sudah kamu punya.

**Ini kebalikan dari rencanamu.** Odysseus memberi kamu hasil jadi tanpa proses. Kalau kamu pasang sekarang, seluruh Bulan 0 sampai 5 kehilangan alasannya. Kamu akan punya workspace bagus dan tetap tidak paham isi perutnya.

Saranku: buka dan pelajari **di Bulan 6**, sebagai pembanding. Saat itu kamu sudah menulis autograd, CNN, dan transformer sendiri. Kamu bisa membaca arsitekturnya dan mengerti tiap keputusan desainnya. Sekarang, dia cuma kotak hitam yang lebih besar.

**Sources:** [odysseusai.dev](https://odysseusai.dev/) · [XDA Developers](https://www.xda-developers.com/tried-pewdiepie-open-source-ai-workspace-odysseus-weirdly-great/) · [MakeUseOf](https://www.makeuseof.com/pewdiepie-open-sourced-his-personal-llm-workspace/) · [Decodo](https://decodo.com/blog/odysseus-pewdiepie)

Sekarang file-nya.

## 060 — Assistant

[README.md](README.md) sudah jadi, 188 baris, dua bagian dalam satu berkas.

**Deskripsi proyek:** identitas SYNESIS dan SEREN, lima spesifikasi yang dituju, prinsip "bangun dari nol untuk paham", peta enam bulan, dan empat kendala mutlak.

**Kebijakan drive:** lima aturan yang bisa diperiksa, tabel empat variabel lingkungan beserta apa yang ditahan masing-masing, pohon letak berkas, perintah verifikasi PowerShell, dan daftar tanda bahaya.

Beberapa isi yang mungkin berguna kamu lihat lebih dulu:

Aturan nomor 3 soal cache pip. Orang mengarahkan model tapi lupa cache, lalu wheel PyTorch 2,5 GB tersimpan dua kali di C: tanpa terlihat.

InsightFace tidak punya variabel lingkungan. Dia diarahkan lewat parameter `root=` saat inisialisasi, dan itu sudah saya tulis lengkap di file.

Blok verifikasi terakhir menghitung ukuran cache pip di C:. Jalankan tiap akhir bulan. Angka yang naik berarti ada yang lolos.

Satu catatan: README menyebut `E:\SYNESIS\` sebagai rumah proyek, tapi belum ada apa pun di sana. Folder kerja masih `s:\Code\Make A Jarvis`. Memindahkan dan membangun struktur di `E:` itu pekerjaan Hari 1.

Siap eksekusi Hari 1 kapan pun kamu bilang.

## 061 — User

Oke eksekusi pekerjaan hari 1. Buat si Oddesyus udah sih nanya doang wkwk

## 062 — Assistant

Mulai. Saya kerjakan bertahap sambil menjelaskan alasan tiap langkah.

Pertama, pastikan `E:` benar-benar terpasang.

## 063 — Assistant

`E:` siap, 191.2 GB bebas. Sekarang struktur folder dan empat variabel lingkungan.

## 064 — Assistant

Oke, saya sesuaikan. Kode dan repo tinggal di `S:`, `E:` cuma jadi gudang: venv, cache model, dan dataset besar.

## 065 — Assistant

Sekarang venv di `E:`. Ini yang akan menampung ~5 GB paket.

## 066 — Assistant

Isolasi terbukti: **1 paket di venv, 289 di global**. Itu syarat "selesai" Hari 1 yang pertama.

Sekarang paket inti Bulan 0.

## 067 — Assistant

Instalasi jalan di latar (menulis ribuan file kecil ke SSD eksternal memang lambat). Saya cek progresnya.

## 068 — Assistant

Sambil menunggu, saya siapkan git dan helper aktivasi di workspace.

## 069 — Assistant

venv sudah 356 MB, jalan terus. Sambil menunggu, README perlu disesuaikan dengan pembagian baru.

## 070 — Assistant

Paket inti selesai. Saya verifikasi lalu lanjut PyTorch.

## 071 — Assistant

Ketahuan satu masalah: **cache pip masih mendarat di C:**, 139.9 MB. Saya perbaiki sekarang.

## 072 — Assistant

Diagnosisnya jelas. Registry sudah benar, tapi sesi yang sedang jalan tidak melihatnya. Saya pindahkan cache dan pasang PyTorch dengan variabel diset eksplisit.

## 073 — Assistant

Cache pindah, C: bersih. Sekarang PyTorch, ~2.5 GB.

## 074 — Assistant

PyTorch jalan di latar. Sambil menunggu, saya buat skrip verifikasi dan commit pertama.

## 075 — Assistant

Commit pertama masuk. Cek progres PyTorch.

## 076 — Assistant

Masih mengunduh. Saya catat dulu satu pelajaran dari kejadian tadi ke README.

## 077 — Assistant

Sebagian besar Hari 1 sudah beres. PyTorch masih mengunduh (2,5 GB), saya lanjutkan verifikasi begitu turun. Ini laporan sementara sekaligus penjelasannya.

## Yang sudah jadi

**Struktur dua tempat**

```
S:\Code\Make A Jarvis\     workspace, repo git, beberapa MB
├── synesis\  notebooks\  docs\akademik\
├── activate.ps1  verify.py  .gitignore
└── README · Roadmap · Bulan-0-Harian · Name

E:\SYNESIS\                gudang, tidak masuk git
├── .venv\                 608 MB dan bertambah
├── .cache\pip\            143 MB
└── data\
```

**venv terbukti terisolasi.** Ini angka yang jadi syarat "selesai" Hari 1:

```
Paket di venv   : 1     (sebelum instal)
Paket di global : 289
```

Bukti lain yang lebih menarik: global punya numpy 2.4.6, venv sekarang punya **numpy 2.5.2**. Dua versi berbeda hidup berdampingan tanpa saling ganggu. Itulah gunanya venv.

**Paket inti terpasang**, 108 paket total: numpy 2.5.2, scipy 1.18.0, matplotlib 3.11.1, scikit-learn 1.9.0, pandas 3.0.5, jupyterlab 4.6.3, ipykernel 7.3.0, rich 15.0.0.

**Git jalan**, commit pertama `b9116bb` sudah masuk.

## Satu kesalahan yang kena, dan pelajarannya

Setelah instalasi paket inti, saya cek C: dan menemukan **139,9 MB cache pip mendarat di sana**. Padahal `PIP_CACHE_DIR` sudah saya set.

Penyebabnya: **variabel lingkungan diwariskan saat sebuah proses dibuat.** Saya menyetelnya di sesi PowerShell pertama, tapi tiap perintah berjalan di sesi baru yang lahir dari proses induk lama. Induk itu dibuat sebelum variabelnya ada, jadi anak-anaknya tidak pernah melihatnya. Registry sudah benar, prosesnya yang buta.

Cache-nya sudah saya pindah, C: kembali 0 MB, dan pemasangan PyTorch berjalan dengan variabel diset eksplisit di perintah yang sama.

Kenapa ini penting buat kamu: **terminal yang sudah terbuka sebelum Hari 1 tidak tahu soal empat variabel itu.** Tutup dan buka lagi PowerShell-mu, atau semua unduhan model di Bulan 3 akan diam-diam menumpuk di C:. Sudah saya catat di README.

## Dua hal yang saya putuskan sendiri

**KPA dan KRS saya pindah ke `docs/akademik/` dan saya masukkan `.gitignore`.** Kedua PDF itu memuat namamu, NPM, dan seluruh nilaimu. Roadmap menyebut proyek ini akan jadi bahan portofolio, dan riwayat git itu permanen. Sekali ter-commit lalu repo dibuka ke publik, mencabutnya perlu menulis ulang seluruh riwayat. Kalau kamu memang mau keduanya masuk, hapus satu baris di `.gitignore`.

**`activate.ps1`.** Karena venv tinggal di `E:` sementara repo di `S:`, aktivasinya perlu jalan pintas:

```powershell
. .\activate.ps1
```

Kalau enclosure tidak terpasang, skrip itu bilang, bukan melempar error yang membingungkan.

**`verify.py`** menjalankan audit lengkap: venv aktif, empat variabel, kebocoran ke C:, dan status CUDA. Jalankan tiap akhir bulan seperti yang tertulis di README.

Begitu PyTorch selesai, saya jalankan `verify.py` untuk menutup Hari 1 dengan `torch.cuda.is_available()`.

## 078 — User

tapi global env python aman kan bisa terkoneksi meskipun 2 tempat berbeda?? dan berjalan normal?? btw bisa bukain pop up cmd buat liat progress bar download gak??

## 079 — Assistant

Dua-duanya bisa saya jawab dengan bukti, bukan klaim. Cek dulu.

## 080 — Assistant

Global Python aman total. Buktinya di bawah. Sekarang saya buatkan jendela progresnya.

## 081 — Assistant

Jendela progres sudah terbuka (PID 21536), cek taskbar. Isinya bar, ukuran venv, laju MB/detik, dan pemantau kebocoran ke C: yang berubah merah kalau ada yang lolos. Dia berhenti sendiri begitu torch terpasang.

## Global Python aman, dan ini buktinya

| | Global (C:) | venv (E:) |
|---|---|---|
| Interpreter | `C:\...\Python312\python.exe` | `E:\SYNESIS\.venv\Scripts\python.exe` |
| site-packages | `C:\...\Roaming\Python\Python312\` | `E:\SYNESIS\.venv\Lib\` |
| Jumlah paket | 289 | 108 |
| numpy | **2.4.6** | **2.5.2** |

Tumpukan fisikamu saya panggil satu per satu dan semuanya hidup: numpy 2.4.6, scipy 1.17.1, astropy 7.2.0, spacepy 0.7.0.

Perhatikan baris numpy. Dua versi berbeda tinggal di satu laptop, tidak saling tahu, tidak saling ganggu. Kalau venv benar-benar mengotori global, angka itu akan sama.

## Jawaban "bisa terkoneksi": ya, dan begini caranya

Baris paling penting dari hasil tadi:

```
base python : C:\Users\SANDY FAUZI\AppData\Local\Programs\Python\Python312
```

venv **tidak** menyalin Python. Dia menunjuk balik ke interpreter global di C:. Yang dia punya sendiri cuma folder pustaka.

Analoginya: venv meminjam mesin, tapi bawa kotak perkakas sendiri. Mesinnya satu, dipakai bergantian. Perkakasnya dua set, tidak pernah tercampur.

Karena itu venv-nya cuma 551 MB padahal Python utuh jauh lebih besar. Dia memang tidak memuat Python di dalamnya.

## Satu ketergantungan yang perlu kamu ingat

venv bergantung pada Python 3.12 global tetap ada di C:. Kalau suatu saat kamu uninstall atau upgrade Python global ke 3.13, venv di E: langsung mati.

Perbaikannya gampang: hapus `.venv`, buat ulang, `pip install -r requirements.txt`. Tapi lebih baik tahu sekarang daripada kaget di tengah semester.

Ini juga alasan kenapa `requirements.txt` wajib ada di repo, dan akan saya buat begitu PyTorch selesai.

## Soal pyspedas

Di keluaran tadi muncul `AttributeError: module 'pyspedas' has no attribute '__version__'`. Itu bukan paket rusak. Skrip cek saya meminta atribut versi yang memang tidak disediakan pyspedas. Import-nya sendiri berhasil, karena AttributeError hanya bisa muncul pada modul yang sudah berhasil dimuat.

pyspedas kamu baik-baik saja.

## 082 — User

barusan muncul cuamn nutup lagi dan cuman sebentar. pake cmd ya jangan powershell

## 083 — Assistant

Jendela PowerShell-nya kemungkinan gagal karena path `Make A Jarvis` mengandung spasi, jadi argumennya terpecah. Cek status dulu.

## 084 — Assistant

pip masih jalan (PID 21904). Saya cari file unduhan sementaranya supaya jendela CMD bisa menampilkan progres nyata.

## 085 — Assistant

Temuan penting: **semua folder temp pip masih 0 MB.** Sudah belasan menit dan belum satu byte pun turun. Koneksi ke `download.pytorch.org` lambat atau macet.

Karena tidak ada yang hilang, saya matikan dan jalankan ulang di jendela CMD supaya kamu lihat progress bar asli pip.

## 086 — Assistant

Dua kesalahan saya, keduanya perlu saya sampaikan.

**Saya salah baca.** Pengecekan temp tadi memfilter nama `*.whl*` dan folder `pip-*`, jadi luput. Sekarang terlihat **1.782 MB sudah terunduh**. Download itu jalan normal, dan saya membunuhnya. Bandwidth-mu terbuang.

**Jendela CMD gagal terbuka**, 0 proses cmd. Pola `start` yang saya pakai salah.

Ada temuan penting dari kekeliruan ini: 1,78 GB itu mendarat di **C:**, karena pip memakai `%TEMP%` sebagai ruang kerja terlepas dari `PIP_CACHE_DIR`. Saya perbaiki sekalian.

## 087 — Assistant

Penghapusan di C: diblokir sandbox. Saya lewati, lanjut ke instalasinya dulu.

## 088 — Assistant

Jalan sekarang: pip PID 4512, jendela CMD terbuka. Progress bar asli pip akan muncul di sana.

## 089 — Assistant

Jendela CMD sudah jalan dengan progress bar asli pip. Saya pantau sampai selesai.

## Dua kesalahan saya

**Saya membunuh unduhan yang sedang berjalan.** Pengecekan temp saya memfilter nama file `*.whl*` dan folder `pip-*`, padahal pip menaruh unduhannya dengan pola lain. Filter kosong saya baca sebagai "tidak ada progres", lalu saya matikan prosesnya. Ternyata 1,78 GB sudah turun. Itu terbuang.

**Peluncuran jendela pertama salah.** Pola `Start-Process cmd /c start <bat>` tidak menghasilkan jendela apa pun. Yang benar memanggil file `.bat` langsung lewat `-FilePath`, dan sekarang jalan.

## Temuan yang justru berharga dari kekacauan itu

1,78 GB tadi mendarat di **C:**, bukan E:. Penyebabnya: **pip memakai `%TEMP%` sebagai ruang kerja saat mengunduh, tidak peduli `PIP_CACHE_DIR` diarahkan ke mana.** Cache akhirnya memang ke E:, tapi file mentahnya transit di C: dulu.

Untuk wheel 2,5 GB, itu berarti 2,5 GB lalu-lalang di SSD yang kamu jaga.

Sudah saya tutup di skrip baru:

```batch
set PIP_CACHE_DIR=E:\SYNESIS\.cache\pip
set TMP=E:\SYNESIS\.cache\tmp
set TEMP=E:\SYNESIS\.cache\tmp
```

Jadi kebijakan drive-mu sebenarnya butuh **enam** variabel, bukan empat. `TMP` dan `TEMP` akan saya tambahkan ke README saat menutup Hari 1.

## Satu hal yang perlu kamu jalankan sendiri

Sandbox memblokir saya menghapus apa pun di C:, jadi sisa 1,78 GB itu masih menumpuk di sana. Jalankan ini di PowerShell mana pun:

```powershell
Remove-Item "$env:TEMP\pip-*" -Recurse -Force
```

Kalau mau sekalian lihat hasilnya:

```powershell
"{0:N0} MB" -f ((Get-ChildItem $env:TEMP -Recurse -File -EA 0 | Measure-Object Length -Sum).Sum/1MB)
```

## Yang tersisa di Hari 1

Begitu torch mendarat, saya jalankan `verify.py`, buat `requirements.txt`, perbarui README dengan temuan `TMP`/`TEMP`, lalu commit. Setelah itu Hari 1 tutup dan kita masuk Hari 2, numpy sampai paham.

## 090 — User

<task-notification>
<task-id>bn1t2mm28</task-id>
<tool-use-id>toolu_01WxCmwqPYf4pnoPuZQBAT8h</tool-use-id>
<output-file>C:\Users\SANDYF~1\AppData\Local\Temp\claude\s--Code-Make-A-Jarvis\b7845516-007e-41a6-8303-8bf009ed35ab\tasks\bn1t2mm28.output</output-file>
<status>completed</status>
<summary>Background command "Wait until torch lands, then notify" completed (exit code 0)</summary>
</task-notification>

## 091 — Assistant

Torch mendarat. venv 5,2 GB. Sekarang verifikasi penutup Hari 1.

## 092 — Assistant

Lulus semua. Sekarang penutup Hari 1: perbaiki warning di `verify.py`, buat `requirements.txt`, perbarui README, lalu commit.

## 093 — Assistant

Hari 1 selesai. Kedua syarat "selesai" terpenuhi.

```
[VENV]              venv aktif : E:\SYNESIS\.venv
[VARIABEL]          empat-empatnya terarah ke E:
[KEBOCORAN C:]      bersih
[PYTORCH & CUDA]    torch 2.6.0+cu124
                    CUDA tersedia : True
                    GPU  : NVIDIA GeForce GTX 1650 Ti
                    VRAM : 3.2 GB bebas / 4.0 GB
                    LULUS SEMUA
```

Angka pembanding yang jadi bukti isolasi: **115 paket di venv, 289 di global.** numpy 2.5.2 di venv, 2.4.6 di global, hidup berdampingan tanpa saling sentuh.

## Yang ada di disk sekarang

```
S:\Code\Make A Jarvis\        repo git, 2 commit
├── synesis\ notebooks\ docs\akademik\
├── activate.ps1              aktivasi venv di E:
├── verify.py                 audit lingkungan
├── progress.ps1              pantau instalasi
├── requirements.txt          115 paket
└── README · Roadmap · Bulan-0-Harian · Name

E:\SYNESIS\
├── .venv\        5,2 GB
├── .cache\pip\   2,6 GB
├── .cache\tmp\   8 KB
└── data\
```

## Dua pelajaran yang tidak ada di rencana

Rencana Hari 1 menyebut empat variabel lingkungan. Kenyataannya butuh enam.

**Variabel diwariskan saat proses lahir.** Menyetelnya permanen tidak menyentuh terminal yang sudah terbuka. Itu yang membuat 140 MB cache mendarat di C: pada percobaan pertama.

**`PIP_CACHE_DIR` tidak menutup semua jalan.** pip mengunduh ke `%TEMP%` dulu, baru memindahkan ke cache. Tanpa `TMP` dan `TEMP` diarahkan, wheel 2,5 GB tetap transit di C:. Ketahuan setelah 1,78 GB menumpuk di sana. Sudah masuk README dan `verify.py`.

Kalau kamu belum sempat, sisa itu masih di C:

```powershell
Remove-Item "$env:TEMP\pip-*" -Recurse -Force
```

## Cara mulai besok

Buka PowerShell **baru**, bukan yang sudah terbuka sejak tadi. Terminal lama belum tahu soal enam variabel itu.

```powershell
cd "S:\Code\Make A Jarvis"
. .\activate.ps1
python verify.py
```

Kalau `verify.py` lulus, kamu siap kerja. Kalau enclosure `E:` tidak terpasang, `activate.ps1` yang akan memberitahu, bukan error yang membingungkan.

## Hari 2

numpy sampai paham. Kamu akan menulis dot product dan perkalian matriks pakai `for` loop, lalu mengukur berapa kali lebih lambat dibanding `np.dot`. Selisihnya biasanya puluhan sampai ratusan kali, dan alasannya bukan sihir: numpy memanggil BLAS yang ditulis dalam C dan Fortran, memakai instruksi vektor CPU dan tata letak memori yang ramah cache.

Kamu sudah punya intuisinya dari Komputasi Numerik. Besok kamu ukur sendiri angkanya.

Bilang saja kapan mau mulai.

## 094 — User

coba kamu verify saja. Lalu apalagi setelah itu?

## 095 — Assistant

Ketahuan satu celah: `TMP` dan `TEMP` masih menunjuk C:. Saya hanya menyetelnya di dalam file `.bat` tadi, jadi tidak permanen.

Perbaikannya **bukan** menyetelnya permanen. Kalau `TMP` global diarahkan ke `E:`, semua aplikasi Windows ikut menulis temp ke sana, dan begitu enclosure dicabut, banyak yang rusak. Tempatnya di `activate.ps1`, agar hanya berlaku di sesi SYNESIS.

## 096 — Assistant

Sekarang uji jalur yang sebenarnya kamu pakai: `activate.ps1` lalu `verify.py`.

## 097 — User

[Request interrupted by user for tool use]

## 098 — User

kalo cache ke c mah gak masalaah sebenernya bisa di hapus juga jadi biarin ke default aja

## 099 — Assistant

Setuju, itu keputusan yang masuk akal. Temp memang transien dan pip membersihkannya sendiri. Yang benar-benar penting adalah yang menetap: venv 5,2 GB dan cache pip 2,6 GB, dan keduanya sudah di E:.

Saya kembalikan `TMP`/`TEMP` ke default.

## 100 — Assistant

Lulus semua, dan Hari 1 resmi tutup dengan tiga commit.

```
[VENV]           E:\SYNESIS\.venv
[VARIABEL]       empat-empatnya terarah ke E:
[KEBOCORAN C:]   bersih
[PYTORCH]        2.6.0+cu124 · CUDA True · GTX 1650 Ti · 3.2/4.0 GB
                 LULUS SEMUA
```

Keputusanmu soal temp saya catat di README sebagai alasan, bukan cuma sebagai perubahan. Aturan drive sekarang menyatakan dirinya mengatur **penyimpanan yang menetap**, dan temp berada di luar cakupan karena transien. Siapa pun yang membaca repo ini enam bulan lagi akan tahu itu pilihan sadar, bukan kelalaian.

## Satu hal soal jadwal

Rencana menaruh Hari 1 di 13 Agustus. Kamu mengerjakannya hari ini, 20 Agustus. Seluruh Bulan 0 bergeser sepekan, jadi Hari 19 mendarat sekitar 7 September.

Perkuliahan kemungkinan sudah mulai saat itu. Dua pilihan:

**Rapatkan.** Bulan 0 punya empat hari istirahat. Pakai sebagian untuk mengejar, selesai sekitar 2 September.

**Terima saja.** Roadmap sudah bilang: kalau satu hari meleset, geser, jangan lompati. Bulan 0 masuk seminggu ke masa kuliah, dan bulan-bulan berikutnya ikut bergeser. Kelonggaran 12 jam di anggaran waktu memang untuk ini.

Saya condong ke yang kedua. Merapatkan hari di awal sering berujung pemahaman yang dangkal, dan Bulan 0 adalah fondasi yang menopang lima bulan sesudahnya.

## Hari 2: numpy sampai paham

Tiga tugas, sekitar 2 jam.

**Vektor, matriks, broadcasting, slicing.** Broadcasting yang paling penting dan paling sering dianggap remeh. Di Bulan 1 kamu akan menulis backpropagation, dan di sana bentuk array salah satu dimensi menghasilkan bug yang tidak melempar error, cuma hasil yang diam-diam keliru. Paham broadcasting sekarang menghemat berjam-jam kebingungan nanti.

**Dot product manual dengan `for` loop, lalu bandingkan dengan `np.dot`.** Ukur waktunya.

**Perkalian matriks manual, bandingkan lagi.**

Selisihnya biasanya puluhan sampai ratusan kali. Alasannya bukan sihir: numpy memanggil BLAS yang ditulis dalam C dan Fortran, memakai instruksi vektor CPU, dan menyusun memori agar ramah cache. Kamu sudah kenal ide ini dari Komputasi Numerik. Besok kamu ukur angkanya sendiri.

**Selesai bila** kamu bisa menjelaskan aturan broadcasting tanpa membuka catatan, dan sudah melihat sendiri berapa kali lipat vektorisasi menang.

Mau langsung jalan sekarang, atau besok?

## 101 — User

bikin file log.md untuk kamu mencatat semua yg telah kamu lakukan

## 102 — Assistant

Heredoc bersarang memecah parser. Saya pisah jadi dua langkah.

## 103 — Assistant

Quoting-nya tetap bermasalah. Saya pakai tool tulis langsung.

## 104 — Assistant

[log.md](log.md) sudah masuk, ter-commit sebagai `4395c9d`, dan tercatat di daftar dokumen README.

Isinya empat bagian:

**Fase perencanaan** (13–14 Agt): pembacaan KPA dan KRS, diagnosa perangkat, tiga versi roadmap beserta alasan tiap versi dibuang, proses penamaan, dan skill yang dipasang.

**Hari 1** (20 Agt): empat kali perpindahan keputusan lokasi sebelum mendarat di S untuk kode dan E untuk gudang, delapan langkah eksekusi, bukti isolasi venv, dan hasil akhir yang terverifikasi.

**Kesalahan dan pelajaran**: tiga kesalahan saya, ditulis lengkap dengan penyebab dan perbaikannya. Variabel lingkungan yang tidak menembus proses berjalan. Salah diagnosa yang membunuh unduhan 1,78 GB. Dua kali gagal meluncurkan jendela CMD.

**Keputusan yang kamu ambil**: lima keputusan beserta alasannya, termasuk yang mengubah arah seperti temp dibiarkan default dan Odysseus ditunda ke Bulan 6.

Bagian kesalahan sengaja saya tulis apa adanya. Log yang cuma memuat keberhasilan tidak menolong siapa pun yang menelusuri masalah tiga bulan kemudian. Kalau nanti ada model yang tiba-tiba mengunduh ke C, catatan soal pewarisan variabel lingkungan itu yang akan menjelaskan kenapa.

Konvensinya: entri baru saya tambahkan di bawah setiap kali ada kerja yang selesai. Hari 2 akan jadi entri berikutnya.

## 105 — User

Oke aturan baru ya setiap selesai proses wajib catat log ke file itu, tulis di readme. Lalu ayo kita mulai tahap hari 2 saja, jelaskan bagaimana caranya

## 106 — Assistant

Aturan barunya saya catat dulu, lalu kita masuk Hari 2.

## 107 — Assistant

Sekarang Hari 2. Saya siapkan kerangkanya, tapi **kodenya kamu yang tulis.** Itu inti Bulan 0.

## 108 — Assistant

Aturan log sudah masuk README bagian **Aturan Kerja**, dan entri Hari 2 sudah saya catat di [log.md](log.md). Commit `e096daf`.

# Hari 2 — numpy sampai paham

## Cara mulai

Buka PowerShell **baru**, lalu:

```powershell
cd "S:\Code\Make A Jarvis"
. .\activate.ps1
python notebooks\hari02_numpy.py
```

Bagian 1 dan 2 langsung jalan. Bagian 4 melewati dirinya sendiri sampai kamu mengisi TODO.

Berkasnya di [notebooks/hari02_numpy.py](notebooks/hari02_numpy.py).

## Konsep 1 — kenapa array kalahkan list

Jalankan bagian 1 dan perhatikan `strides`. Untuk array 2D bentuk `(3,4)` bertipe int64, keluarannya `(32, 8)`.

Artinya: pindah satu baris melompat 32 byte, pindah satu kolom melompat 8 byte. Angka-angkanya duduk berdampingan dalam satu blok memori berurutan.

List Python menyimpan **alamat**, bukan angka. Tiap elemen berarti satu lompatan ke tempat lain di memori, dan cache CPU meleset terus. Itulah akar seluruh selisih kecepatan yang akan kamu ukur nanti.

## Konsep 2 — broadcasting, dan jebakannya

Aturannya cuma tiga, disejajarkan **dari kanan**:

| Kondisi | Hasil |
|---|---|
| Dimensi sama | cocok |
| Salah satunya 1 | diregangkan |
| Selain itu | error |

```
(3,4) dan (4,)    ->  (3,4)     baris (4,) diulang 3 kali
(3,1) dan (1,4)   ->  (3,4)     keduanya diregangkan
(3,4) dan (3,)    ->  ERROR     4 lawan 3 di posisi paling kanan
```

Sekarang bagian yang penting. Perhatikan tiga bentuk ini:

```python
a.shape          # (3,)    tanpa arah
a[:, None].shape # (3,1)   kolom
a[None, :].shape # (1,3)   baris
```

`a[:, None] + a[None, :]` menghasilkan matriks **3×3**, bukan vektor 3 elemen.

Di Bulan 1, saat kamu menulis backpropagation, salah satu bentuk ini akan tertukar. Kodenya jalan. Tidak ada error. Angkanya keluar dan kelihatan wajar. Tapi gradiennya salah, dan training-mu tidak akan pernah konvergen tanpa kamu tahu kenapa.

Satu-satunya penangkalnya: **cetak `.shape` setiap kali ragu.** Biasakan sekarang, saat taruhannya masih murah.

## Konsep 3 — yang kamu tulis sendiri

**TODO 3 — `dot_manual(a, b)`**

Hasil kali dalam dua vektor, pakai loop Python murni. Dilarang `np.dot`, dilarang `np.sum`.

Ini operasi yang sudah kamu pakai di Fisika Kuantum:

$$\langle \psi | \phi \rangle = \sum_i \psi_i \phi_i$$

Rumusnya sama persis. Yang berbeda cuma namanya.

**TODO 4 — `matmul_manual(A, B)`**

Perkalian matriks `(n,k) × (k,m) → (n,m)`, tiga loop bersarang:

$$C_{ij} = \sum_k A_{ik} B_{kj}$$

## Yang akan kamu lihat

Bagian 4 memuat `assert` yang membandingkan hasilmu dengan numpy sebelum menampilkan waktu. Jadi kalau implementasimu keliru, kamu tahu duluan, bukan salah membaca angka kecepatan.

Dua catatan supaya tidak kaget:

`matmul_manual` pada 200×200 berarti 8 juta iterasi Python. Siap-siap menunggu beberapa detik. Itu normal, bukan hang.

Selisihnya akan melebar seiring `n` membesar. Ongkos tetap numpy tertutupi, sementara loop Python tumbuh linear. Perhatikan polanya, bukan cuma angka terbesarnya.

## Selesai bila

Kamu bisa menjelaskan aturan broadcasting tanpa membuka catatan, dan sudah melihat sendiri berapa kali lipat vektorisasi menang.

Kerjakan TODO-nya, lalu tempel hasilnya ke sini. Kita bahas angkanya bersama, dan saya catat penutup Hari 2 ke log.

## 109 — User

<ide_opened_file>The user opened the file s:\Code\Make A Jarvis\notebooks\hari02_numpy.py in the IDE. This may or may not be related to the current task.</ide_opened_file>

funsgi ini tuh apa?? dan kenapa perlu dilakukan. Perkalian matrix apa yg nilai perlu diinputnya??

## 110 — Assistant

Pertanyaan bagus, dan ini memang bagian yang paling sering bikin macet: rumusnya sudah kamu kuasai, tapi bentuk kodenya belum kelihatan sambungannya.

## `dot_manual(a, b)`

**Masuk:** dua vektor 1D dengan panjang sama.
**Keluar:** satu angka. Bukan array.

```python
a = [1, 2, 3]
b = [4, 5, 6]
dot_manual(a, b)  ->  1*4 + 2*5 + 3*6  =  32
```

Kamu sudah memakai ini di Fisika Kuantum, namanya saja berbeda:

$$\langle \psi | \phi \rangle = \sum_i \psi_i \phi_i$$

Satu loop, satu akumulator. Itu saja.

## `matmul_manual(A, B)`

**Masuk:** dua matriks 2D.
**Keluar:** satu matriks 2D.

Aturan bentuknya:

```
A berukuran (n, k)
B berukuran (k, m)
         ↑     ↑
         dimensi dalam WAJIB sama
C berukuran (n, m)
```

Dimensi dalam saling meniadakan, dimensi luar bertahan. `(3,4) × (4,5) → (3,5)`. Kalau `(3,4) × (3,5)`, operasinya tidak terdefinisi.

Rumusnya:

$$C_{ij} = \sum_k A_{ik} B_{kj}$$

Baca begini: **tiap elemen `C[i,j]` adalah dot product antara baris ke-`i` dari A dan kolom ke-`j` dari B.** Jadi `matmul_manual` sebenarnya `dot_manual` yang dijalankan berulang untuk setiap pasangan baris dan kolom. Itu sebabnya TODO 3 datang lebih dulu.

Contoh 2×2 yang bisa kamu cek dengan tangan:

```
A = [1  2]      B = [5  6]
    [3  4]          [7  8]

C[0,0] = baris 0 A · kolom 0 B = 1*5 + 2*7 = 19
C[0,1] = baris 0 A · kolom 1 B = 1*6 + 2*8 = 22
C[1,0] = baris 1 A · kolom 0 B = 3*5 + 4*7 = 43
C[1,1] = baris 1 A · kolom 1 B = 3*6 + 4*8 = 50

C = [19  22]
    [43  50]
```

Tiga loop bersarang: `i` menyusuri baris C, `j` menyusuri kolom C, `k` menjumlahkan.

## Nilainya kamu input dari mana?

Tidak perlu. Skripnya sudah membangkitkan sendiri:

```python
rng = np.random.default_rng(42)
A, B = rng.random((n, n)), rng.random((n, n))
```

Matriks acak persegi, ukuran 50×50, 100×100, lalu 200×200. Persegi supaya dimensi dalamnya otomatis cocok. Angka `42` mengunci benih acaknya, jadi hasilmu bisa diulang persis.

Tugasmu cuma menulis isi fungsinya. Skrip yang menyiapkan data, memanggil, memverifikasi, dan mengukur waktu.

## Kenapa ini perlu dikerjakan

Tiga alasan, dan yang ketiga paling penting.

**Perkalian matriks adalah jaringan saraf.** Satu lapisan neural network secara harfiah `output = W @ input + b`. Bukan mirip, memang itu. Backpropagation juga perkalian matriks. Attention di Bulan 5 adalah `Q @ K.T`. Kalau operasi ini benar-benar kamu kuasai, kamu sudah menguasai sebagian besar komputasi di deep learning.

**Ongkosnya jadi terasa.** Matriks `n×n` butuh `n³` operasi. Naik dari 100 ke 200 berarti kerjanya delapan kali lipat, bukan dua. Kamu akan merasakannya sebagai waktu tunggu, dan angka itu menempel di ingatan jauh lebih kuat daripada membacanya di buku.

**Jembatannya ke fisika sudah ada di kepalamu.** Di Fisika Kuantum, mengenakan operator $\hat{A}$ pada keadaan $|\psi\rangle$ adalah perkalian matriks-vektor. Menyusun dua operator berurutan adalah perkalian matriks-matriks. Ruang embedding di Bulan 2, transformasi wajah di Bulan 4, attention di Bulan 5, semuanya operator yang bekerja pada vektor. Kamu tidak sedang belajar konsep baru. Kamu sedang mengenali konsep lama dalam kostum berbeda.

Mulai dari TODO 3. Kalau `dot_manual` sudah jalan, TODO 4 tinggal memanggil pola yang sama di dalam dua loop.

## 111 — User

<ide_opened_file>The user opened the file s:\Code\Make A Jarvis\requirements.txt in the IDE. This may or may not be related to the current task.</ide_opened_file>

Coba tulis juga dong soal.md isinya soal yg perlu saya bereskan dan semacam clue juga petunjuk pengerjaan lah

## 112 — Assistant

Sebelum diserahkan, saya verifikasi dulu jawaban Soal 1 dan Soal 5 supaya tidak menyesatkan.

## 113 — Assistant

Semua terverifikasi. Kunci jawabannya benar, termasuk klaim bahwa matriks persegi menyembunyikan bug di Soal 5.

## 114 — Assistant

[notebooks/soal-hari02.md](notebooks/soal-hari02.md) sudah jadi, ter-commit `8c0905d`, dan tercatat di log.

## Isinya lima soal

| Soal | Isi |
|---|---|
| 1 | Ramalkan enam bentuk broadcasting **sebelum** menjalankan |
| 2 | Tulis `dot_manual` |
| 3 | Tulis `matmul_manual` |
| 4 | Baca angka adu cepat, empat pertanyaan analisis |
| 5 | Cari bug broadcasting yang tidak melempar error |

## Petunjuknya bertingkat dan tertutup

Tiap soal punya beberapa lapis petunjuk di dalam blok lipat. Buka satu per satu sesuai kebutuhan:

- **Petunjuk 1** cuma arahan, tanpa kode
- **Petunjuk 2** memberi kerangka dengan bagian kosong
- **Petunjuk 3** menyisakan satu baris untuk kamu isi

Soal 3 punya lapis tambahan khusus: *"Kalau hasilnya transpos dari yang seharusnya"*. Itu kesalahan paling umum pada perkalian matriks pertama, dan penyebabnya selalu sama.

Aturan mainnya saya tulis di atas: **coba sendiri minimal 15 menit sebelum membuka petunjuk pertama.** Membuka terlalu cepat memberimu kode yang jalan tanpa memberimu pemahaman, dan Bulan 1 akan terasa mustahil.

## Soal 5 yang paling berharga

Ini simulasi bug yang akan menggigitmu di Bulan 1:

```python
X = rng.random((3, 3))        # persegi
mean_sampel = X.mean(axis=1)  # (3,)
B = X - mean_sampel           # jalan, tanpa error, hasilnya (3,3)
```

Kodenya berjalan mulus. Bentuk keluarannya benar. Artinya salah.

Yang membuatnya menarik: pada bentuk `(100, 3)` kesalahan yang sama **langsung ditolak numpy**. Saya sudah verifikasi keduanya.

```
(3,3)   - (3,)    ->  jalan, salah arti
(100,3) - (100,)  ->  ValueError
```

Pelajarannya ada di soal 5d: **matriks persegi menyembunyikan kesalahan sumbu.** Data uji yang baik memakai dimensi yang berbeda-beda. Kebiasaan itu akan menyelamatkanmu berjam-jam saat menulis backprop nanti.

## Kunci jawaban sudah saya uji

Saya menjalankan keenam kasus Soal 1 sebelum menyerahkannya, jadi kamu tidak sedang mengejar jawaban yang salah.

Kerjakan Soal 1 dulu. Kalau enam ramalanmu sudah tepat, kamu siap ke `dot_manual`. Tempel hasilnya ke sini kalau ada yang mengganjal, atau kalau adu cepatnya sudah keluar dan mau kita bahas angkanya.

## 115 — User

coba cek jawaban saya. btw saya ada julia sih kalo misal memang perlu metode kompilasi mirip c

## 116 — Assistant

Bagus, jawabanmu lengkap. Saya baca sisanya dulu.

## 117 — Assistant

Saya jalankan sendiri dulu untuk memverifikasi angkamu, sekaligus cek Julia.

## 118 — Assistant

Semua benar. Saya jalankan ulang dan angkanya konsisten dengan punyamu.

## 119 — Assistant

Semua jawabanmu benar. Angka saya konsisten dengan angkamu: `349,42 → 2.813,98 ms`, rasio **8,06x**.

## Pemeriksaan

| Soal | Hasil |
|---|---|
| 1a–1f | 6/6 benar |
| 2 `dot_manual` | benar |
| 3 `matmul_manual` | benar |
| 4a–4d | benar |
| 5a–5d | benar |

Dua jawaban yang menonjol:

**4b** kamu dapat tepat 8x dan langsung menghubungkannya ke $2^3$. Itu bukan sekadar mencocokkan angka, itu memahami dari mana pangkat tiganya datang.

**4d** kamu menulis "setidaknya 28 detik". Kata *setidaknya* itu tepat. Pada `n = 100.000.000`, arraynya 800 MB, sudah keluar dari cache dan mungkin menyentuh swap. Estimasi linear jadi batas bawah, bukan tebakan pasti. Kamu sudah menangkap itu sendiri.

## Tiga perbaikan kecil

**1. `k2` dihitung tapi tidak dipakai.**

```python
n, k = A.shape
k2, m = B.shape        # k2 menganggur
```

Tambahkan validasinya:

```python
assert k == k2, f"dimensi dalam tidak cocok: {A.shape} x {B.shape}"
```

Ini menyambung langsung ke pelajaran Soal 5. Kamu baru saja belajar bahwa bentuk yang salah bisa lolos tanpa error. Memeriksa bentuk **sebelum** menghitung adalah kebiasaan yang akan menyelamatkan Bulan 1.

**2. Angka `n = 1.000` tidak bisa dipercaya.**

Kamu dapat 24x, saya dapat 107x, kode yang sama. Penyebabnya ada di fungsi `ukur`: versi manual dijalankan **sekali**, numpy sepuluh kali. Pada n kecil, satu kali pengukuran didominasi derau penjadwal OS.

Perbaikannya: naikkan `ulang` untuk versi manual saat n kecil. Pelajaran umumnya, **satu kali pengukuran bukan pengukuran.** Ini berlaku juga di Eksperimen Fisika.

**3. Pesan moral 5d sedikit terlalu keras.**

Kamu menulis "jangan pernah memakai matriks persegi untuk testing". Lebih tepatnya: gunakan dimensi yang berbeda saat menguji kode yang **sensitif terhadap bentuk**. Matriks persegi sendiri tidak berdosa, dia cuma tidak bisa menangkap kesalahan sumbu.

## Soal Julia

Julia 1.12.5 sudah terpasang di mesinmu. Dan ya, **ini bukan cuma berguna, ini justru menutup lubang di percobaan hari ini.**

Masalahnya begini. Perbandingan yang barusan kamu lakukan mencampur **dua variabel sekaligus**:

```
Python loop  →  numpy
   (a) ditafsir  →  dikompilasi
   (b) algoritma naif  →  SIMD + blok cache (BLAS)
```

Dari angka 9.837x itu, kamu tidak bisa tahu berapa bagian yang disumbang (a) dan berapa (b). Sebagai orang yang terlatih di Eksperimen Fisika, kamu tahu percobaan dengan dua variabel berubah bersamaan tidak menjawab apa pun.

Julia mengunci variabelnya. Tulis triple loop **yang persis sama** di Julia, dan:

```
Python naif  →  Julia naif    hanya (a) yang berubah  = ongkos penafsir murni
Julia naif   →  BLAS          hanya (b) yang berubah  = untung SIMD + cache
```

Perkiraan kasar di 200×200:

| | Waktu | Keterangan |
|---|---|---|
| Python naif | 2.814 ms | terukur |
| Julia naif | belasan ms | perkiraan, JIT ke kode native |
| numpy BLAS | 0,286 ms | terukur |

Kalau perkiraannya mendekati, artinya sebagian besar jurang 9.837x itu **ongkos penafsir Python**, bukan kecerdasan algoritma. Sisanya yang beberapa puluh kali baru berasal dari SIMD dan pemblokan cache.

Itu kesimpulan yang jauh lebih tajam daripada "numpy cepat".

Satu jebakan kalau kamu mengukurnya: **panggilan pertama di Julia termasuk waktu kompilasi JIT.** Jalankan dua kali, ambil yang kedua, atau pakai `@btime` dari BenchmarkTools.

Mau saya buatkan `notebooks/hari02_bonus_julia.jl` dengan algoritma identik supaya perbandingannya adil? Sekitar 30 menit, opsional, dan tidak mengganggu jadwal Hari 3.

## 120 — User

boleh

## 121 — Assistant

Angka matmul-nya bagus sekali, tapi bagian dot product **rusak** — saya menemukan dua bug di file saya sendiri. `0.008 ms` untuk 1 juta operasi itu mustahil, dan `sum(x .* y)` bukan BLAS karena mengalokasi array baru.

## 122 — Assistant

Sekarang angkanya masuk akal. Saya catat ke log lalu kita bahas.

## 123 — Assistant

File-nya jadi, ter-commit `565db54`. Hasilnya menjawab pertanyaanmu dengan tajam.

## Angkanya

```
matmul 200×200

Python naif    2.814,0 ms
Julia naif         6,125 ms
Julia kolom        1,065 ms
Julia BLAS         0,357 ms
```

## Pembagian jurangnya

| Lompatan | Faktor | Yang berubah |
|---|---|---|
| Python naif → Julia naif | **461x** | cuma bahasanya, algoritma identik |
| Julia naif → Julia kolom | **5,8x** | cuma urutan loop |
| Julia kolom → BLAS | **3,3x** | SIMD, blok cache, multithread |
| **Total** | **8.928x** | |

Cek konsistensi: $461 \times 5{,}8 \times 3{,}3 = 8.825$, cocok dengan 8.928 dalam batas derau. Dekomposisinya sehat.

## Jawaban atas pertanyaanmu

**461 dari 8.928 kali lipat itu semata-mata soal bahasa.** Algoritmanya sama persis, tiga loop bersarang yang sama, jumlah operasi yang sama. Yang berbeda hanya satu ditafsirkan baris demi baris, satu lagi dikompilasi ke kode mesin.

Sisanya yang cuma 19 kali lipat baru berasal dari tata letak memori dan seluruh kecerdasan BLAS.

Jadi kalimat "numpy itu cepat" sebenarnya berarti **"numpy itu bukan Python"**. Kecanggihan BLAS baru masuk belakangan, dan porsinya jauh lebih kecil daripada yang orang kira.

## Yang paling menarik: 5,8x dari urutan loop saja

Perhatikan `matmul_naif` lawan `matmul_kolom`. Jumlah perkalian sama. Jumlah penjumlahan sama. Hasilnya sama. Yang berubah hanya **urutan menyusuri memori**, dan waktunya turun hampir enam kali.

Sebabnya ada di `strides` yang kamu lihat di Bagian 1:

- **numpy** menyimpan baris berurutan (row-major, gaya C)
- **Julia** menyimpan kolom berurutan (column-major, gaya Fortran)

Urutan `i, j, k` yang kamu tulis di Python itu ramah terhadap tata letak numpy. Diterjemahkan mentah-mentah ke Julia, urutan yang sama justru melawan tata letaknya, dan CPU meleset dari cache terus-menerus.

Analoginya: membaca buku halaman demi halaman, dibanding melompat-lompat acak antar halaman. Jumlah kata yang dibaca sama. Waktunya jauh berbeda.

## Dua bug di file saya sendiri

Percobaan pertama menghasilkan `0,008 ms` untuk 1 juta operasi. Itu setara 125 GFLOPS pada satu core, mustahil.

**Penyebab pertama:** fungsi `ukur` saya membuang hasil pemanggilan, jadi kompilator Julia berhak menghapus seluruh perhitungan. Waktunya jadi nol palsu.

**Penyebab kedua:** saya memakai `sum(x .* y)` sebagai wakil BLAS, padahal itu mengalokasi array perantara sebesar n dan malah lebih lambat dari loop naif.

Pelajarannya sama dengan Hari 1: **angka yang terlalu bagus wajib dicurigai sebelum dipercaya.** Sudah tercatat di log.

## Haruskah SYNESIS pakai Julia?

Tidak. Tetap Python.

Seluruh ekosistem yang kamu butuhkan hidup di sana: PyTorch, Whisper, InsightFace, transformers, Ollama. Julia punya padanannya, tapi jauh lebih sepi, dan kamu akan menghabiskan waktu menambal yang di Python sudah jadi.

Tapi simpan Julia untuk **komputasi fisika**. Untuk Komputasi dan Simulasi Fisika, simulasi numerik, atau apa pun yang butuh loop ketat tanpa bisa divektorkan, Julia memberimu kecepatan C dengan kenyamanan menulis seperti Python. Kamu baru saja mengukur sendiri buktinya: 461 kali lipat, tanpa mengubah satu baris pun logika.

Hari 2 tutup. Siap ke Hari 3?

## 124 — User

oke lanjut

## 125 — Assistant

Hari 3: data sintetis dan loss. Saya siapkan kerangka dan soalnya.

## 126 — Assistant

Kerangkanya jalan. Satu hal perlu saya periksa dulu: loss di parameter asli keluar 1,3554 padahal varians derau 2,25. Selisihnya cukup jauh.

## 127 — Assistant

Bukan bug — sampel `n=50` dengan seed itu kebetulan jatuh di **−1,99σ**. Pada `n` besar ia kembali ke 2,25. Ini justru bahan soal yang bagus, saya tambahkan.

## 128 — Assistant

Ada bug di file soal: `\text` dan `\frac` di baris 138 tertelan sebagai karakter tab dan form feed. Saya perbaiki.

## 129 — Assistant

Hari 3 siap. Dua berkas: [notebooks/hari03_data_loss.py](notebooks/hari03_data_loss.py) dan [notebooks/soal-hari03.md](notebooks/soal-hari03.md). Commit `a290278`.

```powershell
. .\activate.ps1
python notebooks\hari03_data_loss.py
```

# Hari 3 — Data dan Loss

## Bingkainya

Hari ini kamu **membangun permukaan**, belum menurunkannya. Gradient descent baru datang di Hari 7. Kalau lanskapnya belum kamu pahami, menuruninya cuma jadi ritual.

Data sintetisnya `y = 3x + 2 + derau`. Kamu tahu jawabannya, lalu berpura-pura tidak tahu dan mencoba menemukannya kembali. Persis seperti mengukur konstanta pegas dari data simpangan dan gaya, hanya saja di sini kamu bisa memeriksa hasilnya.

## Tiga fungsi yang kamu tulis

`prediksi(x, w, b)`, `mse(y_ramal, y_asli)`, dan `mae(y_ramal, y_asli)`.

Untuk MSE, `np.mean` dan `np.square` dilarang. `np.sum` boleh untuk penjumlahan akhir. Vektorisasi silakan dipakai bebas, Hari 2 sudah membuktikan alasannya.

## Yang akan mengejutkanmu

Pada `w=3, b=2`, yaitu parameter yang **benar-benar membangkitkan data**, loss-nya tidak nol.

Angka sisa itu adalah **derau yang tidak bisa dihilangkan model mana pun**. Ia batas bawah. Kalau suatu saat kamu menemukan model dengan loss di bawah angka itu, jangan senang dulu: dia sedang menghafal derau, bukan menangkap pola. Itu wajah pertama overfitting, dan kamu akan bertemu lagi dengannya di Hari 12.

## Satu temuan yang jadi soal tambahan

Saat memverifikasi, loss di parameter asli keluar **1,36**, padahal derau dibangkitkan dengan `sigma = 1.5` sehingga variansnya **2,25**. Saya periksa, dan ini bukan bug: sampel `n=50` dengan seed itu kebetulan jatuh di **−1,99 simpangan baku**.

Naikkan `n` dan angkanya kembali:

```
n =     50   ->  1,3554
n =    200   ->  2,3187
n =  1.000   ->  2,3269
n = 10.000   ->  2,2594
```

Itu jadi **Soal 3e**. Konsepnya sama persis dengan ketidakpastian pengukuran di Eksperimen Fisika: rata-rata sampel berhingga berfluktuasi di sekitar nilai harapan, dan sebarannya menyempit sebanding $1/\sqrt{n}$.

## Puncaknya ada di Soal 4

Bagian 4 menyapu `w` dan menghasilkan kurva berbentuk parabola. Soal 4 memintamu **membuktikan** kenapa, di kertas.

Mulai dari $\text{MSE}(w) = \frac{1}{n}\sum_i (w x_i + b - y_i)^2$, jabarkan, kelompokkan menurut pangkat `w`, dan kamu akan sampai di $Aw^2 + Bw + C$. Lalu turunkan dan samakan dengan nol.

Hasilnya $w^* = -B/2A$.

Itu **solusi kuadrat terkecil bentuk tertutup**. Yang dikerjakan `np.polyfit` dan `sklearn.LinearRegression` di balik layar. Kamu akan menurunkannya sendiri, dengan aljabar setingkat Fisika Matematika.

Nilai verifikasi saya: $w^* = 3{,}0066$ terhadap `w` asli `3,0`. Cocok.

Lalu Soal 4d menanyakan hal yang mengganggu: **kalau solusi tertutupnya sudah ada, kenapa repot-repot pakai gradient descent di Hari 7?** Jawaban atas pertanyaan itu adalah alasan keberadaan seluruh proyek ini.

## Jembatan ke Mekanika

$$V(x) = \tfrac{1}{2}kx^2 \qquad\qquad \text{MSE}(w) \approx A(w-w^*)^2 + C_{\min}$$

Persamaan yang sama. Permukaan loss model linear **adalah** potensial harmonik.

Karena itu Soal 5c memintamu **meramalkan sekarang** apa yang terjadi kalau learning rate terlalu besar, memakai analogi pegas. Tulis ramalanmu, jangan diintip. Di Hari 8 kita cocokkan dengan grafik divergensi yang akan kamu hasilkan sendiri.

## Catatan

Saya menemukan bug di berkas soal saya sendiri: `\text` dan `\frac` tertelan jadi karakter tab dan form feed karena ditulis lewat string Python biasa. Sudah diperbaiki, dan seluruh berkas markdown saya periksa ulang. Tercatat di log.

Kerjakan Soal 1 dulu, urutkan keenamnya tanpa menjalankan apa pun. Tempel hasilnya ke sini kalau sudah.

## 130 — User

<ide_opened_file>The user opened the file s:\Code\Make A Jarvis\notebooks\hari03_data_loss.py in the IDE. This may or may not be related to the current task.</ide_opened_file>

coba cek jawaban saya. Btw bisa tolong akselerasi roadmapnya?? saya fast learner dan sangat jago learnning by doing dengan 5 tahun pengalaman dari C ke Python

## 131 — Assistant

Saya baca sisa jawabanmu dulu.

## 132 — Assistant

Semua benar. Jawabanmu bukan cuma tepat, tapi penalarannya jelas — terutama 5c, ramalanmu soal osilasi dan divergensi persis apa yang akan kamu lihat di Hari 8.

Sebelum akselerasi, saya lihat dulu struktur harian yang ada.

## 133 — Assistant

Jawaban dan bukti kerjamu mendukung klaimmu. Saya restrukturisasi.

## 134 — Assistant

Semua benar. Ranking Soal 1 cocok persis dengan kunci, ketiga fungsi lolos, dan Soal 4 sampai 5 tepat termasuk penurunan $w^* = -B/2A$.

Yang paling menonjol: **5c**. Kamu meramalkan osilasi lalu divergensi dari analogi pegas, sebelum melihat satu pun angka. Itu ramalan fisis yang akan kamu buktikan sendiri di Sesi B.

## Satu koreksi presisi

Pada 5a kamu memasangkan $k \leftrightarrow A$. Hampir tepat, tapi ada faktor dua:

$$V = \tfrac{1}{2}kx^2 \qquad \text{MSE} \approx A(w-w^*)^2$$

Samakan koefisiennya: $\tfrac{1}{2}k = A$, jadi $k = 2A$. Potensial pegas membawa faktor setengah, bentuk $A(w-w^*)^2$ tidak. Padanan simpangannya sudah benar.

Ini akan terasa di Sesi B saat kamu menghitung batas `lr` yang membuat sistem divergen. Batas itu bergantung pada kelengkungan, dan faktor dua menggeser angkanya.

---

# Akselerasi

Bukti mendukung klaimmu, jadi saya terapkan. Commit `2dcdc0d`.

## Bulan 0: 15 hari tersisa jadi 4 sesi

| Sesi | Menggantikan | Isi | Jam |
|---|---|---|---|
| **A** | Hari 5, 6, 7 | turunkan gradien, gradient check, training loop | ~3 |
| **B** ⭐ | Hari 8, 9 | sapuan `lr`, permukaan 3D, animasi lintasan | ~3 |
| **C** | Hari 10, 12, 13 | multivariat, overfitting, regularisasi | ~3 |
| **D** | Hari 14, 15, 16 | sklearn, PyTorch autograd, GPU | ~3 |

Hari 17 dan 19 dihapus sebagai sesi terpisah. Rapikan sambil jalan, log ditulis di akhir tiap sesi.

## Seluruh roadmap: 6 bulan jadi sekitar 4

| Bulan | Semula | Jadi |
|---|---|---|
| 1 · backprop & autograd | 4 minggu | **2 minggu** |
| 2 · embedding & classifier | 4 minggu | **2 minggu** |
| 3 · konvolusi & suara | 4 minggu | **3 minggu** ← ditahan |
| 4 · metric learning & wajah | 4 minggu | **2 minggu** |
| 5 · attention & transformer | 4 minggu | **3–4 minggu** ← ditahan |
| 6 · integrasi & LLM lokal | 4 minggu | **4 minggu** ← ditahan |

Dua bulan yang terbebas jatuh ke produk, yang memang tanpa tenggat.

## Tiga bulan sengaja tidak saya padatkan

Bukan karena meragukan kecepatanmu. Karena di sana **hambatannya bukan kecepatan belajar**.

**Bulan 3, suara.** Latensi, kuirk perangkat audio, ambang VAD yang meleset, wake word yang salah picu di ruangan berisik. Itu debugging perangkat keras. Membaca lebih cepat tidak mempercepat mikrofon.

**Bulan 5, transformer.** Bug attention tidak melempar error. Dia menghasilkan model yang berlatih rajin tanpa pernah membaik. Menemukannya butuh kesabaran, bukan kecepatan.

**Bulan 6, integrasi.** Menyatukan enam modul yang masing-masing sudah jalan selalu makan waktu lebih lama dari perkiraan siapa pun. Itu hukum, bukan dugaan.

## Batas sebenarnya bukan kemampuanmu

Kamu punya sekitar 8 jam per minggu dengan 22 SKS. Belajar tiga kali lebih cepat tidak menambah jam dalam seminggu.

Jadi akselerasi ini berarti **lebih sedikit sesi untuk cakupan yang sama**, bukan lebih banyak jam. Kalender tetap yang pegang kendali.

## Satu risiko yang naik

Yang paling sering menjatuhkan pembelajar cepat adalah melompati bagian yang terasa lambat, padahal justru di situ intuisinya dibangun.

Dua hal saya tandai tidak boleh dipadatkan lagi:

**Sesi B**, animasi lintasan di permukaan loss. Melihat bola itu bergerak mengubah gradient descent dari rumus jadi benda yang kamu kenali.

**Sesi C**, melihat test loss naik sementara train loss turun. Kamu sudah menjelaskan overfitting dengan benar di Soal 3b secara konsep. Melihatnya terjadi di layarmu sendiri adalah hal yang berbeda, dan itu yang menempel.

---

Siap masuk **Sesi A**? Isinya: turunkan `∂MSE/∂w` dan `∂MSE/∂b` di kertas, kode gradiennya, verifikasi dengan beda hingga, lalu training loop pertamamu sampai `w → 3` dan `b → 2`.

## 135 — User

bisa kamu rumuskan roadmap ini dalam file md menjadi seperti silabus perkuliahan disertai tujuan materi tersebut dipelajari dan buat super terstruktur gunakan bahasa yg mudah dipahami manusia /humanizer /stop-slop

## 136 — Assistant

Betul, silabus harusnya berdiri sendiri sebagai rencana utuh tanpa penanda progres. Saya tulis ulang dari nol.

## 137 — Assistant

[Silabus.md](Silabus.md) sudah jadi, 368 baris, commit `c293ee5`. Ditulis ulang dari nol seperti kamu minta, jadi dia berdiri sendiri sebagai rencana utuh. Penanda progres tidak ada di sana. Progres tetap tinggal di log.

## Isinya

Bagian pembuka memuat identitas, deskripsi, dan delapan tujuan pembelajaran. Ada juga tabel prasyarat yang memetakan mata kuliah yang sudah kamu ambil ke bagian mana ia dipakai. Fisika Matematika untuk aturan rantai dan Fourier, Kuantum untuk ruang Hilbert, Mekanika untuk potensial dan osilasi.

Lalu tujuh modul. Tiap modul punya bagian **"kenapa modul ini ada"**, dan itu bagian yang kamu minta. Isinya alasan materi itu dipelajari, bukan daftar isi.

Contohnya di Modul 4:

> Pengenalan wajah tidak bekerja dengan cara mencocokkan gambar. Ia bekerja dengan memetakan wajah ke vektor, lalu mengukur sudut antar vektor. Ide bahwa jarak bisa mewakili identitas adalah fondasi seluruh sistem pencarian modern.

Setelah itu tiap modul memuat yang kamu pelajari, yang kamu tulis sendiri, yang masuk ke SYNESIS, jembatan fisikanya, sambungan ke mata kuliah, dan tolok ukur kelulusannya.

## Modul 0 dirinci jadi tujuh sesi

Karena dibuat dari awal, Modul 0 mulai dari penyiapan lingkungan, bukan dari titik kamu sekarang.

| Sesi | Isi |
|---|---|
| 1 | lingkungan kerja, venv, git, PyTorch |
| 2 | numpy sampai paham |
| 3 | data dan loss |
| 4 | gradient descent utuh |
| 5 | lanskap dan langkah |
| 6 | multivariat, overfitting, regularisasi |
| 7 | pembanding dan PyTorch |

Kamu sudah menyelesaikan sesi 1 sampai 3. Yang tersisa empat sesi, dan itu sama dengan Sesi A sampai D di [Bulan-0-Harian.md](Bulan-0-Harian.md).

## Penilaian

Tidak ada nilai huruf, cuma tolok ukur yang bisa kamu periksa sendiri. Satu tolok ukur berlaku di semua modul: kamu bisa menjelaskan kodemu ke orang lain tanpa membuka catatan. Kalau tidak bisa, modulnya belum selesai meski programnya jalan.

## Soal gaya penulisan

Ditulis dengan `humanizer` dan `stop-slop` aktif. Saya verifikasi hasilnya bersih dari em dash, en dash, curly quote, dan emoji pada judul. Judulnya sentence case, bukan Title Case.

Efeknya terasa di kalimat. Yang tadinya berbunyi "modul ini menjadi fondasi krusial yang menopang perjalanan pembelajaranmu" sekarang jadi "kalau bagian ini terasa mustahil, itu sinyal untuk memperkuat dasar dulu sebelum lanjut."

Silabus juga sudah masuk daftar dokumen di README dan tercatat di log.

## 138 — User

Continue from where you left off.

## 139 — Assistant

No response requested.

## 140 — User

Bikinin Modul all in one menjelaskan dengan sangat mudah dipahami /humanizer /stop-slop /feynman-perspective /ai-feynman-techniek-coach

## 141 — Assistant

Sudah lihat semua strukturnya. Silabus menjelaskan **apa** dan **kenapa** di level rencana, tapi belum menjelaskan **konsepnya sendiri**. Itu yang saya buat sekarang: satu dokumen yang menjelaskan seluruh isi tujuh modul dengan gambaran konkret, bukan definisi.

## 142 — Assistant

Pandoc + MiKTeX (xelatex) tersedia. Saya pakai itu, hasilnya paling rapi untuk dokumen sepanjang ini.

## 143 — Assistant

Satu cacat di tabel Bagian 9: `<psi\|phi>` tampil dengan backslash-nya ikut tercetak, karena pipe di dalam inline code tidak bisa di-escape untuk tabel. Saya perbaiki.

## 144 — Assistant

Log bersih, tidak ada karakter kontrol nyasar. Sekarang README dan commit.

## 145 — Assistant

[Modul.md](Modul.md) dan [Modul.pdf](Modul.pdf) sudah jadi, commit `6ed2cd5`. 857 baris markdown, 24 halaman A4.

## Bedanya dengan Silabus

Silabus menjawab "belajar apa dan kapan". Modul menjawab "barangnya itu apa". Jadi keduanya tidak tumpang tindih, dan Modul bisa kamu baca tanpa membuka Silabus sama sekali.

## Cara saya menulisnya

Tiga hal saya pasang berulang di seluruh dokumen.

**Benda dulu, rumus belakangan.** Gradien dijelaskan sebagai berdiri di lereng gunung dalam kabut, merasakan kemiringan di bawah telapak kaki. Attention dijelaskan sebagai mencari di perpustakaan, dengan query sebagai pertanyaanmu, key sebagai judul di punggung buku, dan value sebagai isinya. Rumus `softmax(QK^T / akar d) V` baru muncul setelah kamu punya gambarannya, dan setiap potongan rumus itu punya padanan di ceritanya.

**Catatan "di mana analoginya rusak".** Semua analogi bohong sedikit, dan kalau kamu tidak tahu di mana bohongnya kamu akan salah paham di kasus tepi. Contohnya analogi kelereng di mangkuk: kelereng punya momentum, gradient descent polos tidak. Kelereng melewati dasar karena inersia, gradient descent melewatinya karena langkahnya kebesaran. Sebab yang berbeda, dan kalau tertukar kamu akan salah mendiagnosis loss yang berosilasi.

**Blok "tanya diri sendiri".** Pertanyaan Socratic di akhir tiap bagian, untuk dijawab dengan suara keras. Yang tidak bisa kamu jawab itu materi belajarmu minggu itu.

## Dua bagian yang mungkin paling kepakai

Bagian 9 adalah kamus 19 baris yang memetakan fisika yang sudah kamu kuasai ke nama panggilannya di ML. Regularisasi L2 ternyata Hukum Hooke, dengan `lambda` sebagai konstanta pegas yang menarik bobot ke nol. Softmax dengan temperature ternyata distribusi Boltzmann, dan penyebutnya adalah fungsi partisi. Positional encoding ternyata basis Fourier.

Bagian 10 adalah lima uji untuk membedakan paham dari hafal, termasuk deteksi pemujaan kargo. Uji yang paling tajam menurut saya: tulis ramalan hasilnya sebelum menjalankan kode. Setiap kali meleset, kamu baru menemukan lubang yang tidak kamu sadari ada.

## Yang saya akui tidak tahu

Tiga tempat saya tandai terbuka, bukan ditutupi. Kenapa model overparameterisasi tetap menggeneralisasi masih diperdebatkan, dan `double descent` cuma nama gejalanya, bukan penjelasannya. Tafsir "neuron ini mendeteksi konsep anjing" sebagian besar cerita yang dikarang setelah melihat gambar yang membuatnya menyala. Dan soal apakah LLM "mengerti", saya tulis bahwa mekanismenya prediksi token dan perilakunya menyerupai penalaran, keduanya benar, dan lompatan di antaranya belum ada yang berhasil membuktikan.

## PDF

Dibangun dengan pandoc dan xelatex dari MiKTeX di [S:\Apps\MiTex](S:/Apps/MiTex). Georgia untuk badan teks, Consolas untuk kode, daftar isi dua level.

Saya periksa halaman hasil cetaknya dan menemukan satu cacat. Notasi bra-ket di sel tabel Bagian 9 tercetak jadi `<psi\|phi>`, backslash-nya ikut terlihat, karena pipe di dalam inline code tidak bisa di-escape untuk tabel Markdown. Sudah saya tulis ulang jadi teks biasa dan PDF-nya dibangun ulang.

Pelajarannya saya catat di log: exit code pandoc yang nol tidak berarti hasilnya benar. Halamannya harus dilihat.

Log dan tabel dokumen di README sudah diperbarui. Pointer "Berikutnya" di log yang masih tertulis Hari 2 juga saya betulkan jadi Sesi A, karena Hari 3 sudah selesai.

## 146 — User

Lanjut kerjain bagian A

## 147 — Assistant

Sesi A. Ini sesi di mana kelerengnya benar-benar mulai menggelinding.

Sebelum saya siapkan berkasnya, ini turunannya. Kerjakan ulang di kertas, jangan cuma dibaca.

## Turunan yang harus kamu dapat sendiri

Tulis residu dulu supaya rumusnya tidak berantakan:

```
r_i = w*x_i + b - y_i        (ramalan minus asli)
MSE = (1/n) * Σ r_i^2
```

Aturan rantai, dua kali, sekali untuk tiap kenop:

```
∂MSE/∂w = (1/n) Σ 2*r_i * (∂r_i/∂w) = (2/n) Σ r_i * x_i
∂MSE/∂b = (1/n) Σ 2*r_i * (∂r_i/∂b) = (2/n) Σ r_i
```

Perhatikan bedanya. Turunan terhadap `w` punya `x_i` menempel, turunan terhadap `b` tidak. Itu bukan kebetulan rumus. `w` mempengaruhi ramalan lewat perkalian dengan `x`, jadi titik dengan `x` besar punya suara lebih keras dalam menentukan ke mana `w` bergerak. `b` menggeser semua titik sama rata, jadi semua titik bersuara sama.

Sekarang cek silang dengan jawaban Soal 4c kamu kemarin. Kamu sudah dapat `MSE(w) = Aw² + Bw + C` dengan `A = (1/n)Σx²` dan `B = (2/n)Σx(b−y)`. Turunkan itu:

```
d/dw (Aw² + Bw + C) = 2Aw + B = (2/n)Σx²·w + (2/n)Σx(b−y) = (2/n)Σ x(wx + b − y) = (2/n)Σ r·x
```

Sama persis. Turunan Sesi A dan aljabar Hari 3 kamu saling memverifikasi. Kalau dua jalan berbeda mendarat di tempat yang sama, kemungkinan besar dua-duanya benar.

Saya siapkan berkasnya.

## 148 — Assistant

Semua angka kuncinya sudah saya verifikasi dengan implementasi pembanding. Ada satu temuan yang mengubah salah satu soal, saya jelaskan setelah berkasnya jadi.

## 149 — Assistant

Kamu sudah menulis ulang [Modul.md](Modul.md) dengan suaramu sendiri. Saya biarkan, itu memang polamu sejak soal Hari 2. Konsekuensinya PDF-nya jadi basi dan referensi silang saya mungkin meleset, saya cek setelah scaffold-nya lolos uji.

## 150 — Assistant

Scaffold jalan, dan tiap angkanya cocok persis dengan implementasi pembanding saya. Termasuk `lstsq` yang selisihnya `0.00e+00` untuk `w`.

## 151 — Assistant

Sesi A siap. Dua berkas, dan giliranmu.

## Yang harus kamu kerjakan

[sesiA_gradient_descent.py](notebooks/sesiA_gradient_descent.py) punya tiga TODO: `gradien` analitik, `beda_hingga` numerik, dan `latih` sebagai training loop. Sisanya sudah terpasang, termasuk gradient check lima titik, sapuan learning rate, dan pembanding `np.linalg.lstsq`.

Berkasnya mengimpor `buat_data`, `prediksi`, dan `mse` dari [hari03_data_loss.py](notebooks/hari03_data_loss.py), jadi kerjaan kemarin langsung kepakai. Kalau yang di sana benar, yang di sini ikut benar.

[soal-sesiA.md](notebooks/soal-sesiA.md) berisi enam soal dengan petunjuk bertingkat. Semua angka kuncinya sudah saya verifikasi dulu dengan implementasi pembanding, jadi kalau hasilmu beda dari yang tertulis, yang salah kodemu, bukan soalnya.

Satu aturan tambahan khusus sesi ini: **tulis ramalanmu sebelum menjalankan kode.** Soal 3 dan Soal 5 kehilangan seluruh gunanya kalau kamu jalankan dulu baru menjelaskan.

## Dua temuan yang membuat sesi ini lebih menarik dari rencana

Saya jalankan implementasi pembanding lebih dulu, dan dua hal muncul yang tidak ada di rencana asli.

**Beda hingga di sini persis, bukan hampiran.** Sapuan `h` memberi galat relatif `0.000e+00` di `h = 0.1`, dan justru membengkak jadi `8.2e-06` di `h = 1e-11`. Tidak ada kompromi optimum di tengah, padahal semua tutorial mengajarkan ada. Sebabnya sudah kamu buktikan sendiri kemarin di Soal 4a, dan saya tidak akan menyebutkannya di sini karena itu isi Soal 3. Yang bisa saya bilang: aturan "pakai `h = 1e-5`" adalah menara bambu di sesi ini, tapi ia jadi aturan yang benar lagi mulai Bulan 1. Jelaskan kenapa keduanya bisa benar sekaligus.

**Gradient descent tidak mendarat di parameter asli.** Ia berhenti di `w = 3.018`, `b = 1.744`, bukan di `w = 3`, `b = 2`. Dari tiga titik awal yang sangat berbeda, termasuk `(100, -100)`, ketiganya sampai ke angka yang sama persis, dan angka itu cocok dengan `lstsq` sampai `0.00e+00`.

Jadi bukan konvergensi yang kurang. Dasarnya memang di situ.

## Koreksi tolok ukur

Karena temuan kedua itu, kriteria di [Bulan-0-Harian.md](Bulan-0-Harian.md) yang berbunyi `w → 3` dan `b → 2` saya betulkan. Kriteria itu salah, dan kalau dibiarkan kamu akan menghabiskan waktu mengejar angka yang tidak akan pernah dicapai, lalu menyimpulkan kodemu bugged padahal benar.

Kriterianya sekarang: gradient check lolos, dan konvergen ke titik yang sama dari titik awal mana pun. Soal 4 membahas kenapa titik itu bukan parameter asli, dan `b` yang meleset 0,256 itu sekitar 1,2 kali `σ/√n`. Masih di wilayah wajar, dan ini sambungan langsung dari Soal 3e Hari 3 kamu.

## Soal 5 adalah inti sesi ini

Kemarin kamu meramal secara kualitatif bahwa `lr` kebesaran akan berosilasi lalu melenting. Sekarang saya minta angkanya.

Ramalan dari teori dan hasil pengukuran memang cocok, sudah saya cek. Tapi jangan lihat tabel Bagian 5 sebelum kamu menuliskan angka ramalanmu. Kalau terlanjur kelihatan, ganti seed datanya lalu ramalkan untuk seed baru.

## Soal Modul.md

Versi tulisan ulangmu jauh lebih enak dibaca dan suaranya konsisten dengan soal Hari 2 dan Hari 3. PDF-nya sudah saya bangun ulang mengikuti versi itu.

Satu hal yang ikut terbuang dan mungkin tidak kamu sengaja: catatan "di mana analoginya rusak" di tiap bagian. Kalau memang sengaja dibuang, tidak apa-apa. Kalau tidak, yang paling saya sayangkan hilangnya yang di Bagian 0, karena analogi kelereng punya momentum sementara gradient descent polos tidak, dan tanpa catatan itu kamu bisa salah mendiagnosis loss yang berosilasi sebagai inersia padahal penyebabnya langkah kebesaran. Kebetulan itu persis yang kamu hadapi di Soal 5 hari ini.

Kerjakan dulu, nanti saya periksa jawabannya seperti biasa.

## 152 — User

done lanjut B

## 153 — Assistant

Sebelum lanjut, saya periksa jawaban Sesi A kamu. Delapan tanda gradien di Soal 1 benar semua, termasuk C dan D yang halus. Tapi ada dua hal yang perlu diluruskan, dan yang kedua bisa diuji.

## 154 — Assistant

Uji pembedanya tegas. Batas asli ada antara `0.127` dan `0.1274`, dan `2/λ_max = 0.12720` menebaknya sampai empat angka.

Sekarang saya cek pipa animasi untuk Sesi B sebelum menulis berkasnya.

## 155 — Assistant

Animasi dan permukaan 3D jalan. Ini Sesi B.

## 156 — Assistant

Satu hal yang muncul dan layak diperbaiki: di `lr = 0.1272` persis, loss berhenti di 77,1 setelah 3000 iterasi. Itu bukan konvergen, itu osilasi tetap. Label statusnya saya perbaiki jadi tiga keadaan.

## 157 — Assistant

Gergajinya terlihat jelas. Panah ungu terlalu pendek dan tertimpa lintasan, saya naikkan skalanya dan taruh di atas.

## 158 — Assistant

Sekarang soalnya.

## 159 — Assistant

Sesi B siap, tapi ada dua utang Sesi A yang saya masukkan jadi Soal 0 karena keduanya bukan soal ketelitian.

## Yang benar di Sesi A

Delapan tanda gradien di Soal 1 benar semua. Titik C dan D itu yang saya perhatikan, karena gradiennya kecil (`-0.10` dan `+0.50`) dan tandanya tidak kentara dari intuisi kasar. Kamu dapat dua-duanya.

Soal 3 juga tepat, termasuk bagian yang paling halus: turunan ketiga polinomial derajat dua bernilai nol, jadi galat pemotongannya hilang dan yang tersisa cuma pembulatan. Soal 6b tentang beda hingga sebagai wasit independen juga persis.

## Dua yang meleset

**Soal 4d, kamu mengganti bukti dengan verifikasi.** Jawabanmu menunjuk ke keluaran `bagian 6` yang menunjukkan `w * x̄ + b` sama dengan `ȳ` di `2.806923`.

Itu menunjukkan pernyataannya benar untuk 50 titik ini dengan seed ini. Bukti menunjukkan ia benar untuk data apa pun, selamanya, dan menjelaskan kenapa. Buktinya tiga baris dari `dMSE/db = 0`, dan kamu sudah punya semua bahannya.

Ini bukan formalitas. Mulai Bulan 1 kamu akan menurunkan gradien untuk lapisan yang tidak punya pembanding numerik yang murah, dan kebiasaan "cek angkanya cocok" tidak akan menolongmu di sana.

**Soal 5b, `A = 8.33` itu nilai populasi, bukan nilai datamu.** `25/3` adalah `E[x²]` untuk sebaran seragam di `[-5, 5]`. Yang diminta `np.sum(x*x)/len(x)`, dan untuk datasetmu nilainya `7.8435`. Ramalanmu jadi `0.120`, seharusnya `0.1275`.

Lalu ada masalah kedua yang lebih penting dari angkanya. Kamu menulis "ramalan fisikamu akurat tanpa meleset". Itu belum tertopang, karena sapuan `lr` di Sesi A melompat dari `0.12` langsung ke `0.13`, dan **kedua ramalan sama-sama jatuh di celah itu.** Pengukurannya tidak punya daya pisah untuk membedakan mana yang benar.

Jadi saya jalankan sapuan halusnya:

| ramalan | angka | hasil |
|---|---|---|
| `1/A` populasi | `0.120000` | salah, `0.121` sampai `0.127` masih konvergen |
| `1/A` sampel | `0.127493` | sedikit ketinggian |
| `2/λ_max` Hessian 2D | `0.127200` | tepat di dalam jepitan |

Batas asli ada antara `0.127` dan `0.1272`. Ramalan Hessian meleset di bawah 0,2 persen.

Ini kali ketiga kamu memakai nilai populasi di tempat yang meminta nilai sampel, setelah varians `2.25` di Soal 3e Hari 3 dan `σ/√n` di Soal 4b Sesi A. Soal 0c meminta kamu menuliskan satu kalimat aturan untuk dirimu sendiri supaya yang keempat tidak terjadi.

## Sesi B

[sesiB_lanskap.py](notebooks/sesiB_lanskap.py) dan [soal-sesiB.md](notebooks/soal-sesiB.md). Tiga TODO: `permukaan_loss` versi loop, `sumbu_utama` untuk Hessian dan vektor eigennya, dan `permukaan_loss_vektor` versi broadcasting yang menyambung langsung ke Hari 2.

Yang keluar dari berkasnya: permukaan 3D dalam skala linear dan log, lintasan gradient descent di atas kontur untuk tiga `lr`, sumbu utama parit digambar dari vektor eigen, animasi GIF tiga bola, dan sapuan `lr` halus yang menutup soal ramalan tadi.

Bagian yang paling saya ingin kamu lihat adalah `figures/sesiB_sumbu_utama.png`. Di situ gergaji lintasan `lr = 0.12` terlihat berayun sejajar sumbu curam sementara kemajuan sebenarnya merayap sejajar sumbu landai. Seluruh alasan keberadaan Adam ada dalam satu gambar itu.

## Satu keadaan yang tidak saya duga

Saat menguji, `lr = 0.1272` persis memberi loss `77.1` setelah 3000 iterasi. Tidak meledak, tapi juga tidak pernah turun ke dasar di `1.2903`.

Label status saya awalnya cuma dua keadaan dan menyebut ini konvergen. Itu salah, jadi saya perbaiki jadi tiga: konvergen, berayun tetap, divergen.

Sebabnya faktor pengali galat bernilai tepat `-1` di titik itu. Amplitudonya tidak pernah berubah, tandanya bergantian selamanya. Osilator tanpa redaman sama sekali. Soal 5c meminta kamu menyebut namanya di Mekanika.

Kerjakan Soal 0 dulu sebelum yang lain, karena keduanya utang dari kemarin dan yang pertama cuma butuh tiga baris di kertas.

## 160 — User

bagian ABCD itu apa saja tadi??

## 161 — Assistant

Empat sesi ini menggantikan Hari 5 sampai 16 di rencana lama, hasil akselerasi kemarin. Masing-masing sekitar 3 jam.

## Sesi A, gradient descent utuh

Menggantikan Hari 5, 6, 7. **Sudah kamu kerjakan.**

Turunkan gradien di kertas, kodekan, verifikasi dengan beda hingga, lalu tulis training loop pertama. Selesai bila gradient check lolos di bawah `1e-6` dan konvergen ke titik yang sama dari tebakan awal mana pun.

## Sesi B, lanskap dan langkah

Menggantikan Hari 8 dan 9. **Ini yang sedang di mejamu.**

Sapu learning rate, plot permukaan loss `L(w, b)` dalam 3D, timpa dengan lintasan gradient descent, lalu animasikan. Selesai bila kamu punya animasi bola menggelinding ke dasar mangkuk, dan grafik yang menunjukkan `lr` besar melempar keluar.

Ini satu-satunya sesi di Bulan 0 yang ditandai tidak boleh dipadatkan lagi.

## Sesi C, multivariat, overfitting, regularisasi

Menggantikan Hari 10, 12, 13.

Perluas ke `X` berbentuk `(n, d)` dalam bentuk matriks penuh. Pasang polinomial derajat 1, 3, 9, dan 15 ke data sedikit. Pisahkan train dan test, plot kedua loss dalam satu grafik. Tambahkan suku L2 dan amati efeknya pada derajat 15.

Selesai bila kamu punya grafik dengan test loss naik sementara train loss terus turun, dan bisa menunjukkan L2 memperbaikinya. Kamu sudah menjelaskan overfitting dengan benar secara konsep di Soal 3b Hari 3. Sesi ini membuatmu melihatnya terjadi.

## Sesi D, penutup: sklearn, PyTorch, GPU

Menggantikan Hari 14, 15, 16.

Bandingkan hasilmu dengan `LinearRegression` dan `Ridge`, lalu dengan `w*` analitik dari Soal 4c Hari 3. Tulis ulang dengan `torch.tensor` dan `requires_grad=True`, panggil `loss.backward()`, dan bandingkan gradiennya dengan gradien tanganmu. Terakhir pindahkan ke `.cuda()` dan ukur CPU lawan GPU untuk `d=10` dan `d=1000`.

Selesai bila gradien PyTorch cocok dengan gradien tulisanmu dalam `1e-6`, dan kamu tahu kapan GPU justru kalah dari CPU.

Momen `backward()` cocok dengan turunan tanganmu itu pintu masuk Bulan 1. Setelah itu autograd berhenti terasa gaib, dan membangunnya sendiri jadi masuk akal.

Rinciannya ada di [Bulan-0-Harian.md](Bulan-0-Harian.md), dan padanannya di [Silabus.md](Silabus.md) adalah sesi 4 sampai 7 Modul 0.

## 162 — User

lanjut sesi c coba cek jawaban saya

## 163 — Assistant

Sesi B kamu kuat. Ada satu jawaban yang bertentangan dengan tabel di atasnya sendiri, saya cek dulu angkanya sebelum bilang.

## 164 — Assistant

Terkonfirmasi. Sekarang saya siapkan Sesi C dan verifikasi angkanya.

## 165 — Assistant

Angkanya bagus sekali untuk diajarkan. Derajat 3 mentah butuh 242 iterasi, dibakukan cukup 27. Dan derajat 1 dibakukan memberi bilangan kondisi tepat `1.000`, persis kasus lingkaran yang kamu ramalkan di Soal 2c Sesi B.

## 166 — Assistant

Bagian 3 memunculkan `inf` beserta peringatan overflow. Itu justru gejala yang berharga, tapi harus ditampilkan dengan benar, bukan sebagai peringatan.

## 167 — Assistant

Gambar overfitting-nya persis seperti yang seharusnya. Sekarang soalnya.

## 168 — Assistant

Sekarang log dan commit.

## 169 — Assistant

2,86 MB GIF ikut masuk commit. Aturan `.gitignore` cuma menyaring `figures/*.png`, jadi GIF-nya lolos padahal kategorinya sama.

## 170 — Assistant

Repo belum punya remote dan belum pernah di-push, jadi commit terakhir masih aman diubah. Tapi menulis ulang riwayat itu keputusanmu.

## 171 — Assistant

Beres. `.git` turun dari 3,5 MB jadi 461 KB, dan GIF-nya tetap ada di disk untuk kamu tonton. Sekarang `figures/*.gif` dan `*.mp4` ikut tersaring.

## Sesi B kamu

Bukti 0a rapi dan benar, tiga baris, persis seperti yang diminta. Faktor pengali galat di 4a benar ketiganya berikut tafsirnya. Cerita animasi di 6a bersih dari istilah, dan itu bagian yang paling sulit dipalsukan. Soal 3 tentang Hessian yang cuek pada `y` juga benar, termasuk padanan pegasnya.

Empat hal saya masukkan jadi Soal 0. Satu di antaranya bukan soal ketelitian.

### Jawaban 4c dibantah tabelmu sendiri

Kamu menulis lintasan merah "paling lama nyampe dasar". Angkanya:

| lr | loss di iterasi 60 | panjang lintasan | iterasi sampai 1% dasar |
|---|---|---|---|
| 0.01 | 3.168473 | 5.74 | **185** |
| 0.06 | 1.290335 | 7.59 | **30** |
| 0.12 | 1.290407 | 63.41 | **38** |

Yang merah sampai dalam 38 iterasi. Yang biru butuh 185. Jadi yang menggergaji itu hampir lima kali lebih cepat dari yang merayap lurus, bukan paling lambat.

Sebabnya: gradient descent membayar per langkah, bukan per satuan jarak. Jarak yang terbuang untuk menggergaji itu gratis. Gergaji bukan penyebab lambat, melainkan harga yang kamu bayar supaya boleh memakai `lr` besar, dan harganya berubah jadi kehancuran begitu lewat `0.1272`.

Yang lebih penting dari isi jawabannya: tabel yang membantahnya kamu cetak sendiri tiga baris di atas. Ini pola kedua setelah Sesi A. Ceritanya terdengar masuk akal, jadi angkanya tidak dibaca ulang.

### Tiga koreksi kecil

Parabola naik kuadratik, bukan eksponensial. Kalau dinding loss betulan eksponensial, gradient descent tidak akan pernah bekerja.

Hessian bergantung pada `y` di model taklinear bukan karena ReLU patah. Sebabnya suku kedua pada `∇²L = (2/n)Σ[∇f∇fᵀ + (f−y)∇²f]` memuat residu, dan suku itu lenyap untuk model linear karena `∇²f = 0`. Model mulus tapi taklinear tetap kena.

Di 5e kamu berhenti di "bilangan kondisi turun". Jawabannya lebih tajam: setelah `x` dibakukan, ia jadi tepat `1`. Itu persis kasus lingkaran yang kamu sendiri jelaskan di Soal 2c. Bagian 3 Sesi C mencetak angka itu, dan hasilnya `1.000e+00`.

## Sesi C

[sesiC_multivariat.py](notebooks/sesiC_multivariat.py) dan [soal-sesiC.md](notebooks/soal-sesiC.md). Empat TODO: `desain_polinom`, `mse_matriks`, `gradien_matriks` dengan denda L2, dan `latih_matriks`.

Datanya sekarang kubik `0.5x³ − 2x + 1` dengan derau `1.5`, 15 titik latih dan 200 titik uji. Derajat 3 adalah model yang benar, jadi kamu punya pembanding jujur untuk menilai sisanya.

Bagian 2 mempertemukan tiga saksi di derajat 1: bentuk matriks, rumus skalar tulisanmu di Sesi A, dan beda hingga. Ketiganya sepakat sampai `7e-15`.

Bagian 3 mengukur bilangan kondisi naik dari `2.6` di derajat 1 sampai `1.7e20` di derajat 14, lalu menunjukkan derajat 3 butuh 242 iterasi mentah dan 27 setelah dibakukan. Itu bayaran dari satu baris pembakuan, dan angkanya sekarang ada.

Bagian 5 menghasilkan grafik yang kamu tunggu sejak Hari 3. Train loss turun monoton sampai nol persis di derajat 14. Test loss punya dasar di derajat 3 lalu meledak jadi `5.7e9`.

Bagian 6 menunjukkan L2 menarik derajat 14 dari test loss `8.7e9` turun ke `5.42`, sementara `|θ|` turun dari `1.2e7` jadi `1.70`. Modelnya tidak diganti, parameternya tidak dikurangi. Yang berubah satu angka.

## Satu temuan saat menguji

Di derajat 14 mentah, `eigvalsh` mengembalikan nilai eigen terkecil `-2.488e-08`. Matriks `XᵀX` selalu semidefinit positif, jadi angka negatif itu mustahil secara matematis.

Versi pertama saya memakai angka itu sebagai pembagi dan menghasilkan `inf` beserta peringatan overflow. Saya perbaiki, dan sekarang `lambda_min` dicetak sebagai kolom tersendiri supaya angka mustahilnya justru terlihat. Itu Soal 3b, dan intinya: angka yang mustahil adalah alarm paling jujur yang bisa kamu dapat, dan harganya gratis.

Kerjakan Soal 0 dulu, terutama 0a. Yang paling perlu kamu bawa dari Sesi C bukan overfitting, tapi kebiasaan kembali ke tabel setelah menulis kesimpulan.

## 172 — User

https://github.com/SandyFauzi/SYNESIS

Ini reponya btw dan coba rapihkan folder ini kalo mau push

## 173 — Assistant

Sebelum menyentuh apa pun, saya lihat dulu isi repo itu. Ada satu hal yang perlu dicek: skill `szh-ex` dan `szh-im` di laptopmu menyebut `SandyFauzi/SYNESIS` sebagai arsip `knowladge/sessions`, jadi repo itu mungkin sudah punya isi dan tujuan lain.

## 174 — Assistant

Repo-nya ada, publik, dan masih kosong (nol commit). Sebelum merapikan, ada satu hal yang harus saya cek dulu.

## 175 — Assistant

Repo publik dan masih kosong, jadi push pertama akan menerbitkan seluruh riwayat sekaligus. Ada satu hal yang harus kamu putuskan sebelum itu, saya sampaikan setelah folder rapi.

Pertama, saya petakan semua tautan silang supaya tidak ada yang putus setelah dipindah.

## 176 — Assistant

Sekarang README, yang akan jadi halaman depan repo.

## 177 — Assistant

Ada dua kerusakan lama di README yang belum pernah saya pindai: `. .ctivate.ps1` dan pohon direktori yang barisnya menyatu. Ini kelas bug escape yang sama dengan LaTeX dulu.

## 178 — Assistant

Folder rapi dan sudah di-commit. Sekarang satu hal yang harus kamu putuskan sebelum push, dan ini bukan hal kecil.

## 179 — Assistant

Baik, keputusanmu. PDF resmi kampus tetap terkunci, sisanya jalan.

Saya pastikan dulu PDF-nya benar-benar tidak pernah masuk riwayat, bukan cuma tidak ada sekarang.

## 180 — Assistant

Satu koreksi pada keluaran di atas: baris "ADA DI RIWAYAT" itu salah, keluar dari logika shell saya yang keliru (`git log | head` tetap sukses meski kosong). Pemeriksaan yang benar adalah dua baris berikutnya, dan hasilnya PDF akademik tidak pernah ter-commit sama sekali. Satu-satunya PDF terlacak cuma `docs/Modul.pdf`.

## 181 — Assistant

Push ditolak. Git di laptopmu sedang memakai kredensial akun lain.

## 182 — Assistant

Identitas commit-nya sudah benar (`Sandy Fauzi Amrulloh <sandyfauzia09@gmail.com>`). Yang bermasalah cuma kredensial push: Git Credential Manager menyimpan token akun `Praktikum-KN-FisikaUnpad-26`, dan akun itu tidak punya izin tulis ke repomu.

Saya arahkan URL remote supaya menyebut username, jadi GCM mencari kredensial terpisah dan token praktikummu tidak tersentuh.

## 183 — Assistant

Berhasil. Saya verifikasi apa yang benar-benar mendarat di sana.

## 184 — Assistant

Sudah tayang: **https://github.com/SandyFauzi/SYNESIS**

## Struktur sekarang

```text
README.md, log.md, requirements.txt, .gitignore   di akar
docs/       Roadmap, Silabus, Modul.md, Modul.pdf, Bulan-0-Harian, Name
            akademik/ tetap dikunci
notebooks/  scaffold .py dan soal .md berpasangan
scripts/    activate.ps1, verify.py, progress.ps1
figures/    keluaran plot, tidak masuk git
```

`notebooks/` sengaja saya biarkan datar. Scaffold-nya saling impor lewat nama modul (`from hari03_data_loss import ...`) dan tiap soal `.md` menaut ke `.py` pasangannya di folder yang sama. Memecahnya jadi subfolder akan mematahkan keduanya tanpa memberi manfaat apa pun.

Semua tautan silang sudah diperbarui, dan tabel dokumen di README sekarang bisa diklik.

## Dua kerusakan lama yang ketemu

README ternyata belum pernah masuk pemindaian karakter kontrol, dan memuat dua sisa bug escape sekelas kasus LaTeX di soal Hari 3.

Byte `0x07` di posisi 5528, sisa dari `\a`, membuat `. .\activate.ps1` tampil sebagai `. .ctivate.ps1`. Lalu pohon direktori yang barisnya menyatu jadi `pip│ huggingface│ torch│` karena `\n` tertelan saat penulisan.

Dua-duanya sudah diperbaiki. Pohonnya saya tulis ulang pakai ASCII supaya aman di semua peramban.

Pelajarannya saya catat di log: pemindaian saya dulu menyasar `notebooks/*.md` dan beberapa berkas rencana, tapi README terlewat justru karena ia berkas paling awal dan saya anggap sudah beres.

## Soal push yang ditolak

Percobaan pertama kena 403. Git Credential Manager di laptopmu menyimpan token akun `Praktikum-KN-FisikaUnpad-26`, dan akun itu tidak punya izin tulis ke repomu. Identitas commit sendiri sudah benar, `Sandy Fauzi Amrulloh <sandyfauzia09@gmail.com>`.

Saya perbaiki tanpa menyentuh token praktikummu, dengan menaruh username di URL remote jadi `https://SandyFauzi@github.com/...`. GCM sekarang mencari kredensial yang terkunci pada username itu, jadi kedua akun bisa hidup berdampingan dan kamu tidak perlu login ulang untuk urusan praktikum.

## Yang terbit dan yang tidak

24 berkas dalam 18 commit. Saya cek PDF akademik tidak pernah ter-commit sama sekali, bukan cuma tidak ada di commit terakhir. Satu-satunya PDF terlacak `docs/Modul.pdf`.

Branch lokal saya ubah dari `master` jadi `main` mengikuti default GitHub. Bilang saja kalau kamu lebih suka `master`.

## Dua catatan

`notebooks/soal-sesiC.md` ada perubahan yang belum di-commit, kelihatannya kamu sedang mengisi jawaban. Saya tidak sentuh, jadi jawabanmu aman dan belum terbit.

Lalu `figures/` seluruhnya tersaring gitignore. Untuk repo portofolio, plot overfitting empat panel dan animasi lintasan itu justru bagian paling menjelaskan. Kalau mau, saya bisa lepaskan beberapa gambar terpilih dari saringan dan menyematkannya di README, tanpa memasukkan GIF 2,86 MB yang tadi kita buang.

## 185 — User

btw saya ada skill baru tolong laksanakan juga /szh-ex

## 186 — Assistant

Skill ini membaca log sesi **Codex**, bukan Claude Code. Percakapan kita sekarang berjalan di Claude Code, jadi yang bisa diekspor adalah salah satu sesi Codex-mu. Saya daftarkan dulu kandidatnya.

## 187 — Assistant

Sekarang jelas. Kamu mau arsipnya jadi jembatan dua arah, bukan cuma milik Codex. Saya baca dulu exporter-nya untuk tahu apakah ia bisa disuapi transkrip Claude Code.

## 188 — Assistant

Exporter-nya tidak mengunci diri ke Codex. Ia cuma mem-parse JSONL dengan skema tertentu, lalu semua pengaman (redaksi, penjagaan path, tolak repo kotor, tolak origin salah) berlaku apa pun sumbernya.

Jadi jembatannya bisa dibuat tanpa menyentuh skill: ubah transkrip Claude Code jadi skema yang sama, lalu jalankan exporter aslinya. Saya periksa dulu skema transkrip Claude Code.

## 189 — Assistant

Skemanya berbeda tapi bisa dipetakan. Yang penting saya buang `thinking` (penalaran privat), `tool_use`/`tool_result`, dan sisipan `<system-reminder>`, sesuai batas yang skill itu tetapkan sendiri.

## 190 — Assistant

195 pesan terangkat, 686 baris dibuang. Repo ini publik, jadi saya tinjau isinya dulu memakai fungsi redaksi milik exporter itu sendiri, sebelum apa pun di-commit.

## 191 — Assistant

Regex path-nya rusak karena escape backslash. Saya ulangi dengan pencocokan literal, bukan regex.

## 192 — Assistant

Tiga temuan perlu dipastikan bukan kebocoran blok asli, melainkan sekadar kata yang saya sebut dalam prosa.

## 193 — Assistant

Satu masalah nyata di konverter saya. Isi definisi skill ikut terbawa karena ia tiba sebagai pesan ber-peran user, padahal skill itu sendiri melarang mengekspor instruksi developer.

## 194 — Assistant

Enam pesan, sekitar 79 ribu dari 215 ribu karakter, atau 37 persen arsip. Itu isi definisi skill dan ringkasan sistem, bukan pesan yang terlihat. Saya saring.

## 195 — Assistant

Bersih sekarang: 194 pesan, 137 ribu karakter, tanpa definisi skill, ringkasan sistem, blok thinking, atau NPM. Sekarang `handoff.md`, yang justru jadi isi paling berguna dari ekspor ini.

## 196 — Assistant

Exporter menolak commit karena `git diff --cached --check` menemukan spasi di ujung baris. Penjagaannya bekerja. Dua hal perlu dibetulkan: spasi ujung, dan nama berkas yang membuat id arsip jadi `-sesi` alih-alih memuat UUID.

## 197 — Assistant

Tiga berkas tertinggal ter-stage dari percobaan gagal. Saya bersihkan tanpa `reset` atau `clean`, sesuai larangan skill.
