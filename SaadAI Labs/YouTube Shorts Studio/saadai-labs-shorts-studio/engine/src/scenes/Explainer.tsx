import React from 'react';
import {AbsoluteFill, Easing, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {Accent, autoSize, Emoji, plain, Scene, shadow, usePop, useTheme} from '../lib';

// Content lives between y≈220 and y≈1220; captions own y≈1255-1500; YouTube's UI covers the rest.
const Stage: React.FC<{children: React.ReactNode; top?: number}> = ({children, top = 230}) => (
  <AbsoluteFill style={{top, height: 1000, bottom: 'auto', alignItems: 'center', justifyContent: 'center', padding: '0 80px'}}>
    {children}
  </AbsoluteFill>
);

const Float: React.FC<{children: React.ReactNode; amp?: number; speed?: number; phase?: number}> = ({children, amp = 14, speed = 14, phase = 0}) => {
  const f = useCurrentFrame();
  return <div style={{transform: `translateY(${Math.sin(f / speed + phase) * amp}px)`}}>{children}</div>;
};

const Shine: React.FC<{delay?: number}> = ({delay = 12}) => {
  const f = useCurrentFrame();
  const x = interpolate(f - delay, [0, 18], [-120, 220], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <div style={{position: 'absolute', inset: 0, overflow: 'hidden', borderRadius: 'inherit', pointerEvents: 'none'}}>
      <div style={{position: 'absolute', top: '-50%', bottom: '-50%', left: `${x}%`, width: '22%', background: 'linear-gradient(90deg, transparent, rgba(255,255,255,0.55), transparent)', transform: 'rotate(18deg)'}} />
    </div>
  );
};

const Rays: React.FC<{color: string; size?: number}> = ({color, size = 900}) => {
  const f = useCurrentFrame();
  return (
    <div style={{position: 'absolute', width: size, height: size, borderRadius: '50%', opacity: 0.18, transform: `rotate(${f * 0.6}deg)`,
      background: `repeating-conic-gradient(${color} 0deg 10deg, transparent 10deg 30deg)`, WebkitMaskImage: 'radial-gradient(circle, #000 20%, transparent 70%)'}} />
  );
};

export const HookScene: React.FC<{s: Scene; i: number}> = ({s}) => {
  const t = useTheme();
  const title = String(s.title ?? '');
  const p = usePop(-9);
  const pe = usePop(-4, {damping: 8, stiffness: 140, mass: 0.6});
  const ps = usePop(10);
  const f = useCurrentFrame();
  const wob = Math.sin(f / 5) * 2.5 * Math.max(0, 1 - f / 45);
  return (
    <Stage>
      <Rays color={t.accent} />
      {s.emoji ? (
        <Float amp={16}>
          <div style={{transform: `scale(${pe}) rotate(${wob * 3}deg)`, marginBottom: 30}}>
            <Emoji e={String(s.emoji)} size={260} style={{filter: 'drop-shadow(0 20px 30px rgba(0,0,0,0.35))'}} />
          </div>
        </Float>
      ) : null}
      <div style={{fontSize: autoSize(title, 118, 22, 64), fontWeight: 900, lineHeight: 1.02, letterSpacing: -3, textAlign: 'center',
        transform: `scale(${interpolate(p, [0, 1], [1.3, 1])}) rotate(${wob}deg)`, textShadow: '0 10px 30px rgba(0,0,0,0.4)'}}>
        <Accent text={title} />
      </div>
      {s.sub ? (
        <div style={{marginTop: 34, fontSize: autoSize(s.sub, 52, 30, 36), fontWeight: 700, color: t.muted, textAlign: 'center', opacity: ps, transform: `translateY(${(1 - ps) * 30}px)`}}>
          <Accent text={String(s.sub)} color={t.accent2} />
        </div>
      ) : null}
    </Stage>
  );
};

export const TextScene: React.FC<{s: Scene; i: number}> = ({s, i}) => {
  const t = useTheme();
  const text = String(s.text ?? s.title ?? '');
  const p = usePop(0);
  const pe = usePop(6, {damping: 9, stiffness: 160, mass: 0.6});
  const f = useCurrentFrame();
  const under = interpolate(f, [10, 24], [0, 100], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic)});
  const tilt = i % 2 ? 1.6 : -1.6;
  return (
    <Stage>
      {s.emoji ? (
        <Float phase={i}>
          <div style={{transform: `scale(${pe}) rotate(${tilt * 4}deg)`, marginBottom: 40}}>
            <Emoji e={String(s.emoji)} size={220} style={{filter: 'drop-shadow(0 18px 26px rgba(0,0,0,0.3))'}} />
          </div>
        </Float>
      ) : null}
      <div style={{position: 'relative', background: t.card, color: t.cardInk, borderRadius: 44, padding: '56px 60px', boxShadow: shadow, maxWidth: 900,
        transform: `rotate(${tilt}deg) scale(${interpolate(p, [0, 1], [0.7, 1])})`}}>
        <div style={{fontSize: autoSize(text, 84, 40, 50), fontWeight: 850, lineHeight: 1.12, letterSpacing: -1.5, textAlign: 'center'}}>
          <Accent text={text} color={t.accent2} />
        </div>
        <div style={{height: 12, width: `${under}%`, background: t.accent, borderRadius: 6, marginTop: 26, marginLeft: 'auto', marginRight: 'auto'}} />
        <Shine delay={14} />
      </div>
    </Stage>
  );
};

