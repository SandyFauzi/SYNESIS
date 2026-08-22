# Kunci Sesi D, versi yang lengkap

Berkas pendamping: [`kunci_sesiD_bukti.py`](kunci_sesiD_bukti.py)
Jawabanmu: [`soal-sesiD.md`](soal-sesiD.md)

Semua angka di halaman ini keluar dari satu perintah:

```powershell
. .\scripts\activate.ps1
python notebooks\kunci_sesiD_bukti.py
```

Jangan percaya satu pun angka di bawah ini sebelum kamu melihatnya keluar
dari layarmu sendiri. Itu aturan yang sama sejak Hari 1.

Ringkasan penilaian:

| Soal | Vonis | Yang kurang |
|---|---|---|
| 1a | Benar, sebabnya keliru | "Matematika absolut" tidak berlaku di float64 |
| 1b | Benar | Bisa dinaikkan dari "konvensi" jadi turunan aljabar |
| 2a | Benar | Alasan sebenarnya autograd dipakai belum disebut |
| 2b | Salah | Bukan eksponensial, dan bukan meledak |
| 3a | Benar seluruhnya | Arahnya bisa dipastikan, bukan cuma diyakini |
| 4a | Salah | Ongkos tetapnya peluncuran kernel, bukan PCIe |

Empat dari enam sudah kokoh. Dua yang salah dua-duanya kelas kesalahan yang
sama: mekanisme yang kedengaran masuk akal, tidak pernah diuji.

---

## Soal 1a. Kenapa angkanya identik dengan scikit-learn

**Yang kamu tulis:** sklearn pakai least square yang sama, dan "matematika itu
absolut, gak peduli siapa yang ngoding, hasilnya pasti sama."

**Kalimat pertama benar. Kalimat kedua salah, dan salahnya penting.**

Matematika memang absolut. Float64 tidak. Aljabar yang identik di kertas bisa
memberi jawaban berbeda tergantung urutan operasinya. Jalankan Bukti 1:

```text
 derajat      cond(X)   cond(X.T X)    beda maks
--------------------------------------------------
       2    3.524e+00     1.242e+01    2.220e-16
       4    1.696e+01     2.877e+02    3.340e-14
       6    1.084e+02     1.174e+04    1.403e-12
       8    6.032e+02     3.639e+05    2.280e-11
      10    4.299e+03     1.848e+07    9.988e-09
      12    2.463e+04     6.066e+08    1.919e-06
```

Kedua kolom itu menyelesaikan persoalan yang sama persis. Yang satu lewat SVD
(`np.linalg.lstsq`), yang satu lewat persamaan normal (`solve(X.T @ X, X.T @ y)`).
Di kertas keduanya menghasilkan theta yang identik. Di mesin, selisihnya naik
sepuluh orde dari derajat 2 ke derajat 12.

Sebabnya ada di kolom tengah. Membentuk `X.T @ X` mengkuadratkan condition
number, dan mengkuadratkan condition number membuang separuh angka penting
sebelum satu pun pembagian dikerjakan. Ini kelanjutan langsung dari Soal 3
Sesi C, cuma sekarang kamu melihat akibatnya pada dua algoritma yang sama-sama
"benar".

**Jawaban yang benar:** angkamu cocok dengan sklearn sampai `1e-16` bukan
karena matematika absolut, tapi karena `LinearRegression` memanggil
`scipy.linalg.lstsq`, yang memanggil LAPACK `gelsd`, rutin yang sama persis
dengan yang dipanggil `np.linalg.lstsq`. Kalian menempuh jalan yang sama, jadi
galat pembulatannya pun sama. Kalau sklearn memilih persamaan normal, di
derajat 12 kalian sudah beda di angka keenam.

Satu koreksi kecil lagi: kamu bilang cocok "sampai desimal ke-9". Itu batas
tampilannya, bukan batas kecocokannya. Format `{:14.9f}` cuma mencetak sembilan
desimal. Kolom selisih di sebelahnya mencetak `1e-16`. Selalu baca kolom
selisih, jangan menghitung digit yang kelihatan sama.

---

## Soal 1b. Kenapa alpha = lam * n

**Jawabanmu benar.** Yang bisa dinaikkan: kamu menyebutnya "konvensi",
seolah-olah sklearn bisa saja memilih angka lain. Tidak bisa. Begitu kamu
memutuskan memakai rata-rata dan sklearn memutuskan memakai jumlah, faktor `n`
itu terpaksa, bukan pilihan.

