# SOP 03 — Meetings and Scrums

**Category:** Meetings
**Version:** 1.0
**Owner:** Studio Lead
**Trigger:** Any scheduled meeting within 24 hours
**Frequency:** Per meeting

---

## Objective

Make every meeting deliberate, time-bounded, and outcome-producing. A meeting without a clear output is a liability, not a collaboration.

This SOP covers four meeting types: Discovery, Check-In, Review, and Retrospective.

---

## Prerequisites

- [ ] Meeting is in calendar with correct duration and video link
- [ ] Attendees confirmed (calendar accept received or verbally confirmed)
- [ ] Relevant context is loaded (client context.md reviewed if client meeting)

---

## Meeting Types and Durations

| Type | Purpose | Duration | Who |
|---|---|---|---|
| Discovery | Understand the client's situation and brief | 60 min | You + client |
| Check-In | Project status and blocker review | 30 min | You + client |
| Review | Present deliverable and gather structured feedback | 45 min | You + client |
| Retrospective | What worked, what didn't, what to do differently | 30 min | You (internal) or You + client |

---

## Steps — Pre-Meeting (all types)

**Step 1 — Prepare 24 hours before**
You:
- Review the client's context.md (if client meeting)
- Confirm the meeting type and prepare the appropriate agenda template (below)
- Identify the 1–2 decisions this meeting needs to produce
- If Review: confirm the deliverable is ready and accessible (link or screen share prepared)
→ Output: Agenda prepared

**Step 2 — Send agenda 2 hours before**
You send the agenda to attendees via email or Slack:
*"Quick agenda for our [TIME] call: [bullet list of 2–3 points]. Main decision we need to make: [X]."*
→ Output: Attendees arrive prepared

---

## Steps — During Meeting

**Step 3 — Open with time + outcome declaration**
Open every meeting: *"We have [X] minutes. By the end I want us to have [specific outcome]. Let's get started."*
Do not ask "how are you" for more than 60 seconds. Warm but efficient.

**Step 4 — Take structured notes**
Use the meeting notes template:
```
Meeting: [type] with [client/person]
Date: YYYY-MM-DD
Attendees:

CONTEXT
- 

DECISIONS MADE
- 

OPEN QUESTIONS
- 

NEXT ACTIONS
[Who] will [do what] by [when]
```
Take notes in `brand-os/05-clients/[client-slug]/correspondence/` or your internal notes folder.

**Step 5 — End with next action summary**
In the last 5 minutes, read back the decisions made and next actions aloud.
*"Before we close: we agreed [X], next steps are [Y] by [DATE], and [Z] by [DATE]. Does that match your understanding?"*

---

## Steps — Post-Meeting

**Step 6 — Send meeting summary within 2 hours**
Send a brief summary message to attendees:

```
Summary from our [TYPE] call — [DATE]

Decisions:
- [Decision 1]
- [Decision 2]

Next steps:
- [NAME] will [action] by [DATE]
- [NAME] will [action] by [DATE]

Let me know if I've missed anything.
```

**Step 7 — Update project board and CRM**
Add any new tasks to the project board (ClickUp / Notion).
Log the meeting in ERPNext contact history with a one-sentence summary.
Update context.md with any new facts about the client.
→ Output: Project board current, CRM updated, context.md updated

---

## Async Scrum Substitute

For projects where weekly check-in calls are disproportionate to the pace, use async scrums instead:

**Cadence:** 2x per week (Monday + Thursday)
**Format:** Brief message via Slack/email/Telegram:

```
ASYNC UPDATE — [DATE]

DONE (since last update):
- 

IN PROGRESS (today + tomorrow):
- 

BLOCKED / NEED FROM YOU:
- 
```

Client responds with the same format or a simple "sounds good." This replaces a 30-minute call for stable projects.

---

## Checkpoints

- **Before Review meetings:** Confirm the deliverable is final and accessible before the meeting starts. Do not open a review call without the work ready to show.
- **Retros:** They are only useful if you are honest. A retro that only celebrates wins is a waste of time.

---

## Tools Required

- Calendar (Google Calendar / Cal.com)
- Video (Zoom / Google Meet / Whereby)
- Meeting notes (Notion or local markdown)
- Project board (ClickUp / Notion)
- ERPNext (contact log)

---

## Failure Modes and Escalation

**Failure: Client does not show up**
Wait 5 minutes. Send a "Just checking — are we still on?" message. If no response by 10 minutes, end the meeting slot and send a calm reschedule message: *"Looks like we missed each other — no worries. My next available slots are [link]."* Do not send multiple messages.

**Failure: Meeting runs over time**
At the scheduled end time, say: *"We're at time. Do you have 5–10 more minutes or shall we schedule a short follow-up call?"* Do not silently continue. Time discipline is a signal of operational maturity.

**Failure: Decision is unclear at end of meeting**
Do not end the meeting without clarity. If needed: *"Before we finish, can we confirm exactly what we decided? I want to make sure my summary is accurate."*

---

## Output / Handoff

Meeting complete when:
- [ ] Notes filed in correct folder
- [ ] Summary sent to attendees within 2 hours
- [ ] CRM contact log updated
- [ ] All next actions in the project board with owners and due dates
