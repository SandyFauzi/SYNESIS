
Mari kita bedah alurnya menggunakan studi kasus nyata dari kodingan yang baru saja kamu jalankan di Sesi 2.

Bayangkan kita sedang melihat **satu titik koordinat** yang sedang ditebak oleh jaringan saraf (arsitektur **2** input $\rightarrow$ **8** neuron tersembunyi $\rightarrow$ **1** output).

### 1. INPUT (Titik Berangkat)

Kita mengambil satu titik dari dataset.

- Misalnya koordinatnya berada di posisi cincin dalam: `x0 = 0.5` dan `x1 = -0.3`.
- Karena ini cincin dalam, label aslinya adalah negatif: `y_asli = -1`.
- Kedua angka koordinat ini tidak dibiarkan sebagai angka biasa, melainkan dibungkus menjadi objek buatanmu: `Value(0.5)` dan `Value(-0.3)`.

---

### 2. PROSES (Maju & Mundur)

Proses ini terbagi menjadi tiga fase utama:

**A. *Forward Pass* (Jalan Maju)**

- **Masuk ke Lapisan Pertama (8 Neuron):** Koordinat `[0.5, -0.3]` masuk secara bersamaan ke 8 neuron. Setiap neuron memiliki bobot ($w$) dan geseran ($b$) acak yang berbeda.
- Masing-masing neuron menghitung perkalian titiknya: `pra = (w0 * 0.5) + (w1 * -0.3) + b`. Ingat, karena menggunakan kelas `Value`, setiap kali operasi `+` atau `*` terjadi, mesinmu sedang diam-diam membangun rantai silsilah (graf) di memori.
- **Ditekuk oleh ReLU:** Nilai `pra` tadi dilewatkan ke fungsi ReLU. Kalau angkanya minus (misal `-2.4`), ReLU mematikannya menjadi `0`. Kalau positif (misal `1.5`), diteruskan apa adanya. Dari sini, keluar 8 angka baru.
- **Masuk ke Lapisan Terakhir (1 Neuron):** Kedelapan angka tadi dirangkum oleh neuron terakhir. Di ujung ini, **tidak ada ReLU**. Kenapa? Agar model bebas memprediksi angka negatif.
- **Hasil Tebakan Awal:** Katakanlah keluaran akhirnya (prediksi) adalah `0.2`. Model menebak ini adalah kelas positif (cincin luar), padahal aslinya negatif. Tebakan ini salah.

**B. Hitung *Loss* (Hukuman)**

- Kita menggunakan Rugi Engsel (*Hinge Loss*): `rugi = max(0, 1 - y_asli * prediksi)`.
- Matematikanya: `1 - (-1 * 0.2) = 1.2`.
- Kerugiannya adalah `1.2`. Angka ini merepresentasikan "seberapa parah" kesalahan tebakan tadi.

**C. *Backward Pass* (Belajar dari Kesalahan)**

- Kita memanggil perintah sakti: `rugi.backward()`.
- Karena tadi saat jalan maju kelas `Value` sudah merajut silsilah, mesin sekarang berjalan mundur dari angka kerugian `1.2`, menelusuri rantai, dan membagikan turunan berantai (gradien) ke setiap bobot.
- Gradien ini berbisik kepada setiap bobot: *"Kalau kamu dibesarkan sedikit, angka kerugian 1.2 tadi akan naik atau turun?"*
- Setelah semua bobot tahu arah kesalahannya, mereka diperbarui menggunakan Gradient Descent: `bobot = bobot - (learning_rate * gradien)`. Bobot pun bergeser sedikit agar tebakan selanjutnya lebih akurat.

---

### 3. OUTPUT (Hasil Akhir Setelah Dilatih)

Kejadian *Input-Maju-Hukum-Mundur* ini diulang ribuan kali ke seluruh titik cincin. Apa hasil akhirnya?

1. **Secara Angka:** Kalau titik `[0.5, -0.3]` tadi dimasukkan lagi sekarang, hasil tebakan akhirnya tidak lagi `0.2`, tapi mungkin menjadi `-1.8` (menebak cincin dalam dengan sangat yakin).
2. **Secara Geometri (Batas Keputusan):** 8 neuron tersembunyi tadi kini telah memposisikan dirinya menjadi 8 garis lurus yang saling melipat dan mengunci, memagar batas antara cincin dalam dan cincin luar seperti sebuah poligon (segi delapan).
3. **Ongkos (Dinding Komputasi):** Untuk memproses satu kejadian tadi saja, mesinmu harus melahirkan ribuan objek `Value` dan menghabiskan 47 milidetik. Ini sangat mahal untuk data sebesar MNIST di sesi depan.

Itulah alur penuhnya. Kamu tidak sekadar menggunakan mesin *black-box* seperti *Scikit-Learn* di Bulan 0; kamu benar-benar mengontrol setiap perkalian, tekukan ReLU, dan pembagian gradien di setiap milidetiknya menggunakan mesin tulisan tanganmu sendiri.
