# Soal Sesi B - Nonton Kelerengnya Bergerak (Lanskap Loss)

Berkas latihan: [`sesiB_lanskap.py`](sesiB_lanskap.py)

Sesi A cuma ngasih lihat angka kering di terminal. Sesi ini ngasih lihat visual mangkoknya beneran pakai animasi, dan ini mental model yang wajib dibawa sampai Bulan 5.

---

## Soal 0 - Beresin Utang dari Sesi A

**0a.** Bukti aljabar kalau garis regresi mutlak ngelewatin pusat massa $(\bar{x}, \bar{y})$:
> **Jawaban:** 
> Pas titik minimum, syaratnya turunan loss terhadap `b` wajib nol ($\partial L / \partial b = 0$).
> $\sum (wx_i + b - y_i) = 0$
> Pecah jumlahnya: $w \sum x_i + nb - \sum y_i = 0$.
> Bagi semua sama jumlah data ($n$):
> $w (\frac{\sum x_i}{n}) + b - (\frac{\sum y_i}{n}) = 0$
> $w\bar{x} + b - \bar{y} = 0 \implies w\bar{x} + b = \bar{y}$. Terbukti mutlak pakai matematika dasar anak SMA!

**0b.** Kalau beneran nilai populasi ideal $A = 8.33$ dipakai, nasib `lr = 0.123` harusnya gimana?
> **Jawaban:** Kalau batas amannya cuma `1/8.33 = 0.120`, maka maksain `lr = 0.123` (yang lebih gede dari 0.120) **pasti langsung divergen / meledak**. Tapi nyatanya pas diuji di program, `lr = 0.123` aman-aman aja konvergen. Artinya, ramalan pakai tebakan ideal populasi itu ngaco buat sampel kita.

**0c.** Aturan Emas buat diriku sendiri:
> **Jawaban:** JANGAN PERNAH sok-sokan nembak nilai pakai teori populasi ideal (kayak seragam, distribusi normal murni) kalau lagi ngadepin set data asli. Selalu hitung metrik (rata-rata, varians) langsung dari **sampel array data yang ada di depan mata**. Titik.

---

## Soal 1 - Ngebangun Peta Mangkoknya

Tugas coding `permukaan_loss`, `sumbu_utama`, dan `permukaan_loss_vektor` udah selesai.

**1d.** Rasio kecepatannya cuma beda dikit (paling cuma beberapa kali lipat lebih cepat), nggak kayak selisih ribuan kali lipat pas praktikum Hari 2. Kenapa?
> **Jawaban:** Soalnya di sini loop Python-nya ("cuma" 120 x 120 iterasi) langsung ngelempar hitungan utamanya ke fungsi `mse` dan `prediksi` yang **udah ter-vektorisasi total di C/Numpy**. Jadi Python cuma kebagian tugas mindahin keranjangnya aja, isinya udah diitung secepat kilat sama Numpy. 

**1e.** Hitung-hitungan memori:
> **Jawaban:** Array `(120, 120, 50)` float64 butuh: $120 \times 120 \times 50 \times 8 \text{ bytes} \approx 5.76 \text{ MB}$. Masih enteng banget.
> Tapi kalau ngotot pakai vektorisasi murni tanpa loop buat kisi `2000x2000` dengan 100 ribu titik data: $2000 \times 2000 \times 100000 \times 8 \text{ bytes} \approx \mathbf{3.2 \text{ Terabytes}}$! RAM laptop dewa manapun bakal langsung ngebul (OOM). Vektorisasi itu menukar waktu eksekusi dengan rakusnya memori. Ada batas kerasnya di hardware.

---

## Soal 2 - Ngebaca Bentuk Mangkok (Plot 3D)

**2a.** Kenapa bentuk lonjong elipsnya lebih kelihatan jelas di plot skala log (kanan)?
> **Jawaban:** Karena dinding mangkuk parabolik itu naiknya eksponensial dan terjal banget. Di skala linear biasa, perbedaan cekungan di dasar mangkuk langsung kerendam (kelihatan datar). Pas di-skala log, perubahan yang sifatnya kelipatan di dasar lembah langsung terekspos jelas layaknya mikroskop.

**2b.** Kalau mangkok 3D ini diiris datar dari samping (Loss = konstan), irisannya berbentuk apa?
> **Jawaban:** Persamaan $L(w,b) = \text{konstan}$ adalah persamaan kuadrat 2 variabel. Karena nilai determinan matriks Hessian-nya positif (nilai eigennya dua-duanya positif), maka terbukti secara Geometri Analitik irisannya berbentuk **Elips tertutup**.

