---
name: editor-berkelas
description: Master skill motion graphics, animasi terprogram, dan video editing kelas profesional untuk AI coding agent. Menggabungkan prinsip motion design (12 Disney principles, easing curves, timing), komposisi & safe-area (16:9, 9:16 vertical Reels/TikTok), kinetic typography, color motion, audio beat-sync, serta resep kode lengkap untuk Remotion (React/TS), Manim (Python math/physics), dan Motion Canvas (TypeScript generators). Gunakan skill ini setiap kali user meminta membuat/mengedit video, animasi, motion graphics, explainer, atau saat user memanggil "editor-berkelas".
version: 1.0.0
---

# Editor Berkelas: Master Motion Graphics & Programmatic Video

Panduan standar tertinggi untuk memproduksi motion graphic dan video berbasis kode (*video-as-code*) menggunakan **Remotion**, **Manim**, dan **Motion Canvas**.

---

## 1. Tiga Pilar Motion Design (Art Direction)

Sebelum menulis baris kode animasi apa pun, tentukan tiga keputusan utama:
1. **Emotional Intent**: Apa rasa yang ingin disampaikan? (Elegan, terpercaya, energik, atau santai).
2. **Visual Narrative**: Cerita mikro per-shot: *Setup $\rightarrow$ Action $\rightarrow$ Resolution*.
3. **Motion Craft**: Masuk akal secara fisik (ada akselerasi, deselerasi, inersia, dan bobot).

### Tiga Lapisan Gerak (Depth & Motion Hierarchy)
Jangan gerakkan semua elemen sekaligus. Pisahkan menjadi 3 lapisan:
- **Hero / Primary (1.0x - 1.5x speed)**: Elemen utama yang menjadi fokus mata (headline, ikon sentral, subjek).
- **Support / Secondary (0.5x - 0.7x speed)**: Elemen pendukung yang merespons hero (bayangan, kartu pembantu, grafik konteks).
- **Ambient / Texture (0.1x - 0.3x speed)**: Kehidupan latar belakang yang tidak mengalihkan perhatian (drifting gradient, grid halus, partikel lembut).

> **Prinsip Restraint (Pengendalian Diri)**: Motion berkelas ditentukan oleh apa yang **tidak** digerakkan. Jika elemen tidak membawa makna, biarkan statis.

---

## 2. Matematika Easing & Timing

**Haram hukumnya memakai `linear`** kecuali untuk putaran tanpa henti (*infinite spinner/marquee*). Semua gerak natural di alam semesta memiliki kurva percepatan.

| Jenis Aksi | Kurva Easing | Nilai Cubic-Bezier / Spring | Karakter Rasa |
| :--- | :--- | :--- | :--- |
| **Masuk (Entrance)** | Ease-Out | `cubic-bezier(0.16, 1, 0.3, 1)` | Datang cepat, mendarat anggun (*snappy settle*) |
| **Keluar (Exit)** | Ease-In | `cubic-bezier(0.7, 0, 0.84, 0)` | Mulai perlahan lalu melesat pergi |
| **Pindah (Reposition)** | Ease-In-Out | `cubic-bezier(0.65, 0, 0.35, 1)` | Simetris, halus, tidak terburu-buru |
| **Playful / Modern Pop** | Overshoot | `cubic-bezier(0.34, 1.56, 0.64, 1)` | Membal sedikit melewati target lalu kembali |

### Durasi Standar (Base Scale)
- **Micro-interaction (hover/toggle/icon pop)**: 150 – 250 ms.
- **Card reveal / UI transition**: 350 – 500 ms.
- **Hero scene entrance**: 600 – 850 ms.
- **Stagger offset**: 30 – 60 ms per baris/kartu. Hindari total cascade lebih dari 900 ms agar penonton tidak jenuh menunggu.

---

## 3. Tata Letak, Grid, & Safe Area

### Grid Standar
- Gunakan **12-Column Grid** untuk 16:9 (lebar 1920px: margin luar 80–120px, gutter 24–32px).
- Terapkan **Baseline Grid 8px**: Semua jarak margin, padding, dan font size menggunakan kelipatan 8 (8, 16, 24, 32, 48, 64px).
- **Rule of Thirds**: Letakkan fokus visual di garis 33% atau 67%, bukan selalu tepat di tengah mati (kecuali untuk simetri formal).

### Safe Area per Format
- **16:9 Landscape (YouTube / Desktop / TV)**:
  - Resolusi: `1920 x 1080`
  - Title safe margin: 10% dari setiap tepi frame (192px horizontal, 108px vertikal).
- **9:16 Vertical (TikTok / IG Reels / Shorts)**:
  - Resolusi: `1080 x 1920`
  - **Zona Terlarang UI**:
    - Bagian atas: sisakan minimal **160px** kosong (nama channel / search bar).
    - Bagian bawah: sisakan minimal **340px** kosong (caption, audio title, navigasi).
    - Bagian kanan: sisakan minimal **120px** kosong (tombol like, comment, share).
    - Konten utama harus berada di tengah (*Center Anchor Box*).

---

## 4. Tipografi Kinetik (Kinetic Typography)

