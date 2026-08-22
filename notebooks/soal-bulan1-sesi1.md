# Soal Bulan 1 Sesi 1 - Mesin autograd buatanmu

Berkas latihan: [`bulan1_sesi1_autograd.py`](bulan1_sesi1_autograd.py)

Bulan 0 selesai. Kamu menutupnya dengan membuktikan gradien tanganmu cocok dengan `loss.backward()` sampai `1e-16`.

Malam ini kamu menulis isi `loss.backward()` itu. Sekitar 90 baris, dan setelah selesai tidak ada lagi kotak hitam di lapisan paling dasar deep learning.

---

## Soal 0 - Tiga koreksi dari Sesi C dan D

Sesi C dan D kamu kuat, dan sebagian besar jawabannya tepat. Tiga hal perlu diluruskan, dan ketiganya mengubah apa yang akan kamu lakukan saat menemui masalah serupa.

### 0a. Lonjakan derajat 8 ke 9 bukan kegagalan presisi

Di Soal 5c Sesi C kamu menulis lonjakan test loss dari `6.35` ke `923.58` terjadi karena "Matriks X^T X CPU-nya mulai ambyar" dan "di pangkat 9 rasio angkanya udah nyebrang batas presisi aman float64".

Ini bisa diuji, jadi saya uji. Derajat 9 diselesaikan ulang dengan **aritmetika pecahan eksak**, nol galat pembulatan sama sekali:

| derajat | cond | test loss float64 | test loss EKSAK | selisih relatif |
|---|---|---|---|---|
| 8 | 1.658e+09 | 6.3470 | 6.3470 | 9.5e-14 |
| 9 | 2.533e+10 | 923.5812 | 923.5812 | 2.8e-12 |

Aritmetika sempurna memberi jawaban yang sama persis. Jadi lonjakan itu **murni overfitting**, bukan presisi.

Perhatikan juga angkanya: cond di derajat 9 adalah `2.5e10`, sementara batas float64 sekitar `1e16`. Masih enam orde di bawahnya.

**0a-i.** Kalau bukan presisi, jelaskan lonjakan itu lewat jumlah parameter lawan jumlah data.
> **Jawaban:** Lonjakan itu murni karena *overfitting*. Pada derajat 9, kita memiliki 10 parameter untuk mencocokkan 15 titik data. Saat rasio parameter terhadap data terlalu tinggi, polinomial memiliki cukup derajat kebebasan untuk menghafal (menangkap derau acak) alih-alih mempelajari tren generiknya. Begitu dieksekusi di luar rentang data latih, kurva polinomial derajat tinggi akan mengalami osilasi ekstrem (fenomena Runge), menghasilkan lonjakan *loss* raksasa.

<details>
<summary>Petunjuk 0a</summary>

Derajat 8 punya 9 parameter, derajat 9 punya 10, dan datamu 15 titik.

Rasio parameter terhadap data naik dari 9/15 jadi 10/15. Setelah ambang tertentu, parameter tambahan berhenti dipakai menangkap pola dan mulai dipakai menghafal derau.

Kerusakannya paling parah di luar rentang data, tempat tidak ada titik yang menahan kurva.
</details>

**0a-ii.** Kenapa penting membedakan "model overfit" dari "aritmetika rusak"? Jawab dengan menyebut perbaikan apa yang akan kamu coba pada masing-masing kasus.
> **Jawaban:** Karena perbaikannya berada di dua domain yang berbeda. Jika mendiagnosisnya sebagai "aritmetika rusak", perbaikannya adalah merombak presisi komputasi (mengganti ke `float128` atau presisi eksak), yang mana sama sekali tidak akan menurunkan *test loss*. Jika mendiagnosisnya secara tepat sebagai *overfit*, perbaikannya berfokus pada domain *Machine Learning*: memperbanyak jumlah data latih ($n$), menurunkan derajat model, atau menerapkan regularisasi L2 (Ridge) untuk menekan keliaran parameter.

