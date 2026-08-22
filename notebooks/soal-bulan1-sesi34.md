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

> **Jawaban:** Tulis $S=\sum_j e^{z_j}$, sehingga
> $L=-z_k+\log S$. Jika $i=k$,
> $\partial L/\partial z_k=-1+e^{z_k}/S=p_k-1$. Jika $i\ne k$,
> $\partial L/\partial z_i=e^{z_i}/S=p_i$. Karena $y_k=1$ dan
> $y_i=0$ untuk $i\ne k$, keduanya menjadi
> $\boxed{\partial L/\partial z_i=p_i-y_i}$.

**1b.** Kenapa mengurangi $\max_j z_j$ dari semua $z$ tidak mengubah $p$ sama
sekali? Tunjukkan aljabarnya, satu baris.

> **Jawaban:** Untuk $m=\max_j z_j$,
> $\frac{e^{z_i-m}}{\sum_j e^{z_j-m}}=
> \frac{e^{-m}e^{z_i}}{e^{-m}\sum_j e^{z_j}}=p_i$.

**1c.** Kalau `m` di TODO 1 kamu ambil sebagai `Value` alih-alih float biasa,
apakah hasil `rugi.data` berubah? Apakah gradiennya berubah? Coba, lalu
jelaskan mana yang berubah dan kenapa.

> **Jawaban:** Tidak secara matematis. Uji memberi `rugi.data` identik
> `1.8358831657033847`; selisih gradien maksimum hanya
> `2.22e-16`. Grafnya berubah: logit maksimum mendapat jalur gradien tambahan
> melalui `m`, tetapi jumlah turunan terhadap pergeseran bersama itu nol
> karena softmax invarian terhadap pergeseran. Sisa beda hanya pembulatan.
> Memakai float menghindari graf dan pembatalan yang tidak berguna.

**1d.** Gradien kelas yang benar bertanda negatif, sembilan lainnya positif.
Jumlahkan kesepuluh gradien itu. Berapa hasilnya, dan kenapa harus begitu?

> **Jawaban:** Hasil ukur `2.11e-16`, yaitu nol dalam batas `float64`.
> Aljabarnya $\sum_i(p_i-y_i)=\sum_i p_i-\sum_i y_i=1-1=0$.
> Menambah konstanta sama ke semua logit memang tidak boleh mengubah rugi.

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

> **Jawaban:** Backward iteratif hanya memindahkan penyusunan urutan
> topologis dari call stack Python ke `list`. Jumlah objek `Value`, operasi
> skalar, dan simpul graf tetap sama, jadi waktu hampir tetap. Vektorisasi
> `Tensor` mengurangi kerja Python per angka, tetapi tidak otomatis mengubah
> kedalaman call stack versi rekursif.

**2b.** `sys.setrecursionlimit(5000)` juga membuat 784-256-10 berjalan.
Sebutkan apa yang terjadi kalau kamu memakai itu lalu menaikkan lapisan
tersembunyi jadi 4096. Kenapa kegagalannya lebih buruk daripada
`RecursionError`?

> **Jawaban:** Kedalaman graf mendekati/melewati 5000. Jika limit terus
> dinaikkan, stack native OS dapat habis lebih dulu. Hasilnya proses mati
> (`stack overflow`/access violation), bukan exception Python yang bisa
> ditangkap. Karena itu lebih buruk daripada `RecursionError` yang aman dan
> memberi pesan.

**2c.** Bagian 3 mencetak `parameter bergradien : 24.613 dari 203.530`. Cuma
seperdelapan parameter yang gradiennya bukan nol. Jelaskan kenapa, dari sifat
gambar MNIST. (Bukan neuron mati. Sebabnya di masukan.)

> **Jawaban:** Mayoritas piksel MNIST hitam, jadi $x_i=0$. Gradien bobot
> pertama adalah $\partial L/\partial W_{ij}=x_i\delta_j$; semua 256 bobot
> dari piksel hitam mendapat nol. Piksel menyala, bias, dan lapisan kedua
> tetap bergradien. Ini sparsitas masukan, bukan ReLU mati.

**2d.** Dari 2c: kalau kamu melatih dengan satu gambar per langkah, berapa
bagian jaringan yang benar-benar belajar tiap langkah? Apa akibatnya pada
pilihan ukuran batch?

> **Jawaban:** Sekitar seperdelapan parameter pada contoh terukur. Batch
> menggabungkan piksel menyala dari banyak digit, sehingga union fitur aktif
> lebih lebar, gradien lebih padat, dan varians lebih kecil. Batch 1 boros
> overhead serta memperbarui jaringan sangat jarang; mini-batch sedang lebih
> masuk akal, selama masih muat memori dan tidak menghilangkan manfaat SGD.

