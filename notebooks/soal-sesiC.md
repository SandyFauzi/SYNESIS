# Soal Sesi C - Multivariat, overfitting, regularisasi

Berkas latihan: [`sesiC_multivariat.py`](sesiC_multivariat.py)

Sesi B memberimu gambar untuk dua parameter. Sesi ini melepas batas jumlah parameter, lalu memakai kebebasan itu untuk membuat model gagal dengan cara yang paling terkenal di seluruh machine learning.

Aturan mainnya sama. Kerjakan sendiri dulu, dan tulis ramalan sebelum menjalankan.

---

## Soal 0 - Empat catatan dari Sesi B

Sesi B kamu kuat. Bukti 0a rapi, faktor pengali galat di 4a benar ketiganya, dan cerita animasi di 6a bersih dari istilah. Empat hal perlu diluruskan, dan yang pertama bukan soal ketelitian.

### 0a. Jawaban 4c bertentangan dengan tabel di atasnya

Kamu menulis lintasan merah "paling lama nyampe dasar". Lihat lagi kolom loss akhir di Bagian 3, plus pengukuran tambahan berikut:

| lr | loss di iterasi 60 | panjang lintasan | iterasi sampai 1% dari dasar |
|---|---|---|---|
| 0.01 | 3.168473 | 5.74 | **185** |
| 0.06 | 1.290335 | 7.59 | **30** |
| 0.12 | 1.290407 | 63.41 | **38** |

Dasar loss-nya `1.290328`.

Yang merah sampai di dasar dalam 38 iterasi. Yang biru butuh 185. Jadi yang menggergaji itu justru hampir lima kali lebih cepat dari yang merayap lurus, bukan paling lambat.

**Tulis ulang jawaban 4c.** Pertanyaannya: kenapa lintasan yang menempuh jarak delapan kali lebih jauh bisa sampai lebih cepat?

<details>
<summary>Petunjuk 0a</summary>

Panjang lintasan dan jumlah iterasi mengukur dua ongkos yang berbeda.

Gradient descent tidak membayar per satuan jarak. Ia membayar per langkah. Satu langkah dengan `lr` besar dan satu langkah dengan `lr` kecil harganya sama, yaitu satu kali hitung gradien.

Jadi jarak yang terbuang untuk menggergaji itu gratis. Yang mahal cuma banyaknya langkah.

Sekarang pertanyaan lanjutan yang lebih menarik: kalau begitu, kenapa orang repot-repot menghindari gergaji?
</details>

<details>
<summary>Petunjuk 0a, lanjutan</summary>

Lihat arah landai, bukan arah curam. Faktor pengalinya:

- `lr = 0.01` memberi `1 - 1.96(0.01) = 0.980`
- `lr = 0.06` memberi `1 - 1.96(0.06) = 0.882`
- `lr = 0.12` memberi `1 - 1.96(0.12) = 0.764`

Arah landai itu yang menentukan kapan selesai, dan ia selalu lebih cepat kalau `lr` lebih besar.

Jadi gergaji bukan penyebab lambat. Gergaji adalah **harga yang kamu bayar** supaya boleh memakai `lr` besar. Dan ada batasnya: melewati `0.1272`, harga itu berubah jadi kehancuran.
</details>

Pelajaran yang lebih penting dari isi jawabannya: kamu menulis kesimpulan yang dibantah oleh tabel yang kamu cetak sendiri tiga baris di atasnya. Cerita terasa masuk akal, jadi angkanya tidak diperiksa ulang. Ini cara paling umum orang membohongi diri sendiri dengan data.

### 0b. Parabola naik secara kuadratik, bukan eksponensial

Di 2a kamu menulis dinding mangkuk "naiknya eksponensial". Alasan log membantu itu benar, tapi kata itu salah, dan kamu mahasiswa fisika.

$w^2$ dan $e^w$ berperilaku sangat berbeda. Kalau dinding loss betulan eksponensial, gradient descent tidak akan pernah bekerja.

### 0c. Hessian bergantung pada `y` bukan karena ReLU patah

Di 3c kamu menulis Hessian ikut bergantung pada `y` di jaringan saraf karena ReLU membuat dindingnya tidak mulus. Kesimpulannya benar, mekanismenya bukan itu. Model tanpa ReLU tapi tetap taklinear juga punya Hessian yang bergantung pada `y`.

