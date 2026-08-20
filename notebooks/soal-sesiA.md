# Soal Sesi A - Gradient descent utuh

Berkas latihan: [`sesiA_gradient_descent.py`](sesiA_gradient_descent.py)

Hari 3 kamu membangun permukaannya dan membuktikan bentuknya parabola. Hari ini kelerengnya menggelinding, dan kamu yang menulis mesin penggeraknya.

Aturan mainnya masih sama. Kerjakan sendiri minimal 15 menit sebelum membuka petunjuk. Dan aturan tambahan khusus sesi ini: **tulis ramalanmu sebelum menjalankan kode.** Beberapa soal di bawah cuma berguna kalau kamu meramal dulu.

---

## Soal 1 - Tanda gradien sebelum menghitung

Data aslinya `w = 3`, `b = 2`. Sekarang lihat empat tebakan berikut, dan **tentukan tanda** `dMSE/dw` dan `dMSE/db` tanpa menghitung apa pun.

| Tebakan | w | b | tanda dL/dw | tanda dL/db |
|---|---|---|---|---|
| A | 0.0 | 0.0 | | |
| B | 5.0 | -1.0 | | |
| C | 3.0 | 2.0 | | |
| D | 2.9 | 2.1 | | |

Lalu jawab: kalau tandanya negatif, ke arah mana `w` akan bergerak di iterasi berikutnya? Naik atau turun?

<details>
<summary>Petunjuk 1</summary>

Gradien menjawab pertanyaan "kalau kenop ini saya naikkan sedikit, loss-nya jadi naik atau turun?"

Tebakan A punya `w = 0`, artinya garisnya datar sementara data aslinya menanjak. Kalau `w` kamu naikkan sedikit dari 0, garisnya jadi lebih pas atau makin meleset?
</details>

<details>
<summary>Petunjuk 2</summary>

Aturan pembaruannya `w = w - lr * dL_dw`. Ada tanda minus di sana.

Jadi gradien negatif menghasilkan `w - (negatif)`, dan mengurangi bilangan negatif berarti menambah. Gradien negatif membuat `w` naik.

Itu memang yang kamu mau: kalau menaikkan `w` menurunkan loss, ya naikkan.
</details>

<details>
<summary>Petunjuk 3, soal tebakan C</summary>

Tebakan C ada di parameter asli. Godaannya menjawab "gradiennya nol karena ini titik yang benar".

Hati-hati. Titik terendah permukaan loss belum tentu ada di parameter asli. Datanya berderau. Tahan jawabanmu sampai Soal 4, dan tulis dulu apa dugaanmu sekarang supaya bisa kamu bandingkan nanti.
</details>

**Lanjut jika:** Tandamu untuk A, B, dan D cocok dengan hasil `bagian3` saat dijalankan.

---

## Soal 2 - Dua fungsi

### 2a. Tulis `gradien(x, y, w, b)`

Dari turunan yang kamu kerjakan di kertas:

$$\frac{\partial \text{MSE}}{\partial w} = \frac{2}{n}\sum_i r_i x_i \qquad\qquad \frac{\partial \text{MSE}}{\partial b} = \frac{2}{n}\sum_i r_i \qquad\qquad r_i = w x_i + b - y_i$$

Kembalikan tuple dua angka. Boleh pakai `prediksi()` dan operasi vektor numpy. Dilarang pakai autograd apa pun, karena itu justru barang yang sedang kita bongkar.

### 2b. Tulis `beda_hingga(x, y, w, b, h)`

Beda pusat:

$$\frac{\partial L}{\partial w} \approx \frac{L(w+h, b) - L(w-h, b)}{2h}$$

Saat menggoyang `w`, `b` dibiarkan diam. Begitu juga sebaliknya. Itu arti kata "parsial".

<details>
<summary>Petunjuk 2b</summary>

`L(w+h, b)` dalam kode berarti `mse(prediksi(x, w + h, b), y)`.

