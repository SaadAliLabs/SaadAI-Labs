---
name: saadai-labs-shorts-studio
description: SaadAI-Labs-ShortsStudio. Creates complete faceless 2D animated YouTube Shorts (also TikTok/Reels) from A to Z - finds viral ideas for a niche, writes 3 scored hooks and a retention-optimised script (explainer, cartoon story, myth-vs-fact or ranking), shows a storyboard for approval, voices it with a realistic male narrator (free Kokoro or ElevenLabs), animates it in Remotion with 2D characters, emoji, stat counters, lists, VS cards and word-by-word captions, adds sound effects and music, checks every scene, renders a 1080x1920 MP4, and writes title, description, hashtags and pinned comment. Remembers each channel's look, voice and past topics. Use whenever the user wants a YouTube Short, faceless/animated/cartoon/explainer short, a video from a title, topic or image, shorts ideas, or to start a shorts channel, even if they don't say skill. Not for editing recorded talking-head reels.
---

# Shorts Studio (2D faceless YouTube Shorts)

You are the writer, director and editor. The bundled Remotion engine does the animation; your job is the part
that decides views: the idea, the hook, the script, which visual shows each beat, and checking the result.

Paths below are relative to this skill's folder. Scripts: `scripts/`. Detailed references:
- `references/script-formulas.md`: hook patterns, the 4 formats, loop endings. **Read before writing any script.**
- `references/spec.md`: channel.json / short.json fields, every scene type, safe zones. **Read before writing a spec.**
- `references/ideas-and-upload.md`: idea mode, reference videos, upload pack, monetisation safety.
- `examples/`: a channel.json and two complete shorts (explainer + story) to copy from.

## What the user can give you
| Input | What you do |
|---|---|
| A title / topic | Go straight to step 3 |
| A niche, or "give me ideas" | Idea mode (references/ideas-and-upload.md) → they pick → step 3 |
| An image (character, logo, brand) | Map it into `theme` / `characters` in channel.json, say what you mapped, then continue |
| A reference video link | V1 can't watch videos: ask for the transcript or a description, copy only the *structure* |
| "Same as last time" / a channel name | Load that channel's channel.json + history.md and continue |

## Workflow

### 1. Setup (once per machine)
`bash scripts/setup.sh` (on claude.ai: see "Running on claude.ai" below; it must run as a background job): installs the Remotion engine to `~/.shorts-studio/engine` (npm, ~1-2 min), ffmpeg,
whisper.cpp + a small English model (word-exact captions), and generates the royalty-free music loops.
Re-run it after updating the skill (it syncs the engine source and keeps everything installed).
Needs Node 18+, Python 3 with numpy + pillow (setup installs them), macOS for the free voice.

### 2. Channel (once per channel)
Find or create the channel folder (ask where; default `~/Shorts/<channel-slug>/`). If there's no `channel.json`,
ask in **one** message: niche, target audience, and vibe (colours / free or ElevenLabs voice / recurring
characters or not). Fill sensible defaults for anything they skip, copying the shape of `examples/channel.json`.
Create `history.md` and `ideas.md` (empty). Read `history.md` before every new short and never repeat a topic.

### 3. Hook + script
Read `references/script-formulas.md`. Pick the format that fits the topic (and isn't the same format as the
last 2 shorts in history.md). Write **3 hook options**, score them, and draft the scenes. Rules that matter most:
frame 0 shows the payoff, narration starts at once, 20-45 s total, one sentence per scene, a visual change every
1.5-4 s, the last line loops into the first. Fact content must be true: check doubtful facts with WebSearch and
keep the source for the description.

Write `shorts/<yyyy-mm-dd-slug>/short.json` (see references/spec.md).

### 4. Storyboard (the human approval step: don't skip it)
```
python3 scripts/build.py <short_dir> --draft
python3 scripts/storyboard.py <short_dir>
```
Fix every WARNING build.py prints first. Then Read `storyboard.jpg` yourself and check each frame: text readable,
nothing overlapping, the right emoji, characters where they should be. Then show the user the 3 hooks
(recommended one marked), the script as a numbered list (scene → narration → visual) and the storyboard image.
End that message with exactly this line, in bold: **Reply "approve" and I'll make the video, or tell me what to change.**
The storyboard JPG is a preview, never the deliverable: a turn that ends with only a JPG and no clear question is a bug.
Changes → edit short.json → rebuild the storyboard. This costs nothing; voicing does. If the user already said to
skip approval ("just make it", "no preview"), show the storyboard and continue straight to step 5 in the same turn.

### 5. Voice
`python3 scripts/voice.py <short_dir>`: voices each scene (cached: editing one scene re-voices only that scene),
times every word with whisper, writes `timing.json`. **The narrator is a realistic male voice by default.**
Provider comes from channel.json `voice`:
- **Kokoro** (default, free, runs locally): a natural neural voice, default blend `am_michael:0.65+am_fenrir:0.35`
  at speed 1.12, with broadcast-style EQ and compression. Other male voices: `am_michael` (warm), `am_fenrir`
  (deep, confident), `am_puck` (energetic), `am_echo`, `am_eric`, `am_liam`, `am_onyx`, and British `bm_george`,
  `bm_fable`, `bm_lewis`, `bm_daniel`. Set `voice.name` to one voice or a blend (`"am_puck:0.5+am_michael:0.5"`).
  `voice.gender: "female"` switches the default to a female voice.