Sebab sebenarnya bisa ditulis persis. Untuk model $f(\theta)$ apa pun:

$$\nabla^2 L = \frac{2}{n}\sum_i \left[ \nabla f_i \nabla f_i^{\top} + (f_i - y_i)\,\nabla^2 f_i \right]$$

**0c-i.** Tunjukkan suku mana yang memuat `y`, dan jelaskan kenapa suku itu lenyap untuk model linear.

<details>
<summary>Petunjuk 0c</summary>

$f_i - y_i$ adalah residu, dan di situlah `y` bersembunyi.

Untuk model linear, $f_i = x_i^{\top}\theta$. Berapa $\nabla^2 f_i$, yaitu turunan kedua ramalan terhadap parameter?

Kalau nol, seluruh suku kedua lenyap berapa pun residunya. Yang tersisa cuma $\nabla f_i \nabla f_i^{\top}$, dan itu tidak memuat `y` sama sekali.

Suku pertama sendirian namanya hampiran Gauss-Newton, dan kamu akan bertemu lagi dengannya.
</details>

**0c-ii.** Dari rumus itu, kapan hampiran Gauss-Newton bagus meski modelnya taklinear?

### 0d. Jawaban 5e kurang satu angka

Kamu benar bahwa membakukan `x` menghapus elemen luar diagonal dan menurunkan bilangan kondisi. Tapi kamu berhenti di "turun", padahal jawabannya jauh lebih tajam.

**Hitung bilangan kondisinya setelah `x` dibakukan.** Kerjakan di kertas, bukan dengan menjalankan kode.

<details>
<summary>Petunjuk 0d</summary>

Setelah dibakukan, $\bar{x} = 0$ dan $\text{var}(x) = 1$, jadi $A = \frac{1}{n}\sum x^2 = \text{var} + \bar{x}^2 = 1$.

Susun Hessian-nya sekarang. Seperti apa bentuknya?
</details>

**0d-ii.** Lalu hubungkan dengan jawabanmu sendiri di Soal 2c Sesi B. Kamu sudah menulis apa yang terjadi kalau kedua nilai eigen sama. Kamu tidak menyadari bahwa 5e menghasilkan tepat kasus itu.

Bagian 3 sesi ini mencetak bilangan kondisi derajat 1 setelah dibakukan. Lihat angkanya.

---

## Soal 1 - Semuanya jadi matriks

### 1a. Tulis `desain_polinom(x, derajat)`

Baris ke-`i` berisi `[1, x_i, x_i^2, ..., x_i^derajat]`, bentuk `(n, derajat+1)`.

**1b.** Kolom pertama berisi angka satu semua. Jelaskan apa yang dikerjakan kolom itu, dan kenapa setelah ada kolom itu kamu tidak butuh `b` sebagai kasus khusus lagi.

### 1c. Tulis `mse_matriks` dan `gradien_matriks`

Turunkan bentuk matriksnya sendiri di kertas, berangkat dari bentuk skalar Sesi A. Jangan disalin dari docstring.

$$\frac{\partial L}{\partial \theta} = \frac{2}{n} X^{\top}(X\theta - y) + 2\lambda\theta$$

<details>
<summary>Petunjuk 1c</summary>

Di Sesi A, $\partial L/\partial w = \frac{2}{n}\sum_i r_i x_i$. Itu hasil kali dalam antara vektor residu dan kolom `x`.

Di Sesi A, $\partial L/\partial b = \frac{2}{n}\sum_i r_i$. Itu hasil kali dalam antara residu dan kolom satuan.

Dua-duanya adalah "hasil kali dalam residu dengan satu kolom X". Kalau kamu mau semua kolom sekaligus, kamu butuh $X^{\top} r$.

Itu saja isinya. Tidak ada aturan baru, cuma cara mengorganisasi yang berbeda.
</details>

**1d.** Kolom 0 tidak boleh didenda L2. Jelaskan apa yang terjadi kalau kamu mendendanya, dan kenapa itu tidak diinginkan.

<details>
<summary>Petunjuk 1d</summary>

