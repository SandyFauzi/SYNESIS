# Bulan 1 Sesi 1–4 — visual code walkthrough

Pipeline gabungan:

1. `manim_scenes.py` merender empat loop konsep matematika.
2. `generate_storyboard.py` membaca setiap baris nonkosong dari tiga notebook.
3. Remotion menyelaraskan visual, penjelasan, dan penyorot kode.
4. Hasil akhir: `video/keluaran/bulan1-sesi1-4-visual.mp4`.

Format mengikuti contoh Tower of Hanoi: vertikal 720×1280, visual di atas,
kode aktif di bawah, 30 fps. Tidak memakai voice-over; seluruh penjelasan ada
di layar.

## Cakupan final

- Sesi 1: autograd buatan sendiri, backward, finite difference, PyTorch.
- Sesi 2: neuron, layer, MLP, ReLU, training, dan neuron mati.
- Sesi 3: softmax MNIST, dinding waktu/rekursi, backward iteratif.
- Sesi 4: Tensor NumPy, operasi matriks, gradient check, dan optimizer.
- 1.526 baris nonkosong ditampilkan satu per satu selama 13:00.

Jalankan ulang `generate_storyboard.py` setelah notebook berubah, lalu
`npm run render`. Empat aset Manim berada di `public/manim`.
