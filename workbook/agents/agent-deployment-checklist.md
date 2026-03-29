# Agent Deployment Checklist

**Chapter References:** Chapter 9 — Running AI Locally | Chapter 14 — n8n and the Automation Layer
**Usage:** Work through each section in order. Each checklist item has a corresponding step in the agent's README. Complete one agent fully before moving to the next.

> **Maturity note:** The agent tools in this stack (OpenClaw, Paperclip, the voice call center) are relatively new platforms. They work for the documented use cases, but edge cases exist and some features are still maturing. Test each agent on low-stakes tasks before trusting it with live production data or financial records.

---

## Section 1: Prerequisites (Complete Before Any Agent Setup)

Before deploying any agent, confirm the base stack is healthy:

- [ ] Docker stack is running (`docker compose ps` — all services show `Up`)
- [ ] Ollama is responding (`curl http://localhost:11434/api/tags` returns a model list)
- [ ] At least one model is pulled (`ollama list` shows at least `llama3.2:3b`)
- [ ] n8n is accessible at `workflow.yourdomain.com`
- [ ] A Telegram bot token is ready (create via @BotFather — you need this for OpenClaw and Paperclip alerts)
- [ ] Your `.env` file has `OPERATOR_TELEGRAM_ID` set (your numeric Telegram user ID)

---

## Section 2: WordPress + WooCommerce Setup

**Purpose:** Self-hosted e-commerce storefront for digital products, templates, or courses.

**Time required:** 60–90 minutes for initial setup.

### Step 1: Deploy the services

```bash
# From the technomancer-stack/docker/ directory:
docker compose up -d wordpress mariadb
```

Confirm both services are running:
```bash
docker compose ps | grep -E "wordpress|mariadb"
```

### Step 2: First-run configuration

```bash
# Install WooCommerce and PDF invoices plugin
docker compose run --rm wp-cli plugin install woocommerce --activate
docker compose run --rm wp-cli plugin install woocommerce-pdf-invoices-packing-slips --activate
```

### Step 3: WooCommerce wizard

Navigate to `shop.yourdomain.com/wp-admin` and complete the setup wizard:

- [ ] Store location and currency confirmed
- [ ] Stripe plugin installed for card payments (`wp-cli plugin install woocommerce-gateway-stripe --activate`)
- [ ] At least one product created and set to Published
- [ ] WooCommerce → Settings → Advanced → Webhooks → New webhook created pointing to your n8n `call-center-crm-update` or `client-onboarding-trigger` workflow

### Step 4: Test

- [ ] Complete a test purchase using Stripe test mode
- [ ] Confirm the order appears in WooCommerce → Orders
- [ ] Confirm the n8n webhook fires (check n8n Executions log)

**Reference:** `docker/docker-compose.yml` — `wordpress`, `mariadb`, `wp-cli` service definitions.

---

## Section 3: OpenClaw Setup

**Purpose:** AI agent accessible from Telegram. Monitors your stack, executes tasks, delivers briefings — all from your phone.

**Time required:** 45–60 minutes for initial setup and skill installation.

### Step 1: Install OpenClaw on the server

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
openclaw onboard --install-daemon
```

During onboarding you will be prompted for:
- Your Ollama endpoint (use `http://localhost:11434` on the same server)
- Your Telegram bot token (from @BotFather)

### Step 2: Configure environment variables

Add to your `.env` file (reference: `docker/.env.example`):

```
OPENCLAW_OLLAMA_HOST=http://ollama:11434
OPENCLAW_MODEL=llama3.2:3b
```

### Step 3: Verify the agent is responding

- [ ] Send `/start` to your Telegram bot
- [ ] Agent responds with a greeting
- [ ] Send `what time is it?` — agent should respond correctly (tests basic inference)

### Step 4: Install skills

In a Telegram conversation with your agent, paste each of these prompts one at a time. The agent will write and install its own plugin:

**Prompt 1 — WooCommerce:**
```
Build a skill that queries WooCommerce orders for today. Use the WooCommerce REST API at WOOCOMMERCE_URL with consumer key WOOCOMMERCE_CONSUMER_KEY and consumer secret WOOCOMMERCE_CONSUMER_SECRET. Return the count and total revenue.
```

**Prompt 2 — n8n trigger:**
```
Build a skill that triggers an n8n webhook by workflow name. Accept a workflow_name parameter and POST to http://n8n:5678/webhook/{workflow_name}. Confirm the trigger was received.
```

**Prompt 3 — ERPNext CRM:**
```
Build a skill that lists my current open leads in ERPNext. Use the ERPNext REST API at ERPNEXT_URL with API key authentication. Return lead name, company, and status for the last 10 open leads.
```

After each installation:
- [ ] Test the skill with a real query
- [ ] Confirm the response matches actual data

### Step 5: Set up a morning briefing cron

Add this cron task to OpenClaw's configuration (via `openclaw dashboard`):

```
Schedule: 0 7 * * 1-5
Instruction: Run the daily briefing: check WooCommerce orders from yesterday, check ERPNext leads created this week, and report any active n8n workflow errors. Format as a short bullet list.
```

- [ ] Cron task created
- [ ] Tested manually with `openclaw task run morning-briefing`
- [ ] First automated briefing received on schedule

**Multi-agent (optional):** If you want separate agents for content and sales work, run a second instance:
```bash
openclaw instance create --name content-agent --port 18790 --telegram-bot YOUR_CONTENT_BOT_TOKEN
```

**Reference:** `agents/openclaw/README.md`

---

## Section 4: Paperclip Setup

**Purpose:** Governance and visibility layer for multiple agents. Tracks tasks, enforces budgets, provides audit trails.

**When to add:** After you have OpenClaw running AND at least one other agent or n8n workflow endpoint active. Paperclip adds value at the point where you need visibility across more than one agent.

