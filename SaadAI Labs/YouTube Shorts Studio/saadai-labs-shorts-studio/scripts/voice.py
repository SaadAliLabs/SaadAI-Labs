#!/usr/bin/env python3
"""Generate the narration for a short and time every word.

    python3 voice.py <short_dir> [--force]

Reads <short_dir>/short.json (each scene's "say" text) and the channel's voice settings
(channel.json -> "voice"). Providers:
  - "kokoro": free, local, realistic neural voices (default male: am_michael+am_fenrir blend). Installed by setup.sh.
  - "elevenlabs": needs ELEVENLABS_API_KEY in the environment; voice.id optional (default: Brian, male)
  - "say": macOS built-in voices (robotic; last resort)
  - "auto" (default): elevenlabs if a key is set, otherwise kokoro, otherwise say
Each scene is voiced separately and cached by text+voice, so editing one line only re-voices that line.
Word timings come from whisper.cpp (whisper-cli) and are aligned back to the script words.
Writes <short_dir>/voice/voice.wav, <short_dir>/timing.json and copies the audio into the engine.
"""
import difflib
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import wave
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from common import ENGINE, FPS, HOME, MODELS, die, duration, find_channel, load_json, run, save_json, slug_of, which, words_of  # noqa: E402

SR = 48000
GAP = 0.16   # silence between scenes (s)
TAIL = 0.22  # extra hold after the last word of a scene (s)


KOKORO_PY = HOME / "venv" / "bin" / "python"
KOKORO_MODEL = MODELS / "kokoro" / "kokoro-v1.0.onnx"
DEFAULT_KOKORO = {"male": "am_michael:0.65+am_fenrir:0.35", "female": "af_heart"}
DEFAULT_ELEVEN = {"male": "nPczCjzI2devNBz1zQrb", "female": "EXAVITQu4vr4xnAQTJ1Y"}  # Brian / Sarah (premade)
# broadcast-style polish: rumble cut, warmth, presence, gentle compression
POLISH = "highpass=f=75,equalizer=f=160:t=q:w=1:g=2,equalizer=f=3200:t=q:w=1.2:g=3,acompressor=threshold=-20dB:ratio=3:attack=8:release=120:makeup=2"


def kokoro_ready():
    return KOKORO_PY.exists() and KOKORO_MODEL.exists()


def tts_kokoro(text, cfg, out_wav: Path):
    voice = cfg.get("name") or DEFAULT_KOKORO.get(cfg.get("gender", "male"), DEFAULT_KOKORO["male"])
    lang = "en-gb" if voice.startswith(("b", "B")) else "en-us"
    with tempfile.TemporaryDirectory() as td:
        tf = Path(td) / "t.txt"
        tf.write_text(text)
        raw = Path(td) / "k.wav"
        run([str(KOKORO_PY), str(Path(__file__).parent / "kokoro_tts.py"), str(tf), str(raw), voice, str(cfg.get("speed", 1.12)), lang], quiet=True)
        to_wav(raw, out_wav, polish=True)
    return f"kokoro:{voice}"


def best_say_voice(gender="male"):
    out = subprocess.run(["say", "-v", "?"], capture_output=True, text=True).stdout
    names = []
    for line in out.splitlines():
        m = re.match(r"^(.+?)\s+(\w\w_\w\w)\s+#", line)
        if m and m.group(2) in ("en_US", "en_GB", "en_AU", "en_IN"):
            names.append(m.group(1).strip())
    for tag in ("(Premium)", "(Enhanced)"):
        for n in names:
            if tag in n:
                return n
    prefs = ("Evan", "Nathan", "Tom", "Aaron", "Daniel", "Alex", "Reed", "Rocko") if gender == "male" else ("Samantha", "Ava", "Zoe", "Karen")
    for pref in prefs:
        for n in names:
            if n.startswith(pref):
                return n
    return names[0] if names else None


def tts_say(text, cfg, out_wav: Path):
    name = cfg.get("name") or best_say_voice()
    rate = str(cfg.get("rate", 190))
    with tempfile.TemporaryDirectory() as td:
        aiff = Path(td) / "a.aiff"
        cmd = ["say", "-r", rate, "-o", str(aiff)] + (["-v", name] if name else []) + [text]
        run(cmd, quiet=True)
        to_wav(aiff, out_wav)
    return f"say:{name}:{rate}"


