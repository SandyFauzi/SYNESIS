# SYNESIS v0.2 — Manual

Asisten lokal. Nol API, nol internet, nol model bahasa. Sejak Bulan 3 ia juga
mendengar dan berbicara, dan itu pun tanpa satu byte pun keluar dari laptop.

---

## Menjalankannya

**Klik dua kali `SYNESIS.exe`** di akar repo. Muncul menu:

```text
============================================================
  SYNESIS v0.2   asisten lokal, tanpa internet
============================================================
  repo : S:\Code\Make A Jarvis
  venv : E:\SYNESIS\.venv\Scripts\python.exe

   1  Suara, dry run       Dengarkan dan jawab, tapi tidak ada alat dipanggil
   2  Suara, LIVE          Alat benar-benar dipanggil. Berkas bisa terbuka
   3  Jendela, dry run     Antarmuka tkinter, aman
   4  Jendela, LIVE        Antarmuka tkinter, alat aktif
   5  Terminal             Ketik perintah, tanpa jendela
   6  Rekam wake word      Rekam contoh 'hey synesis' dengan hitungan mundur
   7  Latih wake word      Latih ulang dari rekaman yang ada
   8  Uji suara keluar     Ucapkan satu kalimat dengan suara Yukino
   9  Periksa semua        Jalankan seluruh pemeriksa modul
   0  Keluar
```

`SYNESIS.cmd` mengerjakan hal yang sama tanpa perlu dibangun ulang. Pakai itu
kalau kamu baru saja mengubah `synesis\luncur.py`.

### Kalau lebih suka mengetik

Direktorinya **`S:\Code\Make A Jarvis`**, akar repo, bukan folder `synesis`.
Kalau kamu berdiri di dalam `synesis\`, paketnya justru tidak ketemu.

```powershell
cd "S:\Code\Make A Jarvis"
. .\scripts\activate.ps1

python -m synesis                   # jendela, dry run
python -m synesis --sungguhan       # jendela, alat aktif
python -m synesis --teks            # terminal
python -m synesis.uji               # periksa semua modul
python -m synesis.latih gabung      # latih ulang intent

python -m synesis.suara dengar      # loop suara, dry run
python -m synesis.suara ucap "hai"  # uji suara keluar
```

`SYNESIS.exe` juga menerima argumen, jadi ia bisa dipakai sebagai pengganti
`python` di dalam skrip lain:

```powershell
.\SYNESIS.exe --teks
.\SYNESIS.exe -m synesis.suara ucap en "Your report is open."
```

> Cara model suaranya dipasang, lengkap dengan kegagalan yang
> ditemui dan pemeriksanya, ada di
> [prosedur_bulan3.md](../prosedur_bulan3.md).

### Apa yang sebenarnya ada di dalam .exe

Cuma peluncurnya, 8,0 MB. Ia mencari python di `E:\SYNESIS\.venv` lalu
memanggilnya; torch, onnxruntime, dan seluruh bobot model tetap di tempatnya.

Konsekuensinya perlu dinyatakan: **.exe ini bukan paket portabel.** Memindahkan
SYNESIS ke komputer lain berarti memindahkan repo dan `E:\SYNESIS`, bukan
menyalin satu berkas. Yang dibeli dengan keputusan itu: 8 MB dan belasan detik
membangun, bukan 3 GB dan belasan menit.

Bangun ulang: `python scripts\bangun_exe.py`.

---

## Dua mode

| mode | artinya |
|---|---|
| **dry run** (bawaan) | menebak dan memutuskan, tetapi tidak ada alat dipanggil |
| **live** | berkas benar-benar dibuka, folder dibaca, shell bisa jalan |

Diubah lewat kotak centang **dry run** di kanan atas jendela, atau `/dry` di
terminal.

Dry run jadi bawaan bukan karena sopan santun. Empat intent mengarah ke shell.
Kalau live yang jadi bawaan, satu tebakan salah di perintah pertama sudah
cukup.

---

## Membaca jawaban

> Daftar lengkap kalimat yang terukur berhasil, beserta yang terukur
> gagal dan sebabnya, ada di [BISA-APA.md](BISA-APA.md).


```text
kamu > cariin file py
  cari_berkas  conf 0.892  BACA  -> jalan
  Ditemukan:
    S:\Code\Make A Jarvis\notebooks\bulan1_kanvas.py
