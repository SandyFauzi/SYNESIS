# Prosedur: memasang model suara ke SYNESIS

Catatan teknis, 26 Agustus 2026. Isinya bukan cerita melainkan urutan
langkah, lengkap dengan perintah dan pemeriksanya, supaya bisa diulang dari
nol kalau `E:\SYNESIS\models` hilang.

Yang dipasang:

```text
Yukinoshita_Yukino.pth   55 MB    RVC v2, 250 epoch, 40 kHz, pitch-guided
Piper id_ID-news_tts     63 MB    yang mengucapkan kalimatnya
Piper en_US-amy          63 MB
Piper ja_JA-hi_fi_captain 77 MB
ContentVec               378 MB   HuBERT, pemisah isi ucapan dari identitas
faster-whisper small     486 MB   pengenal ucapan
```

---

## Langkah 0 — Membaca apa yang sebenarnya ada

Sebelum memasang apa pun, berkasnya dibuka dan ditanya ia model apa. Ini
langkah yang paling sering dilewati orang, dan yang menentukan seluruh sisa
prosedurnya.

```python
import torch
d = torch.load(r"E:\SYNESIS\models\voice\yukino\Yukinoshita_Yukino.pth",
               map_location="cpu", weights_only=False)
print(list(d.keys()))
print(d["config"], d["sr"], d["f0"], d["version"], d["info"])
```

Keluarannya:

```text
['weight', 'config', 'info', 'sr', 'f0', 'version']
config  [1025, 32, 192, 192, 768, 2, 6, 3, 0, '1', [3,7,11],
         [[1,3,5],[1,3,5],[1,3,5]], [10,10,2,2], 512, [16,16,4,4],
         109, 256, 40000]
sr      '40k'      f0  1      version 'v2'      info '250epoch'
```

Dari satu baris itu seluruh arsitekturnya sudah tertentu:

| isi config | arti | akibatnya |
| --- | --- | --- |
| `version v2`, `768` | ciri masukan 768 dimensi | butuh ContentVec, bukan HuBERT v1 |
| `f0 = 1` | pitch-guided | butuh penaksir nada dasar |
| `40000` | laju keluaran 40 kHz | dekoder menaikkan laju 400 kali |
| `[10,10,2,2]` | empat tahap upsample | 10x10x2x2 = 400, dan 400 cuplikan pada 40 kHz = 10 ms = satu bingkai |
| `109` | 109 slot pembicara | `emb_g`, dipakai indeks 0 |
| `192, 192, 768, 2, 6` | laten, tersembunyi, filter, kepala, lapisan | ukuran encoder |

Lalu kuncinya dihitung, karena jumlah kunci adalah peta modulnya:

```python
import collections
print(collections.Counter(k.split(".")[0] for k in d["weight"]))
# Counter({'dec': 243, 'enc_p': 113, 'flow': 100, 'emb_g': 1})   total 457
```

Tiga blok: encoder, aliran balik, dekoder. Itu VITS.

---

## Langkah 1 — Mencoba jalan yang sudah ada, dan mencatat kegagalannya

Dua paket siap pakai dicoba lebih dulu. Keduanya gagal, dan keduanya gagal di
tahap penyelesaian dependensi, bukan di tahap pemakaian:

```powershell
python -m pip install --dry-run rvc-python
#   rvc-python -> fairseq==0.12.2
#   fairseq 0.12.2 tidak punya wheel untuk Python 3.12, harus dikompilasi

python -m pip install --dry-run rvc-inferpy
#   ERROR: ResolutionImpossible
#   rvc-inferpy -> faiss-cpu==1.7.3
#   Additionally, some packages in these conflicts have no matching
#   distributions available for your environment: faiss-cpu
```

Pilihan yang tersisa dua:

1. pasang Python 3.10 khusus untuk satu paket, lalu jalankan RVC di proses
   terpisah;
2. tulis lintasan inferensinya sendiri.

Yang dipilih nomor dua, dan alasannya bisa diukur: nomor satu menambah satu
lingkungan Python penuh (sekitar 3 GB dengan torch-nya sendiri) dan satu batas
proses yang harus dilewati tiap kali SYNESIS bicara. Nomor dua menambah satu
berkas 699 baris.

