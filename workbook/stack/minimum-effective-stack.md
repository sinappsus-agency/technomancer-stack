# Minimum Effective Stack Planner

**Purpose:** Define the smallest set of tools that fully supports your current business stage — before adding complexity.

The principle: the best stack is the one you actually use, not the one that is theoretically complete.

---

## Part 1: Business Stage Assessment

Before planning your stack, identify your current stage. This changes which components are essential vs. premature.

**Circle your current stage:**

| Stage | Revenue | Team | Complexity Needed |
|-------|---------|------|-------------------|
| **Exploration** | Pre-revenue or <$12k/yr | Solo | Minimum viable stack only |
| **Validation** | $12–60k/yr | Solo or 1-2 contractors | Core automation + basic CRM |
| **Growth** | $60–250k/yr | Small team | Full stack justified |
| **Scale** | $250k+/yr | Team | Full stack + custom tooling |

**My current stage:** ______________________

---

## Part 2: The Minimum Viable Stack for Your Stage

### Stage: Exploration

You need to focus on finding what works — not on running infrastructure.

**Minimum Viable Stack:**

| Function | Tool | Cost |
|----------|------|------|
| AI assistant | Claude / ChatGPT (subscription) | $20/month |
| Notes + writing | Notion or Obsidian | Free |
| Email | Gmail or Fastmail | Free–$5/month |
| Simple automation | n8n Cloud (free tier) or Make (free tier) | $0 |
| Client communication | Email + Calendly | Free |
| **Total** | | **~$25/month** |

**Do NOT add at this stage:** VPS, self-hosted services, ERPNext, custom domains for services

---

### Stage: Validation

You have a service that works. Now you need to systematise delivery and track what's performing.

**Minimum Viable Stack:**

| Function | Tool | Cost |
|----------|------|------|
| AI (writing + code) | Claude Pro + GitHub Copilot | $30/month |
| Automation | n8n Cloud Starter or self-hosted | $0–$20/month |
| CRM + email | Notifuse (self-hosted) | VPS only |
| File storage | MinIO (self-hosted) | VPS only |
| Analytics | Matomo (self-hosted) | VPS only |
| VPS (runs above) | Contabo VPS S | €5/month |
| **Total** | | **~$55–$75/month** |

**Add these when validated:** Full ERPNext, Terraform, advanced AI agents

---

### Stage: Growth

Revenue is proven. Systematise everything and start building the full Technomancer Stack.

**Full Stack — see:** `docker/docker-compose.yml` and `technomancer-stack/README.md`

At this stage, also consider activating the optional layers:

| Optional Layer | What it adds | When to add |
|---------------|-------------|-------------|
| **WordPress + WooCommerce** | Self-hosted storefront for digital products, templates, or courses. Zero transaction fees. | When you have a product to sell |
| **OpenClaw (AI agent)** | Phone-accessible agent that monitors your stack and executes tasks from Telegram. | When you're managing multiple services daily and want a unified interface |
| **Paperclip (agent control plane)** | Governance, budget tracking, and audit trails for multiple agents. | When you have 2+ agents running and need cost visibility |
| **Call Center voice agent** | Automated inbound call handling with AI transcription and CRM update. | When inbound call volume justifies automation (consult + test before production) |

**Setup guides for all optional layers:** `workbook/agents/agent-deployment-checklist.md`

---

## Part 3: Stack Decision Worksheet

For each tool you are considering adding, complete this row:

| Tool | Function | Do I have this covered already? | Frequency of need | Decision |
|------|----------|--------------------------------|-------------------|----------|
| | | Yes / No / Partially | Daily / Weekly / Rarely | Add / Defer / Skip |

**Decision criteria:**
- If frequency is Rarely → Skip unless critical
- If function is already covered → Skip
- If frequency is Daily and not covered → Add immediately
- If frequency is Weekly → Defer until growth stage

---

## Part 4: The Stack You Have Now

List every tool you are currently paying for or regularly using:

| Tool | Cost/Month | Primary Usage | Hours/Week I Use It | Keep / Replace / Drop |
|------|-----------|---------------|---------------------|----------------------|
| | | | | |
| | | | | |
| | | | | |

**Total current spend:** $____________/month

**After review — tools to drop:** ________________________________

**After review — tools to replace with OSS:** ________________________________

**Projected post-migration spend:** $____________/month

---

## Part 5: 90-Day Stack Migration Plan

| Week | Action | Tool Being Added / Replaced | Status |
|------|--------|---------------------------|--------|
| 1–2 | VPS setup and Traefik | Contabo VPS | |
| 3–4 | n8n self-hosted | Replace: Zapier/Make | |
| 5–6 | Notifuse + email | Replace: Mailchimp/Beehiiv | |
| 7–8 | MinIO | Replace: Google Drive / Dropbox | |
| 9–10 | Matomo | Replace: Google Analytics | |
| 11–12 | Ollama local AI | Supplement: OpenAI API | |

Customise this plan based on your current stack and priorities.

---

*See also:* `workbook/automation/automation-audit-template.md` — once your stack is in place, audit which tasks to automate first.
