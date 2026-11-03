# LEAD AI System 2 – Find Businesses With a Specific Problem (No Code)

A free Claude skill by **SaadAI Labs**. Tell Claude the exact problem you fix, and it finds businesses that **actually have it**, with proof, then writes your pitch and saves it in Gmail.

Works on the regular claude.ai app (Pro plan). No coding needed.

---

## What it does

Type one sentence, like:

> Find 20 restaurants in Lahore with no website

> Find 15 gyms in Dubai with inactive Instagram

> Find 10 real estate agencies in London not running Meta ads

The skill then:

1. **Reads your sentence:** business type, place, problem and how many.
2. **Searches** for businesses of that type in that place.
3. **Confirms the problem for each one** and only keeps businesses where it found public proof (with a source link).
4. **Scores** each lead from 1 to 10.
5. **Writes** a personal email (and a DM version) that mentions their exact problem, signed with your name.
6. **Saves** the emails as Gmail drafts. It never sends anything.
7. **Adds** every lead to your "SaadAI Lead Tracker" Google Sheet, the same sheet the original Lead Finder uses, so you never pitch the same business twice.

---

## Problems it can find

| Problem | How it's checked |
|---|---|
| No website | Google listing, Instagram bio and Facebook show no website |
| Broken / outdated website | Site errors, "under construction", very old copyright |
| Inactive Instagram | No post in the last 60 days |
| No Instagram / social media | No profile found |
| Not running Meta ads | Meta Ad Library shows no active ads |
| No online booking | Phone, WhatsApp or DM only |
| Few Google reviews | Under 20 reviews |
| Low rating | Under 4.0 stars |
| Not replying to reviews | Recent reviews with no owner reply |
| No contact form / email | Phone number only |
| Not secure website | No https |
| Anything else | Describe it, and Claude turns it into a visible sign to check |

If Claude can't verify a problem (for example, the Ad Library won't load), it marks the business "Couldn't check" and leaves it out. It never guesses.

---

## What's in this folder

| File | What it is |
|---|---|
| `saadai-labs-finder2.zip` | The skill, ready to upload to Claude |
| `saadai-labs-finder2/SKILL.md` | The skill's instructions |
| `saadai-labs-finder2/templates/my-profile.md` | Fill-in profile card (shared with the other SaadAI skills) |
| `saadai-labs-finder2/templates/SaadAI-Lead-Tracker.xlsx` | Formatted lead tracker (used if Google Drive isn't connected) |

---

## Setup (5 minutes)

1. **Download** `saadai-labs-finder2.zip`.
2. **Upload:** Settings → Capabilities → Skills → upload the zip.
3. **Connect** Gmail and Google Drive in Settings → Connectors.
4. **Run it** in a new chat: `Find 10 [business type] in [city] with [problem]`
5. Answer the one-time setup questions and save the profile card to your Project.

Then open **Gmail → Drafts**, check each pitch, and send it yourself.

---

## Tips

- **Be specific.** "Restaurants in Gulberg, Lahore with no website" works better than "businesses in Pakistan".
- **Expect fewer results than you asked for** on strict problems. The skill only keeps confirmed matches, and it tells you how many businesses it checked.
- **Click 2–3 source links** before sending. Online info can be outdated.

---

## Rules this skill follows

- Only confirmed problems, each with a source link.
- Public business information only.
- Never sends messages. Drafts only.
- Maximum 20 leads per run, every message personal. No spam.

---

Made by **SaadAI Labs**. More free AI systems for businesses are coming to this repo every week.