---

## Langkah 2 — Mengganti tiga bagian yang tidak bisa dipasang

RVC asli memakai tiga hal yang tidak tersedia. Masing-masing dicarikan
gantinya, dan tiap penggantian dicatat konsekuensinya.

| yang tidak ada | penggantinya | konsekuensi |
| --- | --- | --- |
| fairseq, untuk memuat HuBERT | `transformers.HubertModel` + bobot `lengyue233/content-vec-best` | tidak ada; keluarannya lapisan yang sama |
| RMVPE, untuk nada dasar | YIN, ditulis sendiri di `rvc.py` | konsonan tak bersuara lebih sering salah |
| faiss, untuk retrieval | dilewati | setara `index_rate = 0`, konsonan kurang tajam |

### ContentVec

```python
from transformers import HubertModel
m = HubertModel.from_pretrained("lengyue233/content-vec-best")
ciri = m(gelombang_16k).last_hidden_state          # (1, T, 768)
```

Dua rincian yang menentukan dan mudah salah:

- **Jangan normalisasi masukannya.** `config.json` model ini menyebut
  `feat_extract_norm: "group"`, yang setara `do_normalize = False`. Sinyal
  masuk apa adanya dalam rentang [-1, 1].
- **Yang dipakai `last_hidden_state`, bukan `final_proj`.** Untuk RVC v2 yang
  dibutuhkan keluaran lapisan ke-12 sebesar 768 dimensi. `final_proj` milik
  v1 dan berdimensi 256; `transformers` akan melaporkannya sebagai
  `UNEXPECTED` waktu memuat, dan laporan itu benar serta boleh diabaikan.

Ciri itu lalu dinaikkan lajunya dua kali lipat, dari 20 ms jadi 10 ms per
bingkai, supaya sejajar dengan kisi nada dasar dan dengan 400 cuplikan per
bingkai di dekoder.

### YIN untuk nada dasar

Ditulis sendiri, dan memakai teorema konvolusi dari Bulan 3 Sesi 1 supaya
murah: fungsi selisih YIN

```text
d(tau) = e(0) + e(tau) - 2 r(tau)
```

dihitung dari autokorelasi `r` lewat FFT, bukan dari gelung bersarang. Tanpa
itu, 100 bingkai per detik tidak bisa dikejar.

Pemeriksanya di `rvc._demo()`: nada murni yang diketahui harus ditemukan
dalam 2 persen.

```text
YIN menemukan 110 Hz -> 110.6 Hz
YIN menemukan 220 Hz -> 220.6 Hz
YIN menemukan 440 Hz -> 440.6 Hz
sunyi -> tak bersuara
```

---

## Langkah 3 — Menyalin arsitekturnya, kunci demi kunci

Aturannya satu dan tidak boleh dilanggar: **nama atribut modul harus persis
sama dengan awalan kunci di dalam `.pth`.** Nama yang enak dibaca manusia
ditaruh di komentar, bukan di kode.

| kunci .pth | kelas di `rvc.py` | isinya |
| --- | --- | --- |
| `enc_p.*` | `TextEncoder768` | Linear 768→192, embedding nada, 6 lapisan perhatian posisi relatif, proj ke 384 |
| `flow.flows.{0,2,4,6}.*` | `ResidualCouplingBlock` | 4 lapisan gandeng, diselingi pembalikan kanal |
| `dec.*` | `GeneratorNSF` | NSF-HiFiGAN, 4 tahap upsample, 12 resblock |
| `emb_g.*` | `nn.Embedding(109, 256)` | identitas pembicara |

Tiga hal yang gampang salah dan tidak menghasilkan pesan galat:

1. **Flip di aliran balik tidak punya bobot.** Kunci `.pth` cuma ada di
   indeks 0, 2, 4, 6, jadi indeks ganjil diisi `nn.Identity()` sebagai tempat
   kosong. Urutan pembalikannya: flip, RCL6, flip, RCL4, flip, RCL2, flip,
   RCL0.
