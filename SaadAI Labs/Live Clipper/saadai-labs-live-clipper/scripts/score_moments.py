"""UC8 - score chat spikes and pick the best moments.

Usage:
  python scripts/score_moments.py RUN_DIR [--top N]

Score per 10-second window = chat speed vs. local baseline + share of hype keywords + share of hype emoji.
A window only qualifies at >= min_speed_ratio (3x) the baseline. Spikes closer than 2 minutes are merged.
Default count: clips_per_hour x stream hours, capped at max_clips_per_run. Weak moments are never added.

Writes RUN_DIR/moments.json and prints a short table (Claude reads this, not the chat).
"""
import argparse
import json
import math
import re
import statistics
from collections import Counter
from pathlib import Path

from common import fmt_ts, load_config, load_json, save_json


def compile_keywords(words):
    pats = []
    for w in words:
        w = w.strip().lower()
        if not w:
            continue
        # whole-word match; allow stretched letters at the end ("noooo", "lmaooo")
        core = re.escape(w)
        if w[-1].isalpha():
            core += re.escape(w[-1]) + "*"
        pats.append((w, re.compile(r"(?<![a-z])" + core + r"(?![a-z])", re.I)))
    return pats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir")
    ap.add_argument("--top", type=int, help="override how many clips to pick")
    a = ap.parse_args()
    cfg = load_config()
    run_dir = Path(a.run_dir).resolve()
    stream = load_json(run_dir / "stream.json", {})

    msgs = [json.loads(l) for l in open(run_dir / "chat.jsonl", encoding="utf-8") if l.strip()]
    if len(msgs) < 50:
        print(f"Only {len(msgs)} chat messages - too few to find real spikes. No clips picked.")
        save_json(run_dir / "moments.json", {"moments": [], "reason": "too few chat messages"})
        return

    W = cfg.get("window_seconds", 10)
    kw = compile_keywords(cfg.get("hype_keywords", []))
    emojis = cfg.get("hype_emojis", [])
    n_win = int(msgs[-1]["t"] // W) + 1
    counts = [0] * n_win
    kw_hits = [0] * n_win
    em_hits = [0] * n_win
    kw_words = [Counter() for _ in range(n_win)]
    em_words = [Counter() for _ in range(n_win)]
    samples = [[] for _ in range(n_win)]
    for m in msgs:
        i = int(m["t"] // W)
        counts[i] += 1
        text = m["text"]
        hit = [w for w, p in kw if p.search(text)]
        if hit:
            kw_hits[i] += 1
            kw_words[i].update(hit)
        es = [e for e in emojis if e in text]
        if es:
            em_hits[i] += 1
            em_words[i].update(es)
        if len(samples[i]) < 40:
            samples[i].append(text)

    # Local baseline: median messages per window over +/- baseline_minutes (ignores quiet gaps at start).
    half = int(cfg.get("baseline_minutes", 10) * 60 / W)
    ratio_min = cfg.get("min_speed_ratio", 3.0)
    # Chat floods with greetings at the start and "gg/bye" at the end of a stream; those are not moments.
    skip_start = cfg.get("skip_start_minutes", 3) * 60
    skip_end = cfg.get("skip_end_minutes", 2) * 60
    last_t = msgs[-1]["t"]
    ended = stream.get("live_status") != "is_live"
    first_win = int(msgs[0]["t"] // W)  # live runs start mid-stream; no baseline from before we watched
    windows = []
    for i in range(first_win, n_win):
        if i * W < skip_start or (ended and i * W > last_t - skip_end):
            continue
        lo, hi = max(first_win, i - half), min(n_win, i + half + 1)
        base = max(1.0, statistics.median(counts[lo:hi]))
        ratio = counts[i] / base
        if ratio < ratio_min or counts[i] < 5:
            continue
        kw_share = kw_hits[i] / counts[i]
        em_share = em_hits[i] / counts[i]
        score = ratio + 3 * kw_share + 2 * em_share
        windows.append({"i": i, "t": i * W, "count": counts[i], "baseline": round(base, 1),
                        "ratio": round(ratio, 1), "kw_share": kw_share, "em_share": em_share,
                        "score": round(score, 2)})

    # Merge spikes less than merge_gap apart; keep the strongest window of each group.
    gap = cfg.get("merge_gap_seconds", 120)
    groups = []
    for w in windows:
        if groups and w["t"] - groups[-1][-1]["t"] < gap:
            groups[-1].append(w)
        else:
            groups.append([w])

    clip_len = cfg.get("clip_seconds", 40)
    lead = cfg.get("lead_seconds", 12)
    duration = stream.get("duration") or (msgs[-1]["t"] + 60)
    moments = []
    for g in groups:
        peak = max(g, key=lambda w: w["score"])
        first = g[0]
        i = peak["i"]
        top_kw = [w for w, _ in kw_words[i].most_common(4)]
        top_em = [e for e, _ in em_words[i].most_common(3)]
        # Chat reacts a few seconds after the action, so start before the first window of the spike.
        start = max(0, first["t"] - lead)
        end = min(duration, start + clip_len)
        why = f"chat {peak['ratio']}x normal ({peak['count']} msgs in {W}s vs ~{peak['baseline']})"
        if top_kw:
            why += f", hype words: {', '.join(top_kw)}"
        if top_em:
            why += f", emoji: {' '.join(top_em)}"
        moments.append({"score": peak["score"], "peak_t": peak["t"], "start": round(start, 1), "end": round(end, 1),
                        "speed_ratio": peak["ratio"], "why": why,
                        "chat_sample": samples[i][:15]})

    hours = max(1.0, (msgs[-1]["t"] - msgs[0]["t"]) / 3600)
    limit = a.top or min(cfg.get("max_clips_per_run", 10), math.ceil(cfg.get("clips_per_hour", 3) * hours))
    moments.sort(key=lambda m: m["score"], reverse=True)
    moments = moments[:limit]
    moments.sort(key=lambda m: m["start"])
    for n, m in enumerate(moments, 1):
        m["clip"] = n

    save_json(run_dir / "moments.json", {"limit": limit, "qualified_spikes": len(groups), "moments": moments})
    print(f"{len(groups)} chat spike(s) qualified (>= {ratio_min}x normal). Picked {len(moments)} (limit {limit}).")
    print("| Clip | Stream time | Score | Why picked |")
    print("|---|---|---|---|")
    for m in moments:
        print(f"| {m['clip']} | {fmt_ts(m['start'])}-{fmt_ts(m['end'])} | {m['score']} | {m['why']} |")


if __name__ == "__main__":
    main()
