# Soal Bulan 3 Sesi 1 - konvolusi, dan ongkosnya

Berkas latihan: [`bulan3_sesi1_konvolusi.py`](bulan3_sesi1_konvolusi.py)

Enam TODO. Sesi ini tidak menyentuh suara sama sekali; ia membereskan operasi
yang dipakai sepanjang Bulan 3 dan Bulan 4, lalu mengukur ongkosnya supaya
keputusan arsitektur di Sesi 3 punya angka, bukan selera.

> Prasyarat: Bulan 1 Sesi 3+4 sudah dikerjakan, karena Bagian 3 memakai
> `mnist.npz` yang sudah tersimpan di `E:\SYNESIS\data`. Tidak ada unduhan
> baru dan tidak ada pustaka baru.

> Semua angka yang dikutip di jawaban berasal dari keluaran
> `python notebooks\bulan3_sesi1_konvolusi.py` di mesin pemilik, GTX 1650 Ti,
> Python 3.12.5, numpy 2.5.2. Angka waktumu akan berbeda; yang harus sama
> adalah urutan dan besaran ordenya.

---

## Soal 1 - Mode, dan penyusutan yang menumpuk

Bagian 1 memberi:

```text
mode      panjang    selisih maks
---------------------------------
full           14        0.00e+00
same           12        0.00e+00
valid          10        0.00e+00
```

**1a.** Turunkan panjang keluaran ketiga mode untuk sinyal panjang $N$ dan
kernel panjang $K$, lalu jelaskan kenapa `same` tidak terdefinisi secara
tunggal ketika $K$ genap.

> **Jawaban:** Konvolusi penuh punya keluaran taknol di setiap $n$ yang
> memungkinkan ada pasangan indeks sah, yaitu $0 \le k \le N-1$ dan
> $0 \le n-k \le K-1$. Gabungan keduanya memberi $0 \le n \le N+K-2$, jadi
> panjangnya $N+K-1$. Terukur: $N=12$, $K=3$, keluar 14.
>
> `valid` hanya mengambil $n$ ketika seluruh kernel tertutup sinyal, yaitu
> $K-1 \le n \le N-1$, panjangnya $N-K+1 = 10$.
>
> `same` mengambil potongan sepanjang $N$ dari tengah hasil penuh. Hasil
> penuh lebih panjang $K-1$, jadi yang dibuang $K-1$ cuplikan, dibagi ke dua
> ujung. Kalau $K$ ganjil, $K-1$ genap dan pembagiannya simetris:
> $(K-1)/2$ di tiap sisi. Kalau $K$ genap, $K-1$ ganjil dan tidak ada
> pembagian simetris; salah satu ujung harus kehilangan satu cuplikan lebih
> banyak. numpy memilih membuang $\lfloor (K-1)/2 \rfloor$ di kiri, tetapi
> itu konvensi, bukan turunan. Konsekuensinya: kernel genap menggeser
> keluaran setengah cuplikan terhadap masukan, dan itulah alasan praktis
> kenapa kernel CNN hampir selalu ganjil.

**1b.** Sebuah CNN menumpuk $L$ lapisan konvolusi `valid` dengan kernel
$K \times K$ tanpa padding. Turunkan ukuran keluarannya, lalu hitung berapa
lapisan $3\times3$ yang muat di atas masukan $28\times28$ sebelum habis.

> **Jawaban:** Tiap lapisan `valid` memotong $K-1$ di tiap sumbu, dan
> pemotongan itu menumpuk secara linear:
>
> $$H_L = H_0 - L(K-1).$$
>
> Untuk $H_0 = 28$ dan $K = 3$: $H_L = 28 - 2L$, jadi $L \le 13$ sebelum
> ukurannya jadi nol, dan $L = 13$ menyisakan $2\times2$. Praktisnya jauh
> lebih sedikit, karena setelah beberapa lapisan yang tersisa terlalu kecil
> untuk dipooling.
>
> Yang menarik adalah medan penerimaan (*receptive field*), yang tumbuh
> dengan laju yang sama: satu piksel keluaran lapisan ke-$L$ dipengaruhi
> $1 + L(K-1)$ piksel masukan di tiap sumbu. Dua lapisan $3\times3$ punya
> medan penerimaan $5\times5$ dengan $2 \cdot 9 = 18$ bobot, sedangkan satu
> lapisan $5\times5$ punya medan yang sama dengan 25 bobot. Dua lapisan kecil
> lebih murah DAN menyisipkan satu ReLU tambahan di antaranya. Itu seluruh
> alasan VGG memakai tumpukan $3\times3$.

