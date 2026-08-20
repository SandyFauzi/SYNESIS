"""Sesi B - lanskap dan langkah.

Jalankan:
    . .\\activate.ps1
    python notebooks\\sesiB_lanskap.py

Sesi A memberi kamu angka. Sesi ini memberi kamu gambar.

Tujuannya satu: mengubah gradient descent dari rumus jadi benda yang kamu
kenali bentuknya. Setelah melihat lintasannya bergerak, kamu tidak akan
pernah lagi menganggap "menuruni permukaan loss" sebagai kiasan.

Berkas ini memakai ulang buat_data, prediksi, mse dari Hari 3, serta
gradien dan latih dari Sesi A. Kalau yang di sana benar, yang di sini
ikut benar.

Bagian bertanda TODO kamu yang isi.
"""

import time
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.animation import FuncAnimation, PillowWriter  # noqa: E402

from hari03_data_loss import B_ASLI, W_ASLI, buat_data, mse, prediksi  # noqa: E402
from sesiA_gradient_descent import latih  # noqa: E402

GARIS = "=" * 62
FIGUR = Path(__file__).resolve().parent.parent / "figures"
FIGUR.mkdir(exist_ok=True)


# ══════════════════════════════════════════════════════════════
# BAGIAN 1 - bangun permukaannya
# ══════════════════════════════════════════════════════════════

def permukaan_loss(x, y, ws, bs):
    """Hitung MSE untuk tiap pasangan (w, b) pada kisi.

    ws berbentuk (nw,), bs berbentuk (nb,).
    Kembalikan array L berbentuk (nb, nw), dengan

        L[j, i] = mse(prediksi(x, ws[i], bs[j]), y)

    Perhatikan urutan indeksnya. Baris untuk b, kolom untuk w. Itu
    konvensi yang dipakai contourf dan plot_surface, dan kalau kamu
    membaliknya gambarnya akan tampak masuk akal tapi salah sumbu.
    Ini jenis bug yang tidak melempar error.

    Versi ini boleh pakai loop bersarang. Yang penting benar dulu.
    Versi cepatnya ada di TODO 3.

    TODO 1
    """
    raise NotImplementedError("permukaan_loss")


def sumbu_utama(x):
    """Matriks Hessian permukaan loss, beserta nilai dan vektor eigennya.

    Kamu sudah menyusun matriks ini di Soal 5d Sesi A:

        H = [[2A, 2*x_rata], [2*x_rata, 2]]     dengan A = (1/n) * jumlah x^2

    Kembalikan tuple (H, nilai_eigen, vektor_eigen) dari np.linalg.eigvalsh
    dan np.linalg.eigh. Vektor eigen ada di KOLOM hasil eigh, bukan baris.

    Kenapa Hessian tidak bergantung pada y sama sekali, padahal loss jelas
    bergantung pada y? Itu Soal 3.

    TODO 2
    """
    raise NotImplementedError("sumbu_utama")


def permukaan_loss_vektor(x, y, ws, bs):
    """Versi tanpa loop sama sekali, memakai broadcasting.

    Ini lanjutan langsung dari Hari 2. Idenya: susun ketiga sumbu supaya
    numpy bisa menyiarkan semuanya sekaligus.

        ws  -> bentuk (1, nw, 1)
        bs  -> bentuk (nb, 1, 1)
        x   -> bentuk (1, 1, n)

    Ramalan model jadi berbentuk (nb, nw, n), lalu rata-ratakan kuadrat
    residunya sepanjang sumbu terakhir.

    Ingat aturan broadcasting dari Hari 2: sejajarkan dari kanan, tiap
    dimensi harus sama atau salah satunya 1.

    Kembalikan array berbentuk (nb, nw), harus sama persis dengan
    keluaran permukaan_loss.

    TODO 3, boleh dilewati kalau waktumu habis. Tapi jangan dilewati
    kalau alasannya cuma karena terasa sulit.
    """
    raise NotImplementedError("permukaan_loss_vektor")


