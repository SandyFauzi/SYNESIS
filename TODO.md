# Sisa pekerjaan

Status per 26 Agustus 2026. Bulan 0, 1, 2, dan 3 sudah selesai disusun.
SYNESIS v0.2 berjalan dengan window, correction loop, retraining 1,8 detik,
dan rantai suara penuh: VAD, wake word, Whisper, Piper, RVC.

Wake word sudah dilatih dengan suara pemilik sendiri: 44 rekaman positif,
24 negatif yang bunyinya mirip, ditambah 1.320 kata Speech Commands.

```text
AUC 0,9867   ambang 0,960
di ambang itu: lolos 90,9 persen positif, 0,0 persen dari 24 negatif mirip
```

Peluncurnya `SYNESIS.exe` di akar repo, 8 MB, tinggal klik dua kali.

---

## Segera

### Koreksi label yang keliru

`synesis/model/koreksi.jsonl` memuat satu label yang tercatat karena bug
dropdown yang sudah ditambal:

```json
{"kalimat": "buka punya FUTRI KARTIKA", "intent": "jalankan_program"}
```

Baris `buka punya futri -> buka_berkas` tidak menggantikannya, sebab
`baca_koreksi` memakai teks kalimat sebagai kunci dan kedua kalimat tersebut
berbeda. Ketik ulang kalimat aslinya di window, pilih `buka_berkas`, lalu
tekan Fix dan Retrain.

### Commit dan push

Seluruh isi `synesis/` belum pernah masuk ke git, dan sembilan commit lama
belum di-push. Berkas berikut menunggu:

```
synesis/__init__.py  __main__.py  fitur.py  niat.py  latih.py
synesis/cli.py  jendela.py  uji.py  MANUAL.md
notebooks/bulan2_sesi3_embedding.py  bulan2_sesi4_synesis.py
notebooks/soal-bulan2-sesi3.md  soal-bulan2-sesi4.md  kunci_b2s34_bukti.py
```

Ditambah seluruh Bulan 3:

```
synesis/suara.py  synesis/rvc.py
notebooks/bulan3_sesi1_konvolusi.py  bulan3_sesi2_spektrogram.py
notebooks/bulan3_sesi3_cnn.py  bulan3_sesi4_wakeword.py
notebooks/soal-bulan3-sesi1.md .. sesi5.md  kunci_b3_bukti.py
prosedur_bulan3.md
scripts/unduh_speech_commands.py  scripts/bangun_exe.py
synesis/luncur.py  synesis/SCRIPT.md  SYNESIS.cmd
```

`SYNESIS.exe` TIDAK masuk git; ia hasil bangun, dan `scripts/bangun_exe.py`
membuatnya ulang dalam belasan detik.

`synesis/model/` sudah diabaikan git kecuali `.gitkeep`. Gambar di
`figures/` juga diabaikan dan memang bisa dibuat ulang dengan menjalankan
notebooknya. Bobot suara TIDAK masuk git dan memang tidak boleh: seluruhnya
di `E:\SYNESIS\models`, dan totalnya sekitar 700 MB.

### Catat ke log.md

Pekerjaan 25 Agustus belum masuk `log.md`: refactor paket, integrasi encoder,
correction loop, dua bug yang saya buat sendiri, dan penurunan waktu training
dari 133,5 detik ke 1,8 detik.

---

## Utang Bulan 3

### Wake word sudah dilatih, yang tersisa menyetelnya

Selesai. 44 positif di `E:\SYNESIS\suara\bangun`, 24 negatif di
`E:\SYNESIS\suara\bukan`, AUC 0,9867, ambang 0,960 tersimpan di dalam `wake.pt`.

Yang tersisa, dan baru bisa dikerjakan sesudah dipakai sungguhan:

- **Kalau sering harus mengulang panggilan**, rekam 20 positif lagi pada
  jarak dan kerasnya suara yang paling sering gagal. Daftar variasinya di
  [`synesis/SCRIPT.md`](synesis/SCRIPT.md) bagian A.
- **Kalau ia menyala sendiri lebih dari sekali per jam**, rekam lagi bagian B,
  yaitu kata yang bunyinya mirip. Itu yang paling menggigit, bukan menaikkan
  ambang.

Menambah rekaman memperbaiki keduanya sekaligus; menggeser ambang cuma
menukar satu dengan yang lain. Alasannya di Soal 6c Sesi 4.

