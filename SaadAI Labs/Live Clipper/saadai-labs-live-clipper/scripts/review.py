"""UC13 - review and approve clips.

  python scripts/review.py summary RUN_DIR          # table to show the user
  python scripts/review.py approve RUN_DIR 1 3      # copy clips 1 and 3 (+ post text) to output/approved/
  python scripts/review.py approve RUN_DIR all
"""
import argparse
import shutil
from pathlib import Path

from common import fmt_ts, load_json, output_root


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("action", choices=["summary", "approve"])
    ap.add_argument("run_dir")
    ap.add_argument("clips", nargs="*")
    a = ap.parse_args()
    run_dir = Path(a.run_dir).resolve()
    data = load_json(run_dir / "moments.json")
    stream = load_json(run_dir / "stream.json", {})

    if a.action == "summary":
        print(f"Stream: {stream.get('title')} - {stream.get('credit')}\n")
        print("| Clip | Stream time | Score | Why picked | File | Title 1 |")
        print("|---|---|---|---|---|---|")
        for m in data["moments"]:
            f = m.get("final") or m.get("vertical") or ("FAILED: " + m["error"][:60] if m.get("error") else "-")
            t1 = (m.get("titles") or ["-"])[0]
            print(f"| {m['clip']} | {fmt_ts(m['start'])}-{fmt_ts(m['end'])} | {m['score']} | {m['why']} | {f} | {t1} |")
        return

    want = None if (not a.clips or a.clips == ["all"]) else {int(c) for c in a.clips}
    dest = output_root() / "approved"
    dest.mkdir(exist_ok=True)
    for m in data["moments"]:
        if (want and m["clip"] not in want) or not m.get("final"):
            continue
        name = f"{run_dir.name}_clip{m['clip']:02d}"
        shutil.copy2(m["final"], dest / f"{name}.mp4")
        post = Path(m["final"].replace("_final.mp4", "_post.txt"))
        if post.exists():
            shutil.copy2(post, dest / f"{name}_post.txt")
        print(f"Approved: {dest / (name + '.mp4')}")


if __name__ == "__main__":
    main()
