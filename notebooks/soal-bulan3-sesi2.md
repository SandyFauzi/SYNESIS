# Soal Bulan 3 Sesi 2 - dari sinyal ke gambar

Berkas latihan: [`bulan3_sesi2_spektrogram.py`](bulan3_sesi2_spektrogram.py)

Dua belas TODO. Sesi ini menutup jarak antara "suara adalah 16.000 angka per
detik" dan "suara adalah gambar yang bisa disapu kernel".

> Prasyarat: Sesi 1 dikerjakan dulu. Teorema konvolusi, konvolusi melingkar,
> dan Nyquist dari sana dipakai langsung di sini.

> Data: `E:\SYNESIS\data\speech_commands`, hasil
> `python scripts\unduh_speech_commands.py`. Kalau folder itu belum ada,
> notebook memakai vokal sintetis dan tetap jalan, tetapi angka Bagian 1
> akan berbeda.

---

## Soal 1 - Pra-penekanan: satu baris, dan apa yang dibatalkannya

Bagian 1 memberi:

```text
tenaga bawah dibanding atas, sebelum pra-penekanan :   +7.2 dB
tenaga bawah dibanding atas, sesudah pra-penekanan :   +4.3 dB
```

**1a.** Turunkan tanggapan frekuensi tapis $y[n] = x[n] - a\,x[n-1]$, lalu
tunjukkan bahwa kemiringannya mendekati 6 dB per oktaf di frekuensi rendah.

> **Jawaban:** Tanggapan impulsnya $h = [1, -a]$, jadi
>
> $$H(\omega) = 1 - a e^{-i\omega}, \qquad
> |H(\omega)|^2 = 1 - 2a\cos\omega + a^2.$$
>
> Untuk $\omega$ kecil, $\cos\omega \approx 1 - \omega^2/2$, jadi
>
> $$|H(\omega)|^2 \approx (1-a)^2 + a\,\omega^2.$$
>
> Ketika $a \to 1$, suku $(1-a)^2$ mengecil dan yang tersisa
> $|H| \approx \sqrt{a}\,\omega$, yaitu sebanding dengan $\omega$. Amplitudo
> sebanding $\omega$ berarti naik 6 dB tiap kali $\omega$ berlipat dua, yaitu
> 6 dB per oktaf. Itu persis kebalikan kemiringan $-6$ dB per oktaf dari
> pulsa pita suara, jadi hasil kalinya kira-kira rata.
>
> Dengan $a = 0{,}97$: $|H|$ di 100 Hz (pada 16 kHz, $\omega = 0{,}0393$)
> adalah 0,0489, dan di 4.000 Hz ($\omega = 1{,}571$) adalah 1,393. Selisih
> 29,1 dB sepanjang 5,3 oktaf, yaitu 5,5 dB per oktaf. Cocok dengan ramalan.
>
> Yang terukur di notebook cuma 2,9 dB, dan itu bukan bantahan: ukurannya
> membandingkan JUMLAH tenaga separuh pita bawah dengan separuh pita atas,
> dan separuh pita bawah pada 16 kHz sudah mencakup 0 sampai 4.000 Hz, yaitu
> hampir seluruh tenaga suara. Suatu ukuran yang kasar memang menghasilkan
> selisih yang kecil.

**1b.** Cuplikan pertama tidak punya $x[n-1]$. Notebook memilih meneruskan
$x[0]$ apa adanya. Sebutkan dua pilihan lain dan akibatnya.

