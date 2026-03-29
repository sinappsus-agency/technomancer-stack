# Automation Audit Template

**Chapter Reference:** Chapter 14 — n8n and the Automation Layer
**Usage:** Complete this audit over one working week. The output is your personalised automation roadmap.

---

## Week 1: Manual Task Log

For every manual task you perform during the week, log it in the table below.

| Date | Task Description | Time Taken | Frequency (daily/weekly/ad-hoc) | Data Pattern? | Reversible if Error? |
|------|-----------------|-----------|--------------------------------|---------------|---------------------|
| | | | | | |
| | | | | | |
| | | | | | |

**Instructions:**
- "Data Pattern?" = Does this task follow a consistent, predictable pattern every time? Yes / No / Usually
- "Reversible if Error?" = If the automation makes an error, can you easily undo it? Yes / No / Partially

---

## Week 2: Automation Candidates

After logging, apply these filters to identify your best automation candidates:

### Priority Tier 1 — Automate First

Criteria: Frequency ≥ 3x/week AND Data Pattern = Yes AND Reversible = Yes

| Task | Estimated Weekly Time Saved | n8n Template Starting Point |
|------|----------------------------|----------------------------|
| | | |
| | | |

### Priority Tier 2 — Automate Second

Criteria: Frequency ≥ 1x/week AND Data Pattern = Usually AND Reversible = Partially or Yes

| Task | Estimated Weekly Time Saved | Notes on Edge Cases |
|------|----------------------------|---------------------|
| | | |
| | | |

### Do Not Automate Yet

Criteria: Reversible = No, OR the task is changing frequently, OR I cannot specify the full pattern

| Task | Reason | When to Revisit |
|------|--------|----------------|
| | | |

---

## Automation Implementation Log

As you build automations, track them here:

| Automation Name | n8n Workflow File | Status | Last Tested | Weekly Time Saved |
|----------------|------------------|--------|-------------|------------------|
| | | Active / Draft / Paused | | |

---

## Common Starting Automations for Solo Agencies

Use these as quick wins to build your first workflows:

1. **New subscriber welcome sequence** — Webhook from website form → n8n → Notifuse sequence trigger
   Template: `crm-welcome-orientation.json`

2. **Meeting transcript to action items** — File upload to MinIO → n8n → AI processing → ERPNext tasks
   Template: `meeting-transcript-processor.json`

3. **Monday morning brief** — Scheduled → Pull data from Matomo + ERPNext → AI summarize → Telegram
   Template: `weekly-intelligence-brief.json`

4. **New client onboarding** — ERPNext quote acceptance → n8n → Project creation + email sequence + Telegram
   Template: `client-onboarding-trigger.json`

5. **Error monitoring for all workflows** — n8n error handler → Telegram alert + MinIO log
   Template: `error-handler-template.json`

6. **Three-touch email drip** — Notifuse subscriber tag event → n8n → Ollama generates personalised copy → Notifuse sends Day 0 / Day 3 / Day 7 emails automatically. Local AI copy generation, zero per-send cost.
   Template: `email-campaign-workflow.json`

7. **Inbound call → CRM update** — Call completion webhook from voice agent → n8n → Ollama analyses transcript → ERPNext contact + activity records created → Telegram alert on booking or escalation.
   Template: `call-center-crm-update.json`
   *Requires:* `agents/call-center/` voice agent running

---

## Quarterly Workflow Review

Every quarter, review your active automations:

- [ ] All active workflows executed at least once in the last 30 days (or are scheduled and not due yet)
- [ ] No workflows with repeated error notifications in the last 30 days that were not addressed
- [ ] No deprecated n8n nodes in active workflows (check n8n UI for warnings)
- [ ] Data volumes reasonable — no workflows consuming unexpectedly high resources
- [ ] Any new manual tasks in the task log that are now automation candidates?
