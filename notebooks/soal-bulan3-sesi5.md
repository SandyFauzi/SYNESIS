# Soal Bulan 3 Sesi 5 - SYNESIS v0.2, telinga dan mulut

Berkas yang dikerjakan: [`synesis/suara.py`](../synesis/suara.py) dan
[`synesis/rvc.py`](../synesis/rvc.py)

Sesi ini tidak punya notebook. Yang dibangun bukan latihan melainkan bagian
dari SYNESIS sendiri, sama seperti Bulan 2 Sesi 4 yang memindahkan pipa niat
ke `synesis/niat.py`.

Rantainya:

```text
mikrofon -> VAD -> wake word -> perekam -> Whisper -> pipa niat Bulan 2
                                                   -> Piper -> RVC -> speaker
```

> Prasyarat: Sesi 2 (fitur log-mel), Sesi 4 (model wake word dan ambangnya),
> serta pipa niat Bulan 2 yang sudah berjalan.

> Semua angka waktu di bawah diukur di mesin pemilik: GTX 1650 Ti 4 GB,
> Python 3.12.5, torch 2.6.0+cu124, kalimat uji sepanjang 3,98 detik audio.

---

## Soal 1 - VAD: kenapa ambangnya tidak boleh berupa angka

`Vad` di `suara.py` tidak memakai ambang mutlak. Ia mengukur lantai derau
ruangan sebagai persentil ke-20 dari tenaga tiga detik terakhir, lalu
memasang ambangnya `VAD_ATAS_DB = 8` desibel di atas itu.

**1a.** Sebutkan tiga hal yang membuat ambang mutlak gagal, dan untuk
masing-masing perkirakan besarnya dalam desibel.

> **Jawaban:**
>
> 1. **Ruangan berbeda.** Kamar sunyi malam hari bisa 25 dBA, ruang kuliah
>    dengan pendingin udara 45 dBA. Selisih 20 dB, dan itu lebih besar
>    daripada seluruh margin yang kita punya.
> 2. **Jarak ke mikrofon.** Tekanan bunyi turun 6 dB tiap kali jarak
>    berlipat dua. Bicara dari 20 cm lalu dari 80 cm sudah selisih 12 dB
>    tanpa mengubah apa pun.
> 3. **Penguatan otomatis Windows.** AGC pada peranti USB menyesuaikan
>    penguatannya sendiri dan bisa bergeser 10 sampai 20 dB tanpa
>    pemberitahuan. Ini yang paling jahat karena ia berubah SELAMA sesi
>    berjalan.
>
> Ketiganya bersama-sama bisa menggeser sinyal 40 dB. Ambang mutlak yang
> disetel di satu keadaan akan menganggap semuanya sunyi atau semuanya suara
> di keadaan lain.
>
> Yang tidak berubah: RASIO antara suara dan lantai derau di ruangan yang
> sama. Ketiga sebab di atas menggeser keduanya bersama-sama. Itulah kenapa
> ukuran relatif bekerja dan ukuran mutlak tidak.

**1b.** Persentil ke-20 dipakai, bukan minimum dan bukan rerata. Jelaskan
kedua penolakan itu.

> **Jawaban:** Minimum terlalu peka: satu potongan 10 milidetik yang
> kebetulan hampir nol akan menarik seluruh lantai derau ke bawah, dan
> ambangnya ikut turun sampai derau sendiri melewatinya. Cukup satu potongan
> buruk dari 300 untuk merusaknya.
>
> Rerata terlalu tercemar: kalau kamu bicara terus selama tiga detik, rerata
> tenaga tiga detik terakhir adalah tenaga SUARAMU, bukan tenaga ruangan.
> Ambangnya lalu naik mengejar suaramu sendiri, dan VAD berhenti mendeteksi.
>
> Persentil ke-20 mengasumsikan paling sedikit 20 persen dari tiga detik
> terakhir adalah jeda. Untuk bicara normal itu benar dengan margin lebar:
> jeda antarkata saja sudah 15 sampai 25 persen dari durasi ucapan. Asumsinya
> gagal kalau kamu bicara tanpa henti lebih dari tiga detik, dan akibatnya
> ucapan terpotong, bukan tidak terdeteksi.

