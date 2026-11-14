"""Kokoro text-to-speech (free, local, realistic). Runs inside ~/.shorts-studio/venv.

    venv/bin/python kokoro_tts.py <text_file> <out.wav> <voice> <speed> <lang>

<voice> is one Kokoro voice ("am_michael") or a blend ("am_michael:0.6+am_fenrir:0.4").
Male voices: am_michael am_fenrir am_puck am_echo am_eric am_liam am_onyx am_adam (US),
             bm_george bm_fable bm_lewis bm_daniel (UK).
"""
import os
import sys
from pathlib import Path

import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

HOME = Path(os.environ.get("SHORTS_STUDIO_HOME", Path.home() / ".shorts-studio"))
MODEL = HOME / "models" / "kokoro" / "kokoro-v1.0.onnx"
VOICES = HOME / "models" / "kokoro" / "voices-v1.0.bin"


def main():
    text_file, out, voice, speed, lang = sys.argv[1:6]
    text = Path(text_file).read_text().strip()
    k = Kokoro(str(MODEL), str(VOICES))
    if "+" in voice or ":" in voice:
        style = None
        for part in voice.split("+"):
            name, _, w = part.partition(":")
            v = k.get_voice_style(name.strip()) * float(w or 1)
            style = v if style is None else style + v
        voice_arg = style
    else:
        voice_arg = voice
    samples, sr = k.create(text, voice=voice_arg, speed=float(speed), lang=lang)
    sf.write(out, np.asarray(samples, dtype=np.float32), sr)


if __name__ == "__main__":
    main()
