# YouTube Shorts Studio – Faceless Animated Shorts with Claude (No Editing Tools)

A free Claude skill by **SaadAI Labs**. Give it one line ("Make a Short about why we yawn") and it creates a complete 2D animated YouTube Short: script, voiceover, captions, sound effects, music and the final MP4. Works for YouTube Shorts, TikTok and Reels.

No Higgsfield, no CapCut, no paid voice tool. Just a Claude Pro account.

---

## What it does

Type:

> /saadai-labs-shorts-studio Make a YouTube Short about why we yawn, 20 to 30 seconds

Shorts Studio then:

1. **Researches ideas** (optional): give it a niche and it finds 10 video ideas, each with a hook and a score out of 20. It marks the top 3 and suggests series.
2. **Writes 3 hooks** and scores them, because the first 2 seconds decide if people swipe.
3. **Writes the script** in one of 4 formats: explainer, cartoon story, myth vs fact, or top 3 ranking. It checks facts on the web and keeps the source.
4. **Shows you a storyboard** for approval. Nothing is voiced or rendered until you say "approve".
5. **Voices it** with a realistic male narrator (free Kokoro voice, or ElevenLabs if you have a key).
6. **Animates it** in Remotion: 2D characters, emoji, stat counters, lists, VS cards and word-by-word captions, plus sound effects and music.
7. **Checks every scene** itself, fixes problems and re-renders.
8. **Gives you the upload pack:** 3 titles, a description with sources, hashtags, a pinned comment and the best cover frame.

It also **remembers your channel**: colours, voice, characters and every topic you've already made, so it never repeats one. Send it a character or brand image and it matches your look.

---

## What's in this folder

| File | What it is |
|---|---|
| `saadai-labs-shorts-studio.zip` | The skill, ready to upload to Claude |
| `saadai-labs-shorts-studio/SKILL.md` | The skill's instructions |
| `saadai-labs-shorts-studio/references/` | Hook formulas, file formats, idea mode and upload guide |
| `saadai-labs-shorts-studio/scripts/` | Setup, voice, storyboard and render scripts |
| `saadai-labs-shorts-studio/engine/` | The Remotion animation engine, sound effects and font |
| `saadai-labs-shorts-studio/examples/` | A sample channel and two complete sample Shorts |

---

## Setup (5 minutes)

1. **Download** `saadai-labs-shorts-studio.zip`.
2. **Upload:** Settings → Capabilities → Skills → upload the zip.
3. **Turn on code execution with network access** in Settings → Capabilities. The skill installs its animation engine and voice in Claude's sandbox at the start of each chat (about 3–6 minutes).
4. **Run it** in a new chat: `/saadai-labs-shorts-studio Make a Short about <your topic>`
5. **Save `channel.json`** when it gives it to you, and upload it in your next chat to keep the same look and voice.

---

## Auto-post to YouTube (free)

1. Make a Google Drive folder called **Ready to Post** and save your finished Shorts there.
2. In Zapier, make a Zap: **Google Drive "New File in Folder" → YouTube "Upload Video"**. Map the file name as the title.
3. Publish the Zap. (Tests inside the Zap editor don't show up on your channel. That's normal.)

One upload uses one Zapier task, so daily posting fits in Zapier's free plan.

---

## Tips

- **Quality beats volume.** YouTube demonetises channels full of near-identical, mass-produced videos. The skill varies formats and styles for you; 1–3 good Shorts a day beats 10 rushed ones.
- **Watch "Viewed vs swiped away"** in YouTube Studio. Under ~60% after a day means the hook failed: ask the skill to rewrite scene 1 only.
- **Use your own character or colours** so your channel looks like a brand, not random AI clips.

---

## Rules this skill follows

- Original scripts only. It copies the structure of a reference video, never its script or characters.
- No living private people as characters, and no medical, legal or financial advice as fact.
- You approve every storyboard before anything is voiced or rendered.
- Every sound effect is CC0 (free for commercial use). See `engine/public/sfx/CREDITS.md`.

---

Made by **SaadAI Labs**. More free AI systems for businesses are coming to this repo every week.