```

| bagian | arti |
|---|---|
| `cari_berkas` | intent yang ditebak |
| `conf 0.892` | keyakinan, 0 sampai 1 |
| `BACA` | kelas risiko alatnya |
| `-> jalan` | apa yang benar-benar terjadi |

### Kelas risiko

| kelas | arti | ambang keyakinan |
|---|---|---|
| `BACA` | tidak mengubah apa pun | 0,500 |
| `TULIS` | mengubah disk, bisa dibatalkan | 0,950 |
| `MERUSAK` | tidak bisa dibatalkan | 0,995 |
| `BAHASA` | butuh model bahasa, belum ada | 0,667 |

Keempat ambang itu tidak disetel tangan. Semuanya turun dari dua angka di
`konfig.py`:

```python
ONGKOS_TOLAK = 1.0
ONGKOS_SALAH = {"BACA": 2.0, "TULIS": 20.0, "MERUSAK": 200.0, "BAHASA": 3.0}
```

Aturannya `p > 1 - ongkos_tolak / ongkos_salah`. Ubah satu angka, kelima belas
ambang bergeser konsisten.

### Enam hasil yang mungkin

| hasil | arti |
|---|---|
| `jalan` | alatnya dipanggil |
| `ditolak - kata asing` | tidak satu pun kata ada di kosakata model |
| `ditolak - keyakinan rendah` | di bawah ambang kelas risikonya |
| `ditolak - tanpa argumen` | intent ketemu, argumennya tidak bisa dibangun |
| `ditolak - izin` | kamu menjawab tidak di dialog |
| `belum ada alat` | intentnya benar, alatnya belum dibuat |

---

## Suara

Seluruh rantainya berjalan luring. Tidak ada yang diunggah, tidak ada yang
disinggahkan di server mana pun.

```text
mikrofon -> VAD -> wake word -> perekam -> Whisper -> pipa niat
                                                   -> Piper -> RVC -> speaker
