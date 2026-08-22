"""Bulan 1 Sesi 1 - mesin autograd buatanmu sendiri.

Jalankan:
    . .\\scripts\\activate.ps1
    python notebooks\\bulan1_sesi1_autograd.py

Di Sesi D kamu membuktikan gradien tanganmu cocok dengan loss.backward()
sampai 1e-16. Malam ini kamu menulis isi loss.backward() itu.

Sekitar 90 baris. Setelah selesai, tidak ada lagi kotak hitam di lapisan
paling dasar deep learning, dan itu berlaku seumur hidup.

Bagian bertanda TODO kamu yang isi.
"""

import math
import random
from pathlib import Path

GARIS = "=" * 62
FIGUR = Path(__file__).resolve().parent.parent / "figures"
FIGUR.mkdir(exist_ok=True)


# ══════════════════════════════════════════════════════════════
# BAGIAN 1 - kelas Value
# ══════════════════════════════════════════════════════════════

class Value:
    """Satu bilangan yang ingat dari mana ia berasal.

    Tiga hal yang ia simpan:
      data      nilainya sekarang
      grad      turunan loss terhadap dirinya, diisi saat backward
      _prev     induk yang melahirkannya
      _backward fungsi yang membagikan grad-nya ke induk

    Itulah seluruh idenya. Sisanya cuma menuliskan aturan turunan lokal
    untuk tiap operasi.
    """

    def __init__(self, data, _anak=(), _op=""):
        self.data = float(data)
        self.grad = 0.0
        self._prev = set(_anak)
        self._op = _op
        self._backward = lambda: None

    def __repr__(self):
        return f"Value(data={self.data:.6g}, grad={self.grad:.6g})"

    # ---------- TODO 1 ----------
    def __add__(self, other):
        """Penjumlahan, beserta aturan pembagian gradiennya.

        Kalau  out = self + other, maka
            d out / d self  = 1
            d out / d other = 1

        Jadi tiap induk menerima grad out apa adanya, dikali 1.

        Kerangkanya:

            other = other if isinstance(other, Value) else Value(other)
            out = Value(self.data + other.data, (self, other), '+')

            def _backward():
                self.grad  += ...
                other.grad += ...

            out._backward = _backward
            return out

        WAJIB memakai += dan bukan =. Kalau sebuah Value dipakai dua kali
        dalam satu ekspresi, misalnya a * a, ia harus MENJUMLAHKAN kedua
        sumbangan itu. Menimpanya berarti membuang salah satunya.

        Kamu sudah menyentuh ide ini di Soal 2b Sesi D, saat menjelaskan
        kenapa PyTorch menumpuk gradien alih-alih menimpanya. Ini alasannya.

        TODO 1a
        """
        raise NotImplementedError("Value.__add__")

    def __mul__(self, other):
        """Perkalian.

        Kalau  out = self * other, maka
            d out / d self  = other.data
            d out / d other = self.data

        Perhatikan silangnya. Turunan terhadap satu faktor adalah faktor
        yang lain. Ini aturan hasil kali, dan di sinilah ia hidup.

        TODO 1b
        """
        raise NotImplementedError("Value.__mul__")

    def __pow__(self, k):
        """Pangkat dengan eksponen tetap. k adalah angka biasa, bukan Value.

            out = self ** k
            d out / d self = k * self.data ** (k - 1)

        TODO 1c
        """
        raise NotImplementedError("Value.__pow__")

    def relu(self):
        """Tekukan. relu(x) = maks(0, x).

            d out / d self = 1 kalau self.data > 0, selain itu 0

        Turunannya di titik 0 tidak terdefinisi secara matematis. Praktiknya
        dipilih 0. Kenapa boleh sembarangan begitu adalah Soal 4.

        TODO 1d
        """
        raise NotImplementedError("Value.relu")

    # ---------- TODO 2 ----------
    def backward(self):
        """Sebarkan gradien dari sini mundur ke seluruh induk.

        Dua langkah.

        Pertama, susun semua simpul dalam urutan topologis. Artinya sebuah
        simpul baru boleh muncul setelah semua yang melahirkannya muncul.
        Ini penting: grad sebuah simpul harus LENGKAP sebelum ia
        membagikannya ke induknya. Kalau urutannya salah, kamu membagikan
        gradien yang belum utuh, dan hasilnya salah tanpa satu pun error.

        Kerangka penyusunannya, telusur mendalam biasa:

            topo, terlihat = [], set()
            def bangun(v):
                if v not in terlihat:
                    terlihat.add(v)
                    for anak in v._prev:
                        bangun(anak)
                    topo.append(v)
            bangun(self)

        Kedua, set grad simpul ini jadi 1.0, lalu panggil _backward tiap
        simpul dalam urutan TERBALIK dari topo.

        Kenapa 1.0? Karena turunan loss terhadap dirinya sendiri adalah 1.
        Itu titik berangkat seluruh rantai.

        TODO 2
        """
        raise NotImplementedError("Value.backward")

    # ---------- disediakan, turunan dari yang di atas ----------
    def __neg__(self):
        return self * -1

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return (-self) + other

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        return self * other**-1

    def __rtruediv__(self, other):
        return other * self**-1


