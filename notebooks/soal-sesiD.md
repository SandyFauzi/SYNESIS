# Soal Sesi D - Pembanding, PyTorch, dan GPU (Penutup Bulan 0)

Berkas latihan: [`sesiD_pytorch.py`](sesiD_pytorch.py)

Malam ini kita nge-adu kodingan manual yang udah kita capek-capek bikin dari Sesi A-C sama monster industri: **Scikit-Learn** dan **PyTorch**.

---

## Soal 1 - Tulisanmu vs Scikit-Learn

**1a. Kenapa pas dibandingin di Regresi Biasa (tanpa denda), angkanya identik sampai desimal ke-9?**
> **Jawaban:** Karena di *under the hood*, Scikit-Learn `LinearRegression` pakai solusi aljabar linier (Least Square) yang sama persis kayak yang kita tulis pakai `np.linalg.lstsq`. Matematika itu absolut, gak peduli siapa yang ngoding, hasilnya pasti sama.

**1b. Di regresi Ridge, Scikit-Learn butuh parameter `alpha = lam * n` biar hasilnya sama kayak rumus kita. Kenapa Scikit-Learn nggak pakai `lambda` murni aja?**
> **Jawaban:** Ini murni masalah **konvensi (kesepakatan)**. Di rumus matriks kita, nilai *error* (MSE) dan *denda* kita bagi dengan jumlah data ($n$) biar nilainya jadi rata-rata. Scikit-Learn milih jalan beda: mereka menghitung total jumlah kuadrat murni tanpa dibagi $n$. Makanya, denda mereka (`alpha`) harus dikalikan $n$ biar setara sama denda rata-rata kita (`lambda`). Beda konvensi sering bikin panik programmer pemula, dikiranya *bug*, padahal cuma beda satuan!

---

## Soal 2 - PyTorch `loss.backward()` Buka-Bukaan

**2a. Gradien manual yang kita turunin berjam-jam di kertas ternyata dicari sama persis oleh PyTorch `loss.backward()` sampai batas ketelitian mesin. Gimana cara PyTorch nemuin angkanya tanpa disuapin rumus aljabar kita?**
> **Jawaban:** PyTorch NGGAK pakai *Symbolic Math* (nggak ngerjain turunan aljabar di kertas). Dia pakai **Autograd** (Diferensiasi Otomatis / Graf Komputasi). Tiap kali kita ngaliin atau nambahin tensor, PyTorch diem-diem nyatet "jejak" operasinya di memori. Pas kita panggil `.backward()`, dia tinggal jalan mundur ngikutin jejak tadi pakai **Aturan Rantai (Chain Rule)** dari kalkulus dasar. Makanya dia bisa sepresisi hitungan analitik, tapi otomatis!

**2b. Kenapa `theta.grad.zero_()` wajib dipanggil di setiap akhir loop?**
> **Jawaban:** Karena desain *default* PyTorch itu **menumpuk (mengakumulasi)** nilai gradien, BUKAN menimpanya. Kalau lupa di-nol-kan, gradien dari iterasi 1 bakal ditambah sama gradien iterasi 2, iterasi 3, dst. Hasilnya gaya dorongnya (gradien) jadi membesar eksponensial dan kelereng kita bakal mental melesat ke luar angkasa tanpa ngeluarin peringatan *error* satupun!

---

## Soal 3 - Ilusi Riwayat Loss (Geser Satu Iterasi)

**3a. Buka `figures/sesiD_dua_loop.png`. Kurva PyTorch dan Numpy kelihatan sama persis, tapi aslinya kalau dicocokin langsung selisihnya gede. Cuma pas digeser satu iterasi baru cocok (selisih nyaris 0). Kok bisa?**
> **Jawaban:** Ini murni kelakuan urutan kode. Di versi Numpy kita, kita ngehitung *Loss* **setelah** kita ngelangkah (`theta = theta - lr*grad`). Sedangkan di PyTorch, kita nyatet *Loss* dari kondisi **sebelum** ngelangkah. Jadi, kurvanya murni fungsi yang sama, cuma selisih satu detik (satu iterasi) pencatatan aja. Makanya di Sesi A dulu dibilang, urutan naruh fungsi `.append()` bisa nipu pas bikin grafik perbandingan!

---

## Soal 4 - Kapan GPU Kalah Sama CPU?

**4a. Liat tabel perbandingan kecepatan dan grafik `figures/sesiD_cpu_gpu.png`. Kenapa buat jumlah data kecil ($n=50$, $d=2$), GPU justru lebih lambat dari CPU laptop biasa?**
> **Jawaban:** Karena ngelempar kerjaan ke GPU itu ada **"Ongkos Administrasi"** (Ongkos Tetap). CPU harus ngirim data ke VRAM GPU lewat kabel *motherboard* (PCIe bus), nyuruh GPU nyalain *kernel*, nunggu GPU selesai, terus mindahin datanya balik ke RAM. Kalau datanya kecil (kayak cuma 50 titik), waktu ngitung aslinya cuma sekejap, tapi waktu transfer datanya (ongkos tetapnya) kelamaan. GPU baru balik modal (menang jauh dari CPU) kalau ukuran datanya raksasa (misal puluhan ribu baris) di mana ongkos transfer ketutup sama kecepatan ngitung paralel ribuan core-nya. Makanya di Bulan 0 ini, mending setia sama CPU!

---

## Tolok Ukur Sesi D

- [x] Regresi Linear Scikit-Learn dipahami punya fondasi sama dengan kode tulisan tangan.
- [x] Perbedaan konvensi (faktor $n$ dan denda bias) pada Scikit-Learn disadari.
- [x] Misteri `loss.backward()` berhasil dibedah sebagai Graf Komputasi, bukan gaib.
- [x] Bahaya numpuk gradien (lupa `zero_()`) pada PyTorch diresapi.
- [x] Ilusi perbedaan grafik karena urutan pencatatan terpecahkan.
- [x] Alasan lambatnya GPU di data kecil (Ongkos VRAM) dikuasai secara fisik.

**PENUTUP BULAN 0:**
Fisika sudah membuktikan diri sebagai penguasa fundamental dari AI! Gradien udah dihitung pakai tangan, matriksnya dibikin sendiri, *overfitting* ditaklukkan pakai gaya pegas. Bulan depan, kita bakal bikin *Autograd* (otaknya PyTorch) pakai tangan kita sendiri dari nol!
