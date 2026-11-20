# Live Clipper – Turn YouTube Live Streams into Viral Clips with Claude

A free Claude Code skill by **SaadAI Labs**. Give it a YouTube live stream, or let it find live GTA 6 streams for you, and it turns the best moments into edited vertical clips for YouTube Shorts, Instagram Reels and TikTok in a few minutes.

The heavy work runs in Python on your computer, so it uses very few Claude tokens and works on the $20 Claude plan.

---

## What it does

Say in Claude Code:

> run live clipper

Live Clipper then:

1. **Asks for the stream source:** paste your own stream link, or let it find streams that are live right now for "GTA 6" (or any keyword), ranked by live viewers.
2. **Reads the live chat** and finds spikes: "CLIP THAT", "LMAO", 💀😂🔥 and sudden bursts of messages.
3. **Scores every moment** and keeps only the strongest (by default 3 clips per hour of stream, up to 10 per run).
4. **Cuts just those parts** and makes them vertical 1080x1920, starting a few seconds before the spike so the whole moment is in the clip.
5. **Edits every clip:** word-by-word English / Roman Urdu captions, a hook in the first seconds, a zoom punch-in and sound effects on the big moment.
6. **Credits the streamer** with `Credit: @streamer` on screen for the whole clip and a credit line with the stream link in the description.
7. **Writes the upload pack:** 3 titles, a description and hashtags for each clip.
8. **Lets you approve** the clips. Approved clips go to `output/approved/`.

---

## What's in this folder

| File | What it is |
|---|---|
| `saadai-labs-live-clipper.zip` | The skill, ready to unzip into your Claude skills folder |
| `saadai-labs-live-clipper/SKILL.md` | The skill's instructions |
| `saadai-labs-live-clipper/setup.md` | Full setup guide |
| `saadai-labs-live-clipper/config.json` | Settings: keyword, clips per hour, clip length, captions, effects |
| `saadai-labs-live-clipper/blocklist.json` | Optional list of streamers to skip |
| `saadai-labs-live-clipper/scripts/` | Python scripts: find streams, read chat, score, cut, captions, sound effects, review |

---

## Setup (about 10 minutes)

1. **Install** Python 3.10–3.13 (python.org, tick "Add to PATH" on Windows) and Node.js (nodejs.org).
2. **Download** `saadai-labs-live-clipper.zip` and unzip it into `~/.claude/skills/saadai-labs-live-clipper`.
3. **Run the one-time setup:**
   - Mac: `python3 ~/.claude/skills/saadai-labs-live-clipper/scripts/setup.py`
   - Windows: `py %USERPROFILE%\.claude\skills\saadai-labs-live-clipper\scripts\setup.py`
4. **Optional, for better live search:** create a free YouTube Data API v3 key in Google Cloud and put `YOUTUBE_API_KEY=your-key` in a `.env` file in the skill folder. Without a key it still searches with yt-dlp.
5. **Run it** in Claude Code: `run live clipper`, `clip this stream: <link>` or `find GTA 6 streams to clip`.

The first caption run downloads the Whisper speech model (about 500 MB), once.

---

## Ways to earn from clipping

- **Paid clipping campaigns:** brands and streamers pay per 1,000 views on approved clips.
- **A monthly clipping service:** clip for streamers, podcasters and coaches for a fixed monthly fee. Use the [LEAD AI System](../LEAD%20AI%20System) to find clients.
- **Your own clip page:** grow a Shorts channel and earn through the YouTube Partner Program and sponsors.

---

## Rules this skill follows

- Every clip credits the streamer, on screen and in the description. Never remove the credit.
- Streamers in `blocklist.json` are skipped. Add anyone who asked not to be clipped.
- Clip responsibly: prefer streamers who allow clipping or run clipping campaigns, and follow YouTube's, Instagram's and TikTok's rules for reused content.

---

Made by **SaadAI Labs**. More free AI systems for businesses are coming to this repo every week.