```

| tahap | yang berjalan | bobotnya di mana |
|---|---|---|
| fitur | log-mel, ditulis sendiri | `suara.py`, tanpa pustaka |
| VAD | tenaga terhadap lantai derau ruangan | `suara.py`, tanpa model |
| wake word | CNN kecil, dilatih dengan suaramu | `E:\SYNESIS\models\wake\wake.pt` |
| pengenal ucapan | faster-whisper `small`, CPU, int8 | `E:\SYNESIS\models\stt` |
| suara keluar | Piper: id, en, ja | `E:\SYNESIS\models\voice\piper` |
| warna suara | RVC v2, ditulis ulang di `rvc.py` | `E:\SYNESIS\models\voice\yukino` |

### Anggaran waktu, terukur

```text
muat ketiga model, sekali saat mulai     31000 ms   di layar pembuka
tunggu diam sebelum berhenti merekam       700 ms
transkripsi, berapa pun panjang ucapan    2600 ms   Whisper small, TETAP
pipa niat                                    5 ms
Piper untuk 3 detik balasan                210 ms   RTF 0,07
RVC untuk 3 detik balasan                  330 ms   RTF 0,11 di GPU
-------------------------------------------------  +
sesudah kamu selesai bicara               3845 ms
```

Batas yang dijanjikan `docs/Modul.md` 3 detik, dan ini **melampauinya
845 milidetik**. Versi pertama dokumen ini mengaku lolos dengan margin 215
milidetik, dan itu salah: transkripsi dihitung sebagai RTF dikali durasi
ucapan, padahal Whisper menambahkan bantalan sampai 30 detik di dalamnya
sehingga ongkosnya TETAP. Terukur 2,48 detik untuk ucapan 1 detik dan 2,60
detik untuk ucapan 8 detik.

Yang bisa menurunkannya, terukur juga: model `base` TIDAK bisa. Pada suara
pemilik ia justru lebih lambat (6,37 detik lawan 3,52 detik untuk 12 detik
ucapan) DAN jauh lebih buruk, karena model yang menebak ngawur menghasilkan
lebih banyak token dan tiap token dibayar waktu. Yang tersisa cuma dua:
Whisper di GPU, atau transkripsi mengalir.

Beban prosesor saat mendengarkan tanpa ada yang bicara: **3,1 persen**, untuk
sepuluh jendela deteksi per detik.

### Tiga bahasa, satu suara

Model Piper menentukan **bahasa dan iramanya**; RVC menentukan **warna
suaranya**. Jadi menambah bahasa cukup menambah satu berkas `.onnx`, dan
orangnya tetap sama.

```powershell
python -m synesis.suara ucap "Halo Sandy, laporan sudah saya buka."
python -m synesis.suara ucap en "Your lab report from last week is already open."
python -m synesis.suara ucap ja "先週の実験レポートはもう開いてあります。"
```

Bahasa Jepang butuh `pyopenjtalk-plus`; Indonesia dan Inggris tidak. Contoh
ketiganya ada di `E:\SYNESIS\suara\contoh`.

Diperiksa dengan mengembalikan keluaran RVC ke Whisper: untuk bahasa Inggris
ia kembali persis sama kata per kata dengan masukan Piper-nya, dan untuk
bahasa Indonesia ia kembali sedikit LEBIH baik daripada keluaran Piper
sendiri.

### Mematikan sebagian

Di `konfig.py`:

| setelan | akibat |
|---|---|
| `SUARA_AKTIF = False` | tidak ada suara sama sekali |
| `RVC_AKTIF = False` | Piper bicara, warnanya tidak diganti |
| `RVC_NADA` | geseran nada dalam semiton, 0 bawaan |
| `WAKE_AMBANG` | ditimpa oleh apa pun yang disimpan `latih` di berkas model |
| `STT_MODEL` | `tiny`, `base`, `small`, `medium`; makin besar makin lambat dan makin tepat |

---

## Wake word

### Keadaan sekarang

```text
positif  44 rekaman "hey synesis"
negatif  24 rekaman kata mirip + 1.320 kata Speech Commands
AUC      0,9867
ambang   0,960

di ambang itu:  lolos 90,9 persen positif,  0,0 persen dari 24 negatif mirip
```

### Merekam ulang atau menambah

Daftar lengkap apa yang perlu diucapkan beserta variasinya ada di
[SCRIPT.md](SCRIPT.md).

```powershell
python -m synesis.suara rekam 20      # dipandu, ada hitungan mundur
python -m synesis.suara latih         # cetak AUC dan ambang terpilih
python -m synesis.suara ambang        # lihat yang tersimpan di model
```

Merekam dengan Perekam Suara Windows juga boleh. Rekam jadi satu berkas
panjang, berhenti sekitar satu detik sesudah tiap ucapan, lalu potong:

```powershell
python -m synesis.suara potong "...\Recording.m4a" bangun
python -m synesis.suara potong "...\Recording-bukan.m4a" bukan
```

Pemotongnya memakai VAD, jadi yang menentukan batas tiap potongan adalah
jeda di antaranya, bukan hitungan.

### Ambangnya bukan titik kesalahan setara

Ia dipilih dengan meminimalkan ongkos, cara yang sama dengan kelima belas
ambang intent:

```text
salah menolak   kamu mengulang sekali                        ongkos   1
salah menerima  SYNESIS menyala di tengah percakapan,
                merekam, lalu melempar apa pun yang
                terdengar ke pipa niat                       ongkos 100
