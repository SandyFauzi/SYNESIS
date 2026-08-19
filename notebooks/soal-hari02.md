# Soal Hari 2 — numpy sampai paham

Berkas kerja: [`hari02_numpy.py`](hari02_numpy.py)

## Cara pakai

Kerjakan berurutan. Soal 3 membutuhkan Soal 2 sudah beres.

Petunjuk disusun bertingkat dan tertutup. **Coba sendiri minimal 15 menit sebelum
membuka petunjuk pertama.** Kalau langsung dibuka, kamu mendapat kode yang jalan
tanpa mendapat pemahaman, dan Bulan 1 akan terasa mustahil.

---

## Soal 1 — Ramalkan bentuknya

Sebelum menjalankan apa pun, **tulis tebakanmu** untuk enam kasus berikut.
Jawab dengan bentuk hasilnya, atau tulis ERROR.

```python
A = np.zeros((3, 4))
u = np.zeros(3)
v = np.zeros(4)
```

| No | Ekspresi | Tebakanmu | Hasil |
|---|---|---|---|
| 1a | `A + v` | | |
| 1b | `A + u` | | |
| 1c | `u[:, None] + v[None, :]` | | |
| 1d | `u + u[:, None]` | | |
| 1e | `np.zeros((2,3,4)) + np.zeros((3,4))` | | |
| 1f | `np.zeros((5,1,3)) + np.zeros((1,4,3))` | | |

Baru setelah semua terisi, jalankan dan bandingkan.

<details>
<summary>Petunjuk 1</summary>

Sejajarkan bentuknya **dari kanan**, lalu periksa kolom per kolom.

```
A : (3, 4)
v :    (4,)
      ─────
      cocok? kolom kanan 4 lawan 4, kolom kiri 3 lawan kosong
```

Dimensi yang hilang di sebelah kiri dianggap 1.
</details>

<details>
<summary>Petunjuk 2</summary>

Tiga kemungkinan per kolom:

- angka sama → lolos
- salah satunya 1 → yang 1 diregangkan
- selain itu → ERROR

Untuk 1d: `u` bentuknya `(3,)`, `u[:, None]` bentuknya `(3,1)`. Sejajarkan dari
kanan: `(3,)` jadi `(1,3)`. Jadi `(3,1)` bertemu `(1,3)`.
</details>

**Selesai bila:** enam-enamnya kamu ramalkan benar sebelum menjalankan.
Kalau ada yang meleset, jangan lanjut. Ulangi sampai ramalanmu tepat.

---

## Soal 2 — `dot_manual(a, b)`

Tulis hasil kali dalam dua vektor 1D memakai loop Python murni.

**Dilarang:** `np.dot`, `np.sum`, `sum()`, `@`, `zip` dengan comprehension.
Tujuannya merasakan loop-nya, bukan menghindarinya.

**Cek benar:**

```python
dot_manual(np.array([1, 2, 3]), np.array([4, 5, 6]))   # -> 32
```

<details>
<summary>Petunjuk 1</summary>

Satu loop, satu penampung. Mulai dari 0, tambahkan hasil kali tiap pasangan.
</details>

<details>
<summary>Petunjuk 2</summary>

```python
total = 0.0
for i in range(len(a)):
    ...
return total
```

Yang perlu kamu isi cuma satu baris di dalam loop.
</details>

<details>
<summary>Petunjuk 3</summary>

Baris itu menambahkan `a[i] * b[i]` ke `total`.

Kalau masih macet, tulis dulu versi n=3 tanpa loop sama sekali, baru lihat
polanya:

```python
total = a[0]*b[0] + a[1]*b[1] + a[2]*b[2]
```
</details>

---

## Soal 3 — `matmul_manual(A, B)`

Perkalian matriks `(n,k) × (k,m) → (n,m)`, loop Python murni.

**Cek benar:**

```python
A = np.array([[1., 2.], [3., 4.]])
B = np.array([[5., 6.], [7., 8.]])
matmul_manual(A, B)
# [[19. 22.]
#  [43. 50.]]
```

Hitung dulu dengan tangan sebelum menjalankan. Kalau hasil tanganmu tidak sama,
masalahnya di pemahaman rumus, bukan di kode.

<details>
<summary>Petunjuk 1</summary>

`C[i,j]` adalah dot product antara **baris ke-i dari A** dan **kolom ke-j dari B**.

Jadi soal ini adalah Soal 2 yang dijalankan berkali-kali.
</details>

<details>
<summary>Petunjuk 2</summary>

Tiga loop bersarang. Tentukan dulu peran masing-masing:

- `i` menyusuri baris hasil
- `j` menyusuri kolom hasil
- `k` menjumlahkan

Loop mana yang berisi akumulator? Yang paling dalam.

Siapkan wadahnya lebih dulu:

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
            ...          # <- satu baris
        C[i, j] = total
