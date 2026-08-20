# Soal Sesi A - Nggelindingin Kelereng (Gradient Descent)

Berkas latihan: [`sesiA_gradient_descent.py`](sesiA_gradient_descent.py)

Kemarin di Hari 3 kita udah sibuk ngebangun bentuk mangkoknya. Hari ini, saatnya kita beneran merakit mesin buat nggelindingin kelerengnya sampai ke dasar mangkok.

---

## Soal 1 - Tebak Arah Gradien Sebelum Ngoding

Data aslinya diciptakan dari `w = 3`, `b = 2`. Coba tebak tanda (positif/negatif) untuk `dMSE/dw` dan `dMSE/db` tanpa pakai kalkulator:

| Tebakan | w | b | tanda dL/dw | tanda dL/db |
|---|---|---|---|---|
| A | 0.0 | 0.0 | Negatif | Negatif |
| B | 5.0 | -1.0 | Positif | Negatif |
| C | 3.0 | 2.0 | Negatif | Positif |
| D | 2.9 | 2.1 | Negatif | Positif |

**Terus, kalau tandanya negatif, si `w` bakal geser ke mana di iterasi selanjutnya? Naik atau turun?**
> **Jawaban:** Bakal NAIK. Karena di rumus update (`w = w - lr * gradien`), kalau gradiennya minus, jadinya dikurangi angka minus (alias ditambah). Artinya, kalau gradien negatif (menandakan loss bakal turun kalau w dinaikin), ya kodenya bakal otomatis naikin nilai w. Insting fisika jalan!

---

## Soal 2 - Bikin Dua Macam Fungsi Turunan

Tadi udah dikerjain di file Python-nya ya:
- **2a.** `gradien(x, y, w, b)`: Turunan mulus analitik (kalkulus asli).
- **2b.** `beda_hingga(x, y, w, b, h)`: Turunan kasaran (numerik beda pusat).

Hasil pengecekannya (Gradient Check) udah lolos semua dengan galat super mungil (sekitar orde `1e-11` atau `1e-12`). Berarti rumus matematikamu 100% akurat.

---

## Soal 3 - Misteri Kenapa Beda Hingga Akurat Banget

Di kelas Komputasi Numerik, biasanya *Central Difference* punya error sisa (*Truncation Error*). Dan idealnya pakai `h` sekecil `1e-5`. Tapi di program ini, galatnya nyaris nggak ada.

