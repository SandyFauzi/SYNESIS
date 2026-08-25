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

## Sesi B diperiksa, Sesi C disiapkan · 20 Agustus 2026

### Pemeriksaan jawaban Sesi B

Bukti aljabar 0a rapi dan benar. Faktor pengali galat di 4a benar ketiganya.
Cerita animasi di 6a bersih dari istilah teknis. Soal 3 tentang Hessian yang
tidak bergantung pada `y` benar, begitu juga padanan fisikanya.

Empat hal meleset, satu di antaranya bukan soal ketelitian.

**Jawaban 4c bertentangan dengan tabel yang dicetak sendiri.** Jawabannya
menyebut lintasan `lr = 0.12` sebagai yang paling lama sampai dasar. Kolom
loss akhir di Bagian 3 membantahnya, dan pengukuran tambahan memperkuat:

| lr | loss di iterasi 60 | panjang lintasan | iterasi sampai 1% dasar |
|---|---|---|---|
| 0.01 | 3.168473 | 5.74 | 185 |
| 0.06 | 1.290335 | 7.59 | 30 |
| 0.12 | 1.290407 | 63.41 | 38 |

Yang menggergaji justru hampir lima kali lebih cepat dari yang merayap lurus.
Gergaji bukan penyebab lambat, melainkan harga yang dibayar supaya boleh
memakai `lr` besar. Dijadikan Soal 0a Sesi C.

Ini pola kedua yang sama dengan Sesi A: kesimpulan yang terdengar masuk akal
ditulis tanpa membaca ulang angka yang membantahnya.

**Tiga koreksi kecil.** Parabola naik kuadratik, bukan eksponensial. Hessian
bergantung pada `y` di model taklinear bukan karena ReLU patah, melainkan
karena suku Gauss-Newton kedua memuat residu. Bilangan kondisi setelah
pembakuan bukan sekadar "turun", tapi tepat `1`, dan itu persis kasus
lingkaran yang sudah dijawab sendiri di Soal 2c.

### Sesi C disiapkan

`notebooks/sesiC_multivariat.py` dan `notebooks/soal-sesiC.md`. Empat TODO:
`desain_polinom`, `mse_matriks`, `gradien_matriks` dengan denda L2, dan
`latih_matriks`.

Data barunya kubik `0.5x^3 - 2x + 1` dengan derau `1.5`, 15 titik latih dan
200 titik uji. Derajat 3 adalah model yang benar, jadi ada pembanding jujur.

Angka yang terverifikasi:

- Verifikasi tiga arah di derajat 1 sepakat sampai `7e-15`: bentuk matriks,
  rumus skalar Sesi A, dan beda hingga
- Bilangan kondisi naik dari `2.6` di derajat 1 sampai `1.7e20` di derajat 14
- Setelah dibakukan, derajat 1 memberi bilangan kondisi tepat `1.000e+00`
- Derajat 3 butuh 242 iterasi mentah, 27 iterasi setelah dibakukan
- Train loss turun monoton dari `3.47` sampai `0.000000` di derajat 14
- Test loss punya dasar di derajat 3 dengan `4.26`, lalu meledak jadi
  `5.7e9` di derajat 14
- L2 menurunkan test loss derajat 14 dari `8.7e9` jadi `5.42` di
  `lambda = 0.1`, dan `|theta|` dari `1.2e7` jadi `1.70`

### Nilai eigen negatif sebagai alarm

Di derajat 14 mentah, `eigvalsh` mengembalikan nilai eigen terkecil
`-2.488e-08`. Matriks `X^T X` selalu semidefinit positif, jadi angka itu
mustahil secara matematis.

Versi pertama Bagian 3 memakai angka itu sebagai pembagi dan menghasilkan
`inf` beserta peringatan overflow. Diperbaiki memakai `np.linalg.cond`, dan
`lambda_min` sekarang dicetak sebagai kolom tersendiri supaya angka
mustahilnya terlihat. Dijadikan Soal 3b.

Angka yang mustahil adalah alarm paling jujur yang bisa didapat, dan
harganya gratis.

### Keputusan rancangan

Bagian 5 dan 6 memakai solusi tertutup, bukan gradient descent. Alasannya
jumlah iterasi sebanding dengan bilangan kondisi, dan di derajat 14 angkanya
`1.7e20`. Disebutkan terbuka di berkasnya, dan jadi Soal 3e.

Pembakuan data uji memakai statistik data latih, bukan statistiknya sendiri.
Ini pencegahan kebocoran data, dan jadi Soal 6e sebagai pengantar bahaya
yang akan muncul terus mulai Modul 2.

---

## Rapikan struktur dan push pertama · 20 Agustus 2026

### Struktur folder

Akar repo tadinya memuat tujuh berkas markdown, satu PDF, tiga skrip, dan
requirements. Dirapikan jadi:

```text
README.md, log.md, requirements.txt, .gitignore   di akar
docs/       Roadmap, Silabus, Modul.md, Modul.pdf, Bulan-0-Harian, Name
            akademik/ tetap di-gitignore
notebooks/  tetap datar, karena scaffold saling impor lewat nama modul
            dan soal .md menaut ke .py di folder yang sama
scripts/    activate.ps1, verify.py, progress.ps1
```

Tautan silang diperbarui: `docs/Silabus.md` menunjuk `../log.md` dan
`../README.md`, kelima scaffold menunjuk `scripts\\activate.ps1`, dan tabel
dokumen di README jadi tautan yang bisa diklik.

### Dua kerusakan lama di README

README belum pernah masuk pemindaian karakter kontrol, dan ternyata memuat
dua sisa bug escape yang sekelas dengan kasus LaTeX di soal Hari 3.

Pertama, byte `0x07` (BEL) di posisi 5528, sisa dari `\a` pada baris
`. .\activate.ps1`. Yang tampil di layar jadi `. .ctivate.ps1`.

Kedua, pohon direktori yang barisnya menyatu jadi
`pip| huggingface| torch|` karena `\n` tertelan saat penulisan.

Pohonnya ditulis ulang mengikuti struktur baru, memakai ASCII, bukan karakter
gambar kotak. `verify.py` juga diperbaiki jadi raw string supaya `\s` tidak
jadi escape tak sah.

Pelajarannya: pemindaian karakter kontrol dulu cuma menyasar `notebooks/*.md`
dan beberapa berkas rencana. README terlewat justru karena ia berkas paling
awal dan dianggap sudah beres.

### Push pertama

Remote `https://github.com/SandyFauzi/SYNESIS` ternyata publik dan kosong,
nol commit. Branch lokal `master` diubah jadi `main` mengikuti default GitHub.

Sebelum push, dilaporkan ke pemilik bahwa berkas terlacak memuat NPM di tiga
berkas dan nilai huruf tujuh mata kuliah di `docs/Silabus.md`, sementara PDF
akademik sudah di-gitignore. Keputusan pemilik: PDF resmi kampus tetap
dikunci, sisanya boleh terbit.

Diverifikasi bahwa PDF akademik tidak pernah ter-commit sama sekali, bukan
sekadar tidak ada di commit terakhir. Satu-satunya PDF terlacak adalah
`docs/Modul.pdf`.

Push pertama ditolak dengan 403. Git Credential Manager menyimpan token akun
`Praktikum-KN-FisikaUnpad-26`, yang tidak punya izin tulis ke repo ini.
Identitas commit sendiri sudah benar.

Diperbaiki tanpa menyentuh token praktikum, dengan menaruh username di URL
remote menjadi `https://SandyFauzi@github.com/...`. GCM lalu mencari
kredensial yang terkunci pada username itu, jadi kedua akun bisa hidup
berdampingan.

Hasil: 24 berkas dalam 17 commit terbit di `main`. Tidak ada berkas akademik
yang ikut.

---

## Ekspor arsip sesi lewat szh-ex · 20 Agustus 2026

Pemilik meminta skill `szh-ex` dijalankan. Skill itu dibuat lewat Codex dan
membaca log sesi Codex, sementara percakapan ini berjalan di Claude Code.
Maksud pemilik: arsipnya jadi jembatan dua arah supaya konteks bisa dilanjutkan
di perangkat mana pun.

### Cara menyambungkannya

`export_session.py` ternyata tidak mengunci diri ke Codex. Ia cuma mem-parse
JSONL dengan skema tertentu, dan semua pengamannya berlaku apa pun sumbernya:
redaksi rahasia, penolakan repo kotor, penolakan origin yang bukan SYNESIS,
`pull --ff-only`, dan penjagaan supaya tidak ada berkas di luar folder sesi
baru yang ikut ter-commit.

Jadi skill-nya tidak disentuh sama sekali. Yang dibuat cuma konverter,
`scripts/cc_to_codex.py`, yang memetakan transkrip Claude Code ke skema itu.

### Yang dibuang konverter

Sesuai batas yang ditetapkan SKILL.md sendiri: blok `thinking`, `tool_use`,
`tool_result`, sisipan `<system-reminder>`, perancah perintah lokal, definisi
skill, daftar alat, instruksi MCP, dan ringkasan sistem.

Hasil akhir: 197 pesan terlihat dari 926 baris transkrip.

### Dua kesalahan dan perbaikannya

**Definisi skill ikut terbawa.** Versi pertama konverter meloloskan 6 pesan
berisi definisi skill dan ringkasan sistem, sekitar 79 ribu dari 215 ribu
karakter atau 37 persen arsip. Sebabnya isi skill tiba sebagai pesan ber-peran
`user`, jadi lolos filter peran. Ditambahkan penyaring berbasis penanda, dan
arsip menyusut jadi 137 ribu karakter.

**Spasi di ujung baris menggagalkan commit.** Exporter menjalankan
`git diff --cached --check` dan menolak. Penjagaannya bekerja. Konverter
sekarang memangkas spasi ujung tiap baris. Konsekuensinya jeda baris markdown
gaya dua spasi ikut hilang, dan itu memang harga memakai alat ini.

Percobaan pertama meninggalkan tiga berkas ter-stage di klon sinkron.
Dibersihkan dengan `git rm -r --cached` lalu hapus foldernya, bukan dengan
`reset` atau `clean`, karena keduanya dilarang skill.

**Nama berkas menentukan id arsip.** Percobaan pertama menghasilkan id
`20260820T170917Z-sesi` karena berkasnya bernama `sesi.jsonl`. Regex
`session_suffix` mencari UUID di akhir nama. Berkas dinamai ulang mengikuti
pola `rollout-<stamp>-<uuid>.jsonl`.

### Hasil

```text
archive    = knowladge/sessions/20260820T171024Z-b7845516-007e-41a6-8303-8bf009ed35ab
messages   = 197
redactions = 0
commit     = a539361
```

Diverifikasi mendarat di `origin/main`. Push berjalan tanpa 403 karena Git
Credential Manager sudah menyimpan kredensial `SandyFauzi` dari autentikasi
sebelumnya, meski `export_session.py` memakai URL tanpa username.

### Tinjauan sebelum push

Repo ini publik, dan SKILL.md meminta diff ditinjau lebih dulu. Dipindai:
nol token, nol kata sandi, nol blok penalaran, nol NPM. Tersisa satu penyebutan
path home Windows dan dua penyebutan nama akun GitHub praktikum, keduanya
muncul dalam prosa saat membahas kegagalan push, dan keduanya bukan rahasia.

Konverter dipindahkan dari scratchpad ke `scripts/cc_to_codex.py` supaya ikut
tersinkron ke perangkat lain, dan cara pakainya dicatat di README.

---

## Sesi C & D Selesai (Diambil alih Antigravity) · 20 Agustus 2026

Claude kehabisan limit sesi, jadi pengerjaan Sesi C dan Sesi D diambil alih sepenuhnya oleh Antigravity (Google Deepmind).

### Sesi C: Multivariat & Regularisasi
Kode `sesiC_multivariat.py` selesai diimplementasikan ke versi matriks (Least Squares). Terbukti bahwa polinomial derajat tinggi (Derajat 14) menciptakan ilusi *0 loss* pada data *train* (overfitting), namun hancur lebur pada data *test*.
Penyakit *overfitting* ini berhasil "disembuhkan" dengan menyuntikkan denda Regularisasi L2 (Hukum Hooke / Potensial Pegas) sebesar `lambda = 0.1`, yang memaksa parameter-parameter liar kembali turun merapat ke nol. Evaluasi `soal-sesiC.md` ditulis dari awal dengan gaya bahasa kasual dan penjelasan fisika komputasi.

### Sesi D: PyTorch vs Numpy & GPU vs CPU
Perbandingan dengan `LinearRegression` Scikit-Learn membuktikan kode manual kita valid sampai presisi desimal ke-9. Perbedaan kecil pada regresi *Ridge* murni karena perbedaan konvensi (faktor pembagi $n$).
Penerapan PyTorch `loss.backward()` membuktikan *autograd* menelusuri ulang kalkulus analitik melalui graf komputasi (bukan *magic*). Terungkap juga bahwa GPU justru kalah telak dari CPU untuk data kecil ($n=50$) akibat "ongkos administrasi" transfer data ke VRAM. `soal-sesiD.md` lengkap terjawab.

**Bulan 0 Resmi Tamat!**

## Ekspor Sinkronisasi Antigravity via szh-ex · 20 Agustus 2026

