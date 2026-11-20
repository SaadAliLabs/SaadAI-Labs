---
name: saadai-labs-live-clipper
description: SaadAI Labs - Live Clipper. Turns any YouTube live stream (live now or a finished live with chat replay) into short, edited vertical 1080x1920 clips for Shorts, Reels and TikTok - finds live GTA 6 (or any keyword) streams ranked by live viewers or takes any stream link, reads live chat spikes ("CLIP THAT", "LMAO", 💀😂🔥) to find the best moments, cuts just those parts, makes them vertical, adds word-by-word English / Roman Urdu captions, a hook, a zoom punch-in and sound effects (whoosh, riser, boom) on the big moment, credits the streamer on screen and in the description, and writes 3 titles, a description and hashtags per clip, then lets the user approve them. Use whenever the user wants to clip a live stream, make clips from a YouTube live or stream, find GTA 6 streams to clip, "clip this stream", "run live clipper", or names SaadAI Labs - Live Clipper, even if they don't say skill.
---

# SaadAI Labs - Live Clipper

Python scripts do all heavy work (yt-dlp, chat reading, ffmpeg, faster-whisper, sound effects). **Never read
chat.jsonl, video or the raw yt-dlp output into context** - only the short tables and small JSON/text files named
below. This keeps token use low.

`SKILL_DIR` = the folder this file is in. Paths below are relative to it. This skill runs in **Claude Code**
(Mac/Windows), in the **Claude desktop app on the user's PC** (computer use), and on **Claude web** (claude.ai
cloud sandbox - YouTube often blocks downloads there, so prefer the PC whenever you can reach it).

### Where am I running? (check once, at the start)
- **PC app mode** (best for the desktop app): you have computer-use / folder-access tools for the user's own PC
  (Windows or Mac) but can't type into a terminal there. Downloads come from the user's home internet, so YouTube's
  bot check rarely appears. Everything runs through one launcher file in the skill folder **on the PC**:
  1. Find the skill folder on the PC (it has `Live Clipper.bat` and `Live Clipper.command`). If there is none, ask
     the user to unzip the skill zip into Documents (e.g. `Documents\saadai-labs-live-clipper`) and give you access
     to that folder. Python must be installed (python.org; on Windows tick "Add python.exe to PATH").
  2. Write the job as `output/job.json` in that folder (create `output/` if missing). Jobs:
     - `{"action": "find", "keyword": "GTA 6"}` -> table in `output/pipeline.log`, list in `output/last_search.json`
     - `{"action": "clip", "pick": 2, "minutes": 10, "top": 3}` (or `"url": "..."` instead of `pick`) -> reads chat,
       scores, cuts and transcribes in one go
     - `{"action": "render"}` -> renders the clips of the last clip job and prints the review table
     - `{"action": "approve", "clips": [1, 3]}` (or `"all"`)
     - `{"action": "setup"}` (the first job of any kind also runs setup by itself, a few minutes)
  3. Double-click `Live Clipper.bat` (Windows, File Explorer) or `Live Clipper.command` (Mac, Finder). A window
     opens and shows progress. On a Mac the first double-click may be blocked as "unidentified developer": ask the
     user to right-click it > Open once.
  4. Read `output/pipeline_status.json` until `state` is `done`, `needs_meta` or `failed`, and read
     `output/pipeline.log` for the tables. Don't re-read a long log over and over: check the status file and only
     the end of the log. A live chat watch takes `minutes` + a few minutes.
  5. On `needs_meta`: write `clips/clipNN.meta.json` in the `run_dir` (step 5 below), then run a `render` job.
  Steps 1-7 below are the same; each script call simply becomes part of a job.
