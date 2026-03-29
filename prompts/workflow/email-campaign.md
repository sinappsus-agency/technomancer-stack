# Email Campaign Copy Prompts

**Purpose:** Ready-to-use prompt templates for generating email campaign copy via Ollama or any LLM. These are structured prompts — fill in the `[BRACKETS]` before submitting.

All campaigns must go through human review before sending. The output of any prompt here is a draft, not a final.

---

## How to Use

1. Choose the campaign type that matches your intent (welcome, nurture, re-engagement, promotional)
2. Fill in all `[BRACKETED]` placeholders
3. Paste into OpenWebUI (`http://[your-server]:3000`) or submit via the n8n email campaign workflow
4. Review output against brand voice (`brand_guide.md`, `persona.md`)
5. Edit before sending

---

## Campaign Types

### 1. Welcome Email (Single)

Sent immediately when someone joins the list.

```
You are a copywriter for [BRAND NAME], a [one-line description of what the brand does].

Write a welcome email for a new subscriber.

Brand voice: [PASTE 2-3 VOICE RULES FROM brand_guide.md]
Audience: [WHO THEY ARE — specific, not generic]

The email should:
- Open with a genuine welcome that reflects the brand's personality (not "Thank you for subscribing")
- Tell the subscriber exactly what to expect from future emails (frequency, content type)
- Give them one immediate piece of value (tip, resource, or insight)
- Set the tone for the relationship — peer-to-peer, not broadcast

Format:
- Subject line: under 50 characters
- Preview text: under 90 characters
- Body: 200-300 words
- CTA: one action (link to first resource, best article, or offer)
- Sign-off: [SENDER NAME]

Output as JSON: { "subject": "", "preview_text": "", "body_html": "", "body_plain": "" }
```

---

### 2. Welcome Sequence — Email 2 (Day 3)

Builds on the welcome. Delivers the first concrete value.

```
You are a copywriter for [BRAND NAME].

Write the second email in a welcome sequence, sent 3 days after signup.

Brand voice: [VOICE RULES]
Subscriber context: They signed up for [WHAT THEY SIGNED UP FOR / LEAD MAGNET TOPIC]

This email should:
- Open with a link to the context from email 1 (brief reference, not recap)
- Deliver one specific insight or framework related to [CORE TOPIC]
- Be actionable: the reader should be able to do something with this today
- Close with a soft question or invitation to reply (builds reply rates + inbox placement)

Format:
- Subject line: story or insight hook, under 50 characters, do not start with "How to"
- Preview text: under 90 characters
- Body: 250-350 words
- CTA: engagement (reply, share, read related article)
- Output as JSON: { "subject": "", "preview_text": "", "body_html": "", "body_plain": "" }
```

---

### 3. Welcome Sequence — Email 3 (Day 7)

Transition from welcome to regular list and introduce the offer.

```
You are a copywriter for [BRAND NAME].

Write the third and final email in a welcome sequence, sent 7 days after signup.

Brand voice: [VOICE RULES]
Primary offer: [WHAT YOU ARE SELLING OR INVITING THEM TO — service / product / community / course]

This email should:
- Feel like a natural evolution of the conversation, not a pivot to a sales email
- Reference what the subscriber has received so far (briefly)
- Introduce the offer as the logical next step for someone who found value in emails 1 and 2
- Be honest about what the offer is and who it is for
- Include a clear CTA with the offer URL

Format:
- Subject line: benefit-led, direct, under 50 characters
- Preview text: reinforces the offer
- Body: 200-280 words
- CTA: [CTA VERB + URL]
- Output as JSON: { "subject": "", "preview_text": "", "body_html": "", "body_plain": "" }
```

---

### 4. Nurture Email (Standalone)

For regular newsletter sends. Value-first, no hard pitch.

```
You are a copywriter for [BRAND NAME].

Write a nurture email on the topic: [TOPIC]

Brand voice: [VOICE RULES]
Audience: [WHO THEY ARE — what they care about, what they're trying to do]
Insight or framework to share: [THE CORE IDEA — 1-2 sentences in your own words]

This email should:
- Open with an observation or specific story that pulls the reader into the topic
- Deliver one well-developed insight (not a list of 10 tips)
- Include one concrete example or case
- End with a question, invitation to reply, or a soft CTA to a related resource

Format:
- Subject line: curiosity-driven or observation-based, under 50 characters
- Preview text: extends subject naturally
- Body: 300-450 words
- At most one external link in the body
- CTA at end: one action only
- Output as JSON: { "subject": "", "preview_text": "", "body_html": "", "body_plain": "" }
```

