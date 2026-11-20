"""UC10/UC11 (+ hook from UC12) - transcribe clips, then burn in captions, @streamer credit and hook.

Step 1:  python scripts/add_captions.py transcribe RUN_DIR [--only 1,3]
         faster-whisper (local) -> clips/clipNN.words.json and a short clipNN.transcript.txt for Claude.
Step 2:  Claude writes clips/clipNN.meta.json (hook, titles, description, hashtags, optional roman_lines).
Step 3:  python scripts/add_captions.py render RUN_DIR [--only 1,3]
         -> clips/clipNN_final.mp4 (captions, credit, hook, zoom punch-in, sound effects) + clipNN_post.txt

Text is drawn with Pillow into transparent overlay frames and composited by ffmpeg, so it works with any
ffmpeg build (no libass/drawtext needed) on Mac and Windows.

meta.json fields:
  hook          short on-screen hook for the first seconds (required)
  titles        list of 3 titles
  description   description text (credit line is added automatically if missing)
  hashtags      list of hashtags
  punch_at      optional: seconds into the clip of the big moment (zoom punch-in + boom). Default ~9s.
  sfx           optional: list of {"t": seconds, "type": whoosh|swoosh_down|pop|boom|riser|ding|glitch,
                "volume": 0-1}. Replaces the default set (whoosh in, swoosh out, riser + boom at the moment).
  roman_lines   optional: one Roman Urdu / English line per transcript segment (same order and count).
                Use when the speech is Urdu/Hindi so captions are readable Roman Urdu.
"""
import argparse
import json
import shutil
import sys
from pathlib import Path

from common import ffmpeg_exe, load_config, load_json, run, save_json
from sfx import ensure_sfx