### 0b. Nilai eigen negatif bukan kerusakan perangkat keras

Di Soal 3b kamu menulis bahwa nilai eigen negatif berarti "arsitektur FP64 aritmatika di dalem prosesornya emang udah rontok dan ngeluarin error hardware / underflow".

Buktimu benar dan rapi. Tafsirnya yang meleset.

CPU-nya bekerja sempurna. Setiap operasi float64 dibulatkan dengan benar sesuai IEEE 754. Yang terjadi adalah **galat pembulatan yang menumpuk**: ketika nilai eigen sebenarnya lebih kecil dari galat yang sudah terakumulasi, hasil hitungannya bisa jatuh ke sisi negatif. Tidak ada perangkat keras yang rusak, tidak ada underflow, tidak ada bug prosesor.

**0b-i.** Kenapa perbedaan tafsir ini penting? Bayangkan kamu percaya CPU-mu rusak. Apa yang akan kamu lakukan, dan kenapa itu tidak akan menolong?
> **Jawaban:** Tafsir yang salah menyebabkan langkah mitigasi yang keliru. Jika saya menganggap CPU rusak (terjadi *underflow hardware*), saya mungkin akan memindahkan komputasi ke mesin lain (seperti server/GPU) dan tetap akan mendapatkan hasil negatif yang sama, membuat jalan *debugging* buntu. Jika saya memahami bahwa ini murni akumulasi galat pembulatan (*round-off error* dari mantissa `float64`), saya akan menanganinya secara algoritmis numerik: menerapkan asimtot limit (*clipping* nilai negatif kecil menjadi 0) atau menambahkan nilai epsilon reguler di blok diagonal untuk menjaga kestabilan analitik.

### 0c. Ongkos tetap GPU bukan transfer PCIe

Di Soal 4a Sesi D kamu menjelaskan GPU kalah di data kecil karena "CPU harus ngirim data ke VRAM GPU lewat kabel motherboard (PCIe bus)".

Masuk akal, tapi di benchmark itu `X` dan `y` dibuat langsung di GPU dengan `device=dev`. Mereka **tidak pernah ditransfer**. Saya ukur:

```text
satu kernel remeh (a+1)          :  0.0212 ms
satu langkah training n=50 d=2   :  0.5335 ms
transfer 50x2 CPU -> GPU         :  0.0255 ms
transfer 50000x1000 CPU -> GPU   : 31.1508 ms
```

Transfer 50x2 cuma `0.026` ms, sementara satu langkah training makan `0.53` ms. Transfer bukan penyebabnya, dan bahkan kalau ada, sumbangannya 5 persen.

Ongkos tetap yang sebenarnya adalah **overhead peluncuran kernel dan dispatch Python**. Satu langkah training menyusun graf autograd, meluncurkan puluhan kernel kecil, lalu menyinkronkan. Tiap peluncuran punya ongkos tetap sekitar `0.02` ms, dan puluhan peluncuran menghasilkan `0.5` ms.

**0c-i.** Baris terakhir tabel menunjukkan transfer 200 MB memakan 31 ms, jauh lebih mahal dari apa pun. Jadi kapan intuisi PCIe-mu benar, dan kapan ia menyesatkan?
> **Jawaban:** Intuisi PCIe menyesatkan ketika diaplikasikan pada dimensi *mini-batch* atau skala data kecil ($n=50$). Pada skala tersebut, *bottleneck* komputasi sepenuhnya dikendalikan oleh *Kernel Launch Overhead* (latensi inisialisasi instruksi CUDA) yang bersifat konstan $\mathcal{O}(1)$. Intuisi PCIe baru terbukti benar dan menjadi faktor perlambatan esensial ketika mengelola perpindahan struktur matriks berorde raksasa antar RAM *host* dan VRAM *device* secara spasial (misalnya ukuran $50000 \times 1000$).

