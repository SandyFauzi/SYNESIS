"""SYNESIS v0.2 di jendela. tkinter, nol dependensi tambahan.

    python -m synesis
    python -m synesis --sungguhan

Otaknya niat.jalankan_pipa. Berkas ini tidak boleh punya aturan keputusan
sendiri; dua salinan kebijakan adalah dua kebijakan.
"""

import sys
import threading
import tkinter as tk
from tkinter import messagebox, ttk

from . import fitur, konfig, latih, niat

WARNA = {
    "latar": "#1e1e22", "panel": "#26262c", "teks": "#e6e6ea",
    "kamu": "#7fb5ff", "synesis": "#9fe3a0", "redup": "#8b8b95",
    "bahaya": "#ff8a80",
}

NADA = {"jalan": "synesis", "tolak_izin": "bahaya"}

# Kunci tindakan dan risiko itu skema data: ia tersimpan apa adanya di
# audit.jsonl. Yang diterjemahkan cuma tampilannya.
TINDAKAN_EN = {
    "jalan": "ran",
    "tolak_kosong": "refused - unknown words",
    "tolak_yakin": "refused - low confidence",
    "tolak_argumen": "refused - no argument",
    "tolak_izin": "refused - permission denied",
    "belum_ada_alat": "no tool yet",
}
RISIKO_EN = {"BACA": "READ", "TULIS": "WRITE",
             "MERUSAK": "DESTRUCTIVE", "BAHASA": "LANGUAGE"}