Denda L2 menarik parameter ke arah nol. Kalau geseran ikut ditarik ke nol, model dipaksa lewat dekat titik asal.

Bayangkan kamu memprediksi suhu dalam Kelvin. Nilai wajarnya sekitar 300. Memaksa geserannya mendekati nol berarti memaksa model meramalkan angka mendekati nol Kelvin.

Sekarang ubah satuannya jadi Celsius. Apakah dendanya masih berarti hal yang sama?
</details>

### 1e. Tulis `latih_matriks`

Isinya sama persis dengan `latih` Sesi A, cuma `theta` jadi vektor.

---

## Soal 2 - Tiga saksi

Bagian 2 membandingkan gradien dari tiga sumber: bentuk matriks, rumus skalar Sesi A, dan beda hingga.

**2a.** Kenapa kesepakatan tiga arah lebih meyakinkan daripada dua arah? Jawab dengan memikirkan cara ketiganya bisa salah bersamaan.

**2b.** Di antara ketiga saksi itu, mana yang paling independen dari dua lainnya, dan kenapa itu penting?

**2c.** Kalau bentuk matriks dan bentuk skalar sepakat, tapi beda hingga tidak, apa yang paling mungkin terjadi?

<details>
<summary>Petunjuk 2c</summary>

Bentuk matriks dan bentuk skalar sama-sama berangkat dari turunan yang kamu kerjakan di kertas.

Kalau turunan di kertasnya salah, keduanya akan salah dengan cara yang sama persis, dan mereka akan sepakat dengan gembira.

Beda hingga tidak pernah melihat turunanmu. Ia cuma menghitung loss dua kali.
</details>

---

## Soal 3 - Bilangan kondisi meledak

**3a.** Sebelum menjalankan, ramalkan: bilangan kondisi $X^{\top}X$ untuk derajat 14 dengan `x` di rentang `[-3, 3]`, kira-kira orde berapa?

<details>
<summary>Petunjuk 3a</summary>

Kolom terakhir berisi $x^{14}$. Untuk $x = 3$ nilainya sekitar $4.8 \times 10^6$, untuk $x = 0.5$ nilainya sekitar $6 \times 10^{-5}$.

Sekarang bandingkan dengan kolom pertama yang isinya angka satu semua. Berapa rasio skala antar kolom, dan apa yang terjadi kalau rasio itu dikuadratkan oleh $X^{\top}X$?
</details>

**3b.** Kolom `lambda_min mentah` di derajat 14 memberi angka **negatif**.

Matriks $X^{\top}X$ selalu semidefinit positif, jadi nilai eigen terkecilnya tidak mungkin negatif. Itu teorema.

Buktikan teoremanya dalam dua baris, lalu jelaskan apa arti angka negatif itu sebenarnya.

<details>
<summary>Petunjuk 3b</summary>

Untuk vektor `v` apa pun, hitung $v^{\top}(X^{\top}X)v$. Kelompokkan ulang jadi $(Xv)^{\top}(Xv)$.

Itu norma kuadrat sebuah vektor. Bisakah ia negatif?
</details>

**3c.** Ini jenis pemeriksaan yang murah dan sangat berguna. Sebutkan dua besaran lain di proyek ini yang punya sifat sama: nilainya tidak mungkin melanggar batas tertentu, jadi kalau melanggar berarti kodemu rusak.

**3d.** Bagian 3 mengukur iterasi yang dibutuhkan derajat 3, mentah lawan dibakukan: `242` lawan `27`. Bilangan kondisinya `3.1e2` lawan `2.4e1`.

Cocokkan kedua rasio itu. Apa hubungan kasar antara bilangan kondisi dan jumlah iterasi?

**3e.** Berdasarkan hubungan itu, perkirakan berapa iterasi yang dibutuhkan gradient descent untuk derajat 14 mentah. Lalu jelaskan kenapa Bagian 5 dan 6 memakai solusi tertutup, bukan gradient descent.

---

## Soal 4 - Melihat model menghafal

Buka `figures/sesiC_derajat.png`.

**4a.** Derajat 14 memberi train loss **nol persis** dengan 15 titik data. Jelaskan kenapa angka 15 dan 14 itu bukan kebetulan.

