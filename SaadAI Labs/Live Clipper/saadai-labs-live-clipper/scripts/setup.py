"""One-command setup (Mac and Windows):  python3 scripts/setup.py   (Windows: py scripts\\setup.py)

Creates .venv inside the skill folder with Python 3.10-3.13 if available (faster-whisper wheels),
installs requirements.txt, checks ffmpeg and Node/Deno, and prints the python path to use.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
VENV = SKILL / ".venv"
WIN = os.name == "nt"


def pick_python():
    cands = []
    if WIN and shutil.which("py"):
        cands += [["py", f"-3.{v}"] for v in (12, 11, 13, 10)]
    for v in ("3.12", "3.11", "3.13", "3.10"):
        p = shutil.which(f"python{v}")
        if p:
            cands.append([p])
    cands.append([sys.executable])
    for c in cands:
        try:
            out = subprocess.run(c + ["-c", "import sys;print(sys.version_info[:2])"], capture_output=True, text=True)
            if out.returncode == 0:
                return c
        except OSError:
            pass
    return [sys.executable]


def main():
    vpy = VENV / ("Scripts/python.exe" if WIN else "bin/python")
    if not vpy.exists():
        py = pick_python()
        print("Creating virtual env with:", " ".join(py))
        subprocess.check_call(py + ["-m", "venv", str(VENV)])
    subprocess.check_call([str(vpy), "-m", "pip", "install", "-q", "--upgrade", "pip"])
    print("Installing packages (yt-dlp, faster-whisper, Pillow, imageio-ffmpeg)...")
    subprocess.check_call([str(vpy), "-m", "pip", "install", "-q", "-r", str(SKILL / "requirements.txt")])

    if shutil.which("ffmpeg"):
        print("ffmpeg: found", shutil.which("ffmpeg"))
    else:
        print("ffmpeg: not on PATH - using the bundled imageio-ffmpeg copy. (Optional: "
              + ("winget install Gyan.FFmpeg" if WIN else "brew install ffmpeg") + ")")
    if not (shutil.which("deno") or shutil.which("node")):
        print("WARNING: YouTube downloads need a JavaScript runtime. Install Node.js (nodejs.org) or Deno (deno.com).")
    env = SKILL / ".env"
    if not env.exists():
        env.write_text("# Optional: YouTube Data API key for better live search (console.cloud.google.com)\nYOUTUBE_API_KEY=\n", encoding="utf-8")
    print("\nSetup done. Run the scripts with:\n  " + str(vpy))


if __name__ == "__main__":
    main()
