# Soal Sesi B - Lanskap dan langkah

Berkas latihan: [`sesiB_lanskap.py`](sesiB_lanskap.py)

Sesi A memberimu angka. Sesi ini memberimu gambar, dan gambar itu yang akan kamu bawa sampai Bulan 5.

Aturan mainnya sama. Kerjakan sendiri minimal 15 menit sebelum membuka petunjuk, dan tulis ramalanmu sebelum menjalankan kode.

Satu aturan tambahan khusus sesi ini: **buka setiap gambar yang dihasilkan, jangan cuma baca angkanya di terminal.** Sesi ini seluruh gunanya ada di gambar.

---

## Soal 0 - Dua hal dari Sesi A yang belum tuntas

Sebelum masuk materi baru, dua utang dari kemarin.

**0a.** Soal 4d Sesi A meminta kamu **membuktikan** bahwa garis optimum lewat titik $(\bar{x}, \bar{y})$. Jawabanmu menunjuk ke keluaran program, dan itu verifikasi numerik, bukan bukti.

Bedanya penting. Program menunjukkan bahwa untuk 50 titik ini, dengan seed ini, angkanya cocok sampai 6 desimal. Bukti menunjukkan bahwa itu berlaku untuk data apa pun, selamanya, dan menjelaskan kenapa.

Kerjakan buktinya sekarang di kertas. Tiga baris cukup.

<details>
<summary>Petunjuk 0a</summary>

Mulai dari syarat titik stasioner:

$$\frac{\partial \text{MSE}}{\partial b} = \frac{2}{n}\sum_i r_i = 0 \quad\Longrightarrow\quad \sum_i (w x_i + b - y_i) = 0$$

Sekarang bagi kedua ruas dengan $n$, lalu pisahkan penjumlahannya jadi tiga bagian. Suku mana yang jadi $\bar{x}$, dan suku mana yang jadi $\bar{y}$?
</details>

**0b.** Di Soal 5b Sesi A kamu memakai $A \approx 8.33$. Angka itu adalah $E[x^2] = 25/3$ untuk sebaran seragam di $[-5, 5]$, yaitu nilai **populasi**.

Nilai untuk **sampelmu** adalah `np.sum(x*x)/len(x)` = `7.8435`.

Ramalanmu jadi `1/8.33 = 0.120`, sementara nilai sampel memberi `1/7.8435 = 0.1275`. Kedua-duanya jatuh di celah antara `0.12` dan `0.13`, jadi sapuan kasar di Bagian 5 Sesi A tidak bisa membedakan mana yang benar.

Bagian 6 sesi ini menyapu dengan langkah yang jauh lebih halus. Sebelum melihat hasilnya, jawab: kalau `A = 8.33` benar, `lr = 0.123` harus bagaimana?

<details>
<summary>Petunjuk 0b</summary>

Ini bukan soal tentang siapa yang salah. Ini soal tentang cara merancang pengukuran yang bisa membedakan dua ramalan.

Dua ramalan yang sama-sama "cocok" dengan pengamatan kasar belum tentu sama-sama benar. Yang membedakan adalah pengamatan yang cukup teliti untuk memaksa keduanya berpisah. Cari daerah di mana keduanya meramalkan hal yang berbeda, lalu ukur di sana.
</details>

**0c.** Ini ketiga kalinya kamu memakai nilai populasi di tempat yang meminta nilai sampel. Pertama di Soal 3e Hari 3 dengan varians `2.25`, kedua di Soal 4b Sesi A, sekarang di sini.

Tulis satu kalimat aturan untuk dirimu sendiri, supaya yang keempat tidak terjadi.

---

## Soal 1 - Bangun permukaannya

### 1a. Tulis `permukaan_loss(x, y, ws, bs)`

Kisi loss untuk tiap pasangan `(w, b)`. Bentuk keluaran `(nb, nw)`, baris untuk `b` dan kolom untuk `w`.

Boleh pakai loop bersarang. Yang penting benar dulu.

<details>
<summary>Petunjuk 1a</summary>

Urutan indeksnya yang sering bikin tersandung. `L[j, i]` dengan `j` menelusuri `bs` dan `i` menelusuri `ws`.

Kalau kamu membaliknya, `contourf` dan `plot_surface` tetap menghasilkan gambar yang tampak masuk akal, cuma sumbunya tertukar. Ini jenis bug yang tidak melempar error, dan satu-satunya cara menangkapnya adalah memeriksa apakah dasar kisinya jatuh di dekat `w = 3.02`, `b = 1.74`.
</details>

### 1b. Tulis `sumbu_utama(x)`