- **Claude web**: `/mnt/user-data` exists, or `SKILL_DIR` is under `/mnt/skills/` (read-only), and you have no
  access to the user's PC.
  - First tell the user plainly: YouTube usually blocks downloads from Claude's cloud servers, so the search will
    work but cutting clips may not. Clipping works reliably in the Claude desktop app on their PC (PC app mode) or
    Claude Code.
  - Setup every new chat (the sandbox starts clean): `python3 SKILL_DIR/scripts/setup.py` (~1-2 min). `PY` = `python3`.
  - If setup prints **NETWORK BLOCKED**, stop and tell the user exactly what it printed: in claude.ai
    **Settings > Capabilities > Code execution**, allow the listed domains (or "All domains"), then open a new chat.
    Don't try other workarounds.
  - Clips are made in `~/LiveClipper/` and every finished clip + post text is copied to `/mnt/user-data/outputs/`,
    so the user can download it from the chat. Tell them it is there; there is no `open` command on the web.
  - Commands can't run in the background. Keep each command short: `--minutes 5` for a live chat watch, and use
    `whisper_model` `base` (faster). If a step gets cut off by a time limit, tell the user and run it again for one clip at a time (`--only N` on cut_clips.py and render).
  - YouTube sometimes blocks sandbox servers ("Sign in to confirm you're not a bot"). Browser cookies don't exist
    on the web, so if that happens say so plainly: another stream won't help (the whole server is blocked). Suggest
    the Claude desktop app on their PC (PC app mode) or Claude Code.
- **Claude Code**: `PY` = `.venv/bin/python` (Mac) or `.venv\Scripts\python.exe` (Windows). If `.venv` is missing, run
  `python3 scripts/setup.py` (Windows: `py scripts\setup.py`) and tell the user it is a one-time setup (a few minutes;
  the first caption run also downloads the Whisper model, ~500 MB for "small"). Long steps: run in the background
  and wait for them to finish. Clips are made in `SKILL_DIR/output/`.

Run every script from the `scripts/` folder (`cd SKILL_DIR/scripts && PY read_chat.py ...`) or give the full path;
each prints a short result. Below, `output/` means the data folder for your surface (`output/` or `~/LiveClipper/`).

## Which streams
Any YouTube live stream can be clipped - no permission step. Every clip is edited (captions, hook, zoom, sound
effects) and **always credits the streamer**: `Credit: @streamer` on screen for the whole clip, and a credit line
with the stream link in the description. Never remove the credit.
`blocklist.json` is an optional skip list: streamers in it are skipped (add one only when the user asks, e.g. a
streamer who asked not to be clipped).

## Workflow

### 1. Choose stream source (UC1)
Ask: **"Do you have a stream link, or should I find live GTA 6 streams for you?"** (skip if they already gave a link).

**Option A - a link (UC2):** `PY read_chat.py URL`

**Option B - auto-find (UC3, UC4):** `PY find_live_streams.py [--keyword "GTA 6"]`
- Uses the YouTube Data API if `YOUTUBE_API_KEY` is set (`.env` in the skill or data folder), otherwise yt-dlp's
  live search. Never ask the user to paste an API key into the chat.
- Show the table (channel, live viewers, live for, title). The user picks a number -> take its `url` from
  `output/last_search.json` -> `PY read_chat.py URL`.

For a stream that is **live now**, `read_chat.py` watches the chat for `--minutes` (default 10 in config). YouTube
only keeps the last ~15 minutes of a live for rewinding, so watch in rounds of 10 minutes and cut right after each
round (on Claude web use 5-minute rounds). For a whole stream, wait until it ends and use the replay. A finished live downloads the full chat replay.

`read_chat.py` prints the `run_dir` - use it for every next step.

### 2. Find and score moments (UC6, UC8)
`PY score_moments.py RUN_DIR [--top N]`
- Qualifies at 3x normal chat speed (`min_speed_ratio`); merges spikes < 2 min apart; default 3 clips per stream
  hour, max 10. Ignores the greeting flood at the start and "gg" at the end.
- If it finds none, say so - never pad with weak moments. Very big streams (100k+ viewers) show a filtered chat that
  barely speeds up; offer to lower `min_speed_ratio` to 1.5-2 (`PY settings.py min_speed_ratio 2`) and re-run.

### 3. Cut and make vertical (UC9)
`PY cut_clips.py RUN_DIR [--crop blur_fit|center]`
- `blur_fit` (default): full frame in the middle over a blurred copy. `center`: fills the screen, crops the sides.
- Downloads only those 40-second parts. Report any clip that FAILED (the reason is in moments.json `error`).

### 4. Transcribe (UC10, part 1)
`PY add_captions.py transcribe RUN_DIR`