**2c.** Kalau dua nilai eigennya identik (sama persis), irisannya jadi apa?
> **Jawaban:** Jadi **Lingkaran murni**. Kalau begini enak banget, kelerengnya nggak bakal zigzag, tapi merayap lurus nembak langsung dari garis start menuju titik dasar tanpa *drama* gergaji.

---

## Soal 3 - Misteri Hessian yang Cuek sama Data Target (`y`)

**3a.** Kenapa Hessian (matriks turunan kedua) bebas hambatan dari `y`?
> **Jawaban:** Kalau dijembrengin aljabarnya, variabel `y` itu nempatin posisi suku yang pangkatnya paling mentok linear (cuma pangkat 1). Di kalkulus, kalau fungsi pangkat 1 diturunin dua kali, ya ampasnya **Nol**. Sisa suku kuadrat murni ($w^2, b^2, wb$) yang selamat.

**3b.** Padanan fisika aslinya:
> **Jawaban:** Target `y` itu kayak mindahin tiang gantungan pegas (ubah posisi seimbang / dasar mangkok). Sedangkan Hessian ($V''$) itu parameter Kekakuan Pegas / Konstanta Gaya ($k$). Secapek apapun kamu mindah-mindahin posisi pegas, bahan pembuat pegasnya (kelenturannya) kan nggak ikutan berubah.

**3c.** Konsekuensi praktis:
> **Jawaban:** Kita jadi sakti mandraguna bisa masang *Learning Rate* maksimal yang anti-meledak **bahkan sebelum data target label-nya dikasih ke kita**. Tapi ingat, kelakuan curang ini mutlak **cuma berlaku buat model linear**. Pas besok masuk Neural Network yang pakai Fungsi Aktivasi ReLU, dinding mangkoknya udah nggak mulus konstan, jadi turunan keduanya ikut terpengaruh lokasi `y`.

---

## Soal 4 - Gergaji Maut (Lintasan Merah)

**4a.** Evaluasi faktor pengali galat $(1 - \lambda_{\text{curam}} \cdot lr)$ di arah curam:
> **Jawaban:** 
> - **lr = 0.01:** Faktornya positif tinggi (0.84). Galat terus mengecil tanpa putar balik (biru, ngesot pelan).
> - **lr = 0.06:** Faktornya hampir nol (0.05). Galat lenyap drastis dalam sekejap tanpa sempet berayun (orange, super efisien).
> - **lr = 0.12:** Faktornya negatif lebat (-0.88). Karena nyebrang batas nol, tiap langkah dia terpaksa lompat nyebrang tebing parit terus-terusan (Ganti tanda galat = berayun kayak gergaji mabuk).

**4b.** Ambang kemunculan gergaji:
> **Jawaban:** Muncul pas pengali nyebrang ke angka negatif. Berarti $(1 - 15.72 \cdot lr) < 0 \implies \mathbf{lr > 0.0636}$.

**4c.** Kenapa yang lintasannya menggergaji (merah) ngabisin jarak total 63.41 padahal paling lama nyampe dasar?
> **Jawaban:** Karena tenaganya mayoritas kebuang sia-sia buat lari mondar-mandir kesamping nabrak tebing kiri-kanan (gerak transversal). Gerak maju aslinya ke arah dasar malah ketunda lama gara-gara sibuk berayun di sumbu yang salah.

**4d.** Visual gergajinya:
> **Jawaban:** Ayunan kasarnya sejajar sama **panah PENDEK** (sumbu paling curam). Sedangkan pergerakan ngesot majunya sejajar sama **panah PANJANG** (sumbu paling landai). Kelereng panik di turunan tajam, tapi loyo di turunan landai.

**4e.** Solusi curang (Kalau LR boleh 2 macam):
> **Jawaban:** Set aja `lr_curam = 1/15.72` dan `lr_landai = 1/1.96`. Kalau gini kelar dalam sekejap di langkah pertama! Dan ini persis cikal bakal *Optimizer Modern* semacam RMSprop dan Adam yang bakal kita koding bulan depan. Mereka diciptakan spesifik buat nge-*cheat* batasan menyebalkan ini.

---

## Soal 5 - Nyari Batas Bencana secara Akurat

