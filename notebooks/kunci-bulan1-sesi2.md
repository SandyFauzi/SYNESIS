# Kunci Bulan 1 Sesi 2 - Neuron, Layer, MLP

Jawaban di [`soal-bulan1-sesi2.md`](soal-bulan1-sesi2.md) diperiksa dengan
pengukuran, bukan pendapat. Semua angka di bawah keluar dari
[`kunci_b1s2_bukti.py`](kunci_b1s2_bukti.py), yang bisa kamu jalankan sendiri:

```
. .\scripts\activate.ps1
python notebooks\kunci_b1s2_bukti.py
```

## Ringkasan

Tujuh TODO jalan. Bagian 3 lolos di `2.063e-12`, jaringan 33 parameter, garis
lurus 63,3 persen lawan 8 neuron 100,0 persen. Kodenya benar sebagai kode.

Dari 31 butir jawaban: **21 benar, 3 sebagian benar, 3 salah, 4 tidak
dikerjakan.**

Keempat yang tidak dikerjakan punya bentuk yang sama: soalnya meminta angka,
jawabannya berisi penalaran. Itu pola yang sama dengan Soal 4c dan 5a di
Sesi 1, dan salah satunya menyembunyikan bug di kodemu sendiri.

---

## Satu bug di kodenya

`Neuron.__init__`:

```python
self.w = [Value(random.uniform(-1, 1) * (2 / n_masuk)**0.5) for _ in range(n_masuk)]
```

Ragam `uniform(-1, 1)` bukan 1, tapi $(b-a)^2/12 = 1/3$. Jadi ragam bobotnya
jadi $\frac{1}{3}\cdot\frac{2}{n} = \frac{2}{3n}$, tiga kali lebih kecil dari
yang kamu turunkan sendiri di 2b dan 2c. Terukur (Uji 1):

```
resep                                        ragam w   ragam z   E[a^2]
uniform(-1,1) * sqrt(2/n)  <- yang dipakai   0.01337    0.6693   0.3348
gauss(0,1)    * sqrt(2/n)  <- He gauss       0.03941    1.9738   0.9881
gauss(0,1)    * sqrt(1/n)                    0.01999    1.0010   0.5005
uniform(-1,1) * sqrt(6/n)  <- He uniform     0.04002    2.0006   0.9989
```

Target He: ragam w $=2/n=0{,}04$, ragam z $=2$, $E[a^2]=1$. Baris pertama
meleset tiga kali lipat di ketiga kolom. Baris terakhir kena persis.

**Perbaikannya dua pilihan.** Pakai `random.gauss(0, 1) * sqrt(2/n)`, atau
tetap uniform tapi dengan batas `sqrt(6/n)`. Yang kedua itu resep resmi He
uniform, dan angkanya bukan kebetulan: $\frac{1}{3}\cdot\frac{6}{n}=\frac{2}{n}$.

Di jaringan dua lapis Sesi 2 ini tidak terlihat, dan itulah kenapa kamu bisa
melewatinya. Ditumpuk sepuluh lapis baru kelihatan (Uji 2):

```
lapis ke                      1         3         5         7        10
uniform * sqrt(2/n)    4.74e-01  1.39e-01  4.64e-02  1.30e-02  1.93e-03
gauss   * sqrt(2/n)    8.40e-01  9.01e-01  9.25e-01  8.46e-01  9.75e-01
gauss   * sqrt(1/n)    5.94e-01  3.18e-01  1.63e-01  7.48e-02  3.05e-02
```

Perhatikan baris ketiga. Resep $1/n$ yang kamu kritik sendiri di jawaban 2d
justru bertahan **lima belas kali lebih baik** daripada resep yang kamu tulis
di kode. Kritikmu benar, dan sasarannya kena ke kodemu sendiri lebih keras.

Satu catatan kecil lagi, `MLP.__init__` menulis `sz = [n_masuk] + ukuran`. Ini
pecah kalau `ukuran` dikirim sebagai tuple. `list(ukuran)` menutup itu.

---

## Verdict per soal

### Soal 1 - bobot nol · 2 benar, 1 setengah, 1 salah

