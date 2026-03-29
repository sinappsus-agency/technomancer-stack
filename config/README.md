# Configuration Files

Service-specific configuration files used by the Docker Compose stack in `docker/docker-compose.yml`. These files are mounted as volumes into their respective containers.

---

## Directory Structure

```
config/
├── traefik/
│   ├── traefik.yml           # Traefik v3 static configuration (entrypoints, providers, ACME)
│   └── dynamic.yml           # Dynamic routing rules (middleware, TLS options, rate limiting)
├── postgres/
│   └── init.sql              # Database initialization — creates databases, pgvector extension, role grants
└── clickhouse/
    ├── clickhouse-config.xml         # ClickHouse server configuration
    └── clickhouse-user-config.xml    # ClickHouse user-level settings
```

---

## Usage

These files are automatically mounted by Docker Compose. You should not need to edit them unless you are:

- **Adding a new subdomain** → edit `traefik/dynamic.yml`
- **Adding a new database** → edit `postgres/init.sql`
- **Tuning ClickHouse performance** → edit `clickhouse/clickhouse-config.xml`

For environment-specific values (domains, API keys, passwords), use the `.env` file in `docker/` — not these config files.

---

## Book Reference

**Chapter 8 — The Self-Hosted Sovereign** covers the full infrastructure setup including Traefik reverse proxy configuration and database initialization.