# ══════════════════════════════════════════════════════════════
# BAGIAN 2 - uji tiap operasi terhadap beda hingga
# ══════════════════════════════════════════════════════════════

def beda_hingga(f, x, h=1e-6):
    """Turunan numerik beda pusat. Wasit yang tidak pernah melihat rumusmu."""
    return (f(x + h) - f(x - h)) / (2 * h)


def bagian2():
    print(GARIS, "\nBAGIAN 2  tiap operasi diadu dengan beda hingga\n", GARIS, sep="")

    uji = [
        ("a + b",        lambda a, b: a + b,              lambda a, b: (1.0, 1.0)),
        ("a * b",        lambda a, b: a * b,              lambda a, b: (b, a)),
        ("a - b",        lambda a, b: a - b,              lambda a, b: (1.0, -1.0)),
        ("a / b",        lambda a, b: a / b,              lambda a, b: (1 / b, -a / b**2)),
        ("a ** 3",       lambda a, b: a**3,               lambda a, b: (3 * a**2, 0.0)),
        ("a * a",        lambda a, b: a * a,              lambda a, b: (2 * a, 0.0)),
        ("(a + b) * a",  lambda a, b: (a + b) * a,        lambda a, b: (2 * a + b, a)),
        # dua sisi relu. Yang pertama aktif, yang kedua mati.
        # Tanpa yang aktif, ujinya lolos secara hampa: analitik dan numerik
        # sama-sama nol, jadi kode yang salah pun ikut lolos.
        ("relu(a*b + 5)", lambda a, b: (a * b + 5.0).relu(), None),
        ("relu(a * b)",   lambda a, b: (a * b).relu(), None),
    ]

    print(f"  {'ekspresi':>14} {'dL/da':>12} {'beda hingga':>13} "
          f"{'dL/db':>12} {'beda hingga':>13}   status")
    print("  " + "-" * 78)

    semua_lolos = True
    for nama, f, _ in uji:
        av, bv = 1.7, -2.3
        a, b = Value(av), Value(bv)
        out = f(a, b)
        out.backward()

        na = beda_hingga(lambda t: f(Value(t), Value(bv)).data, av)
        nb = beda_hingga(lambda t: f(Value(av), Value(t)).data, bv)

        ok = abs(a.grad - na) < 1e-5 and abs(b.grad - nb) < 1e-5
        semua_lolos = semua_lolos and ok
        print(f"  {nama:>14} {a.grad:12.6f} {na:13.6f} "
              f"{b.grad:12.6f} {nb:13.6f}   {'lolos' if ok else 'GAGAL'}")

    print(f"""
  Semua lolos: {semua_lolos}

  Perhatikan baris 'a * a'. Di situ satu Value dipakai dua kali, dan
  gradiennya harus 2a. Kalau kamu memakai = alih-alih += di dalam
  _backward, baris itu akan memberi a saja, bukan 2a.

  Itu satu-satunya baris di tabel ini yang bisa membedakan kode benar
  dari kode yang kelihatan benar.""")
    return semua_lolos


# ══════════════════════════════════════════════════════════════
# BAGIAN 3 - ekspresi acak, ratusan kali
# ══════════════════════════════════════════════════════════════

def bagian3(n_uji=300, seed=3):
    print("\n" + GARIS, "\nBAGIAN 3  ekspresi acak lawan beda hingga\n", GARIS, sep="")

    rng = random.Random(seed)
    terburuk, ekspresi_terburuk = 0.0, ""
    gagal = 0

    for _ in range(n_uji):
        av, bv, cv = [rng.uniform(-3, 3) for _ in range(3)]

        def bangun(a, b, c):
            t = (a * b + c) * a
            t = t + (b - c) * (a + 1.0)
            t = t * (c * c + 0.5)
            return t.relu() + t * 0.1

        a, b, c = Value(av), Value(bv), Value(cv)
        out = bangun(a, b, c)
        out.backward()

        for nilai, simpul, indeks in [(av, a, 0), (bv, b, 1), (cv, c, 2)]:
            def f(t, i=indeks):
                arg = [Value(av), Value(bv), Value(cv)]
                arg[i] = Value(t)
                return bangun(*arg).data
            num = beda_hingga(f, nilai, 1e-6)
            rel = abs(simpul.grad - num) / max(1e-8, abs(simpul.grad) + abs(num))
            if rel > terburuk:
                terburuk, ekspresi_terburuk = rel, f"a={av:.3f} b={bv:.3f} c={cv:.3f}"
            if rel > 1e-5:
                gagal += 1

    print(f"  ekspresi diuji     : {n_uji}, masing-masing 3 peubah")
    print(f"  galat relatif maks : {terburuk:.3e}   pada {ekspresi_terburuk}")
    print(f"  yang gagal         : {gagal}")
    print("""
  Ekspresinya sengaja dibuat berantakan: satu peubah muncul berkali-kali,
  ada relu di ujung, ada perkalian bersarang. Persis situasi tempat urutan
  topologis dan penumpukan gradien bisa salah diam-diam.

  Kalau semuanya lolos, mesinmu sudah benar untuk graf sembarang.""")
    return gagal == 0


