# OpenClaw — AI Agent Integration

> **Maturity notice:** OpenClaw is a young, fast-moving open-source project. It works remarkably well for many tasks, but it is not production-hardened. Test every integration in isolation before connecting it to live customer-facing systems. Expect breaking changes between versions. The community is active and the pace of improvement is fast — check the GitHub changelog before upgrading.

---

## What Is OpenClaw

OpenClaw is an open-source personal AI agent that runs on your server. It is not a chatbot — it is an autonomous agent that can:

- Take actions on your behalf (send emails, browse the web, run shell commands, call APIs)
- Connect to messaging apps (Telegram, WhatsApp, Discord, Slack, iMessage) and respond from there
- Run cron jobs and heartbeat tasks in the background without being prompted
- Build and install its own skills by writing JavaScript plugins
- Operate multiple named instances as a "team" — each with its own persona, memory, and purpose
- Connect to any LLM (Anthropic Claude, OpenAI, Google Gemini, or local models via Ollama)

In the Technomancer stack, OpenClaw serves as the **AI operator layer** — the human-controlled brain that ties together n8n, ERPNext, Notifuse, WooCommerce, and the content machine into a single conversational interface accessible via Telegram.

---

## Architecture in This Stack

```
[Telegram / WhatsApp]
         │
         ▼
  ┌──────────────────────────────────┐
  │         OpenClaw Gateway          │
  │         (port 18789)              │
  │                                   │
  │  Model: Ollama llama3.2 (local)   │
  │  OR: Claude / GPT-4 API          │
  │                                   │
  │  Skills installed:                │
  │  ├── wordpress-woocommerce        │
  │  ├── n8n-trigger                  │
  │  ├── notifuse-campaigns           │
  │  ├── erpnext-crm                  │
  │  ├── postgres-query               │
  │  └── telegram-alerts              │
  └──────────────────────────────────┘
         │              │
         ▼              ▼
    [Ollama]      [n8n webhooks]
    (local LLM)   (automation)
         │              │
         ▼              ▼
  [PostgreSQL]    [ERPNext CRM]
  [WooCommerce]   [Notifuse]
```

---

## Setup

### Prerequisites

- The technomancer-stack Docker environment running (Traefik, Ollama, PostgreSQL, n8n)
- A Telegram bot token (from @BotFather) or a WhatsApp Business API connection
- Node.js 22 or 24 on the server (or run via Docker)
- An LLM API key (Anthropic Claude recommended) — or rely on Ollama for fully local inference

### Install OpenClaw on VPS

```bash
# SSH into your Contabo VPS, then:
curl -fsSL https://openclaw.ai/install.sh | bash

# Run onboarding (installs daemon + configures LLM + Telegram)
openclaw onboard --install-daemon

# Or to use Ollama as the model provider:
# When prompted for model provider, select "Ollama"
# Enter endpoint: http://localhost:11434
# Enter model: llama3.2:3b

# Verify gateway is running
openclaw gateway status

# Open dashboard in browser
openclaw dashboard
```

### Docker Deployment (alternative)

Add to `docker/docker-compose.yml`:

```yaml
  ##############################################################################
  # OPENCLAW — AI agent platform
  # Access gateway at: agent.yourdomain.com (internal dashboard)
  ##############################################################################
  openclaw:
    image: node:22-alpine
    container_name: openclaw
    restart: unless-stopped
    networks:
      - traefik-public
      - backend
    working_dir: /app
    command: sh -c "npm install -g openclaw && openclaw gateway start"
    environment:
      OPENCLAW_MODEL_PROVIDER: ollama
      OPENCLAW_OLLAMA_HOST: http://ollama:11434
      OPENCLAW_OLLAMA_MODEL: llama3.2:3b
      OPENCLAW_TELEGRAM_TOKEN: ${OPENCLAW_TELEGRAM_TOKEN}
      OPENCLAW_SECRET: ${OPENCLAW_SECRET}
    volumes:
      - openclaw-data:/root/.openclaw
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.openclaw.rule=Host(`agent.${BASE_DOMAIN}`)"
      - "traefik.http.routers.openclaw.entrypoints=websecure"
      - "traefik.http.routers.openclaw.tls=true"
      - "traefik.http.routers.openclaw.tls.certresolver=letsencrypt"
      - "traefik.http.services.openclaw.loadbalancer.server.port=18789"
```

Add volume:
```yaml
volumes:
  openclaw-data:
```

Add to `.env.example`:
```
OPENCLAW_TELEGRAM_TOKEN=your_telegram_bot_token
OPENCLAW_SECRET=replace_with_strong_secret
```

---

## Skills to Install