> **Jawaban:** Pilihan lain: (i) anggap $x[-1] = 0$, sehingga
> $y[0] = x[0]$ juga, jadi hasilnya identik dengan yang dipakai; (ii) buang
> cuplikan pertama, sehingga sinyalnya memendek satu.
>
> Ketiganya berbeda pada satu cuplikan dari 16.000, jadi akibatnya nol untuk
> pengenalan kata. Yang penting bukan pilihannya melainkan konsistensinya:
> kalau latihan memakai satu cara dan inferensi memakai cara lain, panjang
> sinyalnya berbeda satu dan seluruh kisi bingkai bergeser. Pergeseran itu
> yang menggigit, bukan nilai satu cuplikannya.
>
> Ini kelanjutan langsung dari Soal 1a Sesi 1: mode `full` dengan kernel
> panjang 2 memberi $N+1$ keluaran, mode `same` memberi $N$, mode `valid`
> memberi $N-1$. Notebook memakai `same`.

**1c.** Notebook sengaja tidak menormalisasi amplitudo sinyal. Kapan
keputusan itu salah?

> **Jawaban:** Salah ketika kerasnya suara berkorelasi dengan label karena
> alasan yang tidak ada hubungannya dengan isi ucapan. Contoh yang nyata:
> kalau kamu merekam "hey synesis" sambil mendekatkan mulut ke mikrofon dan
> merekam contoh negatif dari jarak biasa, model akan mempelajari jaraknya,
> bukan katanya, dan akurasi ujinya akan tinggi sementara di pemakaian
> sehari-hari ia gagal.
>
> Amplitudo tetap dibiarkan karena normalisasi yang lebih tepat dikerjakan
> setelah logaritma, yaitu pengurangan rerata di Bagian 7. Di ranah log,
> perubahan kerasnya suara adalah geseran tetap di seluruh koefisien, jadi
> mengurangkan rerata membuangnya seluruhnya tanpa merusak bentuk
> spektrumnya. Menormalisasi di ranah waktu tidak punya sifat itu.

---

## Soal 2 - Matriks Fourier

Bagian 2 memberi:

```text
      N   matriks (ms)    FFT (ms)     rasio   N/log2(N)
   ------------------------------------------------------
    128         0.0848      0.0287       2.9        18.3
   2048         2.0898      0.0313      66.9       186.2
```

**2a.** Rasio terukur selalu di bawah ramalan $N/\log_2 N$. Sebutkan dua
sebabnya, dan ramalkan arah selisihnya kalau $N$ dinaikkan terus.

> **Jawaban:** Sebab pertama: $W x$ dikerjakan BLAS pada bilangan kompleks
> dengan pola akses memori berurutan dan pemanfaatan SIMD penuh, jadi
> konstanta per operasinya kecil. FFT punya pola akses berpasangan
> bertingkat yang lebih ramah cache dalam teori tetapi lebih rumit dalam
> praktik, ditambah ongkos tetap menyusun rencana transformasi.
>
> Sebab kedua: waktu FFT untuk $N$ kecil didominasi ongkos tetap, bukan
> $N\log N$. Terlihat di tabel: dari $N = 128$ ke $N = 256$, waktu FFT
> justru TURUN dari 0,0287 ke 0,0139 ms, yang mustahil kalau yang diukur
> murni kerja algoritmanya. Yang terukur di baris itu sebagian besar
> pemanggilan fungsinya.
>
> Ramalan untuk $N$ besar: rasio terukur akan mendekati $N/\log_2 N$ dari
> bawah dan akhirnya menyalipnya, karena matriksnya berhenti muat di cache.
> $N = 8192$ memberi matriks $8192^2 \times 16$ byte $= 1{,}07$ GB, dan di
> situ perkalian matriksnya jadi terikat lebar pita memori, bukan
> kemampuan hitung.

**2b.** Ortogonalitas $W W^H = N I$ terukur menyimpang $2{,}2\times10^{-14}$.
Apa yang bisa disimpulkan dari angka itu, dan apa yang tidak?