**1c.** Kenapa `full` yang benar untuk tanggapan impuls, sedangkan `valid`
yang benar untuk lapisan CNN?

> **Jawaban:** Tanggapan impuls menggambarkan sistem fisis: gema ruangan
> tidak berhenti begitu berkas audionya habis, jadi memotong ekornya berarti
> membuang bagian dari jawabannya. `full` menyimpan seluruh ekor.
>
> Lapisan CNN membaca ciri dari petak yang benar-benar ada. Nilai di mode
> `full` yang berada di luar $[K-1, N-1]$ dihitung dari nol imajiner, jadi
> ia mengukur "seberapa mirip petak ini dengan kernel, kalau setengah
> petaknya kosong". Itu bukan pengukuran yang berguna, dan di lapisan awal
> ia menghasilkan tanggapan palsu di sepanjang tepi gambar. Padding tetap
> dipakai di CNN modern, tetapi alasannya menjaga ukuran, bukan menjaga
> kebenaran.

---

## Soal 2 - Titik silang FFT, diturunkan lalu dibandingkan

Bagian 2 memberi:

```text
       N     K   langsung (ms)    FFT (ms)    rasio
  ---------------------------------------------------
    1024    16           0.025       0.072     0.35
    1024   128           0.031       0.065     0.47
    1024  1024           0.141       0.066     2.13
   65536    16           1.077       5.919     0.18
   65536   128           1.827       6.501     0.28
   65536  1024           6.421       5.880     1.09
```

**2a.** Turunkan syarat $K$ agar konvolusi lewat FFT lebih murah daripada
cara langsung, sebagai fungsi $N$. Nyatakan asumsi tentang konstantanya.

> **Jawaban:** Cara langsung memakai $c_1 N K$ operasi. Lewat FFT: dua
> transformasi maju, satu perkalian titik, satu transformasi balik, semuanya
> pada panjang $M \ge N+K-1$, jadi $c_2\,\cdot 3 M \log_2 M + c_3 M$. Untuk
> $K \ll N$, $M \approx N$ dan sukunya didominasi $3 c_2 N \log_2 N$.
> Syaratnya
>
> $$c_1 N K > 3 c_2 N \log_2 N \quad\Longleftrightarrow\quad
> K > \frac{3 c_2}{c_1}\log_2 N.$$
>
> Titik silangnya tumbuh dengan $\log_2 N$, bukan dengan $N$. Itulah kenapa
> menaikkan $N$ seratus kali lipat hampir tidak menggeser $K$ ambangnya.
>
> Asumsi konstantanya: $c_1$ untuk `np.convolve` kecil karena gelungnya di C
> dan bekerja di float64 berurutan; $c_2$ jauh lebih besar karena FFT
> bekerja di bilangan kompleks, mengalokasikan array sementara, dan
> mengakses memori dengan pola yang tidak berurutan.
>
> Dicocokkan ke tabel: pada $N = 1024$, silangnya ada di antara $K = 128$
> (rasio 0,47) dan $K = 1024$ (rasio 2,13). Ambil silang di rasio 1, sekitar
> $K \approx 400$. Dengan $\log_2 1024 = 10$, itu memberi
> $3c_2/c_1 \approx 40$. Ramalan untuk $N = 65536$, $\log_2 N = 16$:
> $K \approx 640$. Terukur, $K = 1024$ memberi rasio 1,09, jadi silangnya
> memang sedikit di bawah 1024. Ramalannya konsisten dengan yang diukur.

**2b.** Bagian 2 mengukur 63 cuplikan tercemar ketika penambahan nol
dihilangkan, dengan $K = 64$. Tunjukkan kenapa jumlahnya persis $K-1$, dan
di mana pencemaran itu mendarat.

