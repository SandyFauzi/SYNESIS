# Soal Sesi C - Membongkar Borok Overfitting & Pasang Sistem Pegas (Regularisasi)

Berkas latihan: [`sesiC_multivariat.py`](sesiC_multivariat.py)

Sesi ini ngelupas borok Machine Learning yang kelihatan magis: *Overfitting*. Kita pakai trik regresi polinomial tingkat tinggi biar ngelihat langsung model *ngibulin* kita dengan ngehafal noise alih-alih belajar pola aslinya.

---

## Soal 0 - Pelurusan Mitos di Sesi B

**0a. Koreksi soal Gergaji (Kenapa yang lintasannya super jauh malah finish duluan?)**
> **Jawaban:** Panjang lintasan dan jumlah loop iterasi itu beda *currency* (ongkos). Di komputasi, bayarannya itu dihitung per "Satu kali ngitung gradien" (per loop), bukan per "Berapa meter kelereng gerak". Gergaji butuh 38 iterasi (langkah besar-besar), merayap lurus butuh 185 iterasi (langkah cebol). Jadi gergaji itu 5x lipat lebih murah/cepat di komputasi! Gergaji itu dihindari BUKAN karena bikin lambat, tapi karena kalau `lr`-nya kegedean dikit lagi (0.1272), dia kebablasan keluar mangkok dan langsung ERROR meledak (*NaN*).

**0c-i & 0c-ii. Misteri ReLU vs Linear di Hessian**
> **Jawaban:** Suku yang punya $y_i$ murni ada di $(f_i - y_i)\nabla^2 f_i$. Di regresi linear $f_i = wx_i + b$, turunan keduanya ($\nabla^2 f_i$) mutlak sama dengan **0**. Makanya seluruh suku yang nampung $y_i$ kehapus. Suku ini disebut *Hampiran Gauss-Newton*, dan dia tetep sakti (bagus) di Non-Linear asalkan error/residu $(f_i - y_i)$ nya super kecil mendekati nol!

**0d. Bilangan Kondisi setelah di-Standarisasi (Z-Score)**
> **Jawaban:** Setelah dibakukan, nilai $\bar{x} = 0$, dan $A = 1$. Matriks Hessiannya jadi diagonal murni $\begin{pmatrix} 2 & 0 \\ 0 & 2 \end{pmatrix}$. Nilai eigennya 2 dan 2, yang artinya bilangan kondisinya mutlak = **1.0**. Elipsnya jadi murni Lingkaran sempurna (Sesi B 2c) dan langkah gradien bakal terjun lurus *perfect* ke tengah dasar!

---

## Soal 1 - Naik Pangkat Jadi Matriks Vektor

**1b. Fitur Dummy (Kolom 1 Isinya 1 Semua)**
> **Jawaban:** Ini manipulasi aljabar pintar. Daripada nulis capek-capek $y = (X \times w) + b$, kita paksa si Bias $b$ masuk nyamar jadi sekutu bareng $w$ ke dalam grup matriks bernama Theta ($\theta$). Karena $X$ kolom awalnya angka 1, pas dikali matrik pasti jadi $1 \times \theta_{bias} = b$. Bikin arsitektur kodenya super rapi karena kita cuma ngurusin 1 vektor matriks doang.

**1c. MSE dan Gradien Versi Matriks**
> **Jawaban:**
> - MSE: `np.mean((X @ theta - y)**2)`
> - Gradien: `(2/n) * (X.T @ (X @ theta - y))`
> Hasilnya udah saya *implement* langsung ke `sesiC_multivariat.py`.

**1d. Haram Men-Denda Bias (Kolom 0)**
> **Jawaban:** Kalo Bias didenda, model kita dipaksa buat ngedorong / narik sumbu Y-intercept biar wajib mepet ke titik 0,0. Misal kita mau prediksi harga rumah (rata-rata 10 Milyar). Masa harga rumah dipaksa narik nyium lantai angka 0? Jelas modelnya bakal miring ngaco. Denda itu khusus buat melumpuhkan kelenturan bentuk kurva (*weights*), BUKAN untuk ngunci posisi ketinggian/kesetimbangan (*bias*).

---

## Soal 2 - Tiga Saksi Kebenaran (Verifikasi Silang)

**2a, 2b, 2c. Kenapa harus tiga saksi?**
> **Jawaban:** Kalkulus matriks dan skalar (Sesi A) bisa aja "bersekongkol" ngeluarin hasil salah yang sama kalau kamu nyontek/turunan aljabarnya salah dari buku. Tapi "Beda Hingga" (Finite Difference) itu pure iterasi numerik buta yang gak nyentuh rumus turunan sama sekali. Kalau Beda Hingga dan rumus matriks sepakat mutlak sampai desimal ke-12, mustahil itu cuma kebetulan!

