# Soal Bulan 2 Sesi 3 - representasi, dan batasnya

Berkas latihan: [`bulan2_sesi3_embedding.py`](bulan2_sesi3_embedding.py)

Delapan TODO. Sesi ini menyerang sebab dari angka buruk Sesi 2: kantong kata
memperlakukan tiap kata sebagai pulau, jadi kata yang belum pernah dilihat
tidak berkurang bobotnya, melainkan hilang sama sekali.

> Prasyarat: Sesi 1 dan 2 dikerjakan dulu. Berkas ini mengimpor `belah_tiga`,
> `bangun_kosakata`, `bobot_idf`, `vektorkan`, dan `latih` dari Sesi 2, serta
> `Tensor` dan `maju` dari Bulan 1 Sesi 3+4. Nol kode autograd baru, lagi.

> Peringatan yang jujur: sesi ini kemungkinan besar tidak berakhir dengan
> lompatan akurasi. Beberapa soal di bawah memang meminta kamu menyimpulkan
> bahwa percobaannya tidak bisa memutuskan. Itu jawaban yang benar, bukan
> jawaban yang menghindar.

---

## Soal 1 - Berapa besar sampel supaya selisih 10 poin berarti

Bagian 1 memberi:

```text
tebak ubah_proyek terus     39.0%      24.1 .. 54.0
model Sesi 2                56.1%      40.9 .. 71.3
```

**1a.** Selang di Sesi 2 dihitung untuk menjawab "berapa data uji yang saya
butuh". Di sini arahnya dibalik. Turunkan lebar selang 95 persen sebagai
fungsi $n$ pada $p = 0{,}56$, lalu tunjukkan kenapa $n = 41$ menghasilkan
lebar sekitar 30 poin.

> **Jawaban:** Akurasi adalah proporsi dari $n$ percobaan Bernoulli, jadi
> $\sigma=\sqrt{p(1-p)/n}$ dan lebar selang 95 persennya
>
> $$W(n)=2\cdot 1{,}96\sqrt{\frac{p(1-p)}{n}}=\frac{3{,}92\sqrt{p(1-p)}}{\sqrt n}.$$
>
> Pada $p=0{,}56$ pembilangnya tetap: $3{,}92\sqrt{0{,}56\cdot 0{,}44}=1{,}9459$.
> Jadi $W(n)=1{,}9459/\sqrt n$, dan $n$ masuk sebagai akar, bukan sebagai
> pengali. Untuk $n=41$: $W=1{,}9459/6{,}403=0{,}3039$, yaitu **30,4 poin**.
> Terukur (Uji A), dan Bagian 1 mencetak selang yang sama, `40,9 .. 71,3`,
> lebar 30,4.
>
> ```
>        n    lebar (poin)
>       41            30.4
>      100            19.5
>      200            13.8
>      400             9.7
>     1000             6.2
>     3840             3.1
> ```
>
> Konsekuensi yang perlu dibawa sepanjang sesi: menyempitkan selang dua kali
> lipat menuntut data empat kali lipat.

**1b.** Kamu mau bisa membedakan dua model yang selisihnya 10 poin persen,
dengan kepercayaan 95 persen. Perlakukan itu sebagai uji dua proporsi
berpasangan: kedua model diuji pada kalimat yang SAMA. Hitung $n$ yang
dibutuhkan, dan sebutkan asumsi apa yang kamu pakai tentang korelasi
kesalahan kedua model.

> **Jawaban:** Berpasangan berarti kedua model diuji pada 41 kalimat yang
> sama, jadi yang dibandingkan bukan dua proporsi bebas melainkan selisih per
> kalimat. Ikuti gagasan McNemar: sebut $b$ jumlah kalimat yang benar di
> model A dan salah di B, dan $c$ kebalikannya. Kalimat yang kedua model
> sama-sama benar atau sama-sama salah tidak menyumbang apa-apa ke selisih,
> jadi ia keluar dari perhitungan sepenuhnya. Itulah tuas pengungkitnya.
>
> Dengan $\psi=(b+c)/n$ porsi kalimat yang BERBEDA dan $\delta=(b-c)/n$
> selisih akurasi,
>
> $$\operatorname{Var}(\hat p_A-\hat p_B)=\frac{\psi-\delta^2}{n},\qquad
> n>\frac{1{,}96^2\,\psi}{\delta^2}=384{,}16\,\psi \;\;\text{untuk }\delta=0{,}10.$$
>
> Terukur (Uji A), dengan kolom kedua memakai kuasa 80 persen
> ($z_\beta=0{,}84$):
>
> ```
>      psi    n (selang 95%)   n (95% + kuasa 80%)
>     0.10                38                    38
>     0.15                58                   103
>     0.20                77                   153
>     0.30               115                   233
>     0.40               154                   310
>     0.55               211                   424
> ```
>
> **Asumsi tentang korelasi kesalahan, dinyatakan terang-terangan:** angkanya
> seluruhnya bergantung pada $\psi$, dan $\psi$ kecil kalau kedua model salah
> pada kalimat yang sama. Dua model yang dilatih dari data yang sama dengan
> kosakata yang sama memang begitu: Bagian 3 menunjukkan lima resep fitur
> berbeda mendarat dalam rentang 7,3 poin, yang berarti mereka salah di
> kalimat yang kurang lebih sama. Saya pakai $\psi\approx 0{,}30$ sebagai
> tebakan kerja, jadi **$n\approx 115$** untuk sekadar selangnya tidak memuat
> nol, dan **$n\approx 233$** kalau saya juga mau 80 persen peluang
> menemukannya kalau memang ada. Batas bawah mutlaknya $\psi\ge\delta=0{,}10$,
> yaitu $n=38$, dan itu cuma tercapai kalau model baru tidak pernah salah di
> tempat model lama benar.
>
> Pembanding tak berpasangan pada $p\approx 0{,}5$: $n=192$ per model, jadi
> 384 kalimat. Berpasangan menghemat dua sampai lima kali lipat, dan
> penghematan itu gratis karena kedua model memang diuji di kalimat yang sama.

**1c.** Bandingkan hasil 1b dengan angka 3.840 dari Soal 1c Sesi 2. Kedua
angka menjawab pertanyaan yang berbeda. Nyatakan bedanya dalam satu kalimat
masing-masing.

> **Jawaban:** Angka 3.840 menjawab: berapa kalimat harus saya TULIS supaya
> akurasi SATU model punya selang selebar 5 poin (576 kalimat uji, lalu
> $576/0{,}15$ untuk belahan 70/15/15).
>
> Angka 115 menjawab: berapa kalimat harus saya UJIKAN pada KEDUA model
> sekaligus supaya selisih 10 poin di antara keduanya bisa dibedakan dari nol.
>
> Yang pertama menakar satu pengukuran mutlak, yang kedua menakar sebuah
> selisih; dan karena berpasangan membatalkan bagian kesalahan yang dipikul
> bersama, yang kedua jauh lebih murah.

**1d.** Dasar mayoritas 39,0 persen itu dihitung dari 41 pesan yang komposisi
kelasnya sangat timpang. Kalau kamu mengumpulkan 200 pesan nyata lagi, apakah
dasar mayoritasnya akan naik, turun, atau tidak bisa ditebak? Jawab dengan
alasan, bukan tebakan.

> **Jawaban:** **Tidak bisa ditebak**, dan alasannya dua lapis, bukan satu.
>
> Pertama, ralat pengukurannya sendiri sudah menelan jawabannya. Dasar
> mayoritas 39,0 persen dari $n=41$ punya selang `24,1 .. 54,0`, lebar 29,9
> poin (Uji A). Sampel baru dari populasi yang SAMA saja sudah bisa mendarat
> di mana pun di dalam pita itu, cuma karena derau pencacahan.
>
> Kedua, 200 pesan berikutnya bukan dari populasi yang sama. Ke-41 pesan itu
> percakapan merancang proyek bersama agen pemrograman; 200 pesan berikutnya
> akan berupa pemakaian SYNESIS. Dua distribusi yang berbeda menurut
> konstruksinya.
>
> Dua gaya tarik yang berlawanan, keduanya masuk akal, dan tidak satu pun
> terukur:
>
> - **turun**: sekarang cuma 8 dari 15 intent terpakai. Makin banyak pesan,
>   makin banyak intent yang tersentuh, dan tujuh kelas yang menganggur cuma
>   bisa mengambil massa dari `ubah_proyek`.
> - **naik**: cara saya memakai asisten mungkin jauh lebih berulang daripada
>   cara saya merancangnya. Kalau ternyata begitu, satu kelas justru memadat.
>
> Yang bisa saya nyatakan tanpa menebak cuma batasnya: dasar mayoritas tidak
> bisa di bawah $1/15=6{,}7$ persen dan tidak bisa di atas 100 persen.

<details>
<summary>Petunjuk 1b</summary>

Untuk dua model yang diuji pada contoh yang sama, yang penting bukan $n$
total melainkan jumlah contoh tempat keduanya BERBEDA. Cari "uji McNemar".
Kamu tidak perlu memakai ujinya; cukup pakai gagasannya untuk melihat kenapa
uji berpasangan butuh sampel jauh lebih kecil daripada uji tak berpasangan.

</details>

---

## Soal 2 - Vektor nol

Bagian 2 menemukan tiga pesan nyata yang seluruh katanya di luar kosakata,
sehingga vektor masukannya nol utuh.

**2a.** Tanpa menjalankan model, turunkan keluaran jaringan untuk masukan nol.
Tulis logitnya sebagai rumus dalam $W_1, b_1, W_2, b_2$.