class Jendela:
    def __init__(self, akar, model, kering=True):
        self.model, self.akar = model, akar
        self.kering = tk.BooleanVar(value=kering)
        self.terakhir = None          # kalimat terakhir, untuk dikoreksi

        akar.title("SYNESIS v0.2")
        akar.configure(bg=WARNA["latar"])
        akar.geometry("760x560")
        akar.minsize(520, 360)

        atas = tk.Frame(akar, bg=WARNA["panel"])
        atas.pack(fill="x")
        tk.Label(atas, text="SYNESIS v0.2", bg=WARNA["panel"],
                 fg=WARNA["teks"], font=("Segoe UI", 11, "bold"),
                 padx=12, pady=8).pack(side="left")
        tk.Checkbutton(
            atas, text="dry run", variable=self.kering,
            command=self._mode, bg=WARNA["panel"], fg=WARNA["teks"],
            selectcolor=WARNA["latar"], activebackground=WARNA["panel"],
            activeforeground=WARNA["teks"], font=("Segoe UI", 9),
        ).pack(side="right", padx=12)

        bingkai = tk.Frame(akar, bg=WARNA["latar"])
        bingkai.pack(fill="both", expand=True, padx=12, pady=(10, 6))
        gulung = ttk.Scrollbar(bingkai)
        gulung.pack(side="right", fill="y")
        self.obrolan = tk.Text(
            bingkai, wrap="word", bg=WARNA["latar"], fg=WARNA["teks"],
            insertbackground=WARNA["teks"], relief="flat", padx=8, pady=8,
            font=("Consolas", 10), yscrollcommand=gulung.set, state="disabled")
        self.obrolan.pack(side="left", fill="both", expand=True)
        gulung.config(command=self.obrolan.yview)
        for nama, warna in WARNA.items():
            self.obrolan.tag_configure(nama, foreground=warna)
        self.obrolan.tag_configure("kamu", font=("Consolas", 10, "bold"))

        koreksi = tk.Frame(akar, bg=WARNA["latar"])
        koreksi.pack(fill="x", padx=12, pady=(0, 6))
        tk.Label(koreksi, text="wrong? correct intent:", bg=WARNA["latar"],
                 fg=WARNA["redup"], font=("Segoe UI", 9)).pack(side="left")
        self.pilihan = ttk.Combobox(koreksi, values=sorted(niat.RUTE),
                                    state="disabled", width=18,
                                    font=("Consolas", 9))
        self.pilihan.pack(side="left", padx=8)
        self.tombol_betul = tk.Button(
            koreksi, text="Fix", command=self.betulkan, relief="flat",
            state="disabled", bg=WARNA["panel"], fg=WARNA["teks"], padx=12,
            activebackground=WARNA["latar"], activeforeground=WARNA["teks"])
        self.tombol_betul.pack(side="left")
        tk.Button(koreksi, text="Retrain", command=self.latih_ulang,
                  relief="flat", bg=WARNA["panel"], fg=WARNA["teks"], padx=12,
                  activebackground=WARNA["latar"],
                  activeforeground=WARNA["teks"]).pack(side="right")
        pakai = [r for r in konfig.RESEP
                 if r == "kantong" or fitur.encoder_ada()]
        self.resep = ttk.Combobox(koreksi, values=pakai, state="readonly",
                                  width=9, font=("Consolas", 9))
        self.resep.set(model["resep"] if model["resep"] in pakai else pakai[0])
        self.resep.pack(side="right", padx=8)

        bawah = tk.Frame(akar, bg=WARNA["latar"])
        bawah.pack(fill="x", padx=12, pady=(0, 12))
        self.masukan = tk.Entry(
            bawah, bg=WARNA["panel"], fg=WARNA["teks"], relief="flat",
            insertbackground=WARNA["teks"], font=("Consolas", 11))
        self.masukan.pack(side="left", fill="x", expand=True, ipady=7,
                          padx=(0, 8))
        self.masukan.bind("<Return>", self.kirim)
        self.masukan.focus_set()
        tk.Button(bawah, text="Send", command=self.kirim, relief="flat",
                  bg=WARNA["panel"], fg=WARNA["teks"], padx=18, pady=6,
                  activebackground=WARNA["latar"],
                  activeforeground=WARNA["teks"]).pack(side="right")

        self.status = tk.Label(akar, anchor="w", bg=WARNA["panel"],
                               fg=WARNA["redup"], font=("Consolas", 8),
                               padx=12, pady=4)
        self.status.pack(fill="x", side="bottom")
        self._status()

        self._tulis(f"{len(model['label'])} intents, "
                    f"{len(model['kosakata'])} columns, recipe "
                    f"{model['resep']}.", "redup")
        self._tulis("When a guess is wrong, pick the right intent below and "
                    "press Fix, then Retrain.", "redup")
        self._mode()
        self._panaskan()

    def _panaskan(self):
        """Muat encoder di utas latar.

        Tanpa ini, kalimat pertama menunggu 17 detik sementara jendelanya
        membeku. Utasnya tidak menyentuh tkinter sama sekali; laporannya
        dikirim balik lewat after() ke utas utama.
        """
        if self.model["resep"] == "kantong" or not fitur.encoder_ada():
            return

        def kerja():
            try:
                fitur.muat_encoder()
                pesan, tag = "encoder ready.", "redup"
            except Exception as e:                   # noqa: BLE001
                pesan, tag = f"encoder failed: {e}", "bahaya"
            self.akar.after(0, lambda: self._tulis(pesan, tag))

        self._tulis("loading encoder in the background...", "redup")
        threading.Thread(target=kerja, daemon=True).start()

    def _status(self):
        n = len(latih.baca_koreksi())
        self.status.config(
            text=f"recipe: {self.model['resep']}  |  fixes: {n}  |  "
                 f"{konfig.AUDIT.name}")

    def _tulis(self, teks, tag="teks"):
        self.obrolan.config(state="normal")
        self.obrolan.insert("end", teks + "\n", tag)
        self.obrolan.config(state="disabled")
        self.obrolan.see("end")

    def _mode(self):
        if self.kering.get():
            self._tulis("Dry run. Tools are not called.", "redup")
        else:
            self._tulis("LIVE mode. Tools will be called.", "bahaya")

    def _izin(self, rencana):
        # askyesno mengembalikan False kalau dialognya ditutup: bawaan menolak.
        return messagebox.askyesno(
            "SYNESIS needs permission",
            f"SYNESIS wants to run:\n\n    {rencana}\n\n"
            f"This is not a read-only tool. Allow?",
            default="no", icon="warning", parent=self.akar)

    def betulkan(self):
        intent = self.pilihan.get().strip()
        if not self.terakhir:
            return
        if intent not in niat.RUTE:
            self._tulis("  pick the correct intent in the dropdown first.", "bahaya")
            return
        latih.catat_koreksi(self.terakhir, intent)
        self._tulis(f"  recorded: '{self.terakhir[:40]}' -> {intent}",
                    "synesis")
        self.tombol_betul.config(state="disabled")
        self._status()

    def latih_ulang(self):
        self._tulis("\nretraining...", "redup")
        self.akar.update()
        try:
            r = latih.latih(self.resep.get(), diam=True)
        except Exception as e:                       # noqa: BLE001
            self._tulis(f"  failed: {type(e).__name__}: {e}", "bahaya")
            return
        self.model = niat.muat_model()
        self._panaskan()
        pesan = (f"  {r['resep']} {r['kolom']} columns  |  "
                 f"{r['detik']:.1f} s  |  "
                 f"{r['sintetis']} synthetic + {r['koreksi']} fixes")
        if r["skor"]:
            benar, n, p = r["skor"]
            pesan += f"  |  held-out {benar}/{n} = {p * 100:.1f}%"
        self._tulis(pesan, "synesis")
        self._status()

    def kirim(self, *_):
        teks = self.masukan.get().strip()
        if not teks:
            return
        if teks == "/latih":
            self.masukan.delete(0, "end")
            self.latih_ulang()
            return
        self.masukan.delete(0, "end")
        self._tulis(f"\nyou > {teks}", "kamu")

        # ponytail: satu utas. Alat baca instan, dan `jalankan` cuma hidup
        # sesudah manusia menekan Ya. Pindah ke utas pekerja kalau nanti ada
        # alat lambat yang tidak lewat dialog izin lebih dulu.
        h = niat.jalankan_pipa(teks, self.model, izin=self._izin,
                               kering=self.kering.get())

        self._tulis(f"  {h['intent'] or '(unknown)'}  "
                    f"conf {h['yakin']:.3f}  "
                    f"{RISIKO_EN.get(h['risiko'], '-')}  "
                    f"-> {TINDAKAN_EN.get(h['tindakan'], h['tindakan'])}",
                    NADA.get(h["tindakan"], "redup"))
        for baris in str(h["hasil"]).splitlines()[:40]:
            self._tulis(f"  {baris}", "teks")

        self.terakhir = teks
        self.pilihan.config(state="readonly")
        self.tombol_betul.config(state="normal")
        # SENGAJA dikosongkan. Kalau diisi tebakan model, satu klik Betulkan
        # tanpa mengganti apa pun akan MENGESAHKAN kesalahannya, dan model
        # belajar bahwa salahnya benar. Pilihan harus disengaja.
        self.pilihan.set("")


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    akar = tk.Tk()
    Jendela(akar, niat.muat_model(), kering="--sungguhan" not in argv)
    akar.mainloop()


def _demo():
    """Bangun jendelanya tanpa memunculkannya, dorong tiga kalimat lewat.

    Setel SYNESIS_AUDIT dulu kalau tidak mau mengotori catatan sungguhan.
    """
    akar = tk.Tk()
    akar.withdraw()
    j = Jendela(akar, niat.muat_model(), kering=True)
    for teks in ("cek ram sama cpu dong", "zzzqq wwwxx", ""):
        j.masukan.insert(0, teks)
        j.kirim()

    j.pilihan.set("cari_berkas")
    j.betulkan()
    akar.update()
    layar = j.obrolan.get("1.0", "end")
    kering_awal = j.kering.get()
    akar.destroy()
    assert kering_awal is True

    # Sengaja tidak memeriksa intent apa yang keluar: itu berubah tiap kali
    # model dilatih ulang, dan uji yang ikut berubah bukan uji.
    assert layar.count("you >") == 2       # yang kosong tidak dikirim
    assert layar.count("conf ") == 2       # tiap kiriman dapat putusan
    assert "unknown words" in layar        # kata asing berhenti sebelum model
    assert "recorded:" in layar            # koreksi tercatat
    print("jendela: lulus")


if __name__ == "__main__":
    main()
