# Dasar gaya dan batas bukti

## Temuan lintas kategori

**Gaya berubah mengikuti fungsi video.** `CC CSM LOOP_1` memakai distorsi dan
aksen warna kuat; `Bumper Conference` memakai bidang putih dan warna identitas;
`OLED PPS` lebih bertumpu pada presenter. Jangan menjadikan salah satunya preset
untuk seluruh pekerjaan.

**Compositing menjadi alat bercerita.** Contoh AMV/MMV memakai perpindahan antara
wajah, ruang luas, tipografi, objek, dan lapisan cahaya. Pada konten sains,
lapisan tambahan berubah menjadi foto, label, diagram, dan tabel yang menjelaskan
narasi. Pertanyaan sebelum menambah layer: bagian cerita atau informasi apa yang
menjadi lebih terbaca?

**Warna dan tekstur dipilih per dunia visual.** Violet/Frieren menunjukkan
highlight bercahaya dan pergeseran hangat-dingin. CSM menunjukkan merah terang,
kontras, dan distorsi. Porak menunjukkan elemen komik berwarna cerah. HUT NESAS
memakai tekstur kertas dan bingkai; konferensi memakai palet logo. Identitasnya
terletak pada kecocokan pilihan, bukan satu LUT.

**Teks mempunyai beberapa peran.** Ada subtitle dialog kecil, lirik/teks 3D
sebagai objek komposisi, judul panel manga, kartu informasi, subtitle presenter,
label lokasi, dan CTA/QR. Pilih peran sebelum menentukan animasinya. Jangan
menyalin subtitle kecil AMV untuk informasi yang harus dibaca di ponsel.

**Proyek dibagi menjadi bagian yang dapat direvisi.** Dari 38 proyek Premiere
utama, 27 mempunyai lebih dari satu objek sequence. Ada nested sequence dan
bagian bernama `Prosedur`, `Ambil Data`, `Analisa`, `Music`, serta urutan
wawancara. Beberapa proyek merujuk `.aep`; render memiliki pasangan CC, SFX,
RSMB, upscale, serta rasio berbeda. Gunakan pemisahan serupa ketika membantu
pekerjaan; hitungan sequence tidak sama dengan jumlah bagian video final.

**Audio mendapat pengolahan khusus.** Komponen proyek mencakup Dynamics
Processing, Multiband Compressor, DeNoise, EQ, reverb, dan pitch shifting pada
proyek tertentu. `10 Foto Angkasa` juga merujuk shutter kamera, paper sound,
button press, dan whoosh. Ini mendukung penggunaan audio narasi, musik, serta
SFX terpisah sesuai fungsi. Tidak membuktikan setelan kompresor, loudness,
beat grid, atau keseimbangan mix yang selalu sama.

## Format hasil

Metadata korpus menunjukkan banyak render `1920×1080`, juga portrait
`1080×1920`, frame lebih sempit seperti `1500×1080`, serta variasi lain.
Frame rate sumber beragam, termasuk pecahan `30000/1001` dan `24000/1001`.
Pilih ukuran/fps dari brief dan kebutuhan proyek; data ini bukan instruksi
untuk selalu mengekspor landscape atau memaksa 60 fps. Periksa rasio,
crop, interpolasi, dan ketajaman teks pada hasil yang benar-benar dirender.

## Tingkat bukti

| Label | Makna | Boleh digunakan untuk |
|---|---|---|
| V | Frame video benar-benar diperiksa | Komposisi, warna, jenis teks, objek/lapisan yang terlihat |
| T | Frame berurutan pada jendela singkat diperiksa | Perubahan posisi, skala, blur, dan transisi pada jendela itu |
| P | Struktur `.prproj` dibaca | Nama sequence, referensi aset, komponen efek dan status bypass |
| M | Metadata/daftar file | Durasi, resolusi, frame rate, hubungan nama versi |
| R | Resep adaptasi | Pilihan kerja yang disimpulkan agar pola berguna pada brief baru |

Resep di setiap profil merupakan R kecuali dijelaskan sebagai pengamatan.
Jangan mengubah resep menjadi pernyataan historis tentang cara Sandzh selalu
mengedit. Jangan menyimpulkan BPM, sinkron beat, atau rasa audio dari gambar.
Saat sinkronisasi penting, analisis/dengarkan audio sumber dan cocokkan dengan
gerak/cut hasilnya.

## Cakupan pemeriksaan awal

634 file terinventarisasi; 401 video berhasil diperiksa metadatanya; 44 berkas
Premiere ditemukan, terdiri dari 38 proyek utama dan 6 autosave. Sebanyak 48
video ditinjau dengan 288 frame tersebar; delapan di antaranya ditambah 64 frame
berurutan. Ini pemeriksaan sampel, bukan penayangan penuh seluruh koleksi.
Data kuantitatif rinci ada dalam `korpus.json`.

Tidak ada `.aep`/`.aepx` di tiga akar yang dipindai. Referensi `.aep` dalam
Premiere hanya dibaca sebagai path; isinya tidak dianalisis. Kurva Graph Editor,
expression, preset plugin AE, dan urutan layer asli belum dapat dipastikan.
Tidak dilakukan penilaian pendengaran audio dalam pembentukan profil awal.
Jangan mengaku telah mendengarkan mix atau mengukur karakter suara.

Folder `S:\Video Convert` memuat hasil edit, rekaman mentah, video unduhan,
overlay, dan simulasi. Watermark `PREVIEW` pada MMV adalah status preview;
logo intro/outro, watermark Sandzh, dan materi kolaborasi jangan disalin
otomatis. Label tahun pada nama file juga dapat berbeda dari teks di frame.

Durasi clip item yang diekstrak dari proyek mencakup nested sequence, bagian
bertumpuk, dan revisi. Jangan menggunakannya sebagai median durasi shot final.
Statistik perubahan visual dari scene detection juga bukan beat detector atau
daftar cut yang pasti.
