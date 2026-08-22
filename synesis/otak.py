"""Sambungan ke Ollama. Ini satu-satunya berkas yang bicara dengan model.

Ollama menyalakan server HTTP di 127.0.0.1:11434. Kita cuma mengirim JSON ke
sana. Tidak ada pustaka khusus, tidak ada SDK, cuma requests. Kalau suatu hari
Ollama diganti dengan yang lain, berkas inilah satu-satunya yang perlu ditulis
ulang.
"""

import json

import requests

from . import konfig


class OtakMati(RuntimeError):
    """Dilempar kalau Ollama tidak bisa dihubungi. Pesannya sengaja panjang
    karena ini error yang paling sering muncul dan paling mudah dibetulkan."""


def _url(jalur):
    return f"{konfig.OLLAMA.rstrip('/')}/{jalur.lstrip('/')}"


def hidup():
    """True kalau server Ollama menyala."""
    try:
        requests.get(_url("api/tags"), timeout=2)
        return True
    except requests.RequestException:
        return False


def pastikan_hidup():
    if hidup():
        return
    raise OtakMati(
        "Ollama tidak menjawab di " + konfig.OLLAMA + "\n"
        "  1. Buka terminal baru, ketik: ollama serve\n"
        "  2. Kalau perintahnya tidak dikenal, Ollama belum terpasang.\n"
        "     Pasang dengan: winget install Ollama.Ollama\n"
        "  3. Kalau sudah menyala tapi tetap gagal, cek port 11434 dipakai\n"
        "     program lain: netstat -ano | findstr 11434"
    )


def daftar_model():
    """Nama model yang sudah diunduh ke disk."""
    pastikan_hidup()
    r = requests.get(_url("api/tags"), timeout=10)
    r.raise_for_status()
    return [m["name"] for m in r.json().get("models", [])]


def pastikan_model(nama):
    """Cek model ada. Kalau belum, beri perintah unduhnya, jangan unduh diam-diam.

    Mengunduh 2 GB tanpa memberi tahu itu perilaku yang buruk, apalagi kalau
    kuota internetnya terbatas.
    """
    punya = daftar_model()
    if nama in punya:
        return True
    # Ollama kadang menyimpan sebagai "qwen2.5:3b" tapi dicari "qwen2.5:3b-instruct"
    if any(p.split(":")[0] == nama.split(":")[0] for p in punya):
        return True
    raise OtakMati(
        f"Model '{nama}' belum ada di disk.\n"
        f"  Unduh dulu:  ollama pull {nama}\n"
        f"  Yang sudah ada: {', '.join(punya) if punya else '(kosong)'}"
    )


def tanya(pesan, model=None, suhu=None, alat_boleh=True):
    """Kirim percakapan, terima jawaban utuh. Dipakai kalau tidak butuh streaming.

    `pesan` adalah daftar dict {"role": ..., "content": ...} gaya OpenAI, yang
    juga dipakai Ollama.
    """
    return "".join(alir(pesan, model=model, suhu=suhu, alat_boleh=alat_boleh))


def alir(pesan, model=None, suhu=None, alat_boleh=True):
    """Sama dengan tanya(), tapi mengembalikan potongan demi potongan.

    Ini yang membuat jawaban muncul mengalir di layar alih-alih diam beberapa
    detik lalu keluar sekaligus. Untuk model 3B di GPU 4 GB, bedanya terasa.
    """
    model = model or konfig.MODEL_UTAMA
    pastikan_hidup()

    badan = {
        "model": model,
        "messages": pesan,
        "stream": True,
        "options": {
            "temperature": konfig.SUHU if suhu is None else suhu,
            "num_ctx": konfig.KONTEKS_MAKS,
            "num_predict": konfig.BALASAN_MAKS,
        },
    }

    try:
        with requests.post(_url("api/chat"), json=badan, stream=True,
                           timeout=300) as r:
            if r.status_code == 404:
                raise OtakMati(
                    f"Ollama menjawab 404 untuk model '{model}'.\n"
                    f"  Kemungkinan besar model belum diunduh.\n"
                    f"  Jalankan:  ollama pull {model}"
                )
            r.raise_for_status()
            for baris in r.iter_lines():
                if not baris:
                    continue
                try:
                    bagian = json.loads(baris)
                except json.JSONDecodeError:
                    continue
                if bagian.get("done"):
                    break
                isi = bagian.get("message", {}).get("content", "")
                if isi:
                    yield isi
    except requests.exceptions.ConnectionError as e:
        raise OtakMati(
            "Sambungan ke Ollama putus di tengah jalan.\n"
            "  Biasanya karena Ollama mati kehabisan VRAM.\n"
            "  Cek dengan: nvidia-smi\n"
            f"  Pesan asli: {e}"
        ) from e


def sematkan(teks, model="nomic-embed-text"):
    """Ubah teks jadi vektor. TIDAK dipakai di v0.1.

    Disediakan karena suatu saat kamu akan mau mengganti pencarian TF-IDF di
    ingat.py dengan pencarian semantik. Kalau itu terjadi, unduh dulu:
        ollama pull nomic-embed-text
    lalu ganti isi ingat.py, bukan berkas ini.
    """
    pastikan_hidup()
    r = requests.post(_url("api/embeddings"),
                      json={"model": model, "prompt": teks}, timeout=60)
    r.raise_for_status()
    return r.json()["embedding"]