- **ElevenLabs** (paid, the most human): used automatically when `ELEVENLABS_API_KEY` is set in the user's shell.
  Default voice Brian (male); `voice.id` picks another. Never ask the user to paste an API key into chat.
- The robotic macOS `say` voice is only a last-resort fallback if Kokoro isn't installed; if you see its warning,
  run setup.sh instead of shipping that voice.
Delivery comes from the script: short sentences, contractions, `!` and `?` where a person would really say
them, and `…` or a comma for a dramatic pause. Flat, long sentences sound flat with any voice.

### 6. Render + QA
`python3 scripts/render.py <short_dir>`: builds props (syncs list items, VS cards and props to the words that
mention them, places sound effects, adds music), renders with Remotion (~30-60 s), normalises to -14 LUFS, and
writes `qa.jpg`. **Read `qa.jpg`** and check every scene against the script: text cut off, overlaps, captions
clashing with visuals, wrong emoji, a character facing the wrong way. Fix and re-render until clean. To check a
moment precisely: `ffmpeg -ss <sec> -i <mp4> -frames:v 1 /tmp/x.png` and Read it.

### 7. Upload pack
Write `<short_dir>/upload.md` (3 titles, description with source, hashtags, pinned comment, cover frame, posting
notes) following `references/ideas-and-upload.md`, and append the short to `history.md`.

Finish by telling the user: where the MP4 is, its length, the recommended title, and one thing to watch in
analytics ("if Viewed vs swiped away is under ~60% after a day, we rewrite the hook").

## Running on claude.ai (web / desktop chat) instead of Claude Code
claude.ai runs the skill in a Linux sandbox that starts empty in every chat and **kills any single command that
runs longer than a few minutes**. Setup and rendering take longer than that, so on claude.ai always run them as
background jobs with `scripts/job.sh` and poll. Never run setup.sh, voice.py or render.py directly there.
Always call scripts by their absolute path inside this skill folder (e.g. `/mnt/skills/user/saadai-labs-shorts-studio/scripts/job.sh`).
(You are on claude.ai if `/mnt/user-data` exists or `uname` says Linux and `~/.shorts-studio/engine` is missing.)

1. **First message of the chat:** start setup immediately, then do the creative work while it installs:
   `bash scripts/job.sh start setup bash scripts/setup.sh`
   Write the hooks, script and short.json meanwhile. Work in `/home/claude/shorts/<channel>/` (or the cwd).
2. Before the storyboard: `bash scripts/job.sh wait setup 150`. Repeat the same command while it says `running`
   (setup takes ~3-6 min). If it says `failed`, read the log lines it prints: a network/403/timeout error means
   code execution has no internet; tell the user to allow network access for code execution in claude.ai
   Settings → Capabilities, then start a new chat. Still deliver the hooks, script and upload pack.
3. Storyboard (step 4) runs directly (it's quick): `python3 scripts/build.py <dir> --draft && python3 scripts/storyboard.py <dir>`.
   If it takes over ~2 min, run it as a job too (`job.sh start story bash -c "..."`).
4. After approval, voice + render as one job:
   `bash scripts/job.sh start render bash -c "python3 scripts/voice.py <dir> && python3 scripts/render.py <dir>"`
   then `bash scripts/job.sh wait render 150`, repeated until `done` (2-6 min). Tell the user it's rendering.
5. render.py copies the MP4 to `/mnt/user-data/outputs/` automatically. Also copy `qa.jpg`, `upload.md` and
   `channel.json` there, check qa.jpg, and present **the MP4 first** as the main file.
6. Notes: whisper usually isn't installed, so word timing is estimated (close, not exact). Save `channel.json`
   to outputs every time: the user uploads it in the next chat to restore the channel's look and voice.

## Changing an existing short
"Make the hook punchier" / "change scene 3" → edit only those scenes in short.json → `voice.py` (re-voices only
changed scenes) → `render.py`. "Different colours / voice / music" → edit channel.json (or override in short.json).

## Batches ("make 5 shorts", "a week of content")
Run Idea mode, get the user to approve the list, then for each short do steps 3-7. Show all storyboards together
in one approval message. Vary formats, scene mixes and backgrounds across the batch; identical-looking videos are
what YouTube's inauthentic-content policy demonetises (see references/ideas-and-upload.md).

## Rules
- Original scripts only. Never copy another creator's script, characters, or channel identity, even if asked
  to "recreate" a video: copy the structure and explain why.
- No real people as characters except clearly historical figures in history stories; never living private people.
- No medical, legal or financial advice as fact. Tips are fine with "check with a pro" in the description.
- Keep the creator in the loop: storyboard approval before voicing, always.
- If something fails, show the error line and fix it; don't hand over a video you haven't looked at.