2. **`conv_post` tidak punya bias.** Kunci `dec.conv_post.bias` memang tidak
   ada, jadi `bias=False`.
3. **`weight_norm` disimpan sebagai pasangan `weight_g` dan `weight_v`.**
   Keduanya digabung sekali di awal jadi `weight` biasa:

```python
weight = weight_v * (weight_g / ||weight_v||)
```

Penggabungan itu menurunkan jumlah kunci dari 457 jadi 353, dan membuat
seluruh modul di `rvc.py` jadi `Conv1d` biasa. Satu lapis kerumitan hilang,
dan inferensinya sedikit lebih cepat.

---

## Langkah 4 — Verifikasi berjenjang

Tiga pemeriksa, disusun dari yang paling lemah ke yang paling menggigit.
Urutannya sengaja: yang lemah cepat dan menangkap kesalahan besar, yang
menggigit lambat dan menangkap kesalahan halus.

### 4a. Kunci dan bentuk

```powershell
python -m synesis.rvc
```

```text
353 kunci, 0 hilang, 0 berlebih; bentuk tiap tensor cocok
```

Menyingkirkan hampir semua kesalahan struktural: lapisan kurang, kanal salah,
kernel keliru, urutan tertukar.

**Yang TIDAK dibuktikannya:** bahwa tensornya dipakai dengan cara yang benar.
Bentuk `(192, 192, 1)` cocok untuk `conv_q` maupun `conv_k`; menukar keduanya
lolos pemeriksaan ini.

### 4b. Nada keluaran mengikuti nada masukan

```text
selisih nada median   -4 sen
dalam 50 sen          74,4 persen bingkai bersuara
```

Empat sen tidak terdengar manusia. Ini membuktikan dekoder benar-benar
memakai eksitasi f0 yang diberikan. Kalau `SourceModuleHnNSF` salah, atau
`noise_convs` tersambung ke tahap yang keliru, keluarannya akan berdesis atau
bernada tetap.

**Yang TIDAK dibuktikannya:** warna suaranya.

### 4c. Whisper membaca kembali keluarannya

Pemeriksa yang menutup perkara, dan yang tidak bisa ditipu: model pengenal
ucapan yang tidak tahu apa-apa tentang RVC diminta membaca hasilnya.

```text
masukan Piper -> "Halo Sandy, laporan praktikum minggu lalu sudah saya buka."
keluaran RVC  -> "Halo Sandy, laporan 4 tikung minggu lalu sudah saya buka."
```

Sepuluh dari sebelas kata terbaca. Itu mustahil terjadi kalau ada bagian
menentukan yang salah.

Diulang untuk tiga bahasa:

```text
en  piper  -> Good evening, Sandy. I am Sineces. Your lab report ... already open.
en  yukino -> Good evening, Sandy. I am Sineces. Your lab report ... already open.
id  piper  -> Halo Sandy, saya Shinesis. Naporan praktikku minggu lalu sudah saya buka.
id  yukino -> Halo Sandy, saya Shenezis. Laporan Paktikum Minggu lalu sudah saya buka.
```

Baris `en` identik kata per kata. Baris `id yukino` justru lebih benar
daripada keluaran Piper-nya sendiri.

---

## Langkah 5 — Memilih sumber suaranya

RVC mengganti WARNA suara; ia tidak membuat ucapan dari teks. Jadi butuh
sesuatu yang berbicara lebih dulu.

| calon | ditolak/dipakai | alasan |
| --- | --- | --- |
| SAPI5 Windows | ditolak | cuma ada `Zira` dan `David`, keduanya en-US. Bahasa Indonesia akan dibaca dengan fonetik Inggris |
| edge-tts | ditolak | butuh internet, melanggar syarat luring |
| **Piper** | **dipakai** | luring, punya suara `id_ID`, dan `piper-tts` punya wheel untuk Python 3.12 |

Konsekuensi rancangannya, dan ini yang membuat tiga bahasa jadi murah:

```text
Piper menentukan  BAHASA dan IRAMA
RVC   menentukan  WARNA SUARA
```