def bagian1(x, y):
    print(GARIS, "\nBAGIAN 1  membangun permukaan\n", GARIS, sep="")

    ws = np.linspace(-2, 8, 120)
    bs = np.linspace(-4, 8, 120)

    t0 = time.perf_counter()
    L = permukaan_loss(x, y, ws, bs)
    t_loop = time.perf_counter() - t0

    print(f"  bentuk kisi   : {L.shape}   (baris = b, kolom = w)")
    print(f"  versi loop    : {t_loop * 1000:8.2f} ms")

    j, i = np.unravel_index(L.argmin(), L.shape)
    print(f"  dasar di kisi : w = {ws[i]:.4f}, b = {bs[j]:.4f}, loss = {L.min():.6f}")

    try:
        t0 = time.perf_counter()
        Lv = permukaan_loss_vektor(x, y, ws, bs)
        t_vek = time.perf_counter() - t0
        cocok = np.allclose(L, Lv)
        print(f"  versi vektor  : {t_vek * 1000:8.2f} ms   "
              f"({t_loop / max(t_vek, 1e-12):.1f} kali lebih cepat)")
        print(f"  hasil identik : {cocok}")
        if not cocok:
            print(f"  selisih maks  : {np.abs(L - Lv).max():.3e}   "
                  f"periksa lagi urutan sumbunya")
    except NotImplementedError:
        print("  versi vektor  : belum diisi (TODO 3)")

    return ws, bs, L


# ══════════════════════════════════════════════════════════════
# BAGIAN 2 - permukaan 3D
# ══════════════════════════════════════════════════════════════

def bagian2(ws, bs, L):
    print("\n" + GARIS, "\nBAGIAN 2  mangkuk dalam 3D\n", GARIS, sep="")

    W, B = np.meshgrid(ws, bs)

    fig = plt.figure(figsize=(11, 4.6))

    ax = fig.add_subplot(121, projection="3d")
    ax.plot_surface(W, B, L, cmap="viridis", alpha=0.85,
                    linewidth=0, antialiased=True, rstride=2, cstride=2)
    ax.set_xlabel("w"); ax.set_ylabel("b"); ax.set_zlabel("MSE")
    ax.set_title("linear")
    ax.view_init(elev=32, azim=-125)

    ax2 = fig.add_subplot(122, projection="3d")
    ax2.plot_surface(W, B, np.log10(L), cmap="viridis", alpha=0.85,
                     linewidth=0, antialiased=True, rstride=2, cstride=2)
    ax2.set_xlabel("w"); ax2.set_ylabel("b"); ax2.set_zlabel("log10 MSE")
    ax2.set_title("skala log")
    ax2.view_init(elev=32, azim=-125)

    plt.tight_layout()
    plt.savefig(FIGUR / "sesiB_permukaan3d.png", dpi=110, bbox_inches="tight")
    plt.close()
    print("  plot disimpan : figures/sesiB_permukaan3d.png")

    print("""
  Buka gambarnya sekarang, jangan nanti.

  Panel kiri adalah mangkuknya. Panel kanan mangkuk yang sama dalam skala
  log, dan di situ bentuk lonjongnya jauh lebih jelas. Ini bukan mangkuk
  bundar. Ia parit memanjang.

  Bentuk lonjong itulah bilangan kondisi 8 yang kamu hitung di Soal 5d
  Sesi A, sekarang dalam wujud yang bisa dilihat mata.""")


# ══════════════════════════════════════════════════════════════
# BAGIAN 3 - lintasan di atas kontur
# ══════════════════════════════════════════════════════════════