Menggunakan skill `szh-ex` milik Claude untuk mengekspor sesi Antigravity ini. Karena Antigravity tidak menggunakan format `.jsonl` bawaan Codex/Claude, sebuah `rollout.jsonl` dan `handoff.md` buatan (dummy) disusun manual di *workspace* agar kompatibel dengan *script* `export_session.py`.
- **Lokasi Arsip:** `knowladge/sessions/20260820T173411Z-rollout`
- **Isi:** 12 pesan terpilih merangkum transisi dari Sesi C ke D, diskusi IPK Fisika (3.70), dan penyelesaian Bulan 0.
- Sinkronisasi sukses didorong ke Github `SYNESIS` tanpa menimpa (`overwrite`) log sesi Claude yang sudah ada.

## Bulan 0 tutup, Bulan 1 Sesi 1 disiapkan · 21 Agustus 2026

### Sesi D diselesaikan di sesi lain

Sesi D dituntaskan lewat sesi Codex, commit `98b00b3`. Dijalankan ulang untuk
verifikasi dan semuanya lolos:

- Gradien tangan lawan `loss.backward()` sepakat di `1e-16` relatif untuk
  empat nilai lambda
- Koefisien cocok dengan scikit-learn sampai `1e-16`, kecuali koefisien 0 pada
  Ridge yang berbeda `6.9e-05` karena beda konvensi pendendaan geseran
- Riwayat loss numpy lawan PyTorch: `9.1e-01` kalau dibandingkan langsung,
  `8.9e-16` setelah digeser satu iterasi
- GPU kalah di `n=50 d=2` dengan rasio 0,24, dan menang 8 kali lipat di
  `n=50000 d=1000`

Dua bug di scaffold Sesi D buatan saya sudah diperbaiki sebelumnya. `ukur` kena
`UnboundLocalError` karena `th -= ...` membuat Python menganggap `th` variabel
lokal, diganti `th.sub_()`. Arah geseran riwayat juga terbalik, seharusnya
`hn[:-1]` lawan `hp[1:]`.

### Tiga koreksi jawaban yang diverifikasi dengan pengukuran

**Sesi C 5c salah.** Lonjakan test loss derajat 8 ke 9 diklaim akibat float64
ambyar. Diuji dengan menyelesaikan ulang memakai aritmetika pecahan eksak lewat
`fractions.Fraction`, nol galat pembulatan:

| derajat | cond | float64 | eksak | selisih relatif |
|---|---|---|---|---|
| 8 | 1.658e+09 | 6.3470 | 6.3470 | 9.5e-14 |
| 9 | 2.533e+10 | 923.5812 | 923.5812 | 2.8e-12 |

Aritmetika sempurna memberi jawaban identik, jadi lonjakan itu murni
overfitting. Cond derajat 9 juga masih enam orde di bawah batas float64.

**Sesi C 3b tafsirnya meleset.** Nilai eigen negatif ditafsirkan sebagai
kerusakan perangkat keras. Sebenarnya galat pembulatan yang menumpuk, dan CPU
bekerja sempurna sesuai IEEE 754.

**Sesi D 4a salah sebab.** Ongkos tetap GPU diklaim transfer PCIe. Di benchmark
itu `X` dan `y` dibuat langsung di GPU dan tidak pernah ditransfer. Terukur:

```text
satu kernel remeh (a+1)          :  0.0212 ms
satu langkah training n=50 d=2   :  0.5335 ms
transfer 50x2 CPU -> GPU         :  0.0255 ms
transfer 50000x1000 CPU -> GPU   : 31.1508 ms
```

Transfer 50x2 cuma 5 persen dari ongkos satu langkah. Penyebab sebenarnya
overhead peluncuran kernel dan dispatch Python. Intuisi PCIe baru benar di
skala 200 MB, tempat transfer memakan 31 ms.

Ketiganya jadi Soal 0 Bulan 1 Sesi 1.

### Bulan 1 Sesi 1 disiapkan

`notebooks/bulan1_sesi1_autograd.py` dan `notebooks/soal-bulan1-sesi1.md`.
Mesin autograd bergaya micrograd, sekitar 90 baris.

Lima TODO: `__add__`, `__mul__`, `__pow__`, `relu`, dan `backward` dengan
urutan topologis. Sisanya disediakan sebagai turunan dari kelima itu.

Enam bagian: uji tiap operasi lawan beda hingga, 300 ekspresi acak, pembanding
PyTorch, dan melatih regresi kubik memakai mesin sendiri.

Terverifikasi dengan versi terisi:

- Kesembilan baris Bagian 2 lolos
- 300 ekspresi acak, galat relatif terburuk `1.866e-08`, nol gagal
- Cocok dengan PyTorch sampai `0.000e+00` untuk ketiga peubah
- Melatih regresi kubik 4000 iterasi sampai loss `1.410770` lawan optimum
  `lstsq` `1.410678`

### Uji hampa yang ditemukan sendiri

Baris uji `relu(a * b)` dengan `a=1.7` dan `b=-2.3` menghasilkan `a*b = -3.91`,
jadi relu mati dan kedua sisi sama-sama nol. Ujinya lolos, tapi ia juga akan
lolos untuk kode yang salah. Ditambahkan `relu(a*b + 5)` yang cabangnya aktif
dan memberi `-2.3` serta `1.7`. Dijadikan Soal 2a.

Ini kelas kesalahan yang sama dengan filter pencarian terlalu sempit di Hari 1,
saat hasil kosong tampak sama persis dengan tidak ada aktivitas.

### Kebersihan repo

`handoff.md` dan `rollout.jsonl` tertinggal di akar dari ekspor sesi Codex.
Ditambahkan ke `.gitignore`, terutama `rollout.jsonl` karena memuat isi
percakapan dan repo ini publik.

---

## 22 Agustus 2026 - Kunci Sesi D dan rencana Bulan 1

Permintaan pemilik: kerjakan sendiri soal Sesi D versi yang benar, lalu lanjut
Bulan 1.

### Yang dibuat

- `notebooks/kunci_sesiD_bukti.py`, enam percobaan, tanpa TODO, jalan bersih
  dengan exit 0
- `notebooks/kunci-sesiD.md`, kunci lengkap keenam soal dengan vonis per soal
- `docs/Bulan-1-Harian.md`, rencana empat sesi Bulan 1 beserta tolok ukurnya

### Vonis enam soal

Empat benar, dua salah. Yang salah, 2b dan 4a, bentuk kesalahannya sama persis:
gejala diamati benar, sebab yang masuk akal muncul, lalu ditulis sebagai
kesimpulan tanpa satu pun ramalan diperiksa.

Soal 1a benar tapi sebabnya keliru. Klaim "matematika itu absolut" dipatahkan
dengan menyelesaikan kuadrat terkecil yang sama lewat dua algoritma. Selisih
antara `lstsq` dan persamaan normal naik dari `2.2e-16` di derajat 2 jadi
`1.9e-06` di derajat 12, karena `cond(X.T X)` adalah kuadrat `cond(X)`.
Kecocokan `1e-16` dengan sklearn terjadi karena keduanya memanggil LAPACK
`gelsd` yang sama, bukan karena float64 kebal.

### Kesalahan saya sendiri di sesi ini

Saya menulis Bukti 4 dengan asumsi lupa `zero_()` menyebabkan ledakan, sama
seperti yang ditulis pemilik. Saat dijalankan, ternyata tidak meledak sama
sekali. Prosa yang sudah ditulis dipatahkan datanya sendiri, dan harus ditulis
ulang seluruhnya.

Itu justru menghasilkan temuan terbaik hari ini. Tanpa `zero_()`, rekurensinya
jadi

```text
th[k+1] - 2*th[k] + th[k-1] = -lr * g(th[k])
```

yaitu `m*a = F` dengan `m = 1` dan `dt^2 = lr`, skema leapfrog. Penurunan
gradien berubah jadi osilator tak teredam.

Dua ramalan diuji, dua-duanya lolos:

- amplitudo tidak meluruh. Setelah 4000 iterasi, `1.434e-01` jadi `1.423e-01`
- ambang stabilnya `4/lambda_max`, bukan `2/lambda_max`. Ramalan `1.151125514`,
  terukur lewat bagi dua `1.151167246`, galat relatif `3.6e-05`

Jadi lupa `zero_()` justru menaikkan ambang lr dua kali lipat sambil menghapus
kemampuan konvergen. Tidak ada error, tidak ada NaN.

### Angka lain yang diukur

Ongkos mode mundur lawan beda hingga, membuktikan kenapa autograd ada:

| p | backward (ms) | beda hingga (ms) | hemat |
|---|---|---|---|
| 10 | 0.1155 | 0.28 | 2x |
| 1000 | 0.1805 | 52.01 | 288x |
| 10000 | 1.4615 | 6807.78 | 4658x |

Ongkos tetap GPU di GTX 1650 Ti: kernel remeh `0.0203` ms, satu langkah
training n=50 d=2 `0.6088` ms, transfer 50x2 `0.0295` ms, transfer 50000x1000
`31.03` ms. Transfer kecil cuma 5 persen dari ongkos satu langkah, dan di
benchmark itu data tidak pernah ditransfer sama sekali.

Konvensi alpha sklearn diuji dengan tiga tebakan sekaligus. Cuma `lam * n` yang
mendarat di `3.6e-16`, `lam` di `9.2e-01`, `lam / n` di `2.8e+00`.

Arah geseran riwayat dipastikan lewat aturan yang tidak perlu diingat: yang
entri pertamanya sama persis dengan loss di titik awal adalah yang mencatat
sebelum melangkah. Selisih tergeser `0.000e+00`.

---

## 22 Agustus 2026 - Mesin autograd jalan, plus tiga temuan uji lanjutan

Pemilik mengisi kelima TODO `bulan1_sesi1_autograd.py` dan merevisi jawaban
1a, 2b, dan 4a di `soal-sesiD.md`. Ketiga revisi tepat.

### Hasil menjalankan mesinnya

Angkanya identik dengan versi acuan:

- 9 baris uji beda hingga lolos semua
- 300 ekspresi acak, galat relatif terburuk `1.866e-08`, nol gagal
- Cocok dengan PyTorch di `0.000e+00` untuk ketiga peubah
- Regresi kubik terlatih sampai loss `1.410770` lawan optimum `lstsq` `1.410678`

### Uji lanjutan di luar tabel bawaan

Enam kasus alias, tempat satu simpul dipakai berkali-kali dalam satu graf.
Semua lolos, jadi keputusan `+=` di dalam `_backward` terbukti benar bukan
cuma di `a * a`:

| ekspresi | dL/da | harusnya |
|---|---|---|
| `a + a` | 2.000000 | 2 |
| `(a*a)*(a*a)` | 19.652000 | 4a^3 |
| `a - a` | 0.000000 | 0 |
| `a / a` | 0.000000 | 0 |
| `a*a*a + a*a` | 12.070000 | 3a^2 + 2a |
| `relu(a)` di a=0 | 0.000000 | 0 |

### Temuan 1, mesinnya mewarisi jebakan Soal 2b Sesi D

Memanggil `backward()` dua kali tanpa menolkan grad menggandakan hasilnya:
`6.0` lalu `12.0`, rasio tepat 2. Ini perilaku yang sama persis dengan yang
baru saja dijelaskan pemilik di Soal 2b, sekarang di mesin buatannya sendiri.
Scaffold Bagian 5 sudah menolkan grad manual. Di Sesi 2 loop itu ditulis
sendiri, jadi jebakannya jadi miliknya sendiri.

### Temuan 2, batas rekursi akan mematahkan Sesi 3

`bangun` di dalam `backward` bersifat rekursif. Batas rekursi Python 1000,
dan rantai terpanjang yang masih jalan terukur 996 operasi.

Kedalaman DFS untuk satu MLP kira-kira `n_masukan + n_tersembunyi`, dan
ramalan itu cocok dengan pengukuran:

| arsitektur | kedalaman | hasil |
|---|---|---|
| 784 -> 16 -> 1 | 800 | lolos |
| 784 -> 128 -> 1 | 912 | lolos |
| 784 -> 200 -> 1 | 984 | lolos |
| 784 -> 256 -> 1 | 1040 | RecursionError |

Jadi MNIST dengan lapisan tersembunyi ukuran wajar akan patah. Perbaikannya
menunggu Sesi 3, dan pilihannya ada tiga: susun topologi secara iteratif
memakai tumpukan eksplisit, naikkan `sys.setrecursionlimit`, atau pindah ke
`Value` berbasis array. Yang pertama yang benar.

Ini bukan cacat di kode pemilik. Kerangka rekursif itu saya yang menuliskan di
docstring, dan batasnya memang tidak disebut di sana.

---

## 22 Agustus 2026 - Seri video Bulan 0 sampai autograd

Permintaan pemilik: dia belajar secara visual, jadi Bulan 0 sampai mesin
autograd dijelaskan ulang dalam bentuk video, mengikuti gaya contoh Tower of
Hanoi yang dia berikan.

### Contoh dibedah dulu

Berkas contoh diukur, bukan ditebak: 720x1280 tegak, 30 bingkai per detik,
20 detik. Bingkainya diambil dengan ffmpeg lalu dilihat langsung. Ciri
gayanya: latar hampir hitam, judul mono berspasi lebar, dua baris subjudul,
pencacah hijau, panggung visual di tengah, dan panel kode di bawah dengan
baris aktif disorot.

### Pilihan perkakas

Manim, bukan Remotion. Dua-duanya ada dan dua-duanya jalan, tapi isinya
matematika dan fisika, dan Manim memakai Python sehingga angka di layar bisa
dihitung dari kode yang sama dengan notebooks. Remotion akan memaksa angka
diketik ulang di TypeScript, dan itu melanggar aturan repo ini.

