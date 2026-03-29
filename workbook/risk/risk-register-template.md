# Risk Register Template

**Chapter Reference:** Chapter 17 — The Risks You Were Not Warned About
**Usage:** Populate this register and review it quarterly. Takes 20 minutes to complete, 20 minutes to review.

---

## How to Use This Register

For each risk row:
1. **Likelihood**: How likely is this risk to occur? (Low / Medium / High)
2. **Impact**: How bad would it be if it occurred? (Low / Medium / High / Critical)
3. **Current Mitigation**: What you have done to reduce the risk
4. **Mitigation Status**: Not started / In progress / Complete
5. **Last Reviewed**: Date of last review

---

## Risk Register

### Category 1: AI Output Risks

| Risk | Likelihood | Impact | Current Mitigation | Status | Last Reviewed |
|------|-----------|--------|-------------------|--------|--------------|
| Hallucinated statistic published in public content | Medium | High | Three-check Verification Protocol (Ch.6) | | |
| AI fabricated legal clause used in client agreement | Low | Critical | Manual review of all client-facing legal language | | |
| AI-generated code with SQL injection vulnerability deployed | Medium | High | Code review checklist before deployment | | |
| Prompt injection attack via customer-submitted content | Low | High | Output schema validation on all customer-facing AI workflows | | |

### Category 2: Infrastructure Risks

| Risk | Likelihood | Impact | Current Mitigation | Status | Last Reviewed |
|------|-----------|--------|-------------------|--------|--------------|
| VPS disk failure (data loss) | Low | Critical | Daily encrypted backups to secondary location | | |
| DDoS attack or VPS suspension | Low | High | VPS provider monitoring; documented recovery runbook | | |
| Server locked out (lost SSH key) | Low | Critical | Backup SSH key in Vaultwarden; VPS provider emergency console access | | |
| Misconfigured Traefik exposes admin interface | Medium | High | Security checklist run after every deployment | | |
| Docker container running as root | Medium | Medium | Quarterly security scan; docker-compose user config | | |

### Category 3: Dependency Risks

| Risk | Likelihood | Impact | Current Mitigation | Status | Last Reviewed |
|------|-----------|--------|-------------------|--------|--------------|
| Domain registrar account compromised | Low | Critical | 2FA on registrar; Vaultwarden credentials | | |
| DNS provider outage | Low | High | DNS TTL configured short; monitor with Uptime Kuma | | |
| AI model API deprecation breaking workflows | Medium | High | OpenRouter abstraction layer; prompts version-controlled | | |
| Email relay (SendGrid/Postmark) account suspended | Low | High | SMTP relay credentials ready for alternative | | |
| n8n breaking change in major update | Low | Medium | Test updates in staging before production | | |

### Category 4: Operational Risks

| Risk | Likelihood | Impact | Current Mitigation | Status | Last Reviewed |
|------|-----------|--------|-------------------|--------|--------------|
| Workflow silent failure (processes incorrectly without alert) | Medium | Medium | Error handler template deployed on all production workflows | | |
| Automation drift (workflow correct 6 months ago, broken now) | Medium | Medium | Monthly workflow audit | | |
| Context drift causing inconsistent client deliverables | Medium | Medium | Session boundary template; per-project style documents | | |
| Vaultwarden vault inaccessible (password manager down) | Low | High | Emergency credential backup in offline encrypted storage | | |

### Category 5: Security Risks

| Risk | Likelihood | Impact | Current Mitigation | Status | Last Reviewed |
|------|-----------|--------|-------------------|--------|--------------|
| Brute force attack on exposed service | High | Medium | Fail2ban installed; SSH password auth disabled | | |
| Credentials exposed in code repository | Low | Critical | .env files in .gitignore; git history scan | | |
| Phishing attack on admin email | Medium | High | 2FA on all admin accounts; security awareness | | |
| API key theft via leaked .env file | Low | Critical | .env never committed; annual key rotation | | |
| Malicious n8n workflow import | Low | High | Only import from trusted sources; review before import | | |

---

## Risk Matrix Reference

```
Impact:    Critical | High    | Medium  | Low
          ---------+---------+---------+--------
High      | URGENT  | URGENT  | REVIEW  | MONITOR
Medium    | URGENT  | REVIEW  | REVIEW  | MONITOR  <-- Likelihood
Low       | REVIEW  | MONITOR | MONITOR | ACCEPT
```

URGENT = Address before next week
REVIEW = Address before next quarter
MONITOR = Track but acceptable at current level
ACCEPT = Risk acknowledged, no action required

---

## Recovery Runbook

Document your recovery procedures here for the most critical risks:

### Server Total Failure Recovery

1. Note the server IP and DNS records that were pointing to it
2. Provision a replacement VPS (Terraform bootstrap: `terraform/server-bootstrap/`)
3. Install Docker and Docker Compose
4. Clone this repository to the new server
5. Restore `.env` file from Vaultwarden backup
6. Restore data volumes from most recent backup in MinIO/B2
7. Run `docker compose up -d`
8. Verify all services are running (`docker compose ps`)
9. Update DNS records to new server IP
10. Verify SSL certificates issued (may take 5–10 minutes)

Estimated recovery time: 45–60 minutes for a clean rebuild.

### n8n Workflow Recovery

1. Access n8n at new URL
2. Import workflow JSONs from `n8n-templates/` directory
3. Reconnect all credentials (stored in Vaultwarden)
4. Verify workflows are active and test each critical one

---

Last Register Update: [DATE]
Next Scheduled Review: [DATE + 90 DAYS]
