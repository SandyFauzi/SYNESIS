# Silabus: membangun SYNESIS dari nol

## Identitas

| | |
|---|---|
| Nama | Membangun AI Personal dari Nol |
| Peserta | Sandy Fauzi Amrulloh, Fisika UNPAD, NPM 140310240054 |
| Periode | Agustus 2026 sampai Desember 2026 |
| Beban | 7 modul, sekitar 120 jam |
| Ritme | 6 sampai 10 jam per minggu |
| Biaya | Rp 0 |
| Prasyarat | Fisika Matematika I sampai III, Komputasi Numerik, pemrograman Python |

Dokumen pendamping: [Roadmap.md](Roadmap.md) untuk rencana besar, [Bulan-0-Harian.md](Bulan-0-Harian.md) untuk rencana harian, [log.md](../log.md) untuk catatan kerja.

---

## Deskripsi

Kamu belajar cara kerja machine learning dengan menulis sendiri algoritma intinya sebelum memakai pustaka mana pun. Backpropagation kamu turunkan dan kode dari kosong. Konvolusi kamu implementasikan manual. Transformer kamu bangun lapis demi lapis.

Setiap modul menghasilkan satu komponen yang benar-benar dipasang ke SYNESIS, asisten AI yang berjalan penuh di laptopmu tanpa internet dan tanpa biaya. Jadi tidak ada latihan yang berakhir di folder sampah.

Materinya berjalan beriringan dengan empat mata kuliah Semester 5 yang kamu ambil. Teori masuk dari kelas, praktik masuk dari sini.

---

## Tujuan pembelajaran

Setelah menyelesaikan seluruh modul, kamu bisa:

1. Menjelaskan cara kerja gradient descent dan membuktikan kenapa ia konvergen, tanpa membuka catatan.
2. Membangun mesin diferensiasi otomatis dari kosong, lalu memakainya melatih jaringan saraf.
3. Melatih classifier dari data yang kamu kumpulkan dan beri label sendiri, lalu memasangnya ke sistem yang berjalan.
4. Mengubah sinyal suara jadi representasi yang bisa dipelajari mesin, dan melatih model pengenal kata dari nol.
5. Menjelaskan kenapa jarak antar vektor bisa mewakili identitas, dan mengkalibrasi ambangnya dengan kurva ROC.
6. Membangun arsitektur transformer utuh dan melatihnya di GPU 4 GB.
7. Merangkai enam modul jadi satu sistem yang menyala berjam-jam tanpa crash.
8. Menerjemahkan konsep machine learning ke padanan fisikanya, dan sebaliknya.

---

## Prasyarat yang sudah kamu penuhi

Kamu masuk dengan bekal yang lebih kuat dari kebanyakan orang yang mulai belajar ML.

| Bekal | Dipakai di |
|---|---|
| Fisika Matematika I sampai III (A-, A, A) | aljabar linear, aturan rantai, Fourier, konvolusi |
| Komputasi Numerik dan praktikumnya | metode iteratif, konvergensi, gradient check |
| Komputasi dan Simulasi Fisika (A) | Monte Carlo, penyelesaian numerik |
| Fisika Kuantum (A-) | ruang Hilbert, hasil kali dalam, proyeksi |
| Mekanika (A-) | prinsip variasional, potensial, osilasi |
| Termodinamika (A-) | entropi, distribusi Boltzmann |
| Pemrograman, 5 tahun C dan Python | seluruh implementasi |

---

## Struktur

| Modul | Topik | Durasi | Keluaran |
|---|---|---|---|
| 0 | Fondasi dan gradient descent | 7 sesi | intuisi lanskap loss |
| 1 | Backpropagation dan jaringan saraf | 2 minggu | mesin autograd buatanmu |
| 2 | Representasi dan klasifikasi | 2 minggu | SYNESIS v0.1 |
| 3 | Sinyal, konvolusi, dan suara | 3 minggu | SYNESIS v0.2 |
| 4 | Metric learning dan visi | 2 minggu | SYNESIS v0.3 |
| 5 | Attention dan transformer | 3 sampai 4 minggu | mini-GPT buatanmu |
| 6 | Integrasi dan LLM lokal | 4 minggu | SYNESIS v1.0 |

---

## Modul 0. Fondasi dan gradient descent

**Durasi:** 7 sesi, sekitar 21 jam

### Kenapa modul ini ada