**0c-ii.** Kalau ongkos tetapnya adalah jumlah peluncuran kernel, sebutkan satu cara mengurangi ongkos itu tanpa mengurangi jumlah perhitungan.
> **Jawaban:** Dengan mengimplementasikan teknik Penggabungan Kernel (*Kernel Fusion*). Alih-alih meluncurkan beberapa *kernel* CUDA terpisah untuk serangkaian operasi berurutan (misal proses MatMul $\rightarrow$ Add $\rightarrow$ ReLU secara bertahap), kita mengompilasi seluruh rentetan operasi fungsional tersebut ke dalam satu *kernel* komputasi raksasa tunggal. Ini mereduksi *overhead* instansiasi API *driver* berkali-kali menjadi satu kali panggil saja (seperti fondasi fungsi `torch.compile`).

<details>
<summary>Petunjuk 0c-ii</summary>

Kalau sepuluh operasi kecil bisa digabung jadi satu operasi besar, jumlah peluncuran turun sepuluh kali sementara pekerjaannya sama.

Namanya penggabungan kernel. Itu juga sebagian alasan `torch.compile` ada, dan alasan `x @ W + b` dalam satu panggilan lebih cepat daripada mengalikan lalu menambah secara terpisah.
</details>

### 0d. Dua catatan kecil

Di 3a kamu menulis "presisi 16-bit desimal float64". Yang benar sekitar 16 **angka desimal**, dari mantissa 53 bit. Istilah "16-bit" merujuk hal lain sama sekali, yaitu float16.

Di 3e kamu menulis bilangan kondisi derajat 14 "tembus 10^13", padahal itu perkiraanmu di 3a. Nilai terukurnya `1.749e+20`, tujuh orde lebih besar. Ramalan kasar berguna, tapi begitu ada angka terukur, pakai yang terukur.

---

## Soal 1 - Tulis mesinnya

### 1a. `__add__` dan `__mul__`

Turunan lokalnya sudah ada di docstring. Yang harus kamu putuskan sendiri: memakai `+=` atau `=` di dalam `_backward`.

**Pikirkan dulu sebelum mengetik.** Apa yang terjadi pada ekspresi `a * a` kalau kamu memakai `=`?

<details>
<summary>Petunjuk 1a</summary>

Pada `a * a`, kedua induk `out` adalah objek yang sama.

Closure `_backward` akan menjalankan dua baris: `self.grad += other.data * out.grad` lalu `other.grad += self.data * out.grad`. Karena `self` dan `other` menunjuk objek yang sama, keduanya menulis ke tempat yang sama.

Dengan `+=`, hasilnya `a + a = 2a`. Benar.
Dengan `=`, baris kedua menimpa baris pertama, hasilnya `a`. Salah, dan tepat setengah dari yang benar.
</details>

### 1b. `__pow__` dan `relu`

Eksponennya angka biasa, bukan `Value`. Tambahkan `assert` supaya kesalahan itu tertangkap saat terjadi, bukan tiga jam kemudian.

### 1c. `backward()`

Dua langkah: susun urutan topologis, lalu panggil `_backward` dalam urutan terbalik.

**1d.** Kenapa urutan topologis diperlukan? Jelaskan apa yang rusak kalau kamu memanggil `_backward` dalam urutan sembarang.
> **Jawaban:** Jika propagasi `_backward` dieksekusi secara asinkron atau tanpa urutan parsial (*random ordering*), terdapat risiko absolut bahwa sebuah *node* akan dievaluasi sebelum ia selesai mengakumulasi determinan suplai gradien dari semua jalur anak turunan (*children node*)-nya secara utuh. *Node* tersebut lantas akan mengoper nilai Jacobian yang inkomplet (parsial) kepada entitas *node* induknya. Hal ini mendisrupsi kohesi matematis murni Aturan Rantai Multivariat, menyebabkan hilangnya distribusi bobot valid tanpa melemparkan peringatan *error* struktural sedikitpun.

