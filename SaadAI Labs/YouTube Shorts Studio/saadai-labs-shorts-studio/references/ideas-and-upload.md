# Idea mode and the upload pack

## Idea mode ("give me ideas", "what should I post", a niche with no topic)
1. Read `channel.json` and `history.md` (if they exist) so you never repeat a topic.
2. Research with WebSearch (send several searches in one turn): what's currently popular in the niche
   ("<niche> facts people don't know", "<niche> reddit most upvoted", "<niche> youtube shorts viral",
   news from the last 30 days, seasonal hooks for the next 2 weeks). Prefer evergreen topics with a fresh angle.
3. Produce **10 ideas** as a table:

| # | Topic | Hook (≤ 12 words) | Format | Curiosity | Broad appeal | Visual (2D) | Fresh angle | Total /20 |

   - *Curiosity*: does the hook open a gap the viewer must close?
   - *Broad appeal*: would someone outside the niche care?
   - *Visual (2D)*: can our scene types show it (emoji, stat, compare, characters)? Topics that need real
     footage (a specific car crash, a celebrity) score low.
   - *Fresh angle*: not just a retold Wikipedia fact; a twist, a "why", a "you" connection.
4. Mark the top 3, suggest a **series** if 3+ ideas share a pattern (series = returning viewers), and append
   all 10 to `ideas.md`. Ask which to make.

## Reference video ("make one like this <link>")
V1 can't watch videos. Ask the user to paste the transcript or describe it (or give the title), then copy the
**structure only** (hook pattern, beat count, pacing, loop trick), never the script, characters or topic.
Tell the user that's what you're doing and why (copying gets channels demonetised).

## Upload pack (write `<short_dir>/upload.md` after the final render)
```
TITLE (≤ 60 chars, the hook rephrased, 1 emoji max, no clickbait it doesn't pay off)
1. ...  2. ...  3. ...   (3 options; mark the recommended one)

DESCRIPTION
Line 1: one-sentence payoff that includes the main keyword (shows under the title).
Line 2: one surprising extra detail or source ("Source: ...") for fact content.
Line 3: channel CTA from channel.json.
#shorts plus 3-5 specific hashtags (#science #brainfacts, not #viral #fyp).

PINNED COMMENT
A question that's easy to answer ("Could you have fallen for this? 😅") or "Part 2?" tease.

COVER FRAME
The frame number/time that reads best as a still (usually the hook at ~0.5s), for the Shorts thumbnail picker.

POSTING NOTES
- Best: post 1 per day at a consistent time; check "Viewed vs swiped away" after 24h.
- Under ~60% viewed: the hook failed. Rewrite only scene 1 and re-render (voice is cached per scene).
- Altered/synthetic content label: 2D cartoon/animated content does NOT need YouTube's "realistic altered content"
  disclosure; tick it only if something could be mistaken for real footage of real people/events.
```
Append the published short to `history.md`: `yyyy-mm-dd | topic | format | chosen hook`.

## Staying monetisable (YouTube "inauthentic content" policy)
YouTube reviews **channels**, not single videos, and refuses ads on mass-produced, template-identical,
low-effort content. AI tools are allowed. To keep a channel safe the skill always:
- rotates formats and scene mixes (check `history.md`: don't use the same format 3 times in a row);
- writes an original script with a real angle and accurate facts (cite a source in the description for facts);
- keeps the human approval step (storyboard) so the creator directs each video;
- never copies another creator's script, characters or exact structure.
Tell users this when they ask about batching or "100 shorts a day": quality and variety beat volume.
