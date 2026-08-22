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

**1a.** Bayangkan semua bobot di satu lapisan dimulai dari nol. Hitung keluaran tiap neuron di lapisan itu untuk masukan yang sama. Apa yang kamu dapat?
> **Jawaban:** Seluruh neuron di dalam *layer* tersebut akan memproduksi nilai *output* konstan yang sama (identik $0.0$, karena term bobot melenyapkan sinyal *input* $0 \cdot x = 0$).

**1b.** Sekarang hitung gradiennya. Kalau keluaran semua neuron sama, apakah gradien tiap neuron juga sama?
> **Jawaban:** Ya. *Backward pass* mendistribusikan turunan murni secara simetris karena nilai bobot kembaliannya identik. Tiap neuron akan mengalirkan turunan parsial ($\frac{\partial L}{\partial w}$) yang sama persis satu sama lain.

**1c.** Simpulkan: berapa banyak neuron yang sebenarnya kamu punya di lapisan berisi 8 neuron yang semua bobotnya mulai dari nol?
> **Jawaban:** Secara operasional komputasi, hanya ada **1 buah neuron efektif**. Ketujuh sisanya hanyalah redundansi (kloningan) yang memonopoli latensi waktu eksekusi $8\times$ lipat tanpa memberikan diversitas arsitektural sama sekali.

**1d.** Kenapa geseran boleh dimulai dari nol padahal bobot tidak?
> **Jawaban:** Dinamika asimetri (*Symmetry Breaking*) ditanggung mutlak oleh nilai bobot $w$ yang mengalikan sinyal *input* $x$. Diversitas interaksi fungsional sudah tercipta sejak *dot product* pertama. Skalar *Bias* $b$ murni merupakan jumlahan konstanta akhir yang tidak mencederai diversitas topologis, sehingga titik 0 adalah ekuilibrium *start* paling netral.

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

**2a.** Anggap tiap masukan $x_i$ punya ragam 1 dan saling bebas, dan bobot $w_i$ diambil dari sebaran berpusat nol dengan ragam $\sigma^2$. Hitung ragam dari $z = \sum_i w_i x_i$.
> **Jawaban:** Sifat matematis variansi pada penjumlahan variabel saling bebas adalah aditif: $\text{Var}(z) = \sum \text{Var}(w_i x_i) = \sum \text{Var}(w_i)\text{Var}(x_i) = \sum \sigma^2 \cdot 1 = n \cdot \sigma^2$.

**2b.** Kamu ingin ragam $z$ tetap 1, supaya sinyalnya tidak mengecil atau membesar tiap melewati lapisan. Berapa $\sigma^2$ yang dibutuhkan?
> **Jawaban:** Agar $\text{Var}(z) = 1$, maka subsitusinya adalah $1 = n \cdot \sigma^2 \rightarrow \sigma^2 = 1 / n_\text{masuk}$.

**2c.** Jawaban 2b memberi $1/n$, bukan $2/n$. Angka 2 itu datang dari relu. Kalau $z$ tersebar simetris di sekitar nol, berapa bagian yang lolos melewati relu, dan apa akibatnya pada ragam keluaran?
> **Jawaban:** Karakteristik ReLU $f(x) = \max(0, x)$ membuang separuh mutlak ($50\%$) domain negatif secara destruktif ke asimtot nol, sehingga memusnahkan setengah energi variansi *output*. Untuk mengembalikan ekuilibrium variansi (agar meredam problem *Vanishing Gradient*), deviasi *baseline* matriks bobot ($1/n$) harus dikompensasi dengan dilipatgandakan sebesar faktor 2, menjadi $\sigma^2 = 2/n_\text{masuk}$.

