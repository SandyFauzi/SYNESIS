# Log Kerja SYNESIS

Catatan kronologis semua yang dikerjakan, termasuk keputusan yang diambil dan
kesalahan yang terjadi. Ditulis oleh asisten, dibaca manusia.

**Konvensi:** entri baru ditambahkan di bawah. Kesalahan dicatat apa adanya,
karena log yang hanya memuat keberhasilan tidak berguna saat menelusuri masalah
tiga bulan kemudian.

---

## Fase Perencanaan · 13 sampai 14 Agustus 2026

### Pembacaan awal

Membaca dua PDF di folder: KPA semester 1 sampai 4 dan KRS semester 5.

- IPK 3,70 dengan 80 SKS terkumpul
- Semester 5 mengambil 22 SKS, 9 mata kuliah
- Empat mata kuliah bersinggungan langsung dengan proyek: Machine Learning,
  DSP untuk Sensor dan Imaging, Robotika Cerdas, Fisika Statistik

### Diagnosa perangkat

```text
CPU    AMD Ryzen 5 4600H, 6 core 12 thread
RAM    15,4 GB
GPU    NVIDIA GTX 1650 Ti, 4 GB VRAM, compute capability 7.5
Python 3.12.5, Git 2.48.1, Node v25.1.0
```

CUDA diuji lewat cupy dan lulus.

Ditemukan 979 MB VRAM terpakai saat idle oleh Wallpaper Engine, Chrome, Epic
Games Launcher, Steam, dan Antigravity. Sisa efektif 3,1 GB, bukan 4 GB. Temuan
ini mengoreksi asumsi awal bahwa iGPU Radeon menggerakkan tampilan.

Python global memuat sekitar 250 paket termasuk tumpukan riset fisika: astropy,
spacepy, pyspedas, cdflib, geopack, juliacall, schroedingerequation.

Mikrofon: 36 perangkat input terdeteksi, Realtek internal siap untuk Bulan 3.

### Tiga versi roadmap

**v1** mengandaikan API berbayar sebagai otak. Dibuang setelah pemilik
menyatakan kendala biaya Rp 0.

**v2** memindahkan otak ke Qwen3-4B lokal. Masih berorientasi produk dengan
tenggat enam bulan. Anggaran waktunya defisit 8 jam.

**v3** membalik kerangkanya. Enam bulan untuk memahami fondasi, produk tanpa
tenggat. Tiap bulan menghasilkan komponen yang benar-benar dipakai, jadi belajar
dan membangun berhenti bersaing memperebutkan waktu. Anggaran berubah jadi
surplus 12 jam.

Temuan yang mengubah arah: SYNESIS tidak butuh LLM sampai Bulan 6. Sebagian
besar perintah harian bisa diselesaikan intent classifier, dan itu supervised
learning klasik yang dikuasai di Bulan 2.

### Penamaan

Nama awal Jarvis diganti jadi SYNESIS untuk ekosistem dan SEREN untuk agen,
panggilan Sera. Pemilik menetapkan kepanjangannya dan menolak revisi akronim.

Ditambahkan lapisan etimologi: synesis adalah kata Yunani Kuno berarti
pemahaman, dari syn (bersama) dan hienai (menaruh). Aristoteles membahasnya di
Nicomachean Ethics Buku VI sebagai keutamaan intelektual untuk menilai dengan
baik.

Seluruh Jarvis diganti di Roadmap.md dan Bulan-0-Harian.md. Wake word Bulan 3
jadi Hey Synesis.

### Berkas yang dibuat

| Berkas | Isi |
|---|---|
| Roadmap.md | Rencana enam bulan, arsitektur, jembatan fisika ke ML |
| Bulan-0-Harian.md | Diagnosa lingkungan dan rencana 19 hari |
| Name.md | Identitas, etimologi, konvensi penamaan |
| README.md | Deskripsi proyek dan kebijakan drive |

### Skill yang dipasang

Tiga skill di direktori skills milik pengguna: revision-coach, lecture-builder,
lesson-plan-designer. Folder ABOUT ME belum ada, jadi dibuatkan template
teaching-profile.md yang masih perlu diisi. Ketiga skill berhenti di langkah
pertama sampai template itu terisi.

---

## Hari 1 · 20 Agustus 2026 · lingkungan

