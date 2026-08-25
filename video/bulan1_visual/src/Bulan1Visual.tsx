import React from 'react';
import {
  AbsoluteFill,
  Loop,
  OffthreadVideo,
  Sequence,
  staticFile,
  useCurrentFrame,
} from 'remotion';
import {CodePanel} from './CodePanel';
import {VisualStage} from './VisualStage';
import type {Chapter, Segment, Storyboard} from './types';

const findSegment = (segments: Segment[], frame: number): Segment => {
  let low = 0;
  let high = segments.length - 1;
  while (low <= high) {
    const mid = (low + high) >> 1;
    if (segments[mid].start <= frame) low = mid + 1;
    else high = mid - 1;
  }
  return segments[Math.max(0, high)];
};

const findChapter = (chapters: Chapter[], frame: number): Chapter =>
  chapters.find((chapter) => frame >= chapter.start && frame < chapter.start + chapter.duration)
  ?? chapters[chapters.length - 1];

const ManimBackground: React.FC<{storyboard: Storyboard}> = ({storyboard}) => (
  <>
    {storyboard.chapters.map((chapter) => (
      <Sequence key={chapter.id} from={chapter.start} durationInFrames={chapter.duration} premountFor={30}>
        <Loop durationInFrames={chapter.manimFrames}>
          <OffthreadVideo
            src={staticFile(chapter.manim)}
            muted
            style={{position: 'absolute', top: 5, left: 25, width: 670, height: 670, objectFit: 'cover'}}
          />
        </Loop>
      </Sequence>
    ))}
  </>
);

export const Bulan1Visual: React.FC<{storyboard: Storyboard}> = ({storyboard}) => {
  const frame = useCurrentFrame();
  const segment = findSegment(storyboard.segments, frame);
  const chapter = findChapter(storyboard.chapters, frame);
  const chapterProgress = Math.min(1, Math.max(0, (frame - chapter.start) / chapter.duration));
  const totalProgress = Math.min(1, frame / (storyboard.totalFrames - 1));
  const outro = frame >= storyboard.totalFrames - storyboard.fps * 3;

  return (
    <AbsoluteFill style={{background: '#08080C', color: '#EDF2F7', fontFamily: 'Arial, sans-serif'}}>
      <div style={{position: 'absolute', inset: 0, background: 'radial-gradient(circle at 50% 18%, rgba(31,58,73,.30), transparent 42%)'}} />
      <ManimBackground storyboard={storyboard} />
      <div style={{position: 'absolute', left: 0, right: 0, top: 0, height: 78, background: 'linear-gradient(180deg,#08080C 68%,transparent)', padding: '18px 24px', display: 'flex', alignItems: 'flex-start', zIndex: 5}}>
        <div style={{flex: 1}}>
          <div style={{fontFamily: 'Consolas, monospace', color: '#37E68A', fontSize: 12, letterSpacing: 1.4}}>MAKE A JARVIS · BULAN 1</div>
          <div style={{fontSize: 20, fontWeight: 700, marginTop: 4}}>{chapter.title}</div>
        </div>
        <div style={{fontFamily: 'Consolas, monospace', fontSize: 12, color: '#7C8797', marginTop: 6}}>SESI {storyboard.chapters.indexOf(chapter) + 1}/4</div>
      </div>
      <VisualStage segment={segment} />
      <CodePanel segment={segment} chapterProgress={chapterProgress} />
      <div style={{position: 'absolute', left: 0, right: 0, bottom: 0, height: 7, background: '#171D25'}}>
        <div style={{height: '100%', width: `${totalProgress * 100}%`, background: '#37E68A'}} />
      </div>
      {outro && (
        <AbsoluteFill style={{zIndex: 20, alignItems: 'center', justifyContent: 'center', background: 'rgba(8,8,12,.94)'}}>
          <div style={{fontFamily: 'Consolas, monospace', fontSize: 14, color: '#37E68A', letterSpacing: 2}}>BULAN 1 · SELESAI</div>
          <div style={{fontSize: 38, fontWeight: 800, marginTop: 13}}>Autograd → MLP → MNIST</div>
          <div style={{fontSize: 30, fontWeight: 750, marginTop: 7, color: '#C9D2DC'}}>Tensor → Optimizer</div>
          <div style={{fontSize: 20, color: '#8994A3', marginTop: 12}}>1.526 baris sudah dilihat, satu per satu.</div>
        </AbsoluteFill>
      )}
    </AbsoluteFill>
  );
};
