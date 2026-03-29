###############################################################################
# Technomancer Stack — Server Bootstrap
# Terraform configuration for Hetzner Cloud
#
# Provisions and configures a production-ready VPS with:
#   - Ubuntu 24.04 LTS
#   - Docker + Docker Compose
#   - UFW firewall (ports 22, 80, 443 only)
#   - fail2ban for SSH brute-force protection
#   - Unattended security upgrades
#   - SSH key authentication
#   - The Technomancer Stack deployed via docker-compose
#
# USAGE:
#   1. Install Terraform: https://developer.hashicorp.com/terraform/install
#   2. Create a Hetzner API token: https://console.hetzner.cloud/
#   3. Add your SSH public key to variables.tf or tfvars
#   4. Run: terraform init && terraform plan && terraform apply
#
# OTHER PROVIDERS:
#   For DigitalOcean, replace the hcloud resources with digitalocean_droplet
#   For Contabo, use the contabo provider or manual provisioning + this script
#   See variables.tf for provider switching notes
###############################################################################

terraform {
  required_version = ">= 1.9.0"

  required_providers {
    hcloud = {
      source  = "hetznercloud/hcloud"
      version = "~> 1.49"
    }
  }
}

###############
# PROVIDER
###############

provider "hcloud" {
  token = var.hetzner_api_token
}

###############
# SSH KEY
###############

resource "hcloud_ssh_key" "technomancer" {
  name       = "technomancer-key-${var.environment}"
  public_key = var.ssh_public_key
}

###############
# FIREWALL
###############

resource "hcloud_firewall" "technomancer" {
  name = "technomancer-firewall-${var.environment}"

  # Allow SSH from anywhere (will be tightened post-bootstrap via fail2ban)
  rule {
    direction = "in"
    protocol  = "tcp"
    port      = "22"
    source_ips = [
      "0.0.0.0/0",
      "::/0",
    ]
  }

  # HTTP — Traefik will redirect to HTTPS
  rule {
    direction = "in"
    protocol  = "tcp"
    port      = "80"
    source_ips = [
      "0.0.0.0/0",
      "::/0",
    ]
  }

  # HTTPS — All services via Traefik
  rule {
    direction = "in"
    protocol  = "tcp"
    port      = "443"
    source_ips = [
      "0.0.0.0/0",
      "::/0",
    ]
  }

  # Allow all outbound
  rule {
    direction   = "out"
    protocol    = "tcp"
    port        = "any"
    destination_ips = [
      "0.0.0.0/0",
      "::/0",
    ]
  }

  rule {
    direction   = "out"
    protocol    = "udp"
    port        = "any"
    destination_ips = [
      "0.0.0.0/0",
      "::/0",
    ]
  }
}

###############
# SERVER
###############

resource "hcloud_server" "technomancer" {
  name        = "technomancer-${var.environment}"
  image       = "ubuntu-24.04"
  server_type = var.server_type
  location    = var.server_location
  ssh_keys    = [hcloud_ssh_key.technomancer.id]
  firewall_ids = [hcloud_firewall.technomancer.id]

  labels = {
    environment = var.environment
    project     = "technomancer-stack"
    managed_by  = "terraform"
  }

  # Cloud-init bootstrap script
  user_data = templatefile("${path.module}/bootstrap.sh.tmpl", {
    domain            = var.base_domain
    email             = var.letsencrypt_email
    git_repo          = var.stack_git_repo
    postgres_password = var.postgres_password
    n8n_key           = var.n8n_encryption_key
    timezone          = var.timezone
  })
}

###############
# VOLUME (optional persistent storage separate from OS disk)
###############

resource "hcloud_volume" "technomancer_data" {
  count    = var.create_separate_volume ? 1 : 0
  name     = "technomancer-data-${var.environment}"
  size     = var.volume_size_gb
  location = var.server_location
  format   = "ext4"

  labels = {
    environment = var.environment
    project     = "technomancer-stack"
  }
}

resource "hcloud_volume_attachment" "technomancer_data" {
  count     = var.create_separate_volume ? 1 : 0
  volume_id = hcloud_volume.technomancer_data[0].id
  server_id = hcloud_server.technomancer.id
  automount = true
}

###############
# DNS (optional — requires Cloudflare provider)
# Uncomment if managing DNS via Terraform
###############

# resource "cloudflare_record" "wildcard" {
#   zone_id = var.cloudflare_zone_id
#   name    = "*"
#   value   = hcloud_server.technomancer.ipv4_address
#   type    = "A"
#   proxied = false
# }

# resource "cloudflare_record" "root" {
#   zone_id = var.cloudflare_zone_id
#   name    = "@"
#   value   = hcloud_server.technomancer.ipv4_address
#   type    = "A"
#   proxied = false
# }