---

## Soal 3 - Backward iteratif

**3a.** Versi rekursif dan versi iteratifmu memberi gradien yang sama persis,
selisih `0.000e+00`. Jelaskan kenapa harus sama persis, bukan sekadar dekat.

> **Jawaban:** Keduanya menjalankan `_backward` yang sama pada DAG yang sama,
> setelah seluruh kontribusi anak terkumpul. Versi iteratif juga mendorong
> anak dalam urutan terbalik agar urutan DFS efektif sama dengan versi
> rekursif. Jadi urutan operasi floating-point pun sama; yang diganti hanya
> tempat penyimpanan stack. Hasil ukur: `0.000e+00`.

**3b.** Di TODO 2 kamu mendorong pasangan `(simpul, sudah_ditelusuri)` ke
tumpukan. Kenapa penandanya perlu? Coba hapus penanda itu dan jelaskan
urutan seperti apa yang kamu dapat.

> **Jawaban:** Penanda membuat simpul dicatat saat kunjungan kedua, sesudah
> semua induknya selesai: post-order. Tanpanya simpul dicatat saat pertama
> diambil: pre-order. Membalik pre-order bisa salah pada DAG bercabang yang
> berbagi simpul, sehingga suatu simpul membagikan gradien sebelum semua
> sumbangan tiba.

**3c.** Kamu memakai `set` berisi `id(v)`. Sesi 1 memakai `set` berisi objek
`Value` langsung. Keduanya jalan. Sebutkan satu keadaan di mana keduanya
berbeda perilakunya.

> **Jawaban:** Saat `Value` diberi `__eq__` berbasis nilai. Set objek dapat
> menganggap dua simpul berbeda tetapi bernilai sama sebagai satu; jika
> `__hash__` hilang, objek bahkan tidak bisa masuk set. Set `id(v)` tetap
> memakai identitas simpul dan tetap jalan.

**3d.** Berapa kedalaman tumpukan yang dipakai versi iteratifmu? Nyatakan
dalam O-besar, dan bandingkan dengan versi rekursif.

> **Jawaban:** Dengan operator `Value` berderajat masuk tetap, tumpukan DFS
> maksimum $O(D)$, dengan $D$ kedalaman graf; pada graf umum berfan-out besar
> batas kasarnya $O(V)$. Rekursif juga memakai $O(D)$ call stack, tetapi
> terkena limit sekitar 1000. List iteratif berada di heap; keduanya tetap
> butuh `terlihat` dan urutan topologis $O(V)$.

---

## Soal 4 - Tensor, dan gradien yang bentuknya harus cocok

**4a.** Untuk `out = A @ B` dengan A berbentuk $(B, n)$ dan B berbentuk
$(n, m)$: turunkan `A.grad` dan `B.grad` dari aturan rantai. Tunjukkan cuma
ada satu susunan perkalian yang bentuknya benar untuk masing-masing.

> **Jawaban:** Misalkan $G=\partial L/\partial out$ berbentuk $(B,m)$.
> Dari $dL=\operatorname{tr}(G^T(dA\,B+A\,dB))$ diperoleh
> $A.grad=GB^T$, berbentuk $(B,m)(m,n)=(B,n)$, dan
> $B.grad=A^TG$, berbentuk $(n,B)(B,m)=(n,m)$. Transposisi/susunan lain
> tidak cocok bentuknya.

**4b.** Di TODO 4, gradien geseran adalah jumlah atas baris batch, bukan
rata-rata. Buktikan itu dari aturan rantai. Lalu jelaskan kenapa mengganti
`sum` dengan `mean` menghasilkan model yang tetap belajar tapi salah, dan
seberapa salah.

> **Jawaban:** Karena $out_{rj}=A_{rj}+b_j$,
> $\partial L/\partial b_j=\sum_r(\partial L/\partial out_{rj})
> (\partial out_{rj}/\partial b_j)=\sum_r G_{rj}$. Gradien rugi sudah dibagi
> $B$ di entropi silang. Memakai `mean` membaginya lagi: gradien bias menjadi
> $B$ kali terlalu kecil, setara learning rate bias `lr / B`. Nilainya masih
> nonnol, maka model tetap belajar lebih lambat/salah skala.

**4c.** `entropi_silang` membagi gradien dengan `B`. Kalau pembagian itu
dihapus, apa yang berubah? Apakah ada nilai laju belajar yang membuatnya
setara lagi? Kalau ada, berapa.

