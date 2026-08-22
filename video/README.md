# Seri video SYNESIS

Penjelasan visual, format tegak 720x1280 supaya enak dilihat di layar telepon.
Dua seri: Bulan 0 dan Bulan 1, masing-masing empat bab.

Dibuat dengan Manim 0.19 memakai venv yang sudah ada di `S:\Code\manimations\.venv`.
Repo ini tidak menyimpan venv sendiri.

## Seri Bulan 0

| Bab | Judul | Isi | Durasi |
|---|---|---|---|
| 1 | Menuruni Bukit | Sesi A. Loss, gradien, dan empat baris training loop | 41,8 detik |
| 2 | Lanskap dan Langkah | Sesi B. Permukaan loss 3D, kontur, dan batas `2/lambda_max` | 43,9 detik |
| 3 | Menghafal atau Paham | Sesi C. Overfitting, dan Ridge sebagai Hukum Hooke | 43,0 detik |
| 4 | Mesin Turunan | Sesi D dan Bulan 1. Graf komputasi dan isi `loss.backward()` | 40,2 detik |

Gabungan keempatnya: `keluaran/synesis-bulan0-lengkap.mp4`, 2 menit 49 detik.

## Seri Bulan 1

| Bab | Judul | Isi | Durasi |
|---|---|---|---|
| 1 | Garis Tidak Cukup | Sesi 2. MLP, lipatan ReLU, dan titik awal yang menentukan | 30,4 detik |
| 2 | Sepuluh Pilihan | Sesi 3. Softmax, entropi silang, dan angka tulisan tangan | 31,8 detik |
| 3 | Dinding di Depan | Ongkos satu objek per angka, dan batas rekursi | 29,6 detik |
| 4 | Pegas dan Gesekan | Sesi 4. Momentum, RMSprop, Adam sebagai osilator teredam | 38,3 detik |

Gabungannya: `keluaran/synesis-bulan1-lengkap.mp4`, 2 menit 10 detik.

Sesi 2 sampai 4 belum dikerjakan pemilik saat seri ini dibuat. Karena itu
seri Bulan 1 menjelaskan konsep dan gejalanya, dan sengaja tidak menampilkan
kode jawaban satu pun. MLP di `siapkan_data_bulan1.py` ditulis vektor penuh
dengan numpy, bentuk yang berbeda dari kelas `Value` yang harus dibangun
sendiri di Sesi 2.

### Angka Bulan 1 dan asalnya

| Angka | Muncul di | Asalnya |
|---|---|---|
| garis lurus 90,67 persen lawan MLP 99,33 persen | Bulan 1 Bab 1 | dua bulan sabit, 300 titik |
| 1 dari 8 titik awal nyangkut di 92,33 persen | Bulan 1 Bab 1 | survei delapan seed |
| akurasi uji 97,98 persen | Bulan 1 Bab 2 | angka 8x8 sklearn, 397 gambar uji |
| 258 objek Value per iterasi, 1.032.000 total | Bulan 1 Bab 3 | cacah `Value.__init__` |
| 0,417 ms lawan 0,012 ms | Bulan 1 Bab 3 | satu langkah Value lawan numpy |
| batas rekursi 996, dinding di 784+256 | Bulan 1 Bab 3 | bagi dua pada mesin autograd pemilik |
| SGD tidak sampai, Adam iterasi 126 | Bulan 1 Bab 4 | lembah bilangan kondisi 384 |

Seri Bulan 1 membaca `video/data/bulan1.npz`. Bangun ulang berkas itu dengan
venv SYNESIS, bukan venv manim, karena butuh sklearn:

```powershell
. .\scripts\activate.ps1
python video\siapkan_data_bulan1.py
```

## Aturan yang dipegang

Tidak ada satu pun angka di layar yang diketik manual. Semuanya dihitung ulang
di dalam berkas babnya, memakai generator, seed, dan rumus yang sama persis
dengan yang ada di `notebooks/`. Kalau kamu mengubah `sesiC_multivariat.py`,
angka di Bab 3 ikut berubah saat dirender ulang.

Beberapa angka yang muncul dan asalnya:

| Angka | Muncul di | Asalnya |
|---|---|---|
| `w = 3.018114`, `b = 1.743558` | Bab 1 | `lstsq` pada data seed 42 |
| `lambda_max = 15.7233`, batas `0.127200` | Bab 2 | nilai eigen Hessian `(2/n) A^T A` |
| test `6.3470` lalu `923.5812` | Bab 3 | derajat 8 lalu 9, data seed 7 dan 99 |
| test `3.8e6` lalu `5.0121` | Bab 3 | derajat 12, tanpa denda lalu `lambda = 0.1` |
| galat `1.866e-08`, cocok `0.000e+00` | Bab 4 | 300 ekspresi acak di `bulan1_sesi1_autograd.py` |

## Cara render

```powershell
cd "S:\Code\Make A Jarvis\video"
S:\Code\manimations\.venv\Scripts\python.exe -m manim -ql --disable_caching -o bab1.mp4 bab1_menuruni.py Bab1
```

Bendera `-ql` tidak menurunkan mutunya. Ukuran bingkai dan laju bingkai
dipaksa oleh `siapkan()` di `sinema.py`, jadi keluarannya tetap 720x1280 pada
30 bingkai per detik apa pun bendera mutunya. Yang berubah cuma lama render.

Atau sekaligus empat-empatnya:

```powershell
.\render.ps1
```

## Berkas

- `sinema.py` kit gaya bersama: palet, bingkai tegak, judul, panel kode dengan
  penyorot baris, kartu angka, dan pembaca data
- `bab1_menuruni.py` sampai `bab4_mesin.py` seri Bulan 0
- `b1_bab1_garis.py` sampai `b1_bab4_pegas.py` seri Bulan 1
- `siapkan_data_bulan1.py` pra-hitung seri Bulan 1, dijalankan dengan venv SYNESIS
- `data/` hasil pra-hitung, tidak masuk git
- `render.ps1` render seri Bulan 0 lalu menyambungnya jadi satu
- `keluaran/` hasil render, tidak masuk git
- `media/` berkas antara dari manim, tidak masuk git

## Kalau mau menyunting

Ubah `PALET` di `sinema.py` untuk mengganti warna seluruh seri sekaligus.
Tata letaknya diatur enam tetapan `Y_` di berkas yang sama, dalam satuan
bingkai dengan `y` dari `-8` sampai `8`.
