# Soal Bulan 3 Sesi 4 - keyword spotter, lalu wake word

Berkas latihan: [`bulan3_sesi4_wakeword.py`](bulan3_sesi4_wakeword.py)

Tiga TODO. Sesi ini yang pertama kali di seluruh kurikulum ini punya himpunan
uji yang cukup besar untuk membaca selisih dua poin sebagai selisih dua poin.

> Prasyarat: Sesi 2 (`fitur_audio`) dan Sesi 3 (arsitektur CNN, pooling
> asimetris, augmentasi geseran waktu). Data:
> `python scripts\unduh_speech_commands.py`, sekitar 40 menit sekali saja.

> Waktu jalan di mesin pemilik sesudah cache fitur ada: 601 detik. Yang
> pertama kali menambahkan 54 detik untuk menghitung fiturnya.

---

## Soal 1 - Belahan menurut pembicara

Bagian 1 memberi:

```text
belahan       berkas    persen
latih         34.126     80.2%
valid          4.054      9.5%
uji            4.366     10.3%

pembicara berbeda            : 2.510
pembicara di lebih dari satu : 0
```

**1a.** `belahan` men-hash bagian nama berkas SEBELUM `_nohash_`. Jelaskan
apa yang akan terjadi kalau ia men-hash seluruh nama berkasnya, dan
perkirakan besarnya dalam poin akurasi.

> **Jawaban:** Nama lengkapnya `<pembicara>_nohash_<n>.wav`, jadi men-hash
> seluruh nama berarti tiap REKAMAN diputuskan sendiri-sendiri. Satu
> pembicara di Speech Commands biasanya menyumbang beberapa rekaman untuk
> kata yang sama, jadi rekamannya akan tersebar ke latih, valid, dan uji
> sekaligus.
>
> Model lalu bisa mengenali kata dengan mengenali SUARANYA: ia sudah pernah
> mendengar orang yang sama mengucapkan kata yang sama, hanya di percobaan
> yang berbeda. Itu bukan kemampuan yang berguna, dan tidak ada satu pun
> tanda di layar bahwa itu yang terjadi.
>
> Besarnya: literatur Speech Commands melaporkan selisih 2 sampai 5 poin
> antara belahan acak dan belahan menurut pembicara untuk model sekelas ini.
> Dengan akurasi 95,49 persen yang terukur, belahan acak diperkirakan
> mendarat di sekitar 97 sampai 98 persen, dan angka itu palsu.
>
> Yang membuat kesalahan ini jahat: ia menaikkan angka. Bug yang menurunkan
> angka akan kamu cari sampai ketemu; bug yang menaikkannya akan kamu
> laporkan.

**1b.** Kenapa hash, bukan pengacak dengan seed?

> **Jawaban:** Karena hash memberi keputusan yang TETAP per pembicara,
> terlepas dari berapa berkas yang ada di folder itu. Pengacak dengan seed
> memberi keputusan yang tetap terhadap URUTAN, dan urutannya berubah begitu
> satu berkas ditambah, dihapus, atau di-glob dengan pola berbeda.
>
> Ini menggigit di sesi ini secara langsung: `ASING_MAKS = 400` memotong
> daftar kata asing. Menaikkannya jadi 500 akan mengubah seluruh belahan
> kalau pengacak yang dipakai, sehingga angka lama dan angka baru tidak bisa
> dibandingkan. Dengan hash, 100 berkas tambahan itu jatuh ke belahan
> masing-masing tanpa menggeser satu pun yang lama.

**1c.** Kelas `_sunyi_` dibuat dari derau latar dan belahannya diacak, bukan
di-hash. Apakah itu melanggar aturan yang sama?

