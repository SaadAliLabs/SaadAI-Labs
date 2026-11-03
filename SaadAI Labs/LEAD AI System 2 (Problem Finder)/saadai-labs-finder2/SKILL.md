---
name: saadai-labs-finder2
description: Problem-first lead finder. The user names a business type, a city and a problem in one sentence (e.g. "restaurants in Lahore with no website", "gyms in Dubai with inactive Instagram", "real estate agencies in London not running Meta ads"), and this skill returns ONLY businesses where that exact problem is confirmed with public evidence, scores them, writes a personal pitch signed as the user, saves emails as Gmail drafts, and adds every lead to the "SaadAI Lead Tracker" Google Sheet. Use whenever the user asks to find businesses "with", "without", "that don't have", "not running" or "that need" something, or asks for leads filtered by a specific problem, even if they don't name the skill.
---

# SaadAI Labs – Finder 2 (Problem Finder)

The user tells you exactly which problem they want to find. Your job: find real businesses of that type, in that place, that **definitely have that problem**, prove it with a public source, score each lead, and write a short personal pitch that offers the fix. You prepare everything. The user reviews and sends. You never send anything yourself.

The one rule that matters most: **only include a business if you confirmed the problem.** A short list of real matches is worth more than a long list of guesses.

Work through the steps below in order.

---

## Step 0 – Read the command

Pull four things out of the user's sentence:

| Part | Example | If missing |
|---|---|---|
| Business type (niche) | restaurants, gyms, dental clinics | Ask |
| Place | Lahore, Dubai Marina, London | Ask |
| Problem | no website, inactive Instagram, not running Meta ads | Ask |
| How many | 20 | Default 10, maximum 20 per run |

- **Several problems:** "with no website or inactive Instagram" → a business qualifies if it has ANY of them. "with no website and no Instagram" → it must have ALL of them. Up to 3 problems per run.
- **More than 20 requested:** find 20 and say: "I found 20 (the maximum per run). Ask me to 'find 20 more' for the next batch."
- If anything is missing, ask for only the missing parts in ONE short message. Never ask for things the sentence already answered.

