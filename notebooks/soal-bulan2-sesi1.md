# Soal Bulan 2 Sesi 1 - Kata jadi angka

Berkas latihan: [`bulan2_sesi1_kata.py`](bulan2_sesi1_kata.py)

Bulan 1 kamu bikin mesin yang bisa menurunkan apa saja. Sekarang mesin itu
dipakai untuk sesuatu yang bukan angka.

Yang kamu tulis malam ini bukan latihan yang dibuang. Ini otak perintah rutin
SYNESIS, dan ia akan menjawab tanpa menyentuh VRAM sama sekali.

---

## Soal 1 - Karung berisi kata

`ke_vektor` membuang urutan kata sepenuhnya. "anjing menggigit orang" dan
"orang menggigit anjing" menghasilkan vektor yang identik.

**1a.** Untuk penerjemah bahasa, itu cacat fatal. Untuk pengklasifikasi intent
milikmu, ternyata hampir tidak masalah. Jelaskan bedanya.

> **Jawaban:** Penerjemah harus menjaga hubungan antarkata: siapa melakukan
> apa kepada siapa. Pengklasifikasi ini hanya perlu memilih satu kategori.
> Kata seperti `disk`, `ram`, atau `buka` sering sudah cukup walau urutannya
> dibuang. Jadi bag-of-words boleh dipakai selama informasi yang dibuang memang
> tidak diperlukan untuk memilih intent.

<details>
<summary>Petunjuk 1a</summary>

Pertanyaannya: berapa banyak informasi yang kamu butuhkan untuk memutuskan?

Menerjemahkan butuh tahu siapa pelaku dan siapa korban. Memutuskan bahwa
"berapa sisa disk" itu `info_sistem` cuma butuh melihat kata "sisa" dan
"disk" ada di kalimatnya, tak peduli urutannya.

Bag-of-words membuang informasi. Yang menentukan adalah apakah yang dibuang
itu informasi yang kamu perlukan.
</details>

**1b.** Bagian 1 mencetak "persen nol : 97,2 persen". Kalau kosakatamu tumbuh
dari 106 jadi 3000 kata karena kamu menambah 400 contoh, angka itu naik atau
turun? Dan apa akibatnya pada ukuran memori?

> **Jawaban:** Naik. Kalimat tiga kata hanya mengisi sekitar `3/3000`, jadi
> sekitar 99,9% elemennya nol. Vektor padat dan matriks bobot tumbuh sebanding
> dengan kosakata: dari 106 ke 3000 berarti sekitar 28,3 kali lebih besar.

**1c.** Kenapa `bangun_kosakata` harus mengurutkan katanya secara alfabet?
Apa yang rusak kalau urutannya berubah tiap kali program dijalankan?

> **Jawaban:** Indeks kata adalah arti setiap kolom. Kalau urutan berubah,
> bobot yang kemarin milik `disk` bisa dibaca sebagai bobot `buka`. Model yang
> dimuat akan memberi keputusan salah walau bentuk matriksnya masih cocok.

<details>
<summary>Petunjuk 1c</summary>

Bayangkan kamu melatih model hari ini, menyimpan bobotnya, lalu memuatnya
besok. Bobot ke-17 milik kata apa?
</details>

---

## Soal 2 - Hasil kali dalam, lagi

Jalankan Bagian 2. Kamu akan melihat:

```text
berapa sisa disk                      vram nya masih sisa berapa              0.516
buka laporan praktikum minggu lalu    buka dokumen skripsi                    0.258
cari file python di folder notebooks  cari semua gambar png                   0.204
berapa sisa disk                      buka dokumen skripsi                    0.000
jalankan script sesiA                 run notebook bulan 1                    0.000
```

**2a.** Baris keempat dan kelima sama-sama nol, tapi artinya berbeda sama
sekali. Jelaskan bedanya, dan kenapa cuma satu di antaranya yang jadi masalah.

> **Jawaban:** Baris keempat nol karena kalimatnya memang beda maksud. Itu
> hasil yang benar. Baris kelima nol padahal maksudnya sama; sinonim `jalankan`
> dan `run` tidak dikenali. Nol kedua menunjukkan informasi makna yang hilang.

**2b.** Baris pertama skornya 0,516, bukan 1,0, padahal maksudnya sama persis.
Hitung sendiri kenapa. Kedua kalimat itu berbagi dua kata dari berapa?

