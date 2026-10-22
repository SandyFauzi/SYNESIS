# Indeks korpus Sandzh

Pemeriksaan 21 Oktober 2026. Indeks lengkap yang dapat dicari: [korpus.json](korpus.json).

| Akar sumber | File | Video dengan metadata | Proyek utama Premiere |
|---|---:|---:|---:|
| `D:\AEP SANDZH\AMVS` | 472 | 333 | 0 |
| `D:\PR Project` | 99 | 41 | 38 |
| `S:\Video Convert` | 63 | 27 | 0 |

Tidak ada folder sumber yang dipindahkan atau disusun ulang. Segmentasi ini berada
di dalam profil skill dan indeks sampel. File yang belum ditinjau visual tetap
berkategori `null`; nama file saja tidak dianggap verifikasi gaya.

## Segmentasi sampel

| Kategori terverifikasi dari sampel | Video |
|---|---:|
| amv-emosional | 7 |
| amv-action | 6 |
| mmv | 2 |
| gmv | 2 |
| cinematic-teaser | 2 |
| aftermovie-event | 5 |
| promosi-sosial | 5 |
| motion-branding | 5 |
| tutorial-praktikum | 5 |
| edukasi-sains | 5 |
| asset-raw-presenter | 2 |
| asset-event-footage | 1 |
| asset-simulation | 1 |

44 dari 48 sampel adalah hasil edit/template; empat lainnya dipisahkan sebagai
rekaman mentah atau aset simulasi. Ini jumlah file sampel, bukan jumlah karya unik.
Pasangan versi dan part kolaborasi dapat berasal dari karya yang sama.

## Cara menelusuri bukti

Cari nama referensi dalam `sampled_videos` untuk kategori, timestamp, sheet, dan
nomor baris. `files` menyimpan daftar 634 file beserta metadata yang tersedia.
`premiere_projects` menyimpan sequence, komponen efek/bypass, dan path media.
`temporal_checks` menyimpan deteksi perubahan visual pada delapan video:
threshold 0.30, frame dikecilkan ke lebar 240, maksimal 140 detik pertama.
Hasil nol tidak membuktikan video tanpa cut; perubahan cahaya/blur dapat menambah
hitungan. Data ini bukan profil tempo atau bukti sinkronisasi musik.

## Contact sheet

Enam sheet pertama mempertahankan kelompok sampling awal. Kelompok itu bukan
segmentasi final: misalnya `Final Osjur` adalah promo, sedangkan `Porska`/`PPF`
adalah bumper. Kategori final ada di tabel dan JSON. Timestamp dalam gambar
dibulatkan; angka terstruktur di JSON menjadi acuan yang lebih tepat.

- [00-amv-emotional](sheets/00-amv-emotional.jpg)
- [01-amv-action-mmv-gmv](sheets/01-amv-action-mmv-gmv.jpg)
- [02-live-event](sheets/02-live-event.jpg)
- [03-motion-promo](sheets/03-motion-promo.jpg)
- [04-premiere-education-promo](sheets/04-premiere-education-promo.jpg)
- [05-mixed-provenance](sheets/05-mixed-provenance.jpg)
- [06-temporal-strips](sheets/06-temporal-strips.jpg)

## Contoh pemakaian skill

- “Buat AMV Violet yang emosional ala Sandzh.” → profil AMV emosional.
- “Edit gameplay MLBB untuk ulang tahun.” → GMV; periksa gameplay dan fungsi teks.
- “Buat bumper konferensi.” → motion branding; mulai dari identitas acara.
- “Rapikan video penjelasan ADC.” → tutorial/praktikum atau edukasi, sesuai isinya.
- “Tiru gaya podcast saya.” → bukti awal hanya proyek; periksa render spesifik
  sebelum menyatakan ciri visual/audio podcast.
