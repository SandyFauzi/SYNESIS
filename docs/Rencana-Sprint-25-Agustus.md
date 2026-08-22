# Rencana Sprint 25 Agustus, dan Nasib Bulan 1 sampai 4

**Ditulis:** 22 Agustus 2026
**Status:** rancangan untuk dibaca dan dikoreksi. Belum ada yang dieksekusi.

---

## 1. Apa yang berubah

Rencana asli: enam bulan membangun pemahaman, LLM lokal baru masuk di Bulan 6.

Rencana baru: SYNESIS v0.1 harus jalan tanggal 25 Agustus, karena langganan
Claude habis 27 Agustus dan tidak ada dana untuk memperpanjang.

Itu memindahkan LLM dari bulan keenam ke hari ketiga.

### Ongkos yang perlu kamu terima sejak awal

Kalau SYNESIS jalan tanggal 25, ia jalan memakai **organ pinjaman**. Model
bahasanya buatan Alibaba, mesin suaranya buatan orang lain, pencarian dan
pemanggilan alatnya buatan saya. Kamu punya produk yang bekerja, tapi belum
punya pemahaman atas isi perutnya.

Itu bukan kegagalan. Itu urutan yang berbeda, dan urutan ini punya keunggulan
sendiri: kamu belajar sambil punya sesuatu yang jalan, bukan belajar sambil
menunggu. Yang penting kamu tahu itu yang sedang terjadi.

### Yang benar-benar hilang tanggal 27

Kode bisa kamu tulis sendiri nanti, apalagi Codex masih ada. Kamu sudah nulis
mesin autograd dari nol; menulis pemanggil HTTP jauh lebih mudah dari itu.

Yang tidak bisa diambil lagi adalah penjelasan yang khusus ke kerjaanmu:
kenapa satu keputusan diambil, apa yang sudah diukur dan hasilnya berapa,
jebakan apa yang sudah ditabrak, dan bagaimana menyambungkan fisika yang kamu
pelajari ke apa yang sedang kamu bangun.

Karena itu pembagian tiga harinya begini:

| Hari | Isi | Kenapa |
|---|---|---|
| 1 | Rangka SYNESIS v0.1 jalan | Supaya ada wadah untuk pengetahuannya |
| 2 | Isi `knowledge/` | Ini yang hilang tanggal 27 |
| 3 | Peta lanjutan, dokumentasi, tes | Supaya kamu bisa lanjut sendirian |

---

## 2. Sprint tiga hari

### Hari 1, Jumat 22 sampai Sabtu 23 Agustus

**Target:** ketik pertanyaan di terminal, SYNESIS menjawab dari model lokal,
mencari ke `knowledge/` lebih dulu, dan bisa memanggil alat sederhana.

**Yang diunduh, sekitar 3 GB:**

| Apa | Ukuran | Ke mana |
|---|---|---|
| Ollama, programnya | ~4,5 GB | `D:\Apps\Ollama`, lewat junction dari `C:` |
| Gemma-2-2B Q4 | ~1,6 GB | `E:\SYNESIS\ollama-models` |
| Qwen2.5-3B Q4 | ~1,9 GB | `E:\SYNESIS\ollama-models` |
| Phi-3 Mini 3.8B Q4 | ~2,2 GB | `E:\SYNESIS\ollama-models` |
| Piper plus suara | ~80 MB | `E:\SYNESIS\suara` |

Total sekitar 10,2 GB. Sisa `D:` 84 GB, sisa `E:` 184 GB. Aman.

**Program di D lewat junction. DIPUTUSKAN 22 Agustus.** Installer Ollama tidak
memberi pilihan folder, jadi dipakai cara yang sudah kamu pakai untuk Minecraft
Java dan Julia:

```
1. pasang seperti biasa, masuk ke %LOCALAPPDATA%\Programs\Ollama
2. matikan Ollama sampai benar-benar tidak ada prosesnya
3. pindahkan seluruh isi foldernya ke D:\Apps\Ollama
4. hapus folder yang di C
5. mklink /J "%LOCALAPPDATA%\Programs\Ollama" "D:\Apps\Ollama"
```

Setelah itu semua program yang mencari jalur `C:` tetap menemukannya, tapi
byte-nya tinggal di `D:`.

Junction, bukan shortcut. Shortcut itu berkas `.lnk` yang cuma dimengerti
Windows Explorer, dan installer atau updater tidak akan mengikutinya. Junction
dimengerti di lapisan sistem berkas, jadi semua program tertipu dengan mulus.

