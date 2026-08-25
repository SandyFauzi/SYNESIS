# Soal Bulan 3 Sesi 3 - CNN, dan apa yang dibelinya

Berkas latihan: [`bulan3_sesi3_cnn.py`](bulan3_sesi3_cnn.py)

Lima TODO. Sesi ini menambahkan tiga operasi ke `Tensor` Bulan 1, memeriksa
gradiennya, lalu memakai CNN yang dihasilkannya untuk menjawab satu
pertanyaan yang jarang ditanyakan: pada jumlah bobot yang SAMA, apakah CNN
benar-benar lebih baik daripada MLP?

> Prasyarat: Bulan 1 Sesi 3+4 (kelas `Tensor`), Bulan 3 Sesi 1 (im2col dan
> korelasi silang), Bulan 3 Sesi 2 (`spektrogram_mel`, `pra_tekan`).

> Waktu jalan di mesin pemilik: 31 detik, sebagian besar di Bagian 3.

---

## Soal 1 - im2col, col2im, dan tanda tambah yang menentukan

**1a.** Bagian 2 menyarankan mengganti `+=` jadi `=` di dalam
`im2col._backward`, lalu menjalankan ulang pemeriksa gradien. Ramalkan apa
yang terjadi, lalu jelaskan kenapa modelnya TETAP bisa dilatih meski
gradiennya salah.

> **Jawaban:** Galat relatifnya melompat dari orde $10^{-9}$ ke orde $10^{-1}$
> untuk entri yang terletak di tengah gambar, dan tetap kecil untuk entri di
> sudut. Sebabnya langsung: piksel tengah masuk ke sembilan petak, jadi
> gradien benarnya jumlah sembilan sumbangan; dengan `=`, yang tersimpan
> hanya sumbangan terakhir, kira-kira sepersembilannya. Piksel sudut cuma
> masuk satu petak, jadi jumlah dan penugasan memberi hasil yang sama.
>
> Modelnya tetap bisa dilatih karena gradien yang salah itu masih
> BERKORELASI POSITIF dengan gradien yang benar: ia satu sumbangan dari
> sembilan yang bertanda sama. Arah pembaruannya masih menurunkan rugi,
> hanya lebih lambat dan bias ke tepi. Rugi tetap turun, akurasi tetap naik,
> dan tidak ada satu pun tanda bahwa ada yang salah.
>
> Itulah alasan Bagian 2 ada, dan alasan ia dijalankan SEBELUM Bagian 3.
> Bug gradien tidak menghasilkan pesan galat; ia menghasilkan hasil yang
> mengecewakan dan tidak bisa dijelaskan.

**1b.** `im2col` menaikkan memori sembilan kali lipat. Untuk lapisan kedua
CNN di Bagian 3 (masukan $13\times13\times8$, batch 64), hitung memorinya
dan bandingkan dengan masukannya.

> **Jawaban:** Keluaran `valid` per contoh $11\times11 = 121$ posisi, tiap
> posisi jadi baris sepanjang $3\times3\times8 = 72$. Untuk batch 64:
> $64 \times 121 \times 72 = 557.568$ angka float64, yaitu 4,46 MB.
>
> Masukannya $64 \times 13 \times 13 \times 8 \times 8 = 692$ KB. Jadi
> pelipatannya 6,4 kali, bukan 9, karena tepi tidak tersalin penuh
> (Soal 6b Sesi 1).
>
> Angka ini kecil, dan tetap layak dihitung: pelipatannya sebanding dengan
> $K_h K_w$ dan dengan jumlah kanal masukan sekaligus. Lapisan dengan 256
> kanal masukan dan kernel $3\times3$ menghasilkan baris sepanjang 2.304,
> dan di situ im2col mulai jadi persoalan nyata. PyTorch memakai algoritma
> berbasis ubin yang tidak pernah membentuk matriksnya secara utuh, dan
> itulah sebagian dari selisih kecepatan di Bagian 5.

---

## Soal 2 - Pooling