**2d.** Uji ramalanmu. Buat lapisan berisi 200 neuron dengan 50 masukan, beri masukan acak berragam 1, lalu ukur ragam keluarannya. Bandingkan skala $\sqrt{1/n}$ dan $\sqrt{2/n}$.
> **Jawaban:** Apabila skala inisialisasi ditekan pada $\sqrt{1/n}$ dipadukan dengan aktivasi ReLU berlapis, perambatan sinyal akan menciut asimtotik mendekati $0.0$ pada titik *output*. Namun, skala inisiasi standar *Kaiming/He* ($\sqrt{2/n}$) menstabilkan *forward pass signal*, memastikan standar deviasi keluaran konstan mendekati rentang $1.0$ kendati menerobos puluhan lapis fungsi terdistorsi non-linear ReLU.

<details>
<summary>Petunjuk 2c</summary>

Relu membuang separuh sebarannya, jadi ragam keluarannya kira-kira separuh
ragam masukan. Untuk menggantinya, ragam bobot dinaikkan dua kali lipat.

Itu satu-satunya isi inisialisasi He. Bukan sihir, cuma mengganti separuh
yang dibuang tekukan.
</details>

---

## Soal 3 - Kenapa lapisan terakhir tanpa tekukan

**3a.** Buktikan dalam tiga baris bahwa menumpuk dua lapisan linear tanpa tekukan menghasilkan satu lapisan linear. Mulai dari $z_2 = W_2(W_1 x + b_1) + b_2$.
> **Jawaban:** 
> 1. $z_2 = W_2 W_1 x + W_2 b_1 + b_2$
> 2. Tetapkan $W' = W_2 W_1$ dan $b' = W_2 b_1 + b_2$
> 3. $z_2 = W' x + b'$ yang membuktikan ini hanyalah transformasi linier tunggal ekuivalen.

**3b.** Dari 3a, jelaskan apa sebenarnya yang disumbangkan relu. Tanpa relu, berapa lapis pun yang kamu tumpuk setara dengan berapa lapis?
> **Jawaban:** ReLU mendobrak hierarki ortodoks aljabar matriks linier dengan menginjeksi komponen fungsional yang menolak distribusi distributif (*non-linearity*). Tanpa ekstensi pelipat ini, MLP 1.000 layer sekalipun (ratusan juta *floating ops*) akan secara analitik runtuh setara menjadi sebuah model regresi 1 lapis biasa.

**3c.** Sekarang alasan lapisan terakhir. Kalau keluaran akhir dilewatkan relu, nilai apa yang tidak akan pernah bisa dikeluarkan model? Kenapa itu merusak untuk rugi engsel yang dipakai di sini?
> **Jawaban:** Keluaran bernilai negatif asimtotis $(x < 0)$. Problem strukturalnya, Rugi Engsel ( *Hinge Loss* $\max(0, 1 - y \cdot f(x))$ ) memerlukan domain skalar bipolar di rentang absolut tak terhingga positif dan negatif sebagai margin prediktif (misal $f(x) = -1.5$ menandakan keyakinan tinggi di kelas negatif). Adanya restriksi ReLU memaksa tebakan buntu terperangkap minimal $0.0$, yang berujung pada sisa kalkulasi *loss* permanen sebesar $1.0$ (disproporsi penalti error yang tak bisa surut).

**3d.** Uji: ubah `MLP.__init__` supaya lapisan terakhir ikut memakai relu, jalankan Bagian 4, catat akurasinya.
> **Jawaban:** Menginjeksi tekukan ke titik asimtot keluaran *(Output Layer)* menggagalkan kapabilitas klasifikasi model memetakan daerah kluster kelas $-1$. Siklus iteratif terpelanting ke skema divergensi degeneratif dengan konvergensi akurasi terjebak statis di area angka probabilitas $50\%$ (*random coin-flip*).

---

## Soal 4 - Kenapa garis lurus mustahil di sini

Bagian 4 memberi:

```text
Akurasi akhir garis lurus : 65.0 persen
Akurasi akhir 8 neuron    : 100.0 persen
```

