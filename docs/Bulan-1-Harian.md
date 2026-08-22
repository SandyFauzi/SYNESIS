# Bulan 1 — Backpropagation dan MLP dari Nol

**Periode:** September 2026, berjalan bersamaan dengan awal perkuliahan
**Target:** MLP tulisan sendiri mencapai akurasi di atas 95 persen di MNIST, tanpa memakai `torch.nn` satu baris pun
**Beban:** sekitar 32 jam, dibagi 4 sesi besar

---

## Apa yang berubah dari Bulan 0

Satu hal saja: **modelnya berhenti linear.** Semua sisanya akibat.

| | Bulan 0 | Bulan 1 |
|---|---|---|
| Permukaan loss | satu mangkuk, satu minimum | banyak lembah, titik awal menentukan tujuan |
| Hessian | tetap, bisa dihitung sebelum melihat `y` | bergantung pada `y` dan pada posisi |
| lr aman | diramalkan dari `2/lambda_max` sebelum training | dicari empiris, karena `lambda_max` bergerak |
| Turunan ketiga | nol, jadi beda hingga pusat eksak | tidak nol, jadi `h = 1e-5` kembali jadi anjuran benar |
| Gradien | diturunkan sekali di kertas, dipakai selamanya | terlalu banyak jalur untuk diturunkan tangan |

Baris terakhir itu alasan Bulan 1 dibuka dengan menulis mesin autograd. Begitu
modelnya bercabang, menurunkan gradien dengan tangan berhenti masuk akal. Bukan
karena sulit, tapi karena jumlah jalurnya meledak.

Yang **tidak** berubah: ukur seberapa salah, cari arah menurun, melangkah,
ulangi. Itu tetap sama sampai Modul 6.

---

## Sesi 1 — Mesin autograd · ~4 jam · SEDANG BERJALAN

Berkas: [`bulan1_sesi1_autograd.py`](../notebooks/bulan1_sesi1_autograd.py)
Soal: [`soal-bulan1-sesi1.md`](../notebooks/soal-bulan1-sesi1.md)

Kelas `Value` bergaya micrograd. Sekitar 90 baris yang kamu tulis, lima TODO:
`__add__`, `__mul__`, `__pow__`, `relu`, dan `backward` dengan urutan topologis.

Keputusan paling menentukan ada di satu karakter: `+=` atau `=` di dalam
`_backward`. Pikirkan dulu apa yang terjadi pada `a * a` sebelum mengetik.

**Selesai bila:** 9 baris uji beda hingga lolos, 300 ekspresi acak lolos tanpa
satu pun gagal, cocok dengan PyTorch, dan mesinmu berhasil melatih regresi kubik
sampai mendekati optimum `lstsq`.

Angka acuan dari versi terisi yang sudah diverifikasi: galat relatif terburuk
`1.866e-08` pada 300 ekspresi, kecocokan PyTorch `0.000e+00`, loss kubik
`1.410770` lawan optimum `1.410678`.

---

## Sesi 2 — Neuron, Layer, MLP · ~4 jam

Di atas mesin Sesi 1, tanpa satu pun `import torch`.

- `Neuron`: bobot dan bias sebagai daftar `Value`, keluarannya `relu(w . x + b)`
- `Layer`: kumpulan `Neuron` yang menerima masukan sama
- `MLP`: rangkaian `Layer`, plus `parameters()` yang mengembalikan semua `Value`
  yang bisa dilatih
- Latih pada masalah klasifikasi yang **tidak bisa dipisahkan garis lurus**,
  misalnya dua bulan sabit yang saling mengunci

Dua hal yang akan kamu temui, dan dua-duanya baru:

**Titik awal menentukan tujuan.** Jalankan training yang sama dari lima seed
berbeda, dapat lima loss akhir berbeda. Di Bulan 0 ini mustahil. Rekam
sebarannya, jangan cuma jalankan sekali.

**Neuron bisa mati.** `relu` yang selalu menerima masukan negatif punya gradien
nol selamanya, jadi bobotnya berhenti diperbarui. Hitung berapa persen neuronmu
mati di akhir training. Ini pengukuran, bukan teori.

**Selesai bila:** MLP-mu memisahkan dua bulan sabit dengan akurasi di atas 95
persen, dan kamu bisa menggambar batas keputusannya.

---

## Sesi 3 — MNIST · ~5 jam

Titik di mana mesin buatanmu bertemu data sungguhan: 60000 gambar, 784 piksel,
10 kelas.

Yang baru:

- **Softmax dan cross-entropy**, menggantikan MSE. Turunkan sendiri kenapa
  gabungan keduanya menghasilkan gradien yang bersih `p - y`
- **Mini-batch**, karena 60000 contoh sekaligus tidak akan muat dan tidak perlu
- **Train, validation, test** tiga cara, bukan dua. Bulan 0 cuma butuh dua
  karena tidak ada hyperparameter yang dipilih dari data

