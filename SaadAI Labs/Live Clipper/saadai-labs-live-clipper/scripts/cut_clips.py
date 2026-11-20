"""UC9 - download only the picked moments and turn them into 1080x1920 vertical clips.

Usage:
  python scripts/cut_clips.py RUN_DIR [--crop blur_fit|center] [--only 1,3]

For each moment in moments.json: yt-dlp --download-sections grabs just that part of the stream, then
ffmpeg makes it vertical:
  blur_fit - whole frame in the middle, blurred zoomed copy behind it (nothing cut off; default)
  center   - fills the screen by cropping the centre of the frame
Writes RUN_DIR/clips/clipNN_vertical.mp4 and records the layout in moments.json.
"""
import argparse
import re
from concurrent.futures import ThreadPoolExecutor
import urllib.parse
from datetime import datetime
from pathlib import Path

from common import ffmpeg_exe, http_get, load_config, load_json, run, save_json, video_info, ytdlp_base

W, H = 1080, 1920


def _live_segments(url, wall_start, wall_end):
    """Segments of a live HLS playlist that cover [wall_start, wall_end] (unix seconds): [(wall, dur, url)]."""
    lines = http_get(url).decode("utf-8").splitlines()
    segs, pdt, dur = [], None, None
    for ln in lines:
        if ln.startswith("#EXT-X-PROGRAM-DATE-TIME:"):
            pdt = datetime.fromisoformat(ln.split(":", 1)[1].replace("Z", "+00:00")).timestamp()
        elif ln.startswith("#EXTINF:"):
            dur = float(ln[8:].split(",")[0])
        elif ln and not ln.startswith("#"):
            if pdt is not None and dur:
                segs.append((pdt, dur, urllib.parse.urljoin(url, ln)))
                pdt += dur  # next segment follows unless a new PROGRAM-DATE-TIME line says otherwise
            dur = None
    if not segs:
        raise RuntimeError("live playlist has no timed segments")
    if wall_start < segs[0][0]:
        mins = (segs[-1][0] - segs[0][0]) / 60
        raise RuntimeError(f"this moment is older than the live rewind window (~{mins:.0f} min). "
                           "Wait for the live to end and clip it from the replay, or watch in shorter rounds.")
    if wall_end > segs[-1][0] + segs[-1][1]:
        raise RuntimeError("this moment has not finished streaming yet - try again in a minute")
    return [s for s in segs if s[0] + s[1] > wall_start and s[0] < wall_end]


def _fetch_joined(segs, path):
    """Download segments in parallel and join them into one file (works for MPEG-TS video and ADTS AAC audio)."""
    with ThreadPoolExecutor(8) as pool:
        parts = list(pool.map(lambda s: http_get(s[2], timeout=60), segs))
    with open(path, "wb") as f:
        for b in parts:
            f.write(b)
    return segs[0][0]


