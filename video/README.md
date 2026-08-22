# Seri video SYNESIS

Penjelasan visual Bulan 0 sampai mesin autograd, empat bab, format tegak
720x1280 supaya enak dilihat di layar telepon.

Dibuat dengan Manim 0.19 memakai venv yang sudah ada di `S:\Code\manimations\.venv`.
Repo ini tidak menyimpan venv sendiri.

## Isi

| Bab | Judul | Isi | Durasi |
|---|---|---|---|
| 1 | Menuruni Bukit | Sesi A. Loss, gradien, dan empat baris training loop | 41,8 detik |
| 2 | Lanskap dan Langkah | Sesi B. Permukaan loss 3D, kontur, dan batas `2/lambda_max` | 43,9 detik |
| 3 | Menghafal atau Paham | Sesi C. Overfitting, dan Ridge sebagai Hukum Hooke | 43,0 detik |
| 4 | Mesin Turunan | Sesi D dan Bulan 1. Graf komputasi dan isi `loss.backward()` | 40,2 detik |

Gabungan keempatnya: `keluaran/synesis-bulan0-lengkap.mp4`, 2 menit 49 detik.

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
  penyorot baris, dan kartu angka
- `bab1_menuruni.py` sampai `bab4_mesin.py` satu bab satu berkas
- `render.ps1` render keempatnya lalu menyambungnya jadi satu
- `keluaran/` hasil render, tidak masuk git
- `media/` berkas antara dari manim, tidak masuk git

## Kalau mau menyunting

Ubah `PALET` di `sinema.py` untuk mengganti warna seluruh seri sekaligus.
Tata letaknya diatur enam tetapan `Y_` di berkas yang sama, dalam satuan
bingkai dengan `y` dari `-8` sampai `8`.
