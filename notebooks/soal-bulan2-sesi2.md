# Soal Bulan 2 Sesi 2 - intent classifier SYNESIS

Berkas latihan: [`bulan2_sesi2_intent.py`](bulan2_sesi2_intent.py)

Tujuh TODO. Sesi ini menutup tiga utang yang digantung Sesi 1: tidak ada data
uji (Soal 6c), buta sinonim (Soal 3), dan salah tebak itu mahal (Soal 8c).

> Prasyarat: Sesi 1 dikerjakan dulu. Dan `Tensor` dari Bulan 1 Sesi 3+4 harus
> jalan, karena berkas ini mengimpornya apa adanya. Nol kode autograd baru.

---

## Soal 1 - Berapa data yang sebenarnya kamu butuh

Bagian 1 memberi:

```text
total perintah : 120
himpunan uji   : 24 kalimat
sqrt(0.9 * 0.1 / 24) = 0.0612, yaitu 6.1 poin persen
```

**1a.** Turunkan sendiri dari mana rumus $\sqrt{p(1-p)/n}$ itu datang. Mulai
dari sebaran binomial: tiap kalimat uji itu satu percobaan Bernoulli dengan
peluang benar $p$.

**1b.** Kamu ingin selang kepercayaan 95 persennya selebar 5 poin persen,
bukan 24. Hitung berapa kalimat uji yang kamu butuhkan.

**1c.** Dari 1b, dan dari proporsi belahan 70/15/15, hitung berapa total
kalimat yang harus kamu tulis. Bandingkan dengan angka 300 sampai 500 di
rencana Bulan 2.

**1d.** Sekarang tulis kalimatnya. Bukan yang saya bayangkan, yang **memang
kamu ucapkan**. Buka riwayat perintah terminalmu, catatan, dan pesanmu
sendiri selama seminggu terakhir sebagai bahan. Catat berapa kelas baru yang
muncul yang tidak ada di delapan kelas awal.

<details>
<summary>Petunjuk 1b</summary>

Lebar selang $\approx 4\sqrt{p(1-p)/n}$. Pasang $p = 0.9$ dan lebar $= 0.05$,
lalu selesaikan untuk $n$.

Perhatikan bahwa $n$ masuk sebagai akar. Menyempitkan selang dua kali lipat
butuh data empat kali lipat, dan itu alasan kenapa "tambah data sedikit" itu
hampir tidak pernah cukup.
</details>

---

## Soal 2 - Kebocoran

`bangun_kosakata` sengaja dipanggil dengan himpunan latih saja.

**2a.** Kalau kosakata dibangun dari SELURUH data, apa persisnya yang bocor?
Jawaban "data uji ikut terlihat" terlalu kasar. Sebutkan informasi apa yang
berpindah, dan lewat jalur apa.

**2b.** Apakah kebocoran itu membuat akurasi uji naik atau turun? Ramalkan
dulu, lalu ukur: ubah satu baris di `__main__`, jalankan Bagian 3, catat.

**2c.** `bobot_idf` juga cuma dihitung dari himpunan latih. Kebocoran macam
apa yang dicegah di situ, dan kenapa ia lebih halus daripada 2a?

**2d.** Di Bagian 3, kosakata dan IDF dihitung ulang di dalam gelung untuk
tiap belahan. Kenapa itu wajib, dan apa yang rusak kalau kamu menghitungnya
sekali di luar gelung?

---

## Soal 3 - Percobaan yang tidak bisa memutuskan

Bagian 3 memberi:

```text
fitur          validasi rata2    uji rata2   uji terburuk   uji terbaik
hitung kata             65.6%        68.2%          54.2%         79.2%
TF-IDF                  65.6%        66.7%          50.0%         75.0%
```

**3a.** Sebaran hasil 25 poin persen, selisih antar-resep 0,0 poin persen.
Nyatakan kesimpulan yang benar dalam satu kalimat, dan jelaskan kenapa
"hitung kata lebih baik" bukan kesimpulan yang sah.

**3b.** Kamu sudah pernah menghadapi bentuk ini di praktikum fisika. Tuliskan
padanannya: apa yang jadi ralat pengukuran, dan apa yang jadi selisih yang
mau diukur.

