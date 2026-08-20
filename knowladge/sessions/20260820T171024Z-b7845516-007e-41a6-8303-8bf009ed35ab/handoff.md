# Handoff

Sesi ini berjalan di Claude Code, bukan Codex. Transkripnya dikonversi ke skema
JSONL yang sama supaya arsip `knowladge/sessions` bisa dibaca dua arah.

## Goal

Membangun SYNESIS, asisten AI personal yang jalan penuh lokal tanpa API dan
tanpa biaya, sambil belajar machine learning dari nol.

Dua jadwal yang terpisah. Enam bulan (Agustus 2026 sampai Februari 2027) untuk
memahami fondasi, berjalan beriringan dengan Semester 5 Fisika UNPAD. Produk
akhirnya sendiri tanpa tenggat.

Peran yang diminta pemilik: guru atau dosen pembimbing, bukan pengganti kerja.
Tiap sesi dikirim sebagai scaffold berisi TODO plus berkas soal dengan petunjuk
bertingkat, lalu jawabannya diperiksa dan dikoreksi.

## Decisions and rationale

**Tulis sendiri dulu, baru pakai pustaka.** Tiap konsep dikerjakan dua kali.
Menulis MLP sendiri lalu melihat `nn.Linear` mengerjakan hal yang sama menghapus
rasa gaibnya. Urutan terbalik justru mengabadikannya.

**Tidak ada LLM sampai Modul 6.** Perintah harian ke asisten ragamnya sedikit,
sekitar tiga puluh jenis. Intent classifier kecil menanganinya di bawah 10
milidetik dan hasilnya bisa diramalkan. LLM cuma untuk permintaan terbuka.

**Kode di S:, pustaka besar di E:.** Pemilik tidak mau SSD C dipakai menyimpan
pustaka atau model di atas 1 GB. venv ada di `E:\SYNESIS\.venv`, di luar repo,
jadi aktivasi lewat `scripts/activate.ps1`. Kalau enclosure E tidak terpasang,
tidak ada yang jalan.

**Cache TMP tetap di C.** Keputusan pemilik, karena bisa dihapus kapan saja.

**Roadmap diakselerasi.** Hari 5 sampai 16 dipadatkan jadi Sesi A sampai D
karena pemilik fast learner dengan 5 tahun pengalaman C dan Python. Sesi B
ditandai tidak boleh dipadatkan lagi, karena hasilnya gambaran di kepala, bukan
pengetahuan.

**Setiap proses yang selesai wajib dicatat di `log.md`,** termasuk kesalahan.

**Data pribadi.** PDF resmi kampus (KPA dan KRS) tetap di-gitignore. NPM dan
nilai huruf dalam bentuk teks boleh terbit, keputusan pemilik setelah risikonya
dilaporkan.

## Current state

Repo publik `https://github.com/SandyFauzi/SYNESIS` sudah terisi, branch `main`.

Struktur: `README.md` dan `log.md` di akar, `docs/` untuk Roadmap, Silabus,
Modul.md beserta Modul.pdf, Bulan-0-Harian, dan Name. `notebooks/` datar berisi
pasangan scaffold `.py` dan soal `.md`. `scripts/` untuk activate, verify, dan
progress. `figures/` dan `docs/akademik/` di-gitignore.

Bulan 0 sudah sampai Sesi C.

| Sesi | Isi | Status |
|---|---|---|
| Hari 2 | numpy, dot dan matmul manual lawan BLAS | selesai |
| Hari 3 | data sintetis, MSE dan MAE, irisan permukaan loss | selesai |
| Sesi A | gradien analitik, beda hingga, training loop | selesai, sudah diperiksa |
| Sesi B | permukaan 3D, lintasan, sumbu utama, animasi | selesai, sudah diperiksa |
| Sesi C | bentuk matriks, overfitting, regularisasi L2 | soal terkirim, jawaban sedang diisi |
| Sesi D | sklearn, PyTorch, `backward()`, CPU lawan GPU | belum dibuat |

Angka penting yang sudah terverifikasi dan dipakai sebagai kunci jawaban:

- Gradient descent konvergen ke `w = 3.018114`, `b = 1.743558`, bukan ke
  parameter asli `w = 3`, `b = 2`. Cocok dengan `lstsq` sampai `0.00e+00`.