def bagian3(x, y, ws, bs, L):
    print("\n" + GARIS, "\nBAGIAN 3  lintasan gradient descent\n", GARIS, sep="")

    W, B = np.meshgrid(ws, bs)
    aras = np.logspace(np.log10(L.min() + 1e-9), np.log10(L.max()), 28)

    daftar = [(0.01, "tab:blue"), (0.06, "tab:orange"), (0.12, "tab:red")]

    fig, sumbu = plt.subplots(1, 3, figsize=(15, 4.6), sharex=True, sharey=True)

    print(f"  {'lr':>6}  {'iterasi':>8}  {'panjang lintasan':>17}  {'loss akhir':>11}")
    print("  " + "-" * 50)

    for ax, (lr, warna) in zip(sumbu, daftar):
        _, _, riwayat = latih(x, y, -1.0, 6.0, lr, 60)
        wt = np.array([r[1] for r in riwayat])
        bt = np.array([r[2] for r in riwayat])

        ax.contour(W, B, L, levels=aras, colors="0.75", linewidths=0.6)
        ax.plot(wt, bt, "-o", color=warna, ms=3, lw=1.2, alpha=0.9)
        ax.plot(wt[0], bt[0], "ks", ms=8, label="mulai")
        ax.plot(W_ASLI, B_ASLI, "g*", ms=14, label="parameter asli")
        j, i = np.unravel_index(L.argmin(), L.shape)
        ax.plot(ws[i], bs[j], "rx", ms=10, mew=2, label="dasar loss")
        ax.set_title(f"lr = {lr}")
        ax.set_xlabel("w")
        ax.grid(alpha=0.25)

        panjang = np.sum(np.hypot(np.diff(wt), np.diff(bt)))
        print(f"  {lr:6}  {len(riwayat):8}  {panjang:17.4f}  {riwayat[-1][3]:11.6f}")

    sumbu[0].set_ylabel("b")
    sumbu[0].legend(fontsize=8, loc="upper right")
    plt.tight_layout()
    plt.savefig(FIGUR / "sesiB_lintasan.png", dpi=110, bbox_inches="tight")
    plt.close()
    print("\n  plot disimpan : figures/sesiB_lintasan.png")

    print("""
  Tiga panel, tiga perilaku, satu permukaan yang sama.

  Yang kiri merayap mulus. Yang tengah mulai membelok. Yang kanan
  menggergaji bolak-balik melintasi parit sambil perlahan maju ke dasar.

  Kolom panjang lintasan mengukur jarak tempuh sebenarnya. Bandingkan
  dengan jarak lurus dari titik mulai ke dasar. Selisihnya adalah ongkos
  yang kamu bayar karena permukaannya lonjong.

  Perhatikan juga bintang hijau dan silang merah tidak berhimpit. Yang
  dituju gradient descent adalah silang merah, dan itu penjelasan Soal 4
  Sesi A dalam bentuk gambar.""")


# ══════════════════════════════════════════════════════════════
# BAGIAN 4 - sumbu utama parit
# ══════════════════════════════════════════════════════════════

def bagian4(x, y, ws, bs, L):
    print("\n" + GARIS, "\nBAGIAN 4  kenapa lintasannya menggergaji\n", GARIS, sep="")

    H, lam, vek = sumbu_utama(x)

    print("  Hessian:")
    print(f"    [[{H[0,0]:8.4f}, {H[0,1]:8.4f}],")
    print(f"     [{H[1,0]:8.4f}, {H[1,1]:8.4f}]]")
    print(f"\n  nilai eigen      : {lam[0]:.4f} (landai), {lam[1]:.4f} (curam)")
    print(f"  bilangan kondisi : {lam[1] / lam[0]:.4f}")
    print(f"  lr kritis        : 2/{lam[1]:.4f} = {2 / lam[1]:.6f}")

    W, B = np.meshgrid(ws, bs)
    aras = np.logspace(np.log10(L.min() + 1e-9), np.log10(L.max()), 28)
    j, i = np.unravel_index(L.argmin(), L.shape)
    w0, b0 = ws[i], bs[j]

    plt.figure(figsize=(7.5, 6))
    plt.contour(W, B, L, levels=aras, colors="0.78", linewidths=0.6)

    _, _, riwayat = latih(x, y, -1.0, 6.0, 0.12, 60)
    plt.plot([r[1] for r in riwayat], [r[2] for r in riwayat],
             "-o", color="tab:red", ms=3, lw=1.2, alpha=0.55, zorder=2,
             label="lr = 0.12")

    for k, warna, nama in [(0, "tab:green", "landai"), (1, "tab:purple", "curam")]:
        v = vek[:, k]
        panjang = 4.0 / np.sqrt(lam[k])
        plt.annotate("", xy=(w0 + v[0] * panjang, b0 + v[1] * panjang),
                     xytext=(w0 - v[0] * panjang, b0 - v[1] * panjang),
                     arrowprops=dict(arrowstyle="<->", color=warna, lw=3.2),
                     zorder=6)
        plt.plot([], [], color=warna, lw=3.2,
                 label=f"sumbu {nama}, lambda = {lam[k]:.2f}")

    plt.plot(w0, b0, "rx", ms=11, mew=2.4)
    plt.xlabel("w"); plt.ylabel("b")
    plt.title("Sumbu utama parit dan lintasan yang menggergaji")
    plt.legend(fontsize=9); plt.grid(alpha=0.25)
    plt.savefig(FIGUR / "sesiB_sumbu_utama.png", dpi=110, bbox_inches="tight")
    plt.close()
    print("\n  plot disimpan    : figures/sesiB_sumbu_utama.png")

    print("""
  Dua panah itu sumbu utama parit, dan panjangnya sengaja dibuat
  berbanding terbalik dengan akar nilai eigen. Panah panjang berarti arah
  landai, panah pendek berarti arah curam.

  Sekarang lihat lintasan merahnya. Gergajinya berayun sejajar panah
  pendek, dan kemajuan sebenarnya merayap sejajar panah panjang.

  Itulah seluruh masalahnya dalam satu gambar. Learning rate dibatasi dari
  atas oleh arah curam, karena arah itu yang meledak duluan. Tapi arah
  landai butuh langkah besar supaya tidak merayap selamanya. Satu angka
  melayani dua kebutuhan yang bertentangan.

  Adam dan RMSprop lahir untuk memecahkan tepat masalah ini, dengan cara
  memberi tiap parameter panjang langkahnya sendiri. Kamu akan menulisnya
  di Bulan 1, dan sekarang kamu sudah tahu untuk apa.""")

    return lam