Tiga rekaman lama yang puncaknya di bawah 0,05 belum dibuang:
`bangun_001`, `bangun_015`, `bangun_024`. Hapus lalu `rekam 3` kalau sempat.

### Uji lapangan yang belum ada

Seluruh angka Bulan 3 diukur di berkas, bukan di ruangan. Yang belum diukur:

- berapa kali wake word menyala palsu dalam satu hari pemakaian nyata;
- berapa FRR di kamar dengan kipas menyala;
- apakah `VAD_ATAS_DB = 8` cocok untuk mikrofon EMEET C60E, atau perlu digeser.

Jalankan `python -m synesis.suara dengar` selama beberapa jam sambil bekerja,
lalu hitung barisnya di `audit.jsonl`.

### Anggaran 3 detik SUDAH terlewati

Ini utang yang paling menggigit, dan `kunci_b3_bukti.py --penuh` sekarang
GAGAL di baris ini dengan sengaja:

```text
[GAGAL] anggaran latensi di bawah 3 detik (janji docs/Modul.md)
        3.84 detik, utang tercatat di TODO.md
```

Sebabnya kesalahan pengukuran saya. Transkripsi dihitung sebagai RTF dikali
durasi ucapan, padahal Whisper membantali masukannya sampai 30 detik sehingga
ongkosnya TETAP:

```text
1,0 detik ucapan -> 2,48 detik      3,0 detik -> 2,60 detik
2,0 detik        -> 2,64 detik      8,0 detik -> 2,60 detik
```

Anggaran sesungguhnya 3.845 milidetik, dan transkripsi memakan 68 persennya.

Tiga jalan keluar, dua di antaranya sudah diukur:

| jalan | keadaan |
| --- | --- |
| model `base` | **diuji, TIDAK bisa.** Pada suara pemilik ia lebih lambat (6,37 detik lawan 3,52 detik untuk 12 detik ucapan) sekaligus jauh lebih buruk. Model yang menebak ngawur mengeluarkan lebih banyak token, dan tiap token dibayar waktu |
| Whisper di GPU | belum diuji. Harganya VRAM, yang sudah dijanjikan untuk Bulan 6 |
| transkripsi mengalir | belum dikerjakan. Ditandai `ponytail:` di `synesis/suara.py`. Menghapus hampir seluruh 2.600 milidetik dari latensi yang TERASA, karena kerjanya bertumpang tindih dengan bicaranya |

Yang sudah dikerjakan dan mengurangi keluhan paling banyak: `panaskan()`.
Sebelumnya ongkos muat 31 detik dibayar di tengah perintah PERTAMA, sehingga
perintah pertama terasa 23 detik dan yang kedua 2,6 detik. Sekarang ia
dipindah ke layar pembuka dengan bilah kemajuan.

### Indeks faiss RVC belum dipakai

`added_IVF1102_Flat_nprobe_1_Yukinoshita_Yukino_v2.index` sebesar 136 MB ada
di folder model dan tidak disentuh sama sekali, setara `index_rate = 0`.

Terukur akibatnya: Whisper membaca keluaran RVC sebagai `laporan 4 tikung`
padahal masukannya `laporan praktikum`. Retrieval mempertajam konsonan, dan
kemungkinan besar itu penyebab utamanya.

Membacanya tanpa faiss berarti menulis pencarian tetangga terdekat sendiri di
atas matriks 136 MB. Bisa dikerjakan dengan numpy, dan perlu diukur dulu
apakah pengaruhnya sepadan. Soal 4c Sesi 5 menyebut cara memisahkannya dari
dua penyebab lain.

### Dialog konfirmasi belum menampilkan transkripsi

Perintah yang datang lewat suara melewati pagar yang sama dengan teks, dan
itu benar. Yang kurang: waktu SYNESIS meminta konfirmasi untuk intent TULIS
atau MERUSAK, ia menampilkan intent dan argumennya tetapi tidak menampilkan
apa yang ia DENGAR. Pemilik jadi tidak bisa melihat bahwa Whisper salah
dengar sebelum menekan ya.

Perbaikannya satu baris di `jendela.py` dan `niat.izin_konsol`: sertakan
`kalimat` di dalam rencana yang ditampilkan.

### `audit.jsonl` sekarang memuat ucapan

