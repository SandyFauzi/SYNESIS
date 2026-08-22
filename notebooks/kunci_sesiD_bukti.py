"""Bukti terukur untuk kunci jawaban Sesi D.

Jalankan:
    . .\\scripts\\activate.ps1
    python notebooks\\kunci_sesiD_bukti.py

Berkas ini tidak punya TODO. Isinya enam percobaan yang memisahkan tebakan
yang kedengaran masuk akal dari sebab yang sebenarnya. Tiap bagian menjawab
satu soal Sesi D, dan tiap angkanya bisa kamu produksi ulang sendiri.

Aturan yang dipakai di sini sama dengan aturan seluruh modul: kalau dua
penjelasan sama-sama terdengar benar, rancang percobaan yang hasilnya berbeda
untuk keduanya. Jangan berdebat, ukur.
"""

import time

import numpy as np
import torch

GARIS = "=" * 66


def judul(n, teks):
    print(f"\n{GARIS}\nBUKTI {n}  {teks}\n{GARIS}")


# ══════════════════════════════════════════════════════════════
# BUKTI 1 - "matematika itu absolut" tidak berlaku di float64
# ══════════════════════════════════════════════════════════════

def bukti1():
    judul(1, "aljabar yang sama, algoritma beda, jawaban beda")

    rng = np.random.default_rng(7)
    x = np.sort(rng.uniform(-1, 1, 40))
    y = np.sin(3 * x) + rng.normal(0, 0.1, 40)

    print("  Dua cara menyelesaikan kuadrat terkecil yang SAMA PERSIS di kertas:")
    print("    A. np.linalg.lstsq          -> SVD, lewat LAPACK gelsd")
    print("    B. solve(X.T @ X, X.T @ y)  -> persamaan normal\n")
    print(f"  {'derajat':>8} {'cond(X)':>12} {'cond(X.T X)':>13} {'beda maks':>12}")
    print("  " + "-" * 50)

    for der in [2, 4, 6, 8, 10, 12]:
        X = np.vander(x, der + 1, increasing=True)
        a, *_ = np.linalg.lstsq(X, y, rcond=None)
        G = X.T @ X
        b = np.linalg.solve(G, X.T @ y)
        print(f"  {der:8d} {np.linalg.cond(X):12.3e} {np.linalg.cond(G):13.3e} "
              f"{np.abs(a - b).max():12.3e}")

    print("""
  Kolom terakhir naik ribuan kali lipat padahal rumusnya identik di kertas.
  Sebabnya cond(X.T X) = cond(X) kuadrat: membentuk X.T X membuang separuh
  angka penting sebelum satu pun pembagian dikerjakan.

  Jadi kalau tulisanmu cocok dengan sklearn sampai 1e-16, itu BUKAN karena
  matematika absolut. Itu karena LinearRegression memanggil scipy.linalg.lstsq,
  yang memanggil LAPACK gelsd, rutin yang sama persis dengan np.linalg.lstsq.
  Kalian menempuh jalan yang sama, jadi galat pembulatannya pun sama.""")


# ══════════════════════════════════════════════════════════════
# BUKTI 2 - konvensi alpha sklearn, diuji bukan dipercaya
# ══════════════════════════════════════════════════════════════

def bukti2():
    judul(2, "alpha = lam * n, dan apa akibatnya kalau salah")

    from sklearn.linear_model import Ridge

    rng = np.random.default_rng(3)
    n = 15
    x = np.sort(rng.uniform(-1, 1, n))
    y = np.sin(3 * x) + rng.normal(0, 0.1, n)
    X = np.vander(x, 4, increasing=True)
    lam = 0.1

    # rumus kita: (1/n)||X th - y||^2 + lam * ||th[1:]||^2
    D = np.eye(X.shape[1])
    D[0, 0] = 0.0
    kita = np.linalg.solve(X.T @ X / n + lam * D, X.T @ y / n)

    print(f"  n = {n}, lambda = {lam}\n")
    print(f"  {'alpha sklearn':>18} {'beda maks lawan rumus kita':>30}")
    print("  " + "-" * 50)
    for alpha, label in [(lam, "lam"), (lam * n, "lam * n"), (lam / n, "lam / n")]:
        sk = Ridge(alpha=alpha, fit_intercept=True).fit(X[:, 1:], y)
        th = np.concatenate([[sk.intercept_], sk.coef_])
        print(f"  {label:>10} = {alpha:5.3f} {np.abs(kita - th).max():30.3e}")

    print("""
  Cuma alpha = lam * n yang mendekati nol. Sebabnya satu baris aljabar:

      L_kita   = (1/n) * SSE + lam   * ||th[1:]||^2
      kalikan n di kedua ruas, letak minimumnya tidak bergeser
      n*L_kita =         SSE + lam*n * ||th[1:]||^2
      L_sklearn=         SSE + alpha * ||th[1:]||^2

  Mengalikan seluruh fungsi loss dengan tetapan positif tidak memindahkan
  letak minimumnya. Yang berubah cuma satuan, dan di situlah alpha = lam * n
  lahir. Bukan selera, bukan kesepakatan sembarangan: itu akibat aritmetika
  dari memilih rata-rata atau jumlah.

  fit_intercept=True juga tidak mendenda geseran, sama seperti denda[0] = 0
  di Sesi C. Kalau ini tidak cocok, baris koefisien 0 sendirian yang meleset.""")


