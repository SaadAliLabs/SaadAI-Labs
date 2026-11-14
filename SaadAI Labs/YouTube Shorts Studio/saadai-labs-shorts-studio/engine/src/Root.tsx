import React from 'react';
import {Composition} from 'remotion';
import {Short} from './Short';
import {ShortProps} from './lib';
import sample from '../sample-props.json';

export const Root: React.FC = () => {
  return (
    <Composition
      id="Short"
      component={Short as unknown as React.FC<Record<string, unknown>>}
      width={1080}
      height={1920}
      fps={30}
      durationInFrames={300}
      defaultProps={sample as unknown as Record<string, unknown>}
      calculateMetadata={({props}) => {
        const p = props as unknown as ShortProps;
        return {durationInFrames: Math.max(30, p.durationInFrames || 300), fps: p.fps || 30};
      }}
    />
  );
};