> **Jawaban:** Kalimat pertama punya 3 kata, kedua 5 kata, dan yang sama hanya
> `berapa` serta `sisa`. Maka skornya
> $2/(\sqrt{3}\sqrt{5})=2/\sqrt{15}=0{,}516$.

**2c.** Rumus kemiripan kosinus itu

$$\text{mirip}(a,b) = \frac{a \cdot b}{|a||b|}$$

Kamu sudah menulis operasi ini tiga kali dengan nama berbeda. Sebutkan
ketiganya dan apa yang diwakili sumbunya masing-masing.

> **Jawaban:** Dalam bra-ket $\langle\psi|\phi\rangle$, sumbunya adalah keadaan
> basis kuantum. Dalam $X^T X$, sumbunya adalah fitur atau kolom matriks desain.
> Di sini $a\cdot b$, sumbunya adalah kata dalam kosakata. Operasinya sama;
> arti koordinatnya yang berbeda.

<details>
<summary>Petunjuk 2c</summary>

Satu di Fisika Kuantum. Satu di Sesi C Bulan 0, saat kamu membangun matriks
desain. Satu di sini.

Rumusnya identik. Yang berubah cuma apa arti satu sumbu.
</details>

---

## Soal 3 - Kebutaan yang harus kamu tangani

`jalankan` dan `run` maksudnya sama, dan skornya nol.

Ada tiga cara memperbaikinya, dengan ongkos yang sangat berbeda. Untuk tiap
cara, tulis apa yang harus kamu kerjakan, dan apa yang kamu bayar.

**3a. Daftar sinonim buatan tangan.** Kamu tulis sendiri bahwa `run` sama
dengan `jalankan`.

> **Jawaban:** Normalisasikan alias sebelum vektorisasi, misalnya `run` menjadi
> `jalankan`. Murah dan mudah dibaca, tetapi daftar harus dirawat sendiri dan
> tidak akan pernah mencakup semua variasi bahasa.

**3b. Tambah contoh latih.** Kamu tidak memperbaiki apa pun, cuma menambah
lebih banyak kalimat berlabel sampai kedua kata itu sama-sama punya bobot
tinggi ke kelas yang sama.

> **Jawaban:** Tambahkan contoh nyata yang memakai kedua kata. Ongkosnya waktu
> melabeli data, tetapi tidak menambah model, VRAM, atau ketergantungan.

**3c. Embedding terlatih.** Ganti hitung-kata dengan vektor dari model yang
sudah dilatih di korpus besar, yang memang menempatkan `run` dan `jalankan`
berdekatan.

> **Jawaban:** Sinonim bisa dekat tanpa didaftarkan satu per satu. Bayarannya
> adalah model tambahan, RAM/VRAM, waktu muat, dan hasil yang lebih sulit
> ditelusuri saat salah.

**3d.** Untuk SYNESIS di laptopmu, mana yang kamu pilih, dan kenapa. Jawab
dengan menyebut kendala yang paling mengikat.

> **Jawaban:** Pakai 3b sebagai jalan utama, ditambah 3a untuk beberapa alias
> yang sangat sering dipakai. Laptop hanya punya VRAM 4 GB dan proyek dirawat
> satu orang, jadi embedding tambahan belum sepadan. Menambah contoh memang
> sudah menjadi pekerjaan Bulan 2.

<details>
<summary>Petunjuk 3d</summary>

Ingat kendala yang selalu menang di laptopmu: VRAM 4 GB, dan kamu satu-satunya
orang yang akan merawat ini.

Perhatikan juga bahwa 3b tidak menambah ketergantungan apa pun. Ia cuma
menambah kerja mengetik, dan kerja itu memang sudah ada di rencana Bulan 2.
</details>

---

## Soal 4 - Kenapa bukan MSE

Bulan 0 seluruhnya memakai MSE. Sekarang tiba-tiba entropi silang.

**4a.** Coba pakai MSE untuk klasifikasi. Ubah `rugi_silang` jadi
`mean((p - y)**2)`, jalankan Bagian 4, catat apa yang terjadi pada kurva
rugi dan akurasinya.

> **Jawaban:** Percobaan adil juga mengganti gradiennya menjadi gradien MSE.
> Rugi turun dari `0.25` ke `0.000926` dan tetap mencapai 100% karena data ini
> mudah. Namun akurasi sempurna baru tercapai di iterasi 85; entropi silang
> mencapainya di iterasi 54. Jadi MSE tidak selalu gagal total, tetapi sinyal
> belajarnya lebih mudah melemah.

