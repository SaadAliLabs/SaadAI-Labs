import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {rand} from '../lib';

// Flat 2D backgrounds, 1080x1920. Ground line at y=1200 (characters stand on it, captions sit below it).
export const GROUND = 1200;

const Sky: React.FC<{a: string; b: string}> = ({a, b}) => <AbsoluteFill style={{background: `linear-gradient(180deg, ${a} 0%, ${b} 100%)`}} />;

const Cloud: React.FC<{x: number; y: number; s: number; speed: number}> = ({x, y, s, speed}) => {
  const f = useCurrentFrame();
  const cx = ((x + f * speed) % 1400) - 160;
  return (
    <g transform={`translate(${cx} ${y}) scale(${s})`} fill="#fff" opacity={0.9}>
      <ellipse cx={0} cy={0} rx={90} ry={44} /><ellipse cx={60} cy={-26} rx={64} ry={50} /><ellipse cx={120} cy={4} rx={80} ry={40} />
    </g>
  );
};

const Stars: React.FC<{n: number}> = ({n}) => {
  const f = useCurrentFrame();
  return (
    <g>
      {Array.from({length: n}, (_, i) => (
        <circle key={i} cx={rand(i + 5) * 1080} cy={rand(i + 77) * 1150} r={2 + rand(i + 9) * 4} fill="#fff" opacity={0.4 + 0.6 * Math.abs(Math.sin(f / (12 + rand(i) * 20) + i))} />
      ))}
    </g>
  );
};

const City: React.FC = () => (
  <>
    <Sky a="#7fd0ff" b="#d8f1ff" />
    <svg viewBox="0 0 1080 1920" style={{position: 'absolute', inset: 0}}>
      <circle cx={820} cy={330} r={110} fill="#ffe37a" />
      <Cloud x={100} y={260} s={1} speed={0.6} /><Cloud x={700} y={480} s={0.7} speed={0.9} />
      {[0, 1, 2, 3, 4, 5, 6].map((i) => {
        const w = 150 + rand(i + 3) * 60;
        const h = 360 + rand(i + 11) * 420;
        const x = i * 160 - 30;
        const col = ['#5b6cff', '#7c5cff', '#4a8bd6', '#6a7ab8', '#8a6be0'][i % 5];
        return (
          <g key={i}>
            <rect x={x} y={GROUND - h} width={w} height={h} fill={col} />
            {Array.from({length: Math.floor(h / 70)}, (_, r) => [0, 1, 2].map((c) => (
              <rect key={`${r}-${c}`} x={x + 22 + c * 42} y={GROUND - h + 30 + r * 70} width={26} height={36} rx={4} fill={rand(i * 31 + r * 7 + c) > 0.45 ? '#ffe9a8' : 'rgba(255,255,255,0.35)'} />
            )))}
          </g>
        );
      })}
      <rect x={0} y={GROUND} width={1080} height={720} fill="#3c4058" />
      <rect x={0} y={GROUND} width={1080} height={26} fill="#9aa0b8" />
      {[0, 1, 2, 3, 4].map((i) => <rect key={i} x={i * 240 + 30} y={GROUND + 140} width={140} height={16} rx={8} fill="#f4f4f4" opacity={0.6} />)}
    </svg>
  </>
);

const Room: React.FC = () => (
  <>
    <Sky a="#ffe8d6" b="#ffd9c0" />
    <svg viewBox="0 0 1080 1920" style={{position: 'absolute', inset: 0}}>
      <rect x={620} y={330} width={330} height={400} rx={18} fill="#9fdcff" stroke="#fff" strokeWidth={22} />
      <path d="M785 330 L785 730 M620 530 L950 530" stroke="#fff" strokeWidth={14} />
      <rect x={130} y={380} width={240} height={180} rx={10} fill="#ff9f7a" stroke="#7a4a3a" strokeWidth={14} />
      <circle cx={250} cy={470} r={45} fill="#ffe37a" />
      <rect x={0} y={GROUND} width={1080} height={720} fill="#c98f62" />
      {[0, 1, 2, 3, 4, 5].map((i) => <rect key={i} x={0} y={GROUND + i * 60} width={1080} height={4} fill="#b07a50" />)}
      <rect x={60} y={GROUND - 230} width={110} height={230} rx={20} fill="#e0784e" />
      <g fill="#3fa66b"><ellipse cx={115} cy={GROUND - 290} rx={70} ry={90} /><ellipse cx={70} cy={GROUND - 240} rx={50} ry={60} /><ellipse cx={160} cy={GROUND - 240} rx={50} ry={60} /></g>
    </svg>
  </>
);

