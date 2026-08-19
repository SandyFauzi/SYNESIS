# Soal Hari 3 — Data dan Loss

Berkas latihan: [`hari03_data_loss.py`](hari03_data_loss.py)

Hari ini kamu membangun **permukaan** yang akan dituruni di Hari 7. Belum ada
gradient descent. Lanskapnya dulu.

Aturan mainnya sama seperti Hari 2: coba sendiri minimal 15 menit sebelum
membuka petunjuk.

---

## Soal 1 — Urutkan sebelum menghitung

Enam tebakan ini ada di Bagian 3. **Urutkan dari loss terkecil ke terbesar
tanpa menjalankan kode apa pun.** Pakai penalaran, bukan tebakan asal.

| Tebakan | w | b | Ranking (1 = terkecil) |
|---|---|---|---|
| A | 0.0 | 0.0 | |
| B | 1.0 | 0.0 | |
| C | 3.0 | 0.0 | |
| D | 5.0 | 2.0 | |
| E | 3.0 | 2.0 | |
| F | 2.9 | 2.1 | |

Parameter aslinya `w = 3`, `b = 2`, dan `x` tersebar di rentang `[-5, 5]`.

<details>
<summary>Petunjuk 1</summary>

Kesalahan pada `w` berlipat oleh `x`. Kalau `w` meleset sebesar `Δw`, ramalanmu
meleset sebesar `Δw · x`, dan `x` bisa sampai 5.

Kesalahan pada `b` tidak berlipat. Meleset `Δb` berarti meleset `Δb` saja,
di semua titik.

Jadi antara salah `w` sebesar 1 dan salah `b` sebesar 1, mana yang lebih mahal?
</details>

<details>
<summary>Petunjuk 2</summary>

Hitung kasar kesalahan tipikal untuk tiap tebakan, ambil `x` tipikal sekitar 2,5:

- A: `Δw = 3`, `Δb = 2` → meleset sekitar `3(2,5) + 2 = 9,5`
- C: `Δw = 0`, `Δb = 2` → meleset sekitar `2`

Kuadratkan, lalu bandingkan.
</details>

**Selesai bila:** urutanmu cocok dengan hasil program.

---

## Soal 2 — Tiga fungsi

### 2a. `prediksi(x, w, b)`

Ramalan model garis lurus. Terima array `x`, kembalikan array.

Boleh pakai operasi vektor numpy. Hari 2 sudah membuktikan kenapa loop tidak
perlu di sini.

### 2b. `mse(y_ramal, y_asli)`

$$\text{MSE} = \frac{1}{n}\sum_i (\hat{y}_i - y_i)^2$$

**Dilarang:** `np.mean`, `np.square`, sklearn.
**Boleh:** pengurangan array, perkalian array, dan `np.sum` untuk penjumlahan akhir.

Kembalikan satu angka.

### 2c. `mae(y_ramal, y_asli)`

$$\text{MAE} = \frac{1}{n}\sum_i |\hat{y}_i - y_i|$$

Pembanding untuk Soal 3.

<details>
<summary>Petunjuk 2b</summary>

Tiga langkah, tiap langkah satu baris:

1. Hitung selisihnya. Array dikurangi array menghasilkan array.
2. Kuadratkan. `arr * arr` tanpa `np.square`.
3. Jumlahkan lalu bagi banyaknya.
</details>

<details>
<summary>Petunjuk 2c</summary>

`np.abs` boleh dipakai. Yang dilarang cuma `np.mean` dan `np.square`.
</details>

**Cek benar:**

```python
y_ramal = np.array([1.0, 2.0, 3.0])
y_asli  = np.array([1.0, 2.0, 5.0])
mse(y_ramal, y_asli)   # -> 1.3333...   karena (0 + 0 + 4)/3
mae(y_ramal, y_asli)   # -> 0.6666...   karena (0 + 0 + 2)/3
```

---

## Soal 3 — Analisis

**3a.** Pada baris "parameter asli" (`w=3, b=2`), loss-nya **tidak nol**.
Kenapa? Angka sisa itu mewakili apa?

**3b.** Kalau kamu menemukan model dengan loss **lebih kecil** dari nilai di 3a,
apakah itu kabar baik? Jelaskan.

**3c.** Bandingkan MSE dan MAE untuk beberapa tebakan yang sama. Tambahkan satu
titik pencilan ke datamu, misalnya ubah satu nilai `y` jadi `y[0] + 50`.
Mana yang berubah lebih drastis? Kenapa?

**3d.** Kenapa MSE memakai kuadrat, bukan nilai mutlak? Beri **dua** alasan:
satu soal turunan, satu soal derau.

**3e.** Loss di parameter asli keluar sekitar **1,36**, padahal derau
dibangkitkan dengan `sigma = 1.5`, jadi variansnya **2,25**. Kenapa keduanya
tidak sama?

Ubah `n` pada `buat_data` menjadi 200, lalu 1000, lalu 10000. Catat angkanya
tiap kali. Apa yang kamu simpulkan?

<details>
<summary>Petunjuk 3e</summary>

Pada parameter asli, selisih ramalan terhadap data **adalah** derau itu sendiri.
Jadi loss-nya adalah rata-rata kuadrat derau atas `n` sampel.

Nilai harapannya memang $\sigma^2$. Tapi rata-rata satu sampel berhingga bukan
nilai harapan, ia berfluktuasi di sekitarnya. Sebaran fluktuasinya:

$$\text{SD}[\text{MSE}] = \sigma^2\sqrt{\frac{2}{n}}$$

Untuk `n = 50` dan `sigma = 1.5`, angkanya sekitar 0,45. Sampel dengan seed 42
kebetulan jatuh sekitar dua simpangan baku di bawah rata-rata.