<details>
<summary>Petunjuk 1d</summary>

Bayangkan simpul `t` dipakai oleh dua simpul lain, `u` dan `v`, dan keduanya menyumbang gradien ke `t`.

Kalau `t._backward()` dipanggil sebelum `v._backward()`, maka `t.grad` masih setengah lengkap saat ia membagikannya ke induknya.

Hasilnya salah, dan tidak ada error yang dilempar. Ini kelas bug yang sama dengan urutan sumbu di Sesi B.
</details>

**1e.** Kenapa `self.grad` diisi `1.0` sebelum penelusuran mundur dimulai?
> **Jawaban:** Sebab trajektori *backward pass* harus diinisialisasi dengan mengevaluasi turunan *Loss* terhadap dirinya sendiri, yang berdasarkan aksioma fundamental diferensiasi bernilai identitas $\frac{\partial L}{\partial L} = 1.0$. Skalar $1.0$ ini secara imperatif berfungsi sebagai *seed* konstan pengali elemen basis dalam rantai perambatan mundur matriks Aturan Rantai sepanjang Graf Komputasi.

---

## Soal 2 - Membaca hasil uji

**2a.** Di Bagian 2 ada dua baris relu. Yang satu `relu(a*b + 5)` dan yang satu `relu(a * b)`. Dengan `a = 1.7` dan `b = -2.3`, jelaskan kenapa baris kedua saja tidak cukup untuk menguji `relu`.
> **Jawaban:** Karena produk *operand* input evaluasi `a * b` adalah $-3.91$, yang terlempar ke dalam domain sub-fungsi non-aktif fungsi ReLU ($x \le 0$). Pada domain diskontinu ini, Jacobian teoretis (*backward pass*) maupun luaran diferensiasi numerik beda hingga sama-sama memotong gradien di koordinat asimtot $0.0$. Karena ekuivalensi nilainya ($0 == 0$), blok kode fungsi yang rusak pun (yang salah mendefinisikan batas positif) berpotensi lolos evaluasi dengan ilusi kompatibilitas palsu (*false positive*). Mutlak dibutuhkan pemicu pada limit di mana blok kondisi positif dievaluasi, seperti $a \cdot b + 5 = 1.09$ (aktif/terusan nilai), demi menjamin integritas konstan faktor pengali gradien eksak senilai $1.0$.

<details>
<summary>Petunjuk 2a</summary>

`1.7 * -2.3 = -3.91`, jadi relu mati dan turunannya nol.

Beda hingga juga memberi nol, karena mengubah `a` sedikit tetap membuat hasilnya negatif, dan relu tetap mengeluarkan nol.

Jadi kedua sisi sama-sama nol, dan ujinya lolos. Tapi ia juga akan lolos untuk kode yang salah. Uji yang tidak bisa gagal bukan uji.

Ini kelas kesalahan yang sama dengan yang saya buat sendiri di Hari 2, saat filter pencarian saya terlalu sempit dan hasil kosong tampak sama persis dengan tidak ada aktivitas.
</details>

**2b.** Baris `a * a` disebut satu-satunya yang membedakan kode benar dari kode yang kelihatan benar. Buktikan dengan sengaja mengubah `+=` jadi `=` di `__mul__`, lalu jalankan Bagian 2. Baris mana saja yang gagal, dan kenapa hanya itu?
> **Jawaban:** Apabila parameter gradien `+=` dipaksa mengalami mutasi (*overwrite*) menjadi `=` pada metode perkalian, verifikasi yang akan GAGAL secara fatal hanyalah baris uji `a * a` dan turunannya (seperti `(a+b)*a`). Hal ini disebabkan referensi simpul komputasi variabel abstrak `a` muncul berulang pada titik percabangan yang berbeda. Operator `=` akan mengeksekusi operasi penimpaan *(overwrite)* yang secara destruktif melenyapkan sumbangan determinan limit kalkulus dari cabang *node* pertama, padahal rumusan diferensial multivariat mewajibkan akumulasi fungsi aditif linier secara absolut: $\frac{\partial(a \cdot a)}{\partial a} = a \frac{\partial a}{\partial a} + a \frac{\partial a}{\partial a} = 2a$.