> **Jawaban:** Semua gradien menjadi $B$ kali lebih besar: itu gradien jumlah
> rugi, bukan rata-rata rugi. Hasil update identik jika learning rate baru
> dibuat `lr_lama / B`.

**4d.** Bagian 4 mengadu 59 parameter dengan beda hingga dan lolos di
`2.79e-10`. Kenapa uji ini tetap perlu padahal kamu sudah menulis aturannya
dari turunan yang benar di kertas?

> **Jawaban:** Turunan kertas tidak menangkap salah kode: transpose terbalik,
> sumbu `sum` salah, pembagi batch hilang, atau `=` mengganti `+=`. Beda
> hingga menguji fungsi utuh lewat jalur independen. Hasil `2.791e-10`
> membuktikan implementasi, bukan hanya rumus, konsisten.

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

> **Jawaban:** Satu lintasan maju memakai
> $784\times128+128\times10=101.632$ perkalian per gambar. Backward memakai
> dua matmul per lapisan, jadi total maju+mundur
> $3\times101.632=304.896$ perkalian per gambar, atau
> $15.244.800.000$ perkalian per epoch. Jika tambahannya ikut dihitung sesuai
> konvensi FLOPS, totalnya sekitar `30.4896 GFLOP`. Waktu median numpy
> `float64` di mesin ini `4.735894 s`, jadi kinerja efektif
> $30.4896/4.735894=\mathbf{6.438\ GFLOPS}$.

**5b.** Ubah `Tensor` supaya memakai `float32`, jalankan ulang Bagian 5, catat
waktunya. Berapa bagian dari selisih numpy lawan PyTorch yang terjelaskan?

> **Jawaban:** GTX 1650 Ti/CPU mesin ini memberi median numpy `float64`
> `4.735894 s`, numpy `float32` `2.462704 s`, dan PyTorch CPU `float32`
> `0.770991 s` per epoch, batch 64. Jadi bagian gap yang hilang adalah
> $(4.735894-2.462704)/(4.735894-0.770991)=\mathbf{57.33\%}$. Rasio numpy
> terhadap PyTorch turun dari `6.14x` ke `3.19x`. Akurasi validasi terbaik
> tetap praktis sama: `97.32%` lawan `97.31%`.

**5c.** GPU tidak menang di tabel itu. Naikkan `batch` di `latih_mnist` dan di
Bagian 6 secara bersamaan sampai GPU menang, lalu catat di batch berapa
titik baliknya. Jelaskan dari mana ongkos tetap itu datang.

> **Jawaban:** Titik balik mesin ini batch **256**. Pada batch 128: numpy
> `3.987313 s`, PyTorch CPU `0.491241 s`, GPU `0.491497 s`—GPU masih kalah
> tipis. Pada batch 256: numpy `1.003787 s`, CPU `0.331539 s`, GPU
> `0.253925 s`; GPU menang. Ongkos tetap berasal dari dispatch PyTorch,
> peluncuran dan penjadwalan kernel CUDA, serta sinkronisasi. Batch kecil
> memberi terlalu sedikit kerja per kernel untuk menutup latensi itu.

**5d.** Rasio 5000x antara Value dan numpy tidak berasal dari aritmetika,
karena jumlah perkalian keduanya sama. Sebutkan tiga sumber ongkosnya, dan
urutkan dari yang terbesar menurutmu.

> **Jawaban:** Urutan perkiraan: (1) loop, operator dispatch, dan pemanggilan
> fungsi interpreter Python per skalar, bukan kernel BLAS; (2) alokasi serta
> garbage collection objek `Value`, closure, set, dan metadata per operasi;
> (3) hashing/traversal DAG skalar saat backward, lengkap dengan pointer
> chasing dan cache locality buruk. Numpy membayar overhead itu per array,
> bukan per angka.

---

## Soal 6 - Validasi yang benar-benar dipakai

Bagian 5 memberi:

```text
akurasi uji, epoch terakhir : 96.03 persen
akurasi uji, epoch pilihan  : 97.27 persen   (epoch 6, dipilih lewat validasi)
```

**6a.** Selisihnya 1,24 persen. Jelaskan dari mana selisih itu datang, dan
kenapa epoch terakhir bukan pilihan yang baik.

> **Jawaban:** Setelah epoch 6, SGD terus mengubah parameter dan mulai
> menyesuaikan noise/keunikan data latih; validasi memburuk. Epoch terakhir
> hanyalah checkpoint terakhir, bukan bukti generalisasi terbaik. Menyimpan
> epoch dengan validasi tertinggi memilih titik sebelum degradasi itu, maka
> uji naik dari `96.03%` ke `97.27%`.