const Park: React.FC = () => (
  <>
    <Sky a="#8fd8ff" b="#e4f7ff" />
    <svg viewBox="0 0 1080 1920" style={{position: 'absolute', inset: 0}}>
      <circle cx={200} cy={300} r={100} fill="#ffe37a" />
      <Cloud x={400} y={300} s={1.1} speed={0.5} /><Cloud x={900} y={520} s={0.8} speed={0.8} />
      <ellipse cx={250} cy={GROUND + 40} rx={600} ry={260} fill="#7ccf6b" />
      <ellipse cx={900} cy={GROUND + 60} rx={560} ry={300} fill="#69bf5c" />
      {[[120, 0.9], [930, 1.1], [760, 0.7]].map(([x, s], i) => (
        <g key={i} transform={`translate(${x} ${GROUND - 20}) scale(${s})`}>
          <rect x={-22} y={-260} width={44} height={260} rx={14} fill="#8a5a3c" />
          <circle cx={0} cy={-320} r={120} fill="#3fa65a" /><circle cx={-80} cy={-260} r={80} fill="#46b062" /><circle cx={80} cy={-260} r={80} fill="#46b062" />
        </g>
      ))}
      <rect x={0} y={GROUND} width={1080} height={720} fill="#5aae4e" />
    </svg>
  </>
);

const Office: React.FC = () => (
  <>
    <Sky a="#e9ecff" b="#d7dcf7" />
    <svg viewBox="0 0 1080 1920" style={{position: 'absolute', inset: 0}}>
      {[0, 1, 2].map((i) => <rect key={i} x={110 + i * 150} y={330} width={110} height={160} rx={8} fill={['#ff9f7a', '#7ab8ff', '#ffd36a'][i]} />)}
      <rect x={80} y={500} width={500} height={16} rx={8} fill="#a7adc9" />
      <rect x={640} y={300} width={340} height={260} rx={20} fill="#2d3150" />
      <rect x={662} y={322} width={296} height={200} rx={10} fill="#6ad1ff" opacity={0.85} />
      <rect x={0} y={GROUND} width={1080} height={720} fill="#9097b5" />
      <rect x={560} y={GROUND - 330} width={480} height={30} rx={10} fill="#7a5a44" />
      <rect x={600} y={GROUND - 300} width={26} height={300} fill="#6a4c39" /><rect x={980} y={GROUND - 300} width={26} height={300} fill="#6a4c39" />
      <rect x={720} y={GROUND - 520} width={230} height={170} rx={14} fill="#1f2238" /><rect x={734} y={GROUND - 506} width={202} height={130} rx={8} fill="#7fe0c0" />
      <rect x={820} y={GROUND - 352} width={30} height={24} fill="#1f2238" />
    </svg>
  </>
);

const Night: React.FC = () => (
  <>
    <Sky a="#0b1030" b="#2b2a6b" />
    <svg viewBox="0 0 1080 1920" style={{position: 'absolute', inset: 0}}>
      <Stars n={70} />
      <circle cx={800} cy={320} r={110} fill="#fff6c8" /><circle cx={845} cy={290} r={100} fill="#1a1d48" />
      {[0, 1, 2, 3, 4].map((i) => {
        const x = i * 230 - 20;
        const h = 220 + rand(i + 2) * 200;
        return (
          <g key={i}>
            <rect x={x} y={GROUND - h} width={200} height={h} fill="#1c1f44" />
            <path d={`M${x - 10} ${GROUND - h} L${x + 100} ${GROUND - h - 90} L${x + 210} ${GROUND - h} Z`} fill="#1c1f44" />
            <rect x={x + 70} y={GROUND - h + 60} width={50} height={60} rx={6} fill="#ffd96a" opacity={0.85} />
          </g>
        );
      })}
      <rect x={0} y={GROUND} width={1080} height={720} fill="#14173a" />
    </svg>
  </>
);

