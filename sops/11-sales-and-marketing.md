# SOP 11 — Sales and Marketing

**Category:** Revenue + Growth
**Version:** 1.0
**Owner:** Studio Lead
**Trigger:** Lead captured (inbound form, DM, referral, call inquiry)
**Frequency:** Per lead event + weekly pipeline review

---

## Objective

Convert qualified inbound leads into proposals within 48 hours, run a structured follow-up sequence of no more than 3 touches over 14 days, and maintain a pipeline view that reflects real opportunity — not wishful thinking.

---

## Prerequisites

- [ ] ERPNext CRM set up with your service items (for proposal generation)
- [ ] Lead capture point defined (form, DM funnel, call center — SOP cross-ref below)
- [ ] Proposal template exists and is branded
- [ ] n8n `client-onboarding-trigger.json` workflow running

---

## Part A — Lead Capture and Qualification

**Trigger:** Any inbound lead from any source

### Step 1 — Log the lead in ERPNext within 24 hours

ERPNext: CRM → Leads → New Lead

Fields to complete:
- Lead Name
- Email + phone
- Source (referral / social / website / cold / call center)
- Industry
- Budget (estimated, ask directly or estimate from context)
- Service type of interest
- Lead status: Open

### Step 2 — Qualify before booking a call

Answer these four questions from initial context or a single qualifying email:

| Question | Pass | Fail |
|---|---|---|
| Do they have a clear problem? | Yes, they can describe it | Unclear or vague |
| Can they afford a studio-level engagement? | Budget signals indicate yes | Bargain-hunting signals |
| Is this in our service area? | Yes, fits current offering | Outside scope |
| Are we able to start in their timeline? | Yes | No — flag in CRM |

If **3 or more Pass**: proceed to proposal.
If **2 or fewer Pass**: park in "Low Priority" status in ERPNext. Do not spend time on a proposal.

### Step 3 — Qualification email (send within 4 hours of lead capture)

For leads that warrant engagement, send a qualifying reply before booking:

**Subject:** Re: [Their subject / your service type they mentioned]

```
Hi [Name],

Thanks for reaching out — I've read through your message.

Before I put together anything specific, I want to make sure we can actually help you. Quick questions:

1. What's the timeline you're working with?
2. Is there a budget range you're working within for this?
3. What would "this worked" look like for you 90 days from now?

Once I have that, I can give you a proper picture of what we can do and whether it makes sense to go further.

[Your Name]
```

---

## Part B — Proposal Process

**Trigger:** Lead qualifies (3+ Pass on criteria above)

### Step 1 — Discovery call (30 minutes maximum)

Before writing a proposal, run discovery. Do not skip this.

Discovery call questions:
1. Tell me about the problem you're trying to solve. (→ listen for root cause, not surface symptom)
2. What have you already tried?
3. What does success look like in 90 days?
4. Who is involved in the decision to proceed?
5. What's your timeline for a decision?

Take notes in ERPNext → Lead → Activity.

### Step 2 — Write the proposal

Proposal sections:
1. **The problem (their words):** Reflect what they told you. No generic agency language.
2. **Our approach:** What we do, why it fits their problem.
3. **Scope:** Specific deliverables. No "and other requirements as needed" clauses.
4. **Timeline:** Start date, milestones, delivery date. Realistic, not optimistic.
5. **Investment:** Clear, no hidden fees. Split into upfront + delivery if applicable.
6. **Next step:** A single clear action (link to sign, or "Reply to confirm").

Length: 1–2 pages. If you need more than 2 pages to explain the engagement, the scope is too complex or too vague.

### Step 3 — Send the proposal within 48 hours of discovery call

Send as PDF from your business email.

Subject: `Proposal — [Service Type] — [Client Name]`

Opening line:  
*"Following our call on [date], here is the proposal you requested."*

Do not over-explain. Let the document do the work.

---

## Part C — Follow-Up Sequence

Maximum 3 touches. No exceptions. If no response after 3, close the lead in ERPNext (status: "Closed — No Response"). You can re-engage in 90 days if they reappear.

### Touch 1 — Day 3 after proposal sent

```
Hi [Name],

Just wanted to check in — did you have a chance to look through the proposal?

Happy to answer any questions or jump on a quick call if anything needs clarifying.

[Your Name]
```

### Touch 2 — Day 7 after proposal sent

```
Hi [Name],

Following up once more on the proposal I sent over.

If the timing or scope isn't quite right, no problem — just let me know and I'll close this off on my end.

If you're still considering it, I'd love to know where you're at.

[Your Name]
```

### Touch 3 — Day 14 after proposal sent (final)

```
Hi [Name],

Last follow-up from me on this. I'm keeping [start date estimate] tentatively open on the schedule for your project, but I need to confirm one way or another by [date] to plan properly.

If this isn't moving forward, no issue at all — just let me know so I can plan accordingly.

[Your Name]
```

---

## Part D — Lost Deal Debrief

**Trigger:** Lead marked Closed (Lost) or Closed (No Response)

When a deal closes without converting:
1. Record the reason in ERPNext: Lead → Notes
2. Categorize: budget / timing / competition / fit / no response
3. Monthly: review all lost deals categorized. If one category appears 3+ times, it is a signal — pricing, messaging, or targeting needs adjustment.

---

## Part E — Weekly Pipeline Review

Every Monday, 15 minutes:
- Open ERPNext CRM → Leads view
- Review every Open lead: has the right touch been sent at the right time?
- Close any leads that are stale (no activity in 14 days, no response expected)
- Note current pipeline value (sum of all active proposal amounts)
- Check call center queue if running (SOP cross-reference: `agents/call-center/README.md`)

---

## Marketing Cadence

Marketing is the top of this funnel. The goal of marketing is to reduce the qualification burden — by attracting leads who already understand what you do and what it costs.

Minimum viable cadence:
- 1 long-form piece per week (LinkedIn / podcast / email)
- 1–3 short-form posts per week (repurposed from long-form via content-machine)
- Email list: minimum 1 newsletter per fortnight
- No chasing vanity metrics on content. The metric is inbound leads and email list growth.

All content creation runs through `agents/content-machine/README.md`.

---

## Cross-References

- Call center inbound lead flow: `agents/call-center/README.md`
- Client onboarding (after won deal): `sops/01-client-onboarding.md`
- Email campaign automation: `n8n-templates/email-campaign-workflow.json`

---

## Tools Required

- ERPNext (CRM, leads, proposals)
- Business email (outbound)
- n8n `client-onboarding-trigger.json` (automation on won lead)
- `agents/content-machine` (content output pipeline)

---

## Failure Modes

**Failure: Proposal sent without discovery call**
You are guessing at scope. This creates underscope, overscope, and client disappointment. Always do discovery first.

**Failure: More than 3 follow-up touches sent**
You are now chasing. It damages positioning. Close the lead. Move on.

**Failure: Qualified leads taking more than 48 hours to get a proposal**
Speed signals seriousness. If you cannot turn a proposal in 48 hours, the problem is either unclear scope (solve: better discovery) or bandwidth (solve: proposal template).

---

## Output / Handoff

Sales cycle complete when:
- [ ] Lead logged in ERPNext
- [ ] Qualification decision made within 24 hours
- [ ] Discovery call notes recorded
- [ ] Proposal sent within 48 hours of discovery call
- [ ] Follow-up sequence running (max 3 touches, 14 days)
- [ ] Lead status updated: Won (→ SOP 01) or Closed
