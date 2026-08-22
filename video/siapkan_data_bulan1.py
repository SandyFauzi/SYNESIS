"""Hitung dulu semua angka yang dipakai seri video Bulan 1, lalu simpan.

Dijalankan dengan venv SYNESIS, bukan venv manim, karena butuh sklearn dan
torch:

    . .\\scripts\\activate.ps1
    python video\\siapkan_data_bulan1.py

Keluarannya satu berkas `video/data/bulan1.npz`. Berkas bab manim cuma
membacanya, jadi venv manim tidak perlu paket apa pun selain numpy.

Alasannya sama dengan aturan seluruh repo ini: angka yang muncul di layar
harus berasal dari perhitungan yang bisa diulang, bukan diketik tangan.

Catatan buat pemilik. MLP di berkas ini ditulis vektor penuh dengan numpy,
sengaja dibuat berbeda dari yang akan kamu tulis di Sesi 2. Punyamu dibangun
di atas kelas `Value`, satu objek per angka, dan itu latihan yang berbeda.
Yang di sini cuma untuk memproduksi gambar.
"""

import json
import sys
from pathlib import Path

import numpy as np

KELUARAN = Path(__file__).resolve().parent / "data"
KELUARAN.mkdir(exist_ok=True)

hasil = {}
angka = {}


def kabar(teks):
    print(f"  {teks}")


# ══════════════════════════════════════════════════════════════
# BAGIAN 1 - dua bulan sabit, yang tidak bisa dibelah garis lurus
# ══════════════════════════════════════════════════════════════

def bulan_sabit(n=300, derau=0.18, seed=3):
    rng = np.random.default_rng(seed)
    m = n // 2
    t1 = rng.uniform(0, np.pi, m)
    t2 = rng.uniform(0, np.pi, n - m)
    x1 = np.stack([np.cos(t1), np.sin(t1)], 1)
    x2 = np.stack([1 - np.cos(t2), 0.5 - np.sin(t2)], 1)
    X = np.concatenate([x1, x2]) + rng.normal(0, derau, (n, 2))
    y = np.concatenate([np.zeros(m), np.ones(n - m)])
    p = rng.permutation(n)
    return X[p], y[p]


def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-np.clip(z, -60, 60)))


def latih_linear(X, y, lr=1.0, n_iter=20000):
    w, b = np.zeros(X.shape[1]), 0.0
    for _ in range(n_iter):
        p = sigmoid(X @ w + b)
        g = p - y
        w -= lr * (X.T @ g) / len(y)
        b -= lr * g.mean()
    return w, b


def latih_mlp(X, y, n_sembunyi=8, lr=0.5, n_iter=20000, seed=0):
    rng = np.random.default_rng(seed)
    W1 = rng.normal(0, 1.0, (X.shape[1], n_sembunyi)) * np.sqrt(2 / X.shape[1])
    b1 = np.zeros(n_sembunyi)
    W2 = rng.normal(0, 1.0, n_sembunyi) * np.sqrt(2 / n_sembunyi)
    b2 = 0.0
    riwayat = []
    for i in range(n_iter):
        Z1 = X @ W1 + b1
        A1 = np.maximum(0.0, Z1)
        p = sigmoid(A1 @ W2 + b2)
        rugi = -np.mean(y * np.log(p + 1e-12) + (1 - y) * np.log(1 - p + 1e-12))
        if i % 40 == 0:
            riwayat.append(rugi)
        d = (p - y) / len(y)
        gW2 = A1.T @ d
        gb2 = d.sum()
        dA1 = np.outer(d, W2) * (Z1 > 0)
        gW1 = X.T @ dA1
        gb1 = dA1.sum(0)
        W1 -= lr * gW1
        b1 -= lr * gb1
        W2 -= lr * gW2
        b2 -= lr * gb2
    return W1, b1, W2, b2, np.array(riwayat)


print("BAGIAN 1  dua bulan sabit")
Xm, ym = bulan_sabit()
w_lin, b_lin = latih_linear(Xm, ym)
akurasi_lin = float(((sigmoid(Xm @ w_lin + b_lin) > 0.5) == ym).mean())

W1, b1, W2, b2, riwayat_mlp = latih_mlp(Xm, ym, seed=1)
A1 = np.maximum(0.0, Xm @ W1 + b1)
akurasi_mlp = float(((sigmoid(A1 @ W2 + b2) > 0.5) == ym).mean())
mati = int(np.sum(A1.max(axis=0) <= 0.0))