Ini konsep yang sama dengan ketidakpastian pengukuran di Eksperimen Fisika.
Memperbanyak titik data mempersempit sebarannya sebanding $1/\sqrt{n}$.
</details>

<details>
<summary>Petunjuk 3d, alasan turunan</summary>

Gambar $f(e) = e^2$ dan $g(e) = |e|$ di sekitar $e = 0$.

Yang satu mulus di titik nol. Yang satu punya patahan tajam.

Di Hari 5 kamu akan menurunkan loss terhadap `w`. Apa yang terjadi kalau
fungsinya punya patahan?
</details>

<details>
<summary>Petunjuk 3d, alasan derau</summary>

Data kamu dibangkitkan dengan `rng.normal`, yaitu derau gaussian.

Rapat peluang gaussian memuat $e^{-(x-\mu)^2/2\sigma^2}$. Ambil logaritmanya,
lalu perhatikan suku yang bergantung pada data.

Ini materi Fisika Statistik. Meminimalkan MSE sama dengan memaksimalkan
peluang, **asalkan** derau memang gaussian.
</details>

---

## Soal 4 — Buktikan parabolanya

Bagian 4 menghasilkan kurva berbentuk parabola. **Buktikan secara aljabar**
bahwa MSE selalu berbentuk kuadratik terhadap `w` saat `b` dikunci.

Mulai dari:

$$\text{MSE}(w) = \frac{1}{n}\sum_i (w x_i + b - y_i)^2$$

Tunjukkan bahwa bentuknya $Aw^2 + Bw + C$, lalu tuliskan `A`, `B`, dan `C`
dalam bentuk rata-rata atas data.

Ini kerja Fisika Matematika, kerjakan di kertas.

<details>
<summary>Petunjuk 1</summary>

Tulis $r_i = w x_i + (b - y_i)$ lalu jabarkan $r_i^2$.

Kelompokkan sukunya berdasarkan pangkat `w`.
</details>

<details>
<summary>Petunjuk 2</summary>

$$(w x_i + c_i)^2 = w^2 x_i^2 + 2 w x_i c_i + c_i^2 \qquad \text{dengan } c_i = b - y_i$$

Sekarang jumlahkan atas `i` dan bagi `n`. Suku mana yang membawa $w^2$?
</details>

<details>
<summary>Petunjuk 3</summary>

$$A = \frac{1}{n}\sum x_i^2 \qquad B = \frac{2}{n}\sum x_i(b - y_i) \qquad C = \frac{1}{n}\sum (b-y_i)^2$$

</details>

**4b.** `A` selalu bernilai positif. Buktikan, dan jelaskan apa artinya untuk
bentuk kurvanya.

**4c.** Cari titik minimumnya secara analitik. Turunkan $Aw^2 + Bw + C$ terhadap
`w`, samakan dengan nol, dan selesaikan untuk `w`.

<details>
<summary>Petunjuk 4c</summary>

$$\frac{d}{dw}(Aw^2 + Bw + C) = 2Aw + B = 0 \implies w^* = -\frac{B}{2A}$$

Substitusikan `A` dan `B` dari Petunjuk 3. Kamu baru saja menurunkan solusi
kuadrat terkecil dalam bentuk tertutup, hal yang sama yang dilakukan
`np.polyfit` dan `sklearn.LinearRegression`.
</details>

**4d.** Kalau solusi tertutupnya sudah ada, kenapa kita repot-repot memakai
gradient descent di Hari 7?

<details>
<summary>Petunjuk 4d</summary>

Solusi tertutup ada karena modelnya **linear terhadap parameternya**.

Coba tulis bentuk tertutup untuk jaringan saraf berlapis tiga dengan fungsi
aktivasi tak linear. Bisa?
</details>

---

## Soal 5 — Jembatan ke Mekanika

**5a.** Bandingkan dua ungkapan ini:

$$V(x) = \tfrac{1}{2} k x^2 \qquad\qquad \text{MSE}(w) \approx A(w - w^*)^2 + C_{\min}$$

Apa padanan `k` di sisi kanan? Apa padanan simpangan `x`?

**5b.** Pada pegas, `k` yang besar berarti apa secara fisis? Pada permukaan
loss, `A` yang besar berarti apa soal bentuk mangkuknya?

**5c.** Di Hari 7 kamu akan menuruni permukaan ini selangkah demi selangkah,
dengan panjang langkah `lr`. Berdasarkan analogi pegas, **ramalkan** apa yang
terjadi kalau `lr` terlalu besar. Tulis ramalanmu sekarang, dan kita cocokkan
di Hari 8.

<details>
<summary>Petunjuk 5c</summary>

Bayangkan massa pada pegas tanpa redaman, tapi posisinya kamu perbarui dalam
lompatan diskret alih-alih kontinu.

Kalau tiap lompatan melampaui titik setimbang lebih jauh dari posisi awalnya,
apa yang terjadi pada amplitudo setelah banyak lompatan?
</details>

---

## Tolok Ukur Hari 3

- [ ] Urutan enam tebakan di Soal 1 benar sebelum dijalankan
- [ ] `prediksi`, `mse`, dan `mae` lolos uji
- [ ] Lima pertanyaan Soal 3 terjawab, termasuk sapuan `n` di 3e
- [ ] Bentuk kuadratik di Soal 4 terbukti di kertas, lengkap dengan `A`, `B`, `C`
- [ ] `w*` analitik diturunkan, dan angkanya cocok dengan `w_min` dari program
- [ ] Ramalan Soal 5c sudah kamu tulis sebelum Hari 8
- [ ] Kamu bisa menjelaskan kenapa loss di parameter asli tidak nol

Kalau tujuh-tujuhnya tercentang, Hari 3 selesai.
