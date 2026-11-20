"""Build the zip to upload to Claude web (claude.ai > Settings > Capabilities > Skills).

  python scripts/make_web_zip.py            # -> ~/Downloads/saadai-labs-live-clipper.zip

The zip holds the skill folder at its top level (claude.ai needs <skill-name>/SKILL.md) and leaves out
.venv (hundreds of MB), .env (your API key - never share it), output/ (your clips) and caches.
"""
import sys
import zipfile
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
NAME = SKILL.name
SKIP_DIRS = {".venv", "output", "__pycache__", ".git"}
SKIP_FILES = {".env", ".DS_Store", ".write_test"}


def main():
    out = Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else Path.home() / "Downloads" / f"{NAME}.zip"
    out.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(SKILL.rglob("*")):
            rel = f.relative_to(SKILL)
            if not f.is_file() or set(rel.parts) & SKIP_DIRS or f.name in SKIP_FILES or f.suffix == ".pyc":
                continue
            z.write(f, f"{NAME}/{rel.as_posix()}")
            count += 1
    print(f"{count} files -> {out} ({out.stat().st_size / 1e6:.2f} MB)")


if __name__ == "__main__":
    main()
