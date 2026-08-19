# Soal Hari 2 — Memahami NumPy

Berkas latihan: [`hari02_numpy.py`](hari02_numpy.py)

## Cara pengerjaan

Kerjakan secara berurutan. Kamu harus menyelesaikan Soal 2 sebelum bisa lanjut ke Soal 3.

Hint (petunjuk) sengaja disembunyikan. Coba kerjakan sendiri minimal 15 menit sebelum mengklik petunjuk pertama. Kalau kamu langsung melihat jawaban, kodenya memang akan jalan, tapi kamu nggak akan paham konsepnya—nanti pas masuk ke materi Bulan 1 kamu bakal kesulitan sendiri.

---

## Soal 1 — Tebak Dimensi (Shape)

Sebelum menjalankan kodenya, **tulis dulu tebakanmu** untuk enam operasi di bawah ini. Jawab dengan bentuk (shape) hasil akhirnya, atau tulis ERROR kalau menurutmu operasi tersebut bakal gagal.

```python
A = np.zeros((3, 4))
u = np.zeros(3)
v = np.zeros(4)
```

| No | Ekspresi | Tebakanmu | Hasil |
|---|---|---|---|
| 1a | `A + v` | `(3, 4)` | `(3, 4)` |
| 1b | `A + u` | `ERROR` | `ERROR` |
| 1c | `u[:, None] + v[None, :]` | `(3, 4)` | `(3, 4)` |
| 1d | `u + u[:, None]` | `(3, 3)` | `(3, 3)` |
| 1e | `np.zeros((2,3,4)) + np.zeros((3,4))` | `(2, 3, 4)` | `(2, 3, 4)` |
| 1f | `np.zeros((5,1,3)) + np.zeros((1,4,3))` | `(5, 4, 3)` | `(5, 4, 3)` |

Pastikan kamu mengisi semua kolom tebakan sebelum me-run script-nya. Baru bandingkan hasilnya.

<details>
<summary>Petunjuk 1</summary>

Posisikan dimensinya dari kanan ke kiri, lalu cek satu per satu.

```
A : (3, 4)
v :    (4,)
      ─────
      cocok? kolom paling kanan 4 vs 4, kolom kirinya 3 vs kosong
```

Kalau ada dimensi yang kosong di sebelah kiri, NumPy bakal nganggep ukurannya 1.
</details>

<details>
<summary>Petunjuk 2</summary>

Aturan broadcasting itu simpel, per kolom cuma ada tiga kemungkinan:

- Angkanya sama → aman
- Salah satu angkanya 1 → angka 1 ini akan di-stretch (diperpanjang) menyesuaikan dimensi lawannya
- Selain kondisi di atas → ERROR

Untuk 1d: shape `u` itu `(3,)`, sedangkan `u[:, None]` itu `(3,1)`. Kalau dijejerin dari kanan: `(3,)` dianggap `(1,3)`. Berarti operasinya adalah menjumlahkan array berukuran `(3,1)` dengan `(1,3)`.
</details>

**Lanjut jika:** Keenam tebakanmu benar sebelum kodenya dijalankan. Kalau masih ada yang salah tebak, jangan dulu lanjut ke soal berikutnya. Pahami ulang aturannya sampai kamu bisa menebak dengan benar.

---

## Soal 2 — Bikin `dot_manual(a, b)`

Coba hitung dot product dari dua array 1D menggunakan perulangan (loop) Python biasa.

**Dilarang pakai:** `np.dot`, `np.sum`, `sum()`, `@`, atau trik `zip` comprehension. Tujuannya biar kamu terbiasa nulis loop sendiri secara manual, bukan nyari jalan pintas.

**Target hasil:**

```python
dot_manual(np.array([1, 2, 3]), np.array([4, 5, 6]))   # -> harusnya 32
```

<details>
<summary>Petunjuk 1</summary>