> **Jawaban:** Model Bagian 2 adalah `maju` dari Bulan 1, yaitu
> $\mathrm{out}=\mathrm{relu}(XW_1+b_1)W_2+b_2$. Pasang $X=0$:
>
> $$\mathrm{out}=\mathrm{relu}(0\cdot W_1+b_1)W_2+b_2=\mathrm{relu}(b_1)\,W_2+b_2.$$
>
> $X$ hilang seluruhnya. Yang tersisa tetapan yang tidak memuat satu pun
> angka dari kalimat.
>
> Terukur (Uji B): selisih antara rumus $\mathrm{relu}(b_1)W_2+b_2$ dan
> keluaran `maju` yang benar-benar dijalankan adalah `0.000e+00`, cocok
> sampai bit terakhir.

**2b.** Dari 2a, kelas apa yang keluar? Apakah kelas itu sama untuk ketiga
pesan? Apakah ia bergantung pada isi kalimat sama sekali?

> **Jawaban:** Kelas yang keluar adalah $\arg\max$ dari satu vektor tetap itu.
> Karena vektornya tidak memuat $X$, ia **sama persis untuk ketiga (di data
> sekarang: kedua) pesan**, dan **sama sekali tidak bergantung pada isi
> kalimat**. Model tidak menebak berdasarkan kalimat; ia mengeluarkan satu
> jawaban baku untuk apa pun yang tidak dikenalinya.
>
> Satu koreksi terhadap soalnya, dilaporkan apa adanya. Soal 2 menyebut TIGA
> pesan bervektor nol. Terukur di data sekarang: **dua**.
>
> ```
> kosakata sintetis     : 402 kata
> kalimat bervektor NOL : 2 dari 41
>   'continue from where you left off.'
>   'iyh katakan kaya distribusi wien'
> ```
>
> Sebabnya bukan salah hitung: `data/bulan2/perintah_train_generated.txt`
> sudah diganti dari 1.080 kalimat (kosakata 353) jadi 15.000 kalimat
> (kosakata 402), dan `data/bulan2/README.md` mencatat pergantian itu.
> Kosakata yang lebih besar menyelamatkan satu kalimat dari nol. Seluruh tabel
> Sesi 3 di bawah ikut bergeser karena sebab yang sama, dan tiap kali itu
> terjadi saya sebutkan.

**2c.** Jalankan modelnya dan periksa jawabanmu di 2b. Catat juga keyakinan
softmax-nya, lalu nyatakan apakah ambang di Soal 5 Sesi 2 akan menolak kasus
ini atau tidak.

> **Jawaban:** Terukur (Uji B), model dua lapis yang sama persis dengan baris
> pertama tabel Bagian 3:
>
> ```
> kelas keluar : obrol, sama untuk SEMUA kalimat nol
> keyakinan    : 0.3972
> ambang tangan obrol = 0.30  -> LOLOS
> ambang ongkos obrol = 0.667 -> DITOLAK
> ```
>
> Ramalan 2b kena: satu kelas, sama untuk semua, tidak bergantung isi.
>
> **Ambang Soal 5 Sesi 2 TIDAK menolak kasus ini.** `AMBANG_INTENT["obrol"]`
> saya setel 0,30, dan keyakinannya 0,397. Jadi model melewatkan sebuah
> kalimat yang secara harfiah tidak ia baca satu katanya pun.
>
> Untuk kelengkapan, model tersimpan yang benar-benar dipakai SYNESIS
> (`model_intent.npz`, softmax satu lapis, 353 kolom) memberi `obrol` dengan
> keyakinan 0,2784, dan itu lolos-tipis di bawah 0,30 sehingga kebetulan
> ditolak. Selisihnya 0,0216. Menggantungkan pagar keamanan pada margin
> sebesar itu bukan pagar.

**2d.** Kalau ternyata ambangnya TIDAK menolak vektor nol, itu cacat yang
serius dan gampang diperbaiki tanpa melatih apa pun. Tulis perbaikannya
sebagai satu syarat yang diperiksa sebelum model dipanggil, dan sebutkan di
mana syarat itu harus dipasang supaya tidak bisa dilewati.

> **Jawaban:** Syaratnya satu baris, dan tidak perlu memanggil model sama
> sekali:
>
> ```python
> if not any(w in model["kosakata"]
>            for w in re.findall(r"[a-z0-9]+", kalimat.lower())):
>     tolak
> ```
>
> Artinya: kalau tidak satu pun kata kalimat itu punya kolom, vektornya nol,
> dan apa pun yang keluar dari model tidak bergantung pada kalimatnya. Menolak
> di situ bukan kehati-hatian berlebihan; itu satu-satunya jawaban yang jujur.
>
> **Di mana dipasang supaya tidak bisa dilewati:** di `jalankan_pipa` sebagai
> langkah 0, sebelum `ramal`. Bukan di `vektorkan` (itu pengubah fitur, bukan
> pengambil keputusan, dan ia dipakai juga waktu melatih), bukan di
> `putuskan` (ia cuma menerima vektor peluang dan tidak pernah melihat
> kalimatnya). `jalankan_pipa` satu-satunya pintu yang dilewati `cli.py`
> maupun seluruh pengukuran, jadi memasangnya di situ berarti tidak ada jalur
> yang melewatinya.
>
> Sudah dipasang di [`../synesis/niat.py`](../synesis/niat.py), dengan
> tindakan baru `tolak_kosong`, dan diuji di `_demo()`:
>
> ```
> python -m synesis.niat
> niat: semua pemeriksaan lulus
> ```

---

## Soal 3 - Panjang potongan yang mana

Sapuan Bagian 3 mengubah satu hal saja, yaitu batas panjang n-gram:

```text
fitur              kolom   pesan nyata      selang 95 persen
kata (Sesi 2)        353         51.2%          35.9 .. 66.5
n-gram 2-4          2668         43.9%          28.7 .. 59.1
n-gram 3-4          2359         56.1%          40.9 .. 71.3
n-gram 3-5          3615         58.5%          43.5 .. 73.6
n-gram 4-6          3615         53.7%          38.4 .. 68.9
```

**3a.** Rentang tabel 14,6 poin. Nyatakan dengan angka dari kolom terakhir
apakah tabel ini bisa memutuskan panjang potongan mana yang lebih baik.

> **Jawaban:** **Tidak bisa.** Terukur, dengan data latih sekarang (15.000
> kalimat sintetis, bukan 1.080 seperti waktu tabel soal dicetak):
>
> ```
> fitur              kolom   pesan nyata      selang 95 persen
> kata (Sesi 2)        402         43.9%          28.7 .. 59.1
> n-gram 2-4          2864         39.0%          24.1 .. 54.0
> n-gram 3-4          2549         46.3%          31.1 .. 61.6
> n-gram 3-5          3940         43.9%          28.7 .. 59.1
> n-gram 4-6          3990         41.5%          26.4 .. 56.5
> ```
>
> Rentang seluruh tabel 7,3 poin. Lebar selang tiap barisnya 30 poin. Titik
> tertinggi (46,3) duduk di dalam selang titik terendah (`24,1 .. 54,0`), dan
> sebaliknya titik terendah (39,0) duduk di dalam selang titik tertinggi
> (`31,1 .. 61,6`). Kelima selang saling memuat titik satu sama lain. Menurut
> aturan yang dipakai sepanjang sesi ini, tidak ada satu baris pun yang boleh
> disebut lebih baik daripada baris lain.
>
> Ada bukti kedua yang lebih tajam daripada perbandingan selang, dan ia datang
> dari kecelakaan: tabel di soal dihitung pada korpus latih lama dan
> rentangnya 14,6 poin dengan urutan `3-5 > 3-4 > 4-6 > kata > 2-4`. Tabel
> saya rentangnya 7,3 poin dengan urutan `3-4 > kata = 3-5 > 4-6 > 2-4`. Baris
> terbaik berpindah hanya karena data latihnya diganti. Peringkat yang
> berpindah waktu satu hal yang tak ada hubungannya diubah adalah peringkat
> yang mengukur derau.

**3b.** Kalau kamu memilih baris tertinggi lalu melaporkannya sebagai "hasil
n-gram karakter", berapa besar kelebihan lapor yang kamu perbuat? Pakai
$\sigma\sqrt{2\ln k}$ dengan $k$ jumlah baris yang kamu bandingkan, dan
jelaskan asal rumus itu dalam satu kalimat.

> **Jawaban:** Asal rumusnya satu kalimat: **nilai harapan maksimum dari $k$
> peubah normal baku tumbuh seperti $\sqrt{2\ln k}$, jadi memilih yang
> terbesar dari $k$ pengukuran berderau lalu melaporkannya seolah satu
> pengukuran menaikkan angkanya kira-kira sebesar $\sigma\sqrt{2\ln k}$.**
>
> Terukur (Uji C), dengan $\sigma=\sqrt{p(1-p)/n}$ pada $n=41$ dan $p$ di
> sekitar rerata tabel:
>
> ```
> sigma satu baris = 7.8 poin
>
>   k baris   sqrt(2 ln k)    kelebihan lapor
>         2          1.177               9.1p
>         3          1.482              11.5p
>         5          1.794              13.9p
>        10          2.146              16.7p
> ```
>
> Saya membandingkan $k=5$ baris. Jadi melaporkan 46,3 persen sebagai "hasil
> n-gram karakter" adalah **kelebihan lapor sekitar 13,9 poin** — hampir dua
> kali lipat seluruh rentang tabelnya sendiri (7,3 poin). Angka yang jujur
> untuk dilaporkan bukan baris terbaik melainkan seluruh tabel, dan itulah
> kenapa tabelnya saya salin utuh di 3a.

**3c.** Kamu tetap harus memilih satu untuk dipakai di Sesi 4. Sebutkan
kriteria yang KAMU pakai untuk memilihnya, dan pastikan kriteria itu bukan
akurasi di tabel ini. Sebutkan minimal dua kriteria dan mana yang menang.

