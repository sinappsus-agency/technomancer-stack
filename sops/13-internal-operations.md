# SOP 13 — Internal Operations

**Category:** Internal + Studio Health
**Version:** 1.0
**Owner:** Studio Lead
**Trigger:** Weekly + Monthly + Quarterly cadence
**Frequency:** Weekly (lightweight), Monthly (financial + content), Quarterly (strategic review)

---

## Objective

Run a solo or small studio with the operational discipline of a larger agency — without the meeting overhead. All internal reviews are time-boxed, documented, and feed directly into decisions. The output of each review is always a specific action, not just a status.

---

## Weekly Cadence

### Monday — Weekly Planning (30 minutes)

**Time block:** 09:00–09:30, first working day of the week

Steps:
1. Open `months/[month].md` — review current month status
2. Review ERPNext project board — update task statuses, flag anything blocked
3. Review pipeline (SOP 11) — any leads needing action this week?
4. Identify the 3 most important outcomes for the week (not tasks — outcomes)

Record in your monthly file under the current week heading:

```
## Week of [DD MMM]

Outcomes for this week:
1. 
2. 
3. 

Projects active:
-

Blockers / flags:
-
```

### Thursday — Client Status Dispatch (20 minutes)

For every active project, send a brief status update to the client (see SOP 03 — async update format). No call required. One message per project.

This is non-optional. Clients who do not hear from you weekly will fill the silence with concern.

### Friday — Weekly Wrap (20 minutes)

Steps:
1. Review the 3 outcomes set on Monday — which were hit? Which weren't?
2. Update ERPNext tasks — close completed, reprioritize open
3. Write a one-paragraph Slack/Notion note or voice memo: what got done, what didn't, why, what changes next week
4. Clear your inbox to zero (archive, not delete)
5. Close all browser tabs unrelated to ongoing work

---

## Monthly Cadence

### First Working Day — Monthly Review (90 minutes)

**Time block:** First Monday of each month, 09:00–10:30

Steps:
1. Financial review (SOP 10, Part C — full monthly review)
2. Content and marketing review:
   - What went out last month? (cross-ref `months/[month].md`)
   - What performed best? (Matomo for web traffic, LinkedIn/social analytics manually)
   - What will go out this month? (brief the content machine)
3. Client health check:
   - Any client at risk of not renewing or not returning?
   - Any client ready for an upsell conversation? (SOP 06)
4. SOP review: did anything break this month that requires an SOP update? Update it now while the failure is fresh.

Record in `months/[month].md`:

```
## Monthly Review — [Month] [Year]

Financial summary: [total invoiced / total received / outstanding]
Top-performing content: 
Client health flags:
SOP updates made:
Marketing plan for this month:
Key focus for this month:
```

---

## Quarterly Cadence

### Quarter-End Review (3 hours — do not cut this short)

Schedule in the last week of each quarter. Block a full morning or afternoon.

#### Section 1 — Results vs Objectives (60 minutes)

Review what you said you would do at the start of the quarter:
- Revenue target: hit / missed / by how much?
- Key projects: completed / delayed / cancelled?
- Capability goal (skill or tool): achieved?
- Content / marketing: what went out vs planned?

Be honest. The quarterly review is not a performance review where you manage up. It is a calibration tool.

#### Section 2 — Stack and Tool Audit (45 minutes)

Review every active subscription, tool, and service:

| Tool | Monthly cost | Still earning its keep? | Action |
|---|---|---|---|
| Contabo VPS | | | |
| n8n (self-hosted, no SaaS cost) | | | |
| ERPNext (self-hosted) | | | |
| Notifuse | | | |
| Matomo | | | |
| [Add others] | | | |

Decisions: Keep / Cancel / Replace / Renegotiate

Also audit the tech stack for security:
- Rotate secrets that haven't been rotated (see `docker/security-checklist.md`)
- Review open ports (Traefik dashboard should be internal only)
- Review contractor access — anyone still has access who shouldn't?

#### Section 3 — Offers and Positioning Review (30 minutes)