1. **Aturan Statis Dulu**:
   - Judul besar (*Display headline*): Tracking dikurangi `-0.02em` s.d. `-0.03em`, line-height `1.1 – 1.2`.
   - Body text: line-height `1.5 – 1.6`.
2. **Teknik Reveal Favorit**:
   - **Mask / Clip Reveal (Paling Bersih)**: Bungkus teks dalam kontainer `overflow: hidden`, animasikan teks dari `translateY(110%)` ke `0%` dengan *ease-out*. Bebas artefak blur, sangat tajam di layar retina.
   - **Blur-in Elegance**: `filter: blur(12px) -> blur(0px)` + `opacity: 0 -> 1`.
3. **Granularitas Split**:
   - Kalimat/Paragraf: Split per **baris** (*line-by-line*).
   - Tagline tajam: Split per **kata** (*word-by-word*).
   - Judul pendek: Split per **karakter** (*char-by-char*).

---

## 5. Resep Kode Tiga Engine di Laptop Ini

Workspace lokal berada di: **`S:\Code\Editing\`**

### A. Remotion (`S:\Code\Editing\remotion-video`)
Framework React 19 + TypeScript.
```tsx
import { useCurrentFrame, useVideoConfig, interpolate, spring, AbsoluteFill, Sequence } from 'remotion';

export const HeroTitle: React.FC<{ text: string }> = ({ text }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Selalu clamp batas interpolate
  const opacity = interpolate(frame, [0, 20], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // Spring entrance yang dinamis
  const entrance = spring({
    frame,
    fps,
    config: { damping: 200, mass: 1, stiffness: 120 },
  });

  const translateY = interpolate(entrance, [0, 1], [40, 0]);

  return (
    <div style={{ overflow: 'hidden' }}>
      <h1 style={{
        opacity,
        transform: `translateY(${translateY}px)`,
        letterSpacing: '-0.02em',
        fontFamily: 'Inter, system-ui, sans-serif',
      }}>
        {text}
      </h1>
    </div>
  );
};
```
*Run CLI*: `npm run dev` (Remotion Studio) atau `npm run build`.

---

### B. Manim (`S:\Code\Editing\manimations`)
Animasi sains & matematika presisi via Python 3.12 (`uv`).
```python
from manim import *

class VisualFormula(Scene):
    def construct(self):
        # 1. Judul & Setup
        title = Text("Konsep Fisika Kuantum", font_size=42, weight=BOLD).to_edge(UP)
        formula1 = MathTex(r"E = h \cdot f").scale(1.4)
        formula2 = MathTex(r"E = \frac{h \cdot c}{\lambda}").scale(1.4)

        # 2. Sequence animasi terencana
        self.play(Write(title), run_time=0.8)
        self.play(FadeIn(formula1, shift=UP * 0.5), rate_func=smooth, run_time=1.0)
        self.wait(0.5)

        # Morphing antar formula
        self.play(TransformMatchingTex(formula1, formula2), run_time=1.2)
        self.wait(1.0)

        # Highlight komponen penting
        box = SurroundingRectangle(formula2, color=BLUE, buff=MED_LARGE_BUFF)
        self.play(Create(box), rate_func=smooth)
        self.wait(2.0)
```
*Run CLI*: `uv run manim -pql nama_file.py VisualFormula`

---

### C. Motion Canvas (`S:\Code\Editing\motion-canvas`)
TypeScript procedural motion berbasis generator & browser studio.
```tsx
import { makeScene2D, Circle, Txt, all, createRef, easeInOutCubic, easeOutBack } from '@motion-canvas/2d';

export default makeScene2D(function* (view) {
  const badge = createRef<Circle>();
  const label = createRef<Txt>();

  view.add(
    <Circle
      ref={badge}
      size={160}
      fill={'#4f46e5'}
      scale={0}
    />
  );

  view.add(
    <Txt
      ref={label}
      text="Editor Berkelas"
      fontFamily="Inter, sans-serif"
      fontWeight={700}
      fill="#ffffff"
      opacity={0}
      y={120}
    />
  );

  // Jalankan animasi paralel yang sinkron
  yield* all(
    badge().scale(1, 0.8, easeOutBack),
    badge().fill('#3b82f6', 0.8, easeInOutCubic),
  );

  yield* all(
    label().opacity(1, 0.5),
    label().y(140, 0.5, easeInOutCubic),
  );
});
```
*Run CLI*: `npm run serve` (membuka editor interaktif di browser).

---

## 6. Prosedur Verifikasi Mandiri (*Deliver-and-Verify Loop*)

Sebelum menyelesaikan hasil pekerjaan ke pengguna, lakukan audit 4 langkah:
1. **Pengecekan Teks (Overflow Check)**: Pastikan tidak ada teks yang menabrak batas layar atau safe area media sosial.
2. **Audit Easing**: Pastikan tidak ada pergerakan patah atau kaku yang menggunakan `linear` secara tidak sengaja.
3. **Contrast Ratio**: Tulisan di atas background harus memiliki rasio kontras minimal 4.5:1.
4. **Validasi Loop / Hold**: Di akhir video atau scene, beri durasi tahan (*hold time*) minimal 1.5–2 detik agar audiens sempat membaca sebelum cut/loop.