> **Jawaban:** Dua kriteria, dan keduanya sengaja bukan kolom akurasi:
>
> **Kriteria 1 - ongkos di waktu pakai.** Kata: 402 kolom. n-gram: 2.549
> sampai 3.990 kolom. `model_intent.npz` sekarang 43 KB pada 353 kolom, jadi
> versi n-gram sekitar sepuluh kali lipat, dan tiap klasifikasi adalah satu
> perkalian matriks selebar itu. Sesi 2 mengukur 0,004 milidetik per perintah;
> sepuluh kali lipat masih tak terasa. **Kriteria ini tidak memutuskan apa
> pun** — ia cuma menyatakan bahwa harganya terjangkau.
>
> **Kriteria 2 - perilaku pada kata yang belum pernah dilihat, diukur bukan
> ditebak.** Ini yang menang.
>
> ```
> satuan                        jumlah   di luar latih
> kata                             667           51.1%
> potongan karakter 3-5           7696           34.6%
>
> kata asing unik                              : 251
> yang masih punya minimal satu potongan dikenal: 228 = 90.8 persen
> kalimat bervektor NOL, fitur kata            : 2 dari 41
> ```
>
> Kolom kata membiarkan 2 dari 41 pesan masuk ke jaringan sebagai vektor nol,
> dan Soal 2 sudah membuktikan bahwa untuk kasus itu model mengeluarkan satu
> jawaban baku dengan keyakinan 0,397 yang lolos ambang tangan. Itu bukan
> akurasi yang lebih rendah; itu jenis kegagalan yang berbeda, dan ia terukur
> pasti, bukan lewat selang selebar 30 poin.
>
> **Yang saya pakai di Sesi 4: n-gram 3-5.** Bukan karena skornya tertinggi
> (bukan; 3-4 yang tertinggi), melainkan karena ia menghapus kelas kegagalan
> vektor nol, dan itu satu-satunya hal di tabel ini yang bisa saya ukur
> dengan pasti. Antara 3-4 dan 3-5 saya ambil 3-5 karena cakupan potongannya
> lebih lebar dengan ongkos setara; selisih akurasi 2,4 poin di antara
> keduanya **secara eksplisit bukan alasannya**, karena 2,4 poin itu satu
> kalimat.
>
> Catatan kejujuran: Sesi 4 tetap berjalan di atas `model_intent.npz` yang
> memakai fitur kata 353 kolom, karena berkas itu prasyarat Sesi 4 dan
> melatihnya ulang akan mengubah seluruh tabel Sesi 4 sehingga tak bisa
> dibandingkan dengan soalnya. Jadi keputusan ini tercatat, belum terpasang.

**3d.** Baris `n-gram 2-4` adalah satu-satunya yang lebih buruk daripada
kata biasa. Ajukan penjelasan mekanistik, lalu rancang satu pengukuran yang
bisa membuktikan penjelasanmu salah.

> **Jawaban:** **Penjelasan mekanistiknya:** potongan 2 huruf adalah "yang"
> dari ruang fitur ini. Jumlahnya sedikit, tapi masing-masing hadir di banyak
> kalimat, sehingga tidak membedakan apa-apa. Dan karena tiap baris
> dinormalkan jadi panjang satu, kolom yang ramai itu **merebut porsi norma**
> dari potongan 3-4 huruf yang justru membedakan. Baris `n-gram 2-4` bukan
> "3-4 ditambah informasi"; ia "3-4 dikali faktor peredam".
>
> **Pengukuran yang dirancang untuk membuktikannya salah:** hitung berapa
> kalimat memuat tiap potongan, per panjang. Kalau potongan 2 huruf ternyata
> sama jarangnya dengan potongan 4 huruf, penjelasan saya salah dan
> tersangkanya berpindah ke jumlah kolom.
>
> Terukur (Uji C), 15.000 kalimat latih:
>
> ```
>   panjang   potongan unik   median df   df > 50%   df = 1
>         2             315         747         13        0
>         3            1069         186          2        0
>         4            1480         132          0        0
>         5            1391         114          0        0
> ```
>
> Median kehadiran potongan 2 huruf 747 kalimat, enam setengah kali lipat
> potongan 5 huruf, dan 13 potongan hadir di lebih dari separuh seluruh
> kalimat sementara panjang 4 dan 5 tidak punya satu pun. Penjelasannya tidak
> terbantah.
>
> Tapi angka kehadiran saja belum menunjukkan mekanismenya. Yang menunjukkan
> ini:
>
> ```
> di fitur n-gram 2-4, potongan 2 huruf memegang 45.9 persen panjang
> kuadrat tiap baris, padahal cuma 172 dari 829 kolom.
> ```
>
> Dua puluh satu persen kolom memegang empat puluh enam persen norma. Itu
> peredamnya, diukur langsung.

<details>
<summary>Petunjuk 3d</summary>

Hitung berapa potongan sepanjang 2 huruf yang ada, dan berapa kalimat yang
memuat masing-masing. Bandingkan dengan potongan sepanjang 5. Salah satu
dari keduanya berperilaku seperti kata "yang" di Sesi 2.

</details>

---

## Soal 4 - Matriks ko-okurensi

**4a.** `matriks_kookurensi` MELEWATI kata di luar kosakata, bukan menghapusnya
dari barisan. Jelaskan apa bedanya bagi hasil, dengan satu contoh kalimat
pendek yang menunjukkan dua hasil berbeda.

> **Jawaban:** Bedanya: **melewati** menjaga jarak asli antar kata,
> **menghapus** memalsukan kedekatan yang tidak pernah ada di teksnya.
>
> Terukur (Uji D), kalimat `saya install venv pakai python`, jendela 2,
> kosakata `{install, python}`:
>
> ```
> dilewati : C[install][python] = 0
> dihapus  : C[install][python] = 1
> ```
>
> `install` di posisi 1 dan `python` di posisi 4, terpisah tiga langkah, jadi
> di luar jendela 2. Kalau `saya`, `venv`, dan `pakai` dibuang dari barisan,
> keduanya jadi bertetangga langsung dan matriks mencatat kedekatan yang
> teksnya tidak pernah punya.
>
> **Yang lebih benar: melewati**, karena jendela adalah alat ukur jarak di
> dalam teks, dan menghapus berarti mengubah teks yang sedang diukur.
>
> Keberatan yang harus ikut ditulis supaya jujur: kalau kosakatanya kecil
> relatif terhadap korpusnya, melewati membuat hampir tidak ada yang
> bertetangga dan matriksnya kosong. Di sini kosakatanya 2.000 dari 12.128
> kata unik dan matriksnya 7,6 persen terisi sesudah PPMI, jadi masalah itu
> tidak muncul. Yang tidak bisa dipertahankan bukan salah satu pilihan itu,
> melainkan tidak tahu pilihan mana yang sedang dipakai.

**4b.** Diagonal matriksnya ternyata tidak nol. Jelaskan kenapa, lalu putuskan
apakah diagonal itu sebaiknya dinolkan sebelum PPMI. Jawaban harus menyebut
akibatnya terhadap $p(i)$ dan $p(j)$, bukan cuma "kelihatannya aneh".

> **Jawaban:** **Kenapa tidak nol:** `C[i][i]` menghitung berapa kali kata $i$
> muncul di dekat kata $i$ LAGI di dalam jendela. Syarat `j != i` cuma
> mencegah pasangan sebuah token dengan dirinya di posisi yang sama; ia tidak
> mencegah kata yang sama muncul dua kali dalam satu jendela. Untuk kata
> sering, itu terjadi terus.
>
> Terukur (Uji D):
>
> ```
> diagonal taknol   : 1206 kata dari 2000
> massa diagonal    : 25.166 dari 1.095.594 = 2,30 persen
> diagonal terbesar : the, yang, md, print, import
> ```
>
> **Akibat menolkannya terhadap $p(i)$ dan $p(j)$, dan ini inti soalnya.**
> Matriksnya simetris, jadi $C[i][i]$ ikut dalam jumlah baris DAN jumlah
> kolom. Menolkannya menurunkan $p(i)$ dan $p(i)$ sekaligus, plus menurunkan
> totalnya. Karena
>
> $$\mathrm{PMI}(i,j)=\log_2\frac{p(i,j)}{p(i)p(j)},$$
>
> menurunkan $p(i)$ **menaikkan PMI setiap pasangan lain yang melibatkan $i$**.
> Jadi menolkan diagonal bukan menghapus satu sel; ia menimbang ulang seluruh
> baris dan seluruh kolom ke atas, dan paling keras justru untuk kata yang
> paling sering, karena merekalah pemilik diagonal terbesar.
>
> Terukur:
>
> ```
> p(the)  turun 1.901% -> 1.822%
> p(yang) turun 1.897% -> 1.890%
> p(md)   turun 0.485% -> 0.457%
> ```
>
> **Putusan: dibiarkan.** Dua alasan. Pertama, diagonal itu sifat nyata dari
> teksnya — kata sering memang berulang dalam lima kata, dan PPMI memang
> bertugas mengukur sifat nyata. Kedua, arah pergeserannya salah: menolkannya
> mengangkat PMI seluruh tetangga kata tersering, padahal justru dominasi kata
> tersering yang PPMI ada untuk melawan.
>
> Dan hasil hilirnya memang tidak peduli:
>
> ```
> median peringkat: diagonal dibiarkan 6, dinolkan 6  (14 pasangan)
> ```
>
> Dua koma tiga persen massa tidak menggerakkan apa pun. Jadi keputusannya
> boleh diambil karena alasannya benar, bukan karena angkanya menuntut.

**4c.** Jendela dipatok 5 kata. Ramalkan lebih dulu apa yang terjadi pada
median peringkat kalau jendelanya 2 dan kalau 15, lalu ukur. Laporkan
ramalanmu apa adanya, termasuk kalau ternyata salah.