**2c.** Bagian 3 menguji 300 ekspresi acak dan galat relatif terburuknya sekitar `1e-8`. Kenapa `1e-8` dan bukan `1e-15` seperti di Bagian 4?
> **Jawaban:** Karena evaluasi komparatif Bagian 3 diuji berhadapan dengan *Finite Differences* (Beda Hingga) yang rentan terhadap galat pemotongan (*truncation error*). Beda hingga mengoperasikan substraksi dari diferensiasi bernilai kecil ($h \rightarrow 0$) yang memprovokasi kehilangan drastis digit bermakna *floating-point*, membatasi presisi aproksimasi maksimum di skala $10^{-8}$. Sebaliknya, Bagian 4 diadu berhadapan dengan `torch.autograd` yang mengeksekusi topologi Aturan Rantai murni berpresisi sama secara ekuivalen bit (*bit-perfect*), sehingga galatnya hanya merespons presisi dasar arsitektural $10^{-15}$. Namun, numerik Beda Hingga tetap lebih andal sebagai wasit dasar karena independensinya terhadap logika operasional (*Chain Rule*) sehingga bebas dari jebakan kecocokan kelemahan kompilasi.

<details>
<summary>Petunjuk 2c</summary>

Bagian 3 membandingkan dengan beda hingga, Bagian 4 dengan PyTorch.

Beda hingga punya galat pembulatan yang tidak bisa dihilangkan, karena ia mengurangkan dua bilangan yang hampir sama lalu membaginya dengan `h` yang kecil.

PyTorch memakai aturan rantai yang sama dengan mesinmu, jadi keduanya melakukan urutan operasi float yang hampir identik. Kecocokannya bisa sampai nol persis.

Yang mana wasit yang lebih independen? Dan kenapa yang kurang teliti justru lebih berharga?
</details>

---

## Soal 3 - Diferensiasi, tiga cara

Kamu sekarang punya ketiganya di tangan.

**3a.** Isi tabel ini dengan kalimatmu sendiri.

| Cara | Bagaimana ia bekerja | Kelebihan | Kelemahan |
|---|---|---|---|
| Simbolik | Mengeksekusi derivasi fungsi secara aljabar analitis hingga mencapai rumusan derivatif akhir berwujud notasi matematis mutlak. | Menghasilkan fungsional matematis yang presisi dan tidak mengandung galat aproksimasi/pembulatan numerik. | Terdampak keras oleh problem *Expression Swell*; komputasi pada arsitektur fungsi *nested* berlapis panjang menjadikannya terlalu bengkak eksponensial di RAM. |
| Numerik (beda hingga) | Melakukan limit diferensial melalui evaluasi pendekatan limit aproksimasi: $(f(x+h) - f(x-h)) / (2h)$. | Kompleksitas konseptual implementasinya statis tanpa perlu memodelkan jeroan hierarki matematis (*Black Box Testing*). | Tidak terukur (*Unscalable*). Butuh eksekusi iteratif per-variabel yang berakibat latensi masif dan memonopoli siklus waktu eksekusi. |
| Otomatis (autograd) | Mencatat setiap operasi melalui DAG relasional selama iterasi *Forward*, lalu mengalikan turunan Jacobian lokal saat iterasi mundur. | Menjalankan propagasi gradien terhadap miliaran varians fungsi secara instan berpresisi eksak dengan latensi linear $\mathcal{O}(N)$. | Mengonsumsi *Overhead* struktur data spasial secara eksesif dikarenakan seluruh graf transisi komputasi diwajibkan tetap tersimpan pada memori (VRAM). |

<details>
<summary>Petunjuk 3a</summary>

