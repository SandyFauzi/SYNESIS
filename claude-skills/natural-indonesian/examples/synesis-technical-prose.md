# Regression example: SYNESIS technical prose

Use this example when checking whether technical Indonesian has drifted into literal translation, mixed register, or unnecessary metaphor.

## Terminology failures

Avoid:

> Kalimat diubah menjadi vektor lewat kantong kata.

Prefer:

> Kalimat diubah menjadi vektor menggunakan Bag of Words (BoW).

Avoid:

> Sesi 2 menambahkan himpunan uji terpisah, matriks bingung, dan ambang keyakinan.

Prefer:

> Sesi 2 menambahkan data uji terpisah, confusion matrix, dan confidence threshold agar model dapat menolak prediksi dengan confidence yang terlalu rendah.

Avoid:

> SYNESIS memilih kelas berongkos harapan terkecil.

Prefer:

> SYNESIS memilih kelas dengan expected cost paling rendah.

Or, for a more Indonesian rendering:

> SYNESIS memilih kelas dengan biaya ekspektasi paling rendah.

Avoid:

> Aturan tangan mengambil objek, waktu, dan jam dari kalimat.

Prefer:

> Ekstraksi slot menggunakan aturan manual untuk mengambil objek, waktu, dan jam dari kalimat.

Avoid:

> Sebelum alat dipanggil masih ada tiga pagar.

Prefer:

> Sebelum tool dipanggil, sistem masih menjalankan tiga lapisan pengaman.

Avoid:

> Isi kepalanya hanya sebelas ribu angka.

Prefer:

> Model linear tersebut hanya memiliki 11.850 parameter.

Avoid:

> Semua percobaan mendarat di pita 36 sampai 56 persen.

Prefer:

> Semua percobaan menghasilkan akurasi dalam rentang 36 sampai 56 persen.

## Register failures

Avoid mixing:

> Model ini hanya memakai satu matriks, tetapi hasilnya cuma benar 56,1 persen.

Choose one register:

> Model ini hanya menggunakan satu matriks, tetapi akurasinya hanya 56,1 persen.

Do not vary `hanya` into `cuma` merely to avoid repetition.

## Metaphor failures

Avoid:

> Graf itu ingat siapa berasal dari siapa.

Prefer:

> Graf tersebut mencatat dependensi antaroperasi.

For a beginner audience, add the analogy after the precise statement:

> Graf tersebut mencatat dependensi antaroperasi. Secara sederhana, setiap hasil menyimpan informasi tentang operasi dan nilai yang membentuknya.

## Preferred paragraph style

Prefer:

> Kalimat diubah menjadi vektor menggunakan Bag of Words (BoW). Setiap kata dalam vocabulary menempati satu fitur, dengan nilai yang menunjukkan frekuensi kemunculannya. Output jaringan kemudian dilewatkan ke softmax sehingga menghasilkan distribusi probabilitas untuk setiap intent. Model dilatih menggunakan cross-entropy loss, dengan gradien terhadap logit yang dapat disederhanakan menjadi `p - y`.

This style keeps Indonesian grammar natural while preserving the terminology practitioners actually use.
