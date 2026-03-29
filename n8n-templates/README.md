# n8n Workflow Templates

Importable n8n workflow JSON files for the automation layer described in **Chapter 16 — n8n and the Automation Layer**.

---

## How to Import

1. Open your n8n instance (e.g. `https://workflow.yourdomain.com`)
2. Click **Add workflow** → **Import from file**
3. Select any `.json` file from this directory
4. Update credentials and environment-specific values (tagged `TODO` in workflow notes)

---

## Template Index

| File | Purpose | Chapter |
|------|---------|---------|
| `client-onboarding-trigger.json` | New client detected → welcome sequence + CRM update | Ch 7 |
| `crm-welcome-orientation.json` | 3-step welcome drip with personalization | Ch 7 |
| `crm-journey-stages.json` | Lifecycle stage management (lead → client → advocate) | Ch 7 |
| `email-campaign-workflow.json` | 3-touch email drip with Ollama-generated copy | Ch 15 |
| `call-center-crm-update.json` | Inbound call → Whisper transcript → AI summary → CRM | Ch 16 |
| `weekly-intelligence-brief.json` | Aggregated weekly report from all data sources | Ch 17 |
| `meeting-transcript-processor.json` | Audio → transcript → action items → task creation | Ch 16 |
| `error-handler-template.json` | Reusable error recovery sub-workflow | Ch 16 |
| `local-ai-processor.json` | Route prompts to local Ollama for processing | Ch 9 |
| `server-control-bot.json` | Telegram bot → server status, restart, health checks | Ch 8 |

---

## Workflow Architecture

All workflows follow the **trigger → transform → act** pattern described in Chapter 16. Key conventions:

- **Error handling:** Every production workflow should include the `error-handler-template` as a sub-workflow
- **Credentials:** Use n8n's credential store — never hardcode secrets in workflow JSON
- **Local AI:** Workflows that use LLMs point to `http://ollama:11434` (Docker internal) by default
- **Naming:** Workflow names use `kebab-case` matching the filename

---

## Customizing Templates

These templates are starting points. Adapt them to your stack:

1. **CRM fields** — Update field mappings to match your ERPNext or CRM schema
2. **Email templates** — Replace placeholder copy with your brand voice (see `prompts/workflow/email-campaign.md`)
3. **Webhook URLs** — Update to your domain
4. **AI model** — Change `llama3.2` to whichever model you run locally

---

## Related Resources

- **`prompts/workflow/`** — Prompt templates used by these workflows
- **`agents/call-center/`** — Full call center architecture (pairs with `call-center-crm-update.json`)
- **`workbook/automation/`** — Automation audit template to plan your workflow needs
- **`docker/docker-compose.yml`** — The n8n service definition and configuration