**Model di E. DIPUTUSKAN 22 Agustus.** Lewat variabel `OLLAMA_MODELS`,
dipasang **sebelum** model pertama ditarik. Kalau terlanjur ke `C:`,
pemindahannya manual.

**Nyala manual. DIPUTUSKAN 22 Agustus.** Autostart dimatikan, karena kalau kamu
main game, VRAM 4 GB harus bebas seluruhnya. Dinyalakan dengan satu perintah
saat mau dipakai.

**Tiga model, bukan satu. DIPUTUSKAN 22 Agustus.** Sesuai req.md.

| Model | Dipakai untuk | Kenapa |
|---|---|---|
| Qwen2.5-3B | bawaan, obrolan dan pemanggilan alat | paling patuh soal format |
| Phi-3 Mini | matematika dan penalaran | memang unggul di situ |
| Gemma-2-2B | jawaban cepat, VRAM lega | paling kecil, sisa VRAM paling banyak |

Ongkos yang harus diterima: tiap pindah model itu bongkar-pasang VRAM, 3 sampai
15 detik. Jadi perpindahan **dipicu perintah, bukan tebakan mesin.** Kalau
SYNESIS berpindah otomatis tiap pertanyaan, kamu akan menunggu sepuluh detik
untuk hal yang seharusnya seketika.

**Berkas yang dibuat:**

```
synesis/konfig.py     semua tetapan di satu tempat        (sudah ditulis)
synesis/otak.py       sambungan ke Ollama                 (sudah ditulis)
synesis/ingat.py      pencarian ke knowledge/, TF-IDF     (sudah ditulis)
synesis/alat.py       baca, cari, info sistem, + pagar    (sudah ditulis)
synesis/suara.py      Piper TTS                           belum
synesis/agen.py       gelung: tanya, alat, jawab          belum
synesis/cli.py        antarmuka terminal                  belum
jarvis.py             titik masuk                         belum
```

Empat yang pertama sudah ada di disk, murni teks, belum menyentuh internet.

**Keputusan desain yang sudah diambil, dan alasannya:**

*Pencarian pakai TF-IDF, bukan embedding.* Embedding lebih pintar tapi butuh
model tambahan, butuh VRAM, dan kalau hasilnya aneh kamu tidak bisa melihat
kenapa. TF-IDF cuma menghitung kata mana yang jarang di seluruh dokumen tapi
sering di satu dokumen. Angkanya bisa kamu cetak dan periksa. Untuk catatan
yang istilahnya kamu tulis sendiri, itu cukup. Kalau nanti terasa kurang,
yang perlu diganti cuma satu berkas.

*Pemanggilan alat pakai satu baris teks, bukan JSON.* Model 3 miliar parameter
sering gagal mengeluarkan JSON yang sah, dan kalau rusak seluruh pemanggilan
gagal. Format `[[ALAT nama|argumen]]` jauh lebih mudah dikeluarkan model kecil
dan lebih mudah diperiksa mata manusia.

*Ada pagar folder, dan perintah yang mengubah disk minta izin.* Model kecil
sering salah tafsir. Tanpa pagar, satu salah tafsir bisa menghapus berkasmu.
Ongkosnya satu ketukan Enter.

*Nama berkas sumber selalu ikut ditampilkan.* Kalau jawaban SYNESIS aneh, kamu
bisa langsung buka berkas yang disebut dan periksa sendiri. Ini satu-satunya
pertahanan nyata terhadap model yang mengarang.

---

### Hari 2, Minggu 24 Agustus

**Target:** `knowledge/` terisi bahan yang tidak bisa didapat lagi setelah 27.

Rencana isinya. Ini yang paling perlu kamu koreksi, karena saya menebak.

```
knowledge/
  synesis/
    arsitektur.md          kenapa tiap bagian dirancang begitu
    troubleshooting.md     gejala, sebab, cara betulkan
    ollama.md              perintah, batas VRAM, apa artinya tiap error
    menambah-alat.md       cara menulis alat baru, langkah demi langkah
  fisika-ke-ml/
    gradien.md             turunan, Hessian, nilai eigen, ambang lr
    osilator.md            momentum, redaman, dan bug zero_()
    pegas.md               regularisasi L2 sebagai Hukum Hooke
    hasil-kali-dalam.md    embedding, kemiripan, bra-ket
    fourier.md             konvolusi, spektrogram, MFCC untuk Bulan 3
  hasil-ukur/
    bulan0.md              semua angka yang sudah diukur, dan artinya
    bulan1.md              autograd, batas rekursi, ongkos Value
  kuliah/
    ml.md                  peta materi ML dan bagian mana yang sudah kamu kode
    dsp.md                 peta materi DSP dan sambungannya ke Bulan 3
  perkakas/
    manim.md               pola yang sudah terbukti jalan di seri video
    git.md                 alur kerja yang dipakai repo ini
    python-numpy.md        jebakan yang sudah pernah menggigit
```

