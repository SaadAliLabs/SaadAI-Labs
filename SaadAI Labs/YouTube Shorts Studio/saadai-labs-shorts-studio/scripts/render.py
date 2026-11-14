#!/usr/bin/env python3
"""Render the final short, normalise loudness for YouTube, and make a QA sheet.

    python3 render.py <short_dir>

Runs build.py (final mode) first. Output: <short_dir>/<slug>.mp4 (1080x1920, 30fps, H.264, -14 LUFS)
and <short_dir>/qa.jpg (frames from every scene, for the frame-by-frame check).
"""
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import ENGINE, FPS, die, duration, load_json, need_engine, run, slug_of  # noqa: E402
from storyboard import sheet  # noqa: E402

HERE = Path(__file__).parent


def loudness(path: Path):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(path), "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True)
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)
    return float(m[-1]) if m else None


def main():
    if len(sys.argv) < 2:
        die(__doc__)
    need_engine()
    short_dir = Path(sys.argv[1]).resolve()
    run([sys.executable, str(HERE / "build.py"), str(short_dir)])
    props_p = short_dir / "props.json"
    props = load_json(props_p)
    slug = slug_of(short_dir)
    raw = short_dir / ".raw.mp4"
    out = short_dir / f"{slug}.mp4"
    print("rendering (this takes a minute or two)...")
    run(["npx", "remotion", "render", "src/index.ts", "Short", str(raw), f"--props={props_p}", "--log=error"], cwd=ENGINE, quiet=True)
    # two-pass loudnorm to -14 LUFS (YouTube's playback target)
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(raw), "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True)
    m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", r.stderr, re.S)
    af = "loudnorm=I=-14:TP=-1.5:LRA=11"
    if m:
        j = json.loads(m.group(0))
        af += f":measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true"
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(raw), "-c:v", "copy", "-af", af, "-ar", "48000", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(out)], quiet=True)
    raw.unlink(missing_ok=True)

    # QA sheet: a frame from each scene, taken from the real render
    tmp = short_dir / ".qa"
    tmp.mkdir(exist_ok=True)
    frames, labels = [], []
    spec = load_json(short_dir / "short.json")
    for i, s in enumerate(props["scenes"]):
        t = (s["start"] + max(int(s["dur"] * 0.62), min(s["dur"] - 1, 24))) / FPS
        fp = tmp / f"q{i:02d}.jpg"
        run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t:.3f}", "-i", str(out), "-frames:v", "1", "-vf", "scale=270:480", str(fp)], quiet=True)
        frames.append(fp)
        labels.append((f"{i + 1}. {s['type']}  {t:.1f}s", spec["scenes"][i].get("say", "")))
    sheet(frames, labels, short_dir / "qa.jpg")
    for f in tmp.glob("*"):
        f.unlink()
    tmp.rmdir()
    lufs = loudness(out)
    print(f"done: {out}\n  length {duration(out):.1f}s, loudness {lufs} LUFS, QA sheet: {short_dir / 'qa.jpg'}")
    # claude.ai: files in /mnt/user-data/outputs are what the user can download
    web_out = Path("/mnt/user-data/outputs")
    if web_out.is_dir():
        import shutil
        shutil.copy2(out, web_out / out.name)
        print(f"  copied for download: {web_out / out.name}")


if __name__ == "__main__":
    main()