<details>
<summary>Petunjuk 4a</summary>

Polinomial derajat 14 punya 15 koefisien. Kamu punya 15 titik.

Berapa banyak persamaan, berapa banyak yang tidak diketahui? Kamu sudah mengenal situasi ini dari aljabar linear.
</details>

**4b.** Kalau kamu tambah satu titik data lagi jadi 16, apa yang terjadi pada train loss derajat 14? Ramalkan dulu, lalu uji dengan mengubah `buat_data(15, seed=7)` jadi `buat_data(16, seed=7)`.

**4c.** Panel derajat 9 sudah liar di tepi, padahal di tengah masih wajar. Kenapa kerusakannya mulai dari tepi?

<details>
<summary>Petunjuk 4c</summary>

Lihat sebaran titik hitamnya. Di mana jarak antar titik paling renggang?

Lalu pikirkan apa yang membatasi kurva di antara dua titik yang berdekatan, dibanding di luar titik terakhir.
</details>

**4d.** Perhatikan bahwa test loss derajat 3 adalah `4.26`, sementara lantai deraunya `2.25`. Kenapa model yang derajatnya persis benar pun tidak mencapai lantai?

---

## Soal 5 - Kurva yang berpisah

Buka `figures/sesiC_train_test.png`.

**5a.** Buktikan pernyataan ini: train loss tidak akan pernah naik saat derajat ditambah, untuk metode kuadrat terkecil.

<details>
<summary>Petunjuk 5a</summary>

Model derajat `d+1` bisa meniru model derajat `d` mana pun. Caranya cukup dengan menyetel koefisien tertinggi jadi nol.

Jadi himpunan fungsi yang bisa dicapai derajat `d` adalah himpunan bagian dari yang bisa dicapai derajat `d+1`.

Mencari minimum pada himpunan yang lebih besar tidak mungkin memberi hasil yang lebih buruk.
</details>

**5b.** Test loss terbaik jatuh di derajat 3, dan derajat sebenarnya juga 3. Apakah ini akan selalu terjadi? Uji dengan mengganti seed data latih ke beberapa nilai lain dan catat di derajat mana test terbaik jatuh.

**5c.** Perhatikan lompatan test loss dari derajat 8 ke derajat 9, yaitu dari `6.35` ke `923.58`. Kenapa lompatannya sedrastis itu, bukan naik perlahan?

**5d.** Kamu punya data baru dan tidak tahu derajat sebenarnya. Kamu juga tidak punya data uji, karena semua data yang kamu punya sudah dipakai untuk melatih. Bagaimana cara memilih derajat?

<details>
<summary>Petunjuk 5d</summary>

Jawaban "sisihkan sebagian data" benar, tapi mahal kalau datamu sedikit. Sisihkan 20 persen dari 15 titik, tinggal 12 untuk melatih.

Ada cara yang memakai setiap titik untuk melatih **dan** untuk menguji, cuma tidak pada saat yang sama. Namanya cross validation, dan idenya: ulangi pembagiannya beberapa kali dengan potongan yang berbeda, lalu rata-ratakan.

Kamu tidak perlu mengodekannya sekarang. Cukup jelaskan cara kerjanya dengan kalimatmu sendiri.
</details>

**5e.** Kenapa melihat kurva train saja tidak akan pernah bisa memberi tahu kamu bahwa model sedang overfit?

---

## Soal 6 - Satu suku yang menyembuhkan

Buka `figures/sesiC_regularisasi.png`.

**6a.** Kolom `|theta|` turun dari jutaan jadi sekitar `1.7`. Jelaskan mekanismenya lewat gradien denda, bukan lewat kalimat "L2 mengecilkan bobot".

<details>
<summary>Petunjuk 6a</summary>

Gradien dari suku $\lambda|\theta|^2$ adalah $2\lambda\theta$.

Itu vektor yang selalu menunjuk menjauhi nol, dan besarnya sebanding dengan jarak dari nol. Pembaruan parameter menguranginya, jadi arah pengaruhnya menuju nol.

Sekarang tulis besarnya sebagai gaya: $F = -k\theta$. Apa nama hukum ini, dan apa padanan $k$?
</details>

