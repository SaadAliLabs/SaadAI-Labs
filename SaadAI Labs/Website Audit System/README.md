# Website Audit System – Audit 10 Websites and Write Your Pitches With Claude (No Code)

A free Claude skill by **SaadAI Labs** for anyone who sells websites, SEO, social media, ads, booking systems or automation. Give it up to 10 business websites. It audits each one against **your** service, scores it, finds the problems you can fix, writes a personal pitch, and saves the emails as Gmail drafts.

Works on the regular claude.ai app (Pro plan). No coding needed.

---

## What it does

Type something like:

> Audit these websites: brightsmile.ae, glowstudio.ae, fitzone.ae

or share a Google Sheet with a column of websites (up to 10 per run).

The skill then:

1. **Asks about you** (first run only): name, agency, email and the service you sell.
2. **Audits each website on 8 checks:** first impression, call to action, contact & booking, trust, mobile signs, Google basics (SEO), freshness and social proof.
3. **Scores each site out of 100** (lower score = bigger opportunity for you).
4. **Picks the top 3 problems that YOUR service fixes.** A web designer and a social media manager get different problems from the same website.
5. **Writes a pitch signed as you:** an email that offers a free audit, plus a short DM version.
6. **Saves the emails as Gmail drafts.** It never sends anything. You review and send.
7. **Records everything in a Google Sheet:** your own sheet if you gave one, or a "SaadAI Website Audits" sheet it creates once and updates on every run.

---

## What's in this folder

| File | What it is |
|---|---|
| `saadai-labs-website-audit.zip` | The skill, ready to upload to Claude |
| `saadai-labs-website-audit/SKILL.md` | The skill's instructions (read it to see exactly how it works) |
| `saadai-labs-website-audit/templates/my-profile.md` | Fill-in profile card so the skill skips the setup questions |
| `saadai-labs-website-audit/templates/SaadAI-Website-Audits.xlsx` | Formatted audit sheet (used if Google Drive isn't connected) |

---

## Setup (5 minutes)

1. **Download** `saadai-labs-website-audit.zip` from this folder.
2. **Upload the skill:** in Claude, go to Settings → Capabilities → Skills, and upload the zip.
3. **Connect your apps:** Settings → Connectors → connect **Gmail** and **Google Drive**.
4. **Run it:** open a new chat (ideally inside a Claude Project) and type:
   `Audit these websites: [site 1], [site 2], [site 3]`
5. **Answer the setup questions**, then save the profile card Claude shows you to your Project files.

Then open **Gmail → Drafts**, read each pitch, edit it, and send it yourself.

Already using the **Lead Finder** skill? Both skills share the same profile card, so you only answer the questions once.

---

## Tips

- **Start with 5 websites.** The maximum is 10 per run; smaller batches are faster and use less of your plan's limit.
- **Check before you send.** Open 1–2 websites yourself to confirm the findings.
- **Use the Speed check link** in each row to test real loading speed with Google PageSpeed Insights (free). Claude reads the website's content but can't measure speed.
- **Lead with value.** The pitch offers a free audit. When they say yes, ask Claude for that site's mini audit and send it.

---

## Rules this skill follows

- Public business information only.
- Never invents problems, emails or links. Sites it can't read are marked "Could not read site".
- Never sends messages. Drafts only. You stay in control.
- Never mocks a business's website. It points out opportunities.
- If a website has no problem your service fixes, it marks it "Low fit" and writes no pitch.

---

Made by **SaadAI Labs**. More free AI systems for businesses are coming to this repo every week.