Tiga baris yang menghasilkannya:

```text
L_kita    = (1/n) * SSE + lam   * ||th[1:]||^2
kalikan n di kedua ruas, letak minimumnya tidak bergeser
n*L_kita  =         SSE + lam*n * ||th[1:]||^2
L_sklearn =         SSE + alpha * ||th[1:]||^2
```

Baris kedua itu kuncinya: mengalikan seluruh fungsi loss dengan tetapan positif
tidak memindahkan letak minimumnya. Yang berubah cuma satuan. Samakan baris
ketiga dan keempat, `alpha = lam * n` jatuh sendiri.

Bukti 2 mengujinya dengan tiga tebakan sekaligus:

```text
   alpha sklearn       beda maks lawan rumus kita
--------------------------------------------------
       lam = 0.100                      9.151e-01
   lam * n = 1.500                      3.608e-16
   lam / n = 0.007                      2.783e+00
```

Cuma satu yang mendarat di ketelitian mesin. Kalau kamu ragu antara `lam * n`
dan `lam / n`, jangan mengingat-ingat. Coba ketiganya, yang benar akan berteriak
`1e-16` sementara yang salah berteriak `1e-1`.

`fit_intercept=True` juga tidak mendenda geseran, sama seperti `denda[0] = 0`
yang kamu tulis di Sesi C. Kalau konvensi ini yang meleset, gejalanya khas:
baris koefisien 0 sendirian yang salah, sisanya cocok.

---

## Soal 2a. Bagaimana PyTorch menemukan gradienmu

**Jawabanmu benar.** Graf komputasi, aturan rantai, bukan aljabar simbolik.
Tidak ada yang perlu dikoreksi.

Yang belum kamu sebut adalah alasan orang repot-repot membangunnya. Kamu sudah
punya dua cara lain yang sama-sama menghasilkan angka benar: turunan analitik di
kertas, dan beda hingga. Kenapa tidak pakai beda hingga saja untuk semuanya?

Karena ongkosnya. Beda hingga butuh `p+1` kali hitung maju untuk `p` parameter.
Mode mundur butuh satu kali maju dan satu kali mundur, berapa pun `p`:

```text
      p   1x maju (ms)   backward (ms)   beda hingga (ms)     hemat
--------------------------------------------------------------------
     10         0.0252          0.1155               0.28        2x
    100         0.0291          0.1197               2.94       25x
   1000         0.0520          0.1805              52.01      288x
  10000         0.6807          1.4615            6807.78     4658x
```

Kolom `backward` naik dua belas kali saat `p` naik seribu kali. Kolom beda
hingga naik sebanding dengan `p`, persis seperti yang diramalkan.

Sekarang lanjutkan garisnya ke model bahasa dengan miliaran parameter. Dengan
beda hingga, satu langkah training butuh miliaran kali hitung maju. Latihan yang
sekarang makan berminggu-minggu akan makan lebih lama dari umur alam semesta.

Jadi mode mundur bukan mempercepat sesuatu yang sudah mungkin. Ia yang membuat
hal itu mungkin sama sekali. Itu jawaban yang membuat Soal 2a berhenti jadi
"gimana caranya" dan jadi "kenapa harus".

Harganya memori. Graf komputasinya wajib disimpan sampai `backward()` selesai,
karena tiap simpul butuh nilai majunya untuk menghitung turunan lokal. Itulah
yang memenuhi VRAM saat melatih model besar, bukan bobotnya. Dengan 4 GB di
kartumu, ini yang akan kamu tabrak lebih dulu daripada jumlah parameter.

---

## Soal 2b. Kenapa zero_() wajib dipanggil

**Ini yang salah.** Kamu menulis gradiennya "membesar eksponensial" dan
modelnya "mental melesat ke luar angkasa". Dua-duanya bisa diuji, dan dua-duanya
tidak terjadi.

### Bagian yang benar

Premisnya betul: PyTorch menumpuk, tidak menimpa. Bekukan theta, panggil
`backward()` berulang kali, lihat norma gradiennya:

```text
 panggilan     norma grad   rasio ke panggilan 1
--------------------------------------------------
         1       0.677624                 1.0000
         2       1.355248                 2.0000
         3       2.032873                 3.0000
         4       2.710497                 4.0000
         5       3.388121                 5.0000
         6       4.065745                 6.0000
```