Peringatan jujur: mesin `Value` bergaya micrograd itu satu objek Python per
angka. Untuk MNIST ia akan **sangat** lambat, mungkin puluhan menit per epoch.
Itu bukan kegagalanmu, itu memang harganya, dan merasakannya langsung adalah
bagian dari pelajarannya. Sesi 4 yang menjelaskan kenapa PyTorch cepat.

Kalau terlalu lambat sampai menghambat, boleh naik ke versi `Value` berbasis
array numpy. Tapi tulis versi per-angka dulu sampai jalan, jangan dilompati.

**Selesai bila:** akurasi test di atas 95 persen, dan kamu bisa menjelaskan
aliran gradien di tiap lapisan tanpa melihat kode.

---

## Sesi 4 — PyTorch, dan menulis optimizer sendiri · ~4 jam

Dua bagian.

**Pertama, tulis ulang MLP Sesi 3 dengan PyTorch.** Hasilnya harus sama, dan
kecepatannya tidak akan sama. Ukur rasionya. Kamu sudah tahu sebabnya dari
Bukti 6 Sesi D: yang mahal bukan menghitung, tapi mengurus. Satu objek Python
per angka berarti satu dispatch per angka.

**Kedua, tulis SGD-with-momentum, RMSprop, dan Adam dengan tangan**, lalu
bandingkan lintasannya di permukaan loss Sesi B yang lembahnya sempit.

Ini menutup janji dari Soal 4e Sesi B, dan sekarang kamu punya bahasa untuk
memahaminya. Dari Bukti 4 Sesi D kamu sudah melihat bahwa rekurensi orde dua
menghasilkan osilator tak teredam:

```text
th[k+1] - 2*th[k] + th[k-1] = -lr * g(th[k])
```

Momentum adalah persamaan yang sama **ditambah gesekan**:

```text
v[k+1] = beta * v[k] - lr * g(th[k])
th[k+1] = th[k] + v[k+1]
```

`beta` itu koefisien redaman. Pasang `beta = 1` dan kamu kembali ke osilator
tak teredam yang lupa `zero_()` tadi. Pasang `beta = 0` dan kamu kembali ke
penurunan gradien biasa. Seluruh keluarga optimizer modern hidup di antara dua
ujung itu, dan itu persis osilator teredam yang kamu pelajari di Fisika Dasar.

**Selesai bila:** ketiga optimizer buatanmu mengalahkan SGD polos di lembah
sempit, dan kamu bisa menyebutkan kondisi masing-masing menang.

---

## Tolok ukur Bulan 1

- [ ] Mesin autograd tulisan sendiri lolos uji beda hingga dan cocok dengan PyTorch
- [ ] `Neuron`, `Layer`, `MLP` berjalan di atas mesin itu tanpa `torch.nn`
- [ ] Masalah yang tidak bisa dipisahkan garis lurus berhasil dipisahkan
- [ ] Sebaran loss akhir dari beberapa titik awal diukur, bukan diasumsikan
- [ ] Persentase neuron mati dihitung
- [ ] Softmax dan cross-entropy diturunkan sendiri sampai bentuk `p - y`
- [ ] MNIST di atas 95 persen dengan mesin buatan sendiri
- [ ] Rasio kecepatan lawan PyTorch diukur, dan sebabnya bisa dijelaskan
- [ ] SGD-momentum, RMSprop, dan Adam ditulis tangan dan dibandingkan
- [ ] Hubungan momentum dengan osilator teredam bisa dijelaskan tanpa melihat catatan

---

## Batas perangkat keras yang perlu diingat

GTX 1650 Ti, 4 GB VRAM, dan sekitar 979 MB sudah terpakai saat idle. Sisa
kurang lebih 3,1 GB.

Bulan 1 tidak akan menyentuh batas itu. MNIST dengan MLP kecil muat di RAM CPU
dengan sangat longgar, dan dari Sesi D kamu sudah tahu model sekecil ini justru
lebih cepat di CPU.

Yang akan menabrak batas itu Bulan 5 dan 6. Teknik yang menyelamatkanmu di sana
sudah kamu temui di Bukti 4 Sesi D: gradient accumulation, yang mungkin justru
karena PyTorch menumpuk gradien alih-alih menimpanya.

---

## Aturan yang tetap berlaku

1. Tulis dulu, baru pakai pustaka. Urutannya tidak boleh dibalik.
2. Tiap gradien diverifikasi dengan beda hingga sebelum dipercaya.
3. Tiap penjelasan yang memakai kata "karena" harus punya satu ramalan yang
   bisa dipatahkan. Turunkan ramalan itu, lalu periksa.
4. Tiap sesi yang selesai dicatat di [`log.md`](../log.md), termasuk yang salah.

Aturan ketiga ditambahkan setelah Sesi D. Dua jawaban di sana keliru dengan
bentuk yang sama: gejala diamati benar, sebab yang masuk akal muncul, lalu
ditulis sebagai kesimpulan tanpa diperiksa. Rinciannya di
[`kunci-sesiD.md`](../notebooks/kunci-sesiD.md).
