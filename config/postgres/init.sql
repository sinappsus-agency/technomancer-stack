-- PostgreSQL Initialisation Script
-- c:\Users\artgr\OneDrive\BACKUP\HTH\technomancer-stack\config\postgres\init.sql
--
-- Executed once when the postgres container is first created.
-- If the data volume already exists, this script is NOT re-run.
-- To re-run: remove the postgres-data volume and restart.
--
-- The POSTGRES_USER and POSTGRES_DB environment variables in docker-compose
-- create the primary user and database automatically. This script adds the
-- additional databases needed by n8n and Notifuse.

-- ── Create service databases ─────────────────────────────────────────────────

CREATE DATABASE n8n
    WITH
    OWNER = technomancer
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.utf8'
    LC_CTYPE = 'en_US.utf8'
    TEMPLATE = template0;

CREATE DATABASE notifuse
    WITH
    OWNER = technomancer
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.utf8'
    LC_CTYPE = 'en_US.utf8'
    TEMPLATE = template0;

-- ── Grant full privileges ─────────────────────────────────────────────────────

GRANT ALL PRIVILEGES ON DATABASE n8n TO technomancer;
GRANT ALL PRIVILEGES ON DATABASE notifuse TO technomancer;

-- ── Extensions (connect to each DB and enable) ───────────────────────────────

\connect n8n
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_stat_statements";

\connect notifuse
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ── Reconnect to default db ───────────────────────────────────────────────────
\connect postgres

-- ── Security hardening ───────────────────────────────────────────────────────
-- Prevent any user from creating objects in the public schema of non-owned dbs.
-- This is a defence-in-depth measure against schema pollution.
REVOKE CREATE ON SCHEMA public FROM PUBLIC;

-- Log connection counts for monitoring
ALTER SYSTEM SET log_connections = 'on';
ALTER SYSTEM SET log_disconnections = 'on';
ALTER SYSTEM SET log_duration = 'off';
-- log_duration off by default — enable temporarily if profiling slow queries.
