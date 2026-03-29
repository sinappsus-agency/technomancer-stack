# MCP Servers

Model Context Protocol (MCP) is the open standard that lets LLM clients (Claude Desktop, OpenWebUI, Cursor, VS Code Copilot, etc.) connect to external tools and data sources. Each MCP server in this directory extends what an AI agent can perceive and do.

---

## Why Self-Host MCP Servers

Running your own MCP servers keeps tool execution on your infrastructure, eliminates per-call SaaS fees, and means sensitive file paths, database queries, and internal API calls never leave your network.

---

## Available MCP Servers in This Stack

### 1. `filesystem/`
Gives agents read/write access to specified directories on the host.

**Use cases:**
- Agent reads a brief from `/brand-os/02-content-source` and writes the output to `/brand-os/03-content-published`
- Agent accesses SOP templates for document generation
- Automated report writing to a monitored folder

**Config:** Restricts access to allowlist directories only. Never expose `/` or system paths.

---

### 2. `n8n-trigger/`
Exposes n8n webhook endpoints as callable MCP tools.

An LLM agent can say *"trigger the client onboarding workflow with these values"* and the MCP server translates that into an authenticated POST to the n8n webhook.

**Use cases:**
- Content agent triggers distribution workflow after drafting
- Call center agent triggers CRM update workflow after a call closes
- AI assistant triggers meeting-transcript-processor on command

**Security:** All webhooks require `Authorization: Bearer <token>` header. Token is stored in `.env` as `N8N_MCP_WEBHOOK_SECRET`.

---

### 3. `memory/`
Persistent, searchable memory store for agents using a local embedding model.

Built on: **nomic-embed-text** (via Ollama) + **PostgreSQL pgvector extension**

Provides:
- `memory_add(content, tags, importance)` — store a fact or context fragment
- `memory_search(query, limit)` — semantic search over stored memory
- `memory_get_recent(n)` — retrieve the n most recent entries
- `memory_forget(id)` — explicit removal

**Use cases:**
- Personal AI assistant remembers client preferences, past decisions, open loops
- Content agent learns what topics have already been covered
- Call center agent remembers caller history between sessions

---

### 4. `web-search/`
Connects to a local **SearXNG** instance (already in Docker compose) for private, logged web search.

**Use cases:**
- Research agent enriches briefs with current information
- Competitive intelligence queries without leaking queries to Google/Bing
- News monitoring for thought leadership content

**Config:** Points to `http://searxng:8080` on the internal `backend` network.

---

### 5. `database/`
Exposes read-only (configurable) SQL access to PostgreSQL for agents that need to query business data.

**Use cases:**
- Agent queries CRM for client context before drafting outreach
- Agent queries campaign performance tables to inform next email brief
- Agent reads SOP status logs to answer "what stage is Project X at"

**Security:**
- Read-only PostgreSQL role `agent_readonly` provisioned in `../config/postgres/init.sql`
- Connection string stored in `.env` as `AGENT_DB_URL`
- Never expose write access to agents without an explicit audit trail

---

## How to Run MCP Servers

MCP servers in this stack run as lightweight Node.js or Python processes. They can be added to the Docker compose or run as standalone processes.

### Option A — Add to docker-compose.yml (recommended)

```yaml
mcp-filesystem:
  image: node:20-alpine
  container_name: mcp-filesystem
  restart: unless-stopped
  working_dir: /app
  volumes:
    - ./agents/mcp-servers/filesystem:/app
    - /home/user/brand-os:/mnt/brand-os:ro   # adjust path
  command: node server.js
  networks:
    - backend
  environment:
    - ALLOWED_DIRS=/mnt/brand-os
```

### Option B — Standalone (local dev)

```bash
cd agents/mcp-servers/filesystem
npm install
node server.js
```

Then configure your LLM client (Claude Desktop, OpenWebUI, etc.) to point to `http://localhost:<port>/mcp`.

---

## Connecting Claude Desktop

In `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "technomancer-filesystem": {
      "command": "node",
      "args": ["/path/to/agents/mcp-servers/filesystem/server.js"],
      "env": {
        "ALLOWED_DIRS": "/path/to/brand-os"
      }
    },
    "technomancer-n8n": {
      "command": "node",
      "args": ["/path/to/agents/mcp-servers/n8n-trigger/server.js"],
      "env": {
        "N8N_BASE_URL": "https://n8n.yourdomain.com",
        "N8N_MCP_WEBHOOK_SECRET": "your-secret-here"
      }
    }
  }
}
```

---

## Security Rules for MCP Servers

1. **Never expose MCP server ports to the public internet.** They run on the internal network or localhost only.
2. **Filesystem MCP must use an explicit allowlist.** No wildcard `/` access.
3. **Database MCP uses a read-only role.** Any write operations go through n8n workflows with an explicit audit log.
4. **Always validate input.** MCP server handlers must sanitize all strings before passing to filesystem or database. Treat all LLM-generated input as untrusted (prompt injection risk).
5. **Log tool calls.** Every tool invocation should write a timestamped log entry so you can audit what agents did and when.