> **Jawaban:** Perkalian di ranah frekuensi pada panjang $M$ menghasilkan
> konvolusi melingkar:
>
> $$y_{\text{ling}}[n] = \sum_k x[k]\,h[(n-k) \bmod M].$$
>
> Hasil linearnya panjang $N+K-1$. Kalau $M = N$, maka $K-1$ cuplikan
> terakhir tidak punya tempat dan indeksnya dibungkus ke $n = 0, 1, \dots,
> K-2$. Jadi yang tercemar persis $K-1$ cuplikan PERTAMA, bukan yang
> terakhir, dan besarnya persis ekor yang terbuang.
>
> Terukur: $K = 64$ memberi 63, dan pencemarannya berada di indeks 0 sampai
> 62. Ini kesalahan yang halus justru karena tidak menghasilkan `nan` atau
> pesan galat; ia menghasilkan angka yang kelihatan wajar di awal berkas
> audio. Di Sesi 2, kesalahan yang sama akan muncul lagi dalam bentuk yang
> berbeda: bingkai yang tumpang tindih tanpa jendela menghasilkan diskontinu
> di sambungannya.

**2c.** Untuk konvolusi audio berdurasi panjang dengan tanggapan impuls
ruangan sepanjang dua detik pada 16 kHz, mana yang kamu pilih, dan kenapa
jawabannya bukan "pilih yang tabelnya lebih cepat"?

> **Jawaban:** Tanggapan impuls dua detik pada 16 kHz berarti $K = 32.000$,
> jauh di atas titik silang mana pun, jadi FFT menang telak. Tetapi
> mengerjakannya sebagai satu FFT raksasa berarti seluruh sinyal harus ada
> sebelum satu cuplikan keluaran pun bisa dihitung, dan itu latensi yang
> tidak bisa diterima untuk sistem yang mendengarkan.
>
> Cara yang dipakai di praktik adalah *overlap-add*: potong sinyal jadi blok
> panjang $B$, konvolusikan tiap blok lewat FFT panjang $B+K-1$, lalu
> jumlahkan ekor blok ke-$i$ ke awal blok ke-$i+1$. Latensinya jadi $B$
> cuplikan, bukan seluruh berkas, dan ongkosnya tetap $O(\log)$ per cuplikan.
>
> Pelajarannya untuk Bulan 3: tabel waktu di Bagian 2 mengukur ongkos total,
> dan sistem yang mendengarkan tidak dinilai dari ongkos total melainkan dari
> latensi. Kedua besaran itu bisa menunjuk ke arah yang berlawanan.

---

## Soal 3 - Berbagi bobot: apa yang dibeli dan apa yang dibayar

Bagian 3 memberi: lapisan padat $28\times28 \to 26\times26$ butuh 529.984
bobot, satu kernel $3\times3$ butuh 9, perbandingannya 58.887 banding 1.

**3a.** Berbagi bobot memaksakan satu asumsi tentang datanya. Sebutkan
asumsinya, dan beri satu contoh data yang melanggarnya.

> **Jawaban:** Asumsinya *stasioneritas terjemahan*: ciri yang berguna di
> satu tempat sama bergunanya di tempat lain. Pendeteksi tepi tegak berguna
> di pojok kiri atas maupun di tengah, jadi tidak perlu ada sembilan angka
> terpisah untuk tiap posisi.
>
> Data yang melanggarnya: foto wajah yang sudah disejajarkan, ketika mata
> selalu ada di baris yang sama. Di situ posisi membawa informasi, dan
> lapisan padat yang punya bobot berbeda per posisi bisa memanfaatkannya.
> Itulah alasan lapisan "locally connected" ada di beberapa arsitektur
> pengenalan wajah lama, dan alasan Bulan 4 mengerjakan penyejajaran wajah
> sebelum mengambil embedding.
>
> Contoh kedua, dan lebih penting untuk Bulan 3: spektrogram TIDAK stasioner
> di sumbu frekuensi. Pola pada 200 Hz dan pola yang sama pada 4.000 Hz
> berarti bunyi yang berbeda, bukan bunyi yang sama yang bergeser. Ia
> stasioner di sumbu waktu saja. Sesi 3 mengukur akibatnya.

**3b.** Kalau berbagi bobot menghemat data, kenapa lapisan padat tidak
dihapus sama sekali dari CNN?