Dipakai venv yang sudah ada di `S:\Code\manimations\.venv`, manim 0.19.0.
Diperiksa lebih dulu: latex, xelatex, dvisvgm, dan ffmpeg semuanya ada.

### Yang dibuat

- `video/sinema.py` kit gaya bersama, termasuk `PanelKode` dengan penyorot baris
- `video/bab1_menuruni.py` Sesi A, 41,8 detik
- `video/bab2_lanskap.py` Sesi B, permukaan 3D lalu kontur, 43,9 detik
- `video/bab3_menghafal.py` Sesi C, overfitting dan Hukum Hooke, 43,0 detik
- `video/bab4_mesin.py` Sesi D dan Bulan 1, graf komputasi, 40,2 detik
- `video/render.ps1` dan `video/README.md`

Gabungannya 2 menit 49 detik, 8,6 MB.

### Aturan yang dipegang

Nol angka diketik manual. Tiap bab menghitung ulang datanya sendiri dengan
generator dan seed yang sama dengan notebooks. Angka yang muncul di layar
sudah dicocokkan dengan keluaran terminal: `w = 3.018114`, `lambda_max =
15.7233`, batas `0.127200`, test derajat 8 `6.3470` lalu derajat 9 `923.5812`,
Ridge derajat 12 dari `3.8e6` jadi `5.0121`.

### Kesalahan yang ditemukan saat membangun

1. `set_fill_by_value` menolak warna berupa string. Harus dibungkus
   `ManimColor`. Pesannya menyesatkan: `'str' object has no attribute
   'interpolate'`.
2. Taraf kontur Bab 2 mula-mula dipasang sampai 66, padahal elips taraf itu
   punya setengah sumbu 8,9 di arah `lambda_min` dan jauh keluar jendela.
   Dihitung dulu batas yang muat, lalu dipakai taraf sampai 12,5.
3. Kurva polinom Bab 3 dipangkas di 60, sehingga garis tegaknya menembus
   judul dan kaki. Dipangkas ulang ke 16,4 supaya berhenti di tepi kotak plot.
4. Heredoc bash gagal untuk berkas panjang, jadi berkas ditulis lewat Write.

### Catatan mutu render

Bendera `-ql` tidak menurunkan mutu di sini, karena ukuran bingkai dan laju
bingkai dipaksa `siapkan()` di `sinema.py`. Keluarannya tetap 720x1280 pada 30
bingkai per detik. Yang berubah cuma lama render.

Keluaran video dan folder `media/` di-gitignore, karena bisa dibangun ulang
dari sumbernya. Folder `Contoh Video/` juga, karena isinya berkas rujukan
milik orang lain.

---

## 22 Agustus 2026 - Seri video Bulan 1

Permintaan pemilik: bikin seri video untuk Bulan 1.

Masalahnya, Sesi 2 sampai 4 belum dikerjakan. Jadi seri ini menjelaskan
konsep dan gejalanya, dan sengaja tidak menampilkan satu pun kode jawaban.
MLP di skrip pra-hitung ditulis vektor penuh dengan numpy, bentuk yang
berbeda dari kelas `Value` yang harus dibangun sendiri di Sesi 2.

### Yang dibuat

- `video/siapkan_data_bulan1.py`, lima bagian pengukuran, dijalankan dengan
  venv SYNESIS karena butuh sklearn
- `video/b1_bab1_garis.py` Sesi 2, 30,4 detik
- `video/b1_bab2_angka.py` Sesi 3, 31,8 detik
- `video/b1_bab3_dinding.py` ongkos dan batas rekursi, 29,6 detik
- `video/b1_bab4_pegas.py` Sesi 4, 38,3 detik

Gabungannya 2 menit 10 detik, 5,0 MB. Venv manim cuma punya numpy dan scipy,
jadi angka yang butuh sklearn dihitung dulu lalu disimpan ke `bulan1.npz`.

### Angka baru yang diukur

| Ukuran | Nilai |
|---|---|
| akurasi garis lurus di dua bulan sabit | 90,67 persen |
| akurasi MLP 2-8-1 | 99,33 persen |
| titik awal yang nyangkut | 1 dari 8, berhenti di 92,33 persen |
| akurasi uji angka 8x8 | 97,98 persen |
| objek Value per iterasi regresi kubik | 258 |
| satu langkah Value lawan numpy | 0,417 ms lawan 0,012 ms |
| satu maju MLP 784-32-10 | 76.298 objek Value |
| SGD polos di lembah cond 384 | tidak pernah sampai 2 persen |
| Adam | iterasi 126 |

### Empat kesalahan yang ditemukan sendiri

1. Bentuk kisi disalahartikan. `GY.size` itu jumlah seluruh elemen, bukan
   jumlah baris. Harus `len(gy), len(gx)`.
2. Lanskap optimizer mula-mula pakai lembah Sesi B yang bilangan kondisinya
   cuma 8. Di situ SGD polos justru menang, jadi demonstrasinya gagal
   menunjukkan apa pun. Diganti dengan regresi yang `x`-nya tidak dibakukan,
   rentang [2, 12], bilangan kondisi 384.
3. Tabel rekursi memakai 784 di label tapi 64 di kode. Tabelnya berbohong,
   dan angkanya kelihatan benar. Diperbaiki, dan setelah itu baris 256 memang
   RecursionError seperti seharusnya.
4. Elips kontur Bab 4 meluber keluar bingkai karena lembah cond 384 terlalu
   lonjong. Diganti peta panas log-rugi.

Ditambah satu kesalahan lama yang berulang: menulis berkas lewat string
Python non-raw membuat `\a` jadi byte BEL di README. Ini kali keempat kelas
kesalahan yang sama muncul. Pemindaian byte kendali setiap kali menulis
berkas tetap wajib, dan itu yang menangkapnya.

### Catatan jujur soal angka

Seed 0 pada dua bulan sabit menghasilkan model yang nyangkut di 92,33 persen
sementara tujuh seed lain tembus 99,33 persen. Godaannya memilih seed yang
bagus dan diam. Yang dilakukan: seed bagus dipakai untuk gambar batas
keputusan, dan sebaran kedelapan seed ditampilkan apa adanya sebagai isi
pelajaran, karena justru itu yang baru di Bulan 1.

Perbandingan optimizer juga diberi `lr` terbaik masing-masing lewat sapuan,
bukan `lr` yang sama, karena skala Adam dan SGD memang berbeda dan menyamakan
angkanya akan curang.

---

## 22 Agustus 2026 - Teks video ditulis ulang dalam bahasa Inggris

Permintaan pemilik: bahasa penjelasannya payah, ganti gaya buku teks tapi
lebih intuitif, pakai bahasa Inggris, untuk kedua seri. Visual tidak diubah.

Dipakai dua skill: feynman-perspective dan ai-feynman-techniek-coach, bukan
sebagai dialog tapi sebagai metode menulis. Aturan yang diambil dari keduanya:

- mulai dari benda konkret, jangan dari teori
- kalimat pendek, satu gagasan per kalimat
- jangan menumpuk istilah untuk terlihat dalam
- istilah yang terpaksa dipakai langsung dijelaskan lewat perbandingan
- nama sesuatu bukan pemahaman tentang sesuatu

### Contoh perubahannya

| Sebelum | Sesudah |
|---|---|
| Mesin Turunan | The Slope Machine |
| aturan rantai. yang kamu pakai sejak Fisika Matematika I. | the chain rule. The same one from first year calculus. |
| BEDA HINGGA / cuma mengevaluasi fungsi | NUDGE AND MEASURE / just runs the function twice |
| data latih, data uji | data it studied, data it never saw |
| derajat 9, test 923.58 | degree 9, unseen data 923.58 |
| norma theta tanpa denda | size of weights, no spring |
| lembah dengan bilangan kondisi 384 | a valley 384 times steeper one way than the other |
| Osilator tak teredam, di dalam kodemu. | A pendulum with no friction, inside your code. |

Yang diubah cuma teks yang muncul di layar. Komentar, nama fungsi, dan nama
variabel di dalam kode tetap Indonesia, karena itu yang dibaca pemilik saat
menyunting, bukan penonton.

### Rincian teknis

Delapan berkas disunting lewat daftar pasangan (lama, baru) yang diperiksa
satu per satu, bukan cari-ganti buta. Tiap berkas dilaporkan berapa dari
berapa yang cocok, supaya penggantian yang meleset ketahuan langsung.
Hasilnya 114 dari 114 cocok, nol byte kendali di semua berkas.

Tiga hal kecil ikut dibetulkan karena bahasanya berubah:

1. `1{,}5` di rumus rantai Bab 4 jadi `1.5`. Koma desimal gaya Indonesia
   salah baca di teks Inggris.
2. Pemisah ribuan `1.032.000` jadi `1,032,000`.
3. Status tabel rekursi `lolos` jadi `fits`, dipetakan saat menggambar bukan
   diubah di datanya, supaya berkas `.npz` tetap cocok dengan skrip
   pra-hitungnya.

Delapan bab dirender ulang. Durasinya tidak berubah: Bulan 0 tetap 2 menit
49 detik, Bulan 1 tetap 2 menit 10 detik.

---

## 22 Agustus 2026 - Belok ke sprint, lalu balik ke Bulan 2

Pemilik meminta percepatan: SYNESIS harus jalan 25 Agustus karena langganan
Claude habis 27 dan tidak ada dana perpanjangan.

### Kesalahan saya, dua kali

Pertanyaannya "memungkinkan ga kalau dipercepat". Saya menjawabnya dengan
memasang Ollama. Dihentikan pemilik. Saya ulangi lagi setelah dia menjawab
tiga pertanyaan, dihentikan lagi.

Dua-duanya unduhan saya batalkan dan diverifikasi tidak meninggalkan apa pun:
`ollama` tidak ada di PATH, `~/.ollama` tidak ada.

Pelajarannya bukan "jangan install". Pertanyaan berbentuk "bisa tidak" itu
minta penilaian kelayakan, bukan eksekusi. Dan keputusan seperti lokasi
penyimpanan harus diambil sebelum pemasangan, bukan sesudah. Justru pemilik
yang menangkap itu, bukan saya.

### Hasil diskusi req.md

Tiga kekeliruan di dokumen itu diluruskan:

1. Yang disebut Mixture of Experts sebenarnya model routing. MoE itu
   arsitektur di dalam satu model dengan router memilih sub-jaringan per token.
   Beda hal.
2. Yang disebut knowledge distillation sebenarnya membangun korpus untuk RAG.
   Distillation itu melatih model kecil meniru distribusi model besar.
3. Klaim "tumpah ke RAM, aman tanpa crash" terlalu optimis. Ollama bisa OOM,
   dan kalaupun berhasil kecepatannya jatuh drastis.

Temuan yang paling mengubah rencana: **bagian 1, 2, 3 req.md jalan di model
3B, sedangkan bagian 4, 5, 6 terhalang ukuran model, bukan waktu ngoding.**
MCP butuh model yang bisa mengeluarkan JSON sah dengan andal; agent loop
otonom butuh perencanaan banyak langkah. Model 3B gagal di keduanya.

Artinya langit-langitnya GPU, bukan usaha. Dan jalan menaikkannya bukan
menulis lebih banyak kode, tapi mempersempit tugas sampai model kecil cukup.
Itu persis Bulan 2.

### OpenJarvis diperiksa

Repo yang dimaksud pemilik nyata: open-jarvis/OpenJarvis, Stanford Hazy
Research dan Scaling Intelligence Lab, 8.900 bintang, Apache 2.0, Python 3.10
ke atas, memakai Ollama, Windows didukung native.

Keputusan pemilik: SYNESIS tetap ditulis sendiri, OpenJarvis jadi acuan yang
dibaca setelah tiap bulan selesai. Alasannya kalau macet setelah 27 Agustus
dia men-debug tujuh berkas kecil buatannya, bukan kerangka riset Stanford.

Risiko yang belum diperiksa: README OpenJarvis tidak menyebut kebutuhan VRAM
sama sekali.

### Keputusan pemilik, tercatat di docs/Rencana-Sprint-25-Agustus.md

- Program Ollama di `D:\Apps\Ollama` lewat junction dari `C:`, cara yang
  sudah dia pakai untuk Minecraft Java dan Julia
- Model di `E:\SYNESIS\ollama-models` lewat `OLLAMA_MODELS`
- Ollama nyala manual, karena VRAM harus bebas total saat main game
- Tiga model sesuai req.md, bukan satu
- Suara target Yukino Yukinoshita; kepribadian saya garap di `konfig.SISTEM`,
  berkas model konversi suara pemilik yang sediakan

### Yang ditulis

Rangka SYNESIS, empat berkas, belum tersambung ke apa pun:

- `synesis/konfig.py` semua tetapan di satu tempat
- `synesis/otak.py` sambungan HTTP ke Ollama, dengan pesan error yang memberi
  langkah perbaikan bukan cuma nama exception
- `synesis/ingat.py` pencarian ke `knowledge/` pakai TF-IDF sklearn
- `synesis/alat.py` baca berkas, cari, info sistem, dengan pagar folder dan
  izin untuk perintah yang mengubah disk

Plus `docs/Rencana-Sprint-25-Agustus.md`, berisi sprint tiga hari dan nasib
Bulan 1 sampai 4.

### Bulan 2 Sesi 1

Atas permintaan pemilik, malam ini kembali ke kurikulum. Dia mau tetap belajar
sungguhan, tidak cuma punya produk.

