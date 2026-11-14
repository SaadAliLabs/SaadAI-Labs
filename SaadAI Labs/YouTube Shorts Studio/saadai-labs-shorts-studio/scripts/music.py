#!/usr/bin/env python3
"""Synthesise royalty-free background loops (no samples, no licences) into the engine.

    python3 music.py            # writes upbeat.wav, calm.wav, mystery.wav, hype.wav

They are deliberately simple and quiet: the voice is the star. Users can drop any licensed
track into ~/.shorts-studio/engine/public/music/<name>.wav and set "music": "<name>".
"""
import sys
import wave
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from common import ENGINE  # noqa: E402

SR = 44100
N = lambda m: 440.0 * 2 ** ((m - 69) / 12)

MOODS = {
    #           bpm  chords (midi roots + quality)                         lead?
    "upbeat":  (112, [(60, "maj"), (67, "maj"), (69, "min"), (65, "maj")], True),
    "calm":    (78,  [(62, "maj7"), (67, "maj7"), (64, "min7"), (69, "sus")], False),
    "mystery": (90,  [(57, "min"), (53, "maj"), (60, "maj"), (55, "maj")], True),
    "hype":    (128, [(57, "min"), (53, "maj"), (60, "maj"), (55, "maj")], True),
}
Q = {"maj": [0, 4, 7], "min": [0, 3, 7], "maj7": [0, 4, 7, 11], "min7": [0, 3, 7, 10], "sus": [0, 5, 7]}


def env(n, a=0.005, d=0.25):
    t = np.arange(n) / SR
    return np.minimum(1, t / a) * np.exp(-t / d)


def tone(f, n, kind="pluck"):
    t = np.arange(n) / SR
    if kind == "pad":
        x = sum(np.sin(2 * np.pi * f * (1 + det) * t) for det in (-0.004, 0, 0.004)) / 3
        return x * np.minimum(1, t / 0.4) * np.minimum(1, (n / SR - t) / 0.4)
    x = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(4 * np.pi * f * t) + 0.12 * np.sin(6 * np.pi * f * t)
    return x * env(n, d=0.22)


def make(name, bpm, chords, lead):
    beat = 60 / bpm
    bar = int(beat * 4 * SR)
    bars = 16
    out = np.zeros(bar * bars)
    rng = np.random.default_rng(7)
    for b in range(bars):
        root, q = chords[b % len(chords)]
        o = b * bar
        notes = [root + i for i in Q[q]]
        # pad
        for m in notes:
            out[o:o + bar] += 0.08 * tone(N(m), bar, "pad")
        # bass on beats
        for k in range(4):
            s = o + int(k * beat * SR)
            n = int(beat * SR * 0.9)
            out[s:s + n] += 0.22 * tone(N(root - 24), n) * (1.0 if k % 2 == 0 else 0.7)
        # arpeggio 8ths
        for k in range(8):
            s = o + int(k * beat / 2 * SR)
            n = int(beat / 2 * SR)
            m = notes[k % len(notes)] + (12 if k >= 4 else 0)
            out[s:s + n] += 0.07 * tone(N(m), n)
        # drums
        if name != "calm":
            for k in range(4):
                s = o + int(k * beat * SR)
                n = int(0.18 * SR)
                t = np.arange(n) / SR
                kick = np.sin(2 * np.pi * (50 + 90 * np.exp(-t * 30)) * t) * np.exp(-t * 18)
                out[s:s + n] += 0.35 * kick
                hs = s + int(beat / 2 * SR)
                hn = int(0.04 * SR)
                out[hs:hs + hn] += 0.05 * rng.standard_normal(hn) * np.exp(-np.arange(hn) / SR * 90)
                if k in (1, 3):
                    sn = int(0.12 * SR)
                    out[s:s + sn] += 0.09 * rng.standard_normal(sn) * np.exp(-np.arange(sn) / SR * 30)
        if lead and b % 4 == 3:
            for k, step in enumerate([0, 2, 4, 2]):
                s = o + int(k * beat * SR)
                n = int(beat * SR)
                out[s:s + n] += 0.05 * tone(N(notes[0] + 12 + step), n)
    out /= max(1e-6, np.abs(out).max()) / 0.7
    path = ENGINE / "public" / "music" / f"{name}.wav"
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((out * 32767).astype(np.int16).tobytes())
    print(f"music: {path} ({len(out) / SR:.1f}s loop)")


if __name__ == "__main__":
    for name, (bpm, chords, lead) in MOODS.items():
        make(name, bpm, chords, lead)