Susun Hessian yang sudah kamu turunkan di Soal 5d Sesi A, lalu ambil nilai dan vektor eigennya.

$$H = \begin{pmatrix} 2A & 2\bar{x} \\ 2\bar{x} & 2 \end{pmatrix}$$

Pakai `np.linalg.eigh`. Vektor eigennya ada di **kolom** hasil, bukan baris.

### 1c. Tulis `permukaan_loss_vektor(x, y, ws, bs)`

Versi tanpa satu pun loop. Ini lanjutan langsung dari Hari 2.

<details>
<summary>Petunjuk 1c</summary>

Susun tiga sumbu supaya numpy bisa menyiarkan semuanya sekaligus:

```
ws  -> (1, nw, 1)
bs  -> (nb, 1, 1)
x   -> (1, 1, n)
y   -> (1, 1, n)
```

Aturan broadcasting dari Hari 2: sejajarkan dari kanan, tiap dimensi harus sama atau salah satunya `1`.

Ramalan `w*x + b` jadi berbentuk `(nb, nw, n)`. Kurangi `y`, kuadratkan, lalu rata-ratakan sepanjang sumbu terakhir dengan `axis=-1`.
</details>

**1d.** Catat rasio kecepatan loop terhadap vektor. Bandingkan dengan angka yang kamu dapat di Hari 2 untuk `dot_manual` lawan `np.dot`. Kenapa rasio di sini jauh lebih kecil?

<details>
<summary>Petunjuk 1d</summary>

Di Hari 2, loop terluar sampai terdalam semuanya berjalan di Python.

Di sini loop-nya cuma dua lapis, dan isi loop-nya adalah `mse(prediksi(...))` yang sudah tervektorisasi. Jadi yang berjalan di Python cuma `120 * 120` iterasi, bukan `120 * 120 * 50`.

Berapa persen pekerjaan yang sudah dikerjakan numpy bahkan di versi "loop"?
</details>

**1e.** Kisi 120 kali 120 dengan 50 titik data menghasilkan array antara berbentuk `(120, 120, 50)` di versi vektor. Hitung berapa MB memori yang dipakai. Lalu perkirakan kebutuhan memorinya kalau kisinya 2000 kali 2000 dan datanya 100 ribu titik.

<details>
<summary>Petunjuk 1e</summary>

`float64` memakan 8 byte. Kalikan saja.

Jawaban untuk kasus kedua akan mengejutkanmu, dan itu poinnya. Vektorisasi menukar waktu dengan memori, dan pertukaran itu punya batas. Kamu akan bertemu batas ini lagi di Bulan 5, saat matriks attention berukuran panjang konteks kuadrat.
</details>

---

## Soal 2 - Membaca mangkuknya

Buka `figures/sesiB_permukaan3d.png`.

**2a.** Panel kiri dan kanan menggambarkan permukaan yang sama, cuma sumbu tegaknya berbeda skala. Kenapa bentuk lonjongnya jauh lebih jelas di panel log?

**2b.** Di Soal 4a Hari 3 kamu membuktikan MSE berbentuk parabola terhadap `w` saat `b` dikunci. Sekarang `b` ikut bebas. Iris permukaan 3D itu dengan bidang datar mendatar. Bentuk apa yang kamu dapat, dan buktikan secara aljabar.

<details>
<summary>Petunjuk 2b</summary>

Loss-nya berbentuk kuadratik dalam dua peubah:

$$L(w,b) = \alpha w^2 + \beta b^2 + \gamma wb + \delta w + \epsilon b + \zeta$$

Menyamakan $L$ dengan sebuah tetapan menghasilkan persamaan derajat dua dalam dua peubah. Kamu sudah mengenal keluarga kurva ini dari Geometri Analitik.

Yang menentukan jenisnya adalah tanda diskriminan $\gamma^2 - 4\alpha\beta$, dan itu setara dengan tanda determinan Hessian. Berapa determinan Hessian-mu, dan apa artinya?
</details>

**2c.** Kalau kedua nilai eigen Hessian sama besar, seperti apa bentuk permukaannya, dan seperti apa lintasan gradient descent di atasnya?

---

## Soal 3 - Hessian yang tidak peduli pada `y`

Perhatikan `sumbu_utama(x)`. Ia cuma menerima `x`. Tidak ada `y` sama sekali.

Padahal loss jelas bergantung pada `y`. Ganti `y`, loss-nya berubah, dasarnya pindah.

**3a.** Jelaskan kenapa Hessian tidak bergantung pada `y`, sementara gradien bergantung.

<details>
<summary>Petunjuk 3a</summary>