> **Jawaban:** Tidak, karena tidak ada pembicara di sana. Yang dijaga aturan
> hash adalah kebocoran IDENTITAS, dan potongan derau ruangan tidak punya
> identitas untuk bocor.
>
> Yang bocor di kelas sunyi adalah hal lain: enam berkas derau latar itu
> dipotong acak, jadi potongan di latih dan potongan di uji bisa berasal dari
> berkas yang sama, bahkan bisa tumpang tindih. Model bisa menghafal derau
> spesifik itu.
>
> Akibatnya kecil karena kelas sunyi bukan yang sulit, dan pengendalinya ada
> di Bagian 6: penyalaan palsu diukur pada derau latar dengan cara yang
> berbeda sama sekali, yaitu jendela geser sepanjang 6,7 menit penuh. Kalau
> model cuma menghafal, angka di Bagian 6 akan buruk.

---

## Soal 2 - Cache fitur, dan apa yang dikorbankannya

Bagian 2 memberi:

```text
waktu fitur per berkas      : 1.20 ms
berkas                      : 44.946
sekali hitung               : 54 detik
dihitung ulang tiap epoch   : 648 detik untuk 12 epoch
X (44946, 98, 40) float16  = 352 MB di memori
```

**2a.** float16 dipakai. Hitung galat kuantisasinya untuk nilai log-mel, dan
tunjukkan bahwa ia di bawah selisih yang berarti.

> **Jawaban:** float16 punya 10 bit mantisa, jadi galat relatifnya sekitar
> $2^{-11} = 4{,}9\times10^{-4}$. Nilai log-mel setelah normalisasi berkisar
> $\pm 40$ dB, jadi galat mutlaknya di orde $40 \times 4{,}9\times10^{-4}
> \approx 0{,}02$ dB.
>
> Bandingkan dengan sebaran datanya: simpangan baku antarucapan terukur
> sekitar 20 dB di Sesi 3. Galat kuantisasinya seperseribu dari itu.
>
> Yang perlu ikut diperiksa dan sering dilupakan: float16 juga punya batas
> jangkauan, sekitar $\pm 65.504$. Nilai log-mel tidak mendekatinya. Kalau
> yang disimpan spektrum daya LINEAR, bukan log, cerita ini berbeda
> sepenuhnya: daya bisa menjangkau belasan orde besaran, dan float16 akan
> membuat sebagian di antaranya jadi nol.

**2b.** Cache membuat augmentasi derau jadi tidak mungkin. Hitung ongkos
mengerjakannya tanpa cache, lalu putuskan.

> **Jawaban:** Tanpa cache, tiap epoch harus membaca 44.946 WAV, menambahkan
> derau, lalu menghitung fiturnya. Fiturnya saja 54 detik per epoch; membaca
> WAV-nya menambah lagi, terukur sekitar 4 ms per berkas pada jalan pertama
> ketika cache dingin, jadi kira-kira 180 detik per epoch.
>
> Dua belas epoch memberi $12 \times 180 = 2.160$ detik, yaitu 36 menit,
> untuk SATU baris tabel. Bagian 3 dan 4 punya lima baris, jadi tiga jam.
>
> Keputusannya: jangan. Yang dikerjakan sebagai gantinya, dan yang memang
> dikerjakan Bagian 5: augmentasi derau di ranah waktu hanya untuk data wake
> word yang jumlahnya 8.400, bukan 44.946. Di situ ongkosnya 34 detik per
> epoch dan sepadan.
>
> Jalan tengah yang tidak diambil dan patut dicatat: menyimpan cache dalam
> beberapa versi, misalnya lima salinan dengan derau berbeda, lalu memilih
> acak tiap epoch. Ongkosnya 5 kali 352 MB = 1,7 GB disk dan 4,5 menit
> sekali. Itu sebenarnya pilihan yang paling masuk akal, dan alasan ia tidak
> diambil cuma satu: augmentasi geseran waktu ternyata sudah cukup untuk
> menjawab pertanyaan Bagian 4.

---

## Soal 3 - Hipotesis Sesi 2, dan jawabannya

Bagian 3 memberi:

