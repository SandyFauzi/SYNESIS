# Soal Bulan 2 Sesi 4 - SYNESIS v0.1, dan ongkos salah tebak

Berkas latihan: [`bulan2_sesi4_synesis.py`](bulan2_sesi4_synesis.py)

Tujuh TODO. Sesi ini mengubah pengklasifikasi jadi sesuatu yang bertindak, dan
karena itu mengubah ukuran keberhasilannya dari akurasi jadi ongkos.

> Prasyarat: Sesi 1 sampai 3 dikerjakan, dan `data/bulan2/model_intent.npz`
> sudah ada. Kalau belum: `python scripts\latih_bulan2.py`.

> Berkas ini mengimpor `synesis.alat`, jadi ia benar-benar bisa memanggil
> shell. Mode kering adalah bawaannya, dan Soal 7 membahas kenapa bawaan itu
> bukan kesopanan melainkan syarat.

---

## Soal 1 - Kelas risiko, dan angka yang bergerak karenanya

Bagian 1 memberi:

```text
BACA         3     7.3%
TULIS        0     0.0%
MERUSAK      2     4.9%
BAHASA      36    87.8%
```

**1a.** Sesi 3 melaporkan 6 dari 41 pesan punya alat; Sesi 4 melaporkan 5.
Telusuri bedanya sampai ke intent mana yang berpindah kelas, lalu putuskan
penilaian mana yang benar dan pertahankan alasannya.

> **Jawaban:** Yang berpindah **satu intent: `ringkas_catatan`**.
>
> `PUNYA_ALAT` di Sesi 3 memuat sepuluh intent, termasuk `ringkas_catatan` dan
> `jadwal`. Tabel `RUTE` di Sesi 4 menaruh `jadwal` di TULIS, jadi ia tetap
> terhitung bisa dikerjakan; tapi `ringkas_catatan` dipindah ke BAHASA. Di
> ke-41 pesan, `ringkas_catatan` muncul tepat sekali:
>
> ```
> BACA         3     7.3%     (info_sistem 3)
> TULIS        0     0.0%
> MERUSAK      2     4.9%     (pasang_paket 2)
> BAHASA      36    87.8%     (termasuk ringkas_catatan 1)
> ```
>
> $3+0+2=5$, dan Sesi 3 menghitung $5+1=6$. Seluruh selisihnya satu pesan
> berlabel `ringkas_catatan`.
>
> **Penilaian yang benar: Sesi 4.** Alasannya harus berupa kriteria yang bisa
> diperiksa, bukan selera: sebuah intent disebut "punya alat" kalau ada entri
> di `alat.DAFTAR` yang mengerjakannya. `DAFTAR` berisi `baca_berkas`,
> `daftar_berkas`, `cari_berkas`, `cari_isi`, `info_sistem`, `jalankan`. Tidak
> ada `ringkas`. Meringkas catatan berarti membaca teks lalu memampatkan
> maknanya, dan itu justru definisi pekerjaan model bahasa; menyebutnya "punya
> alat" berarti menghitung alat yang saya bayangkan, bukan alat yang ada.
>
> Sesi 3 memakai kriteria yang lebih longgar — "atau bisa dibuatkan alat tanpa
> model bahasa" — dan kriteria yang memuat kata "bisa" akan selalu menghasilkan
> angka yang lebih besar, karena batasnya imajinasi saya.
>
> Catatan yang mengurangi arti kedua angka sekaligus: 6 lawan 5 dari 41 itu
> selisih 2,4 poin persen, sementara selang 95 persen di $n=41$ selebar sekitar
> 30 poin. Perdebatan taksonomi ini bergerak jauh di dalam derau. Yang penting
> bukan mana yang lebih besar, melainkan bahwa keduanya jauh di bawah 80
> persen.

**1b.** Kamu baru saja melihat angka utama bergerak karena satu keputusan
taksonomi, tanpa satu baris kode berubah. Sebutkan aturan yang akan kamu
pakai supaya ini tidak jadi cara diam-diam memperbaiki angka laporan.

> **Jawaban:** Tiga aturan, dan yang ketiga yang benar-benar mengikat.
>
> 1. **Kriterianya harus mekanis, bukan penilaian.** "Ada entri di
>    `alat.DAFTAR` yang namanya dipetakan `RUTE`" bisa diperiksa program;
>    "bisa dibuatkan alat tanpa LLM" tidak bisa. Kriteria yang butuh selera
>    akan selalu bergerak ke arah yang menguntungkan.
> 2. **Taksonomi dibekukan sebelum pengukuran dijalankan, bukan sesudah
>    melihat angkanya.** Kalau `RUTE` berubah, perubahannya di-commit
>    tersendiri, dengan tanggal dan alasan, sebelum pengukuran mana pun
>    memakainya.
> 3. **Selama satu taksonomi belum diterima, angka utamanya dilaporkan
>    berpasangan.** Bukan "5 dari 41" melainkan "5 dari 41 menurut RUTE
>    commit `<sha>`; 6 dari 41 menurut PUNYA_ALAT Sesi 3". Aturan ini yang
>    paling mengikat karena ia menghapus keuntungannya: kalau kedua angka
>    tetap terbit berdampingan, mengubah taksonomi tidak lagi memperbaiki
>    laporan, jadi tidak ada gunanya melakukannya diam-diam.
>
> Dan satu kebiasaan yang lebih murah daripada ketiganya: catat pergeserannya
> di `log.md` pada hari ia terjadi. Yang membuat perubahan diam-diam mungkin
> bukan niat buruk, melainkan lupa.

**1c.** Tiga intent memetakan ke alat `jalankan`, yaitu shell. Sebutkan
kenapa memetakan tiga intent berbeda ke satu alat berbahaya itu keputusan
yang lebih buruk daripada kelihatannya, dan usulkan gantinya.

> **Jawaban:** Ketiganya `kelola_repo` (TULIS), `jalankan_program` (MERUSAK),
> `kontrol_sistem` (MERUSAK). Tiga alasan kenapa lebih buruk daripada
> kelihatannya, diurut dari yang paling sering diabaikan:
>
> 1. **Kelas risiko menempel di intent, tapi kerusakan dikerjakan alat.**
>    `kelola_repo` dapat ambang TULIS 0,950 karena "git itu bisa dibatalkan".
>    Tapi begitu masuk ke `jalankan`, `git status` dan `rm -rf` adalah
>    pemanggilan yang sama dengan argumen berbeda. Radius ledaknya MERUSAK,
>    ambangnya TULIS. Yang menahan cuma tebakan intent yang tepat, dan
>    tebakan itu 56 persen benar.
> 2. **Salah tebak DI ANTARA ketiganya tidak terlihat oleh lapisan mana pun
>    sesudahnya.** Nama alatnya sama, bentuk argumennya sama, gerbang izinnya
>    sama. Tidak ada satu pun pemeriksaan hilir yang bisa membedakan
>    `kelola_repo` yang salah jadi `kontrol_sistem`.
> 3. **Barisan auditnya mencatat intent, bukan akibat.** Sesudah kejadian,
>    `audit.jsonl` memberi tahu saya intent apa yang model kira, bukan
>    perintah apa yang benar-benar jalan. Untuk sebuah alat shell, itu
>    catatan yang salah medannya.
>
> **Gantinya: buang shell bebas dari perutean intent seluruhnya, dan beri tiap
> intent alat sempit dengan daftar perintah yang diizinkan.**
>
> ```
> kelola_repo      -> git_status, git_diff, git_commit   argumen: pesan commit
> pasang_paket     -> pasang_paket                        argumen: nama paket, dicocokkan ^[A-Za-z0-9._-]+$
> kontrol_sistem   -> (belum ada; jangan dipetakan sampai alatnya sempit)
> jalankan_program -> (belum ada; sama)
> ```
>
> `jalankan` yang bebas tetap ada di `alat.DAFTAR`, tapi tidak lagi jadi
> tujuan intent mana pun. Ia cuma bisa dicapai lewat pintu darurat yang
> selalu bertanya, dan yang mencatat perintah lengkapnya ke audit.
> Perbedaannya: sesudah ini, salah tebak intent membatasi kerusakan pada
> perintah-perintah yang alat itu memang boleh keluarkan.

**1d.** `hitung` diberi kelas BACA padahal alatnya belum ada. Kalau kamu
membuatkan alatnya nanti, apakah kelasnya tetap BACA? Jawab dengan menyebut
implementasi apa yang membuatnya tetap BACA dan implementasi apa yang
menaikkannya jadi MERUSAK.

> **Jawaban:** **Tetap BACA kalau alatnya penilai aritmetika terbatas.**
> Naik jadi **MERUSAK kalau alatnya `eval`.**
>
> Implementasi yang membuatnya tetap BACA:
>
> ```python
> import ast, operator
> BOLEH = {ast.Expression, ast.BinOp, ast.UnaryOp, ast.Constant,
>          ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
>          ast.Mod, ast.Pow, ast.USub, ast.UAdd}
>
> def hitung(teks):
>     pohon = ast.parse(teks, mode="eval")
>     for simpul in ast.walk(pohon):
>         if type(simpul) not in BOLEH:
>             raise ValueError(f"simpul tidak diizinkan: {type(simpul).__name__}")
>         if isinstance(simpul, ast.Constant) and not isinstance(simpul.value, (int, float)):
>             raise ValueError("cuma angka")
>     ...
> ```
>
> Yang membuatnya BACA bukan bahwa ia memakai `ast`, melainkan bahwa daftar
> simpulnya **daftar putih**. Tidak ada `ast.Call`, jadi tidak ada pemanggilan
> fungsi. Tidak ada `ast.Name` dan `ast.Attribute`, jadi tidak ada cara
> menyentuh apa pun di luar ungkapan itu sendiri. Ia tidak bisa menyentuh
> disk, jaringan, maupun proses.
>
> Implementasi yang menaikkannya jadi MERUSAK, dan panjangnya satu baris:
>
> ```python
> def hitung(teks):
>     return eval(teks)
> ```
>
> Cara tersingkat menghitung `12 * (3 + 4)` di Python memang itu, dan itu
> juga alasan kategori kerentanan bernama eksekusi kode jarak jauh ada.
> `eval("__import__('os').system('...')")` adalah shell, dipanggil dari
> intent yang tabel `RUTE` beri label BACA dan ambang 0,500. Dengan kata
> lain: satu keputusan implementasi bisa menaikkan kelas risiko dua tingkat
> **tanpa mengubah satu baris pun di `RUTE`**, dan tabel risikonya tidak akan
> tahu.
>
> Satu bahaya ketiga yang tetap ada bahkan di versi daftar putih: `2 ** 10**9`
> menggantung prosesnya dan memakan memori sampai habis. Itu bukan MERUSAK,
> tapi ia penolakan layanan terhadap diri sendiri. Jadi batasi eksponen, dan
> panjang masukannya.
>
> Kesimpulan yang lebih umum, dan ini yang layak dibawa: **kelas risiko adalah
> sifat implementasi alat, bukan sifat intent.** `RUTE` menyimpannya di kolom
> intent karena itu yang paling mudah dibaca manusia, dan itu utang yang harus
> ditulis di suatu tempat sebelum ia menagih.

<details>
<summary>Petunjuk 1d</summary>

Cara paling singkat menghitung "12 * (3 + 4)" di Python cuma satu baris, dan
baris itu adalah alasan kenapa ada kategori kerentanan bernama eksekusi kode
jarak jauh.

</details>

---

## Soal 2 - Ambang yang diturunkan

**2a.** Turunkan `ambang_dari_ongkos` di atas kertas. Mulai dari
$c_\text{salah}(1-p) < c_\text{tolak}$, selesaikan untuk $p$, dan nyatakan
hasilnya sebagai $p > 1 - c_\text{tolak}/c_\text{salah}$.

> **Jawaban:** Dua pilihan, dua ongkos harapan. Model memberi peluang $p$ untuk
> kelas $k$.
>
> $$\text{ongkos bertindak}=c_\text{salah}\cdot(1-p)+0\cdot p,\qquad
> \text{ongkos menolak}=c_\text{tolak}.$$
>
> Baris pertama nilai harapan: dengan peluang $p$ tindakannya benar dan
> ongkosnya nol, dengan peluang $1-p$ salah dan ongkosnya penuh.
>
> Bertindak layak hanya kalau lebih murah:
>
> $$c_\text{salah}(1-p)<c_\text{tolak}.$$
>
> Bagi kedua ruas dengan $c_\text{salah}$. Karena $c_\text{salah}>0$, arah
> pertidaksamaannya tidak berbalik:
>
> $$1-p<\frac{c_\text{tolak}}{c_\text{salah}}
> \;\Longrightarrow\;
> -p<\frac{c_\text{tolak}}{c_\text{salah}}-1
> \;\Longrightarrow\;
> \boxed{\;p>1-\frac{c_\text{tolak}}{c_\text{salah}}\;}$$
>
> Kalikan $-1$ di langkah terakhir, dan di situ arahnya berbalik.
>
> Dua kasus tepinya jatuh sendiri dari rumusnya. Kalau
> $c_\text{tolak}>c_\text{salah}$ hasilnya negatif, dan ambang negatif berarti
> "selalu bertindak", yang memang benar: kalau bertanya lebih mahal daripada
> salah, jangan bertanya. Kalau $c_\text{tolak}=0$ hasilnya 1, yaitu "tidak
> pernah bertindak", yang juga benar: kalau bertanya gratis, selalu bertanya.
> Keduanya dipotong ke $[0,1]$ di kodenya, bukan dilempar sebagai galat.