**1c.** `Vad.segmen` memakai dua ambang: naik di `lantai + 8` dan turun di
`lantai + 4`. Kenapa bukan satu ambang untuk keduanya?

> **Jawaban:** Satu ambang membuat setiap potongan yang kebetulan jatuh tepat
> di sekitarnya berkedip antara "suara" dan "sunyi", dan tiap kedipan
> memotong ucapan jadi dua segmen.
>
> Yang lebih menentukan lagi: konsonan letup memang berhenti total.
> Pengucapan /p/, /t/, /k/ menutup saluran suara sepenuhnya selama 30 sampai
> 60 milidetik sebelum meledak, jadi tenaga di tengah kata benar-benar turun
> ke lantai derau. Dengan satu ambang, kata "praktikum" bisa terpecah jadi
> tiga segmen.
>
> Histeresis menyelesaikan keduanya: sekali masuk keadaan "sedang bicara",
> yang dibutuhkan untuk keluar lebih rendah, dan tambahan syarat
> `VAD_DIAM_MS = 700` membuat jeda pendek tidak pernah cukup untuk mengakhiri
> ucapan. 700 milidetik dipilih karena jeda antarkalimat manusia biasanya di
> atas itu, sedangkan jeda antarkata di bawahnya.

---

## Soal 2 - Anggaran latensi

Diukur, untuk kalimat balasan sepanjang 3,98 detik audio:

```text
tahap                              muat pertama   sesudah panas   RTF
---------------------------------------------------------------------
Piper id_ID-news_tts-medium              4,15 s          0,28 s   0,07
faster-whisper small, CPU int8          40,65 s          2,60 s      —
RVC v2, GPU                             22,31 s          0,42 s   0,11
```

Kolom RTF sengaja dikosongkan untuk Whisper. Lihat ralat di 2a: ongkosnya
tidak sebanding dengan durasi ucapan, jadi RTF bukan ukuran yang berarti
untuknya.

**2a.** Susun anggaran latensi dari akhir ucapanmu sampai bunyi pertama
balasan, untuk perintah sepanjang 2 detik dan balasan sepanjang 3 detik.

> **Jawaban:**
>
> ```text
> tunggu diam sebelum berhenti merekam       700 ms   VAD_DIAM_MS
> transkripsi, berapa pun panjangnya        2600 ms   ongkos TETAP, bukan RTF
> pipa niat Bulan 2                            5 ms   satu perkalian matriks
> Piper untuk 3 detik balasan                210 ms   0,07 x 3000
> RVC untuk 3 detik balasan                  330 ms   0,11 x 3000
> -------------------------------------------------  +
> total                                     3845 ms
> ```
>
> **Ralat.** Versi pertama jawaban ini menghitung transkripsi sebagai
> $0{,}77 \times 2000 = 1540$ milidetik, yaitu RTF dikali durasi ucapan.
> Diukur ulang pada beberapa panjang, ongkosnya ternyata TETAP:
>
> ```text
> 1,0 detik ucapan -> 2,48 detik      3,0 detik -> 2,60 detik
> 2,0 detik        -> 2,64 detik      8,0 detik -> 2,60 detik
> ```
>
> Sebabnya Whisper menambahkan bantalan sampai 30 detik sebelum menghitung
> mel-nya, jadi encoder-nya selalu memproses jendela yang sama besarnya.
> Angka RTF 0,77 yang saya kutip cuma kebetulan benar untuk satu klip 3,98
> detik yang dipakai mengukurnya. RTF adalah ukuran yang salah untuk model
> ini.
>
> Modul.md menuntut di bawah 3 detik, dan angka ini MELAMPAUINYA 845
> milidetik. Yang menarik: balasan yang lebih panjang hampir tidak menambah
> apa-apa, cuma 180 milidetik per detik tambahan. Yang menentukan suku tetap
> di baris kedua.
>
> Yang TIDAK masuk anggaran ini dan harus disebut: waktu muat, terukur 31
> detik untuk ketiga model. Sampai sekarang ongkos itu dibayar di tengah
> perintah PERTAMA, sehingga perintah pertama terasa 23 detik dan perintah
> kedua 2,6 detik. `panaskan()` memindahkannya ke layar pembuka dengan bilah
> kemajuan. Ongkosnya tidak hilang, cuma pindah ke tempat yang jujur.