kabar(f"akurasi model garis lurus : {akurasi_lin:.4f}")
kabar(f"akurasi MLP 2-8-1         : {akurasi_mlp:.4f}")
kabar(f"neuron mati               : {mati} dari {W1.shape[1]}")

# peta keputusan pada kisi
gx = np.linspace(-2.0, 3.0, 220)
gy = np.linspace(-1.6, 2.0, 200)
GX, GY = np.meshgrid(gx, gy)
kisi = np.stack([GX.ravel(), GY.ravel()], 1)
peta_lin = sigmoid(kisi @ w_lin + b_lin).reshape(len(gy), len(gx))
peta_mlp = sigmoid(np.maximum(0.0, kisi @ W1 + b1) @ W2 + b2).reshape(
    len(gy), len(gx))

# lipatan tiap neuron: garis di mana pra-aktivasi berpindah tanda
garis_lipat = []
for j in range(W1.shape[1]):
    a, bb, c = float(W1[0, j]), float(W1[1, j]), float(b1[j])
    if abs(bb) < 1e-9:
        continue
    xs = np.array([-2.0, 3.0])
    garis_lipat.append(np.stack([xs, -(a * xs + c) / bb], 1))

hasil["moon_X"] = Xm
hasil["moon_y"] = ym
hasil["moon_gx"] = gx
hasil["moon_gy"] = gy
hasil["moon_peta_lin"] = peta_lin
hasil["moon_peta_mlp"] = peta_mlp
hasil["moon_lipat"] = np.array(garis_lipat) if garis_lipat else np.zeros((0, 2, 2))
hasil["moon_rugi"] = riwayat_mlp
angka["moon_akurasi_lin"] = akurasi_lin
angka["moon_akurasi_mlp"] = akurasi_mlp
angka["moon_neuron_mati"] = mati
angka["moon_n_sembunyi"] = int(W1.shape[1])

# titik awal berbeda, hasil berbeda. ini yang tidak pernah terjadi di Bulan 0.
rugi_akhir, mati_survei, akurasi_survei = [], [], []
for s in range(8):
    w1s, b1s, w2s, b2s, r = latih_mlp(Xm, ym, seed=s)
    rugi_akhir.append(float(r[-1]))
    a1s = np.maximum(0.0, Xm @ w1s + b1s)
    mati_survei.append(int(np.sum(a1s.max(axis=0) <= 0.0)))
    akurasi_survei.append(float(((sigmoid(a1s @ w2s + b2s) > 0.5) == ym).mean()))
angka["moon_akurasi_survei"] = akurasi_survei
kabar(f"akurasi per titik awal    : {[round(a,4) for a in akurasi_survei]}")
angka["moon_mati_survei"] = mati_survei
kabar(f"neuron mati per seed      : {mati_survei}")
angka["moon_rugi_sebaran"] = rugi_akhir
kabar(f"rugi akhir 8 titik awal   : min {min(rugi_akhir):.4f} "
      f"maks {max(rugi_akhir):.4f}")


# ══════════════════════════════════════════════════════════════
# BAGIAN 2 - angka delapan kali delapan, pengganti MNIST
# ══════════════════════════════════════════════════════════════

print("BAGIAN 2  angka tulisan tangan")
from sklearn.datasets import load_digits  # noqa: E402

d = load_digits()
Xd = d.data / 16.0
yd = d.target
rng = np.random.default_rng(0)
p = rng.permutation(len(yd))
Xd, yd = Xd[p], yd[p]
n_latih = 1400
Xtr, ytr, Xte, yte = Xd[:n_latih], yd[:n_latih], Xd[n_latih:], yd[n_latih:]


def satu_panas(y, k=10):
    O = np.zeros((len(y), k))
    O[np.arange(len(y)), y] = 1.0
    return O


def softmax(Z):
    Z = Z - Z.max(1, keepdims=True)
    E = np.exp(Z)
    return E / E.sum(1, keepdims=True)