return C
```

Baris yang kosong itu menambahkan `A[i, kk] * B[kk, j]` ke `total`.

Perhatikan urutan indeksnya. `A[i, kk]` bergerak menyusuri baris, `B[kk, j]`
bergerak menyusuri kolom. Tertukar sedikit saja hasilnya jadi transpos.
</details>

<details>
<summary>Kalau hasilnya transpos dari yang seharusnya</summary>

Kamu kemungkinan menulis `B[j, kk]` alih-alih `B[kk, j]`. Indeks penjumlahan
`kk` harus menjadi indeks **baris** pada B, karena dimensi dalam yang saling
meniadakan adalah `k`.
</details>

---

## Soal 4 — Baca angkanya

Setelah bagian adu cepat jalan, jawab empat pertanyaan ini. Jawabannya ada di
angka yang keluar, bukan di internet.

**4a.** Pada `dot`, berapa kali numpy menang saat `n = 1.000`, dan saat
`n = 1.000.000`? Kenapa rasionya berubah?

**4b.** Pada `matmul`, ukur waktu manual di `100×100` dan `200×200`. Berapa kali
lipat lebih lambat? Cocokkah dengan ramalan `n³`?

**4c.** Kenapa numpy tetap butuh waktu, tidak nol? Apa yang tetap harus
dikerjakan bahkan oleh kode C yang dioptimasi?

**4d.** Kalau `dot_manual` dijalankan pada `n = 100.000.000`, kira-kira berapa
lama? Hitung dari angka yang sudah kamu punya, jangan dijalankan.

<details>
<summary>Petunjuk 4a</summary>

Setiap pemanggilan numpy punya ongkos tetap: pemeriksaan tipe, alokasi,
pemanggilan fungsi Python. Ongkos itu sama besarnya untuk n kecil maupun besar.

Pada n kecil, ongkos tetap mendominasi. Pada n besar, ia tenggelam.
</details>

<details>
<summary>Petunjuk 4b</summary>

Tiga loop bersarang berukuran n berarti `n × n × n` iterasi.

Dari 100 ke 200, n berlipat dua. Jadi kerjanya berlipat berapa?
</details>

---

## Soal 5 — Cari bug yang tidak melempar error

Ini simulasi masalah yang akan menggigitmu di Bulan 1.

```python
X = rng.random((3, 3))        # 3 sampel, 3 fitur. Persegi.

mean_fitur  = X.mean(axis=0)  # rata-rata tiap kolom -> bentuk (3,)
mean_sampel = X.mean(axis=1)  # rata-rata tiap baris -> bentuk (3,)

A = X - mean_fitur            # jalan
B = X - mean_sampel           # jalan juga
```

Keduanya berjalan. Tidak ada error. Bentuk hasilnya sama-sama `(3,3)`.

**5a.** Kalau maksudmu "kurangi tiap fitur dengan rata-rata fiturnya", mana yang
benar?

**5b.** `B` sebenarnya menghitung apa? Jelaskan dengan kalimat.

**5c.** Perbaiki `B` agar mengurangi tiap **baris** dengan rata-rata barisnya.

**5d.** Kenapa bug ini tidak muncul kalau `X` berbentuk `(100, 3)`? Apa artinya
itu untuk kebiasaan mengujimu?

<details>
<summary>Petunjuk 5c</summary>

`mean_sampel` bentuknya `(3,)`. Broadcasting menyejajarkannya dari kanan, jadi
dia diperlakukan sebagai `(1,3)`, yaitu satu baris yang diulang ke bawah.

Kamu butuh dia jadi kolom: `(3,1)`.
</details>

<details>
<summary>Petunjuk 5d</summary>

Pada `(100,3)`, `mean_sampel` berbentuk `(100,)`. Sejajarkan dari kanan: 100
bertemu 3. Tidak cocok, tidak ada yang bernilai 1, jadi numpy melempar error.

Matriks persegi menyembunyikan kesalahan bentuk. Data uji yang baik memakai
dimensi yang **berbeda-beda**.
</details>

---

## Tolok Ukur Hari 2

- [ ] Enam ramalan bentuk di Soal 1 benar sebelum dijalankan
- [ ] `dot_manual` lolos uji `[1,2,3] · [4,5,6] = 32`
- [ ] `matmul_manual` lolos uji 2×2 dan cocok dengan hitungan tanganmu
- [ ] Bagian adu cepat berjalan tanpa `assert` gagal
- [ ] Empat pertanyaan Soal 4 terjawab dengan angka dari layarmu sendiri
- [ ] Soal 5 terjawab, termasuk 5d
- [ ] Kamu bisa menjelaskan aturan broadcasting tanpa membuka catatan

Kalau tujuh-tujuhnya tercentang, Hari 2 selesai dan Hari 3 terbuka.
