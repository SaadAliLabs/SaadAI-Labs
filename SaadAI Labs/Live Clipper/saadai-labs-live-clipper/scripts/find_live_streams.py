"""UC3/UC4 - find live streams for a keyword and rank them by live viewers.

Usage:
  python scripts/find_live_streams.py                    # uses config search_keyword
  python scripts/find_live_streams.py --keyword "GTA 6"
  python scripts/find_live_streams.py --check URL        # channel facts of one stream

Prints a numbered table and writes output/last_search.json (the list the user picks from).
Uses the YouTube Data API when YOUTUBE_API_KEY is set in .env, otherwise yt-dlp's live search.
"""
import argparse
import json
import os
import sys
import urllib.parse
from datetime import datetime, timezone

from common import (check_blocklist, http_get, load_config, load_env, output_root, run, save_json,
                    video_info, ytdlp_base)


def _get(url, params):
    return json.loads(http_get(url + "?" + urllib.parse.urlencode(params)).decode("utf-8"))


def search_api(keyword, n, key):
    s = _get("https://www.googleapis.com/youtube/v3/search", {
        "part": "snippet", "eventType": "live", "type": "video", "q": keyword,
        "maxResults": min(50, n * 3), "order": "viewCount", "key": key})
    ids = [i["id"]["videoId"] for i in s.get("items", [])]
    if not ids:
        return []
    v = _get("https://www.googleapis.com/youtube/v3/videos", {
        "part": "snippet,liveStreamingDetails", "id": ",".join(ids), "key": key})
    out = []
    for it in v.get("items", []):
        lsd = it.get("liveStreamingDetails", {})
        start = lsd.get("actualStartTime")
        live_min = None
        if start:
            st = datetime.fromisoformat(start.replace("Z", "+00:00"))
            live_min = int((datetime.now(timezone.utc) - st).total_seconds() // 60)
        out.append({
            "video_id": it["id"], "url": f"https://www.youtube.com/watch?v={it['id']}",
            "title": it["snippet"]["title"], "channel": it["snippet"]["channelTitle"],
            "channel_id": it["snippet"]["channelId"], "handle": None,
            "viewers": int(lsd.get("concurrentViewers", 0) or 0), "live_minutes": live_min})
    return out


def search_ytdlp(keyword, n):
    # sp=EgJAAQ%3D%3D is YouTube's "Live" filter on the search results page.
    url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote(keyword) + "&sp=EgJAAQ%253D%253D"
    res = run(ytdlp_base() + ["--flat-playlist", "-J", "--playlist-end", str(n * 3), url])
    data = json.loads(res.stdout)
    out = []
    for e in data.get("entries") or []:
        if not e or e.get("live_status") not in (None, "is_live"):
            continue
        out.append({
            "video_id": e.get("id"), "url": e.get("url") or f"https://www.youtube.com/watch?v={e.get('id')}",
            "title": e.get("title"), "channel": e.get("channel") or e.get("uploader"),
            "channel_id": e.get("channel_id"), "handle": e.get("uploader_id"),
            "viewers": int(e.get("concurrent_view_count") or e.get("view_count") or 0), "live_minutes": None})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--keyword")
    ap.add_argument("--max", type=int)
    ap.add_argument("--show-all", action="store_true", help="also show block-listed streamers")
    ap.add_argument("--check", help="show channel facts for one stream URL")
    a = ap.parse_args()
    cfg = load_config()
    load_env()

    if a.check:
        info = video_info(a.check)
        e = check_blocklist(info.get("channel_id"), info.get("uploader_id"), info.get("channel"))
        print(json.dumps({"channel": info.get("channel"), "handle": info.get("uploader_id"),
                          "channel_id": info.get("channel_id"), "live_status": info.get("live_status"),
                          "blocked": bool(e)}, ensure_ascii=False, indent=2))
        return

    keyword = a.keyword or cfg.get("search_keyword", "GTA 6")
    n = a.max or cfg.get("search_max_results", 10)
    show_all = a.show_all or cfg.get("show_blocked", False)
    key = os.environ.get("YOUTUBE_API_KEY")
    source = "YouTube Data API"
    streams = []
    if key:
        try:
            streams = search_api(keyword, n, key)
        except Exception as ex:
            print(f"(YouTube API failed: {ex}; using yt-dlp search instead)", file=sys.stderr)
    if not streams:
        source = "yt-dlp live search (no API key; viewer counts may be missing)"
        streams = search_ytdlp(keyword, n)

    for s in streams:
        s["blocked"] = bool(check_blocklist(s.get("channel_id"), s.get("handle"), s.get("channel")))
    streams.sort(key=lambda s: s["viewers"], reverse=True)
    hidden = sum(1 for s in streams if s["blocked"])
    shown = streams if show_all else [s for s in streams if not s["blocked"]]
    shown = shown[:n]
    for i, s in enumerate(shown, 1):
        s["pick"] = i

    save_json(output_root() / "last_search.json", {"keyword": keyword, "source": source, "streams": shown})
    print(f"Live streams for '{keyword}' via {source}")
    print("| # | Channel | Live viewers | Live for | Title |")
    print("|---|---|---|---|---|")
    for s in shown:
        lm = f"{s['live_minutes'] // 60}h {s['live_minutes'] % 60}m" if s["live_minutes"] is not None else "?"
        print(f"| {s['pick']} | {s['channel']} | {s['viewers']:,} | {lm} | {(s['title'] or '')[:60]} |")
    if not shown:
        print("(none to show)")
    if hidden and not show_all:
        print(f"\n{hidden} stream(s) hidden because the streamer is on your blocklist.json.")


if __name__ == "__main__":
    main()
