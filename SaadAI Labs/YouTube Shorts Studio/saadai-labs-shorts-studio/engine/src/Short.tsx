import React from 'react';
import {AbsoluteFill, Audio, Sequence, interpolate, staticFile, useCurrentFrame, useVideoConfig, continueRender, delayRender} from 'remotion';
import {loadFont} from '@remotion/fonts';
import {DEFAULT_THEME, PropsCtx, Scene, ShortProps, ThemeCtx} from './lib';
import {Backdrop} from './parts/Backdrop';
import {Captions} from './parts/Captions';
import {SceneIn} from './parts/SceneIn';
import {HookScene, TextScene, StatScene, ListScene, CompareScene, IconScene, EndScene} from './scenes/Explainer';
import {StoryScene} from './scenes/Story';

const fontHandle = delayRender('font');
loadFont({family: 'Inter', url: staticFile('fonts/Inter.ttf'), weight: '100 900'})
  .then(() => continueRender(fontHandle))
  .catch(() => continueRender(fontHandle));

const SCENES: Record<string, React.FC<{s: Scene; i: number}>> = {
  hook: HookScene,
  text: TextScene,
  stat: StatScene,
  list: ListScene,
  compare: CompareScene,
  icon: IconScene,
  end: EndScene,
  story: StoryScene,
};

const Music: React.FC<{src: string; vol: number; total: number}> = ({src, vol, total}) => {
  return (
    <Audio
      src={staticFile(src)}
      loop
      volume={(f) =>
        vol *
        interpolate(f, [0, 15, total - 25, total], [0, 1, 1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})
      }
    />
  );
};

export const Short: React.FC<ShortProps> = (props) => {
  const theme = {...DEFAULT_THEME, ...(props.theme || {})};
  const {durationInFrames} = useVideoConfig();
  const frame = useCurrentFrame();
  const scenes = props.scenes || [];
  const last = scenes.length - 1;
  // story scenes paint their own world; explainer scenes sit on the animated brand backdrop
  const current = scenes.find((s) => frame >= s.start && frame < s.start + s.dur);
  return (
    <PropsCtx.Provider value={{...props, theme}}>
      <ThemeCtx.Provider value={theme}>
        <AbsoluteFill style={{fontFamily: `${theme.font}, Inter, Helvetica, Arial, sans-serif`, color: theme.ink, background: theme.bg1}}>
          <Backdrop dim={current?.type === 'story'} />
          {scenes.map((s, i) => {
            const C = SCENES[s.type] || TextScene;
            return (
              <Sequence key={i} from={s.start} durationInFrames={s.dur} name={`${i + 1}. ${s.type}`}>
                <SceneIn dur={s.dur} pre={i === 0 ? 9 : 0} fadeOut={i !== last} kind={s.type}>
                  <C s={s} i={i} />
                </SceneIn>
              </Sequence>
            );
          })}
          {props.captions !== false && <Captions />}
          {props.watermark ? (
            <div style={{position: 'absolute', top: 120, width: '100%', textAlign: 'center', fontSize: 30, fontWeight: 700, opacity: 0.55, letterSpacing: 1}}>
              {props.watermark}
            </div>
          ) : null}
          {props.voice ? <Audio src={staticFile(props.voice)} /> : null}
          {props.music ? <Music src={props.music} vol={props.musicVolume ?? 0.09} total={durationInFrames} /> : null}
          {(props.sfx || []).map((e, i) => (
            <Sequence key={`sfx${i}`} from={Math.max(0, Math.round(e.frame))} durationInFrames={90} layout="none">
              <Audio src={staticFile(e.src)} volume={e.vol} />
            </Sequence>
          ))}
        </AbsoluteFill>
      </ThemeCtx.Provider>
    </PropsCtx.Provider>
  );
};