> **Jawaban:** Yang bisa disimpulkan: matriksnya dibangun benar, dan
> penumpukan galat pembulatan sepanjang $N = 256$ suku penjumlahan tetap di
> orde $\sqrt{N}\,\varepsilon$ dengan $\varepsilon \approx 2{,}2\times10^{-16}$.
> $\sqrt{256} \times 2{,}2\times10^{-16} = 3{,}5\times10^{-15}$, dan yang
> terukur satu orde di atasnya. Wajar.
>
> Yang TIDAK bisa disimpulkan: bahwa DFT-nya "benar" dalam arti yang lebih
> berguna. Ortogonalitas cuma memeriksa strukturnya, bukan konvensi tandanya.
> Matriks dengan $+2\pi i$ sebagai ganti $-2\pi i$ juga lolos uji ini, dan ia
> menghitung DFT balik, bukan DFT maju. Pemeriksa yang benar-benar menggigit
> adalah baris di atasnya, yaitu perbandingan langsung dengan `np.fft.fft`.

---

## Soal 3 - Cuping samping jendela kotak, diturunkan

Bagian 3 memberi:

```text
jendela     cuping samping (dB)   lebar cuping utama   gain koheren
-----------------------------------------------------------------
kotak                     -13.3                  2.0          1.000
hann                      -31.5                  4.0          0.500
```

**3a.** Turunkan tingkat cuping samping pertama jendela kotak secara
analitik, dan bandingkan dengan $-13{,}3$ dB.

> **Jawaban:** Transformasi Fourier waktu-diskret jendela kotak panjang $N$
> adalah inti Dirichlet:
>
> $$W(f) = \sum_{n=0}^{N-1} e^{-2\pi i f n}
> = e^{-i\pi f (N-1)} \frac{\sin(\pi f N)}{\sin(\pi f)}.$$
>
> Puncak utamanya di $f = 0$ dengan $|W(0)| = N$. Nolnya di $f = k/N$.
> Cuping samping pertama berada di antara $f = 1/N$ dan $f = 2/N$, dan untuk
> $N$ besar puncaknya mendekati $f = 3/(2N)$. Di situ $\sin(\pi f N) = \pm 1$
> dan $\sin(\pi f) \approx \pi f = 3\pi/(2N)$, jadi
>
> $$|W| \approx \frac{2N}{3\pi} \quad\Longrightarrow\quad
> 20\log_{10}\frac{|W|}{N} = 20\log_{10}\frac{2}{3\pi} = -13{,}46\ \text{dB}.$$
>
> Terukur $-13{,}3$ dB. Selisih 0,16 dB berasal dari hampiran $f = 3/(2N)$;
> puncak sebenarnya sedikit bergeser ke kiri. Angkanya tidak bergantung pada
> $N$, dan itulah sebabnya ia layak dihafal.
>
> Kalau kamu meneruskan ke cuping berikutnya: $f \approx 5/(2N)$ memberi
> $20\log_{10}(2/5\pi) = -17{,}9$ dB, jadi peluruhannya cuma 6 dB per oktaf.
> Sangat lambat, dan itulah cacat utama jendela kotak.

**3b.** Kolom "gain koheren" memberi 1,000 untuk kotak dan 0,500 untuk Hann.
Jelaskan artinya, dan apa yang harus dilakukan kalau kamu mau membandingkan
tinggi puncak antar jendela.

> **Jawaban:** Gain koheren adalah $\frac{1}{N}\sum_n w[n]$, yaitu berapa
> bagian amplitudo sinyal yang lolos. Hann memberi 0,5 karena separuh
> bingkainya ditekan, jadi puncak spektrumnya 6 dB lebih rendah daripada
> jendela kotak untuk sinyal yang sama.
>
> Kalau kamu membandingkan tinggi puncak, bagi hasilnya dengan gain koheren.
> Kalau kamu membandingkan tenaga derau, yang benar bukan itu melainkan gain
> tak-koheren $\sqrt{\frac{1}{N}\sum w[n]^2}$, yang untuk Hann bernilai
> $\sqrt{3/8} = 0{,}612$. Rasio kedua gain itu adalah *equivalent noise
> bandwidth*, dan untuk Hann nilainya 1,5 bin.
>
> Untuk Bulan 3, hal ini tidak menggigit karena Bagian 7 mengurangkan rerata
> tiap koefisien, dan pengurangan itu membuang setiap faktor tetap. Ia
> menggigit kalau kamu melaporkan tingkat tekanan bunyi mutlak, misalnya
> untuk kalibrasi VAD dalam dBFS.