Tulis loss-nya lengkap sebagai polinomial dalam `w` dan `b`. Di suku yang mana `y` muncul, dan berapa pangkat `w` atau `b` di suku itu?

Turunkan dua kali. Suku berpangkat berapa yang selamat dari dua kali penurunan?
</details>

**3b.** Terjemahkan ke fisika. Kalau loss adalah energi potensial, Hessian adalah apa? Dan kenapa masuk akal kalau besaran itu tidak bergantung pada `y`?

<details>
<summary>Petunjuk 3b</summary>

Untuk pegas, $V(x) = \frac{1}{2}kx^2$ dan $V''(x) = k$.

Menggeser pegas ke posisi setimbang yang berbeda mengubah $V$ dan mengubah gayanya. Apakah itu mengubah kekakuan pegasnya?

`y` menentukan di mana dasarnya. `x` menentukan seberapa kaku dindingnya. Dua peran yang berbeda.
</details>

**3c.** Konsekuensi praktisnya: kamu bisa menghitung `lr` maksimum yang aman **sebelum** melihat satu pun label. Kapan ini berguna, dan kapan ini menyesatkan?

<details>
<summary>Petunjuk 3c</summary>

Sifat ini datang dari model yang linear. Di jaringan berlapis dengan ReLU, apakah turunan kedua masih bebas dari `y`?

Jawaban yang benar untuk 3c bukan "selalu berguna" dan bukan "tidak pernah berguna".
</details>

---

## Soal 4 - Gergaji

Buka `figures/sesiB_lintasan.png` dan `figures/sesiB_sumbu_utama.png`.

**4a.** Tiga panel, tiga `lr`, satu permukaan. Jelaskan ketiga perilakunya lewat faktor pengali galat $(1 - \lambda \eta)$ yang kamu turunkan di Soal 5a Sesi A. Hitung faktornya untuk arah curam pada tiap `lr`.

<details>
<summary>Petunjuk 4a</summary>

$\lambda_{\text{curam}} = 15.72$.

- `lr = 0.01` memberi faktor $1 - 15.72(0.01) = 0.843$
- `lr = 0.06` memberi $1 - 15.72(0.06) = ?$
- `lr = 0.12` memberi $1 - 15.72(0.12) = ?$

Faktor positif berarti galat mengecil tanpa berganti tanda. Faktor negatif berarti berganti tanda tiap iterasi. Nilai mutlak menentukan seberapa cepat mengecil.

Sekarang cocokkan ketiga angka itu dengan ketiga gambar.
</details>

**4b.** Pada `lr` berapa gergaji mulai muncul? Turunkan angkanya, jangan ditebak dari gambar.

**4c.** Kolom panjang lintasan di terminal: `5.74` untuk `lr = 0.01`, `7.59` untuk `0.06`, dan `63.41` untuk `0.12`. Kenapa yang paling cepat mendekati dasar justru menempuh jarak paling jauh?

**4d.** Di gambar sumbu utama, gergajinya berayun sejajar panah yang mana, dan kemajuan sebenarnya terjadi sejajar panah yang mana? Jelaskan kenapa harus begitu.

**4e.** Bayangkan kamu boleh memakai dua `lr` berbeda, satu untuk arah curam dan satu untuk arah landai. Berapa nilai ideal masing-masing supaya galat di kedua arah lenyap dalam satu langkah?

<details>
<summary>Petunjuk 4e</summary>

Faktor pengali galat adalah $(1 - \lambda\eta)$. Supaya galatnya nol dalam satu langkah, faktornya harus nol.

$\eta = 1/\lambda$ untuk tiap arah, jadi $1/15.72$ dan $1/1.96$.

Ini yang dikerjakan metode Newton, dan alasannya tidak dipakai di deep learning adalah biaya. Menghitung dan membalik Hessian untuk model dua parameter itu remeh. Untuk model empat miliar parameter, Hessian-nya punya $1.6 \times 10^{19}$ elemen. Adam adalah hampiran murah untuk ide ini.
</details>

---

## Soal 5 - Batas yang tajam

Bagian 6 menyapu `lr` dengan langkah halus.

**5a.** Sebelum melihat tabelnya, tulis ramalanmu: di antara dua nilai `lr` mana batasnya jatuh?

**5b.** Ada satu baris berlabel `berayun tetap`. Loss-nya berhenti di sekitar 77 setelah 3000 iterasi, tidak meledak tapi juga tidak turun ke dasar. Jelaskan kenapa, lewat nilai faktor pengali galat di titik itu.

<details>
<summary>Petunjuk 5b</summary>