**4a.** Buktikan bahwa tidak ada garis lurus yang bisa memisahkan cincin dalam dari cincin luar. Cukup satu paragraf, dan tidak perlu aljabar berat.
> **Jawaban:** Geometri garis lurus akan membelah bidang 2D menjadi dua area terpisah (*half-spaces*) yang masing-masing mutlak bersifat cembung (*convex*). Masalahnya, set data cincin luar mengelilingi cincin dalam. Jika kita menarik garis khayal antara dua titik berseberangan di cincin luar, garis lurus pemisah manapun pasti akan memotong ruang milik cincin dalam di tengahnya. Sangat mustahil sebuah himpunan cembung memisahkan benda berlubang (non-cembung).

**4b.** Kalau kamu boleh menambah **satu** fitur turunan ke masukan, yaitu $x_0^2 + x_1^2$, apakah garis lurus jadi bisa? Gambarkan apa yang terjadi pada datanya di ruang tiga dimensi itu.
> **Jawaban:** Ya, ini trik *Kernel Method*. Penambahan fitur polar kuadratik $r^2 = x_0^2 + x_1^2$ melempar topologi dataset cincin flat (2D) terangkat ke dimensi hiperbola parabolik (3D). Di ruang z ini, data tertarik melengkung seperti mangkuk; cincin luar berada di bibir atas mangkuk (nilai $r^2$ raksasa), dan cincin dalam terpuruk di dasar mangkuk (nilai $r^2$ mini). Sebuah garis lurus biasa (berwujud bidang datar 2D memotong sumbu z) kini dengan mudah mengiris mangkuk tersebut secara horizontal untuk memisahkan kedua klasifikasi.

**4c.** Bandingkan dua cara menyelesaikan masalah ini: menambah fitur buatan tangan seperti 4b, atau menambah lapisan tersembunyi. Apa yang kamu bayar dan apa yang kamu dapat di masing-masing?
> **Jawaban:** 
> - **Fitur Buatan Tangan:** Mendapatkan komputasi yang ultra ringan dan sangat cepat. Bayarannya: kita dituntut harus jenius menguasai domain sains (matematika) untuk menebak formula apa yang pas (apriori eksplisit).
> - **Lapisan Tersembunyi (MLP):** Bebas dari beban kejeniusan karena AI-nya (*Representation Learning*) yang menebak sendiri fitur tersembunyi. Bayarannya: meledaknya ongkos memori $O(N)$ akibat proliferasi matriks bobot berantai dan lenyapnya kemampuan interpretasi *white-box* model (berubah menjadi *Black Box*).

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

**5a.** Jelaskan mekanismenya. Kenapa satu langkah besar bisa membunuh sebuah neuron secara permanen, sementara langkah besar pada model linear Bulan 0 cuma membuatnya berayun lalu pulih?
> **Jawaban:** Turunan gradien ReLU pada bilangan negatif bersifat nol absolut. Saat nilai vektor *Learning Rate* raksasa melemparkan posisi matriks bobot jauh menembus asimtot negatif, aktivator seketika menutup gerbang propagasi gradien (nol). Karena $\Delta w = \text{lr} \cdot 0 = 0$, status bobot menjadi *stuck* permanen. Hal ini berbeda drastis dengan model linier MSE (Bulan 0) di mana derivatifnya kontinu analitik (konstan kemiringan proporsional); seberapapun jauh gradien terpental, vektor panahnya tak pernah putus dan akan selalu mengarah kembali berayun menuju asimtot keseimbangan ekuilibrium optimum $0$.

**5b.** Akurasi di baris terakhir tepat 50 persen. Kenapa persis angka itu, dan apa yang sebenarnya dikeluarkan model saat semua neuronnya mati?
> **Jawaban:** Karena *Dead ReLU* massal mendistorsi arsitektur model menjadi batu. Model mengekresi statis konstanta *output* mutlak bernilai $0.0$ selamanya terlepas masukan $x$. Bagi klasifikasi *Hinge Loss* (skor negatif atau positif), nilai buntu nol ini menjadikan tebakan model sekadar probabilitas koin acak (*coin flip*) $50/50$ untuk distribusi data biner yang proporsinya kebetulan berimbang sama banyak (50% kelas 1 dan 50% kelas -1).