### Keputusan lokasi

Pembahasan berpindah beberapa kali sebelum mendarat:

1. Awalnya diusulkan drive X karena E adalah SSD dalam enclosure, dan venv
   menyimpan path absolut sehingga rentan pada pergeseran huruf drive
2. Pemilik memilih E untuk portabilitas antar perangkat. Diterima
3. Pemilik meluruskan kendala sebenarnya: bukan isolasi Python global, tapi
   menjaga C dari pustaka dan model di atas 1 GB
4. Di tengah eksekusi, pemilik memutuskan workspace tetap di S, dan E hanya
   jadi gudang

Hasil akhir:

```text
S:\Code\Make A Jarvis     kode, dokumen, repo git
E:\SYNESIS                venv, cache model, dataset
```

### Langkah yang dijalankan

1. Verifikasi drive E terpasang. 191,2 GB bebas, NTFS, label Sandzh BackUp
2. Membuat E:\SYNESIS beserta subfolder cache untuk pip, huggingface, torch,
   ollama, dan insightface
3. Menyetel 4 variabel lingkungan User lewat registry
4. Membongkar folder kode yang terlanjur dibuat di E setelah pemilik
   memindahkan workspace ke S
5. Membuat venv di E:\SYNESIS\.venv
6. Memasang numpy, scipy, matplotlib, scikit-learn, pandas, jupyterlab,
   ipykernel, rich
7. Memasang torch dan torchvision dari indeks cu124
8. Inisialisasi git, menulis gitignore, commit

### Bukti isolasi

```text
paket di venv    :   1   (sebelum instal)
paket di global  : 289
numpy di venv    : 2.5.2
numpy di global  : 2.4.6
base python venv : C:\...\Python312   <- menunjuk balik ke interpreter global
```

venv meminjam interpreter, membawa pustaka sendiri. Tumpukan fisika di global
diuji ulang setelah instalasi: numpy 2.4.6, scipy 1.17.1, astropy 7.2.0, dan
spacepy 0.7.0 semuanya hidup.

### Berkas pendukung yang dibuat

| Berkas | Gunanya |
|---|---|
| activate.ps1 | Aktivasi venv yang tinggal di drive lain, dengan pesan jelas kalau E tidak terpasang |
| verify.py | Audit lingkungan: venv, variabel, kebocoran ke C, status CUDA |
| progress.ps1 | Pemantau progres instalasi paket besar |
| requirements.txt | 115 paket, dengan catatan indeks cu124 untuk torch |
| .gitignore | Menutup venv, dataset, bobot model, dan dokumen akademik |

Dua PDF akademik dipindahkan ke docs/akademik/ dan dimasukkan gitignore.
Keduanya memuat nama, NPM, dan seluruh nilai. Roadmap menyebut proyek ini akan
jadi bahan portofolio, dan riwayat git bersifat permanen.

### Hasil akhir

```text
torch 2.6.0+cu124
CUDA tersedia : True
GPU  : NVIDIA GeForce GTX 1650 Ti
VRAM : 3,2 GB bebas / 4,0 GB
venv : 5,2 GB    cache pip : 2,6 GB    paket : 115
verify.py : LULUS SEMUA
```

---

## Kesalahan dan Pelajaran

### 1. Variabel lingkungan tidak menembus proses yang sudah jalan

Setelah memasang paket inti, 139,9 MB cache pip ditemukan di C padahal
PIP_CACHE_DIR sudah disetel.

Penyebabnya: variabel lingkungan diwariskan saat proses dibuat. Registry sudah
benar, tapi sesi yang sedang berjalan lahir dari induk yang dibuat sebelum
variabel itu ada.

Cache dipindahkan ke E. Perintah berikutnya menyetel variabel eksplisit di baris
yang sama.

**Konsekuensi untuk pemilik:** terminal yang terbuka sebelum Hari 1 belum tahu
soal keempat variabel. Tutup dan buka lagi.

### 2. Salah diagnosa, membunuh unduhan yang sedang jalan

Instalasi PyTorch di latar terlihat diam selama belasan menit. Pengecekan folder
temp memfilter nama berakhiran whl dan direktori berawalan pip, dan hasilnya
kosong. Kesimpulan macet diambil, proses dimatikan.