def tts_eleven(text, cfg, out_wav: Path):
    key = os.environ.get("ELEVENLABS_API_KEY")
    vid = cfg.get("id") or DEFAULT_ELEVEN.get(cfg.get("gender", "male"), DEFAULT_ELEVEN["male"])
    if not key:
        die("ElevenLabs needs ELEVENLABS_API_KEY in the environment")
    body = json.dumps({
        "text": text,
        "model_id": cfg.get("model", "eleven_multilingual_v2"),
        "voice_settings": {"stability": cfg.get("stability", 0.45), "similarity_boost": cfg.get("similarity", 0.8),
                           "style": cfg.get("style", 0.25), "use_speaker_boost": True, "speed": cfg.get("speed", 1.05)},
    }).encode()
    req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format=mp3_44100_128", data=body,
                                 headers={"xi-api-key": key, "Content-Type": "application/json", "Accept": "audio/mpeg"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            mp3 = r.read()
    except urllib.error.HTTPError as e:
        die(f"ElevenLabs error {e.code}: {e.read()[:300]!r}")
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "a.mp3"
        p.write_bytes(mp3)
        to_wav(p, out_wav)
    return f"eleven:{vid}:{cfg.get('model', 'eleven_multilingual_v2')}"


def to_wav(src: Path, dst: Path, polish=False):
    # trim leading/trailing silence so scene timing is tight
    af = (POLISH + ",") * polish + "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.02,areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,areverse"
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), "-af", af, "-ar", str(SR), "-ac", "1", "-c:a", "pcm_s16le", str(dst)], quiet=True)


def read_wav(p: Path):
    with wave.open(str(p)) as w:
        return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0


def write_wav(p: Path, x):
    x = np.clip(x, -1, 1)
    with wave.open(str(p), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())


def whisper_model():
    cands = [MODELS / "ggml-base.en.bin", MODELS / "ggml-small.en.bin",
             Path.home() / ".saadai-reel-editor/models/ggml-large-v3-turbo-q5_0.bin"] + sorted(MODELS.glob("ggml-*.bin"))
    for c in cands:
        if c.exists() and c.stat().st_size > 1_000_000:
            return c
    return None


def whisper_words(wav: Path, lang: str):
    """Returns [(token, start_s, end_s)] or None if whisper is unavailable."""
    exe = which("whisper-cli")
    model = whisper_model()
    if not exe or not model:
        return None
    with tempfile.TemporaryDirectory() as td:
        base = Path(td) / "w"
        r = subprocess.run([exe, "-m", str(model), "-f", str(wav), "-l", lang, "-ml", "1", "-sow", "-oj", "-of", str(base), "-np"],
                           capture_output=True, text=True)
        js = base.with_suffix(".json")
        if r.returncode != 0 or not js.exists():
            return None
        data = json.loads(js.read_text())
    out = []
    for seg in data.get("transcription", []):
        txt = seg.get("text", "").strip()
        if not txt or txt.startswith("["):
            continue
        out.append((txt, seg["offsets"]["from"] / 1000, seg["offsets"]["to"] / 1000))
    return out


norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())


def align(script_words, tokens, clip_dur):
    """Give each script word a (start, end) in seconds, using whisper tokens where words match."""
    n = len(script_words)
    if n == 0:
        return []
    times = [None] * n
    if tokens:
        sm = difflib.SequenceMatcher(a=[norm(w) for w in script_words], b=[norm(t[0]) for t in tokens], autojunk=False)
        for a, b, size in sm.get_matching_blocks():
            for k in range(size):
                times[a + k] = (tokens[b + k][1], tokens[b + k][2])
        span = (tokens[0][1], tokens[-1][2]) if tokens else (0, clip_dur)
    else:
        span = (0.0, clip_dur)
    # fill unmatched runs proportionally to word length between known neighbours
    i = 0
    while i < n:
        if times[i] is not None:
            i += 1
            continue
        j = i
        while j < n and times[j] is None:
            j += 1
        left = times[i - 1][1] if i > 0 else span[0]
        right = times[j][0] if j < n else max(span[1], left + 0.3 * (j - i))
        weights = [len(script_words[k]) + 2 for k in range(i, j)]
        tot = sum(weights)
        t = left
        for k, wgt in zip(range(i, j), weights):
            d = (right - left) * wgt / tot
            times[k] = (t, t + d)
            t += d
        i = j
    # monotonic + minimum length
    fixed = []
    prev = 0.0
    for s, e in times:
        s = max(s, prev)
        e = max(e, s + 0.08)
        fixed.append((s, e))
        prev = s
    return fixed