**6b.** Derajat 14 tanpa denda memberi test loss di atas 8 miliar. Derajat 14 yang sama dengan `lambda = 0.1` memberi `5.42`. Derajat 3 memberi `4.26`.

Jadi model dengan 15 parameter dan satu suku denda hampir menyamai model dengan 4 parameter yang derajatnya persis benar. Apa yang sebenarnya dikerjakan denda itu terhadap **jumlah parameter efektif**?

<details>
<summary>Petunjuk 6b</summary>

Parameter yang nilainya ditekan mendekati nol hampir tidak menyumbang apa pun pada ramalan.

Jadi meski ada 15 parameter yang secara resmi bisa diputar, berapa banyak yang benar-benar bekerja?

Denda tidak menghapus parameter. Ia membuat memakainya jadi mahal, sehingga model cuma memakai yang benar-benar berguna. Ada besaran yang mengukur ini secara tepat, namanya derajat kebebasan efektif.
</details>

**6c.** Kolom `lambda` punya bentuk U yang sama dengan kolom derajat di Bagian 5. Jelaskan kenapa dua kenop yang sangat berbeda menghasilkan bentuk yang sama.

**6d.** Terjemahkan seluruh Bagian 6 ke bahasa fisika. Apa energi potensialnya, apa gaya pemulihnya, apa tetapan pegasnya, dan apa arti keadaan setimbangnya?

**6e.** Bagian 6 membakukan fitur data uji memakai `m` dan `s` dari data **latih**, bukan dari data uji sendiri. Jelaskan kenapa memakai statistik data uji itu salah, meski hasilnya terlihat lebih bagus.

<details>
<summary>Petunjuk 6e</summary>

Data uji berperan sebagai pengganti data masa depan yang belum ada.

Kalau kamu menghitung rata-rata dan simpangan baku dari data uji, model sudah menyerap informasi tentang data itu sebelum diuji.

Namanya kebocoran data. Ia jarang melempar error, hasilnya selalu terlihat lebih bagus, dan ia baru ketahuan setelah sistemmu dipakai di dunia nyata dan gagal. Ini akan jadi salah satu bahaya utama di Modul 2 sampai 4.
</details>

---

## Tolok Ukur Sesi C

- [ ] Jawaban 4c Sesi B ditulis ulang, dan perbedaan ongkos per langkah lawan per jarak jelas
- [ ] Bilangan kondisi setelah pembakuan dihitung di kertas, dan sambungannya ke Soal 2c Sesi B disadari
- [ ] Bentuk matriks gradien diturunkan sendiri dari bentuk skalar Sesi A
- [ ] Kolom 0 tidak didenda, dan kamu bisa menjelaskan kenapa
- [ ] Ketiga saksi di Bagian 2 sepakat di bawah `1e-12`
- [ ] Semidefinit positif dibuktikan dalam dua baris, dan arti nilai eigen negatif kamu pahami
- [ ] Hubungan bilangan kondisi dengan jumlah iterasi dicocokkan dengan angka terukur
- [ ] Train loss nol di derajat 14 dijelaskan lewat jumlah persamaan lawan jumlah yang tak diketahui
- [ ] Grafik train turun sementara test naik dihasilkan dan kamu bisa membacanya
- [ ] L2 menurunkan test loss derajat 14 dari miliaran jadi satu digit, dan mekanismenya kamu jelaskan lewat gaya pemulih
- [ ] Kebocoran data lewat pembakuan dipahami sebagai bahaya, bukan detail teknis

Kalau kesebelas kotak beres, Bulan 0 tinggal satu sesi.

Satu catatan penutup. Dua sesi terakhir kamu menulis kesimpulan yang dibantah oleh angka yang kamu cetak sendiri: nilai populasi di Sesi A, dan arah kesimpulan di 4c Sesi B. Dua-duanya terjadi karena ceritanya terdengar masuk akal, jadi tabelnya tidak dibaca ulang.

Itu bukan kelemahan kecil. Itu justru cara paling umum orang pintar tersesat, karena orang yang tidak bisa menyusun cerita yang masuk akal tidak pernah kena masalah ini. Kebiasaan yang menolongmu cuma satu: setelah menulis kesimpulan, kembali ke angkanya dan cari baris yang membantahnya.