Pakai satu loop dan satu variabel penyimpan hasil (akumulator). Mulai dari 0, lalu tambahkan hasil perkalian tiap pasang angkanya.
</details>

<details>
<summary>Petunjuk 2</summary>

```python
total = 0.0
for i in range(len(a)):
    ...
return total
```

Yang perlu kamu tulis cuma satu baris di dalam loop itu.
</details>

<details>
<summary>Petunjuk 3</summary>

Isi baris yang kosong tadi dengan ngejumlahin `a[i] * b[i]` ke variabel `total`.

Kalau masih bingung juga, coba tulis versi manualnya (tanpa loop) buat array berisi 3 elemen, lalu perhatiin polanya:

```python
total = a[0]*b[0] + a[1]*b[1] + a[2]*b[2]
```
</details>

---

## Soal 3 — Bikin `matmul_manual(A, B)`

Buat fungsi perkalian matriks `(n,k) × (k,m) → (n,m)` pakai loop Python murni.

**Target hasil:**

```python
A = np.array([[1., 2.], [3., 4.]])
B = np.array([[5., 6.], [7., 8.]])
matmul_manual(A, B)
# [[19. 22.]
#  [43. 50.]]
```

Hitung manual di kertas dulu sebelum nge-run kodenya. Kalau hasil hitungan tanganmu beda sama kodenya, kemungkinan besar pemahaman rumus matriksumu yang kurang pas, bukan murni salah kode.

<details>
<summary>Petunjuk 1</summary>

Elemen `C[i,j]` itu pada dasarnya adalah hasil dot product antara **baris ke-i dari matriks A** dan **kolom ke-j dari matriks B**.

Intinya, soal ini cuma ngulang-ngulang logika yang udah kamu bikin di Soal 2.
</details>

<details>
<summary>Petunjuk 2</summary>

Kamu butuh tiga loop bersarang (nested loops). Tentukan dulu tugas tiap variabelnya:

- `i` untuk iterasi baris matriks hasil
- `j` untuk iterasi kolom matriks hasil
- `k` buat proses penjumlahannya

Di loop mana variabel akumulatornya ditaruh? Pasti di loop yang paling dalam.

Bikin dulu wadah matriks kosong buat nampung hasilnya:

```python
n, k = A.shape
k2, m = B.shape
C = np.zeros((n, m))
```
</details>

<details>
<summary>Petunjuk 3</summary>

```python
for i in range(n):
    for j in range(m):
        total = 0.0
        for kk in range(k):
            ...          # <- isi satu baris ini
        C[i, j] = total
return C
```

Baris yang kosong itu tugasnya nambahin nilai `A[i, kk] * B[kk, j]` ke dalam `total`.

Hati-hati sama urutan indeksnya. `A[i, kk]` itu bergerak ke samping menyusuri baris, sedangkan `B[kk, j]` bergerak ke bawah menyusuri kolom. Kalau sampai ketukar posisinya, hasilnya malah jadi matriks transpos.
</details>

<details>
<summary>Petunjuk 4: Kalau hasil kodenya malah jadi transpos</summary>

Mungkin kamu nulisnya `B[j, kk]` padahal seharusnya `B[kk, j]`. Indeks penjumlahan `kk` itu posisinya harus ada di bagian **baris** pada matriks B.
</details>

---

## Soal 4 — Analisis Performa

Setelah bagian pengujian kecepatan (benchmark) selesai jalan, coba jawab empat pertanyaan ini. Jawabannya murni dari angka yang muncul di terminalmu, nggak usah cari di internet.

**4a.** Waktu nyobain `dot`, berapa kali lipat kecepatan Numpy menang telak saat `n = 1.000` dibanding saat `n = 1.000.000`? Menurutmu kenapa perbedaan kecepatannya malah makin jauh pas datanya makin gede?
> **Jawaban:** Saat `n=1.000` NumPy menang sekitar 24x lipat, namun saat `n=1.000.000` kemenangannya meroket sampai 523x lipat. Pas datanya kecil, persentase waktu banyak habis terpotong untuk *overhead* pemanggilan fungsi ke C. Namun saat datanya raksasa, komputasi murni yang super efisien di C (memanfaatkan SIMD/BLAS) jauh meninggalkan loop Python yang melambat secara konstan/linear.

