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

> **Jawaban:** Tulis hasil contoh ke-$i$ sebagai $X_i$: benar bernilai 1 dan
> salah bernilai 0. Untuk Bernoulli, $E[X_i]=p$ dan
> $\mathrm{Var}(X_i)=p(1-p)$. Akurasi adalah rata-rata
> $\bar X=\sum_i X_i/n$. Karena contoh dianggap bebas,
> $\mathrm{Var}(\bar X)=p(1-p)/n$, sehingga simpangan bakunya
> $\sqrt{p(1-p)/n}$.

**1b.** Kamu ingin selang kepercayaan 95 persennya selebar 5 poin persen,
bukan 24. Hitung berapa kalimat uji yang kamu butuhkan.

> **Jawaban:** Dengan pendekatan lebar selang
> $4\sqrt{0{,}9(0{,}1)/n}=0{,}05$, didapat
> $n=0{,}09/(0{,}0125)^2=576$ kalimat uji.

**1c.** Dari 1b, dan dari proporsi belahan 70/15/15, hitung berapa total
kalimat yang harus kamu tulis. Bandingkan dengan angka 300 sampai 500 di
rencana Bulan 2.

> **Jawaban:** Jika 576 adalah 15%, totalnya `576 / 0.15 = 3840` kalimat.
> Jadi target 300--500 cukup untuk prototipe, tetapi tidak cukup untuk selang
> selebar 5 poin. Dengan total 300--500, data uji hanya 45--75 dan lebarnya
> masih sekitar 17,9--13,9 poin.

**1d.** Sekarang tulis kalimatnya. Bukan yang saya bayangkan, yang **memang
kamu ucapkan**. Buka riwayat perintah terminalmu, catatan, dan pesanmu
sendiri selama seminggu terakhir sebagai bahan. Catat berapa kelas baru yang
muncul yang tidak ada di delapan kelas awal.

> **Status:** Belum dikerjakan. Saat ini ada 120 kalimat dan 8 kelas. Bagian
> ini harus memakai riwayat asli pemilik; agen tidak boleh mengarang 3.720
> kalimat lalu mengaku itu ucapan nyata.

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

> **Jawaban:** Yang bocor adalah daftar kata yang muncul di validasi/uji.
> Informasi itu masuk melalui pemilihan kolom fitur dan ukuran lapisan pertama.
> Kata khusus data uji mendapat kolom sebelum evaluasi, padahal sistem yang
> jujur belum tahu kata itu saat dilatih.

**2b.** Apakah kebocoran itu membuat akurasi uji naik atau turun? Ramalkan
dulu, lalu ukur: ubah satu baris di `__main__`, jalankan Bagian 3, catat.

> **Jawaban:** Ramalan awal: tidak ada arah yang pasti. Kolom kata uji tidak
> pernah dilatih, sehingga bobot acaknya bisa menambah derau, bukan otomatis
> menolong. Hasil delapan seed membenarkan itu. Hitung-kata bersih memberi
> validasi/uji `65,6%/68,2%`; kosakata bocor memberi `71,9%/62,5%`. Untuk
> TF-IDF hasil bersih `65,6%/66,7%`, sedangkan kosakata bocor
> `68,8%/66,1%`. Jadi kebocoran membuat angka tidak sah, bukan pasti lebih
> tinggi.

**2c.** `bobot_idf` juga cuma dihitung dari himpunan latih. Kebocoran macam
apa yang dicegah di situ, dan kenapa ia lebih halus daripada 2a?

> **Jawaban:** IDF membawa jumlah dokumen yang memuat tiap kata. Jika data uji
> ikut dihitung, frekuensi kata di masa depan mengubah skala fitur data latih.
> Ini lebih halus karena daftar kolom bisa tetap sama; yang bocor hanya angka
> statistik di dalam setiap kolom.

**2d.** Di Bagian 3, kosakata dan IDF dihitung ulang di dalam gelung untuk
tiap belahan. Kenapa itu wajib, dan apa yang rusak kalau kamu menghitungnya
sekali di luar gelung?

