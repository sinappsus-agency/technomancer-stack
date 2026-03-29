# Technomancer Stack — GitHub Copilot Instructions

This file is read automatically by GitHub Copilot at the start of every agent or chat session in this workspace. It describes the Technomancer Stack so you do not have to re-explain it.

---

## Stack Overview

| Service | Role | Location |
|---------|------|----------|
| Docker + Traefik | Container orchestration + reverse proxy | VPS / Docker Compose |
| n8n | Workflow automation engine | `http://localhost:5678` |
| Ollama | Local LLM inference | `http://localhost:11434` |
| ComfyUI Desktop | Local image/video generation | `http://127.0.0.1:8000` |
| ERPNext | CRM, ERP, project management | Docker service |
| MinIO | S3-compatible object storage | `http://localhost:9000`, bucket: `technomancer-content` |
| Matomo | Self-hosted analytics | Docker service |
| Notifuse | Notification and monitoring | Docker service |
| PostgreSQL | Primary relational database | Docker service, ERPNext-managed |

Infrastructure is provisioned with **Terraform** (see `terraform/server-bootstrap/`). The VPS host is **Hetzner** (Germany, EU data residency).

---

## Repository Structure

```
technomancer-stack/
├── .github/
│   └── copilot-instructions.md     ← this file
├── docker/
│   ├── docker-compose.yml          ← all services in one file
│   └── .env.example                ← secret template (never commit .env)
├── config/
│   ├── traefik/                    ← Traefik static and dynamic config
│   └── postgres/                   ← DB init scripts
├── terraform/
│   └── server-bootstrap/           ← VPS provisioning (Hetzner)
├── templates/
│   └── n8n/                        ← n8n workflow JSON exports
├── comfyui/
│   ├── SKILL.md                    ← ComfyUI agent skill file
│   └── workflows/                  ← ComfyUI API-format workflow JSONs
├── agents/
│   ├── personal-ai-infrastructure/ ← PAI agent config
│   └── paperclip/                  ← Paperclip agent config
└── workbook/                       ← Business and narrative planning templates
```

---

## Coding Conventions

### n8n
- Workflows are stored as JSON in `templates/n8n/`
- When writing automation logic, use **Code nodes in JavaScript** (not Python)
- Sub-workflows are preferable to deeply nested single workflows
- Credential names follow the pattern: `service-purpose` (e.g., `minio-main`, `postgres-erpnext`)

### ComfyUI
- Workflow files use **API format** JSON (not graph format — no layout metadata needed)
- Workflow JSONs are stored in `comfyui/workflows/`
- Default model: SDXL at 1024×1024. For photorealism or text-in-image: Flux.1 Dev. For video: Wan2.1
- See `comfyui/SKILL.md` for full API usage, node reference, and prompt guidelines

### Docker / Compose
- All services defined in `docker/docker-compose.yml`
- Use named volumes for persistent data — never bind-mount data directories to the host in production
- Environment variables come from `.env` — never hardcode credentials in Compose files
- Traefik labels on each service define routing — see `config/traefik/dynamic.yml` for patterns

### Terraform
- Resources are in `terraform/server-bootstrap/`
- Provider: Hetzner Cloud (`hcloud`)
- Write all infrastructure as code — do not use the Hetzner dashboard for changes tracked in this repo
- Variables go in `variables.tf`; secrets go in `.tfvars` (gitignored)

### Secrets and Security
- Secrets live in `.env` only — see `.env.example` for the full list of required variables
- `.env` is gitignored. Never commit it.
- Rotate API keys in `.env` and redeploy; do not store secrets in code
- Database passwords, API keys, and webhook secrets must be unique per service

---

## Standing Agent Instructions

When operating in agent mode in this workspace:

1. **Read before writing** — check the existing file content before making edits
2. **Preserve the docker-compose.yml structure** — add services but do not reorganise existing ones without explicit instruction
3. **Always validate JSON** — ComfyUI workflow JSON and n8n export JSON must be valid; check syntax before outputting
4. **Output workflow files to the correct directory** — ComfyUI workflows → `comfyui/workflows/`, n8n workflows → `templates/n8n/`
5. **Default to self-hosted** — when there is a self-hosted option, prefer it over a cloud API dependency
6. **Reference the companion skill files** — before working with ComfyUI, read `comfyui/SKILL.md` for API format details and prompt conventions
7. **Never output a .env file** — only update `.env.example` when new secrets are needed

---

## Common Task Patterns

### "Add a new n8n workflow for X"
1. Read the relevant service's documentation or existing workflow templates
2. Construct the workflow as n8n-compatible JSON (format matches n8n export)
3. Save to `templates/n8n/descriptive-name.json`
4. Add a one-line description to the workflow's `meta.description` field

### "Generate an image of X"
1. Read `comfyui/SKILL.md` for current model options and API format
2. Choose the appropriate model based on the task (SDXL, Flux, Wan2.1)
3. Construct API-format workflow JSON with the specified prompt
4. Submit via POST to `http://127.0.0.1:8000/prompt`

### "Add a new service to the stack"
1. Add service definition to `docker/docker-compose.yml` with Traefik labels
2. Add required environment variables to `docker/.env.example`
3. If the service needs persistent data, define a named volume
4. Document the service in `docker/README.md`

### "Write a Terraform resource for X"
1. Work in `terraform/server-bootstrap/`
2. Add variables to `variables.tf` — never hardcode values
3. Follow the existing naming convention: `hcloud_server.technomancer-*`