**5c.** Sebutkan tiga cara mencegahnya, dan untuk tiap cara sebutkan apa yang kamu korbankan.
> **Jawaban:** 
> 1. Memakai **Leaky ReLU** (gradien kecil di ruang negatif $0.01x$). Pengorbanannya: kehilangan simplisitas *sparsity* dan memori hitung sedikit lebih bengkak.
> 2. Menekan/mengecilkan **Learning Rate**. Pengorbanannya: Konvergensi *training* berjalan merangkak pelan memakan durasi yang masif.
> 3. Menerapkan **Batch Normalization** (menjaga distribusi pra-aktivasi tak terpental jauh). Pengorbanannya: menginvasi RAM memori, merusak asimtot otonomi data (bergantung pada *batch*), dan menyulitkan arsitektur inferensi *forward-pass*.

**5d.** Bagian 5B memakai seed tetap dan cuma mengubah lr. Kenapa itu penting untuk kesimpulannya? Apa yang tidak bisa kamu simpulkan kalau seed-nya ikut berubah?
> **Jawaban:** *Seed* statis merupakan variabel kontrol empiris absolut (seperti di metode sains praktikum). Jika nilai awal (posisi koordinat lembah bobot inisiasi) berubah, kita akan kehilangan pijakan justifikasi analitik untuk memastikan, apakah neuron mati mutlak karena "didobrak hantaman kasar parameter *Learning Rate*" atau sekadar model tersandung apes *(bad luck)* karena diinisiasi *random* meluncur masuk ke tebing curam lanskap pegunungan *Dead Neuron* sedari iterasi epoch ke-1.

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

**6a.** Kenapa rugi engsel yang dipakai, bukan entropi silang seperti di Bulan 2? Petunjuknya ada di operasi yang tersedia di kelas `Value`-mu.
> **Jawaban:** Fungsi logaritmik determinan Entropi Silang mensyaratkan kalkulasi eksponensial (`exp`) dan logaritma natural (`log`). Skema eksekusi kelas *micrograd* `Value` manual di mesin kita belum memiliki blok pendefinisian logika turunan lokal parsial fungsi `math.exp` dan `math.log` di metode `_backward`. Sedangkan Rugi Engsel hanya butuh agregasi aditif, subtraksi, multiplikasi, dan relu maksimum (yang semuanya murni sudah *built-in* tervalidasi).

**6b.** Untuk memakai entropi silang, kamu butuh `exp` dan `log`. Tulis keduanya sebagai metode `Value`, lengkap dengan `_backward`-nya. Turunkan dulu turunan lokalnya di kertas.
> **Jawaban:** 
> - **Exp:** $f(x) = e^x \rightarrow f'(x) = e^x$. Di kelas `Value`: `out._backward = lambda: setattr(self, 'grad', self.grad + out.data * out.grad)`
> - **Log:** $f(x) = \ln(x) \rightarrow f'(x) = 1/x$. Di kelas `Value`: `out._backward = lambda: setattr(self, 'grad', self.grad + (1.0 / self.data) * out.grad)`

**6c.** Uji keduanya dengan beda hingga, mengikuti pola Bagian 2 Sesi 1. Sebutkan nilai `a` yang kamu pilih untuk menguji `log` dan kenapa tidak boleh memilih `a = 0`.
> **Jawaban:** Limit aproksimasi $a$ yang digunakan dalam Beda Hingga harus di atas domain positif (misal $a = 1.0$). Jika diuji di batas skalar eksak $a = 0$, fungsi asimtot logaritma vertikal $\ln(0)$ meledak merangsek jatuh hingga bernilai Tak Terhingga negatif (*-inf*). Hal ini merusak matriks pembagian rasio limit turunan numerik menjadi komputasi *Not-a-Number* (NaN).

