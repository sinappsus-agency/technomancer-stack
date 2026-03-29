# SOP 12 — Branding Quick Start

**Category:** Brand + Creative
**Version:** 1.0
**Owner:** Studio Lead
**Trigger:** New brand project initiated (client or internal)
**Frequency:** Per brand engagement

---

## Objective

Complete the brand foundation for a client — or for the studio itself — using a structured single-day engagement protocol that produces a brand platform document, voice calibration, and visual identity brief ready for design execution.

This is also the studio's productizable branding offer: a fixed-scope, fixed-fee engagement (Brand Sprint Day) that can be delivered in one working day.

---

## Prerequisites

- [ ] Pre-workshop questionnaire completed and returned by client (see Section A)
- [ ] Workshop slot confirmed (4 hours minimum, 6 hours preferred)
- [ ] Video call (Google Meet / Zoom) with recording option enabled
- [ ] Brand Platform Document template open (see Section C)

---

## Section A — Pre-Workshop Questionnaire

Send at least 48 hours before the session. Require all answers before proceeding.

```
BRAND FOUNDATION QUESTIONNAIRE — [CLIENT NAME]

1. In one sentence, what does your business do and who does it do it for?

2. Why does this exist? Not what it does — why it matters that it exists at all.

3. Who is your primary customer? Describe a real person, not a demographic category.

4. What do you want them to feel when they encounter your brand? (pick 3 maximum)

5. What do you never want them to feel or think about your brand?

6. Name 3 brands you respect (in any industry). What do you respect about each?

7. Name 3 brands you do NOT want to look or sound like. Why?

8. What does your closest competitor do better than you right now?

9. What do you do better than everyone else? If you don't know, what do you want to?

10. If your brand were a person, describe them in 3 sentences.
```

---

## Section B — Workshop Facilitation Flow

**Total duration:** 4–6 hours
**Format:** Video call + shared live document (Google Docs or Notion)

### Block 1 — Discovery (90 minutes)

Purpose: Understand the founder's intent and the audience's need.

Go through questionnaire answers verbally. Do not lecture — facilitate. Ask "why" at least once on every answer.

Key extraction questions:
- "You said X. What would you say if you had to reduce that to a single sentence?"
- "Who is NOT your customer? Who are you trying to repel?"
- "If you could only say one thing about this brand, what would it be?"

Record exact phrases the founder uses. These phrases often become the brand voice.

### Block 2 — Brand Foundation Canvas (60 minutes)

Fill in the Brand Foundation Canvas live, with the client able to see it:

```
BRAND FOUNDATION CANVAS — [CLIENT NAME]

PURPOSE (why it exists):

POSITIONING (who, what, and against what alternatives):

AUDIENCE (specific, named, described):

VALUES (3–5 max, each with a one-sentence description):

VOICE ATTRIBUTES (3–5 adjectives, each with a "we are this / we are not that" pair):

PROMISE (what the customer can always expect):

TAGLINE OPTIONS (3 candidates — not final):
```

Do not leave the canvas workshop until every field has content. Taglines are not final — they are working hypotheses.

### Block 3 — Voice Calibration (45 minutes)

Voice calibration produces the practical writing rules, not abstract principles.

For each voice attribute identified in Block 2, produce:

1. A writing sample that CORRECTLY reflects the voice (write it live with the client)
2. A rewrite of the same sample that violates the voice
3. A 1-sentence rule extracted from the contrast

**Example:**

> Voice attribute: Direct / not condescending
>
> Correct: "You have three options. Here's what each one costs."
>
> Violation: "Great question! There are a few different things to consider here, and it really depends on your needs, but..."
>
> Rule: "Say the thing. Don't buffer it."

Compile all rules into a Voice Rules section of the Brand Platform Document.

### Block 4 — Visual Identity Brief (45 minutes)

This is NOT a design session. It is a brief that will direct a designer.

Fill in:

```
VISUAL IDENTITY BRIEF — [CLIENT NAME]

FEELING to evoke in visual form (reference the 3 feelings from questionnaire):

REFERENCE BRANDS (aesthetic reference, not identity copying):

REFERENCE ANTI-BRANDS (what to avoid visually):

COLOUR DIRECTION (warm/cool, saturated/muted, light/dark — no specific hex codes yet):

TYPOGRAPHY DIRECTION (serif/sans, formal/casual, geometric/humanist):

PHOTOGRAPHY / IMAGERY STYLE:

LOGO DIRECTION (mark only / wordmark / combination / abstract / literal):

WHAT MUST BE AVOIDED:
```

### Closing (15 minutes)

Confirm with the client:
- What they approved in the session (read back the Purpose, Positioning, Promise)
- What happens next (visual design, deliverable dates)
- What they still need to decide (outstanding questions — note them explicitly)

---

## Section C — Brand Platform Document

The final output of the Brand Sprint Day. Contains:

1. Brand Foundation Canvas (final, from Block 2)
2. Audience Profile (written as a named persona, from Block 1)
3. Voice Rules (from Block 3)
4. Visual Identity Brief (from Block 4)
5. Tagline candidates (from workshop)
6. Approved tags and phrases from the discovery verbatim

**Template file:** `prompts/brand/origin-stack-refinement.md` (adapt for client use)

Deliver in two formats: PDF (for the client's files) + editable doc (for ongoing reference).

Delivery timeline: within 24 hours of the workshop.

---

## Internal Brand Use

For the studio's own brand (Graphifx / Technomancer), the same protocol applies.

The studio Brand Platform Document lives in:
- `brand_guide.md` (values, positioning, mission)
- `persona.md` (audience profile)
- `visual_identity.md` (visual direction)

When any of these change, update them in the repo — they are the source of truth for all AI prompts and content generation.

---

## Tools Required

- Video call (Google Meet / Zoom)
- Google Docs or Notion (live collaborative document)
- ERPNext (project and deliverable record)
- `prompts/brand/origin-stack-refinement.md` (prompt template for AI brand voice calibration)
- Canva / Figma (visual identity execution — not part of this SOP)

---

## Failure Modes

**Failure: Client skips the pre-workshop questionnaire**
Reschedule the session. Do not run the workshop without it. The questionnaire forces prior reflection that the session cannot replicate.

**Failure: Client wants to skip Block 3 (voice calibration)**
The visual identity is easier and more tangible, so clients often want to get there faster. Do not skip voice. Visual execution without a voice calibration produces a brand that looks right but sounds generic.

**Failure: No approved Brand Platform Document before design begins**
Design without an approved platform creates rework. Never hand a brief to a designer without a signed-off Brand Foundation Canvas.

---

## Output / Handoff

Brand Sprint Day complete when:
- [ ] Brand Foundation Canvas completed and verbally approved in session
- [ ] Voice Rules written (minimum 3, each with example + anti-example)
- [ ] Visual Identity Brief filled in
- [ ] Brand Platform Document sent to client within 24 hours
- [ ] ERPNext project updated with approved deliverable
- [ ] Design brief issued (if visual execution follows)
