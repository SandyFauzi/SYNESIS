# Soal Sesi D - Pembanding, PyTorch, dan GPU (Penutup Bulan 0)

Berkas latihan: [`sesiD_pytorch.py`](sesiD_pytorch.py)

Malam ini kita nge-adu kodingan manual yang udah kita capek-capek bikin dari Sesi A-C sama monster industri: **Scikit-Learn** dan **PyTorch**.

---

## Soal 1 - Tulisanmu vs Scikit-Learn

**1a. Kenapa pas dibandingin di Regresi Biasa (tanpa denda), angkanya identik sampai desimal ke-9?**
> **Jawaban:** Karena di *under the hood*, Scikit-Learn `LinearRegression` pakai solusi aljabar linier (Least Square) yang sama persis kayak yang kita tulis pakai `np.linalg.lstsq`. Lebih tepatnya, keduanya bermuara ke rutin LAPACK yang sama (`gelsd`), jadi bukan cuma matematikanya yang identik, tapi jalur komputasi *floating point*-nya pun persis satu langkah. Kalau Scikit-Learn memilih jalur lain (misal persamaan normal `X.T @ X`), di derajat tinggi hasilnya bisa beda di angka keenam karena *condition number* yang dikuadratkan membuang separuh angka penting.

**1b. Di regresi Ridge, Scikit-Learn butuh parameter `alpha = lam * n` biar hasilnya sama kayak rumus kita. Kenapa Scikit-Learn nggak pakai `lambda` murni aja?**
> **Jawaban:** Ini murni masalah **konvensi (kesepakatan)**. Di rumus matriks kita, nilai *error* (MSE) dan *denda* kita bagi dengan jumlah data ($n$) biar nilainya jadi rata-rata. Scikit-Learn milih jalan beda: mereka menghitung total jumlah kuadrat murni tanpa dibagi $n$. Makanya, denda mereka (`alpha`) harus dikalikan $n$ biar setara sama denda rata-rata kita (`lambda`). Beda konvensi sering bikin panik programmer pemula, dikiranya *bug*, padahal cuma beda satuan!

---

## Soal 2 - PyTorch `loss.backward()` Buka-Bukaan

**2a. Gradien manual yang kita turunin berjam-jam di kertas ternyata dicari sama persis oleh PyTorch `loss.backward()` sampai batas ketelitian mesin. Gimana cara PyTorch nemuin angkanya tanpa disuapin rumus aljabar kita?**
> **Jawaban:** PyTorch NGGAK pakai *Symbolic Math* (nggak ngerjain turunan aljabar di kertas). Dia pakai **Autograd** (Diferensiasi Otomatis / Graf Komputasi). Tiap kali kita ngaliin atau nambahin tensor, PyTorch diem-diem nyatet "jejak" operasinya di memori. Pas kita panggil `.backward()`, dia tinggal jalan mundur ngikutin jejak tadi pakai **Aturan Rantai (Chain Rule)** dari kalkulus dasar. Makanya dia bisa sepresisi hitungan analitik, tapi otomatis!

**2b. Kenapa `theta.grad.zero_()` wajib dipanggil di setiap akhir loop?**
> **Jawaban:** Karena desain *default* PyTorch itu **menumpuk (mengakumulasi)** nilai gradien, BUKAN menimpanya. Tapi akumulasinya bersifat **linier**, bukan eksponensial: kalau kita bekukan `theta` dan panggil `backward()` berulang, norma gradiennya naik dengan rasio 1, 2, 3, 4, bukan 1, 2, 4, 8. Efek di *training loop* sungguhan juga bukan ledakan. Rekurensi `theta` berubah dari orde satu jadi orde dua: `th[k+1] - 2*th[k] + th[k-1] = -lr * g(th[k])`, yang secara fisika itu persamaan **osilator tak teredam** (Hukum Newton tanpa gesekan). Loss-nya turun sebentar, lalu berayun bolak-balik di sekitar minimum tanpa pernah mendarat, dengan ambang *learning rate* aman bergeser dari `2/lambda_max` ke `4/lambda_max`. Nggak ada NaN, nggak ada *error*, dan itu justru yang bikin bahayanya sulit terdeteksi.

---

## Soal 3 - Ilusi Riwayat Loss (Geser Satu Iterasi)

**3a. Buka `figures/sesiD_dua_loop.png`. Kurva PyTorch dan Numpy kelihatan sama persis, tapi aslinya kalau dicocokin langsung selisihnya gede. Cuma pas digeser satu iterasi baru cocok (selisih nyaris 0). Kok bisa?**
> **Jawaban:** Ini murni kelakuan urutan kode. Di versi Numpy kita, kita ngehitung *Loss* **setelah** kita ngelangkah (`theta = theta - lr*grad`). Sedangkan di PyTorch, kita nyatet *Loss* dari kondisi **sebelum** ngelangkah. Jadi, kurvanya murni fungsi yang sama, cuma selisih satu detik (satu iterasi) pencatatan aja. Makanya di Sesi A dulu dibilang, urutan naruh fungsi `.append()` bisa nipu pas bikin grafik perbandingan!

---

## Soal 4 - Kapan GPU Kalah Sama CPU?

**4a. Liat tabel perbandingan kecepatan dan grafik `figures/sesiD_cpu_gpu.png`. Kenapa buat jumlah data kecil ($n=50$, $d=2$), GPU justru lebih lambat dari CPU laptop biasa?**
> **Jawaban:** Bukan karena transfer PCIe! Di kode `sesiD_pytorch.py`, tensor `X`, `y`, dan `th` semuanya dibuat langsung di VRAM (`device=dev`) dan nggak pernah menyeberang PCIe satu kali pun. Penyebab sebenarnya adalah **ongkos peluncuran kernel** (*kernel launch overhead*). Tiap operasi tensor (matmul, kurang, pangkat, rata-rata, lalu pasangan mundurnya) harus melewati dispatcher PyTorch, disusun jadi perintah CUDA, dikirim ke antrean driver GPU, dijadwalkan, lalu disinkronkan. Satu kernel paling remeh (`a + 1`) aja makan sekitar 0.02 ms. Satu langkah training kecil meluncurkan belasan kernel, jadi totalnya sekitar 0.6 ms, padahal hitungan aslinya (600 operasi *floating point*) selesai dalam waktu yang bahkan nggak terukur oleh GPU yang sanggup triliunan FLOPS. Intuisi PCIe tetap benar tapi tempatnya beda: transfer baru jadi bottleneck kalau datanya raksasa (misal matriks `50000 x 1000` yang makan 31 ms untuk ditransfer).

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