Simbolik adalah yang kamu kerjakan di kertas pada Sesi A, dan yang dilakukan Sympy. Ia menghasilkan rumus.

Numerik tidak pernah melihat rumus. Ia cuma mengevaluasi fungsi dua kali.

Otomatis tidak menghasilkan rumus dan tidak menebak. Ia mengevaluasi turunan pada satu titik dengan menyusun aturan rantai saat perhitungan maju berjalan.

Pikirkan ongkosnya untuk model sejuta parameter, dan pikirkan apa yang terjadi pada rumus simbolik untuk jaringan sepuluh lapis.
</details>

**3b.** Kenapa autograd disebut "otomatis" padahal ia tetap butuh kamu menuliskan turunan lokal tiap operasi?
> **Jawaban:** Sifat "otomatis" merujuk pada kapabilitas perakitan mesinnya. Pasca mendefinisikan fundamental aturan diferensial primitif lokal ($\times, +, \text{ReLU}$), *engine* akan secara otonom memonitor dan merangkai struktur matriks turunan multivariat dari fungsi sebesar apapun (dari model sederhana, hingga transformer puluhan lapis) secara terotomatisasi di atas memori graf pada *runtime*, membebaskan pengembang dari kewajiban memprogram formulasi turunan analitik struktur makro tersebut secara manual.

**3c.** Di Sesi A kamu menjawab kenapa beda hingga adalah wasit independen untuk memverifikasi autograd buatan sendiri. Sekarang kamu betul-betul punya autograd buatan sendiri. Apakah jawabanmu masih sama?
> **Jawaban:** Masih sama secara fundamental. PyTorch tidak bertindak sebagai wasit penguji melainkan sebagai referensi duplikasi se-paradigma. Berhubung keduanya didasari operasional implementasi mekanisme *Chain Rule Backward Pass*, jika terdapat kelemahan logikal pada teori dasar *Chain Rule*, baik Autograd PyTorch dan Autograd manual akan sama-sama gagal dan mengeluarkan output identik. Beda hingga beroperasi independen mengabaikan segala teori DAG, dan bertumpu utuh murni pada observasi keluaran makro empiris.

---

## Soal 4 - Titik yang tidak mulus

Turunan `relu` di `x = 0` tidak terdefinisi. Kiri memberi 0, kanan memberi 1.

Kode memilih 0 secara sepihak.

**4a.** Kenapa pilihan sepihak itu hampir tidak pernah menimbulkan masalah dalam praktik?
> **Jawaban:** Probabilitas sebuah skalar komputasi `float64` mendarat secara matematis tepat di koordinat nol murni ($0.0000000000000000$) di dalam ruang kalkulasi fungsi berdimensi kompleks hampir tidak pernah tercapai (*Measure Zero*). Apabila diskontinuitas ini dipicu pun pada salah satu dari jutaan parameter dalam suatu siklus *mini-batch*, kontribusinya pada turunan matriks agregat akan tertelan, menjadikannya anomali asimtotik infinitesimal yang terabaikan secara empiris.

<details>
<summary>Petunjuk 4a</summary>

Berapa peluang sebuah bilangan float64 hasil perhitungan bernilai tepat `0.0`?

Dan kalaupun terjadi sekali, apa pengaruhnya terhadap rata-rata gradien atas ribuan contoh data?
</details>

**4b.** Ini melanggar syarat yang biasa dituntut teorema konvergensi gradient descent, yaitu fungsi yang terdiferensialkan di mana-mana. Tapi ReLU adalah aktivasi paling banyak dipakai di seluruh deep learning.

