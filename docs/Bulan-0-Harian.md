# Bulan 0 — Diagnosa Lingkungan & Rencana Harian

**Periode:** 13–31 Agustus 2026 (19 hari, sebelum perkuliahan mulai)
**Target:** memahami gradient descent sampai ke tulang, dengan kode yang kamu tulis sendiri
**Beban:** ~28 jam · 15 hari aktif · 4 hari istirahat

---

## Bagian I — Diagnosa Lingkungan

### Vonis: **Sangat layak.** Lebih siap dari perkiraan.

Laptopmu sudah punya hampir seluruh fondasi yang dibutuhkan. Temuan terpentingnya:

> **Bulan 0 bisa dimulai hari ini tanpa menginstal apa pun.**
> numpy, matplotlib, scipy, dan scikit-learn semuanya sudah terpasang dan versinya baru.

### Yang sudah ada dan langsung terpakai

| Paket | Versi | Dipakai di |
|---|---|---|
| numpy | 2.4.6 | **Bulan 0–1** — seluruh fondasi |
| matplotlib | 3.10.9 | **Bulan 0** — plot loss & permukaan |
| scipy | 1.17.1 | Bulan 0–3 |
| scikit-learn | 1.9.0 | **Bulan 2** — intent classifier |
| pandas | 3.0.3 | Bulan 2 |
| jupyter / jupyterlab | 4.2.4 | seluruh bulan — eksplorasi |
| sounddevice | 0.5.2 | **Bulan 3** — I/O audio |
| onnxruntime | 1.27.0 | **Bulan 4** — mesin InsightFace |
| pypdf · pymupdf · python-docx · openpyxl | — | **Bulan 6** — metadata |
| psutil · pywin32 | 6.0.0 · 306 | **Bulan 6** — tool sistem |
| PyWavelets | 1.9.0 | Bulan 3 — analisis sinyal |
| manim · pyvista · vtk · plotly | — | **Bulan 0** — visualisasi permukaan loss |
| rich | 14.3.3 | CLI SYNESIS |
| numba · cupy-cuda12x | — | akselerasi |

Kejutan menyenangkan: **manim, pyvista, dan vtk** sudah terpasang. Untuk memvisualisasikan permukaan loss dan menganimasikan lintasan gradient descent di Bulan 0, perkakasnya sudah lebih dari cukup.

### CUDA: terverifikasi berfungsi

```text
cupy CUDA test      : LULUS
CUDA runtime        : 12.9
Compute capability  : 7.5  (Turing — didukung penuh PyTorch)
Driver              : 555.85
```

GPU-mu bukan sekadar terpasang — sudah terbukti bisa dipakai komputasi.

### Perangkat masukan

```text
Mikrofon : 36 perangkat input terdeteksi
           [2] Microphone Array (Realtek) — mikrofon internal, siap untuk Bulan 3
Kamera   : ditunda ke Bulan 4 (butuh cv2)
```

### Yang belum ada

| Paket | Dibutuhkan | Kapan pasang |
|---|---|---|
| **torch / torchvision / torchaudio** | **Bulan 1** | **Hari 1** *(pasang awal, pakai belakangan)* |
| librosa · soundfile | Bulan 3 | Nov |
| opencv-python | Bulan 4 | Des |
| insightface | Bulan 4 | Des |
| faster-whisper · openWakeWord · piper | Bulan 3 | Nov |
| sentence-transformers | Bulan 2 *(opsional)* | Okt |
| Ollama | Bulan 6 | Feb |

Hanya **PyTorch** yang benar-benar mendesak, dan itu pun baru dipakai di Bulan 1.

---

### Tiga temuan yang perlu ditindaklanjuti

#### 1. ⚠️ VRAM sudah terpakai 979 MB saat idle

```text
Total 4096 MB · terpakai 979 MB · tersisa ~3.1 GB
```

Ini mengoreksi asumsi di roadmap. Saya sempat menduga tampilan Windows digerakkan iGPU Radeon sehingga 1650 Ti bebas penuh — ternyata tidak. Pemakainya teridentifikasi:

`wallpaper_engine` · `chrome` · `EpicGamesLauncher` · `steamwebhelper` · `Antigravity` · `explorer`

**Tindakan:** sebelum sesi training, tutup **Wallpaper Engine** dan launcher game. Itu saja biasanya membebaskan 500–700 MB. Untuk Bulan 0–4 tidak kritis (semua latihan muat di 2 GB), tapi akan terasa di Bulan 5–6 saat mini-GPT dan Qwen3-4B berjalan.

#### 2. ⚠️ Wajib venv terpisah — jangan sentuh Python global

Python global-mu berisi **~250 paket**, termasuk perkakas riset fisika yang jelas kamu pakai: `astropy`, `spacepy`, `pyspedas`, `cdflib`, `hapiclient`, `geopack`, `juliacall`, `schroedingerequation`.

**Menginstal PyTorch dan pustaka ML ke lingkungan global berisiko merusak semua itu.** Beberapa pustaka ML nanti akan meminta versi numpy yang lebih rendah, dan pip akan menurunkan versi numpy global tanpa bertanya — lalu tumpukan fisikamu ikut rusak di tengah semester.

