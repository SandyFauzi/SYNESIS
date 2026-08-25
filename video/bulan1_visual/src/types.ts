export type CodeLine = {no: number; text: string};

export type Segment = {
  start: number;
  duration: number;
  chapter: string;
  file: string;
  line: number;
  totalLines: number;
  window: CodeLine[];
  caption: string;
  scope: string;
  visual: string;
};

export type Chapter = {
  id: string;
  title: string;
  file: string;
  start: number;
  duration: number;
  manim: string;
  manimFrames: number;
  segments: number[];
};

export type Storyboard = {
  fps: number;
  width: number;
  height: number;
  totalFrames: number;
  chapters: Chapter[];
  segments: Segment[];
};