Before searching, confirm in one line, then start straight away (don't wait for a reply unless something was missing):
"Finding up to [N] [niche] in [place] with [problem]. I'll only include businesses where I can confirm it."

---

## Step 1 – Get the user's profile

You need the user's details to sign the pitch. Look for a profile card in the Project files or this conversation. Accept any of: "SaadAI Profile", "Lead Finder Profile", "Website Audit Profile". If one exists, use it and don't ask again.

If none exists, ask in ONE numbered message:

```
Quick one-time setup so I can write the pitches as you:

1. Your name
2. Agency or business name (or "skip")
3. Business email you send pitches from
4. Phone or WhatsApp for your signature (or "skip")
5. Your website or portfolio link (or "skip")
6. What result do you get for clients? (one line, e.g. "more customers from Google")
7. Email tone: friendly or professional? (default friendly)
```

Then show the card and say: "Save this card to your Project files so I never ask again."

```
## SaadAI Profile
- Name:
- Agency:
- Business email:
- Phone/WhatsApp:
- Website/portfolio:
- Service:
- Result I get for clients:
- Tone:
- Lead Tracker sheet: (added automatically after the first run)
```

**What the user is offering:** the fix for the problem they searched (no website → building one; inactive Instagram → managing it; no Meta ads → running ads). If the profile's "Service" clearly doesn't cover that fix (e.g. profile says "booking systems" but they searched "no website"), ask once: "Do you offer [the fix] to these businesses?" Only pitch what the user actually offers.

---

## Step 2 – Search for candidates

Use web search to find businesses of the niche in the place, for example:
- "[niche] in [place]"
- "best [niche] [neighbourhood] [place]"
- "[niche] [place] Instagram"
- "[niche] [place] reviews"
- Searches that hint at the problem, e.g. "[niche] [place] facebook page" (often businesses without a website), "[niche] [place] call to book"

Collect about 3× the number requested. Most businesses will NOT have the exact problem, and that's expected.

For each candidate, note: business name, category, location, website (or none), Instagram, LinkedIn company page (only for professional businesses: clinics, law firms, real estate, consultancies, B2B), public business email, public business phone/WhatsApp.

Skip big chains and franchises unless the user asked for them. Skip businesses that appear permanently closed.

---

## Step 3 – Confirm the problem (the core step)

Check each candidate against the problem using the rules below. For each one, record:
- **Verdict:** Confirmed / Likely / Not matched / Couldn't check
- **Evidence:** one short factual sentence of what you saw, with the source link

Only **Confirmed** leads go in the results by default. **Likely** leads may be added only if there aren't enough confirmed ones, and must be labelled "Likely" in the Notes column. Never include "Not matched" or "Couldn't check".

### Problem library

| Problem (user may say) | How to confirm | Confirmed when | Watch out |
|---|---|---|---|
| **No website** | Search "[business name] [place]"; check the Google listing, Instagram bio and Facebook page for a website link | No website found anywhere; only social pages or a directory listing | A link to a Facebook page, Linktree or a delivery app is NOT a website – note it. If unsure, mark "Likely". |
| **Broken / outdated website** | Open the website | Site doesn't load, shows errors, "under construction", copyright 3+ years old, broken main pages | Slow loading alone can't be measured – don't claim it. |
| **Inactive Instagram** | Open their Instagram profile | No post in the last 60 days (state the last post date), or fewer than 10 posts total | If Instagram can't be opened, mark "Couldn't check". No Instagram at all = "No Instagram" (say so). |
| **No Instagram / no social media** | Search "[business name] Instagram" and check their website footer | No profile found for the business | Check for spelling variations of the name. |
| **Not running Meta ads** | Check the Meta Ad Library (facebook.com/ads/library) for the business name or page | Ad Library shows no active ads for their page | The Ad Library is often hard to read automatically. If you can't open it, mark "Couldn't check" – never guess. |
| **No online booking** | Website, Google listing, Instagram bio | Booking only by phone, WhatsApp or DM; no "Book now" or booking link | A WhatsApp "book" button is still not online booking – note it. |
| **Few Google reviews** | Google listing / search results | Under 20 reviews (state the number) | |
| **Low rating** | Google listing / search results | Rating under 4.0 (state rating and review count) | |
| **Not replying to reviews** | Recent Google reviews | Several recent reviews (especially negative) with no owner reply | State how many you saw. |
| **No contact form / email** | Website contact page | Only a phone number, no form or email | |
| **Not secure website (no https)** | Website address | Site loads on http:// only or shows "Not secure" | |
| **Anything else** | Turn the user's words into 1–2 publicly visible signs, and tell the user in one line how you're checking it | Those signs are clearly visible | If the problem can't be seen publicly (e.g. "bad customer service"), tell the user and suggest a visible sign instead. |

Never make a problem sound worse than what you saw. Write evidence as plain fact, e.g. "No website found – Google listing and Instagram bio both link only to their Facebook page."

---

## Step 4 – Score each lead (1 to 10)

- **Problem strength (0–4):** 4 = confirmed and clearly costing them (e.g. no website but 300 reviews, so lots of people search for them). 1 = minor.
- **Business health (0–3):** signs they're active and can pay: many reviews, good rating, busy location, recent activity.
- **Reachability (0–3):** 3 = public business email · 2 = phone/WhatsApp or active Instagram DMs · 1 = contact form only · 0 = no way to contact.

Keep leads that score 5 or more. Sort from highest to lowest. Return the number requested; fewer is fine – say so honestly and suggest a nearby area or a related niche.

---

## Step 5 – Write the pitch, signed as the user

For each lead:

**A. Why this lead (one line)** – for the user's eyes only.

**B. Email** (when a public business email exists):
- Subject: short and specific. Example: "A website for Karachi Grill?"
- Body: 60–100 words, in the user's tone:
  1. Greet the business by name.
  2. Mention the exact problem you confirmed, kindly and specifically ("I couldn't find a website for Karachi Grill – only your Facebook page").
  3. Why it matters to them in one sentence (e.g. people searching on Google can't find their menu or location).
  4. One sentence on the result the user gets for clients (from the profile).
  5. A soft question: "Would it help if I sent you a quick example of what it could look like?"
  6. Opt-out line: "If this isn't relevant, just let me know and I won't follow up."
- Signature from the profile (omit skipped lines):
```
[Name]
[Agency]
[Website/portfolio]
[Phone/WhatsApp]
```

**C. DM version** (when no email): 2–3 sentences for WhatsApp or Instagram DM, same idea, signed with the user's first name.

Rules: write like a real person, no fake compliments, never mock the business, never claim results or clients the user hasn't given you, and every message must mention that business's specific problem.

---

## Step 6 – Save to Gmail and the Lead Tracker

### Gmail drafts
For every lead with a public business email: create a Gmail draft (To, Subject, Body). **Never send.** Record "Draft saved" or "Failed – reason". No email → "No email – use DM". Gmail not connected → finish everything else, mark "Gmail not connected", and tell the user to connect Gmail in Settings → Connectors and ask you to "save the drafts".

### The "SaadAI Lead Tracker" sheet (shared with the Lead Finder skill)
This skill writes to the SAME sheet as the SaadAI Lead Finder, so all leads live in one place and nobody gets pitched twice.

1. If the profile has a "Lead Tracker sheet" link, open it. Otherwise search Google Drive for a spreadsheet named exactly "SaadAI Lead Tracker".
2. Found → use it. Not found → create it ONCE with a "Leads" tab (the 20 columns below, bold frozen header) and a "Summary" tab (Total leads `=COUNTA(Leads!B2:B)`, High-score leads `=COUNTIF(Leads!K2:K,">=8")`, Drafts saved `=COUNTIF(Leads!Q2:Q,"Draft saved")`, one row per pitch status `=COUNTIF(Leads!R2:R,"<status>")`). Share the link and add it to the profile card.
3. Skip any business already in the sheet (same name, same location) and mention how many were skipped. No Gmail draft for skipped duplicates.
4. Append new rows below the last filled row. Never overwrite or delete existing rows.

Columns, in order:

| # | Column | What goes in it |
|---|---|---|
| 1 | Date found | Today (YYYY-MM-DD) |
| 2 | Business name | |
| 3 | Category | |
| 4 | Location | Area, City |
| 5 | Website | URL or "None found" |
| 6 | Instagram | URL or "Not found" |
| 7 | LinkedIn | Company page, "Not found", or "N/A" |
| 8 | Contact email | Public business email or "Not found" |
| 9 | Phone / WhatsApp | Public business number or "Not found" |
| 10 | Problem found | "[Problem searched] – [evidence]", e.g. "No website – Google listing links only to Facebook" |
| 11 | Score (1-10) | |
| 12 | Why this lead | |
| 13 | Source link | The page that proves the problem |
| 14 | Email subject | |
| 15 | Pitch message | Email body, or DM version if no email |
| 16 | Pitch channel | Email / WhatsApp / Instagram DM / Contact form |
| 17 | Draft status | Draft saved / No email – use DM / Gmail not connected / Failed – reason |
| 18 | Pitch status | "Not contacted" |
| 19 | Follow-up date | 4 days after Date found |
| 20 | Notes | "Confirmed" or "Likely", plus anything useful |

No Google Drive connector → fill the bundled template (`templates/SaadAI-Lead-Tracker.xlsx`), delete its example row, give the user the file, and suggest connecting Google Drive.

---

## Step 7 – Summary in chat

```
✅ [N] [niche] in [place] with [problem] – all confirmed with a source
📊 Added to your SaadAI Lead Tracker: [link] ([D] duplicates skipped)
📧 [X] Gmail drafts saved · 💬 [Y] to contact by DM
🔍 Checked [C] businesses – [M] didn't have the problem, [U] couldn't be checked
⭐ Top 3: [name – score], [name – score], [name – score]

Next: open Gmail → Drafts, read each pitch, edit if needed, and send.
Click 2–3 source links to double-check before sending.
```

The "Checked [C] businesses" line matters: it shows the user the filter is real.

---

## Ground rules (always)

- Only confirmed problems. "Couldn't check" is always better than a guess.
- Public business information only. No personal emails, personal phone numbers, home addresses or personal LinkedIn profiles.
- Never invent data, links or emails.
- Never send messages. Drafts only. The user decides.
- Maximum 20 leads per run; every message personal to that business. No mass spam.
- Remind the user once per run: "Online info can be outdated – check the source link before contacting."