**3a & 3b.** Kalau kita coba pakai `h = 0.1` (yang hitungannya gede banget), hasilnya malah bisa jauh lebih akurat dibanding `h = 1e-11`. Kok bisa?
> **Jawaban:** Karena fungsi MSE di model regresi linear ini murni fungsi parabola (polinomial derajat 2). Menurut deret Taylor, *truncation error* dari metode beda pusat itu berbanding lurus sama turunan ketiga dari fungsinya ($f'''(w)$). Berhubung ini polinomial derajat 2, turunan ketiganya ya **NOL MUTLAK**. 
Jadi pakai `h` segede gajah pun nggak akan ada *truncation error*. Tapi kalau pakai `h` kekecilan kayak `1e-11`, malah bakal muncul error pembulatan dari float memori komputer (*round-off error*). Makanya `h=0.1` menang telak di sini.

**3d.** Apakah aturan "selalu pakai h=1e-5" itu cuma mitos (*cargo cult*)?
> **Jawaban:** Aturan `1e-5` itu aturan kompromi *trade-off* umum buat fungsi yang rumit. Di kasus regresi linear ini, pakai `h=1e-5` agak buang-buang potensi. Nanti pas kita masuk ke Jaringan Saraf Tiruan (Neural Network) di Bulan 1 yang fungsinya udah dipatahin sama ReLU, turunan ketiganya udah nggak nol lagi. Di sanalah aturan `1e-5` baru terpakai beneran.

---

## Soal 4 - Kok Berhentinya Bukan di b = 2?

**4a.** Pas di-run, modelnya berenti di `w = 3.018` dan `b = 1.743`. Meleset dari target asli (`w=3, b=2`). Ini bug atau apa?
> **Jawaban:** BUKAN BUG. Gradient descent murni bekerja nyari titik dasar mangkok **berdasarkan kumpulan data sampel yang ada di depan matanya**. Karena 50 titik sampel kita udah disisipin "derau/noise" secara acak, titik pusat gravitasi datanya ikut bergeser dikit. Model kita sukses ngasih jawaban "terbaik" untuk data yang kotor itu, bukan menebak kebenaran alam semesta.

**4b.** Hitung simpangan baku prediksi `b` = $\sigma/\sqrt{n} = 1.5/\sqrt{50} \approx 0.21$. Error kita `0.26`, masih tergolong wajar (masih di sekitar batas 1 sigma fluktuasi acak).

**4c.** Kenapa tebakan `w` jauh lebih akurat (cuma meleset 0.01) dibanding `b`?
> **Jawaban:** Karena `w` itu kemiringan yang ditarik/diukur melintasi bentangan nilai `x` dari -5 sampai 5 (lengan torsi yang panjang). Mengukur kemiringan di atas rentang yang lebar itu jauh lebih presisi (varians/fluktuasi `x` ikut menekan nilai ketidakpastian). Berbeda dengan `b` (titik potong/geseran vertikal murni) yang ketidakpastiannya lebih telanjang bergantung pada jumlah data doang.

**4d.** Buktiin kalau garis optimum pasti membelah persis titik pusat massa (rata-rata x dan rata-rata y).
> **Jawaban:** Udah dibuktiin di *output* script `bagian 6`. Garis tebakan `w * rata_x + b` hasilnya identik plek sama nilai `rata_y` (yaitu `2.806923`). Ini sesuai syarat mutlak turunan minimum `dMSE/db = 0`.

**4e.** Kalau `derau` diset ke 0?
> **Jawaban:** Kalau nggak ada noise, kelerengnya bakal mendarat mulus mutlak tepat di angka aslinya: `w=3.0` dan `b=2.0`.

---

## Soal 5 - Meramal Bencana Kiamat (Batas Maksimal Learning Rate)

Ini *masterpiece*-nya sesi ini. Meramal batas angka *Learning Rate* (LR) secara fisis.

**5a & 5b.** Anggap ini sistem pegas berosilasi. Supaya errornya ($w - w^*$) menyusut tiap iterasi, faktor pelipatnya nggak boleh ngelewatin angka 1.
Rumus batas amannya: `lr < 1 / A`.
Di datamu, nilai $A = \frac{\sum x^2}{n} \approx 8.33$.
Berarti batas kritis `lr` adalah sekitar `1 / 8.33 = 0.120`.

**5c.** Pas dicek di log `bagian 5`:
- `lr = 0.12` -> Konvergen (Aman, jalan merambat).
- `lr = 0.13` -> DIVERGEN (Meledak / NaN).
Ramalan fisikamu akurat tanpa meleset! Batasnya memang bersembunyi di antara angka 0.12 dan 0.13.

**5d & 5e.** Kenapa mangkoknya bukan mangkok bundar melainkan lonjong (Bilangan Kondisi = 8)?
> **Jawaban:** Karena rentang sebaran variabel `x` beda sama variabel `b`. Akibatnya, kurvanya punya dua kelengkungan yang beda (sumbu yang satu terjal, sumbu lainnya landai). Ini bikin 1 nilai `lr` tunggal nggak akan pernah memuaskan kedua belah pihak. Kalau ngikutin yang landai, jalannya kelamaan. Kalau ngikutin yang terjal, keburu meledak. Makanya besok-besok kita butuh *Optimizer* canggih kayak Adam yang bisa ngasih LR beda-beda buat tiap kenop.

---

## Soal 6 - Menatap Bulan Depan

**6a.** Kenapa di Neural Network (Bulan 1), kalau kelereng dilepas dari titik beda, berhentinya di titik yang beda?
> **Jawaban:** Karena mangkoknya udah nggak mulus (cuma 1 dasar). Neural Network punya buanyak banget bukit dan lembah lokal (Local Minima) gara-gara disisipin lekukan Fungsi Aktivasi (ReLU).

**6b.** Kenapa kita harus verifikasi autograd buatan kita pakai metode kuno Beda Hingga (Gradient Check), bukan dicocokin sama output PyTorch aja?
> **Jawaban:** Kalau dicocokin sama PyTorch dan hasilnya beda, kita nggak tahu siapa yang salah (bisa jadi settingan PyTorch kita yang keliru). Beda Hingga itu hakim/wasit independen dari alam semesta matematika murni. Kalau kalkulusmu beda sama Beda Hingga, 100% kode kalkulusmu yang salah.

**6c.** Empat baris suci *training loop*:
```python
loss = hitung_loss()
grad = hitung_gradien()
w = w - lr * grad
b = b - lr * grad
```
Kalau baris 3 dan 4 dipindah ke atas (di-update dulu sebelum loss dihitung), sejarah *tracking* loss bakal geser satu iterasi (ngelaporin kondisi setelah jalan, bukan sebelum jalan).

---

## Tolok Ukur Sesi A

- [x] Turunan `dMSE/dw` dan `dMSE/db` diturunkan di kertas, bukan disalin
- [x] Tanda gradien di Soal 1 diramal benar sebelum dijalankan
- [x] Kelima titik gradient check lolos di bawah `1e-6`
- [x] Sapuan `h` dijalankan, dan kamu bisa menjelaskan kenapa `h` besar menang di sini
- [x] Kamu bisa menjelaskan kenapa `b` mendarat di 1,74 dan bukan 2, tanpa menyebutnya bug
- [x] Garis lewat titik pusat massa dibuktikan di kertas dari `dMSE/db = 0`
- [x] `lr` kritis diramal dari `A` **sebelum** melihat tabel, dan cocok dengan hasil
- [x] Nilai eigen Hessian dihitung, dan bilangan kondisinya kamu tafsirkan
- [x] Training konvergen ke titik yang sama dari tiga titik awal yang jauh berbeda
- [x] Hasil gradient descent cocok dengan `lstsq` sampai enam angka di belakang koma

Kalau semua udah dicentang, sah! Kamu udah membunuh semua "ilmu hitam" di balik Machine Learning dasar. Siap meluncur ke Sesi B!