**2b.** Tabel Bagian 2 menunjukkan selisih ambang tangan lawan ambang ongkos
untuk lima belas intent. Hitung berapa yang positif dan berapa yang negatif,
lalu sebutkan kesalahan sistematis apa yang kamu buat waktu menyetel dengan
tangan di Sesi 2.

> **Jawaban:** Terukur (Uji I): **11 positif, 3 negatif, 1 nol.**
>
> ```
> terbesar positif: obrol +0.367, tanya_umum +0.367, jelaskan_konsep +0.267
> terbesar negatif: ubah_proyek -0.183, hitung -0.100, buka_berkas -0.050
> nol             : info_sistem (0.500 lawan 0.500, kebetulan)
> ```
>
> **Kesalahan sistematisnya: saya menyetel ambang dengan tangan menurut
> seberapa RUMIT intent itu terasa, bukan menurut seberapa mahal salahnya.**
> Sebelas dari lima belas terlalu longgar, jadi ini bukan derau melainkan
> kemiringan berarah.
>
> Polanya terbaca kalau tabelnya dikelompokkan per kelas risiko:
>
> - **BACA** (4 intent): $-0{,}050, +0{,}100, -0{,}100, 0{,}000$. Rerata
>   praktis nol. Di sinilah tangan saya terkalibrasi, dan sebabnya jelas:
>   inilah intent yang saya bayangkan sedang saya pakai waktu menyetelnya.
> - **TULIS dan MERUSAK** (5 intent): semuanya positif, $+0{,}050$ sampai
>   $+0{,}145$. Saya sudah tahu ini berbahaya dan menaikkan ambangnya ke 0,85
>   sampai 0,90 — dan itu masih kurang. Model ongkos menuntut 0,950 dan 0,995.
>   Saya menyetelnya tinggi, tapi saya tidak menyetelnya sesuai ongkos, karena
>   0,90 terasa seperti angka yang tinggi sementara $1-1/200=0{,}995$ adalah
>   angka yang tinggi.
> - **BAHASA** (6 intent): lima positif, satu negatif besar. `obrol` dan
>   `tanya_umum` saya beri 0,30 karena "salah tebak obrol kan cuma ngobrol".
>   Model ongkos memberi 0,667, karena BAHASA berarti tidak ada alatnya dan
>   bertindak berarti menjawab dengan percaya diri untuk permintaan yang
>   sebenarnya belum bisa dilayani.
>
> Jadi kesalahannya bukan "terlalu longgar" saja. Kesalahannya saya memakai
> sumbu yang salah: kerumitan intent, bukan ongkos salah. Kedua sumbu itu
> kebetulan sejajar untuk BACA, dan itulah kenapa saya tidak menyadarinya.

**2c.** Selisih terbesar ada di `obrol` dan `tanya_umum`, keduanya sekitar
+0,37. Hubungkan dengan kesimpulan yang kamu tulis sendiri di Soal 8c Sesi 2,
bahwa ambang ongkos bukan pendeteksi kalimat asing. Apakah ambang ongkos
memperbaiki masalah itu, atau cuma menutupinya?

> **Jawaban:** Kesimpulan Soal 8c Sesi 2 saya sendiri: dari lima kalimat yang
> berada di luar seluruh taksonomi intent, ambang global 0,50 menangkap empat,
> ambang per intent cuma dua. Keyakinan softmax bukan pendeteksi kalimat asing.
>
> **Ambang ongkos menutupinya, tidak memperbaikinya.**
>
> Alasannya struktural. Ambang ongkos menaikkan bar `obrol` dari 0,30 ke
> 0,667, jadi lebih banyak kalimat asing tertolak. Tapi ia **tidak menambah
> satu bit informasi pun** tentang apakah kalimatnya di dalam ranah. Ia cuma
> membuat model lebih sering menolak, untuk semua kalimat sekaligus. Kalimat
> asing yang kebetulan mencetak 0,70 untuk `obrol` tetap lolos, dan tidak ada
> apa pun di dalam pipa yang tahu bedanya.
>
> Buktinya ada di pengukuran saya sendiri. Terukur (Uji I), pesan
> `bagian abcd itu apa saja tadi??` — kalimat yang **jelas di dalam ranah**,
> label benarnya `jelaskan_konsep` — ditolak dengan keyakinan 0,461. Sementara
> Soal 2c Sesi 3 mengukur bahwa kalimat bervektor nol, yang **sepenuhnya di
> luar ranah**, keluar dengan keyakinan 0,397. Selisih keduanya 0,064, dan
> ambang mana pun yang menolak yang kedua juga menolak yang pertama. Ambang
> memperlakukan "asing" dan "meragukan" sebagai hal yang sama, karena dari
> sudut pandangnya keduanya memang satu angka yang sama.
>
> **Yang sebenarnya memperbaikinya adalah sinyal dari luar softmax.** Tiga
> yang tersedia tanpa melatih apa pun:
>
> 1. **Porsi kata di luar kosakata.** Sudah terukur: 51,1 persen token pesan
>    nyata tidak punya kolom, dan 2 kalimat vektornya nol utuh. Yang terakhir
>    bisa ditolak dengan kepastian penuh, tanpa memanggil model. Sudah
>    dipasang sebagai `tolak_kosong` di `synesis/niat.py` (Soal 2d Sesi 3).
> 2. **Logit maksimum, bukan peluang ternormalkan.** Softmax membagi habis
>    peluang ke kelas yang ADA, jadi ia tidak punya cara menyatakan "bukan
>    salah satu dari ini". Besaran logit sebelum normalisasi masih memuat
>    sebagian informasi itu.
> 3. **Kelas "bukan apa-apa" yang dilatih dari teks di luar ranah.** Ini yang
>    paling benar dan paling mahal, karena butuh contoh negatif yang mewakili,
>    dan itu kembali ke `audit.jsonl`.

**2d.** Satu intent punya selisih negatif besar. Cari yang mana, lalu
putuskan apakah ambang tangan atau ambang ongkos yang lebih benar untuk intent
itu. Kalau menurutmu ambang tangan yang benar, berarti ada sesuatu yang tidak
tertangkap model ongkosnya. Sebutkan apa.

> **Jawaban:** Yang selisihnya negatif besar: **`ubah_proyek`, $-0{,}183$**
> (ambang tangan 0,850, ambang ongkos 0,667).
>
> **Ambang tangan yang lebih benar untuk intent ini**, dan yang tidak
> tertangkap model ongkosnya adalah **peluang awal kelasnya**.
>
> `ubah_proyek` bukan sembarang kelas BAHASA. Terukur, ia kelas terbesar di
> data nyata: 16 dari 41 pesan, 39,0 persen, dan ia dasar mayoritas yang
> dipakai seluruh Sesi 3 sebagai pembanding. Kelas yang menyerap 39 persen lalu
> lintas adalah tempat model membuang segala yang tidak ia pahami. Bertindak
> atasnya berarti menjawab "saya mengerti, kamu mau mengubah proyeknya"
> untuk kalimat yang sebenarnya tidak dimengerti sama sekali.
>
> Model ongkos memberi satu angka per KELAS RISIKO. Ia karena itu memberi
> `ubah_proyek` dan `obrol` ongkos salah yang sama, 3,0, padahal salah tebak
> `ubah_proyek` berarti mengaku paham sebuah instruksi proyek sementara salah
> tebak `obrol` berarti salah membalas basa-basi. Yang hilang: **suku ongkos
> yang bergantung pada peluang awal kelas, bukan pada kelas risikonya.**
>
> Bentuk perbaikannya, tanpa membongkar modelnya: kalikan $c_\text{salah}$
> dengan faktor yang naik bersama porsi kelas itu di data, misalnya
> $c_\text{salah}\cdot(1+\pi_k)$ dengan $\pi_k$ porsi kelas $k$. Untuk
> `ubah_proyek` itu memberi $3{,}0\times 1{,}39=4{,}17$ dan ambang
> $1-1/4{,}17=0{,}760$, mendekat ke 0,850 yang saya setel dengan tangan. Tapi
> $\pi_k$ diukur dari 41 pesan yang sama yang dipakai menguji, jadi
> memasangnya sekarang berarti membocorkan himpunan uji ke dalam kebijakan.
> Ditulis sebagai rencana, tidak dipasang, sampai `audit.jsonl` cukup panjang
> untuk memberi $\pi_k$ dari sumber terpisah.
>
> Dua selisih negatif lainnya, `hitung` $-0{,}100$ dan `buka_berkas`
> $-0{,}050$, ada di dalam ketelitian sebuah setelan tangan dan tidak layak
> dipertahankan.

**2e.** Angka 200,0 untuk MERUSAK tidak diukur, cuma ditulis. Rancang cara
mengukurnya dari pengalamanmu sendiri, dengan satuan yang jelas. Lalu sebutkan
apakah tabel ambangnya akan banyak berubah kalau angkanya ternyata 50 atau
1000.

> **Jawaban:** **Cara mengukurnya, dengan satuan yang jelas.** Ongkos menolak
> punya satuan yang nyata dan bisa saya ukur langsung: waktu saya mengetik
> ulang perintahnya, kira-kira 10 detik. Jadikan itu satuan pokoknya, lalu
> ongkos salah diukur dalam satuan yang sama:
>
> $$c_\text{salah}[\text{MERUSAK}]=\frac{\text{median menit membereskan}\times 60}{10}.$$
>
> Datanya dikumpulkan, bukan dikira: tiap kali saya sendiri menyebabkan
> kejadian tak terbalikkan — `pip install` ke venv yang salah, `git reset
> --hard` yang keliru, berkas terhapus — catat menit dari "aduh" sampai
> kembali ke keadaan semula. Sepuluh kejadian sudah memberi median yang bisa
> dipakai. Angka 200 berarti saya mengklaim medannya 33 menit. Dari ingatan,
> itu tidak jauh; tapi ingatan persis yang sedang saya coba hindari.
>
> **Apakah tabelnya banyak berubah kalau ternyata 50 atau 1000?** Terukur
> (Uji K):
>
> ```
> keyakinan MERUSAK tertinggi di 41 pesan: 0.913
>
> ongkos     50 -> ambang 0.980 -> tetap ditolak
> ongkos    200 -> ambang 0.995 -> tetap ditolak
> ongkos   1000 -> ambang 0.999 -> tetap ditolak
> ```
>
> **Ambangnya bergerak sedikit, perilakunya tidak bergerak sama sekali.**
> Ambangnya cuma merentang 0,980 sampai 0,999, yaitu 1,9 poin, karena
> $1-1/c$ sudah hampir rata untuk $c$ sebesar itu. Dan keyakinan MERUSAK
> tertinggi yang pernah dicapai model di seluruh 41 pesan adalah 0,913, di
> bawah ketiganya. Jadi ketiga setelan itu menghasilkan keputusan yang identik
> untuk setiap pesan yang saya punya.
>
> Kesimpulan yang lebih berguna daripada "200 itu benar": untuk kelas risiko
> tertinggi, **nilai mutlaknya hampir tidak penting; yang penting rasionya
> terhadap kelas lain**, karena rasio itulah yang menentukan kelas mana yang
> dimenangkan `putuskan` waktu peluangnya berdekatan. Yang benar-benar harus
> saya ukur bukan 200, melainkan apakah MERUSAK sungguh seratus kali lebih
> mahal daripada BACA.

---

## Soal 3 - Akurasi dan ongkos memberi pemenang berbeda

Bagian 3 memberi:

```text
kebijakan                 benar  salah  tolak    ongkos   ongkos/pesan
argmax polos                 23     18      0     447.0          10.90
ambang tangan Sesi 2         15     10     16     242.0           5.90
ongkos harapan               15      7     19      39.0           0.95
```

**3a.** Urutkan barisnya menurut kolom benar, lalu menurut kolom ongkos.
Nyatakan apakah kedua urutan itu sama, dan apa artinya untuk laporan yang
cuma menyebut akurasi.

