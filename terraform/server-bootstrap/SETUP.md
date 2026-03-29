# Server Bootstrap — Setup Guide

## Overview

This Terraform configuration provisions and configures a production-ready VPS for the Technomancer Stack. It:

- Creates a Hetzner Cloud VPS (Ubuntu 24.04 LTS)
- Configures UFW firewall (ports 22, 80, 443 only)
- Installs Docker and Docker Compose
- Configures fail2ban (SSH brute-force protection)
- Enables automatic security updates
- Creates the data directory scaffold
- Writes a starter `.env` file
- Outputs connection details and DNS instructions

---

## Prerequisites

| Tool | Purpose | Install guide |
|------|---------|---------------|
| Terraform ≥ 1.9 | Infrastructure provisioning | https://developer.hashicorp.com/terraform/install |
| Hetzner Cloud account | VPS provider | https://www.hetzner.com/cloud |
| SSH key pair | Server access | `ssh-keygen -t ed25519` |

---

## Step 1: Get Your Hetzner API Token

1. Log in to [Hetzner Cloud Console](https://console.hetzner.cloud/)
2. Open your project → Security → API Tokens
3. Click "Generate API Token" → Read & Write
4. Copy the token — you will only see it once

---

## Step 2: Configure Variables

Create a `terraform.tfvars` file (never commit this to git):

```hcl
# terraform.tfvars — DO NOT COMMIT TO GIT
hetzner_api_token  = "your-hetzner-api-token-here"
ssh_public_key     = "ssh-ed25519 AAAAC3... your-key-comment"
base_domain        = "yourdomain.com"
letsencrypt_email  = "you@yourdomain.com"
postgres_password  = "generate-with-openssl-rand-base64-32"
n8n_encryption_key = "generate-with-openssl-rand-hex-32"

# Optional — defaults shown
server_type    = "cx32"     # 4 vCPU, 8 GB RAM — recommended
server_location = "nbg1"   # Nuremberg, Germany
environment    = "prod"
timezone       = "Africa/Johannesburg"
```

Generate secrets:
```bash
openssl rand -base64 32   # for postgres_password
openssl rand -hex 32      # for n8n_encryption_key
```

**Add to .gitignore immediately:**
```
terraform.tfvars
*.tfstate
*.tfstate.backup
.terraform/
```

---

## Step 3: Initialise and Apply

```bash
# Navigate to this directory
cd terraform/server-bootstrap

# Initialise Terraform (download providers)
terraform init

# Preview what will be created
terraform plan

# Apply — creates the server
terraform apply
```

Review the plan output carefully before typing `yes`. Terraform will show you exactly what it will create.

---

## Step 4: Configure DNS

After `terraform apply` completes, it will output your server IP and DNS instructions:

```
service_urls = {
  n8n         = "https://workflow.yourdomain.com"
  notifuse    = "https://email.yourdomain.com"
  minio       = "https://s3.yourdomain.com"
  ...
}

dns_record_instructions = <<EOT
  Create the following DNS records at your domain registrar:

  Type    Name    Value               TTL
  A       *       194.XXX.XXX.XXX     300
  A       @       194.XXX.XXX.XXX     300
EOT
```

Go to your domain registrar and create these two records. The wildcard `*` covers all subdomains.

---

## Step 5: Connect and Complete Setup

```bash
# SSH into your server (command shown in terraform output)
ssh root@YOUR_SERVER_IP

# Verify Docker is running
docker --version
docker compose version

# Navigate to the deploy directory
cd /opt/technomancer

# Edit the .env file with all required values
nano docker/.env
# See: docker/.env.example for all required variables

# Start all services
cd docker
docker compose up -d

# Monitor startup (takes 1-3 minutes)
docker compose logs -f
```

---

## Server Type Selection

| Server Type | vCPU | RAM | Cost/month | When to use |
|-------------|------|-----|------------|-------------|
| `cx22` | 2 | 4 GB | ~€4 | Minimum — n8n + Traefik only |
| `cx32` | 4 | 8 GB | ~€9 | Full stack without ERPNext |
| `cx42` | 8 | 16 GB | ~€18 | Full stack with ERPNext + Ollama |
| `cpx31` | 4 | 8 GB | ~€12 | CPU-optimised — better for Ollama |

**Recommendation:** Start with `cx32`. Hetzner allows live resize with no data loss.

---

## Alternative Providers

This configuration is written for Hetzner but can be adapted:

**DigitalOcean:**
- Replace `hcloud_server` with `digitalocean_droplet`
- Replace `hcloud_firewall` with `digitalocean_firewall`
- Equivalent droplet: `s-2vcpu-4gb` ($24/month)

**Contabo:**
- Contabo has no official Terraform provider
- Provision manually via Contabo panel
- Copy `bootstrap.sh.tmpl` and run it manually as root
- Equivalent plan: VPS S (4 vCPU, 8 GB RAM, €4.99/month)

---

## Destroying the Server

```bash
terraform destroy
```

**Warning:** This will permanently delete the server and all data on it. Make sure you have backups before running this. Volume data will also be destroyed unless `create_separate_volume = true` was used.

---

## Security Notes

- The bootstrap script creates only the minimum required firewall rules
- SSH is open to all IPs initially — fail2ban will block brute-force attempts
- Change your SSH port (from 22) in `/etc/ssh/sshd_config` after deployment for additional security
- All `.env` files with secrets are mode 600 (owner read only)
- The `acme.json` file (Let's Encrypt certificates) is mode 600 — this is required by Traefik