**3c.** Untuk mendeteksi dua nada yang berjarak 30 Hz dengan salah satunya
40 dB lebih lemah, jendela mana yang kamu pilih pada bingkai 25 ms?

> **Jawaban:** Bingkai 25 ms pada 16 kHz adalah $N = 400$, jadi satu bin
> $= 40$ Hz. Dua nada berjarak 30 Hz mendarat di bin yang sama atau
> bersebelahan, dan tidak ada jendela yang bisa memisahkannya. Jawaban yang
> benar adalah menolak premisnya: perpanjang bingkainya.
>
> Untuk memisahkan 30 Hz butuh $\Delta f \le 15$ Hz dengan Hann, yang cuping
> utamanya 4 bin, jadi $\Delta f_{\text{efektif}} = 4 f_s/N \le 30$ memberi
> $N \ge 2133$, yaitu 133 ms. Dengan jendela kotak, cuping utamanya 2 bin
> sehingga $N \ge 1067$ cukup untuk memisahkan, TETAPI cuping sampingnya
> $-13$ dB akan mengubur nada yang 40 dB lebih lemah sepenuhnya. Jadi Hann
> dengan bingkai lebih panjang.
>
> Ini contoh yang tepat untuk melihat bahwa "resolusi" punya dua arti yang
> berbeda dan sering tertukar: kemampuan memisahkan dua puncak yang
> setinggi, dan kemampuan melihat puncak lemah di dekat puncak kuat. Yang
> pertama ditentukan lebar cuping utama, yang kedua ditentukan tingkat cuping
> samping, dan jendela yang baik di satu sisi selalu lebih buruk di sisi
> lain.

---

## Soal 4 - Ketakpastian, dan pilihan 25 milidetik

Bagian 4 memberi $\Delta f \cdot \Delta t = 1{,}00$ untuk semua panjang
bingkai.

**4a.** Tunjukkan bahwa hasil kali itu tetap, lalu nyatakan hubungannya
dengan pertidaksamaan Cauchy-Schwarz yang kamu pakai di Fisika Kuantum.

> **Jawaban:** Dengan $N$ cuplikan pada laju $f_s$: jarak bin
> $\Delta f = f_s/N$ dan durasi bingkai $\Delta t = N/f_s$. Hasil kalinya
> $(f_s/N)(N/f_s) = 1$, tepat, tanpa hampiran.
>
> Hubungannya dengan bentuk kuantum: untuk pasangan Fourier sembarang $f$ dan
> $\hat f$, dengan sebaran didefinisikan sebagai simpangan baku dari rapat
> $|f|^2$ dan $|\hat f|^2$, pertidaksamaan Cauchy-Schwarz memberi
>
> $$\sigma_t\,\sigma_\omega \ge \tfrac{1}{2}.$$
>
> Turunannya tidak menyebut fisika sama sekali; yang dipakai cuma sifat
> transformasi Fourier. Di mekanika kuantum, $p = \hbar k$ mengubahnya jadi
> $\sigma_x \sigma_p \ge \hbar/2$, dan $\hbar$ masuk semata-mata sebagai
> faktor konversi satuan.
>
> Yang dihitung notebook bukan $\sigma$ melainkan lebar kotak, jadi
> tetapannya 1 dan bukan 1/2. Kesamaan tercapai untuk sinyal Gaussian, dan
> itulah kenapa transformasi Gabor memakai jendela Gaussian: ia satu-satunya
> yang mencapai batas bawahnya.

