# Script rekaman wake word SYNESIS

Yang perlu diucapkan, berikut variasinya. Sekitar 15 menit sekali duduk.

Tiga bagian, dan ketiganya perlu:

| bagian | isi                        | jumlah | dipakai untuk                                  |
| ------ | -------------------------- | ------ | ---------------------------------------------- |
| A      | "hey synesis"              | 44     | kelas POSITIF model wake word                  |
| B      | kata yang mirip tapi bukan | 24     | kelas NEGATIF, yang paling menentukan          |
| C      | kalimat perintah biasa     | 24     | menguji pipa penuh, dan mengisi`audit.jsonl` |

---

## Sebelum mulai

**Satu aturan yang menentukan segalanya: berhenti sekitar satu detik sesudah
tiap ucapan.** Pemotongnya bekerja dari jeda, bukan dari hitungan. Kalau kamu
bicara terus tanpa jeda, dua ucapan menyatu jadi satu berkas dan berkas itu
terbuang.

Rekaman lama kamu, `Recording (2).m4a`, jatuh persis di kasus itu:

```text
  no    mulai   durasi   puncak  catatan
   1    0.15s    8.51s    0.985  terlalu panjang, mungkin dua ucapan menyatu
   2   10.53s   16.48s    0.493  terlalu panjang, mungkin dua ucapan menyatu
```

Aturan lain:

- **Jangan berteriak dan jangan berbisik ke mikrofon.** Puncak 0,985 di
  rekaman lama itu artinya sinyalnya nyaris terpotong. Sasarannya 0,3 sampai
  0,8.
- **Ucapkan dengan cara yang sama seperti kamu akan memakainya sehari-hari.**
  Kalau saat memakai nanti kamu bilang "hei sinesis" dengan santai, jangan
  merekamnya dengan artikulasi presenter berita.
- **Ejaannya tidak penting, pengucapannya yang penting.** Pilih satu cara
  mengucapkannya, lalu pakai itu terus. "hey sinesis", "hei sinesis", atau
  "hey synesis" boleh, asal konsisten.
- **Biarkan suara ruangan apa adanya.** Kipas, AC, dan lalu lintas justru
  membantu; model yang cuma pernah mendengar ruangan senyap akan gagal di
  ruangan biasa.

### Dua cara merekam, pilih satu

**Cara 1 — dipandu SYNESIS (dianjurkan).** Ada hitungan mundur, tiap ucapan
langsung tersimpan sendiri, tidak perlu dipotong:

```powershell
. .\scripts\activate.ps1
python -m synesis.suara rekam 44
```

**Cara 2 — Perekam Suara Windows.** Rekam jadi satu berkas panjang sambil
mengikuti daftar di bawah, lalu potong:

```powershell
python -m synesis.suara potong "C:\Users\SANDY FAUZI\Documents\Sound recordings\Recording.m4a" bangun
```

Cara 2 yang perlu jeda satu detik itu. Cara 1 tidak, karena batasnya
ditentukan hitungan mundur.

---

## Bagian A — 44 kali "hey synesis"

Ucapkan **"hey synesis"** tiap baris, dengan variasi yang tertulis. Variasinya
bukan hiasan: 44 rekaman yang seragam menghasilkan model yang cuma bekerja
kalau kamu duduk persis seperti waktu merekam.

### A1. Jarak (12 ucapan)

| no | ucapan | cara |
| ------ | ----------- | -------------------------------------- |
| 1–3 | hey synesis | dekat, sekitar 20 cm dari mikrofon |
| 4–6 | hey synesis | jarak duduk biasa, sekitar 50 cm |
| 7–9 | hey synesis | agak jauh, sekitar 1,5 meter |
| 10–12 | hey synesis | dari seberang ruangan, sekitar 3 meter |

### A2. Kerasnya suara (8 ucapan)

| no | ucapan | cara |
| ------ | ----------- | ------------------------------------------ |
| 13–15 | hey synesis | pelan, hampir berbisik tapi masih bersuara |
| 16–18 | hey synesis | biasa |
| 19–20 | hey synesis | keras, seperti memanggil dari dapur |

### A3. Kecepatan dan irama (8 ucapan)