**3c.** Rancang percobaan yang BISA memutuskan. Berapa belahan, berapa data,
atau uji statistik apa. Sebutkan yang paling murah lebih dulu.

**3d.** Berkas ini tetap memakai `hitung kata` untuk bagian selanjutnya.
Karena akurasi tidak bisa jadi alasan, sebutkan alasan yang sah untuk memilih
salah satunya. Ada beberapa, sebut minimal dua.

<details>
<summary>Petunjuk 3d</summary>

Kalau dua pilihan sama baiknya secara terukur, yang menentukan bukan lagi
akurasi. Pikirkan: mana yang lebih sedikit kodenya, mana yang lebih sedikit
keadaan yang harus disimpan waktu SYNESIS jalan, mana yang lebih gampang
kamu jelaskan waktu ia salah.

Sesi 1 Soal 3d menanyakan pertanyaan bertipe sama untuk embedding.
</details>

---

## Soal 4 - Matriks bingung

Buka matriks bingung di keluaran Bagian 4.

**4a.** Sebutkan pasangan kelas yang paling sering tertukar di matriksmu.
Buka kalimat-kalimat yang salah itu satu per satu.

**4b.** Untuk tiap kesalahan di 4a, putuskan: ini masalah model, atau masalah
data? Kriterianya tegas — kalau kamu sendiri tidak bisa menentukan kelasnya
dari kalimat itu saja, itu masalah data, bukan model.

**4c.** `buka_berkas` dan `jalankan_program` sama-sama sering diawali kata
"buka". Apakah keduanya memang dua intent, atau sebenarnya satu intent dengan
slot yang berbeda? Argumentasikan dua-duanya, lalu putuskan.

**4d.** Kelas mana yang presisinya rendah tapi recall-nya tinggi? Jelaskan
apa artinya itu secara konkret untuk pengguna SYNESIS, dalam satu kalimat
tanpa istilah presisi atau recall.

---

## Soal 5 - Ambang, dan ongkos yang tidak simetris

Bagian 5 memberi:

```text
  ambang     benar    salah   menolak   asing ditolak
    0.00        18        6         0        0 dari 5
    0.50        15        5         4        4 dari 5
    0.90         9        0        15        5 dari 5
```

**5a.** Di ambang 0,00 model menebak salah 6 kali dan tidak pernah menolak.
Kelima kalimat asing juga dapat kelas. Jelaskan dari sifat softmax kenapa ia
TIDAK BISA mengeluarkan "bukan salah satu dari ini", walau seyakin apa pun
kamu berharap.

**5b.** Susun tabel ongkos untuk SYNESIS. Untuk tiap intent, isi dua kolom:
harga satu tebakan salah, dan harga satu penolakan yang seharusnya diterima.
Pakai satuan apa pun asal konsisten.

**5c.** Dari 5b, tentukan ambang per intent, bukan satu ambang global.
Terapkan di kode, jalankan ulang Bagian 5, dan bandingkan dengan ambang
tunggal terbaik.

**5d.** Ada cara ketiga selain menebak dan menolak: bertanya balik. Rancang
kapan SYNESIS harus bertanya "maksudmu buka berkas atau jalankan program?"
Nyatakan syaratnya dalam besaran yang bisa dihitung dari keluaran softmax.

<details>
<summary>Petunjuk 5d</summary>

Peluang tertinggi rendah artinya model tidak yakin apa pun. Itu penolakan.

Tapi ada keadaan lain: peluang tertinggi dan kedua tertinggi hampir sama
besar, dan dua-duanya cukup tinggi. Model yakin jawabannya salah satu dari
dua, dan cuma tidak tahu yang mana. Itu keadaan yang pantas ditanyakan, bukan
ditolak.

Selisih dua peluang teratas namanya margin.
</details>

---

## Soal 6 - Kapan aturan tangan berhenti cukup

`ekstrak_slot` sengaja bukan pembelajaran mesin.

**6a.** Tambah lima frasa waktu ke tabel `WAKTU` yang memang kamu pakai, lalu
catat berapa lama waktu yang kamu butuhkan. Bandingkan dengan waktu yang
dibutuhkan untuk melabeli lima puluh kalimat baru.

**6b.** Sebutkan tiga bentuk kalimat yang membuat `ekstrak_slot` versimu
salah, yang tidak bisa kamu perbaiki dengan sekadar menambah entri tabel.

