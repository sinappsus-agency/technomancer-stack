###############################################################################
# outputs.tf — Output values after terraform apply
###############################################################################

output "server_ip" {
  description = "Public IPv4 address of the Technomancer server"
  value       = hcloud_server.technomancer.ipv4_address
}

output "server_ip_v6" {
  description = "Public IPv6 address of the Technomancer server"
  value       = hcloud_server.technomancer.ipv6_address
}

output "server_id" {
  description = "Hetzner server ID (for use with hcloud CLI)"
  value       = hcloud_server.technomancer.id
}

output "ssh_command" {
  description = "SSH command to connect to your server"
  value       = "ssh root@${hcloud_server.technomancer.ipv4_address}"
}

output "service_urls" {
  description = "URLs for all deployed services (after DNS is configured)"
  value = {
    n8n          = "https://workflow.${var.base_domain}"
    notifuse     = "https://email.${var.base_domain}"
    minio        = "https://s3.${var.base_domain}"
    matomo       = "https://analytics.${var.base_domain}"
    vaultwarden  = "https://vault.${var.base_domain}"
    uptime_kuma  = "https://status.${var.base_domain}"
    traefik      = "https://traefik.${var.base_domain}"
    erp          = "https://erp.${var.base_domain} (if ERPNext enabled)"
  }
}

output "dns_record_instructions" {
  description = "DNS records you need to create at your domain registrar"
  value = <<-EOT
    Create the following DNS records at your domain registrar:

    Type    Name    Value                          TTL
    A       *       ${hcloud_server.technomancer.ipv4_address}    300
    A       @       ${hcloud_server.technomancer.ipv4_address}    300

    The wildcard A record (*) covers all subdomains (workflow., email., s3., etc.)
    Once records propagate (~5–15 minutes), Traefik will auto-provision SSL certificates.
  EOT
}

output "volume_id" {
  description = "Data volume ID (if created)"
  value       = var.create_separate_volume ? hcloud_volume.technomancer_data[0].id : "No separate volume created"
}