```text
dasar mayoritas uji : 9.25%
ucapan uji          : 4.594
lebar selang 95%    : 1.74 poin

fitur           dimensi   parameter   detik   akurasi uji
log-mel 40           40      49.884     109        95.52%
MFCC 13              13      44.508      76        94.21%
MFCC 40              40      49.884     115        94.17%
```

Jalan kedua dengan seed, data, dan kode yang sama persis memberi 95,49 /
94,32 / 94,14. Selisih antarjalan sampai 0,11 poin, dan itu bukan bug: kernel
cuDNN memakai penjumlahan atomik yang urutannya tidak dijamin, jadi latihan
di GPU tidak sepenuhnya dapat diulang meskipun seed-nya dipatok. Angka itu
perlu diingat sebagai lantai derau pengukuran.

**3a.** Tuliskan kesimpulan yang keluar dari angka itu, apa pun angkanya.

> **Jawaban:** Hipotesis Soal 6b Sesi 2 berbunyi: untuk CNN, log-mel
> mengalahkan MFCC, dan selisihnya melampaui selang 1,74 poin.
>
> Terukur, log-mel menang atas keduanya. Selisih terhadap MFCC 13 adalah
> 1,31 poin dan terhadap MFCC 40 adalah 1,35 poin. Keduanya DI DALAM selang
> 1,74 poin.
>
> Kesimpulannya, dan ini yang harus ditulis apa adanya: arah ramalannya
> benar, besarnya tidak terbukti. Log-mel memang di atas keduanya di ketiga
> pengukuran, dan konsistensi arah itu bukan nol informasi, tetapi satu
> pengukuran tunggal dengan selang 1,74 poin tidak bisa menyatakan bahwa
> selisih 1,35 poin nyata.
>
> Yang perlu dikerjakan untuk memutuskan, dan yang tidak dikerjakan di sini
> karena ongkosnya: ulangi ketiganya dengan lima seed berbeda dan bandingkan
> mediannya, atau pakai uji McNemar berpasangan yang jauh lebih murah karena
> ketiga model diuji di ucapan yang sama. Soal 1b Bulan 2 Sesi 3 sudah
> menurunkan rumusnya.

**3b.** Baris MFCC 40 adalah pengendali. Apa yang dipisahkannya, dan apa
kesimpulan yang bisa ditarik dari posisinya?

> **Jawaban:** Ia memisahkan dua penjelasan yang berbeda untuk kemenangan
> log-mel: apakah yang berperan JUMLAH DIMENSI, atau STRUKTUR LOKAL di sumbu
> frekuensi.
>
> Kalau yang berperan jumlah dimensi, MFCC 40 seharusnya menyusul log-mel 40,
> karena keduanya 40 dimensi dan jumlah parameternya identik (49.884, sama
> persis). Terukur MFCC 40 justru sedikit DI BAWAH MFCC 13, dan 1,35 poin di
> bawah log-mel. Kedua jalan memberi urutan yang sama.
>
> Jadi arah bukti menunjuk ke struktur, bukan ke dimensi, dan itu konsisten
> dengan mekanisme yang diusulkan di Sesi 2: DCT mengaduk sumbu frekuensi,
> sehingga kernel 3x3 menyapu tetangga yang tidak lagi bertetangga.
>
> Sekali lagi, ini arah bukti dan bukan bukti. Selisih MFCC 40 dan MFCC 13
> adalah 0,04 poin, dan itu bahkan di bawah selisih antarjalan yang 0,11
> poin. Dua baris itu tidak bisa dibedakan sama sekali.

**3c.** Dasar mayoritasnya 9,25 persen. Kenapa serendah itu, dan apa yang
akan berubah kalau kelas `_asing_` dinaikkan porsinya?