def latih_angka(Xtr, ytr, n_sembunyi=32, lr=0.5, n_epoch=260, seed=1):
    rng = np.random.default_rng(seed)
    W1 = rng.normal(0, np.sqrt(2 / Xtr.shape[1]), (Xtr.shape[1], n_sembunyi))
    b1 = np.zeros(n_sembunyi)
    W2 = rng.normal(0, np.sqrt(2 / n_sembunyi), (n_sembunyi, 10))
    b2 = np.zeros(10)
    T = satu_panas(ytr)
    riwayat = []
    for _ in range(n_epoch):
        Z1 = Xtr @ W1 + b1
        A1 = np.maximum(0.0, Z1)
        P = softmax(A1 @ W2 + b2)
        riwayat.append(float(-np.mean(np.sum(T * np.log(P + 1e-12), 1))))
        dZ2 = (P - T) / len(ytr)          # gradien bersih softmax + entropi silang
        gW2, gb2 = A1.T @ dZ2, dZ2.sum(0)
        dA1 = dZ2 @ W2.T * (Z1 > 0)
        gW1, gb1 = Xtr.T @ dA1, dA1.sum(0)
        W1 -= lr * gW1
        b1 -= lr * gb1
        W2 -= lr * gW2
        b2 -= lr * gb2
    return W1, b1, W2, b2, np.array(riwayat)


dW1, db1, dW2, db2, rugi_angka = latih_angka(Xtr, ytr)


def ramal(X):
    return softmax(np.maximum(0.0, X @ dW1 + db1) @ dW2 + db2)


akurasi_tr = float((ramal(Xtr).argmax(1) == ytr).mean())
akurasi_te = float((ramal(Xte).argmax(1) == yte).mean())
kabar(f"akurasi latih : {akurasi_tr:.4f}")
kabar(f"akurasi uji   : {akurasi_te:.4f}")

# sepuluh contoh, satu per angka, plus ramalannya
contoh, contoh_label, contoh_ramal = [], [], []
for k in range(10):
    i = int(np.where(yte == k)[0][0])
    contoh.append(Xte[i].reshape(8, 8))
    contoh_label.append(int(yte[i]))
    contoh_ramal.append(int(ramal(Xte[i:i + 1]).argmax()))

hasil["angka_contoh"] = np.array(contoh)
hasil["angka_label"] = np.array(contoh_label)
hasil["angka_ramal"] = np.array(contoh_ramal)
hasil["angka_rugi"] = rugi_angka
hasil["angka_bobot1"] = dW1[:, :8].T.reshape(8, 8, 8)
angka["angka_akurasi_tr"] = akurasi_tr
angka["angka_akurasi_te"] = akurasi_te
angka["angka_n_latih"] = int(len(ytr))
angka["angka_n_uji"] = int(len(yte))
angka["angka_piksel"] = int(Xd.shape[1])
angka["angka_parameter"] = int(dW1.size + db1.size + dW2.size + db2.size)


# ══════════════════════════════════════════════════════════════
# BAGIAN 3 - pegas, gesekan, dan Adam, di lembah sempit Sesi B
# ══════════════════════════════════════════════════════════════

print("BAGIAN 3  optimizer di lembah sempit")
# Lembahnya sengaja dibuat sempit dengan cara yang paling sering terjadi di
# dunia nyata: x tidak dibakukan, rentangnya [2, 12] bukan sekitar nol.
# Akibatnya bilangan kondisi Hessian jadi 384, dan lembahnya jadi ngarai.
rngB = np.random.default_rng(5)
XB = rngB.uniform(2, 12, 60)
YB = 3.0 * XB + 2.0 + rngB.normal(0, 1.5, 60)
AB = np.column_stack([XB, np.ones_like(XB)])
HB = (2.0 / len(XB)) * (AB.T @ AB)
evB = np.linalg.eigvalsh(HB)
theta_opt = np.linalg.lstsq(AB, YB, rcond=None)[0]
LR_BATAS = 2.0 / float(evB.max())


def rugiB(t):
    return float(np.mean((AB @ t - YB) ** 2))


def gradB(t):
    return (2.0 / len(XB)) * (AB.T @ (AB @ t - YB))


def jalan_optimizer(nama, lr, n=400, beta=0.9):
    t = np.zeros(2)
    v = np.zeros(2)
    s = np.zeros(2)
    jejak = [t.copy()]
    for k in range(1, n + 1):
        g = gradB(t)
        if nama == "sgd":
            t = t - lr * g
        elif nama == "momentum":
            v = beta * v - lr * g
            t = t + v
        elif nama == "rmsprop":
            s = 0.9 * s + 0.1 * g * g
            t = t - lr * g / (np.sqrt(s) + 1e-8)
        elif nama == "adam":
            v = 0.9 * v + 0.1 * g
            s = 0.999 * s + 0.001 * g * g
            vk = v / (1 - 0.9 ** k)
            sk = s / (1 - 0.999 ** k)
            t = t - lr * vk / (np.sqrt(sk) + 1e-8)
        jejak.append(t.copy())
        if not np.isfinite(t).all():
            break
    return np.array(jejak)