**2b.** Suku mana yang paling besar, dan sebutkan tiga cara memotongnya
beserta harganya.

> **Jawaban:** Transkripsi, 2.600 dari 3.845 milidetik, yaitu 68 persen.
>
> 1. **Model lebih kecil. Diukur, dan TIDAK bisa dipakai.** Pada suara Piper
>    yang bersih, `base` memang tiga kali lebih cepat: 0,83 detik lawan 2,46
>    detik. Tetapi pada suara pemilik yang sesungguhnya ia justru lebih
>    LAMBAT sekaligus jauh lebih buruk:
>
>    ```text
>    base   6,37 detik   'terasa 3 Hello, ini sumpah-sumpah rasa'
>    small  3,52 detik   'TES 123, halo. Ya, ini sampel suara saya.'
>    ```
>
>    Sebabnya waktu decoding Whisper sebanding dengan jumlah token yang
>    dikeluarkannya, dan model yang menebak ngawur mengeluarkan lebih
>    banyak token. Model yang lebih kecil bukan cuma lebih tidak tepat; pada
>    masukan yang sulit ia juga lebih lambat. Ini contoh yang bagus kenapa
>    tolok ukur pada data bersih menyesatkan.
> 2. **Pindah ke GPU.** Akan sangat cepat, dan harganya bukan uang melainkan
>    VRAM: 4 GB harus dibagi dengan model bahasa Bulan 6. Roadmap sudah
>    memutuskan GPU disimpan untuk Bulan 6, jadi ini pilihan yang sengaja
>    tidak diambil.
> 3. **Transkripsi mengalir.** Mulai mentranskripsi begitu ucapan dimulai,
>    bukan sesudah selesai. Menghapus hampir seluruh 1.540 milidetik itu dari
>    latensi yang TERASA, karena kerjanya bertumpang tindih dengan bicaranya.
>    Harganya kerumitan yang besar dan akurasi sedikit lebih rendah di batas
>    potongan.
>
> Nomor tiga yang benar, dan sekarang anggarannya MEMANG sudah terlewati,
> jadi ia berhenti jadi pilihan dan mulai jadi utang. Ditandai `ponytail:`
> di kode dan tercatat di `TODO.md`.

**2c.** `VAD_DIAM_MS = 700` masuk anggaran sebagai 700 milidetik penuh.
Bisakah dihapus?

> **Jawaban:** Tidak bisa dihapus, tetapi bisa dipindahkan. Selama 700
> milidetik itu SYNESIS sudah punya seluruh audionya; yang belum ia punya
> cuma keyakinan bahwa kamu sudah selesai bicara.
>
> Jadi transkripsi bisa DIMULAI di milidetik ke-0 dari jeda, berjalan
> bersamaan dengan penungguan, lalu dibatalkan kalau ternyata kamu
> melanjutkan kalimat. Yang dibayar cuma kerja yang terbuang, dan kerja
> terbuang itu murah karena prosesor sedang menganggur.
>
> Memendekkan 700 jadi 300 adalah jalan yang salah: kamu akan sering dipotong
> di tengah kalimat, dan ongkos mengulang seluruh perintah jauh lebih besar
> daripada 400 milidetik.

---

## Soal 3 - Ambang wake word, sekali lagi dari ongkos

`pilih_ambang` di `suara.py` meminimalkan `100 x FAR + 1 x FRR`, bukan
menyamakan keduanya.