---

### 5. Re-Engagement Email

For subscribers inactive for 60+ days.

```
You are a copywriter for [BRAND NAME].

Write a re-engagement email for inactive subscribers (no opens or clicks in 60+ days).

Brand voice: [VOICE RULES]
Audience: [WHO THEY ARE]
Best asset or offer available right now: [LINK OR DESCRIPTION]

Rules:
- Be direct and honest. Acknowledge that they haven't heard from us in a while.
- Do not grovel or apologise excessively
- Give them a reason to stay: one strong piece of value or a relevant offer
- Give them a clear option to unsubscribe — respecting their decision improves list hygiene
- Line: "If this isn't for you anymore, no hard feelings — unsubscribe below."

Format:
- Subject line: honest, slightly personal, under 45 characters. Example: "Still interested?"
- Preview text: direct follow-through on subject
- Body: 150-200 words
- Two CTAs: (1) the value/offer link, (2) the unsubscribe link (phrased naturally)
- Output as JSON: { "subject": "", "preview_text": "", "body_html": "", "body_plain": "" }
```

---

### 6. Promotional Email

For a specific offer, launch, or time-sensitive campaign.

```
You are a copywriter for [BRAND NAME].

Write a promotional email for: [OFFER NAME]

Brand voice: [VOICE RULES]
Audience: [WHO THEY ARE AND WHY THIS OFFER IS RELEVANT TO THEM]
Offer details:
- What it is: [DESCRIPTION]
- What it does for them: [OUTCOME / BENEFIT]
- Price / investment: [PRICE OR "contact for quote"]
- Deadline or scarcity: [DATE / LIMITED SPOTS / NONE]
- CTA URL: [URL]

Rules:
- Lead with the outcome, not the features
- Be specific about what they get — no vague "transform your [X]" language
- If there is a deadline, it must be real. Do not fabricate urgency.
- One offer. One CTA. Do not upsell or cross-sell in this email.

Format:
- Subject line: outcome-led or scarcity-based, under 50 characters
- Preview text: reinforces urgency or benefit
- Body: 200-300 words
- CTA: imperative verb + URL
- Output as JSON: { "subject": "", "preview_text": "", "body_html": "", "body_plain": "" }
```

---

## Subject Line Generator (standalone)

Use this when you have body copy but need subject line options.

```
Generate 5 subject line options for this email:

[PASTE EMAIL BODY]

Brand: [BRAND NAME]
Audience: [WHO]
Email type: [welcome / nurture / offer / re-engagement]

Rules for all options:
- Under 50 characters
- No emoji unless brand uses emoji consistently
- No "How to", "Top X", "You won't believe", or "Just checking in"
- At least one option should be a question
- At least one option should be a bold statement
- At least one option should be curiosity-gap framing

Output: numbered list, no explanations.
```

---

## A/B Subject Line Test Pairs

Use these patterns to generate subject line variants for split testing:

| Test type | Version A | Version B |
|---|---|---|
| Curiosity vs. direct | Implied benefit | Stated benefit |
| Short vs. long | Under 35 chars | 45-50 chars |
| Question vs. statement | Why most [X] fail | Most [X] are failing. Here's why. |
| Personal vs. corporate | I stopped doing this in 2023 | The case against [common practice] |

Always test subject lines with a minimum 500-subscriber sample per variant for statistical significance.

---

## Quality Checklist Before Sending

- [ ] Subject line under 50 characters and avoids spam triggers
- [ ] Preview text does not repeat the subject line
- [ ] One CTA — not two, not three
- [ ] Copy reviewed for voice alignment (check `brand_guide.md`)
- [ ] No placeholder text (`[NAME]`, `[LINK]`) in sent version
- [ ] Unsubscribe link present (legal requirement in most jurisdictions)
- [ ] Tested in plain text view (many clients display plain text)
- [ ] Sent from a deliverability-warmed address (not cold domain)
