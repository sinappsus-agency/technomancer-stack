# SOP 08 — Team Communication

**Category:** Team Communication
**Version:** 1.0
**Owner:** Studio Lead
**Trigger:** Ongoing — reviewed at the start of any new contractor engagement
**Frequency:** Continuous, with weekly internal review

---

## Objective

Define how information moves through a small team or contractor network so that nothing important lives only in one person's head, context is preserved across asynchronous gaps, and the operator is not a constant relay station.

---

## Prerequisites

- [ ] All active contractors and collaborators have been onboarded (SOP 09)
- [ ] All team members have access to the communication channels below

---

## Communication Channel Guide

Use the right channel for the right message type. Do not mix them.

| Channel | Purpose | Expected response time |
|---|---|---|
| Slack (or Discord) `#project-[name]` | Project-specific updates, questions, files | Within working hours, same day |
| Slack `#general` | Studio-wide announcements, non-urgent team notes | Within 24 hours |
| WhatsApp / SMS | Urgent, time-sensitive issues only | ASAP |
| Email | External-facing (clients, vendors, invoices) | Within 24 business hours |
| Telegram (operator only) | n8n automation alerts, bot notifications | N/A (automated) |
| Project board (ClickUp / Notion) | Task updates, file links, status changes | Updated when task status changes |
| Video call | Complex discussions, feedback sessions, retros | Scheduled in advance |

**Rule:** If it would take more than 3 messages back and forth to resolve in Slack, it is a video call.

---

## Async-First Communication Norms

This studio operates async-first. This means:

1. **No interruption culture.** Do not expect real-time responses unless explicitly marked urgent.
2. **Context-complete messages.** Every message includes enough context that the recipient doesn't need to ask a clarifying question. "Does this look okay?" is not a context-complete message. "I updated the header section per your note — see attached. Does the spacing on mobile look right to you?" is.
3. **Decisions in writing.** Verbal decisions (calls, spontaneous conversations) are followed up with a written summary within 2 hours.
4. **One channel per topic.** Don't split a conversation across Slack, email, and WhatsApp.

---

## Status and Blocker Reporting

All active team members report status twice per week using this format (Slack DM or `#project-[name]`):

```
STATUS UPDATE — [DATE]

DONE:
- 

IN PROGRESS:
- 

BLOCKED / NEED FROM YOU:
- [specific ask and deadline]

ON TRACK FOR [NEXT MILESTONE] by [DATE]: YES / AT-RISK / NO
```

If the update contains "BLOCKED": the Studio Lead responds within 4 hours during business days.

---

## Internal Escalation Protocol

When does something escalate to the Studio Lead?

| Situation | Action |
|---|---|
| Task will miss deadline | Notify Studio Lead with 24 hours notice minimum |
| Scope question not in the brief | Notify Studio Lead — do not freelance the answer |
| Client contacts you directly (rare) | Acknowledge warmly, cc Studio Lead, let Studio Lead respond |
| Technical blocker | Post in Slack with specifics. Studio Lead responds within 4h or redirects |
| Anything that could embarrass the studio | Escalate immediately via WhatsApp |

---

## End-of-Week Wrap

Every Friday (or last working day of the week), each active team member sends a weekly wrap via Slack:

```
WEEKLY WRAP — [NAME] — [DATE]

COMPLETED THIS WEEK:
- 

WHAT CARRIED OVER (and why):
- 

PLAN FOR NEXT WEEK:
- 

ANYTHING I NEED YOU TO KNOW:
- 
```

Studio Lead reviews all wraps by end of day Friday and responds to anything needing action.

---

## Tools Required

- Slack or Discord (team communication)
- Project board (task and status)
- Video tool (Zoom / Whereby / Meet)
- Telegram (automated alerts — Studio Lead only)

---

## Failure Modes and Escalation

**Failure: A team member consistently misses status updates**
Address privately, not in a group channel. Explain why the updates matter (visibility, not control). If it continues after one direct conversation: this is an onboarding and fit issue.

**Failure: A decision was made in a call but not followed up in writing**
Follow up within 24 hours if you notice it. Make it a habit to end every call with "I'll send a summary of what we decided." See SOP 03 (Meetings).

**Failure: Information is split across multiple channels**
Consolidate: summarise the thread in the project board task where it belongs. The project board is the single source of truth for project-specific information.

---

## Output / Handoff

Communication SOP is "active" rather than having a single completion state. Review it:
- [ ] When a new contractor is onboarded
- [ ] When the team grows or changes composition
- [ ] When a communication failure causes a project issue