> **Jawaban, ramalan ditulis lebih dulu:**
>
> Jendela 2 menangkap kolokasi — kata yang memang bersebelahan secara
> harfiah: `gradient descent`, `pip install`, `git commit`. Jendela 15
> mengaburkannya jadi keterkaitan topik dan membuat matriksnya jauh lebih
> padat, jadi lebih banyak pasangan dapat bukti tapi tiap bukti lebih lemah.
> `PASANGAN_UJI` saya lebih dari separuh berupa kolokasi. **Ramalan saya:
> jendela 2 LEBIH BAIK daripada 5, dan jendela 15 lebih buruk. Urutan
> terbaik ke terburuk: 2, 5, 15.**
>
> Terukur (Uji D):
>
> ```
>   jendela   taknol PPMI   median peringkat
>         2          3.9%                  6
>         5          7.6%                  6
>        15         13.9%                  8
> ```
>
> **Ramalan saya separuh salah.** Bagian kedua kena: jendela 15 memang lebih
> buruk (8 lawan 6), dan kepadatan matriksnya memang naik hampir empat kali
> lipat dari jendela 2 ke 15, persis seperti yang saya duga. Bagian pertama
> meleset: jendela 2 **tidak** lebih baik daripada 5, keduanya seri di 6.
>
> Yang saya salah duga: saya mengira mempersempit jendela akan mempertajam
> kolokasi. Ternyata ia juga membuang bukti — jendela 2 cuma mengisi 3,9
> persen sel, separuh dari jendela 5. Ketajaman yang didapat dan bukti yang
> hilang saling meniadakan. Dan 15 pasangan uji terlalu sedikit untuk memisah
> selisih sekecil itu, yang membawa langsung ke Soal 5c.

**4d.** Matriks 2.000 x 2.000 float64 memakan berapa MB? Kalau kamu ingin
kosakata 50.000 seperti korpus sungguhan, berapa? Sebutkan satu perubahan
struktur data yang membuatnya muat, dan apa yang kamu korbankan.

> **Jawaban:** Terukur (Uji D):
>
> ```
>  2000 x 2000 =      31 MB = 0,03 GB
> 50000 x 50000 =  19.073 MB = 18,62 GB
> ```
>
> $50.000^2\times 8 = 2\times 10^{10}$ bita. Delapan belas setengah gigabita
> untuk satu matriks, sebelum SVD-nya minta ruang kerja sendiri. Laptop ini
> tidak punya.
>
> **Perubahan struktur data: simpan jarang, bukan rapat.** Terukur, sesudah
> PPMI cuma 7,6 persen sel yang taknol, jadi COO/CSR pada kosakata 50.000
> kira-kira $50.000^2\times 0{,}076\times 16$ bita $\approx 2{,}8$ GB, dan
> turun jadi sekitar 1,4 GB dengan `float32` plus `int32`.
>
> **Yang dikorbankan, tiga hal, dan yang ketiga paling mahal:**
>
> 1. Akses satu sel tidak lagi satu geseran alamat melainkan pencarian.
> 2. `C[i,j] += 1` waktu membangun jadi lambat sekali, jadi matriksnya harus
>    dibangun dulu di `Counter` berkunci `(i, j)` lalu dikonversi sekali.
> 3. `np.linalg.svd` tidak berlaku lagi. Harus pindah ke SVD terpotong seperti
>    `scipy.sparse.linalg.svds`, yang memberi cuma $d$ nilai singular teratas
>    dan memberikannya secara hampiran, bukan eksak. Jadi yang dikorbankan
>    bukan cuma kenyamanan, melainkan kepastian bahwa arah yang saya potong
>    memang arah yang paling sedikit menjelaskan.

---

## Soal 5 - PPMI dan penilaiannya

**5a.** Turunkan PMI dari definisi informasi bersama. Tunjukkan kenapa
penyebut $p(i)p(j)$ itu tepat peluang gabungan seandainya $i$ dan $j$ saling
bebas, dan karena itu PMI mengukur simpangan dari kebebasan.

> **Jawaban:** Informasi bersama antara dua peubah acak adalah
>
> $$I(X;Y)=\sum_{i,j}p(i,j)\log_2\frac{p(i,j)}{p(i)p(j)}.$$
>
> Ia sebuah nilai harapan. Yang di dalam logaritma, sebelum dijumlahkan
> berbobot, adalah sumbangan satu pasangan tertentu, dan itulah PMI:
>
> $$\mathrm{PMI}(i,j)=\log_2\frac{p(i,j)}{p(i)p(j)}.$$
>
> Jadi $I(X;Y)=\mathbb{E}[\mathrm{PMI}]$: informasi bersama adalah rerata PMI,
> dan PMI adalah informasi bersama yang dibongkar per pasangan.
>
> **Kenapa penyebutnya tepat peluang gabungan seandainya bebas.** Kebebasan
> DIDEFINISIKAN sebagai $p(i,j)=p(i)p(j)$. Jadi $p(i)p(j)$ bukan hampiran
> atau pilihan selera; ia persis nilai yang akan diambil $p(i,j)$ kalau $i$
> dan $j$ tidak berhubungan. Rasionya karena itu terbaca "berapa kali lebih
> sering daripada yang diramalkan kebebasan", dan logaritmanya memberi:
>
> - $\mathrm{PMI}=0$ persis waktu $p(i,j)=p(i)p(j)$, yaitu bebas;
> - $\mathrm{PMI}>0$ waktu bersebelahan lebih sering daripada kebetulan;
> - $\mathrm{PMI}<0$ waktu lebih jarang.
>
> Karena itu PMI mengukur **simpangan dari kebebasan**, dalam satuan bit, dan
> bukan mengukur seberapa sering dua kata bersebelahan.

**5b.** Nilai PMI negatif dibuang. Sebutkan dua alasan berbeda: satu alasan
statistik tentang korpus kecil, satu alasan komputasi tentang SVD.

> **Jawaban:**
>
> **Alasan statistik, tentang korpus kecil.** PMI negatif berarti "bersebelahan
> LEBIH JARANG daripada kebetulan". Untuk memperkirakan ketidakhadiran dengan
> andal, hitungan harapan tiap sel harus cukup besar supaya nol punya arti.
> Terukur: korpus 167.334 token dengan jendela 5 kiri-kanan menghasilkan
> sekitar 1,1 juta pasangan yang tersebar ke $2000^2=4$ juta sel. Rerata isi
> satu sel di bawah satu. Sel bernilai nol bisa berarti dua kata itu memang
> saling menolak, atau berarti pasangan itu belum pernah tersampel, dan tidak
> ada di dalam data ini yang bisa memisahkan keduanya. Jadi nilai negatifnya
> hampir seluruhnya derau pencacahan.
>
> **Alasan komputasi, tentang SVD.** Menyimpan yang negatif membuat matriksnya
> rapat: keempat juta sel punya nilai, dan sebagian besarnya $\log 0=-\infty$
> yang harus dipatok ke suatu angka berhingga yang dipilih sembarang. Memotong
> di nol menyisakan 7,6 persen sel taknol (terukur), yang (a) muat di memori
> pada kosakata yang lebih besar, (b) membolehkan SVD terpotong jarang, dan
> (c) mencegah SVD menghabiskan arah singular pertamanya untuk menjelaskan
> nilai lantai yang dipakai bersama oleh 92 persen matriks. Arah yang terbuang
> itu bukan cuma boros; ia menggeser arah lain yang benar-benar berisi.

**5c.** Bagian 5 melaporkan median peringkat sekitar 5 dari 2.000 kata,
dengan pembanding acak 1.000. Simpulkan apa artinya untuk kualitas vektor
katamu, dan nyatakan seberapa yakin kamu boleh dari 15 pasangan uji.

> **Jawaban:** Terukur (Bagian 5), kosakata 2.000 kata:
>
> ```
> pasangan uji terpakai : 15 dari 16
> median peringkat      : 5 dari 2000 kata
> pembanding acak       : 1000
> ```
>
> **Artinya untuk kualitas vektor:** untuk pasangan uji yang khas, pasangannya
> ada di peringkat 5 dari 2.000, yaitu 200 kali lebih baik daripada dadu.
> Vektor itu jelas menangkap sesuatu yang nyata tentang korpus saya, dan
> menangkapnya dari teks tanpa label sama sekali.
>
> **Seberapa yakin saya boleh dari 15 pasangan: sangat tidak.** Median dari 15
> sampel ditentukan oleh satu-dua nilai di tengah. Selang kepercayaan 95
> persen bebas-sebaran untuk median pada $n=15$ terbentang dari statistik
> terurut ke-4 sampai ke-12 (dari binomial$(15;0{,}5)$, $P(X\le 3)=0{,}018$).
> Itu lebih dari separuh sampel. Jadi pernyataan yang boleh saya buat bukan
> "median peringkat 5", melainkan "median peringkat ada di suatu tempat antara
> pengukuran ke-4 dan ke-12 saya", dan saya tidak punya cukup pasangan untuk
> mempersempitnya.
>
> Bukti tambahan bahwa 15 pasangan terlalu sedikit datang dari Soal 4c: tiga
> ukuran jendela yang sangat berbeda memberi median 6, 6, dan 8. Alat ukurnya
> tidak bisa memisahkan tiga percobaan yang jelas berbeda, jadi ia juga tidak
> bisa dipercaya waktu ia memberi angka bagus.

**5d.** Pasangan uji di `PASANGAN_UJI` disusun oleh saya, sesudah melihat
korpusnya. Sebutkan bias apa yang masuk lewat jalan itu, dan rancang cara
menyusun pasangan uji yang tidak punya bias itu.

