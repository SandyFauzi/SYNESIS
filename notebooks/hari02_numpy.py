"""Hari 2 - numpy sampai paham.

Cara pakai:
    . .\\activate.ps1
    python notebooks\\hari02_numpy.py

Bagian bertanda TODO kamu yang isi. Jangan lihat np.dot dulu.
Tujuannya bukan menghasilkan kode benar, tapi tahu kenapa kode benar itu cepat.
"""

import time

import numpy as np

GARIS = "=" * 62


# ══════════════════════════════════════════════════════════════
# BAGIAN 1 - kenapa array bukan list
# ══════════════════════════════════════════════════════════════

def bagian1():
    print(GARIS, "\nBAGIAN 1  array vs list\n", GARIS, sep="")

    lst = [1, 2, 3, 4]
    arr = np.array([1, 2, 3, 4])

    print(f"list  : {lst}   tipe elemen bebas, isinya penunjuk ke objek Python")
    print(f"array : {arr}   satu dtype, satu blok memori berurutan")
    print(f"dtype   : {arr.dtype}")
    print(f"shape   : {arr.shape}")
    print(f"strides : {arr.strides}   <- lompatan byte antar elemen")
    print(f"nbytes  : {arr.nbytes}")

    # Inilah sumber kecepatannya. Elemen array duduk berdampingan di memori,
    # jadi CPU bisa menarik beberapa sekaligus ke cache dan mengolahnya dengan
    # satu instruksi vektor. List Python menyimpan alamat, bukan angka, jadi
    # tiap elemen perlu satu lompatan ke tempat lain.

    print(f"\n2D shape  : {np.arange(12).reshape(3, 4).shape}")
    print(f"2D strides: {np.arange(12).reshape(3, 4).strides}")


# ══════════════════════════════════════════════════════════════
# BAGIAN 2 - broadcasting
# ══════════════════════════════════════════════════════════════

def bagian2():
    print("\n" + GARIS, "\nBAGIAN 2  broadcasting\n", GARIS, sep="")

    # ATURANNYA, disejajarkan dari kanan:
    #   1. Dimensi sama            -> cocok
    #   2. Salah satunya 1         -> diregangkan
    #   3. Selain itu              -> error
    #
    #   (3,4) dan   (4,)  ->  (3,4)     baris (4,) diulang 3 kali
    #   (3,1) dan   (1,4) ->  (3,4)     keduanya diregangkan
    #   (3,4) dan   (3,)  ->  ERROR     4 lawan 3 di posisi paling kanan

    A = np.arange(12).reshape(3, 4)
    v = np.array([10, 20, 30, 40])
    u = np.array([100, 200, 300])

    # TODO 2a: sebelum menjalankan, TULIS tebakanmu di sini.
    #   A + v            -> shape ?
    #   A + u            -> shape ?
    #   A + u[:, None]   -> shape ?
    #   Baru jalankan dan bandingkan.

    print(f"A shape          : {A.shape}")
    print(f"A + v            : {(A + v).shape}")
    print(f"A + u[:, None]   : {(A + u[:, None]).shape}")
    try:
        _ = A + u
        print("A + u            : berhasil (tidak seharusnya)")
    except ValueError as e:
        print(f"A + u            : ERROR  ->  {e}")

    # Jebakan yang akan menggigitmu di Bulan 1.
    # Keduanya JALAN, tanpa error, tapi hasilnya beda arti.
    a = np.array([1, 2, 3])
    print(f"\na[:, None] shape : {a[:, None].shape}   kolom")
    print(f"a[None, :] shape : {a[None, :].shape}   baris")
    print(f"a[:, None] + a[None, :] -> {(a[:, None] + a[None, :]).shape}   matriks 3x3")
    # Saat menulis backprop nanti, salah satu di antara dua bentuk ini akan
    # menghasilkan angka yang kelihatan wajar tapi salah. Tidak ada error.
    # Cara menangkapnya cuma satu: selalu cetak .shape saat ragu.


# ══════════════════════════════════════════════════════════════
# BAGIAN 3 - dot product tulis tangan
# ══════════════════════════════════════════════════════════════

def dot_manual(a, b):
    """Hasil kali dalam dua vektor 1D, pakai loop Python murni.

    Yang sama persis dengan <psi|phi> di Fisika Kuantum:
        sum(a[i] * b[i]) untuk semua i

    TODO 3: isi fungsi ini. Dilarang memakai np.dot atau np.sum.
    """
    raise NotImplementedError("TODO 3")


def matmul_manual(A, B):
    """Perkalian matriks (n,k) x (k,m) -> (n,m), loop Python murni.

    C[i,j] = sum(A[i,k] * B[k,j]) untuk semua k

    TODO 4: isi fungsi ini. Tiga loop bersarang.
    """
    raise NotImplementedError("TODO 4")


# ══════════════════════════════════════════════════════════════
# BAGIAN 4 - adu cepat
# ══════════════════════════════════════════════════════════════

def ukur(fn, *args, ulang=1):
    mulai = time.perf_counter()
    for _ in range(ulang):
        hasil = fn(*args)
    return hasil, (time.perf_counter() - mulai) / ulang


def bagian4():
    print("\n" + GARIS, "\nBAGIAN 4  adu cepat\n", GARIS, sep="")

    rng = np.random.default_rng(42)

    for n in (1_000, 100_000, 1_000_000):
        a, b = rng.random(n), rng.random(n)
        try:
            h_manual, t_manual = ukur(dot_manual, a, b)
        except NotImplementedError:
            print("  TODO 3 belum diisi, lewati adu cepat")
            return
        h_numpy, t_numpy = ukur(np.dot, a, b, ulang=10)

        assert abs(h_manual - h_numpy) < 1e-6, "hasilmu beda dari numpy"
        print(f"  n = {n:>9,}   manual {t_manual * 1e3:8.2f} ms   "
              f"numpy {t_numpy * 1e3:7.3f} ms   "
              f"numpy menang {t_manual / t_numpy:6.0f}x")

    print()
    for n in (50, 100, 200):
        A, B = rng.random((n, n)), rng.random((n, n))
        try:
            C_manual, t_manual = ukur(matmul_manual, A, B)
        except NotImplementedError:
            print("  TODO 4 belum diisi, lewati")
            return
        C_numpy, t_numpy = ukur(lambda x, y: x @ y, A, B, ulang=10)

        assert np.allclose(C_manual, C_numpy), "hasilmu beda dari numpy"
        print(f"  {n}x{n}   manual {t_manual * 1e3:9.2f} ms   "
              f"numpy {t_numpy * 1e3:7.3f} ms   "
              f"numpy menang {t_manual / t_numpy:6.0f}x")

    print("""
  Kenapa selisihnya sejauh itu:

  1. Loop Python menafsirkan ulang bytecode tiap iterasi. numpy menyerahkan
     seluruh perhitungan ke BLAS, pustaka C dan Fortran yang sudah dikompilasi.
  2. BLAS memakai instruksi SIMD, satu instruksi memproses 4 sampai 8 angka.
  3. Matriks dipecah jadi blok agar muat di cache CPU. Kamu sudah kenal ide ini
     dari Komputasi Numerik.

  Perhatikan juga: makin besar n, makin lebar jaraknya. Ongkos tetap numpy
  tertutupi, sementara loop Python tumbuh linear.""")


if __name__ == "__main__":
    bagian1()
    bagian2()
    bagian4()
