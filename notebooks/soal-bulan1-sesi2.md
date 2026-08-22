# Soal Bulan 1 Sesi 2 - Neuron, Layer, MLP

Berkas latihan: [`bulan1_sesi2_mlp.py`](bulan1_sesi2_mlp.py)

Sesi 1 kamu menulis mesin yang bisa menurunkan ekspresi apa pun. Malam ini
mesin itu dipakai untuk sesuatu yang bentuknya jaringan, bukan rumus.

Tidak ada satu pun `import torch` di berkas ini.

> Catatan: tiga jawaban Sesi 1 masih menunggu perbaikan, yaitu 2b, 5a, dan 4c.
> Kerjakan itu dulu kalau belum, karena 2b menyangkut `+=` yang dipakai
> seluruh sesi ini.

---

## Soal 1 - Kenapa bobot tidak boleh mulai dari nol

`Neuron.__init__` mengacak bobot tapi memulai geseran dari nol.

**1a.** Bayangkan semua bobot di satu lapisan dimulai dari nol. Hitung
keluaran tiap neuron di lapisan itu untuk masukan yang sama. Apa yang kamu
dapat?

**1b.** Sekarang hitung gradiennya. Kalau keluaran semua neuron sama, apakah
gradien tiap neuron juga sama?

**1c.** Simpulkan: berapa banyak neuron yang sebenarnya kamu punya di lapisan
berisi 8 neuron yang semua bobotnya mulai dari nol?

**1d.** Kenapa geseran boleh dimulai dari nol padahal bobot tidak?

<details>
<summary>Petunjuk 1</summary>

Kalau dua neuron identik dan menerima masukan identik, mereka menghasilkan
keluaran identik dan menerima gradien identik. Jadi mereka diperbarui secara
identik, selamanya. Delapan neuron yang selalu sama persis itu satu neuron
dengan biaya delapan kali lipat.

Namanya symmetry breaking. Yang perlu berbeda cuma satu hal per neuron, dan
bobotlah yang mengalikan masukan sehingga perbedaannya terbawa.
</details>

---

## Soal 2 - Dari mana angka 2 di sqrt(2/n)

Skala acak yang dipakai adalah $\sqrt{2/n_\text{masuk}}$.

**2a.** Anggap tiap masukan $x_i$ punya ragam 1 dan saling bebas, dan bobot
$w_i$ diambil dari sebaran berpusat nol dengan ragam $\sigma^2$. Hitung ragam
dari $z = \sum_i w_i x_i$.

**2b.** Kamu ingin ragam $z$ tetap 1, supaya sinyalnya tidak mengecil atau
membesar tiap melewati lapisan. Berapa $\sigma^2$ yang dibutuhkan?

**2c.** Jawaban 2b memberi $1/n$, bukan $2/n$. Angka 2 itu datang dari relu.
Kalau $z$ tersebar simetris di sekitar nol, berapa bagian yang lolos melewati
relu, dan apa akibatnya pada ragam keluaran?

**2d.** Uji ramalanmu. Buat lapisan berisi 200 neuron dengan 50 masukan,
beri masukan acak berragam 1, lalu ukur ragam keluarannya. Bandingkan skala
$\sqrt{1/n}$ dan $\sqrt{2/n}$.

<details>
<summary>Petunjuk 2c</summary>

Relu membuang separuh sebarannya, jadi ragam keluarannya kira-kira separuh
ragam masukan. Untuk menggantinya, ragam bobot dinaikkan dua kali lipat.

Itu satu-satunya isi inisialisasi He. Bukan sihir, cuma mengganti separuh
yang dibuang tekukan.
</details>

---

## Soal 3 - Kenapa lapisan terakhir tanpa tekukan

**3a.** Buktikan dalam tiga baris bahwa menumpuk dua lapisan linear tanpa
tekukan menghasilkan satu lapisan linear. Mulai dari $z_2 = W_2(W_1 x + b_1) + b_2$.

**3b.** Dari 3a, jelaskan apa sebenarnya yang disumbangkan relu. Tanpa relu,
berapa lapis pun yang kamu tumpuk setara dengan berapa lapis?