Semua pelatihan model, dari regresi linear sampai GPT, mengerjakan hal yang sama: mencari titik terendah pada sebuah permukaan. Kalau kamu paham betul cara satu titik bergerak menuruni permukaan itu, semua yang datang setelahnya hanyalah permukaan yang lebih berdimensi.

Modul ini juga jadi gerbang. Kalau bagian ini terasa mustahil, itu sinyal untuk memperkuat dasar dulu sebelum lanjut.

### Rincian sesi

**Sesi 1. Lingkungan kerja.** Struktur repo, virtual environment terpisah, git, dan pemasangan PyTorch dengan CUDA. Kamu memisahkan lingkungan proyek dari Python global supaya tumpukan riset fisikamu aman, dan mengarahkan seluruh berkas besar ke drive terpisah.

**Sesi 2. numpy sampai paham.** Vektor, matriks, broadcasting, slicing, dan tata letak memori. Kamu menulis dot product dan perkalian matriks dengan loop Python, lalu mengadu kecepatannya melawan numpy. Selisihnya ratusan sampai ribuan kali, dan kamu akan tahu persis dari mana selisih itu datang.

**Sesi 3. Data dan loss.** Membangkitkan data sintetis berderau, menulis fungsi MSE dan MAE tanpa pustaka, lalu memetakan loss untuk berbagai tebakan parameter. Kamu membuktikan secara aljabar bahwa permukaan loss model linear selalu berbentuk parabola, lalu menurunkan solusi kuadrat terkecil bentuk tertutup.

**Sesi 4. Gradient descent utuh.** Menurunkan gradien di kertas, mengodekannya, memverifikasinya dengan beda hingga, lalu menulis training loop pertama sampai parameternya konvergen ke nilai asli.

**Sesi 5. Lanskap dan langkah.** Menyapu learning rate dari yang terlalu kecil sampai yang membuat sistem divergen. Memplot permukaan loss dalam 3D dan menganimasikan lintasan gradient descent di atasnya.

**Sesi 6. Multivariat, overfitting, regularisasi.** Memperluas ke banyak fitur dalam bentuk matriks penuh. Memasang polinomial berderajat tinggi ke data sedikit, lalu melihat sendiri test loss naik sementara train loss terus turun. Menambahkan suku L2 dan mengamati efeknya.

**Sesi 7. Pembanding dan PyTorch.** Membandingkan hasilmu dengan scikit-learn dan dengan solusi analitik. Menulis ulang dengan PyTorch, lalu membandingkan gradien dari `loss.backward()` dengan gradien turunan tanganmu. Mengukur CPU lawan GPU dan mencari tahu kapan GPU justru kalah.

### Yang kamu tulis sendiri

Regresi linear murni numpy. Fungsi MSE dan MAE tanpa pustaka. Gradien analitik yang diverifikasi dengan beda hingga. Training loop dari kosong. Plot permukaan loss 3D beserta animasi lintasannya.

### Jembatan fisika

Loss adalah energi potensial. Gradient descent adalah bola menggelinding ke lembah. Permukaan loss model linear berbentuk parabola, jadi ia potensial harmonik dengan `k = 2A` di mana `A` adalah kelengkungannya. Karena itu learning rate yang kebesaran menghasilkan osilasi lalu divergensi, persis sistem pegas yang kekurangan redaman.

### Tolok ukur

Kamu bisa memasang garis pada data berisik tanpa memanggil satu pun pustaka ML, menjelaskan tiap baris kodenya, dan menunjukkan grafik divergensi beserta alasannya.

---

## Modul 1. Backpropagation dan jaringan saraf

**Durasi:** 2 minggu, sekitar 16 jam

### Kenapa modul ini ada

Backpropagation adalah satu-satunya alasan deep learning bisa bekerja. Tanpanya, melatih jaringan dengan jutaan parameter mustahil.

Kebanyakan orang memakai `loss.backward()` seumur hidup tanpa tahu isinya. Kamu akan menulis isinya sendiri, sekitar 150 baris, lalu melihat PyTorch mengerjakan hal yang sama. Setelah itu tidak ada lagi kotak hitam di lapisan paling dasar.

### Yang kamu pelajari

Graf komputasi dan cara gradien mengalir mundur menembusnya. Fungsi aktivasi dan alasan keberadaannya. Cara melatih jaringan berlapis. Perbedaan antara diferensiasi simbolik, numerik, dan otomatis.

### Yang kamu tulis sendiri

Mesin autograd bergaya micrograd, lengkap dengan kelas `Value` yang melacak operasi dan menurunkan gradiennya otomatis. MLP yang dibangun di atas mesin itu. Pelatihan MNIST sampai akurasi di atas 95 persen. Versi PyTorch dari kode yang sama, untuk dibandingkan.

