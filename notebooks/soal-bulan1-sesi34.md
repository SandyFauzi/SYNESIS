# Soal Bulan 1 Sesi 3+4 - MNIST, dua dinding, optimizer

Berkas latihan: [`bulan1_sesi34_mnist.py`](bulan1_sesi34_mnist.py)

Sembilan TODO. Sesi 3 dan Sesi 4 digabung, karena keduanya berpusat pada
pertanyaan yang sama: apa yang sebenarnya mahal, dan apa yang sebenarnya
menolong.

Data MNIST dibaca dari `E:\SYNESIS\data`. Sudah ada di sana.

> Prasyarat dari Sesi 2 yang sudah kamu bereskan: inisialisasi He yang benar,
> dan `exp` serta `log` di kelas `Value`. Bagian 1 memakai keduanya.

---

## Soal 1 - Kenapa gradiennya jadi p minus y

Bagian 1 memberi selisih `1.11e-16` antara gradien autograd dan `p - y`.

**1a.** Turunkan sendiri di kertas. Mulai dari

$$L = -\log p_k, \qquad p_i = \frac{e^{z_i}}{\sum_j e^{z_j}}$$

Hitung $\partial L / \partial z_i$ untuk dua kasus terpisah: $i = k$ dan
$i \neq k$. Tunjukkan keduanya bisa ditulis dalam satu baris sebagai
$p_i - y_i$ dengan $y$ vektor one-hot.

**1b.** Kenapa mengurangi $\max_j z_j$ dari semua $z$ tidak mengubah $p$ sama
sekali? Tunjukkan aljabarnya, satu baris.

**1c.** Kalau `m` di TODO 1 kamu ambil sebagai `Value` alih-alih float biasa,
apakah hasil `rugi.data` berubah? Apakah gradiennya berubah? Coba, lalu
jelaskan mana yang berubah dan kenapa.

**1d.** Gradien kelas yang benar bertanda negatif, sembilan lainnya positif.
Jumlahkan kesepuluh gradien itu. Berapa hasilnya, dan kenapa harus begitu?

<details>
<summary>Petunjuk 1d</summary>

$\sum_i p_i = 1$ dan $\sum_i y_i = 1$.

Akibatnya softmax tidak bisa menaikkan semua logit sekaligus. Ia cuma bisa
memindahkan peluang dari satu kelas ke kelas lain. Itu sifat yang tidak
dimiliki sigmoid per-kelas, dan itu alasan softmax dipakai untuk klasifikasi
yang jawabannya cuma satu.
</details>

---

## Soal 2 - Dua dinding, dan kenapa urutannya penting

Bagian 2 memberi:

```text
784-32-10, 25.450 parameter
satu epoch 50000    : 6.2 jam
784-256-10 : RecursionError: maximum recursion depth exceeded
```

**2a.** Bagian 3 menghapus dinding rekursi tanpa memperbaiki waktu sedikit
pun. Jelaskan kenapa keduanya benar-benar independen, dari sifat masing-masing
perbaikan.

**2b.** `sys.setrecursionlimit(5000)` juga membuat 784-256-10 berjalan.
Sebutkan apa yang terjadi kalau kamu memakai itu lalu menaikkan lapisan
tersembunyi jadi 4096. Kenapa kegagalannya lebih buruk daripada
`RecursionError`?

**2c.** Bagian 3 mencetak `parameter bergradien : 24.613 dari 203.530`. Cuma
seperdelapan parameter yang gradiennya bukan nol. Jelaskan kenapa, dari sifat
gambar MNIST. (Bukan neuron mati. Sebabnya di masukan.)

**2d.** Dari 2c: kalau kamu melatih dengan satu gambar per langkah, berapa
bagian jaringan yang benar-benar belajar tiap langkah? Apa akibatnya pada
pilihan ukuran batch?

---

## Soal 3 - Backward iteratif

**3a.** Versi rekursif dan versi iteratifmu memberi gradien yang sama persis,
selisih `0.000e+00`. Jelaskan kenapa harus sama persis, bukan sekadar dekat.

**3b.** Di TODO 2 kamu mendorong pasangan `(simpul, sudah_ditelusuri)` ke
tumpukan. Kenapa penandanya perlu? Coba hapus penanda itu dan jelaskan
urutan seperti apa yang kamu dapat.