Menambah bahasa cuma menambah satu berkas `.onnx`, dan orangnya tetap sama.
Bahasa Jepang butuh `pyopenjtalk-plus`; paket aslinya `pyopenjtalk` tidak
punya wheel untuk Python 3.12.

---

## Langkah 6 — Memasangnya ke SYNESIS

Satu fungsi, tiga tahap, dan tiap tahap bisa dimatikan sendiri-sendiri.

```python
def ucap(teks, mainkan_juga=True, simpan=None, model=None):
    x, laju = sintesis(teks, model)                       # Piper
    if konfig.RVC_AKTIF and Path(konfig.RVC_MODEL).exists() and len(x):
        x, laju = warnai(x, laju)                         # RVC
    if mainkan_juga and len(x):
        mainkan(x, laju)                                  # speaker
```

Setelannya di `konfig.py`:

```python
PIPER_SUARA = {"id": ..., "en": ..., "ja": ...}
RVC_MODEL   = GUDANG / "models" / "voice" / "yukino" / "Yukinoshita_Yukino.pth"
RVC_AKTIF   = True
RVC_NADA    = 0        # geseran semiton
```

Ketiga model dimuat sekali lalu disimpan sebagai variabel modul, karena muat
pertamanya mahal dan pemakaian berikutnya murah:

```text
              muat pertama   sesudah panas   RTF
Piper              4,15 s         0,28 s     0,07
faster-whisper     8,21 s         2,60 s        —   ongkos TETAP, lihat catatan
RVC (GPU)         22,31 s         0,42 s     0,11
RVC (CPU)              —          6,63 s     1,66

Catatan: kolom RTF sengaja kosong untuk Whisper. Ia menambahkan bantalan
sampai 30 detik sebelum menghitung mel, jadi ongkosnya tidak bergantung pada
panjang ucapan: 2,48 detik untuk ucapan 1 detik, 2,60 detik untuk 8 detik.
Memakai RTF untuk model semacam ini menghasilkan anggaran yang salah, dan
itu pernah terjadi di dokumen ini.
```

Baris terakhir yang menentukan satu penyimpangan dari Roadmap: RTF 1,66 di
CPU berarti lebih lambat daripada waktu nyata, jadi RVC memakai GPU meskipun
Roadmap menjanjikan seluruh Bulan 3 di CPU. `RVC_AKTIF = False` mengembalikan
janji itu dengan harga suara Piper polos.

---

## Langkah 7 — Dua tabrakan yang tidak ada di dokumentasi mana pun

### 7a. Dua cuDNN dalam satu proses

```text
Could not load symbol cudnnGetLibConfig. Error code 127
```

Muncul kalau `faster-whisper` dipanggil lebih dulu lalu RVC. torch dan
ctranslate2 masing-masing membawa salinan cuDNN sendiri, dan Windows
menyelesaikan simbol DLL berdasarkan yang termuat duluan.

Tambalannya satu konvolusi, dipanggil sebelum Whisper dimuat:

```python
def _panaskan_cudnn():
    F.conv2d(torch.zeros(1, 1, 8, 8, device="cuda"),
             torch.zeros(1, 1, 3, 3, device="cuda"))
    torch.cuda.synchronize()
```

`torch.cuda.is_available()` tidak cukup: ia menyentuh driver CUDA, bukan
cuDNN. Yang menyentuh cuDNN adalah operasi yang memakainya.

Ditandai `ponytail:` beserta cara memeriksa kapan ia boleh dihapus: hapus
panggilannya, jalankan `transkrip` lalu `warnai` dalam satu proses, lihat
apakah pesannya muncul.

### 7b. Cache HuggingFace kembar

ContentVec terunduh dua kali, 378 MB masing-masing, karena tiga tempat
menyebut jalur cache dan salah satunya berbeda. Sekarang ketiganya satu
jalur, dan semuanya `setdefault` sehingga `HF_HOME` yang sudah disetel
pengguna tetap menang:

```text
synesis/konfig.py   os.environ.setdefault("HF_HOME", str(HF_CACHE))
synesis/luncur.py   lingkungan.setdefault("HF_HOME", r"E:\SYNESIS\.cache\huggingface")
SYNESIS.cmd         if "%HF_HOME%"=="" set HF_HOME=E:\SYNESIS\.cache\huggingface
```

Pemeriksanya: jalankan dengan jaringan dimatikan dari sisi huggingface. Kalau
masih ada yang kurang, ia gagal, bukan mengunduh.

```powershell
$env:HF_HUB_OFFLINE=1
python -m synesis.suara ucap "Uji luring."
```

---

## Mengulang dari nol

Kalau `E:\SYNESIS\models` hilang, urutannya begini.

```powershell
cd "S:\Code\Make A Jarvis"
. .\scripts\activate.ps1

# 1. suara Piper
python - <<'PY'
import urllib.request, pathlib
tuj = pathlib.Path(r"E:/SYNESIS/models/voice/piper"); tuj.mkdir(parents=True, exist_ok=True)
base = "https://huggingface.co/rhasspy/piper-voices/resolve/main/"
for b in ("id/id_ID/news_tts/medium/id_ID-news_tts-medium.onnx",
          "id/id_ID/news_tts/medium/id_ID-news_tts-medium.onnx.json",
          "en/en_US/amy/medium/en_US-amy-medium.onnx",
          "en/en_US/amy/medium/en_US-amy-medium.onnx.json",
          "ja/ja_JA/hi_fi_captain/medium/ja_JA-hi_fi_captain-medium.onnx",
          "ja/ja_JA/hi_fi_captain/medium/ja_JA-hi_fi_captain-medium.onnx.json"):
    urllib.request.urlretrieve(base + b, tuj / pathlib.Path(b).name)
PY

# 2. model RVC: salin sendiri ke E:\SYNESIS\models\voice\yukino\

# 3. ContentVec dan Whisper terunduh sendiri saat pertama dipakai
python -m synesis.rvc                  # periksa 353 kunci
python -m synesis.suara ucap "Halo."   # muat semuanya, sekitar 70 detik
```

Paket yang dibutuhkan, dan yang sengaja TIDAK dipasang, tercatat di kepala
`requirements.txt`.

---

## Yang belum dikerjakan

`added_IVF1102_Flat_nprobe_1_Yukinoshita_Yukino_v2.index`, 136 MB, ada di
folder model dan tidak disentuh sama sekali.

Akibatnya terukur: `praktikum` terbaca `4 tikung`. Retrieval mempertajam
konsonan, dan itu tersangka utamanya. Dua tersangka lain: YIN lebih sering
salah daripada RMVPE pada konsonan tak bersuara, dan model ini dilatih pada
suara Jepang sehingga fonem Indonesia diucapkan dengan pendekatan terdekat.

Cara memisahkan ketiganya ada di
[soal-bulan3-sesi5.md](notebooks/soal-bulan3-sesi5.md) Soal 4c: ukur ulang
dengan f0 dari `torchcrepe` sebagai ganti YIN. Kalau kejelasannya melompat,
tersangka keduanya yang benar. Kalau tidak, yang perlu dikerjakan adalah
membaca berkas `.index` itu tanpa faiss.

---

## Berkas yang terlibat

| berkas | perannya |
| --- | --- |
| [`synesis/rvc.py`](synesis/rvc.py) | arsitektur RVC v2, YIN, kelas `Yukino` |
| [`synesis/suara.py`](synesis/suara.py) | `sintesis`, `warnai`, `ucap`, dan tambalan cuDNN |
| [`synesis/konfig.py`](synesis/konfig.py) | jalur model, `RVC_AKTIF`, `RVC_NADA`, `PIPER_SUARA` |
| [`notebooks/kunci_b3_bukti.py`](notebooks/kunci_b3_bukti.py) | Uji F, pemeriksa 353 kunci dan YIN |
| [`notebooks/soal-bulan3-sesi5.md`](notebooks/soal-bulan3-sesi5.md) | Soal 4 dan 5, penalaran di balik keputusannya |
| [`synesis/MANUAL.md`](synesis/MANUAL.md) | cara memakainya sehari-hari |
