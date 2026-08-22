# Kunci Bulan 1 Sesi 3+4 - MNIST, dua dinding, optimizer

Jawaban di [`soal-bulan1-sesi34.md`](soal-bulan1-sesi34.md) diperiksa dengan
pengukuran. Angka di bawah keluar dari
[`kunci_b1s34_bukti.py`](kunci_b1s34_bukti.py):

```
. .\scripts\activate.ps1
python notebooks\kunci_b1s34_bukti.py
```

## Ringkasan

Sembilan TODO jalan, dan keluarannya identik dengan versi acuan sampai digit
terakhir: `1.11e-16`, `2.791e-10`, `96.03` lawan `97.27` persen, `484.0`,
`63 / 255 / 52`. Berkasnya keluar 0 tanpa satu peringatan pun.

**Dari 31 butir: 30 benar, 1 salah.**

Bandingkan dengan Sesi 2, yang 4 butirnya tidak dikerjakan sama sekali. Kali
ini setiap soal yang meminta angka dijawab dengan angka, termasuk 5b, 5c, dan
7d yang menuntut kamu menulis dan menjalankan percobaan sendiri di luar berkas
sesi. Itu perubahan yang paling berarti dari seluruh malam ini.

---

## Yang salah: 6a

Kamu jawab epoch 7 memburuk karena model "mulai menyesuaikan noise/keunikan
data latih", yaitu overfitting. Terukur (Uji C):

```
 epoch   akurasi latih   akurasi validasi
------------------------------------------
     4          97.46%             96.81%
     5          97.91%             97.09%
     6          98.10%             97.32%
     7          97.11%             96.37%
```

Akurasi **latih** ikut jatuh, dari 98,10 ke 97,11, di epoch yang sama waktu
validasi jatuh dari 97,32 ke 96,37. Keduanya turun bersama.

Overfitting punya tanda tangan yang tidak bisa ditiru: latih terus naik
sementara validasi turun. Model yang menghafal data latihnya tidak tiba-tiba
lupa. Yang terjadi di sini lain: laju belajar 0,1 dipertahankan sampai akhir,
dan langkah-langkah terakhir mendarat di tempat yang lebih buruk untuk kedua
himpunan sekaligus. Itu derau SGD.

Sisa jawaban 6a tetap berlaku. Epoch terakhir memang bukan pilihan yang baik,
dan menyimpan epoch dengan validasi tertinggi memang yang benar. Yang salah
cuma sebabnya.

Cara memisahkan kedua sebab itu murah: **catat akurasi latih di sebelah
validasi.** Tanpa kolom itu, overfitting dan derau langkah kelihatan persis
sama dari luar. Berkas sesi tidak mencetaknya, dan itu kelalaian saya.

---

## Yang benar, dan yang layak dicatat kenapa

### 3a - dan `reversed()` yang menyelamatkannya

Kamu tulis: "Versi iteratif juga mendorong anak dalam urutan terbalik agar
urutan DFS efektif sama dengan versi rekursif. Jadi urutan operasi
floating-point pun sama."

Itu benar, dan bukan sekadar benar. Baris `reversed()` di TODO 2-mu adalah
satu-satunya yang membuatnya benar. Terukur (Uji B), graf yang sama, cuma cara
telusurnya diganti:

```
20-12-5, 4 contoh, 317 parameter, 2956 simpul
  iteratif + reversed        selisih 0.000e+00   beda bit    0 dari 317
  iteratif tanpa reversed    selisih 1.110e-16   beda bit  164 dari 317
  iteratif anak diacak       selisih 5.551e-17   beda bit  117 dari 317

60-40-10, 8 contoh, 2850 parameter, 48829 simpul
  iteratif + reversed        selisih 0.000e+00   beda bit    0 dari 2850
  iteratif tanpa reversed    selisih 1.110e-16   beda bit 1764 dari 2850
  iteratif anak diacak       selisih 1.110e-16   beda bit 1513 dari 2850
```

Ketiga cara sama-sama benar secara matematis. Ketiganya menghasilkan urutan
topologis yang sah. Yang membedakan cuma urutan penjumlahannya, dan
penjumlahan titik-mengambang tidak asosiatif.

Kalau kamu menghapus `reversed()`, kodemu tetap lolos semua uji beda hingga,
tetap melatih MNIST ke 97 persen, dan tetap memberi gradien yang benar. Yang
hilang cuma jaminan bit demi bit yang kamu klaim di 3a.

**Dan satu kelemahan di berkas sesi yang ini menyingkap.** Uji Bagian 3
awalnya memakai jaringan 4-3-2. Lihat baris pertama tabel Uji B: di ukuran
itu ketiga cara memberi `0.000e+00`. Uji sekecil itu lolos apa pun yang kamu
tulis, jadi ia tidak bisa membuktikan klaimnya sendiri. Sudah diperbesar jadi
20-12-5 dan kedua versi sekarang dijalankan pada graf yang sama:

```
diadu dengan versi rekursif, 2956 simpul, graf sama
  selisih gradien maks   : 0.000e+00
  beda bit               : 0 dari 317
```

### 1c dan 1d - angkanya persis

```
m float  rugi 1.8358831657033847   jumlah gradien  2.108e-16
m Value  rugi 1.8358831657033847   jumlah gradien -1.128e-17
selisih gradien antara kedua versi : 2.220e-16
```