> **Jawaban:** Dua belas kelas yang hampir seimbang memberi dasar mayoritas
> mendekati $1/12 = 8{,}3$ persen. Terukur 9,25 persen karena `yes` sedikit
> lebih banyak daripada yang lain.
>
> Kalau `ASING_MAKS` dinaikkan dari 400 jadi 4.000, kelas `_asing_` akan
> memuat sekitar 38.000 ucapan, yaitu separuh seluruh data. Dasar
> mayoritasnya melompat ke sekitar 50 persen, dan setiap angka akurasi di
> tabel jadi tidak bisa dibandingkan dengan yang sekarang.
>
> Yang lebih penting: model akan mempelajari bahwa menjawab `_asing_` hampir
> selalu benar, dan akurasi keseluruhan bisa naik sementara kemampuan
> membedakan sepuluh kata intinya turun. Ukuran yang tidak tertipu adalah
> akurasi per kelas, atau matriks kebingungan. Akurasi tunggal untuk data
> yang timpang adalah angka yang menyesatkan, dan itu pelajaran yang sama
> dengan Tuas C di Bulan 2 Sesi 3, tempat menggabungkan lima belas intent
> jadi dua kelas memberi 85,4 persen yang persis sama dengan dasar
> mayoritasnya.

---

## Soal 4 - Augmentasi, dan himpunan uji yang buta

Bagian 4 memberi:

```text
model                        uji sejajar   uji digeser    jatuh
tanpa augmentasi                  95.28%        92.77%    2.50
geseran waktu +-100 ms            95.52%        93.84%    1.68
```

**4a.** Kalau kamu cuma membaca kolom pertama, kesimpulan apa yang kamu
ambil, dan kenapa kesimpulan itu salah?

> **Jawaban:** Kolom pertama memberi 95,28 lawan 95,52, selisih 0,24 poin,
> jauh di dalam selang 1,74 poin dan cuma dua kali selisih antarjalan.
> Kesimpulan yang diambil: augmentasi geseran waktu tidak berguna, buang saja.
>
> Kesimpulan itu salah karena himpunan uji resminya BERBAGI CACAT dengan data
> latihnya. Keduanya berisi kliping satu detik dengan kata di tengah, jadi
> model yang mempelajari "kata ada di tengah" sebagai ciri akan tetap benar
> di himpunan uji itu. Himpunan ujinya buta terhadap masalah yang justru
> paling penting.
>
> Kolom kedua menghapus kebutaan itu dengan menggeser ucapan ujinya sampai
> 250 milidetik, dan di situ selisihnya jadi 1,07 poin dengan arah yang
> jelas. Kolom `jatuh` lebih tajam lagi: 2,50 lawan 1,68, artinya augmentasi
> memotong kerapuhannya sepertiga. Kedua jalan memberi arah yang sama, dan
> jalan sebelumnya memberi 2,83 lawan 1,57.
>
> Pelajarannya bisa dinyatakan tanpa menyebut audio sama sekali: himpunan uji
> yang benar secara prosedur, yaitu terpisah dari data latih dan tidak
> pernah dipakai memilih apa pun, tetap bisa salah secara isi.

**4b.** Ramalan Bagian 6 Sesi 3 adalah rasio 0,406 di sumbu waktu menandakan
posisi membawa informasi. Apakah Bagian 4 membuktikannya?

> **Jawaban:** Mendukung, tidak membuktikan. Yang ditunjukkan Bagian 4:
> model yang dilatih tanpa augmentasi lebih rapuh terhadap geseran daripada
> yang dilatih dengan augmentasi. Itu konsisten dengan "model memungut posisi
> sebagai ciri", tetapi juga konsisten dengan penjelasan yang lebih lemah:
> augmentasi menambah keragaman apa pun, dan keragaman selalu membantu
> ketahanan.
>
> Yang memisahkan keduanya: latih dengan augmentasi yang TIDAK berkaitan
> dengan geseran, misalnya penambahan derau, lalu ukur kejatuhan yang sama.
> Kalau ia juga turun banyak, yang bekerja keragaman umum. Kalau tidak,
> barulah klaim tentang posisi punya dukungan.
>
> Percobaan itu belum dijalankan, dan itu sebabnya kalimat di notebook
> memakai kata "menandakan", bukan "membuktikan".