Sampai v0.1, isinya kalimat yang diketik pemilik sendiri. Sejak v0.2 ia
memuat transkripsi apa pun yang terdengar sesudah wake word menyala,
termasuk suara orang lain di ruangan yang sama.

Berkasnya tidak pernah meninggalkan mesin dan sudah ada di `.gitignore`, jadi
ini bukan kebocoran keluar. Yang belum ada: batas umur untuk baris yang
berasal dari suara, misalnya dibuang otomatis sesudah 30 hari kecuali ia jadi
koreksi.

---

## Utang Bulan 2

### Kumpulkan kalimat nyata sampai 300–500

Data uji sekarang 41 pesan, dan Soal 1c Sesi 2 menghitung 3.840 kalimat untuk
selang kepercayaan selebar 5 poin. Target menengah 300 sampai 500 kalimat.

Pengumpulannya tidak dilakukan dengan menulis kalimat, melainkan dengan
memakai SYNESIS untuk pekerjaan sehari-hari lalu mengoreksi prediksinya. Tiap
koreksi masuk ke `koreksi.jsonl`, dan tiap keputusan masuk ke `audit.jsonl`.

### Uji hipotesis label tumpang tindih

Enam pendekatan perbaikan sudah diuji dan seluruhnya menghasilkan akurasi
dalam rentang 36 sampai 56 persen. Kemungkinan terakhir yang belum diuji:
lima belas label intent terlalu tumpang tindih untuk dipisahkan berdasarkan
teksnya.

Pengujiannya tidak memerlukan unduhan atau training. Beri label ulang 41 pesan
tersebut tanpa melihat label lama, lalu bandingkan. Jika Anda sendiri tidak
konsisten pada sekitar 40 persen kasus, batas atasnya memang berasal dari
label, bukan dari model.

---

## Bug terukur yang belum ditambal

### Spasi di akhir nama menembus lapisan pengaman kedua

```
_aman("S:/Code/Make A Jarvis/.env.")  -> ditolak
_aman("S:/Code/Make A Jarvis/.env ")  -> lolos
```

Windows membuang spasi di akhir nama ketika membuka berkas, sehingga jalur
yang lolos tetap terbaca. Terukur: `log.md`, `log.md.`, dan `log.md.`
ketiganya terbaca 90.867 karakter, sama dengan `log.md`.

Perbaikannya satu baris di `_bukan_rahasia`, sebelum `POLA_RAHASIA.match`:

```python
bagian = bagian.rstrip(". ")
```

Dampaknya nyata karena `S:\Code` memuat `.env` milik tiga proyek lain.

### `cari_isi` tidak melewati `_aman`

Fungsi tersebut membaca isi berkas `.md` dan `.py` secara langsung, sehingga
lapisan pengaman kedua tidak berlaku. Saat ini tidak ada berkas yang terdampak,
tetapi `secrets.py` yang dibuat besok akan lolos.

### `jalankan` tidak memiliki path guard

Keadaan tersebut memang disengaja, sebab `jalankan` dijaga oleh konfirmasi
manusia dan confidence threshold 0,995. Konsekuensinya perlu dicatat: selama
`jalankan` ada, lapisan pengaman kedua hanya membatasi tool baca.

### Training bisa menimpa model tanpa jejak

Model sempat berubah dari `gabung` 789 kolom ke `kantong` 402 kolom tanpa
catatan siapa yang memicunya. `latih.latih()` sebaiknya menulis satu baris ke
berkas log setiap kali menyimpan model.

---

## Tool yang belum dibuat

Tujuh intent memiliki tool, delapan sisanya belum. Dua di antaranya bisa
dikerjakan tanpa language model:

| intent | catatan |
| ---------- | ---------------------------------------------------------------------------------------- |
| `hitung` | Soal 1d Sesi 4 membahas kenapa`eval` membuat kelas risikonya naik dari BACA ke MERUSAK |
| `jadwal` | perlu tool tulis pertama, kelas risiko TULIS |

Enam sisanya (`jelaskan_konsep`, `lanjut_tugas`, `obrol`, `ringkas_catatan`,
`tanya_umum`, `ubah_proyek`) memerlukan language model di Bulan 6.

---

## Perbaikan kualitas yang tertunda

Ditandai `ponytail:` di dalam kode dan sengaja belum dikerjakan:

- `synesis/jendela.py:218` — window berjalan satu thread. Pindahkan ke worker
  thread jika nanti ada tool lambat yang tidak melewati dialog konfirmasi.
- `synesis/fitur.py` — `vektorkan` dan `ekstrak_slot` punya dua salinan, satu
  di paket dan satu di `notebooks/`. Notebooks adalah jawaban latihan yang
  dibekukan, jadi duplikasi ini disengaja.
- `notebooks/bulan1_kanvas.py:113` — pergeseran center of mass memakai
  `np.roll` dengan bilangan bulat.
- `scripts/generate_bulan2_data.py:243` — pengacakan deterministik.
- `synesis/suara.py` — `transkrip` menunggu ucapannya selesai sebelum mulai.
  Upgrade path-nya transkripsi mengalir; lihat Utang Bulan 3.
- `synesis/suara.py` — `_panaskan_cudnn` ada semata-mata karena torch dan
  ctranslate2 membawa cuDNN sendiri-sendiri. Boleh dihapus begitu keduanya
  memakai versi yang sama; cara memeriksanya ada di Soal 5b Sesi 5.
- `synesis/suara.py` dan `notebooks/bulan3_sesi2_spektrogram.py` — `fitur_audio`
  punya dua salinan, alasannya sama dengan `fitur.py`. Yang menjaganya tetap
  sama: Uji E di `kunci_b3_bukti.py`.
- Jendela tkinter belum punya tombol suara. Sengaja: `dengar()` gelung yang
  memblokir, dan `jendela.py` masih satu thread. Keduanya utang yang sama,
  jadi yang atas dulu.

---

## Bulan 4 sampai 6

Belum disusun. Perkiraan dari `docs/Roadmap.md`:

| bulan | materi                                         | jam | perkiraan sesi |
| ----- | ---------------------------------------------- | --- | -------------- |
| 4     | metric learning, face recognition              | 20  | 3              |
| 5     | attention, transformer, mini-GPT               | 28  | 4              |
| 6     | agent loop, language model lokal, SYNESIS v1.0 | 24  | 4              |

Bulan 3 sudah selesai disusun dan seluruh berkasnya jalan:

| sesi | berkas                          | isi                                  |
| ---- | ------------------------------- | ------------------------------------ |
| 1    | `bulan3_sesi1_konvolusi.py`     | konvolusi 1D/2D, im2col, aliasing    |
| 2    | `bulan3_sesi2_spektrogram.py`   | STFT, mel, MFCC, semuanya dari nol   |
| 3    | `bulan3_sesi3_cnn.py`           | CNN di atas `Tensor` Bulan 1         |
| 4    | `bulan3_sesi4_wakeword.py`      | Speech Commands, wake word, ROC      |
| 5    | `synesis/suara.py`, `rvc.py`    | SYNESIS v0.2                         |
| —    | `kunci_b3_bukti.py`             | 50 klaim Bulan 3, diuji ulang        |

Dua hal yang MASUK di luar Roadmap, dari `req.md` bagian 5:

- Piper bahasa Indonesia sebagai ganti `en_US-amy-medium`;
- RVC v2 untuk warna suara Yukino, lintasan inferensinya ditulis sendiri
  karena `rvc-python` dan `rvc-inferpy` sama-sama gagal dipasang di
  Python 3.12 (fairseq dan faiss-cpu tidak punya wheel).

Satu janji Roadmap yang tidak ditepati dan perlu dicatat: "semua di CPU, GPU
disimpan untuk Bulan 6". RVC memakai GPU, karena di CPU RTF-nya terukur 1,66,
lebih lambat daripada waktu nyata. `RVC_AKTIF = False` mengembalikan janji itu
dengan harga suara Piper polos.

---

## Yang perlu ditinjau ulang

Bagian 4 `docs/Roadmap.md` menyatakan 80 sampai 90 persen pemakaian harian
dapat ditangani classifier tanpa language model. Pada 41 pesan nyata, angkanya
5 dari 41 atau sekitar 12 persen.

Sampel tersebut berasal dari satu arsip percakapan perancangan proyek yang
memang terbuka dari ujung ke ujung, sehingga belum tentu mewakili cara Anda
memakai SYNESIS untuk membuka berkas praktikum. Pernyataan di roadmap perlu
ditinjau ulang setelah `audit.jsonl` memuat pemakaian yang lebih representatif.