| butir | verdict |
|---|---|
| 1a | **benar**, keluarannya nol semua |
| 1b | **setengah benar** |
| 1c | **salah** |
| 1d | **benar** |

**1c salah, dan salahnya menarik.** Kamu jawab "1 neuron efektif, 7 sisanya
kloningan". Terukur (Uji 3):

```
bobot lapisan tersembunyi = 0 semua
  |grad| terbesar di lapisan tersembunyi : 0.000e+00
  akurasi setelah 200 iterasi           : 50.0 persen
  w[0] tiap neuron sesudah latih        : 0.0000 .. 0.0000  (rentang 0.0000)
```

Bukan 1 neuron efektif. **Nol.** Gradiennya bukan kecil, tapi nol tepat, dan
bobotnya tidak bergerak satu iterasi pun.

Sebabnya relu, dan kamu sudah menulis sendiri sebabnya di 5a. Kalau semua
bobot dan geseran nol maka pra-aktivasi nol, dan `self.data > 0` di
`relu._backward` memberi `False` untuk nol. Turunannya nol. Lapisannya mati
sebelum latihan dimulai, matinya jenis yang sama persis dengan lr = 8 di
Bagian 5B.

**1b setengah benar, dan sebagiannya salah saya.** Untuk kasus nol, gradiennya
memang identik, karena identik nol. Tapi cerita umum "neuron identik menerima
gradien identik" tidak berlaku untuk satu lapisan saja. Terukur:

```
bobot lapisan tersembunyi = 0.5 semua (seragam, tapi tak nol)
  |grad| terbesar di lapisan tersembunyi : 9.645e-02
  akurasi setelah 200 iterasi           : 68.3 persen
  w[0] tiap neuron sesudah latih        : 0.2998 .. 0.5372  (rentang 0.2374)
```

Bobotnya seragam, tapi lapisan sesudahnya acak. Gradien neuron $j$ mengandung
faktor $v_j$ dari lapisan keluaran, dan $v_j$ berbeda-beda. Jadi simetrinya
patah sendiri dalam satu langkah.

Cerita "8 kloningan selamanya" cuma benar kalau **seluruh** jaringan seragam.
Petunjuk 1 yang saya tulis di soal menyederhanakan ini terlalu jauh, dan itu
yang menuntunmu ke 1c.

### Soal 2 - angka 2 pada sqrt(2/n) · 3 benar, 1 tidak dikerjakan

2a, 2b, 2c benar semua, dan turunannya rapi.

**2d tidak dikerjakan.** Soalnya bilang "Uji ramalanmu. Buat lapisan berisi
200 neuron dengan 50 masukan, beri masukan acak berragam 1, lalu ukur ragam
keluarannya." Jawabanmu tidak memuat satu angka pun.

Ini bukan formalitas. Kalau kamu menjalankannya, bug di paragraf pertama
kunci ini akan ketahuan malam itu juga, oleh kamu sendiri, dalam empat baris
kode. Ini kali kedua setelah Soal 4c Sesi 1: yang tidak diukur, tidak
ketahuan.

### Soal 3 - lapisan terakhir tanpa tekukan · 3 benar, 1 salah

3a, 3b, 3c benar. Bukti tiga barisnya bersih, dan alasan 3c tepat: dengan
keluaran terkunci $\geq 0$, titik berkelas $-1$ punya rugi minimum 1.

**3d salah pada angkanya.** Kamu tulis akurasi terjebak di 50 persen.
Terukur (Uji 4):

```
akurasi                       : 59.2 persen
ramalan terkecil              : 0.0000
ramalan negatif               : 0 dari 120
```

Bagian "tidak bisa negatif" benar. Kesimpulan 50 persennya tidak.

Sebabnya ada di satu baris di dalam `latih`:

```python
benar = sum(1 for yi, s in zip(y, skor) if (s.data > 0) == (yi > 0))
```

Ramalan tepat nol dihitung sebagai kelas $-1$. Jadi model masih bisa
memisahkan dua kelas, cuma lewat "nol lawan positif" alih-alih "negatif lawan
positif". Yang hilang bukan kemampuan memisahkan, tapi margin, dan seluruh
gradien di daerah nol itu.