**3a.** Turunkan kenapa titik kesalahan setara (EER) adalah pilihan yang
salah di sini, dan tunjukkan ambang mana yang dipilih dari tabel Sesi 4.

> **Jawaban:** EER adalah titik ketika FAR = FRR. Ia optimal HANYA kalau
> ongkos kedua kesalahan sama, karena meminimalkan `c x FAR + c x FRR`
> memang menyamakan turunannya di titik itu.
>
> Di sini ongkosnya 1 banding 100, jadi yang diminimalkan
> `100\,\text{FAR} + \text{FRR}`, dan titik optimalnya bergeser jauh ke
> ambang yang lebih tinggi. Dari tabel Sesi 4:
>
> ```text
> ambang    FAR      FRR      ongkos = 100 FAR + FRR
> 0,047   0,0379   0,0379    3,79 + 0,04 = 3,83     <- EER
> 0,500   0,00121  0,2593    0,12 + 0,26 = 0,38
> 0,900   0,00000  0,4815    0,00 + 0,48 = 0,48
> ```
>
> Yang menang 0,500, dengan ongkos sepersepuluh dari EER. Perhatikan bahwa
> ambang 0,900 justru lebih buruk daripada 0,500 meskipun FAR-nya nol: sekali
> FAR sudah nol, menaikkan ambang cuma menambah FRR tanpa membeli apa pun.
>
> Ini bentuk yang sama persis dengan `niat.ambang_dari_ongkos` di Bulan 2,
> dan itu bukan kebetulan: keduanya soal keputusan dengan ongkos tak simetris.

**3b.** Rasio 1 banding 100 itu tebakan. Rancang cara mengukurnya.

> **Jawaban:** Ongkos salah menolak bisa diukur langsung: waktu mengulang
> "hey synesis" ditambah waktu sadar bahwa ia tidak menyala, kira-kira 2
> detik. Itu satuannya.
>
> Ongkos salah menerima tidak bisa diukur dengan stopwatch karena ia bukan
> ongkos waktu. Yang bisa dikerjakan: catat setiap penyalaan palsu di
> `audit.jsonl` bersama apa yang akhirnya dilakukan pipa niat sesudahnya.
> Sesudah terkumpul beberapa puluh, kelompokkan menurut akibat terburuknya:
>
> ```text
> tidak ada intent yang lewat ambang      -> ongkos ~ ongkos salah menolak
> intent BACA jalan, hasilnya salah       -> ongkos ~ 2 x
> intent TULIS atau MERUSAK sampai dialog -> ongkos jauh lebih besar
> ```
>
> Bobotnya lalu jadi rerata berbobot menurut porsi masing-masing. Angka 100
> bertahan hanya kalau kelompok ketiga cukup sering; kalau ternyata pagar
> Bulan 2 menahan semuanya di kelompok pertama, rasio yang benar mungkin
> mendekati 5, dan ambangnya harus turun.
>
> Pengukurannya belum dilakukan, dan angka 100 harus diperlakukan sebagai
> tebakan yang eksplisit, bukan hasil.

---

## Soal 4 - RVC yang ditulis ulang

`rvc.py` memeriksa bahwa ke-353 kunci `state_dict` model cocok dengan isi
berkas `.pth`.

**4a.** Apa yang dibuktikan pemeriksaan 353 kunci itu, dan apa yang tidak?

> **Jawaban:** Yang dibuktikan: setiap modul ada, jumlahnya benar, dan
> BENTUK setiap tensor cocok. Itu menyingkirkan hampir semua kesalahan
> struktural: lapisan yang kurang, jumlah kanal yang salah, ukuran kernel
> yang keliru, urutan lapisan yang tertukar.
>
> Yang TIDAK dibuktikan: bahwa tensornya dipakai dengan cara yang benar.
> Bentuk `(192, 192, 1)` cocok untuk `conv_q` maupun `conv_k`; menukar
> keduanya lolos pemeriksaan dan menghasilkan perhatian yang salah. Begitu
> juga urutan `torch.split` untuk `m` dan `logs`, arah `torch.flip` di aliran
> balik, dan tanda pembalikan di lapisan gandeng.
>
> Pemeriksaan yang menutup sebagian celah itu ada di Soal 4b.

