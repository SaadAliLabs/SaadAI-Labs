"""Shared helpers for the Live Clipper scripts (paths, config, block-list, tools)."""
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = SKILL_DIR / "config.json"
BLOCKLIST_PATH = SKILL_DIR / "blocklist.json"

# Windows consoles default to a legacy code page; make printing emoji / Urdu safe.
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def http_get(url, timeout=30):
    """GET a URL and return bytes. Uses certifi's certificates (python.org Python on Mac ships without them)."""
    import ssl
    import urllib.request
    try:
        import certifi
        ctx = ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        ctx = ssl.create_default_context()
    with urllib.request.urlopen(url, timeout=timeout, context=ctx) as r:
        return r.read()


def load_json(path, default=None):
    path = Path(path)
    if not path.exists():
        return default
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_config():
    return load_json(CONFIG_PATH, {})


def load_env():
    """Read KEY=VALUE lines from the skill's .env into os.environ (no extra package needed)."""
    env = SKILL_DIR / ".env"
    if env.exists():
        for line in env.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def output_root():
    cfg = load_config()
    custom = (cfg.get("output_dir") or "").strip()
    root = Path(os.path.expanduser(custom)) if custom else SKILL_DIR / "output"
    root.mkdir(parents=True, exist_ok=True)
    return root


def new_run_dir(video_id):
    d = output_root() / f"{datetime.now():%Y%m%d-%H%M}_{video_id}"
    d.mkdir(parents=True, exist_ok=True)
    return d


def ffmpeg_exe():
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        sys.exit("ffmpeg not found. Run scripts/setup.py, or install ffmpeg (Mac: brew install ffmpeg, Windows: winget install Gyan.FFmpeg).")


def ytdlp_base():
    """yt-dlp command with ffmpeg location and a JS runtime (YouTube needs one for some formats)."""
    cmd = [sys.executable, "-m", "yt_dlp", "--no-warnings", "--ffmpeg-location", ffmpeg_exe()]
    if not shutil.which("deno") and shutil.which("node"):
        cmd += ["--js-runtimes", "node"]
    return cmd


def run(cmd, check=True, capture=True, **kw):
    res = subprocess.run(cmd, capture_output=capture, text=True, encoding="utf-8", errors="replace", **kw)
    if check and res.returncode != 0:
        tail = (res.stderr or res.stdout or "")[-1500:]
        raise RuntimeError(f"Command failed ({res.returncode}): {' '.join(map(str, cmd[:6]))} ...\n{tail}")
    return res


def video_info(url):
    res = run(ytdlp_base() + ["-J", "--skip-download", url])
    return json.loads(res.stdout)


def fmt_ts(seconds):
    seconds = int(max(0, seconds))
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


# ---------- block-list ----------
# Every stream can be clipped. blocklist.json is an optional list of streamers the user chooses to skip
# (for example a streamer who asked people not to clip them, or who sends takedowns).

def _norm(s):
    return re.sub(r"\s+", "", (s or "").lower().lstrip("@"))


def blocklist_entries():
    data = load_json(BLOCKLIST_PATH, {"streamers": []})
    return data.get("streamers", [])


def check_blocklist(channel_id=None, handle=None, name=None):
    """Return the matching block-list entry, or None (None = OK to clip)."""
    for e in blocklist_entries():
        if channel_id and e.get("channel_id") and e["channel_id"] == channel_id:
            return e
        if handle and e.get("handle") and _norm(e["handle"]) == _norm(handle):
            return e
        if name and e.get("name") and _norm(e["name"]) == _norm(name):
            return e
    return None


def credit_handle(info):
    """Best '@handle' to credit for a stream."""
    h = info.get("uploader_id") or info.get("channel") or info.get("uploader") or "streamer"
    h = str(h).strip()
    return h if h.startswith("@") else "@" + h.replace(" ", "")