Aturan isinya: **spesifik ke kerjaanmu, bukan tutorial umum.** Codex bisa
menjelaskan apa itu gradient descent. Codex tidak tahu bahwa di data seed 42
milikmu, `lambda_max` bernilai 15,7233 dan ambang `lr` aman jatuh di 0,1272.
Yang kedua itu yang ditulis.

---

### Hari 3, Senin 25 Agustus

**Target:** kamu bisa jalan sendirian.

- `docs/Peta-Lanjutan.md`, rencana fitur berikutnya beserta urutan dan
  perkiraan kesulitan
- `scripts/cek_synesis.py`, satu perintah untuk memastikan semua bagian hidup
- `README` diperbarui, cara pakai dari nol
- Uji akhir menyeluruh, lalu commit dan push

---

## 3. Nasib Bulan 1 sampai 4

Roadmap lama menyusun bulan-bulan ini sebagai **jalan menuju produk**. Sekarang
produknya sudah ada duluan, jadi maknanya berubah.

Maknanya yang baru: **SYNESIS v0.1 lahir dengan organ pinjaman. Tiap bulan kamu
mengganti satu organ pinjaman dengan organ yang kamu tumbuhkan sendiri.**

Itu bukan penghiburan. Tiap penggantian punya keuntungan teknis yang bisa
diukur, dan saya sebutkan di tiap bulan.

---

### Bulan 1 — Backprop dan MLP dari nol · September

**Status:** Sesi 1 sedang berjalan. Mesin autogradmu sudah lolos semua uji.
Tinggal perbaiki jawaban 2b, 5a, 4c.

**Rencana lama tetap berlaku**, tidak ada yang perlu diubah. Sesi 2 membangun
`Neuron`, `Layer`, `MLP`. Sesi 3 MNIST. Sesi 4 menulis Adam sendiri.

**Organ yang diganti:** belum ada. Bulan ini menumbuhkan kemampuan, bukan
komponen.

**Untungnya buat SYNESIS:** setelah bulan ini kamu bisa **membaca kode model
apa pun**. Kalau Qwen berperilaku aneh, kamu punya alat untuk menyelidiki
alih-alih menebak. Itu bedanya pemakai dan pemilik.

**Bisa tanpa Claude?** Bisa. Semua bahannya sudah ada di repo: berkas latihan,
soal, kunci Sesi D, dan seri videonya. Codex cukup untuk menemani.

---

### Bulan 2 — Embedding dan classifier · Oktober

**Rencana lama:** bag-of-words, regresi logistik manual, cross-entropy
diturunkan sendiri, lalu intent classifier dengan 300-500 contoh perintahmu.

**Yang berubah:** dulu ini yang **melahirkan** SYNESIS v0.1. Sekarang v0.1
sudah ada, jadi intent classifier jadi **pengganti** LLM untuk perintah rutin.

**Organ yang diganti:** LLM untuk perintah sehari-hari.

**Untungnya bisa diukur.** Sekarang tiap "berapa sisa disk" harus melewati
model 1,9 GB: muat ke VRAM, hitung ratusan juta operasi, keluarkan teks.
Classifier hasil Bulan 2 menjawab pertanyaan yang sama dalam hitungan
milidetik, tanpa menyentuh VRAM sama sekali. LLM disimpan untuk yang memang
butuh bahasa.

Ini juga membebaskan VRAM, dan VRAM adalah sumber daya paling sempit di
laptopmu.

**Sambungan matkul:** masih kandidat terkuat untuk tugas besar Machine
Learning. Siklus supervised learning utuh, dan sekarang datanya punya konteks
nyata karena sistemnya sudah dipakai.

---

### Bulan 3 — Konvolusi, sinyal, dan suara · November

**Rencana lama:** konvolusi manual, spektrogram dari nol, MFCC, CNN kecil,
wake word dilatih dengan suaramu sendiri.

**Yang berubah:** SYNESIS v0.1 sudah bisa **bicara** karena Piper dipasang di
Hari 1. Yang belum, ia belum bisa **mendengar**.

**Organ yang diganti:** mengetik diganti berbicara.