**4b.** Terukur: median selisih nada antara masukan dan keluaran $-4$ sen,
dan 74,4 persen bingkai bersuara berada dalam 50 sen. Apa yang dibuktikan
angka itu?

> **Jawaban:** Bahwa dekoder benar-benar memakai eksitasi f0 yang kita
> berikan. Satu sen adalah seperseratus semiton, jadi $-4$ sen adalah selisih
> yang tidak terdengar manusia.
>
> Kenapa ini menggigit: dekoder NSF menerima gelombang sinus pada f0 sebagai
> masukan terpisah. Kalau `SourceModuleHnNSF` salah, misalnya fasenya
> dihitung per bingkai dan bukan per cuplikan, atau `noise_convs` disambung
> ke tahap yang keliru, keluarannya tidak akan mengikuti f0 masukan. Ia akan
> berdesis, atau bernada di frekuensi lain, atau bernada tetap.
>
> Yang belum dibuktikannya: WARNA suaranya. Nada yang benar dengan warna yang
> salah tetap lolos uji ini. Soal 4c menutupnya.

**4c.** Whisper mentranskripsi keluaran RVC sebagai `"Halo Sandy, laporan 4
tikung minggu lalu sudah saya buka."`, sedangkan masukan Piper-nya
`"Halo Sandy, laporan praktikum minggu lalu sudah saya buka."` Apa
kesimpulannya?

> **Jawaban:** Kesimpulan pertama, dan yang terpenting: keluarannya adalah
> UCAPAN, bukan derau. Sebuah model pengenal suara yang tidak tahu apa-apa
> tentang RVC berhasil membaca sepuluh dari sebelas kata. Itu tidak mungkin
> terjadi kalau arsitekturnya salah pada bagian mana pun yang menentukan.
>
> Kesimpulan kedua: ada kerugian kejelasan yang nyata. `praktikum` jadi
> `4 tikung`. Tiga penjelasan yang mungkin, dan urutan kekuatannya:
>
> 1. **Tidak ada retrieval.** RVC asli memakai indeks faiss untuk menarik
>    ciri terlatih yang paling mirip, dan itu mempertajam konsonan. Kita
>    melewatinya sepenuhnya, setara `index_rate = 0`. Ini penjelasan yang
>    paling mungkin.
> 2. **F0 dari YIN, bukan RMVPE.** YIN salah pada konsonan tak bersuara lebih
>    sering daripada RMVPE, dan `praktikum` penuh konsonan tak bersuara.
> 3. **Model dilatih pada suara Jepang.** Fonem Indonesia yang tidak ada di
>    data latih diucapkan dengan pendekatan terdekat.
>
> Cara membedakannya, dan ini soalnya: ukur ulang dengan f0 dari `torchcrepe`
> sebagai ganti YIN. Kalau kejelasannya melompat, penjelasan 2 yang benar.
> Kalau tidak, penjelasan 1, dan yang perlu dikerjakan adalah membaca berkas
> `.index` sepanjang 136 MB itu tanpa faiss.

---

## Soal 5 - Dua pustaka, dua cuDNN

Terukur: memanggil `faster_whisper` lebih dulu lalu RVC menghasilkan

```text
Could not load symbol cudnnGetLibConfig. Error code 127
```

sedangkan urutan sebaliknya berjalan.

**5a.** Jelaskan sebabnya, dan kenapa satu konvolusi $3\times3$ di atas
tensor $8\times8$ cukup untuk menyelesaikannya.