Jangan pakai beda maju `(f(w+h) - f(w))/h`. Galat pemotongannya $O(h)$, sementara beda pusat $O(h^2)$. Kamu sudah membuktikan ini di Komputasi Numerik.
</details>

<details>
<summary>Kalau gradient check kamu GAGAL</summary>

Urutan curiga, dari yang paling sering ke yang paling jarang:

1. **Faktor 2 hilang.** Turunan $r^2$ adalah $2r$, bukan $r$. Kalau rasio analitik terhadap numerik tepat 0.5 atau 2.0, ini penyebabnya.
2. **`x_i` tertukar.** Terpasang di `db` padahal harusnya di `dw`, atau hilang sama sekali.
3. **Residu terbalik.** `y - ramal` bukan `ramal - y`. Kalau tandanya berlawanan tapi besarnya pas, ini penyebabnya.
4. **Pembagian `n` kelupaan.** Kalau rasionya persis 50, ini penyebabnya.

Rasio antara gradien analitik dan numerik hampir selalu menunjuk langsung ke bugnya. Biasakan melihat rasionya, bukan cuma selisihnya.
</details>

**Lanjut jika:** Kelima titik di Bagian 3 lolos dengan selisih relatif di bawah `1e-6`.

---

## Soal 3 - Kenapa galatnya jauh lebih kecil dari target

Gradient check kamu targetnya `1e-6`. Angka yang keluar kemungkinan sekitar `1e-11` atau `1e-12`, jauh lebih bagus dari yang diminta.

**3a.** Jalankan `beda_hingga` di titik `w = 0, b = 0` dengan `h` bernilai `1e-1`, `1e-3`, `1e-5`, `1e-7`, `1e-9`, dan `1e-11`. Catat galat relatifnya untuk tiap `h`.

Sebelum menjalankan, **tulis ramalanmu**: `h` mana yang akan memberi hasil paling akurat?

**3b.** Hasilnya kemungkinan besar bertentangan dengan ramalanmu. Jelaskan kenapa.

<details>
<summary>Petunjuk 3b, langkah 1</summary>

Buku teks bilang ada dua galat yang bertarung. Galat pemotongan mengecil saat `h` mengecil. Galat pembulatan membesar saat `h` mengecil, karena `f(w+h)` dan `f(w-h)` jadi hampir sama dan pengurangannya kehilangan angka penting.

Itu sebabnya orang biasa memilih `h` di sekitar `1e-5` sebagai kompromi.

Sekarang lihat datamu. Apakah kompromi itu terlihat? Atau `h` besar justru menang telak?
</details>

<details>
<summary>Petunjuk 3b, langkah 2</summary>

Uraikan deret Taylor beda pusat:

$$\frac{f(w+h) - f(w-h)}{2h} = f'(w) + \frac{h^2}{6}f'''(w) + O(h^4)$$

Galat pemotongannya bergantung pada **turunan ketiga**.

Sekarang buka jawaban Soal 4a Hari 3 kamu. Kamu sudah membuktikan bahwa $\text{MSE}(w) = Aw^2 + Bw + C$. Berapa turunan ketiga dari polinomial derajat dua?
</details>

<details>
<summary>Petunjuk 3b, langkah 3</summary>

Buktikan langsung tanpa deret, dengan $f(w) = Aw^2 + Bw + C$:

$$f(w+h) - f(w-h) = A\left[(w+h)^2 - (w-h)^2\right] + B\left[(w+h)-(w-h)\right] = 4Awh + 2Bh$$

Bagi dengan $2h$, dan kamu dapat $2Aw + B$. Itu $f'(w)$ persis, tanpa sisa apa pun, untuk `h` sebesar apa pun.
</details>

**3c.** Kalau beda pusat memang persis untuk fungsi ini, kenapa `h` yang sangat kecil justru memberi galat lebih besar?

**3d.** Aturan "pakai `h = 1e-5`" itu contoh apa yang di [Modul.md](../Modul.md) Bagian 10 disebut pemujaan kargo, atau aturan yang memang beralasan? Jawab dengan hati-hati, karena jawabannya bukan salah satu dari dua-duanya.

