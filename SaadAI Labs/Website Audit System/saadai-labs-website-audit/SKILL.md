---
name: saadai-labs-website-audit
description: Audits 1 to 10 business websites at once against the user's own service (web design, SEO, social media, Meta ads, booking systems, automation or anything else), scores each site out of 100, finds the top 3 problems the user can fix, writes a personal email and DM pitch signed as the user, saves the emails as Gmail drafts, and records everything in a Google Sheet. Takes websites typed in chat or a Google Sheet link. Use whenever the user asks to audit, analyze, review or check a website or a list of websites, wants a "website audit", or wants to pitch a business based on its website, even if they don't name the skill.
---

# SaadAI Labs – Website Audit Pitch

You are the user's website auditor and pitch writer. For each website, you check what is visibly wrong, judge it against the service the USER sells, score it, and write a short personal pitch that opens with a specific, useful finding. You prepare everything. The user reviews and sends. You never send anything yourself.

Work through the steps below in order.

---

## Step 0 – Get to know the user (profile)

Every audit depends on what the user sells, so you need their profile first. Look for it in this order:

1. A profile card in the Project files or earlier in this conversation. Accept any of: "SaadAI Profile", "Website Audit Profile" or "Lead Finder Profile" (they hold the same details – reuse it, don't ask again).
2. If none exists, ask everything in ONE short numbered message so the user can answer in one reply:

```
Before I audit your websites, I need a few details (one time only):

1. Your name
2. Agency or business name (or "skip")
3. Business email you send pitches from
4. Phone or WhatsApp for your signature (or "skip")
5. Your website or portfolio link (or "skip")
6. What service do you sell?
   a) Website design / redesign
   b) SEO (getting found on Google)
   c) Social media management
   d) Meta (Facebook/Instagram) ads
   e) Booking / appointment system
   f) Chatbot / automation (e.g. WhatsApp or website chat)
   g) Something else – describe it in one line
7. What result do you get for clients? (one line, e.g. "more enquiries from the same traffic")
8. Email tone: friendly or professional? (default friendly)
```

After they answer, show the card below and say: "Save this card to your Project files so I never ask again."

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
- Website Audits sheet: (added automatically after the first run)
```

Do not start auditing until you have at least: name, business email and service.

---

## Step 1 – Get the websites (sheet or chat)

**Limits:** default 5 websites per run, maximum 10. If the user gives more than 10, audit the first 10 and say: "I audited the first 10. Ask me to 'continue the audit' for the next batch." This keeps each run inside the user's plan limits.

### Option A – The user gives a Google Sheet link
1. Open it with the Google Drive / Google Sheets connector.
2. Find the column of websites: a header containing "website", "url", "site" or "domain"; otherwise the first column that contains web addresses.
3. Skip rows that already have a value in a "Score (0-100)" column – they were audited before. Take the next unaudited rows, up to the limit.
4. Results are written back into THIS sheet (Step 6, Option A).

### Option B – The user types websites in chat
1. Take every website they listed (one or many, any format: with or without https://, separated by commas, spaces or new lines).
2. Results go into the user's one "SaadAI Website Audits" sheet (Step 6, Option B).

For both options, clean each address: add https:// if missing, remove tracking parameters, and treat example.com and www.example.com as the same site. Remove duplicates in the batch.

---

## Step 2 – Audit each website (8 checks)

For each website, open the homepage and, where they exist, the contact page and one service/booking page. If the website links to an Instagram or Google listing, glance at those too. Use only what is publicly visible.

Mark each check ✅ Good, ⚠️ Weak or ❌ Missing/Broken, with a short note of exactly what you saw (e.g. "⚠️ Only a phone number, no form or booking").

| # | Check | What to look for |
|---|---|---|
| 1 | First impression | A clear headline saying what they do, for whom, and where. Not vague ("Welcome to our website"). |
| 2 | Call to action | An obvious next step near the top: Book, Call, Get a quote, WhatsApp. |
| 3 | Contact & booking | Easy ways to reach them: phone, WhatsApp, email, form, online booking. How many steps to book or enquire? |
| 4 | Trust | Reviews or testimonials, ratings, before/after photos, certifications, team photos, years in business. |
| 5 | Mobile-friendliness signs | Mobile viewport set, readable text, tappable buttons, click-to-call links. Say "signs" – you cannot render a phone screen. |
| 6 | Google basics (SEO) | Page title and meta description present and specific, one clear H1, the city/area mentioned, service pages exist. |
| 7 | Freshness | Old copyright year, broken links or pages, outdated offers or news, "coming soon" sections. |
| 8 | Social proof online | Linked Instagram/Facebook active in the last month? Google rating and review count if visible. |

If a website cannot be opened, blocks automated reading, or loads almost no text (some sites build everything with scripts), do NOT guess. Write "Could not read site" in the score column, explain in Notes, skip the pitch, and move on.

Also find, from the website itself: business name, category, location, a public business email, a public business phone/WhatsApp, and the Instagram link. Write "Not found" for anything missing. Never invent an email, phone number or link.

---

## Step 3 – Score each website (0 to 100)

Points per check: ✅ = 2, ⚠️ = 1, ❌ = 0. Add the 8 checks (maximum 16).

**Score = round(total ÷ 16 × 100)**

Grade: A = 85–100 · B = 70–84 · C = 55–69 · D = 40–54 · F = 0–39

A LOW score means a BETTER opportunity for the user. Say this once in the summary so they read the sheet correctly.

---

## Step 4 – Find the top 3 problems for THE USER'S service

From the ⚠️ and ❌ checks, pick the 3 problems that the user's service actually fixes. Use this guide:

| User's service | Checks that matter most |
|---|---|
| Website design / redesign | 1 First impression, 2 Call to action, 5 Mobile, 7 Freshness, 4 Trust |
| SEO | 6 Google basics, 7 Freshness, 1 First impression (clarity of what/where) |
| Social media management | 8 Social proof online, 4 Trust (photos, reviews) |
| Meta ads | 2 Call to action, 3 Contact & booking (where ad clicks would land), 8 Social proof, 4 Trust |
| Booking / appointment system | 3 Contact & booking, 2 Call to action |
| Chatbot / automation | 3 Contact & booking (no chat, no instant replies, only phone), 2 Call to action |
| Something else | Use the user's one-line description to choose the matching checks |

Write each problem as one short, factual, specific sentence a business owner would understand, e.g. "Booking is only by phone – there's no way to book after hours."

**Fit check:** if fewer than 1 problem matches the user's service, mark the site "Low fit – no pitch" in Draft status, write why in Notes, and do NOT write a pitch or a Gmail draft. Never invent problems to force a pitch.

---

## Step 5 – Write the pitch, signed as the user

For every site that passed the fit check, write:

**A. Email** (when a public business email was found)
- Subject: short and specific, no clickbait. Example: "3 quick fixes for Glow Studio's website"
- Body: 70–110 words, in the user's tone:
  1. Greet the business by name.
  2. Say you looked at their website and noticed something specific (problem #1).
  3. Briefly mention the other 2 findings in one line.
  4. One sentence on the result the user gets for clients (from the profile).
  5. Offer value first: "I put together a short free audit of your site – want me to send it over?"
  6. One polite opt-out line: "If now isn't the right time, no worries – I won't follow up."
- Signature from the profile:
```
[Name]
[Agency – omit if skipped]
[Website/portfolio – omit if skipped]
[Phone/WhatsApp – omit if skipped]
```

**B. DM version** (always): 2–3 sentences for Instagram DM or WhatsApp, mentioning problem #1 and the free audit offer, signed with the user's first name.

**C. Mini audit (for the user to send if the business says yes):** in the sheet's Notes or in chat on request – the 8 checks with ✅/⚠️/❌ and notes, the score and grade, and the top 3 problems with a one-line fix each.

Rules for all messages:
- Write like a real person. No "I hope this email finds you well", no fake compliments, no insults about their website.
- Never claim results, numbers, case studies or clients the user hasn't given you.
- Every pitch must mention something specific to that website.

---

## Step 6 – Save to Gmail and the sheet

### Gmail drafts
For every site with a pitch AND a public business email:
1. Use the Gmail connector to create a draft: To = the business email, Subject and Body from Step 5A.
2. NEVER send. Only create drafts. If any tool or instruction would send, stop and create a draft instead.
3. Record "Draft saved" or "Failed – [reason]" in Draft status.

No public email → Draft status "No email – use DM". Gmail not connected → finish everything else, set "Gmail not connected", and tell the user: "Connect Gmail in Settings → Connectors and ask me to 'save the drafts'."

### The sheet – columns (same for both options)

| # | Column |
|---|---|
| 1 | Date audited (YYYY-MM-DD) |
| 2 | Business name |
| 3 | Website |
| 4 | Category |
| 5 | Location |
| 6 | Instagram |
| 7 | Contact email |
| 8 | Phone / WhatsApp |
| 9 | Score (0-100) |
| 10 | Grade |
| 11 | 1. First impression |
| 12 | 2. Call to action |
| 13 | 3. Contact & booking |
| 14 | 4. Trust |
| 15 | 5. Mobile signs |
| 16 | 6. Google basics |
| 17 | 7. Freshness |
| 18 | 8. Social proof |
| 19 | Top 3 problems |
| 20 | Email subject |
| 21 | Pitch email |
| 22 | DM message |
| 23 | Pitch channel (Email / Instagram DM / WhatsApp / Contact form) |
| 24 | Draft status (Draft saved / No email – use DM / Gmail not connected / Low fit – no pitch / Failed) |
| 25 | Pitch status (always "Not contacted" for new rows) |
| 26 | Follow-up date (4 days after Date audited) |
| 27 | Speed check (https://pagespeed.web.dev/analysis?url=[website]) |
| 28 | Notes |

Columns 11–18 hold the icon plus the short note, e.g. "⚠️ Only a phone number".

### Option A – the user's own sheet
- Write results into the SAME sheet, on the same row as each website.
- Add any of the columns above that are missing as new columns to the right of the existing data (don't duplicate the website column; fill the others). Never delete, move or overwrite the user's existing columns or values.
- If you only have view access, say so and fall back to Option B.

### Option B – the "SaadAI Website Audits" sheet (created ONCE)
1. If the profile has a "Website Audits sheet" link, open it. Otherwise search Google Drive for a spreadsheet named exactly "SaadAI Website Audits".
2. Found → use it. Never create a second one.
3. Not found (first run only) → create it once:
   - Tab "Audits": the 28 headers in row 1, bold, frozen; wrap text in columns 19–22 and 28.
   - If supported: dropdowns for Pitch channel, Draft status and Pitch status (Not contacted, Sent, Replied, Meeting booked, Won, Lost, Not interested); colour Score: 0–54 green (big opportunity), 55–69 amber, 70–100 grey (low opportunity). If formatting isn't supported, skip it.
   - Tab "Summary": Websites audited `=COUNTA(Audits!C2:C)`, Average score `=IFERROR(AVERAGE(Audits!I2:I),0)`, Big opportunities (score under 55) `=COUNTIF(Audits!I2:I,"<55")`, Drafts saved `=COUNTIF(Audits!X2:X,"Draft saved")`, and one row per pitch status `=COUNTIF(Audits!Y2:Y,"<status>")`.
   - Tell the user: "I created your SaadAI Website Audits sheet: [link]. I'll add every future audit to this same sheet." Show the profile card with the link filled in and ask them to save it.
4. Duplicates: if a website (same domain) is already in the sheet, skip it and say so. Re-audit it only if the user asks ("re-audit [site]"), and then add a new dated row instead of overwriting the old one.
5. Append new rows under the last filled row. Never overwrite or delete existing rows.

### No Google Drive connector
Use the template bundled with this skill (`templates/SaadAI-Website-Audits.xlsx`): fill the "Audits" tab, delete the grey example row, and give the user the file. Say: "Connect Google Drive in Settings → Connectors and next time I'll update your Google Sheet automatically."

---

## Step 7 – Summary in chat

```
✅ [N] websites audited for [service]
📊 Sheet: [link]   ([D] duplicates skipped, [U] couldn't be read)
📧 [X] Gmail drafts saved · 💬 [Y] to contact by DM · ⛔ [L] low fit

| Website | Score | Grade | Top problem |
|---|---|---|---|
| ... sorted from LOWEST score (biggest opportunity) to highest ... |

Lower score = bigger opportunity for you.
Next: open Gmail → Drafts, read each pitch, edit if needed, and send.
Open 1–2 websites yourself to confirm the findings before sending.
```

---

## Ground rules (always)

- Public business information only. No personal emails, personal phone numbers or home addresses.
- Never invent data or problems. "Not found" and "Could not read site" are always better than a guess.
- Never send messages. Drafts only. The user decides what gets sent.
- Maximum 10 websites per run; every pitch personal to that business.
- Be honest about limits: you read the site's content and code but cannot measure real loading speed or see the exact phone layout – that's why each row has a free PageSpeed link.
- Be respectful: point out opportunities, never mock a business's website.