> **Jawaban:** **Bias yang masuk: bias penyusun yang sudah melihat data.** Saya
> memilih pasangan yang saya sudah tahu bersebelahan di tulisan saya sendiri —
> `python`/`venv`, `git`/`commit`, `gpu`/`cuda`. Tapi bersebelahan di tulisan
> saya PERSIS statistik yang dipasangi PPMI-SVD. Jadi ujinya menanyakan
> "apakah pipa ini mengawetkan ko-okurensi yang sudah bisa saya lihat dengan
> membaca", bukan "apakah representasi ini tahu sesuatu yang saya tidak tahu".
> Itu uji kewarasan pipa, bukan uji representasi.
>
> Bias kedua, lebih halus dan lebih memalukan: 15 dari 16 pasangan terpakai,
> artinya satu pasangan gugur karena katanya tidak ada di kosakata. Kalau saya
> sudah membuka daftar tetangga sebelum menyusun daftarnya — dan saya menulis
> keduanya di sesi yang sama — saya akan memilih pasangan yang daftarnya
> sudah tunjukkan, tanpa berniat curang sedikit pun.
>
> **Rancangan yang tidak punya bias itu.** Kuncinya bukan kecerdikan melainkan
> urutan: daftarnya harus dibekukan sebelum modelnya ada, dan disusun oleh
> orang yang belum melihat modelnya. Itulah sebenarnya yang membuat tolok ukur
> analogi seperti `man : king :: woman : queen` sah — bukan karena
> pasangannya pintar, melainkan karena penyusunnya tidak pernah melihat model
> yang akan diuji, dan daftarnya terbit lebih dulu.
>
> Protokol untuk skala saya:
>
> 1. Ambil 100 kata acak dari kosakata 2.000, dengan benih yang dicatat.
> 2. Serahkan daftar itu ke orang lain, atau ke saya sendiri pada waktu
>    berikutnya, dan minta satu kata yang paling diharapkan berdekatan untuk
>    tiap kata — **tanpa** pernah melihat daftar tetangga.
> 3. Bekukan daftarnya ke berkas, commit, baru jalankan.
> 4. Yang gugur karena di luar kosakata dihitung sebagai gugur, bukan dibuang
>    diam-diam. Angka "15 dari 16" harus jadi bagian dari laporan.
>
> Yang mengubah statusnya dari kesan jadi bukti adalah langkah 3, dan
> satu-satunya biaya langkah 3 adalah kesabaran.

<details>
<summary>Petunjuk 5d</summary>

Bandingkan dengan cara orang menyusun tolok ukur analogi kata seperti
`man : king :: woman : queen`. Perhatikan siapa yang menyusun daftarnya dan
apakah mereka sudah melihat model yang akan diuji.

</details>

---

## Soal 6 - Ukuran korpus

Sapuan Bagian 5 memberi median peringkat pada empat ukuran korpus, dengan
kosakata dipatok sama.

**6a.** Salin tabelnya, lalu nyatakan apakah kurvanya masih menurun di titik
terakhir. Simpulkan apakah menambah teks masih akan menolong.

> **Jawaban:** Terukur (Bagian 5), kosakata dipatok 1.200 kata dari korpus
> penuh supaya cuma satu variabel yang berubah:
>
> ```
>   token dibaca  pasangan   median peringkat    acak
>          16258        12                600     600
>          40647        12                576     600
>          81294        12                  8     600
>         162589        12                  3     600
> ```
>
> **Masih menurun di titik terakhir**: 8 turun ke 3, yaitu membaik 2,7 kali
> lipat waktu korpusnya digandakan. Jadi ya, korpusnya masih lapar dan
> menambah teks masih akan menolong.
>
> Satu syarat yang harus ikut disebut, kalau tidak kesimpulan ini menyesatkan:
> peringkat median tidak bisa turun di bawah 1, dan sekarang sudah di 3. Cuma
> tersisa dua langkah ruang. **Alat ukurnya akan jenuh jauh sebelum
> representasinya jenuh**, jadi lain kali korpusnya digandakan angka ini akan
> mendatar entah representasinya membaik atau tidak. Menyimpulkan "sudah
> cukup" dari kurva yang mendatar di 2 akan salah.

**6b.** Antara dua titik tengah ada penurunan yang sangat tajam. Ajukan
penjelasan kenapa kualitas vektor kata melompat, bukan naik perlahan.
Kaitkan dengan berapa kali sebuah kata harus muncul supaya hitungan
tetangganya berhenti didominasi kebetulan.

> **Jawaban:** Penurunan tajamnya antara 40.647 dan 81.294 token: median 576
> — praktis sama dengan acak 600 — jatuh ke 8.
>
> **Kenapa melompat, bukan naik perlahan.** Baris tetangga sebuah kata baru
> berguna sesudah hitungannya berhenti didominasi kebetulan. Kata yang muncul
> $f$ kali dengan jendela 5 kiri-kanan menaruh sekitar $10f$ hitungan yang
> tersebar ke seluruh kosakata. Di bawah kira-kira sepuluh sampai dua puluh
> kemunculan, hampir tiap sel di barisnya bernilai 0 atau 1, dan PPMI tidak
> punya cara memisahkan hubungan nyata dari satu kebetulan tunggal. Barisnya
> derau, dan arah SVD yang dibangun darinya juga derau.
>
> Yang membuatnya melompat: kata tidak menyeberangi ambang itu satu per satu.
> Frekuensi kata mengikuti Zipf, jadi sebongkah besar kosakata duduk di pita
> frekuensi yang sempit, dan menggandakan korpus **memindahkan seluruh
> bongkahan itu melewati garis pada saat yang sama**.
>
> Terukur (Uji E), kolom terakhir menghitung median kemunculan kata-kata di
> `PASANGAN_UJI` di tiap ukuran korpus:
>
> ```
>   token dibaca   median peringkat   median hitungan kata uji
>          16733                571                          0
>          41833                573                          0
>          83667                  6                         28
>         167334                  3                         78
> ```
>
> Kata ujinya melompat dari median 0 kemunculan ke 28 di langkah yang sama
> dengan lompatan peringkat. Itu bukan korelasi longgar; itu mekanismenya
> terbaca langsung. Selama kata ujinya belum muncul, tidak ada yang bisa
> dipelajari tentangnya, berapa pun bagusnya sisa pipanya.

**6c.** GloVe dilatih pada 6 miliar token. Korpusmu sekitar 150 ribu. Hitung
rasionya, lalu sebutkan dua kemampuan yang korpus sebesar itu punya dan
korpusmu tidak akan pernah punya berapa lama pun kamu menulis.

> **Jawaban:** Terukur: korpus saya 167.334 token, GloVe $6\times 10^9$. Rasio
> **35.856 kali**, sekitar 4,6 orde besaran.
>
> **Dua kemampuan yang tidak akan pernah saya punya, berapa lama pun saya
> menulis:**
>
> 1. **Statistik untuk ekor panjang.** Kosakata GloVe 400.000 kata punya
>    hitungan yang bisa dipakai untuk kata yang muncul beberapa kali dalam
>    semiliar. Korpus saya punya 12.128 kata unik, dan yang 2.000 tersering
>    saja sudah harus dipatok supaya matriksnya muat. Sisa sepuluh ribu kata
>    itu permanen tak terpakai, dan menulis lebih banyak tidak
>    memperbaikinya: saya cuma menulis tentang hal yang saya tulis.
>
> 2. **Struktur analogi dan pemisahan makna.** Hubungan seperti
>    `raja - pria + wanita ~ ratu` menuntut keempat katanya terlihat di banyak
>    konteks berbeda supaya vektor SELISIHNYA stabil. Itu butuh kata yang sama
>    dipakai lintas topik dan lintas laras, dan korpus satu penulis satu
>    proyek secara struktural tidak bisa menyediakannya pada panjang berapa
>    pun.
>
> Versi jujurnya: batas korpus saya bukan jumlah token, melainkan bahwa ia
> sampel berukuran satu dari ruang konteks. Satu penulis, satu ranah, satu
> tahun.

**6d.** Sebaliknya: sebutkan satu hal yang korpus 150 ribu katamu tahu dan
GloVe tidak tahu. Beri satu contoh kata dari daftar tetangga di Bagian 5.

> **Jawaban:** Yang korpus saya tahu dan GloVe tidak: **arti kata di dalam
> tata letak berkas dan kebiasaan proyek ini.**
>
> Contoh dari daftar tetangga Bagian 5:
>
> ```
> roadmap -> harian, silabus, pdf, rencana, jarvis, dokumen, modul
> ```
>
> Di GloVe, `roadmap` duduk dekat `plan`, `strategy`, `blueprint`, `vision` —
> bahasa Inggris bisnis yang umum. Di korpus saya ia duduk dekat `silabus`,
> `harian`, `modul`, dan `jarvis`, karena di proyek ini "Roadmap" adalah
> sebuah berkas tertentu di `docs/`, bertetangga dengan `Silabus.md`,
> `Modul.md`, dan `Bulan-1-Harian.md`. Itu bukan fakta umum tentang kata
> "roadmap"; itu fakta tentang folder saya, dan justru fakta itulah yang akan
> membuat SYNESIS bisa menyelesaikan "buka roadmap".
>
> Contoh kedua yang lebih tajam:
>
> ```
> install -> publish, plugin, claude, powershell, confirmation, catalog, confirm
> ```
>
> Itu kosakata `claude-skills/`. Tidak ada korpus umum yang akan menaruh
> `install` bertetangga dengan `claude` dan `catalog`, karena tetangga itu
> ada hanya di repo ini.

---

## Soal 7 - Prapelatihan dan langit-langit sintetis

Bagian 6 mengadu embedding acak lawan embedding yang dimulai dari vektor
PPMI-SVD korpusmu sendiri.

**7a.** Kolom validasi sintetis kedua baris itu 100 persen, padahal titik
awalnya sangat berbeda. Jelaskan kenapa kolom itu tidak bisa membedakan apa
pun, dengan menyebut sifat data sintetisnya.