### Jembatan fisika

Backpropagation adalah aturan rantai dari Fisika Matematika, diterapkan mundur menembus graf. Tidak ada matematika baru di sini. Yang baru cuma nama dan cara mengorganisasinya.

### Sambungan mata kuliah

Machine Learning mulai berjalan. Teori dari kelas, implementasi dari sini.

### Tolok ukur

MLP buatanmu mencapai akurasi di atas 95 persen di MNIST, dan kamu bisa menjelaskan aliran gradien pada tiap lapisan tanpa membuka kode.

---

## Modul 2. Representasi dan klasifikasi

**Durasi:** 2 minggu, sekitar 12 jam

### Kenapa modul ini ada

Mesin tidak mengerti kata. Ia mengerti vektor. Seluruh cara kerja NLP modern bergantung pada satu ide: ubah makna jadi titik di ruang berdimensi tinggi, lalu ukur jaraknya.

Modul ini juga menghasilkan komponen SYNESIS yang pertama benar-benar berguna. Setelah ini asistenmu sudah bisa dipakai, tanpa satu pun LLM.

### Yang kamu pelajari

Bag-of-words dan embedding. Regresi logistik dan cross-entropy. Cara mengumpulkan dan memberi label data sendiri. Evaluasi dengan confusion matrix dan pembagian train/test.

### Yang kamu tulis sendiri

Klasifikasi teks dari nol, mulai dari bag-of-words sampai regresi logistik, semuanya manual. Cross-entropy loss yang kamu turunkan sendiri. Intent classifier yang dilatih dari 300 sampai 500 perintah buatanmu.

### Yang masuk ke SYNESIS

Intent classifier, plus toolset filesystem dasar dan safety gate. Hasilnya SYNESIS v0.1: perintah teks masuk, intent dikenali, tool dijalankan.

### Jembatan fisika

Embedding adalah vektor di ruang berdimensi tinggi, dan kemiripan adalah hasil kali dalam. Operasinya sama dengan proyeksi keadaan di Fisika Kuantum. Softmax adalah distribusi Boltzmann, dan parameter temperature memang dinamai dari suhu termodinamika. Cross-entropy adalah entropi dari Termodinamika.

### Sambungan mata kuliah

Kandidat terkuat untuk tugas besar Machine Learning. Siklusnya utuh: kumpulkan data, beri label, latih, evaluasi, pasang ke sistem nyata.

### Tolok ukur

Kamu mengetik perintah dengan kalimatmu sendiri, dan SYNESIS mengerjakannya lewat classifier yang kamu latih.

---

## Modul 3. Sinyal, konvolusi, dan suara

**Durasi:** 3 minggu, sekitar 20 jam

### Kenapa modul ini ada

Suara adalah sinyal satu dimensi yang berubah terhadap waktu. Untuk membuat mesin mengenalinya, sinyal itu harus diubah dulu jadi representasi waktu-frekuensi. Di situlah Fourier masuk.

Modul ini juga tempat kenyataan menggigit. Latensi, kuirk perangkat audio, ambang VAD yang meleset, wake word yang salah picu di ruangan berisik. Semua itu perlu jam yang tidak bisa dipercepat.

### Yang kamu pelajari

Sampling, framing, dan windowing. Spektrogram dan MFCC. Konvolusi satu dan dua dimensi. Arsitektur CNN. Deteksi aktivitas suara. Pipeline speech-to-text dan text-to-speech.

### Yang kamu tulis sendiri

Konvolusi 1D dan 2D manual. Spektrogram dari nol, mulai framing sampai FFT. MFCC dari nol. CNN kecil tanpa pustaka, lalu versi PyTorch-nya. Keyword spotter yang dilatih pada Google Speech Commands.

### Yang masuk ke SYNESIS

Wake word yang dilatih dengan suaramu sendiri, VAD, Whisper untuk transkripsi umum, dan Piper untuk balasan suara. Hasilnya SYNESIS v0.2.

### Jembatan fisika

Ini praktikum DSP. Transformasi Fourier, windowing, teorema konvolusi, aliasing. Semuanya dari Gelombang dan DSP. Lapisan konvolusi pada CNN adalah konvolusi yang sama dari Fisika Matematika III.

### Sambungan mata kuliah

Kandidat terkuat untuk tugas DSP untuk Sensor dan Imaging.

### Tolok ukur