> **Jawaban:** Terukur:
>
> ```
> urut menurut BENAR (banyak ke sedikit)   urut menurut ONGKOS (murah ke mahal)
> 1  argmax polos          23              1  ongkos harapan          39.0
> 2  ambang tangan         15              2  ambang tangan          242.0
> 3  ongkos harapan        15              3  argmax polos           447.0
> ```
>
> **Kedua urutan itu berkebalikan persis.** Baris yang paling banyak benar
> adalah baris yang paling mahal, dengan selisih 11 kali lipat.
>
> **Artinya untuk laporan yang cuma menyebut akurasi:** laporan seperti itu
> akan merekomendasikan sistem yang terburuk. Bukan sistem yang agak kurang
> baik — sistem yang paling mahal dari ketiganya. Untuk pengklasifikasi yang
> cuma mengisi tabel, akurasi memang ukuran yang benar. Begitu keluarannya
> jadi tindakan, akurasi berhenti mengukur hal yang penting, karena ia
> memperlakukan salah membuka berkas dan salah menjalankan shell sebagai satu
> kesalahan yang sama.
>
> Kalimat yang harus dibawa keluar: 8 jawaban benar tambahan dibayar dengan
> 408 satuan ongkos. Itu bukan tukar-tambah yang buruk; itu tukar-tambah yang
> tidak akan pernah saya setujui kalau saya melihat kedua kolomnya.

**3b.** Baris kedua dan ketiga sama-sama benar 15 kali, tapi ongkosnya beda
enam kali lipat. Jelaskan dari mana selisih itu datang, dengan menyebut
kelas risiko yang terlibat.

> **Jawaban:** Terukur (Uji K), rincian ongkos salahnya:
>
> ```
> ambang tangan    salah: 1 x BACA (2), 8 x BAHASA (3), 1 x MERUSAK (200) = 226.0
>                  tolak: 16 x 1.0                                        =  16.0
>                                                                     total 242.0
>
> ongkos harapan   salah: 1 x BACA (2), 6 x BAHASA (3)                    =  20.0
>                  tolak: 19 x 1.0                                        =  19.0
>                                                                     total  39.0
> ```
>
> **Seluruh selisihnya satu tindakan.** Ambang tangan meloloskan satu tindakan
> MERUSAK yang salah, dan tindakan tunggal itu berharga 200,0 — lebih besar
> daripada seluruh ongkos kebijakan ongkos harapan digabung (39,0).
>
> Kelas risiko yang terlibat: **MERUSAK**. Ambang tangan untuk ketiga intent
> MERUSAK saya setel 0,85 sampai 0,90. Model ongkos menuntut 0,995. Satu pesan
> mendarat di antara keduanya, dan celah 0,095 poin itulah seluruh perbedaan
> antara 242 dan 39.
>
> Perhatikan juga bahwa kedua kebijakan sama-sama benar 15 kali. Kolom "benar"
> tidak menyimpan satu pun informasi tentang perbedaan yang paling penting di
> antara mereka.

**3c.** Baris pertama benar 23 kali, paling banyak dari ketiganya, dan paling
mahal. Hitung selisih ongkosnya terhadap baris ketiga, lalu nyatakan selisih
itu setara berapa tindakan MERUSAK yang salah. Bandingkan dengan 8 jawaban
benar tambahan yang jadi bayarannya.

> **Jawaban:** Selisih ongkosnya $447{,}0-39{,}0=\mathbf{408{,}0}$.
>
> Dalam satuan tindakan MERUSAK yang salah: $408{,}0/200{,}0=\mathbf{2{,}04}$
> tindakan MERUSAK yang salah.
>
> Bayarannya 8 jawaban benar tambahan (23 lawan 15). Jadi harga satu jawaban
> benar tambahan adalah $408/8=51$ satuan, yaitu **51 kali menolak dan
> bertanya**, atau **25 tindakan BACA yang salah**, atau **seperempat tindakan
> MERUSAK yang salah**.
>
> Terjemahan yang membuatnya terasa: untuk mendapat satu jawaban benar
> tambahan, saya bersedia meminta maaf pada diri sendiri 51 kali, atau
> membereskan seperempat kali kerusakan tak terbalikkan. Diucapkan begitu,
> tidak ada orang yang akan menyetujuinya. Yang membuatnya terlihat masuk akal
> cuma satu hal: kolom "benar" ditulis, dan kolom "ongkos" tidak.

**3d.** Kebijakan "selalu menolak" tidak ada di tabel. Hitung ongkosnya,
tambahkan sebagai baris keempat, lalu nyatakan apakah kebijakan ongkos
harapan mengalahkannya. Kalau tidak, itu temuan penting dan harus kamu
tuliskan apa adanya.

> **Jawaban:** Kebijakan "selalu menolak" tidak pernah bertindak, jadi tidak
> pernah salah, dan ongkosnya $41\times \text{ONGKOS\_TOLAK}=41{,}0$.
>
> Terukur (Uji H), tabel lengkap dengan baris keempatnya:
>
> ```
> kebijakan                 benar  salah  tolak    ongkos   ongkos/pesan
> argmax polos                 23     18      0     447.0          10.90
> ambang tangan Sesi 2         15     10     16     242.0           5.90
> ongkos harapan               15      7     19      39.0           0.95
> selalu menolak                0      0     41      41.0           1.00
> ```
>
> **Apakah kebijakan ongkos harapan mengalahkannya? Nyaris tidak.** 39,0 lawan
> 41,0. Selisihnya **2,0 satuan atas 41 pesan, yaitu 0,05 per pesan, yaitu 4,9
> persen.**
>
> Dan ini temuan penting, jadi ditulis apa adanya: **seluruh mesin Sesi 4 —
> lima belas ambang yang diturunkan, perbandingan ongkos semua kelas,
> ekstraksi slot, pagar jalur, gerbang izin, catatan audit — mengalahkan
> `return -1` sebanyak dua koma nol satuan.** Sebuah kebijakan yang bisa
> ditulis dalam satu baris dan tidak pernah menyalakan apa pun berada di dalam
> 5 persen dari kebijakan terbaik yang saya bangun.
>
> Sebabnya bukan kebijakannya, melainkan papan skornya. Model ongkos memberi
> 0 untuk tindakan yang benar. Melakukan hal yang benar tidak dihargai, cuma
> tidak dihukum. Sistem apa pun yang dinilai begitu akan menyimpulkan bahwa
> diam adalah strategi terbaik, **dan kesimpulan itu benar menurut aturannya
> sendiri**. Yang salah aturannya. Soal 3e memperbaikinya.

**3e.** Dari 3d, susun ulang tabel ongkos supaya kebijakan yang bertindak
punya peluang menang. Kamu boleh mengubah `ONGKOS_TOLAK`, `ONGKOS_SALAH`,
atau menambah ongkos untuk manfaat tindakan yang benar. Sebutkan mana yang
kamu pilih dan kenapa yang lain kamu tolak.

> **Jawaban:** **Yang saya pilih: menambahkan manfaat untuk tindakan yang
> benar.** `ONGKOS_TOLAK` dan `ONGKOS_SALAH` tidak diubah sama sekali.
>
> ```python
> MANFAAT_BENAR = -2.0     # satu tindakan benar setara dua kali tidak bertanya
> ```
>
> Ongkos harapan bertindak jadi $m\cdot p+c_\text{salah}(1-p)$, dan
> menurunkan ulang pertidaksamaan Soal 2a memberi
>
> $$p>\frac{c_\text{salah}-c_\text{tolak}}{c_\text{salah}-m},$$
>
> yang kembali jadi $1-c_\text{tolak}/c_\text{salah}$ persis waktu $m=0$.
>
> Terukur (Uji H):
>
> ```
> risiko      ambang lama  ambang baru
> BACA              0.500        0.250
> TULIS             0.950        0.864
> MERUSAK           0.995        0.985
> BAHASA            0.667        0.400
>
> kebijakan                 benar  salah  tolak    ongkos   ongkos/pesan
> argmax polos                 23     18      0     401.0           9.78
> ambang tangan Sesi 2         15     10     16     212.0           5.17
> ongkos + manfaat             19     11     11       5.0           0.12
> selalu menolak                0      0     41      41.0           1.00
> ```
>
> Kebijakan yang bertindak sekarang menang **delapan kali lipat** atas
> kebijakan diam (5,0 lawan 41,0), dan ia bertindak lebih sering: 19 benar
> lawan 15 sebelumnya. Yang perlu diperhatikan, dan ini yang meyakinkan saya
> bahwa perubahannya benar: **ambang MERUSAK nyaris tidak bergerak**, 0,995
> jadi 0,985. Manfaat sebesar 2,0 tidak berarti apa-apa dibandingkan ongkos
> 200,0, jadi kehati-hatian di tempat yang penting tetap utuh. Yang mencair
> adalah BACA dan BAHASA, tempat memang tidak ada yang perlu dijaga.
>
> **Kenapa dua pilihan lain saya tolak:**
>
> **Mengubah `ONGKOS_TOLAK`.** Menurunkannya membuat menolak lebih murah lagi,
> yaitu arah yang berlawanan dengan yang saya butuhkan. Menaikkannya memang
> memaksa bertindak, tapi ia memaksa bertindak **di semua kelas sekaligus**,
> termasuk MERUSAK — persis kegagalan yang seluruh rancangan ini ada untuk
> mencegahnya. Lagi pula `ONGKOS_TOLAK` adalah satu-satunya angka di tabel
> ini yang punya satuan yang bisa saya ukur langsung (sepuluh detik mengetik
> ulang). Ia jangkar, bukan tuas.
>
> **Mengubah `ONGKOS_SALAH`.** Menurunkannya supaya bertindak jadi menarik
> berarti membuang urutan antar kelas risiko, dan urutan itu satu-satunya
> bagian dari model ini yang saya yakini. Soal 2e sudah mengukur bahwa nilai
> mutlaknya hampir tidak berpengaruh sementara rasionya sangat berpengaruh;
> mengutak-atiknya berarti merusak bagian yang bekerja untuk memperbaiki
> bagian yang hilang.
>
> Yang hilang memang suku manfaatnya, dan menambahkannya adalah satu-satunya
> perubahan yang menyembuhkan kemerosotan "diam itu optimal" di sumbernya:
> papan skor yang memberi nilai 0 untuk hasil terbaiknya membuat tidak
> melakukan apa pun optimal menurut konstruksinya.

<details>
<summary>Petunjuk 3e</summary>

Model ongkos sekarang memberi 0 untuk tindakan benar. Artinya melakukan hal
yang benar tidak dihargai sama sekali, cuma tidak dihukum. Sistem apa pun
yang dinilai begitu akan menyimpulkan bahwa diam adalah strategi terbaik,
dan kesimpulan itu benar menurut aturannya sendiri.

</details>

---

## Soal 4 - Argumen yang tidak boleh ditebak

**4a.** `slot_ke_argumen` mengembalikan None kalau slot "objek" tidak ada,
walau intentnya sudah tertebak dengan keyakinan tinggi. Nyatakan kenapa
melanjutkan dengan argumen tebakan lebih berbahaya daripada salah tebak
intent.

> **Jawaban:** Karena **salah tebak intent masih akan ditangkap lapisan
> berikutnya, salah tebak argumen tidak akan ditangkap siapa pun.**
>
> Intent yang salah harus melewati kelas risikonya, ambang keyakinannya,
> gerbang izinnya, dan pagar alatnya sendiri. Empat lapisan, dan Bagian 5
> mengukur bahwa lapisan-lapisan itu memang menahan: 40 dari 41 pesan
> berhenti sebelum bertindak.
>
> Argumen yang salah melewati semuanya, karena setiap lapisan sesudah
> `slot_ke_argumen` memeriksa **bentuk** tindakannya, bukan apakah sasarannya
> yang saya maksud. `baca_berkas` dengan jalur tebakan adalah tindakan BACA
> yang sah, atas jalur yang sah, di dalam folder yang sah. `_aman`
> meloloskannya. Gerbang izin tidak dipanggil karena BACA. Barisan auditnya
> tercatat sebagai berhasil.
>
> Dan ada beda yang lebih tajam lagi soal apa yang saya lihat. Intent yang
> salah kelihatan salah — SYNESIS melakukan sesuatu yang jelas bukan
> permintaan saya, dan saya langsung tahu. Argumen yang salah kelihatan
> **berhasil**, dengan isi yang keliru. Kegagalan yang menyamar jadi
> keberhasilan adalah kegagalan yang tidak pernah saya perbaiki, karena saya
> tidak pernah tahu ia terjadi.
>
> Karena itu `None` adalah jawaban yang sah, dan sering benar.

**4b.** Untuk `cari_berkas`, objek yang tidak memuat `*` dibungkus jadi
`*objek*`. Jalankan `buka laporan praktikum minggu lalu` lewat
`ekstrak_slot`, lalu periksa apakah argumen yang keluar benar-benar berguna
sebagai pola nama berkas. Laporkan apa adanya.

