# Soal Hari 3 — Data dan Loss

Berkas latihan: [`hari03_data_loss.py`](hari03_data_loss.py)

Hari ini kamu bakal ngebangun **lanskap permukaan (surface)** yang bakal ditelusuri algoritmanya nanti di Hari 7. Jadi kita belum masuk ke *gradient descent* ya, baru ngegambar petanya doang.

Aturan mainnya masih sama: usahakan kerjain sendiri minimal 15 menit sebelum buka contekan/petunjuk.

---

## Soal 1 — Urutkan sebelum menghitung

Di Bagian 3, ada enam tebakan parameter `w` dan `b`. **Urutkan dari loss yang paling kecil sampai paling gede tanpa nge-run kodenya.** Pakai logika, jangan asal tebak.

| Tebakan | w | b | Ranking (1 = terkecil) |
|---|---|---|---|
| A | 0.0 | 0.0 | 6 |
| B | 1.0 | 0.0 | 5 |
| C | 3.0 | 0.0 | 3 |
| D | 5.0 | 2.0 | 4 |
| E | 3.0 | 2.0 | 1 |
| F | 2.9 | 2.1 | 2 |

Sebagai pengingat, parameter aslinya itu `w = 3`, `b = 2`, dan nilai `x` tersebar di rentang `[-5, 5]`.

<details>
<summary>Petunjuk 1</summary>

Error/kesalahan di nilai `w` itu efeknya bakal dilipatgandakan oleh `x`. Kalau `w` meleset sebesar `Δw`, tebakanmu bakal meleset sejauh `Δw * x` (ingat, `x` bisa sampai angka 5).

Sebaliknya, error di `b` nggak dilipatgandakan. Kalau meleset `Δb`, ya tebakannya cuma geser sejauh `Δb` aja konstan di semua titik.

Nah, dari sini coba pikir: salah di `w` sebesar 1 vs salah di `b` sebesar 1, efeknya fatalan mana?
</details>

<details>
<summary>Petunjuk 2</summary>

Coba hitung kasar aja pake contoh titik ekstrem `x` di sekitar 2.5:

- Tebakan A: error `Δw = 3`, `Δb = 2` → meleset sekitar `3*(2.5) + 2 = 9.5`
- Tebakan C: error `Δw = 0`, `Δb = 2` → meleset sekitar `2`

Nah, coba kuadratkan nilainya lalu bandingin.
</details>

**Lanjut jika:** Urutan yang kamu bikin cocok sama hasil pas program di-run.

---

## Soal 2 — Tiga fungsi

### 2a. Bikin `prediksi(x, w, b)`

Fungsi ini buat ngitung tebakan model regresi linear biasa. Terima input array `x`, dan keluarin array tebakan.
Boleh banget pakai operasi vektor NumPy di sini (ingat pelajaran Hari 2, kita udah ninggalin loop biasa).

### 2b. Bikin `mse(y_ramal, y_asli)`

Ini rumus Mean Squared Error (MSE):
$$\text{MSE} = \frac{1}{n}\sum_i (\hat{y}_i - y_i)^2$$

**Dilarang pakai:** `np.mean`, `np.square`, atau library `sklearn`.
**Boleh pakai:** Operasi kurang/kali antar array, dan `np.sum` buat ngejumlahin total di akhir. Outputnya harus berupa **satu angka**.

### 2c. Bikin `mae(y_ramal, y_asli)`

Ini rumus Mean Absolute Error (MAE):
$$\text{MAE} = \frac{1}{n}\sum_i |\hat{y}_i - y_i|$$

Fungsi ini cuma buat bahan perbandingan di Soal 3 nanti.

<details>
<summary>Petunjuk 2b</summary>

Cukup tiga baris kode aja:
1. Kurangin array tebakan sama aslinya.
2. Kuadratkan selisihnya pakai perkalian biasa `array * array`.
3. Pakai `np.sum` terus dibagi sama total datanya (`len`).
</details>

<details>
<summary>Petunjuk 2c</summary>

Kalau di sini, kamu boleh pakai `np.abs` buat dapetin nilai mutlaknya.
</details>

**Target hasil tes:**
```python
y_ramal = np.array([1.0, 2.0, 3.0])
y_asli  = np.array([1.0, 2.0, 5.0])
mse(y_ramal, y_asli)   # -> harusnya 1.333... karena (0 + 0 + 4) / 3
mae(y_ramal, y_asli)   # -> harusnya 0.666... karena (0 + 0 + 2) / 3
```