**4c.** Geseran dikerjakan di ranah bingkai dengan `np.roll`, bukan di ranah
waktu. Sebutkan bedanya, dan kapan bedanya menggigit.

> **Jawaban:** Di ranah waktu, menggeser sinyal lalu menghitung fiturnya
> menghasilkan bingkai yang jatuh di posisi cuplikan yang berbeda, jadi isi
> tiap bingkai benar-benar berubah. Di ranah bingkai, yang digeser
> bingkainya yang sudah jadi, jadi isinya identik dan cuma urutannya bergeser.
>
> Geseran di ranah bingkai kelipatan 10 milidetik, dan tidak bisa lebih halus.
> Geseran di ranah waktu bisa satu cuplikan, yaitu 0,0625 milidetik.
>
> Menggigit ketika yang mau diuji ketahanan terhadap geseran SUB-BINGKAI,
> yaitu kurang dari 10 milidetik. Untuk wake word itu tidak penting: yang
> menentukan apakah kata mendarat di awal atau di tengah jendela, dan itu
> ratusan milidetik. Ia jadi penting untuk pengenalan fonem yang perlu
> penyejajaran halus.
>
> Ada beda kedua yang lebih halus dan lebih berbahaya: `np.roll` melingkar,
> jadi bingkai yang keluar di kanan masuk lagi di kiri. Notebook menambalnya
> dengan mengulang bingkai tepi, dan tanpa tambalan itu, ekor kata bisa
> muncul di awal potongan. Kesalahannya persis konvolusi melingkar dari
> Soal 2b Sesi 1, muncul lagi di tempat yang sama sekali berbeda.

---

## Soal 5 - Ambang, dari ongkos

Bagian 5 memberi:

```text
positif 400   negatif 8000   latih 6788  valid 761  uji 851
akurasi uji 98.82%   AUC 0.9907

   ambang   FAR (persen)   FRR (persen)   salah/jam*
    0.500          0.364          25.93          131
    0.900          0.000          44.44            0
    0.950          0.000          51.85            0
    0.990          0.000          70.37            0
    0.999          0.000          92.59            0

EER 3,91 persen di ambang 0,005
ambang dari ongkos 100 banding 1 : 0,738
```

**5a.** Pilih satu ambang untuk dipakai SYNESIS, lalu tuliskan ongkos yang
kamu asumsikan.

> **Jawaban:** Asumsi ongkos, dinyatakan terang-terangan:
>
> ```text
> salah menolak  ulangi "hey synesis" sekali            ongkos 1
> salah menerima SYNESIS menyala, merekam, dan melempar
>                apa pun yang terdengar ke pipa niat     ongkos 100
> ```
>
> Ongkos tiap baris tabel:
>
> ```text
> ambang 0,500   100 x 0,00364 + 0,2593 = 0,623
> ambang 0,738   100 x 0,00000 + 0,4074 = 0,407   <- minimum
> ambang 0,900   100 x 0,00000 + 0,4444 = 0,444
> ambang 0,999   100 x 0,00000 + 0,9259 = 0,926
> ```
>
> Yang menang 0,738, dan letaknya masuk akal: ia ambang TERENDAH yang sudah
> membuat FAR nol. Sekali FAR menyentuh nol, menaikkan ambang lebih jauh cuma
> menambah FRR tanpa membeli apa pun. Itu bentuk umum yang layak diingat:
> dengan ongkos yang sangat tak simetris, jawabannya selalu ambang terendah
> yang sudah menutup kesalahan mahalnya.
>
> Keberatan atas jawaban saya sendiri, dan ini yang paling penting:
> FAR = 0,000 artinya nol dari 824 ucapan negatif di himpunan uji, dan nol
> dari 824 bukan berarti nol. Aturan tiga memberi batas atas 95 persen
> sebesar $3/824 = 0{,}36$ persen. Pada 36.000 keputusan per jam, batas atas
> itu berarti 131 penyalaan palsu per jam, yaitu persis angka yang tercetak
> di baris 0,500.
>
> Jadi tabel ini TIDAK bisa menjamin bahwa SYNESIS aman dibiarkan menyala.
> Yang bisa menjawabnya cuma Bagian 6, karena ia mengukur pada bahan yang
> berbeda: derau ruangan tanpa satu pun kata.

