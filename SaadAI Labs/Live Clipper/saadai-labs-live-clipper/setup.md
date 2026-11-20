# SaadAI Labs - Live Clipper: setup

## What you need
- **Claude Code** (desktop app, terminal or claude.ai/code). The heavy work runs in Python, so token use stays low.
- **Python 3.10-3.13** - python.org (tick "Add to PATH" on Windows).
- **Node.js** (nodejs.org) - YouTube needs a JavaScript runtime for downloads.
- ffmpeg is optional: a copy comes with the Python packages. (Mac: `brew install ffmpeg`, Windows: `winget install Gyan.FFmpeg`.)

## Install (one command)
Unzip this folder into your Claude skills folder (`~/.claude/skills/saadai-labs-live-clipper`), then:

- Mac: `python3 ~/.claude/skills/saadai-labs-live-clipper/scripts/setup.py`
- Windows: `py %USERPROFILE%\.claude\skills\saadai-labs-live-clipper\scripts\setup.py`

## Optional: YouTube API key (better live search with viewer counts)
1. console.cloud.google.com -> new project -> enable "YouTube Data API v3" -> Credentials -> API key.
2. Paste it into `.env` in this folder: `YOUTUBE_API_KEY=your-key`
Without a key the skill still searches live streams with yt-dlp.

## Optional: skip list
Put any streamer you don't want to clip in `blocklist.json`:
```json
{ "name": "Streamer", "handle": "@streamer", "channel_id": "UC...", "reason": "asked not to be clipped" }
```

## Use it
In Claude Code say: **"clip this stream: <link>"** or **"find GTA 6 streams to clip"**.
Every clip gets captions, a hook, a zoom punch-in, sound effects and a `Credit: @streamer` tag.
Clips land in `output/<date>_<video id>/clips/`; approved ones in `output/approved/`.

Always keep the streamer credit, and follow YouTube's, Instagram's and TikTok's rules for reused content.
