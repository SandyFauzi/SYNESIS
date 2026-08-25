"""Latih ulang pengklasifikasi intent. python -m synesis.latih

Sumber data latih:
  1. korpus sintetis, dipotong konfig.SINTETIS_MAKS
  2. koreksi.jsonl, yaitu perbaikan yang kamu ketik sendiri di jendela

perintah_eval_real.txt TIDAK pernah masuk latihan. Dia satu-satunya ujian
yang jujur; melatihinya membuat angkanya berhenti berarti.
"""

import json
import sys
import time
from collections import Counter

import numpy as np

from . import konfig
from .fitur import KATA, bangun_fitur, encoder_ada, vektorkan


def _baca_pasangan(berkas):
    if not berkas.exists():
        return []
    keluar = []
    for baris in berkas.read_text(encoding="utf-8").splitlines():
        baris = baris.strip()
        if not baris or baris.startswith("#") or "|" not in baris:
            continue
        label, kalimat = baris.split("|", 1)
        keluar.append((kalimat.strip().lower(), label.strip()))
    return keluar


def baca_koreksi(berkas=None):
    """koreksi.jsonl -> [(kalimat, intent)]. Kalimat sama, yang terakhir menang."""
    berkas = berkas or konfig.KOREKSI
    if not berkas.exists():
        return []
    terakhir = {}
    for baris in berkas.read_text(encoding="utf-8").splitlines():
        if not baris.strip():
            continue
        try:
            d = json.loads(baris)
        except json.JSONDecodeError:
            continue
        if d.get("kalimat") and d.get("intent"):
            terakhir[d["kalimat"].strip().lower()] = d["intent"].strip()
    return list(terakhir.items())


def catat_koreksi(kalimat, intent, berkas=None):
    berkas = berkas or konfig.KOREKSI
    berkas.parent.mkdir(parents=True, exist_ok=True)
    with berkas.open("a", encoding="utf-8") as f:
        print(json.dumps({"kalimat": kalimat, "intent": intent},
                         ensure_ascii=False), file=f)


def kosakata(kalimat):
    kata = set()
    for k in kalimat:
        kata.update(KATA.findall(k.lower()))
    return {w: i for i, w in enumerate(sorted(kata))}


def softmax_latih(X, y, n_kelas, lr=0.5, epoch=400, seed=0):
    rng = np.random.default_rng(seed)
    W = rng.normal(0, 0.01, (X.shape[1], n_kelas))
    b = np.zeros(n_kelas)
    baris = np.arange(len(y))
    for _ in range(epoch):
        z = X @ W + b
        p = np.exp(z - z.max(1, keepdims=True))
        p /= p.sum(1, keepdims=True)
        p[baris, y] -= 1.0
        p /= len(y)
        W -= lr * (X.T @ p)
        b -= lr * p.sum(0)
    return W, b


