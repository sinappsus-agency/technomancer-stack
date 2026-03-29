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
│   ├── postgres/               # PostgreSQL init SQL + role grants
│   └── clickhouse/             # ClickHouse analytics database config
│
├── comfyui/                    # Visual production layer — image + video generation
│   ├── SKILL.md                # Agent skill — model reference, prompt engineering, API docs
│   ├── mcp/
│   │   ├── server.py           # 15-tool MCP server (ComfyUI ↔ VS Code bridge)
│   │   └── README.md           # MCP server setup guide
│   ├── workflows/              # Parameterized workflow templates (ready to run)
│   └── exports/                # Staging area — drop raw ComfyUI exports here for import
│
├── n8n-templates/              # Importable n8n workflow JSON files
│   ├── README.md               # Template index + chapter mapping
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
│   ├── mcp-servers/                    # Model Context Protocol server configs
│   ├── personal-ai-infrastructure/     # 4-level context hierarchy + memory store
│   ├── call-center/                    # Automated inbound/outbound call system
│   ├── openclaw/                       # OpenClaw AI agent platform integration
│   ├── paperclip/                      # Paperclip agent control plane
│   └── think-tank-prompts/             # Multi-agent decision prompts
│
├── iot/                                # Physical layer — hardware + sensors
│   ├── mqtt/                           # MQTT broker configs and topic schemas
│   └── biometric-resonance/            # Heart coherence + collective resonance
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
└── workbook/                   # Interactive planning templates — fill out alongside the book
    ├── narrative/              # Story arc and platform character exercises (Ch 2)
    ├── stack/                  # Minimum effective stack + ComfyUI workflow planning (Ch 5, 11)
    ├── automation/             # Automation audit template (Ch 16)
    ├── agents/                 # Agent deployment checklist (Ch 12)
    └── risk/                   # Risk register template (Ch 19)
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
| `comfyui/` | Chapter 11 — The Visual Stack: ComfyUI, Stable Diffusion, and Generative Media |
| `comfyui/mcp/` | Chapter 11 — MCP bridge for programmatic image/video generation |
| `comfyui/workflows/` | Chapter 11 — Parameterized workflow templates (SDXL, LTX Video) |
| `iot/mqtt/` | Chapter 10 — IoT and the Physical Layer |
| `iot/biometric-resonance/` | Chapter 10 — Heart coherence + collective resonance sensor integration |
| `prompts/brand/` | Chapter 1 — The Origin Stack |
| `prompts/verification/` | Chapter 6 — AI as Creative Clone |
| `prompts/workflow/channel-formats.md` | Chapter 2 — Narrative Systems |
| `prompts/workflow/email-campaign.md` | Chapter 15 — The Distribution Engine |
| `workbook/narrative/` | Chapter 2 — Narrative Systems |
| `workbook/stack/` | Chapter 5 — The Techno Stack |
| `workbook/automation/` | Chapter 16 — The Automation Audit |
| `workbook/agents/` | Chapter 12 — Agent Deployment |
| `workbook/risk/` | Chapter 19 — The Risks You Were Not Warned About |
| `sops/` | Throughout — SOP library referenced across all operational chapters |

---

## Using the Workbook

The `workbook/` directory contains interactive planning templates designed to be filled out as you read. Each template corresponds to a specific chapter and builds on the previous one:

1. **Narrative** (`workbook/narrative/`) — Define your origin story, brand voice, and platform character. Start here alongside Chapter 2.
2. **Stack** (`workbook/stack/`) — Map your minimum effective stack and plan your ComfyUI visual production workflows. Use with Chapters 5 and 11.
3. **Agents** (`workbook/agents/`) — Agent deployment checklist: which agents to build, what they connect to, and how they hand off to humans. Use with Chapter 12.
4. **Automation** (`workbook/automation/`) — Audit your current manual processes and identify what to automate first. Use with Chapter 16.
5. **Risk** (`workbook/risk/`) — Risk register for AI operations: bias, hallucination, data exposure, vendor lock-in. Use with Chapter 19.

Each template is a markdown file you can edit directly or copy into your own project. The goal is a working operational blueprint — not a theoretical exercise.

---

## Using ComfyUI

The `comfyui/` directory contains a complete visual production layer that bridges VS Code to ComfyUI for programmatic image and video generation. See the [comfyui/README.md](comfyui/README.md) for full setup instructions.

**Quick overview:**
- `comfyui/mcp/server.py` — 15-tool MCP server that lets your AI assistant queue ComfyUI jobs, poll for results, and download outputs directly from the chat interface
- `comfyui/workflows/` — Parameterized workflow templates (SDXL text-to-image, LTX 2.3 image+audio-to-video)
- `comfyui/exports/` — Drop zone for raw ComfyUI API exports; use `import_workflow()` to convert them into parameterized templates
- `comfyui/SKILL.md` — Agent skill reference: model specs, prompt engineering rules, resolution tables

This integrates with Chapter 11 — The Visual Stack. You need ComfyUI Desktop installed locally (the MCP server connects to `http://127.0.0.1:8188` by default).

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
