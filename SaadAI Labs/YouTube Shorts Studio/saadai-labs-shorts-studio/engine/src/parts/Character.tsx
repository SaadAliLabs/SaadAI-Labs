import React from 'react';
import {useCurrentFrame} from 'remotion';
import {CharacterCfg} from '../lib';

export type Expr = 'neutral' | 'happy' | 'sad' | 'shocked' | 'angry' | 'thinking' | 'smug';
export type Pose = 'idle' | 'wave' | 'point' | 'cheer' | 'shrug' | 'think' | 'hips' | 'facepalm' | 'run';

// [upper, forearm] angles in degrees for left and right arm. 0 = hanging down; positive = towards the viewer's left.
const POSES: Record<Pose, {l: [number, number]; r: [number, number]}> = {
  idle: {l: [10, 6], r: [-10, -6]},
  wave: {l: [10, 6], r: [-125, -40]},
  point: {l: [10, 6], r: [-88, -4]},
  cheer: {l: [155, 10], r: [-155, -10]},
  shrug: {l: [55, -105], r: [-55, 105]},
  think: {l: [10, 6], r: [-28, -138]},
  hips: {l: [42, -88], r: [-42, 88]},
  facepalm: {l: [10, 6], r: [-35, -150]},
  run: {l: [-40, 70], r: [40, -70]},
};

const darker = (hex: string, k = 0.78) => {
  const h = hex.replace('#', '');
  if (h.length !== 6) return hex;
  const n = (i: number) => Math.round(parseInt(h.slice(i, i + 2), 16) * k).toString(16).padStart(2, '0');
  return `#${n(0)}${n(2)}${n(4)}`;
};

const Arm: React.FC<{x: number; y: number; a: [number, number]; color: string; skin: string}> = ({x, y, a, color, skin}) => (
  <g transform={`translate(${x} ${y}) rotate(${a[0]})`}>
    <rect x={-15} y={-6} width={30} height={84} rx={15} fill={color} />
    <g transform={`translate(0 72) rotate(${a[1]})`}>
      <rect x={-13} y={-4} width={26} height={74} rx={13} fill={color} />
      <circle cx={0} cy={74} r={19} fill={skin} />
    </g>
  </g>
);

/**
 * Flat 2D character drawn in SVG (viewBox 300x620, feet at y≈612).
 * Idle bob, blinking, expressions, arm poses and a mouth that flaps while `talking`.
 */