> **Jawaban:** Terukur (Uji I):
>
> ```
> ekstrak_slot('buka laporan praktikum minggu lalu')
>   = {'waktu': -7, 'objek': 'laporan praktikum'}
>
> slot_ke_argumen('buka_berkas', ...) -> 'laporan praktikum'
> berkas yang cocok dengan pola itu di akar repo: 0
> ```
>
> **Argumennya tidak berguna sebagai pola nama berkas.** Dilaporkan apa adanya:
> ia frasa bahasa manusia, bukan pola. `baca_berkas` menyelesaikannya relatif
> terhadap direktori kerja, jadi ia jadi
> `S:\Code\Make A Jarvis\laporan praktikum`, dan tidak ada apa pun di situ.
>
> Diuji ujung ke ujung lewat mode percakapan sungguhan:
>
> ```
> python -m synesis.cli --sungguhan
>   kamu > buka laporan praktikum minggu lalu
>   intent  : buka_berkas  (yakin 0.951, risiko BACA)
>   tindakan: jalan
>     Tidak ada berkas di S:\Code\Make A Jarvis\laporan praktikum
> ```
>
> Tiga hal yang perlu dicatat dari baris itu. Keyakinannya 0,951, jadi
> ambangnya bukan yang menghalangi. Tindakannya `jalan`, jadi pipanya memang
> sampai memanggil alat. Dan slot `waktu` bernilai $-7$ berhasil diekstraksi,
> lalu dibuang tanpa dipakai — itu Soal 4d.

**4c.** Dari 4b: `ekstrak_slot` mengembalikan objek berupa frasa bahasa
manusia, sedangkan alat butuh pola nama berkas. Sebutkan langkah apa yang
hilang di antara keduanya, dan apakah langkah itu bisa ditulis dengan aturan
tangan atau butuh belajar.

> **Jawaban:** **Langkah yang hilang: penerjemah frasa jadi pola nama berkas,
> plus pemilih di antara hasil yang cocok.** Empat pekerjaan di dalamnya:
>
> 1. buang kata isian, ubah kata isi jadi pola: `laporan praktikum` jadi
>    `*lapor*prakt*` atau `*praktikum*`;
> 2. tentukan di mana mencari — `FOLDER_BOLEH`, bukan direktori kerja;
> 3. saring dengan waktu ubah berkas, memakai slot `waktu` yang sekarang
>    terbuang;
> 4. kalau lebih dari satu cocok, **bertanya**, jangan memilih. Soal 4a
>    sudah menjelaskan kenapa memilih di sini lebih berbahaya daripada
>    menyerah.
>
> **Bisa ditulis dengan aturan tangan? Sebagian besar ya, sebagian kecil
> tidak, dan garis pemisahnya jelas.**
>
> Bisa aturan tangan: butir 1 sampai 4 di atas, sekitar lima belas baris.
> Buang kata isian, ambil kata isi, sambung dengan bintang, `rglob` di
> `FOLDER_BOLEH`, urut menurut `st_mtime`. Itu menyelesaikan kasus yang nama
> berkasnya berbagi kata dengan cara saya menyebutnya, dan itu mayoritas
> kasus.
>
> Tidak bisa aturan tangan: waktu nama berkasnya **tidak berbagi satu kata pun**
> dengan cara saya menyebutnya. `laporan praktikum minggu lalu` yang
> sebenarnya menunjuk `LAPRAK_FISDAS_M3.docx` tidak bisa dijembatani aturan
> apa pun, karena tidak ada informasi yang menghubungkan keduanya di dalam
> kedua string itu. Yang bisa menjembataninya cuma dua: sebuah indeks isi
> berkas, atau catatan tentang berkas mana yang sebenarnya saya buka sesudah
> mengatakan itu.
>
> Yang kedua sudah ada bentuknya. `audit.jsonl` memuat kalimatnya; kalau ia
> juga memuat berkas yang akhirnya saya buka, tiap baris jadi satu pasangan
> (frasa, berkas). Beberapa ratus pasangan cukup untuk mempelajari pemetaan
> itu. Jadi urutannya: **aturan tangan sekarang, belajar kemudian, dan
> aturan tangan itu sendiri yang mengumpulkan data untuk belajarnya.**

**4d.** Slot "waktu" diekstrak tapi tidak dipakai sama sekali di
`slot_ke_argumen`. Rancang bagaimana ia dipakai untuk `cari_berkas`, dan
sebutkan alat baru apa yang perlu ditambahkan ke `synesis/alat.py`.

> **Jawaban:** **Rancangan pemakaian slot `waktu` untuk `cari_berkas`.**
>
> `ekstrak_slot` mengembalikan `waktu` sebagai geseran hari bertanda: $-7$
> untuk "minggu lalu", $-1$ untuk "kemarin", $+1$ untuk "besok". Untuk mencari
> berkas cuma geseran negatif dan nol yang punya arti — berkas tidak diubah di
> masa depan. Tafsirkan geseran $-d$ sebagai **jendela** $[\text{sekarang}-d\
> \text{hari},\ \text{sekarang}]$, bukan sebagai satu hari tertentu, karena
> "minggu lalu" dalam ucapan saya berarti "belakangan ini", bukan "tujuh hari
> yang lalu tepat".
>
> Lalu saring hasil `rglob` dengan `p.stat().st_mtime`, dan urutkan yang
> tersisa dari yang terbaru.
>
> **Alat baru yang perlu ditambahkan ke `synesis/alat.py`:** tidak ada alat
> baru. `cari_berkas` diperluas untuk menerima penyaring waktu, karena alat
> kedua berarti menyalin gelung `FOLDER_BOLEH` dan penyaring berkas
> tersembunyi ke dua tempat yang bisa berbeda diam-diam.
>
> Protokol alatnya satu string, jadi penyaringnya ditempel di ujung argumen
> dengan awalan yang tidak mungkin muncul di pola nama berkas:
>
> ```
> cari_berkas|*laporan* sejak:7
> ```
>
> ```python
> def cari_berkas(arg):
>     pola, _, sisa = arg.strip().partition(" sejak:")
>     hari = int(sisa) if sisa.isdigit() else None
>     batas = time.time() - hari * 86400 if hari else 0
>     ...
>     if p.stat().st_mtime < batas:
>         continue
> ```
>
> `slot_ke_argumen` yang menempelkannya, dari `slot["waktu"]`, dan cuma untuk
> `cari_berkas`. Untuk `buka_berkas` slot waktu tidak dipakai, karena membuka
> berkas menuntut satu sasaran pasti dan penyaring waktu tidak memberikannya —
> ia cuma mempersempit daftar, dan daftar yang sempit tetap bukan satu berkas.
> Itu tetap Soal 4c.

---

## Soal 5 - Pagar diadu, bukan diasumsikan

**5a.** Kedelapan serangan di `SERANGAN_JALUR` ditolak. Untuk masing-masing,
sebutkan mekanisme mana di `alat._aman` yang menolaknya: `resolve()`,
`relative_to()`, atau keduanya.

> **Jawaban:** Terukur (Uji G). Kolom "mentah" berarti jalurnya sudah di dalam
> `FOLDER_BOLEH` SEBELUM `resolve()`; kolom "resolve" berarti masih di dalam
> sesudahnya.
>
> ```
> jalur                                        mentah  resolve  penolak
> S:/.../..(/..)/Windows/System32/config/SAM     True    False   resolve() lalu relative_to()
> ../../../../../../Windows/win.ini             False    False   relative_to() saja
> C:/Users/SANDY FAUZI/.ssh/id_rsa              False    False   relative_to() saja
> S:/Code/Make A Jarvis/../../../Users           True    False   resolve() lalu relative_to()
> ~/.bash_history                               False    False   expanduser() lalu relative_to()
> \\?\C:\Windows\System32\drivers\etc\hosts     False    False   relative_to() saja
> S:/Code/Make A Jarvis/./../../boot.ini         True    False   resolve() lalu relative_to()
> //localhost/C$/Windows                        False    False   relative_to() saja
> ```
>
> **Tiga jalur ditolak oleh keduanya bekerja sama** — jalur ber-`..` yang
> secara tertulis ada di dalam pagar, dan cuma `resolve()` yang membongkar ke
> mana ia sebenarnya menunjuk. Untuk ketiganya, `relative_to()` sendirian akan
> **meloloskan** mereka; lihat 5d.
>
> **Empat jalur ditolak `relative_to()` sendirian**, karena mereka tidak pernah
> berada di dalam pagar pada tahap mana pun. `resolve()` tidak diperlukan.
>
> **Dan satu jalur ditolak oleh mekanisme ketiga yang soalnya tidak sebutkan:
> `expanduser()`.** Terukur:
>
> ```
> Path('~/.bash_history').resolve()               -> S:\Code\Make A Jarvis\~\.bash_history
> Path('~/.bash_history').expanduser().resolve()  -> C:\Users\SANDY FAUZI\.bash_history
> ```
>
> Tanpa `expanduser()`, `~` diperlakukan sebagai nama folder biasa dan
> jalurnya berakhir **di dalam** repo, jadi `relative_to()` meloloskannya dan
> `resolve()` tidak menolong sama sekali. Yang menyelamatkan baris itu adalah
> `expanduser()` di baris pertama `_aman`, dan pilihan soal antara dua
> mekanisme tidak memuat jawabannya.

**5b.** Tambahkan minimal tiga seranganmu sendiri. Untuk tiap satu, tulis
lebih dulu ramalanmu apakah ia lolos, baru jalankan. Laporkan ramalan yang
salah apa adanya.

> **Jawaban:** Empat serangan tambahan. **Ramalan ditulis lebih dulu**, di
> dalam komentar `SERANGAN_JALUR` pada
> [`bulan2_sesi4_synesis.py`](bulan2_sesi4_synesis.py), sebelum satu pun
> dijalankan.
>
> | # | jalur | ramalan | terukur |
> |---|---|---|---|
> | 1 | `S:/CodeRahasia/rahasia.txt` | ditolak | **ditolak** |
> | 2 | `S:/Code/Make A Jarvis/../../Code/Make A Jarvis/log.md` | lolos | **lolos** |
> | 3 | `S:/Code/Make A Jarvis/.git/config` | lolos | **lolos** |
> | 4 | `S:/Code/Make A Jarvis/log.md:rahasia` | lolos | **lolos** |
>
> **Keempat ramalan kena.** Itu bukan hasil yang membanggakan; itu tanda saya
> memilih serangan yang terlalu mudah saya prediksi. Alasan memilih
> masing-masing:
>
> **1 — kekeliruan awalan string.** Ini yang paling saya ingin tahu.
> `S:/CodeRahasia` bukan anak dari `S:/Code`, tapi sebagai string ia berawalan
> `S:/Code`. Pagar yang ditulis dengan `str.startswith()` akan meloloskannya,
> dan itu cara paling umum orang menulis pemeriksaan ini. `_aman` memakai
> `Path.relative_to()`, yang membandingkan komponen jalur, jadi `CodeRahasia`
> tidak cocok dengan `Code`. Ditolak, dan alasannya persis yang saya harapkan.
>
> **2 — kendali negatif, dan sengaja diramalkan LOLOS.** `..` yang keluar lalu
> masuk lagi berakhir di dalam pagar, dan memang seharusnya diizinkan. Kalau
> baris ini ditolak, artinya pagarnya menolak token `..` alih-alih menolak
> tujuannya, dan pagar seperti itu akan menolak jalur sah sambil tetap bisa
> ditembus dengan symlink. Ia lolos, jadi pagarnya memeriksa tujuan.
>
> **Baris LOLOS di keluaran Bagian 4 karena serangan ini bukan kegagalan
> pagar.** Berkasnya menyalakan peringatan "ADA SERANGAN YANG LOLOS" untuk
> setiap baris yang lolos, dan untuk kendali negatif peringatan itu memang
> semestinya menyala.
>
> **3 — di dalam pagar tapi tetap tidak boleh dibaca.** `.git/config` memuat
> alamat remote dan, dengan credential helper, token. Pagar jalur memeriksa
> DI MANA, bukan APA. Ini Soal 5e, dan sengaja saya masukkan sebagai serangan
> supaya lubangnya muncul sebagai baris LOLOS di keluaran, bukan sebagai
> paragraf.
>
> **4 — aliran data alternatif NTFS.** `log.md:rahasia` adalah aliran
> tersembunyi di dalam berkas yang namanya sah. Saya duga `resolve()` akan
> memperlakukan seluruhnya sebagai nama berkas biasa di dalam `S:/Code`, dan
> memang begitu.
>
> **Sesudah lapisan kedua dipasang** (Soal 5e), serangan 3 dan 4 jadi ditolak
> dan serangan 2 tetap lolos, yang memang harus:
>
> ```
> ditolak  S:/Code/Make A Jarvis/.git/config     ditahan lapisan isi lewat '.git'
> ditolak  S:/Code/Make A Jarvis/log.md:rahasia  aliran data alternatif NTFS
> LOLOS    S:/Code/Make A Jarvis/../../Code/Make A Jarvis/log.md
> ```
>
> Jadi 12 serangan, 11 ditolak, 1 lolos dan itu kendali negatifnya.

**5c.** `FOLDER_BOLEH` memuat `S:/Code`. Sebutkan apa saja yang jadi bisa
dibaca SYNESIS karena baris itu, dan putuskan apakah kamu masih mau baris itu
ada di sana.

