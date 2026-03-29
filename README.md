# technomancer-stack

The companion repository for **TECHNOMANCER: The One-Person Superbrand**.

This repository contains the runnable infrastructure, workflow templates, agent configurations, prompts, and workbook materials referenced throughout the book.

---

## Quick Start

1. Copy `.env.example` to `.env` and populate with your values
2. Navigate to `terraform/server-bootstrap/` and follow `SETUP.md`
3. After server is provisioned, run `docker compose up -d` from the `docker/` directory
4. Import n8n workflow templates from `n8n-templates/` into your n8n instance
5. Review and adapt prompts in `prompts/` for your brand voice

---

## Repository Structure

```
technomancer-stack/
│
├── terraform/
│   └── server-bootstrap/       # VPS provisioning + initial security hardening
│
├── docker/
│   ├── docker-compose.yml      # Master compose file — all services below run from here
│   ├── .env.example            # All required environment variables
│   ├── security-checklist.md  # Post-deployment security verification
│   │
│   │  [Services running on your server:]
│   ├── [traefik]               # Reverse proxy + Let's Encrypt SSL termination
│   ├── [n8n]                   # Workflow automation engine (the brain)
│   ├── [ollama]                # Local AI inference — Llama, Mistral, Gemma
│   ├── [postgresql]            # Shared database for n8n, Notifuse
│   ├── [notifuse]              # Email marketing + transactional email
│   ├── [erpnext]               # ERP + CRM (accounts, leads, projects, invoices)
│   ├── [minio]                 # S3-compatible object storage (media, backups)
│   ├── [wordpress + woocommerce] # Storefront, sales pages, digital products
│   ├── [vaultwarden]           # Self-hosted password manager (Bitwarden-compatible)
│   ├── [matomo]                # Full open-source analytics — GDPR-clean, no GA required
│   ├── [uptime-kuma]           # Server + service uptime monitoring + alerts
│   ├── [freeswitch]            # SIP call server (call center — optional)
│   ├── [piper-tts]             # Local text-to-speech for voice agents (optional)
│   └── [drachtio]              # SIP application server — bridges calls to AI (optional)
│
│  [Config files live in config/ not docker/ — see below]
│
├── config/
│   ├── traefik/                # Traefik v3 static + dynamic config
│   └── postgres/               # PostgreSQL init SQL + role grants
│
├── n8n-templates/              # Importable n8n workflow JSON files
│   ├── client-onboarding-trigger.json
│   ├── crm-welcome-orientation.json
│   ├── crm-journey-stages.json
│   ├── weekly-intelligence-brief.json
│   ├── meeting-transcript-processor.json
│   ├── local-ai-processor.json
│   ├── server-control-bot.json
│   ├── error-handler-template.json
│   ├── email-campaign-workflow.json    # 3-touch drip sequence with Ollama copy generation
│   └── call-center-crm-update.json    # Inbound call → CRM update via AI transcript analysis
│
├── agents/
│   ├── README.md                       # Agent system overview + integration map
│   ├── content-machine/                # 6-agent content production pipeline
│   │   └── README.md
│   ├── mcp-servers/                    # Model Context Protocol server configs
│   │   └── README.md                  # filesystem, n8n-trigger, memory, web-search, database
│   ├── personal-ai-infrastructure/     # 4-level context hierarchy + memory store
│   │   └── README.md
│   ├── call-center/                    # Automated inbound/outbound call system
│   │   └── README.md                  # FreeSWITCH + Whisper + Ollama + Piper TTS + Drachtio handler code
│   ├── openclaw/                       # OpenClaw AI agent platform integration
│   │   └── README.md                  # Setup, skills, WooCommerce/Notifuse/n8n connections
│   └── paperclip/                      # Paperclip agent control plane
│       └── README.md                  # Org chart, agent workforce management, budget governance
│
├── sops/                               # Standard Operating Procedures — all 13 runnable
│   ├── README.md
│   ├── 01-client-onboarding.md
│   ├── 02-client-follow-up.md
│   ├── 03-meetings-and-scrums.md
│   ├── 04-project-management.md
│   ├── 05-quality-assurance.md
│   ├── 06-upselling.md
│   ├── 07-client-feedback.md
│   ├── 08-team-communication.md
│   ├── 09-training-onboarding.md
│   ├── 10-financial-management.md
│   ├── 11-sales-and-marketing.md
│   ├── 12-branding-quick-start.md
│   └── 13-internal-operations.md
│
├── prompts/
│   ├── brand/                  # Brand voice and origin stack prompts
│   │   └── origin-stack-refinement.md
│   ├── verification/           # AI output verification checklists
│   └── workflow/               # Channel formats + campaign copy prompt templates
│       ├── channel-formats.md  # Format specs: email, LinkedIn, Twitter, video, blog, podcast
│       └── email-campaign.md  # Ready-to-use prompts for all email campaign types
│
└── workbook/
    ├── narrative/              # Story arc and platform character exercises
    ├── stack/                  # Minimum effective stack planning
    ├── automation/             # Automation audit template
    └── risk/                   # Risk register template
```

---

## Chapter References

Each directory maps to specific chapters in the book:

| Directory | Chapter |
|-----------|---------|
| `terraform/server-bootstrap/` | Chapter 8 — The Self-Hosted Sovereign |
| `docker/` | Chapter 8 — The Self-Hosted Sovereign |
| `config/traefik/` | Chapter 8 — The Self-Hosted Sovereign |
| `agents/mcp-servers/` | Chapter 9 — Running AI Locally |
| `agents/personal-ai-infrastructure/` | Chapter 9 — Running AI Locally |
| `agents/content-machine/` | Chapter 6 — AI as Creative Clone |
| `agents/call-center/` | Chapter 14 — n8n and the Automation Layer |
| `agents/openclaw/` | Chapter 9 — Running AI Locally |
| `agents/paperclip/` | Chapter 9 — Running AI Locally |
| `n8n-templates/` | Chapter 14 — n8n and the Automation Layer |
| `n8n-templates/email-campaign-workflow.json` | Chapter 15 — The Distribution Engine |
| `n8n-templates/call-center-crm-update.json` | Chapter 14 — n8n and the Automation Layer |
| `prompts/brand/` | Chapter 1 — The Origin Stack |
| `prompts/verification/` | Chapter 6 — AI as Creative Clone |
| `prompts/workflow/channel-formats.md` | Chapter 2 — Narrative Systems |
| `prompts/workflow/email-campaign.md` | Chapter 15 — The Distribution Engine |
| `workbook/narrative/` | Chapter 2 — Narrative Systems |
| `workbook/stack/` | Chapter 5 — The Techno Stack |
| `workbook/automation/` | Chapter 14 — n8n and the Automation Layer |
| `workbook/risk/` | Chapter 17 — The Risks You Were Not Warned About |
| `sops/` | Throughout — SOP library referenced across all operational chapters |

---

## Prerequisites

- A VPS with Ubuntu 22.04 (Contabo, Hetzner, or DigitalOcean recommended)
- A domain name with DNS management access
- Docker and Docker Compose installed on the server
- Terraform installed on your local machine (for initial provisioning)
- Basic familiarity with command-line operations

All of these are covered in the book. If you are starting from zero, read Chapters 8 and 9 before working through this repository.

---

## Security Note

This repository contains configuration templates, not live credentials. The `.env.example` file documents required variables with placeholder values. Never commit a populated `.env` file to version control. See `docker/security-checklist.md` for the full post-deployment security review.

---

## License

This repository and its contents are provided for personal use by purchasers of TECHNOMANCER: The One-Person Superbrand. Commercial redistribution or resale of the repository contents is not permitted.