**3c.** Kamu memakai `set` berisi `id(v)`. Sesi 1 memakai `set` berisi objek
`Value` langsung. Keduanya jalan. Sebutkan satu keadaan di mana keduanya
berbeda perilakunya.

**3d.** Berapa kedalaman tumpukan yang dipakai versi iteratifmu? Nyatakan
dalam O-besar, dan bandingkan dengan versi rekursif.

---

## Soal 4 - Tensor, dan gradien yang bentuknya harus cocok

**4a.** Untuk `out = A @ B` dengan A berbentuk $(B, n)$ dan B berbentuk
$(n, m)$: turunkan `A.grad` dan `B.grad` dari aturan rantai. Tunjukkan cuma
ada satu susunan perkalian yang bentuknya benar untuk masing-masing.

**4b.** Di TODO 4, gradien geseran adalah jumlah atas baris batch, bukan
rata-rata. Buktikan itu dari aturan rantai. Lalu jelaskan kenapa mengganti
`sum` dengan `mean` menghasilkan model yang tetap belajar tapi salah, dan
seberapa salah.

**4c.** `entropi_silang` membagi gradien dengan `B`. Kalau pembagian itu
dihapus, apa yang berubah? Apakah ada nilai laju belajar yang membuatnya
setara lagi? Kalau ada, berapa.

**4d.** Bagian 4 mengadu 59 parameter dengan beda hingga dan lolos di
`2.79e-10`. Kenapa uji ini tetap perlu padahal kamu sudah menulis aturannya
dari turunan yang benar di kertas?

---

## Soal 5 - Ongkos

Bagian 5 dan 6 memberi kira-kira:

```text
Value, sebutir            6.2 jam         1x
Tensor, numpy             4.5 dtk      5015x
PyTorch CPU               1.4 dtk         3.3x lawan numpy
PyTorch GPU               1.4 dtk         3.2x lawan numpy
```

**5a.** Hitung berapa perkalian titik-mengambang yang dikerjakan satu epoch
784-128-10 pada 50000 gambar, maju dan mundur. Bandingkan dengan waktu numpy
yang terukur untuk mendapat GFLOPS efektifnya.

**5b.** Ubah `Tensor` supaya memakai `float32`, jalankan ulang Bagian 5, catat
waktunya. Berapa bagian dari selisih numpy lawan PyTorch yang terjelaskan?

**5c.** GPU tidak menang di tabel itu. Naikkan `batch` di `latih_mnist` dan di
Bagian 6 secara bersamaan sampai GPU menang, lalu catat di batch berapa
titik baliknya. Jelaskan dari mana ongkos tetap itu datang.

**5d.** Rasio 5000x antara Value dan numpy tidak berasal dari aritmetika,
karena jumlah perkalian keduanya sama. Sebutkan tiga sumber ongkosnya, dan
urutkan dari yang terbesar menurutmu.

---

## Soal 6 - Validasi yang benar-benar dipakai

Bagian 5 memberi:

```text
akurasi uji, epoch terakhir : 96.03 persen
akurasi uji, epoch pilihan  : 97.27 persen   (epoch 6, dipilih lewat validasi)
```

**6a.** Selisihnya 1,24 persen. Jelaskan dari mana selisih itu datang, dan
kenapa epoch terakhir bukan pilihan yang baik.

**6b.** Kenapa epoch pilihan tidak boleh dipilih memakai himpunan uji?
Jawaban "karena itu curang" tidak cukup. Sebutkan apa persisnya yang jadi
tidak valid dan bagi siapa.

**6c.** Akurasi validasi di epoch 6 adalah 97,32 dan akurasi ujinya 97,27.
Angka mana yang boleh kamu laporkan sebagai ramalan untuk data baru, dan
kenapa yang satunya tidak.

**6d.** Kamu memilih satu hyperparameter (epoch) dari 8 kandidat memakai
validasi 10000 gambar. Kalau kamu memilih dari 5000 kandidat, apa yang mulai
rusak? Perkirakan besarannya.

---

## Soal 7 - Optimizer, dan osilator teredam

Bagian 7 memberi:

```text
bilangan kondisi : 484.0
ambang SGD, 2/lam_max : 0.016103

optimizer     lr terbaik   rugi akhir   iterasi ke 1%
SGD polos        0.01585     1.515682               -
momentum         0.01585     1.500141              63
RMSprop          0.01995     1.508664             255
Adam             5.01187     1.500141              52
```