OpenClaw uses a skill system (JavaScript plugins) that extend what it can do. Install from [ClawHub](https://clawhub.ai/) or write your own.

### Install from ClawHub

```bash
# Connect to OpenClaw via Telegram and type:
# "install skill wordpress" — will find and install WordPress skill

# Or via CLI:
openclaw skill install wordpress
openclaw skill install browser
openclaw skill install github
```

### Custom Skills for This Stack

The following skills are not on ClawHub but are straightforward to build in a chat session with OpenClaw. Ask it to build each one:

**"Build me a skill that queries WooCommerce orders"**
- Uses WooCommerce REST API (Consumer Key + Secret from WP Admin → WooCommerce → Settings → Advanced → REST API)
- Endpoint: `GET https://shop.yourdomain.com/wp-json/wc/v3/orders?per_page=10&orderby=date`
- Returns: today's sales count, total revenue, pending orders

**"Build me a skill that triggers an n8n workflow by name"**
- Uses n8n API: `POST https://workflow.yourdomain.com/api/v1/workflows/{id}/activate`
- Or fires a named webhook: `POST https://workflow.yourdomain.com/webhook/[slug]`
- This lets you say "Start the email campaign for segment: new-leads"

**"Build me a skill that sends a Notifuse campaign"**
- Uses Notifuse API to trigger a pre-built campaign to a segment
- Returns confirmation of send count

**"Build me a skill that queries my CRM leads"**
- Connects to ERPNext REST API
- `GET https://erp.yourdomain.com/api/resource/Lead?filters=[["status","=","Open"]]`
- Returns open leads count + summary

**"Build me a skill that queries PostgreSQL directly"**
- Uses `pg` npm package to run read-only queries
- Useful for custom reports: calls logged, email campaign stats, etc.

---

## Integration Workflows

### 1. WooCommerce Sales Briefing (Daily Cron)

After installing the WooCommerce skill, ask OpenClaw to set up a daily briefing:

> "Every morning at 8am, check yesterday's WooCommerce sales and send me a summary on Telegram. Include: total orders, total revenue, any orders still pending fulfillment, and any failed payments."

OpenClaw will create a cron skill that runs automatically. No manual trigger needed.

### 2. Lead Funnel Auto-Reply

Connect OpenClaw to your WooCommerce webhook for new form submissions (WPForms / Gravity Forms):

> "When a new lead comes in from the website contact form (via n8n webhook to my OpenClaw), reply to them within 5 minutes with a personalised welcome message based on what they said they need. Then log their details in ERPNext as a new lead. Then add them to the Notifuse welcome sequence."

Implement this by:
1. In n8n: create a webhook trigger on new WPForms submission → POST to OpenClaw webhook endpoint
2. OpenClaw receives the lead data, uses LLM to draft a personalised reply, sends via Gmail/Notifuse skill
3. Simultaneously logs in ERPNext and triggers Notifuse via API

### 3. Notifuse Campaign Generation

Ask OpenClaw to draft email campaigns based on recent content:

> "Look at the last 3 blog posts on our WordPress site. Draft a 3-email nurture campaign that references each one. Format each email as: subject line, preview text, body (under 300 words), CTA. Post the drafts to Telegram for my approval before sending."

The approval gate is important — always add "post drafts for my approval" to campaign generation tasks.

### 4. n8n Workflow Trigger via Chat

> "Trigger my weekly intelligence brief workflow in n8n"

OpenClaw fires the n8n webhook → n8n executes the full workflow → results posted back to Telegram.

This turns n8n into a voice/message-controlled automation system rather than a purely scheduled one.

### 5. Meta Ads Monitoring (Browser Skill)

> "Every Monday at 9am, open the Meta Ads Manager, screenshot the performance summary for this week, and send it to me on Telegram."

OpenClaw uses its browser skill to log in and extract data. This works but is fragile — Meta's UI changes frequently. Use the Meta Graph API via a custom skill where possible for reliability.

---

## Multi-Agent Setup

You can run multiple named OpenClaw instances on the same server, each with its own persona and Telegram bot:

| Agent Name | Purpose | Telegram Bot |
|---|---|---|
| Studio Lead (main) | Strategy, decisions, briefings | @YourMainBot |
| Content Assistant | Content drafts, scheduling | @ContentBot |
| Sales Agent | Lead qualification, CRM updates | @SalesBot |
| Ops Agent | Server monitoring, backups | @OpsBot |

Each agent has separate memory and context. They can collaborate by sharing a group Telegram chat where each bot is a member.

**Set up a second instance:**
```bash
openclaw instance create --name content-assistant --port 18790
openclaw instance content-assistant onboard
```

---

## Caveat: Limitations to Know Before Deploying

OpenClaw is young (launched in 2025). It is genuinely powerful but has real limitations:

1. **Skills can break** — if the target UI or API changes, the skill needs updating. Treat all skills as "probably works, verify before trusting with live data."

2. **Local model quality** — using `llama3.2:3b` keeps costs at zero but the reasoning quality is lower than Claude or GPT-4. For complex multi-step tasks, use an API model and set a budget limit.

3. **Self-modification risk** — OpenClaw can modify its own skills and system prompt. This is a feature but also a risk. Back up `~/.openclaw` before major updates.

4. **No built-in auth for webhooks** — when exposing OpenClaw to receive webhooks (e.g., from n8n), add a shared secret header check in your skill code.

5. **Memory is not encrypted by default** — the agent's memory store is plain JSON files. Store credentials in Vaultwarden and pull them into skills at runtime rather than storing them in memory.

6. **Version volatility** — the project updates frequently. Pin to a specific version in production: `npm install -g openclaw@x.x.x` rather than `@latest`.

---

## Chapter Reference

This integration is covered in **Chapter 9 — Running AI Locally** in TECHNOMANCER: The One-Person Superbrand.
