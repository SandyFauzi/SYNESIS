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

### Belum selesai

Menunggu pemilik mengisi TODO 3 dan TODO 4, lalu membaca hasil adu cepat.

---

## Berikutnya

**Hari 2, numpy sampai paham.** Broadcasting, slicing, lalu menulis dot product
dan perkalian matriks manual untuk diadu kecepatannya melawan np.dot.

Jadwal bergeser sepekan dari rencana semula. Hari 19 mendarat sekitar
7 September, kemungkinan sudah masuk masa kuliah.
