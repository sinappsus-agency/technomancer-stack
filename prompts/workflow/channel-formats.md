# Channel Formats Reference

**Purpose:** Defines the structural and format requirements for each content channel the studio publishes to. Use these specs when prompting the content-machine agents or when manually producing content.

All formats draw from the Brand OS. Voice rules and positioning from `prompts/brand/origin-stack-refinement.md` always take precedence over format specs.

---

## Email Newsletter

**Audience:** Opted-in list (warm, mid-funnel)
**Frequency:** Minimum fortnightly
**Length:** 350–600 words (body only, excluding subject/signature)
**Tone:** Direct, peer-to-peer. Not broadcast. Write as if to one person.

### Structure

```
Subject line: [single benefit or curiosity hook] — under 50 characters
Preview text: [extends subject, adds urgency or specificity] — under 90 characters

---

[Hook — 1-2 sentences. Tension or observation. No "In today's newsletter..."]

[Problem or insight — 1 paragraph. What pattern are you naming?]

[Depth — 2-4 paragraphs. Your actual thinking. Specific. No filler.]

[Takeaway — 1 paragraph. What should the reader do or think differently?]

[CTA — 1 sentence + link. One CTA only.]

---
[Sign-off]
```

### Rules
- Subject line: never start with "How to" or a generic topic word
- No emoji in subject lines
- No "I hope this email finds you well"
- CTA = one action, one link. Never "check out / follow / also reply / and share"
- Always write in the same voice as `persona.md` — address the reader's ambition, not their fear

---

## LinkedIn Post

**Audience:** Professional, cold-to-warm
**Frequency:** 3–5 times per week
**Length:** 900–1,500 characters (LinkedIn's visible fold is ~230 characters)
**Tone:** Authoritative but accessible. First-person. Specific, not generic.

### Structure

```
Line 1: [Hook — scroll-stopper. Statement, question, or specific fact. Under 130 characters.]
Line 2: [Blank line]
Line 3–6: [Build — 3-5 short paragraphs. One idea per paragraph. Max 2 sentences per line.]
Line 7: [Blank line]
Line 8–10: [Payoff — the insight, the lesson, the reframe]
Line 11: [Blank line]
Line 12: [CTA — optional. "What would you add?" or specific follow-up action]
```

### Rules
- First line must work as a standalone statement — it is what shows before "see more"
- Never start with "I" (LinkedIn algorithm buries these)
- No hashtag spam — max 3 relevant hashtags at the end if used at all
- Do not summarise the post at the end. The post IS the summary.
- Avoid: "Excited to share", "In my experience", "The truth is"
- End on a thought, not a pitch

### Short Hook Patterns (use any)
- Contrarian: "Most [role/people] are wrong about [topic]."
- Specific observation: "[Specific number or fact]. Here's what it means."
- Reframe: "We've been thinking about [topic] backwards."
- Story open: "[Short story setup in one sentence]. What happened next changed how I [do thing]."

---

## Twitter / X Thread

**Audience:** Cold — broad or technical
**Frequency:** 2–3 threads per week (or repurposed from long-form)
**Length:** 5–12 tweets per thread. First tweet: under 250 characters.
**Tone:** Punchy. Dense with ideas. No padding.

### Structure

```
Tweet 1: [Hook. The single most interesting or provocative statement in the thread.]
Tweet 2: [Context — why this matters or what problem it's addressing]
Tweets 3-N: [One idea per tweet. Short. Optionally numbered: "2/"]
Final tweet: [The synthesis or actionable takeaway + CTA or link if relevant]
```

### Rules
- Tweet 1 must work without any follow-up. It earns the thread read.
- Number tweets only if the list framing adds value ("10 things you didn't know about X")
- Do not end every tweet with "Thread below 🧵" — only Tweet 1 if at all
- Quote from the long-form piece exactly when the phrase is strong enough
- Threads repurposed from email or LinkedIn: rebuild for the format, do not copy-paste

---

## Video Script (Short-Form Reel / YouTube Short)

**Audience:** Cold — social discovery
**Duration:** 30–90 seconds
**Tone:** Energetic but not performative. Clear and specific.

### Structure

```
[0-3 sec] HOOK: One sentence. State the payoff or the tension up front.
[3-10 sec] PROBLEM: Why this matters. What's at stake?
[10-50 sec] CONTENT: The actual value. Demo, teaching, insight, story.
[50-60/90 sec] CTA: "Follow for more like this" or specific offer/link.
```

### Visual direction
- Hook frame: text overlay + clear visual context (not black screen)
- Subtitles: always on (auto-gen minimum, burn-in preferred)
- B-roll: relevant screen recordings, workspace, product visual — not stock
- No talking-head-only unless the face + voice IS the content

### Scripting rules
- Write the hook first. If the hook doesn't work, the video doesn't work.
- Read the script aloud before recording. If you stumble, rewrite.
- Every sentence must survive by itself — never build a sentence on "as I was saying"
- 30-second target: 75 words of spoken script. 60-second: 150 words. 90-second: 225 words.

---

## Long-Form Blog Post / Article

**Audience:** SEO + mid-funnel warm (on-site or Medium)
**Length:** 1,200–2,500 words (sweet spot: 1,500)
**Tone:** Authoritative. Structured. Dense with specifics.

### Structure

```
H1: [Title — keyword-aware but written for humans, not bots]

[Lead — 2-3 sentence hook. The problem or tension.]

## [Section heading 1]
[Body]

## [Section heading 2]
[Body]

## [Section heading 3]
[Body]

---
[Conclusion — The synthesis. What to do with this information.]
[CTA — One action: subscribe, book, read next]
```

### Rules
- Section headings: use them. Scannable structure is readable structure.
- No keyword-stuffing. Target one phrase naturally. Do not repeat it mechanically.
- Images: at least one cover image + one supporting image minimum
- Internal links: link to 2–3 other posts or pages where relevant
- Minimum 1 external source cited (adds credibility, not SEO juice on its own)
- Always end with a CTA. A post without a CTA is a conversation with no next step.

---

## Podcast Episode Script

**Audience:** Warm — existing listeners or discovery via platforms
**Duration:** 15–45 minutes (solo) or 30–60 min (guest)
**Tone:** Conversational but structured. On-brand voice throughout.

### Structure

```
[INTRO — 60-90 sec]
Hook: What is this episode about and why does it matter today?
Guest intro if applicable.

[SEGMENT 1 — Context + Problem (5-8 min)]
Set up the problem or topic. What are most people getting wrong?

[SEGMENT 2 — Your take / Framework (10-15 min)]
Your perspective. Specific. Named model or framework if applicable.

[SEGMENT 3 — Application (5-8 min)]
What does the listener do with this? Specific scenario or example.

[OUTRO — 60-90 sec]
Summary of key takeaways (3 max).
CTA: subscribe, review, follow, or specific link.
```

### Solo episode rules
- Notes-only scripting is preferred for natural delivery — full scripts tend to sound read
- Open loop in the title and first 60 seconds: give a reason to stay until the end
- Chapters: timestamps and chapter markers for episodes over 20 minutes

---

## How to Use This File in Prompts

When prompting the content-machine or any AI for content, include the relevant section from this file as context:

```
[Paste the channel format spec here]

Now write [content type] on [topic] for [audience] following these format rules.
Brand voice: [paste from persona.md or brand_guide.md]
```

For email campaign sequences specifically, use `prompts/workflow/email-campaign.md` instead.
