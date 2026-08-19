# Hari 2 bonus - memisahkan dua variabel yang tercampur
#
# Jalankan:  julia notebooks\hari02_bonus_julia.jl
#
# Perbandingan Python lawan numpy mencampur dua hal sekaligus:
#   (a) ditafsir lawan dikompilasi
#   (b) algoritma naif lawan SIMD dan pemblokan cache (BLAS)
#
# Berkas ini menulis algoritma yang PERSIS SAMA dengan matmul_manual milikmu,
# tapi dalam bahasa yang dikompilasi. Yang berubah cuma (a). Selisih yang
# tersisa terhadap BLAS adalah (b).

using LinearAlgebra

const GARIS = "="^62

# Julia memakai indeks mulai dari 1, bukan 0. Selain itu strukturnya identik
# dengan matmul_manual di hari02_numpy.py.

function dot_naif(a, b)
    total = 0.0
    for i in 1:length(a)
        total += a[i] * b[i]
    end
    return total
end

function matmul_naif(A, B)
    n, k = size(A)
    k2, m = size(B)
    @assert k == k2 "dimensi dalam tidak cocok"
    C = zeros(n, m)
    for i in 1:n
        for j in 1:m
            total = 0.0
            for kk in 1:k
                total += A[i, kk] * B[kk, j]
            end
            C[i, j] = total
        end
    end
    return C
end

# Versi kedua: urutan loop dibalik agar cocok dengan tata letak memori Julia.
#
# numpy menyimpan baris secara berurutan (row-major, seperti C).
# Julia menyimpan kolom secara berurutan (column-major, seperti Fortran).
#
# Ingat strides di Bagian 1. Loop paling dalam sebaiknya menyusuri indeks yang
# paling rapat di memori. Di Julia indeks itu adalah i, bukan kk.

function matmul_kolom(A, B)
    n, k = size(A)
    k2, m = size(B)
    @assert k == k2 "dimensi dalam tidak cocok"
    C = zeros(n, m)
    for j in 1:m
        for kk in 1:k
            b = B[kk, j]
            @inbounds for i in 1:n
                C[i, j] += A[i, kk] * b
            end
        end
    end
    return C
end

# Pengukuran. Panggilan pertama di Julia memuat waktu kompilasi JIT, jadi selalu
# ada satu putaran pemanasan yang dibuang sebelum mengukur.

function ukur(f, args...; ulang=5)
    hasil = f(args...)               # pemanasan, memicu kompilasi JIT
    t_min = Inf
    for _ in 1:ulang
        # Hasilnya WAJIB ditampung. Kalau dibuang, kompilator Julia berhak
        # menghapus seluruh perhitungan dan waktunya jadi nol palsu.
        t = @elapsed (hasil = f(args...))
        t_min = min(t_min, t)
    end
    return hasil, t_min * 1000       # milidetik
end

function main()
    println(GARIS)
    println("BONUS  Julia lawan Python lawan BLAS")
    println(GARIS)
    println("Julia ", VERSION, "   thread BLAS: ", Sys.CPU_THREADS)

    # Angka Python dari mesin yang sama, untuk pembanding
    py_dot = Dict(1_000 => 0.31, 100_000 => 39.06, 1_000_000 => 291.74)
    py_mat = Dict(50 => 44.32, 100 => 349.42, 200 => 2813.98)

    println("\n", GARIS)
    println("DOT PRODUCT")
    println(GARIS)
    println(rpad("n", 12), rpad("Python naif", 14), rpad("Julia naif", 14),
            rpad("Julia BLAS", 14), "Julia menang")
    for n in (1_000, 100_000, 1_000_000)
        a, b = rand(n), rand(n)
        _, t_naif = ukur(dot_naif, a, b)
        _, t_blas = ukur(dot, a, b)      # LinearAlgebra.dot, benar-benar BLAS
        println(rpad(string(n), 12),
                rpad(string(round(py_dot[n], digits=2), " ms"), 14),
                rpad(string(round(t_naif, digits=3), " ms"), 14),
                rpad(string(round(t_blas, digits=3), " ms"), 14),
                t_naif > 0 ? string(round(Int, py_dot[n] / t_naif), "x") : "terlalu cepat")
    end

    println("\n", GARIS)
    println("PERKALIAN MATRIKS")
    println(GARIS)
    println(rpad("ukuran", 12), rpad("Python naif", 14), rpad("Julia naif", 14),
            rpad("Julia kolom", 14), "Julia BLAS")
    for n in (50, 100, 200)
        A, B = rand(n, n), rand(n, n)
        C1, t_naif = ukur(matmul_naif, A, B)
        C2, t_kol = ukur(matmul_kolom, A, B)
        C3, t_blas = ukur(*, A, B)
        @assert isapprox(C1, C3) "matmul_naif salah"
        @assert isapprox(C2, C3) "matmul_kolom salah"
        println(rpad("$(n)x$(n)", 12),
                rpad(string(round(py_mat[n], digits=1), " ms"), 14),
                rpad(string(round(t_naif, digits=3), " ms"), 14),
                rpad(string(round(t_kol, digits=3), " ms"), 14),
                round(t_blas, digits=3), " ms")
    end

    n = 200
    A, B = rand(n, n), rand(n, n)
    _, t_naif = ukur(matmul_naif, A, B)
    _, t_kol = ukur(matmul_kolom, A, B)
    _, t_blas = ukur(*, A, B)
    py = py_mat[n]

    println("\n", GARIS)
    println("PEMBAGIAN JURANG, pada 200x200")
    println(GARIS)
    println("""
  Python naif  -> Julia naif   : $(round(py / t_naif, digits=0))x
      Algoritmanya identik. Selisih ini murni ongkos penafsir Python.

  Julia naif   -> Julia kolom  : $(round(t_naif / t_kol, digits=1))x
      Algoritma sama, urutan loop diubah agar cocok tata letak memori.
      Ini efek cache murni, tanpa mengubah jumlah operasi sama sekali.

  Julia kolom  -> BLAS         : $(round(t_kol / t_blas, digits=1))x
      Sisa keunggulan BLAS: SIMD, pemblokan cache berlapis, multithread.

  Total Python -> BLAS         : $(round(py / t_blas, digits=0))x

  Kesimpulan yang bisa kamu tarik sendiri dari angka di atas:
  berapa bagian dari jurang itu soal BAHASA, dan berapa soal ALGORITMA?
""")
end

main()