**2a.** Kalau dua nilai di dalam satu petak persis sama, `argmax` memilih
yang pertama dan gradiennya seluruhnya jatuh ke sana. Apakah itu benar?

> **Jawaban:** Fungsi maksimum tidak terdiferensialkan di titik itu, jadi
> tidak ada jawaban "benar" dalam arti kalkulus biasa. Yang ada subgradien,
> dan seluruh himpunan
> $\{\alpha e_i + (1-\alpha) e_j : 0\le\alpha\le 1\}$ adalah subgradien yang
> sah. Memilih $\alpha = 1$ adalah pilihan yang sah, membagi rata juga sah.
>
> Untuk data pecahan yang berasal dari pengukuran, kasus ini praktis tidak
> pernah terjadi. Ia terjadi pada masukan yang mengandung banyak nilai
> identik, dan MNIST punya itu: latar belakangnya nol persis. Setelah ReLU,
> seluruh petak yang mati bernilai nol dan gradiennya jatuh semua ke pojok
> kiri atas. Karena nilainya nol, gradien yang mengalir juga nol, jadi
> akibatnya tetap tidak ada.

**2b.** Pooling $2\times2$ dan konvolusi dengan langkah 2 sama-sama
menyusutkan ukuran separuh. Sebutkan bedanya, dan mana yang kamu pilih untuk
spektrogram.

> **Jawaban:** Konvolusi berlangkah 2 memilih posisi berdasarkan KISI: ia
> selalu mengambil posisi genap, apa pun isinya. Max pooling memilih
> berdasarkan ISI: ia mengambil yang terbesar di dalam petaknya, di mana pun
> letaknya.
>
> Akibatnya, pooling memberi ketidakpekaan terhadap pergeseran kecil, sedang
> langkah 2 tidak: menggeser masukan satu piksel mengubah seluruh keluaran
> lapisan berlangkah. Ongkosnya, pooling membuang informasi posisi tepat, dan
> lapisan berlangkah mempertahankannya sambil belajar bagaimana meringkas.
>
> Untuk spektrogram saya memilih pooling di sumbu waktu dan TIDAK di sumbu
> frekuensi, atau pooling frekuensi dengan petak yang lebih kecil. Alasannya
> dari Bagian 6: pergeseran 10 milidetik di sumbu waktu memang tidak berarti
> apa-apa dan layak dibuang, sedangkan pergeseran satu tapis mel di frekuensi
> rendah adalah selisih 30 Hz, dan 30 Hz di daerah formant pertama bisa
> membedakan vokal.
>
> Arsitektur di Bagian 3 memakai pooling simetris $2\times2$ karena ia
> menangani MNIST. Sesi 4 memakai petak asimetris, dan sekarang alasannya
> bisa dituliskan.

---

## Soal 3 - CNN lawan MLP pada jumlah bobot yang sama

Bagian 3 memberi:

```text
model                            bobot    detik   akurasi uji
-------------------------------------------------------------
CNN 8-16, kolam 2x2              5.258     22.2        96.43%
MLP 7 tersembunyi                5.575      0.4        84.05%
```

**3a.** Perbandingan ini menyamakan jumlah bobot dan membiarkan yang lain
berbeda. Sebutkan tiga hal yang tidak disamakan, dan untuk masing-masing
tentukan apakah ia menguntungkan CNN atau MLP.