# tiap optimizer diberi lr terbaiknya sendiri, hasil sapuan.
# membandingkan pada lr yang sama akan curang, karena skalanya memang beda.
ATURAN = {
    "sgd": 0.99 * LR_BATAS,
    "momentum": 0.19 * LR_BATAS,
    "rmsprop": 0.09,
    "adam": 0.70,
}
norma_opt = float(np.linalg.norm(theta_opt))
jejak = {}
for nama, lr in ATURAN.items():
    j = jalan_optimizer(nama, lr)
    jejak[nama] = j
    hasil[f"opt_{nama}"] = j
    d = np.linalg.norm(j - theta_opt, axis=1) / norma_opt
    tiba = next((i for i, v in enumerate(d) if v < 0.02), -1)
    angka[f"opt_{nama}_lr"] = float(lr)
    angka[f"opt_{nama}_jarak_akhir"] = float(d[-1])
    angka[f"opt_{nama}_iterasi"] = int(tiba)
    tampil = "tidak sampai" if tiba < 0 else str(tiba)
    kabar(f"{nama:9} lr {lr:.5f}  jarak akhir {d[-1]:.5f}  "
          f"sampai 2 persen di iterasi {tampil}")

# peta rugi pada jendela yang digambar. elips eksak tidak dipakai karena
# lembah dengan bilangan kondisi 384 terlalu lonjong untuk muat di bingkai.
ogx = np.linspace(-0.4, 3.6, 240)
ogy = np.linspace(-1.2, 4.2, 220)
OGX, OGY = np.meshgrid(ogx, ogy)
kisi_t = np.stack([OGX.ravel(), OGY.ravel()], 1)
rugi_kisi = np.mean((kisi_t @ AB.T - YB[None, :]) ** 2, axis=1)
rugi_kisi = np.log10(rugi_kisi - rugiB(theta_opt) + 1e-3).reshape(len(ogy), len(ogx))
rugi_kisi = (rugi_kisi - rugi_kisi.min()) / (rugi_kisi.max() - rugi_kisi.min())
hasil["opt_peta"] = rugi_kisi
hasil["opt_gx"] = ogx
hasil["opt_gy"] = ogy

hasil["opt_theta_opt"] = theta_opt
angka["opt_lam_min"] = float(evB.min())
angka["opt_lam_maks"] = float(evB.max())
angka["opt_kondisi"] = float(evB.max() / evB.min())
angka["opt_lr_batas"] = float(LR_BATAS)
angka["opt_rugi_min"] = rugiB(theta_opt)
angka["opt_n_iter"] = 400


# ══════════════════════════════════════════════════════════════
# BAGIAN 4 - batas rekursi mesin autograd buatan pemilik
# ══════════════════════════════════════════════════════════════

print("BAGIAN 4  batas rekursi mesin autograd")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "notebooks"))
try:
    from bulan1_sesi1_autograd import Value

    def bisa(n):
        v = Value(1.0)
        out = v
        for _ in range(n):
            out = out + 1.0
        try:
            out.backward()
            return True
        except RecursionError:
            return False

    lo, hi = 50, 3000
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if bisa(mid):
            lo = mid
        else:
            hi = mid
    angka["rekursi_batas"] = int(lo)
    angka["rekursi_limit_python"] = int(sys.getrecursionlimit())
    kabar(f"rantai terpanjang yang jalan : {lo}")

    import random as _rnd
    _r = _rnd.Random(0)

    def neuron(xs, w, b):
        s = b
        for xi, wi in zip(xs, w):
            s = s + wi * xi
        return s.relu()

    tabel = []
    for n_sem in [16, 128, 200, 256]:
        xs = [Value(_r.uniform(-1, 1)) for _ in range(784)]
        try:
            h = [neuron(xs, [Value(_r.uniform(-1, 1)) for _ in range(784)],
                        Value(0.0)) for _ in range(n_sem)]
            out = neuron(h, [Value(_r.uniform(-1, 1)) for _ in range(n_sem)],
                         Value(0.0))
            out.backward()
            st = "lolos"
        except RecursionError:
            st = "RecursionError"
        tabel.append([784, n_sem, 784 + n_sem, st])
        kabar(f"MLP 784 -> {n_sem:4d} -> 1   kedalaman ~ {784 + n_sem:5d}   {st}")
    angka["rekursi_tabel"] = tabel
except Exception as e:                                    # noqa: BLE001
    kabar(f"mesin autograd belum bisa diimpor: {e}")
    angka["rekursi_batas"] = None