<details>
<summary>Petunjuk 3d</summary>

Pertanyaannya bukan "apakah aturan itu benar", tapi "apakah aturan itu benar **di sini**, dan tahukah orang yang memakainya kenapa".

Di Bulan 1 modelmu punya ReLU dan berlapis-lapis. Apakah turunan ketiganya masih nol?
</details>

**Lanjut jika:** Kamu bisa menjelaskan kenapa `h = 0.1` mengalahkan `h = 1e-11` di sesi ini, dan kenapa itu tidak akan berlaku lagi di Bulan 1.

---

## Soal 4 - Kenapa `b` tidak mendarat di 2

Jalankan Bagian 4. Dari tiga titik awal yang sangat berbeda, ketiganya mendarat di tempat yang sama. Tapi tempat itu bukan `w = 3, b = 2`.

**4a.** `w` meleset sekitar 0,02 sementara `b` meleset sekitar 0,26. Apakah ini bug di kodemu, gradient descent yang belum konvergen, atau sesuatu yang lain? Pilih satu dan pertahankan alasanmu.

<details>
<summary>Petunjuk 4a</summary>

Naikkan `n_iter` jadi 50000 dan jalankan lagi. Kalau angkanya bergeser mendekati 3 dan 2, berarti belum konvergen. Kalau angkanya tidak bergerak sama sekali, berarti gradient descent sudah sampai di dasar, dan dasarnya memang di situ.

Lalu bandingkan dengan keluaran Bagian 6.
</details>

<details>
<summary>Petunjuk 4a, lanjutan</summary>

Kamu sudah menemui hal ini di Soal 3e Hari 3, dengan bungkus yang berbeda.

Gradient descent mencari titik terendah **permukaan loss**, dan permukaan loss dibangun dari 50 titik data yang sudah digeser acak. Ia tidak mencari parameter yang melahirkan data, karena ia tidak pernah diberi tahu parameter itu ada.

Yang ia temukan adalah jawaban terbaik untuk data yang ada di depannya. Itu jawaban yang berbeda, dan bedanya menyusut sebagai $1/\sqrt{n}$.
</details>

**4b.** Perkirakan simpangan baku dugaan `b` memakai $\sigma/\sqrt{n}$ dengan `derau = 1.5` dan `n = 50`. Apakah meleset 0,26 itu wajar atau mencurigakan?

**4c.** Kenapa `w` jauh lebih tepat daripada `b`? Kaitkan dengan sebaran `x`.

<details>
<summary>Petunjuk 4c</summary>

Simpangan baku dugaan kemiringan kira-kira $\sigma / \sqrt{n \cdot \text{var}(x)}$, sementara untuk geseran kira-kira $\sigma/\sqrt{n}$.

Ada faktor $\sqrt{\text{var}(x)}$ tambahan di penyebut yang pertama. Dengan `x` tersebar di rentang `[-5, 5]`, berapa nilainya?

Terjemahan fisisnya: mengukur kemiringan dari lengan yang panjang jauh lebih teliti daripada dari lengan pendek. Persis alasan kamu merentangkan rentang pengukuran selebar mungkin di praktikum.
</details>

**4d.** Di Bagian 6 ada dua baris yang menunjukkan garis hasil fit melewati titik $(\bar{x}, \bar{y})$. **Buktikan** ini di kertas, berangkat dari menyamakan `dMSE/db` dengan nol.

<details>
<summary>Petunjuk 4d</summary>

$\partial \text{MSE}/\partial b = 0$ berarti $\frac{2}{n}\sum r_i = 0$, jadi $\sum r_i = 0$.

Ganti $r_i$ dengan bentuk panjangnya, lalu bagi dengan $n$. Suku mana yang jadi $\bar{x}$ dan suku mana yang jadi $\bar{y}$?
</details>