**4b.** Kalau bingkainya 8 ms, apa yang rusak? Kalau 100 ms, apa yang rusak?

> **Jawaban:** Pada 8 ms, $\Delta f = 125$ Hz. Nada dasar suara pria sekitar
> 100 sampai 150 Hz, jadi harmoniknya berjarak kurang dari satu bin dan
> struktur harmoniknya lenyap sepenuhnya. Lebih parah, bingkai 8 ms tidak
> memuat satu periode penuh nada dasar suara pria (satu periode 8 sampai
> 12,5 ms), jadi periodisitasnya tidak terukur dan yang tersisa hanya
> tanggapan sesaat.
>
> Pada 100 ms, $\Delta f = 10$ Hz dan resolusi frekuensinya bagus, tetapi
> satu bingkai memuat beberapa fonem sekaligus. Kata "stop" berdurasi sekitar
> 500 ms dan memuat empat bunyi, jadi bingkai 100 ms merata-ratakan
> seperempat kata. Yang terukur jadi campuran, dan pergeseran formant yang
> membedakan /o/ dari /u/ hilang di dalam rerata.
>
> Rentang 20 sampai 30 ms bukan hasil optimasi melainkan jendela sempit yang
> disisakan kedua batas fisis itu.

**4c.** Loncat 10 ms berarti bingkai bertumpang tindih 60 persen. Kenapa
tidak dibuat tanpa tumpang tindih sama sekali, yang jelas lebih murah?

> **Jawaban:** Tanpa tumpang tindih, kejadian yang jatuh di sambungan dua
> bingkai terpotong jadi dua bagian yang masing-masing lemah, dan jendela
> Hann menekan tepat di sambungan itu, jadi kejadiannya bisa nyaris hilang.
> Pelepasan konsonan letup berdurasi 5 sampai 10 ms; ia muat seluruhnya di
> dalam satu bingkai 25 ms, tetapi hanya kalau ada bingkai yang posisinya
> pas.
>
> Tumpang tindih menjamin bahwa setiap titik waktu tertutup oleh beberapa
> bingkai dengan bobot jendela yang berbeda-beda, jadi selalu ada bingkai
> yang menempatkan kejadian itu di dekat pusatnya. Syarat formalnya
> *constant overlap-add*: jumlah jendela yang digeser harus konstan, dan
> Hann periodik memenuhinya pada loncat $N/2$ dan setiap pembaginya.
>
> Ongkosnya jumlah bingkai berlipat 2,5 kali, dan itu ongkos yang jelas
> sepadan: seluruh spektrogram satu detik cuma 98 kali 257 angka.

---

## Soal 5 - Bank tapis mel

Bagian 5 memberi lebar tapis 93,1 Hz di ujung bawah dan 995,8 Hz di ujung
atas, dan jumlah tapis per oktaf yang hampir rata.

**5a.** Apakah bank tapis mel bisa dibalik? Nyatakan syaratnya dalam bahasa
aljabar linear, lalu jawab untuk bank $40 \times 257$ di notebook.

> **Jawaban:** Bank tapis adalah matriks $B$ berukuran $40 \times 257$ yang
> bekerja sebagai $m = B s$. Membalikkannya berarti memulihkan $s$ dari $m$,
> dan itu mustahil: $B$ memetakan ruang berdimensi 257 ke ruang berdimensi
> 40, jadi ruang nolnya berdimensi paling sedikit 217. Setiap $s$ dalam ruang
> nol itu tidak terlihat sama sekali di $m$.
>
> Yang bisa dilakukan hanya pseudo-invers $B^{+} = B^\top (B B^\top)^{-1}$,
> yang memberi $s$ berenergi terkecil di antara semua yang konsisten dengan
> $m$. Hasilnya terdengar teredam dan "berlubang", karena rincian di dalam
> tiap pita diganti bentuk segitiga tapisnya.
>
> Dan itu belum menyentuh masalah yang lebih besar: $m$ dihitung dari
> $|S|^2$, jadi FASE-nya sudah dibuang lebih dulu. Memulihkan sinyal dari
> besarannya saja memerlukan algoritma iteratif seperti Griffin-Lim, atau
> model vocoder terlatih. Itulah alasan vocoder ada di setiap sistem TTS
> modern, dan alasan Sesi 5 tidak mencoba membalik spektrogram sama sekali.

