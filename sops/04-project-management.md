# SOP 04 — Project Management

**Category:** Project Management
**Version:** 1.0
**Owner:** Studio Lead
**Trigger:** New project initiated (kickoff call complete)
**Frequency:** Per project, from initiation to archive

---

## Objective

Define how work moves through the studio from brief to completion without the operator becoming a single point of failure for every decision and handoff.

---

## Prerequisites

- [ ] SOP 01 (Client Onboarding) complete
- [ ] Kickoff call done and notes filed
- [ ] Scope and deliverables confirmed (in writing — email or brief document)
- [ ] Timeline and milestone dates agreed

---

## Project Lifecycle Stages

```
Brief → Scoping → Active Delivery → Review → Revision → Final Delivery → Archive
```

In your project board, each project moves through these columns.

---

## Steps — Project Initiation

**Step 1 — Translate brief into work breakdown**
You review the kickoff notes and scope document.
You create a task breakdown in the project board (ClickUp / Notion / Linear) using this structure:

```
Project: [Client Name] — [Project Name]
Due: [Final delivery date]

MILESTONES:
M1: [Deliverable] — due [DATE]
M2: [Deliverable] — due [DATE]
M3: Final delivery — due [DATE]

TASKS under M1:
- [ ] [Task name] | Owner: [Role] | Est: [Xh] | Due: [DATE]
- [ ] [Task name] | Owner: [Role] | Est: [Xh] | Due: [DATE]
```

→ Output: Project fully tasked in project board

**Step 2 — Set timeline in ERPNext**
Create or update the project record in ERPNext:
- Start date, expected end date
- Contracted value
- Milestone dates
→ Output: ERPNext project record complete

**Step 3 — Send project plan to client**
Share a simplified version of the milestone plan with the client via email.
(Not the internal task breakdown — a clean summary: *"Here's how the project flows..."*)
→ Output: Client has line-of-sight on timeline

---

## Steps — Active Delivery

**Step 4 — Weekly project review (internal)**
Every Monday, you review all active projects in the board.
For each: are we on track? Is anything blocked? Does the client need to do anything?
→ Output: Weekly review notes, blockers escalated

**Step 5 — Send status update to client**
Every [CADENCE — e.g., Thursday] you send a brief status update to the client via their preferred channel.

```
[PROJECT NAME] — Status Update [DATE]

Completed this week:
- 

In progress:
- 

Needs from you:
- [action or decision] by [DATE]

On track for [NEXT MILESTONE] on [DATE].
```

Do not send this more than twice per week. Less is more if work is moving.

**Step 6 — Handle scope change requests**
If the client requests new work outside the agreed scope:

1. Acknowledge: *"Happy to look at that."*
2. Assess: add a scope assessment task to the board. Review and estimate the work.
3. Quote: send a scope change request email with hours/cost and revised timeline.
4. Wait for written approval before proceeding.
5. If approved: update ERPNext project value, update project board, send updated milestone plan.

⚠️ Never start out-of-scope work without written client approval. Verbal approval does not invoice.

---

## Steps — Delivery and Close

**Step 7 — Pre-delivery QA**
Before sending any deliverable, run SOP 05 (Quality Assurance).
→ Output: QA checklist complete, deliverable approved internally

**Step 8 — Deliver and confirm**
Send the deliverable to the client with:
- What is included
- How to access it
- Any instructions for review
- Review deadline: *"Please let me know your feedback by [DATE]."*
→ Output: Delivery confirmation sent

**Step 9 — Close the project**
When client signs off:
1. Update ERPNext to "Completed" status
2. Issue final invoice (SOP 10)
3. Log final delivery in `correspondence/`
4. Trigger SOP 02 (Client Follow-Up) flow
5. Archive the project folder in MinIO under `/archive/[year]/[client-slug]/`
→ Output: Project archived, follow-up sequence running

---

## Checkpoints

- **Before starting any milestone:** Confirm the previous milestone is client-approved in writing.
- **Before scope change work:** Written client approval in hand.
- **Before final delivery:** QA complete (SOP 05).

---

## Tools Required

- Project board (ClickUp / Notion / Linear)
- ERPNext (project and invoice records)
- MinIO (file archive)
- n8n (status update automation — optional)

---

## Failure Modes and Escalation

**Failure: Client goes silent after receiving deliverable**
Send one follow-up after 48 hours: *"Just checking in — did the [deliverable] come through okay?"* If no response after 5 business days, escalate: phone call. Log all contact attempts. If milestone sign-off is blocked, invoice is on hold — note this to client explicitly.

**Failure: Scope creep without formal change request**
If work has already been done outside scope: raise a change request immediately, even retroactively. Do not swallow uncompensated work without documentation. If the client disputes: reference the original scope document.

**Failure: Project runs over timeline**
Inform the client proactively — never let them discover a deadline miss by the silence. Provide a revised timeline with explanation and new delivery date confirmed in writing.

---

## Output / Handoff

Project management flow ends when:
- [ ] Final deliverable accepted in writing
- [ ] Final invoice issued
- [ ] ERPNext status = "Completed"
- [ ] SOP 02 (Follow-Up) sequence triggered
- [ ] Project folder archived in MinIO