`2.220e-16` dan `2.11e-16` yang kamu laporkan, dua-duanya kena. Penjelasanmu
juga tepat: memakai `Value` memberi logit terbesar satu jalur gradien
tambahan, dan sumbangan jalur itu saling menghapus karena softmax kebal
terhadap pergeseran bersama.

### 5c - titik baliknya memang 256

Diulang tiga kali per titik, plus sekali pemanasan (Uji D):

```
 batch             numpy f64             torch CPU             torch GPU
    64     2.264/2.785/6.587     0.840/0.894/0.908     0.996/1.017/1.204
   128     1.182/1.303/1.397     0.468/0.469/0.470     0.472/0.477/0.488
   256     0.974/0.990/1.036     0.325/0.327/0.340     0.248/0.249/0.333
   512     0.837/0.868/0.926     0.234/0.246/0.247     0.127/0.128/0.131
  1024     0.820/0.831/0.844     0.189/0.194/0.196     0.063/0.067/0.068
```

Batch 256 GPU menang, dan sesudah itu jaraknya melebar sampai hampir tiga kali
lipat di batch 1024. Persis jawabanmu.

### 7d - lanskap kuartikmu memang membalik urutannya

```
L(x, y) = x^4/4 + y^2/2, mulai dari (100, 100)

optimizer       lr terbaik    rugi akhir   iterasi ke rugi 1
SGD polos      0.000186718       3443.48        tidak pernah
momentum       6.50968e-05       1365.28        tidak pernah
RMSprop           0.147738    0.00272814                 783
Adam                    10       1.83926        tidak pernah
```

Beda tipis dari angkamu karena kisi sapuannya beda, kesimpulannya sama.
Alasan yang kamu tulis juga tepat: kurvatur sumbu kuartik bergerak dari 30000
menuju nol, jadi satu laju belajar global harus cukup kecil untuk selamat di
awal dan sesudah itu terlalu kecil untuk sisanya.

Satu catatan: baris Adam jangan dipakai menyimpulkan apa pun. Laju belajar
terbaiknya jatuh tepat di ujung atas sapuan, artinya sapuannya belum
melingkupi Adam.

### 7b - turunannya rapi

Diperiksa satu per satu:

```
faktor langkah tunak      1/(1-0.9) = 10
akar momentum             sqrt(0.9) = 0.94868
faktor SGD sumbu landai   1 - 0.01585*0.2566 = 0.995933
rasio laju asimtotik      ln(0.94868)/ln(0.995933) = 12.93
```

Semua kena. Dan kamu benar mencatat sendiri bahwa rasio terukurnya cuma
4,84x, bukan 12,9x, karena transien dan ambang absolut. Menuliskan selisih
antara ramalan asimtotik dan hasil terukur, alih-alih memilih salah satu yang
kelihatan lebih baik, itu yang membedakan laporan dari iklan.

### 6d - aritmetiknya benar

```
sigma binomial       sqrt(0.97*0.03/10000) = 0.00171  =  0.171 poin persen
bias seleksi 5000    0.00171 * sqrt(2*ln 5000) = 0.0070  =  0.70 poin persen
```

Kedua angka kena, dan syarat "kandidat yang berkorelasi mengurangi angka itu"
juga tepat.

---

## Satu keluhan cara mengukur

`5a`, `5b`, dan `5c` melaporkan waktu sampai enam angka di belakang koma:
`4.735894 s`, `0.770991 s`, `0.491241 s`. Semuanya dari satu kali jalan.

Lihat kolom numpy batch 64 di tabel Uji D: `2.264 / 2.785 / 6.587`. Ulangan
terlambat hampir tiga kali ulangan tercepat, untuk pekerjaan yang sama persis.
Angka keenam di belakang komamu tidak membawa informasi apa-apa, dan angka
pertamanya pun perlu tanda kurang-lebih.

Ini keluhan yang sama yang saya kena di Bagian 5 dan sudah diperbaiki di sana.
Sekarang giliranmu. Aturannya satu kalimat: **kalau kamu melaporkan waktu,
laporkan sebarannya.**

Akibatnya menjalar ke 5a. GFLOPS efektif `6.438` yang kamu hitung memakai
`4.735894 s`. Dengan `2.264 s` angkanya jadi `13.5 GFLOPS`. Cara hitungmu
benar, jumlah perkaliannya benar, konvensi 2 FLOP per kali-tambah benar. Yang
tidak stabil cuma penyebutnya.

---

## Bulan 1 tutup

Kedua belas kotak tolok ukur beres, dan yang lebih penting, kesepuluh kotak
Bulan 1 di `docs/Bulan-1-Harian.md` ikut tertutup.

Kamu punya dua mesin autograd tulisan sendiri, satu per-angka dan satu
per-array, dan keduanya sudah diadu dengan beda hingga. Kamu sudah menabrak
empat jenis kegagalan yang berbeda dan tahu alat mana yang menangkap
masing-masing. Kamu sudah menulis tiga optimizer dan bisa menunjukkan lanskap
tempat masing-masing menang.

Yang tersisa dari Bulan 1 cuma satu kebiasaan yang belum melekat: melaporkan
sebaran, bukan satu angka. Itu muncul tiga kali malam ini, di 5a, 5b, dan 5c,
dan sekali di 2d Sesi 2.

Bulan 2 Sesi 1 sudah menunggu di `soal-bulan2-sesi1.md`, tujuh TODO.