export const StatScene: React.FC<{s: Scene; i: number}> = ({s}) => {
  const t = useTheme();
  const f = useCurrentFrame();
  const value = Number(s.value ?? 0);
  const dec = Number(s.decimals ?? (Number.isInteger(value) ? 0 : 1));
  const prog = interpolate(f, [4, 34], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic)});
  const shown = (value * prog).toLocaleString('en-US', {minimumFractionDigits: dec, maximumFractionDigits: dec});
  const done = usePop(34, {damping: 8, stiffness: 200, mass: 0.5});
  const lp = usePop(8);
  const numStr = `${s.prefix ?? ''}${shown}${s.suffix ?? ''}`;
  const pct = String(s.suffix ?? '').trim() === '%' ? Math.min(100, value) : null;
  const R = 300;
  const C = 2 * Math.PI * R;
  return (
    <Stage>
      <div style={{position: 'relative', width: 760, height: 760, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
        <svg width={760} height={760} style={{position: 'absolute', transform: 'rotate(-90deg)'}}>
          <circle cx={380} cy={380} r={R} stroke="rgba(255,255,255,0.12)" strokeWidth={44} fill="none" />
          <circle cx={380} cy={380} r={R} stroke={t.accent} strokeWidth={44} fill="none" strokeLinecap="round"
            strokeDasharray={C} strokeDashoffset={C * (1 - (pct !== null ? (pct / 100) * prog : prog))} />
        </svg>
        <div style={{textAlign: 'center', transform: `scale(${1 + 0.12 * Math.sin(done * Math.PI)})`}}>
          {s.emoji ? <Emoji e={String(s.emoji)} size={110} /> : null}
          <div style={{fontSize: autoSize(numStr, 150, 4, 80), fontWeight: 900, letterSpacing: -6, color: t.accent, lineHeight: 1, fontVariantNumeric: 'tabular-nums'}}>{numStr}</div>
        </div>
      </div>
      <div style={{marginTop: 40, fontSize: autoSize(s.label, 64, 26, 40), fontWeight: 800, textAlign: 'center', opacity: lp, transform: `translateY(${(1 - lp) * 40}px)`}}>
        <Accent text={String(s.label ?? '')} color={t.accent2} />
      </div>
    </Stage>
  );
};

type Item = {emoji?: string; text: string; at?: number};

export const ListScene: React.FC<{s: Scene; i: number}> = ({s}) => {
  const t = useTheme();
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const items = (s.items as Item[]) || [];
  const tp = usePop(0);
  const n = items.length;
  const itemSize = n > 4 ? 50 : 60;
  return (
    <Stage>
      {s.title ? (
        <div style={{fontSize: autoSize(s.title, 80, 22, 52), fontWeight: 900, textAlign: 'center', marginBottom: 46, letterSpacing: -2, transform: `scale(${tp})`}}>
          <Accent text={String(s.title)} />
        </div>
      ) : null}
      <div style={{display: 'flex', flexDirection: 'column', gap: n > 4 ? 22 : 30, width: 900}}>
        {items.map((it, k) => {
          const at = it.at ?? Math.round(8 + k * 14);
          const sp = spring({frame: f - at, fps, config: {damping: 12, stiffness: 190, mass: 0.6}});
          const latest = items.findIndex((x, j) => j > k && f >= (x.at ?? 8 + j * 14)) === -1 && f >= at;
          return (
            <div key={k} style={{display: 'flex', alignItems: 'center', gap: 30, background: latest ? t.accent : t.card, color: t.cardInk, borderRadius: 34,
              padding: n > 4 ? '22px 34px' : '30px 40px', boxShadow: shadow, opacity: Math.min(1, sp * 1.5),
              transform: `translateX(${(1 - sp) * (k % 2 ? 160 : -160)}px) scale(${interpolate(sp, [0, 1], [0.8, latest ? 1.03 : 1])})`}}>
              <div style={{width: n > 4 ? 84 : 100, height: n > 4 ? 84 : 100, borderRadius: 26, background: latest ? t.cardInk : t.bg2, display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0}}>
                {it.emoji ? <Emoji e={it.emoji} size={n > 4 ? 52 : 62} /> : <span style={{color: t.accent, fontWeight: 900, fontSize: 52}}>{k + 1}</span>}
              </div>
              <div style={{fontSize: autoSize(it.text, itemSize, 22, 36), fontWeight: 800, lineHeight: 1.1, letterSpacing: -1}}>
                <Accent text={it.text} color={latest ? t.cardInk : t.accent2} />
              </div>
            </div>
          );
        })}
      </div>
    </Stage>
  );
};

type Side = {emoji?: string; label: string; sub?: string};

export const CompareScene: React.FC<{s: Scene; i: number}> = ({s}) => {
  const t = useTheme();
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const L = (s.left as Side) || {label: ''};
  const Rt = (s.right as Side) || {label: ''};
  const rightAt = Number(s.rightAt ?? 18);
  const lp = spring({frame: f, fps, config: {damping: 13, stiffness: 180}});
  const rp = spring({frame: f - rightAt, fps, config: {damping: 13, stiffness: 180}});
  const vs = spring({frame: f - rightAt - 6, fps, config: {damping: 7, stiffness: 220, mass: 0.5}});
  const card = (side: Side, p: number, dir: number, good: boolean) => (
    <div style={{width: 430, minHeight: 560, borderRadius: 44, background: good ? t.accent : t.card, color: t.cardInk, boxShadow: shadow, padding: '50px 30px',
      display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 24, opacity: Math.min(1, p * 1.5),
      transform: `translateX(${(1 - p) * dir * 500}px) rotate(${dir * -3 * p}deg)`}}>
      {side.emoji ? <Emoji e={side.emoji} size={170} /> : null}
      <div style={{fontSize: autoSize(side.label, 66, 10, 38), fontWeight: 900, textAlign: 'center', letterSpacing: -1.5, lineHeight: 1.05}}>{plain(side.label)}</div>
      {side.sub ? <div style={{fontSize: autoSize(side.sub, 40, 24, 28), fontWeight: 650, textAlign: 'center', opacity: 0.75, lineHeight: 1.2}}>{plain(side.sub)}</div> : null}
    </div>
  );
  return (
    <Stage>
      {s.title ? <div style={{fontSize: autoSize(s.title, 76, 22, 48), fontWeight: 900, textAlign: 'center', marginBottom: 50, letterSpacing: -2}}><Accent text={String(s.title)} /></div> : null}
      <div style={{display: 'flex', gap: 40, alignItems: 'stretch', position: 'relative'}}>
        {card(L, lp, -1, s.winner === 'left')}
        {card(Rt, rp, 1, s.winner === 'right')}
        <div style={{position: 'absolute', left: '50%', top: '50%', width: 150, height: 150, marginLeft: -75, marginTop: -75, borderRadius: '50%', background: t.accent2,
          color: '#fff', fontWeight: 900, fontSize: 60, display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: shadow, border: '8px solid #fff', transform: `scale(${vs}) rotate(${(1 - vs) * 90}deg)`}}>
          {String(s.vs ?? 'VS')}
        </div>
      </div>
    </Stage>
  );
};

export const IconScene: React.FC<{s: Scene; i: number}> = ({s}) => {
  const t = useTheme();
  const f = useCurrentFrame();
  const p = usePop(0, {damping: 7, stiffness: 150, mass: 0.7});
  const lp = usePop(10);
  const orbit = ((s.orbit as string[]) || []).slice(0, 6);
  return (
    <Stage>
      <Rays color={t.accent2} size={950} />
      <div style={{position: 'relative', width: 700, height: 700, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
        <div style={{transform: `scale(${p}) rotate(${Math.sin(f / 9) * 6}deg)`}}>
          <Emoji e={String(s.emoji ?? '✨')} size={400} style={{filter: 'drop-shadow(0 30px 40px rgba(0,0,0,0.35))'}} />
        </div>
        {orbit.map((e, k) => {
          const a = (k / orbit.length) * Math.PI * 2 + f / 40;
          const op = spring({frame: f - 8 - k * 4, fps: 30, config: {damping: 10}});
          return (
            <div key={k} style={{position: 'absolute', left: 350 + Math.cos(a) * 320 - 55, top: 350 + Math.sin(a) * 320 - 55, transform: `scale(${op})`}}>
              <Emoji e={e} size={110} />
            </div>
          );
        })}
      </div>
      {s.label ? (
        <div style={{marginTop: 30, fontSize: autoSize(s.label, 80, 20, 48), fontWeight: 900, textAlign: 'center', letterSpacing: -2, opacity: lp, transform: `translateY(${(1 - lp) * 40}px)`}}>
          <Accent text={String(s.label)} />
        </div>
      ) : null}
    </Stage>
  );
};

export const EndScene: React.FC<{s: Scene; i: number}> = ({s}) => {
  const t = useTheme();
  const f = useCurrentFrame();
  const p = usePop(0);
  const text = String(s.text ?? '');
  return (
    <Stage>
      {s.emoji ? (
        <div style={{transform: `scale(${p}) rotate(${Math.sin(f / 7) * 8}deg)`, marginBottom: 30}}>
          <Emoji e={String(s.emoji)} size={200} />
        </div>
      ) : null}
      <div style={{fontSize: autoSize(text, 100, 24, 58), fontWeight: 900, textAlign: 'center', letterSpacing: -2.5, lineHeight: 1.05, transform: `scale(${interpolate(p, [0, 1], [0.6, 1])})`}}>
        <Accent text={text} color={t.accent} />
      </div>
    </Stage>
  );
};
