# SOP 07 — Client Feedback and Satisfaction

**Category:** Client Feedback + Satisfaction
**Version:** 1.0
**Owner:** Studio Lead
**Trigger:** Project delivery complete (within 5 days)
**Frequency:** Per project + quarterly for ongoing retainer clients

---

## Objective

Systematically capture what is working, what is not, and what would make a client a stronger advocate — so that quality compounds over time and reputation becomes an asset, not a hope.

---

## Prerequisites

- [ ] Project delivery complete (or quarterly retainer milestone reached)
- [ ] Post-delivery check-in from SOP 02 is done first (let 3–5 days pass after delivery before requesting formal feedback)

---

## The Feedback Stack

Three feedback types serve different purposes:

| Type | Tool | Timing | Purpose |
|---|---|---|---|
| Pulse survey | Short form (3 questions) | Mid-project | Catch issues early |
| Post-project survey | Longer form (5–7 questions) | Within 5 days of delivery | Full satisfaction assessment |
| Testimonial request | Email outreach | 10–14 days after positive survey | Social proof |

---

## Steps — Post-Project Survey

**Step 1 — Trigger the feedback workflow in n8n**
The `crm-journey-stages.json` workflow automatically sends the post-project survey form via Notifuse when the CRM project status is moved to "Delivered."

Confirm the automation fired by checking n8n Executions.
If it didn't fire: manually send the survey link via the client's preferred channel.

**Step 2 — Review feedback when received**
When the form response arrives (n8n webhook → Telegram notification), you review it fully.

Read for:
- NPS score (0–10)
- Any specific negative signals
- Any specific positive signals suitable for a testimonial
- Any themes that recur across multiple clients

**Step 3 — Respond to the feedback within 24 hours**
Acknowledge every response personally. Do not use an automated "thanks for filling this in" message.

If score is 9–10: *"Really glad this hit the mark. If you're open to it, I'd love to share a version of what you described as a case study or a short quote — would that be okay?"*

If score is 7–8: *"Thank you for the honest feedback. The note about [X] is useful — I'll make sure that's handled differently next time. Happy to talk through anything in more depth."*

If score is 1–6: **Call, do not email.** See Negative Feedback Protocol below.

---

## Negative Feedback Protocol (NPS 1–6)

1. Call the client within 24 hours of receiving the low score.
2. Open with: *"I want to understand what went wrong from your perspective. I'm not calling to push back — I want to hear it."*
3. Listen without defending. Take notes.
4. Identify whether the issue is recoverable.
   - If yes: propose specific remediation. Follow through. Send a summary email after the call.
   - If no: acknowledge, apologise where warranted, and close the loop professionally.
5. After the call: document the failure root cause in your internal retro notes. Update the relevant SOP to prevent recurrence.
6. Do not request a testimonial from a low-score client. Earn it first.

---

## Testimonial Extraction

**Step 4 — Request testimonial (for 9–10 scores)**
Send this message 10–14 days after the post-project survey:

```
Hi [NAME],

Really glad [PROJECT] landed well. I'm building out case studies and testimonials for [PURPOSE — website / book launch / etc.] and wondered if you'd be willing to help.

If yes, three options — whatever's easiest:
1. I draft a summary of what we did and the outcome, you review and approve
2. I send 3 short questions by email and use your answers
3. 10-minute video call and I handle the edit

Let me know what works.

[NAME]
```

**Step 5 — Store the testimonial**
Store the approved testimonial in:
- `brand-os/04-offers/testimonials/[client-slug]-testimonial.md`
- ERPNext client record (testimonial field)
- MinIO/assets as formatted image asset for social/marketing use

---

## Mid-Project Pulse Survey

For projects over 4 weeks, send a pulse survey at the midpoint.

3-question format:
1. *On a scale of 1–5, how satisfied are you with the project's progress so far?*
2. *Is there anything we could be doing better or differently?*
3. *Is there anything blocking you on your side that we should know about?*

Send via Notifuse link manually or trigger from n8n timeline automation.
Review response. If anything is flagged, address it within 48 hours.

---

## Tools Required

- n8n (`crm-journey-stages.json` — handles automated send)
- Notifuse (email delivery)
- ERPNext (NPS scores and feedback logs)
- Telegram (operator notification on form response)
- Survey tool (Tally / Typeform / Google Form)

---

## Failure Modes and Escalation

**Failure: Client does not complete the survey**
Send one reminder after 5 days: *"Quick question — did our feedback form reach you? Happy to do it verbally if easier."* If still no response: log "no feedback received" in ERPNext and move on.

**Failure: Negative feedback is generic ("wasn't great")**
Call to understand specifics. Generic negative feedback is almost impossible to act on — you need the specific moment or expectation that was missed.

**Failure: You receive a 10/10 but the client is hard to reach for a testimonial**
Respect their time. Send one testimonial request. If no response after 2 weeks, let it go. You can still reference the engagement (without a direct quote) if they are willing to be a reference.

---

## Output / Handoff

Feedback cycle complete when:
- [ ] Post-project survey sent and response received (or follow-up attempted)
- [ ] NPS score logged in ERPNext
- [ ] Feedback acknowledged personally within 24 hours
- [ ] Testimonial requested (if 9–10 score) and stored if received
- [ ] Any negative feedback: root cause documented, relevant SOP updated