> **Jawaban:** Karena keduanya mengerjakan pekerjaan yang berbeda. Lapisan
> konvolusi menjawab "ciri apa yang ada di sini", dan jawabannya bersifat
> lokal sesuai medan penerimaannya. Keputusan akhir membutuhkan gabungan
> seluruh posisi, dan penggabungan itu justru operasi yang TIDAK boleh
> berbagi bobot, karena posisi mulai berarti begitu ciri lokalnya sudah
> diringkas.
>
> Kecenderungan modern memang mengganti lapisan padat besar dengan
> *global average pooling*, dan itu bukan bantahan: rerata global adalah
> lapisan padat dengan bobot dipatok $1/n$, yaitu pilihan paling ekstrem di
> arah "posisi tidak berarti sama sekali".

---

## Soal 4 - Teorema untuk korelasi, dan konjugatnya

Bagian 4 memberi selisih 7,84 antara konvolusi dan korelasi untuk `sobel_x`,
dan nol untuk `kotak` dan `tajam`.

**4a.** Turunkan padanan teorema konvolusi untuk korelasi silang, dan
tunjukkan di mana konjugat kompleks muncul.

> **Jawaban:** Korelasi silang $(f \star g)(t) = \int \overline{f(\tau)}\,
> g(t+\tau)\,d\tau$. Tulis ulang sebagai konvolusi dengan versi yang
> dipantulkan: $f \star g = \overline{f(-t)} * g$. Sifat transformasi
> Fourier untuk pemantulan dan konjugasi,
>
> $$\mathcal{F}\{\overline{f(-t)}\}(\omega) = \overline{F(\omega)},$$
>
> memberi
>
> $$\mathcal{F}\{f \star g\} = \overline{F(\omega)}\,G(\omega).$$
>
> Jadi bedanya dengan teorema konvolusi tepat satu garis konjugat di atas
> $F$. Untuk sinyal real, konjugasi di ranah frekuensi setara dengan
> pemantulan di ranah waktu, dan di situlah selisih tanda pada `sobel_x`
> berasal.
>
> Akibat praktis yang sering dilupakan: $|{\mathcal{F}\{f \star f\}}| =
> |F|^2$, yaitu rapat spektrum daya. Autokorelasi dan spektrum daya adalah
> pasangan Fourier, dan itu teorema Wiener-Khinchin yang sudah kamu pakai
> di Fisika Statistik.

**4b.** Kernel mana di Bagian 3 yang membuat konvolusi dan korelasi
memberikan hasil identik, dan syarat umumnya apa?

> **Jawaban:** `kotak` dan `tajam`, keduanya memberi selisih nol. Syaratnya
> $k[u,v] = k[-u,-v]$, yaitu kernel simetris terhadap pusatnya di kedua
> sumbu. `kotak` seluruhnya konstan sehingga jelas simetris; `tajam`
> berbentuk salib dengan empat lengan bernilai sama.
>
> `sobel_x` antisimetris di sumbu mendatar: $k[u,-v] = -k[u,v]$. Membaliknya
> membalik tanda seluruh hasilnya, jadi selisih maksimumnya persis dua kali
> tanggapan maksimum: terukur $2 \times 3{,}918 = 7{,}836$, dan yang
> tercetak 7,835. Cocok.

**4c.** Apakah menyebut lapisan CNN "konvolusi" itu kesalahan yang perlu
diperbaiki, atau sekadar penamaan yang terlanjur?

> **Jawaban:** Terlanjur, dan tidak perlu diperbaiki di kode, tetapi wajib
> diketahui di kepala. Alasannya: kernelnya dipelajari, jadi ruang fungsi
> yang bisa diwakili lapisan korelasi identik dengan ruang fungsi lapisan
> konvolusi. Model tinggal mempelajari $k[-u,-v]$ sebagai ganti $k[u,v]$,
> dan rugi akhirnya sama.
>
> Yang menggigit adalah ketika kamu menyambungkannya ke teori. Kalau kamu
> memakai teorema konvolusi untuk mempercepat lapisan CNN lewat FFT, kamu
> harus menambahkan konjugat dari Soal 4a atau membalik kernelnya, kalau
> tidak hasilnya salah tanpa satu pun pesan galat. Hal yang sama berlaku
> ketika kamu membandingkan bobot terlatih dengan kernel Sobel klasik:
> tandanya bisa terbalik, dan itu bukan kegagalan latihan.

