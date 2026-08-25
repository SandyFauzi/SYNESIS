# SYNESIS bisa merespon apa saja

Daftar ini bukan tebakan. Tiap baris di bawah benar-benar dijalankan lewat
pipa niat pada 26 Agustus 2026, dan angka keyakinannya yang tercetak.

Jawaban pendeknya: **tiga hal yang benar-benar jalan**, empat hal yang
sengaja ditahan sampai kamu mengizinkan, dan delapan hal yang menunggu model
bahasa di Bulan 6.

---

## Yang benar-benar jalan

### 1. Info sistem

```text
kamu > cek ram sama cpu dong
  info_sistem  conf 0.882  BACA  -> jalan
    System:
      CPU      : 66 percent
      RAM      : 12.6 of 15.4 GB
      Disk C:  : 82 GB free of 246 GB
      Disk E:  : 178 GB free of 477 GB
      Disk S:  : 103 GB free of 954 GB
      GPU      : NVIDIA GeForce GTX 1650 Ti, VRAM 1669 of 4096 MB
```

Yang terukur berhasil:

| kalimat | keyakinan |
| --- | --- |
| berapa sisa disk dan ram | 0,978 |
| cek spek laptop | 0,904 |
| cek ram sama cpu dong | 0,882 |
| cek vram gpu | 0,858 |

Yang terukur GAGAL, dan ini yang menarik:

| kalimat | keyakinan | hasil |
| --- | --- | --- |
| `info sistem` | 0,303 | ditolak |
| `berapa memori terpakai` | 0,323 | ditolak |

Kalimat yang paling ringkas justru yang paling gampang ditolak. Sebabnya
model dilatih dari kalimat seperti orang bicara, bukan dari nama perintah.
"info sistem" terdengar seperti label menu, dan label menu tidak ada di data
latihnya.

### 2. Mencari berkas

```text
kamu > cariin file py
  cari_berkas  conf 0.946  BACA  -> jalan
    Found:
      S:\Code\Make A Jarvis\notebooks\bulan1_kanvas.py
      S:\Code\Make A Jarvis\notebooks\bulan1_sesi1_autograd.py
      S:\Code\Make A Jarvis\notebooks\bulan1_sesi2_mlp.py
      ...
```

| kalimat | keyakinan |
| --- | --- |
| cari file suara | 0,947 |
| cariin file py | 0,946 |
| temukan berkas md | 0,925 |
| cari file log | 0,914 |
| cari berkas notebooks | 0,796 |
| cariin dokumen markdown | 0,647 |

Polanya jelas: **kata kerja + kata "file" atau "berkas" + apa yang dicari.**
Semakin dekat ke pola itu, semakin tinggi keyakinannya.

### 3. Membuka berkas

```text
kamu > buka log.md
  buka_berkas  conf 0.841  BACA  -> jalan
    log.md:
    # Log Kerja SYNESIS

    Catatan kronologis semua yang dikerjakan, termasuk keputusan yang
    diambil dan kesalahan yang terjadi.
```

| kalimat | keyakinan |
| --- | --- |
| bukain laporan praktikum | 0,917 |
| tampilkan log.md | 0,872 |
| buka berkas readme | 0,843 |
| buka log.md | 0,841 |
| buka file konfig | 0,661 |

Yang terukur GAGAL dan patut jadi peringatan:

```text
kamu > buka todo
  jalankan_program  conf 0.613  MERUSAK  -> ditolak
```

Dua kata saja, dan model salah menebaknya sebagai menjalankan program. Yang
menyelamatkan bukan ketepatan model melainkan ambangnya: intent MERUSAK
menuntut keyakinan 0,995, dan 0,613 jauh di bawahnya. Tulis
`buka file todo` atau `buka todo.md` dan ia benar.

Kalau nama berkasnya cocok ke beberapa berkas, SYNESIS mendaftarkannya dan
bertanya. Ia tidak menebak.

---

## Yang ditahan sampai kamu mengizinkan

Empat intent mengarah ke shell. Semuanya dikenali, semuanya memunculkan
dialog konfirmasi, dan jawaban bawaan dialognya **Tidak**.

| kalimat | intent | keyakinan | risiko |
| --- | --- | --- | --- |
| commit perubahan ini | kelola_repo | 0,945 | TULIS |
| install numpy | pasang_paket | 0,604 | MERUSAK |
| git status dong | kelola_repo | 0,581 | TULIS |
| restart laptop | kontrol_sistem | 0,408 | MERUSAK |

Perhatikan bahwa keempatnya di atas tercatat **ditolak** waktu diuji, karena
keyakinannya belum melewati ambang kelas risikonya: TULIS menuntut 0,950 dan
MERUSAK menuntut 0,995.

