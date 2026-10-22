# AMV action dan GMV

## AMV action

Referensi di `D:\AEP SANDZH\AMVS`:

- `CC Comp Madara Wasted.mp4`: wajah 1.21 dtk, aksi 5.76 dtk, mata 10.62 dtk,
  kekuatan biru 15.47–20.93 dtk. Perubahan skala subjek menjadi bagian urutan.
- `CC CSM LOOP_1.mp4`: elemen angka/cahaya pada 1.09 dtk, fragmen komposisi
  5.19 dtk, close-up relatif bersih 9.56 dtk, distorsi merah/putih 13.94–18.86
  dtk, gangguan warna 23.78 dtk. Jendela 13.00–14.05 dtk ditinjau berurutan.
- `PART 9 SANDZH.mp4`: potongan kolaborasi 10.71 dtk dengan karakter, flash,
  cahaya ungu, serta teks/ruang compositing. Jendela 4.90–5.95 dtk diperiksa.
- `Part 39 - Sandzh 2.mp4`: 7.34 dtk; karakter bertekstur halftone dan
  perpindahan dari adegan lebar menuju ekspresi.

Resep: tentukan apa yang akan menjadi impact—gerakan, tatapan, serangan,
kemunculan kekuatan—lalu susun setup → impact → pemulihan. Pilih sumber dengan
arah gerak yang dapat disambung. Tempatkan perpindahan skala, flash, distorsi,
atau shake pada aksen terpilih setelah memeriksa audio; sisakan momen gambar
bersih agar energi berikutnya terbaca.

Pola terlihat dapat didekati dengan transform, directional/radial blur,
displacement, glow, mask, dan remap jika editor mendukung. Nama plugin maupun
kurva timing persis tidak terverifikasi dari render. Jangan menyebut teknik
tertentu sebagai plugin asli hanya karena tampak serupa.

## GMV

- `Flow GMV MLBB Naruto CC.mp4`, 40.04 dtk: kartu profil/akun, elemen anime,
  gameplay, lalu karakter. Sampel 1.60, 7.61, 14.01, 20.42, 27.63, 34.83 dtk.
- `GMV RSMB Wydiq.mp4`, 20.89 dtk: perayaan pemain dengan teks besar,
  gameplay, lightning/glow, dan blur kuat; jendela 9.80–10.85 dtk diperiksa.

Resep: tentukan momen gameplay yang ingin ditonjolkan. Bangun konteks singkat,
kejadian utama, lalu payoff. Teks nama/ucapan dan animasi game boleh mengambil
peran panggung; hero, target, dan hasil aksi tetap harus bisa dikenali.
Lindungi area HUD yang relevan terhadap cerita. Kombinasi anime–game adalah
salah satu pilihan teramati, bukan kewajiban untuk setiap highlight.

Nama `RSMB` ada pada render, tetapi parameter plugin belum diperiksa. Jika
melakukan retiming/interpolasi, periksa tepi HUD, karakter, efek skill, dan
objek transparan untuk artefak sebelum menerapkan blur tambahan.

## Modifier kolaborasi/MEP

`PART 9 SANDZH`, `Part 39`, `SANDZH'S OC 2`, dan versi `NOCC`/`CC` menjadi
petunjuk adanya pekerjaan per part. Pastikan durasi, batas masuk/keluar,
ukuran frame, fps, color pass, audio, serta kebutuhan transisi ditentukan
oleh brief kolaborasi. Jangan mengubah panjang part untuk menambah logo.
Slate seperti `YOUR PART 1/2` adalah instruksi template, bukan elemen yang
otomatis masuk ke video final.