- Are the current service offers still the right ones?
- Is there a recurring request you keep getting that isn't a current offer?
- Is there an offer that nobody is buying? Kill it or fix it.
- What is the next productizable offer that could be added? (Reference: `Book/manuscript/appendices/appendix-i-sop-templates-reference.md`)

#### Section 4 — Next Quarter Objectives (45 minutes)

Set 3 objectives for the next quarter. Each objective must meet these criteria:
- It is specific (not "grow revenue" — "invoice R50k in branding projects")
- It is achievable in 90 days
- It requires a specific action, not just a circumstance

Format:

```
Q[X] [YEAR] OBJECTIVES

1. [Objective]: [Key actions to achieve it]: [How I will measure it]
2. [Objective]: [Key actions to achieve it]: [How I will measure it]
3. [Objective]: [Key actions to achieve it]: [How I will measure it]
```

Record in `months/[month].md` at the top of the new quarter's section.

---

## Annual Studio Review

Once per year (Q4 review expanded):

1. **Annual revenue vs targets:** Were the four quarterly targets met?
2. **Capability audit:** What can you build / design / execute today that you could not do 12 months ago?
3. **Client portfolio review:** Who are your best clients? What made them good? How do you attract more like them?
4. **SOP completeness:** Are all 13 SOPs in this directory current and trusted? When was each last used and validated?
5. **Studio positioning:** Is the current brand, persona, and offer set the right one for next year? What shifts?
6. **One-year vision:** Write one paragraph describing where the studio is in 12 months if the next year goes well.

---

## Automation Maintenance

The studio's automation infrastructure requires periodic maintenance:

### Monthly (15 minutes)
- Review n8n execution log: any workflows in error state?
- Check Uptime Kuma dashboard: any service down alerts in the last 30 days?
- Check MinIO storage usage: any bucket unexpectedly large?

### Quarterly (30 minutes)
- Review all n8n workflows: are any unused or broken?
- Check Docker container versions: any significantly out of date? (conservative upgrade: test in staging first)
- Review postgres disk usage on VPS
- Check Matomo analytics for site/dashboard performance

### Commands for quick health check:
```bash
# n8n execution log summary (recent errors)
docker logs n8n --since 24h | grep "error"

# All container status
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Disk usage
df -h
```

---

## Metrics to Track

Keep these simple. A metric you don't review is a metric you don't have.

| Metric | Where to find it | Review frequency |
|---|---|---|
| Monthly revenue invoiced | ERPNext - Sales Invoice | Monthly |
| Accounts receivable aging | ERPNext - AR Aged Summary | Monthly |
| Active clients | ERPNext - CRM | Monthly |
| New inbound leads | ERPNext - CRM Leads | Weekly |
| Website unique visitors | Matomo | Monthly |
| Email list size | Notifuse | Monthly |
| Content output (pieces published) | `months/[month].md` | Monthly |
| n8n workflow error rate | n8n execution log | Monthly |

---

## Tools Required

- ERPNext (financial + CRM review)
- Matomo (web analytics)
- Uptime Kuma (infrastructure monitoring)
- n8n (automation health)
- `months/[month].md` (operational record)
- Docker / Portainer (container health)

---

## Failure Modes

**Failure: Weekly review skipped repeatedly**
The studio runs on momentum. Missing three consecutive weekly reviews means you are operating reactively. The Monday planning block is non-negotiable. Set a recurring calendar event and treat it as client time.

**Failure: Quarterly review delayed to "when there's a quiet moment"**
There is never a quiet moment. It must be scheduled. The quarterly review is the single most high-leverage activity in this SOP library. Missing it costs more than any client project.

**Failure: Stack audit skipped in quarterly review**
Security regressions accumulate silently. One missed secret rotation or one forgotten access provision is how a breach happens. The stack audit is not optional.

---

## Output per Review

**Weekly:** Updated `months/[month].md` weekly block + clean ERPNext task board
**Monthly:** Full monthly review section in `months/[month].md`
**Quarterly:** Q objectives document + stack audit log + offers review notes
**Annual:** Annual review written summary, filed in `months/` folder for the relevant year
