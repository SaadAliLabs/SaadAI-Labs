import React from 'react';
import {spring, useCurrentFrame, useVideoConfig} from 'remotion';

export type Theme = {
  bg1: string;
  bg2: string;
  ink: string;
  muted: string;
  accent: string;
  accent2: string;
  card: string;
  cardInk: string;
  font: string;
};

export const DEFAULT_THEME: Theme = {
  bg1: '#0f1226',
  bg2: '#2b1d63',
  ink: '#ffffff',
  muted: '#c9c6ff',
  accent: '#ffd23f',
  accent2: '#ff5d8f',
  card: '#ffffff',
  cardInk: '#16142c',
  font: 'Inter',
};

export type Word = {w: string; s: number; e: number; scene: number};
export type SfxEvent = {src: string; frame: number; vol: number};

export type CharacterCfg = {
  skin?: string;
  hair?: 'short' | 'long' | 'bun' | 'curly' | 'bald' | 'cap' | 'spiky';
  hairColor?: string;
  shirt?: string;
  pants?: string;
  shoes?: string;
  glasses?: boolean;
  beard?: boolean;
};

// A scene as it arrives in props.json (built by scripts/build.py). start/dur are frames.
export type Scene = {
  type: string;
  start: number;
  dur: number;
  [k: string]: unknown;
};

export type ShortProps = {
  fps: number;
  durationInFrames: number;
  theme: Theme;
  scenes: Scene[];
  words: Word[];
  sfx: SfxEvent[];
  characters: Record<string, CharacterCfg>;
  voice: string | null;
  music: string | null;
  musicVolume: number;
  captions: boolean;
  captionStyle?: 'pop' | 'box';
  watermark?: string;
};

export const ThemeCtx = React.createContext<Theme>(DEFAULT_THEME);
export const useTheme = () => React.useContext(ThemeCtx);

export const PropsCtx = React.createContext<ShortProps | null>(null);
export const useShort = () => React.useContext(PropsCtx) as ShortProps;

export const EMOJI_FONT = '"Apple Color Emoji","Segoe UI Emoji","Noto Color Emoji",sans-serif';

/** Renders text where *words* in asterisks get the accent colour. */
export const Accent: React.FC<{text: string; color?: string}> = ({text, color}) => {
  const t = useTheme();
  const parts = String(text ?? '').split(/(\*[^*]+\*)/g);
  return (
    <>
      {parts.map((p, i) =>
        p.length > 2 && p.startsWith('*') && p.endsWith('*') ? (
          <span key={i} style={{color: color ?? t.accent}}>
            {p.slice(1, -1)}
          </span>
        ) : (
          <span key={i}>{p}</span>
        ),
      )}
    </>
  );
};

export const plain = (s: unknown) => String(s ?? '').replace(/\*/g, '');

/** Shrinks a font size for longer strings so text never overflows its box. */
export const autoSize = (text: unknown, base: number, refChars: number, min = 36) => {
  const n = Math.max(1, plain(text).length);
  if (n <= refChars) return base;
  return Math.max(min, Math.round(base * Math.sqrt(refChars / n)));
};

export const usePop = (delay = 0, cfg = {damping: 12, stiffness: 170, mass: 0.6}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  return spring({frame: f - delay, fps, config: cfg});
};

export const Emoji: React.FC<{e: string; size: number; style?: React.CSSProperties}> = ({e, size, style}) => (
  <span style={{fontFamily: EMOJI_FONT, fontSize: size, lineHeight: 1, display: 'inline-block', ...style}}>{e}</span>
);

/** Deterministic pseudo-random in [0,1) from a seed. */
export const rand = (seed: number) => {
  const x = Math.sin(seed * 12.9898 + 78.233) * 43758.5453;
  return x - Math.floor(x);
};

export const shadow = '0 18px 40px rgba(0,0,0,0.28)';