# ══════════════════════════════════════════════════════════════
# BUKTI 3 - alasan sebenarnya autograd dipakai: ongkosnya
# ══════════════════════════════════════════════════════════════

def bukti3():
    judul(3, "kenapa mundur sekali mengalahkan maju p+1 kali")

    print("  Beda hingga butuh p+1 kali hitung maju untuk p parameter.")
    print("  Mode mundur butuh 1 kali maju + 1 kali mundur, berapa pun p.\n")
    print(f"  {'p':>7} {'1x maju (ms)':>14} {'backward (ms)':>15} "
          f"{'beda hingga (ms)':>18} {'hemat':>9}")
    print("  " + "-" * 68)

    for p in [10, 100, 1000, 10000]:
        X = torch.randn(200, p, dtype=torch.double)
        y = torch.randn(200, dtype=torch.double)
        th = torch.zeros(p, dtype=torch.double, requires_grad=True)

        def maju():
            with torch.no_grad():
                return ((X @ th - y) ** 2).mean()

        def mundur():
            th.grad = None
            ((X @ th - y) ** 2).mean().backward()

        for _ in range(3):
            maju()
        t0 = time.perf_counter()
        for _ in range(20):
            maju()
        t_maju = (time.perf_counter() - t0) / 20 * 1000

        for _ in range(3):
            mundur()
        t0 = time.perf_counter()
        for _ in range(20):
            mundur()
        t_mundur = (time.perf_counter() - t0) / 20 * 1000

        t_bh = t_maju * (p + 1)
        print(f"  {p:7d} {t_maju:14.4f} {t_mundur:15.4f} {t_bh:18.2f} "
              f"{t_bh / t_mundur:8.0f}x")

    print("""
  Kolom backward nyaris tidak peduli pada p. Kolom beda hingga naik sebanding
  dengan p. Di p = 10000 selisihnya sudah ribuan kali.

  Ini bukan soal kenyamanan. Model bahasa punya miliaran parameter. Dengan
  beda hingga, satu langkah training butuh miliaran kali hitung maju, dan
  latihan yang sekarang makan berminggu-minggu akan makan lebih lama dari
  umur alam semesta. Mode mundur bukan mempercepat hal yang sudah mungkin.
  Ia yang membuat hal itu mungkin sama sekali.

  Harganya memori: graf komputasinya harus disimpan sampai backward selesai.
  Itulah yang memenuhi VRAM saat melatih model besar, bukan bobotnya.""")


# ══════════════════════════════════════════════════════════════
# BUKTI 4 - gradien menumpuk itu LINEAR, ledakannya dari umpan balik
# ══════════════════════════════════════════════════════════════