Pengecekan berikutnya menunjukkan 1.782 MB sudah terunduh. Filternya yang salah,
bukan unduhannya. Bandwidth terbuang dan unduhan mengulang dari nol.

**Pelajaran:** filter yang sempit menghasilkan hasil kosong yang tampak sama
persis dengan tidak ada aktivitas. Ukur ukuran direktori secara keseluruhan
sebelum menyimpulkan sesuatu berhenti.

### 3. Peluncuran jendela CMD gagal dua kali

Percobaan pertama memakai Start-Process powershell dengan flag File pada path
mengandung spasi. Argumennya terpecah dan jendela tertutup seketika.

Percobaan kedua memakai cmd start. Tidak menghasilkan jendela sama sekali.

Yang berhasil: menulis berkas bat di path tanpa spasi lalu memanggilnya langsung
dengan Start-Process FilePath.

---

## Keputusan yang Diambil Pemilik

| Keputusan | Alasan |
|---|---|
| Nama SYNESIS dan SEREN dikunci beserta kepanjangannya | Milik pemilik, tidak dibuka untuk revisi |
| Workspace di S, gudang di E | Repo tetap ringan, barang berat terpisah |
| venv bersih tanpa system-site-packages | Menjaga portabilitas antar perangkat |
| TMP dan TEMP dibiarkan default di C | Temp bersifat transien dan bisa dihapus. Mengarahkannya ke E membuat semua aplikasi Windows rapuh saat enclosure dicabut |
| Odysseus ditunda ke Bulan 6 | Memasangnya sekarang melewati seluruh proses belajar Bulan 0 sampai 5 |

---

## Hari 2 · 20 Agustus 2026 · numpy (berjalan)

### Aturan baru

Pemilik menetapkan: setiap proses yang selesai wajib dicatat di log ini.
Aturannya ditulis di README bagian Aturan Kerja.

### Kerangka latihan disiapkan

Dibuat `notebooks/hari02_numpy.py`, berisi empat bagian:

| Bagian | Isi | Status |
|---|---|---|
| 1 | Array lawan list: dtype, shape, strides, nbytes | contoh diberikan |
| 2 | Broadcasting: aturan, kasus gagal, jebakan kolom lawan baris | contoh diberikan |
| 3 | `dot_manual` dengan loop Python | TODO pemilik |
| 4 | `matmul_manual` tiga loop bersarang | TODO pemilik |
| 5 | Adu cepat lawan numpy, tiga ukuran n | otomatis |

Kode inti sengaja tidak diisi. Nilai Bulan 0 ada pada menulisnya sendiri, jadi
asisten hanya menyiapkan kerangka, penjelasan, dan pemeriksa kebenaran.

Bagian adu cepat memuat `assert` yang membandingkan hasil pemilik dengan numpy,
jadi kesalahan implementasi ketahuan sebelum angka waktunya dibaca.

Diuji jalan: bagian 1 dan 2 keluar benar, bagian 4 melewati diri sendiri dengan
pesan jelas selama TODO belum diisi.

### Soal latihan disiapkan

Dibuat `notebooks/soal-hari02.md`, lima soal dengan petunjuk bertingkat yang
tertutup di blok `<details>`. Pemilik bisa mengatur sendiri seberapa banyak
bantuan yang diambil.

| Soal | Isi |
|---|---|
| 1 | Ramalkan enam bentuk broadcasting sebelum menjalankan |
| 2 | Tulis `dot_manual`, tiga tingkat petunjuk |
| 3 | Tulis `matmul_manual`, tiga tingkat plus panduan kalau hasilnya transpos |
| 4 | Baca angka adu cepat, empat pertanyaan analisis |
| 5 | Cari bug broadcasting yang tidak melempar error |

Soal 5 memakai matriks persegi 3x3, karena bentuk persegi membuat kesalahan
sumbu lolos tanpa error. Pada bentuk (100,3) kesalahan yang sama langsung
ditolak numpy. Ini melatih kebiasaan menguji dengan dimensi yang berbeda-beda,
kebiasaan yang akan menyelamatkan Bulan 1.

Kunci jawaban diverifikasi dengan menjalankannya:

```text
1a (3,4)   1b ERROR   1c (3,4)   1d (3,3)   1e (2,3,4)   1f (5,4,3)
```