export const Character: React.FC<{cfg: CharacterCfg; expr?: Expr; pose?: Pose; talking?: boolean; height?: number; flip?: boolean; seed?: number}> = ({
  cfg,
  expr = 'neutral',
  pose = 'idle',
  talking = false,
  height = 640,
  flip = false,
  seed = 0,
}) => {
  const f = useCurrentFrame() + seed * 17;
  const skin = cfg.skin ?? '#f2c39b';
  const hairC = cfg.hairColor ?? '#2b1d14';
  const shirt = cfg.shirt ?? '#4f7cff';
  const pants = cfg.pants ?? '#2a2f45';
  const shoes = cfg.shoes ?? '#1b1b22';
  const hair = cfg.hair ?? 'short';
  const P = POSES[pose] ?? POSES.idle;
  const wave = pose === 'wave' ? Math.sin(f / 3.2) * 22 : 0;
  const runSwing = pose === 'run' ? Math.sin(f / 2.5) : 0;
  const l: [number, number] = pose === 'run' ? [P.l[0] * runSwing, P.l[1]] : P.l;
  const r: [number, number] = pose === 'run' ? [P.r[0] * runSwing, P.r[1]] : [P.r[0], P.r[1] + wave];
  const bob = Math.sin(f / 9) * 5 + (pose === 'run' ? Math.abs(Math.sin(f / 2.5)) * -14 : 0);
  const blinkPhase = f % 96;
  const blink = blinkPhase < 4 ? Math.abs(blinkPhase - 2) / 2 : 1;
  const mouthOpen = talking ? 0.35 + 0.65 * Math.abs(Math.sin(f / 2.1)) * (0.6 + 0.4 * Math.sin(f / 5.3)) : 0;
  const headTilt = talking ? Math.sin(f / 11) * 3 : Math.sin(f / 23) * 1.5;
  const legSwing = pose === 'run' ? Math.sin(f / 2.5) * 28 : 0;

  const brows: Record<Expr, [number, number]> = {neutral: [0, 0], happy: [-6, 0], sad: [14, -6], shocked: [-16, 0], angry: [-16, 8], thinking: [-14, 0], smug: [-4, 4]};
  const [browLift, browTilt] = brows[expr] ?? [0, 0];
  const eyeY = 182;
  const big = expr === 'shocked';

  let mouth: React.ReactNode;
  if (talking || expr === 'shocked') {
    const ry = expr === 'shocked' && !talking ? 16 : 4 + 15 * mouthOpen;
    mouth = <ellipse cx={150} cy={232} rx={expr === 'shocked' ? 16 : 20} ry={ry} fill="#5a1f2a" />;
  } else if (expr === 'happy') {
    mouth = <path d="M122 224 Q150 256 178 224 Q150 236 122 224 Z" fill="#5a1f2a" />;
  } else if (expr === 'sad') {
    mouth = <path d="M128 240 Q150 222 172 240" stroke="#5a1f2a" strokeWidth={7} fill="none" strokeLinecap="round" />;
  } else if (expr === 'angry') {
    mouth = <path d="M128 236 L172 236" stroke="#5a1f2a" strokeWidth={8} strokeLinecap="round" />;
  } else if (expr === 'thinking') {
    mouth = <path d="M140 236 Q158 230 170 238" stroke="#5a1f2a" strokeWidth={7} fill="none" strokeLinecap="round" />;
  } else if (expr === 'smug') {
    mouth = <path d="M130 232 Q160 246 176 226" stroke="#5a1f2a" strokeWidth={7} fill="none" strokeLinecap="round" />;
  } else {
    mouth = <path d="M132 232 Q150 242 168 232" stroke="#5a1f2a" strokeWidth={7} fill="none" strokeLinecap="round" />;
  }

  const hairBack = hair === 'long' ? <path d="M70 170 Q66 330 92 352 L208 352 Q234 330 230 170 Z" fill={hairC} /> : null;
  let hairTop: React.ReactNode = null;
  if (hair === 'short' || hair === 'long') hairTop = <path d="M72 178 Q70 92 150 88 Q232 92 228 178 Q214 132 172 126 Q120 128 96 150 Q80 162 72 178 Z" fill={hairC} />;
  if (hair === 'bun') hairTop = <g fill={hairC}><circle cx={150} cy={78} r={36} /><path d="M72 176 Q72 98 150 96 Q228 98 228 176 Q200 130 150 128 Q100 130 72 176 Z" /></g>;
  if (hair === 'curly') hairTop = <g fill={hairC}>{[[86, 150], [102, 116], [132, 98], [168, 98], [198, 116], [214, 150], [150, 108]].map(([x, y], k) => <circle key={k} cx={x} cy={y} r={30} />)}</g>;
  if (hair === 'spiky') hairTop = <path d="M74 176 L84 108 L108 128 L122 82 L146 116 L166 74 L182 116 L206 92 L210 132 L230 120 L226 176 Q200 132 150 130 Q100 132 74 176 Z" fill={hairC} />;
  if (hair === 'cap') hairTop = <g><path d="M72 170 Q72 92 150 90 Q228 92 228 170 Z" fill={hairC} /><rect x={150} y={150} width={120} height={22} rx={11} fill={darker(hairC)} /></g>;

  return (
    <svg viewBox="0 0 300 620" height={height} style={{overflow: 'visible', transform: flip ? 'scaleX(-1)' : undefined}}>
      <ellipse cx={150} cy={612} rx={96} ry={14} fill="rgba(0,0,0,0.18)" />
      <g transform={`translate(0 ${bob})`}>
        {/* legs */}
        <g transform={`rotate(${legSwing} 128 440)`}><rect x={112} y={430} width={34} height={160} rx={16} fill={pants} /><ellipse cx={124} cy={596} rx={30} ry={14} fill={shoes} /></g>
        <g transform={`rotate(${-legSwing} 172 440)`}><rect x={154} y={430} width={34} height={160} rx={16} fill={pants} /><ellipse cx={176} cy={596} rx={30} ry={14} fill={shoes} /></g>
        {hairBack}
        {/* torso */}
        <rect x={86} y={266} width={128} height={196} rx={52} fill={shirt} />
        <path d="M128 270 L150 300 L172 270 Z" fill={darker(shirt, 0.85)} />
        <rect x={134} y={244} width={32} height={34} rx={10} fill={darker(skin, 0.92)} />
        <Arm x={96} y={292} a={l} color={darker(shirt, 0.9)} skin={skin} />
        <Arm x={204} y={292} a={r} color={darker(shirt, 0.9)} skin={skin} />
        {/* head */}
        <g transform={`rotate(${headTilt} 150 250)`}>
          <circle cx={74} cy={190} r={16} fill={darker(skin, 0.95)} />
          <circle cx={226} cy={190} r={16} fill={darker(skin, 0.95)} />
          <circle cx={150} cy={178} r={80} fill={skin} />
          {hairTop}
          {cfg.beard ? <path d="M84 196 Q92 268 150 270 Q208 268 216 196 Q196 246 150 248 Q104 246 84 196 Z" fill={hairC} /> : null}
          {/* brows */}
          <rect x={102} y={eyeY - 40 + browLift + browTilt} width={38} height={9} rx={4.5} fill={hairC} transform={`rotate(${browTilt * 1.6} 121 ${eyeY - 36})`} />
          <rect x={160} y={eyeY - 40 + browLift + (expr === 'thinking' ? -6 : browTilt)} width={38} height={9} rx={4.5} fill={hairC} transform={`rotate(${-browTilt * 1.6} 179 ${eyeY - 36})`} />
          {/* eyes */}
          {big ? (
            <g>
              <circle cx={121} cy={eyeY} r={20} fill="#fff" /><circle cx={179} cy={eyeY} r={20} fill="#fff" />
              <circle cx={121} cy={eyeY} r={9} fill="#1b1b22" /><circle cx={179} cy={eyeY} r={9} fill="#1b1b22" />
            </g>
          ) : expr === 'happy' && !talking ? (
            <g stroke="#1b1b22" strokeWidth={7} fill="none" strokeLinecap="round">
              <path d={`M108 ${eyeY + 4} Q121 ${eyeY - 12} 134 ${eyeY + 4}`} /><path d={`M166 ${eyeY + 4} Q179 ${eyeY - 12} 192 ${eyeY + 4}`} />
            </g>
          ) : (
            <g fill="#1b1b22">
              <ellipse cx={121} cy={eyeY} rx={10} ry={12 * blink} /><ellipse cx={179} cy={eyeY} rx={10} ry={12 * blink} />
              <circle cx={124} cy={eyeY - 4} r={3} fill="#fff" opacity={blink} /><circle cx={182} cy={eyeY - 4} r={3} fill="#fff" opacity={blink} />
            </g>
          )}
          {cfg.glasses ? (
            <g stroke="#1b1b22" strokeWidth={6} fill="rgba(255,255,255,0.15)"><circle cx={121} cy={eyeY} r={26} /><circle cx={179} cy={eyeY} r={26} /><path d="M147 180 L153 180" /></g>
          ) : null}
          {expr === 'happy' || expr === 'smug' ? <g fill="#ff8a8a" opacity={0.45}><circle cx={100} cy={214} r={13} /><circle cx={200} cy={214} r={13} /></g> : null}
          {expr === 'sad' ? <path d="M196 204 q6 14 0 20 q-6 -6 0 -20 Z" fill="#7fc8ff" /> : null}
          {mouth}
        </g>
      </g>
    </svg>
  );
};
