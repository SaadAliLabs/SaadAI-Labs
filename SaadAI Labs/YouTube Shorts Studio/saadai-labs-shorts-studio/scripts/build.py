#!/usr/bin/env python3
"""Turn short.json (+ timing.json from voice.py) into the engine's props.json.

    python3 build.py <short_dir> [--draft]

--draft estimates timing from word counts (no voice needed) so the storyboard can be checked
before any narration is generated. Without --draft it requires timing.json from voice.py.
Also: syncs list items / compare cards / props to the words that mention them, places sound
effects, picks the music bed, and prints quality warnings.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import ENGINE, FPS, die, find_channel, load_json, save_json, slug_of, words_of  # noqa: E402

STOP = set("the a an and or but to of in on at for with is are was were be it this that you your my our their i we they he she its as so if then just".split())
WPS = 2.75  # draft speaking speed (words/second)

SWISH = ["sfx/swish_3.wav", "sfx/swish_7.wav", "sfx/swish_8.wav", "sfx/swish_9.wav"]
POPS = ["sfx/pop_1.wav", "sfx/pop_2.wav", "sfx/pop_3.wav", "sfx/pop_4.wav"]
APPEAR = ["sfx/appear_1.wav", "sfx/appear_2.wav", "sfx/appear_3.wav", "sfx/appear_4.wav"]

norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())


def cue_word(text):
    for w in words_of(text):
        n = norm(w)
        if len(n) > 2 and n not in STOP:
            return n
    return None


def find_cue(cue, scene_words, after):
    if not cue:
        return None
    c = norm(cue)
    for w in scene_words:
        if w["s"] >= after and (norm(w["w"]) == c or (len(c) > 4 and norm(w["w"]).startswith(c[:5]))):
            return w["s"]
    return None


def draft_timing(scenes):
    t = 0
    out_s, out_w = [], []
    for i, sc in enumerate(scenes):
        ws = words_of(sc.get("say", ""))
        d = max(float(sc.get("hold", 0)), float(sc.get("min", 1.2)), len(ws) / WPS + 0.45) if ws else max(float(sc.get("hold", 0)), 1.2)
        start = round(t * FPS)
        if ws:
            span = (len(ws) / WPS) * FPS
            per = span / len(ws)
            for k, w in enumerate(ws):
                out_w.append({"w": w, "s": round(start + k * per), "e": round(start + (k + 1) * per), "scene": i})
        t += d
        out_s.append({"start": start, "dur": round(t * FPS) - start})
    return {"scenes": out_s, "words": out_w, "durationInFrames": round(t * FPS)}


def main():
    if len(sys.argv) < 2:
        die(__doc__)
    short_dir = Path(sys.argv[1]).resolve()
    draft = "--draft" in sys.argv
    spec = load_json(short_dir / "short.json")
    _, channel = find_channel(short_dir)
    scenes = spec.get("scenes", [])
    if not scenes:
        die("short.json has no scenes")

    if draft:
        timing = draft_timing(scenes)
    else:
        tp = short_dir / "timing.json"
        if not tp.exists():
            die("timing.json not found: run voice.py first (or use --draft for a storyboard)")
        timing = load_json(tp)
        if len(timing["scenes"]) != len(scenes):
            die("short.json changed since voice.py ran (scene count differs). Re-run voice.py.")

    words = timing["words"]
    out_scenes, sfx = [], []
    warnings = []
    for i, (sc, tm) in enumerate(zip(scenes, timing["scenes"])):
        s = {k: v for k, v in sc.items() if k not in ("say", "hold", "min", "notes")}
        s["start"], s["dur"] = tm["start"], tm["dur"]
        typ = s.get("type", "text")
        sw = [w for w in words if w["scene"] == i]
        rel = lambda fr: max(0, fr - s["start"] - 3)
        # transition whoosh on every cut
        if i == 0:
            sfx.append({"src": "sfx/whoosh_big_1.wav", "frame": 0, "vol": 0.45})
            sfx.append({"src": "sfx/sparkle_1.wav", "frame": 8, "vol": 0.25})
        else:
            sfx.append({"src": SWISH[i % 4], "frame": s["start"], "vol": 0.32})

        if typ == "list":
            items = s.get("items", [])
            after = s["start"]
            n = len(items)
            for k, it in enumerate(items):
                hit = find_cue(it.get("cue") or cue_word(it.get("text", "")), sw, after) if sw else None
                if hit is None:
                    hit = s["start"] + 6 + round(k * (s["dur"] * 0.75) / max(1, n))
                    if sw:
                        warnings.append(f"scene {i + 1}: list item '{it.get('text')}' isn't mentioned in the narration; timed evenly")
                it["at"] = rel(hit)
                after = hit + 1
                sfx.append({"src": POPS[k % 4], "frame": s["start"] + it["at"], "vol": 0.4})
        elif typ == "compare":
            right = s.get("right", {})
            hit = find_cue(right.get("cue") or cue_word(right.get("label", "")), sw, s["start"] + 6) if sw else None
            s["rightAt"] = rel(hit) if hit is not None else round(s["dur"] * 0.4)
            sfx += [{"src": APPEAR[0], "frame": s["start"] + 2, "vol": 0.35},
                    {"src": APPEAR[1], "frame": s["start"] + s["rightAt"], "vol": 0.35},
                    {"src": "sfx/punch_1.wav", "frame": s["start"] + s["rightAt"] + 6, "vol": 0.3}]
        elif typ == "stat":
            sfx += [{"src": "sfx/fill_1.wav", "frame": s["start"] + 4, "vol": 0.35},
                    {"src": "sfx/stamp_1.wav", "frame": s["start"] + 34, "vol": 0.38}]
        elif typ in ("icon", "hook"):
            sfx.append({"src": POPS[i % 4], "frame": s["start"] + 4, "vol": 0.35})
            if typ == "icon":
                sfx.append({"src": "sfx/sparkle_2.wav", "frame": s["start"] + 12, "vol": 0.25})
        elif typ == "text":
            sfx.append({"src": APPEAR[i % 4], "frame": s["start"] + 3, "vol": 0.3})
        elif typ == "end":
            sfx.append({"src": "sfx/sparkle_2.wav", "frame": s["start"] + 4, "vol": 0.3})
        elif typ == "story":
            for k, p in enumerate(s.get("props", [])):
                hit = find_cue(p.get("cue"), sw, s["start"]) if p.get("cue") and sw else None
                p["at"] = rel(hit) if hit is not None else p.get("at", 6 + k * 5)
                p.pop("cue", None)
                sfx.append({"src": POPS[(i + k) % 4], "frame": s["start"] + p["at"], "vol": 0.3})
            if s.get("bubble"):
                s["bubbleAt"] = s.get("bubbleAt", 8)
                sfx.append({"src": "sfx/caption_1.wav", "frame": s["start"] + s["bubbleAt"], "vol": 0.28})
            if s.get("camera") == "shake":
                sfx.append({"src": "sfx/punch_1.wav", "frame": s["start"] + 1, "vol": 0.35})
            if not s.get("cast") and not s.get("props"):
                warnings.append(f"scene {i + 1}: story scene has no cast and no props")
        out_scenes.append(s)

    theme = {**channel.get("theme", {}), **spec.get("theme", {})}
    characters = {**channel.get("characters", {}), **spec.get("characters", {})}
    mood = spec.get("music", channel.get("music", "upbeat"))
    music = None
    if mood and mood != "none":
        m = ENGINE / "public" / "music" / f"{mood}.wav"
        if m.exists():
            music = f"music/{mood}.wav"
        else:
            warnings.append(f"music '{mood}' not found in engine (run scripts/music.py)")
    slug = slug_of(short_dir)
    voice = None if draft else f"p/{slug}/voice.wav"
    if voice and not (ENGINE / "public" / voice).exists():
        die(f"voice file missing in engine: {voice}. Re-run voice.py")

    total = timing["durationInFrames"]
    props = {
        "fps": FPS,
        "durationInFrames": total,
        "theme": theme,
        "scenes": out_scenes,
        "words": words,
        "sfx": sorted(sfx, key=lambda e: e["frame"]),
        "characters": characters,
        "voice": voice,
        "music": music,
        "musicVolume": float(spec.get("musicVolume", channel.get("musicVolume", 0.08))),
        "captions": spec.get("captions", True),
        "captionStyle": spec.get("captionStyle", channel.get("captionStyle", "pop")),
        "watermark": spec.get("watermark", channel.get("watermark", "")),
    }
    save_json(short_dir / ("props.draft.json" if draft else "props.json"), props)

    # ---- quality checks (the stuff that decides swipe-away rate) ----
    secs = total / FPS
    if secs > 60:
        warnings.append(f"runtime {secs:.1f}s is over 60s; viral Shorts are usually 20-45s, trim it")
    first = scenes[0]
    if first.get("type") not in ("hook", "story") or (first.get("type") == "story" and not first.get("title")):
        warnings.append("scene 1 should be a 'hook' (or a 'story' scene with a 'title') so frame 0 shows the payoff")
    if words and words[0]["s"] > 12:
        warnings.append("narration starts later than 0.4s; start talking immediately")
    if first.get("say") and len(words_of(first["say"])) > 16:
        warnings.append("hook line is over 16 words; the first sentence should land in ~2-3 seconds")
    for i, sc in enumerate(scenes):
        d = timing["scenes"][i]["dur"] / FPS
        if d > 6.5:
            warnings.append(f"scene {i + 1} lasts {d:.1f}s; split it (aim for a visual change every 1.5-4s)")
    if scenes[-1].get("type") not in ("end", "story", "text", "hook"):
        warnings.append("last scene should set up the loop back into the hook (type 'end')")
    print(f"{'DRAFT ' if draft else ''}props written: {len(out_scenes)} scenes, {secs:.1f}s, {len(words)} words, {len(sfx)} sfx, music={music}")
    for w in warnings:
        print(f"WARNING: {w}")


if __name__ == "__main__":
    main()