Klaim Soal 5 juga diuji: pada (3,3) kedua operasi jalan, pada (100,3) numpy
menolak dengan ValueError.

### Selesai

Pemilik mengisi TODO 3 dan TODO 4, menjawab seluruh soal, dan menulis ulang
soal-hari02.md dengan gaya bahasanya sendiri.

Hasil pemeriksaan: Soal 1 enam-enamnya benar, `dot_manual` dan `matmul_manual`
benar, Soal 4 dan Soal 5 semuanya benar.

Angka adu cepat pada mesin ini:

```text
dot     n=1.000       manual    0,31 ms   numpy 0,003 ms      107x
        n=100.000     manual   39,06 ms   numpy 0,078 ms      501x
        n=1.000.000   manual  291,74 ms   numpy 0,490 ms      596x

matmul  50x50         manual    44,32 ms   numpy 0,019 ms    2.365x
        100x100       manual   349,42 ms   numpy 0,090 ms    3.886x
        200x200       manual  2.813,98 ms  numpy 0,286 ms    9.837x
```

Rasio 100x100 ke 200x200 keluar 8,06x, cocok dengan ramalan n pangkat tiga.

### Catatan perbaikan

Tiga hal kecil yang diangkat saat pemeriksaan:

1. `matmul_manual` menghitung `k2` dari bentuk B tapi tidak memakainya. Sebaiknya
   memvalidasi `k == k2`, yang langsung menyambung ke pelajaran Soal 5 soal
   memeriksa bentuk sebelum menghitung.
2. Angka pada n=1.000 berbeda jauh antara dua kali jalan, 24x lawan 107x. Fungsi
   `ukur` menjalankan versi manual sekali saja, terlalu berisik pada n kecil.
3. Pesan moral 5d perlu sedikit dilonggarkan. Matriks persegi tidak terlarang,
   yang penting memakai dimensi berbeda saat menguji kode yang sensitif bentuk.

### Pertanyaan terbuka

Pemilik menyebut punya Julia 1.12.5 terpasang dan menanyakan apakah kompilasi
seperti C ada gunanya di sini. Jawabannya ya, karena percobaan saat ini masih
mencampur dua variabel: bahasa dan optimasi algoritma. Julia dengan algoritma
naif yang sama akan memisahkan keduanya.

---

## Hari 2 bonus · 20 Agustus 2026 · Julia

Dibuat `notebooks/hari02_bonus_julia.jl` untuk memisahkan dua variabel yang
tercampur pada percobaan Python lawan numpy: bahasa dan optimasi algoritma.

Julia 1.12.5 sudah terpasang. Berkas memuat tiga versi:

| Versi | Isi |
|---|---|
| `matmul_naif` | terjemahan persis dari matmul_manual Python |
| `matmul_kolom` | algoritma sama, urutan loop disesuaikan tata letak column-major Julia |
| `*` bawaan | BLAS |

### Dua bug pada percobaan pertama

**Dead code elimination.** Fungsi `ukur` versi awal membuang hasil pemanggilan
di dalam generator, jadi kompilator Julia berhak menghapus seluruh perhitungan.
Waktunya keluar 0,008 ms untuk 1 juta operasi, setara 125 GFLOPS, mustahil untuk
loop skalar satu core. Diperbaiki dengan menampung hasil ke variabel yang
tertangkap closure.

**Pembanding BLAS yang keliru.** `sum(x .* y)` dipakai sebagai wakil BLAS,
padahal ia mengalokasi array perantara sebesar n dan justru lebih lambat dari
loop naif. Diganti `LinearAlgebra.dot`.

Pelajarannya sama dengan yang sudah muncul di Hari 1: angka yang terlalu bagus
wajib dicurigai sebelum dipercaya.

### Hasil setelah perbaikan

```text
dot     n=1.000.000    Python 291,74 ms   Julia naif 0,840 ms   Julia BLAS 0,384 ms

matmul  200x200        Python 2.814,0 ms
                       Julia naif   6,125 ms
                       Julia kolom  1,065 ms
                       Julia BLAS   0,357 ms
```

### Pembagian jurang pada 200x200