**7a.** `lr terbaik` SGD adalah 0,01585 dan ambangnya 0,016103. Jaraknya
kurang dari 2 persen. Jelaskan kenapa sapuan memilih nilai yang nyaris tepat
di tepi jurang, dan apa artinya untuk memilih laju belajar di praktik.

**7b.** Momentum dan SGD memakai laju belajar yang sama persis di tabel itu,
tapi satu tiba dan satu tidak. Dari persamaan osilator teredam, turunkan
faktor percepatan efektif momentum untuk `beta = 0.9`. Cocokkan dengan
angkanya.

**7c.** Laju belajar terbaik Adam adalah 5,01, tiga ratus kali lebih besar
dari SGD. Jelaskan kenapa itu tidak melanggar ambang `2/lam_max`. Petunjuknya
ada di penyebut Adam.

**7d.** RMSprop kalah dari momentum di lanskap ini. Buat satu lanskap di mana
RMSprop menang, jalankan, dan tunjukkan angkanya. Lalu sebutkan sifat lanskap
apa yang menentukan siapa menang.

<details>
<summary>Petunjuk 7b</summary>

Untuk kuadratik dengan eigen $\lambda$, SGD mengecilkan galat dengan faktor
$|1 - \eta\lambda|$ tiap langkah. Momentum dengan $\beta$ mengubahnya jadi
rekurensi orde dua, dan akar karakteristiknya berukuran $\sqrt{\beta}$ pada
rezim teredam-kurang.

Bandingkan berapa langkah yang dibutuhkan masing-masing untuk mengecilkan
galat di sumbu terlandai dengan faktor yang sama.
</details>

<details>
<summary>Petunjuk 7d</summary>

Momentum menolong waktu arah gradien konsisten tapi skalanya timpang secara
seragam. RMSprop menolong waktu tiap sumbu punya skala gradien yang
berbeda-beda dan berubah-ubah sepanjang lintasan.

Lanskap kuadratik murni menguntungkan momentum. Yang menguntungkan RMSprop
adalah yang skalanya tidak tetap, misalnya rugi yang mengandung suku
berpangkat empat di satu sumbu saja.
</details>

---

## Soal 8 - Menutup Bulan 1

**8a.** Sebutkan tiga hal yang mesin `Value`-mu bisa lakukan tapi `Tensor`-mu
tidak. Lalu sebutkan kenapa PyTorch memilih jalan `Tensor`.

**8b.** Sepanjang Bulan 1 kamu menabrak empat kegagalan yang bentuknya
berbeda: gradien salah tanpa error, neuron mati permanen, batas rekursi, dan
lambat yang tidak bisa ditunggu. Untuk tiap-tiapnya, sebutkan alat yang
menangkapnya.

**8c.** Kamu sekarang punya dua mesin autograd tulisan sendiri, satu
per-angka dan satu per-array. Untuk SYNESIS, keduanya tidak akan dipakai
melatih apa pun. Jelaskan apa yang tetap kamu dapat dari menulisnya, dalam
kalimat yang bukan basa-basi.

---

## Tolok Ukur Bulan 1 Sesi 3+4

- [ ] `dL/dz = p - y` diturunkan sendiri di kertas, bukan diterima
- [ ] Softmax dan entropi silang jalan di atas kelas `Value` buatanmu
- [ ] Dinding waktu dan dinding rekursi dua-duanya ditabrak sungguhan
- [ ] `backward` iteratif ditulis sendiri, dan hasilnya identik dengan rekursif
- [ ] Empat aturan turunan `Tensor` lolos uji beda hingga di bawah `1e-5`
- [ ] MNIST di atas 95 persen dengan mesin buatan sendiri, nol `torch.nn`
- [ ] Epoch dipilih lewat validasi, dan bedanya dengan epoch terakhir dicatat
- [ ] Rasio kecepatan lawan PyTorch diukur, dan sebabnya bisa dijelaskan
- [ ] `float32` diuji, dan bagiannya dalam selisih itu dihitung
- [ ] SGD-momentum, RMSprop, dan Adam ditulis tangan dan dibandingkan di lr terbaiknya masing-masing
- [ ] Hubungan momentum dengan osilator teredam bisa dijelaskan tanpa catatan
- [ ] Satu lanskap di mana RMSprop menang dibuat sendiri dan ditunjukkan

Kalau kedua belas kotak beres, Bulan 1 tutup. Bulan 2 sudah menunggu di
`soal-bulan2-sesi1.md`.