> **Jawaban:**
>
> 1. **Jumlah operasi per contoh.** CNN memakai 22,2 detik dan MLP 0,4
>    detik, jadi CNN melakukan sekitar 55 kali lebih banyak kerja untuk
>    jumlah bobot yang sama. Menguntungkan CNN, dan ini bukan cacat kecil:
>    perbandingan yang menyamakan ANGGARAN HITUNGAN dan bukan jumlah bobot
>    akan memberi MLP jauh lebih banyak parameter.
>
> 2. **Kedalaman.** CNN punya tiga lapisan berbobot dan dua ReLU; MLP punya
>    dua lapisan dan satu ReLU. Menguntungkan CNN. Pembanding yang lebih
>    ketat adalah MLP dua lapisan tersembunyi dengan jumlah bobot yang sama.
>
> 3. **Laju belajar dan jumlah epoch.** Keduanya dipatok sama (0,05 dan 3),
>    dan itu tidak netral: nilai yang baik untuk satu arsitektur belum tentu
>    baik untuk yang lain. Arahnya tidak bisa ditebak tanpa menyapunya.
>
> Kesimpulan yang jujur: selisih 12,4 poin itu nyata, tetapi ia tidak
> membuktikan "CNN lebih baik daripada MLP pada anggaran yang sama". Yang
> dibuktikannya lebih sempit dan tetap berguna: pada jumlah PARAMETER yang
> sama, susunan berbagi bobot mengalahkan lapisan padat, dan selisihnya jauh
> lebih besar daripada selang kepercayaannya.

**3b.** Ramalkan apa yang terjadi kalau data latihnya dinaikkan dari 10.000
ke 50.000, dan model mana yang lebih diuntungkan.

> **Jawaban:** Keduanya naik, tetapi MLP naik jauh lebih banyak. Sebabnya
> MLP 7 neuron tersembunyi TIDAK sedang terbatas data; ia terbatas kapasitas.
> Tujuh neuron adalah leher botol yang memaksa 784 dimensi masuk ke 7, dan
> menambah data tidak melebarkan leher botol.
>
> Jadi ramalan yang tepat justru sebaliknya: menambah data tidak banyak
> menolong MLP 7-neuron, dan sedikit menolong CNN. Yang benar-benar menolong
> MLP adalah menambah neuron, dan itu berarti menambah parameter, dan itu
> membatalkan syarat perbandingannya.
>
> Di situlah letak seluruh gagasan berbagi bobot: CNN 5.258 bobot punya
> kapasitas untuk mewakili fungsi yang jauh lebih kaya daripada MLP 5.575
> bobot, karena bobotnya dipakai di banyak posisi. Jumlah parameter dan
> kapasitas bukan hal yang sama, dan CNN adalah bukti tandingan yang paling
> bersih untuk asumsi bahwa keduanya sama.
>
> Ramalan terukur untuk dijalankan sendiri: pada 50.000 contoh, CNN naik ke
> sekitar 98 persen dan MLP 7-neuron mentok di bawah 88 persen.

---

## Soal 4 - Kernel yang ditemukan sendiri

Bagian 4 memberi delapan kernel dengan jumlah antara $-1{,}57$ dan $+1{,}89$,
dan kemiripan kosinus tertinggi 0,832 terhadap `sobel_x`.

**4a.** Kenapa tanda kemiripan kosinus diabaikan?

> **Jawaban:** Kernel $-k$ mendeteksi pola yang sama dengan $k$, hanya dengan
> keluaran bertanda terbalik, dan lapisan berikutnya bisa membalik tandanya
> kembali dengan bobot negatif. Jadi $k$ dan $-k$ mengerjakan pekerjaan yang
> setara, dan membedakan keduanya berarti mengukur konvensi, bukan fungsi.
>
> Alasan kedua yang lebih menggigit: ReLU sesudah konvolusi TIDAK simetris,
> jadi $k$ dan $-k$ sebenarnya tidak setara di jaringan ini. $k$ meneruskan
> tepi terang-ke-gelap dan mematikan yang sebaliknya. Jadi mengabaikan tanda
> adalah penyederhanaan yang perlu dinyatakan, bukan kebenaran. Yang
> dijawabnya cuma "apakah kernel ini menyapu arah yang sama", dan itu memang
> yang ingin diketahui.

**4b.** Empat dari delapan kernel punya jumlah yang jauh dari nol
($+1{,}44$, $-1{,}57$, $+1{,}65$, $+1{,}89$). Apakah itu berarti latihannya
gagal?