| no | ucapan | cara |
| ------ | ------------ | ---------------------------- |
| 21–23 | hey synesis | cepat, buru-buru |
| 24–26 | hey synesis | lambat, tiap suku kata jelas |
| 27–28 | hey, synesis | dengan jeda kecil di tengah |

### A4. Arah kepala dan posisi (8 ucapan)

| no | ucapan | cara |
| ------ | ----------- | -------------------------------- |
| 29–31 | hey synesis | menghadap layar, seperti biasa |
| 32–33 | hey synesis | menoleh ke samping |
| 34–35 | hey synesis | membelakangi mikrofon |
| 36 | hey synesis | sambil menunduk melihat keyboard |

### A5. Keadaan suara (8 ucapan)

| no | ucapan | cara |
| ------ | ----------- | --------------------------------------------- |
| 37–38 | hey synesis | suara pagi, belum sepenuhnya bangun |
| 39–40 | hey synesis | sambil tersenyum, nada naik |
| 41–42 | hey synesis | datar, lelah |
| 43–44 | hey synesis | dengan derau: kipas menyala, atau musik pelan |

Setelah bagian A, hentikan rekaman dan potong dulu:

```powershell
python -m synesis.suara potong "...\Recording.m4a" bangun
```

Periksa hasilnya: harus ada sekitar 44 berkas di `E:\SYNESIS\suara\bangun`,
durasi tiap berkas antara 0,6 dan 1,8 detik. Yang bertanda "terlalu panjang"
berarti dua ucapan menyatu; hapus berkasnya dan rekam ulang beberapa.

---

## Bagian B — 24 ucapan yang BUKAN wake word

Ini bagian yang paling menentukan, dan yang paling sering dilewatkan orang.
Model butuh tahu di mana batasnya. Tanpa bagian B, model belajar bahwa "ada
suara manusia" sama dengan "bangun".

Rekam ini sebagai berkas terpisah, lalu potong dengan label `bukan`:

```powershell
python -m synesis.suara potong "...\Recording-bukan.m4a" bukan
```

### B1. Bunyinya mirip, artinya beda (10 ucapan)

| no | ucapan     |
| -- | ---------- |
| 1  | hey        |
| 2  | synesis    |
| 3  | sinusitis  |
| 4  | sintesis   |
| 5  | sinis      |
| 6  | hey series |
| 7  | hei siapa  |
| 8  | analisis   |
| 9  | hey sisir  |
| 10 | genesis    |

### B2. Separuh wake word (6 ucapan)

| no | ucapan  |
| -- | ------- |
| 11 | hey hey |
| 12 | sis     |
| 13 | ne sis  |
| 14 | hey sin |
| 15 | esis    |
| 16 | hey nes |

### B3. Percakapan biasa (8 ucapan)

Ucapkan seperti sedang bicara ke orang, bukan ke mesin.

| no | ucapan                |
| -- | --------------------- |
| 17 | iya bentar            |
| 18 | oke nanti aku kirim   |
| 19 | halo, ini siapa ya    |
| 20 | wah gila sih ini      |
| 21 | nanti sore aja ya     |
| 22 | aduh lupa lagi        |
| 23 | sebentar aku cek dulu |
| 24 | udah, itu aja         |

> Kalau Speech Commands sudah diunduh, `latih` otomatis menambahkan puluhan
> ribu kata bahasa Inggris sebagai negatif tambahan. Bagian B tetap perlu,
> karena yang di sana tidak ada satu pun yang mirip "hey synesis" dan tidak
> ada satu pun yang memakai suaramu.

---

## Bagian C — 24 kalimat perintah

Bukan untuk wake word. Ini untuk menguji rantai penuh dan untuk mengisi
`audit.jsonl`, yaitu utang Bulan 2 yang sampai sekarang cuma punya 41 kalimat
nyata.

Cara merekamnya berbeda: **jangan direkam ke berkas.** Jalankan loop suaranya,
lalu ucapkan satu per satu, diawali wake word:

```powershell
python -m synesis.suara dengar
```

Ucapkan "hey synesis", tunggu SYNESIS menyala, baru ucapkan kalimatnya.

### C1. Yang sudah punya alat (12 kalimat)

