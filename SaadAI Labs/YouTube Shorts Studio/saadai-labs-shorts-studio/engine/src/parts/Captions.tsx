import React from 'react';
import {interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {useShort, useTheme, Word} from '../lib';

type Page = {words: Word[]; s: number; e: number};

const buildPages = (words: Word[], fps: number): Page[] => {
  const pages: Page[] = [];
  let cur: Word[] = [];
  const flush = () => {
    if (cur.length) pages.push({words: cur, s: cur[0].s, e: cur[cur.length - 1].e});
    cur = [];
  };
  words.forEach((w, i) => {
    const prev = words[i - 1];
    const gap = prev ? w.s - prev.e : 0;
    const chars = cur.reduce((a, x) => a + x.w.length + 1, 0);
    if (cur.length && (cur.length >= 3 || chars + w.w.length > 16 || gap > fps * 0.35 || (prev && prev.scene !== w.scene))) flush();
    cur.push(w);
    if (/[.!?,:;]$/.test(w.w)) flush();
  });
  flush();
  // hold each page until the next one starts (max 0.6s) so captions don't flicker
  pages.forEach((p, i) => {
    const next = pages[i + 1];
    p.e = next ? Math.min(next.s, p.e + fps * 0.6) : p.e + fps * 0.6;
  });
  return pages;
};

/** Word-by-word captions: 1-3 words per page, active word in accent colour with a pop. Sits in the Shorts safe zone. */
export const Captions: React.FC = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = useTheme();
  const props = useShort();
  const pages = React.useMemo(() => buildPages(props.words || [], fps), [props.words, fps]);
  const page = pages.find((p) => f >= p.s && f < p.e);
  if (!page) return null;
  const enter = spring({frame: f - page.s, fps, config: {damping: 13, stiffness: 220, mass: 0.5}});
  const box = props.captionStyle === 'box';
  return (
    <div
      style={{
        position: 'absolute',
        top: 1255,
        left: 70,
        right: 130,
        display: 'flex',
        justifyContent: 'center',
        flexWrap: 'wrap',
        gap: '0 40px',
        transform: `scale(${interpolate(enter, [0, 1], [0.82, 1])})`,
        opacity: Math.min(1, enter * 2),
      }}
    >
      {page.words.map((w, i) => {
        const active = f >= w.s && f < (page.words[i + 1]?.s ?? page.e);
        const said = f >= w.s;
        const pop = spring({frame: f - w.s, fps, config: {damping: 10, stiffness: 260, mass: 0.4}});
        const txt = w.w.replace(/\*/g, '').toUpperCase();
        return (
          <span
            key={i}
            style={{
              fontSize: 92,
              fontWeight: 900,
              letterSpacing: -1,
              lineHeight: 1.12,
              color: active ? (box ? t.cardInk : t.accent) : said ? t.ink : 'rgba(255,255,255,0.92)',
              background: active && box ? t.accent : 'transparent',
              borderRadius: 18,
              padding: box ? '0 14px' : 0,
              WebkitTextStroke: box && active ? '0px' : '14px rgba(0,0,0,0.92)',
              paintOrder: 'stroke fill',
              textShadow: '0 8px 24px rgba(0,0,0,0.45)',
              transform: active ? `scale(${interpolate(pop, [0, 1], [1.2, 1.04])}) rotate(${i % 2 ? 1.5 : -1.5}deg)` : 'scale(1)',
              display: 'inline-block',
            }}
          >
            {txt}
          </span>
        );
      })}
    </div>
  );
};