---

## Soal 3 — Analisis

**3a.** Coba cek baris "parameter asli" (`w=3, b=2`). Ternyata nilai loss-nya **tidak nol**. Kok bisa? Angka sisa itu mewakili apa?
> **Jawaban:** Nilai loss tidak nol karena ada *noise* (derau) pada data, yaitu faktor `rng.normal(0, derau, n)`. Walaupun kita memakai tebakan `w` dan `b` yang paling sempurna sekalipun, garis lurus regresi tidak akan bisa melewati semua titik yang sudah diacak posisinya secara acak oleh derau tersebut.

**3b.** Misalnya kamu berhasil nemuin parameter model yang ngasih loss **jauh lebih kecil** dari angka di nomor 3a tadi. Apakah ini prestasi? Coba jelaskan.
> **Jawaban:** Malah bahaya, ini namanya *Overfitting*. Karena loss minimal mutlak aslinya sudah dibatasi oleh derau bawaan data. Kalau loss-nya dipaksa turun jauh lebih dari batas itu, artinya modelmu keliru karena cuma "menghafal" pola acak noise-nya, bukan mempelajari tren/pola sebaran umum yang aslinya (yang di mana ini adalah tujuan awal Machine Learning).

**3c.** Bandingkan hasil dari MSE dan MAE. Coba iseng tambahin satu titik *outlier* ekstrem (misal ubah data pertama jadi `y[0] + 50`). Mana yang hasil error-nya melonjak lebih gila? Kenapa?
> **Jawaban:** Nilai fungsi MSE bakal melonjak sangat jauh. Karena di rumus MSE ada proses pengkuadratan, error sebesar 50 akan berubah jadi penalti raksasa sebesar 2500. MAE cuma menghitung nilai mutlak (penalti 50). Ini membuktikan kalau MSE itu sangat "sensitif" dan rentan meledak gara-gara data *outlier*.

**3d.** Terus kalau MAE lebih kebal outlier, kenapa rumus *loss* yang paling populer dipakai di ML justru MSE (pakai kuadrat) dan bukan nilai mutlak? Sebutin **dua** alasan: satu dari sisi turunan, satu dari sisi distribusi noise.
> **Jawaban:** 
> 1. **Turunan:** Grafik fungsi kuadrat ($x^2$) bentuknya melengkung mulus berbentuk mangkok membulat di titik 0, sangat gampang diturunkan secara kalkulus (turunannya adalah $2x$). Sedangkan nilai mutlak ($|x|$) grafiknya berbentuk "V" kaku dengan patahan/sudut tajam persis di titik nol. Karena titik terendahnya adalah sudut mati, ia jadi *tidak bisa diturunkan (non-differentiable)* di titik 0.
> 2. **Derau/Noise:** Di alam nyata, noise/derau (seperti sensor eror) itu biasanya mengikuti distribusi normal (Gaussian Bell Curve). Secara hitungan probabilitas (Fisika Statistik), mencari parameter yang menghasilkan MSE terendah itu setara secara matematis dengan mencari parameter yang paling besar peluang/probabilitas kebenarannya (*Maximum Likelihood Estimation*) jika deraunya memang Gaussian.

**3e.** Waktu dites pakai parameter asli, loss-nya sekitar **1,36**. Padahal noise dibuat pakai `sigma = 1.5`, yang artinya varians teoritisnya harusnya **2,25**. Kenapa angkanya bisa beda? 
Coba eksperimen: ubah variabel `n` di kode fungsi `buat_data` jadi 200, terus 1.000, lalu 10.000. Catat loss-nya. Kesimpulannya apa?
> **Jawaban:** Ini terjadi karena di `n=50` (ukuran sampel sangat kecil), rata-rata hitungan acaknya belum konstan atau belum stabil untuk mencerminkan nilai aslinya, jadi masih banyak fluktuasi statistik (ketidakpastian). Ketika `n` kita perbanyak jadi 10.000, angkanya akan perlahan konvergen mendekati nilai ideal `2.25`. Kesimpulannya: Semakin banyak data latih/observasi yang dikumpulkan, semakin kecil peluang *error* simpangannya, sesuai dengan hukum statistik *Law of Large Numbers*.

<details>
<summary>Petunjuk 3e</summary>