> **Jawaban:** Terukur (Uji K):
>
> ```
> S:/Code memuat 47 entri tingkat atas, 79.729 berkas
> yang cocok POLA_RAHASIA: 1.335
> ```
>
> Baris `Path("S:/Code")` di `FOLDER_BOLEH` membuat setiap berkas dari semua
> 47 proyek di drive itu bisa dibaca SYNESIS: kode orang lain, `node_modules`,
> berkas data, dan 1.335 berkas yang namanya saja sudah menandakan rahasia —
> `.env`, `.git/config`, kunci, kredensial.
>
> **Apakah saya masih mau baris itu ada di sana? Tidak.**
>
> Alasan baris itu ditulis masuk akal: supaya SYNESIS bisa mencari lintas
> proyek. Tapi yang mengarahkan alat itu adalah pengklasifikasi kantong kata
> 353 kolom dengan akurasi 56 persen di data nyata, dan Sesi 3 sudah mengukur
> bahwa untuk kalimat yang tidak dikenalinya ia mengeluarkan satu tebakan tetap
> tanpa membaca kalimatnya. Menyerahkan 79.729 berkas ke penunjuk sebesar itu
> bukan perhitungan yang seimbang.
>
> **Yang saya lakukan:** persempit jadi `AKAR` dan `E:/SYNESIS` saja, dan
> tambahkan folder proyek tertentu satu per satu waktu `audit.jsonl`
> menunjukkan saya benar-benar membutuhkannya. Itu urutan yang benar:
> perluasan izin harus dipicu kebutuhan yang tercatat, bukan diantisipasi.
>
> Belum saya ubah di `konfig.py` sekarang, karena mengubahnya akan mengubah
> keluaran Bagian 4 sehingga tabel serangan di atas tidak lagi bisa
> dibandingkan dengan soalnya. Ditulis sebagai keputusan, dan lapisan
> keduanya (5e) sudah dipasang lebih dulu karena ia menutup lubang yang lebih
> tajam dengan risiko yang lebih kecil.

**5d.** `_aman` memanggil `resolve()` sebelum memeriksa. Jelaskan kenapa
urutan itu penting, lalu tunjukkan satu jalur yang akan lolos kalau urutannya
dibalik.

> **Jawaban:** **Kenapa urutannya penting:** `relative_to()` membandingkan
> komponen jalur seperti yang TERTULIS. Baginya `..` cuma sebuah komponen,
> bukan perintah untuk naik. Cuma `resolve()` yang mengubah jalur tertulis
> jadi jalur yang benar-benar akan dibuka. Memeriksa sebelum me-resolve berarti
> memeriksa jalur yang tidak akan pernah dibuka siapa pun.
>
> Terukur (Uji G), kalau urutannya dibalik — `relative_to()` dulu, `resolve()`
> sesudahnya — **tiga dari dua belas serangan lolos**:
>
> ```
> LOLOS: S:/Code/Make A Jarvis/../../Windows/System32/config/SAM
>        sesungguhnya menunjuk S:\Windows\System32\config\SAM
> LOLOS: S:/Code/Make A Jarvis/../../../Users
>        sesungguhnya menunjuk S:\Users
> LOLOS: S:/Code/Make A Jarvis/./../../boot.ini
>        sesungguhnya menunjuk S:\boot.ini
> ```
>
> Ambil yang pertama sebagai contoh yang diminta soal. Sebagai deretan
> komponen, `S:/Code/Make A Jarvis/../../Windows/...` diawali
> `S:`, `Code`, `Make A Jarvis`, jadi `relative_to(S:/Code/Make A Jarvis)`
> berhasil dan pagar mengatakan aman. Baru sesudah itu `resolve()` menyusutkan
> `..` dan jalurnya berubah jadi `S:\Windows\System32\config\SAM`, yang sudah
> lolos pemeriksaan dan tidak diperiksa lagi.
>
> Aturan umumnya, dan ia berlaku jauh di luar berkas: **normalisasi sebelum
> validasi, selalu.** Memvalidasi bentuk yang belum dinormalkan berarti
> memvalidasi sesuatu yang bukan yang akan dipakai. Kerentanan jalur, suntikan
> SQL lewat penyandian ganda, dan pengelabuan Unicode semuanya varian dari
> kesalahan urutan yang sama.

**5e.** Pagar ini memeriksa jalur, bukan isi. Sebutkan satu berkas di dalam
`FOLDER_BOLEH` yang tetap tidak seharusnya dibaca dan dikirim ke mana pun,
lalu usulkan lapisan kedua yang menangkapnya.

> **Jawaban:** Berkas di dalam `FOLDER_BOLEH` yang tetap tidak boleh dibaca dan
> dikirim ke mana pun: **`S:/Code/Make A Jarvis/.git/config`**. Ia memuat
> alamat remote, dan dengan credential helper yang menyimpan ke berkas, ia
> memuat token. Pagar jalur menganggapnya sah karena letaknya memang di dalam
> folder yang diizinkan, dan itu terukur — ia salah satu serangan saya di 5b
> dan ia LOLOS.
>
> Terukur, ada 1.335 berkas semacam itu di `S:/Code` (Uji K).
>
> **Lapisan kedua, sudah dipasang** di
> [`../synesis/alat.py`](../synesis/alat.py):
>
> ```python
> POLA_RAHASIA = re.compile(
>     r"^(\.env(\..*)?|\.git|\.ssh|\.aws|\.npmrc|id_[a-z0-9]+"
>     r"|.*\.(key|pem|pfx|p12)|credentials(\..*)?|secrets?\..*)$",
>     re.IGNORECASE)
>
> def _bukan_rahasia(p):
>     for bagian in p.parts[1:]:
>         if ":" in bagian:
>             raise DitolakPagar(...)          # aliran data alternatif NTFS
>         if POLA_RAHASIA.match(bagian):
>             raise DitolakPagar(...)
>     return p
> ```
>
> Ia dipanggil dari dalam `_aman`, tepat sesudah jalurnya terbukti ada di
> dalam pagar. Alasannya sama dengan Soal 2d Sesi 3: `_aman` satu-satunya
> pintu yang dilewati `baca_berkas` dan `daftar_berkas`, jadi memasangnya di
> situ berarti tidak ada pembaca yang bisa melewatinya. Memasangnya di tiap
> alat berarti alat berikutnya yang saya tulis akan lupa.
>
> Ia mencocokkan **komponen jalur, bukan isi**, jadi ongkosnya nol dan tidak
> ada berkas yang dibuka untuk memutuskan. Terukur sesudah dipasang: jalur sah
> tetap lolos (`log.md`, `notebooks/`), dua serangan baru ditolak.
>
> **Lapisan ketiga, belum dipasang dan sengaja:** pemindai isi yang mencari
> pola token (`ghp_[A-Za-z0-9]{36}`, `sk-[A-Za-z0-9]{32,}`, blok
> `BEGIN PRIVATE KEY`) dan entropi tinggi di dalam berkas yang sudah lolos
> dua lapisan pertama. Ia perlu waktu SYNESIS mulai mengirim isi berkas ke
> suatu tempat — ke prompt LLM di Bulan 6, misalnya. Sekarang isinya cuma
> dicetak ke terminal saya sendiri, jadi lapisan ketiga belum membeli apa
> pun. Ditulis di sini supaya tidak lupa waktu Bulan 6 datang.

<details>
<summary>Petunjuk 5e</summary>

Cari `.env`, `.git/config`, dan berkas berisi token di dalam repomu sendiri.
Pagar jalur menganggap ketiganya sah karena memang ada di dalam folder yang
diizinkan.

</details>

---

## Soal 6 - Ujung ke ujung

**6a.** Salin tabel tindakan Bagian 5. Untuk tiap baris, sebutkan lapisan
mana yang menghentikannya: ambang ongkos, ketiadaan alat, ketiadaan argumen,
atau gerbang izin.

> **Jawaban:** Terukur (Bagian 5):
>
> ```
> tindakan              jumlah   bagian    lapisan yang menghentikannya
> jalan                      1     2.4%    (tidak dihentikan)
> tolak_yakin               19    46.3%    ambang ongkos
> tolak_argumen              0     0.0%    ketiadaan argumen
> tolak_izin                 0     0.0%    gerbang izin
> belum_ada_alat            21    51.2%    ketiadaan alat
> ```
>
> Dua lapisan mengerjakan seluruh pekerjaan: **ambang ongkos** menahan 19, dan
> **ketiadaan alat** menahan 21. Dua lapisan lainnya nol.
>
> Nol pada `tolak_argumen` punya sebab yang bisa dilacak: yang lolos ambang
> cuma satu pesan, dan pesan itu `info_sistem`, yang argumennya string kosong
> menurut rancangan. Lapisan argumen tidak pernah punya kesempatan.
>
> Nol pada `tolak_izin` lebih perlu diperhatikan, dan **ia bukan bukti
> gerbangnya bekerja**. Gerbang izin cuma dipanggil untuk risiko selain BACA,
> dan ambang ongkos untuk TULIS dan MERUSAK adalah 0,950 dan 0,995. Terukur
> (Uji K), keyakinan MERUSAK tertinggi di seluruh 41 pesan adalah 0,913. Tidak
> ada satu pun pesan yang pernah sampai ke gerbang itu. Ia belum diuji sama
> sekali oleh pengukuran ini.
>
> Diuji terpisah dengan peluang buatan, supaya pernyataan "gerbangnya
> terpasang" punya bukti:
>
> ```
> peluang pasang_paket 0.999 -> putuskan memilih pasang_paket
>                            -> risiko MERUSAK, izin=None -> tolak_izin
> ```
>
> Dan dengan `izin=izin_konsol` di mode percakapan sungguhan, `install numpy`
> berhenti di `tolak_yakin` pada keyakinan 0,911, jadi bahkan di jalur nyata
> ambangnya yang menahan lebih dulu.

**6b.** Jumlah tindakan yang meleset ternyata nol. Nyatakan apakah itu bukti
pagarnya bekerja, atau akibat dari kebijakan yang hampir tidak pernah
bertindak. Bedakan keduanya dengan satu pengukuran.

> **Jawaban:** **Akibat dari kebijakan yang hampir tidak pernah bertindak**, dan
> angkanya menutup perdebatan.
>
> Pipa itu bertindak **1 kali dari 41**. Nol tindakan yang meleset dari satu
> tindakan adalah nol kegagalan dari satu percobaan. Terukur (Uji K), aturan
> tiga memberi batas atas laju salah $3/1$, yang dipotong jadi 100 persen:
> **pengukuran itu tidak membatasi apa pun sama sekali.**
>
> **Satu pengukuran yang memisahkan keduanya:** paksa kebijakannya selalu
> bertindak, dan hitung berapa yang meleset. Kalau pagarnya yang bekerja,
> angkanya harus tetap kecil. Kalau abstensinya yang bekerja, angkanya harus
> melonjak.
>
> Terukur (Uji K):
>
> ```
> kebijakan sekarang (ongkos harapan) : bertindak  1, meleset  0 dari 41
> argmax polos (selalu bertindak)     : bertindak 41, meleset 18 dari 41
> ```
>
> Delapan belas dari empat puluh satu. **Yang menahan kerusakan bukan pagarnya
> melainkan diamnya.** Lapisan pagar — argumen, izin, jalur — memang terpasang
> dan terbukti benar satu per satu di Bagian 4, tapi di jalannya Bagian 5
> mereka tidak pernah menahan apa pun karena tidak pernah ada yang sampai ke
> mereka.
>
> Itu bukan alasan membongkar pagarnya. Itu alasan berhenti mengutip "0
> tindakan meleset" sebagai bukti bahwa pagarnya bekerja, dan mulai
> mengutipnya sebagai apa adanya: SYNESIS v0.1 aman terutama karena ia hampir
> tidak melakukan apa pun. Soal 3e menaikkan angka bertindak dari 1 jadi
> lebih banyak, dan begitu itu terpasang, pengukuran ini harus diulang.

**6c.** Ambil tiga pesan yang berakhir `tolak_yakin`, dan periksa apakah
memang seharusnya ditolak. Kalau ada yang seharusnya jalan, telusuri sampai
ke keyakinan model dan ambang kelasnya.