---

## Soal 5 - Keterpisahan dan peringkat

Bagian 5 memberi rasio 1,81 sampai 9,03 untuk $\sigma$ dari 1,0 sampai 8,0.

**5a.** Periksa apakah `SOBEL_X` terpisah. Kalau ya, tuliskan kedua
vektornya.

> **Jawaban:** Terpisah. `np.linalg.matrix_rank(SOBEL_X)` memberi 1, dan
> faktorisasinya
>
> $$\begin{pmatrix}-1&0&1\\-2&0&2\\-1&0&1\end{pmatrix}
> = \begin{pmatrix}1\\2\\1\end{pmatrix}
> \begin{pmatrix}-1&0&1\end{pmatrix}.$$
>
> Kedua faktornya punya arti sendiri-sendiri: $[1, 2, 1]$ adalah penghalus
> Gaussian tiga titik di sumbu tegak, dan $[-1, 0, 1]$ adalah turunan pusat
> di sumbu mendatar. Jadi Sobel bukan satu kernel ajaib, melainkan turunan
> yang dihaluskan lebih dulu di sumbu tegak lurusnya. Penghalusan itu ada
> karena turunan memperbesar derau, dan itu persoalan yang sama dengan
> mendiferensiasikan data terukur di praktikum.
>
> `tajam` tidak terpisah: peringkatnya 2, jadi ia butuh dua pasang vektor
> untuk ditulis ulang, dan mengerjakannya sebagai dua sapuan terpisah lalu
> menjumlahkannya justru lebih mahal daripada satu sapuan $3\times3$.

**5b.** Rasio percepatannya diramalkan $K^2/(2K) = K/2$, jadi 3,5 untuk
$K = 7$ dan 24,5 untuk $K = 49$. Terukurnya 1,81 dan 9,03. Jelaskan
selisihnya.

> **Jawaban:** Ramalan $K/2$ hanya menghitung perkalian, dan yang terukur
> menghitung waktu. Tiga sebab selisihnya:
>
> 1. Dua sapuan 1D memanggil `convolve2d` dua kali, jadi ongkos tetap per
>    panggilan dibayar dua kali, ditambah satu array antara berukuran penuh
>    yang harus dialokasikan dan ditulis.
> 2. Sapuan 2D membaca petak $K \times K$ yang bersebelahan di memori,
>    sehingga cache-nya bekerja baik. Sapuan kolom membaca dengan langkah
>    lebar, dan setiap lompatan berpeluang meleset dari cache.
> 3. Gambarnya cuma $108\times108$; ongkos tetapnya belum tenggelam.
>
> Arah tren tetap benar dan itu yang penting: rasionya naik hampir linear
> terhadap $K$ (1,81 → 2,48 → 4,97 → 9,03 untuk $K$ 7 → 13 → 25 → 49).
> Kalau ada yang melaporkan percepatan persis $K/2$ dari pengukuran, patut
> dicurigai bahwa yang dilaporkan hitungan perkalian, bukan stopwatch.

---

## Soal 6 - col2im, diturunkan sebelum ditulis

Bagian 6 memberi percepatan 548x dan pelipatan memori 8,7x.

**6a.** `im2col` menyalin tiap piksel sebanyak $K_h K_w$ kali. Turunkan
gradien terhadap masukannya, dan tunjukkan kenapa jawabannya adalah
penjumlahan, bukan pemilihan.

> **Jawaban:** `im2col` adalah pemetaan linear $C = S g$ dengan $S$ matriks
> yang setiap barisnya memuat tepat satu angka 1. Untuk pemetaan linear,
> aturan rantai memberi
>
> $$\frac{\partial \mathcal{L}}{\partial g} = S^{\top}
> \frac{\partial \mathcal{L}}{\partial C}.$$
>
> $S^\top$ punya satu angka 1 di setiap kolom yang menunjuk ke salinan, jadi
> mengalikannya berarti MENJUMLAHKAN seluruh gradien dari setiap salinan
> kembali ke piksel asalnya. Itulah `col2im`.
>
> Kenapa penjumlahan dan bukan pemilihan: satu piksel benar-benar
> memengaruhi $K_h K_w$ keluaran yang berbeda, jadi turunannya adalah jumlah
> sumbangan dari seluruh jalur. Ini persis aturan yang sudah kamu pakai di
> Bulan 1 pada `Tensor.__add__` untuk geseran yang disiarkan: siaran maju
> berarti jumlah mundur. Aturannya satu, penampilannya saja berbeda.