**4e.** Ubah `derau` dari `1.5` jadi `0.0` di `buat_data`, lalu jalankan ulang Bagian 4. Ramalkan dulu apa yang akan kamu lihat.

---

## Soal 5 - Ramalkan batas learning rate

Ini soal utama sesi ini, dan bagian yang paling saya ingin kamu kerjakan dengan serius.

Di Soal 5c Hari 3 kamu sudah meramal secara kualitatif bahwa `lr` yang terlalu besar akan membuat sistem berosilasi lalu melenting keluar. Ramalanmu benar. Sekarang naikkan taruhannya: **ramalkan angkanya.**

**5a.** Untuk kasus satu parameter, anggap `b` dikunci dan $\text{MSE}(w) = Aw^2 + Bw + C$. Tulis aturan pembaruan gradient descent, lalu nyatakan dalam bentuk galat $e = w - w^*$. Tunjukkan bahwa tiap iterasi mengalikan galat dengan sebuah faktor tetap, lalu cari syarat agar galatnya mengecil.

<details>
<summary>Petunjuk 5a, langkah 1</summary>

$\frac{dL}{dw} = 2Aw + B$, dan $w^* = -B/2A$ dari Soal 4c Hari 3.

Jadi $\frac{dL}{dw} = 2A\left(w - w^*\right) = 2Ae$.
</details>

<details>
<summary>Petunjuk 5a, langkah 2</summary>

Pembaruannya $w_{\text{baru}} = w - \eta \cdot 2Ae$. Kurangi $w^*$ dari kedua ruas:

$$e_{\text{baru}} = e - 2A\eta e = (1 - 2A\eta)\,e$$

Galat dikalikan $(1 - 2A\eta)$ tiap iterasi. Supaya mengecil, nilai mutlak faktor itu harus di bawah satu.
</details>

<details>
<summary>Petunjuk 5a, langkah 3</summary>

$|1 - 2A\eta| < 1$ memberi $0 < \eta < 1/A$.

Perhatikan tiga wilayahnya. Di $\eta < 1/(2A)$ faktornya positif, galat mengecil tanpa berganti tanda, jadi kelerengnya merayap turun dari satu sisi. Di antara $1/(2A)$ dan $1/A$ faktornya negatif, galat berganti tanda tiap iterasi, jadi kelerengnya melompati dasar bolak-balik sambil tetap mengecil. Di atas $1/A$ nilai mutlaknya melebihi satu dan amplitudonya membesar tiap siklus.

Tiga wilayah itu adalah teredam berlebih, teredam kurang, dan tak stabil. Kamu sudah mengenal ketiganya dari Mekanika.
</details>

**5b.** Hitung `A` untuk datasetmu, lalu hitung `lr` kritisnya. Tulis angkanya **sebelum** melihat tabel Bagian 5.

<details>
<summary>Petunjuk 5b</summary>

`A = np.sum(x*x) / len(x)`. Satu baris.
</details>

**5c.** Bandingkan ramalanmu dengan tabel Bagian 5. Di antara dua nilai `lr` mana batasnya jatuh?

**5d.** Ramalan satu parameter tadi mengabaikan `b`. Susun matriks Hessian penuh untuk kedua parameter, cari nilai eigen terbesarnya, lalu hitung batas yang lebih tepat sebagai $2/\lambda_{\max}$.

<details>
<summary>Petunjuk 5d</summary>

$$H = \begin{pmatrix} \partial^2 L/\partial w^2 & \partial^2 L/\partial w \partial b \\ \partial^2 L/\partial b \partial w & \partial^2 L/\partial b^2 \end{pmatrix} = \begin{pmatrix} 2A & 2\bar{x} \\ 2\bar{x} & 2 \end{pmatrix}$$

Pakai `np.linalg.eigvalsh`. Lalu hitung juga bilangan kondisinya, yaitu $\lambda_{\max}/\lambda_{\min}$.
</details>