> **Jawaban:** Tidak. Kernel yang jumlahnya besar bekerja sebagai pengukur
> tingkat kecerahan lokal, dan untuk MNIST itu berguna: berapa banyak tinta
> ada di daerah ini adalah ciri yang nyata. Yang keliru adalah harapan bahwa
> seluruh kernel akan jadi pendeteksi tepi.
>
> Yang ditunjukkan tabelnya lebih halus: ada campuran. Beberapa kernel
> jumlahnya mendekati nol dan bertindak sebagai pendeteksi perubahan;
> beberapa jumlahnya besar dan bertindak sebagai pengukur tenaga. Model
> memilih campuran itu sendiri, dan campuran itu masuk akal untuk data yang
> latarnya nol dan objeknya putih.
>
> Untuk membuktikan bahwa ini pilihan model dan bukan kebetulan inisialisasi:
> jalankan ulang dengan seed berbeda dan periksa apakah campurannya bertahan.
> Kalau porsi kernel berjumlah nol tetap serupa, itu sifat masalahnya. Kalau
> berubah acak, itu derau inisialisasi.

---

## Soal 5 - PyTorch, dan penerjemahan yang bisa gagal diam-diam

Bagian 5 memberi selisih $1{,}07\times10^{-14}$ antara numpy dan PyTorch.

**5a.** Sebutkan tiga kesalahan penerjemahan tata letak yang TIDAK akan
memicu pesan galat, hanya angka yang berbeda.

> **Jawaban:**
>
> 1. **Lupa membalik kernel.** Kalau kamu menganggap `F.conv2d` mengerjakan
>    konvolusi sejati dan membalik kernelmu sebelum menyalinnya, hasilnya
>    berbeda tetapi bentuknya sama persis. Sesi 1 Bagian 4 sudah menyiapkan
>    jebakan ini.
>
> 2. **Urutan sumbu bobot.** Bobot kita $(K_h, K_w, C_{in}, C_{out})$,
>    PyTorch $(C_{out}, C_{in}, K_h, K_w)$. Untuk kernel $3\times3$ dengan
>    $C_{in} = C_{out} = 8$, seluruh permutasi yang salah tetap menghasilkan
>    tensor $8\times8\times3\times3$ yang sah.
>
> 3. **Urutan perataan sebelum lapisan padat.** Kita meratakan
>    kanal-terakhir, PyTorch secara alami meratakan kanal-kedua. Bentuknya
>    sama, isinya teracak. Inilah kenapa Bagian 5 memanggil `permute` sebelum
>    `reshape`, dan kenapa satu baris itu perlu komentar.
>
> Ketiganya menghasilkan model yang tetap bisa dilatih dan mencapai akurasi
> yang lumayan, karena bobotnya toh dipelajari. Ia menggigit ketika kamu
> memuat bobot terlatih ke implementasi yang lain, dan itu persis yang akan
> dilakukan Sesi 5 waktu memuat model wake word ke SYNESIS.

**5b.** Percepatan GPU cuma 18 kali dibandingkan numpy, dan cuma 1,8 kali
dibandingkan PyTorch CPU. Kenapa serendah itu?

> **Jawaban:** Modelnya terlalu kecil. Batch 64 gambar $28\times28$ dengan 8
> dan 16 kanal menghasilkan kernel GPU yang selesai dalam mikrodetik,
> sedangkan ongkos meluncurkan tiap kernel dan menyalin data tetap dibayar.
> Yang terukur di baris CUDA sebagian besar ongkos peluncuran, bukan
> hitungannya.
>
> Buktinya bisa didapat tanpa mengubah model: naikkan batch dari 64 ke 1024
> dan ukur lagi. Waktu CPU akan naik kira-kira 16 kali, waktu GPU jauh lebih
> sedikit, dan rasionya melebar.
>
> Konsekuensinya untuk Sesi 4: model wake word yang kecil tidak akan
> mendapat banyak dari GPU pada inferensi satu-satu, dan itu kabar baik.
> SYNESIS harus berjalan di CPU sambil GPU disimpan untuk Bulan 6, dan Bagian
> 5 baru saja mengukur bahwa harganya tidak mahal.

---

## Soal 6 - Stasioneritas, dan ramalan yang meleset