> **Jawaban:** Terukur (Uji I), tiga pesan pertama yang berakhir `tolak_yakin`:
>
> ```
> 'bagian abcd itu apa saja tadi??'
>   label benar   : jelaskan_konsep   (BAHASA, tidak ada alat)
>   tebakan model : obrol yakin 0.461, ambang obrol 0.667
>   kelas termurah: obrol ongkos 1.62 lawan ongkos menolak 1.0
>
> 'bikin file log.md untuk kamu mencatat semua yg telah'
>   label benar   : ubah_proyek       (BAHASA, tidak ada alat)
>   tebakan model : ubah_proyek yakin 0.492, ambang 0.667
>   kelas termurah: ubah_proyek ongkos 1.52 lawan ongkos menolak 1.0
>
> 'bikinin modul all in one menjelaskan dengan sangat m'
>   label benar   : ubah_proyek       (BAHASA, tidak ada alat)
>   tebakan model : tanya_umum yakin 0.222
>   kelas termurah: cari_berkas ongkos 1.84 lawan ongkos menolak 1.0
> ```
>
> **Ketiganya memang seharusnya ditolak, tapi bukan karena alasan yang
> ditolakkan.** Label benar ketiganya BAHASA, jadi seandainya ambangnya
> meloloskan mereka, ketiganya tetap akan berhenti di `belum_ada_alat` satu
> langkah kemudian. Penolakannya benar dan mubazir sekaligus.
>
> Yang kedua paling layak diperhatikan: **modelnya BENAR** — ia menebak
> `ubah_proyek` dan label benarnya `ubah_proyek` — dan ia tetap ditolak karena
> keyakinannya 0,492 di bawah 0,667. Jadi ambang ongkos membuang tebakan yang
> tepat. Itu bukan kesalahan; itu memang harga yang model ongkos putuskan
> layak dibayar, dan di sini harganya nol karena `ubah_proyek` tidak punya
> alat.
>
> Pertanyaan yang lebih tajam daripada memeriksa tiga pesan: berapa dari 19
> penolakan yang benar-benar mencegah sesuatu? Terukur (Uji K):
>
> ```
> dari 19 pesan tolak_yakin, yang label BENARNYA punya alat: 3
> ```
>
> **Enam belas dari sembilan belas akan berhenti di `belum_ada_alat`
> juga.** Untuk mereka, ambangnya tidak mencegah apa pun; taksonomilah yang
> mencegah. Ambang ongkos benar-benar bekerja untuk 3 pesan dari 41.

**6d.** Jalankan mode percakapan, ketik `buka laporan praktikum minggu lalu`,
dan catat apa yang terjadi sampai selesai. Kalau berkasnya tidak terbuka,
sebutkan di langkah mana ia berhenti dan apa yang kurang. Ini kalimat
"selesai bila" dari rencana Bulan 2, jadi laporkan hasilnya apa adanya.

> **Jawaban:** Dijalankan sungguhan, bukan mode kering, lewat pipa yang sudah
> pindah ke `synesis/`:
>
> ```
> python -m synesis.cli --sungguhan
>
> ==================================================================
>   SYNESIS v0.1  mode SUNGGUHAN  ketik /keluar untuk berhenti
> ==================================================================
>   Mode sungguhan. Alat akan benar-benar dipanggil.
>
>   kamu > buka laporan praktikum minggu lalu
>   intent  : buka_berkas  (yakin 0.951, risiko BACA)
>   tindakan: jalan
>     Tidak ada berkas di S:\Code\Make A Jarvis\laporan praktikum
>
>   kamu > /keluar
>
>   Catatan tersimpan di S:\Code\Make A Jarvis\data\bulan2\audit.jsonl
> ```
>
> **Berkasnya tidak terbuka.** Dilaporkan apa adanya, karena ini kalimat
> "selesai bila" dari rencana Bulan 2.
>
> Di langkah mana ia berhenti, dan apa yang kurang. Yang berhasil, satu per
> satu: kalimatnya divektorkan, model memberi `buka_berkas` dengan keyakinan
> 0,951, ambang ongkos BACA 0,500 melewatkannya, `ekstrak_slot` menemukan
> `objek='laporan praktikum'` dan `waktu=-7`, `slot_ke_argumen` membentuk
> argumennya, risikonya BACA jadi gerbang izin dilewati sesuai rancangan,
> `alat.pakai("baca_berkas", ...)` dipanggil, `_aman` meloloskan jalurnya, dan
> alat menjawab.
>
> Semua lapisan bekerja. **Yang berhenti di langkah terakhir, dan yang kurang
> adalah langkah yang memang belum pernah ditulis: penerjemah dari frasa
> bahasa manusia jadi pola nama berkas.** `laporan praktikum` diserahkan ke
> `baca_berkas` sebagai jalur, diselesaikan relatif terhadap direktori kerja,
> dan tidak ada berkas bernama itu. Itu Soal 4c, dan ia satu-satunya hal yang
> berdiri di antara jalannya ini dan sasaran Bulan 2.
>
> Untuk kelengkapan, dua kalimat lain di sesi sungguhan yang sama:
>
> ```
>   kamu > install numpy
>   intent  : pasang_paket  (yakin 0.911, risiko MERUSAK)
>   tindakan: tolak_yakin
>
>   kamu > berapa sisa disk
>   intent  : info_sistem  (yakin 0.403, risiko BACA)
>   tindakan: tolak_yakin
> ```
>
> Yang pertama persis perilaku yang dituju: keyakinan 0,911 tinggi menurut
> ukuran mana pun yang biasa dipakai, dan tetap ditolak karena MERUSAK
> menuntut 0,995. Yang kedua menunjukkan harganya: pertanyaan yang tidak
> berbahaya sama sekali juga ditolak, karena 0,403 di bawah 0,500. Kedua baris
> itu keluar dari satu aturan yang sama, dan itulah maksudnya.

---

## Soal 7 - Catatan audit dan mode kering

**7a.** `jalankan_pipa` memakai `kering=True` sebagai bawaan. Sebutkan kenapa
bawaan itu syarat, bukan kesopanan, dengan menyebut satu urutan kejadian yang
mungkin terjadi kalau bawaannya `False`.

> **Jawaban:** **Urutan kejadian yang mungkin terjadi kalau bawaannya
> `False`,** dan ia tidak butuh kelalaian besar:
>
> 1. Saya mengimpor `jalankan_pipa` di sebuah notebook untuk memeriksa tabel
>    ambang, dan menjalankannya atas ke-41 pesan nyata seperti yang Bagian 5
>    lakukan.
> 2. Bawaannya `kering=False`, jadi setiap pesan yang lolos ambang benar-benar
>    memanggil alatnya. Untuk `buka_berkas` dan `cari_berkas` risikonya BACA,
>    jadi gerbang izin tidak dipanggil sama sekali.
> 3. `baca_berkas` mengembalikan sampai 60.000 karakter isi berkas, dan
>    `jalankan_pipa` menaruh isi itu di medan `hasil`, yang lalu ditulis ke
>    `audit.jsonl` sebagai satu baris JSON.
> 4. Sekarang berkas yang isinya saya tidak pernah niat baca ada salinannya di
>    dalam catatan audit, permanen, karena catatan itu hanya-menambah menurut
>    rancangan.
>
> Langkah 4 yang membuatnya syarat, bukan kesopanan: kekeliruan itu tidak bisa
> dibatalkan dengan menekan Ctrl-C. Dan itu baru jalur BACA. Begitu ada yang
> menyerahkan `izin=izin_konsol`, seperti yang `repl` memang lakukan, satu
> ketukan `y` pada prompt yang sedang saya baca sambil lalu menjalankan
> perintah shell sungguhan.
>
> Aturan umumnya: **setelan yang merusak harus menuntut saya mengetik sesuatu;
> setelan yang aman harus tidak menuntut apa-apa.** Bawaan adalah pilihan yang
> diambil oleh orang yang tidak sedang memperhatikan, dan orang yang tidak
> sedang memperhatikan adalah kondisi paling umum saya berada.
>
> `--sungguhan` di `synesis/cli.py` mahal secara sengaja: ia harus diketik,
> dan ia mencetak satu baris peringatan sebelum prompt pertama.

**7b.** Audit ditulis untuk SEMUA tindakan, termasuk yang ditolak. Sebutkan
kenapa baris yang ditolak lebih berharga daripada baris yang jalan, untuk
tujuan yang diukur di Bagian 7 Sesi 3.

> **Jawaban:** Tujuan yang diukur Bagian 7 Sesi 3 adalah menemukan apa yang
> paling kurang dari Bulan 2, dan jawabannya catatan pemakaian yang mewakili.
> Untuk tujuan itu, **baris yang ditolak lebih berharga karena baris yang
> jalan hanya menegaskan apa yang sudah bisa.**
>
> Baris `jalan` berbunyi: kalimat ini sudah tertangani. Ia tidak menunjuk
> pekerjaan apa pun.
>
> Baris yang ditolak berbunyi: kalimat ini benar-benar saya ucapkan, dan
> sistem tidak bisa menanganinya. Itu contoh berlabel untuk celahnya, dan
> labelnya datang dari pemakaian, bukan dari generator.
>
> Terukur, dari 41 pesan:
>
> ```
> belum_ada_alat  21    daftar alat yang harus dibuat, terurut menurut frekuensi
> tolak_yakin     19    kalimat tempat model paling ragu
> jalan            1    yang sudah bisa
> ```
>
> Dua puluh satu baris `belum_ada_alat` adalah daftar pekerjaan Bulan 3 yang
> tidak dikarang siapa pun. Sembilan belas baris `tolak_yakin` adalah persis
> sampel yang akan dibeli mahal oleh pembelajaran aktif: contoh tempat model
> paling tidak yakin, yaitu tempat satu label manusia paling banyak
> mengurangi ketidakpastian.
>
> Dan satu baris `jalan` itu, dibandingkan dengan 40 lainnya, adalah alasan
> kenapa mencatat yang ditolak bukan sekadar berguna melainkan satu-satunya
> cara catatan ini punya isi sama sekali. Kalau audit cuma memuat yang jalan,
> sesudah 41 pesan ia akan berisi satu baris.

**7c.** JSONL dipilih daripada JSON. Sebutkan dua sifat yang membuatnya lebih
cocok untuk catatan yang tumbuh, dan satu hal yang jadi lebih sulit.

> **Jawaban:** **Dua sifat yang membuat JSONL lebih cocok untuk catatan yang
> tumbuh:**
>
> 1. **Menambah tanpa membaca.** Satu baris ditulis dengan membuka mode `"a"`
>    dan menulis satu baris. Tidak ada baca-ubah-tulis atas seluruh berkas,
>    jadi ongkos menambah tetap sama entah berkasnya 10 baris atau 10 juta,
>    dan dua proses yang menulis bersamaan menyisipkan baris yang berselang,
>    bukan merusak strukturnya. Berkas JSON menuntut kurung penutup, jadi tiap
>    penambahan adalah menulis ulang.
> 2. **Tahan gagal sebagian.** Larik JSON harus utuh secara sintaks untuk bisa
>    diurai; proses yang mati di tengah penulisan merusak seluruh riwayat.
>    JSONL rusak paling banter satu baris terakhir, dan sisanya tetap terbaca.
>    Untuk catatan audit, sifat ini bukan kenyamanan — catatan yang bisa hilang
>    seluruhnya karena satu penulisan gagal bukan catatan.
>
> Sifat ketiga yang tidak diminta tapi ikut: ia bisa dialirkan. Membaca 100.000
> baris tidak menuntut memuat semuanya ke memori, dan `wc -l`, `tail`, `grep`
> semuanya jalan tanpa pengurai JSON sama sekali.
>
> **Satu hal yang jadi lebih sulit: tidak ada tempat untuk metadata seberkas.**
> Versi skema, pemilik, rentang tanggal, jumlah baris — di JSON semuanya
> tinggal jadi kunci di tingkat atas. Di JSONL tidak ada tingkat atas, jadi
> tiap baris harus membawa versinya sendiri, dan berkasnya tidak bisa
> divalidasi sebagai satu dokumen. Akibat sehari-harinya: `json.load(f)` gagal,
> dan siapa pun yang mencoba membacanya pertama kali akan mencoba itu dulu.

**7d.** Audit ini memuat kalimat perintahmu apa adanya. Sebutkan jenis
informasi apa yang bisa bocor lewat berkas ini, dan putuskan apakah
`data/bulan2/audit.jsonl` boleh masuk git. Alasan harus menyebut isi
`.gitignore` sekarang.

> **Jawaban:** **Jenis informasi yang bisa bocor lewat berkas ini.** Medan
> `kalimat` disimpan apa adanya, tanpa dibersihkan. Terukur, baris pertama
> dari jalannya uji saya berbunyi:
>
> ```json
> {"kalimat": "<path> kerjain dan jelasin. lemvar soalnya belum ada si claude malah limit", ...}
> ```
>
> Jadi yang lewat ke sana: **jalur berkas absolut** (termasuk nama pengguna
> Windows saya, yang muncul sebagai `C:\Users\SANDY FAUZI\...`), nama proyek
> dan klien, nama orang yang saya sebut, penanda akademik seperti kode mata
> kuliah dan NPM, dan kunci API kalau saya pernah menempelkannya ke sebuah
> perintah. Medan `argumen` membawa jalur absolut lagi. Dan medan `hasil` di
> mode sungguhan bisa memuat sampai 60.000 karakter isi berkas.
>
> Ditambah satu yang bukan isi: **cap waktu tiap baris**. Empat puluh satu
> baris beserta waktunya adalah catatan jam kerja saya.
>
> **Boleh masuk git? Tidak.**
>
> Dan menurut `.gitignore` sekarang ia memang sudah tidak bisa, tapi karena
> alasan yang salah. Baris yang menutupinya:
>
> ```
> # Dataset & bobot model - semua di E:\SYNESIS\
> data/
> ```
>
> Seluruh folder `data/` diabaikan, jadi `data/bulan2/audit.jsonl` sudah aman
> hari ini tanpa perubahan apa pun. Tapi komentarnya menyebut ukuran berkas,
> bukan kerahasiaan. Siapa pun yang nanti memutuskan untuk mulai melacak
> sebagian `data/` — misalnya `data/bulan2/README.md`, yang memang layak
> dilacak — akan melonggarkan baris itu dan tidak punya alasan menduga bahwa
> ada catatan berisi pesan pribadi di dalamnya.
>
> Jadi saya tambahkan baris eksplisit di bawah judul **Rahasia**, tempat
> `.env` dan `*.key` sudah berada:
>
> ```
> # Rahasia
> .env
> *.key
> data/bulan2/audit.jsonl      # memuat kalimat perintah apa adanya
> ```
>
> Repo ini sudah punya kebijakan yang tepat untuk kelas berkas seperti ini —
> `docs/akademik/` diabaikan dengan komentar "nama, NPM, nilai - jangan masuk
> git". Yang kurang cuma menerapkannya ke audit. Aturan yang dibawa: berkas
> diabaikan karena satu alasan tidak boleh diandalkan melindungi alasan yang
> lain.

