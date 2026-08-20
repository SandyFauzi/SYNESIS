# Handoff

## Goal
Menyelesaikan Sesi C (Multivariat, Regularisasi L2) dan Sesi D (PyTorch vs Numpy, GPU vs CPU) dari kurikulum SYNESIS Bulan 0. Sesi ini dikerjakan oleh Antigravity menggantikan Claude yang terkena limit.

## Decisions and rationale
- Semua kodingan diubah ke bentuk matriks (Least Squares).
- Regularisasi L2 dimodelkan sebagai Energi Potensial Pegas (Hukum Hooke).
- Soal-soal dijawab secara natural/kasual dengan penjelasan fisika mendalam yang relevan dengan latar belakang Fisika Komputasi user (IPK 3.70).
- Membuktikan Scikit-Learn dan PyTorch `loss.backward()` memakai fundamental matematika yang sama persis dengan kode buatan sendiri (Numpy).

## Current state
- `sesiC_multivariat.py` dan `sesiD_pytorch.py` berhasil diisi dan berjalan sukses.
- `soal-sesiC.md` dan `soal-sesiD.md` lengkap terjawab.
- Bulan 0 (Dasar Gradient Descent) secara resmi tamat.

## Important files and commands
- `notebooks/sesiC_multivariat.py`
- `notebooks/soal-sesiC.md`
- `notebooks/sesiD_pytorch.py`
- `notebooks/soal-sesiD.md`

## Open items and risks
- Bersiap masuk ke Bulan 1 untuk membangun mesin Autograd (Micrograd) dari nol.

## Suggested next prompt
"Lanjut Bulan 1! Buka silabusnya dan ayo bikin Micrograd dari nol."