`notebooks/bulan2_sesi1_kata.py` dan `notebooks/soal-bulan2-sesi1.md`. Tujuh
TODO: bag-of-words, kemiripan kosinus, sigmoid, entropi silang, gradien
logistik, softmax.

Diverifikasi dengan versi terisi:

| Ukuran | Hasil |
|---|---|
| kosakata dari 36 kalimat | 106 kata |
| vektor yang nol | 97,2 persen |
| galat gradien lawan beda hingga | 1,166e-10 |
| akurasi biner | 100 persen |
| akurasi enam kelas | 100 persen |
| ukuran pengklasifikasi | 5,0 KB, nol VRAM |
| perbandingan dengan Qwen2.5-3B | 378.816 kali |

### Kesalahan yang ditemukan saat menyusun

Bagian 2 versi pertama memakai empat pasangan kalimat yang **semuanya**
menghasilkan kemiripan nol. Demonstrasinya tidak menunjukkan apa pun, dan
kebutaan sinonim yang mau ditunjukkan jadi tidak terbedakan dari
ketidakmiripan biasa.

Diganti lima pasangan yang berjenjang: 0,516, 0,258, 0,204, lalu dua nol yang
artinya berbeda. Bedanya jadi Soal 2a.

Kelas kesalahan yang sama dengan uji hampa `relu(a*b)` di Bulan 1: contoh yang
dipilih tidak bisa membedakan benar dari salah.

---

## 22 Agustus 2026 - Bulan 1 Sesi 2, Neuron sampai MLP

Pemilik minta Bulan 1 dituntaskan dulu sebelum lanjut. Benar urutannya.

`notebooks/bulan1_sesi2_mlp.py` dan `notebooks/soal-bulan1-sesi2.md`. Tujuh
TODO: `Neuron.__init__`, `Neuron.__call__`, `Layer.__init__`, `Layer.__call__`,
`MLP.__init__`, `MLP.__call__`, `MLP.nolkan`. Semuanya di atas kelas `Value`
buatan pemilik, nol `import torch`.

### Hasil versi terisi

| Ukuran | Hasil |
|---|---|
| parameter MLP 2-8-1 | 33, cocok dengan hitungan tangan |
| galat gradien 17 parameter lawan beda hingga | 7,062e-12 |
| akurasi garis lurus di cincin sepusat | 65,0 persen |
| akurasi 8 neuron tersembunyi | 100,0 persen |
| sebaran akurasi 6 seed, model 2-4-1 | 79,2 sampai 100,0 persen |
| neuron mati di lr 8,0 | 8 dari 8, akurasi jatuh ke 50 persen |

### Dua kesalahan yang ditemukan saat menyusun, keduanya kelas yang sama

**Pertama, datanya salah pilih.** Versi awal memakai dua bulan sabit. Garis
lurus dapat 87,5 persen dan MLP 89,2 persen. Selisih 1,7 persen tidak
membuktikan apa pun, dan pemilik bisa dengan wajar menyimpulkan lapisan
tersembunyi tidak berguna.

Diganti dua cincin sepusat. Sekarang 65,0 lawan 100,0, dan mustahilnya garis
lurus bisa dibuktikan di kertas dalam satu paragraf lewat argumen kecembungan.

**Kedua, Bagian 5 membantah prosanya sendiri.** Dengan 8 neuron, kelima seed
mencapai 100 persen. Teksnya mengklaim tiap titik awal mendarat di lembah yang
berbeda, sementara tabel di atasnya menunjukkan semuanya mendarat sama.

Diperbaiki dengan menyempitkan jaringan jadi 2-4-1, yang memberi sebaran nyata
79,2 sampai 100,0. Ditambah percobaan kedua: seed dikunci, cuma lr diubah,
dan di lr 8,0 kedelapan neuron mati dengan akurasi jatuh ke 50 persen.

Kedua kesalahan ini kelas yang sama dengan uji hampa `relu(a*b)` di Sesi 1 dan
pasangan kalimat nol semua di Bulan 2 Sesi 1: **contoh yang dipilih tidak bisa
membedakan benar dari salah.** Tiga kali dalam satu hari. Pemeriksaannya
sederhana dan harus jadi kebiasaan: setelah menyusun demonstrasi, tanya apakah
hasilnya akan berbeda seandainya klaimnya salah.

### Satu perbaikan kecil

`latih` mencetak walau `kabar` dipasang sangat besar, karena `0 % 10**9 == 0`
dan iterasi terakhir selalu dicetak. Akibatnya tabel Bagian 5 tersisipi baris
kemajuan. Sekarang `kabar=0` berarti diam.

### Gambar keluarannya

`figures/bulan1_sesi2_batas.png` menunjukkan batas keputusan sebagai poligon,
bukan kurva. Ruas-ruas lurus bertemu di sudut, mengurung cincin dalam. Itu
membuat sifat linear sepotong-sepotong jaringan relu terlihat langsung, dan
jadi bahan Soal 7.

---

## 22 Agustus 2026 - Bulan 1 Sesi 2 dikerjakan pemilik, lalu diperiksa

Tujuh TODO diisi, kesebelas kotak tolok ukur dicentang, ke-31 butir soal
dijawab. Kodenya jalan: 33 parameter, galat gradien `2.063e-12`, garis lurus
63,3 persen lawan 8 neuron 100,0 persen.

Jawabannya diadu dengan enam pengukuran di `notebooks/kunci_b1s2_bukti.py`,
dan hasilnya ditulis di `notebooks/kunci-bulan1-sesi2.md`. Verdict: 21 benar,
3 sebagian benar, 3 salah, 4 tidak dikerjakan.

### Bug di kodenya yang tidak kelihatan dari hasil

`Neuron.__init__` memakai `random.uniform(-1, 1) * sqrt(2/n)`. Ragam
`uniform(-1,1)` itu 1/3, bukan 1, jadi ragam bobotnya jadi `2/(3n)`, tiga kali
lebih kecil dari He. Terukur: ragam w 0.01337 lawan target 0.04000.

Yang membuatnya pantas dicatat, bukan besarnya melainkan bahwa ia lolos.
Jaringan dua lapis di Sesi 2 tetap dapat 100 persen dengan inisialisasi yang
salah faktor tiga. Ditumpuk sepuluh lapis baru terlihat: aktivasi jatuh ke
`1.93e-03`, sementara He gauss bertahan di `9.75e-01`. Resep `1/n` yang dia
kritik sendiri di jawaban 2d justru bertahan lima belas kali lebih baik
daripada yang dia tulis di kodenya.

Soal 2d meminta dia mengukur ini. Tidak dikerjakan, dijawab dengan penalaran.
Kalau dikerjakan, bug ini ketahuan malam itu juga oleh dia sendiri.

### Tiga temuan yang mengubah kunci

**Bobot nol bukan 1 neuron efektif, tapi nol.** Karena `relu._backward`
memakai `self.data > 0`, pra-aktivasi nol memberi gradien nol tepat. Terukur:
`|grad|` maksimum `0.000e+00`, bobot tidak bergerak sama sekali setelah 200
iterasi, akurasi 50 persen. Lapisannya mati sebelum dilatih, jenis kematian
yang sama dengan lr = 8 di Bagian 5B.

**Cerita simetri di petunjuk saya sendiri terlalu ringkas.** Petunjuk 1
menulis "neuron identik menerima gradien identik" tanpa syarat. Diuji dengan
bobot seragam tapi tak nol dan lapisan keluaran acak: gradiennya langsung
berbeda (`9.645e-02`) dan bobotnya menyebar sejauh 0.2374 dalam 200 iterasi.
Simetri patah sendiri. Klaim itu cuma berlaku kalau seluruh jaringan seragam.

**Sudut di batas keputusan itu 2 kali jumlah neuron, bukan kurang.** Terukur
16 sudut untuk 8 neuron dan 62 untuk 32, stabil di kisi 200 sampai 1600.
Tiap neuron kena persis 2 penyeberangan, karena garis lurus yang memotong
kurva tertutup harus masuk sekali dan keluar sekali. Untuk 32 neuron, 31 yang
ikut melipat; satu garis lipatnya lewat di luar kurva.

Aturannya: `sudut = 2 x (neuron yang garis lipatnya memotong batas)`.

### Dua koreksi angka

`relu` di lapisan terakhir tidak mengunci akurasi di 50 persen, terukur 59,2
persen. Sebabnya `(s.data > 0) == (yi > 0)` menghitung ramalan tepat nol
sebagai kelas -1, jadi model masih memisahkan lewat "nol lawan positif".

Satu epoch MNIST 784-32-10 bukan 29 hari, tapi 5,5 sampai 11,5 jam. Sumber
selisihnya: 49 ms di Bagian 7 dibaca sebagai ongkos satu gambar, padahal itu
satu iterasi penuh atas 120 titik. Persis 120 kali lipat. Dinding rekursi di
784-256-10 tetap menabrak seperti hitungannya, `RecursionError` di kedalaman
1040 lawan batas 1000.

Sebaran tiga pengukuran waktu untuk pekerjaan yang sama persis: 328, 575, 687
ms. Mesin `Value` didominasi alokasi objek Python, bukan aritmetika, jadi satu
angka tunggal untuk ongkos seperti ini menyesatkan.

### Yang wajib dibereskan sebelum Sesi 3

Inisialisasi diperbaiki, dan `exp` serta `log` ditulis di `Value` lengkap
dengan `_backward` plus uji beda hingga. Keduanya dipakai Sesi 3. Kotak tolok
ukur "exp dan log ditambahkan" tercentang padahal rumusnya baru ada di berkas
jawaban, bukan di `bulan1_sesi1_autograd.py`.

---

## 22 Agustus 2026 - Empat perbaikan Sesi 2, lalu Sesi 3+4 digabung

Keempat butir wajib dari kunci dibereskan pemilik. Diperiksa:

- inisialisasi jadi `random.gauss(0, 1) * sqrt(2/n)`
- `exp` dan `log` ditulis di `Value` lengkap `_backward`, ditambahkan ke
  tabel beda hingga Bagian 2 Sesi 1, dan dua-duanya lolos
- dua kotak tolok ukur yang tercentang tanpa bukti diturunkan sendiri

### Yang masih meleset di 2d

Kodenya ditulis, tapi tetap tidak dijalankan. Angka yang dilaporkan, "sekitar
0,5 dan sekitar 1,0", benar untuk `E[a^2]` sedangkan kodenya mengembalikan
`np.var`. Dijalankan apa adanya:

```
np.var, skala sqrt(1/n) : 0.1515   (dia klaim ~0.5)
np.var, skala sqrt(2/n) : 1.0484   (dia klaim ~1.0)

dirata-rata 200 lemparan   np.var(a)   E[a^2]
sqrt(1/n)                     0.3466   0.5110
sqrt(2/n)                     0.6778   0.9980
```

Untuk `z ~ N(0, s^2)` dan `a = relu(z)`: `E[a^2] = s^2/2` tapi
`Var(a) = 0.3408 s^2`, karena relu membuat keluarannya tidak lagi berpusat
nol. Kesimpulannya benar, alatnya mengukur besaran lain, dan satu lemparan
terlalu berisik untuk dibaca.

### Sesi 3+4 digabung, atas permintaan pemilik

`notebooks/bulan1_sesi34_mnist.py`, sembilan TODO, plus
`notebooks/soal-bulan1-sesi34.md` berisi delapan soal dan dua belas kotak.

Urutan bagiannya sengaja: entropi silang di atas `Value` (memakai `exp` dan
`log` yang baru dia tulis), tabrak dinding waktu, tabrak dinding rekursi,
tembus rekursi lewat backward iteratif, tembus waktu lewat `Tensor` numpy,
MNIST, pembanding PyTorch, lalu tiga optimizer tulisan tangan.

Versi terisi dijalankan penuh, keluar 0, tanpa peringatan:

```
gradien entropi silang lawan p - y     selisih 1.11e-16
784-32-10 dengan Value                 6.2 jam per epoch
784-256-10 dengan Value                RecursionError, kedalaman 1040
784-256-10 sesudah backward iteratif   lolos, 2924 ms
empat aturan turunan Tensor            galat relatif 2.791e-10
MNIST, epoch terakhir                  96.03 persen
MNIST, epoch dipilih lewat validasi    97.27 persen  (epoch 6)
Value lawan Tensor numpy               sekitar 5000x
numpy lawan PyTorch CPU                sekitar 3x
bilangan kondisi lembah                484.0
iterasi ke 1 persen                    SGD tidak pernah, momentum 63,
                                       RMSprop 255, Adam 52
```

MNIST diunduh sekali ke `E:\SYNESIS\data`, 11 MB, lalu disimpan sebagai npz
supaya jalan berikutnya tidak perlu jaringan.

### Tiga hal yang dibetulkan waktu menyusunnya

**Himpunan validasi tidak dipakai memilih apa pun.** Versi pertama membelah
data jadi tiga lalu melaporkan akurasi uji di epoch terakhir. Itu upacara,
bukan metode. Sekarang parameter di epoch dengan validasi terbaik disimpan,
dan kedua angka dilaporkan berdampingan: 96,03 lawan 97,27. Selisih 1,24
persen itu jadi bahan Soal 6.

**Waktu epoch dilaporkan sebagai rata-rata.** Sebarannya 3,0 sampai 8,9 detik
karena epoch pertama menyentuh 313 MB data untuk pertama kali. Sekarang yang
dipakai nilai tengah, dan sebarannya ikut dicetak.