| Lompatan | Faktor | Sebabnya |
|---|---|---|
| Python naif ke Julia naif | 461x | ongkos penafsir, algoritma identik |
| Julia naif ke Julia kolom | 5,8x | urutan loop cocok tata letak memori |
| Julia kolom ke BLAS | 3,3x | SIMD, pemblokan cache, multithread |
| **Total Python ke BLAS** | **8.928x** | |

Perkalian ketiga faktor menghasilkan 8.825, cocok dengan 8.928 dalam batas
derau pengukuran.

Temuan pokoknya: **461 dari 8.928 kali lipat itu semata soal bahasa.** Sisanya
yang 19 kali lipat baru berasal dari tata letak memori dan kecerdasan BLAS.

---

## Hari 3 · 20 Agustus 2026 · data dan loss (disiapkan)

Dibuat `notebooks/hari03_data_loss.py` dan `notebooks/soal-hari03.md`.

Data sintetis `y = 3x + 2 + derau`, n=50, sigma=1.5, seed 42. Tiga fungsi
dikosongkan sebagai TODO: `prediksi`, `mse`, `mae`.

Bagian 4 menyapu `w` dengan `b` dikunci, menghasilkan irisan 1D dari permukaan
loss. Bentuknya parabola, dan itu jembatan ke potensial harmonik di Mekanika.

### Kunci jawaban, diverifikasi

```text
Ranking Soal 1 : E(1,3554) < F(1,4971) < C(4,3552) < D(32,52) < B(38,75) < A(79,49)
Uji mse/mae    : 1,3333 dan 0,6667
w* analitik    : 3,0066     w asli 3,0     sapuan grid 3,0251
A = 7,8435 (positif)   B = -47,1647
```

### Temuan yang jadi soal tambahan

Loss di parameter asli keluar 1,3554, padahal varians derau 2,25. Selisihnya
diperiksa dan bukan bug: sampel n=50 dengan seed 42 jatuh di -1,99 simpangan
baku. Pada n=200 angkanya 2,3187, pada n=10000 jadi 2,2594.

Dijadikan Soal 3e, lengkap dengan rumus sebaran $\sigma^2\sqrt{2/n}$ dan
kaitannya ke ketidakpastian pengukuran di Eksperimen Fisika.

Soal 4 menjadi puncak Hari 3: pemilik menurunkan sendiri bentuk $Aw^2+Bw+C$
lalu $w^* = -B/2A$, yaitu solusi kuadrat terkecil bentuk tertutup.

---

## Hari 3 selesai + akselerasi · 20 Agustus 2026

### Jawaban Hari 3 diperiksa

Seluruhnya benar. Ranking Soal 1 cocok persis dengan kunci. Tiga fungsi lolos
uji. Soal 3a sampai 3e benar. Soal 4b, 4c, 4d benar termasuk penurunan
`w* = -B/2A`. Soal 5a sampai 5c benar.

Satu koreksi presisi: pada 5a padanannya `k = 2A`, bukan `k = A`, karena
potensial pegas memuat faktor setengah sementara bentuk `A(w-w*)^2` tidak.

### Akselerasi diminta dan diterapkan

Pemilik menyatakan diri pembelajar cepat dengan 5 tahun pengalaman C ke Python.
Bukti mendukung: Hari 1 sampai 3 tuntas dalam satu hari, seluruh jawaban benar
termasuk penurunan aljabar dan ramalan perilaku divergensi sebelum melihat data.

**Bulan-0-Harian.md**: Hari 5 sampai 19 digabung jadi empat sesi.

| Sesi | Menggantikan | Isi |
|---|---|---|
| A | Hari 5, 6, 7 | turunkan gradien, gradient check, training loop |
| B | Hari 8, 9 | sapuan learning rate, permukaan 3D, animasi |
| C | Hari 10, 12, 13 | multivariat, overfitting, regularisasi |
| D | Hari 14, 15, 16 | sklearn, PyTorch autograd, GPU |

**Roadmap.md**: bagian 5b ditambahkan. Total kira-kira 4 bulan, bukan 6.

Tiga bulan sengaja tidak dipadatkan: Bulan 3 karena debugging audio tidak bisa
dipercepat, Bulan 5 karena attention memang sulit, Bulan 6 karena integrasi
selalu molor.

Dicatat juga bahwa batas sebenarnya adalah kalender, bukan kemampuan. Dengan
22 SKS dan sekitar 8 jam per minggu, akselerasi berarti lebih sedikit sesi
untuk cakupan sama, bukan lebih banyak jam.

