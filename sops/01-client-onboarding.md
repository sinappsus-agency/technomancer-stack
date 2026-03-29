# SOP 01 — Client Onboarding

**Category:** Client Onboarding
**Version:** 1.0
**Owner:** Studio Lead
**Trigger:** New client agreement signed (DocuSign/PandaDoc completion notification received)
**Frequency:** Per new client engagement

---

## Objective

Move a newly signed client from agreement to first delivery meeting within **72 hours**, without dropped context, missed access grants, or jarring first impressions.

A client who experiences a smooth onboarding enters the project with higher confidence and lower micromanagement tendency.

---

## Prerequisites

- [ ] Agreement fully executed and stored in `brand-os/05-clients/[client-slug]/agreements/`
- [ ] Deposit invoice sent and payment confirmed (see SOP 10 — Financial Management)
- [ ] Client's primary contact details confirmed (name, email, phone, preferred communication channel)
- [ ] Project brief or scope summary available

---

## Steps

**Step 1 — Create client workspace**
You create a new folder at `brand-os/05-clients/[client-slug]/` with the following structure:
```
[client-slug]/
├── context.md          ← personal-ai-infrastructure context file
├── agreements/         ← signed contracts
├── briefs/             ← all project briefs
├── deliverables/       ← all work products
├── correspondence/     ← key emails, meeting notes
└── assets/             ← logos, brand files, source material provided by client
```
→ Output: client workspace folder created

**Step 2 — Populate context.md**
You complete `context.md` using the template in `agents/personal-ai-infrastructure/README.md`.
Fill in: who they are, what you're doing, their communication style, open loops.
→ Output: client AI context file ready for use in every session involving this client

**Step 3 — Trigger the n8n onboarding workflow**
You open n8n and run the `client-onboarding-trigger.json` workflow manually, OR it fires automatically from the DocuSign webhook.

This workflow:
- Creates the client record in ERPNext CRM with status "Onboarding"
- Sends the client a branded welcome email via Notifuse
- Creates the project record in your project management tool
- Posts a notification to your Telegram with client name and project type
→ Output: CRM record created, welcome email sent, Telegram notification received

**Step 4 — Send the onboarding questionnaire**
You send the onboarding questionnaire link to the client via their preferred channel.
The questionnaire covers: communication preference, availability, success definition, key stakeholders, constraints, examples they love/hate.
→ Output: Questionnaire sent, response awaited

**Step 5 — Grant access**
You provision access to all shared tools the engagement requires:
- Project board (ClickUp / Notion): invite with correct permission level (Comment or Edit, not Admin)
- Shared folder in MinIO or Google Drive
- Communication channel (Slack workspace or WhatsApp group)

⚠️ Never grant Admin access to any shared tool. Minimum necessary permissions only.
→ Output: Access confirmation sent to client

**Step 6 — Schedule the kickoff call**
You send 3 available time slots via your scheduling tool (Cal.com / Calendly).
Default kickoff call duration: 60 minutes.
→ Output: Kickoff call booked and confirmed

**Step 7 — Prepare the kickoff briefing doc**
You create `briefs/kickoff-prep.md` using the brief template.
This doc contains: confirmed scope, open questions, proposed milestones, your initial hypotheses.
→ Output: Kickoff prep doc ready before the call

---

## Checkpoints

- **Before Step 3:** Confirm deposit received. Do not begin onboarding workflow until payment clears.
- **Before Step 5:** Confirm the client has signed the questionnaire or at minimum responded to confirm receipt of onboarding email.
- **Before kickoff call:** Questionnaire responses reviewed. Any blocker questions identified.

---

## Tools Required

- n8n (onboarding workflow)
- ERPNext (CRM record)
- Notifuse (welcome email)
- Telegram (operator notification)
- Cal.com or Calendly (scheduling)
- MinIO or Google Drive (client assets)
- Your project management tool (ClickUp / Notion / Linear)

---

## Failure Modes and Escalation

**Failure: DocuSign webhook doesn't fire**
Check n8n workflow execution log. Manually trigger `client-onboarding-trigger.json` with client data. Confirm webhook URL is still active in DocuSign settings.

**Failure: Client doesn't respond to questionnaire within 48 hours**
Send one follow-up via their preferred channel. If no response after 72 hours, call (phone or video). Log the contact attempt in `correspondence/`. If unreachable for 5 business days, flag in Telegram and follow escalation protocol.

**Failure: Access grant bounces (wrong email)**
Verify email against the signed agreement. If mismatch, contact client to confirm the correct address. Update CRM and context.md with corrected address.

---

## Output / Handoff

Onboarding is complete when:
- [ ] CRM status updated to "Active"
- [ ] Kickoff call completed and notes filed in `correspondence/kickoff-notes.md`
- [ ] context.md updated with any new facts from kickoff call
- [ ] First milestone confirmed and in the project board
- [ ] SOP 04 (Project Management) is now the active SOP for this engagement