**Tindakan:** seluruh proyek ini hidup di `.venv` terpisah. Tidak ada satu pun `pip install` yang dijalankan di luar venv aktif.

#### 3. ⚠️ numpy 2.4.6 dan pandas 3.0.3 sangat baru

Keduanya versi terkini. Sebagian pustaka ML (terutama `librosa` dan `insightface` di Bulan 3–4) kadang tertinggal beberapa bulan dari rilis numpy mayor.

**Tindakan:** venv terpisah sekaligus menyelesaikan masalah ini — kalau nanti butuh numpy versi lebih rendah, turunkan **di dalam venv**, tanpa menyentuh lingkungan fisikamu.

---

### Ringkasan kesiapan

| Aspek | Status |
|---|---|
| CPU (Ryzen 5 4600H, 6C/12T) | ✅ Memadai |
| RAM 15.4 GB | ✅ Lega |
| GPU CUDA 4 GB | ✅ Berfungsi — ⚠️ 3.1 GB efektif |
| Disk (C: 77.7 GB · S: 55.8 GB bebas) | ✅ Cukup |
| Python 3.12.5 + Git | ✅ Siap |
| Fondasi numerik (numpy/scipy/sklearn) | ✅ **Sudah lengkap** |
| PyTorch | ❌ Pasang Hari 1 |
| Mikrofon | ✅ Terdeteksi |
| Isolasi lingkungan | ❌ **Wajib dibuat Hari 1** |

**Tidak ada satu pun penghambat.** Yang kurang hanya venv dan PyTorch, keduanya beres di Hari 1.

---

## Bagian II — Rencana Harian

Pola tiap hari: satu tujuan, tugas konkret, dan definisi selesai yang bisa diperiksa. Kalau satu hari meleset, geser — jangan lompati.

---

### Minggu 1 · Fondasi & numpy (13–16 Agt)

#### Hari 1 — Kamis 13 Agt · 2 jam · *Lingkungan*

- Struktur repo: `synesis/`, `notebooks/`, `data/`, `README.md`, `.gitignore`
- `python -m venv .venv` lalu aktifkan
- **Verifikasi isolasi**: `pip list` di dalam venv harus jauh lebih pendek dari global
- Pasang: `numpy matplotlib scipy scikit-learn jupyter rich`
- Pasang PyTorch (wheel **cu124** — paling aman untuk driver 555.85), lalu **sisihkan; belum dipakai sampai Hari 15**
- `git init` + commit pertama

**Selesai bila:** `python -c "import torch; print(torch.cuda.is_available())"` mencetak `True`, dan `pip list` di venv jauh lebih pendek dari global.

#### Hari 2 — Jumat 14 Agt · 2 jam · *numpy sampai paham*

- Vektor, matriks, broadcasting, slicing
- Tulis dot product manual dengan `for` loop, lalu bandingkan dengan `np.dot` — **ukur selisih waktunya**
- Tulis perkalian matriks manual, bandingkan lagi

**Selesai bila:** kamu bisa menjelaskan aturan broadcasting, dan sudah melihat sendiri vektorisasi puluhan-ratusan kali lebih cepat.

#### Hari 3 — Sabtu 15 Agt · 2 jam · *Data & loss*

- Bangkitkan data sintetis: `y = 3x + 2 + noise`
- Plot dengan matplotlib
- **Tulis fungsi MSE sendiri** — jangan pakai pustaka
- Hitung loss untuk beberapa tebakan `(w, b)` secara manual

**Selesai bila:** punya plot data, dan bisa menghitung loss untuk sembarang `(w, b)`.

#### Hari 4 — Minggu 16 Agt · **ISTIRAHAT**

---

### Sisa Bulan 0 — dipadatkan jadi 4 sesi

> **Direvisi 20 Agustus 2026.** Hari 1 sampai 3 selesai dalam satu hari dengan
> seluruh jawaban benar, termasuk penurunan aljabar dan ramalan perilaku
> divergensi. Ditambah 5 tahun pengalaman C dan Python, rencana harian aslinya
> terlalu lambat. Hari 5 sampai 19 digabung jadi empat sesi.
>
> Yang dipadatkan: bagian yang keterampilanmu sudah menutupinya.
> Yang **tidak** dipadatkan: bagian yang membangun intuisi, karena itu
> pengalaman, bukan tugas.

---

#### Sesi A — Gradient descent utuh · ~3 jam
*Menggantikan Hari 5, 6, 7*

- Turunkan `∂MSE/∂w` dan `∂MSE/∂b` di kertas
- Kode fungsi gradien dari rumus itu
- **Gradient check**: bandingkan analitik lawan beda hingga, target selisih < `1e-6`
- Training loop: hitung loss, hitung gradien, perbarui, ulang

**Selesai bila:** gradient check lolos di bawah `1e-6`, dan training konvergen
ke titik yang sama dari tebakan awal apa pun.

Titik itu `w = 3.018`, `b = 1.744`, bukan `w = 3`, `b = 2`. Gradient descent
mencari dasar permukaan loss, dan permukaan itu dibangun dari 50 titik data
yang sudah digeser acak. Ia tidak pernah diberi tahu parameter asli itu ada.