### 5. Write hook, titles, hashtags, effect timing (UC12) - your job
For each clip read only `clips/clipNN.transcript.txt` and that clip's `why` + `chat_sample` in `moments.json`.
Write `clips/clipNN.meta.json`:
```json
{
  "hook": "HE DID NOT SEE THAT COMING",
  "titles": ["...", "...", "..."],
  "description": "1-2 lines about the moment. (Credit line + stream link are added automatically.)",
  "hashtags": ["#GTA6", "#GTA6Clips", "#gaming", "..."],
  "punch_at": 9.5,
  "roman_lines": ["one Roman Urdu line per transcript segment, same order and count"]
}
```
- **hook**: max ~6 words, curiosity or shock, readable in under 2 seconds. Don't lie about what happens.
- **titles**: 3 different angles (what happened / reaction / question). Under 70 characters. Name the game.
- **hashtags**: 5-8, mix big (#GTA6) and specific; include the streamer's name as a tag.
- **punch_at**: seconds into the clip where the big moment happens (the scream, crash, punchline) - use the
  transcript timings. Zoom punch-in, riser and boom land there. Leave out to use the default (~9 s).
- **sfx** (optional): your own list `[{"t": 3.2, "type": "ding"}, ...]` replaces the default set. Types: whoosh,
  swoosh_down, pop, boom, riser, ding, glitch. Default: whoosh when the hook appears, swoosh when it leaves,
  riser into the moment, boom on it. Keep it to 3-6 effects so it doesn't feel spammy.
- **roman_lines**: only when transcript language is `ur` or `hi`: rewrite each segment in Roman Urdu (Latin letters,
  how people type on WhatsApp). Same count as segments or it is ignored. For English, leave it out.
- Don't invent what happened beyond what the transcript and chat show.

### 6. Render (UC10, UC11)
`PY add_captions.py render RUN_DIR` -> `clips/clipNN_final.mp4` + `clips/clipNN_post.txt`
- Word-by-word captions (active word yellow), `Credit: @streamer` for the whole clip, hook for the first 2 seconds,
  zoom punch-in and sound effects on the moment, stream audio kept, credit line + stream link in the description.

### 7. Review and approve (UC13)
`PY review.py summary RUN_DIR` -> show the table (clip, stream time, score, why picked, file, title).
Offer to open the clips (Claude Code on Mac: `open FILE`; Claude web: they are already in the chat's downloads). When the user approves: `PY review.py approve RUN_DIR 1 3` (or `all`) ->
copies to `output/approved/` with the post text (on Claude web also to `/mnt/user-data/outputs/approved_*`). Give full file paths.
To change one clip: edit its meta.json (hook, punch_at, sfx...) and re-run render with `--only N`.

## Settings
Change a setting with `PY settings.py KEY VALUE` (show all: `PY settings.py`). It saves to `output/config.json`, which
overrides the skill's `config.json` - this works on Claude web, where the skill folder is read-only. Keys:
`search_keyword`, `watch_minutes`, `min_speed_ratio`, `clips_per_hour`, `max_clips_per_run`, `clip_seconds` (30-45),
`lead_seconds` (10-15), `crop_mode`, `whisper_model` (`base` faster / `small` better), `whisper_language` (null = auto),
`hype_keywords`, `hype_emojis`, `caption_highlight`, `hook_seconds`, `sound_effects` (on/off), `sfx_volume` (0-1),
`caption_pops` (pop on every caption line), `punch_in`, `punch_zoom`, `font_path`, `output_dir` (empty = `output/`).
Change them when the user asks ("give me 5 clips", "no sound effects", "louder effects", "use the center crop").

## Not built yet (v2 - only if asked)
Loud-audio moment detection, face-on-top layout, Urdu/Hindi script captions, Google Sheet log of clips and views,
auto-posting to Shorts/Reels/TikTok, watching 3-5 streams with WhatsApp/Telegram approval.

## Sharing the skill (Claude web upload)
`PY make_web_zip.py` builds `~/Downloads/saadai-labs-live-clipper.zip` with the folder at the top level, leaving out
`.venv`, `.env` (API key), `output/` and caches. The user uploads it in claude.ai **Settings > Capabilities > Skills**
(code execution must be on). Never zip the skill folder by hand - it would include the API key and ~350 MB of `.venv`.

## Troubleshooting
- "Sign in to confirm you're not a bot" / 403: update yt-dlp (`PY -m pip install -U "yt-dlp[default]"`); if it continues,
  the user can add `--cookies-from-browser chrome` to the yt-dlp command in `common.py` `ytdlp_base()` (ask first).
- "No chat found": chat replay is off for that stream - pick another.
- "older than the live rewind window": the moment is more than ~15 min old on a live stream - wait for the replay.
