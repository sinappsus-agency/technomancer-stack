# Docker Stack — Master Configuration

This directory contains the Docker Compose configuration for the full Technomancer Stack.

## Files

- `docker-compose.yml` — Master compose file. Start with this.
- `.env.example` — Copy to `.env` and populate before running.
- `security-checklist.md` — Post-deployment security verification steps.

## Quick Deploy

```bash
# 1. Copy and populate environment file
cp .env.example .env
nano .env  # Fill in all required values

# 2. Start the full stack
docker compose up -d

# 3. Verify all services are running
docker compose ps
```

## Services Included

| Service | Subdomain | Purpose |
|---------|-----------|---------|
| Traefik | traefik.yourdomain.com | Reverse proxy + SSL |
| n8n | workflow.yourdomain.com | Workflow automation |
| Notifuse | email.yourdomain.com | Email marketing |
| ERPNext | erp.yourdomain.com | CRM + business ops |
| MinIO | s3.yourdomain.com | Object storage |
| MinIO Console | s3-console.yourdomain.com | Storage admin UI |
| Ollama | (internal only) | Local AI inference |
| Vaultwarden | vault.yourdomain.com | Password manager |
| Matomo | analytics.yourdomain.com | Web analytics |
| Uptime Kuma | status.yourdomain.com | Service monitoring |

## Updating Services

```bash
# Pull latest images for all services
docker compose pull

# Restart with updated images
docker compose up -d
```

## Backups

Daily backups are handled via n8n workflow. See `n8n-templates/backup-automation.json`.
Manual backup: `docker compose exec n8n n8n export:workflow --all --output=/backup/`

## Logs

```bash
# View logs for a specific service
docker compose logs -f n8n

# View all service logs
docker compose logs -f
```