W, H = 1080, 1920
FONT_CANDIDATES = [
    "/System/Library/Fonts/Supplemental/Arial Black.ttf",
    "/System/Library/Fonts/Supplemental/Impact.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
    "C:/Windows/Fonts/ariblk.ttf",
    "C:/Windows/Fonts/impact.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]


# ---------------- transcribe ----------------

def transcribe(run_dir, only, cfg):
    from faster_whisper import WhisperModel
    data = load_json(run_dir / "moments.json")
    model_name = cfg.get("whisper_model", "small")
    print(f"Loading Whisper '{model_name}' (first time downloads the model)...", flush=True)
    model = WhisperModel(model_name, device="auto", compute_type="int8")
    for m in data["moments"]:
        if (only and m["clip"] not in only) or not m.get("vertical"):
            continue
        segs, info = model.transcribe(m["vertical"], language=cfg.get("whisper_language"),
                                      word_timestamps=True, vad_filter=True)
        out = []
        for s in segs:
            words = [{"w": w.word.strip(), "s": round(w.start, 2), "e": round(w.end, 2)} for w in (s.words or []) if w.word.strip()]
            out.append({"start": round(s.start, 2), "end": round(s.end, 2), "text": s.text.strip(), "words": words})
        base = run_dir / "clips" / f"clip{m['clip']:02d}"
        save_json(str(base) + ".words.json", {"language": info.language, "segments": out})
        lines = [f"[{i}] {s['start']:.1f}-{s['end']:.1f}s: {s['text']}" for i, s in enumerate(out)]
        Path(str(base) + ".transcript.txt").write_text(
            f"language: {info.language}\n" + ("\n".join(lines) or "(no speech found)") + "\n", encoding="utf-8")
        m["language"] = info.language
        print(f"Clip {m['clip']}: {len(out)} segments, language={info.language}")
    save_json(run_dir / "moments.json", data)


# ---------------- render ----------------

def find_font(cfg):
    for p in [cfg.get("font_path")] + FONT_CANDIDATES:
        if p and Path(p).exists():
            return p
    return None


def load_font(path, size):
    from PIL import ImageFont
    return ImageFont.truetype(path, size) if path else ImageFont.load_default(size=size)


def caption_words(words_json, meta):
    """List of {w, s, e}. Uses roman_lines (spread over each segment's time) when given."""
    segs = words_json.get("segments", [])
    roman = meta.get("roman_lines")
    if roman and len(roman) == len(segs):
        out = []
        for seg, line in zip(segs, roman):
            toks = line.split()
            if not toks:
                continue
            total = sum(len(t) + 2 for t in toks)
            t = seg["start"]
            span = max(0.3, seg["end"] - seg["start"])
            for tok in toks:
                d = span * (len(tok) + 2) / total
                out.append({"w": tok, "s": t, "e": t + d})
                t += d
        return out
    if roman:
        print("  note: roman_lines count does not match segments; using the Whisper words instead", file=sys.stderr)
    return [w for s in segs for w in s["words"]]


def chunk_words(words, n):
    chunks, cur = [], []
    for w in words:
        cur.append(w)
        ends_sentence = w["w"][-1:] in ".?!,"
        if len(cur) >= n or ends_sentence:
            chunks.append(cur)
            cur = []
    if cur:
        chunks.append(cur)
    return chunks


def wrap(draw, text, font, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


class Painter:
    def __init__(self, cfg, layout, credit, hook):
        self.font_path = find_font(cfg)
        self.cap_font = load_font(self.font_path, 78)
        self.hook_font = load_font(self.font_path, 72)
        self.credit_font = load_font(self.font_path, 38)
        self.white = cfg.get("caption_color", "#FFFFFF")
        self.hi = cfg.get("caption_highlight", "#FFD60A")
        self.layout = layout or {"mode": "center", "fg_top": 0, "fg_bottom": H}
        self.credit = credit
        self.hook = (hook or "").upper()
        if self.layout["mode"] == "blur_fit":
            self.hook_y = max(240, self.layout["fg_top"] - 330)
            self.credit_y = self.layout["fg_top"] - 70
            self.cap_y = self.layout["fg_bottom"] + 90
        else:
            self.hook_y, self.credit_y, self.cap_y = 300, 1480, 1230

    def frame(self, show_hook, chunk, active):
        from PIL import Image, ImageDraw
        img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        # credit pill (whole clip)
        text = f"Credit: {self.credit}"
        tw = d.textlength(text, font=self.credit_font)
        x0 = (W - tw) / 2 - 26
        d.rounded_rectangle([x0, self.credit_y - 8, x0 + tw + 52, self.credit_y + 52], radius=30, fill=(0, 0, 0, 165))
        d.text(((W - tw) / 2, self.credit_y), text, font=self.credit_font, fill="#FFFFFF")
        # hook (first seconds)
        if show_hook and self.hook:
            lines = wrap(d, self.hook, self.hook_font, W - 140)
            lh = 86
            box_h = lh * len(lines) + 40
            y = self.hook_y
            d.rounded_rectangle([50, y - 20, W - 50, y - 20 + box_h], radius=24, fill=(255, 214, 10, 240))
            for i, ln in enumerate(lines):
                lw = d.textlength(ln, font=self.hook_font)
                d.text(((W - lw) / 2, y + i * lh), ln, font=self.hook_font, fill="#111111")
        # captions (word by word, active word highlighted)
        if chunk:
            words = [w["w"].upper() for w in chunk]
            space = d.textlength(" ", font=self.cap_font)
            lines, cur, cur_w = [], [], 0
            for i, w in enumerate(words):
                ww = d.textlength(w, font=self.cap_font)
                if cur and cur_w + space + ww > W - 120:
                    lines.append(cur)
                    cur, cur_w = [], 0
                cur.append((i, w, ww))
                cur_w += (space if len(cur) > 1 else 0) + ww
            if cur:
                lines.append(cur)
            for li, line in enumerate(lines):
                total = sum(ww for _, _, ww in line) + space * (len(line) - 1)
                x = (W - total) / 2
                y = self.cap_y + li * 96
                for i, w, ww in line:
                    color = self.hi if i == active else self.white
                    d.text((x, y), w, font=self.cap_font, fill=color, stroke_width=8, stroke_fill="#000000")
                    x += ww + space
        return img


def render(run_dir, only, cfg):
    global SFX
    SFX = ensure_sfx()
    data = load_json(run_dir / "moments.json")
    stream = load_json(run_dir / "stream.json")
    hook_secs = cfg.get("hook_seconds", 2.0)
    per_line = cfg.get("caption_words_per_line", 3)
    for m in data["moments"]:
        if (only and m["clip"] not in only) or not m.get("vertical"):
            continue
        base = run_dir / "clips" / f"clip{m['clip']:02d}"
        meta = load_json(str(base) + ".meta.json")
        if not meta or not meta.get("hook"):
            print(f"Clip {m['clip']}: skipped - write {base.name}.meta.json with a hook first")
            continue
        words_json = load_json(str(base) + ".words.json", {"segments": []})
        words = caption_words(words_json, meta)
        chunks = chunk_words(words, per_line)

        res = run([ffmpeg_exe(), "-hide_banner", "-i", m["vertical"]], check=False)
        import re
        dm = re.search(r"Duration: (\d+):(\d+):([\d.]+)", res.stderr or "")
        dur = int(dm.group(1)) * 3600 + int(dm.group(2)) * 60 + float(dm.group(3)) if dm else m["end"] - m["start"]

        # Timeline of states: (start, end, show_hook, chunk_index, active_word_index)
        cuts = {0.0, min(hook_secs, dur), dur}
        for c in chunks:
            for w in c:
                for t in (w["s"], w["e"]):
                    if 0 <= t <= dur:
                        cuts.add(round(t, 2))
        cuts = sorted(cuts)
        painter = Painter(cfg, m.get("layout"), stream.get("credit", "@streamer"), meta["hook"])
        ov_dir = run_dir / "clips" / f"_overlay{m['clip']:02d}"
        shutil.rmtree(ov_dir, ignore_errors=True)
        ov_dir.mkdir()
        cache, entries = {}, []
        for a, b in zip(cuts, cuts[1:]):
            if b - a < 0.01:
                continue
            mid = (a + b) / 2
            state = (mid < hook_secs, None, None)
            for ci, c in enumerate(chunks):
                # show a chunk from its first word to its last word (+0.3s hold)
                if c[0]["s"] <= mid <= c[-1]["e"] + 0.3:
                    active = next((wi for wi, w in enumerate(c) if w["s"] <= mid <= w["e"]), None)
                    state = (mid < hook_secs, ci, active)
                    break
            if state not in cache:
                p = ov_dir / f"f{len(cache):04d}.png"
                painter.frame(state[0], chunks[state[1]] if state[1] is not None else None, state[2]).save(p)
                cache[state] = p
            entries.append((cache[state], b - a))
        concat = ov_dir / "overlay.ffconcat"
        with open(concat, "w", encoding="utf-8") as f:
            f.write("ffconcat version 1.0\n")
            for p, d in entries:
                f.write(f"file '{p.name}'\nduration {d:.3f}\n")
            f.write(f"file '{entries[-1][0].name}'\n")

        # --- the big moment: zoom punch-in + sound effects ---
        moment_t = meta.get("punch_at")
        if moment_t is None:
            # chat reacts a few seconds after the action; clips start lead_seconds before the spike
            moment_t = max(hook_secs + 0.5, min(dur - 1, cfg.get("lead_seconds", 12) - 3))
        moment_t = float(moment_t)
        zoom = cfg.get("punch_zoom", 0.14) if cfg.get("punch_in", True) else 0
        if zoom:
            # quick ease-in to +14% at the moment, hold briefly, ease out over ~0.8s
            z = f"{zoom}*max(0\\,1-abs(t-{moment_t:.2f})/0.8)"
            vbase = (f"[0:v]scale=w='trunc({W}*(1+{z})/2)*2':h='trunc({H}*(1+{z})/2)*2':eval=frame,"
                     f"crop={W}:{H}:(iw-{W})/2:(ih-{H})/2,setsar=1[b]")
        else:
            vbase = "[0:v]null[b]"

        sfx_list = meta.get("sfx")
        if sfx_list is None and cfg.get("sound_effects", True):
            sfx_list = [{"t": 0.0, "type": "whoosh"},
                        {"t": max(0.0, min(hook_secs, dur) - 0.15), "type": "swoosh_down"},
                        {"t": max(0.0, moment_t - 1.3), "type": "riser"},
                        {"t": moment_t, "type": "boom"}]
            if cfg.get("caption_pops", False):
                sfx_list += [{"t": c[0]["s"], "type": "pop"} for c in chunks]
        sfx_list = [s for s in (sfx_list or []) if s.get("type") in SFX and 0 <= float(s.get("t", 0)) < dur]

        has_audio = "Audio:" in (res.stderr or "")
        inputs = ["-i", m["vertical"], "-f", "concat", "-safe", "0", "-i", str(concat)]
        fc = [vbase, "[1:v]format=rgba[o]", "[b][o]overlay=0:0:eof_action=repeat:format=auto[v]"]
        amix_in = []
        if has_audio:
            fc.append("[0:a]aformat=sample_rates=48000:channel_layouts=stereo[a0]")
            amix_in.append("[a0]")
        vol = cfg.get("sfx_volume", 0.45)
        for k, s in enumerate(sfx_list):
            inputs += ["-i", str(SFX[s["type"]])]
            idx = 2 + k
            ms = int(float(s["t"]) * 1000)
            fc.append(f"[{idx}:a]adelay={ms}|{ms},volume={float(s.get('volume', vol)):.2f}[s{k}]")
            amix_in.append(f"[s{k}]")
        amap = []
        if amix_in:
            fc.append("".join(amix_in) + f"amix=inputs={len(amix_in)}:duration=first:normalize=0,alimiter=limit=0.95[a]"
                      if has_audio else
                      "".join(amix_in) + f"amix=inputs={len(amix_in)}:duration=longest:normalize=0,apad,alimiter=limit=0.95[a]")
            amap = ["-map", "[a]", "-c:a", "aac", "-b:a", "192k"]
        final = Path(str(base) + "_final.mp4")
        run([ffmpeg_exe(), "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(fc),
             "-map", "[v]", *amap, "-t", f"{dur:.2f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
             "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(final)])
        shutil.rmtree(ov_dir, ignore_errors=True)

        credit = stream.get("credit", "@streamer")
        desc = meta.get("description", "")
        if credit.lower() not in desc.lower():
            desc = (desc + f"\n\nClip from {credit}'s live stream: {stream.get('url')}").strip()
        titles = meta.get("titles", [])
        tags = " ".join(h if h.startswith("#") else "#" + h for h in meta.get("hashtags", []))
        post = "TITLES\n" + "\n".join(f"{i}. {t}" for i, t in enumerate(titles, 1)) + \
               f"\n\nDESCRIPTION\n{desc}\n\nHASHTAGS\n{tags}\n"
        Path(str(base) + "_post.txt").write_text(post, encoding="utf-8")
        m["final"] = str(final)
        m["titles"] = titles
        print(f"Clip {m['clip']}: {final.name}")
    save_json(run_dir / "moments.json", data)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=["transcribe", "render"])
    ap.add_argument("run_dir")
    ap.add_argument("--only")
    a = ap.parse_args()
    only = {int(x) for x in a.only.split(",")} if a.only else None
    cfg = load_config()
    (transcribe if a.step == "transcribe" else render)(Path(a.run_dir).resolve(), only, cfg)


if __name__ == "__main__":
    main()