def _potong_berimbang(pasang, maks, seed=0):
    """Ambil sebanyak-banyaknya `maks`, porsi tiap kelas dijaga."""
    if len(pasang) <= maks:
        return pasang
    kelompok = {}
    for c in pasang:
        kelompok.setdefault(c[1], []).append(c)
    per = max(1, maks // len(kelompok))
    rng = np.random.default_rng(seed)
    keluar = []
    for lab in sorted(kelompok):
        g = kelompok[lab]
        keluar.extend(g[i] for i in rng.permutation(len(g))[:per])
    return keluar


def latih(resep=None, diam=False):
    """Latih, simpan, kembalikan ringkasan.

    resep: kantong | encoder | gabung. None memakai konfig.RESEP_BAWAAN.
    """
    resep = resep or konfig.RESEP_BAWAAN
    if resep not in konfig.RESEP:
        raise ValueError(f"unknown recipe: {resep}")
    if resep != "kantong" and not encoder_ada():
        raise RuntimeError(
            f"recipe '{resep}' needs sentence-transformers. "
            f"Use 'kantong', or install the package.")
    def kabar(*a):
        if not diam:
            print(*a)

    mulai = time.perf_counter()
    sintetis = _potong_berimbang(
        _baca_pasangan(konfig.LATIH_SINTETIS), konfig.SINTETIS_MAKS)
    koreksi = baca_koreksi()
    uji = _baca_pasangan(konfig.UJI_NYATA)
    if not sintetis and not koreksi:
        raise SystemExit(f"No training data at {konfig.LATIH_SINTETIS}")

    # Koreksi diulang supaya tidak tenggelam di antara ribuan kalimat sintetis.
    ulang = 0 if not koreksi else min(konfig.ULANG_MAKS, max(1, round(
        konfig.PORSI_KOREKSI * len(sintetis)
        / (len(koreksi) * (1 - konfig.PORSI_KOREKSI)))))
    latih_set = sintetis + koreksi * ulang

    label = sorted({l for _, l in latih_set} | {l for _, l in uji})
    L = {l: i for i, l in enumerate(label)}
    kos = kosakata([k for k, _ in latih_set])
    X = bangun_fitur([k for k, _ in latih_set], resep, kos, cache=True)
    y = np.array([L[l] for _, l in latih_set])

    # Fitur rapat butuh langkah lebih besar daripada kantong kata yang jarang.
    W, b = softmax_latih(X, y, len(label),
                         lr=0.5 if resep == "kantong" else 2.0)

    kabar(f"  recipe    : {resep}  ({X.shape[1]} columns)")
    kabar(f"  synthetic : {len(sintetis)}")
    if koreksi:
        kabar(f"  fixes     : {len(koreksi)} sentences, repeated {ulang}x "
              f"({len(koreksi) * ulang / len(latih_set) * 100:.0f}%)")
    else:
        kabar("  fixes     : none yet. Correct a guess in the window first.")
    kabar(f"  vocabulary: {len(kos)}   classes: {len(label)}")

    skor = None
    if uji:
        Xu = bangun_fitur([k for k, _ in uji], resep, kos, cache=True)
        yu = np.array([L[l] for _, l in uji])
        benar = int(((Xu @ W + b).argmax(1) == yu).sum())
        n = len(uji)
        p = benar / n
        s = 1.96 * (p * (1 - p) / n) ** 0.5
        skor = (benar, n, p)
        kabar(f"  held-out  : {benar}/{n} = {p * 100:.1f}%"
              f"   95% CI {max(0, p - s) * 100:.1f} .. {min(1, p + s) * 100:.1f}")
        kabar(f"  baseline  : {max(Counter(yu.tolist()).values()) / n * 100:.1f}%"
              f" (always guess the largest class)")

    konfig.MODEL_INTENT.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        konfig.MODEL_INTENT,
        resep=np.array(resep),
        label=np.array(label),
        kosakata=np.array(sorted(kos, key=kos.get)),
        idf=np.zeros(0),
        W=W, b=b,
    )
    detik = time.perf_counter() - mulai
    kabar(f"  saved     : {konfig.MODEL_INTENT.name} "
          f"({konfig.MODEL_INTENT.stat().st_size / 1024:.0f} KB) "
          f"in {detik:.1f} s")
    return {"detik": detik, "resep": resep, "kolom": int(X.shape[1]),
            "sintetis": len(sintetis), "koreksi": len(koreksi),
            "kelas": len(label), "kosakata": len(kos), "skor": skor}


def _demo():
    tmp = konfig.MODEL_INTENT.parent / "_latih_demo.jsonl"
    tmp.unlink(missing_ok=True)
    catat_koreksi("buka berkas laporan", "buka_berkas", tmp)
    catat_koreksi("buka berkas laporan", "cari_berkas", tmp)   # ditimpa
    catat_koreksi("berapa sisa disk", "info_sistem", tmp)
    k = dict(baca_koreksi(tmp))
    assert k["buka berkas laporan"] == "cari_berkas", k
    assert len(k) == 2
    tmp.unlink()

    p = [("a", "x")] * 50 + [("b", "y")] * 50
    assert len(_potong_berimbang(p, 20)) == 20
    assert len(_potong_berimbang(p, 500)) == 100
    assert Counter(l for _, l in _potong_berimbang(p, 20))["x"] == 10

    # satu koreksi tidak boleh membanjiri data latih
    assert min(konfig.ULANG_MAKS, 1286) == konfig.ULANG_MAKS

    X = vektorkan(["a b", "c"], {"a": 0, "b": 1, "c": 2})
    W, b = softmax_latih(X, np.array([0, 1]), 2, epoch=200)
    assert (X @ W + b).argmax(1).tolist() == [0, 1]
    print("latih: lulus")


if __name__ == "__main__":
    pilih = sys.argv[1] if len(sys.argv) > 1 else None
    latih(pilih)
