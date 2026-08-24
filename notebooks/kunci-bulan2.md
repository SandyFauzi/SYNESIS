# Kunci Bulan 2 Sesi 1 dan Sesi 2

Jawaban di [`soal-bulan2-sesi1.md`](soal-bulan2-sesi1.md) dan
[`soal-bulan2-sesi2.md`](soal-bulan2-sesi2.md) diperiksa dengan pengukuran.
Angka di bawah keluar dari [`kunci_b2_bukti.py`](kunci_b2_bukti.py):

```
. .\scripts\activate.ps1
python notebooks\kunci_b2_bukti.py
```

## Ringkasan

Empat belas TODO jalan, dua berkas keluar 0. Sesi 1: galat gradien
`1.166e-10` dan `1.440e-11`, akurasi 100 persen di enam kelas. Sesi 2:
sebaran uji 25 poin persen, 0,004 milidetik per perintah.

**Tidak ada satu pun jawaban yang salah.** Yang ada cuma satu angka tertukar
waktu disalin, dan dua butir yang sengaja kamu tandai belum dikerjakan karena
memang butuh data pribadimu.

Ini pertama kalinya sejak Sesi D Bulan 0 semua yang meminta angka dijawab
dengan angka yang bisa saya ulang. Enam belas nilai terukur yang kamu tulis,
enam belas cocok sampai digit terakhir, termasuk lima keyakinan softmax
sampai empat angka di belakang koma.

---

## Kamu membantah berkas saya, dan kamu benar

Sesi 1 Soal 7d menyuruh menghapus pengurangan maksimum lalu menjalankan
Bagian 5 dengan `W` awal dikali 1000. Soal 7c sudah menyatakan lebih dulu
bahwa tanpa pengurangan itu `exp` jadi tak hingga dan hasilnya `nan`.

Kamu jalankan, dan melaporkan bahwa `×1000` **tidak** meluap. Terukur (Uji A):

```
exp meluap di atas ln(1.8e308) = 709.78

 kali W awal   logit maks    nan   akurasi  softmax
        1000       496.17  False     86.1%  polos
        1000       496.17  False     86.1%  kurangi maks
        1500       744.25   True       nan  polos
        1500       744.25  False     72.2%  kurangi maks

ambang terukur: pengali 1430.5, logit maks di situ 709.78
```

Angkamu kena persis: 496,17 dan 86,1 persen di `×1000`, lalu 744,25 dan `nan`
di `×1500`.

`exp(496)` itu sekitar $10^{215}$. Besar sekali, dan masih muat di float64.
Yang meluap baru di atas $\ln(1{,}8 \times 10^{308}) = 709{,}78$, dan itu
tercapai di pengali sekitar 1430.

Soal 7c benar sebagai pernyataan umum. Angka 1000 di Soal 7d yang salah
kalibrasi, dan itu kesalahan saya. Kamu mengukurnya, menemukan bahwa dugaan
soalnya tidak terbukti, dan menuliskan itu alih-alih menuliskan apa yang
soalnya harapkan. Itu jawaban yang lebih baik daripada jawaban yang "benar".

Satu tambahan dari tabel yang kamu belum sebut. Di `×1500`, versi yang
mengurangi maksimum tetap hidup tapi akurasinya jatuh ke 72,2 persen.
Pengurangan maksimum menyelamatkanmu dari `nan`, bukan dari inisialisasi yang
buruk. Dua penyakit berbeda.

---

## Satu pengujian saya yang keliru, bukan jawabanmu

Sesi 2 Soal 2b. Kamu laporkan kebocoran kosakata memberi TF-IDF `68,8/66,1`.
Waktu memeriksa saya dapat `67,7`, dan sempat mengira angkamu meleset.

Terukur (Uji C), tiga tingkat:

```
tingkat                     fitur          validasi      uji
bersih                      hitung kata       65.6%    68.2%
bersih                      TF-IDF            65.6%    66.7%
kosakata bocor, IDF bersih  hitung kata       71.9%    62.5%
kosakata bocor, IDF bersih  TF-IDF            68.8%    66.1%
kosakata + IDF bocor        TF-IDF            68.8%    67.7%
```

Baris tengah punyamu. Baris bawah punya saya. Soal 2b cuma menyuruh mengubah
**satu baris**, yaitu sumber kosakatanya; saya membocorkan IDF-nya juga.
Percobaan yang benar yang kamu jalankan, dan keempat angkamu kena persis.

Yang paling berharga dari hasil ini bukan angkanya, tapi arahnya. Validasi
naik dari 65,6 ke 71,9 sementara uji justru **turun** dari 68,2 ke 62,5.
Ramalanmu di 2b sudah menyebut itu lebih dulu: "tidak ada arah yang pasti,
kolom kata uji tidak pernah dilatih sehingga bobot acaknya bisa menambah
derau". Kebocoran tidak selalu menaikkan angka. Yang pasti rusak: angkanya
berhenti berarti, karena sistem yang dilaporkan bukan sistem yang akan jalan.

---

## Yang lain, dikonfirmasi

### S1 Soal 4a - MSE diadu dengan gradiennya sendiri

```
rugi          rugi akhir   akurasi   iterasi ke 100%
silang          0.025147    100.0%                54
mse             0.009026    100.0%                85
```

Iterasi 54 lawan 85, persis laporanmu. Dan cara mengujinya yang benar: kamu
mengganti rugi **beserta gradiennya**. Percobaan yang menukar rugi tapi
menyisakan gradien lama tidak menguji apa pun.

Satu angka tertukar: rugi akhir MSE terukur `0,009026`, kamu tulis
`0,000926`. Digitnya berpindah waktu disalin. Kesimpulan tidak berubah, dan
memang dua kolom rugi itu tidak boleh dibandingkan langsung karena rumusnya
beda. Yang membandingkan cuma kolom iterasi, dan itu yang kamu pakai.

### S1 Soal 4b dan 4c - selisih 500 kali

```
gradien MSE lewat sigmoid   2(0.999)(0.000999) = 0.001996
gradien entropi silang      p - y              = 0.999
rasio                                            500.5
```

Ketiganya benar. Dan 5a-5b menurunkan `p - y` sampai selesai, dengan faktor
$p(1-p)$ yang saling menghapus ditunjukkan eksplisit.

### S1 Soal 6a - 642 parameter

$106 \times 6 + 6 = 642$ untuk 36 contoh, yaitu 17,8 parameter per contoh.
Benar.

### S2 Soal 1b dan 1c - hitungan yang menghasilkan pekerjaan

```
lebar selang 5 poin  ->  n = 0.09 / 0.0125^2 = 576 kalimat uji
576 / 0.15                                    = 3840 kalimat total
300 sampai 500 total  ->  uji 45-75  ->  lebar 17.9 sampai 13.9 poin
```

Keempat angka benar. Dan kesimpulan yang kamu tarik yang penting: angka
300-500 di rencana Bulan 2 cukup untuk prototipe, tidak cukup untuk selang
5 poin. Rencana itu saya yang tulis, dan kamu baru saja menunjukkan batasnya
dengan aritmetika.

### S2 Soal 4a dan 4d - matriks bingung dibaca satu per satu

Keenam arah kesalahan kamu sebut lengkap dengan kalimatnya, masing-masing
terjadi sekali. Dan 4d benar: `obrol` presisi 60 persen recall 100 persen,
diterjemahkan tanpa istilah jadi "semua obrolan dikenali, tapi dua dari lima
kalimat yang dikirim ke obrol sebenarnya perintah".

### S2 Soal 5c dan 8c - ambang ongkos, dan batasnya