### Soal 4 - garis lurus mustahil · 2 benar, 1 sebagian benar

4a benar, argumen cembungnya tepat.

**4b benar isinya, salah istilahnya.** Bentuk yang kamu maksud paraboloid
(mangkuk putar), bukan "hiperbola parabolik". Hyperbolic paraboloid itu
pelana, bentuk yang melengkung naik di satu sumbu dan turun di sumbu lain.
Gambaranmu selanjutnya, cincin luar di bibir mangkuk dan cincin dalam di
dasar, benar dan itu yang penting.

**4c sebagian.** Perbandingannya betul di arah besar. Tapi "meledaknya ongkos
memori $O(N)$" bukan harga sebenarnya, dan ongkos yang paling penting justru
kamu lewatkan padahal kamu sudah mengukurnya sendiri di Bagian 5A:

```
seed   rugi akhir   akurasi
   0       0.3355     93.3%
   2       0.4742     82.5%
   4       0.1800     95.8%
```

Fitur buatan tangan memberi jawaban tunggal. Latih seribu kali, hasilnya
sama. Lapisan tersembunyi menghapus jaminan itu: yang kamu bayar bukan cuma
tafsir, tapi **reprodusibilitas**. Mulai sekarang, satu angka tanpa sebaran
bukan hasil.

### Soal 5 - neuron mati · 3 benar, 1 sebagian

5b, 5c, 5d benar. 5d bagus, kontrol variabelnya persis alasan praktikum.

**5a mekanismenya benar, pembandingnya salah.** Kamu tulis untuk model linear
"seberapapun jauh gradien terpental, vektornya akan selalu mengarah kembali
berayun menuju ekuilibrium".

Tidak. Sesi D mengukur ambangnya:

```
lambda_max Hessian                    3.474859996
ambang GD biasa, 2/lambda_max         0.575562757
```

Di atas $2/\lambda_{max}$, gradient descent linear **menyimpang**, bukan
berayun lalu pulih. Amplitudonya membesar tiap langkah dan tidak pernah
kembali.

Bedanya dengan relu tetap nyata, tapi bukan "pulih lawan mati". Yang benar:
di model linear gradiennya tidak pernah nol, jadi jalan pulang selalu ada
kalau lr diperkecil. Di relu gradiennya nol tepat, jadi memperkecil lr
sesudahnya tidak menolong apa pun.

### Soal 6 - rugi engsel · 3 benar, 1 tidak dikerjakan

6a, 6c, 6d benar. Turunan lokal `exp` dan `log` di 6b juga benar.

**Tapi `exp` dan `log` belum ada di `Value`.** Diperiksa:

```
grep "def exp\|def log" notebooks/bulan1_sesi1_autograd.py   ->  kosong
```

Kotak "exp dan log ditambahkan ke Value, diuji dengan beda hingga" tercentang
di tolok ukur, padahal yang ada baru rumusnya di berkas jawaban. Sesi 3 butuh
keduanya untuk entropi silang, jadi ini yang pertama harus dikerjakan.

Dua catatan waktu menulisnya. Pertama, `math.log(0)` di Python melempar
`ValueError`, bukan menghasilkan `-inf` seperti tulisanmu di 6c. Kedua,
alasan `a = 0` terlarang berlaku juga untuk semua `a < 0`, dan itu yang lebih
sering menabrakmu di praktik.

### Soal 7 - batas keputusan poligon · 2 benar, 2 tidak dikerjakan

7a dan 7d benar. 7d bagus, kaitan ke limit Archimedes tepat.

**7b dan 7c ditebak, tidak dihitung.** Kamu tulis "kemungkinan kurang dari 8,
misal 6 atau 7". Terukur (Uji 5), dan stabil di empat resolusi kisi:

```
 neuron   kisi   sudut   ikut melipat  potongan   seberang/neuron
      8    200      16       8 dari 8         1            {2: 8}
      8   1600      16       8 dari 8         1            {2: 8}
     32    200      62     31 dari 32         1           {2: 31}
     32   1600      62     31 dari 32         1           {2: 31}
```

**16 sudut, bukan kurang dari 8.** Dua kali jumlah neuron.