**Gambar lintasan optimizer tidak terbaca.** Empat lintasan saling menimpa,
dua di antaranya tertutup total. Diganti dua panel, dan panel kanan yang
menentukan: jarak ke dasar terhadap iterasi dengan sumbu tegak logaritmik.
Di situ perbedaan keempatnya terbaca langsung sebagai kemiringan garis.

### Hasil yang tidak diduga tapi dipertahankan

PyTorch GPU tidak menang lawan PyTorch CPU (1,4 lawan 1,4 detik). Batch 64 di
jaringan 784-128-10 terlalu kecil untuk menutup ongkos tetap tiap panggilan
kernel. Ini konsisten dengan Bukti 6 Sesi D dan jadi bahan Soal 5c, yang
meminta dia mencari batas baliknya sendiri.

---

## 23 Agustus 2026 - Sesi 3+4 dikerjakan pemilik, Bulan 1 tutup

Sembilan TODO diisi, 31 butir soal dijawab, dua belas kotak dicentang.
Keluarannya identik dengan versi acuan sampai digit terakhir, keluar 0 tanpa
peringatan.

Jawabannya diadu dengan lima pengukuran di `notebooks/kunci_b1s34_bukti.py`,
hasilnya di `notebooks/kunci-bulan1-sesi34.md`. **Verdict: 30 benar, 1 salah.**

Bandingkan Sesi 2 yang empat butirnya tidak dikerjakan sama sekali. Kali ini
tiap soal yang meminta angka dijawab dengan angka, termasuk 5b, 5c, dan 7d
yang menuntut menulis percobaan sendiri di luar berkas sesi.

### Yang salah: 6a, dan sebabnya bukan overfitting

Dia menjelaskan penurunan validasi di epoch 7 sebagai overfitting. Diukur
dengan menambah kolom akurasi latih:

```
 epoch   akurasi latih   akurasi validasi
     6          98.10%             97.32%
     7          97.11%             96.37%
```

Latih ikut jatuh bersama validasi. Overfitting berarti latih terus naik
sementara validasi turun; model yang menghafal tidak tiba-tiba lupa. Yang
terjadi: lr 0,1 dipertahankan sampai akhir dan langkah terakhir mendarat di
tempat yang lebih buruk untuk kedua himpunan sekaligus.

Berkas sesi tidak mencetak akurasi latih, jadi dua sebab yang berbeda
kelihatan sama dari luar. Itu kelalaian saya waktu menyusunnya.

### Temuan terbaik malam ini: reversed() yang menyelamatkan 3a

Dia mengklaim gradien iteratif dan rekursif identik bit demi bit karena
`reversed()` di dorongan anak menyamakan urutan DFS. Diuji pada graf yang
sama dengan tiga cara telusur:

```
60-40-10, 8 contoh, 2850 parameter, 48829 simpul
  iteratif + reversed        selisih 0.000e+00   beda bit    0 dari 2850
  iteratif tanpa reversed    selisih 1.110e-16   beda bit 1764 dari 2850
  iteratif anak diacak       selisih 1.110e-16   beda bit 1513 dari 2850
```

Ketiganya benar secara matematis. Yang berbeda cuma urutan penjumlahan, dan
penjumlahan titik-mengambang tidak asosiatif. Tanpa `reversed()` kodenya
tetap lolos semua uji beda hingga dan tetap melatih MNIST ke 97 persen; yang
hilang cuma jaminan bit demi bit yang dia klaim.

### Kelemahan berkas sesi yang temuan itu menyingkap

Uji Bagian 3 semula memakai jaringan 4-3-2. Di ukuran itu ketiga cara telusur
memberi `0.000e+00`, jadi ujinya lolos apa pun yang ditulis. Sekali lagi pola
"contoh yang dipilih tidak bisa membedakan benar dari salah", kali ini di
berkas saya.

Diperbaiki dua hal sekaligus: diperbesar jadi 20-12-5 dengan 4 contoh, dan
kedua versi sekarang dijalankan pada graf yang sama, karena dua graf terpisah
punya alamat objek berbeda sehingga urutan iterasi set-nya berbeda dan
selisih 1e-17 muncul dari situ, bukan dari kode yang diuji. Sesudah itu:

```
diadu dengan versi rekursif, 2956 simpul, graf sama
  selisih gradien maks : 0.000e+00
  beda bit             : 0 dari 317
```

### Klaim lain yang dikonfirmasi

- 1c dan 1d: rugi identik `1.8358831657033847`, selisih gradien `2.220e-16`,
  jumlah gradien `2.108e-16`. Ketiga angka yang dia laporkan kena.
- 5c: titik balik GPU memang batch 256. Diulang tiga kali per titik; di batch
  1024 GPU hampir tiga kali lebih cepat dari CPU.
- 7d: lanskap `x^4/4 + y^2/2` dari (100,100) memang membalik urutannya.
  RMSprop tiba di rugi 1 pada iterasi 783, momentum tidak pernah.
- 7b: keempat angka turunan osilator teredamnya benar, dan dia sendiri
  mencatat rasio terukur 4,84x berbeda dari ramalan asimtotik 12,9x.
- 6d: sigma binomial 0,171 poin persen dan bias seleksi 0,70 poin persen,
  dua-duanya benar.

### Kebiasaan yang belum melekat

5a, 5b, dan 5c melaporkan waktu sampai enam angka di belakang koma dari satu
kali jalan. Kolom numpy batch 64 di pengukuran ulang: `2.264 / 2.785 / 6.587`
detik untuk pekerjaan yang sama persis. Angka keenamnya tidak berarti apa-apa.

Sama dengan keluhan yang saya kena sendiri di Bagian 5 kemarin. Muncul tiga
kali malam ini plus sekali di 2d Sesi 2. Aturannya satu kalimat: kalau
melaporkan waktu, laporkan sebarannya.

### Bulan 1 tutup

Kesepuluh kotak di `docs/Bulan-1-Harian.md` tertutup, termasuk "cocok dengan
PyTorch" yang sudah dikerjakan di Bagian 4 Sesi 1.

---

## 23 Agustus 2026 - Kanvas tulis tangan, produk akhir Bulan 1

`notebooks/bulan1_kanvas.py`. Kanvas tkinter di kiri, tebakan plus batang
peluang sepuluh kelas plus kotak 28x28 yang dilihat model di kanan.

Nol dependensi baru: tkinter stdlib, Pillow sudah ada, `Tensor` dan `maju`
dipakai ulang dari `bulan1_sesi34_mnist`. Bobot dilatih sekali lalu disimpan
ke `E:\SYNESIS\data\mnist_model_128.npz`, akurasi uji 97,27 persen.

Yang menentukan hidup-matinya bukan modelnya, tapi pengecilannya: potong ke
kotak isi, skala sisi terpanjang jadi 20, tempel ke 28x28 dengan pusat massa
di tengah. Itu cara MNIST dibuat, dan tanpa itu jaringan 97 persen menebak
asal karena masukannya bukan benda yang sama dengan yang dilatihkan.

Filter pengecilan BOX, bukan LANCZOS, karena BOX itu rata-rata luas yang
dipakai MNIST asli dan tidak bisa berdering di tepi keras. Diukur pada 300
gambar uji lewat jalur kanvas: BOX 95,3 persen, LANCZOS 95,0, BILINEAR 94,7.
Coretan pena sintetis 22 piksel: 1 dan 7 di atas 99 persen, 4 di 82 persen.

Satu koreksi ke diri sendiri. Uji pertama memberi 84,3 persen dan sempat
saya kira preprocessing-nya bocor. Ternyata pembesaran LANCZOS di skrip
ujinya yang berdering, bukan kodenya; jalur asli tidak pernah membesarkan
apa pun. Ujinya yang salah, bukan yang diuji.

Cuma angka 0-9. Huruf butuh EMNIST, 562 MB, belum diunduh.

---

## 24 Agustus 2026 - Bulan 2 Sesi 2 disiapkan

`notebooks/bulan2_sesi2_intent.py` plus `notebooks/soal-bulan2-sesi2.md`.
Tujuh TODO, delapan soal, dua belas kotak.

Sesi 1 sudah ada sejak 22 Agustus dan belum dikerjakan, jadi tidak dibuat
ulang. Sesi 2 menyambung tiga utang yang digantung Sesi 1: tidak ada data uji
(Soal 6c), buta sinonim (Soal 3), dan salah tebak itu mahal (Soal 8c).

Isinya: belahan tiga arah berstrata, TF-IDF, matriks bingung, presisi dan
recall, ambang "tidak tahu", ekstraksi slot. Mesin belajarnya tidak baru sama
sekali: `Tensor` dan `maju` dari Bulan 1 Sesi 3+4 diimpor apa adanya, nol
baris autograd baru. Data 120 perintah bahasa Indonesia, 8 intent, disimpan
sebagai teks di dalam berkas supaya pemilik menambahnya sendiri.

Versi terisi jalan penuh, keluar 0:

```
himpunan uji 24 kalimat, sigma binomial 6,1 poin persen
hitung kata   validasi 65,6  uji 68,2   terburuk 54,2  terbaik 79,2
TF-IDF        validasi 65,6  uji 66,7   terburuk 50,0  terbaik 75,0
ambang 0,00   18 benar  6 salah   0 tolak   0 dari 5 asing ditolak
ambang 0,90    9 benar  0 salah  15 tolak   5 dari 5 asing ditolak
0,004 milidetik per perintah, model 68,3 KB, kosakata 173 kata
```

### Tiga hal yang dibetulkan waktu menyusunnya

**Perbandingan TF-IDF lawan hitung-kata seri di satu belahan.** Versi pertama
melatih sekali dan melaporkan 75,0 lawan 75,0 di uji. Tidak ada resolusi.
Diganti delapan belahan dengan seed berbeda: sebaran hasil 25 poin persen,
selisih antar-resep 0,0 poin persen. Kesimpulan yang benar jadi "percobaan
ini tidak bisa memutuskan", dan itu yang diminta Soal 3.

**Ambang di Bagian 5 mentok.** Pemilihan epoch terbaik memakai `>` sehingga
seri dimenangkan epoch paling awal, dan model berhenti waktu peluangnya masih
hampir rata. Akibatnya di ambang 0,5 sudah 23 dari 24 ditolak, dan tabelnya
tidak menunjukkan apa-apa. Diganti `>=` supaya seri dimenangkan yang lebih
terlatih. Sekarang kurvanya punya bentuk.

**Spesifikasi jam saya sendiri ngawur.** Docstring meminta "jam tiga"
diterjemahkan jadi `15:00`. Itu menebak, dan "jam tiga" memang ambigu.
Diperbaiki jadi `03:00` kecuali ada penanda sore atau malam, dan larangan
menebak itu jadi Soal 7.

---

## Catatan disk, 24 Agustus 2026

Pemilik melihat C: turun 3 GB dan bertanya. Diukur, tidak ada yang dihapus:

```
Temp total                                       3.6 GB
  pip-unpack.../torch-2.6.0+cu124.whl   1.87 GB   20 Agu 01:22
  WinGet/Ollama.Ollama.0.32.15           1.6 GB   22 Agu 19:07
  claude (scratchpad)                     16 MB
MNIST + bobot (E:)                        86 MB
```

Yang 1,6 GB itu sisa unduhan dua percobaan pasang Ollama yang dibatalkan
pemilik pada 22 Agustus. Waktu itu saya melapor "tidak meninggalkan apa-apa";
yang saya periksa cuma programnya terpasang atau tidak, bukan cache
unduhannya. Laporan itu salah dan sudah dikoreksi.

---

## 24 Agustus 2026 - Bulan 2 Sesi 1 dan 2 dikerjakan

Keempat berkas selesai diisi:

- `notebooks/bulan2_sesi1_kata.py`
- `notebooks/soal-bulan2-sesi1.md`
- `notebooks/bulan2_sesi2_intent.py`
- `notebooks/soal-bulan2-sesi2.md`

Empat belas TODO kode sudah jalan. Sesi 1 lolos gradient check dengan galat
relatif `1,166e-10` untuk bobot dan `1,440e-11` untuk bias. Sesi 2 kembali
menghasilkan angka acuan: 80/16/24 data, kosakata 173 kata, hitung-kata
68,2 persen, TF-IDF 66,7 persen, dan 0,004 milidetik per perintah.

Ambang per intent ditambahkan berdasarkan ongkos salah. Hasil seed 0 berubah
dari 15 benar, 5 salah, 4 tolak pada ambang global 0,50 menjadi 14 benar,
3 salah, 7 tolak. Ia tidak dipakai sebagai pendeteksi data asing karena lima
kalimat asing tetap lolos melalui kelas berongkos rendah. Kesimpulannya:
ambang keamanan dan deteksi di-luar-kelas adalah dua masalah berbeda.

Semua jawaban teori diisi dari hasil pengukuran. Dua dugaan awal dikoreksi:

- Target selang kepercayaan selebar 5 poin pada akurasi 90 persen memerlukan
  576 kalimat uji, jadi sekitar 3.840 total pada belahan 70/15/15. Target
  300--500 hanya cukup untuk prototipe.
- Softmax tanpa pengurangan maksimum belum rusak pada bobot awal `x1000`
  untuk seed ini; logit terbesar baru 496. Kerusakan `nan` benar-benar muncul
  pada `x1500`, saat logit mencapai 744 dan `exp` overflow.