**7e.** Catatan audit yang hanya bisa ditambah tetap bisa dihapus seluruhnya
oleh siapa pun yang bisa menulis ke folder itu. Sebutkan apa yang sebenarnya
dijamin sifat "hanya menambah" dan apa yang tidak.

> **Jawaban:** **Yang dijamin sifat hanya-menambah:** bahwa SYNESIS sendiri,
> dalam pemakaian normal, tidak bisa menulis ulang atau menyusun ulang apa yang
> sudah ia tulis. Tiap keputusan tetap ada, dalam urutan ia dibuat, jadi
> jalannya bisa diputar ulang. Ia menghapus satu mode kegagalan tertentu: bug
> di versi berikutnya yang diam-diam menyunting riwayatnya sendiri. Itu jaminan
> tentang **perilaku penulisnya**, dan cakupannya persis sebesar itu.
>
> **Yang tidak dijamin:** keutuhan terhadap siapa pun atau apa pun yang bisa
> menulis ke folder itu. Berkasnya bisa dipotong, disunting di editor teks,
> atau dihapus seluruhnya, dan tidak ada apa pun di dalamnya yang akan
> menunjukkan bahwa itu terjadi. Tidak ada rantai hash, tidak ada tanda tangan,
> tidak ada salinan di luar. Baris yang dihapus dari tengah tidak meninggalkan
> lubang yang bisa dilihat. Menambah baris palsu bertanggal kemarin juga tidak
> terdeteksi.
>
> Dan saya sendiri sudah melakukannya dalam sesi ini, jadi bukti bahwa
> "hanya-menambah" tidak mencegah penghapusan ada di riwayat kerja saya
> sendiri: `audit.jsonl` hasil jalannya uji saya dipindahkan keluar repo
> supaya berkas yang nanti tumbuh berisi pemakaian sungguhan saja. Satu
> perintah, dan seluruh berkasnya hilang dari tempatnya.
>
> **Yang benar-benar memberi bukti gangguan**, dan harganya satu medan per
> baris: rantai hash. Tiap baris membawa
> `sha256(hash_baris_sebelumnya + isi_baris)`. Menyunting atau menghapus satu
> baris memutus rantainya dari titik itu ke depan, dan pemutusan itu bisa
> dideteksi tanpa membandingkan dengan apa pun. Lalu kirim hash paling
> depannya ke tempat lain secara berkala — satu commit harian berisi satu
> baris hash, atau salinan ke `E:/SYNESIS` — supaya menulis ulang SELURUH
> rantai pun tetap ketahuan.
>
> Yang tersisa sesudah itu bukan lagi masalah berkas, melainkan masalah
> kepercayaan: catatan yang saya buat tentang diri saya sendiri, disimpan di
> mesin saya sendiri, tidak akan pernah jadi bukti bagi orang lain. Ia bisa
> jadi bukti bagi saya, dan untuk tujuan Bagian 7 Sesi 3 itu memang cukup.

---

## Soal 8 - Rencana pengumpulan data nyata

**8a.** Bagian 7 Sesi 3 menyimpulkan bahwa yang paling kurang bukan
representasi melainkan catatan pemakaian yang mewakili. Nyatakan berapa baris
audit yang kamu butuhkan sebelum melatih ulang, dan turunkan angkanya dari
Soal 1 Sesi 3, bukan dari perasaan.

> **Jawaban:** Diturunkan dari Soal 1 Sesi 3, bukan dari perasaan, dan lewat
> dua jalur karena Soal 8d menuntut kriterianya memakai ongkos.
>
> **Jalur akurasi (Soal 1b Sesi 3).** Untuk membedakan perbaikan 10 poin dari
> nol, uji berpasangan pada porsi ketidaksepakatan $\psi\approx 0{,}30$
> menuntut $n\approx 115$ kalimat uji untuk selangnya tidak memuat nol, dan
> $n\approx 233$ kalau saya juga mau 80 persen peluang menemukannya.
>
> **Jalur ongkos, yang dipakai.** Ongkos per pesan bukan Bernoulli, jadi
> rumusnya berbeda. Terukur (Uji J), kebijakan sekarang atas 41 pesan:
>
> ```
> ongkos per pesan: rerata 0.951, simpangan baku 0.999, maksimum 3.0
> ```
>
> Untuk perbaikan sebesar $d$ per pesan dengan simpangan baku selisih $s$,
> $n=(1{,}96\,s/d)^2$:
>
> ```
>   perbaikan d    s = 0,50    s = 1,00    s = 1,50
>          0.10          96         384         864
>          0.25          15          61         138
>          0.50           4          15          35
> ```
>
> Sasaran saya menurunkan ongkos dari 0,95 ke 0,70 per pesan, yaitu
> $d=0{,}25$. Dengan $s\approx 1{,}0$ terukur, itu **61 pesan uji
> berpasangan.**
>
> Satu peringatan yang membuat 61 itu batas bawah, bukan jawaban: $s=0{,}999$
> diukur dari kebijakan yang hampir tidak pernah bertindak, jadi ongkosnya
> hampir selalu 1,0 dan ragamnya kecil karena alasan yang salah. Begitu Soal
> 3e terpasang dan pipanya mulai bertindak, tindakan MERUSAK yang salah
> berbobot 200,0 masuk ke ragamnya, dan $s$ melonjak. Jadi angka 61 harus
> dihitung ulang dari data audit sendiri, bukan dipakai apa adanya.
>
> **Baris audit yang dibutuhkan.** 61 pesan uji dengan belahan 70/15/15
> memberi $61/0{,}15\approx 407$ baris. Baris audit tidak semuanya berupa
> kalimat berbeda — ada pengulangan, salah ketik, dan perintah `/kering`.
> Dibulatkan ke **500 baris berkalimat berbeda**, dengan sekurangnya 30 baris
> per intent yang akan saya pertahankan.
>
> Untuk pembanding: kalau saya bersikeras memakai akurasi juga, 115 pesan uji
> menuntut sekitar 767 baris. Kriteria ongkos lebih murah karena ia mengukur
> hal yang lebih besar geserannya.

**8b.** Selama masa pengumpulan, SYNESIS akan sering menolak, dan itu
melelahkan. Sebutkan risiko bahwa kamu berhenti memakainya sebelum datanya
cukup, dan rancang satu perubahan yang menurunkan risiko itu tanpa
menurunkan mutu datanya.

> **Jawaban:** **Risikonya nyata dan angkanya sudah ada.** Terukur, dari 41
> pesan: 46,3 persen ditolak dan 51,2 persen berhenti karena tidak ada
> alatnya. SYNESIS menolak atau menyerah pada 97,6 persen kalimat. Sebuah
> program yang berguna satu kali dari empat puluh tidak akan saya buka besok,
> apalagi selama enam minggu. Rencana yang menuntut 500 baris dari alat
> setidak-berguna itu akan mati di baris ke-tiga puluh.
>
> Ini juga tepat pola Soal 8e: yang paling mungkin membuat rencananya gagal
> bukan salah hitung melainkan saya berhenti memakainya.
>
> **Perubahan yang saya rancang: waktu pipanya menolak, ia harus tetap
> mengerjakan sesuatu yang berguna — dan cara ia melakukannya justru
> MENAIKKAN mutu datanya.**
>
> Gantikan penolakan diam dengan pilihan bernomor:
>
> ```
> kamu > bikin ringkasan bab 3
>   Saya tidak cukup yakin. Tebakan terdekat:
>     1  ringkas_catatan   0.41
>     2  ubah_proyek       0.22
>     3  cari_berkas       0.11
>   Pilih nomor, atau ketik ulang, atau Enter untuk lewat.
> ```
>
> Kenapa ini tidak menurunkan mutu data, dan justru sebaliknya. Sekarang baris
> yang ditolak berisi tebakan model dan tidak berisi kebenaran; nilainya cuma
> sebagai "kalimat yang gagal". Sesudah perubahan ini, tiap penolakan yang
> saya jawab dengan nomor menghasilkan baris berisi **label yang saya
> konfirmasi sendiri**. Penolakan berubah dari data mentah jadi data emas, dan
> justru penolakan yang paling banyak, 19 dari 41.
>
> Yang tidak boleh saya lakukan, dan godaannya besar: **menurunkan ambangnya
> supaya SYNESIS lebih sering bertindak.** Itu menukar mutu data dengan
> kenyamanan, dan ia persis tukar-tambah yang seluruh Sesi 4 dibangun untuk
> menolak. Ambangnya turun karena model ongkosnya diperbaiki (Soal 3e), bukan
> karena saya bosan.
>
> Satu tambahan kecil dengan hasil besar: `Enter untuk lewat` harus ada.
> Kalau satu-satunya jalan keluar adalah memilih nomor, saya akan memilih
> asal-asalan waktu terburu-buru, dan label asal-asalan lebih buruk daripada
> tidak ada label.

**8c.** Kamu tahu sedang mencatat dirimu sendiri, dan itu bisa mengubah cara
kamu mengetik. Sebutkan nama efek ini, lalu rancang cara mengukur seberapa
besar ia terjadi pada datamu.

> **Jawaban:** Namanya **efek Hawthorne** di ilmu sosial. Di fisika ia
> persoalan alat ukur yang mengganggu keadaan yang diukurnya — mengukur suhu
> dengan termometer yang menyerap panas, atau mengukur posisi elektron dengan
> foton yang menendangnya.
>
> **Cara mengukur seberapa besar ia terjadi pada data saya.** Kuncinya
> pembanding yang tidak bisa saya pengaruhi, dan saya sudah punya dua, karena
> keduanya ditulis sebelum alat ukurnya ada:
>
> - riwayat PSReadLine saya, di
>   `(Get-PSReadlineOption).HistorySavePath`;
> - ke-41 pesan di `data/bulan2/raw/`, yang ditulis waktu merancang proyek ini
>   dan bukan waktu memakainya.
>
> **Empat besaran yang dibandingkan, semuanya bisa dihitung program:**
>
> 1. median panjang kalimat dalam token;
> 2. porsi token di luar kosakata model (untuk 41 pesan arsip sudah terukur:
>    51,1 persen);
> 3. porsi kalimat yang diawali kata kerja perintah;
> 4. nisbah tipe terhadap token, yaitu seberapa beragam kosakatanya.
>
> Kalau kalimat di `audit.jsonl` **lebih pendek, lebih sedikit kata asingnya,
> dan lebih sering berbentuk perintah** daripada kedua pembanding, itu efeknya,
> dan selisih tiap besaran adalah besar efeknya. Arah itu yang saya duga: kalau
> saya tahu sedang melatih pengklasifikasi, saya akan tanpa sadar mengetik
> kalimat yang mudah diklasifikasi.
>
> **Ukuran kedua, yang tidak butuh pembanding sama sekali:** belah audit
> menurut minggu, dan hitung keempat besaran itu per minggu. Efek Hawthorne
> luruh waktu kebaruannya hilang. Kalau minggu 1 berbeda dari minggu 4 dan
> minggu 4 bergeser mendekati pembandingnya, kurva peluruhan itu sendiri
> adalah pengukuran efeknya, **dan ia juga memberi tahu saya untuk membuang
> minggu 1.**
>
> Yang tidak bisa saya lakukan: menghilangkan efeknya. Saya satu-satunya
> pengguna dan saya yang menulis alat ukurnya. Yang bisa saya lakukan
> mengukurnya, lalu melaporkan angkanya bersama hasilnya, seperti ralat
> pengukuran mana pun.

**8d.** Susun kriteria berhenti: kapan pengumpulan dianggap cukup, apa yang
dilatih ulang, dan bagaimana kamu tahu model barunya lebih baik. Syaratnya
satu: kriteria "lebih baik" harus memakai ongkos, bukan akurasi.