Sebabnya geometri murni, dan sekali dilihat tidak bisa dilupakan. Tiap neuron
menyumbang satu garis lipat lurus di bidang. Batas keputusannya satu kurva
tertutup yang mengurung cincin dalam. Garis lurus yang memotong kurva
tertutup harus **masuk sekali dan keluar sekali**. Dua penyeberangan, dua
sudut, per neuron. Kolom terakhir membuktikan tiap neuron kena persis 2.

Jadi aturannya:

$$\text{sudut} = 2 \times (\text{neuron yang garis lipatnya memotong batas})$$

Untuk 32 neuron: 62 sudut, 31 neuron ikut. Satu neuron garis lipatnya lewat
di luar kurva sehingga tidak menyumbang sudut sama sekali. Itulah "kenapa
bisa kurang" yang ditanyakan 7b, cuma tempatnya di model 32, bukan di model 8.

Ramalanmu di 7c, poligon bersisi 32, meleset dua kali: bukan 32, dan bukan
sama dengan jumlah neuron.

### Soal 8 - ongkos dan dinding · 3 benar, 1 salah besaran

8b, 8c, 8d benar. Urutan perbaikan di 8d tepat, dan alasannya tepat.

**8a metodenya benar, angkanya meleset 120 kali.** Terukur (Uji 6):

```
batas rekursi mesin ini : 1000

784-32-10     50.869 Value per gambar
             3 ukuran : 328 ms, 575 ms, 687 ms
             satu epoch 60000 gambar = 5.5 sampai 11.5 jam
             kedalaman kira-kira 816 < 1000, aman
784-256-10   PECAH   RecursionError: maximum recursion depth exceeded
             kedalaman kira-kira 1040 > 1000
```

Ramalanmu 29 hari. Sebenarnya berjam-jam, bukan berminggu-minggu.

Sumber salahnya satu: kamu baca 49 ms sebagai ongkos satu gambar. Itu ongkos
satu iterasi penuh atas 120 titik, jadi ongkos satu titik sekitar 0,4 ms.
Persis 120 kali lipat, dan itu selisihmu.

Perhatikan juga sebaran tiga pengukuran di atas: 328 sampai 687 ms untuk
pekerjaan yang sama persis. Mesin `Value` didominasi alokasi objek Python dan
pemungut sampah, bukan aritmetika. Satu angka tunggal untuk ongkos seperti
ini menyesatkan, dan itu alasan kedua kenapa laporan tanpa sebaran tidak
diterima.

Kesimpulanmu selamat. Belasan jam per epoch tetap tidak bisa dipakai, dan
dinding rekursi tetap menabrak di 784-256-10, persis seperti hitunganmu.

---

## Yang harus dibereskan sebelum Sesi 3

1. **Perbaiki inisialisasi.** `gauss(0,1) * sqrt(2/n)` atau
   `uniform(-1,1) * sqrt(6/n)`. Lalu jalankan Uji 1 lagi dan pastikan ragam w
   kena `2/n`.
2. **Tulis `exp` dan `log` di `Value`,** lengkap `_backward`, lalu uji dengan
   beda hingga seperti Bagian 2 Sesi 1. Sesi 3 memakainya untuk entropi
   silang.
3. **Kerjakan 2d.** Empat baris, dan itu yang seharusnya menangkap butir 1.
4. **Betulkan tolok ukur** yang tercentang tapi belum dikerjakan. Kotak yang
   dicentang tanpa bukti lebih berbahaya daripada kotak kosong, karena ia
   menutup pintu pemeriksaan.

Nomor 1 dan 2 bukan pilihan. Sesi 3 membangun di atas `Neuron` dan `Value`
yang sama, dan dua-duanya dipakai di sana.

---

## Catatan untuk saya sendiri

Petunjuk 1 di soal menulis "kalau dua neuron identik dan menerima masukan
identik, mereka menghasilkan keluaran identik dan menerima gradien identik".
Itu benar cuma kalau lapisan sesudahnya juga seragam. Ditulis tanpa syarat
itu, kalimatnya salah, dan pengukuran di Uji 3 menunjukkan simetrinya patah
dalam satu langkah.