**5b.** Kenapa tiap tapis dibagi lebarnya? Ramalkan bentuk spektrum mel
kalau normalisasi itu dihapus.

> **Jawaban:** Tanpa normalisasi, tapis yang lebar menjumlahkan lebih banyak
> bin FFT, jadi keluarannya lebih besar semata-mata karena ia lebar. Karena
> lebar tapis naik 10,7 kali dari ujung bawah ke ujung atas, koefisien mel
> tertinggi akan sekitar 10 dB lebih besar daripada yang terendah untuk derau
> putih, yaitu untuk masukan yang sama sekali tidak punya struktur.
>
> Kemiringan palsu itu tetap untuk setiap ucapan, jadi ia tidak merusak
> pembedaan setelah pengurangan rerata di Bagian 7. Yang dirusaknya adalah
> pembacaan manusia atas gambarnya, dan kemampuan model linear yang tidak
> punya bias per koefisien.
>
> Catatan yang jujur: `librosa` memakai normalisasi `slaney` yang persis ini,
> dan `torchaudio` bawaannya TIDAK menormalisasi. Jadi dua pustaka umum
> memberi angka yang berbeda untuk masukan yang sama. Kalau kamu melatih
> dengan satu dan melakukan inferensi dengan yang lain, modelnya rusak tanpa
> satu pun pesan galat. Ini alasan konkret kenapa fungsi fiturnya ditulis
> sendiri dan dibekukan di satu tempat.

**5c.** Tabel memberi 2 tapis di oktaf 125-250 Hz dan 10 tapis di oktaf
4.000-8.000 Hz. Kalau skalanya benar-benar logaritmik, keduanya seharusnya
sama. Jelaskan selisihnya.

> **Jawaban:** Skala mel tidak logaritmik di seluruh jangkauannya. Rumusnya
> $m = 2595\log_{10}(1 + f/700)$, dan suku $+1$ di dalam logaritma membuatnya
> hampir LINEAR untuk $f \ll 700$ Hz: $\log_{10}(1+u) \approx u/\ln 10$.
> Barulah untuk $f \gg 700$ Hz ia berperilaku logaritmik.
>
> Jadi di oktaf 125-250 Hz, mel masih bekerja mendekati linear, dan pita
> selebar 125 Hz hanya kebagian sedikit tapis. Di atas 700 Hz ia logaritmik
> dan tiap oktaf kebagian jumlah tapis yang hampir sama: terukur 7, 9, 10
> untuk tiga oktaf teratas, sudah cukup rata.
>
> Bentuk campuran ini disengaja dan cocok dengan pengukuran psikoakustik:
> telinga memang membedakan nada rendah secara hampir linear, dan barulah di
> atas sekitar 500 Hz beralih ke perilaku logaritmik.

---

## Soal 6 - MFCC, dan hipotesis yang bisa gagal

Bagian 6 memberi:

```text
representasi                  dimensi   |korelasi| rerata
---------------------------------------------------------
log mel                            40               0.599
MFCC penuh                         40               0.193
MFCC dipotong 13                   13               0.317
```

**6a.** Kenapa MFCC yang dipotong 13 justru LEBIH berkorelasi daripada MFCC
penuh?

