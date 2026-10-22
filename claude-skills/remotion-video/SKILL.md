---
name: remotion-video
description: This skill should be used when the user asks to "make a video with Remotion", "create a programmatic/data-driven video in React", "render an MP4/GIF from code", "animate with useCurrentFrame/interpolate/spring", "sync video to audio/beats", or "render a templated video per record headlessly". Covers building React compositions and rendering them via CLI or @remotion/renderer.
version: 0.1.0
---

# Remotion (Programmatic Video)

Build real MP4/GIF/WebM videos in React. Every frame is a pure function of `useCurrentFrame()`, so output is deterministic, scrubbable, diffable, and renderable in CI. The code-first alternative to After Effects for templated and data-driven motion graphics.

## When to use

- Render MP4/GIF/WebM from code (social clips, title cards, explainers).
- Templated/data-driven videos: one composition, many outputs from props (per-user, per-record, per-row of a CSV/DB).
- Motion graphics that must be versioned, code-reviewed, and rendered in CI without a GUI.
- Programmatic audio sync, charts that animate from data, or embedding shaders/Three.js into video.

## Core techniques

### Frame-driven animation

Animation is derived from the current frame, never from `setState` or `requestAnimationFrame`. `interpolate` maps an input range to an output range; `spring` produces physically natural motion.

```jsx
import {useCurrentFrame, useVideoConfig, interpolate, spring} from 'remotion';

export const Title = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  // Fade in over frames 0-30, then stay (clamp prevents over/undershoot).
  const opacity = interpolate(frame, [0, 30], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // Spring entrance; divide by spring duration is unnecessary — drive transforms directly.
  const scale = spring({frame, fps, config: {damping: 200, mass: 1, stiffness: 100}});

  return <h1 style={{opacity, transform: `scale(${scale})`}}>Hello</h1>;
};
```

Always clamp `interpolate` unless an intentional overshoot is desired — by default it extrapolates linearly past the range, which produces opacity > 1 or negative values.

### Scheduling: Sequence and Series

`<Sequence>` shifts time: children see `frame` reset to 0 at the sequence's `from`. Use it to place clips on a timeline. `<Series>` lays out back-to-back segments without manual offset math.

```jsx
import {Sequence, Series, AbsoluteFill} from 'remotion';

export const Timeline = () => (
  <AbsoluteFill style={{backgroundColor: 'black'}}>
    <Sequence from={0} durationInFrames={60}><Intro /></Sequence>
    <Sequence from={60} durationInFrames={90}><Body /></Sequence>

    {/* Series auto-sequences; offset overlaps the previous segment for crossfades */}
    <Series>
      <Series.Sequence durationInFrames={60}><ShotA /></Series.Sequence>
      <Series.Sequence durationInFrames={60} offset={-15}><ShotB /></Series.Sequence>
    </Series>
  </AbsoluteFill>
);
```

### Composition registration + parametric props

The `<Composition>` declares id, size, fps, duration, and `defaultProps`. A zod schema makes props type-safe and editable in the Studio sidebar.

```jsx
import {Composition} from 'remotion';
import {z} from 'zod';

export const schema = z.object({
  title: z.string(),
  accent: z.string(),
  fps: z.number().default(30),
});

export const Root = () => (
  <Composition
    id="Promo"
    component={Promo}
    durationInFrames={150}
    fps={30}
    width={1080}
    height={1920}
    schema={schema}
    defaultProps={{title: 'Launch', accent: '#5b8cff', fps: 30}}
  />
);
```

To make duration data-dependent, use `calculateMetadata` on the Composition to compute `durationInFrames` from props (e.g. number of rows × frames per row) before render.