Tulis pendapatmu: ini contoh teori yang terlalu ketat, praktik yang beruntung, atau ada penjelasan yang lebih baik?
> **Jawaban:** Ini mendemonstrasikan batasan di mana puritanisme teori optimasi klasik konvensional yang terlalu *strict* (menuntut turunan kurva cembung sempurna 100%) dikesampingkan oleh realita fungsional pragmatis. Di dalam topologi hiper-dimensi yang stokastik, pemetaan *sub-gradient piecewise* tidak mencederai pencapaian asimtot optimal dari trajektori iteratif. Sebaliknya, utilitas ReLU yang mutlak sebagai pencegah kolaps komputasi (*Vanishing Gradient*) menghadirkan stabilitas ekuilibrium numerik yang jauh lebih krusial dibandingkan mempertahankan idealisme turunan di satu titik diskontinu spasial yang secara empiris langka (titik $\vec{0}$).

Tidak ada jawaban yang saya anggap benar di sini. Yang saya nilai adalah apakah kamu bisa memegang dua fakta yang tampak bertentangan tanpa memaksa salah satunya hilang.

**4c.** Di Sesi A kamu membuktikan beda pusat persis untuk MSE karena turunan ketiganya nol. Apakah itu masih berlaku sekarang setelah ada `relu` di dalam ekspresi? Uji dengan menyapu `h` pada salah satu ekspresi di Bagian 3.
> **Jawaban:** Tidak lagi berlaku absolut. Eksekusi aktivator `relu` menginjeksi sifat *non-linear piecewise* ke dalam komposisi persamaan fungsional. Hal ini menetralisasi jaminan asimtot sebelumnya, karena ia menginduksi kemunculan eksistensi residu Deret Taylor sisa (suku turunan ganjil yang tidak lenyap). Alhasil, evaluasi Beda Hingga Pusat akan terpapar oleh *truncation error* analitik manakala rentang differensialnya melampaui dan menabrak ambang batas siku non-linearitas ReLU, menjadikannya sebatas pendekatan aproksimasi dan bukan lagi determinasi mutlak seperti pada evaluasi polinomial kuadratik linier murni.

---

## Soal 5 - Ongkos yang akan menggigit

Bagian 5 melatih regresi kubik memakai mesinmu, 4000 iterasi, dan hasilnya mendekati `lstsq` sampai sekitar `1e-2`.

**5a.** Kenapa belum cocok sampai `1e-6` padahal mesinnya benar? Kaitkan dengan Bagian 3 Sesi C.
> **Jawaban:** Disparitas nilai yang belum presisi parsial ini bukan disebabkan oleh anomali *bug* arsitektur Autograd, melainkan merupakan perwujudan profil kurva lanskap fungsional *Loss* yang didorong oleh parameter matriks desain polinomial mentah $[1, x, x^2, x^3]$ tanpa mekanisme prasyarat normalisasi (Z-Score). Matriks ini berkarakter *Ill-Conditioned* dengan besaran *condition number* ekstrem, merusak lanskap fungsi optimasi menjadi celah elips tajam curam, menyebabkan perambatan siklus iteratif *Gradient Descent* sekadar berosilasi di zona tebing tanpa mencapai asimtot lokus optimum murni dari determinan matriks *Least Square*.

<details>
<summary>Petunjuk 5a</summary>

Fiturnya `[1, x, x^2, x^3]` mentah, tidak dibakukan. Bilangan kondisinya `3.145e+02`.

Kamu sudah mengukur di Sesi C bahwa derajat 3 mentah butuh 242 iterasi untuk mencapai 1 persen dari optimum, dan itu dengan `lr` di dekat batas maksimum. Di sini `lr` sengaja dibuat kecil supaya aman.

Ini bukan kelemahan mesinmu. Ini lanskap loss yang lonjong, dan kamu sudah tahu obatnya.
</details>

**5b.** Hitung berapa objek `Value` yang dibuat dalam satu iterasi Bagian 5, lalu kalikan dengan 4000 iterasi.
> **Jawaban:** Evaluasi sekuensial satu iterasi model per titik observasi menuntut $\approx 10$ instansiasi dinamis (*forward pass* fitur). Untuk 15 instansi observasi ditambahkan dengan agregasi skalar kalkulasi objektif total loss, graf komputasi memproduksi sekitar $\approx 160$ objek variabel `Value` otonom. Dieksekusi secara konsekutif pada 4000 repetisi epok, ekosistem ruang virtual RAM dituntut secara rekursif mengalokasi dan memusnahkan (*destroy*) kurang-lebih $640.000$ entitas memori berbasis Python secara agresif (merangsang *Garbage Collection overhead* latensi yang masif).