const Space: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <>
      <Sky a="#05061a" b="#1a0f3d" />
      <svg viewBox="0 0 1080 1920" style={{position: 'absolute', inset: 0}}>
        <Stars n={110} />
        <g transform={`translate(780 430) rotate(${-18 + Math.sin(f / 60) * 2})`}>
          <circle r={150} fill="#ff9f5a" /><ellipse rx={270} ry={50} fill="none" stroke="#ffd7a8" strokeWidth={18} opacity={0.8} />
        </g>
        <circle cx={200} cy={820} r={60} fill="#7ab8ff" /><circle cx={185} cy={805} r={20} fill="#5ad19a" />
        <ellipse cx={540} cy={GROUND + 520} rx={900} ry={560} fill="#9aa0b8" />
        {[[300, GROUND + 80, 50], [760, GROUND + 140, 70], [520, GROUND + 260, 40]].map(([x, y, r], i) => <circle key={i} cx={x} cy={y} r={r} fill="#7f859e" />)}
      </svg>
    </>
  );
};

const Classroom: React.FC = () => (
  <>
    <Sky a="#fff1d0" b="#ffe5b0" />
    <svg viewBox="0 0 1080 1920" style={{position: 'absolute', inset: 0}}>
      <rect x={90} y={300} width={900} height={480} rx={20} fill="#2f6b4f" stroke="#8a5a3c" strokeWidth={24} />
      <path d="M170 420 q60 -40 120 0 t120 0 M170 520 h300 M600 420 l80 120 l80 -120" stroke="#e8fff0" strokeWidth={10} fill="none" opacity={0.7} strokeLinecap="round" />
      <rect x={0} y={GROUND} width={1080} height={720} fill="#d9a066" />
      <rect x={720} y={GROUND - 170} width={300} height={24} rx={8} fill="#8a5a3c" /><rect x={740} y={GROUND - 146} width={20} height={146} fill="#7a4a30" /><rect x={980} y={GROUND - 146} width={20} height={146} fill="#7a4a30" />
    </svg>
  </>
);

const Kitchen: React.FC = () => (
  <>
    <Sky a="#e6fbf4" b="#cdf3e6" />
    <svg viewBox="0 0 1080 1920" style={{position: 'absolute', inset: 0}}>
      {Array.from({length: 8}, (_, r) => Array.from({length: 7}, (_, c) => <rect key={`${r}${c}`} x={c * 160} y={600 + r * 80} width={156} height={76} fill={(r + c) % 2 ? '#bfeedd' : '#d8f7ec'} />))}
      <rect x={80} y={300} width={380} height={230} rx={16} fill="#ffffff" stroke="#9adcc6" strokeWidth={10} />
      <rect x={600} y={280} width={400} height={250} rx={16} fill="#ffcf9e" />
      <rect x={0} y={GROUND - 260} width={1080} height={40} fill="#f4f4f4" />
      <rect x={0} y={GROUND - 220} width={1080} height={220} fill="#ff9f7a" />
      {[0, 1, 2, 3].map((i) => <rect key={i} x={40 + i * 270} y={GROUND - 190} width={230} height={160} rx={12} fill="#ff8a62" />)}
      <rect x={0} y={GROUND} width={1080} height={720} fill="#e8d8c8" />
    </svg>
  </>
);

export const WORLDS: Record<string, React.FC> = {city: City, room: Room, park: Park, office: Office, night: Night, space: Space, classroom: Classroom, kitchen: Kitchen};