Kamu memanggil "Hey Synesis" dengan wake word buatanmu sendiri, dan sistemnya menjawab dalam waktu di bawah 3 detik.

---

## Modul 4. Metric learning dan visi

**Durasi:** 2 minggu, sekitar 12 jam

### Kenapa modul ini ada

Pengenalan wajah tidak bekerja dengan cara mencocokkan gambar. Ia bekerja dengan memetakan wajah ke vektor, lalu mengukur sudut antar vektor. Ide bahwa jarak bisa mewakili identitas adalah fondasi seluruh sistem pencarian modern, dari pencarian gambar sampai rekomendasi.

Modul ini juga tempat kamu belajar bahwa memilih ambang itu keputusan, bukan hitungan. Ambang yang terlalu longgar menerima orang asing. Terlalu ketat menolak kamu sendiri.

### Yang kamu pelajari

Metric learning dan contrastive loss. Cara kerja ArcFace dan pemisahan sudut. Enrollment dan pencocokan. Kurva ROC, FAR, dan FRR. Kalibrasi ambang.

### Yang kamu tulis sendiri

Siamese network kecil dengan contrastive loss. Pelatihan pada dataset wajah kecil, lalu pengamatan cara embedding-nya memisah. Alur enrollment dan pencocokan. Kurva ROC beserta penentuan ambangnya.

### Yang masuk ke SYNESIS

Pengenalan wajah dengan ambang yang kamu kalibrasi sendiri, dipakai untuk membuka sesi dan mengautentikasi operasi sensitif. Hasilnya SYNESIS v0.3.

### Jembatan fisika

Embedding wajah adalah vektor ternormalisasi di permukaan bola satuan berdimensi 512. Pengenalan adalah proyeksi. ArcFace bekerja dengan memaksimalkan pemisahan sudut, dan itu geometri.

### Sambungan mata kuliah

Kurva ROC dan kalibrasi ambang adalah materi laporan Machine Learning yang kuat.

### Tolok ukur

SYNESIS mengenalimu dari webcam dalam waktu di bawah 1 detik, hampir tidak pernah menerima wajah asing, dan kamu bisa menjelaskan kenapa ambangnya berada di angka itu.

---

## Modul 5. Attention dan transformer

**Durasi:** 3 sampai 4 minggu, sekitar 20 jam

### Kenapa modul ini ada

Semua LLM modern berdiri di atas satu arsitektur. Kalau kamu membangunnya sendiri, Qwen3-4B yang kamu jalankan di Modul 6 berhenti jadi kotak hitam.

Modul ini paling sulit. Bug di sini tidak melempar error. Ia menghasilkan model yang berlatih rajin tanpa pernah membaik, dan menemukannya butuh kesabaran.

### Yang kamu pelajari

Self-attention dan alasan keberadaannya. Multi-head attention. Positional encoding. Arsitektur transformer utuh. Tokenisasi. Sampling dan temperature.

### Yang kamu tulis sendiri

Self-attention dari nol dengan numpy, termasuk penurunan query, key, dan value. Multi-head attention. Positional encoding. Transformer utuh bergaya nanoGPT. Mini-GPT yang kamu latih pada teks pilihanmu sendiri, beberapa juta parameter, 30 sampai 60 menit di GTX 1650 Ti.

Modelnya akan payah. Itu wajar. Poinnya kamu sudah membangun dan melatih LLM sendiri.

### Jembatan fisika

Attention adalah hasil kali dalam berbobot, jadi ruang Hilbert lagi. Positional encoding memakai sinus dan kosinus berbagai frekuensi, dan itu deret Fourier. Sampling temperature adalah distribusi Boltzmann. Jadwal penurunan learning rate adalah jadwal pendinginan, dan istilah simulated annealing memang berasal dari mekanika statistik.

### Sambungan mata kuliah

Fisika Statistik memberi kerangka teoretisnya.

### Tolok ukur

Mini-GPT buatanmu menghasilkan teks yang menyerupai data latihnya, dan kamu bisa menjelaskan tiap komponen transformer tanpa membuka catatan.

---

## Modul 6. Integrasi dan LLM lokal

**Durasi:** 4 minggu, sekitar 20 jam

### Kenapa modul ini ada

Enam modul sebelumnya menghasilkan enam bagian yang masing-masing jalan sendiri. Menyatukannya adalah pekerjaan tersendiri, dan selalu memakan waktu lebih lama dari perkiraan siapa pun.

Modul ini juga tempat LLM akhirnya masuk, dan porsinya kecil: hanya untuk permintaan terbuka yang tidak bisa ditangkap intent classifier.