**5b.** EER-nya 3,73 persen di ambang 0,005. Kenapa ambang itu begitu rendah,
dan apa artinya untuk kalibrasi model?

> **Jawaban:** Ambang EER serendah 0,005 berarti sebaran skor kelas negatif
> menumpuk sangat rapat di dekat nol, sedangkan kelas positif tersebar. Untuk
> menyamakan FAR dan FRR, ambangnya harus diturunkan sampai hampir menyentuh
> nol.
>
> Artinya modelnya YAKIN pada kelas negatif dan RAGU pada kelas positif, dan
> itu akibat langsung dari ketidakseimbangan 400 lawan 8.000: entropi silang
> tanpa pembobotan menghargai model yang berani menjawab "bukan".
>
> Akibatnya untuk kalibrasi: nilai softmax di sini bukan peluang. Skor 0,417
> tidak berarti "41,7 persen yakin". Ia cuma bilangan yang urutannya berarti,
> dan itulah kenapa ambangnya dipilih dari kurva ROC yang hanya bergantung
> pada urutan, bukan dari nilai mutlaknya.
>
> `synesis/suara.py` menambal sebabnya di tempat berbeda: `latih_wake`
> memakai `CrossEntropyLoss(weight=[1, n_neg/n_pos])`, jadi model wake word
> yang dilatih dari suaramu sendiri tidak menumpuk di ujung yang sama.

**5c.** `marvin` dipakai sebagai pengganti wake word. Sebutkan apa yang
hilang dari penggantian itu.

> **Jawaban:** Yang hilang paling besar: jumlah pembicara. `marvin` di
> Speech Commands diucapkan ratusan orang, jadi model harus belajar mengenali
> KATANYA. Wake word yang sesungguhnya diucapkan satu orang, jadi model boleh
> belajar mengenali kata DAN suaranya sekaligus, dan itu justru diinginkan:
> SYNESIS memang tidak perlu bangun untuk orang lain.
>
> Arah selisihnya bisa ditebak dan patut ditulis sebagai ramalan: model dari
> satu pembicara akan punya FRR lebih rendah untuk pemiliknya dan FAR jauh
> lebih rendah untuk orang lain, dengan data yang jauh lebih sedikit.
>
> Yang hilang kedua: `marvin` satu kata dua suku, sedangkan "hey synesis"
> empat suku dan hampir satu detik. Kata yang lebih panjang lebih mudah
> dibedakan dari kata lain, tetapi lebih mudah terpotong oleh jendela satu
> detik. `WAKE_LONCAT_MS` dan panjang jendelanya mungkin perlu disetel ulang
> sesudah rekaman aslinya ada.
>
> Yang TIDAK hilang: seluruh pipanya. Itulah gunanya pengganti, dan itulah
> sebabnya angka di Bagian 5 dan 6 tetap berarti sebagai pembuktian bahwa
> pipanya bekerja, meskipun tidak bisa dipindahkan begitu saja ke wake word
> yang sebenarnya.

---

## Soal 6 - Deteksi mengalir, dan latensi yang titik acuannya salah

Bagian 6 memberi:

```text
derau latar : 6.7 menit
   ambang   penyalaan    per jam
    0.500           0        0.0
    0.900           0        0.0
    0.990           0        0.0
    0.999           0        0.0

terdeteksi              : 19 dari 27
latensi median          : -190 ms
latensi persentil ke-90 : +32 ms
waktu satu jendela      : 3.1 ms
beban prosesor          : 3.1%
```