> **Jawaban:** torch dan ctranslate2 masing-masing membawa salinan cuDNN
> sendiri di dalam paketnya. Windows menyelesaikan simbol DLL berdasarkan
> yang sudah termuat lebih dulu di dalam proses, jadi pustaka yang memuat
> belakangan menemukan simbol milik yang duluan. Kalau versinya berbeda, ada
> simbol yang tidak ada, dan itu persis `cudnnGetLibConfig`.
>
> Satu konvolusi memaksa torch benar-benar MEMUAT cuDNN-nya, bukan sekadar
> mengimpor modulnya. `torch.cuda.is_available()` tidak cukup: ia menyentuh
> driver CUDA, bukan cuDNN. Yang menyentuh cuDNN adalah operasi yang
> memakainya, dan konvolusi adalah yang paling langsung.
>
> `torch.cuda.synchronize()` di baris berikutnya memastikan pemuatan itu
> benar-benar selesai sebelum fungsinya kembali.

**5b.** Perbaikan ini ditandai `ponytail:` di kode. Kapan ia boleh dihapus,
dan bagaimana kamu tahu?

> **Jawaban:** Boleh dihapus ketika torch dan ctranslate2 memakai versi cuDNN
> yang sama, atau ketika salah satu berhenti membawa salinannya sendiri.
>
> Cara mengetahuinya tanpa menebak: hapus panggilan `_panaskan_cudnn()`,
> jalankan `transkrip` lalu `warnai` dalam satu proses, dan lihat apakah
> pesannya muncul. Itu dua baris uji dan lima detik.
>
> Yang TIDAK boleh dilakukan: menghapusnya karena "sepertinya sudah tidak
> perlu". Kegagalannya tidak terjadi di semua mesin dan tidak terjadi di
> semua urutan panggilan, jadi ia jenis bug yang hilang saat diperiksa dan
> muncul saat dipakai.

---

## Soal 6 - Duplikasi yang disengaja

`fitur_audio` ada di dua tempat: `notebooks/bulan3_sesi2_spektrogram.py` dan
`synesis/suara.py`.

**6a.** Kenapa tidak diimpor saja dari satu tempat?

> **Jawaban:** Karena keduanya punya umur yang berbeda. Notebook adalah
> jawaban latihan yang dibekukan: angka yang tercetak di dalamnya dikutip di
> berkas soal, dan mengubah kodenya membatalkan kutipan itu. `suara.py`
> adalah bagian SYNESIS yang akan terus berubah selama masih dipakai.
>
> Kalau `suara.py` mengimpor dari notebook, maka setiap perbaikan di SYNESIS
> harus menyentuh berkas yang seharusnya beku, dan setiap kali notebook
> dijalankan ulang untuk memeriksa jawaban, ia menarik kode yang sudah
> berbeda dari yang menghasilkan angkanya.
>
> Keputusan yang sama sudah diambil di Bulan 2 untuk `vektorkan` dan
> `ekstrak_slot`, dan sudah tercatat di `TODO.md` sebagai duplikasi yang
> disengaja.

**6b.** Yang tidak boleh berbeda cuma angkanya. Rancang pemeriksa yang
menangkap perbedaan itu.

> **Jawaban:** Satu fungsi di `kunci_b3_bukti.py` yang mengimpor kedua versi
> lalu membandingkan keluarannya pada masukan yang sama:
>
> ```python
> from bulan3_sesi2_spektrogram import fitur_audio as versi_notebook
> from synesis.suara import fitur_audio as versi_paket
> x = np.random.default_rng(0).normal(0, 0.05, 16000)
> assert np.abs(versi_notebook(x) - versi_paket(x)).max() < 1e-9
> ```
>
> Yang harus ikut diperiksa, dan lebih mudah lupa: tetapannya. `LAJU`,
> `BINGKAI`, `LONCAT`, `N_FFT`, `N_MEL`, dan `PRA_TEKAN` harus sama di kedua
> berkas. Satu saja berbeda, dan model wake word yang dilatih di Sesi 4
> membaca bentuk masukan yang berbeda saat dipakai di Sesi 5, tanpa satu pun
> pesan galat sampai akurasinya jatuh.

---

## Soal 7 - Yang berubah pada keamanan

**7a.** `audit.jsonl` sekarang bisa memuat teks yang tidak pernah kamu ketik.
Sebutkan akibatnya.

