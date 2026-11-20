"""UC2/UC6 - validate a stream and read its live chat (or chat replay) with timestamps.

Usage:
  python scripts/read_chat.py URL [--minutes 30] [--run-dir DIR]

- Ended live with chat replay: downloads the whole replay.
- Live right now: watches the chat for --minutes (default config watch_minutes), then stops.
- Any YouTube live can be clipped; only streamers the user put in blocklist.json are skipped.

Writes into a new run folder: stream.json (stream facts) and chat.jsonl (one message per line:
{"t": seconds into the stream, "text": "..."}). Prints only a short summary, never the chat itself.
"""
import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

from common import (check_blocklist, credit_handle, load_config, new_run_dir, save_json, video_info,
                    ytdlp_base)


def message_text(renderer):
    parts = []
    for run in (renderer.get("message") or {}).get("runs", []):
        if "text" in run:
            parts.append(run["text"])
        elif "emoji" in run:
            em = run["emoji"]
            sc = (em.get("shortcuts") or [""])[0]
            # Unicode emoji have their character as emojiId; custom channel emoji get their :shortcut:
            parts.append(em.get("emojiId") if not em.get("isCustomEmoji") else sc)
    return "".join(parts).strip()


def parse_chat_file(path, stream_start_ts, is_live):
    """Parse yt-dlp's live_chat JSON-lines file into [{t, text}]."""
    msgs = []
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue  # last line of a stopped live download can be half-written
            rep = obj.get("replayChatItemAction", {})
            offset_ms = obj.get("videoOffsetTimeMsec") or rep.get("videoOffsetTimeMsec")
            for act in rep.get("actions", []):
                item = (act.get("addChatItemAction") or {}).get("item", {})
                r = item.get("liveChatTextMessageRenderer") or item.get("liveChatPaidMessageRenderer")
                if not r:
                    continue
                text = message_text(r)
                if not text:
                    continue
                t = None
                if is_live and r.get("timestampUsec") and stream_start_ts:
                    t = int(r["timestampUsec"]) / 1e6 - stream_start_ts
                elif offset_ms is not None:
                    t = int(offset_ms) / 1000.0
                if t is None or t < 0:
                    continue
                msgs.append({"t": round(t, 2), "text": text[:200]})
    msgs.sort(key=lambda m: m["t"])
    return msgs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--minutes", type=float, help="how long to watch a stream that is live now")
    ap.add_argument("--own", action="store_true", help=argparse.SUPPRESS)  # kept for old prompts; no effect
    ap.add_argument("--run-dir")
    a = ap.parse_args()
    cfg = load_config()

    info = video_info(a.url)
    status = info.get("live_status")
    vid = info["id"]
    if status not in ("is_live", "was_live", "post_live"):
        sys.exit(f"Not a live stream (live_status={status}). Give a YouTube link that is live now or a finished live with chat replay.")

    blocked = check_blocklist(info.get("channel_id"), info.get("uploader_id"), info.get("channel"))
    if blocked:
        sys.exit(f"SKIPPED: {info.get('channel')} is on your blocklist.json"
                 + (f" ({blocked.get('reason')})" if blocked.get('reason') else "") + ". Remove them there to clip.")

    run_dir = Path(a.run_dir).resolve() if a.run_dir else new_run_dir(vid)
    run_dir.mkdir(parents=True, exist_ok=True)
    is_live = status == "is_live"
    start_ts = info.get("release_timestamp") or info.get("timestamp")

    stream = {
        "url": a.url, "video_id": vid, "title": info.get("title"), "channel": info.get("channel"),
        "channel_id": info.get("channel_id"), "handle": info.get("uploader_id"),
        "credit": credit_handle(info), "live_status": status, "start_ts": start_ts,
        "duration": info.get("duration"),
        "width": info.get("width"), "height": info.get("height"),
    }
    save_json(run_dir / "stream.json", stream)

    out_tmpl = str(run_dir / "chat.%(ext)s")
    cmd = ytdlp_base() + ["--skip-download", "--write-subs", "--sub-langs", "live_chat", "-o", out_tmpl, a.url]
    if is_live:
        minutes = a.minutes or cfg.get("watch_minutes", 30)
        print(f"Stream is LIVE. Watching chat for {minutes:g} minutes...", flush=True)
        proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        deadline = time.time() + minutes * 60
        while time.time() < deadline and proc.poll() is None:
            time.sleep(5)
        if proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(15)
            except subprocess.TimeoutExpired:
                proc.kill()
        stream["watched_until_ts"] = time.time()
        save_json(run_dir / "stream.json", stream)
    else:
        print("Finished live. Downloading the chat replay (long streams can take a few minutes)...", flush=True)
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        if res.returncode != 0:
            sys.exit("Could not download chat replay:\n" + (res.stderr or "")[-1200:])

    files = sorted(run_dir.glob("chat.live_chat.json*"))
    if not files:
        sys.exit("No chat found. The stream may have chat turned off or chat replay disabled.")
    msgs = parse_chat_file(files[0], start_ts, is_live)
    with open(run_dir / "chat.jsonl", "w", encoding="utf-8") as f:
        for m in msgs:
            f.write(json.dumps(m, ensure_ascii=False) + "\n")
    for p in files:
        p.unlink()

    span = (msgs[-1]["t"] - msgs[0]["t"]) / 60 if msgs else 0
    print(json.dumps({"run_dir": str(run_dir), "channel": stream["channel"], "credit": stream["credit"],
                      "live_status": status, "messages": len(msgs), "chat_minutes": round(span, 1)},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