# ══════════════════════════════════════════════════════════════
# BAGIAN 5 - ongkos satu objek per angka
# ══════════════════════════════════════════════════════════════

print("BAGIAN 5  ongkos mesin Value")
try:
    import random as _r2
    import time as _t

    from bulan1_sesi1_autograd import Value as _V

    _cacah = {"n": 0}
    _asli = _V.__init__

    def _hitung(self, data, _anak=(), _op=""):
        _cacah["n"] += 1
        _asli(self, data, _anak, _op)

    _V.__init__ = _hitung

    # satu iterasi regresi kubik, persis Bagian 5 berkas latihan
    rngC = np.random.default_rng(7)
    xs = list(np.sort(rngC.uniform(-3, 3, 15)))
    ys = list(0.5 * np.array(xs) ** 3 - 2.0 * np.array(xs) + 1.0
              + rngC.normal(0, 1.5, 15))
    rr = _r2.Random(0)
    theta = [_V(rr.uniform(-0.1, 0.1)) for _ in range(4)]

    _cacah["n"] = 0
    t0 = _t.perf_counter()
    rugi = _V(0.0)
    for xi, yi in zip(xs, ys):
        ramal = _V(0.0)
        pangkat = 1.0
        for th in theta:
            ramal = ramal + th * pangkat
            pangkat = pangkat * float(xi)
        r = ramal - float(yi)
        rugi = rugi + r * r
    rugi = rugi * (1.0 / len(xs))
    for th in theta:
        th.grad = 0.0
    rugi.backward()
    waktu_value = (_t.perf_counter() - t0) * 1000
    per_iter = _cacah["n"]

    # tandingannya, hitungan yang sama persis dengan numpy
    Xc = np.vander(np.array(xs), 4, increasing=True)
    yc = np.array(ys)
    thc = np.array([th.data for th in theta])
    t0 = _t.perf_counter()
    for _ in range(20):
        res = Xc @ thc - yc
        _ = float(np.mean(res ** 2))
        _g = (2.0 / len(yc)) * (Xc.T @ res)
    waktu_numpy = (_t.perf_counter() - t0) / 20 * 1000

    angka["value_per_iterasi"] = int(per_iter)
    angka["value_total"] = int(per_iter * 4000)
    angka["waktu_value_ms"] = float(waktu_value)
    angka["waktu_numpy_ms"] = float(waktu_numpy)
    kabar(f"objek Value per iterasi : {per_iter}")
    kabar(f"selama 4000 iterasi     : {per_iter * 4000}")
    kabar(f"satu langkah Value      : {waktu_value:.3f} ms")
    kabar(f"satu langkah numpy      : {waktu_numpy:.3f} ms")

    # satu hitung maju MLP 784-32-10, cuma dicacah, tanpa backward
    _cacah["n"] = 0
    masukan = [_V(rr.uniform(0, 1)) for _ in range(784)]
    _cacah["n"] = 0
    sembunyi = []
    for _ in range(32):
        s_ = _V(0.0)
        for xi_, wi_ in zip(masukan, [_V(rr.uniform(-1, 1)) for _ in range(784)]):
            s_ = s_ + wi_ * xi_
        sembunyi.append(s_.relu())
    for _ in range(10):
        s_ = _V(0.0)
        for hi_, wi_ in zip(sembunyi, [_V(rr.uniform(-1, 1)) for _ in range(32)]):
            s_ = s_ + wi_ * hi_
    angka["value_mnist_satu_maju"] = int(_cacah["n"])
    kabar(f"satu maju MLP 784-32-10 : {_cacah['n']} objek Value")

    _V.__init__ = _asli
except Exception as e:                                    # noqa: BLE001
    kabar(f"pengukuran ongkos gagal: {e}")
    angka["value_per_iterasi"] = 0
    angka["value_total"] = 0
    angka["value_mnist_satu_maju"] = 0
    angka["waktu_value_ms"] = 0.0
    angka["waktu_numpy_ms"] = 0.0


# ══════════════════════════════════════════════════════════════
np.savez_compressed(KELUARAN / "bulan1.npz", **hasil)
(KELUARAN / "bulan1.json").write_text(
    json.dumps(angka, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"\nDisimpan ke {KELUARAN}")
print(f"  bulan1.npz  {(KELUARAN / 'bulan1.npz').stat().st_size / 1024:.0f} KB")
print(f"  bulan1.json {(KELUARAN / 'bulan1.json').stat().st_size} byte")