def main():
    if len(sys.argv) < 2:
        die(__doc__)
    short_dir = Path(sys.argv[1]).resolve()
    force = "--force" in sys.argv
    spec = load_json(short_dir / "short.json")
    _, channel = find_channel(short_dir)
    vcfg = {**channel.get("voice", {}), **spec.get("voice", {})}
    provider = vcfg.get("provider", "auto")
    if provider == "auto":
        provider = "elevenlabs" if os.environ.get("ELEVENLABS_API_KEY") else ("kokoro" if kokoro_ready() else "say")
    if provider == "kokoro" and not kokoro_ready():
        die("Kokoro voice not installed. Run scripts/setup.sh")
    if provider == "say" and not which("say"):
        die("macOS 'say' not found. Set voice.provider to 'elevenlabs' and export ELEVENLABS_API_KEY.")
    if provider == "say" and not vcfg.get("name"):
        vcfg["name"] = best_say_voice(vcfg.get("gender", "male"))
    if provider == "say":
        print(f"WARNING: using the robotic macOS voice {vcfg['name']}; run setup.sh to install the realistic Kokoro voices")
    if provider == "kokoro":
        print(f"voice: Kokoro {vcfg.get('name') or DEFAULT_KOKORO.get(vcfg.get('gender', 'male'))} (free, local)")
    lang = vcfg.get("lang", channel.get("language", "en"))[:2]
    vdir = short_dir / "voice"
    vdir.mkdir(exist_ok=True)
    cache_p = vdir / "cache.json"
    cache = json.loads(cache_p.read_text()) if cache_p.exists() else {}

    scenes = spec.get("scenes", [])
    timing = {"fps": FPS, "provider": provider, "scenes": [], "words": []}
    pieces = []
    t = 0.0
    for i, sc in enumerate(scenes):
        text = (sc.get("say") or "").strip()
        hold = float(sc.get("hold", 0))
        if not text:
            d = max(hold, float(sc.get("min", 1.2)))
            timing["scenes"].append({"start": round(t * FPS), "dur": round(d * FPS)})
            pieces.append((t, None))
            t += d
            continue
        spoken = re.sub(r"\*", "", text)
        key = hashlib.sha1(f"{provider}|{json.dumps(vcfg, sort_keys=True)}|{spoken}".encode()).hexdigest()[:16]
        clip = vdir / f"scene_{i + 1:02d}.wav"
        if force or cache.get(str(i)) != key or not clip.exists():
            print(f"voicing scene {i + 1}: {spoken[:60]}")
            {"elevenlabs": tts_eleven, "kokoro": tts_kokoro}.get(provider, tts_say)(spoken, vcfg, clip)
            cache[str(i)] = key
        cd = duration(clip)
        toks = whisper_words(clip, lang)
        sw = words_of(text)
        tw = align([re.sub(r"\*", "", w) for w in sw], toks, cd)
        for w, (s, e) in zip(sw, tw):
            timing["words"].append({"w": w, "s": round((t + s) * FPS), "e": round((t + e) * FPS), "scene": i})
        d = max(cd + TAIL + (GAP if i < len(scenes) - 1 else 0.35), hold, float(sc.get("min", 0)))
        timing["scenes"].append({"start": round(t * FPS), "dur": round(d * FPS), "voice": round(cd, 3)})
        pieces.append((t, clip))
        t += d
    # make scene frames contiguous
    for a, b in zip(timing["scenes"], timing["scenes"][1:]):
        a["dur"] = b["start"] - a["start"]
    total = timing["scenes"][-1]["start"] + timing["scenes"][-1]["dur"] if timing["scenes"] else 0
    timing["durationInFrames"] = total

    mix = np.zeros(int(total / FPS * SR) + SR, dtype=np.float32)
    for start, clip in pieces:
        if clip is None:
            continue
        x = read_wav(clip)
        o = int(start * SR)
        mix[o:o + len(x)] += x[: max(0, len(mix) - o)]
    mix = mix[: int(total / FPS * SR)]
    write_wav(vdir / "voice.wav", mix)
    save_json(cache_p, cache)
    save_json(short_dir / "timing.json", timing)

    dest = ENGINE / "public" / "p" / slug_of(short_dir)
    dest.mkdir(parents=True, exist_ok=True)
    shutil.copy2(vdir / "voice.wav", dest / "voice.wav")
    aligned = "whisper" if whisper_model() and which("whisper-cli") else "estimated (whisper not installed)"
    print(f"voice: {provider}, {len(timing['words'])} words, {total / FPS:.1f}s, word timing: {aligned}")


if __name__ == "__main__":
    main()