def bukti4():
    judul(4, "lupa zero_() menumpuk linear, bukan eksponensial")

    torch.manual_seed(0)
    X = torch.randn(30, 3, dtype=torch.double)
    y = torch.randn(30, dtype=torch.double)

    # Percobaan A: theta DIBEKUKAN, cuma backward berulang.
    th = torch.zeros(3, dtype=torch.double, requires_grad=True)
    print("  A. theta dibekukan, backward dipanggil berulang tanpa zero_():\n")
    print(f"  {'panggilan':>10} {'norma grad':>14} {'rasio ke panggilan 1':>22}")
    print("  " + "-" * 50)
    dasar = None
    for k in range(1, 7):
        ((X @ th - y) ** 2).mean().backward()
        norm = th.grad.norm().item()
        if dasar is None:
            dasar = norm
        print(f"  {k:10d} {norm:14.6f} {norm / dasar:22.4f}")

    print("""
  Rasionya 1, 2, 3, 4, 5, 6. Persis bilangan bulat. Menumpuk = penjumlahan
  berulang, dan penjumlahan berulang itu LINEAR, bukan eksponensial.
""")

    def jalan(lr, n_iter, pakai_zero):
        th = torch.zeros(3, dtype=torch.double, requires_grad=True)
        riwayat = []
        for _ in range(n_iter):
            loss = ((X @ th - y) ** 2).mean()
            riwayat.append(loss.item())
            loss.backward()
            with torch.no_grad():
                th.sub_(lr * th.grad)
                if pakai_zero:
                    th.grad.zero_()
        return np.array(riwayat)

    # Percobaan B: loop training sungguhan, theta ikut berubah.
    print("  B. loop training sungguhan, lr = 0.05, dengan dan tanpa zero_():\n")
    print(f"  {'iterasi':>8} {'loss pakai zero_()':>22} {'loss tanpa zero_()':>22}")
    print("  " + "-" * 54)

    benar = jalan(0.05, 40, True)
    salah = jalan(0.05, 40, False)
    for i in [0, 2, 4, 6, 8, 12, 20, 30, 39]:
        print(f"  {i:8d} {benar[i]:22.6f} {salah[i]:22.6f}")

    opt = np.linalg.lstsq(X.numpy(), y.numpy(), rcond=None)[0]
    L_min = float(((X.numpy() @ opt - y.numpy()) ** 2).mean())
    print(f"\n  loss minimum sejati : {L_min:.9f}")

    print("""
  Yang tanpa zero_() TIDAK meledak. Ia turun sebentar, lalu berbalik, lalu
  berayun dan tidak pernah mendarat. Kalau kamu menduga ledakan, dugaan itu
  baru saja dipatahkan datanya sendiri.

  Sebabnya bisa diturunkan di kertas dalam tiga baris. Tanpa zero_(),
  gradien yang dipakai di langkah k adalah jumlah seluruh gradien sebelumnya:

      th[k+1] = th[k] - lr * ( g(th[0]) + ... + g(th[k]) )
      th[k]   = th[k-1] - lr * ( g(th[0]) + ... + g(th[k-1]) )

  Kurangkan baris kedua dari baris pertama, semua suku lama saling hapus:

      th[k+1] - 2*th[k] + th[k-1] = -lr * g(th[k])

  Ruas kiri itu turunan kedua terhadap waktu diskret. Ruas kanan itu gaya.
  Kamu tidak sedang menjalankan penurunan gradien lagi. Kamu sedang
  mengintegrasikan m*a = F dengan m = 1 dan dt^2 = lr, persis skema leapfrog
  yang dipakai di simulasi mekanika.

  Penurunan gradien punya gesekan, jadi ia berhenti di dasar. Hukum Newton
  tanpa gesekan tidak punya alasan untuk berhenti. Massanya jatuh ke dasar
  lembah, kelebihan lajunya membawanya naik ke sisi seberang, dan begitu
  seterusnya selamanya.""")

    # Percobaan C: amplitudo tidak meluruh.
    r = jalan(0.3, 4000, False)
    print("\n  C. lr = 0.3 tanpa zero_(), dijalankan 4000 iterasi:\n")
    print(f"  {'amplitudo ayunan 100 iterasi pertama':<40} "
          f"{r[:100].max() - r[:100].min():.6e}")
    print(f"  {'amplitudo ayunan 100 iterasi terakhir':<40} "
          f"{r[-100:].max() - r[-100:].min():.6e}")
    print("""
  Empat ribu iterasi, amplitudonya praktis tidak berubah. Tidak ada energi
  yang hilang. Itu tanda pasti sistem tak teredam, dan itu cocok dengan
  keadaan marginal yang kamu temukan di Soal 4 Sesi B, cuma di sini ia jadi
  keadaan permanen, bukan satu titik lr yang harus dikenai tepat.
""")

    # Percobaan D: ambang divergensinya justru naik dua kali lipat.
    H = (2 / len(y)) * (X.T @ X).numpy()
    lmax = np.linalg.eigvalsh(H).max()

    def divergen(lr):
        r = jalan(lr, 400, False)
        return (not np.isfinite(r[-1])) or r[-1] > 1e6

    lo, hi = 1.0, 1.4
    for _ in range(40):
        mid = (lo + hi) / 2
        if divergen(mid):
            hi = mid
        else:
            lo = mid

    print("  D. kalau ia osilator, ambang stabilnya harus 4/lambda_max:\n")
    print(f"  {'lambda_max Hessian':<34} {lmax:14.9f}")
    print(f"  {'ambang GD biasa, 2/lambda_max':<34} {2 / lmax:14.9f}")
    print(f"  {'ambang tanpa zero_(), 4/lambda_max':<34} {4 / lmax:14.9f}")
    print(f"  {'ambang terukur, dicari bagi dua':<34} {lo:14.9f}")
    print(f"  {'galat relatif ramalan':<34} "
          f"{abs(lo - 4 / lmax) / (4 / lmax):14.3e}")

    print("""
  Cocok sampai lima angka. Ramalannya keluar dari persamaan ciri
  r^2 - (2 - lr*lambda) r + 1 = 0. Hasil kali akarnya tepat 1, jadi
  amplitudonya memang tidak boleh meluruh, dan akarnya tetap di lingkaran
  satuan selama 0 <= lr*lambda <= 4.

  Jadi lupa zero_() justru MENAIKKAN ambang lr sampai dua kali lipat, sambil
  menghapus kemampuan konvergen sama sekali. Ini gejala yang jahat: modelmu
  tidak error, tidak NaN, tidak meledak. Ia cuma berhenti membaik di angka
  yang salah, dan kamu akan menyalahkan learning rate, arsitektur, atau
  datamu selama berjam-jam sebelum curiga pada satu baris yang hilang.

  Cara mendiagnosisnya ada di percobaan A: bekukan parameternya, panggil
  backward beberapa kali, lihat rasionya. Kalau 1, 2, 3, 4, penumpukan
  terbukti. Kalau tetap 1, penyebabnya di tempat lain.

  Dan penumpukan ini fitur, bukan cacat. Kartumu 4 GB. Untuk melatih dengan
  batch 128 yang tidak muat, jalankan empat batch berisi 32 tanpa zero_(),
  bagi gradiennya empat, baru melangkah. Hasilnya sama dengan batch 128,
  memorinya seperempat. Namanya gradient accumulation, dan ia jadi mungkin
  justru karena PyTorch memilih menumpuk.""")


