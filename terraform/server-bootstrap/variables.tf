###############################################################################
# variables.tf — Input variables for the Technomancer Stack bootstrap
###############################################################################

##########
# PROVIDER
##########

variable "hetzner_api_token" {
  description = "Hetzner Cloud API token. Create at: https://console.hetzner.cloud/projects/*/security/tokens"
  type        = string
  sensitive   = true
}

##########
# SERVER
##########

variable "server_type" {
  description = "Hetzner server type. cx22=2vCPU/4GB (minimum), cx32=4vCPU/8GB (recommended for full stack)."
  type        = string
  default     = "cx32"

  validation {
    condition     = contains(["cx22", "cx32", "cx42", "cpx11", "cpx21", "cpx31"], var.server_type)
    error_message = "Must be a valid Hetzner server type. See: https://www.hetzner.com/cloud"
  }
}

variable "server_location" {
  description = "Hetzner datacenter location. nbg1=Nuremberg (EU), fsn1=Falkenstein (EU), hel1=Helsinki (EU), ash=Ashburn (US)"
  type        = string
  default     = "nbg1"
}

variable "environment" {
  description = "Deployment environment label. Used in resource names."
  type        = string
  default     = "prod"

  validation {
    condition     = contains(["prod", "staging", "dev"], var.environment)
    error_message = "Environment must be prod, staging, or dev."
  }
}

##########
# SECURITY
##########

variable "ssh_public_key" {
  description = "SSH public key for server access. Get yours with: cat ~/.ssh/id_ed25519.pub"
  type        = string
}

##########
# DOMAIN
##########

variable "base_domain" {
  description = "Your domain name. Services will be deployed to subdomains: workflow.yourdomain.com, etc."
  type        = string

  validation {
    condition     = can(regex("^[a-z0-9][a-z0-9-]{0,61}[a-z0-9]\\.[a-z]{2,}$", var.base_domain))
    error_message = "Must be a valid domain name (e.g., yourdomain.com)."
  }
}

variable "letsencrypt_email" {
  description = "Email for Let's Encrypt certificate notifications and renewals."
  type        = string
}

##########
# STACK CONFIGURATION
##########

variable "timezone" {
  description = "Server timezone. Used by n8n for scheduling and logs. See: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones"
  type        = string
  default     = "Africa/Johannesburg"
}

variable "stack_git_repo" {
  description = "Git repository URL containing your docker-compose.yml and config files. The bootstrap script will clone this. Leave empty to skip git clone."
  type        = string
  default     = ""
}

##########
# SECRETS (for cloud-init template injection)
##########

variable "postgres_password" {
  description = "PostgreSQL superuser password. Generate with: openssl rand -base64 32"
  type        = string
  sensitive   = true

  validation {
    condition     = length(var.postgres_password) >= 24
    error_message = "PostgreSQL password must be at least 24 characters."
  }
}

variable "n8n_encryption_key" {
  description = "n8n encryption key for credential storage. Generate with: openssl rand -hex 32"
  type        = string
  sensitive   = true

  validation {
    condition     = length(var.n8n_encryption_key) >= 32
    error_message = "n8n encryption key must be at least 32 characters."
  }
}

##########
# VOLUME
##########

variable "create_separate_volume" {
  description = "Whether to create a separate Hetzner Volume for data storage. Recommended for production — easier to resize and snapshot independently."
  type        = bool
  default     = false
}

variable "volume_size_gb" {
  description = "Size of the separate data volume in GB. Only used if create_separate_volume = true."
  type        = number
  default     = 50

  validation {
    condition     = var.volume_size_gb >= 10 && var.volume_size_gb <= 10240
    error_message = "Volume size must be between 10 and 10240 GB."
  }
}