Rasionya bilangan bulat berurutan. Menumpuk berarti menjumlahkan, dan
menjumlahkan itu **linear**. Eksponensial akan memberi 1, 2, 4, 8, 16.
Beda ini bukan soal istilah. Ia menentukan apa yang kamu cari saat mendiagnosis.

### Bagian yang salah, dan ini yang menarik

Jalankan loop training sungguhan tanpa `zero_()`, `lr = 0.05`:

```text
 iterasi     loss pakai zero_()     loss tanpa zero_()
------------------------------------------------------
       0               1.029094               1.029094
       2               0.989100               0.971217
       4               0.961514               0.906678
       6               0.942139               0.908733
       8               0.928347               0.964385
      12               0.911259               1.005914
      20               0.897361               0.970890
      30               0.892832               0.937922
      39               0.891866               0.951032

loss minimum sejati : 0.891516807
```

Yang lupa `zero_()` tidak melesat ke mana pun. Ia turun sebentar, sempat
mendahului yang benar di iterasi 4, lalu berbalik dan berayun selamanya di
sekitar 0.95. Yang benar mendarat di 0.8919, dekat sekali dengan minimum sejati
0.8915.

### Kenapa berayun, diturunkan di kertas

Tanpa `zero_()`, gradien yang dipakai di langkah `k` adalah jumlah seluruh
gradien sebelumnya:

```text
th[k+1] = th[k]   - lr * ( g(th[0]) + ... + g(th[k])   )
th[k]   = th[k-1] - lr * ( g(th[0]) + ... + g(th[k-1]) )
```

Kurangkan baris kedua dari baris pertama. Semua suku lama saling menghapus, dan
yang tersisa satu:

```text
th[k+1] - 2*th[k] + th[k-1] = -lr * g(th[k])
```

Ruas kiri itu beda hingga pusat untuk turunan **kedua** terhadap waktu diskret.
Ruas kanan itu gaya. Kamu sudah pernah melihat persamaan ini, cuma di mata
kuliah yang lain:

```text
m * a = F
```

dengan `m = 1` dan `dt^2 = lr`. Itu skema leapfrog, integrator yang dipakai di
simulasi mekanika dan dinamika molekul.

Jadi lupa `zero_()` tidak merusak gradient descent. Ia **menggantinya dengan
hukum Newton tanpa gesekan.** Gradient descent punya gesekan, jadi ia berhenti
di dasar lembah. Massa tanpa gesekan tidak punya alasan untuk berhenti: ia jatuh
ke dasar, kelebihan lajunya membawanya naik ke sisi seberang, lalu balik lagi,
selamanya.

### Dua ramalan yang membuktikannya

Kalau benar ini osilator tak teredam, dua hal harus terjadi.

**Pertama, amplitudonya tidak boleh meluruh.** Jalankan 4000 iterasi:

```text
amplitudo ayunan 100 iterasi pertama     1.434367e-01
amplitudo ayunan 100 iterasi terakhir    1.422975e-01
```

Empat ribu iterasi, tidak ada energi yang hilang. Ini keadaan marginal yang kamu
temukan di Soal 4 Sesi B, cuma di sana ia cuma muncul di satu nilai lr yang harus
dikenai tepat. Di sini ia jadi keadaan permanen untuk semua lr.

**Kedua, ambang kestabilannya harus berubah.** Persamaan cirinya
`r^2 - (2 - lr*lambda) r + 1 = 0`. Hasil kali akarnya tepat 1, jadi amplitudonya
memang tidak boleh meluruh. Akarnya tetap di lingkaran satuan selama
`0 <= lr*lambda <= 4`, jadi ambangnya `lr < 4/lambda_max`, bukan
`lr < 2/lambda_max` seperti gradient descent biasa:

```text
lambda_max Hessian                    3.474859996
ambang GD biasa, 2/lambda_max         0.575562757
ambang tanpa zero_(), 4/lambda_max    1.151125514
ambang terukur, dicari bagi dua       1.151167246
galat relatif ramalan                   3.625e-05
```

Cocok sampai lima angka.

**Jawaban yang benar untuk 2b:** `zero_()` wajib karena PyTorch menumpuk
gradien, dan penumpukan itu linear. Akibatnya bukan ledakan. Rekurensinya
berubah dari orde satu jadi orde dua, yang secara fisika berarti gradient
descent berubah jadi osilator tak teredam. Modelmu berhenti membaik dan berayun
di sekitar minimum tanpa pernah mendarat, ambang lr amannya justru naik dua kali
lipat, dan tidak ada satu pun error, NaN, atau peringatan.