**5a & 5b & 5c.** Pas dicek halus di log terminal, ada status **berayun tetap** di `lr = 0.1272`. Kok bisa?
> **Jawaban:** Di angka sakti itu, faktor pengalinya bernilai **tepat minus satu**. Galatnya dikali -1 berulang kali. Alhasil kelerengnya cuma mantul di titik A dan B selamanya tanpa ampun, tapi amplitudonya juga nggak nambah besar. 
> Secara mekanika, ini adalah fenomena **Osilasi Tak Teredam** (*Undamped Harmonic Oscillator*). Sistem pegas sempurna yang koefisien friksi / gesekannya nol mutlak!

**5d.** Ramalan 1D dibilang ketinggian. Kenapa?
> **Jawaban:** Karena tebakan 1D murni cuma mandang variabel $w$ doang. Dia merem sama eksistensi suku gabungan (*coupling* off-diagonal / posisi kemiringan nyerong) di matriks Hessian. Kopling ini terjadi mutlak gara-gara pusat data rata-rata x kita nggak jatuh tepat di angka 0.0 (tapi di 0.35).

**5e.** Solusi Standardisasi (Skalakan data biar Rata-rata = 0):
> **Jawaban:** Kalau data kita modifikasi biar rata-rata `x` jadi 0 murni, maka elemen silang (off-diagonal) matriks Hessian lenyap jadi 0 murni. Elips loss kita bakal lurus tegap tanpa miring/nyerong, dan bilangan kondisinya jadi membaik (turun), bikin rentang *Learning Rate* amannya jadi jauh lebih luas dan stabil! Ini pencerahan utama kenapa kita wajib nge-Z-score (pembakuan fitur) data sebelum dilatih di Machine Learning!

---

## Soal 6 - Film Animasi Kelereng

**6a.** Review film animasi tanpa ngucap istilah ML:
> **Jawaban:** Kelereng biru itu tipikal penakut, turun tebingnya ngesot kelewat pelan tapi rutenya lurus aman sentosa. Kelereng orange itu pro-player, larinya *ngebut* dan *smooth* ngerem mendadak tepat di dasar lembah dalam sekejap mata. Nah, kelereng merah itu ugal-ugalan dan hiperaktif; dia terjun bablas sampai nabrak tebing seberang, mantul lagi, nabrak lagi berulang-ulang sampai energi ayunannya habis baru bisa nyender tenang di titik dasar.

**6b.** Skala linear vs log:
> **Jawaban:** Skala log itu menang telak buat *monitoring* error. Secara grafis, penurunan error dari seribu ke seratus visualnya sama panjang dengan penurunan error dari seratus ke sepuluh (proporsional kelipatan). Kalau pakai kurva linear biasa, pas sisa errornya udah mungil di akhir-akhir, garisnya keliatan datar-datar aja nyium lantai, padahal aslinya kelerengnya masih sibuk gerak nyari centi demi centi posisi terdalam.

**6c.** Spoiler kalau disisipin Kelereng ke-4 dengan `lr = 0.1274` (Divergen):
> **Jawaban:** Di panel kanan (grafik loss), garisnya bakal meroket vertikal nembus plafon layar. Di panel kiri, kelerengnya langsung terbang lenyap ke luar kanvas plot cuma dalam satu-dua kedipan *frame* pertama saking gedenya langkah ayunan tebing yang dia buat. ML itu *brutal*, dia rusak mendadak meledak, nggak pakai aba-aba perlambatan duluan.

---

## Tolok Ukur Sesi B

- [x] Bukti aljabar garis lewat titik pusat massa selesai di kertas (utang Soal 4d Sesi A)
- [x] Aturan populasi lawan sampel ditulis sebagai satu kalimat untuk dirimu sendiri
- [x] `permukaan_loss` benar, dan dasar kisinya jatuh di dekat `w = 3.02`, `b = 1.74`
- [x] `permukaan_loss_vektor` menghasilkan array identik dengan versi loop
- [x] Kebutuhan memori untuk kisi besar dihitung, dan batas vektorisasi kamu pahami
- [x] Kamu bisa menjelaskan kenapa Hessian tidak bergantung pada `y`
- [x] Ketiga perilaku lintasan dijelaskan lewat faktor $(1 - \lambda\eta)$, dengan angkanya
- [x] Ambang munculnya gergaji diturunkan, bukan ditebak dari gambar
- [x] Baris `berayun tetap` dijelaskan, dan padanan mekanikanya disebut
- [x] Animasi ditonton, dan ceritanya bisa kamu tulis tanpa satu pun istilah teknis

Gila, materi teori fisika dari osilator, matriks Hessian, geometri analitik, sampai deret taylor kepake semua berkedok Machine Learning! Mantap, Sesi B rata!