Dua sesi ditandai tidak boleh dipadatkan lagi: animasi permukaan loss di Sesi B
dan pengalaman melihat overfitting di Sesi C. Keduanya pengalaman, bukan tugas.

---

## Silabus · 20 Agustus 2026

Dibuat `Silabus.md`, versi silabus dari roadmap dengan tujuan pembelajaran per
modul. Ditulis ulang dari nol atas permintaan pemilik supaya berdiri sendiri
sebagai rencana utuh, tanpa penanda progres. Progres tetap tinggal di berkas
log ini.

Struktur: identitas, deskripsi, delapan tujuan pembelajaran, tabel prasyarat
yang sudah dipenuhi, tujuh modul, skema penilaian, aturan kerja, daftar alat,
dan referensi.

Tiap modul memuat bagian "kenapa modul ini ada" yang menjawab alasan materinya
dipelajari, bukan cuma daftar isinya. Modul 0 dirinci jadi tujuh sesi mulai dari
penyiapan lingkungan.

Ditulis dengan skill `humanizer` dan `stop-slop` aktif. Diverifikasi bersih dari
em dash, en dash, curly quote, dan emoji pada judul. 368 baris, 16 bagian utama,
44 sub-bagian.

---

## Modul all-in-one · 20 Agustus 2026

Menulis `Modul.md`, dokumen penjelasan yang berdiri sendiri di samping silabus.
Silabus menjawab "belajar apa dan kapan". Modul menjawab "barangnya itu apa".

857 baris, 14 bagian utama, 41 sub-bagian. Isinya penjelasan seluruh konsep dari
tujuh modul: gradient descent, overfitting, backpropagation, embedding, softmax,
Fourier, konvolusi, metric learning, attention, transformer, dan agent loop.

Tiga hal dipasang di tiap bagian. Gambaran konkret sebelum rumus. Catatan
"di mana analoginya rusak" supaya kasus tepi tidak salah dipahami. Blok
"tanya diri sendiri" berisi pertanyaan Socratic untuk dijawab dengan suara keras.

Bagian 9 memuat kamus 19 baris yang memetakan konsep fisika yang sudah dikuasai
ke nama panggilannya di machine learning. Bagian 10 berisi lima uji kejujuran
untuk membedakan paham dari hafal, termasuk deteksi pemujaan kargo.

Bagian yang sengaja mengaku tidak tahu: kenapa model overparameterisasi tetap
menggeneralisasi (double descent masih diperdebatkan), tafsir peran attention
head dan neuron lapisan dalam (interpretability masih muda), dan apakah LLM
"mengerti" (mekanismenya prediksi token, perilakunya menyerupai penalaran,
lompatan di antaranya belum terbukti).

Ditulis dengan skill `humanizer`, `stop-slop`, `feynman-perspective`, dan
`ai-feynman-techniek-coach` aktif. Verifikasi bersih: 0 em dash, 0 en dash,
0 curly quote, tanpa emoji.

### Versi PDF

Dikonversi ke `Modul.pdf` dengan pandoc 3 dan xelatex dari MiKTeX di
`S:\Apps\MiTex`. A4, margin 2,3 cm, Georgia untuk badan teks, Consolas untuk
kode, daftar isi dua level. 24 halaman, 124 KB.

Satu cacat ditemukan saat memeriksa hasil cetakan dan sudah diperbaiki. Notasi
bra-ket `<psi|phi>` di dalam sel tabel Bagian 9 tercetak berikut backslash-nya,
karena pipe di dalam inline code tidak bisa di-escape untuk tabel Markdown.
Selnya ditulis ulang jadi teks biasa. Pelajarannya: verifikasi keluaran PDF
dengan melihat halamannya, bukan cuma dengan mengecek exit code pandoc.

---

## Sesi A · 20 Agustus 2026

Menyiapkan `notebooks/sesiA_gradient_descent.py` dan `notebooks/soal-sesiA.md`.
Scaffold memakai ulang `buat_data`, `prediksi`, dan `mse` dari berkas Hari 3
lewat import, jadi kalau yang di sana benar yang di sini ikut benar.