> **Jawaban:** Terukur (Bagian 6): embedding acak 100,0 persen, embedding
> PPMI-SVD 99,3 persen. Selisih 0,7 poin dari dua titik awal yang sama sekali
> berbeda.
>
> **Sifat data sintetisnya yang membuat kolom itu buta:** kalimatnya dibuat
> oleh `scripts/generate_bulan2_data.py` dari sekumpulan cetakan tetap
> (`BENTUK_PERINTAH`, `BENTUK_OBROL`, dan seterusnya) yang diisi dari daftar
> isian tetap. Belahan validasinya diambil dari generator yang SAMA dengan
> belahan latihnya, jadi tiap kalimat validasi adalah susunan ulang potongan
> yang sudah pernah dilihat model dengan label yang sama. Tugasnya bisa
> diselesaikan dari cetakan permukaannya saja, nyaris tabel pencarian.
>
> Kolom yang bernilai 100 persen untuk setiap susunan yang dicoba punya daya
> pisah nol. Ia mengukur bahwa pengoptimalnya konvergen, bukan bahwa
> representasinya bagus. Sesi 1 sudah menyebut 100 persen sebagai gejala,
> bukan prestasi; Bagian 6 di sini menunjukkan gejala yang sama, kali ini
> untuk dua model yang seharusnya bisa dibedakan.

**7b.** Kolom pesan nyata bergerak sedikit. Nyatakan dengan selangnya apakah
gerakan itu terukur.