**4b.** Turunkan kenapa. Untuk MSE dengan sigmoid, gradiennya mengandung
faktor $\sigma'(z) = \sigma(z)(1-\sigma(z))$. Berapa nilai faktor itu saat
model sangat yakin tapi sangat salah, misalnya $p = 0{,}999$ padahal $y = 0$?

> **Jawaban:** $p(1-p)=0{,}999\times0{,}001=0{,}000999$. Untuk
> $L=(p-y)^2$, gradien lengkapnya sekitar
> $2(0{,}999)(0{,}000999)=0{,}001996$: kecil walau ramalannya sangat salah.

**4c.** Sekarang hitung gradien entropi silang di titik yang sama. Apa
bedanya, dan kenapa itu menentukan?

> **Jawaban:** Gradien terhadap logit langsung $p-y=0{,}999$. Nilainya sekitar
> 500 kali gradien MSE di atas, sehingga model yang sangat yakin tetapi salah
> menerima koreksi kuat, bukan malah hampir berhenti.

<details>
<summary>Petunjuk 4b dan 4c</summary>

$\sigma(z)(1-\sigma(z))$ di $p = 0{,}999$ bernilai sekitar $0{,}000999$.

Artinya: model sangat salah, tapi sinyal perbaikannya nyaris nol. Ia terjebak.

Entropi silang dirancang supaya faktor itu saling menghapus. Yang tersisa
persis $p - y$, yang bernilai $0{,}999$ di titik itu. Sangat salah, sangat
kuat dikoreksi.

Itu bukan kebetulan matematis. Entropi silang memang dipilih karena
menghasilkan pembatalan itu.
</details>

---

## Soal 5 - Buktikan p minus y

Di video Bulan 1 Bab 2 kamu melihat $\partial L/\partial z = p - y$ muncul
begitu saja. Sekarang buktikan.

**5a.** Untuk satu contoh, dengan $z = w \cdot x + b$ dan $p = \sigma(z)$ dan

$$L = -\bigl[y \log p + (1-y)\log(1-p)\bigr]$$

turunkan $\partial L/\partial z$ langkah demi langkah sampai dapat $p - y$.

> **Jawaban:**
> $$\frac{\partial L}{\partial p}=-\frac{y}{p}+\frac{1-y}{1-p}
> =\frac{p-y}{p(1-p)}$$
> dan $\partial p/\partial z=p(1-p)$. Keduanya dikalikan, faktor
> $p(1-p)$ habis, sehingga $\partial L/\partial z=p-y$.

**5b.** Lanjutkan sampai $\partial L/\partial w$ dan $\partial L/\partial b$,
lalu bandingkan dengan yang kamu tulis di `gradien_logistik`.

> **Jawaban:** Karena $\partial z/\partial w=x$ dan
> $\partial z/\partial b=1$, untuk satu contoh didapat
> $\partial L/\partial w=(p-y)x$ dan $\partial L/\partial b=p-y$.
> Untuk satu batch tinggal dirata-ratakan: `X.T @ (p-y) / n` dan
> `mean(p-y)`, sama dengan kode.

**5c.** Jalankan Bagian 3. Galat relatifnya harus di bawah `1e-6`. Kalau
lolos, kamu baru saja membuktikan turunan kertasmu benar tanpa mempercayai
kertasnya.

> **Jawaban:** Lolos. Galat relatif `dL/dw = 1.166e-10` dan
> `dL/db = 1.440e-11`.

**5d.** Bagian 3 menyebut beda pusat tidak lagi eksak di sini, berbeda dengan
Sesi A Bulan 0. Kenapa? Kaitkan dengan turunan ketiga.

