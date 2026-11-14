import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {Accent, autoSize, CharacterCfg, Emoji, plain, Scene, shadow, useShort, useTheme} from '../lib';
import {Character, Expr, Pose} from '../parts/Character';
import {GROUND, WORLDS} from '../parts/Worlds';

type Cast = {id: string; x?: number; expr?: Expr; pose?: Pose; speaking?: boolean; flip?: boolean; scale?: number; enter?: 'left' | 'right' | 'pop' | 'none'};
type Prop = {emoji: string; x: number; y: number; size?: number; anim?: 'float' | 'bounce' | 'spin' | 'pop' | 'shake' | 'fall'; at?: number};
type Bubble = {who?: string; text: string; kind?: 'say' | 'think' | 'shout'};

const PropEl: React.FC<{p: Prop; k: number}> = ({p, k}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t0 = p.at ?? 6 + k * 5;
  const pop = spring({frame: f - t0, fps, config: {damping: 9, stiffness: 180, mass: 0.6}});
  let tf = `scale(${pop})`;
  const g = f - t0;
  if (p.anim === 'float' || !p.anim) tf += ` translateY(${Math.sin(f / 12 + k) * 16}px)`;
  if (p.anim === 'bounce') tf += ` translateY(${-Math.abs(Math.sin(f / 6)) * 50}px)`;
  if (p.anim === 'spin') tf += ` rotate(${f * 4}deg)`;
  if (p.anim === 'shake') tf += ` rotate(${Math.sin(f / 1.6) * 10}deg)`;
  if (p.anim === 'fall') tf += ` translateY(${interpolate(g, [0, 24], [-700, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})}px)`;
  const size = p.size ?? 140;
  return (
    <div style={{position: 'absolute', left: p.x * 1080 - size / 2, top: p.y * 1920 - size / 2, transform: tf}}>
      <Emoji e={p.emoji} size={size} style={{filter: 'drop-shadow(0 12px 16px rgba(0,0,0,0.25))'}} />
    </div>
  );
};

export const StoryScene: React.FC<{s: Scene; i: number}> = ({s}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = useTheme();
  const short = useShort();
  const World = WORLDS[String(s.bg ?? 'city')] ?? WORLDS.city;
  const cast = (s.cast as Cast[]) || [];
  const props = (s.props as Prop[]) || [];
  const bubble = s.bubble as Bubble | undefined;
  const camera = String(s.camera ?? 'zoom');
  // is a narration word being spoken right now (global frame)?
  const gf = f + s.start;
  const speakingNow = (short.words || []).some((w) => gf >= w.s && gf < w.e);
  const zoom = camera === 'zoom' ? interpolate(f, [0, s.dur], [1, 1.07]) : camera === 'punch' ? 1.12 : 1;
  const panX = camera === 'pan' ? interpolate(f, [0, s.dur], [30, -30]) : 0;
  const shake = camera === 'shake' ? Math.sin(f * 1.9) * 9 * Math.max(0, 1 - f / 20) : 0;
  const bubbleAt = Number(s.bubbleAt ?? 8);
  const bp = spring({frame: f - bubbleAt, fps, config: {damping: 11, stiffness: 200, mass: 0.6}});
  const speaker = cast.find((c) => c.id === bubble?.who) ?? cast.find((c) => c.speaking) ?? cast[0];
  const tailX = (speaker?.x ?? 0.5) * 1080;
  const title = s.title ? String(s.title) : '';
  const tp = spring({frame: f + (s.start === 0 ? 9 : 0), fps, config: {damping: 12, stiffness: 180}});

  return (
    <AbsoluteFill style={{overflow: 'hidden'}}>
      <AbsoluteFill style={{transform: `scale(${zoom}) translateX(${panX + shake}px)`, transformOrigin: '50% 60%'}}>
        <World />
        {cast.map((c, k) => {
          const cfg: CharacterCfg = short.characters?.[c.id] ?? {};
          const enter = c.enter ?? (k === 0 ? 'pop' : 'right');
          const ep = spring({frame: f - k * 4, fps, config: {damping: 14, stiffness: 150}});
          const ex = enter === 'left' ? (1 - ep) * -700 : enter === 'right' ? (1 - ep) * 700 : 0;
          const es = enter === 'pop' ? interpolate(ep, [0, 1], [0.6, 1]) : 1;
          const h = 760 * (c.scale ?? 1);
          const x = (c.x ?? (cast.length === 1 ? 0.5 : k === 0 ? 0.28 : 0.72)) * 1080;
          return (
            <div key={k} style={{position: 'absolute', left: x - (h * 300) / 620 / 2, top: GROUND + 8 - h, transform: `translateX(${ex}px) scale(${es})`, transformOrigin: '50% 100%'}}>
              <Character cfg={cfg} expr={c.expr} pose={c.pose} talking={!!c.speaking && speakingNow} height={h} flip={c.flip} seed={k} />
            </div>
          );
        })}
        {props.map((p, k) => <PropEl key={k} p={p} k={k} />)}
      </AbsoluteFill>
      {title ? (
        <div style={{position: 'absolute', top: 210, left: 60, right: 60, textAlign: 'center', transform: `scale(${interpolate(tp, [0, 1], [1.3, 1])})`, opacity: Math.min(1, tp * 2)}}>
          <span style={{display: 'inline-block', background: t.cardInk, color: '#fff', padding: '18px 34px', borderRadius: 28, fontSize: autoSize(title, 76, 22, 46), fontWeight: 900, letterSpacing: -1.5, lineHeight: 1.08, boxShadow: shadow}}>
            <Accent text={title} />
          </span>
        </div>
      ) : null}
      {bubble?.text ? (
        <div style={{position: 'absolute', top: title ? 370 : 240, left: 70, right: 70, display: 'flex', justifyContent: 'center', transform: `scale(${bp})`, transformOrigin: `${tailX - 70}px 100%`}}>
          <div style={{position: 'relative', background: bubble.kind === 'shout' ? t.accent : '#fff', color: '#16142c', borderRadius: bubble.kind === 'think' ? 80 : 40, padding: '34px 44px', maxWidth: 860, boxShadow: shadow,
            fontSize: autoSize(bubble.text, 62, 34, 40), fontWeight: 850, lineHeight: 1.15, textAlign: 'center', letterSpacing: -0.8, border: '6px solid #16142c'}}>
            {plain(bubble.text)}
            <div style={{position: 'absolute', bottom: -34, left: Math.min(Math.max(tailX - 70 - 30, 40), 760), width: 0, height: 0, borderLeft: '26px solid transparent', borderRight: '26px solid transparent', borderTop: '36px solid #16142c'}} />
          </div>
        </div>
      ) : null}
    </AbsoluteFill>
  );
};