Pemeriksaan kasus tepi lolos untuk sigmoid `+-1000`, softmax logit `+-1000`,
vektor seluruhnya nol, pembagian nol presisi/recall, belahan yang dapat
diulang, frasa waktu terpanjang, `jam tiga -> 03:00`, dan
`jam 3 sore -> 15:00`. Kedua skrip keluar dengan kode 0.

### Yang sengaja belum ditutup

Data tetap 120 kalimat. Menambah sampai 3.840 dan menambah lima frasa waktu
harus memakai ucapan serta riwayat asli pemilik, bukan kalimat buatan agen.
Karena itu satu kotak Sesi 2 tetap kosong.

---

## 24 Agustus 2026 - Bulan 2 diperiksa, tidak ada yang salah

Jawaban kedua sesi diadu dengan empat pengukuran di
`notebooks/kunci_b2_bukti.py`, hasilnya di `notebooks/kunci-bulan2.md`.

Enam belas nilai terukur yang dia tulis, enam belas cocok sampai digit
terakhir, termasuk lima keyakinan softmax sampai empat angka di belakang
koma. Yang ada cuma satu angka tertukar waktu disalin, dan dua butir yang
sengaja ditandai belum dikerjakan. Tolok ukur Sesi 1 dua belas dari dua
belas, Sesi 2 sebelas dari dua belas.

### Dia membantah berkas saya, dan dia benar

Soal 7c Sesi 1 menyatakan softmax tanpa pengurangan maksimum menghasilkan
`nan`, dan Soal 7d menyuruh membuktikannya dengan `W` awal dikali 1000.
Diukur:

```
exp meluap di atas ln(1.8e308) = 709.78

 kali W awal   logit maks    nan   akurasi  softmax
        1000       496.17  False     86.1%  polos
        1500       744.25   True       nan  polos
        1500       744.25  False     72.2%  kurangi maks

ambang terukur: pengali 1430.5, logit maks di situ 709.78
```

exp(496) sekitar 1e215, masih muat di float64. Pernyataan 7c benar secara
umum, tapi pengali 1000 di 7d tidak cukup membuktikannya di data ini.
Kalibrasi soalnya salah, dan itu kesalahan saya. Dia mengukur, menemukan
dugaan soalnya tidak terbukti, lalu menuliskan itu alih-alih menuliskan apa
yang soalnya harapkan.

Tambahan yang belum dia sebut: di pengali 1500 versi yang mengurangi maksimum
tetap hidup tapi akurasinya jatuh ke 72,2 persen. Pengurangan maksimum
menyelamatkan dari `nan`, bukan dari inisialisasi buruk.

### Satu pengujian saya yang keliru, bukan jawabannya

Soal 2b Sesi 2, kebocoran kosakata untuk TF-IDF. Dia laporkan `68,8/66,1`,
saya dapat `67,7`, dan sempat mengira angkanya meleset. Diukur tiga tingkat:

```
bersih                      TF-IDF   65.6%  66.7%
kosakata bocor, IDF bersih  TF-IDF   68.8%  66.1%
kosakata + IDF bocor        TF-IDF   68.8%  67.7%
```

Soal 2b cuma menyuruh mengubah satu baris, yaitu sumber kosakatanya. Saya
membocorkan IDF-nya juga. Baris tengah percobaan yang benar, dan itu yang dia
jalankan.

Arah hasilnya lebih berharga daripada angkanya: validasi naik 65,6 ke 71,9
sementara uji turun 68,2 ke 62,5. Ramalannya di 2b sudah menyebut itu lebih
dulu, bahwa arah kebocoran tidak pasti.

### Yang lain, dikonfirmasi

- MSE lawan entropi silang: 100 persen di iterasi 85 lawan 54, persis. Cara
  mengujinya benar, rugi diganti beserta gradiennya. Satu angka tertukar:
  rugi akhir MSE `0,009026`, dia tulis `0,000926`.
- 642 parameter untuk 36 contoh, rasio gradien 500 kali, dan turunan `p - y`
  lengkap sampai selesai. Semua benar.
- 576 kalimat uji dan 3.840 total untuk selang 5 poin, benar. Kesimpulannya
  menunjukkan batas angka 300-500 yang saya tulis sendiri di rencana Bulan 2.
- Ambang per intent 14/3/7 lawan global 15/5/4, dan kelima keyakinan perintah
  butuh-LLM, semua sama persis.

### Yang paling berharga

Dia menyimpulkan sendiri, tanpa diminta soal, bahwa ambang ongkos BUKAN
pendeteksi kalimat asing: nol dari lima kalimat asing tertolak karena kelas
murah seperti `obrol` sengaja longgar. Ambang per intent bahkan menangkap
lebih sedikit perintah-butuh-LLM daripada ambang global, 2 lawan 4, dengan
sebab yang sama.

Keluhan tersisa dari kunci Bulan 1 Sesi 3+4 adalah "laporkan sebaran, bukan
satu angka". Sesi 2 menutupnya lewat tiga hal yang tidak diminta eksplisit:
menyatakan percobaan tidak bisa memutuskan alih-alih memilih pemenang,
menerjemahkannya ke ralat alat lawan sinyal, dan menuliskan ramalan lebih
dulu sebelum mengukur.

---

## 24 Agustus 2026 - Data intent dari arsip nyata dan generator

SSD `S:` dipindai secara baca-saja. Folder aplikasi, game, cache, video,
Recycle Bin, dan folder sistem diabaikan. Sumber yang benar-benar memuat gaya
perintah pemilik adalah dua arsip `knowladge/sessions` dan `rollout.jsonl` di
repo ini. Log Aslab dan chat kelompok sengaja tidak diambil karena memuat
NPM/nilai orang lain dan tidak relevan untuk intent SYNESIS.

Tiga sumber disalin, bukan dipindah, ke `data/bulan2/raw`. SHA-256 sumber
sebelum, sumber sesudah, dan salinan dibandingkan; ketiganya identik. Hash
disimpan di `data/bulan2/raw/SHA256.txt`. Tidak ada sumber yang berubah,
berpindah, atau terhapus.

`scripts/generate_bulan2_data.py` ditambahkan. Hasil lokalnya, yang memang
diabaikan Git lewat aturan `data/`:

- 1.080 kalimat sintetis, 15 intent, tepat 72 per intent.
- 41 pesan pengguna nyata yang sudah membuang path dan nomor panjang.
- 41 pesan nyata berlabel utama untuk smoke test gaya bahasa.

Tujuh kelas ditambahkan karena muncul nyata di percakapan pemilik:
`info_sistem`, `ubah_proyek`, `kelola_repo`, `pasang_paket`,
`jelaskan_konsep`, `tanya_umum`, dan `lanjut_tugas`. Loader Sesi 2 sekarang
bisa menerima berkas `label | kalimat` lewat argumen baris perintah, tanpa
mengubah perilaku data bawaan.

Hasil yang tidak boleh disalahartikan:

```text
validasi sintetis         100,0 persen
pesan nyata               21/41 = 51,2 persen
pesan nyata non-duplikat  19/39 = 48,7 persen
```

Skor 100 persen terjadi karena pola generator yang sama tersebar ke belahan
validasi. Ia bukan bukti memahami bahasa pemilik. Angka sekitar 49 persen
adalah batas awal yang lebih jujur. Data sintetis dipakai untuk latihan saja;
pesan nyata baru harus tetap menjadi ujian.

---

## 25 Agustus 2026 - Bulan 2 Sesi 3 dan 4 disusun, dan roadmap saya terbantah

Dua berkas latihan baru, `bulan2_sesi3_embedding.py` (8 TODO) dan
`bulan2_sesi4_synesis.py` (7 TODO), beserta soalnya. Semua angka di bawah
diukur lebih dulu, sebelum kalimatnya ditulis.

### Sesi 3 menyerang sebab, bukan gejala

Sesi 2 berakhir di 56,1 persen pada 41 pesan nyata, dengan OOV 55,2 persen.
Sesi 3 membangun tiga jalan keluar dan mengukur ketiganya.

Yang pertama, dasar pembanding yang selama ini hilang:

```text
resep                     akurasi      selang 95 persen
tebak ubah_proyek terus     39.0%          24.1 .. 54.0
model Sesi 2                56.1%          40.9 .. 71.3
```

Batas bawah model cuma 1,9 poin di atas menebak buta. Semua tabel sesudah ini
dibaca dengan selang selebar 30 poin di kepala.

Yang kedua, n-gram karakter. Kekerabatan morfologis jatuh gratis dari ejaan:
`hapus` dan `menghapus` berkosinus 0,721, padahal dengan kolom kata 0,000.
Tapi sapuan panjang potongannya merentang 43,9 sampai 58,5 persen, dan lebar
itu jauh di dalam derau.

Yang ketiga, vektor kata dari korpus repo sendiri lewat ko-okurensi, PPMI,
dan SVD. Ini yang mengejutkan:

```text
   token dibaca  pasangan   median peringkat    acak
          15455        12                535     600
          38638        12                583     600
          77276        12                 12     600
         154553        12                  4     600
```

Median peringkat 4 dari 2.000 kata, dengan pembanding acak 1.000. Vektor
katanya bagus, dan lompatannya tajam antara 38 ribu dan 77 ribu token.

Dan justru itu yang membuat hasil hilirnya berarti: representasi yang jelas
bagus cuma menggeser akurasi 51,2 ke 56,1 persen, di dalam selang.

### Tiga tuas ditarik, dan yang ketiga membantah rencana saya

```text
TUAS A  tambah kalimat nyata      0 -> 20 kalimat : 54,1 -> 55,2 persen
TUAS B  naikkan porsinya          2,6 -> 51,6 persen porsi : datar
TUAS C  gabungkan jadi 2 kelas    85,4 persen, dasar mayoritas 85,4 persen
```

Tuas B menutup dugaan yang paling masuk akal, yaitu bahwa 20 kalimat nyata
tenggelam di antara 750 sintetis. Dinaikkan sampai lebih dari separuh data
latih, hasilnya tetap datar. Dugaan itu salah.

Tuas C yang paling penting, dan hasilnya menyakitkan buat saya:

```text
pesan yang intentnya PUNYA alat : 6 dari 41
pesan yang butuh model bahasa   : 35 dari 41
```

Bagian 4 di `docs/Roadmap.md`, yang saya tulis sendiri, menyatakan 80 sampai
90 persen pemakaian harian bisa ditangani pengklasifikasi tanpa LLM. Di
sampel ini angkanya 15 persen.

Keberatan yang harus ikut dicatat supaya jujur: 41 pesan itu semuanya dari
satu arsip, yaitu percakapan merancang proyek ini bersama agen pemrograman,
dan itu memang percakapan terbuka dari ujung ke ujung. Ia bukan sampel cara
pemilik akan memakai SYNESIS untuk membuka berkas praktikum. Tapi ia
satu-satunya rekaman pemakaian nyata yang ada, dan sampai ada yang lain,
dialah bukti terbaik.

Kesimpulan yang keluar dari ketiga tuas: yang paling kurang dari Bulan 2
bukan representasi, bukan arsitektur, dan bukan jumlah epoch. Yang kurang
catatan pemakaian yang mewakili.

### Sesi 4 membangun alat pencatat itu, sekaligus SYNESIS v0.1

Utang tertua Bulan 2 ditutup di sini. Di Sesi 2, `AMBANG_INTENT` disetel
tangan, lima belas angka tanpa alasan yang bisa dipertahankan. Sekarang
kelima belasnya turun dari dua tetapan ongkos:

```text
ongkos menolak = 1,0
ongkos salah   = BACA 2,0  TULIS 20,0  MERUSAK 200,0  BAHASA 3,0
ambang         = 1 - ongkos_tolak / ongkos_salah
```

Dua belas dari lima belas ambang tangan ternyata terlalu longgar. Yang
terlonggar `obrol` dan `tanya_umum`, masing-masing meleset 0,37.

Lalu ketiga kebijakan diadu dengan ongkos total, bukan akurasi:

```text
kebijakan              benar  salah  tolak   ongkos   ongkos/pesan
argmax polos              23     18      0    447,0          10,90
ambang tangan Sesi 2      15     10     16    242,0           5,90
ongkos harapan            15      7     19     39,0           0,95
selalu menolak             0      0     41     41,0           1,00
```

Baris yang paling banyak benar adalah baris yang paling mahal. Urutan menurut
akurasi dan urutan menurut ongkos berbeda, dan itu seluruh isi Bagian 3.

Baris terakhir sengaja saya sisakan sebagai soal, karena hasilnya tidak
nyaman: kebijakan ongkos harapan cuma menang 2,0 dari kebijakan yang tidak
pernah melakukan apa pun. Sebabnya model ongkosnya memberi 0 untuk tindakan
benar, jadi melakukan hal yang benar tidak dihargai, cuma tidak dihukum.
Soal 3e memintanya diperbaiki.

Pagar jalur diadu dengan delapan serangan, delapan-delapannya ditolak. Pipa
ujung ke ujung di 41 pesan: 1 sampai bertindak, 0 bertindak salah.

Mode percakapan jalan. `buka laporan praktikum minggu lalu` sampai memanggil
alat, dan hasilnya `Tidak ada berkas di S:\Code\Make A Jarvis\laporan
praktikum`. Itu bukan kegagalan pagar; itu langkah yang memang belum ada,
yaitu penerjemah frasa manusia jadi pola nama berkas. Sudah jadi Soal 4c.

### Empat kesalahan saya di sesi ini