# ══════════════════════════════════════════════════════════════
# BAGIAN 5 - animasi
# ══════════════════════════════════════════════════════════════

def bagian5(x, y, ws, bs, L):
    print("\n" + GARIS, "\nBAGIAN 5  animasi\n", GARIS, sep="")

    W, B = np.meshgrid(ws, bs)
    aras = np.logspace(np.log10(L.min() + 1e-9), np.log10(L.max()), 28)

    lintasan = {}
    for lr, warna in [(0.01, "tab:blue"), (0.06, "tab:orange"), (0.12, "tab:red")]:
        _, _, riwayat = latih(x, y, -1.0, 6.0, lr, 80)
        lintasan[lr] = (np.array([r[1] for r in riwayat]),
                        np.array([r[2] for r in riwayat]),
                        np.array([r[3] for r in riwayat]), warna)

    fig, (kiri, kanan) = plt.subplots(1, 2, figsize=(12, 5))

    kiri.contour(W, B, L, levels=aras, colors="0.78", linewidths=0.6)
    j, i = np.unravel_index(L.argmin(), L.shape)
    kiri.plot(ws[i], bs[j], "rx", ms=11, mew=2.4)
    kiri.set_xlabel("w"); kiri.set_ylabel("b")
    kiri.set_title("lintasan di atas kontur"); kiri.grid(alpha=0.25)

    kanan.set_xlim(0, 80); kanan.set_yscale("log")
    kanan.set_ylim(max(L.min() * 0.7, 1e-2), 400)
    kanan.set_xlabel("iterasi"); kanan.set_ylabel("MSE")
    kanan.set_title("kurva loss"); kanan.grid(alpha=0.25)

    seni = []
    for lr, (wt, bt, lt, warna) in lintasan.items():
        jejak, = kiri.plot([], [], "-", color=warna, lw=1.4, alpha=0.85)
        bola, = kiri.plot([], [], "o", color=warna, ms=9, label=f"lr = {lr}")
        kurva, = kanan.plot([], [], "-", color=warna, lw=1.8, label=f"lr = {lr}")
        seni.append((jejak, bola, kurva, wt, bt, lt))
    kiri.legend(fontsize=9, loc="upper right")
    kanan.legend(fontsize=9)

    def bingkai(k):
        keluar = []
        for jejak, bola, kurva, wt, bt, lt in seni:
            m = min(k + 1, len(wt))
            jejak.set_data(wt[:m], bt[:m])
            bola.set_data([wt[m - 1]], [bt[m - 1]])
            kurva.set_data(range(m), lt[:m])
            keluar += [jejak, bola, kurva]
        return keluar

    t0 = time.perf_counter()
    anim = FuncAnimation(fig, bingkai, frames=80, interval=80, blit=True)
    anim.save(FIGUR / "sesiB_animasi.gif", writer=PillowWriter(fps=12))
    plt.close()

    print(f"  gif disimpan  : figures/sesiB_animasi.gif "
          f"({time.perf_counter() - t0:.1f} detik)")
    print("""
  Buka gif-nya. Ini bagian yang tidak boleh kamu lewati, dan alasannya
  bukan karena hasilnya bagus dipandang.

  Tiga bola berangkat dari titik yang sama di permukaan yang sama, dan
  yang membedakan cuma satu angka. Kamu bisa melihat langsung bola merah
  menggergaji sementara bola biru merayap lurus tapi lambat.

  Setelah menonton ini beberapa kali, "menuruni permukaan loss" berhenti
  jadi kalimat dan mulai jadi benda. Seluruh Bulan 1 sampai 5 berdiri di
  atas intuisi ini, dan intuisi itu tidak bisa dibaca, cuma bisa dilihat.""")