**3c.** Sekarang alasan lapisan terakhir. Kalau keluaran akhir dilewatkan
relu, nilai apa yang tidak akan pernah bisa dikeluarkan model? Kenapa itu
merusak untuk rugi engsel yang dipakai di sini?

**3d.** Uji: ubah `MLP.__init__` supaya lapisan terakhir ikut memakai relu,
jalankan Bagian 4, catat akurasinya.

---

## Soal 4 - Kenapa garis lurus mustahil di sini

Bagian 4 memberi:

```text
Akurasi akhir garis lurus : 65.0 persen
Akurasi akhir 8 neuron    : 100.0 persen
```

**4a.** Buktikan bahwa tidak ada garis lurus yang bisa memisahkan cincin dalam
dari cincin luar. Cukup satu paragraf, dan tidak perlu aljabar berat.

**4b.** Kalau kamu boleh menambah **satu** fitur turunan ke masukan, yaitu
$x_0^2 + x_1^2$, apakah garis lurus jadi bisa? Gambarkan apa yang terjadi pada
datanya di ruang tiga dimensi itu.

**4c.** Bandingkan dua cara menyelesaikan masalah ini: menambah fitur buatan
tangan seperti 4b, atau menambah lapisan tersembunyi. Apa yang kamu bayar dan
apa yang kamu dapat di masing-masing?

<details>
<summary>Petunjuk 4a</summary>

Garis lurus membelah bidang jadi dua bagian, dan tiap bagian adalah himpunan
cembung. Ambil dua titik pada cincin luar yang saling berseberangan lewat
pusat. Garis penghubung keduanya melewati pusat, dan di pusat itu ada titik
cincin dalam.
</details>

<details>
<summary>Petunjuk 4c</summary>

4b berhasil karena kamu sudah tahu jawabannya. Kamu tahu datanya berbentuk
lingkaran, jadi kamu tahu $r^2$ adalah fitur yang tepat.

Lapisan tersembunyi tidak diberi tahu apa-apa. Ia menemukan sendiri sekumpulan
lipatan yang cukup. Harganya: kamu tidak lagi bisa menjelaskan fiturnya dalam
satu kalimat.

Ini pertukaran yang akan kamu temui berulang kali sampai Bulan 6.
</details>

---

## Soal 5 - Neuron mati

Bagian 5B memberi:

```text
    lr   neuron mati     akurasi
  0.15      0 dari 8      100.0%
   3.0      0 dari 8      100.0%
   8.0      8 dari 8       50.0%
```

**5a.** Jelaskan mekanismenya. Kenapa satu langkah besar bisa membunuh sebuah
neuron secara permanen, sementara langkah besar pada model linear Bulan 0
cuma membuatnya berayun lalu pulih?

**5b.** Akurasi di baris terakhir tepat 50 persen. Kenapa persis angka itu,
dan apa yang sebenarnya dikeluarkan model saat semua neuronnya mati?

**5c.** Sebutkan tiga cara mencegahnya, dan untuk tiap cara sebutkan apa yang
kamu korbankan.

**5d.** Bagian 5B memakai seed tetap dan cuma mengubah lr. Kenapa itu penting
untuk kesimpulannya? Apa yang tidak bisa kamu simpulkan kalau seed-nya ikut
berubah?

<details>
<summary>Petunjuk 5a</summary>

Turunan relu di daerah negatif bukan kecil. Ia nol.

Nol bukan angka kecil yang bisa pulih. Nol berarti tidak ada informasi yang
mengalir balik ke bobot itu selamanya, tak peduli seberapa salah keluarannya.
Di Bulan 0 tidak ada operasi yang gradiennya bisa nol permanen.
</details>

---

## Soal 6 - Rugi engsel, dan yang belum ada di mesinmu

`rugi_engsel` memakai `max(0, 1 - y * ramalan)`.

**6a.** Kenapa rugi engsel yang dipakai, bukan entropi silang seperti di
Bulan 2? Petunjuknya ada di operasi yang tersedia di kelas `Value`-mu.

**6b.** Untuk memakai entropi silang, kamu butuh `exp` dan `log`. Tulis
keduanya sebagai metode `Value`, lengkap dengan `_backward`-nya. Turunkan
dulu turunan lokalnya di kertas.