**4b.** Di bagian `matmul`, ukur waktu eksekusi fungsi manualmu untuk matriks `100×100` dan `200×200`. Berapa kali lebih lambat? Apakah hasilnya sesuai dengan teori kompleksitas algoritma `O(n³)`?
> **Jawaban:** Waktu pengerjaan melambat dari ~361 ms (100x100) menjadi ~2889 ms (200x200), alias 8 kali lebih lambat. Ini sangat sesuai dengan teori $O(n^3)$ karena ketika dimensi matrik (n) dilipatgandakan $2 \times$, beban perulangan bertambah $2^3 = 8$ kali lipat.

**4c.** Kenapa waktu eksekusi NumPy tetep butuh waktu sekian milidetik, nggak bisa benar-benar instan (nol)? Memangnya apa sih proses internal yang harus dikerjain walau kode aslinya udah berupa bahasa C?
> **Jawaban:** Walaupun dieksekusi di ranah C, Python tetap butuh waktu untuk mengecek tipe data memori (*type checking*), mengalokasikan RAM untuk array output baru, dan menerjemahkan pemanggilan objek Python ke struktur C-Array (overhead *C API*).

**4d.** Coba hitung secara kasar, kalau fungsi `dot_manual` dieksekusi buat array sebesar `n = 100.000.000`, kira-kira butuh waktu berapa lama? Estimasikan dari angka yang udah kamu punya aja, jangan nekat ngerun kodenya (bisa nge-hang komputernya).
> **Jawaban:** Berdasarkan data `n = 1.000.000` (yang butuh ~283 ms) dan fakta bahwa kerumitan kodenya linier $O(n)$, maka `n = 100.000.000` (100 kali lipat) akan memakan waktu setidaknya $283 \times 100 = 28.300$ ms, alias sekitar **28 detik**.

<details>
<summary>Petunjuk 4a</summary>

Tiap kali fungsi NumPy dipanggil dari Python, ada "biaya administrasi" (overhead) tetap yang wajib jalan: ngecek tipe data, alokasi memori, dsb. Overhead ini makan waktu yang sama persis entah datanya besar atau kecil.

Pas datanya kecil (`n=1.000`), overhead ini kerasa gede banget ngebebanin kodenya. Tapi pas komputasinya makin berat (`n=1.000.000`), waktu buat overhead ini jadi nggak seberapa dibanding waktu perhitungannya, makanya porsinya mengecil.
</details>

<details>
<summary>Petunjuk 4b</summary>

Tiga loop bersarang di mana masing-masing ngerun n iterasi berarti total kerjanya `n × n × n`.

Dari ukuran 100 naik ke 200 itu berarti `n` membesar 2 kali lipat. Berdasarkan rumusnya, harusnya total pengerjaannya jadi berapa kali lipat?
</details>

---

## Soal 5 — Debugging (Nyari bug yang nggak ngeluarin error)

Ini simulasi error logika yang sering bikin pusing karena Python nggak nampilin peringatan apa-apa. Nanti di Bulan 1 kamu bakal nemu kasus serupa.

```python
X = rng.random((3, 3))        # 3 sampel, 3 fitur. Matriks persegi.

mean_fitur  = X.mean(axis=0)  # rata-rata per kolom -> shape (3,)
mean_sampel = X.mean(axis=1)  # rata-rata per baris -> shape (3,)

A = X - mean_fitur            # Kodenya jalan
B = X - mean_sampel           # Kodenya juga jalan tanpa masalah
```

Kedua perhitungan di atas berhasil dieksekusi. Nggak ada error. Shape hasilnya sama-sama `(3,3)`.

