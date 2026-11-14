"""Shared helpers for the Shorts Studio scripts."""
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
HOME = Path(os.environ.get("SHORTS_STUDIO_HOME", Path.home() / ".shorts-studio"))
ENGINE = HOME / "engine"
MODELS = HOME / "models"
FPS = 30


def die(msg: str):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def load_json(p: Path):
    try:
        return json.loads(Path(p).read_text())
    except FileNotFoundError:
        die(f"missing file: {p}")
    except json.JSONDecodeError as e:
        die(f"{p} is not valid JSON: {e}")


def save_json(p: Path, data):
    Path(p).write_text(json.dumps(data, indent=2, ensure_ascii=False))


def find_channel(short_dir: Path):
    """channel.json lives in the channel folder; shorts sit in <channel>/shorts/<slug>/."""
    d = short_dir.resolve()
    for _ in range(4):
        c = d / "channel.json"
        if c.exists():
            return c.parent, load_json(c)
        d = d.parent
    return None, {}


def slug_of(short_dir: Path):
    return re.sub(r"[^a-z0-9-]+", "-", short_dir.resolve().name.lower()).strip("-") or "short"


def run(cmd, cwd=None, quiet=False):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout[-3000:], r.stderr[-3000:], file=sys.stderr)
        die(f"command failed: {' '.join(map(str, cmd))[:300]}")
    if not quiet and r.stdout.strip():
        print(r.stdout.strip()[-2000:])
    return r.stdout


def duration(path: Path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                         capture_output=True, text=True).stdout.strip()
    return float(out or 0)


def need_engine():
    if not (ENGINE / "node_modules" / "remotion").exists():
        die(f"engine not installed at {ENGINE}. Run: zsh {SKILL_DIR}/scripts/setup.sh")


def words_of(text: str):
    return [w for w in re.split(r"\s+", (text or "").strip()) if w]


def which(name):
    return shutil.which(name)