Di `lr` tepat sama dengan $2/\lambda_{\max}$, faktornya menjadi $1 - \lambda_{\max}\cdot\frac{2}{\lambda_{\max}} = -1$.

Galat dikalikan minus satu tiap iterasi. Tandanya bergantian, besarnya tidak pernah berubah.
</details>

**5c.** Sebut nama gejala ini di Mekanika. Sistem seperti apa yang berperilaku begini, dan berapa nilai koefisien redamannya?

**5d.** Ramalan Hessian 2D memberi `0.1272` dan ramalan 1D dengan `A` sampel memberi `0.1275`. Yang 2D lebih tepat. Kenapa yang 1D sedikit ketinggian?

<details>
<summary>Petunjuk 5d</summary>

Ramalan 1D menganggap arah `w` dan arah `b` sepenuhnya terpisah. Lihat elemen luar diagonal Hessian-mu. Nilainya `0.7047`, bukan nol.

Elemen itu nol cuma kalau $\bar{x} = 0$. Sebaran `x` kamu punya rata-rata `0.3523`, tidak persis nol karena 50 sampel.

Coba geser datanya supaya $\bar{x} = 0$ persis, lalu bandingkan lagi kedua ramalan. Ini juga menjelaskan kenapa orang membakukan fitur sebelum melatih model.
</details>

**5e.** Soal 5d barusan menyinggung pembakuan fitur. Kalau `x` digeser dan diskalakan supaya rata-ratanya nol dan simpangan bakunya satu, apa yang terjadi pada Hessian, pada bilangan kondisi, dan pada `lr` yang aman?

Kerjakan di kertas dulu, lalu uji dengan mengubah `buat_data`.

---

## Soal 6 - Animasi

Buka `figures/sesiB_animasi.gif` dan tonton sampai habis, minimal tiga kali.

**6a.** Tulis satu paragraf tentang apa yang kamu lihat, dengan bahasamu sendiri, tanpa memakai kata gradien, eigen, atau konvergen.

Ini bukan soal iseng. Kalau kamu bisa menceritakan gambar itu tanpa istilah, kamu sudah punya bendanya. Kalau tidak bisa, kamu baru punya labelnya.

**6b.** Panel kanan memakai skala log pada sumbu tegak. Coba ganti jadi linear, jalankan ulang, dan bandingkan. Mana yang lebih informatif, dan kenapa kurva loss hampir selalu digambar dalam skala log?

**6c.** Tambahkan satu bola lagi dengan `lr = 0.1274`, yang sudah divergen. Ramalkan dulu apa yang akan kamu lihat di kedua panel, lalu jalankan.

<details>
<summary>Petunjuk 6c</summary>

Kamu perlu mengubah batas sumbu di panel kiri, atau bolanya akan langsung keluar bingkai dalam beberapa bingkai pertama dan kamu tidak melihat apa pun.

Itu sendiri sebuah pelajaran tentang divergensi. Ia tidak melambat lebih dulu untuk memberi tahu kamu.
</details>

---

## Tolok Ukur Sesi B

- [ ] Bukti aljabar garis lewat titik pusat massa selesai di kertas (utang Soal 4d Sesi A)
- [ ] Aturan populasi lawan sampel ditulis sebagai satu kalimat untuk dirimu sendiri
- [ ] `permukaan_loss` benar, dan dasar kisinya jatuh di dekat `w = 3.02`, `b = 1.74`
- [ ] `permukaan_loss_vektor` menghasilkan array identik dengan versi loop
- [ ] Kebutuhan memori untuk kisi besar dihitung, dan batas vektorisasi kamu pahami
- [ ] Kamu bisa menjelaskan kenapa Hessian tidak bergantung pada `y`
- [ ] Ketiga perilaku lintasan dijelaskan lewat faktor $(1 - \lambda\eta)$, dengan angkanya
- [ ] Ambang munculnya gergaji diturunkan, bukan ditebak dari gambar
- [ ] Baris `berayun tetap` dijelaskan, dan padanan mekanikanya disebut
- [ ] Animasi ditonton, dan ceritanya bisa kamu tulis tanpa satu pun istilah teknis

Kalau kesepuluh kotak beres, Bulan 0 tinggal dua sesi lagi.

Satu catatan penutup. Sesi ini satu-satunya di Bulan 0 yang ditandai tidak boleh dipadatkan. Alasannya bukan karena materinya banyak, tapi karena hasilnya bukan pengetahuan melainkan gambaran di kepala. Gambaran tidak bisa dibaca cepat. Ia harus ditonton sampai kamu bosan, dan kebosanan itu tanda ia sudah masuk.