**6c.** Uji keduanya dengan beda hingga, mengikuti pola Bagian 2 Sesi 1.
Sebutkan nilai `a` yang kamu pilih untuk menguji `log` dan kenapa tidak boleh
memilih `a = 0`.

**6d.** Rugi engsel bernilai nol untuk semua titik yang sudah benar dengan
margin cukup. Apa akibatnya pada gradien, dan kenapa itu justru berguna?

---

## Soal 7 - Batas keputusan itu poligon

Buka `figures/bulan1_sesi2_batas.png`.

**7a.** Batas hijaunya melengkung dari jauh, tapi kalau diikuti pelan-pelan ia
tersusun dari ruas lurus yang bertemu di sudut. Jelaskan kenapa harus begitu,
dari sifat relu.

**7b.** Model itu punya 8 neuron tersembunyi. Hitung berapa sudut yang kamu
lihat di batasnya. Apakah jumlahnya cocok dengan 8? Kalau tidak, kenapa bisa
kurang?

**7c.** Ramalkan bentuk batasnya kalau neuron tersembunyi dinaikkan jadi 32.
Lalu jalankan dan bandingkan dengan ramalanmu.

**7d.** Model relu tidak pernah menghasilkan lengkungan sejati, satu pun. Tapi
ia bisa mendekati lingkaran sedekat yang kamu mau. Jelaskan bagaimana dua
kalimat itu bisa sama-sama benar.

---

## Soal 8 - Ongkos, dan dinding di depan

Bagian 7 mencetak jumlah objek `Value` dan waktu satu iterasi.

**8a.** Catat angkanya. Lalu hitung: berapa lama satu epoch MNIST dengan
jaringan 784-32-10 pada 60000 gambar, kalau ongkos per objek sama?

**8b.** Dari Sesi 1 kamu sudah tahu batas rekursi mesinmu 996, dan bahwa
kedalaman kira-kira `n_masuk + n_sembunyi`. Untuk 784-32-10, apakah kamu
menabrak batas itu? Hitung.

**8c.** Untuk 784-256-10 bagaimana? Ini yang akan kamu tabrak di Sesi 3.

**8d.** Sebutkan dua perbaikan yang mungkin, dan urutkan mana yang harus
dikerjakan lebih dulu. Ingat bahwa memperbaiki yang salah lebih dulu berarti
kamu tetap menabrak dinding satunya.

<details>
<summary>Petunjuk 8d</summary>

Satu dinding soal waktu, satu soal kedalaman tumpukan. Keduanya independen,
dan memperbaiki satu tidak menolong satunya.

Yang soal kedalaman punya perbaikan yang benar dan perbaikan yang menunda
masalah. Menaikkan `sys.setrecursionlimit` termasuk yang menunda.
</details>

---

## Tolok Ukur Bulan 1 Sesi 2

- [ ] `Neuron`, `Layer`, `MLP` ditulis sendiri di atas kelas `Value` buatanmu
- [ ] Tidak ada `import torch` di mana pun
- [ ] Bagian 3 lolos, galat gradien di bawah `1e-5` untuk 17 parameter
- [ ] Alasan bobot tidak boleh nol semua bisa dijelaskan tanpa membuka catatan
- [ ] Angka 2 pada `sqrt(2/n)` diturunkan sendiri, dan diuji di 2d
- [ ] Tumpukan lapisan linear dibuktikan setara satu lapisan linear
- [ ] Mustahilnya garis lurus di cincin sepusat dibuktikan, bukan diterima
- [ ] Kematian neuron di `lr = 8` diamati sendiri, dan mekanismenya dipahami
- [ ] `exp` dan `log` ditambahkan ke `Value`, diuji dengan beda hingga
- [ ] Sudut pada batas keputusan dihitung dan dibandingkan dengan jumlah neuron
- [ ] Dua dinding Sesi 3 dihitung sendiri, dan urutan perbaikannya diputuskan

Kalau kesebelas kotak beres, Sesi 3 melatih ini di MNIST, dan kedua dinding
itu akan menabrakmu sungguhan.
