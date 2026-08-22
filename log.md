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

## Berikutnya

**Bulan 2 Sesi 1** sudah siap di `soal-bulan2-sesi1.md`, tujuh TODO, belum
dikerjakan.

**Bulan 3** belum disusun.