1. Saya menulis bahwa PPMI membuang lebih dari separuh sel matriks. Diukur:
   dari 8,0 persen taknol ke 7,3 persen, jadi sekitar sepersepuluh dari yang
   terisi. Penyaringan terbesarnya ada di nilai sel, bukan jumlahnya: lima
   kata tersering memegang 7,7 persen massa mentah, tinggal 0,5 persen
   sesudah PPMI. Kalimatnya diganti, dan pengukuran massa itu dijadikan
   keluaran supaya tidak perlu dipercaya begitu saja.

2. Saya menulis bahwa diagonal matriks ko-okurensi harus nol. Tidak. Kata
   yang sering muncul dua kali dalam satu jendela, dan 1.173 kata punya
   diagonal taknol. Yang dicegah cuma pasangan kata dengan dirinya di posisi
   yang sama. Jadi Soal 4b.

3. Sapuan ukuran korpus versi pertama mengembalikan `nan` untuk dua titik
   terkecil, karena kosakatanya ikut mengecil bersama korpusnya sehingga
   tidak ada pasangan uji yang tersedia. Diperbaiki dengan memaku kosakata
   ke korpus penuh, sehingga yang berubah cuma satu variabel.

4. Bagian 7 versi pertama menulis kesimpulan "kalau menambah kalimat nyata
   menggeser lebih jauh daripada representasi" sebelum diukur. Diukur,
   ternyata datar juga. Bagian itu ditulis ulang jadi tiga tuas, dan Tuas B
   ditambahkan justru untuk menutup dugaan saya sendiri.

Satu catatan kebersihan: menguji Sesi 4 sempat menulis `data/bulan2/audit.jsonl`
berisi 86 baris dari jalannya uji saya, bukan pemakaian pemilik. Berkas itu
dipindahkan keluar repo ke folder sementara, tidak dihapus, supaya
`audit.jsonl` yang nanti tumbuh benar-benar berisi pemakaian sungguhan.

---

## 26 Agustus 2026 - Bulan 3 disusun dan dikerjakan, SYNESIS v0.2 bicara

Lima sesi, empat berkas latihan baru beserta soalnya, dua modul baru di
`synesis/`, dan satu berkas bukti yang menguji ulang lima puluh klaim di
seluruh bulan. Semua angka di bawah diukur lebih dulu, sebelum kalimatnya
ditulis, dan yang meleset dari ramalan saya ditinggalkan apa adanya.

### Sesi 1: konvolusi, dan satu istilah yang dipakai salah

Konvolusi 1D dan 2D ditulis dari definisinya, lalu diadu dengan numpy dan
scipy. Selisihnya nol sampai batas float64 untuk ketiga mode.

Dua hasil yang layak dibawa seumur hidup. Yang pertama, titik silang FFT:

```text
     N     K   langsung (ms)    FFT (ms)    rasio
  1024    16           0.025       0.072     0.35
  1024  1024           0.141       0.066     2.13
 65536    16           1.077       5.919     0.18
 65536  1024           6.421       5.880     1.09
```

Titik silangnya tumbuh dengan log N, bukan dengan N, jadi menaikkan panjang
sinyal enam puluh empat kali lipat hampir tidak menggesernya. Untuk kernel
CNN yang cuma tiga titik, FFT tidak pernah menang, dan itulah kenapa tidak
ada framework yang memakainya untuk lapisan konvolusi.

Yang kedua, dan yang paling sering dilewatkan buku teks: `nn.Conv2d`
mengerjakan KORELASI SILANG, bukan konvolusi. Terukur, dengan kernel Sobel
yang antisimetris, selisih keduanya 7,84 sedangkan tanggapan maksimumnya
3,918 — persis dua kali lipat, karena membalik kernel antisimetris membalik
tandanya. Untuk kernel simetris seperti kotak dan tajam, selisihnya nol.

im2col mengubah konvolusi jadi satu perkalian matriks dan mempercepatnya
548 kali dibandingkan gelung Python, dengan harga memori 8,7 kali lipat.
Bagian itu jadi fondasi seluruh Sesi 3.

### Sesi 2: suara jadi gambar, tanpa librosa

Spektrogram, bank mel, dan MFCC ditulis dari nol dengan `wave` bawaan Python
dan numpy. librosa sengaja tidak dipasang, dan alasannya bukan kemurnian:
fungsi yang sama dipasang ke `synesis/suara.py` di Sesi 5, dan menyeret numba
dan soundfile untuk tujuh puluh baris matematika tidak sepadan.

Tiga angka yang keluar cocok dengan turunannya di kertas:

```text
jendela     cuping samping (dB)   lebar cuping utama   gain koheren
kotak                     -13.3                  2.0          1.000
hann                      -31.5                  4.0          0.500
```

Turunan analitik untuk kotak memberi 20 log10(2/3pi) = -13,46 dB, dan yang
terukur -13,26. Selisih 0,2 dB berasal dari hampiran letak puncaknya.

Hasil kali resolusi waktu dan frekuensi tetap 1,00 untuk setiap panjang
bingkai, dan itu bukan kebetulan aritmetika melainkan prinsip ketakpastian
yang sama dengan yang saya turunkan di Fisika Kuantum, tanpa tetapan Planck
karena tidak ada kuantisasi yang terlibat.

MFCC diukur, bukan diceritakan. Tapis mel bersebelahan bertumpang tindih 50
persen sehingga keluarannya berkorelasi 0,599; DCT menurunkannya jadi 0,193,
dan 99,7 persen tenaganya tersisa di 13 koefisien pertama.

### Sesi 3: CNN dari nol, dan perbandingan yang jarang dilakukan orang

Tiga operasi ditambahkan ke `Tensor` Bulan 1: im2col, bentuk_ulang, dan
maks_kolam. Konvolusinya sendiri TIDAK punya aturan turunan baru; ia lahir
dari `__matmul__` dan `__add__` yang sudah ada sejak Agustus. Gradien
gabungannya diperiksa terhadap selisih terhingga dan meleset 1,71e-09.

Lalu perbandingan yang jarang dilakukan tutorial mana pun: CNN dan MLP
diadu pada JUMLAH BOBOT yang sama, bukan pada arsitektur yang enak dilihat.

```text
model                            bobot    detik   akurasi uji
CNN 8-16, kolam 2x2              5.258     22.2        96.43%
MLP 7 tersembunyi                5.575      0.4        84.05%
```

Selisih 12,4 poin di 10.000 gambar uji, selangnya 0,6 poin, jadi terukur.
Kolom detik menyimpan pelajaran yang kedua: CNN 55 kali lebih lambat untuk
bobot yang sama. Berbagi bobot menghemat PARAMETER, bukan hitungan, dan itu
pertukaran yang sengaja diambil karena parameter mahal sedangkan hitungan
tinggal menunggu.

Versi PyTorch dari arsitektur yang sama, dengan bobot yang disalin, memberi
keluaran yang berbeda 1,07e-14. Dua implementasi bebas, angka yang sama.

### Ramalan saya di Sesi 3 terbalik, dan itu yang paling berguna

Bagian 6 mengukur apakah spektrogram boleh diperlakukan sebagai gambar.
Ramalan saya: sumbu frekuensi tidak stasioner (pola pada 200 Hz berarti hal
lain daripada pola yang sama pada 4.000 Hz), sumbu waktu stasioner (kata bisa
diucapkan kapan saja).

Terukur, dengan ukuran yang sama persis untuk kedua sumbu:

```text
sumbu            rasio tanpa pra-tekan   rasio dengan pra-tekan
frekuensi                        0.389                    0.114
waktu                            0.376                    0.406
```

Urutannya terbalik dari ramalan saya, dan dua sebabnya keduanya berguna.

Pertama, saya sedang mengukur akibat kerja saya sendiri. Pra-penekanan satu
baris dari Sesi 2 memang dipasang untuk meratakan sumbu frekuensi, dan ia
bekerja jauh lebih baik daripada yang saya duga: 0,389 turun jadi 0,114.

Kedua, sumbu waktu tidak stasioner karena DATANYA, bukan karena suaranya.
Speech Commands memotong tiap ucapan jadi tepat satu detik dengan katanya di
tengah, jadi posisi memang membawa informasi di dalam dataset itu. Di
pemakaian nyata, ketika SYNESIS mendengarkan terus-menerus, kata bisa mendarat
di mana saja.

Konsekuensinya langsung dan terukur di Sesi 4, dan itulah yang membuat
pengukuran ini berharga meskipun ramalannya salah.

### Sesi 4: himpunan uji yang akhirnya cukup besar

Speech Commands v0.02 diunduh sebagai aliran dan hanya kata yang dipakai yang
ditulis ke disk: 42.546 berkas dari 2.510 pembicara, ditambah 2.400 potongan
sunyi dari derau latar.

Belahannya menurut PEMBICARA, bukan menurut berkas, dan pemeriksanya satu
baris: nol pembicara muncul di lebih dari satu belahan. Kebocoran yang
dicegahnya adalah kebocoran yang menaikkan angka, dan bug yang menaikkan
angka tidak akan pernah saya cari sampai ketemu.

Untuk pertama kalinya sejak Agustus, himpunan ujinya 4.594 ucapan dan
selangnya 1,74 poin, bukan 30 poin seperti 41 kalimat Bulan 2.

Hipotesis dari Sesi 2 diuji, lengkap dengan pengendalinya:

```text
fitur           dimensi   parameter   detik   akurasi uji
log-mel 40           40      49.884     109        95.52%
MFCC 13              13      44.508      76        94.21%
MFCC 40              40      49.884     115        94.17%
```

Baris ketiga yang menentukan: ia punya dimensi dan jumlah parameter yang
IDENTIK dengan log-mel, jadi kalau yang berperan sekadar jumlah dimensi, ia
seharusnya menyusul. Ia tidak menyusul. Arah buktinya menunjuk ke struktur
lokal, sesuai mekanisme yang saya usulkan di Sesi 2.

Tapi selisihnya 1,35 poin dan selangnya 1,74 poin, jadi hipotesisnya belum
terbukti. Ditulis apa adanya di berkas soalnya.

Satu angka yang baru saya sadari perlu dilaporkan: menjalankan ulang seluruh
tabel dengan seed, data, dan kode yang sama memberi 95,49 / 94,32 / 94,14.
Selisih antarjalan sampai 0,11 poin, karena kernel cuDNN memakai penjumlahan
atomik yang urutannya tidak dijamin. Itu lantai derau pengukuran, dan
sekarang tercatat.

### Augmentasi, dan himpunan uji yang buta terhadap masalahnya sendiri

```text
model                        uji sejajar   uji digeser    jatuh
tanpa augmentasi                  95.28%        92.77%    2.50
geseran waktu +-100 ms            95.52%        93.84%    1.68
```

Kolom pertama berselisih 0,24 poin, yaitu dua kali lantai derau. Kalau cuma
itu yang dibaca, kesimpulannya augmentasi tidak berguna.

Kolom kedua menggeser ucapan ujinya sampai 250 milidetik dan menghapus
kebutaan itu. Himpunan uji resmi Speech Commands berbagi cacat dengan data
latihnya: keduanya kliping satu detik dengan kata di tengah. Model yang
memungut "di tengah" sebagai ciri tetap benar di sana, dan gagal di ruangan.

Ini yang paling saya bawa dari Sesi 4: himpunan uji yang benar secara
prosedur, terpisah dari data latih dan tidak dipakai memilih apa pun, tetap
bisa salah secara isi.

### Wake word, ambang dari ongkos, dan penyalaan per jam

Kelas positifnya `marvin` sebagai pengganti sampai pemilik merekam suaranya
sendiri. AUC 0,9907, akurasi 98,82 persen.

Ambangnya TIDAK diambil dari titik kesalahan setara, karena kedua kesalahan
tidak sama mahal. Kerangkanya sama dengan lima belas ambang intent Bulan 2:

```text
ambang 0,500   100 x 0,00364 + 0,2593 = 0,623
ambang 0,738   100 x 0,00000 + 0,4074 = 0,407   <- minimum
ambang 0,900   100 x 0,00000 + 0,4444 = 0,444
```

Bentuk umumnya layak dicatat: dengan ongkos yang sangat tak simetris,
jawabannya selalu ambang TERENDAH yang sudah menutup kesalahan mahalnya.

Lalu angka yang benar-benar menentukan apakah SYNESIS layak dibiarkan
menyala, dan yang jauh lebih jujur daripada FAR di atas: nol penyalaan
sepanjang 6,7 menit derau latar, di keempat ambang yang diuji. Beban
prosesornya 3,1 persen untuk sepuluh jendela per detik.

### Sesi 5: SYNESIS v0.2 mendengar dan menjawab

```text
mikrofon -> VAD -> wake word -> perekam -> Whisper -> pipa niat Bulan 2
                                                   -> Piper -> RVC -> speaker
```

VAD ditulis sendiri, bukan silero, dan ambangnya relatif terhadap lantai
derau ruangan yang diukur sebagai persentil ke-20 dari tiga detik terakhir.
Ambang mutlak tidak mungkin bekerja: ruangan, jarak ke mikrofon, dan AGC
Windows bersama-sama bisa menggeser sinyal 40 dB.

Anggaran latensinya, seluruhnya terukur:

```text
tunggu diam sebelum berhenti merekam       700 ms
transkripsi, berapa pun panjang ucapan    2600 ms   Whisper small, TETAP
pipa niat Bulan 2                            5 ms
Piper untuk 3 detik balasan                210 ms   RTF 0,07
RVC untuk 3 detik balasan                  330 ms   RTF 0,11 di GPU
-------------------------------------------------  +
                                          3845 ms   batas Modul.md 3.000 ms
```