# ══════════════════════════════════════════════════════════════
# BAGIAN 6 - batas yang tajam
# ══════════════════════════════════════════════════════════════

def bagian6(x, y, lam):
    print("\n" + GARIS, "\nBAGIAN 6  mencari batas lr dengan teliti\n", GARIS, sep="")

    ramalan = 2 / lam[1]
    A_sampel = np.sum(x * x) / len(x)

    print(f"  ramalan 2D, 2/lambda_max        : {ramalan:.6f}")
    print(f"  ramalan 1D, 1/A dari sampel     : {1 / A_sampel:.6f}   (A = {A_sampel:.4f})")
    print(f"  ramalan 1D, 1/A dari populasi   : {3 / 25:.6f}   (A = {25/3:.4f})\n")

    uji = [0.119, 0.121, 0.123, 0.125, 0.127, 0.1272, 0.1274, 0.128, 0.130]
    print(f"  {'lr':>8}   {'loss akhir':>22}   status")
    print("  " + "-" * 52)

    dasar = mse(prediksi(x, *np.linalg.lstsq(
        np.vstack([x, np.ones(len(x))]).T, y, rcond=None)[0]), y)

    batas_bawah, batas_atas = None, None
    for lr in uji:
        w, b, _ = latih(x, y, 0.0, 0.0, lr, 3000)
        ok = np.isfinite(w) and np.isfinite(b)
        loss = mse(prediksi(x, w, b), y) if ok else np.inf

        if not np.isfinite(loss) or loss > 1e6:
            status = "DIVERGEN"
        elif loss > dasar * 1.01:
            status = "berayun tetap"
        else:
            status = "konvergen"

        if status == "konvergen":
            batas_bawah = lr
        elif batas_atas is None:
            batas_atas = lr
        print(f"  {lr:8}   {loss:22.6f}   {status}")

    print(f"""
  Batas sebenarnya terjepit antara {batas_bawah} dan {batas_atas}, dan
  ramalan Hessian jatuh persis di dalam jepitan itu.

  Perhatikan baris yang berlabel berayun tetap. Di situ loss-nya tidak
  meledak, tapi juga tidak pernah turun ke dasar. Ia terkunci berayun
  dengan amplitudo yang sama selamanya, karena faktor pengalinya bernilai
  tepat minus satu. Itu osilator tanpa redaman sama sekali, bukan sistem
  yang stabil dan bukan sistem yang lepas.

  Ramalan Hessian 2D meleset kurang dari 0,2 persen. Ramalan 1D dengan A
  sampel sedikit ketinggian, karena ia mengabaikan kopling antara w dan b
  yang muncul dari x rata-rata yang tidak nol.

  Ramalan dengan A populasi meleset jauh, dan bedanya bisa kamu uji: kalau
  angka itu benar, lr = 0.123 seharusnya sudah meledak. Lihat sendiri di
  tabel apakah itu terjadi.

  Ini ketiga kalinya kamu bertemu perbedaan nilai populasi lawan nilai
  sampel di modul ini. Pertama di Soal 3e Hari 3, kedua di Soal 4 Sesi A,
  dan sekarang di sini. Datamu tidak pernah tahu apa yang seharusnya. Ia
  cuma tahu 50 angka yang ada di depannya.""")


if __name__ == "__main__":
    x, y = buat_data()
    try:
        ws, bs, L = bagian1(x, y)
        bagian2(ws, bs, L)
        bagian3(x, y, ws, bs, L)
        lam = bagian4(x, y, ws, bs, L)
        bagian5(x, y, ws, bs, L)
        bagian6(x, y, lam)
    except NotImplementedError as e:
        print(f"\n  {e} belum diisi. Kerjakan TODO dulu.")