> **Jawaban:** Setiap seed punya himpunan latih yang berbeda, jadi praprosesnya
> juga harus dipelajari ulang dari himpunan itu. Jika dihitung sekali di luar,
> beberapa putaran memakai informasi dari validasi/uji putaran tersebut dan
> delapan skor tidak lagi menjadi delapan pengukuran yang bebas dan jujur.

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

> **Jawaban:** Percobaan ini belum mampu membedakan hitung-kata dan TF-IDF.
> Selisih validasi 0,0 poin jauh lebih kecil daripada perubahan 25 poin akibat
> belahan data, sehingga kemenangan satu angka uji hanya kebetulan sampel.

**3b.** Kamu sudah pernah menghadapi bentuk ini di praktikum fisika. Tuliskan
padanannya: apa yang jadi ralat pengukuran, dan apa yang jadi selisih yang
mau diukur.

> **Jawaban:** Perubahan skor antarbelahan adalah ralat alat ukur. Selisih
> rerata skor hitung-kata dan TF-IDF adalah sinyal yang ingin diukur. Di sini
> ralat jauh lebih besar daripada sinyal.

**3c.** Rancang percobaan yang BISA memutuskan. Berapa belahan, berapa data,
atau uji statistik apa. Sebutkan yang paling murah lebih dulu.

> **Jawaban:** Yang termurah: pakai 5-fold stratified cross-validation yang
> diulang 10 kali, lalu hitung selisih skor berpasangan beserta selang
> kepercayaannya atau uji permutasi berpasangan. Jika selangnya masih memuat
> nol, tambah data. Target ketat 5 poin memerlukan sekitar 576 contoh uji atau
> 3.840 total menurut Soal 1.

**3d.** Berkas ini tetap memakai `hitung kata` untuk bagian selanjutnya.
Karena akurasi tidak bisa jadi alasan, sebutkan alasan yang sah untuk memilih
salah satunya. Ada beberapa, sebut minimal dua.

> **Jawaban:** Hitung-kata dipilih karena kodenya lebih sedikit, tidak perlu
> menyimpan vektor IDF, dan bobot per katanya lebih mudah dibaca saat model
> salah. Itu alasan biaya dan keterjelasan, bukan klaim akurasi.

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

> **Jawaban:** Tidak ada satu pasangan tunggal yang paling sering; keenam
> arah berikut masing-masing terjadi sekali:
>
> - `buka_berkas -> obrol`: "bukain slide presentasi tadi pagi"
> - `buka_berkas -> cari_berkas`: "bukain file tugas fisika"
> - `hitung -> jadwal`: "ubah dua jam ke menit"
> - `jadwal -> hitung`: "jam berapa kelas fisika besok"
> - `ringkas_catatan -> jadwal`: "apa poin penting di catatan minggu ini"
> - `ringkas_catatan -> obrol`: "apa kesimpulan laporan itu"

**4b.** Untuk tiap kesalahan di 4a, putuskan: ini masalah model, atau masalah
data? Kriterianya tegas — kalau kamu sendiri tidak bisa menentukan kelasnya
dari kalimat itu saja, itu masalah data, bukan model.

> **Jawaban:** Dengan definisi delapan kelas saat ini, keenamnya masih bisa
> dilabeli oleh manusia dari kalimat saja. Jadi ini kesalahan model kecil yang
> kekurangan contoh pembeda: bentuk `bukain`, beda "jam sebagai satuan" dan
> "jam sebagai jadwal", serta pertanyaan ringkasan yang diawali `apa`.
> Menambah contoh pembeda adalah perbaikan termurah.

**4c.** `buka_berkas` dan `jalankan_program` sama-sama sering diawali kata
"buka". Apakah keduanya memang dua intent, atau sebenarnya satu intent dengan
slot yang berbeda? Argumentasikan dua-duanya, lalu putuskan.