Tiga TODO: `gradien` analitik, `beda_hingga` numerik, dan `latih` sebagai
training loop. Sisanya sudah jadi: gradient check di lima titik, konvergensi
dari tiga titik awal, sapuan learning rate, dan pembanding `np.linalg.lstsq`.

### Kunci jawaban diverifikasi

Implementasi pembanding dijalankan lebih dulu supaya angka di soal bukan
tebakan. Yang terverifikasi:

- Gradient check lolos di `1e-11` sampai `1e-12`, jauh di bawah target `1e-6`
- Konvergen ke `w = 3.018114`, `b = 1.743558` dari `(0,0)`, `(-5,10)`, dan
  `(100,-100)`, ketiganya sama sampai enam angka di belakang koma
- Cocok dengan `lstsq` sampai `0.00e+00` untuk `w` dan `2.66e-15` untuk `b`
- Rata-rata residu di optimum `-2.84e-16`, dan garis lewat titik pusat massa
  data tepat di `y` rata-rata `2.806923`
- `A = 7.8435`, eigen Hessian `1.9638` dan `15.7233`, bilangan kondisi `8.01`
- `lr` kritis ramalan `2/lambda_max = 0.1272`. Terukur: `0.12` konvergen,
  `0.13` divergen. Ramalan dan pengukuran cocok.

### Temuan yang mengubah soal

Sapuan `h` pada beda hingga memberi hasil yang melawan aturan umum. Galat
relatif di `h = 1e-1` justru `0.000e+00`, sementara di `h = 1e-11` membengkak
jadi `8.2e-06`. Tidak ada kompromi optimum di tengah.

Sebabnya: beda pusat punya galat pemotongan `(h^2/6) f'''`, dan MSE terhadap
`w` adalah polinomial derajat dua persis, seperti yang sudah dibuktikan sendiri
di Soal 4a Hari 3. Turunan ketiganya nol, jadi galat pemotongannya nol untuk
`h` sebesar apa pun. Yang tersisa cuma galat pembulatan, dan itu membesar saat
`h` mengecil.

Jadi anjuran "pakai h = 1e-5" adalah menara bambu di sesi ini. Ia tetap
anjuran yang benar mulai Bulan 1, saat ReLU membuat turunan ketiga tidak nol
lagi. Ini jadi Soal 3.

### Koreksi tolok ukur

Bulan-0-Harian.md menulis kriteria selesai `w -> 3` dan `b -> 2`. Itu tidak
tepat. Gradient descent mencari dasar permukaan loss, dan dasarnya ada di
`w = 3.018`, `b = 1.744`, bukan di parameter yang membangkitkan data. Selisih
`b` sebesar 0,256 itu sekitar 1,2 kali `sigma/akar(n) = 0.212`, jadi wajar.
Kriterianya diperbaiki, dan bedanya dijadikan Soal 4.

### Modul.md ditulis ulang pemilik

Pemilik menulis ulang `Modul.md` dengan suaranya sendiri, dari 857 baris jadi
148 baris. Sepuluh bagian dan kamus fisika tetap ada. Yang hilang: catatan
"di mana analoginya rusak" dan blok "tanya diri sendiri" di tiap bagian.
`Modul.pdf` dibangun ulang mengikuti versi baru.

---

## Sesi A diperiksa, Sesi B disiapkan · 20 Agustus 2026

### Pemeriksaan jawaban Sesi A

Delapan tanda gradien di Soal 1 benar semua, termasuk titik C dan D yang
gradiennya kecil dan tandanya tidak kentara. Soal 3 tentang turunan ketiga
nol, Soal 4a sampai 4c, dan Soal 6 semuanya benar.

Dua hal meleset.

**Soal 4d, verifikasi dipakai menggantikan bukti.** Soal meminta pembuktian
aljabar bahwa garis optimum lewat titik pusat massa. Jawabannya menunjuk ke
keluaran program yang menunjukkan angkanya cocok. Itu bukti untuk satu
dataset dengan satu seed, bukan bukti untuk data apa pun. Buktinya cuma tiga
baris dari `dMSE/db = 0`. Dijadikan Soal 0a Sesi B.

**Soal 5b, nilai populasi dipakai di tempat nilai sampel.** `A = 8.33` itu
`E[x^2] = 25/3` untuk sebaran seragam di `[-5, 5]`, bukan `(1/n) sum x^2`
dari dataset yang nilainya `7.8435`. Ramalannya jadi `0.120`, seharusnya
`0.1275`.