**Time required:** 30–45 minutes.

### Step 1: Install the Paperclip CLI

```bash
npm install -g @paperclipai/cli
paperclip init
```

The init wizard will ask for your workspace name and create `~/.paperclip/config.yaml`.

### Step 2: Define your organisation

Create `agents/paperclip/org.yaml`:

```yaml
org:
  name: Your Studio Name
  mission: Operate a sovereign solo creative studio at scale
  operator: your-telegram-handle

goals:
  - Deliver client work on schedule with consistent quality
  - Maintain studio presence and lead capture without founder attention
  - Keep AI infrastructure costs under €50/month
```

### Step 3: Register your agents

Create `agents/paperclip/agents.yaml` (edit to match your actual endpoints):

```yaml
agents:
  - name: studio-lead
    description: OpenClaw instance. Handles briefings, WooCommerce queries, ERPNext.
    adapter:
      type: http
      base_url: http://openclaw:18789
    budget:
      daily_tokens: 50000

  - name: n8n-automation
    description: n8n workflow engine for scheduled and event-triggered automations.
    adapter:
      type: webhook
      url: http://n8n:5678
    budget:
      daily_tokens: 100000

  - name: voice-agent
    description: Inbound call handler. Answers inquiries, books appointments, logs to CRM.
    adapter:
      type: webhook
      url: http://call-handler:3000
    budget:
      daily_tokens: 20000
```

### Step 4: Load configuration and verify

```bash
paperclip config load agents/paperclip/org.yaml agents/paperclip/agents.yaml
paperclip status
```

Expected output: a table showing each registered agent, current status, and daily token usage.

- [ ] All agents appear in `paperclip status`
- [ ] Token budgets shown correctly
- [ ] `paperclip audit` returns a clean initial log (no errors)

### Step 5: Add an approval gate for campaigns

Before any email campaign send, require approval:

```bash
paperclip gate add --agent n8n-automation --action "send_campaign" --require-approval
```

Test the gate:
```bash
paperclip task assign n8n-automation "Send the weekly newsletter campaign"
# Should pause and prompt: "Action requires approval. Approve? [y/N]"
```

- [ ] Gate tested and working
- [ ] Gate confirmed to block without explicit approval

**Reference:** `agents/paperclip/README.md`

---

## Section 5: Call Center Voice Agent Setup

**Purpose:** AI-powered inbound call handling. Answers calls, qualifies leads, books appointments via webhook, logs outcomes to ERPNext via n8n workflow.

**Time required:** 2–3 hours including testing (telephony setup adds complexity).

**Prerequisites:** A Telnyx account with an inbound phone number and SIP connection. Your server needs port 5060 (SIP) and a port range for RTP media reachable from Telnyx.

### Step 1: Deploy call center services

```bash
# From technomancer-stack/docker/:
docker compose up -d freeswitch piper-tts drachtio
```

- [ ] FreeSWITCH running (`docker compose ps freeswitch` shows `Up`)
- [ ] Piper TTS running (test: `curl -X POST http://localhost:10200/api/tts -d '{"text":"hello world"}' --output /tmp/test.wav`)
- [ ] Drachtio running on port 9022

### Step 2: Deploy the call handler Node.js application

```bash
cd agents/call-center/handler
npm install
# Set required environment variables in .env:
# DRACHTIO_HOST, WHISPER_API_URL or DEEPGRAM_API_KEY
# OLLAMA_HOST, N8N_BASE_URL, OPERATOR_TELEGRAM_ID, TELEGRAM_BOT_TOKEN
npm start
```

- [ ] Call handler starts without errors
- [ ] Logs show: `Drachtio connected` and `Registered with FreeSWITCH`

### Step 3: Configure the n8n call center CRM workflow

Import `n8n-templates/call-center-crm-update.json` in n8n:

- [ ] Workflow imported
- [ ] ERPNext credentials configured in the ERPNext nodes
- [ ] Telegram credentials configured in the alert node
- [ ] Webhook URL noted: `https://workflow.yourdomain.com/webhook/call-center/complete`
- [ ] `CALL_COMPLETE_WEBHOOK` variable set in call handler `.env`

### Step 4: Test a call

Use a softphone app (Zoiper, Linphone) configured to your Telnyx SIP credentials:

- [ ] Dial your Telnyx number
- [ ] Agent greeting plays (TTS audio)
- [ ] Agent responds to a spoken question
- [ ] Call ends gracefully when "goodbye" is said
- [ ] n8n workflow fires (check Executions log)
- [ ] ERPNext CRM record created for the test call
- [ ] Telegram notification received

**Reference:** `agents/call-center/README.md`

---

## Section 6: Ongoing Agent Health Checks

Add these to your quarterly stack review:

- [ ] `paperclip audit` — review token spend per agent over the last 30 days. Adjust budgets if any agent is consistently near its ceiling.
- [ ] OpenClaw skills tested for each: do all three custom skills return accurate live data?
- [ ] Call handler log reviewed: any calls that dropped unexpectedly? Any TTS failures?
- [ ] n8n → call-center-crm-update.json — any failed executions in the last 30 days?
- [ ] WooCommerce webhooks firing correctly to n8n (check n8n Executions for woocommerce webhook trigger)
- [ ] All agents responding within acceptable latency (voice agent target: <2 seconds first response)

**Token spend targets (monthly, across all agents):**

| Agent | Target | Alert if over |
|-------|--------|--------------|
| studio-lead (OpenClaw) | <75,000 tokens | 100,000 |
| n8n-automation | <150,000 tokens | 250,000 |
| voice-agent | <30,000 tokens | 50,000 |

If any agent consistently exceeds targets, audit its task log in Paperclip to identify high-cost instructions and either refine the prompts or lower inference frequency.