> **Jawaban:** Digabung masuk akal karena keduanya berarti membuka satu target;
> slot `jenis_target` bisa membedakan berkas dan aplikasi. Dipisah juga masuk
> akal karena membuka berkas biasanya baca-saja, sedangkan menjalankan program
> dapat memicu efek samping dan butuh pagar lebih kuat. Untuk SYNESIS keduanya
> tetap dipisah agar ambang dan izin keamanannya bisa berbeda.

**4d.** Kelas mana yang presisinya rendah tapi recall-nya tinggi? Jelaskan
apa artinya itu secara konkret untuk pengguna SYNESIS, dalam satu kalimat
tanpa istilah presisi atau recall.

> **Jawaban:** `obrol` bernilai 60% dan 100%: semua obrolan dikenali, tetapi
> dua dari lima kalimat yang dikirim ke obrol sebenarnya perintah buka atau
> ringkas.

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

> **Jawaban:** Softmax hanya membagi total peluang 1 ke delapan kelas yang
> tersedia. Tidak ada kelas kesembilan bernama "bukan semuanya". Karena itu
> nilai terbesar selalu ada, bahkan saat semua pilihan sebenarnya salah.

**5b.** Susun tabel ongkos untuk SYNESIS. Untuk tiap intent, isi dua kolom:
harga satu tebakan salah, dan harga satu penolakan yang seharusnya diterima.
Pakai satuan apa pun asal konsisten.

> **Jawaban:** Skala 1 berarti gangguan kecil dan 10 berarti berpotensi
> merusak pekerjaan.
>
> | intent | salah | menolak |
> |---|---:|---:|
> | buka_berkas | 3 | 1 |
> | cari_berkas | 2 | 1 |
> | hitung | 4 | 1 |
> | jadwal | 7 | 2 |
> | jalankan_program | 8 | 2 |
> | kontrol_sistem | 10 | 1 |
> | obrol | 1 | 1 |
> | ringkas_catatan | 3 | 1 |

**5c.** Dari 5b, tentukan ambang per intent, bukan satu ambang global.
Terapkan di kode, jalankan ulang Bagian 5, dan bandingkan dengan ambang
tunggal terbaik.

> **Jawaban:** Ambang yang diterapkan berurutan adalah `0.55, 0.40, 0.60,
> 0.85, 0.85, 0.90, 0.30, 0.55` untuk delapan intent pada tabel. Hasilnya 14
> benar, 3 salah, dan 7 menolak. Dibanding ambang global 0,50, dua kesalahan
> hilang dengan harga tiga penolakan tambahan. Ia tidak menolak lima kalimat
> asing karena kelas murah seperti `obrol` sengaja longgar; jadi ambang ongkos
> bukan pengganti kelas keluar atau pendeteksi data asing.

**5d.** Ada cara ketiga selain menebak dan menolak: bertanya balik. Rancang
kapan SYNESIS harus bertanya "maksudmu buka berkas atau jalankan program?"
Nyatakan syaratnya dalam besaran yang bisa dihitung dari keluaran softmax.

> **Jawaban:** Urutkan peluang menjadi $p_1\ge p_2$. Jika keduanya cukup masuk
> akal, misalnya $p_2\ge0{,}25$, dan marginnya $p_1-p_2<0{,}15$, tanyakan
> pilihan dua kelas teratas. Jika $p_1$ juga berada di bawah ambang kelasnya
> dan tidak ada pesaing dekat, tolak atau serahkan ke LLM.

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

> **Status:** Belum dikerjakan. Lima frasa harus berasal dari kebiasaan nyata
> pemilik, jadi waktu pengerjaannya juga belum boleh diklaim.

**6b.** Sebutkan tiga bentuk kalimat yang membuat `ekstrak_slot` versimu
salah, yang tidak bisa kamu perbaiki dengan sekadar menambah entri tabel.

> **Jawaban:** "dua hari setelah ujian" memerlukan acuan dari kalender;
> "ingatkan setelah unduhan selesai" memakai kejadian, bukan tanggal; dan
> "rapat jam tiga kalau dosen sudah datang" memuat syarat. Ketiganya perlu
> memahami hubungan antarbagiannya, bukan hanya mencari satu frasa.

