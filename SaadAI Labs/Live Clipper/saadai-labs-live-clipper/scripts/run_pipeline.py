"""PC app mode: run a whole job from one double-click, with a log Claude can read.

Used when Claude works on the user's PC through the Claude desktop app (computer use + folder access) and
cannot type into a terminal. Claude writes a job file, double-clicks the launcher in the skill folder
(Windows: "Live Clipper.bat", Mac: "Live Clipper.command"), then reads the log and status files.

  job file:  <data folder>/job.json           (data folder = <skill>/output on a PC)
  log:       <data folder>/pipeline.log       (overwritten by each job)
  status:    <data folder>/pipeline_status.json  {"state": "running|needs_meta|done|failed", ...}

Jobs (job.json):
  {"action": "setup"}
  {"action": "find", "keyword": "GTA 6"}
  {"action": "clip", "url": "https://www.youtube.com/watch?v=...", "minutes": 10, "top": 3, "crop": "blur_fit"}
  {"action": "clip", "pick": 2}                        # number from the last "find" table
  {"action": "render", "run_dir": "..."}                # run_dir optional: uses the last clip job's run
  {"action": "approve", "run_dir": "...", "clips": "all"}   # or [1, 3]

Can also be run directly:  python scripts/run_pipeline.py [--job PATH]
"""
import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
WIN = os.name == "nt"
VENV_PY = SKILL / ".venv" / ("Scripts/python.exe" if WIN else "bin/python")

sys.path.insert(0, str(HERE))
from common import load_json, output_root, save_json  # noqa: E402  (stdlib only, works before setup)

DATA = output_root()
LOG = DATA / "pipeline.log"
STATUS = DATA / "pipeline_status.json"


def log(msg):
    line = f"[{datetime.now():%H:%M:%S}] {msg}"
    print(line, flush=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def status(state, **extra):
    data = load_json(STATUS, {}) or {}
    data.update(extra, state=state, updated=datetime.now().isoformat(timespec="seconds"), log=str(LOG))
    save_json(STATUS, data)


def py():
    return str(VENV_PY) if VENV_PY.exists() else sys.executable


def step(name, args):
    """Run one skill script, copying its output into the log. Returns its full output."""
    status("running", step=name)
    log(f"--- {name} ---")
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
    proc = subprocess.Popen([py(), *args], cwd=HERE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            text=True, encoding="utf-8", errors="replace", env=env)
    out = []
    for line in proc.stdout:
        out.append(line)
        log("  " + line.rstrip())
    if proc.wait() != 0:
        raise RuntimeError(f"{name} failed (see the lines above)")
    return "".join(out)


def ensure_setup():
    if VENV_PY.exists():
        return
    log("First run: setting up (a few minutes)...")
    step("setup", ["setup.py"])


def clip(job):
    url = job.get("url")
    if not url and job.get("pick"):
        streams = (load_json(DATA / "last_search.json", {}) or {}).get("streams", [])
        n = int(job["pick"])
        if not 1 <= n <= len(streams):
            raise RuntimeError(f"pick {n} is not in the last search (1-{len(streams)}). Run a find job first.")
        url = streams[n - 1]["url"]
        log(f"Picked #{n}: {streams[n - 1].get('channel')} - {url}")
    if not url:
        raise RuntimeError('clip job needs "url" or "pick"')
    args = ["read_chat.py", url]
    if job.get("minutes"):
        args += ["--minutes", str(job["minutes"])]
    out = step("read chat", args)
    start = out.find("{")
    run_dir = json.loads(out[start:out.rfind("}") + 1])["run_dir"]
    status("running", run_dir=run_dir)
    out = step("score moments", ["score_moments.py", run_dir] + (["--top", str(job["top"])] if job.get("top") else []))
    moments = (load_json(Path(run_dir) / "moments.json", {}) or {}).get("moments", [])
    if not moments:
        log("No strong moments found - nothing to cut.")
        return status("done", run_dir=run_dir, result="no_moments")
    step("cut clips", ["cut_clips.py", run_dir] + (["--crop", job["crop"]] if job.get("crop") else []))
    step("transcribe", ["add_captions.py", "transcribe", run_dir])
    log("NEXT: Claude writes clips/clipNN.meta.json for each clip, then runs a render job.")
    status("needs_meta", run_dir=run_dir)


def render(job):
    run_dir = job.get("run_dir") or (load_json(STATUS, {}) or {}).get("run_dir")
    if not run_dir:
        raise RuntimeError('render job needs "run_dir"')
    step("render", ["add_captions.py", "render", run_dir])
    step("summary", ["review.py", "summary", run_dir])
    status("done", run_dir=run_dir, result="rendered")


def approve(job):
    run_dir = job.get("run_dir") or (load_json(STATUS, {}) or {}).get("run_dir")
    clips = job.get("clips", "all")
    clips = ["all"] if clips == "all" else [str(c) for c in clips]
    step("approve", ["review.py", "approve", run_dir, *clips])
    status("done", run_dir=run_dir, result="approved")


def main():
    job_path = Path(sys.argv[sys.argv.index("--job") + 1]) if "--job" in sys.argv else DATA / "job.json"
    LOG.write_text("", encoding="utf-8")
    last_run = (load_json(STATUS, {}) or {}).get("run_dir")
    save_json(STATUS, {"run_dir": last_run} if last_run else {})
    job = load_json(job_path)
    if not job:
        log(f"No job file at {job_path}. Write one (see run_pipeline.py) and start the launcher again.")
        status("failed", error="no job file")
        return 1
    action = job.get("action")
    log(f"Job: {json.dumps(job, ensure_ascii=False)}")
    status("running", action=action, step="start")
    try:
        if action == "setup":
            step("setup", ["setup.py"])
            status("done", result="setup")
        else:
            ensure_setup()
            if action == "find":
                step("find streams", ["find_live_streams.py"] + (["--keyword", job["keyword"]] if job.get("keyword") else []))
                status("done", result="found", table=str(DATA / "last_search.json"))
            elif action == "clip":
                clip(job)
            elif action == "render":
                render(job)
            elif action == "approve":
                approve(job)
            else:
                raise RuntimeError(f"unknown action {action!r}")
    except Exception as exc:  # noqa: BLE001
        log(f"FAILED: {exc}")
        status("failed", error=str(exc)[:500])
        return 1
    log("FINISHED")
    return 0


if __name__ == "__main__":
    code = main()
    if "--no-wait" not in sys.argv and os.environ.get("LIVECLIPPER_NO_WAIT") != "1":
        time.sleep(3)  # leave the launcher window up briefly so the user sees how it ended
    sys.exit(code)