# ══════════════════════════════════════════════════════════════
# BUKTI 5 - arah geseran riwayat, dipastikan bukan ditebak
# ══════════════════════════════════════════════════════════════

def bukti5():
    judul(5, "siapa mencatat sebelum, siapa mencatat sesudah")

    Xn = np.random.default_rng(1).normal(0, 1, (25, 3))
    yn = np.random.default_rng(2).normal(0, 1, 25)
    th0 = np.zeros(3)
    lr = 0.05

    def mse(th):
        return float(((Xn @ th - yn) ** 2).mean())

    def grad(th):
        return (2 / len(yn)) * (Xn.T @ (Xn @ th - yn))

    # gaya Sesi C: catat SESUDAH melangkah
    th, sesudah = th0.copy(), []
    for _ in range(5):
        th = th - lr * grad(th)
        sesudah.append(mse(th))

    # gaya Sesi D PyTorch: catat SEBELUM melangkah
    th, sebelum = th0.copy(), []
    for _ in range(5):
        sebelum.append(mse(th))
        th = th - lr * grad(th)

    print(f"  loss di titik awal theta0 : {mse(th0):.9f}\n")
    print(f"  {'indeks':>7} {'catat SESUDAH':>16} {'catat SEBELUM':>16}")
    print("  " + "-" * 42)
    for i in range(5):
        print(f"  {i:7d} {sesudah[i]:16.9f} {sebelum[i]:16.9f}")

    a, b = np.array(sesudah), np.array(sebelum)
    print(f"\n  dibandingkan langsung  a[k] lawan b[k]   : {np.abs(a - b).max():.3e}")
    print(f"  digeser                a[k] lawan b[k+1]  : "
          f"{np.abs(a[:-1] - b[1:]).max():.3e}")

    print("""
  Baris pertama kolom SEBELUM sama persis dengan loss di titik awal, karena
  belum satu langkah pun dikerjakan. Kolom SESUDAH melewatkan nilai itu
  selamanya: entri ke-0 miliknya sudah hasil satu pembaruan.

  Jadi a[k] = b[k+1], dan itu sebabnya perbandingan yang cocok adalah
  hn[:-1] lawan hp[1:], bukan sebaliknya. Arahnya bisa dipastikan tanpa
  menebak: cukup lihat mana yang entri pertamanya sama dengan loss awal.

  Panjang keduanya sama, nilai akhir parameternya sama, dan kurvanya bertumpuk
  rapi di skala log. Tidak ada satu pun yang memberi peringatan.""")