Ini persis sama kayak ngitung ketidakpastian pengukuran di praktikum Fisika Dasar.
Nilai loss di parameter asli ya sebanding sama varians noise-nya. 
Tapi kan varians (2.25) itu nilai harapan (*expected value*) mutlaknya populasi (jumlah tidak terbatas). Sementara di program, kita cuma ngambil 50 sampel data acak. Makin banyak porsi sampel datanya, sebarannya rentang erornya bakal terus menyusut karena faktor $1/\sqrt{n}$.
</details>

<details>
<summary>Petunjuk 3d, alasan turunan</summary>

Gambar $f(e) = e^2$ dan $g(e) = |e|$ di sekitar sumbu tengah $e = 0$.

Yang satu sangat membulat (mulus) di dasar mangkoknya. Yang satu bentuk V dan punya patahan tajam.
Di Hari 5 nanti, kamu akan mencoba menurunkan loss terhadap variabel `w`. Apa yang terjadi pada titik yang tajam saat mau diturunkan?
</details>

<details>
<summary>Petunjuk 3d, alasan derau</summary>

Data yang kamu generate tadi dibangkitkan pakai `rng.normal`, alias pakai derau gaussian.
Coba ingat Fisika Statistik. Meminimalkan MSE itu matematis ekuivalen sama dengan memaksimalkan peluang, **asalkan** sifat alamiah gangguannya memang gaussian.
</details>

---

## Soal 4 — Pembuktian Parabola

Di plot Bagian 4, visualisasi kurvanya terbukti melengkung layaknya fungsi parabola biasa. Silakan **buktikan secara matematis/aljabar** kalau MSE emang bakal selalu ngebentuk fungsi kuadratik terhadap variabel kemiringan `w`, dengan syarat nilai `b` kita kunci diam.

Berangkat dari rumus ini:
$$\text{MSE}(w) = \frac{1}{n}\sum_i (w x_i + b - y_i)^2$$

Buktikan kalau hasil peleburannya bakal punya struktur $Aw^2 + Bw + C$, lalu bongkar rumusnya si `A`, `B`, dan `C`. (Ngerjainnya pakai corat-coret di kertas buram ya).

<details>
<summary>Petunjuk 1</summary>

Tulis ringkasannya jadi $r_i = w x_i + (b - y_i)$, terus bongkar $r_i^2$.
Satukan elemennya urutkan dari variabel $w$ pangkat tinggi.
</details>

<details>
<summary>Petunjuk 2</summary>

Nanti hasilnya kira-kira gini:
$$(w x_i + c_i)^2 = w^2 x_i^2 + 2 w x_i c_i + c_i^2 \qquad \text{di mana } c_i = b - y_i$$
Lalu terapin tanda sigma buat ngejumlahin semua perulangannya. Fokus, suku mana aja yang dikawinkan dengan $w^2$?
</details>

<details>
<summary>Petunjuk 3</summary>

$$A = \frac{1}{n}\sum x_i^2 \qquad B = \frac{2}{n}\sum x_i(b - y_i) \qquad C = \frac{1}{n}\sum (b-y_i)^2$$
</details>

**4b.** Buktikan kalau `A` bakalan terus-terusan bernilai positif. Terus, apa korelasi tanda positif ini terhadap rupa kurva mangkok kita?
> **Jawaban:** Nilai $A = \frac{1}{n}\sum x_i^2$. Karena inputan $x_i$ selalu dipangkat dua kan (kuadrat), maka hasil totalnya akan selalu menduduki rentang angka positif absolut. Dalam fungsi polinomial pangkat dua ($y = Ax^2 + Bx + C$), koefisien $A > 0$ menandakan kalau kurva parabolanya mutlak selalu melekuk/terbuka ke atas (menyediakan dasar sebagai "lembah" minimum untuk dituruni). Kalau negatif, dia malah terbuka ke bawah ibarat bukit terbalik.

**4c.** Coba cari titik terdalam di mangkoknya (posisi titik ekstrem minimum) pakai turunan manual (analitik). Turunkan rumus $Aw^2 + Bw + C$ terhadap variabel `w`, samakan hasilnya dengan 0, lalu rumuskan nilai `w` jadinya.
> **Jawaban:** 
> Penurunan Kalkulus 101: $\frac{d}{dw}(Aw^2 + Bw + C) = 2Aw + B = 0$
> Solusi nilai minimum absolut: $w^* = -\frac{B}{2A}$
> Ini ibarat contekan jalan pintas: kamu berhasil menemukan titik lembah ideal secara instan tanpa perlu susah-susah jalan merayap di tebing. Algoritma `sklearn.LinearRegression` murni make rumus konstan ginian.

