import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';

/** Entry/exit motion shared by every scene: quick spring rise + slight zoom, short fade at the cut. */
export const SceneIn: React.FC<{children: React.ReactNode; dur: number; pre?: number; fadeOut?: boolean; kind: string}> = ({
  children,
  dur,
  pre = 0,
  fadeOut = true,
  kind,
}) => {
  const f = useCurrentFrame() + pre;
  const {fps} = useVideoConfig();
  const s = spring({frame: f, fps, config: {damping: 15, stiffness: 190, mass: 0.7}});
  const out = fadeOut
    ? interpolate(f - pre, [dur - 4, dur], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})
    : 1;
  const story = kind === 'story';
  const ty = story ? 0 : interpolate(s, [0, 1], [110, 0]);
  const sc = story ? interpolate(s, [0, 1], [1.08, 1]) : interpolate(s, [0, 1], [0.9, 1]);
  const op = story ? Math.min(1, s * 2.2) : Math.min(1, s * 1.6);
  return (
    <AbsoluteFill style={{opacity: op * out, transform: `translateY(${ty}px) scale(${sc})`}}>{children}</AbsoluteFill>
  );
};