```

Bentuk umumnya layak diingat: dengan ongkos yang sangat tak simetris,
jawabannya selalu ambang TERENDAH yang sudah membuat FAR nol. Menaikkannya
lebih jauh cuma menambah kegagalan mengenali tanpa membeli apa pun.

---

## Mengoreksi tebakan yang salah

Di bawah kotak percakapan:

```text
salah? intent yang benar:  [ dropdown ]  [Fix]        [gabung] [Retrain]
```

1. SYNESIS menebak salah
2. Pilih intent yang benar di dropdown
3. Tekan **Fix**

Tersimpan ke `synesis/model/koreksi.jsonl`. Di terminal: `/wrong <intent>`.

**Dropdown-nya sengaja kosong saat muncul.** Versi lama mengisinya lebih dulu
dengan tebakan model sendiri, sehingga satu klik ceroboh mengesahkan kesalahan
dan mengajari model bahwa galatnya benar. Keyakinan pada satu label salah
sempat melompat dari 0,700 ke 0,995 karena itu. Pilihannya harus disengaja.

**Ini pekerjaan utamamu.** Bukan menulis kalimat latihan, melainkan memakai
SYNESIS untuk kerja sungguhan dan membetulkannya waktu ia salah.

### Melatih ulang intent

Tekan **Retrain**, atau ketik `/train`.

```text
melatih ulang...
  gabung 789 kolom  |  1,8 detik  |  3000 sintetis + 3 koreksi
  uji tertahan 23/41 = 56,1%
```

Model barunya langsung dipakai, tanpa restart.

| resep | kolom | butuh | catatan |
|---|---|---|---|
| `kantong` | ~400 | tidak ada | hitungan kata, muat seketika |
| `encoder` | 384 | sentence-transformers | MiniLM multibahasa |
| `gabung` | ~790 | sentence-transformers | keduanya, bawaan |

```text
kantong    16/41 = 39,0%     24,1 .. 54,0
encoder    17/41 = 41,5%     26,4 .. 56,5
gabung     23/41 = 56,1%     40,9 .. 71,3
dasar      16/41 = 39,0%
```

`gabung` titik tengahnya tertinggi, tetapi selangnya masih tumpang tindih
dengan yang lain. Itu pembacaan yang jujur.

---

## Pagar keamanan

Tiga lapis, dan suara TIDAK melewati satu pun di antaranya, karena ia masuk
ke pipa yang sama persis dengan teks.

1. **Jalur.** `_aman` menolak apa pun di luar `FOLDER_BOLEH`.
2. **Isi.** `_bukan_rahasia` menolak berkas yang namanya mencurigakan.
3. **Manusia.** `BUTUH_IZIN` menuntut konfirmasi untuk hapus, tulis, jalankan.

Yang BERUBAH sejak ada suara adalah peluang masukan yang tidak disengaja.
Mengetik "hapus semua" butuh sepuluh ketukan yang disadari; Whisper bisa
menghasilkan kalimat itu dari salah dengar. Jadi lapisan yang paling
menanggung beban tambahan adalah ambang keyakinan, dan untuk intent MERUSAK
ambangnya 0,995 justru karena hal semacam ini.

### Yang berubah pada catatan

`audit.jsonl` sekarang bisa memuat teks yang tidak pernah kamu ketik:
transkripsi apa pun yang terdengar sesudah wake word menyala, termasuk suara
orang lain di ruangan yang sama. Berkasnya tidak pernah meninggalkan mesin dan
sudah ada di `.gitignore`, jadi ini bukan kebocoran keluar. Yang perlu
disadari cakupannya, sebelum menyalakan `dengar` di ruangan berisi orang lain.

---

## Di mana semuanya disimpan

```text
S:\Code\Make A Jarvis\          repo, kode dan dokumen
  SYNESIS.exe                   peluncur, 8 MB, dibuat ulang kapan saja
  SYNESIS.cmd                   peluncur tanpa build
  synesis\
    luncur.py                   isi peluncur
    konfig.py                   seluruh setelan, satu tempat
    fitur.py                    kalimat -> vektor, kalimat -> slot
    niat.py                     model, kebijakan ongkos, pipa keputusan
    alat.py                     alat dan pagarnya
    latih.py                    pelatih intent
    suara.py                    mikrofon, VAD, wake word, Whisper, Piper
    rvc.py                      inferensi RVC v2, ditulis dari nol
    cli.py  jendela.py  uji.py
    MANUAL.md  SCRIPT.md
    model\                      diabaikan git kecuali .gitkeep
      model_intent.npz          otaknya
      audit.jsonl               catatan keputusan
      koreksi.jsonl             labelmu
      embed_cache.npz           embedding tersimpan

