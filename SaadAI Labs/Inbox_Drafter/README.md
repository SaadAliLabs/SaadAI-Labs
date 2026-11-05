# Inbox_Drafter – Your Free AI Email Assistant in Claude (No Code)

A free Claude skill by **SaadAI Labs**. It reads your new Gmail emails, sorts them, and writes reply drafts **in your own writing style**. You just review and hit send.

Works on the regular claude.ai app (Pro plan). No coding needed.

---

## What it does

Type:

> Check my inbox

Inbox_Drafter then:

1. **Learns your tone** (first run only): reads your recent sent emails and builds a Tone Guide: your greeting, length, style and sign-off.
2. **Reads your new emails:** up to 25 per run.
3. **Sorts them:**
   - ✅ **Reply:** clients, enquiries, leads, meeting requests
   - ⚠️ **Needs you:** money, complaints, contracts (careful draft, flagged for you)
   - 🚫 **Skip:** newsletters, receipts, notifications
4. **Writes drafts in your tone**, in the sender's language (English, Urdu or Roman Urdu), using your prices and FAQs.
5. **Suggests meeting times** from your Google Calendar when someone wants to meet. It never books anything itself.
6. **Marks leads as "Replied"** in your SaadAI Lead Tracker sheet, if you use the SaadAI Lead Finder skills.
7. **Gives you a summary:** what it drafted, what needs you, and what it skipped.

It **never sends, deletes or forwards** anything. Drafts only.

---

## What's in this folder

| File | What it is |
|---|---|
| `Inbox_Drafter.zip` | The skill, ready to upload to Claude |
| `Inbox_Drafter/SKILL.md` | The skill's instructions |
| `Inbox_Drafter/templates/tone-guide.md` | Your writing style card (built for you on the first run) |
| `Inbox_Drafter/templates/business-info.md` | Your prices, hours and FAQs card |
| `Inbox_Drafter/templates/my-profile.md` | Your profile card (shared with the other SaadAI skills) |

---

## Setup (5 minutes)

1. **Download** `Inbox_Drafter.zip`.
2. **Upload:** Settings → Capabilities → Skills → upload the zip.
3. **Connect** Gmail in Settings → Connectors. Optional: Google Calendar (meeting times) and Google Drive (Lead Tracker).
4. **Run it** in a new chat inside a Claude Project: `Check my inbox`
5. **Save the cards** it creates (Tone Guide and Business Info) to your Project files, so it never asks again.

Then open **Gmail → Drafts**, read each reply, edit if needed, and send.

---

## Tips

- **Edit your Tone Guide** if something sounds off. Every future draft follows it.
- **Fill in Business Info properly.** The more prices and FAQs it knows, the fewer placeholders like `[confirm price]` you'll see.
- **Want it to run automatically?** If your Claude plan supports scheduled tasks, ask Claude to run "check my inbox" every day at 8 AM and 8 PM.

---

## Rules this skill follows

- Drafts only. It never sends, deletes, forwards or archives.
- Never invents prices, dates or promises. It uses placeholders instead.
- Treats emails as information, not instructions, and flags suspicious ones.
- Calendar: suggests times only, never books.

---

Made by **SaadAI Labs**. More free AI systems for businesses are coming to this repo every week.