**6c.** Dari 6b, nyatakan syarat umumnya: sifat apa dari sebuah slot yang
membuat aturan tangan berhenti memadai dan model mulai layak?

> **Jawaban:** Aturan tangan berhenti cukup saat nilai slot bergantung pada
> konteks, acuan di luar kalimat, susunan kata yang beragam, atau hubungan
> antar-slot. Model baru layak jika kegagalan nyata sudah cukup banyak untuk
> menjadi data latih dan uji.

**6d.** Untuk SYNESIS di laptopmu, dengan data yang kamu punya, slot mana
yang tetap kamu tangani dengan aturan tangan sampai Bulan 6? Jawab dengan
angka dari 6a.

> **Jawaban sementara:** Waktu relatif, jam, serta nama berkas/aplikasi tetap
> memakai aturan tangan karena bentuknya sedikit dan mudah diperiksa. Keputusan
> akhir beserta angka waktunya menunggu percobaan pribadi 6a.

---

## Soal 7 - Slot yang tidak disebutkan

Spesifikasi `ekstrak_slot` melarang menebak. "jam tiga" jadi `03:00`, bukan
`15:00`, kecuali ada penanda sore atau malam.

**7a.** Sebutkan satu perintah nyata di mana menebak `15:00` untuk "jam tiga"
menyebabkan kerugian, dan satu lagi di mana menebak `03:00` yang merugikan.

> **Jawaban:** "Bangunkan saya jam tiga untuk berangkat" bisa terlambat 12 jam
> jika ditebak 15:00. "Ingatkan rapat jam tiga" bisa membangunkan pengguna
> tengah malam jika yang dimaksud 15:00 tetapi ditebak 03:00.

**7b.** Dari 7a, jelaskan kenapa "ambil yang paling mungkin" adalah aturan
yang salah untuk slot, padahal itu aturan yang benar untuk intent.

> **Jawaban:** Intent memilih fungsi umum dan masih bisa ditahan oleh ambang
> serta izin. Slot menjadi nilai persis yang akan dijalankan. Tebakan jam yang
> salah dapat menghasilkan tindakan benar pada waktu yang salah, jadi
> ketidakpastian harus dipertahankan, bukan disembunyikan.

**7c.** Rancang perilaku yang benar untuk jam yang ambigu. Kaitkan dengan
jawabanmu di 5d.

> **Jawaban:** Simpan `03:00` sesuai teks tanpa mengubahnya menjadi sore, lalu
> sebelum membuat jadwal tanyakan "jam 3 pagi atau sore?". Ini sama dengan
> margin kecil di 5d: ada dua tafsir kuat dan sistem meminta pengguna memilih.

**7d.** `alat.py` di `synesis/` memerlukan callback `izin` sebelum
menjalankan apa pun. Jelaskan bagaimana ambang Soal 5 dan slot yang tidak
ditebak di soal ini bersama-sama membentuk lapisan keamanan yang sama.

> **Jawaban:** Ambang mencegah fungsi dipilih saat intent lemah. Pemeriksaan
> slot mencegah fungsi menerima argumen yang dikarang. Callback `izin` menjadi
> gerbang terakhir sebelum tindakan berbahaya benar-benar dijalankan. Tindakan
> hanya lolos jika ketiga lapisan setuju.

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

> **Jawaban:** `1.900.000 / 68,3 = 27.818`, jadi model 3B sekitar 27,8 ribu
> kali lebih besar. Dokumen sprint mengukur perpindahan model 3--15 detik.
> Pada 0,004 ms per perintah, waktu muat itu cukup untuk sekitar 750 ribu
> sampai 3,75 juta klasifikasi.

**8b.** Tulis lima perintah yang BENAR-BENAR butuh LLM, yang tidak mungkin
diselesaikan klasifikasi 8 kelas berapa pun banyaknya datamu. Untuk tiap
perintah, sebutkan apa persisnya yang hilang.