def download_live_section(stream, m, out, max_h):
    """Cut a moment from a stream that is still live, using YouTube's ~15 min rewind (HLS) window."""
    info = video_info(stream["url"])
    fmts = [f for f in info.get("formats", []) if "m3u8" in (f.get("protocol") or "")]
    vids = sorted([f for f in fmts if f.get("vcodec") not in (None, "none") and (f.get("height") or 0) <= max_h],
                  key=lambda f: f.get("height") or 0)
    # YouTube live audio-only HLS formats (233/234) report acodec=None, so detect them by "no video".
    auds = sorted([f for f in fmts if f.get("vcodec") in (None, "none") and f.get("acodec") != "none"],
                  key=lambda f: (f.get("abr") or f.get("tbr") or 0, f.get("format_id") or ""))
    if not vids:
        raise RuntimeError("no live HLS video format found")
    st = stream["start_ts"]
    ws, we = st + m["start"], st + m["end"]
    v_file, a_file = out.with_suffix(".v.ts"), out.with_suffix(".a.aac")
    v0 = _fetch_joined(_live_segments(vids[-1]["url"], ws, we), v_file)
    inputs = ["-ss", f"{max(0, ws - v0):.2f}", "-i", str(v_file)]
    maps = ["-map", "0:v:0"]
    if auds and vids[-1].get("acodec") in (None, "none"):
        a0 = _fetch_joined(_live_segments(auds[-1]["url"], ws, we), a_file)
        inputs += ["-ss", f"{max(0, ws - a0):.2f}", "-i", str(a_file)]
        maps += ["-map", "1:a:0"]
    else:
        maps += ["-map", "0:a?"]
    dst = out.with_suffix(".mp4")
    run([ffmpeg_exe(), "-y", "-loglevel", "error", *inputs, *maps, "-t", f"{m['end'] - m['start']:.2f}",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-c:a", "aac", str(dst)])
    for p in (v_file, a_file):
        p.unlink(missing_ok=True)
    return dst


def download_section(stream, m, raw_dir, max_h):
    out = raw_dir / f"clip{m['clip']:02d}"
    for old in raw_dir.glob(out.name + ".*"):
        old.unlink()
    if stream.get("live_status") == "is_live":
        return download_live_section(stream, m, out, max_h)
    cmd = ytdlp_base() + [
        "-f", f"bv*[height<={max_h}]+ba/b[height<={max_h}]/b",
        "--download-sections", f"*{m['start']}-{m['end']}",
        "--force-keyframes-at-cuts", "--merge-output-format", "mp4",
        "-o", str(out) + ".%(ext)s", stream["url"]]
    run(cmd)
    files = [p for p in raw_dir.glob(out.name + ".*") if p.suffix in (".mp4", ".mkv", ".webm")]
    if not files:
        raise RuntimeError(f"Download of clip {m['clip']} produced no file")
    return files[0]


def make_vertical(src, dst, mode, src_w, src_h):
    if mode == "center":
        vf = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}"
        layout = {"mode": "center", "fg_top": 0, "fg_bottom": H}
        filt = ["-vf", vf + ",setsar=1"]
    else:
        fg_h = int(round(W * src_h / src_w / 2) * 2) if src_w and src_h else 608
        fg_h = min(fg_h, H)
        top = (H - fg_h) // 2
        layout = {"mode": "blur_fit", "fg_top": top, "fg_bottom": top + fg_h}
        fc = (f"[0:v]split[a][b];"
              f"[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},gblur=sigma=28,eq=brightness=-0.12[bg];"
              f"[b]scale={W}:{fg_h}[fg];[bg][fg]overlay=0:{top},setsar=1[v]")
        filt = ["-filter_complex", fc, "-map", "[v]", "-map", "0:a?"]
    run([ffmpeg_exe(), "-y", "-loglevel", "error", "-i", str(src), *filt,
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
         "-r", "30", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", str(dst)])
    return layout


def probe_size(path):
    res = run([ffmpeg_exe(), "-hide_banner", "-i", str(path)], check=False)
    import re
    m = re.search(r"Video:.*?(\d{3,5})x(\d{3,5})", res.stderr or "")
    return (int(m.group(1)), int(m.group(2))) if m else (None, None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir")
    ap.add_argument("--crop", choices=["blur_fit", "center"])
    ap.add_argument("--only", help="comma-separated clip numbers")
    a = ap.parse_args()
    cfg = load_config()
    run_dir = Path(a.run_dir).resolve()
    stream = load_json(run_dir / "stream.json")
    data = load_json(run_dir / "moments.json")
    mode = a.crop or cfg.get("crop_mode", "blur_fit")
    only = {int(x) for x in a.only.split(",")} if a.only else None
    raw_dir = run_dir / "raw"
    clips_dir = run_dir / "clips"
    raw_dir.mkdir(exist_ok=True)
    clips_dir.mkdir(exist_ok=True)

    for m in data["moments"]:
        if only and m["clip"] not in only:
            continue
        print(f"Clip {m['clip']}: downloading {m['start']:.0f}s-{m['end']:.0f}s ...", flush=True)
        try:
            raw = download_section(stream, m, raw_dir, cfg.get("max_source_height", 1080))
            sw, sh = probe_size(raw)
            dst = clips_dir / f"clip{m['clip']:02d}_vertical.mp4"
            m["layout"] = make_vertical(raw, dst, mode, sw, sh)
            m["vertical"] = str(dst)
            m.pop("error", None)
            print(f"  -> {dst.name}")
        except Exception as ex:
            m["error"] = str(ex)[-500:]
            print(f"  FAILED: {str(ex)[-300:]}")
    save_json(run_dir / "moments.json", data)


if __name__ == "__main__":
    main()