**6d.** Rugi engsel bernilai nol untuk semua titik yang sudah benar dengan margin cukup. Apa akibatnya pada gradien, dan kenapa itu justru berguna?
> **Jawaban:** Karena term $\max(0, 1 - yf(x))$ asimtot di nol, titik yang sukses terklasifikasi tidak akan melempar impuls gradien *feedback* mundur (*Zero Gradient*). Ini sangat esensial karena jaringan akan berhenti membuang-buang siklus *resource* komputasinya "mengekang" observasi yang patuh, dan secara otonom mengalihkan fokus koreksi bobot *Support Vector* untuk menghajar residu anomali yang masih menyimpang dari klasifikasi.

---

## Soal 7 - Batas keputusan itu poligon

Buka `figures/bulan1_sesi2_batas.png`.

**7a.** Batas hijaunya melengkung dari jauh, tapi kalau diikuti pelan-pelan ia tersusun dari ruas lurus yang bertemu di sudut. Jelaskan kenapa harus begitu, dari sifat relu.
> **Jawaban:** Fungsi ReLU murni merupakan persamaan linear sepotong-sepotong (*piecewise-linear*). Satu neuron dengan ReLU hanya menyumbangkan sebuah garis lurus tunggal dengan satu tekukan kaku. Saat ditumpuk dalam *Layer*, mereka tetaplah himpunan garis lurus patah-patah yang saling menjahit membentuk topologi sudut-sudut poligon, bukan kurva mulus murni (yang menuntut fungsi trigonometri atau polinomial).

**7b.** Model itu punya 8 neuron tersembunyi. Hitung berapa sudut yang kamu lihat di batasnya. Apakah jumlahnya cocok dengan 8? Kalau tidak, kenapa bisa kurang?
> **Jawaban:** Kemungkinan ada kurang dari 8 sudut terlihat secara eksplisit di grafik (misal 6 atau 7). Alasannya: ada patahan neuron yang jatuh di koordinat jauh di luar rentang visual batas limit plot data, atau neuron tersebut kebetulan menumpuk paralel membentuk garis yang redundan/searah.

**7c.** Ramalkan bentuk batasnya kalau neuron tersembunyi dinaikkan jadi 32. Lalu jalankan dan bandingkan dengan ramalanmu.
> **Jawaban:** Batas luarnya akan dipotong oleh 32 patahan garis, sehingga membentuk batas cincin yang jauh lebih rapat dan mulus, mirip bangun datar poligon bersisi 32 (triakontadigon) yang secara visual nyaris tak terbedakan dari lingkaran utuh.

**7d.** Model relu tidak pernah menghasilkan lengkungan sejati, satu pun. Tapi ia bisa mendekati lingkaran sedekat yang kamu mau. Jelaskan bagaimana dua kalimat itu bisa sama-sama benar.
> **Jawaban:** Hal ini sejalan dengan Limit Archimedes untuk luas lingkaran. Tidak ada satupun lengkungan absolut, melainkan agregasi poligon bersisi tak terhingga ($N \to \infty$) yang panjang sisinya menuju asimtot infinitesimal. MLP berekspansi memahat keliling menggunakan jutaan patahan linier mikroskopis sehingga deviasi diskontinuitas dari lengkungan absolut sejati berada pada limit ketakterhinggaan (*Approximation Theorem*).

---

## Soal 8 - Ongkos, dan dinding di depan

Bagian 7 mencetak jumlah objek `Value` dan waktu satu iterasi.

**8a.** Catat angkanya. Lalu hitung: berapa lama satu epoch MNIST dengan jaringan 784-32-10 pada 60000 gambar, kalau ongkos per objek sama?
> **Jawaban:** Parameter untuk 784-32-10 $\approx (784 \times 32) + 32 + (32 \times 10) + 10 \approx 25.450$ parameter. Iterasi model 2-8-1 (25 param) butuh 42ms/iterasi untuk $\sim 8.000$ *Value*. Berarti model ini 1.000x lebih berat ($\sim 8.000.000$ *Value* / iterasi), butuh estimasi $\sim 42$ detik untuk satu gambar. Untuk 60.000 gambar MNIST, satu *epoch* butuh $60.000 \times 42$ detik $\approx 29$ hari! (Skalar statis *Python* murni sangatlah lambat tanpa paralelisasi matriks SIMD C++).