> **Jawaban:** Ukurannya rerata $|korelasi|$ atas pasangan kolom yang
> berbeda, dan memotong 27 koefisien terakhir membuang pasangan-pasangan yang
> korelasinya paling kecil. Koefisien tinggi menangkap variasi cepat yang
> mendekati derau, dan derau tidak berkorelasi dengan apa pun. Jadi yang
> tersisa punya rerata lebih tinggi hanya karena penyebutnya berubah.
>
> Ini contoh statistik ringkas yang menyesatkan kalau dibaca tanpa
> memperhatikan atas populasi mana ia dihitung. Perbandingan yang adil
> membandingkan 13 kolom pertama MFCC dengan 13 kolom log-mel yang mana pun,
> dan di situ MFCC tetap menang telak.

**6b.** Nyatakan ramalan "untuk CNN, log-mel mengalahkan MFCC" sebagai
hipotesis yang bisa gagal, lengkap dengan angka yang akan membantahnya.

> **Jawaban:** Hipotesis: dengan arsitektur, data, dan anggaran latihan yang
> sama, CNN yang dilatih di atas log-mel 40 dimensi mencapai akurasi uji
> lebih tinggi daripada CNN yang dilatih di atas MFCC 13 dimensi, dan
> selisihnya melampaui selang kepercayaan 95 persen dari himpunan ujinya.
>
> Himpunan uji Speech Commands untuk 12 kelas berisi sekitar 4.890 ucapan.
> Pada $p \approx 0{,}9$, lebar selang 95 persennya
> $2 \cdot 1{,}96\sqrt{0{,}9 \cdot 0{,}1/4890} = 1{,}7$ poin. Jadi selisih di
> bawah 1,7 poin TIDAK menghitung, dan hipotesisnya cuma didukung kalau
> log-mel menang lebih dari itu.
>
> Yang akan membantahnya: MFCC menang, atau selisihnya di bawah 1,7 poin.
> Kemungkinan ketiga yang harus disiapkan sejak sekarang: log-mel menang
> tetapi hanya karena dimensinya tiga kali lebih besar, bukan karena
> strukturnya. Pengendaliannya adalah menjalankan MFCC 40 koefisien penuh
> sebagai baris ketiga. Kalau MFCC 40 menyusul log-mel 40, maka yang berperan
> jumlah dimensi; kalau tidak, yang berperan strukturnya.
>
> Berbeda dengan Bulan 2, di sini $n = 4890$ dan bukan 41, jadi untuk pertama
> kalinya selisih beberapa poin benar-benar bisa dibaca.

**6c.** Kalau DCT merusak struktur lokal untuk CNN, kenapa JPEG memakai DCT
padahal gambar juga punya struktur lokal?

> **Jawaban:** Karena JPEG memakainya untuk tujuan yang berlawanan. JPEG
> mengompresi: ia ingin tenaga terkumpul di sedikit koefisien supaya sisanya
> bisa dikuantisasi kasar dan dibuang. Struktur lokal justru yang dikorbankan
> dengan sengaja, dan artefak blok $8\times8$ yang terlihat di gambar JPEG
> berkualitas rendah adalah harga yang dibayar secara sadar.
>
> CNN tidak mengompresi. Ia mencari pola, dan pola yang dicarinya
> didefinisikan oleh kedekatan: kernel $3\times3$ mengasumsikan bahwa tiga
> nilai bersebelahan memang bertetangga. DCT mengubah sumbu jadi indeks
> frekuensi, dan koefisien ke-3 tidak "bertetangga" dengan koefisien ke-4
> dalam arti apa pun yang berguna untuk kernel.
>
> Ringkasnya: dekorelasi berguna kalau modelmu mengasumsikan kebebasan, dan
> merugikan kalau modelmu memanfaatkan ketergantungan. Model campuran
> Gaussian termasuk yang pertama; CNN termasuk yang kedua.

---

## Soal 7 - Anggaran fitur untuk wake word

Bagian 7 memberi:

```text
fitur                               bentuk   angka/detik
--------------------------------------------------------
sinyal mentah                   (16000, 1)        16.000
log-mel                           (98, 40)         3.920
MFCC 13                           (98, 13)         1.274
log-mel + delta + delta2         (98, 120)        11.760
```