| no | ucapkan                  |
| -- | ------------------------ |
| 1  | buka log titik em de     |
| 2  | tampilkan file todo      |
| 3  | bukain laporan praktikum |
| 4  | buka berkas readme       |
| 5  | cariin file py           |
| 6  | cari berkas notebooks    |
| 7  | cari file log            |
| 8  | temukan berkas markdown  |
| 9  | cek ram sama cpu dong    |
| 10 | berapa sisa disk dan ram |
| 11 | cek vram gpu             |
| 12 | info sistem              |

### C2. Yang belum punya alat, dan memang harus ditolak (6 kalimat)

Ini menguji pagar, bukan kemampuan. Yang benar adalah SYNESIS menolak.

| no | ucapkan                         |
| -- | ------------------------------- |
| 13 | jelaskan apa itu konvolusi      |
| 14 | ringkas catatan kuliah hari ini |
| 15 | hitung dua tambah dua           |
| 16 | ingatkan aku besok jam sembilan |
| 17 | lanjutkan tugas kemarin         |
| 18 | gimana kabarmu                  |

### C3. Kalimat sehari-harimu sendiri (6 kalimat)

Bagian ini kosong dengan sengaja. Ucapkan enam kalimat yang benar-benar akan
kamu pakai, dengan kata-katamu sendiri, bukan meniru daftar di atas. Justru
kalimat inilah yang paling berharga, karena 41 kalimat nyata yang ada sekarang
semuanya berasal dari satu arsip percakapan dan belum tentu mewakili cara kamu
memakai SYNESIS.

Kalau tebakan intent-nya salah, betulkan lewat jendela atau `/wrong <intent>`.
Tiap koreksi masuk ke `koreksi.jsonl` dan ikut dilatih.

---

## Sesudah semuanya direkam

```powershell
python -m synesis.suara latih
python -m synesis.suara ambang
```

Keluarannya kira-kira begini:

```text
  positif 44  negatif 1344
  fitur                 |################################|    1388/1388
  latih wake word       |################################|      25/25
  AUC 0.9942  ambang 0.612  -> E:\SYNESIS\models\wake\wake.pt
```

Negatifnya 1.344 karena `latih` mengambil 30 kata Speech Commands untuk tiap
satu contoh positif, ditambah 24 rekaman bagian B. Perbandingan 1 banding 30
itu sengaja, dan `CrossEntropyLoss` di dalamnya membobot ulang kelas positif
supaya model tidak belajar menjawab "bukan" untuk apa pun.

### Cara tahu hasilnya cukup baik

| angka              | batas                | kalau di bawahnya                                           |
| ------------------ | -------------------- | ----------------------------------------------------------- |
| AUC                | di atas 0,98         | rekam 20 contoh lagi, terutama di jarak yang belum tercakup |
| jumlah positif     | paling sedikit 40    | tambah                                                      |
| durasi tiap berkas | 0,6 sampai 1,8 detik | yang di luar itu hapus dan ulangi                           |

Lalu uji di keadaan nyata:

```powershell
python -m synesis.suara dengar
```

Biarkan menyala sambil kamu bekerja setengah jam. Dua hal yang perlu dihitung,
dan keduanya belum pernah diukur di ruangan sungguhan:

- **berapa kali ia menyala padahal kamu tidak memanggilnya.** Kalau lebih dari
  sekali per jam, naikkan `WAKE_AMBANG` di `konfig.py`, atau tambah rekaman
  bagian B.
- **berapa kali kamu harus mengulang panggilan.** Kalau lebih dari satu dari
  lima, tambah rekaman bagian A pada jarak dan kerasnya suara yang sering
  gagal.

Keduanya menukar satu dengan yang lain, dan yang memperbaiki keduanya
sekaligus cuma satu: menambah rekaman. Alasannya ada di
[soal-bulan3-sesi4.md](notebooks/soal-bulan3-sesi4.md) Soal 6c.

---

## Ringkasan perintah

```powershell
. .\scripts\activate.ps1

python -m synesis.suara rekam 44                    # cara 1, dipandu
python -m synesis.suara potong "...\Rekaman.m4a" bangun   # cara 2, dipotong
python -m synesis.suara potong "...\Bukan.m4a"   bukan

python -m synesis.suara latih
python -m synesis.suara ambang
python -m synesis.suara dengar
```