```
ambang per intent : 14 benar, 3 salah, 7 menolak
ambang global 0,50: 15 benar, 5 salah, 4 menolak
asing ditolak ambang per intent : 0 dari 5

perintah yang butuh LLM                          kelas      yakin
bandingkan hasil eksperimen ini ...    ringkas_catatan     0.5988
jelaskan backpropagation ...                     obrol     0.4035
baca dua makalah ini lalu kritik ...            jadwal     0.4448
rancang arsitektur synesis ...             cari_berkas     0.4042
kenapa model ini overfit ...                    jadwal     0.4722

ditangkap ambang global 0,50 : 4 dari 5
ditangkap ambang per intent  : 2 dari 5
```

Semua sama persis, termasuk kelima keyakinan sampai empat angka di belakang
koma. "Dua kesalahan hilang dengan harga tiga penolakan tambahan" juga benar:
5 turun ke 3, 4 naik ke 7.

Dan kesimpulan terpenting di seluruh Sesi 2 kamu sebut sendiri tanpa diminta:
**ambang ongkos bukan pendeteksi kalimat asing.** Nol dari lima tertolak,
karena kelas murah seperti `obrol` sengaja dibuat longgar dan kalimat asing
cenderung mendarat di situ. Ambang per intent malah menangkap LEBIH SEDIKIT
perintah-butuh-LLM daripada ambang global, 2 lawan 4, dengan sebab yang sama.

Dua alat berbeda untuk dua masalah berbeda, dan menyatukannya membuat
dua-duanya lebih buruk.

---

## Dua butir yang sengaja kamu kosongkan

Tolok ukur Sesi 1 dua belas dari dua belas. Sesi 2 sebelas dari dua belas.

Butir `1d` dan `6a` di Sesi 2 kamu tandai belum dikerjakan, dengan alasan: butuh
riwayat perintah nyatamu, dan agen tidak boleh mengarang 3.720 kalimat lalu
mengaku itu ucapan nyata.

Itu keputusan yang benar, dan saya catat sebagai kredit, bukan kekurangan.
Mengisinya dengan kalimat karangan akan membuat sepuluh kotak lain di
bawahnya jadi bohong, karena semua angka sesudahnya diukur dari data itu.

Tapi kedua kotak itu tetap harus diisi, dan sekarang bukan lagi soal
menulis-nulis. `1c` sudah memberimu angkanya: 3.840 kalimat untuk selang 5
poin. Kalau 3.840 terlalu banyak untuk sekarang, hitung ulang untuk selang 8
atau 10 poin dan tulis sebanyak itu, lalu laporkan selangnya apa adanya.
Yang tidak boleh cuma satu: melaporkan akurasi tanpa selangnya.

---

## Kebiasaan yang akhirnya melekat

Di kunci Bulan 1 Sesi 3+4 saya menulis satu keluhan yang tersisa: melaporkan
sebaran, bukan satu angka.

Sesi 2 kamu mengerjakan tiga hal tanpa diminta yang menutup keluhan itu.
Soal 3a menyatakan "percobaan ini belum mampu membedakan" alih-alih memilih
pemenang. Soal 3b menerjemahkannya ke bahasa praktikum: sebaran antarbelahan
itu ralat alat, selisih antar-resep itu sinyal, dan di sini ralat jauh lebih
besar dari sinyal. Soal 2b menuliskan ramalan lebih dulu, lalu mengukur, lalu
melaporkan bahwa ramalannya sendiri yang benar dan arah kebocoran memang
tidak pasti.

Itu tiga bentuk berbeda dari kebiasaan yang sama, dan tidak satu pun diminta
secara eksplisit oleh soalnya.

---

## Berikutnya

SYNESIS v0.1 tinggal disambungkan: `bulan2_sesi2_intent.py` menghasilkan
intent dan slot, `synesis/alat.py` menunggu keduanya, dan `izin` sudah ada di
sana sebagai gerbang terakhir seperti yang kamu uraikan di 7d.

Bulan 3 belum disusun.