---

## Soal 3 - Tragedi Meledaknya Presisi Matriks

**3a. Ramalan Ekstrem Presisi $X^T X$ di Derajat 14**
> **Jawaban:** Kolom polinomial terakhir di $x=3$ adalah $3^{14} \approx 4.7 \times 10^6$. Pas dimasukin ke rumus $X^T X$, angkanya dikuadratin lagi jadi gila-gilaan tembus orde $10^{13}$. Digandeng sama kolom awal yang angkanya cuma 1, rasio terjomplang ini (Bilangan Kondisi) dijamin merobek dan menghancurkan presisi 16-bit desimal `float64` CPU kita.

**3b. Pembuktian Eigen Negatif yang Mustahil Secara Teori**
> **Jawaban:** Teorema norm: $v^T (X^T X) v = (Xv)^T (Xv) = ||Xv||^2$. Hasil kuadrat norma itu MUSTAHIL kurang dari nol ($\ge 0$). Kalau komputermu ngeluarin angka eigen negatif, artinya arsitektur FP64 aritmatika di dalem prosesornya emang udah rontok dan ngeluarin *error hardware / underflow*, bukan fisika barunya yang aneh.

**3d & 3e. Hubungan Kondisi dan Iterasi Gradient Descent**
> **Jawaban:** Ratio bilangan kondisi (mentah vs baku) di derajat 3 sekitar 12x lipat (3.1e2 vs 2.4e1). Ternyata rasio lama iterasi loopnya juga sama-sama anjlok drastis (242 loop jadi sisa 27 loop, sekitar 9x). Hubungannya sebanding lurus linier! Bayangin kalo di Derajat 14 bilangan kondisinya tembus $10^{13}$, iterasinya mau berapa triliun loop? Makanya buat Derajat tinggi kita wajib menyerah pakai Gradien Descent dan beralih pakai Solusi Tertutup Matrix (Invers Matrix / Least Square).

---

## Soal 4 - Tertipu Ilusi *Overfitting*

**4a. Kenapa Derajat 14 sukses nembus error = 0 murni?**
> **Jawaban:** Polinom pangkat 14 punya **15 biji kenop koefisien**. Data sampel latih kita ada tepat **15 titik observasi**. Di Aljabar Linear, 15 Variabel buat nyelesain 15 Persamaan pasti punya 1 jawaban unik absolut! Makanya kurvanya dipaksa meliuk gila-gilaan ngelewatin tiap titik debu *noise* tanpa miss.

**4b & 4c. Kalau datanya ditambah, atau di ujung grafik?**
> **Jawaban:** Kalau sampel data digenapin jadi 16, model bakal keringat dingin. Dia gak punya sisa kelenturan/kenop lagi buat maksa ngelewatin titik ke-16. Error langsung *break* pecah telur ($> 0$). Kerusakannya super terlihat di ujung grafik absis (batas $\pm 3$) gara-gara koefisien pangkat tinggi ($x^9, x^{14}$) bakal ngedorong dominan bikin kurvanya nukik/meroket tak terkontrol ke Infinity di celah yang nggak ada titik datanya.

**4d. Kenapa Derajat 3 asli pun nggak bisa nyentuh Error 0?**
> **Jawaban:** Fungsi kubik sejati (derajat 3) adalah ruh dari simulasi kita, error-nya stagnan di $4.26$. Dia nggak bisa neken ke nol karena lantai absolut *error* kita udah diganjal murni sama varians stokastik acak Gaussian (Noise buatan $= 2.25$). Menekan di bawah lantai varians murni = overfit nge-hafalin posisi debu acak.

---

## Soal 5 - Drama Train VS Test (Puncak Masalah)

**5a. Hukum Alam "Train Loss Gak Pernah Naik"**
> **Jawaban:** Menambah derajat (dari $x^3 \rightarrow x^4$) itu ngasih ruang dimensi kelenturan ekstra buat model. Kalau ternyata kenop $x^4$ malah bikin tambah ancur, komputer pinteran dikit cukup nge-set $w_4 = 0$ dan si model langsung nge-rewind wujud balik jadi $x^3$. Makanya error Train secara logika matematis pasti diam di tempat atau makin turun, mustahil naik.

**5c. Kenapa Test Loss Derajat 8 ke 9 Loncat Eksplosif (6 ke 923)?**
> **Jawaban:** Ini gara-gara perpaduan overfit dan Matriks $X^T X$ CPU-nya mulai ambyar. Di pangkat 9 rasio angkanya udah nyebrang batas presisi aman *float64*. Invers-nya penuh sama halusinasi artefak numerik.