> **Jawaban:** Terukur (Bagian 6):
>
> ```
> model                   validasi sintetis   pesan nyata      selang 95 persen
> embedding acak                     100.0%         39.0%          24.1 .. 54.0
> embedding PPMI-SVD                  99.3%         41.5%          26.4 .. 56.5
> ```
>
> **Tidak terukur.** Geserannya 2,4 poin, yaitu satu kalimat dari 41. Selang
> keduanya, `24,1 .. 54,0` dan `26,4 .. 56,5`, bertumpang tindih di hampir
> seluruh panjangnya, dan yang lebih menentukan: masing-masing titik duduk
> jauh di dalam selang lawannya. Menurut aturan yang dinyatakan di Bagian 1
> ("sebuah resep dianggap lebih baik hanya kalau selangnya tidak lagi memuat
> resep pembanding"), prapelatihan PPMI-SVD tidak lebih baik daripada acak di
> pengukuran ini.
>
> Perlu ditambahkan supaya kesimpulannya tidak dibaca terlalu jauh: ini bukan
> bukti bahwa prapelatihan tidak berguna. Ini bukti bahwa 41 kalimat uji tidak
> bisa mengukurnya. Soal 1b sudah menghitung berapa yang dibutuhkan, dan
> jawabannya sekitar 115.

**7c.** Bagian 6 memberi vektor awal hanya untuk kata yang ada di korpus,
dan menyisakan nol untuk sisanya. Kata yang bervektor nol punya sifat khusus
selama latihan. Turunkan sifat itu dari aturan turunan `__matmul__`, lalu
sebutkan apakah kata itu bisa belajar apa-apa.

> **Jawaban:** Turunan untuk `E` dari `__matmul__`, pada `H0 = X @ E`:
>
> ```python
> other.grad += self.data.T @ out.grad      # E.grad += X.T @ H0.grad
> ```
>
> Baris ke-$i$ dari `X.T` adalah kolom ke-$i$ dari `X`. Kalau kata $i$ tidak
> pernah muncul di satu pun kalimat latih, kolom itu nol seluruhnya, jadi
> baris ke-$i$ dari `X.T @ H0.grad` **nol persis** — tak peduli apa isi
> `E[i]`, tak peduli berapa epoch. Barisnya tidak pernah bergerak dari nilai
> awalnya.
>
> **Jadi kata itu tidak bisa belajar apa-apa**, dan karena nilai awalnya nol
> untuk kata yang tak ada di korpus, ia tetap nol selamanya. Waktu meramal,
> sumbangannya ke `X @ E` juga nol, jadi ia tak terlihat — persis sama dengan
> berada di luar kosakata, kecuali ia menghabiskan satu kolom.
>
> Terukur (Uji F). Data latih penuh memakai setiap kata, jadi kasusnya harus
> dibuat dengan memotong ke 200 kalimat:
>
> ```
>   200 kalimat latih, kosakata 402, kolom NOL di data latih: 325
>       |grad E| terbesar di baris kolom nol   : 0.000e+00
>       |grad E| terbesar di baris kata yang ada: 1.261e-02
> 10500 kalimat latih, kosakata 402, kolom NOL di data latih: 0
>       |grad E| terbesar di baris kata yang ada: 2.193e-03
> ```
>
> Nol persis, bukan kecil. Dan dari baris kedua: di data latih penuh **tidak
> ada satu pun kolom yang nol**, jadi 169 kata yang dapat vektor awal nol di
> Bagian 6 sebenarnya SEMUANYA masih bisa belajar. Vektor awal nol bukan
> hukuman mati; yang mematikan gabungan "awal nol" dan "tak pernah muncul".
>
> Ada mekanisme kedua yang saya temukan waktu mengukurnya, dan ia bukan yang
> ditanyakan petunjuknya:
>
> ```
> E awal NOL seluruhnya: |grad E| terbesar 0.000e+00
> ```
>
> Kalau SELURUH `E` nol, `H0 = X @ 0 = 0`, lalu `relu(0 @ W1 + b1)` dengan
> `b1` juga nol memberi nol, dan turunan `relu` di nol bernilai nol karena
> aturannya `(self.data > 0)`. Gradiennya mati di tekukan, bukan di `X`.
> Jaringan itu tidak bisa mulai belajar sama sekali. Itulah kenapa
> `latih_embed` mengisi `E` dengan bilangan acak waktu `E0=None`, dan kenapa
> memberi nol untuk SEBAGIAN baris aman sementara memberi nol untuk semuanya
> tidak.

**7d.** Prapelatihan seperti ini adalah gagasan yang sama dengan BERT, cuma
kecil. Sebutkan tiga hal yang BERT tambahkan di atasnya, dan untuk tiap satu,
sebutkan masalah apa yang diselesaikannya.

> **Jawaban:** Tiga yang BERT tambahkan di atas gagasan yang sama, dan masalah
> yang diselesaikan masing-masing:
>
> 1. **Vektor kontekstual dari transformer, bukan satu vektor per jenis kata.**
>    Masalah yang diselesaikan: kata bermakna banyak dan bergantung konteks.
>    Di tabel saya `buka` punya persis satu vektor, entah maksudnya membuka
>    berkas atau membuka sesi. BERT menghitung vektor berbeda untuk tiap
>    kemunculan, dari seluruh kalimatnya.
>
> 2. **Sasaran prapelatihan yang menuntut RAMALAN, bukan pencacahan: masked
>    language modeling.** Masalah yang diselesaikan: matriks PPMI saya cuma
>    mencatat bahwa dua kata bersebelahan, tidak mencatat urutan maupun
>    susunannya. Meramalkan kata yang disembunyikan dari konteksnya memaksa
>    representasi memuat sintaks dan batasan pemilihan kata, yang persis
>    dibuang oleh hitungan ko-okurensi.
>
> 3. **Penalaan seluruh tumpukan pada tugas hilir, bukan sekadar memakai
>    vektornya sebagai nilai awal yang beku.** Masalah yang diselesaikan:
>    persis yang diukur Bagian 6. `E` saya berangkat dari PPMI-SVD, tapi semua
>    yang di atasnya berangkat dari acak dan harus belajar dari 41 kalimat
>    nyata. BERT membawa bobot terlatih untuk SETIAP lapisan, jadi tugas
>    hilirnya cuma perlu mempelajari langkah terakhir, dan itulah alasan ia
>    berhasil dengan ratusan contoh berlabel dan bukan ribuan.
>
> Yang keempat, layak disebut karena ia justru gagasan Bagian 3: **tokenisasi
> subkata (WordPiece)**. Itu versi industrinya dari n-gram karakter, dan ia
> menghapus kategori "di luar kosakata" sepenuhnya — masalah yang Bagian 2
> ukur sebagai 51,1 persen token dan dua kalimat bervektor nol.

<details>
<summary>Petunjuk 7c</summary>

Kalau baris ke-$i$ dari `E` bernilai nol, apakah gradiennya juga nol?
Perhatikan bahwa gradien untuk `E` datang dari `X.T @ out.grad`, dan `X`
kolom ke-$i$ nol untuk kata yang tidak pernah muncul.

</details>

---

## Soal 8 - Tuas mana yang sebenarnya menahan

Bagian 7 menarik tiga tuas dan melaporkan ketiganya.

**8a.** Salin ketiga tabel. Untuk tiap tuas, nyatakan apakah gerakannya lebih
besar atau lebih kecil daripada lebar selang, dan simpulkan.

> **Jawaban:** Ketiga tabel, disalin dari jalannya sendiri, lalu tiap gerakan
> diadu dengan lebar selangnya.
>
> **TUAS A - tambah kalimat nyata**
>
> ```
>   k nyata   n uji    rerata   terburuk   terbaik
>         0      41     48.8%      43.9%     53.7%
>         5      36     48.3%      44.4%     52.8%
>        10      31     49.0%      45.2%     54.8%
>        15      26     47.7%      38.5%     57.7%
>        20      21     44.8%      38.1%     52.4%
> ```
>
> Gerakan seluruh kolom rerata: 4,2 poin. Lebar selang di $k=0$ ($n=41$)
> sekitar 30 poin, dan di $k=20$ ($n=21$) melebar jadi
> $2(1{,}96)\sqrt{0{,}448\cdot 0{,}552/21}=42{,}5$ poin. **Gerakannya sepuluh
> kali lebih kecil daripada selangnya.** Kesimpulan: menambah sampai 20
> kalimat nyata tidak menggerakkan apa pun yang bisa diukur, dan
> kecenderungan menurun yang terlihat justru sesuai dengan himpunan uji yang
> mengecil, bukan dengan tuasnya.
>
> **TUAS B - naikkan porsinya**
>
> ```
>   k nyata  diulang  n latih   porsi    rerata   terbaik
>        20        1    10520    0.2%     44.4%     52.4%
>        20        5    10600    0.9%     49.2%     52.4%
>        20       15    10800    2.8%     50.8%     57.1%
>        20       40    11300    7.1%     49.2%     57.1%
> ```
>
> Gerakan 6,4 poin lawan selang sekitar 42 poin. Tidak terukur. **Tapi tabel
> ini tidak menjalankan percobaan yang soalnya klaim** — lihat 8b.
>
> **TUAS C - gabungkan kelasnya**
>
> ```
> tugas                           akurasi      selang 95 persen
> 15 intent                         43.9%          28.7 .. 59.1
> 2 kelas: alat atau LLM            78.0%          65.4 .. 90.7
> dasar mayoritas 2 kelas           85.4%          74.5 .. 96.2
> ```
>
> Ini satu-satunya tuas yang gerakannya lebih besar daripada lebar selang:
> 43,9 ke 78,0 adalah 34,1 poin, dan selang keduanya (`28,7 .. 59,1` lawan
> `65,4 .. 90,7`) **tidak bertumpang tindih**. Jadi gerakannya terukur.
>
> Dan justru itulah jebakannya. Baris ketiga menunjukkan bahwa dasar mayoritas
> tugas dua kelas adalah 85,4 persen, **di atas** model dua kelasnya sendiri
> (78,0), dan selang dasar mayoritas memuat titik modelnya. Menggabungkan
> kelas menghasilkan angka yang jauh lebih besar dan model yang lebih buruk
> daripada menebak buta. Kesimpulan Tuas C: penggabungan kelas bukan
> perbaikan, ia penipuan optik terhadap diri sendiri, dan satu-satunya yang
> menangkapnya adalah dasar mayoritas yang dihitung di Bagian 1.

**8b.** Tuas B menaikkan porsi kalimat nyata sampai lebih dari separuh data
latih tanpa mengubah hasil. Dugaan "kalimat nyata tenggelam di gradien"
karena itu gugur. Ajukan penjelasan pengganti, lalu rancang satu pengukuran
yang bisa memisahkannya dari penjelasan lain.

> **Jawaban, dan bagian pertamanya membantah premis soalnya.**
>
> Soal menyatakan "Tuas B menaikkan porsi kalimat nyata sampai lebih dari
> separuh data latih tanpa mengubah hasil". Terukur, sapuannya berhenti di
> **7,1 persen**, bukan lebih dari separuh. Sebabnya data sintetisnya sudah
> diganti dari 1.080 kalimat jadi 15.000, jadi `ulangi=40` yang dulu memberi
> 51,6 persen sekarang cuma memberi 7,1. **Percobaan yang dipakai soal untuk
> menggugurkan dugaan itu tidak pernah dijalankan pada data ini.**
>
> Jadi saya tarik sendiri tuasnya lebih jauh (Uji L):
>
> ```
>   k nyata  diulang  n latih   porsi    rerata   terbaik   detik
>        20       40    11300    7.1%     49.2%     57.1%      84
>        20      200    14500   27.6%     52.4%     57.1%     106
>        20      600    22500   53.3%     55.6%     57.1%     160
> ```
>
> Reratanya naik monoton: 49,2 ke 52,4 ke 55,6, total 6,4 poin waktu porsinya
> naik dari 7 ke 53 persen. Itu masih jauh lebih kecil daripada selang 42 poin
> di $n_{\text{uji}}=21$, jadi **tetap tidak terukur**. Tapi ia satu-satunya
> kecenderungan monoton di seluruh sesi ini, dan ia muncul persis di tuas yang
> soalnya nyatakan datar. Jadi dugaan "kalimat nyata tenggelam di gradien"
> **tidak gugur**. Ia belum diuji dengan benar, dan bukti awalnya condong ke
> arah yang berlawanan dari yang soalnya tulis.
>
> **Penjelasan pengganti yang tetap perlu diajukan**, karena kenaikan 6,4 poin
> dari pengulangan 30 kali lipat itu payah untuk ukuran tuas yang ditarik
> sekeras itu: ke-20 kalimat nyata tidak memuat informasi yang dibutuhkan,
> bukan kalah suara. Terukur, 51,1 persen token pesan nyata tidak punya kolom
> sama sekali. Mengulang sebuah kalimat yang kata-kata pentingnya tidak punya
> kolom bukan menambah sinyal; ia mengulang sinyal lemah yang sama enam ratus
> kali, dan penurunan gradien atas contoh yang diulang menuju pada menghafal
> contoh itu, bukan pada menyamaratakan darinya.
>
> **Pengukuran yang memisahkan kedua penjelasan:** laporkan akurasi LATIH pada
> ke-20 kalimat nyata yang diulang itu, berdampingan dengan akurasi ujinya.
>
> - Kalau akurasi latih mendekati 100 persen sementara uji tetap datar,
>   penjelasannya menghafal-tanpa-menyamaratakan, dan tuasnya memang sudah
>   ditarik habis.
> - Kalau akurasi latih JUGA rendah, model bahkan tidak bisa mencocokkan
>   kalimat itu, dan masalahnya ada di ruang fiturnya — yaitu 51,1 persen
>   token tanpa kolom. Itu menuding langsung ke n-gram karakter dari Soal 3c,
>   dan bukan ke jumlah data.
>
> Kedua hasil itu menunjuk ke pekerjaan yang berbeda, dan itulah gunanya
> pengukuran ini.

**8c.** Tuas C menemukan 6 dari 41 pesan nyata yang intent-nya punya alat.
Bagian 4 di [`../docs/Roadmap.md`](../docs/Roadmap.md) menyatakan 80 sampai 90
persen pemakaian harian bisa ditangani pengklasifikasi tanpa LLM. Nyatakan
apakah pengukuran ini membantah pernyataan itu, dan sebutkan dengan tepat
batas keberlakuan pengukuranmu.

> **Jawaban:** Terukur: 6 dari 41 pesan nyata punya intent yang punya alat,
> yaitu 14,6 persen. Bagian 4 `docs/Roadmap.md` menyatakan 80 sampai 90
> persen.
>
> **Apakah ini membantah pernyataan itu? Tidak, sebagaimana dinyatakan.** Dan
> kalimat berikutnya sama pentingnya: pernyataan itu juga tidak pernah punya
> dukungan sendiri.
>
> **Batas keberlakuan pengukuran saya, disebut dengan tepat:**
>
> 1. **Satu sumber.** Keempat puluh satu pesan berasal dari satu arsip
>    percakapan merancang proyek ini bersama agen pemrograman.
> 2. **Satu penulis, satu periode.** Tidak ada sampel dari waktu lain atau
>    suasana kerja lain.
> 3. **Laras yang salah.** Itu percakapan, bukan perintah. Roadmap bicara
>    tentang "pemakaian harian" SYNESIS, sebuah sistem yang belum ada waktu
>    ke-41 pesan itu ditulis. Kedua populasi tidak beririsan.
> 4. **Label dari saya sendiri, sesudah kejadian**, dengan segala bias yang
>    Soal 5d bahas untuk pasangan uji.
> 5. **Taksonomi yang menentukan "punya alat" ternyata bergerak.** Sesi 4 Soal
>    1a mengukur bahwa satu keputusan taksonomi memindahkan angkanya dari 6
>    jadi 5, tanpa satu baris kode berubah. Angka pembilangnya sendiri punya
>    ralat sebesar satu.
>
> **Yang tetap ditegakkan pengukuran ini, dan ini bukan hal kecil:** sebelum
> ini, klaim 80-90 persen berdiri tanpa satu pun pengukuran. Sekarang ada satu
> pengukuran, dari populasi bertetangga, yang keluar di 15 persen. Itu
> memindahkan beban pembuktian. Klaimnya sekarang menuntut bukti, dan ada satu
> cara nyata untuk mendapatkannya, yaitu `audit.jsonl`. Sampai itu ada,
> Bagian 4 Roadmap harus ditandai belum terdukung, bukan dibuang dan bukan
> dipercaya.

**8d.** 41 pesan itu semuanya dari satu arsip, yaitu percakapan merancang
proyek ini. Rancang cara mengumpulkan sampel yang mewakili pemakaian SYNESIS
sebenarnya. Sebutkan apa yang dicatat, kapan dicatatnya, dan bagaimana kamu
mencegah dirimu sendiri mengubah cara bicara karena tahu sedang dicatat.

> **Jawaban:** Alat pencatatnya sudah jadi di Sesi 4, yaitu `catat_audit` di
> [`../synesis/niat.py`](../synesis/niat.py). Yang belum, dan yang ditanyakan
> di sini, adalah protokolnya.
>
> **Apa yang dicatat.** Enam medan, dan yang keenam paling penting:
>
> 1. kalimat mentah, apa adanya, tanpa dibersihkan;
> 2. cap waktu UTC;
> 3. tiga intent teratas beserta peluangnya, bukan cuma yang menang, supaya
>    nanti bisa dihitung ulang dengan ambang berbeda tanpa mengulang sesinya;
> 4. keputusan yang diambil dan lapisan mana yang menghentikannya;
> 5. argumen kalau terbentuk;
> 6. **apa yang saya lakukan SESUDAHNYA** — mengetik ulang, mengerjakan
>    sendiri, atau menyerah. Itulah labelnya. Tanpa medan keenam, catatannya
>    berisi tebakan model dan tidak berisi kebenaran.
>
> **Kapan dicatat.** Pada saat pengetikan, otomatis, oleh pipanya sendiri.
> Bukan di sesi peninjauan sesudahnya, karena peninjauan sesudahnya adalah
> saya yang mengarang ulang apa yang saya katakan. `jalankan_pipa` sudah
> mencatat tiap keputusan termasuk yang ditolak, jadi bagian ini selesai
> secara teknis.
>
> **Mencegah diri sendiri berubah cara bicara.** Efeknya punya nama —
> efek Hawthorne di ilmu sosial, gangguan alat ukur terhadap keadaan yang
> diukurnya di fisika. Empat langkah, diurut dari yang paling berpengaruh:
>
> 1. **Buat SYNESIS jadi jalur yang paling sedikit hambatannya, bukan
>    program terpisah yang harus saya ingat.** Kalau saya harus ingat untuk
>    memakainya, sampelnya jadi "saat-saat saya ingat", dan itu sampel bias
>    yang paling parah dari keempatnya, karena ia menyaring berdasarkan
>    suasana hati dan jenis tugas sekaligus.
> 2. **Sembunyikan alat ukurnya waktu dipakai.** Tidak ada pencacah di
>    prompt, tidak ada pesan "tercatat", tidak ada berkas yang terlihat
>    membesar. Jumlah baris cuma keluar kalau saya minta lewat perintah
>    tersendiri, dan saya cuma memeriksanya di jadwal tetap, misalnya sekali
>    seminggu.
> 3. **Jangan membaca berkasnya selama pengumpulan.** Tetapkan tanggal, jangan
>    dibuka sebelum itu. Membacanya di tengah jalan mengubah saya jadi penyunting
>    sampel saya sendiri, dan itu persis bias yang saya sebut di Soal 5d untuk
>    pasangan uji.
> 4. **Kumpulkan pembanding yang tidak bisa saya pengaruhi**, supaya efeknya
>    bisa DIUKUR alih-alih diandaikan hilang. Dua sudah ada dan keduanya
>    ditulis sebelum alat ukurnya ada: riwayat shell saya, dan ke-41 pesan
>    arsip ini. Bandingkan panjang kalimat, laju kata di luar kosakata, dan
>    porsi kalimat berbentuk perintah. Kalau catatan audit lebih pendek, lebih
>    rapi, dan lebih menyerupai perintah daripada pembandingnya, selisih itu
>    adalah besar efeknya.
>
> Langkah 4 yang membuat ketiga langkah lain jujur: tanpanya, saya cuma
> berharap efeknya kecil.

**8e.** Putuskan apa yang dikerjakan sesudah sesi ini, dan urutkan tiga
kandidat berikut dengan alasan berbasis angka: menambah data nyata,
mengganti representasi, mengubah taksonomi intent. Boleh menambah kandidat
keempat.

> **Jawaban:** Urutannya, dengan alasan dari angka, ditambah kandidat keempat
> yang menempati peringkat dua.
>
> **1. Mengumpulkan catatan pemakaian yang mewakili.**
> Bukan "menambah data nyata ke data latih" — Tuas A sudah menguji itu dan
> hasilnya datar (48,8 ke 44,8 lawan selang 42 poin). Bedanya penting: Tuas A
> menambah 20 kalimat dari arsip yang populasinya salah. Yang kurang 400
> sampai 500 kalimat dari populasi yang BENAR. Angka yang membenarkan: dari
> Soal 1b, sebelum perbaikan 10 poin bisa dibedakan dari nol saya butuh 115
> sampai 233 kalimat uji. Sekarang saya punya 41, dan semuanya dari satu
> arsip. Setiap selang di seluruh sesi ini selebar 30 poin, dan itu akibat
> langsung dari $n=41$. Tidak ada tuas lain yang bisa dinilai sampai ini ada.
>
> **2. Membangun penerjemah frasa manusia jadi pola nama berkas.**
> Kandidat keempat, dan ia naik ke peringkat dua karena angkanya paling
> tegas. Dari Sesi 4: 21 dari 41 pesan berhenti di `belum_ada_alat`, cuma 1
> yang sampai memanggil alat, dan kalimat sasaran Bulan 2 (`buka laporan
> praktikum minggu lalu`) melewati pengklasifikasi, ambang, argumen, dan
> pemanggilan alat, lalu gagal persis di satu langkah yang belum ada. Ini
> satu-satunya tempat di seluruh Bulan 2 di mana pekerjaan yang jumlahnya
> tetap mengubah kegagalan terukur jadi keberhasilan terukur, dan ia tidak
> butuh data tambahan sama sekali.
>
> **3. Mengubah taksonomi intent.**
> Tuas C sudah menunjukkan penggabungan kelas menghasilkan angka lebih besar
> (78,0) dan model lebih buruk daripada dasar mayoritasnya (85,4). Jadi
> perubahan taksonomi demi akurasi ditolak berdasarkan angka. **Tapi** ada
> perubahan taksonomi yang layak, yaitu yang diminta Sesi 4 Soal 1c: memecah
> ketiga intent yang bermuara ke `jalankan` jadi intent-intent beralat sempit.
> Itu perubahan keselamatan, dinilai dengan ongkos, bukan dengan 43,9 persen.
>
> **4. Mengganti representasi.**
> Terakhir, dan setiap angka di sesi ini mengatakan begitu. Lima resep fitur
> merentang 7,3 poin lawan selang 30 poin (Soal 3a). Prapelatihan PPMI-SVD
> menggeser 2,4 poin, yaitu satu kalimat (Soal 7b). Vektor katanya sendiri
> jelas bagus — median peringkat 3 dari 1.200 lawan acak 600 — dan itu justru
> yang membuat hasil hilirnya berarti: **representasi yang terbukti bagus
> tetap tidak menggerakkan akurasi hilir**, jadi hambatannya memang bukan di
> situ.
>
> Satu pengecualian yang saya bawa dari Soal 3c: pindah ke n-gram 3-5 tetap
> layak dikerjakan bersamaan dengan butir 1, bukan demi akurasi melainkan
> demi menghapus kelas kegagalan vektor nol yang terukur pasti di 2 dari 41.

<details>
<summary>Petunjuk 8d</summary>

Efek yang kamu cegah di kalimat terakhir punya nama di ilmu sosial dan di
fisika sekaligus. Di ilmu sosial namanya efek Hawthorne. Di fisika, itu
persoalan alat ukur yang mengganggu keadaan yang diukurnya.

</details>

---

## Tolok Ukur Bulan 2 Sesi 3

- [x] Selang binomial ditulis sendiri, dan dipakai di tiap tabel akurasi
- [x] Dasar mayoritas dihitung sebelum model dinilai bagus atau jelek
- [x] Kosinus ditulis sendiri, dan kaitannya dengan hasil kali dalam dinyatakan
- [x] Kebutaan sinonim dibuktikan dengan angka nol, bukan disebut saja
- [x] Kelas kalimat bervektor nol diturunkan di atas kertas sebelum dijalankan
- [x] N-gram karakter ditulis sendiri, lengkap dengan penanda batas kata
- [x] Sapuan panjang potongan dilaporkan seluruhnya, bukan cuma baris terbaik
- [x] Matriks ko-okurensi ditulis sendiri, dan sifat diagonalnya dijelaskan
- [x] PPMI diturunkan dari definisi kebebasan, bukan disalin rumusnya
- [x] Tetangga terdekat dinilai dengan peringkat, bukan dengan kesan
- [x] Bias penyusunan pasangan uji dinyatakan dan dicarikan gantinya
- [x] Kurva ukuran korpus dibaca, dan kesimpulan "masih lapar" atau tidak diambil
- [x] Lapisan embedding ditulis sebagai perkalian matriks, tanpa operasi Tensor baru
- [x] Nasib kata bervektor nol diturunkan dari aturan turunan `__matmul__`
- [x] Ketiga tuas Bagian 7 dibandingkan dengan lebar selang, satu per satu
- [x] Pernyataan 80 sampai 90 persen di Roadmap diuji dengan angka, dan batasnya disebut

Kalau keenam belas kotak beres, kamu punya sesuatu yang lebih berguna daripada
akurasi yang lebih tinggi: kamu tahu tuas mana yang tidak perlu ditarik lagi.

---

## Catatan jalannya

Kedelapan TODO di [`bulan2_sesi3_embedding.py`](bulan2_sesi3_embedding.py)
terisi, dan berkasnya jalan sampai selesai dalam 1.599 detik. Angka yang
dipakai jawaban di atas keluar dari dua tempat:

```
python notebooks\bulan2_sesi3_embedding.py     tabel tiap Bagian
python notebooks\kunci_b2s34_bukti.py          Uji A sampai Uji L
```

**Satu hal yang harus dibaca sebelum membandingkan angka di atas dengan
tabel yang tercetak di dalam soal ini.** Tabel di soal dihitung waktu
`data/bulan2/perintah_train_generated.txt` masih 1.080 kalimat dengan
kosakata 353 kolom. Berkas itu sudah diganti jadi 15.000 kalimat, kosakata
402 kolom, dan `data/bulan2/README.md` mencatat pergantiannya. Akibatnya:

| yang bergeser | di soal | terukur sekarang |
|---|---|---|
| kosakata sintetis | 353 | 402 |
| token pesan nyata di luar kosakata | 55,2% | 51,1% |
| kalimat bervektor nol | 3 | 2 |
| rentang sapuan n-gram | 14,6 poin | 7,3 poin |
| baris n-gram terbaik | 3-5 | 3-4 |
| porsi maksimum Tuas B | 51,6% | 7,1% |
| Tuas C, 2 kelas | 85,4% | 78,0% |

Bagian 1 tidak bergeser sama sekali (41 pesan, 39,0 persen, 56,1 persen,
selang `40,9 .. 71,3`), karena ia tidak menyentuh data latih.

Dua tempat yang jawabannya membantah soalnya, dan keduanya ditulis apa
adanya di tempatnya: Soal 2b (dua kalimat bervektor nol, bukan tiga) dan
Soal 8b (Tuas B tidak pernah ditarik sampai lebih dari separuh, jadi dugaan
yang soalnya nyatakan gugur sebenarnya belum diuji; ditarik sendiri sampai
53,3 persen di Uji L, dan hasilnya naik monoton).

Satu ramalan saya sendiri yang meleset, di Soal 4c: saya meramalkan jendela
2 lebih baik daripada jendela 5. Terukur, keduanya seri di median peringkat
6. Yang benar cuma separuh ramalan itu, yaitu bahwa jendela 15 lebih buruk.