Kesimpulan "ramalan akurat tanpa meleset" tidak tertopang, karena sapuan `lr`
di Sesi A langkahnya `0.12` lalu `0.13`, dan kedua ramalan sama-sama jatuh di
celah itu. Pengukurannya tidak cukup teliti untuk memisahkan keduanya.

### Uji pembeda dijalankan

Sapuan halus antara `0.119` dan `0.130` dijalankan untuk memisahkan ketiga
ramalan:

| ramalan | nilai | hasil |
|---|---|---|
| `1/A` populasi | `0.120000` | salah, `0.121` sampai `0.127` masih konvergen |
| `1/A` sampel | `0.127493` | sedikit ketinggian |
| `2/lambda_max` Hessian 2D | `0.127200` | tepat di dalam jepitan |

Batas terukur ada antara `0.127` dan `0.1272`. Ramalan Hessian meleset di
bawah 0,2 persen. Yang 1D ketinggian karena mengabaikan elemen luar diagonal
Hessian yang bernilai `0.7047`, dan elemen itu nol cuma kalau `x` rata-rata
nol persis.

Ini kali ketiga nilai populasi dipakai menggantikan nilai sampel, setelah
Soal 3e Hari 3 dan Soal 4b Sesi A. Dijadikan Soal 0b dan 0c Sesi B.

### Sesi B disiapkan

`notebooks/sesiB_lanskap.py` dan `notebooks/soal-sesiB.md`. Tiga TODO:
`permukaan_loss` versi loop, `sumbu_utama` untuk Hessian dan eigen, serta
`permukaan_loss_vektor` versi broadcasting sebagai lanjutan Hari 2.

Enam bagian: kisi permukaan, plot 3D linear dan log, lintasan di atas kontur
untuk tiga `lr`, sumbu utama dari vektor eigen, animasi GIF, dan sapuan `lr`
halus.

Angka yang terverifikasi dengan menjalankan versi terisi:

- Versi vektor 17,7 kali lebih cepat dari versi loop, hasil identik
- Hessian `[[15.6871, 0.7047], [0.7047, 2.0]]`, eigen `1.9638` dan `15.7233`
- Determinan Hessian `30.8776`, sama dengan `4 * var(x)`, jadi irisannya elips
- Bilangan kondisi `8.0065`
- Panjang lintasan 60 iterasi: `5.74` di `lr=0.01`, `7.59` di `0.06`,
  `63.41` di `0.12`
- Faktor pengali galat arah curam: `+0.843`, `+0.057`, `-0.887`
- Ambang munculnya gergaji `1/lambda_max = 0.0636`
- Animasi GIF 80 bingkai selesai dalam 16 detik

### Keadaan ketiga di sapuan lr

Di `lr = 0.1272` persis, loss berhenti di `77.1` setelah 3000 iterasi. Tidak
meledak, tapi juga tidak turun ke dasar `1.2903`. Label status awalnya cuma
dua keadaan dan menyebut ini konvergen, dan itu salah. Diperbaiki jadi tiga
keadaan: konvergen, berayun tetap, divergen.

Sebabnya faktor pengali galat bernilai tepat `-1` di titik itu, jadi
amplitudonya tidak pernah berubah. Osilator tanpa redaman sama sekali.
Dijadikan Soal 5b dan 5c.

### Panah sumbu utama diperbaiki

Panah arah curam awalnya terlalu pendek dan tertimpa lintasan, jadi rasio
kedua sumbu tidak terbaca. Skalanya dinaikkan dan `zorder`-nya ditaruh di
atas lintasan. Diperiksa dengan melihat gambarnya, bukan dengan menganggap
kodenya benar.

---

## Berikutnya

**Sesi B dikerjakan pemilik.** Tiga TODO diisi, dua utang Sesi A dilunasi,
sepuluh kotak tolok ukur dituntaskan.

**Sesi C setelahnya, multivariat dan overfitting.** Perluas ke `X` berbentuk
`(n, d)` dalam bentuk matriks penuh, pasang polinomial derajat 1, 3, 9, dan 15
ke data sedikit, pisahkan train dan test, lalu tambahkan suku L2.