**5d & 5e. Cara Tes Model Tanpa Ngetes (Data Validation K-Fold)**
> **Jawaban:** Kalau data ujian nggak ada, pakai aja trik licik bernama *Cross Validation*. Potong datamu jadi 5 blok. Blok 1-4 dipakai buat latihan, Blok 5 dipake ujian. Terus tukeran siklusnya sampai semua ngerasain jadi penguji.
> Jangan pernah buta ngeliatin Kurva Train aja! Kurva train bakal manis banget ke 0 ngebohongin kamu, padahal aslinya di dunia nyata modelnya murni ngehafal buta (Overfit kronis).

---

## Soal 6 - Pil Ajaib Pengekang Kehancuran (L2 Regularization)

**6a & 6d. Denda L2 = Ilmu Hukum Hooke Pegas**
> **Jawaban:**
> Denda penalti $\lambda \theta^2$ itu sejatinya Energi Potensial Pegas Fisika ($V = \frac{1}{2} k x^2$).
> Turunannya ($2\lambda \theta$) adalah **Gaya Pemulih Pegas** ($F = -kx$).
> Konstanta pegasnya adalah **$2\lambda$**.
> Titik keseimbangannya ($0.0$).
> Kalau ada parameter (koefisien theta) yang sok-sokan naik nilainya (meliuk-liuk lebay), pegas L2 bakal narik dan mukul kenceng dia balik ke arah Nol!

**6b. Restorasi Parameter Efektif**
> **Jawaban:** Derajat 14 punya 15 parameter. Tapi pas kita tembak pakai Regularisasi Lambda 0.1, error Test-nya anjlok balik manis ke level Derajat 3. Ini artinya, gaya pegas tadi sukses meredam dan mematikan fungsi belasan derajat tinggi yang nggak penting, maksa sisa "parameter aktif" / *Degrees of Freedom* nya balik cuma nyisa jadi 4 komponen berguna murni doang.

**6c. Kurva Bentuk U (Kenop Derajat vs Kenop Lambda)**
> **Jawaban:** Keduanya nyetel tensi *Bias vs Variance Trade-off*.
> - Derajat naik = melenturkan model (Overfit).
> - Lambda naik = mengeraskan/mengkakukan model pegas (Underfit).
> Kedua kenop sama-sama ngukur keseimbangan tarik tambang antara Kelenturan (hafal *noise*) lawan Kaku (gagal nangkep *pattern*).

**6e. Dosa Fatal Pembakuan (Data Leakage)**
> **Jawaban:** Standarisasi (Z-Score) data Test/Uji WAJIB murni nyolong nilai Rata-rata dan Standar Deviasi milik data Train. Jangan pernah ngehitung manual z-score murni milik test itu sendiri! Kalo kamu hitung sendiri, artinya kamu ngebiarin model ngintip "kisi-kisi ujian" (sebaran data masa depan) sebelum bertanding di ring asli. Ini musibah terbesar yang bikin bocor (Data Leakage) dan akurasi palsu!

---

## Tolok Ukur Sesi C

- [x] Jawaban 4c Sesi B ditulis ulang, dan perbedaan ongkos per langkah lawan per jarak jelas
- [x] Bilangan kondisi setelah pembakuan dihitung di kertas, dan sambungannya ke Soal 2c Sesi B disadari
- [x] Bentuk matriks gradien diturunkan sendiri dari bentuk skalar Sesi A
- [x] Kolom 0 tidak didenda, dan kamu bisa menjelaskan kenapa
- [x] Ketiga saksi di Bagian 2 sepakat di bawah `1e-12`
- [x] Semidefinit positif dibuktikan dalam dua baris, dan arti nilai eigen negatif kamu pahami
- [x] Hubungan bilangan kondisi dengan jumlah iterasi dicocokkan dengan angka terukur
- [x] Train loss nol di derajat 14 dijelaskan lewat jumlah persamaan lawan jumlah yang tak diketahui
- [x] Grafik train turun sementara test naik dihasilkan dan kamu bisa membacanya
- [x] L2 menurunkan test loss derajat 14 dari miliaran jadi satu digit, dan mekanismenya kamu jelaskan lewat gaya pemulih
- [x] Kebocoran data lewat pembakuan dipahami sebagai bahaya, bukan detail teknis

Semua kotak udah terisi centang! Overfitting dan Bias-Variance udah ditaklukkan pakai ilmu fisika (Hukum Pegas) wkwk. Gas sisa Bulan 0-nya!