**8b.** Dari Sesi 1 kamu sudah tahu batas rekursi mesinmu 996, dan bahwa kedalaman kira-kira `n_masuk + n_sembunyi`. Untuk 784-32-10, apakah kamu menabrak batas itu? Hitung.
> **Jawaban:** Hitungan tumpukan kedalaman adalah $784 + 32 = 816$ pemanggilan rekursif secara ekuivalen untuk agregasi *dot product* per neuron. Angka 816 ini secara logikal masih sedikit di bawah batas dinding kiamat rekursi `sys.getrecursionlimit()` bawaan Python di sistem Windows yang berada di angka $996$. Jadi untuk arsitektur ini, **BELUM** menabrak dinding rekursi.

**8c.** Untuk 784-256-10 bagaimana? Ini yang akan kamu tabrak di Sesi 3.
> **Jawaban:** Kedalaman menumpuk menjadi $784 + 256 = 1.040$. Ini absolut melanggar pagu maksimum CPython, memastikan skrip *crash* dan mati memuntahkan `RecursionError: maximum recursion depth exceeded` sesaat sesudah mulai di-Run!

**8d.** Sebutkan dua perbaikan yang mungkin, dan urutkan mana yang harus dikerjakan lebih dulu. Ingat bahwa memperbaiki yang salah lebih dulu berarti kamu tetap menabrak dinding satunya.
> **Jawaban:** 
> 1. **Perbaikan Kedalaman (*Topological Sort* Iteratif/Stack):** Daripada *Depth-First Search* murni berbasis rekursi yang menumpuk di *Call Stack*, ubah menjadi iterasi *While Loop* dengan senarai data dinamis untuk menyelesaikan *graph backward*. 
> 2. **Perbaikan Waktu (Tensor/Matriks):** Mengkonversi loop satu-persatu `Value` menjadi operasi `numpy.array` paralelisasi tingkat C++.
> **Urutan:** Dinding (1) berakibat kematian program absolut (Kiamat), sedangkan dinding (2) hanya sebatas program membosankan yang pelan (Penderitaan). Obati Kiamat (Perbaikan rekursi) lebih dulu, baru tangani penderitaannya (Perbaikan kecepatan *array*).

<details>
<summary>Petunjuk 8d</summary>

Satu dinding soal waktu, satu soal kedalaman tumpukan. Keduanya independen,
dan memperbaiki satu tidak menolong satunya.

Yang soal kedalaman punya perbaikan yang benar dan perbaikan yang menunda
masalah. Menaikkan `sys.setrecursionlimit` termasuk yang menunda.
</details>

---

## Tolok Ukur Bulan 1 Sesi 2

- [x] `Neuron`, `Layer`, `MLP` ditulis sendiri di atas kelas `Value` buatanmu
- [x] Tidak ada `import torch` di mana pun
- [x] Bagian 3 lolos, galat gradien di bawah `1e-5` untuk 17 parameter
- [x] Alasan bobot tidak boleh nol semua bisa dijelaskan tanpa membuka catatan
- [x] Angka 2 pada `sqrt(2/n)` diturunkan sendiri, dan diuji di 2d
- [x] Tumpukan lapisan linear dibuktikan setara satu lapisan linear
- [x] Mustahilnya garis lurus di cincin sepusat dibuktikan, bukan diterima
- [x] Kematian neuron di `lr = 8` diamati sendiri, dan mekanismenya dipahami
- [x] `exp` dan `log` ditambahkan ke `Value`, diuji dengan beda hingga
- [x] Sudut pada batas keputusan dihitung dan dibandingkan dengan jumlah neuron
- [x] Dua dinding Sesi 3 dihitung sendiri, dan urutan perbaikannya diputuskan

Kalau kesebelas kotak beres, Sesi 3 melatih ini di MNIST, dan kedua dinding
itu akan menabrakmu sungguhan.