**6b.** Piksel mana yang menerima gradien paling sedikit, dan apa akibatnya
untuk latihan?

> **Jawaban:** Piksel di sudut. Pada mode `valid`, piksel $(0,0)$ hanya masuk
> ke satu petak, sedangkan piksel di tengah masuk ke $K_h K_w$ petak. Jadi
> gradien di sudut sekitar $1/(K_h K_w)$ kali gradien di tengah, yaitu
> sepersembilan untuk kernel $3\times3$.
>
> Akibatnya lapisan awal belajar lebih lambat di tepi gambar daripada di
> tengahnya. Untuk MNIST hal ini tidak menggigit karena tepinya nol. Untuk
> spektrogram di Sesi 4 ia menggigit, karena baris frekuensi terendah dan
> tertinggi ada di tepi dan keduanya membawa informasi.
>
> Ini juga menjelaskan pelipatan memori terukur 8,7 dan bukan tepat 9:
> piksel tepi tidak tersalin penuh sembilan kali.

**6c.** Berapa memori matriks `im2col` untuk satu batch 64 spektrogram
$40 \times 101$ dengan kernel $3\times3$ dan 32 kanal keluaran, dalam
float32? Bandingkan dengan ukuran batch mentahnya.

> **Jawaban:** Keluaran `valid` per spektrogram $38 \times 99 = 3.762$
> posisi, tiap posisi jadi satu baris sepanjang $3 \times 3 = 9$. Untuk 64
> contoh: $64 \times 3.762 \times 9 = 2.166.912$ angka, kali 4 byte =
> **8,67 MB**.
>
> Batch mentahnya $64 \times 40 \times 101 \times 4 = 1{,}03$ MB. Jadi
> pelipatannya 8,4x, sesuai ramalan $\approx K_h K_w$ dikurangi efek tepi.
>
> Angka itu masih kecil, dan itulah alasan im2col dipakai apa adanya di Sesi
> 3. Ia berhenti kecil di lapisan kedua yang punya 32 kanal masukan:
> barisnya jadi $32 \times 9 = 288$, dan memorinya naik jadi sekitar 277 MB
> untuk batch yang sama. Di situ orang mulai memakai konvolusi langsung
> berbasis ubin, atau memecah batch. Soal ini sengaja diberikan supaya kamu
> mengenali batasnya sebelum menabraknya.

---

## Soal 7 - Nyquist, dan keputusan laju cuplik untuk SYNESIS

Bagian 7 memberi: pada 1.000 Hz, sinus 600 Hz menghasilkan cuplikan yang
identik dengan sinus 400 Hz.

**7a.** Turunkan rumus frekuensi terlihat untuk sembarang $f$ dan laju
cuplik $f_s$, dan sebutkan kapan tandanya ikut terbalik.