**6b.** Kenapa epoch pilihan tidak boleh dipilih memakai himpunan uji?
Jawaban "karena itu curang" tidak cukup. Sebutkan apa persisnya yang jadi
tidak valid dan bagi siapa.

> **Jawaban:** Memilih epoch dari skor uji memasukkan informasi uji ke proses
> fitting hyperparameter. Skor maksimum yang lalu dilaporkan menjadi bias ke
> atas akibat seleksi, sehingga bukan lagi estimasi independen untuk data
> baru. Yang dirugikan ialah pembaca/pengguna yang mengandalkan angka itu.
> Validasi memilih; uji disentuh sekali setelah keputusan selesai.

**6c.** Akurasi validasi di epoch 6 adalah 97,32 dan akurasi ujinya 97,27.
Angka mana yang boleh kamu laporkan sebagai ramalan untuk data baru, dan
kenapa yang satunya tidak.

> **Jawaban:** Laporkan **akurasi uji 97,27%** sebagai estimasi data baru.
> Nilai validasi 97,32% sudah dipakai memilih epoch, maka secara kondisional
> cenderung optimistis dan bukan evaluasi akhir yang independen.

**6d.** Kamu memilih satu hyperparameter (epoch) dari 8 kandidat memakai
validasi 10000 gambar. Kalau kamu memilih dari 5000 kandidat, apa yang mulai
rusak? Perkirakan besarannya.

> **Jawaban:** Model mulai overfit ke himpunan validasi lewat pencarian
> hyperparameter. Untuk akurasi sekitar 97%, simpangan baku binomial validasi
> ialah $\sqrt{0.97(0.03)/10000}=0.00171$ atau `0.171` poin persen. Maksimum
> dari 5000 kandidat independen mendapat bias seleksi kira-kira
> $\sigma\sqrt{2\ln 5000}\approx0.0070$, sekitar **0,70 poin persen**.
> Kandidat yang berkorelasi mengurangi angka itu, tetapi kerusakannya tetap:
> validasi berubah menjadi data latih tingkat kedua.

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

> **Jawaban:** Pada kuadratik, makin besar $\eta$ yang masih stabil, makin
> cepat sumbu landai menyusut. Karena penilaian hanya 300 iterasi, sapuan
> memilih titik terbesar tepat di bawah $2/\lambda_{max}$. Praktiknya jangan
> menetap di tepi: minibatch, perubahan kurvatur, dan galat numerik dapat
> mendorongnya melewati batas. Pakai LR range test, sisakan margin, lalu decay.

**7b.** Momentum dan SGD memakai laju belajar yang sama persis di tabel itu,
tapi satu tiba dan satu tidak. Dari persamaan osilator teredam, turunkan
faktor percepatan efektif momentum untuk `beta = 0.9`. Cocokkan dengan
angkanya.

> **Jawaban:** Untuk gradien yang konsisten,
> $v_\infty=-\eta g/(1-\beta)$, jadi faktor langkah efektifnya
> $1/(1-0.9)=\mathbf{10\times}$. Pada rezim teredam-kurang, akar momentum
> bermagnitudo $\sqrt{0.9}=0.94868$. Sumbu lambat SGD punya faktor
> $1-\eta\lambda_{min}=0.99593$; rasio laju log asimtotiknya
> $\ln(0.94868)/\ln(0.99593)=12.9\times$. Dalam lintasan nyata, momentum
> mencapai ambang pada iterasi 63; SGD baru iterasi 305, atau `4.84x`, karena
> transien dan ambang absolut membuat rasio terukur lebih kecil.

**7c.** Laju belajar terbaik Adam adalah 5,01, tiga ratus kali lebih besar
dari SGD. Jelaskan kenapa itu tidak melanggar ambang `2/lam_max`. Petunjuknya
ada di penyebut Adam.

> **Jawaban:** Batas $2/\lambda_{max}$ berlaku untuk langkah
> $-\eta g$ tanpa prasyarat. Adam memakai
> $-\eta\hat m/(\sqrt{\hat s}+\epsilon)$; penyebut menormalkan setiap
> koordinat menurut skala gradiennya. Maka `5.01` bukan koefisien langsung
> terhadap Hessian asli. Stabilitasnya ditentukan Hessian yang sudah
> diprasyaratkan dan dinamika $m,s$, bukan ambang SGD mentah.