**7a.** Wake word "hey synesis" berdurasi sekitar 1,2 detik. Hitung dimensi
masukan model untuk keempat baris di atas, dan sebutkan mana yang layak
dilatih dari 200 contoh rekaman.

> **Jawaban:** Pada 1,2 detik: sinyal mentah 19.200; log-mel
> $118 \times 40 = 4.720$; MFCC $118 \times 13 = 1.534$; log-mel plus delta
> $118 \times 120 = 14.160$.
>
> Dengan 200 contoh, tidak satu pun layak dilatih dengan model padat: 200
> contoh untuk 1.534 dimensi saja sudah kurang tujuh kali lipat, dan
> aturan kasar yang biasa dipakai meminta paling sedikit sepuluh contoh per
> dimensi.
>
> Yang membuatnya mungkin adalah berbagi bobot dari Soal 3 Sesi 1. CNN
> dengan 8 kernel $3\times3$ punya 72 bobot di lapisan pertama, bukan 4.720,
> dan jumlah bobotnyalah yang menentukan berapa contoh yang dibutuhkan,
> bukan dimensi masukannya. Itulah kenapa Sesi 3 mengerjakan CNN sebelum
> Sesi 4 mengumpulkan rekaman: urutannya bukan selera.
>
> Jalan kedua, dan yang benar-benar dipakai di Sesi 4: jangan melatih dari
> nol. Latih pengenal 12 kata dari Speech Commands yang punya puluhan ribu
> contoh, lalu ganti lapisan terakhirnya saja dengan dua kelas.

**7b.** Delta menambah dimensi tiga kali lipat. Rancang percobaan yang
memutuskan apakah tambahan itu sepadan untuk CNN, dan sebutkan apa yang
membuat percobaan itu tidak sahih.

> **Jawaban:** Percobaannya: arsitektur, seed, jumlah epoch, dan belahan data
> dipatok sama; satu-satunya yang berubah masukannya, 40 kanal lawan 120
> kanal. Ukurannya akurasi di himpunan uji yang sama, dan keputusannya
> memakai selang 1,7 poin dari Soal 6b.
>
> Yang membuatnya tidak sahih:
>
> 1. Jumlah parameter ikut berubah, karena lapisan pertama sekarang membaca
>    120 kanal. Modelnya jadi lebih besar, dan kalau ia menang kita tidak tahu
>    apakah karena delta atau karena kapasitasnya. Pengendaliannya:
>    seimbangkan jumlah parameter dengan mengurangi kanal keluaran.
> 2. Kalau normalisasi dikerjakan setelah delta dihitung, maka jalur 120
>    kanal mendapat normalisasi yang berbeda. Urutan operasinya harus persis
>    sama.
> 3. Satu kali latihan tidak cukup. Selisih antar seed pada CNN kecil bisa
>    mencapai satu poin, jadi minimal tiga seed dan yang dilaporkan
>    mediannya.
>
> Ramalan yang saya catat sebelum mengukurnya, supaya bisa salah: delta tidak
> membantu, selisihnya di bawah 1,7 poin, karena kernel yang menyapu sumbu
> waktu bisa mempelajari turunan itu sendiri dan Sesi 1 sudah menunjukkan
> bentuk kernelnya, yaitu $[-1, 0, 1]$.

---

## Yang dibawa ke Sesi 3

| dari sini | dipakai di sana |
| --- | --- |
| `fitur_audio` yang dibekukan | masukan CNN, tanpa versi kedua yang diam-diam berbeda |
| log-mel lawan MFCC | hipotesis Soal 6b diuji dengan angka |
| ketakpastian waktu-frekuensi | alasan kernel waktu dan kernel frekuensi dipisah |
| sumbu frekuensi tidak stasioner | alasan kernel tidak dibagi sepanjang sumbu itu |