Bagian 6 memberi:

```text
sumbu            rasio tanpa pra-tekan   rasio dengan pra-tekan
---------------------------------------------------------------
frekuensi                        0.389                    0.114
waktu                            0.376                    0.406
```

**6a.** Rancang pengukuran yang memisahkan ketidakstasioneran sumbu waktu
yang berasal dari SUARA dari yang berasal dari cara datanya dipotong.

> **Jawaban:** Sumbernya bisa dipisah dengan menghapus penyebab yang
> dicurigai, lalu mengukur ulang.
>
> Pengukuran 1, kendali negatif: geser tiap ucapan secara acak sebesar
> $\pm 200$ milidetik dengan pembungkusan melingkar, lalu hitung ulang
> rasionya. Kalau ketidakstasionerannya berasal dari penyejajaran dataset,
> rasio waktu akan jatuh mendekati nol. Kalau ia bertahan, ada sesuatu
> tentang suaranya sendiri.
>
> Pengukuran 2, sumber yang lebih baik: pakai rekaman kontinu, bukan potongan
> satu detik. `_background_noise_` di Speech Commands berisi berkas berdurasi
> menit, dan potongan satu detik yang diambil dari posisi acak di dalamnya
> tidak punya penyejajaran sama sekali. Rasio waktunya adalah dasar yang
> benar-benar bebas artefak pemotongan.
>
> Pengukuran 3, pemisah yang paling langsung: hitung rasionya di dalam
> wilayah yang sudah dipotong VAD, yaitu hanya bingkai antara awal dan akhir
> ucapan. Kalau ketidakstasionerannya cuma "sunyi di tepi", memotong tepinya
> menghapusnya.
>
> Ramalan saya sebelum menjalankannya: ketiganya akan menurunkan rasio waktu
> di bawah 0,15, dan sisa yang bertahan berasal dari kenyataan bahwa kata
> punya awal, tengah, dan akhir yang memang berbeda secara akustik.

**6b.** Bagian 6 menemukan bahwa pra-penekanan menurunkan rasio frekuensi
dari 0,389 ke 0,114. Apakah itu berarti pra-penekanan membuat sumbu frekuensi
jadi stasioner, sehingga berbagi bobot di sumbu itu jadi sah?

> **Jawaban:** Tidak, dan membedakannya penting. Rasio yang diukur cuma
> melihat RERATA per posisi. Ia buta terhadap perbedaan yang tidak muncul di
> rerata, misalnya perbedaan bentuk korelasi antartapis, atau perbedaan
> ragam. Dua baris mel bisa punya rerata yang sama persis dan tetap
> memerlukan pendeteksi yang berbeda.
>
> Yang dibuktikan angka 0,114 lebih sempit: sesudah pra-penekanan, tidak ada
> lagi kemiringan tetap yang harus dipelajari ulang oleh setiap kernel di
> setiap posisi. Itu memang keuntungan nyata, dan itu memang salah satu
> beban yang membuat berbagi bobot mahal. Tetapi ia tidak menjawab apakah
> pola pada 200 Hz berarti hal yang sama dengan pola yang sama pada 4.000 Hz.
>
> Ukuran yang menjawab itu bukan statistik melainkan percobaan: latih dua
> model, satu berbagi bobot di kedua sumbu dan satu hanya di sumbu waktu,
> lalu bandingkan akurasi ujinya. Sesi 4 menjalankannya.

---

## Yang dibawa ke Sesi 4

| dari sini | dipakai di sana |
| --- | --- |
| gradien yang sudah diperiksa | keyakinan bahwa `nn.Conv2d` mengerjakan hal yang sama |
| CNN lawan MLP pada bobot sama | alasan memakai CNN untuk 200 rekaman wake word |
| rasio waktu 0,406 | alasan augmentasi geseran waktu, dengan angkanya |
| pooling asimetris | rancangan arsitektur untuk spektrogram |
| percepatan GPU cuma 18x di model kecil | alasan SYNESIS berjalan di CPU |