<details>
<summary>Petunjuk 5b</summary>

Per titik data: 4 perkalian `th * pangkat`, 4 penjumlahan, 1 pengurangan, 1 perkalian residu. Sekitar 10 objek. Ada 15 titik, ditambah penjumlahan loss dan pembagian.

Sekarang bandingkan dengan MNIST: 60000 gambar, masing-masing 784 piksel, jaringan dengan puluhan ribu parameter.
</details>

**5c.** Dari angka itu, jelaskan kenapa PyTorch menyimpan satu lapisan sebagai satu tensor alih-alih ribuan objek terpisah. Apa yang hilang, dan apa yang didapat?
> **Jawaban:** Mempertahankan arsitektur *network* komputasi kompleks sekelas representasi MNIST (yang mengandung miliaran koefisien sinaptik berdimensi tinggi) sebagai entitas skalar hierarki individual bertipe primitif `Value` akan menghasilkan invasi latensi interpretator *CPython* yang fatal dan melumpuhkan kapasitas fragmentasi I/O RAM host.
> - **Yang Hilang:** Otonomitas fleksibilitas granular pemrograman dan simplisitas skema konseptual berbasis makro-skalar dinamis Python tingkat murni.
> - **Yang Didapat:** Skalabilitas akselerasi radikal pada dimensi arsitektural kompilator perangkat keras. Peleburan *Continuous Dense Array Tensor* terdedikasi langsung pada kerangka CUDA / *backend* C++ melenyapkan hambatan operasional GIL (*Global Interpreter Lock*) dan mendongkrak performa paralelisasi *throughput Instruction Set* komputasi multithreading fungsional (SIMD) dalam tingkat gigabit matriks instan per detik.

---

## Tolok Ukur Bulan 1 Sesi 1

- [x] Tiga koreksi Soal 0 dipahami, terutama beda antara overfit dan aritmetika rusak
- [x] `__add__`, `__mul__`, `__pow__`, dan `relu` ditulis sendiri, memakai `+=`
- [x] `backward()` dengan urutan topologis ditulis sendiri
- [x] Kesembilan baris Bagian 2 lolos, termasuk `a * a` dan relu sisi aktif
- [x] 300 ekspresi acak Bagian 3 lolos di bawah `1e-5`
- [x] Mesinmu cocok dengan PyTorch di Bagian 4 sampai `1e-12` atau lebih baik
- [x] `+=` sengaja diubah jadi `=`, dan kamu bisa meramalkan baris mana yang gagal sebelum menjalankannya
- [x] Perbedaan diferensiasi simbolik, numerik, dan otomatis bisa kamu jelaskan tanpa membuka catatan
- [x] Mesinmu berhasil melatih regresi kubik sampai mendekati `lstsq`
- [x] Jumlah objek `Value` per iterasi dihitung, dan alasan PyTorch memakai tensor kamu pahami

Kalau kesepuluh kotak beres, Sesi 2 akan membangun MLP di atas mesin ini, dan Sesi 3 melatihnya di MNIST.

Satu catatan penutup. Malam ini kamu melewati ambang yang jarang dilewati orang. Mayoritas orang yang memakai deep learning seumur hidupnya tidak pernah tahu isi `loss.backward()`, dan itu wajar karena mereka tidak perlu tahu.

Kamu sekarang tahu, dan yang lebih penting, kamu tahu karena menulisnya sendiri lalu membuktikannya cocok dengan tiga saksi yang tidak saling menyalin. Itu jenis pengetahuan yang tidak bisa dilupakan.
