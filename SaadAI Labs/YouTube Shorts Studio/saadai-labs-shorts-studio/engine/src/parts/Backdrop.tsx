import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {rand, useTheme} from '../lib';

/** Persistent animated brand background (gradient + slow floating shapes) so cuts feel continuous. */
export const Backdrop: React.FC<{dim?: boolean}> = ({dim}) => {
  const t = useTheme();
  const f = useCurrentFrame();
  const shapes = Array.from({length: 14}, (_, i) => i);
  return (
    <AbsoluteFill style={{background: `radial-gradient(120% 80% at 50% 20%, ${t.bg2} 0%, ${t.bg1} 70%)`, opacity: dim ? 0 : 1}}>
      {shapes.map((i) => {
        const x = rand(i + 1) * 1080;
        const y0 = rand(i + 31) * 1920;
        const size = 40 + rand(i + 7) * 150;
        const speed = 0.25 + rand(i + 13) * 0.6;
        const y = ((y0 - f * speed * 2) % 2100 + 2100) % 2100 - 90;
        const rot = f * (rand(i + 3) - 0.5) * 1.2;
        const isRing = i % 3 === 0;
        const col = i % 2 ? t.accent : t.accent2;
        return (
          <div
            key={i}
            style={{
              position: 'absolute',
              left: x - size / 2,
              top: y,
              width: size,
              height: size,
              borderRadius: i % 4 === 1 ? 24 : '50%',
              border: isRing ? `6px solid ${col}` : 'none',
              background: isRing ? 'transparent' : col,
              opacity: isRing ? 0.16 : 0.08,
              transform: `rotate(${rot}deg)`,
            }}
          />
        );
      })}
      <AbsoluteFill style={{background: 'radial-gradient(90% 60% at 50% 50%, transparent 55%, rgba(0,0,0,0.35) 100%)'}} />
    </AbsoluteFill>
  );
};
