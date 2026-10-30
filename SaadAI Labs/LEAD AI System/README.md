# LEAD AI System – Find Clients With Claude (No Code)

A free Claude skill by **SaadAI Labs** that finds qualified local business leads for your service, writes a personal email pitch for each one, saves the pitches as Gmail drafts, and keeps every lead in one Google Sheet.

Works on the regular claude.ai app (Pro plan). No coding needed.

---

## What it does

You type one sentence, like:

> Find 10 hair salons in Dubai that need online booking.

The skill then:

1. **Asks about you** (first run only): your name, agency, email, the service you sell, and your target niche and city.
2. **Searches** the web for matching businesses.
3. **Checks** each one for the problem your service fixes (no online booking, no website, inactive Instagram, no Meta ads, or your own).
4. **Scores** each lead from 1 to 10.
5. **Writes** a short, personal email pitch signed with your name.
6. **Saves** each pitch as a draft in your Gmail. It never sends anything. You review and send.
7. **Adds** every lead to your "SaadAI Lead Tracker" Google Sheet. The sheet is created on the first run and updated on every run after, with duplicates skipped.

---

## What's in this folder

| File | What it is |
|---|---|
| `saadai-labs-lead-finder.zip` | The skill, ready to upload to Claude |
| `saadai-labs-lead-finder/SKILL.md` | The skill's instructions (read it to see exactly how it works) |
| `saadai-labs-lead-finder/templates/my-profile.md` | Fill-in profile card so the skill skips the setup questions |
| `saadai-labs-lead-finder/templates/SaadAI-Lead-Tracker.xlsx` | Formatted lead tracker (used if Google Drive isn't connected) |

---

## Setup (5 minutes)

1. **Download** `saadai-labs-lead-finder.zip` from this folder.
2. **Upload the skill:** in Claude, go to Settings → Capabilities → Skills, and upload the zip.
3. **Connect your apps:** Settings → Connectors → connect **Gmail** and **Google Drive**.
4. **Run it:** open a new chat (ideally inside a Claude Project) and type:
   `Find 5 [type of business] in [city] that need [your service].`
5. **Answer the setup questions**, then save the profile card Claude shows you to your Project files. Next time, it skips the questions.

Then open **Gmail → Drafts**, read each pitch, edit it, and send it yourself.

---

## Tips

- **Start small:** run 5–10 leads at a time (max 20). It's faster and uses less of your plan's limit.
- **Check before you send:** every lead has a source link. Click it to confirm the business is real and the problem is accurate. AI search can be outdated.
- **Follow up once:** the sheet sets a follow-up date 4 days after each lead is found.
- **Update the "Pitch status" column** as you go: Not contacted → Sent → Replied → Meeting booked → Won / Lost.

---

## Rules this skill follows

- Public business information only. No personal emails, personal phone numbers or personal LinkedIn profiles.
- Never invents data. Missing details are marked "Not found".
- Never sends messages. Drafts only. You stay in control.
- Every message is personal to that business. No mass spam.

---

Made by **SaadAI Labs**. More free AI systems for businesses are coming to this repo every week.