MELAMPAUI batas 845 milidetik. Versi pertama catatan ini mengaku lolos
dengan margin 215 milidetik, dan itu kesalahan ketujuh saya di bulan ini:
transkripsi dihitung sebagai RTF dikali durasi ucapan, padahal Whisper
menambahkan bantalan sampai 30 detik sehingga ongkosnya TETAP.

```text
1,0 detik ucapan -> 2,48 detik      3,0 detik -> 2,60 detik
2,0 detik        -> 2,64 detik      8,0 detik -> 2,60 detik
```

Angka RTF 0,77 kebetulan benar untuk satu klip 3,98 detik yang dipakai
mengukurnya, dan salah untuk yang lain. RTF ukuran yang keliru untuk model
yang membantali masukannya.

Suku terbesarnya tetap transkripsi, sekarang 68 persen. Model `base` diukur
sebagai jalan keluar dan TIDAK bisa dipakai: pada suara pemilik ia lebih
lambat (6,37 detik lawan 3,52 detik untuk 12 detik ucapan) sekaligus jauh
lebih buruk, karena model yang menebak ngawur menghasilkan lebih banyak
token dan tiap token dibayar waktu. Yang tersisa: Whisper di GPU, atau
transkripsi mengalir.

### RVC ditulis ulang, karena dua paketnya tidak bisa dipasang

`req.md` bagian 5 meminta suara Yukino lewat RVC. Dua paket yang ada gagal
di tahap penyelesaian dependensi, bukan di tahap pemakaian:

```text
rvc-python  -> fairseq==0.12.2   tidak ada wheel untuk Python 3.12
rvc-inferpy -> faiss-cpu==1.7.3  tidak ada wheel untuk Python 3.12
```

Pilihannya memasang Python 3.10 khusus untuk satu paket, atau menulis
lintasan inferensinya sendiri. Saya menulisnya: `synesis/rvc.py`, sekitar
500 baris, arsitektur SynthesizerTrnMs768NSFsid yaitu VITS dengan dekoder
NSF-HiFiGAN. ContentVec diambil dari `transformers`, F0 dari YIN yang ditulis
sendiri, faiss tidak dipakai sama sekali.

Tiga pemeriksa, berurutan dari yang paling lemah ke yang paling menggigit:

```text
353 dari 353 kunci .pth cocok dengan state_dict model, bentuknya juga
nada keluaran mengikuti nada masukan: median -4 sen, 74,4 persen dalam 50 sen
Whisper membaca keluarannya sebagai kalimat Indonesia
```

Yang ketiga yang menutup perkara. Masukannya
`"Halo Sandy, laporan praktikum minggu lalu sudah saya buka."` dan Whisper
membaca keluaran RVC-nya sebagai
`"Halo Sandy, laporan 4 tikung minggu lalu sudah saya buka."` Sepuluh dari
sebelas kata terbaca oleh model yang tidak tahu apa-apa tentang RVC.

Satu kata rusak, dan tersangka utamanya indeks faiss 136 MB yang tidak
dipakai. Cara memisahkannya dari dua tersangka lain sudah jadi Soal 4c.

Waktunya: muat 22 detik sekali, lalu 0,42 detik untuk 4 detik audio di GPU,
dan 6,63 detik di CPU. RTF 1,66 di CPU berarti lebih lambat daripada waktu
nyata, dan itulah satu-satunya alasan RVC memakai GPU meskipun Roadmap
menjanjikan seluruh Bulan 3 di CPU. `RVC_AKTIF = False` mengembalikan janji
itu dengan harga suara Piper polos.

### Enam kesalahan saya di bulan ini

1. Ramalan stasioneritas saya terbalik. Saya menulis Bagian 6 Sesi 3 dengan
   keyakinan bahwa sumbu frekuensi yang tidak stasioner. Terukur, sumbu waktu
   yang tidak stasioner, dan sebabnya cara dataset dipotong. Ramalannya saya
   tinggalkan di dalam berkas supaya bisa dibandingkan.

2. Ambang wake word semula saya ambil dari titik kesalahan setara, yaitu
   0,047. Akibatnya Bagian 6 melaporkan latensi minus 2.000 milidetik, karena
   model menyala di jendela pertama yang isinya derau. Angka mustahil itu
   yang menunjukkan bahwa ambangnya salah, bukan latensinya.

3. Latensi diukur terhadap titik acuan yang salah. Sesudah ambangnya
   diperbaiki, angkanya masih minus 300 milidetik, dan sebabnya saya mengukur
   terhadap ujung kliping satu detik, bukan terhadap akhir tenaga katanya.
   Kliping Speech Commands punya 250 milidetik sunyi di tiap ujung.

4. `roc` saya tidak menangani peringkat SERI, jadi dua kumpulan skor yang
   identik memberi AUC 0,25 dan bukan 0,5. Yang menangkapnya bukan mata saya
   melainkan `kunci_b3_bukti.py`, yang memang saya tulis untuk itu.

5. `bikin_model` tidak memaku seed sebelum bobotnya diinisialisasi, jadi dua
   baris tabel yang seharusnya cuma berbeda pada fiturnya juga berbeda pada
   bobot awalnya. Perbandingan di Bagian 3 dan 4 kehilangan pengendaliannya
   sampai baris itu dipindahkan.

6. Pengunduh Speech Commands versi pertama tidak menangani awalan `./` pada
   nama anggota tar. Ia berjalan empat menit tanpa satu pun pesan galat dan
   tanpa satu pun berkas tertulis. Kegagalan yang paling mahal memang yang
   diam.

Ditambah satu yang bukan kesalahan saya tetapi memakan waktu sama banyaknya:
torch dan ctranslate2 masing-masing membawa cuDNN sendiri, jadi memanggil
faster-whisper lebih dulu membuat RVC mati dengan
`Could not load symbol cudnnGetLibConfig. Error code 127`. Tambalannya satu
konvolusi 3x3 di atas tensor 8x8 sebelum Whisper dimuat, ditandai `ponytail:`
dengan cara memeriksa kapan ia boleh dihapus.

### Wake word akhirnya dilatih dengan suara pemilik

Pemilik merekam sendiri di hari yang sama: 44 ucapan "hey synesis" dan 24
ucapan yang bunyinya mirip tetapi bukan. Daftar apa yang perlu diucapkan
beserta variasinya ditulis lebih dulu di `synesis/SCRIPT.md`, dan bagian
negatifnya yang paling menentukan: `sinusitis`, `sintesis`, `genesis`,
`hey series`, `sis`, `esis`, ditambah delapan kalimat percakapan biasa.

Ke-24 negatif itu mendarat di folder yang salah, yaitu `suara/bangun`
bernomor 044 sampai 067, karena `rekam_contoh` selalu menulis ke sana.
Ketahuan dengan mentranskripsi berkas di sekitar batasnya:

```text
bangun_043  'Bangun Seren'      <- positif, Whisper tidak tahu kata "synesis"
bangun_044  'Hey!'              <- negatif, sudah masuk daftar bagian B
bangun_053  'Genesis'
bangun_067  'Udah itu aja'
```

Dipindahkan ke `suara/bukan`, lalu dilatih:

```text
positif 44   negatif 24 + 1.320 Speech Commands
AUC 0,9867   ambang 0,960 dari ongkos 100 banding 1

ambang   lolos positif   lolos negatif mirip
 0,500          93,2%              20,8%
 0,900          90,9%               0,0%
 0,960          90,9%               0,0%
 0,990          59,1%               0,0%
```

Baris 0,900 dan 0,960 identik, dan itu bentuk yang sama dengan yang muncul
di Sesi 4 dengan `marvin`: sekali FAR menyentuh nol, menaikkan ambang cuma
menambah kegagalan mengenali tanpa membeli apa pun.

Tiga rekaman puncaknya di bawah 0,05 dan sebaiknya diulang. Sisanya sehat:
puncak 0,004 sampai 0,700 dengan median 0,269, tidak satu pun mentok.

### Peluncur .exe, dan kenapa isinya cuma 8 MB

`SYNESIS.exe` di akar repo. Yang dikemas PyInstaller hanya `synesis/luncur.py`,
yaitu menu yang mencari python di `E:\SYNESIS\.venv` lalu memanggilnya.
torch, onnxruntime, dan seluruh bobot tetap di tempatnya.

```text
kemas peluncur saja     8,0 MB, dibangun 16 detik
kemas seluruh SYNESIS   sekitar 3 GB, belasan menit, dan pecah tiap kali
                        torch atau onnxruntime menambah berkas data yang
                        tidak terdeteksi PyInstaller
```

Harga keputusan itu perlu ditulis terang-terangan: .exe-nya BUKAN paket
portabel. Memindahkan SYNESIS ke komputer lain berarti memindahkan repo dan
`E:\SYNESIS`, bukan menyalin satu berkas.

`SYNESIS.cmd` mengerjakan hal yang sama tanpa perlu dibangun ulang, dan itu
yang dipakai kalau `luncur.py` baru saja diubah.

### Manual ditulis ulang

`synesis/MANUAL.md` sebelumnya berbahasa Inggris dan cuma memuat v0.1. Ia
ditulis ulang dalam bahasa Indonesia untuk v0.2: peluncur, dua mode, kelas
risiko, rantai suara lengkap dengan anggaran waktunya, wake word beserta
angkanya, tiga bahasa, pagar keamanan, peta seluruh berkas, tabel kerusakan,
dan bagian batasnya yang jujur.

`script.md` ikut dipindahkan jadi `synesis/SCRIPT.md`, supaya seluruh dokumen
yang dibaca saat memakai SYNESIS ada di satu folder dengan kodenya.

### Satu alat kecil yang lahir dari kesalahan pemilik

Rekaman pertama pemilik satu berkas m4a sepanjang 26,9 detik berisi kalimat
menyambung, bukan 44 ucapan terpisah. Dari situ lahir
`python -m synesis.suara potong`, yang membaca m4a lewat `av` tanpa ffmpeg,
memotongnya per ucapan dengan VAD Bulan 3, dan melaporkan tiap potongan:

```text
  no    mulai   durasi   puncak  catatan
   1    0.15s    8.51s    0.985  terlalu panjang, mungkin dua ucapan menyatu
   2   10.53s   16.48s    0.493  terlalu panjang, mungkin dua ucapan menyatu
```

Dua peringatan itu yang jadi aturan nomor satu di `SCRIPT.md`: berhenti
sekitar satu detik sesudah tiap ucapan, karena pemotongnya bekerja dari jeda
dan bukan dari hitungan.

### Suara Yukino dalam tiga bahasa

Piper menentukan bahasa dan iramanya, RVC menentukan warna suaranya. Jadi
menambah bahasa cuma menambah satu berkas .onnx, dan orangnya tetap sama.

Diperiksa dengan mengembalikan keluaran RVC ke Whisper, tiap bahasa dengan
kode bahasanya sendiri:

```text
en  piper  -> Good evening, Sandy. I am Sineces. Your lab report ... already open.
en  yukino -> Good evening, Sandy. I am Sineces. Your lab report ... already open.
id  piper  -> Halo Sandy, saya Shinesis. Naporan praktikku minggu lalu sudah saya buka.
id  yukino -> Halo Sandy, saya Shenezis. Laporan Paktikum Minggu lalu sudah saya buka.
```

Baris en identik kata per kata, dan baris id yukino justru LEBIH benar
daripada keluaran Piper-nya sendiri. Bahasa Jepang butuh `pyopenjtalk-plus`,
karena `pyopenjtalk` asli tidak punya wheel untuk Python 3.12.

Suara pemilik sendiri juga dikonversi jadi Yukino sebagai uji arah sebaliknya.
f0 median pemilik 144 Hz, Yukino 261 Hz, jadi jarak nadanya +10,4 semiton,
dan `nada=+10` yang paling benar: f0 keluarannya mendarat di 248 Hz dan
transkripsinya paling utuh di antara ketiga pilihan.

---

## Berikutnya

**Bulan 3 tutup.** Wake word sudah dilatih dengan suara pemilik sendiri,
AUC 0,9867, dan peluncurnya tinggal diklik dua kali. Yang tersisa cuma
menyetelnya sesudah dipakai sungguhan, dan itu memerlukan jam pemakaian,
bukan baris kode.

**Bulan 2** masih punya utang yang sama seperti sebelumnya: 41 kalimat nyata
terlalu sedikit, dan hipotesis label tumpang tindih belum diuji. Keduanya
tidak menghalangi Bulan 4, dan `audit.jsonl` sekarang terisi jauh lebih cepat
karena perintah bisa masuk lewat suara.

**Roadmap:** klaim 80 sampai 90 persen di Bagian 4 `docs/Roadmap.md` masih
belum punya dukungan pengukuran. Satu janji lain sudah terbukti dilanggar
dengan sengaja: "semua di CPU, GPU disimpan untuk Bulan 6" tidak berlaku
untuk RVC, yang RTF-nya 1,66 di CPU.

**Bulan 4** belum disusun. Menurut Roadmap: metric learning dan pengenalan
wajah, sekitar 20 jam, tiga sesi. Kurva ROC dan kalibrasi ambang yang dipakai
di Bulan 3 Sesi 4 dan 5 akan dipakai lagi di sana untuk FAR dan FRR wajah,
jadi bagian itu sudah punya fondasinya.
