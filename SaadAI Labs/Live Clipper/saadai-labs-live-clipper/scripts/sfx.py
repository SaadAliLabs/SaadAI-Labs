"""Sound effects, synthesized with numpy (no downloads, no copyright issues).

  python scripts/sfx.py            # (re)build assets/sfx/*.wav

Effects: whoosh, pop, boom, riser, ding, swoosh_down, glitch.
The renderer calls ensure_sfx() automatically, so running this by hand is optional.
"""
import wave
from pathlib import Path

import numpy as np

from common import SKILL_DIR

SR = 48000
SFX_DIR = SKILL_DIR / "assets" / "sfx"
rng = np.random.default_rng(7)


def _t(sec):
    return np.linspace(0, sec, int(SR * sec), endpoint=False)


def _lowpass(x, alpha):
    y = np.empty_like(x)
    acc = 0.0
    for i, v in enumerate(x):
        acc += alpha * (v - acc)
        y[i] = acc
    return y


def _bandnoise(n, lo_alpha, hi_alpha):
    noise = rng.standard_normal(n)
    return _lowpass(noise, lo_alpha) - _lowpass(noise, hi_alpha)


def whoosh(sec=0.55):
    t = _t(sec)
    env = np.sin(np.pi * (t / sec) ** 0.7) ** 2
    x = _bandnoise(len(t), 0.25, 0.02) * env
    return x


def swoosh_down(sec=0.45):
    return whoosh(sec)[::-1]


def pop(sec=0.09):
    t = _t(sec)
    f = 900 * np.exp(-t * 30) + 250
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 45)
    return x


def boom(sec=1.4):
    t = _t(sec)
    f = 95 * np.exp(-t * 3) + 38
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 2.6)
    click = rng.standard_normal(len(t)) * np.exp(-t * 90) * 0.5
    x = np.tanh((body + click) * 2.2)
    return x


def riser(sec=1.3):
    t = _t(sec)
    f = 200 + 1400 * (t / sec) ** 2
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.35
    noise = _bandnoise(len(t), 0.5, 0.05) * 0.6
    env = (t / sec) ** 2
    return (tone + noise) * env


def ding(sec=0.9):
    t = _t(sec)
    x = sum(a * np.sin(2 * np.pi * f * t) for f, a in ((1320, 1), (2640, 0.4), (3960, 0.15)))
    return x * np.exp(-t * 5)


def glitch(sec=0.35):
    t = _t(sec)
    sq = np.sign(np.sin(2 * np.pi * 180 * t)) * (rng.random(len(t)) > 0.3)
    chops = (np.floor(t * 40) % 2)
    return sq * chops * 0.6 * np.exp(-t * 4)


EFFECTS = {"whoosh": whoosh, "swoosh_down": swoosh_down, "pop": pop, "boom": boom,
           "riser": riser, "ding": ding, "glitch": glitch}


def _write(path, x, peak=0.9):
    x = x / (np.max(np.abs(x)) + 1e-9) * peak
    stereo = np.repeat((x * 32767).astype("<i2")[:, None], 2, axis=1)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(stereo.tobytes())


def ensure_sfx(force=False):
    SFX_DIR.mkdir(parents=True, exist_ok=True)
    for name, fn in EFFECTS.items():
        p = SFX_DIR / f"{name}.wav"
        if force or not p.exists():
            _write(p, fn())
    return {name: SFX_DIR / f"{name}.wav" for name in EFFECTS}


if __name__ == "__main__":
    for k, v in ensure_sfx(force=True).items():
        print(k, v)