**5a.** Kalau tujuan kamu adalah "mengurangi tiap kolom data dengan rata-rata fitur tersebut", operasi mana yang secara matematis bener?
> **Jawaban:** Operasi variabel `A`.

**5b.** Variabel `B` itu sebenarnya ngitung apaan sih secara logika? Coba jelasin pakai bahasamu.
> **Jawaban:** Variabel `B` secara salah mengurangkan setiap *kolom* dalam matriks `X` dengan rata-rata dari *baris*. Karena `mean_sampel` itu array `(3,)`, aturan broadcasting memaksanya jadi `(1,3)`, mengurangkannya mendatar alih-alih menurun. Secara statistik, perhitungan ini nggak punya makna logis.

**5c.** Benerin kode `B` biar dia ngurangin tiap **baris** matriks dengan nilai rata-rata baris tersebut.
> **Jawaban:** Kodenya harus disesuaikan dimensinya jadi vertikal: `B = X - mean_sampel[:, None]`.

**5d.** Kenapa bug semacam di perhitungan `B` ini nggak bakal kejadian kalau matriks `X` bentuknya `(100, 3)`? Hal ini ngajarin apa soal bikin dummy data buat ngetes algoritma?
> **Jawaban:** Karena jika `X` adalah `(100, 3)`, maka `mean_sampel` adalah `(100,)`. NumPy akan gagal mem-broadcasting shape `(100,)` dari kanan ke matriks `(100, 3)` (100 ketemu 3 dan error). Pesan moralnya: **Jangan pernah memakai matriks persegi (misal 3x3) sebagai dummy data untuk testing**. Matriks persegi bisa meloloskan error orientasi array/broadcasting seperti kasus ini.

<details>
<summary>Petunjuk 5c</summary>

Shape `mean_sampel` aslinya `(3,)`. Karena NumPy otomatis melakukan broadcasting dengan cara nyamain dimensi dari kanan, array ini dianggap array 2D dengan shape `(1,3)`. Artinya array 1 baris diulang (di-copy) ke bawah sebanyak 3 kali.

Padahal yang kamu perlukan itu bentuk kolom, di mana shape-nya wajib `(3,1)`.
</details>

<details>
<summary>Petunjuk 5d</summary>

Pada kasus `(100,3)`, output `mean_sampel` pasti berukuran `(100,)`. Waktu dijejerkan dari kanan untuk operasi matematika, NumPy bakal berusaha nyocokin angka 100 dengan 3. Karena nggak ada yang sama, dan nggak ada yang angka 1, NumPy nyerah lalu memunculkan pesan error.

Intinya: pakai matriks berbentuk persegi saat ngetes kode itu bahaya banget karena bisa nyembunyiin error bentuk array (shape errors). Biasain ngetes fungsi pakai dummy matriks dengan baris dan kolom yang panjangnya beda.
</details>

---

## Tolok Ukur Hari 2

- [x] Bisa menebak 6 dimensi output di Soal 1 dengan benar sebelum kodenya di-run
- [x] Fungsi `dot_manual` sukses menghasilkan nilai `32` saat dikasih tes `[1,2,3] · [4,5,6]`
- [x] Fungsi `matmul_manual` sukses mengalikan matriks 2×2 dan hasilnya klop sama hitungan kertas
- [x] Bagian benchmark kecepatan sukses nyelesaiin run-nya tanpa mental di tengah jalan gara-gara gagal fungsi `assert`
- [x] Keempat pertanyaan dari Soal 4 berhasil kamu jawab pakai angka yang muncul di layarmu sendiri
- [x] Berhasil nyelesaiin Soal 5, termasuk paham sama pesan moral di nomor 5d
- [x] Kamu bisa ngejelasin aturan main NumPy broadcasting ke orang lain tanpa harus nyontek catatan

Kalau 7 kotak di atas udah tercentang semua, selamat! Materi Hari 2 udah beres. Silakan lanjut ke Hari 3.