### Yang kamu pelajari

Arsitektur agent dan siklus sense, plan, act. State machine. Tool calling dan cara memaksa keluaran JSON valid dengan grammar. Manajemen resource. Perancangan lapisan keamanan.

### Yang kamu bangun

Ollama dengan Qwen3-4B lokal. Agent loop dengan tool calling dan grammar GBNF. Orkestrator berbentuk state machine. Ekstraktor metadata dan pembaca log. Safety gate versi kedua dengan rate limiting dan kill switch.

### Jembatan fisika

Siklus agent adalah lingkar kendali dengan umpan balik, kerangka yang sama dengan Robotika Cerdas dan Otomasi Sistem Fisik.

### Sambungan mata kuliah

Robotika Cerdas dan Otomasi Sistem Fisik.

### Tolok ukur

Perintah suara masuk, dikenali, dieksekusi, lalu dijawab dengan suara. Sepenuhnya offline. Menyala 8 jam tanpa crash, tanpa satu pun operasi berbahaya lolos tanpa konfirmasi.

---

## Penilaian

Tidak ada nilai huruf. Yang ada tolok ukur yang bisa kamu periksa sendiri.

| Modul | Lulus bila |
|---|---|
| 0 | Regresi linear jalan tanpa pustaka ML, dan kamu bisa menjelaskan tiap barisnya |
| 1 | MLP buatanmu tembus 95 persen di MNIST |
| 2 | Perintah teks dengan kalimatmu sendiri dieksekusi dengan benar |
| 3 | Wake word buatanmu menjawab dalam 3 detik |
| 4 | Wajahmu dikenali dalam 1 detik, wajah asing ditolak |
| 5 | Mini-GPT menghasilkan teks menyerupai data latihnya |
| 6 | Sistem menyala 8 jam tanpa crash |

Satu tolok ukur tambahan yang berlaku di semua modul: kamu bisa menjelaskan kodemu sendiri ke orang lain tanpa membuka catatan. Kalau tidak bisa, modulnya belum selesai meski programnya jalan.

---

## Aturan kerja

**Tulis dulu, baru pakai pustaka.** Tiap konsep dikerjakan dua kali. Sekali dari nol, sekali dengan pustaka. Urutannya tidak boleh dibalik. Menulis MLP sendiri lalu melihat `nn.Linear` melakukan hal yang sama akan menghapus rasa gaibnya untuk selamanya. Langsung memakai `nn.Linear` justru mengabadikan rasa itu.

**Selalu ada yang berjalan.** Tiap modul berakhir dengan program yang bisa dijalankan dan ditunjukkan, bukan catatan atau tutorial yang setengah ditonton.

**Belajar tepat pada waktunya.** Jangan menghabiskan waktu menonton kursus ML di depan. Pelajari tiap konsep pada minggu ia dibutuhkan.

**Terjemahkan ke bahasa fisika.** Tiap konsep baru, tanyakan padanannya di fisika. Hampir selalu ada, dan itu keunggulan yang tidak dimiliki mayoritas orang yang belajar ML.

**Catat di log.** Setiap proses yang selesai masuk [log.md](../log.md), termasuk kesalahan dan cara memperbaikinya.

---

## Alat

Semuanya gratis dan berjalan lokal. Rincian versi ada di [README.md](../README.md).

Python 3.12 dengan numpy, scipy, matplotlib, dan scikit-learn untuk fondasi. PyTorch untuk deep learning. librosa, faster-whisper, openWakeWord, dan Piper untuk suara. OpenCV dan InsightFace untuk visi. Ollama dengan Qwen3-4B untuk LLM lokal.

Perangkat: Ryzen 5 4600H, RAM 15,4 GB, GTX 1650 Ti dengan 4 GB VRAM. Cukup untuk semua yang dilatih di sini.

---

## Referensi

Dokumen di repo ini: [Roadmap.md](Roadmap.md), [Bulan-0-Harian.md](Bulan-0-Harian.md), [Name.md](Name.md), [log.md](../log.md).

Bahan luar yang dipakai: nanoGPT dan micrograd karya Andrej Karpathy untuk Modul 1 dan 5, dataset MNIST untuk Modul 1, Google Speech Commands untuk Modul 3, dokumentasi InsightFace untuk Modul 4.

Empat mata kuliah Semester 5 yang berjalan beriringan: Machine Learning, DSP untuk Sensor dan Imaging, Fisika Statistik, dan Robotika Cerdas dan Otomasi Sistem Fisik.
