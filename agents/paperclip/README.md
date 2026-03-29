# Paperclip — Agent Workforce Control Plane

> **Maturity notice:** Paperclip is a new platform built for the emerging AI-agent workforce paradigm. The concept it solves for is real and increasingly important as you run multiple agents simultaneously — but the tooling is actively evolving. Treat it as a powerful organising layer for your agent fleet, not as a mission-critical production system. Test thoroughly before relying on it to govern anything that touches live client data or payments.

---

## What Is Paperclip

Paperclip is the **command, communication, and control plane** for a company of AI agents. Think of it as the "management layer" that sits above your individual agents (OpenClaw instances, n8n workflows acting as agents, the call center AI, etc.).

A solo operator running multiple AI agents needs to answer these questions at a glance:
- Which agent is working on what right now?
- Is any agent stuck, looping, or burning tokens on nothing useful?
- How much am I spending on LLM inference this week, and which agent is consuming the most?
- Is an agent about to take an action that requires my approval first?
- Which agents are supposed to report to which level of authority?

Paperclip answers all of these.

**What it is NOT:** Paperclip does not run agents. It orchestrates them. Agents run wherever they run (OpenClaw on the VPS, n8n workflows, shell scripts) and "phone home" to Paperclip. The control plane stays clean and separate from execution.

---

## Architecture

```
┌─────────────────────────────────────────────┐
│             PAPERCLIP CONTROL PLANE          │
│                                              │
│   Org Chart (who reports to whom)            │
│   Task Registry (what's assigned + status)   │
│   Budget Ledger (token spend per agent)      │
│   Goal Hierarchy (what serves what)          │
│   Audit Trail (what every agent did)         │
│   Approval Gates (board-level decisions)     │
└──────────────────┬──────────────────────────┘
                   │ HTTP API
       ┌───────────┴───────────┐
       │                       │
       ▼                       ▼
┌─────────────┐       ┌──────────────────┐
│  OpenClaw   │       │   n8n Workflow    │
│  Agents     │       │  (adapter)        │
│  (executor) │       │  (executor)       │
└─────────────┘       └──────────────────┘
       │                       │
       ▼                       ▼
 Phone home to          Phone home to
 Paperclip via          Paperclip via
 HTTP adapter           HTTP adapter
```

---

## The Two Layers

### Layer 1: Control Plane (Paperclip)

The central nervous system. Manages:
- **Agent registry** — every agent is an "employee" with a role, reporting line, and token budget
- **Org chart** — whose directions does each agent follow? What can it decide alone?
- **Task assignment** — tasks are dispatched to agents; Paperclip tracks status (queued → running → complete → failed)
- **Budget enforcement** — each agent has a token salary. When budget is exhausted, the agent pauses until you approve more
- **Goal alignment** — agents see how their current task connects to the studio's top-level objectives
- **Heartbeat monitoring** — if an agent stops checking in, Paperclip flags it

### Layer 2: Execution Adapters

Paperclip does not care how an agent runs. If it can call an HTTP endpoint, it is an agent. Adapters exist for:
- **Claude Code** — coding tasks
- **OpenAI Codex** — coding tasks via OpenAI
- **Shell processes** — any command-line tool
- **HTTP webhooks** — n8n workflows, custom scripts, the call center handler

In the Technomancer stack, the adapters are:
- OpenClaw agent instances (via their gateway API)
- n8n workflows (via webhook URLs)
- The call center handler (via its HTTP endpoint)

---

## How to Set Up Paperclip

### Prerequisites

- Node.js 18+ on the VPS
- The Paperclip package (install via npm)
- A running technomancer-stack (agents need to exist before you manage them)

### Install

```bash
npm install -g @paperclipai/cli

paperclip init
# Follow the wizard — creates ~/.paperclip with org config
```

### Define Your Organisation

```yaml
# ~/.paperclip/org.yaml
name: "Technomancer Studio"
mission: "Build and run the one-person superbrand"

goals:
  - id: studio-revenue
    name: "Monthly Recurring Revenue"
    target: "R50,000 MRR by Q4"
  - id: content-output
    name: "Weekly Content"
    target: "4 published pieces per week across all channels"
  - id: client-satisfaction
    name: "Client Satisfaction"
    target: "NPS > 70 at every 90-day review"
```

### Register Agents

```yaml
# ~/.paperclip/agents.yaml

agents:
  - id: studio-lead
    name: "Studio Lead (OpenClaw)"
    role: "Strategic decisions, briefings, client communication oversight"
    reports_to: operator          # the human
    budget_tokens_per_day: 100000
    adapter:
      type: http
      endpoint: http://openclaw:18789/api/task
      auth_header: "X-OpenClaw-Secret"
      auth_token: "${OPENCLAW_SECRET}"

  - id: content-agent
    name: "Content Agent (OpenClaw)"
    role: "Draft and schedule content across all channels"
    reports_to: studio-lead
    budget_tokens_per_day: 80000
    adapter:
      type: http
      endpoint: http://openclaw-content:18790/api/task
      auth_header: "X-OpenClaw-Secret"
      auth_token: "${OPENCLAW_SECRET}"

  - id: n8n-automation
    name: "Automation Engine (n8n)"
    role: "Execute structured workflows, CRM updates, email sends"
    reports_to: studio-lead
    budget_tokens_per_day: 20000    # n8n uses Ollama via HTTP calls
    adapter:
      type: webhook
      endpoint: https://workflow.yourdomain.com/webhook/paperclip-task
      auth_token: "${N8N_WEBHOOK_SECRET}"

  - id: voice-agent
    name: "Call Center (AI Voice)"
    role: "Handle inbound calls, qualify leads, book appointments"
    reports_to: studio-lead
    budget_tokens_per_day: 30000
    adapter:
      type: webhook
      endpoint: http://call-handler:3000/paperclip-task
      auth_token: "${DRACHTIO_SECRET}"
```