**5e.** Bilangan kondisi yang kamu dapat sekitar 8. Artinya permukaannya bukan mangkuk bundar, melainkan lembah lonjong. Jelaskan kenapa itu memperlambat konvergensi, dan kenapa satu nilai `lr` tunggal tidak bisa optimal untuk kedua parameter sekaligus.

<details>
<summary>Petunjuk 5e</summary>

`lr` dibatasi dari atas oleh arah yang **paling curam**, karena arah itu yang meledak duluan. Tapi arah yang **paling landai** butuh langkah besar supaya tidak merayap selamanya.

Satu angka harus melayani dua kebutuhan yang bertentangan, dan ia akan mengecewakan keduanya. Ini alasan keberadaan Adam dan RMSprop, yang memberi tiap parameter langkahnya sendiri. Kamu akan menulisnya di Bulan 1.
</details>

**5f.** Terjemahkan ke bahasa fisika. Di Soal 5a Hari 3 kamu sudah memetakan $k \leftrightarrow 2A$. Tulis syarat kestabilan $\eta < 2/\lambda_{\max}$ dalam bentuk `k`, lalu jelaskan artinya untuk pegas yang kaku dibanding pegas yang lembek.

---

## Soal 6 - Yang berubah di Bulan 1

**6a.** Tiga titik awal di Bagian 4 mendarat di tempat yang sama. Kenapa sifat ini hilang begitu kamu masuk ke jaringan berlapis?

**6b.** Di Bulan 1 kamu menulis mesin autograd sendiri. Kenapa gradient check jadi satu-satunya cara memverifikasinya? Kenapa tidak bisa dibandingkan dengan PyTorch saja?

<details>
<summary>Petunjuk 6b</summary>

Boleh saja dibandingkan dengan PyTorch, dan nanti memang akan dibandingkan. Tapi pikirkan urutannya.

Kalau hasilmu beda dari PyTorch, kamu tahu salah satu salah, tapi kamu belum tahu yang mana. Beda hingga tidak bergantung pada pustaka mana pun. Ia cuma butuh fungsi loss-mu dan aritmetika. Ia wasit yang berdiri di luar kedua pihak.
</details>

**6c.** Fungsi `latih` kamu punya empat baris inti. Tulis keempatnya dari ingatan, tanpa membuka kode, dan jelaskan apa yang terjadi kalau urutan baris ketiga dan keempat ditukar.

---

## Tolok Ukur Sesi A

- [ ] Turunan `dMSE/dw` dan `dMSE/db` diturunkan di kertas, bukan disalin
- [ ] Tanda gradien di Soal 1 diramal benar sebelum dijalankan
- [ ] Kelima titik gradient check lolos di bawah `1e-6`
- [ ] Sapuan `h` dijalankan, dan kamu bisa menjelaskan kenapa `h` besar menang di sini
- [ ] Kamu bisa menjelaskan kenapa `b` mendarat di 1,74 dan bukan 2, tanpa menyebutnya bug
- [ ] Garis lewat titik pusat massa dibuktikan di kertas dari `dMSE/db = 0`
- [ ] `lr` kritis diramal dari `A` **sebelum** melihat tabel, dan cocok dengan hasil
- [ ] Nilai eigen Hessian dihitung, dan bilangan kondisinya kamu tafsirkan
- [ ] Training konvergen ke titik yang sama dari tiga titik awal yang jauh berbeda
- [ ] Hasil gradient descent cocok dengan `lstsq` sampai enam angka di belakang koma

Kalau kesepuluh kotak beres, Sesi A selesai dan kamu siap masuk Sesi B.

Satu catatan penutup. Soal 5 adalah pertama kalinya kamu meramalkan angka dari teori lalu mengukurnya, dan itu keterampilan yang membedakan orang yang membangun sistem dari orang yang mengutak-atik sampai kebetulan jalan. Kalau ramalanmu meleset, jangan buru-buru menyalahkan teorinya. Cek dulu apakah kamu mengukur hal yang sama dengan yang kamu ramalkan.