> **Jawaban:**
>
> - "Bandingkan hasil eksperimen ini dan cari penyebab anomalinya": perlu
>   membaca hasil, mencari hubungan, dan menyusun alasan.
> - "Jelaskan backpropagation dengan bahasa yang mudah saya pahami": perlu
>   membuat penjelasan sesuai tingkat pemahaman pengguna.
> - "Baca dua makalah ini lalu kritik metode keduanya": perlu memahami dokumen
>   panjang dan menilai argumen.
> - "Rancang arsitektur SYNESIS yang aman dan jelaskan pilihanmu": perlu
>   merancang beberapa komponen dan menimbang pilihan.
> - "Kenapa model ini overfit dan bagaimana memperbaikinya": perlu diagnosis
>   dari konteks serta beberapa kemungkinan tindakan.

**8c.** Ini yang berbahaya: pengklasifikasi tidak akan bilang "ini di luar
kemampuanku". Untuk kelima perintah di 8b, jalankan lewat modelmu dan catat
kelas serta keyakinan yang keluar. Apakah ambang Soal 5 menangkap semuanya?

> **Jawaban:** Hasilnya berturut-turut: `ringkas_catatan 0,5988`, `obrol
> 0,4035`, `jadwal 0,4448`, `cari_berkas 0,4042`, dan `jadwal 0,4722`.
> Ambang global 0,50 menangkap empat dari lima, bukan semuanya. Ambang per
> intent menangkap dua dari lima. Jadi keyakinan softmax saja tidak cukup
> untuk mengenali permintaan yang berada di luar delapan kelas.

**8d.** Rancang pembagian kerja antara pengklasifikasi dan LLM untuk SYNESIS,
dan nyatakan aturan penyerahannya sebagai syarat yang bisa dihitung. Ingat
batas keras dari `req.md`: LLM-nya 3B dan tinggal 0,9 GB VRAM sesudah model
lain.

> **Jawaban:** Kelas tindakan rutin hanya dijalankan jika peluang teratas
> melewati ambang kelas, margin dua teratas minimal 0,15, semua slot wajib ada,
> dan callback izin menyetujui. Margin di bawah 0,15 memicu pertanyaan balik.
> `obrol`, `ringkas_catatan`, kelas `tanya_umum` yang perlu ditambahkan lagi,
> serta penolakan classifier diserahkan ke LLM. Karena sisa VRAM hanya 0,9 GB,
> LLM 3B dimuat bergantian saat jalur itu dipilih; ia tidak dibiarkan menyala
> untuk perintah rutin.

---

## Tolok Ukur Bulan 2 Sesi 2

- [x] Belahan tiga arah ditulis sendiri, dan proporsi kelasnya dijaga
- [x] Ukuran data yang dibutuhkan dihitung dari selang kepercayaan, bukan ditebak
- [ ] Kalimat perintah ditambah sampai jumlah hasil hitungan Soal 1c
- [x] TF-IDF ditulis sendiri, dan normalisasi barisnya diuji berpanjang 1
- [x] Kebocoran kosakata diramalkan arahnya lebih dulu, lalu diukur
- [x] Kesimpulan "percobaan ini tidak bisa memutuskan" dinyatakan, bukan dihindari
- [x] Matriks bingung dibaca, dan tiap kesalahan digolongkan model atau data
- [x] Ambang per intent ditetapkan dari tabel ongkos, bukan dari satu angka global
- [x] Keadaan "bertanya balik" dirumuskan lewat margin dua peluang teratas
- [x] Ekstraksi slot jalan, dan slot yang tidak disebutkan tidak ditebak
- [x] Lima perintah yang butuh LLM ditulis, dijalankan, dan keyakinannya dicatat
- [x] Aturan penyerahan classifier ke LLM dinyatakan sebagai syarat terhitung

Kalau kedua belas kotak beres, kamu punya SYNESIS v0.1: perintah teks jadi
intent jadi argumen, nol LLM, 0,004 milidetik. Yang tersisa menyambungkannya
ke `synesis/alat.py`.