**7d.** RMSprop kalah dari momentum di lanskap ini. Buat satu lanskap di mana
RMSprop menang, jalankan, dan tunjukkan angkanya. Lalu sebutkan sifat lanskap
apa yang menentukan siapa menang.

> **Jawaban:** Dipakai
> $L(x,y)=x^4/4+y^2/2$, $\theta_0=(100,100)$, 1000 iterasi, lalu kedua
> optimizer mendapat sapuan LR logaritmik yang sama dari $10^{-8}$ sampai
> $10^1$. Momentum terbaik: `lr=1.1220e-4`, rugi akhir `528.2553`, tidak
> pernah mencapai rugi 1. RMSprop terbaik: `lr=0.125893`, rugi akhir
> `0.001951`, mencapai rugi 1 pada iterasi 898. Kurvatur sumbu kuartik
> $3x^2$ berubah dari 30000 menuju nol. Momentum harus memakai LR global kecil
> untuk selamat di awal; RMSprop menormalkan skala gradien yang berubah.
> Gradien konsisten dengan kurvatur tetap menguntungkan momentum; skala per
> sumbu yang timpang dan berubah sepanjang lintasan menguntungkan RMSprop.

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

> **Jawaban:** `Value` saat ini mendukung (1) perkalian/pembagian/pangkat
> skalar umum, (2) `exp` dan `log` sebagai operasi graf mandiri, dan (3)
> ekspresi Python skalar bercabang/tidak beraturan. `Tensor` latihan hanya
> punya matmul, tambah-bias, ReLU, dan entropi silang. PyTorch memilih tensor
> karena satu objek mengurus banyak angka lewat SIMD/BLAS/GPU, memori rapat,
> batching, dan overhead Python jauh lebih kecil.

**8b.** Sepanjang Bulan 1 kamu menabrak empat kegagalan yang bentuknya
berbeda: gradien salah tanpa error, neuron mati permanen, batas rekursi, dan
lambat yang tidak bisa ditunggu. Untuk tiap-tiapnya, sebutkan alat yang
menangkapnya.

> **Jawaban:** Gradien salah ditangkap **gradient check beda hingga**.
> Neuron mati ditangkap **pengukuran aktivasi/gradien per neuron pada seluruh
> data** (`hitung_mati`). Batas rekursi ditangkap **stress test graf dalam dan
> `RecursionError`**. Lambat ditangkap **benchmark `perf_counter` per gambar
> lalu ekstrapolasi waktu epoch**. Empat kegagalan, empat alat ukur berbeda.

**8c.** Kamu sekarang punya dua mesin autograd tulisan sendiri, satu
per-angka dan satu per-array. Untuk SYNESIS, keduanya tidak akan dipakai
melatih apa pun. Jelaskan apa yang tetap kamu dapat dari menulisnya, dalam
kalimat yang bukan basa-basi.

> **Jawaban:** Saya sekarang bisa menelusuri gradien PyTorch sampai aturan
> lokal, urutan topologis, akumulasi cabang, broadcasting, dan biaya graf;
> saat custom operation memberi gradien salah atau training lambat, saya tahu
> invariant mana yang diuji dan alat apa yang membuktikannya.

---

## Tolok Ukur Bulan 1 Sesi 3+4

- [x] `dL/dz = p - y` diturunkan sendiri di kertas, bukan diterima
- [x] Softmax dan entropi silang jalan di atas kelas `Value` buatanmu
- [x] Dinding waktu dan dinding rekursi dua-duanya ditabrak sungguhan
- [x] `backward` iteratif ditulis sendiri, dan hasilnya identik dengan rekursif
- [x] Empat aturan turunan `Tensor` lolos uji beda hingga di bawah `1e-5`
- [x] MNIST di atas 95 persen dengan mesin buatan sendiri, nol `torch.nn`
- [x] Epoch dipilih lewat validasi, dan bedanya dengan epoch terakhir dicatat
- [x] Rasio kecepatan lawan PyTorch diukur, dan sebabnya bisa dijelaskan
- [x] `float32` diuji, dan bagiannya dalam selisih itu dihitung
- [x] SGD-momentum, RMSprop, dan Adam ditulis tangan dan dibandingkan di lr terbaiknya masing-masing
- [x] Hubungan momentum dengan osilator teredam bisa dijelaskan tanpa catatan
- [x] Satu lanskap di mana RMSprop menang dibuat sendiri dan ditunjukkan

Kalau kedua belas kotak beres, Bulan 1 tutup. Bulan 2 sudah menunggu di
`soal-bulan2-sesi1.md`.