### Add Paperclip to Docker Compose

```yaml
  ##############################################################################
  # PAPERCLIP — Agent workforce control plane
  ##############################################################################
  paperclip:
    image: node:22-alpine
    container_name: paperclip
    restart: unless-stopped
    networks:
      - traefik-public
      - backend
    working_dir: /app
    command: sh -c "npm install -g @paperclipai/cli && paperclip server start"
    environment:
      PAPERCLIP_SECRET: ${PAPERCLIP_SECRET}
    volumes:
      - paperclip-data:/root/.paperclip
      - ./config/paperclip:/root/.paperclip/config:ro
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.paperclip.rule=Host(`agents.${BASE_DOMAIN}`)"
      - "traefik.http.routers.paperclip.entrypoints=websecure"
      - "traefik.http.routers.paperclip.tls=true"
      - "traefik.http.routers.paperclip.tls.certresolver=letsencrypt"
      - "traefik.http.services.paperclip.loadbalancer.server.port=4000"
```

Add to `docker/docker-compose.yml` volumes:
```yaml
  paperclip-data:
```

Add to `.env.example`:
```
PAPERCLIP_SECRET=replace_with_strong_secret
```

---

## Daily Use

### View the Dashboard

```bash
paperclip status
# or open: https://agents.yourdomain.com
```

Output:
```
TECHNOMANCER STUDIO  —  Agent Status
─────────────────────────────────────────────
Studio Lead       ● Active    task: "Draft client proposal for Mango Brand"
Content Agent     ● Idle      last run: 2h ago
n8n Automation    ● Running   task: "Weekly intelligence brief" (step 3/7)
Voice Agent       ○ Standby   calls today: 4 / leads: 2

Budget burn today:  Studio Lead 12,400 tokens  │  Content 8,200  │  n8n 3,100
Total:  23,700 / 230,000 daily budget  (10.3%)
─────────────────────────────────────────────
⚠  Content Agent exceeded budget at 14:30. Paused. Type 'paperclip approve budget content-agent +50000' to continue.
```

### Assign a Task

```bash
paperclip task assign "Analyse last month's WooCommerce sales and write a one-page performance summary" --agent studio-lead --goal studio-revenue
```

### View Audit Trail

```bash
paperclip audit --agent voice-agent --last 24h
```

### Approve a Budget Extension

```bash
paperclip approve budget content-agent +50000
```

### Set an Approval Gate

For high-stakes tasks (e.g., sending emails to your full list, posting publicly, making API calls to paid services), add a gate:

```bash
paperclip gate add "send email campaign" --requires operator-approval
```

Any agent attempting an action matching this description will pause and send a Telegram alert to the operator for approval before proceeding.

---

## Integration with OpenClaw

OpenClaw and Paperclip complement each other:

- **OpenClaw** is the conversational execution layer — it understands natural language instructions and can take real actions
- **Paperclip** is the governance layer — it ensures agents operate within defined budgets, org structures, and approval requirements

The simplest integration:
1. Paperclip assigns a task to OpenClaw via HTTP
2. OpenClaw executes the task (using its skills and LLM reasoning)
3. OpenClaw posts the result back to Paperclip's task endpoint
4. Paperclip logs the completion, deducts tokens from budget, updates task status

The operator sees all of this in the Paperclip dashboard and can intervene at any point via Telegram.

---

## Org Chart for the One-Person Studio

```
OPERATOR (you)
     │
     ▼
STUDIO LEAD AGENT
(OpenClaw — strategic decisions, client comms, briefings)
     │
     ├──▶ CONTENT AGENT
     │    (OpenClaw — drafts, scheduling, repurposing)
     │
     ├──▶ AUTOMATION ENGINE (n8n)
     │    (workflows, CRM, email, data processing)
     │
     └──▶ VOICE AGENT
          (call center AI — inbound leads, appointment booking)
```

Each level can only direct agents below it in the chart. The content agent cannot trigger n8n workflows directly — that request goes up to the studio lead, which dispatches to n8n. This prevents agents from taking arbitrary actions outside their scope.

---

## Limitations and Known Caveats

1. **Very new platform** — Paperclip's adapter ecosystem is minimal at launch. Expect to write glue code for some integrations.

2. **No visual dashboard yet** — the current interface is CLI-first. The web dashboard is in development. Expect this to improve quickly.

3. **Adapter reliability depends on agent availability** — if OpenClaw's gateway is down, Paperclip sees the task as failed. Build retry logic into critical workflows.

4. **Budget tracking is approximate** — Ollama does not report token counts the same way Claude/OpenAI does. Budget numbers for local model agents are estimates based on text length heuristics.

5. **Multi-agent coordination is not yet real-time** — agents do not communicate directly through Paperclip right now. Coordination happens via shared data (PostgreSQL, n8n webhooks). Direct agent-to-agent messaging is on the roadmap.

6. **Not a replacement for human oversight** — the approval gate system is only as strong as your configuration. Set up gates for any action that is expensive, irreversible, or customer-facing.

---

## Chapter Reference

Paperclip is covered in **Chapter 9 — Running AI Locally** in TECHNOMANCER: The One-Person Superbrand, alongside OpenClaw and the MCP server layer. Together they form the complete AI infrastructure for the one-person superbrand.