> **Jawaban:** Sampai v0.1, seluruh isi `audit.jsonl` adalah kalimat yang
> kamu ketik sendiri, jadi kamu tahu persis apa yang tercatat. Sejak v0.2, ia
> memuat transkripsi apa pun yang terdengar sesudah wake word menyala,
> termasuk:
>
> - kalimat yang tidak ditujukan ke SYNESIS, kalau wake word salah menyala;
> - suara orang lain di ruangan yang sama;
> - lanjutan kalimatmu sesudah kamu berhenti menyadari SYNESIS masih merekam.
>
> `audit.jsonl` sudah ada di `.gitignore` dan tidak pernah meninggalkan
> mesin, jadi ini bukan kebocoran keluar. Yang berubah adalah cakupan apa
> yang tersimpan, dan itu perlu disadari sebelum menyalakan `dengar` di
> ruangan berisi orang lain.
>
> Yang layak ditambahkan, dan belum ada: batas umur untuk baris audit yang
> berasal dari suara, misalnya dibuang otomatis setelah 30 hari kecuali ia
> jadi koreksi.

**7b.** Apakah pagar jalur Bulan 2 masih cukup sekarang bahwa perintah bisa
masuk lewat suara?

> **Jawaban:** Pagarnya sama dan tetap berlaku: `_aman` memeriksa jalur,
> `_bukan_rahasia` memeriksa isi, dan `BUTUH_IZIN` menuntut konfirmasi
> manusia. Suara tidak melewati satu pun di antaranya, karena ia masuk ke
> pipa yang sama persis dengan teks.
>
> Yang BERUBAH adalah peluang masukan yang tidak disengaja. Mengetik
> "hapus semua" memerlukan sepuluh ketukan yang disadari; Whisper bisa
> menghasilkan kalimat itu dari salah dengar. Jadi lapisan yang paling
> menanggung beban tambahan adalah ambang keyakinan, dan untuk intent
> MERUSAK ambangnya 0,995 justru karena hal semacam ini.
>
> Satu hal yang belum ada dan seharusnya ada: dialog konfirmasi untuk
> perintah yang datang lewat suara sebaiknya menampilkan TRANSKRIPSINYA, agar
> kamu bisa melihat bahwa yang didengar SYNESIS bukan yang kamu ucapkan.
> Ditandai sebagai utang di `TODO.md`.

---

## Yang menutup Bulan 3

| janji Roadmap | keadaan |
| --- | --- |
| konvolusi 1D dan 2D manual | Sesi 1, diverifikasi terhadap numpy dan scipy |
| spektrogram dari nol | Sesi 2, framing, jendela, FFT |
| MFCC dari nol | Sesi 2, termasuk DCT-II sendiri |
| CNN dari nol lalu versi PyTorch | Sesi 3, selisih 1,07e-14 |
| keyword spotter Speech Commands | Sesi 4, 12 kelas |
| wake word dilatih dengan suaramu | Sesi 5, `suara rekam` lalu `suara latih` |
| VAD | Sesi 5, ditulis sendiri, bukan silero |
| Whisper untuk transkripsi umum | Sesi 5, faster-whisper CPU |
| Piper untuk balasan suara | Sesi 5, suara bahasa Indonesia |
| semua di CPU, GPU untuk Bulan 6 | sebagian: RVC memakai GPU |

Baris terakhir adalah penyimpangan yang perlu dicatat terang-terangan. RVC
tidak ada di Roadmap sama sekali; ia datang dari `req.md` bagian 5. Ia
memakai GPU karena di CPU RTF-nya terukur 1,66, yaitu lebih lambat daripada
waktu nyata, dan itu memakan anggaran VRAM yang direncanakan untuk model
bahasa Bulan 6. `RVC_AKTIF = False` mematikan keseluruhannya dan
mengembalikan janji itu; `Yukino(peranti="cpu")` mempertahankan suaranya
dengan harga 1,66 kali durasi balasan.