**Untungnya:** wake word buatanmu berjalan di CPU dengan model sangat kecil.
Artinya SYNESIS bisa menunggu dipanggil tanpa memakan VRAM sedikit pun, dan
GPU tetap kosong untuk LLM. Ini bukan sekadar fitur, ini yang membuat asisten
selalu siaga jadi mungkin di laptop 4 GB.

**Sambungan matkul:** ini praktikum DSP. Fourier, windowing, konvolusi,
aliasing. Kandidat terkuat untuk tugas DSP untuk Sensor dan Imaging.

---

### Bulan 4 — Metric learning dan wajah · Desember

**Rencana lama:** Siamese network, contrastive loss, ArcFace, InsightFace,
kalibrasi ambang dengan kurva ROC.

**Yang berubah:** hampir tidak ada. Bagian ini memang berdiri sendiri.

**Organ yang ditambah:** SYNESIS tahu siapa yang di depan layar.

**Untungnya:** pagar keamanan di `alat.py` sekarang bergantung pada kamu
menekan Enter. Dengan pengenalan wajah, ia bisa bergantung pada **siapa** yang
menekan. Perintah yang mengubah disk cuma jalan kalau yang duduk di depan
memang kamu.

**Sambungan matkul:** kurva ROC dan kalibrasi ambang adalah bahan laporan ML
yang kuat.

---

### Yang jelas mundur

**MCP, bagian 4 req.md.** Itu implementasi protokol, bukan fitur. Sendirian
butuh berhari-hari penuh. Tempatnya setelah Bulan 2, saat kamu sudah nyaman
dengan bentuk alat dan intent.

**Voice, bagian 5 req.md. DIPUTUSKAN 22 Agustus.** TTS masuk Hari 1, dan
`suara.py` dibuat dua tahap:

```
tahap 1  teks -> wav        Piper, CPU, nol VRAM, selalu jalan
tahap 2  wav  -> wav        konversi suara, opsional, mati secara bawaan
```

Tahap dua menjalankan model apa pun yang kamu taruh di `E:\SYNESIS\suara` dan
kamu sebut di `konfig.py`. Berkas modelnya kamu yang sediakan.

**Target suara: Yukino Yukinoshita. DIPUTUSKAN 22 Agustus.** Dua bagian
terpisah, dikerjakan orang berbeda:

| Bagian | Siapa | Kapan |
|---|---|---|
| Kepribadian: pilihan kata, ritme, sikap | saya, di `konfig.SISTEM` | Hari 1 |
| Timbre: berkas model konversi suara | kamu, taruh di `E:\SYNESIS\suara` | kapan saja |

Bagian pertama yang sebenarnya membawa karakter. Dingin dan elegan itu soal
kalimat pendek, kata yang dipilih hati-hati, dan apa yang sengaja tidak
diucapkan. Itu jalan hari ini, nol VRAM, tanpa unduhan apa pun.

Angka yang perlu kamu tahu sebelum menyalakan tahap dua:

| | VRAM | Bisa barengan LLM? |
|---|---|---|
| Piper saja | 0 | ya |
| RVC di GPU | 1 sampai 2 GB | tidak, sisa VRAM cuma 0,9 GB |
| RVC di CPU | 0 | ya, tapi kecepatannya harus diukur dulu |

Jalur CPU itu yang paling mungkin dipakai, dan saya belum tahu seberapa cepat
di prosesormu. Itu pengukuran sepuluh menit, dilakukan setelah rangkanya jalan.

**Otonomi penuh, bagian 6 req.md.** "Jalankan script lalu perbaiki kalau ada
error" tanpa konfirmasi adalah agen yang bisa menghapus skripsimu karena satu
salah tafsir. Versi warasnya sudah masuk Hari 1: agen mengusulkan, kamu
menyetujui. Otonomi lebih jauh menunggu sampai kamu punya data seberapa sering
usulnya benar.

---

---

## 3b. OpenJarvis sebagai acuan. DIPUTUSKAN 22 Agustus.

Repo yang kamu maksud di Bagian 6 req.md itu nyata dan serius:

```
open-jarvis/OpenJarvis
Stanford Hazy Research + Scaling Intelligence Lab
8.900 bintang, 1.049 commit, aktif
Apache 2.0
Python >= 3.10, memakai Ollama, ekstensi Rust, GUI Tauri
Windows didukung native
```

Isinya persis yang kamu gambarkan: agent loop, sistem skill, katalog tool,
delapan agen bawaan dengan tiga mode jalan, dan evaluasi yang memperlakukan
energi serta latensi sebagai kendala kelas satu.

**Keputusan: SYNESIS tetap ditulis sendiri. OpenJarvis dipakai sebagai acuan,
bukan sebagai fondasi.**

