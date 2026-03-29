# SOP 02 — Client Follow-Up

**Category:** Client Follow-Up
**Version:** 1.0
**Owner:** Studio Lead
**Trigger:** Delivery completed, OR 30/60/90-day relationship milestone reached
**Frequency:** Per project + ongoing relationship cadence

---

## Objective

Maintain active, intentional client relationships between project phases so that renewals, referrals, and expansions happen naturally — not because you scrambled to remember someone at the last minute.

Most relationship revenue loss is silent. This SOP prevents that.

---

## Prerequisites

- [ ] Project delivery is complete (or a defined phase is complete)
- [ ] CRM record for client exists in ERPNext and is current
- [ ] context.md for client is up to date

---

## The Three Follow-Up Types

### Type A — Post-Delivery Check-In (within 5 days of delivery)
**Trigger:** Project delivery marked complete in project board
**Purpose:** Confirm satisfaction, surface any issues before they become complaints, plant the seed for next engagement

### Type B — Milestone Check-In (30 / 60 / 90 days post-delivery)
**Trigger:** n8n date-based automation fires (from CRM field `delivery_date`)
**Purpose:** Check on results, share a relevant insight, maintain warmth without selling

### Type C — Inactive Re-Engagement (90+ days since last contact)
**Trigger:** n8n automation flags contact as "no activity in 90 days"
**Purpose:** Reconnect without awkwardness, offer something of value, assess renewal opportunity

---

## Steps — Type A (Post-Delivery)

**Step 1 — Send delivery confirmation message**
Within 24 hours of delivery, you send a message via their preferred channel (email or Slack):
- Summarise what was delivered
- Note anything that may need their attention
- Ask: *"Does everything look right from your side?"*
→ Output: Delivery confirmation sent

**Step 2 — Log delivery in CRM**
In ERPNext, update project status to "Delivered" and set `delivery_date` to today.
This triggers the 30/60/90-day automation sequence in n8n (`crm-journey-stages.json`).
→ Output: CRM updated, automation triggered

**Step 3 — Send feedback request (Day 5)**
n8n sends the post-project feedback form automatically (see SOP 07).
You review the response when it arrives.
→ Output: Feedback form sent

---

## Steps — Type B (Milestone Check-In)

**Step 1 — Review context before reaching out**
Open the client's `context.md`. Refresh your memory on:
- What you delivered
- What outcomes they were hoping for
- Any personal context (team changes, upcoming events, challenges they mentioned)

**Step 2 — Prepare a value-first message**
Do not open with "Just checking in." Open with something relevant:
- An insight that applies to their situation
- A short resource (article, tool, framework) that connects to their goals
- A question about how something specific is going

Template:
```
Hi [NAME],

[Relevant insight or observation in 1–2 sentences].

How is [specific thing from their context] going since we wrapped up?

[Your name]
```

**Step 3 — Send via preferred channel and log**
Send the message. Update ERPNext contact log with date and summary.
→ Output: Check-in sent, CRM updated

---

## Steps — Type C (Re-Engagement)

**Step 1 — Audit the relationship before reaching out**
Review context.md and ERPNext history. Understand:
- Why did contact go quiet? (project ended, budget cycle, life event?)
- Was the last interaction positive?
- Is there a genuine reason to reach out now?

If the last interaction was neutral or positive: proceed.
If there was an unresolved issue: resolve it before contact.

**Step 2 — Lead with value, not pitch**
Re-engagement messages that open with "I haven't heard from you" or "Are you ready to work together again?" rarely convert.

Lead with:
- Something you thought of specifically for them
- An invitation (webinar, resource, free audit)
- A genuine question about something important to them

**Step 3 — One reach-out, then rest**
If no response after one re-engagement message, move the contact to "Dormant" in ERPNext and set a 6-month review flag.
Do not follow up more than once on a re-engagement. Respect the signal.

---

## Checkpoints

- **Type B messages:** Review context.md before every milestone check-in. A generic check-in is often worse than no check-in.
- **Type C:** Always check for unresolved issues before re-engaging.

---

## Tools Required

- n8n (`crm-journey-stages.json` — handles 30/60/90 automation)
- ERPNext (CRM contact log, relationship status)
- Notifuse (email sends for automated touches)
- Context.md (client AI context file)

---

## Failure Modes and Escalation

**Failure: n8n automation doesn't fire for milestone check-in**
Check that `delivery_date` was set in ERPNext when the project was marked delivered. Manually trigger the sequence if needed.

**Failure: You send a generic check-in and it falls flat**
Logged lesson: always refresh context.md before any outreach. Update your system prompt to remind you to check context before drafting follow-ups.

**Failure: Client has moved company or changed email**
Update ERPNext with new details. Resend any pending check-ins to the correct address.

---

## Output / Handoff

- Type A complete: CRM updated, feedback request sent, 30/60/90 automation running
- Type B complete: Message sent, CRM log updated
- Type C complete: Either relationship reactivated (return to Type A flow) or marked "Dormant" with review date