Itu memang yang diinginkan. Kesalahan pada `restart laptop` jauh lebih mahal
daripada kesalahan pada `cari file py`, jadi ambangnya jauh lebih tinggi.

---

## Yang dikenali tapi alatnya belum ada

Ia tahu maksudmu, dan ia jujur bilang belum bisa.

| kalimat | intent | keyakinan | hasil |
| --- | --- | --- | --- |
| ingatkan aku besok jam sembilan | jadwal | 0,989 | belum ada alat |
| hitung dua tambah dua | hitung | 0,980 | belum ada alat |
| ringkas catatan kuliah | ringkas_catatan | 0,734 | belum ada alat |

`hitung` dan `jadwal` sebenarnya bisa dibuat tanpa model bahasa sama sekali;
keduanya tercatat di `TODO.md` sebagai pekerjaan yang belum diambil.

---

## Yang butuh model bahasa, dan itu Bulan 6

Enam intent ini tidak akan pernah berhasil sampai ada LLM lokal:
`jelaskan_konsep`, `lanjut_tugas`, `obrol`, `ringkas_catatan`, `tanya_umum`,
`ubah_proyek`.

| kalimat | intent | keyakinan |
| --- | --- | --- |
| apa itu fourier | obrol | 0,527 |
| lanjutkan tugas kemarin | lanjut_tugas | 0,416 |
| jelaskan apa itu konvolusi | jelaskan_konsep | 0,382 |
| gimana kabarmu | — | 0,000 |

Baris terakhir berbeda dari yang lain: keyakinannya nol karena **tidak satu
pun katanya ada di kosakata model**. "gimana" dan "kabarmu" tidak pernah
muncul di data latihnya. Itu bukan tebakan yang salah; itu penolakan sebelum
menebak.

Jadi jangan mengajaknya mengobrol. Ia bukan chatbot, dan sampai Bulan 6 ia
memang tidak dirancang jadi chatbot.

---

## Jadi apa yang sebaiknya diucapkan

Sepuluh kalimat yang terukur berhasil, urut dari yang paling andal:

```text
berapa sisa disk dan ram
cari file suara
cariin file py
temukan berkas md
bukain laporan praktikum
cek spek laptop
cari file log
tampilkan log.md
cek ram sama cpu dong
buka berkas readme
```

Lewat suara, tiap kalimat didahului wake word:

```text
"hey synesis"  ... tunggu ia menyala ...  "cariin file py"
```

### Tiga aturan yang menaikkan peluangnya

1. **Bicara seperti ke orang, bukan seperti ke menu.** `cek ram sama cpu dong`
   berhasil di 0,882; `info sistem` ditolak di 0,303.
2. **Sebut kata "file" atau "berkas".** `cari file log` 0,914 lawan
   `buka todo` yang ditebak sebagai menjalankan program.
3. **Jangan terlalu pendek.** Dua kata sering tidak cukup untuk membedakan
   membuka berkas dari menjalankan program.

---

## Kalau ia salah, itu justru yang paling berguna

Di jendela, pilih intent yang benar di dropdown lalu tekan **Fix**. Di
terminal: `/wrong <intent>`.

```text
kamu > buka todo
  jalankan_program  conf 0.613  MERUSAK  -> ditolak
kamu > /wrong buka_berkas
  tercatat: 'buka todo' -> buka_berkas
```

Tiap koreksi masuk ke `koreksi.jsonl` dan ikut dilatih di `Retrain`
berikutnya, yang memakan 1,8 detik.

Ini bukan sekadar fitur kenyamanan. Data uji SYNESIS sekarang cuma 41 kalimat
nyata, dan itu terlalu sedikit sehingga selang kepercayaannya 30 poin.
Targetnya 300 sampai 500. Cara mengumpulkannya bukan menulis kalimat di
berkas, melainkan memakai SYNESIS untuk kerja sungguhan lalu membetulkannya
waktu ia salah.

---

## Angka jujurnya

Dari 41 pesan nyata di arsip percakapan, cuma **5 atau 6** yang intent-nya
punya alat. Akurasinya **56,1 persen** dengan dasar mayoritas 39,0 persen,
dan selang 95 persennya `40,9 .. 71,3`.

Enam cara memperbaikinya sudah dicoba dan diukur; semuanya mendarat di
rentang 36 sampai 56 persen. Yang tersisa dan belum diuji: lima belas label
intent itu sendiri mungkin terlalu tumpang tindih untuk dipisahkan dari
teksnya.

Jadi jangan berharap ia mengerti semua yang kamu ucapkan. Yang dijaminnya:
ia tidak bertindak waktu ragu, dan tiap kesalahan tercatat supaya bisa
dibetulkan.

Selebihnya di [MANUAL.md](MANUAL.md).