- Batas learning rate terukur antara `0.127` dan `0.1272`. Ramalan Hessian
  `2/lambda_max = 0.12720` meleset di bawah 0,2 persen.
- Di `lr = 0.1272` persis, sistem berayun tetap, bukan konvergen, karena faktor
  pengali galat bernilai tepat minus satu.
- Bilangan kondisi Hessian Sesi B `8.0065`. Setelah fitur dibakukan jadi `1.000`.
- Regresi polinomial derajat 14 pada 15 titik memberi train loss nol dan test
  loss `5.7e9`. Dengan `lambda = 0.1` test loss turun jadi `5.42`.
- Beda pusat persis untuk MSE karena turunan ketiga polinomial derajat dua nol,
  jadi `h = 0.1` mengalahkan `h = 1e-11`.

## Important files and commands

```powershell
. .\scripts\activate.ps1              # venv ada di E:\SYNESIS\.venv
python scripts\verify.py              # audit lingkungan, jalankan tiap akhir bulan
python notebooks\sesiC_multivariat.py # sesi terakhir yang aktif
```

Dokumen: `docs/Silabus.md` untuk urutan dan tolok ukur, `docs/Roadmap.md` untuk
rencana besar, `docs/Modul.md` untuk penjelasan konsep, `log.md` untuk riwayat
kerja termasuk kesalahan.

Perangkat: Ryzen 5 4600H, RAM 15,4 GB, GTX 1650 Ti 4 GB dengan sekitar 979 MB
terpakai saat idle.

## Open items and risks

**Pola berulang pada jawaban pemilik.** Dua kali menulis kesimpulan yang
dibantah oleh tabel yang dicetak sendiri. Di Sesi A memakai nilai populasi
`25/3` di tempat yang meminta nilai sampel `7.8435`. Di Sesi B menyebut lintasan
menggergaji sebagai paling lambat, padahal terukur 38 iterasi lawan 185. Ini
sudah dijadikan Soal 0 di sesi berikutnya. Terus periksa pola ini.

**Bug escape berulang.** Menulis berkas lewat string Python non-raw sudah tiga
kali merusak isi: `\text` dan `\frac` jadi tab dan form feed, `\a` jadi byte BEL
di README, `\s` jadi escape tak sah di verify.py. Selalu pindai karakter kontrol
setelah menulis berkas.

**Kredensial git dua akun.** Git Credential Manager menyimpan token akun
praktikum yang tidak punya izin tulis ke repo ini. Solusinya remote memakai
`https://SandyFauzi@github.com/...` supaya GCM mencari kredensial terkunci pada
username itu. Skrip szh-ex memakai URL tanpa username, jadi push-nya bisa kena
403 dan perlu penanganan terpisah.

**Berkas ABOUT ME belum diisi.** `~/.claude/ABOUT ME/teaching-profile.md` masih
kosong, jadi tiga skill pengajaran (revision-coach, lecture-builder,
lesson-plan-designer) akan berhenti di Step 0.

**Sisa pip temp di C.** Sekitar 1,78 GB, perlu dihapus manual dengan
`Remove-Item "$env:TEMP\pip-*" -Recurse -Force`.

**Figures tidak masuk git.** Plot overfitting empat panel dan animasi lintasan
justru bagian paling menjelaskan untuk repo portofolio. Belum diputuskan apakah
sebagian akan dilepas dari saringan.

**Bicara dengan dosen.** Modul proyek ini kandidat kuat untuk tugas besar
Machine Learning dan DSP. Perlu dibicarakan di pekan pertama kuliah, sebelum
topik tugas dikunci.

## Suggested next prompt

Periksa jawaban Sesi C saya di `notebooks/soal-sesiC.md`, lalu buat Sesi D
sebagai penutup Bulan 0. Isinya membandingkan hasil tulisan tangan dengan
`LinearRegression` dan `Ridge`, menulis ulang dengan `torch.tensor` dan
`requires_grad=True`, mencocokkan `loss.backward()` dengan gradien tangan dalam
`1e-6`, lalu mengukur CPU lawan GPU untuk `d=10` dan `d=1000`.

Ikuti pola yang sudah berjalan: scaffold berisi TODO, berkas soal dengan
petunjuk bertingkat di blok `<details>`, semua angka kunci diverifikasi lebih
dulu dengan implementasi pembanding, lalu catat di `log.md` dan commit.
