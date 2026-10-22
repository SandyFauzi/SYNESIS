---
name: sandzh-video-editor
description: >-
  Mengedit, merencanakan, atau mengevaluasi video dengan mengadaptasi gaya editing
  Sandy Fauzi Amrulloh (Sandzh) dari korpus lokalnya. Gunakan untuk permintaan
  gaya Sandzh/Sandy pada AMV emosional, AMV action, MMV, GMV, cinematic teaser,
  aftermovie, bumper, promosi sosial, edukasi sains, dan tutorial/praktikum.
  Pilih profil sesuai jenis video; jangan menerapkan seluruh efek AMV pada
  video penjelasan. Tidak menangani peniruan gaya penulisan atau desain web.
---

# Sandzh Video Editor

Adaptasikan keputusan editing Sandzh: hubungan antargambar, pembagian energi,
komposisi berlapis, teks, warna, dan fungsi efek. Dasarkan pilihan pada kategori
dan referensi yang paling dekat dengan brief terbaru.

## Pilih profil

| Kategori | Cocok untuk | Baca |
|---|---|---|
| AMV emosional | Relasi karakter, nostalgia, lirik, suasana | [amv-emosional.md](references/amv-emosional.md) |
| AMV action | Pertarungan, impact, montage anime berenergi tinggi | [amv-action-gmv.md](references/amv-action-gmv.md), bagian AMV |
| MMV | Panel manga, karakter cutout, animasi kedalaman | [mmv.md](references/mmv.md) |
| GMV | Gameplay, kill highlight, perayaan pemain | [amv-action-gmv.md](references/amv-action-gmv.md), bagian GMV |
| Cinematic/teaser | Adegan live action, mood film, cerita promosi | [cinematic-event.md](references/cinematic-event.md), bagian cinematic |
| Aftermovie/event | Rangkuman kegiatan, olahraga, kilas balik | [cinematic-event.md](references/cinematic-event.md), bagian event |
| Motion branding/bumper | Logo reveal, layar acara, visual tematik | [motion-branding.md](references/motion-branding.md) |
| Promosi sosial | Oprec, ajakan, format interaktif, video vertikal | [promosi-sosial.md](references/promosi-sosial.md) |
| Edukasi sains | Presenter, penjelasan konsep, visual pendukung | [edukasi-sains.md](references/edukasi-sains.md) |
| Tutorial/praktikum | Rekaman layar, langkah kerja, alat, tabel hasil | [tutorial-praktikum.md](references/tutorial-praktikum.md) |

Kolaborasi/MEP, lirik, portrait, dan landscape adalah modifier, bukan alasan
mengganti kategori utama. Untuk dua kategori sekaligus, tetapkan satu fungsi
utama lalu ambil teknik pendukung yang cocok. Contoh: promo acara dapat memakai
cerita cinematic dengan bumper identitas di akhir.

## Gunakan bukti dengan tepat

Korpus awal diperiksa pada 21 Oktober 2026:

- `D:\AEP SANDZH\AMVS`
- `D:\PR Project`
- `S:\Video Convert`

Baca [dasar-gaya.md](references/dasar-gaya.md) untuk pola bersama, batas
pengamatan, dan tingkat keyakinan. Untuk mencari berkas dan cuplikan yang
mendasari profil, gunakan [korpus.md](references/korpus.md), lalu cari nama
yang relevan dalam `references/korpus.json`. Jangan memuat seluruh katalog
atau semua profil jika tugas hanya membutuhkan satu kategori.

Prioritas keputusan: brief pengguna saat ini → contoh Sandzh yang dipilih
pengguna → pola kategori yang diamati → resep implementasi dalam skill.
Angka durasi, besaran efek, font, kurva easing, atau target audio yang tidak
diukur dari sumber harus disebut sebagai pilihan kerja, bukan preset pribadi
Sandzh. File `.prproj` membuktikan struktur proyek dan keberadaan komponen;
komponen itu belum tentu aktif di hasil akhir.

## Kerjakan sesuai tujuan

1. Tentukan kategori dari isi dan tujuan video. Periksa format, durasi, sumber
   gambar, musik/voice-over, serta hasil yang diminta. Isi kekosongan kecil dengan
   asumsi wajar; tanyakan hanya informasi yang menentukan hasil.
2. Pilih satu sampai tiga referensi yang paling dekat. Jika sumber tersedia,
   lihat cuplikan pembuka, bagian utama, transisi penting, dan penutup. Untuk
   meniru gerak, ambil frame berurutan di jendela pendek; contact sheet yang
   tersebar sepanjang video hanya membuktikan komposisi dan variasi visual.
3. Susun struktur editing: fungsi setiap bagian, sumber shot, informasi/emosi,
   alasan cut atau transisi, teks, dan lapisan audio. Musik menjadi acuan untuk
   montage; penjelasan menjadi acuan untuk edukasi dan tutorial.
4. Kerjakan rough cut terlebih dahulu, kemudian compositing/motion, warna,
   teks, dan audio sesuai kebutuhan. Gunakan proyek/nest per bagian bila
   kompleksitasnya membantu revisi. Jangan menambahkan tahapan yang tidak berguna.
5. Tinjau hasil pada kecepatan normal dan per frame di transisi penting.
   Periksa wajah, garis manga, HUD, rumus, teks, sinkronisasi, pemotongan audio,
   dan frame kosong yang tidak disengaja. Bedakan slate/hold kolaborasi yang
   memang diminta dari kesalahan render.

Untuk menelaah sumber lokal tanpa mengubahnya:

```powershell
$sandzhInspector = Join-Path $env:USERPROFILE '.claude\skills\sandzh-video-editor\scripts\inspect_reference.py'
python $sandzhInspector "D:\AEP SANDZH\AMVS\Violet - Stay.mp4" --out-dir work/violet --start 8 --span 1.2 --frames 9
python $sandzhInspector "D:\PR Project\Bandros.prproj" --out-dir work/bandros
```

Jalankan dari workspace tugas agar hasil masuk ke `work/`. Jika skill dipasang
di lokasi lain, sesuaikan path skrip relatif terhadap `SKILL.md`. Skrip memerlukan
Python dan FFmpeg/FFprobe untuk video; Pillow hanya untuk contact sheet gabungan.
Jika Pillow tidak tersedia, frame individual tetap dihasilkan. Pemeriksaan
`.prproj` hanya menggunakan pustaka standar Python.

## Bentuk hasil

- Jika diminta mengedit: kerjakan hasil yang dapat diperiksa dengan alat yang
  tersedia; sebutkan path proyek/render dan keterbatasan yang benar-benar ada.
- Jika diminta rencana: berikan timeline ringkas berisi rentang waktu, shot,
  tujuan cut, motion/teks, dan audio. Jangan mengaku telah merender.
- Jika diminta review: tunjukkan timestamp, masalah yang terlihat/terdengar,
  lalu perubahan konkret yang mendekatkannya ke profil terpilih.

Adobe Premiere dan After Effects adalah alur yang teramati, bukan keharusan
untuk semua tugas. Gunakan editor atau renderer pilihan pengguna. Padanan efek
boleh memakai alat native; jangan menyatakan hasil identik tanpa perbandingan.
Pertahankan sumber dan buat versi kerja/render yang jelas. Nama `Final`, `CC`,
`WM`, atau `RSMB` membantu pencarian, tetapi tidak menentukan kualitas atau
kelayakan publikasi tanpa pemeriksaan visual.
