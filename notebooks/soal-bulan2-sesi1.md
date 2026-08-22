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

**1c.** Kenapa `bangun_kosakata` harus mengurutkan katanya secara alfabet?
Apa yang rusak kalau urutannya berubah tiap kali program dijalankan?

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

**2b.** Baris pertama skornya 0,516, bukan 1,0, padahal maksudnya sama persis.
Hitung sendiri kenapa. Kedua kalimat itu berbagi dua kata dari berapa?

**2c.** Rumus kemiripan kosinus itu

$$\text{mirip}(a,b) = \frac{a \cdot b}{|a||b|}$$

Kamu sudah menulis operasi ini tiga kali dengan nama berbeda. Sebutkan
ketiganya dan apa yang diwakili sumbunya masing-masing.

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

**3b. Tambah contoh latih.** Kamu tidak memperbaiki apa pun, cuma menambah
lebih banyak kalimat berlabel sampai kedua kata itu sama-sama punya bobot
tinggi ke kelas yang sama.

**3c. Embedding terlatih.** Ganti hitung-kata dengan vektor dari model yang
sudah dilatih di korpus besar, yang memang menempatkan `run` dan `jalankan`
berdekatan.

**3d.** Untuk SYNESIS di laptopmu, mana yang kamu pilih, dan kenapa. Jawab
dengan menyebut kendala yang paling mengikat.

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

**4b.** Turunkan kenapa. Untuk MSE dengan sigmoid, gradiennya mengandung
faktor $\sigma'(z) = \sigma(z)(1-\sigma(z))$. Berapa nilai faktor itu saat
model sangat yakin tapi sangat salah, misalnya $p = 0{,}999$ padahal $y = 0$?

**4c.** Sekarang hitung gradien entropi silang di titik yang sama. Apa
bedanya, dan kenapa itu menentukan?

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

**5b.** Lanjutkan sampai $\partial L/\partial w$ dan $\partial L/\partial b$,
lalu bandingkan dengan yang kamu tulis di `gradien_logistik`.

**5c.** Jalankan Bagian 3. Galat relatifnya harus di bawah `1e-6`. Kalau
lolos, kamu baru saja membuktikan turunan kertasmu benar tanpa mempercayai
kertasnya.

**5d.** Bagian 3 menyebut beda pusat tidak lagi eksak di sini, berbeda dengan
Sesi A Bulan 0. Kenapa? Kaitkan dengan turunan ketiga.

---

## Soal 6 - Akurasi seratus persen itu mencurigakan

Bagian 5 melaporkan akurasi latih 100 persen dan matriks kebingungan yang
diagonalnya sempurna.

**6a.** Hitung: berapa parameter yang dilatih, dan berapa contoh yang dipakai
melatihnya? Bagian 6 mencetak angka pertamanya.

**6b.** Kamu sudah pernah melihat rasio seperti ini. Di Sesi C Bulan 0, 15
titik data dengan 10 parameter menghasilkan apa? Apa nama gejalanya?

**6c.** Kenapa Bagian 5 tidak punya data uji, dan kenapa itu cacat yang harus
kamu perbaiki sebelum melangkah ke Sesi 2?

**6d.** Rancang perbaikannya. Berapa contoh yang kamu sisihkan, dipilih
bagaimana, dan apa yang kamu ukur setelahnya.

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

**7b.** Model bahasa punya parameter bernama `temperature`. Berdasarkan 7a,
ramalkan apa yang terjadi pada keluaran saat temperature mendekati nol, dan
saat temperature sangat besar. Jawab dengan bahasa fisika, bukan bahasa ML.

**7c.** Di `softmax` kamu wajib mengurangi maksimum tiap baris sebelum `exp`.
Buktikan dalam satu baris aljabar bahwa itu tidak mengubah hasilnya. Lalu
jelaskan kenapa tanpa itu programnya rusak.

**7d.** Hapus pengurangan maksimum, lalu jalankan Bagian 5 dengan `W` awal
dikalikan 1000. Catat apa yang keluar.

---

## Soal 8 - Sambungan ke SYNESIS

Bagian 6 mencetak perbandingan ukuran: pengklasifikasi 5 KB lawan model
1.900.000 KB.

**8a.** Sebutkan tiga jenis perintah yang harus ditangani pengklasifikasi, dan
tiga yang harus dilempar ke LLM. Apa aturan pembedanya?

**8b.** Kelas `tanya_umum` di data latih itu sebenarnya bukan intent, tapi
pintu keluar. Jelaskan kenapa memberi nama pada "tidak tahu" lebih baik
daripada memakai ambang keyakinan.

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

**8d.** Perkirakan: berapa milidetik yang dibutuhkan pengklasifikasi ini untuk
satu perintah? Ukur, jangan tebak.

---

## Tolok Ukur Bulan 2 Sesi 1

- [ ] `bangun_kosakata` dan `ke_vektor` ditulis sendiri, kosakata terurut
- [ ] `kemiripan` ditulis sendiri, dan hubungannya dengan bra-ket bisa dijelaskan
- [ ] `sigmoid` aman dari overflow, dibuktikan dengan masukan -1000
- [ ] `rugi_silang` aman dari log nol
- [ ] `gradien_logistik` diturunkan di kertas dulu, baru dikode
- [ ] Bagian 3 lolos, galat relatif di bawah `1e-6`
- [ ] MSE dicoba dan kegagalannya diamati sendiri, bukan dipercaya dari soal
- [ ] `softmax` ditulis sendiri, dan pengurangan maksimum dibuktikan tidak mengubah hasil
- [ ] Rusaknya softmax tanpa pengurangan maksimum dilihat sendiri
- [ ] Akurasi 100 persen dipahami sebagai gejala, bukan prestasi
- [ ] Pemisahan latih dan uji berstrata dirancang
- [ ] Waktu satu klasifikasi diukur dalam milidetik

Kalau kedua belas kotak beres, Sesi 2 mengubah ini jadi komponen SYNESIS yang
sungguhan: 300 sampai 500 perintahmu sendiri, ekstraksi parameter, dan gerbang
keamanan.