Itu justru yang membuatnya jahat. Sesuatu yang meledak akan kamu temukan dalam
sepuluh detik. Sesuatu yang berhenti membaik di angka yang salah akan membuatmu
menyalahkan learning rate, arsitektur, dan datamu selama berjam-jam sebelum
curiga pada satu baris yang hilang.

**Cara mendiagnosisnya:** bekukan parameternya, panggil `backward()` empat kali,
lihat rasio norma gradiennya. Kalau 1, 2, 3, 4, penumpukan terbukti. Kalau tetap
1, penyebabnya di tempat lain.

**Dan ini fitur, bukan cacat.** Kartumu 4 GB. Untuk melatih dengan batch 128 yang
tidak muat di VRAM, jalankan empat batch berisi 32 tanpa `zero_()`, bagi
gradiennya empat, baru melangkah. Hasilnya identik dengan batch 128, memorinya
seperempat. Namanya gradient accumulation, dan ia mungkin justru karena PyTorch
memilih menumpuk. Kamu akan memakainya di Bulan 2.

---

## Soal 3a. Ilusi geseran satu iterasi

**Jawabanmu benar seluruhnya,** termasuk arahnya, yang mudah tertukar.

Satu hal yang bisa ditingkatkan: kamu menyatakannya sebagai fakta yang kamu
ingat. Ia bisa dipastikan dalam satu tatapan. Lihat Bukti 5:

```text
loss di titik awal theta0 : 0.704182250

 indeks    catat SESUDAH    catat SEBELUM
------------------------------------------
      0      0.698891016      0.704182250
      1      0.694126417      0.698891016
      2      0.689820738      0.694126417
      3      0.685916944      0.689820738
      4      0.682366802      0.685916944

dibandingkan langsung  a[k] lawan b[k]   : 5.291e-03
digeser                a[k] lawan b[k+1]  : 0.000e+00
```

Baris pertama kolom SEBELUM sama persis dengan loss di titik awal, sampai
digit terakhir, karena belum satu langkah pun dikerjakan. Kolom SESUDAH
melewatkan nilai itu selamanya: entri ke-0 miliknya sudah hasil satu pembaruan.

Jadi aturannya: **yang entri pertamanya sama dengan loss di titik awal adalah
yang mencatat sebelum melangkah.** Dari situ `a[k] = b[k+1]` menyusul sendiri,
dan itu sebabnya perbandingan yang cocok adalah `hn[:-1]` lawan `hp[1:]`, bukan
sebaliknya. Selisihnya `0.000e+00`, bukan sekadar kecil.

Yang membuat jebakan ini berbahaya: panjang kedua riwayat sama, parameter
akhirnya identik, dan kurvanya bertumpuk rapi di skala log. Tidak ada satu pun
yang memberi peringatan. Kamu sudah menjawab persis soal ini di Soal 6c Sesi A,
sebelum melihat akibatnya. Sekarang kamu melihat akibatnya.

---

## Soal 4a. Kenapa GPU kalah di data kecil

**Ini yang salah.** Kesimpulanmu benar, mekanismenya tidak.

Yang kamu tulis: "CPU harus ngirim data ke VRAM GPU lewat kabel motherboard
(PCIe bus)... waktu transfer datanya (ongkos tetapnya) kelamaan."

Buka lagi `sesiD_pytorch.py`, fungsi `ukur`:

```python
X = torch.randn(n, d, device=dev, dtype=torch.float32)
y = torch.randn(n, device=dev, dtype=torch.float32)
th = torch.zeros(d, device=dev, requires_grad=True)
```

`device=dev`. Ketiganya lahir di VRAM dan tidak pernah menyeberang PCIe satu
kali pun, tidak saat pemanasan, tidak di dalam loop. Kalau transfer penyebabnya,
ongkos tetap itu seharusnya nol.

Empat pengukuran di kartumu sendiri:

```text
perangkat : NVIDIA GeForce GTX 1650 Ti

apa yang diukur                                    ms
------------------------------------------------------
satu kernel paling remeh (a + 1)               0.0203
satu langkah training n=50 d=2                 0.6088
transfer 50x2 CPU -> GPU                       0.0295
transfer 50000x1000 CPU -> GPU                31.0321
```

Tiga hal yang mematikan klaim PCIe:

1. Datanya tidak pernah ditransfer, tapi ongkos `0.6088` ms tetap ada.
2. Kalaupun ditransfer, `50x2` cuma 608 byte dan makan `0.0295` ms, sekitar
   5 persen dari ongkos satu langkah. Sembilan puluh lima persennya tidak
   terjelaskan.
3. Satu kernel paling remeh yang bisa ditulis, `a + 1`, sudah makan `0.0203` ms
   padahal ia menyentuh satu angka. Satu langkah training meluncurkan belasan
   kernel: matmul, kurang, pangkat, rata-rata, lalu pasangan mundurnya, lalu
   pembaruan. Belasan kali `0.0203` sudah seukuran `0.6088`.

Hitungan aslinya sendiri sekitar 600 operasi mengambang. Kartu ini sanggup
triliunan per detik, jadi bagian menghitungnya selesai dalam waktu yang bahkan
tidak terukur di sini.

**Jawaban yang benar:** ongkos tetapnya adalah **peluncuran kernel plus dispatch
Python dan CUDA**. Tiap operasi tensor harus melewati dispatcher PyTorch, disusun
jadi perintah CUDA, dikirim ke antrean driver, dijadwalkan GPU, lalu
disinkronkan. Ongkos itu dibayar per operasi dan hampir tidak peduli seberapa
besar datanya. Di `n=50, d=2` ongkos itu adalah keseluruhan waktunya.

Itu juga yang menjelaskan kolom GPU di sapuanmu tetap datar dari `n=100` sampai
`n=10000`. Kalau yang dibayar transfer, kolom itu akan naik sebanding dengan
`n`, karena data yang ditransfer memang seratus kali lebih besar.

**Intuisi PCIe-mu tidak sia-sia.** Lihat baris keempat: `50000x1000` makan
`31.03` ms, lebih dari lima puluh kali satu langkah training. Di sana kamu benar
sekali, dan itulah alasan orang menaruh data di GPU sekali lalu membiarkannya di
sana selama seluruh training. Yang keliru cuma penempatannya: kamu memakai sebab
yang benar untuk kasus besar guna menjelaskan gejala di kasus kecil.

Cara mengujinya lain kali, sebelum menulis penjelasan: kalau kamu menduga
transfer, hilangkan transfernya. Kalau gejalanya bertahan, dugaanmu mati.

---

## Yang perlu diperbaiki di soal-sesiD.md

Sunting sendiri dua jawaban ini, jangan salin dari sini. Tulis ulang dengan
kalimatmu, dan sebutkan angka yang kamu lihat di layarmu:

- **2b** ganti "membesar eksponensial" dan "mental melesat ke luar angkasa".
  Sebutkan rasio 1, 2, 3, 4, sebutkan bahwa ia berayun bukan meledak, dan
  sebutkan ambang `4/lambda_max`.
- **4a** ganti mekanismenya jadi peluncuran kernel. Pertahankan bagian PCIe,
  tapi pindahkan ke tempat yang benar, yaitu kasus `50000x1000`.

Tambahkan juga satu kalimat di **1a** bahwa cocoknya karena rutin LAPACK-nya
sama, bukan karena float64 absolut.

Sesudah itu Bulan 0 benar-benar tutup.

---

## Satu pola yang muncul dua kali

Kesalahan 2b dan 4a bentuknya sama persis:

1. Gejalanya diamati dengan benar.
2. Sebab yang masuk akal muncul di kepala.
3. Sebab itu langsung ditulis sebagai kesimpulan.
4. Langkah yang hilang: menanyakan apa lagi yang harus terjadi kalau sebab itu
   benar, lalu memeriksanya.

Kalau PCIe penyebabnya, menghilangkan transfer harus menghilangkan ongkosnya.
Kalau eksponensial, rasionya harus 1, 2, 4, 8. Dua-duanya bisa diperiksa dalam
lima menit, dan dua-duanya langsung mematikan dugaannya.

Ini bukan kelemahan berpikirmu. Justru sebaliknya: kamu punya banyak model
mental yang siap dipanggil, dan itu bahan mentah yang bagus. Yang perlu
ditambahkan cuma satu kebiasaan, yaitu menurunkan satu ramalan yang bisa
dipatahkan sebelum menulis kata "karena".

Fisika sudah mengajarimu ini. Kamu tidak pernah menerima sebuah teori sebelum
melihat prediksinya diukur. Berlakukan aturan yang sama untuk penjelasan tentang
kodemu sendiri.
