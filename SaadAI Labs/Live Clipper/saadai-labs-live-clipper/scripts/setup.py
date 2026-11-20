"""One-command setup:  python3 scripts/setup.py   (Windows: py scripts\\setup.py)

Claude Code (Mac/Windows): creates .venv inside the skill folder with Python 3.10-3.13 if available
(faster-whisper wheels), installs requirements.txt, checks ffmpeg and Node/Deno.
Claude web (claude.ai): the skill folder is read-only, so packages go into the sandbox's own Python
(no .venv) and setup checks that YouTube can be reached. Use --web to force this mode.
Prints the python to use (PY) at the end.
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


def can_write(folder):
    try:
        probe = folder / ".write_test"
        probe.write_text("ok", encoding="utf-8")
        probe.unlink()
        return True
    except OSError:
        return False


def web_setup():
    """claude.ai sandbox: install into the current Python, then check the network."""
    req = str(SKILL / "requirements.txt")
    print("Claude web mode: installing packages into the sandbox Python (yt-dlp, faster-whisper, Pillow, imageio-ffmpeg)...")
    base = [sys.executable, "-m", "pip", "install", "-q", "-r", req]
    if subprocess.run(base).returncode != 0:
        subprocess.check_call(base + ["--break-system-packages"])
    print("ffmpeg:", shutil.which("ffmpeg") or "using the bundled imageio-ffmpeg copy")
    if not (shutil.which("deno") or shutil.which("node")):
        print("WARNING: no Node.js or Deno in this sandbox - some YouTube formats may fail.")
    import ssl
    import urllib.request
    try:
        import certifi
        ctx = ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        ctx = ssl.create_default_context()
    ok = True
    for host in ("https://www.youtube.com", "https://huggingface.co"):
        try:
            urllib.request.urlopen(host, timeout=15, context=ctx)
            print("network:", host, "OK")
        except Exception as exc:  # noqa: BLE001
            ok = False
            print("network:", host, "BLOCKED", f"({str(exc)[:80]})")
    if not ok:
        print("\nNETWORK BLOCKED. In claude.ai go to Settings > Capabilities > Code execution and allow these")
        print("domains (or 'All domains'): youtube.com, *.youtube.com, *.googlevideo.com, *.ytimg.com,")
        print("youtubei.googleapis.com, huggingface.co, *.huggingface.co, *.hf.co  - then start a NEW chat.")
    print("\nSetup done. PY =", sys.executable)


def main():
    if "--web" in sys.argv or Path("/mnt/user-data").is_dir() or not can_write(SKILL):
        return web_setup()
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