**6a.** Versi pertama bagian ini mengukur latensi terhadap detik ke-3, yaitu
ujung potongan satu detiknya, dan memberi median $-300$ milidetik. Jelaskan
kenapa angka itu tidak berarti apa-apa.

> **Jawaban:** Speech Commands memberi kliping tepat satu detik dengan
> katanya kira-kira di tengah. Kata `marvin` sendiri berdurasi sekitar 0,5
> detik, jadi 250 milidetik pertama dan 250 milidetik terakhir kliping itu
> kesunyian.
>
> Mengukur latensi terhadap detik ke-3 berarti mengukur terhadap akhir
> KESUNYIAN, bukan akhir kata. Angka $-300$ milidetik itu cuma melaporkan
> bahwa ada 300 milidetik sunyi di ekor kliping, dan tidak mengatakan apa pun
> tentang model.
>
> Titik acuan yang benar adalah akhir tenaga katanya, dan itu bisa dihitung
> dari kliping itu sendiri: cari bingkai terakhir yang tenaganya masih di
> dalam 25 dB dari puncaknya. Sesudah diperbaiki, mediannya $-190$
> milidetik.
>
> Pelajarannya bukan tentang audio: sebuah pengukuran bisa presisi, dapat
> diulang, dan sepenuhnya salah karena titik acuannya salah. Yang menangkap
> kesalahan ini bukan uji apa pun melainkan satu tanda minus yang tidak masuk
> akal, dan tanda minus itu hampir lolos karena angkanya kelihatan wajar.

**6b.** Sesudah diperbaiki, mediannya masih negatif. Apakah itu masih salah?

> **Jawaban:** Tidak. Negatif berarti model melewati ambang SEBELUM kata
> selesai, dan itu memang bisa terjadi: jendela satu detik yang sudah memuat
> sebagian besar kata sudah cukup, dan model tidak wajib menunggu suku kata
> terakhir.
>
> Yang tidak mungkin adalah mendeteksi sebelum katanya MULAI, yaitu latensi
> di bawah $-500$ milidetik untuk kata 0,5 detik. Persentil ke-90 di
> $+32$ milidetik menunjukkan sebaran yang wajar: sebagian besar deteksi
> mendarat di sekitar akhir kata, sebagian sedikit lebih awal.
>
> Untuk wake word, mendeteksi lebih awal adalah keuntungan langsung: SYNESIS
> bisa mulai merekam perintahnya sebelum penuturnya selesai mengucapkan nama
> panggilannya. `synesis/suara.py` justru mengandalkan itu lewat pra-gulung
> 300 milidetik.

**6c.** Deteksinya cuma 19 dari 27, sedangkan versi dengan ambang EER
mendapat 25 dari 27. Apakah ambangnya salah?

> **Jawaban:** Tidak, dan pertukarannya persis yang diminta. Ambang 0,738
> dipilih untuk meminimalkan ongkos dengan salah menerima 100 kali lebih
> mahal, dan harga yang dibayar adalah FRR 40,7 persen di tabel Bagian 5 dan
> 8 dari 27 kegagalan di sini.
>
> Angka 19 dari 27 memang terasa buruk, dan dua hal menahannya dari jadi
> alasan menurunkan ambang:
>
> 1. Yang gagal itu `marvin` dari 27 pembicara yang berbeda-beda, sedangkan
>    wake word yang sesungguhnya cuma perlu bekerja untuk satu orang. Soal 5c
>    sudah menyebut kenapa FRR pengganti tidak bisa dipindahkan.
> 2. Salah menolak bisa diperbaiki penuturnya dalam satu detik dengan
>    mengulang. Salah menerima tidak bisa diperbaiki siapa pun.
>
> Yang benar dikerjakan sesudah rekaman aslinya ada: ukur ulang, dan kalau
> FRR-nya masih di atas 20 persen untuk suaramu sendiri, rekam lebih banyak
> contoh sebelum menurunkan ambang. Menambah data memperbaiki keduanya;
> menurunkan ambang menukar satu dengan yang lain.