> **Jawaban:**
>
> **Kapan pengumpulan dianggap cukup — empat syarat, semuanya harus terpenuhi:**
>
> 1. **≥ 500 baris audit dengan `kalimat` yang berbeda-beda** (dari Soal 8a:
>    61 pesan uji dibagi 0,15, dibulatkan naik untuk pengulangan).
> 2. **≥ 30 baris untuk tiap intent yang akan dipertahankan.** Syarat ini yang
>    menangkap kegagalan "500 baris tapi cuma 5 kalimat berbeda".
> 3. **≥ 4 minggu kalender berlalu**, supaya sampelnya melintasi lebih dari
>    satu jenis minggu — minggu kuliah, minggu ujian, minggu libur.
> 4. **Keempat besaran Soal 8c mendatar selama 2 minggu terakhir**, yang
>    menandakan efek Hawthorne sudah luruh. Data dari minggu 1 dibuang.
>
> **Apa yang dilatih ulang.** Cuma pengklasifikasi intent. Bukan taksonominya,
> bukan tabel ongkosnya, bukan ambangnya — kalau lebih dari satu hal berubah,
> perbandingannya tidak bisa dibaca, dan itu pelajaran Bagian 3 Sesi 3 tentang
> sapuan satu variabel. Data latihnya sintetis ditambah baris audit yang
> labelnya saya konfirmasi lewat pilihan bernomor Soal 8b.
>
> **Belahan ujinya menurut WAKTU, bukan acak.** Lima belas persen baris
> terakhir menurut cap waktu jadi himpunan uji. Belahan acak membocorkan
> kosakata masa depan ke masa lalu: kalau saya mulai memakai kata baru di
> minggu 5, belahan acak menaruh sebagiannya di data latih dan model terlihat
> lebih pintar daripada ia akan bekerja besok.
>
> **Kriteria "lebih baik", dan ia memakai ongkos:**
>
> Model baru menang kalau **ongkos total kebijakan ongkos harapan atas baris
> uji yang sama turun sekurangnya 0,25 per pesan, dengan selang 95 persen
> berpasangan atas selisihnya tidak memuat nol** ($n\ge 61$ dari Soal 8a,
> dihitung ulang dengan $s$ dari data audit sendiri). `ONGKOS_SALAH` dan
> `ONGKOS_TOLAK` harus sama persis dengan yang dipakai model lama, kalau tidak
> yang dibandingkan dua papan skor yang berbeda.
>
> Akurasi tetap dilaporkan, di kolom sebelahnya, dan **tidak ikut memutuskan**.
> Bagian 3 sudah mengukur kenapa: urutan menurut akurasi dan urutan menurut
> ongkos berkebalikan persis.
>
> **Satu gerbang keras yang bukan tukar-tambah:** jumlah tindakan MERUSAK yang
> salah pada himpunan uji harus tetap nol. Kalau model baru lebih murah tapi
> menjalankan satu perintah shell yang keliru, ia kalah, berapa pun angkanya.
> Ongkos 200,0 itu perkiraan; sebuah `rm` yang salah bukan.
>
> **Dan dasar mayoritas dihitung dulu, sebelum model manapun disebut bagus.**
> Tuas C Sesi 3 mengukur apa yang terjadi kalau langkah itu dilewati: tugas dua
> kelas mencetak 78,0 persen dan terlihat hebat sampai dasar mayoritasnya
> dihitung dan ternyata 85,4.

**8e.** Tuliskan apa yang paling mungkin membuat rencana 8d gagal, lalu
tuliskan bagaimana kamu akan tahu bahwa itu sedang terjadi.

> **Jawaban:** **Yang paling mungkin membuat rencana 8d gagal: saya tidak
> pernah sampai 500 baris, karena saya cuma mengetik ke SYNESIS waktu saya
> ingat SYNESIS ada, dan saya hampir tidak pernah ingat.**
>
> Bukan salah hitung, bukan model yang buruk, bukan bug. Auditnya bertambah
> tiga baris seminggu alih-alih empat puluh, dan sesudah dua bulan saya
> menyimpulkan bahwa "datanya belum cukup" seolah itu keadaan cuaca, bukan
> akibat dari SYNESIS berupa program terpisah yang harus dibuka.
>
> **Bagaimana saya akan tahu itu sedang terjadi.** Satu pemeriksaan, di jadwal
> tetap, dengan ambang yang ditulis sekarang selagi saya belum punya
> kepentingan atas jawabannya:
>
> ```
> tiap Minggu malam:  wc -l data/bulan2/audit.jsonl
>
>   < 40 baris di akhir minggu 2   -> rencananya sudah gagal
>   < 120 baris di akhir minggu 4  -> gagal
> ```
>
> Ambangnya dari aritmetika 8d: 500 baris dalam 6 minggu berarti sekitar 83
> baris seminggu, jadi 40 di minggu 2 sudah setengah laju yang dibutuhkan dan
> tidak akan mengejar. Yang membuat pemeriksaan ini bekerja adalah angkanya
> ditulis lebih dulu; kalau saya menunggu sampai minggu 4 baru memutuskan apa
> yang dianggap terlalu lambat, saya akan memutuskan bahwa yang saya punya
> ternyata cukup.
>
> Dan pemeriksaan mingguan itu tidak boleh berupa pencacah di prompt, karena
> Soal 8c menuntut alat ukurnya tak terlihat selama pemakaian. Ia perintah
> tersendiri yang saya jalankan di hari yang saya tetapkan, dan `audit.jsonl`
> sendiri tidak dibuka.
>
> **Kalau alarmnya menyala,** yang diubah bukan sasarannya melainkan cara
> SYNESIS dijangkau: jadikan ia yang saya ketik memang tanpa berpikir —
> pembungkus prompt shell, atau satu tombol pintas — bukan program yang harus
> saya ingat untuk dibuka. Menurunkan sasaran dari 500 ke 200 menggoda dan
> salah: 200 baris memberi 30 pesan uji, dan Soal 8a sudah menghitung bahwa 30
> tidak bisa membedakan perbaikan yang saya cari dari nol. Rencana yang
> sasarannya diturunkan sampai bisa dicapai menghasilkan angka yang tidak bisa
> memutuskan apa pun, dan itu lebih buruk daripada tidak mengukur, karena ia
> terlihat seperti pengukuran.
>
> **Kegagalan kedua yang paling mungkin: 500 baris berisi lima kalimat yang
> sama berulang.** Sudah tertangkap oleh syarat 8d(1) dan 8d(2), yang menghitung
> kalimat berbeda dan menuntut 30 per intent. Kalau ia terjadi, hasilnya akan
> terbaca "500 baris, 40 kalimat berbeda", dan kesimpulan yang benar bukan
> "kumpulkan lagi" melainkan bahwa cara saya memakai SYNESIS memang sesempit
> itu — yang berarti pengklasifikasinya sudah cukup dan masalahnya tidak
> pernah ada di model.

---

## Tolok Ukur Bulan 2 Sesi 4

- [x] Tiap intent diberi kelas risiko, dan alasannya ongkos salah, bukan kerumitan
- [x] Ambang diturunkan dari pertidaksamaan ongkos, bukan disetel per intent
- [x] Ambang tangan Sesi 2 dibandingkan dengan hasil turunan, dan polanya dibaca
- [x] Keputusan memakai ongkos harapan semua kelas, bukan argmax lalu ambang
- [x] Kebijakan dibandingkan dengan ongkos total, dan bedanya dari akurasi disebut
- [x] Kebijakan "selalu menolak" ikut dihitung sebagai pembanding
- [x] Argumen yang tidak bisa dibentuk menghentikan pipa, bukan ditebak
- [x] Pagar jalur diadu dengan minimal sebelas serangan, tiga di antaranya milikmu
- [x] Ramalan lolos atau tidak ditulis sebelum serangan dijalankan
- [x] Catatan audit hanya menambah, dan memuat yang ditolak juga
- [x] Mode kering jadi bawaan, dan alasannya dinyatakan sebagai syarat
- [x] Gerbang izin manusia dipasang untuk semua risiko selain BACA
- [x] Pipa diukur ujung ke ujung, dan jumlah tindakan meleset dilaporkan
- [x] Mode percakapan dijalankan sungguhan, dan hasilnya dilaporkan apa adanya
- [x] Rencana pengumpulan data punya kriteria berhenti yang memakai ongkos
- [x] Pipa dipindahkan ke `synesis/niat.py` dan dipanggil dari `synesis/cli.py`

Kotak terakhir yang membuat Bulan 2 benar-benar tutup. Sampai pipanya tinggal
di `notebooks/`, ia latihan. Sesudah pindah ke `synesis/`, ia SYNESIS v0.1.

---

## Catatan jalannya

Ketujuh TODO di [`bulan2_sesi4_synesis.py`](bulan2_sesi4_synesis.py) terisi,
berkasnya jalan sampai selesai dalam 0,3 detik, dan seluruh tabel Bagian 1
sampai 5 cocok dengan yang tercetak di soal ini sampai digit terakhir
(447,0 / 242,0 / 39,0). Itu karena Sesi 4 membaca `data/bulan2/model_intent.npz`
yang memang belum dilatih ulang. Tabel Sesi 3 bergeser; tabel Sesi 4 tidak.

```
python notebooks\bulan2_sesi4_synesis.py       Bagian 1 sampai 6
python notebooks\kunci_b2s34_bukti.py          Uji G sampai Uji L
python -m synesis.niat                         pemeriksaan pipa
python -m synesis.cli --sungguhan              mode percakapan
```

### Kotak terakhir: pipanya sudah pindah

- [`../synesis/niat.py`](../synesis/niat.py) memuat `RUTE`, kelas risiko,
  `ambang_dari_ongkos`, `putuskan`, `slot_ke_argumen`, `catat_audit`, dan
  `jalankan_pipa`, lengkap dengan `_demo()` yang gagal kalau logikanya rusak.
- [`../synesis/cli.py`](../synesis/cli.py) memanggilnya. Bawaannya kering;
  `--sungguhan` harus diketik.
- Kedua tetapan ongkos dan kedua jalur berkas pindah ke
  [`../synesis/konfig.py`](../synesis/konfig.py), sesuai aturan berkas itu
  sendiri bahwa berkas lain tidak boleh memuat angka atau jalur langsung.
- `vektorkan` dan `ekstrak_slot` tetap diimpor dari notebook Sesi 2, dengan
  komentar yang menyebut kapan keduanya harus dipindah. Menyalinnya berarti
  dua salinan yang bisa berbeda diam-diam, dan itu harga yang lebih mahal
  daripada satu impor lintas folder.

### Dua perubahan pada kode yang sudah ada

Keduanya penutupan lubang yang diukur oleh soalnya sendiri, jadi ditulis di
sini supaya tidak lewat begitu saja.

1. **Lapisan kedua pagar** di [`../synesis/alat.py`](../synesis/alat.py):
   `POLA_RAHASIA` dan `_bukan_rahasia`, dipanggil dari dalam `_aman`. Soal 5b
   dan 5e menembus pagar jalur dengan `.git/config` dan aliran data alternatif
   NTFS, keduanya jalur yang seluruhnya sah. Sesudah lapisan ini, 11 dari 12
   serangan ditolak dan yang satu lolos adalah kendali negatifnya.
2. **Penolakan vektor nol** di `synesis/niat.py`: tindakan baru `tolak_kosong`,
   diperiksa sebelum model dipanggil. Soal 2d Sesi 3 memintanya, dan Soal 2c
   Sesi 3 mengukur kenapa: kalimat yang tidak dikenali satu katanya pun keluar
   sebagai `obrol` dengan keyakinan 0,397, dan ambang tangan `obrol` cuma 0,30.

### Tiga temuan yang tidak nyaman, ditulis apa adanya

1. **Kebijakan ongkos harapan cuma menang 2,0 dari kebijakan yang tidak pernah
   melakukan apa pun** (39,0 lawan 41,0, yaitu 4,9 persen). Sebabnya papan
   skornya memberi 0 untuk tindakan benar. Soal 3e menambahkan manfaat
   $-2{,}0$ dan selisihnya jadi delapan kali lipat (5,0 lawan 41,0).
2. **"0 tindakan meleset" bukan bukti pagarnya bekerja.** Pipanya cuma
   bertindak 1 kali dari 41, dan aturan tiga atas satu percobaan tidak
   membatasi apa pun. Dipaksa selalu bertindak, angkanya 18 meleset dari 41.
3. **Ambang ongkos benar-benar mencegah sesuatu untuk 3 pesan saja.** Dari 19
   pesan `tolak_yakin`, cuma 3 yang label benarnya punya alat; 16 sisanya akan
   berhenti di `belum_ada_alat` juga.

### Dan kalimat "selesai bila" Bulan 2

`buka laporan praktikum minggu lalu` sampai memanggil `baca_berkas` dengan
keyakinan 0,951, lalu berhenti di `Tidak ada berkas di S:\Code\Make A
Jarvis\laporan praktikum`. Berkasnya tidak terbuka. Yang kurang bukan pagar,
bukan ambang, bukan model: yang kurang penerjemah frasa manusia jadi pola nama
berkas, dan itu Soal 4c.