# ══════════════════════════════════════════════════════════════
# BAGIAN 4 - saksi ketiga, PyTorch
# ══════════════════════════════════════════════════════════════

def bagian4():
    print("\n" + GARIS, "\nBAGIAN 4  mesinmu lawan PyTorch\n", GARIS, sep="")

    try:
        import torch
    except ImportError:
        print("  PyTorch tidak tersedia. Bagian ini dilewati.")
        return

    av, bv, cv = 1.3, -0.7, 2.1

    a, b, c = Value(av), Value(bv), Value(cv)
    t = (a * b + c) * a + (b - c) * (a + 1.0)
    out = (t * (c * c + 0.5)).relu() + t * 0.1
    out.backward()

    ta = torch.tensor(av, dtype=torch.double, requires_grad=True)
    tb = torch.tensor(bv, dtype=torch.double, requires_grad=True)
    tc = torch.tensor(cv, dtype=torch.double, requires_grad=True)
    tt = (ta * tb + tc) * ta + (tb - tc) * (ta + 1.0)
    tout = (tt * (tc * tc + 0.5)).relu() + tt * 0.1
    tout.backward()

    print(f"  nilai keluaran : mesinmu {out.data:.12f}, torch {tout.item():.12f}")
    print(f"\n  {'peubah':>8} {'mesinmu':>16} {'pytorch':>16} {'selisih':>12}")
    print("  " + "-" * 56)
    for nama, mine, theirs in [("a", a.grad, ta.grad.item()),
                               ("b", b.grad, tb.grad.item()),
                               ("c", c.grad, tc.grad.item())]:
        print(f"  {nama:>8} {mine:16.12f} {theirs:16.12f} {abs(mine - theirs):12.3e}")

    print("""
  Tiga saksi lagi, seperti Sesi C dan D. Mesinmu, PyTorch, dan beda hingga
  di Bagian 3. Ketiganya sepakat, dan tidak ada satu pun yang menyalin
  rumus dari yang lain.

  Bedanya sekarang: dua dari tiga saksi itu kamu yang menulis.""")


# ══════════════════════════════════════════════════════════════
# BAGIAN 5 - latih model Sesi C memakai mesinmu
# ══════════════════════════════════════════════════════════════

def bagian5():
    print("\n" + GARIS, "\nBAGIAN 5  melatih dengan mesinmu sendiri\n", GARIS, sep="")

    from sesiC_multivariat import buat_data

    x_np, y_np = buat_data(15, seed=7)
    xs = [float(v) for v in x_np]
    ys = [float(v) for v in y_np]

    # regresi kubik, empat parameter
    rng = random.Random(0)
    theta = [Value(rng.uniform(-0.1, 0.1)) for _ in range(4)]
    lr, n_iter = 0.002, 4000

    for langkah in range(n_iter):
        loss = Value(0.0)
        for xi, yi in zip(xs, ys):
            ramal = Value(0.0)
            pangkat = 1.0
            for k, th in enumerate(theta):
                ramal = ramal + th * pangkat
                pangkat = pangkat * xi
            r = ramal - yi
            loss = loss + r * r
        loss = loss * (1.0 / len(xs))

        for th in theta:
            th.grad = 0.0
        loss.backward()
        for th in theta:
            th.data -= lr * th.grad

        if langkah in (0, 100, 500, 1500, n_iter - 1):
            print(f"  iterasi {langkah:5d}   loss = {loss.data:.6f}")

    import numpy as np
    from sesiC_multivariat import desain_polinom, mse_matriks
    X = desain_polinom(x_np, 3)
    th_lstsq, *_ = np.linalg.lstsq(X, y_np, rcond=None)

    print(f"\n  {'koef':>6} {'mesinmu':>14} {'lstsq':>14} {'selisih':>12}")
    print("  " + "-" * 50)
    for i, (m, l) in enumerate(zip(theta, th_lstsq)):
        print(f"  {i:6d} {m.data:14.6f} {l:14.6f} {abs(m.data - l):12.3e}")
    print(f"\n  loss optimum lstsq : {mse_matriks(X, y_np, th_lstsq):.6f}")

    print("""
  Mesin yang kamu tulis malam ini baru saja melatih model, dari nol, tanpa
  satu pun pustaka machine learning.

  Ia lambat. Tiap operasi membuat objek Python, dan tiap iterasi menyusun
  ulang seluruh graf dari awal. Untuk 15 titik dan 4 parameter itu tidak
  terasa. Untuk MNIST nanti ia akan terasa sekali, dan di situlah kamu akan
  mengerti kenapa PyTorch menyimpan seluruh lapisan sebagai satu tensor
  alih-alih ribuan objek Value.""")


if __name__ == "__main__":
    try:
        bagian2()
        bagian3()
        bagian4()
        bagian5()
    except NotImplementedError as e:
        print(f"\n  {e} belum diisi. Kerjakan TODO dulu.")
