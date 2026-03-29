# SOP 09 — Training and Contractor Onboarding

**Category:** Training + Development
**Version:** 1.0
**Owner:** Studio Lead
**Trigger:** New contractor or collaborator engaged
**Frequency:** Per new hire or contractor

---

## Objective

Enable any contractor or collaborator to reach operating standard within 48 hours — without bespoke orientation, repeated explanations, or the Studio Lead becoming a bottleneck.

---

## Prerequisites

- [ ] Contractor agreement signed and filed
- [ ] First project or task identified
- [ ] Access to tools provisioned (see Step 3)

---

## Steps

**Step 1 — Send the pre-start package (48 hours before first day)**
Email the contractor:
- Studio onboarding guide (this SOP links to it)
- Brand voice primer (`prompts/brand/origin-stack-refinement.md`)
- Communication norms summary (SOP 08 summary)
- Project brief for their first task
- Login credentials or access invites for all required tools

**Step 2 — Schedule a 30-minute orientation call**
First day, first interaction. Not a task briefing — a context briefing.

Orientation call agenda:
1. Who the studio is and what it stands for (5 min)
2. How communication works (5 min — reference SOP 08)
3. How projects are tracked (5 min — project board walkthrough)
4. Their specific engagement: what they own, what success looks like (10 min)
5. Questions (5 min)

**Step 3 — Provision access (minimum necessary permissions)**
Provision access to exactly the tools they need for their role. Nothing more.

| Role type | Access provisioned |
|---|---|
| Copywriter | Project board (writer permission), Slack, brand prompts folder |
| Designer | Project board, Slack, MinIO brand assets bucket (read), Figma project |
| Developer | Project board, Slack, GitHub repository, Staging environment only (not production) |
| VA / Coordinator | Project board (admin for their projects), Slack, ERPNext (limited view) |

⚠️ No contractor gets production database access, Traefik admin, n8n admin, or Vaultwarden access.
⚠️ All access is provisioned with a review date (90 days). Unused access is revoked.

**Step 4 — Share the quality standard**
The quality standard is not communicated verbally — it is documented. Share:
- SOP 05 (QA checklist relevant to their deliverable type)
- 2–3 examples of past work that represents the quality bar
- One example of work that did NOT meet the standard and why (if available)

**Step 5 — First deliverable review**
On the first task delivered by a new contractor:
- Run SOP 05 (QA) fully — do not shortcut it on the first submission
- Give structured written feedback using this format:

```
FEEDBACK — [CONTRACTOR NAME] — [DELIVERABLE] — [DATE]

WHAT WORKED:
- 

WHAT NEEDS CHANGING:
- [Specific item]: [Why it matters] + [How to fix it]

STANDARD REFERENCE:
- [Link or quote from brand guide / SOP that applies]
```

Send feedback via Slack, not email. Keep it in the project channel context.

**Step 6 — 2-week check-in**
Two weeks after start, 15-minute call:
- Is everything clear?
- Is there anything in the process that feels unclear or broken?
- Any resource they need that wasn't provided?

Update any gaps found. This is a feedback loop for SOP improvement, not performance review.

---

## Skill Library

Maintain a shared reference library for common skills required in the studio:

| Resource | Location | For |
|---|---|---|
| Brand voice guide | `prompts/brand/` | All creative roles |
| QA checklists | `sops/05-quality-assurance.md` | All delivery roles |
| Project board guide | Internal Notion doc | All roles |
| Stack overview | `docker/README.md` | Technical roles |
| n8n workflow map | `n8n-templates/README.md` | Automation roles |

---

## Offboarding

When a contractor engagement ends:
1. Revoke all tool access within 24 hours of final delivery
2. Rotate any shared passwords they had access to
3. Archive their project contributions to MinIO
4. Log engagement summary in ERPNext (quality, reliability, re-engage: yes/no)

---

## Tools Required

- Email (pre-start package)
- Slack / Discord (communication)
- Project board (access provisioning)
- MinIO (brand assets access)
- ERPNext (contractor record)
- Vaultwarden (credential management — never share master vault)

---

## Failure Modes and Escalation

**Failure: Contractor delivers below standard on first task**
Do not accept substandard work silently. Use the structured feedback format above. One revision cycle. If still below standard after revision, this is a fit issue — address directly and close the engagement.

**Failure: Contractor asks questions already answered in the onboarding doc**
Update the doc to make the answer clearer. One clarification is a question; two on the same topic is a documentation gap.

**Failure: Access not revoked after engagement ends**
This is a security failure. See `docker/security-checklist.md`. Run the access audit immediately.

---

## Output / Handoff

Onboarding complete when:
- [ ] Orientation call done
- [ ] All access provisioned
- [ ] Brand voice + QA standards shared
- [ ] First task reviewed with structured feedback
- [ ] 2-week check-in scheduled