E:\SYNESIS\                     semua yang besar, di luar repo
  .venv\                        lingkungan Python
  suara\bangun\   44 wav        "hey synesis"
  suara\bukan\    24 wav        kata mirip yang bukan
  suara\contoh\   11 wav        contoh suara Yukino tiga bahasa
  models\wake\                  wake.pt
  models\stt\        486 MB     faster-whisper small
  models\voice\piper\ 203 MB    id, en, ja
  models\voice\yukino\ 327 MB   .pth dan .index
  data\speech_commands\ 1,2 GB  42.546 wav, negatif untuk wake word
```

---

## Kalau rusak

| gejala | sebab | perbaikan |
|---|---|---|
| `venv tidak ditemukan` | enclosure E: tidak terpasang | pasang, atau bangun ulang venv-nya |
| `No model at ...` | belum pernah dilatih | `python -m synesis.latih gabung` |
| pesan pertama lambat | encoder masih dimuat | tunggu `encoder siap`, sekitar 18 detik |
| dropdown resep cuma satu | sentence-transformers hilang | `pip install sentence-transformers`, atau pakai `kantong` |
| semua ditolak | model dilatih dengan resep lain | latih ulang, periksa `resep:` di bilah status |
| `model wake word belum ada` | belum direkam atau dilatih | `suara rekam 40`, lalu `suara latih` |
| wake word tidak pernah menyala | ambang terlalu tinggi, contoh terlalu sedikit | rekam 20 lagi, latih ulang, lihat `suara ambang` |
| wake word menyala terus | negatif terlalu sedikit | rekam bagian B di SCRIPT.md |
| suaranya datar, bukan Yukino | `.pth` hilang atau `RVC_AKTIF = False` | periksa `E:\SYNESIS\models\voice\yukino` |
| `ucap` pertama 15 detik | Piper, ContentVec, RVC dimuat sekaligus | cuma panggilan pertama; sesudahnya ~0,3 detik |
| tidak ada suara sama sekali | peranti keluaran salah | `python -c "import sounddevice; print(sounddevice.query_devices())"` |
| unduhan mendarat di C: | `HF_HOME` tidak disetel | sudah dipatok ke `E:\SYNESIS` di `konfig.py` |

Periksa semuanya sekaligus:

```powershell
python -m synesis.uji
```

---

## Batasnya, dengan jujur

**Intent.** Dari 41 pesan nyata di arsip, cuma **5 atau 6** yang intent-nya
punya alat. Sisanya permintaan terbuka yang butuh model bahasa, dan itu Bulan
6. Akurasinya **56,1 persen**, dasar mayoritas **39,0 persen**, selang 95
persennya `40,9 .. 71,3`. Keunggulannya tipis dan belum terukur kokoh.

Enam cara memperbaikinya sudah dicoba dan diukur. Semuanya mendarat di
rentang 36 sampai 56 persen. Yang tersisa dan belum diuji: lima belas label
intent itu sendiri mungkin terlalu tumpang tindih untuk dipisahkan dari
teksnya.

**Wake word.** AUC 0,9867 dari 44 rekaman. Seluruh angka itu diukur di
berkas, bukan di ruangan. Berapa kali ia menyala palsu dalam satu hari kerja,
dan berapa sering kamu harus mengulang panggilan di kamar dengan kipas
menyala, keduanya belum pernah diukur.

**Suara keluar.** Satu kata dari sebelas rusak pada uji kejelasan:
`praktikum` terbaca `4 tikung`. Tersangka utamanya indeks faiss 136 MB yang
tidak dipakai sama sekali.

Jadi jangan berharap SYNESIS v0.2 mengerti semua yang kamu ucapkan. Yang
dijaminnya: ia tidak akan bertindak waktu ragu, dan tiap kesalahan tercatat
supaya bisa dibetulkan.