Gradient check itu teknik yang akan kamu pakai terus sampai Bulan 5. Di Bulan 1
ia menjadi satu-satunya cara memverifikasi mesin autograd buatanmu sendiri.

---

#### Sesi B — Lanskap dan langkah · ~3 jam ⭐
*Menggantikan Hari 8 dan 9*

- Sapu `lr` = 0.0001, 0.01, 0.1, 1.0. Plot semua kurva loss dalam satu grafik
- **Cocokkan dengan ramalanmu di Soal 5c Hari 3**
- Plot permukaan loss `L(w, b)` dalam 3D
- Timpa dengan lintasan gradient descent, lalu animasikan

**Selesai bila:** kamu punya animasi bola menggelinding ke dasar mangkuk, dan
grafik yang menunjukkan `lr` besar melempar keluar.

**Sesi ini tidak boleh dipadatkan lagi.** Melihat lintasan itu bergerak mengubah
gradient descent dari rumus jadi benda yang kamu kenali. Setelah itu kamu tidak
akan pernah lagi menganggapnya abstrak, dan seluruh Bulan 1 sampai 5 berdiri di
atas intuisi ini.

---

#### Sesi C — Multivariat, overfitting, regularisasi · ~3 jam
*Menggantikan Hari 10, 12, 13*

- Perluas ke `X` berbentuk `(n, d)`, tulis ulang penuh dalam bentuk matriks
- Fit polinomial derajat 1, 3, 9, 15 ke data sedikit
- Split train/test, plot kedua loss dalam satu grafik
- Tambahkan suku L2, amati efeknya pada derajat 15

**Selesai bila:** kamu punya grafik dengan **test loss naik sementara train loss
turun**, dan kamu bisa menunjukkan L2 memperbaikinya.

Kamu sudah menjelaskan overfitting dengan benar di Soal 3b secara konsep.
Sesi ini membuatmu **melihatnya terjadi**. Dua hal berbeda.

---

#### Sesi D — Penutup: sklearn, PyTorch, GPU · ~3 jam
*Menggantikan Hari 14, 15, 16*

- Jalankan `LinearRegression` dan `Ridge`, bandingkan koefisiennya dengan hasilmu
- Bandingkan juga dengan `w*` analitik dari Soal 4c Hari 3
- Tulis ulang dengan `torch.tensor` dan `requires_grad=True`
- Panggil `loss.backward()`, **bandingkan gradiennya dengan gradien tanganmu**
- Pindahkan ke `.cuda()`, ukur CPU lawan GPU untuk `d=10` dan `d=1000`

**Selesai bila:** gradien PyTorch cocok dengan gradien tulisanmu dalam `1e-6`,
dan kamu tahu kapan GPU justru kalah dari CPU.

Momen `backward()` cocok dengan turunan tanganmu adalah pintu masuk Bulan 1.
Setelah itu autograd berhenti terasa gaib, dan membangunnya sendiri jadi masuk
akal.

---

#### Rapikan dan tinjau
*Menggantikan Hari 17 dan 19*

Tidak lagi jadi sesi terpisah. Rapikan sambil jalan, dan tulis entri log di
akhir tiap sesi sesuai aturan di README.

Satu hal yang tetap perlu waktu khusus: **susun pertanyaan untuk dosen Machine
Learning dan DSP** soal menjadikan modul proyek ini sebagai tugas besar.
Lakukan di minggu pertama kuliah, sebelum topik tugas ditetapkan.

---

## Bagian III — Yang Tidak Boleh Dilakukan Bulan Ini

1. **Jangan `pip install` di luar venv.** Tumpukan fisikamu (astropy, spacepy, pyspedas) taruhannya.
2. **Jangan menonton kursus ML.** Kamu akan lupa sebelum sempat memakainya. Tulis kode.
3. **Jangan pakai PyTorch sebelum Hari 15.** Seluruh nilai Bulan 0 ada pada menulisnya sendiri lebih dulu.
4. **Jangan lompat ke neural network.** Regresi linear dulu sampai benar-benar paham — semua yang datang setelahnya adalah gagasan yang sama, bertingkat.
5. **Jangan mengejar kerapian kode.** Cukup berjalan dan bisa kamu jelaskan. Rapikan di Hari 17.

---

## Bagian IV — Tolok Ukur Bulan 0

Di akhir 31 Agustus, kamu seharusnya bisa menjawab tanpa membuka catatan:

- [ ] Kenapa loss function itu **permukaan energi potensial**?
- [ ] Apa yang terjadi kalau learning rate terlalu besar, dan **kenapa**?
- [ ] Bagaimana cara memeriksa gradienmu benar tanpa mempercayainya begitu saja?
- [ ] Kenapa test loss bisa naik saat train loss turun?
- [ ] Apa sebenarnya yang dilakukan `loss.backward()` di PyTorch?
- [ ] Kapan GPU **tidak** membantu?

Kalau enam-enamnya terjawab, fondasi untuk lima bulan berikutnya sudah kokoh.
