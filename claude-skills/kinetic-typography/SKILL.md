---
name: kinetic-typography
description: This skill should be used when the user asks to "animate a headline", "make a kinetic typography video", "do a split-text reveal", "stagger text by character/word/line", "make a lyric or caption video", "animate a variable font weight", "put text on a path", or "create an animated title card". Covers reveal techniques in CSS, GSAP SplitText, Framer Motion, and Remotion.
version: 0.1.0
---

# Kinetic Typography

Animate text expressively: splitting copy into lines/words/characters, staggering reveals, masking, blurring, and morphing weight.

## Core Rules
1. **Static Type First**: Lock line-height (1.1-1.2 for headlines), tracking (tighten display by -1% to -3%), and alignment before animating.
2. **Split Granularity**:
   - By line: Calmest, most premium.
   - By word: Energetic, great for taglines & lyric hits.
   - By character: Most kinetic/playful.
3. **Mask / Clip Reveal**:
   - Wrap each line in `overflow: hidden`.
   - Animate the child from `translateY(110%)` to `0%` using `cubic-bezier(0.16, 1, 0.3, 1)`.
   - Stagger: lines 60-100ms, words 40-70ms, characters 20-40ms apart.