# ══════════════════════════════════════════════════════════════
# BUKTI 6 - ongkos tetap GPU bukan PCIe
# ══════════════════════════════════════════════════════════════

def waktu_gpu(fn, n=200, pemanasan=20):
    for _ in range(pemanasan):
        fn()
    torch.cuda.synchronize()
    t0 = time.perf_counter()
    for _ in range(n):
        fn()
    torch.cuda.synchronize()
    return (time.perf_counter() - t0) / n * 1000


def bukti6():
    judul(6, "ongkos tetap GPU: peluncuran kernel, bukan transfer PCIe")

    if not torch.cuda.is_available():
        print("  CUDA tidak tersedia, bagian ini dilewati.")
        return

    dev = torch.device("cuda")
    print(f"  perangkat : {torch.cuda.get_device_name(0)}\n")

    # Klaimnya: 'CPU harus ngirim data ke VRAM lewat PCIe'.
    # Ramalan klaim itu: kalau data tidak pernah ditransfer, ongkosnya hilang.
    X = torch.randn(50, 2, device=dev)
    y = torch.randn(50, device=dev)
    th = torch.zeros(2, device=dev, requires_grad=True)

    def langkah():
        th.grad = None
        ((X @ th - y) ** 2).mean().backward()
        with torch.no_grad():
            th.sub_(1e-3 * th.grad)

    t_langkah = waktu_gpu(langkah)

    a = torch.zeros(1, device=dev)
    t_kernel = waktu_gpu(lambda: a + 1)

    Xc = X.cpu()
    t_kirim_kecil = waktu_gpu(lambda: Xc.to(dev))

    Xbig = torch.randn(50000, 1000)
    t_kirim_besar = waktu_gpu(lambda: Xbig.to(dev), n=20, pemanasan=3)

    # berapa kerja hitung sebenarnya di n=50 d=2
    flop = 2 * 50 * 2 * 3          # maju + mundur, kasarnya
    byte = (50 * 2 + 50 + 2) * 4

    print(f"  {'apa yang diukur':<42} {'ms':>10}")
    print("  " + "-" * 54)
    print(f"  {'satu kernel paling remeh (a + 1)':<42} {t_kernel:10.4f}")
    print(f"  {'satu langkah training n=50 d=2':<42} {t_langkah:10.4f}")
    print(f"  {'transfer 50x2 CPU -> GPU':<42} {t_kirim_kecil:10.4f}")
    print(f"  {'transfer 50000x1000 CPU -> GPU':<42} {t_kirim_besar:10.4f}")

    print(f"""
  Tiga hal yang mematikan klaim PCIe:

  1. Di benchmark Sesi D, X dan y dibuat dengan device=dev. Datanya lahir di
     VRAM dan tidak pernah menyeberang PCIe satu kali pun. Kalau transfer
     penyebabnya, ongkos {t_langkah:.4f} ms itu seharusnya tidak ada.

  2. Kalaupun ditransfer, 50x2 cuma {byte} byte dan makan {t_kirim_kecil:.4f} ms,
     sekitar {t_kirim_kecil / t_langkah * 100:.0f} persen dari ongkos satu langkah.

  3. Satu kernel paling remeh yang bisa ditulis, a + 1, sudah makan
     {t_kernel:.4f} ms. Satu langkah training meluncurkan belasan kernel
     (matmul, kurang, pangkat, rata-rata, lalu pasangan mundurnya, lalu
     pembaruan). Belasan kali {t_kernel:.4f} sudah seukuran {t_langkah:.4f}.

  Hitungan aslinya sendiri sekitar {flop} operasi mengambang. Kartu ini sanggup
  triliunan per detik, jadi bagian menghitungnya selesai dalam waktu yang
  bahkan tidak terukur di sini.

  Kesimpulan: ongkos tetapnya adalah peluncuran kernel plus dispatch Python
  dan CUDA, bukan PCIe. Intuisi PCIe baru benar di baris keempat, transfer
  50000x1000 yang makan {t_kirim_besar:.2f} ms. Di sana ia benar sekali, dan
  itulah alasan kita menaruh data di GPU sekali lalu membiarkannya di sana.""")


if __name__ == "__main__":
    bukti1()
    bukti2()
    bukti3()
    bukti4()
    bukti5()
    bukti6()
    print(f"\n{GARIS}\nSelesai. Tiap angka di kunci-sesiD.md berasal dari sini."
          f"\n{GARIS}")
