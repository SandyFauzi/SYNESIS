---
name: animation-principles
description: This skill should be used when the user asks to "make this animation feel natural", "fix motion that feels stiff/floaty/cheap", "my animation looks robotic", "choose an easing curve", "how do I use the Graph Editor", "add overshoot or bounce", "Easy Ease isn't enough", "make snappy motion", "pick a duration for this transition", "stagger a list animation", "sync animation to a beat", or "review motion for good timing". It is the tech-agnostic foundation for deciding how something should move.
version: 0.1.0
---

# Motion Principles

Decide how something should move so it feels right — independent of the tool used to build it. Answers timing, easing, spacing, weight, and rhythm.

## Three Pillars
1. **Emotional intent**: What should the viewer feel? (joy, calm, urgency, trust, elegance)
2. **Visual narrative**: What's the micro-story? Setup → action → resolution
3. **Motion craft**: How do we make it believable? Physics, secondary motion, arcs, follow-through

## Three Motion Layers
- **Primary / Hero**: The main action the eye follows (1.0–1.5x speed).
- **Secondary / Support**: Supporting richness reacting to the primary (0.5–0.7x speed).
- **Ambient / Texture**: Background life that never demands attention (0.1–0.3x speed).

## Easing Curves
- **Enter / Appear**: ease-out `cubic-bezier(0.16, 1, 0.3, 1)` (fast start, gentle settle).
- **Exit / Disappear**: ease-in `cubic-bezier(0.7, 0, 0.84, 0)` (gentle start, fast exit).
- **Move / Reposition**: ease-in-out `cubic-bezier(0.65, 0, 0.35, 1)`.
- **Playful / Pop**: `cubic-bezier(0.34, 1.56, 0.64, 1)` (overshoot & settle).