Alasannya bukan gengsi. Kalau macet setelah 27 Agustus, kamu men-debug tujuh
berkas kecil buatanmu, bukan kerangka riset Stanford. Dan repo itu Apache 2.0,
tidak akan ke mana-mana, jadi tidak ada yang hilang kalau dibaca belakangan.

### Kapan membaca bagian mana

Ini kegiatan yang tidak butuh Claude sama sekali, jadi cocok dikerjakan
setelah 27 Agustus.

| Kapan | Yang dibaca | Untuk menjawab |
|---|---|---|
| Setelah v0.1 jalan | cara mereka mengevaluasi energi dan latensi | kendala utamamu VRAM, dan mereka memang mengukurnya |
| Setelah Bulan 1 | agent loop mereka | bandingkan dengan `agen.py` milikmu, cari yang kamu lewatkan |
| Setelah Bulan 2 | sistem skill dan katalog tool | bandingkan dengan `alat.py` dan intent classifier-mu |
| Kalau butuh terjadwal | tiga mode jalan mereka | SYNESIS v0.1 cuma punya mode on-demand |

Urutannya sengaja begitu. Membaca kode orang sebelum menulis versimu sendiri
membuatmu meniru bentuknya tanpa tahu kenapa. Membacanya sesudah, kamu punya
pertanyaan sungguhan untuk diajukan ke kode itu.

### Risiko yang belum diperiksa

README OpenJarvis tidak menyebutkan kebutuhan VRAM sama sekali. Untuk proyek
yang mengukur energi dan latensi, itu ganjil, dan biasanya artinya diuji di
mesin jauh lebih besar dari 1650 Ti 4 GB. Belum diverifikasi.

## 4. Yang saya butuh kamu putuskan

Delapan hal. Tidak perlu dijawab semua sekaligus, tapi lima yang pertama
memblokir Hari 1.

Nomor 1, 2, 3, dan 5 sudah diputuskan 22 Agustus. Rinciannya di bagian Hari 1.

4. **Bahasa TTS tahap satu.** Suara Piper bahasa Inggris jauh lebih halus. Yang
   Indonesia ada tapi kasar. Kalau jawabannya Indonesia tapi suaranya model
   Inggris, pelafalannya akan aneh. Kamu perlu dengar sendiri sebelum
   memutuskan. Ini terpisah dari tahap dua, dan tidak memblokir apa pun.

6. **Daftar isi `knowledge/` di atas benar?** Mana yang tidak akan kamu pakai,
   dan apa yang saya lewatkan.

7. **Perintah apa yang paling sering kamu ketik sehari-hari?** Ini menentukan
   alat mana yang dibuat lebih dulu, dan nanti jadi bahan mentah intent
   classifier Bulan 2.

8. **Bulan 1 diteruskan atau ditunda?** Sesi 1 hampir selesai. Bisa diselesaikan
   dulu sebelum sprint, atau ditunda sampai setelah 25.

---

## 5. Risiko yang saya lihat

| Risiko | Kemungkinan | Kalau terjadi |
|---|---|---|
| Unduhan 3 GB lambat atau putus | Sedang | Hari 1 molor. Model bisa diganti yang 1,5 GB |
| Qwen2.5-3B payah berbahasa Indonesia | Sedang | Ganti Gemma-2-2B, atau paksa jawab Inggris |
| Model 3B gagal pakai alat dengan andal | **Tinggi** | Alat dipanggil manual dengan perintah garis miring, LLM cuma untuk bahasa |
| VRAM penuh saat model dan aplikasi lain jalan | Sedang | Turun ke kuantisasi lebih kecil, atau jalankan di CPU |
| Tiga hari ternyata tidak cukup | Sedang | Hari 3 dipotong, dokumentasi dipadatkan, `knowledge/` diprioritaskan |

Baris ketiga yang paling perlu kamu waspadai. Model 3 miliar parameter memang
sering gagal memanggil alat dengan benar. Kalau itu terjadi, rencana
cadangannya sudah jelas dan tidak menghancurkan apa pun: perintah alat kamu
ketik langsung dengan garis miring, dan LLM tetap berguna untuk yang lain.

---

## 6. Apa yang sudah ada di disk sekarang

Tidak ada yang terpasang. Tidak ada yang diunduh. `ollama` belum ada,
`~/.ollama` belum ada.

Yang ada cuma empat berkas Python di `synesis/`, murni teks lokal, dan bisa
dihapus dalam satu detik kalau arahnya tidak kamu suka.