**6c.** Dari 6b, nyatakan syarat umumnya: sifat apa dari sebuah slot yang
membuat aturan tangan berhenti memadai dan model mulai layak?

**6d.** Untuk SYNESIS di laptopmu, dengan data yang kamu punya, slot mana
yang tetap kamu tangani dengan aturan tangan sampai Bulan 6? Jawab dengan
angka dari 6a.

---

## Soal 7 - Slot yang tidak disebutkan

Spesifikasi `ekstrak_slot` melarang menebak. "jam tiga" jadi `03:00`, bukan
`15:00`, kecuali ada penanda sore atau malam.

**7a.** Sebutkan satu perintah nyata di mana menebak `15:00` untuk "jam tiga"
menyebabkan kerugian, dan satu lagi di mana menebak `03:00` yang merugikan.

**7b.** Dari 7a, jelaskan kenapa "ambil yang paling mungkin" adalah aturan
yang salah untuk slot, padahal itu aturan yang benar untuk intent.

**7c.** Rancang perilaku yang benar untuk jam yang ambigu. Kaitkan dengan
jawabanmu di 5d.

**7d.** `alat.py` di `synesis/` memerlukan callback `izin` sebelum
menjalankan apa pun. Jelaskan bagaimana ambang Soal 5 dan slot yang tidak
ditebak di soal ini bersama-sama membentuk lapisan keamanan yang sama.

---

## Soal 8 - Batas pengklasifikasi ini

Bagian 7 memberi:

```text
total          : 0.004 milidetik per perintah
ukuran model   : 68.3 KB
kosakata       : 173 kata
```

**8a.** Bandingkan dengan model bahasa 3B yang butuh sekitar 1.900.000 KB.
Hitung rasionya, lalu hitung berapa perintah yang bisa diproses
pengklasifikasi ini dalam waktu yang dibutuhkan LLM untuk memuat bobotnya
saja.

**8b.** Tulis lima perintah yang BENAR-BENAR butuh LLM, yang tidak mungkin
diselesaikan klasifikasi 8 kelas berapa pun banyaknya datamu. Untuk tiap
perintah, sebutkan apa persisnya yang hilang.

**8c.** Ini yang berbahaya: pengklasifikasi tidak akan bilang "ini di luar
kemampuanku". Untuk kelima perintah di 8b, jalankan lewat modelmu dan catat
kelas serta keyakinan yang keluar. Apakah ambang Soal 5 menangkap semuanya?

**8d.** Rancang pembagian kerja antara pengklasifikasi dan LLM untuk SYNESIS,
dan nyatakan aturan penyerahannya sebagai syarat yang bisa dihitung. Ingat
batas keras dari `req.md`: LLM-nya 3B dan tinggal 0,9 GB VRAM sesudah model
lain.

---

## Tolok Ukur Bulan 2 Sesi 2

- [ ] Belahan tiga arah ditulis sendiri, dan proporsi kelasnya dijaga
- [ ] Ukuran data yang dibutuhkan dihitung dari selang kepercayaan, bukan ditebak
- [ ] Kalimat perintah ditambah sampai jumlah hasil hitungan Soal 1c
- [ ] TF-IDF ditulis sendiri, dan normalisasi barisnya diuji berpanjang 1
- [ ] Kebocoran kosakata diramalkan arahnya lebih dulu, lalu diukur
- [ ] Kesimpulan "percobaan ini tidak bisa memutuskan" dinyatakan, bukan dihindari
- [ ] Matriks bingung dibaca, dan tiap kesalahan digolongkan model atau data
- [ ] Ambang per intent ditetapkan dari tabel ongkos, bukan dari satu angka global
- [ ] Keadaan "bertanya balik" dirumuskan lewat margin dua peluang teratas
- [ ] Ekstraksi slot jalan, dan slot yang tidak disebutkan tidak ditebak
- [ ] Lima perintah yang butuh LLM ditulis, dijalankan, dan keyakinannya dicatat
- [ ] Aturan penyerahan classifier ke LLM dinyatakan sebagai syarat terhitung

Kalau kedua belas kotak beres, kamu punya SYNESIS v0.1: perintah teks jadi
intent jadi argumen, nol LLM, 0,004 milidetik. Yang tersisa menyambungkannya
ke `synesis/alat.py`.
