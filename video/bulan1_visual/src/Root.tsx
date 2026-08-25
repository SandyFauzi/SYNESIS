import React from 'react';
import {Composition} from 'remotion';
import rawStoryboard from './storyboard.json';
import type {Storyboard} from './types';
import {Bulan1Visual} from './Bulan1Visual';

const storyboard = rawStoryboard as Storyboard;

export const Root: React.FC = () => (
  <Composition
    id="Bulan1Visual"
    component={Bulan1Visual}
    durationInFrames={storyboard.totalFrames}
    fps={storyboard.fps}
    width={storyboard.width}
    height={storyboard.height}
    defaultProps={{storyboard}}
  />
);