**6d.** Hitung pertukaran antara panjang jendela, penghalusan, dan latensi.

> **Jawaban:** Dua sumbangan tetap:
>
> ```text
> jendela 1 detik      keputusan pertama baru ada sesudah jendelanya terisi
> penghalusan 3 titik  rerata bergerak atas 3 jendela berjarak 100 ms,
>                      jadi menunda sekitar 100 ms
> ```
>
> Memendekkan jendela jadi 0,7 detik memotong 300 milidetik dari latensi
> terburuk, dan harganya kata yang lebih panjang dari 0,7 detik tidak pernah
> muat utuh. "Hey synesis" hampir satu detik, jadi ini bukan pilihan.
>
> Menghapus penghalusan memotong 100 milidetik, dan harganya penyalaan palsu
> naik: satu jendela yang kebetulan tinggi sudah cukup untuk memicu, dan
> `haluskan` ada justru untuk menuntut tiga jendela berturut-turut.
>
> Yang bisa ditukar tanpa harga: `WAKE_LONCAT_MS` dari 100 jadi 50. Latensi
> deteksi berkurang rata-rata 25 milidetik dan beban prosesor naik dari 3,1
> jadi 6,2 persen. Itu pertukaran yang bagus, dan tidak diambil hanya karena
> 3,1 persen sudah cukup nyaman.

---

## Soal 7 - Yang dibawa ke Sesi 5

**7a.** Bagian 5 mengukur FAR pada ucapan, Bagian 6 pada derau ruangan.
Jelaskan kenapa keduanya harus ada.

> **Jawaban:** Keduanya menjawab pertanyaan yang berbeda, dan mengganti salah
> satunya dengan yang lain menghasilkan keputusan yang salah.
>
> FAR pada ucapan menjawab: "kalau ada orang bicara dan bukan mengucapkan
> wake word, seberapa sering SYNESIS salah bangun?" Itu keadaan yang jarang
> tetapi berbahaya, misalnya waktu kamu menelepon.
>
> Penyalaan per jam pada derau menjawab: "kalau tidak ada yang bicara sama
> sekali, seberapa sering SYNESIS bangun sendiri?" Itu keadaan SYNESIS selama
> 99 persen waktunya, dan itulah yang menentukan apakah fiturnya akan
> dimatikan dalam seminggu.
>
> Angka yang satu tidak bisa diturunkan dari yang lain, karena sebarannya
> berbeda: derau ruangan bukan sekadar ucapan yang pelan.

**7b.** Sebutkan apa yang HARUS diukur ulang sesudah wake word yang
sesungguhnya direkam, dan apa yang tidak perlu.

> **Jawaban:** Harus diukur ulang:
>
> - AUC, FAR, FRR, dan ambangnya. Seluruhnya bergantung pada model, dan
>   modelnya berganti.
> - penyalaan per jam pada derau ruangan. Bahkan idealnya bukan pada
>   `_background_noise_` Speech Commands, melainkan pada rekaman kamar
>   sendiri.
> - latensi, karena "hey synesis" jauh lebih panjang daripada `marvin`.
>
> Tidak perlu diukur ulang:
>
> - beban prosesor, karena arsitekturnya sama persis dan masukannya sama
>   besar;
> - bentuk fitur dan jumlah parameter;
> - kesimpulan Bagian 3 dan 4 tentang log-mel dan augmentasi, karena keduanya
>   diukur pada tugas 12 kelas yang tidak berubah.
>
> Yang paling gampang dilupakan: ambang yang tersimpan di dalam berkas model.
> `Wake.muat` membacanya dari sana, bukan dari `konfig.WAKE_AMBANG`, justru
> supaya ambang lama tidak terbawa ke model baru.