> **Jawaban:** Galat utama beda pusat sebanding dengan $f'''(x)h^2/6$.
> Untuk polinom derajat paling tinggi dua, turunan ketiganya nol sehingga
> rumus eksak, selain galat pembulatan. Sigmoid dan log punya turunan ketiga
> yang tidak nol, jadi selalu tersisa galat kecil berorde $h^2$.

---

## Soal 6 - Akurasi seratus persen itu mencurigakan

Bagian 5 melaporkan akurasi latih 100 persen dan matriks kebingungan yang
diagonalnya sempurna.

**6a.** Hitung: berapa parameter yang dilatih, dan berapa contoh yang dipakai
melatihnya? Bagian 6 mencetak angka pertamanya.

> **Jawaban:** Ada 642 parameter untuk 36 contoh, atau sekitar 17,8 parameter
> per contoh.

**6b.** Kamu sudah pernah melihat rasio seperti ini. Di Sesi C Bulan 0, 15
titik data dengan 10 parameter menghasilkan apa? Apa nama gejalanya?

> **Jawaban:** Model menghafal titik latih dan buruk di luar data latih.
> Gejalanya bernama overfitting.

**6c.** Kenapa Bagian 5 tidak punya data uji, dan kenapa itu cacat yang harus
kamu perbaiki sebelum melangkah ke Sesi 2?

> **Jawaban:** Semua 36 kalimat dipakai untuk melatih sekaligus menilai.
> Akurasi 100% hanya membuktikan model bisa mengingat data yang sudah dilihat,
> bukan memahami kalimat baru.

**6d.** Rancang perbaikannya. Berapa contoh yang kamu sisihkan, dipilih
bagaimana, dan apa yang kamu ukur setelahnya.

> **Jawaban:** Sesi 2 memakai belahan berstrata 70/15/15. Pada 120 contoh,
> pembulatan per kelas menghasilkan 80 latih, 16 validasi, dan 24 uji. Validasi
> memilih model/epoch; uji hanya dipakai terakhir untuk akurasi, matriks
> bingung, presisi, dan recall.

<details>
<summary>Petunjuk 6d</summary>

Jangan asal potong 20 persen terakhir. Data di `DATA` terurut per kelas, jadi
memotong bagian belakang berarti kelas `tanya_umum` hilang seluruhnya dari
data latih.

Yang kamu butuhkan adalah pemisahan yang menjaga proporsi tiap kelas. Namanya
stratified split, dan kamu bisa menulisnya sendiri dalam lima baris.
</details>

---

## Soal 7 - Boltzmann, lagi-lagi

`softmax` menghasilkan

$$p_k = \frac{e^{z_k}}{\sum_j e^{z_j}}$$

**7a.** Tulis distribusi Boltzmann dari Fisika Statistik, lalu tunjukkan
pemetaan suku demi suku ke rumus di atas. Apa yang berperan sebagai energi,
dan apa yang berperan sebagai $kT$?

> **Jawaban:** Distribusi Boltzmann adalah
> $P_k=e^{-E_k/(kT)}/\sum_j e^{-E_j/(kT)}$. Jadi logit softmax memetakan ke
> $z_k=-E_k/(kT)$. Jika softmax ditulis `softmax(z/T_model)`, energi berperan
> sebagai $-z$ dan `T_model` berperan seperti $kT$ dalam satuan yang dipilih.

**7b.** Model bahasa punya parameter bernama `temperature`. Berdasarkan 7a,
ramalkan apa yang terjadi pada keluaran saat temperature mendekati nol, dan
saat temperature sangat besar. Jawab dengan bahasa fisika, bukan bahasa ML.

> **Jawaban:** Saat suhu mendekati nol, hampir seluruh populasi jatuh ke
> keadaan berenergi paling rendah. Saat suhu sangat besar, beda energi menjadi
> tidak penting dan populasi mendekati merata di semua keadaan.

**7c.** Di `softmax` kamu wajib mengurangi maksimum tiap baris sebelum `exp`.
Buktikan dalam satu baris aljabar bahwa itu tidak mengubah hasilnya. Lalu
jelaskan kenapa tanpa itu programnya rusak.

> **Jawaban:**
> $$\frac{e^{z_k-c}}{\sum_j e^{z_j-c}}
> =\frac{e^{-c}e^{z_k}}{e^{-c}\sum_j e^{z_j}}
> =\frac{e^{z_k}}{\sum_j e^{z_j}}.$$
> Memilih $c=\max(z)$ membuat eksponen terbesar tepat 1. Tanpanya, logit besar
> membuat `exp` menjadi tak hingga, lalu pembagian menghasilkan `nan`.

**7d.** Hapus pengurangan maksimum, lalu jalankan Bagian 5 dengan `W` awal
dikalikan 1000. Catat apa yang keluar.

> **Jawaban:** Pada data dan seed ini, `×1000` ternyata masih finite karena
> logit terbesar hanya `496.17`; latihan selesai dengan akurasi 86,1%. Jadi
> dugaan soal tidak terbukti pada skala itu. Pada `×1500`, logit terbesar
> `744.25`, `exp` overflow, dan muncul `nan`. Pengurangan maksimum membuat
> keduanya tetap aman.

---

## Soal 8 - Sambungan ke SYNESIS

Bagian 6 mencetak perbandingan ukuran: pengklasifikasi 5 KB lawan model
1.900.000 KB.

**8a.** Sebutkan tiga jenis perintah yang harus ditangani pengklasifikasi, dan
tiga yang harus dilempar ke LLM. Apa aturan pembedanya?

> **Jawaban:** Pengklasifikasi menangani perintah rutin dengan hasil tetap,
> misalnya membuka berkas, mencari berkas, dan membaca info sistem. LLM
> menangani penjelasan konsep, membandingkan beberapa pilihan, dan menyusun
> rencana. Aturannya: kalau keluaran bisa dipetakan ke fungsi dan argumen yang
> jelas, pakai pengklasifikasi; kalau perlu memahami konteks atau membuat
> jawaban baru, pakai LLM.

**8b.** Kelas `tanya_umum` di data latih itu sebenarnya bukan intent, tapi
pintu keluar. Jelaskan kenapa memberi nama pada "tidak tahu" lebih baik
daripada memakai ambang keyakinan.

> **Jawaban:** Contoh `tanya_umum` mengajari model bentuk kalimat yang memang
> harus keluar menuju LLM. Ambang hanya melihat besar angka softmax, padahal
> softmax bisa sangat yakin pada kalimat asing. Kelas pintu keluar mempelajari
> keputusan itu dari contoh, walau ambang tetap berguna sebagai pagar kedua.

<details>
<summary>Petunjuk 8b</summary>

Ambang keyakinan pada softmax itu tipuan. Softmax selalu menghasilkan angka
yang berjumlah satu, bahkan untuk masukan yang benar-benar di luar semua
kelas. Ia bisa sangat yakin dan sangat salah.

Melatih kelas pembuangan secara eksplisit membuat "ini bukan urusanku"
menjadi keputusan yang dipelajari, bukan tebakan dari ambang.
</details>

**8c.** Kalau pengklasifikasi salah menebak dan menjalankan alat yang salah,
apa yang menahan kerusakannya? Sebut mekanismenya di `synesis/alat.py`.

> **Jawaban:** Alat `jalankan` tidak bergerak tanpa callback `izin` yang
> mengembalikan `True`. Tanpa persetujuan manusia ia membatalkan perintah.
> Akses berkas juga melewati pagar jalur, dan proses shell dibatasi 60 detik.

**8d.** Perkirakan: berapa milidetik yang dibutuhkan pengklasifikasi ini untuk
satu perintah? Ukur, jangan tebak.

> **Jawaban:** Pengukuran 20.000 kali untuk tokenisasi, vektorisasi,
> perkalian, softmax, dan argmax memberi sekitar **0,016 ms per perintah**.
> Angka dapat sedikit berubah antarrun karena penjadwalan CPU.

---

## Tolok Ukur Bulan 2 Sesi 1

- [x] `bangun_kosakata` dan `ke_vektor` ditulis sendiri, kosakata terurut
- [x] `kemiripan` ditulis sendiri, dan hubungannya dengan bra-ket bisa dijelaskan
- [x] `sigmoid` aman dari overflow, dibuktikan dengan masukan -1000
- [x] `rugi_silang` aman dari log nol
- [x] `gradien_logistik` diturunkan di kertas dulu, baru dikode
- [x] Bagian 3 lolos, galat relatif di bawah `1e-6`
- [x] MSE dicoba dan kegagalannya diamati sendiri, bukan dipercaya dari soal
- [x] `softmax` ditulis sendiri, dan pengurangan maksimum dibuktikan tidak mengubah hasil
- [x] Rusaknya softmax tanpa pengurangan maksimum dilihat sendiri
- [x] Akurasi 100 persen dipahami sebagai gejala, bukan prestasi
- [x] Pemisahan latih dan uji berstrata dirancang
- [x] Waktu satu klasifikasi diukur dalam milidetik

Kalau kedua belas kotak beres, Sesi 2 mengubah ini jadi komponen SYNESIS yang
sungguhan: 300 sampai 500 perintahmu sendiri, ekstraksi parameter, dan gerbang
keamanan.