> **Jawaban:** Cuplikan $x[n] = \sin(2\pi f n / f_s)$ tidak berubah kalau
> $f$ digeser kelipatan $f_s$, karena $\sin$ berperiode $2\pi$. Jadi cukup
> tinjau $r = f \bmod f_s$. Kalau $r \le f_s/2$, frekuensi terlihatnya $r$.
> Kalau $r > f_s/2$, tulis $r = f_s - r'$ dengan $r' < f_s/2$, dan
>
> $$\sin\!\left(\frac{2\pi (f_s - r') n}{f_s}\right)
> = \sin\!\left(2\pi n - \frac{2\pi r' n}{f_s}\right)
> = -\sin\!\left(\frac{2\pi r' n}{f_s}\right).$$
>
> Jadi frekuensi terlihatnya $f_s - r$, dengan tanda terbalik. Itu sebabnya
> Bagian 7 mengambil minimum dari selisih dan jumlah: lipatan di atas
> Nyquist membalik fase.
>
> Untuk sinyal real, pembalikan fase ini tidak terlihat pada spektrum
> besarannya, dan itulah kenapa aliasing pada spektrogram muncul sebagai
> garis yang memantul di batas atas gambar, bukan sebagai sesuatu yang
> jelas-jelas rusak.

**7b.** Mikrofon laptop mencuplik 44.100 Hz, sedangkan model wake word
bekerja di 16.000 Hz. Apa yang harus dilakukan, dan apa yang terjadi kalau
kamu cuma mengambil tiap cuplikan ke-2,75?

> **Jawaban:** Harus ditapis lebih dulu, baru dicuplik ulang. Mengambil tiap
> cuplikan ke-$M$ tanpa tapis adalah pencuplikan ulang telanjang, dan segala
> isi di atas 8.000 Hz akan melipat ke bawah 8.000 Hz sesuai 7a. Desis dan
> gerisik pada 12.000 Hz akan mendarat di 4.000 Hz, tepat di tengah pita
> yang dipakai membedakan kata.
>
> Rasio 44.100 ke 16.000 bukan bilangan bulat ($2{,}75625$), jadi tidak bisa
> sekadar mengambil satu dari sekian. Cara yang benar: tapis lolos-rendah
> dengan sudut potong di bawah 8.000 Hz, lalu interpolasi ke kisi waktu yang
> baru. `scipy.signal.resample_poly(x, 160, 441)` mengerjakan keduanya
> sekaligus, dan pecahan $160/441$ itu persis $16.000/44.100$ setelah
> disederhanakan.
>
> Cara paling murah, dan yang dipakai SYNESIS: minta PortAudio membuka
> peranti langsung pada 16.000 Hz dan biarkan driver yang mengerjakan
> penapisannya. Kalau peranti menolak, barulah `resample_poly` dipakai.
> Sesi 5 memuat pemeriksanya.

**7c.** Kenapa 16 kHz cukup untuk pengenalan kata tetapi tidak cukup untuk
musik, dan apa hubungannya dengan skala mel di Sesi 2?

> **Jawaban:** Pengenalan kata bergantung pada formant, yaitu puncak
> resonansi saluran vokal, dan tiga formant pertama yang membedakan vokal
> semuanya di bawah 3.500 Hz. Konsonan desis seperti /s/ memang menaruh
> tenaga sampai di atas 8.000 Hz, dan itulah yang hilang pada 16 kHz.
> Kehilangan itu terukur kecil untuk mengenali kata, karena konteks
> menutupnya.
>
> Musik menuntut lebih karena telinga mendengar sampai sekitar 20 kHz dan
> warna nada bergantung pada harmonik tinggi yang tidak bisa ditebak dari
> konteks. Nyquist menuntut $f_s > 40$ kHz, dan 44,1 kHz memberi margin
> untuk tapis yang tidak ideal.
>
> Hubungannya dengan skala mel: telinga memisahkan frekuensi rendah jauh
> lebih halus daripada frekuensi tinggi, kira-kira secara logaritmik di atas
> 1.000 Hz. Jadi separuh atas pita 16 kHz, yaitu 4.000 sampai 8.000 Hz,
> hanya menempati sedikit tapis mel, sedangkan 0 sampai 1.000 Hz menempati
> banyak. Membuang di atas 8.000 Hz murah persis karena wilayah itu memang
> yang paling kasar diwakili. Sesi 2 mengukur berapa tapis mel yang jatuh di
> tiap oktaf.

---

## Yang dibawa ke Sesi 2

| dari sini | dipakai di sana |
| --- | --- |
| teorema konvolusi | STFT sebagai bank tapis, bukan cuma sekumpulan FFT |
| konvolusi melingkar dan penambahan nol | kenapa bingkai dijendela sebelum di-FFT |
| aliasing dan Nyquist | pilihan 16 kHz, dan pemeriksaan laju cuplik mikrofon |
| keterpisahan | kernel waktu dan kernel frekuensi dipisah di Sesi 3 |
| im2col | lapisan konvolusi dilatih tanpa aturan turunan baru di Sesi 3 |