**4d.** Lah, kalau secara kalkulus emang udah ada rumus instan pencari jalan pintas (solusi analitik tertutup), ngapain capek-capek pusing belajar *gradient descent* iteratif di sesi Hari 7 nanti?
> **Jawaban:** Karena solusi tertutup instan macam itu **cuma eksis secara gaib buat model arsitektur yang super sederhana kayak regresi garis lurus**. Tapi pas besok-besok kamu pindah nanganin model ruwet kayak *Neural Network* Jaringan Saraf Tiruan dengan milyaran node non-linear, secara matematis kamu nggak bisa muter rumusnya untuk mendapatkan bentuk *closed-form*. Opsimu cuma satu: merayap di tebing perlahan-lahan ke bawah (Gradient Descent).

---

## Soal 5 — Jembatan ke Ilmu Mekanika Fisika

**5a.** Mari kita cocokan dua parameter semesta ini:
$$V(x) = \tfrac{1}{2} k x^2 \qquad\qquad \text{MSE}(w) \approx A(w - w^*)^2 + C_{\min}$$
Mekanika Fisika energi potensial pegas (Kiri) berhadapan dengan fungsi Error di Machine Learning (Kanan). Apa padanan si variabel kekuatan Konstanta Pegas `k` di dunia model ML ini? Terus jarak dorongan simpangan `x` sejajar maknanya dengan variabel yang mana?
> **Jawaban:** Nilai konstan `k` itu satu bahasa dengan seberapa curam bukit datanya `A` (parameter kuadratik yang menentukan kelengkungan dinding). Sedangkan jarak/simpangan tarikan pegas `x`, memiliki arti seberapa geser melesetnya tebakan modelmu saat ini dibanding target absolut kebenarannya, yakni nilai `(w - w*)`. 

**5b.** Kalau ditarik dari per-pegasan, `k` yang tebal berarti per-nya keras/kaku alot ditarik. Nah kalau di *landscape* kerugian, `A` yang besar itu secara harfiah menggambarkan bentuk lembah yang gimana?
> **Jawaban:** Nilai parameter `A` (sebagai konstan pengali kelengkungan parabolik) yang besar bakal mencetak dinding tebing "mangkok kurva error" yang amat curam, kaku dan ramping terjal. Sebaliknya, saat koefisien ini tipis, mangkoknya akan santai merosot lebih luas, landai ibarat dataran kawah kuali.

**5c.** Lusa di Hari 7, targetnya adalah membuat program yang akan turun langkah demi langkah menuruni tebing mangkok tadi dengan ukuran lompatan kakinya, `lr` (*Learning Rate*). Meminjam logika beban berat pada pegas berayun tadi, **terka**, apa bencana yang akan muncul kalau `lr`-mu diseting kelewat ambisius (sangat besar)? 
> **Jawaban:** Sama halnya melepas balok pada karet/pegas secara kasar tanpa ada gesekan sama sekali. Tapi bayangkan perpindahan ini meloncat secara putus-putus. Ketika setingan langkah terlalu jauh, lompatan yang harusnya nyampe tenang di dasar mangkok justru terlampau kuat (kebablasan) sampai numbur dinding ke seberang jurang, yang posisinya justru makin tinggi letaknya. Saking besarnya lompatannya, nilainya bakal mentul-mentul kesana-kemari (*osilasi berlebihan*) dan pada puncaknya bakal melenting liar jauh (Divergen/NaNDomain). 

---

## Tolok Ukur Hari 3

- [x] Urutan enam tebakan di Soal 1 benar sebelum dijalankan
- [x] `prediksi`, `mse`, dan `mae` lolos uji
- [x] Lima pertanyaan Soal 3 terjawab, termasuk sapuan `n` di 3e
- [x] Bentuk kuadratik di Soal 4 terbukti di kertas, lengkap dengan `A`, `B`, `C`
- [x] `w*` analitik diturunkan, dan angkanya cocok dengan `w_min` dari program
- [x] Ramalan Soal 5c sudah kamu tulis sebelum Hari 8
- [x] Kamu bisa menjelaskan kenapa loss di parameter asli tidak nol

Kalau ketujuh kotak udah berhasil kamu tuntaskan, silakan tepuk tangan! Kamu resmi lulus Hari 3.
