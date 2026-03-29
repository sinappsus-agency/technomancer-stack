# Personal AI Infrastructure

Implementation of the "Personal AI" model — a context-aware, memory-equipped assistant layer that knows your work, your clients, your preferences, and your operating standards well enough to extend your capacity without becoming a liability.

---

## The Model

The personal AI infrastructure is not a single chatbot. It is a layered context architecture:

```
┌─────────────────────────────────────────────────────────┐
│                     YOU (operator)                       │
│            (ultimate authority on all output)            │
└───────────────────────────┬─────────────────────────────┘
                            │ queries, commands, reviews
┌───────────────────────────▼─────────────────────────────┐
│               Personal AI Interface Layer                 │
│    (Claude Desktop, OpenWebUI, or custom UI via n8n)     │
│         Connected to MCP servers in this stack           │
└──────┬────────────────────┬───────────────────┬─────────┘
       │                    │                   │
┌──────▼──────┐   ┌─────────▼────────┐  ┌──────▼──────────┐
│  memory/    │   │  filesystem/     │  │  n8n-trigger/    │
│  (who you   │   │  (your docs,    │  │  (run workflows  │
│  are, what  │   │   briefs, SOPs) │  │   on command)   │
│  you know)  │   └──────────────────┘  └──────────────────┘
└─────────────┘
```

The key insight: *the assistant is only as intelligent as the context you give it.* A generic AI assistant knows nothing about your clients, your standards, or your current work. This infrastructure is what bridges that gap.

---

## Context Hierarchy

### Level 1 — Brand OS (static, rarely changes)
Your identity, standards, and operating philosophy. Loaded as system context in every session.

Files:
- `brand-os/01-strategy/origin-stack.md` — who you are, what you stand for
- `brand-os/01-strategy/brand-voice.md` — how you sound
- `../../prompts/brand/origin-stack-refinement.md` — LLM-optimized brand context file

### Level 2 — Client Context (per-client, updated per project)
One context file per client. The assistant loads the relevant client context when you name the client.

Format: `brand-os/05-clients/<client-slug>/context.md`

```markdown
# Client Context: [Company Name]
Last updated: YYYY-MM-DD

## Who they are
[2-3 sentence summary]

## What we're doing for them
[Current project, deliverables, timeline]

## Their communication style
[Direct/formal/casual, preferred channel, decision-maker contact]

## Open loops
- [ ] Waiting on brand questionnaire response
- [ ] Need to send revised timeline

## Notes from last conversation
[Key takeaways, decisions made, next actions]
```

### Level 3 — Project Context (per-project, updated frequently)
Brief, status, open questions, and blockers for active projects.

### Level 4 — Session Context (per-conversation)
What you're working on right now. The assistant uses previous messages + memory search to maintain thread continuity.

---

## Memory Store Configuration

The memory MCP server stores facts, decisions, and context fragments that should persist across sessions.

Categories:
- `client` — facts about clients
- `decision` — decisions made and their rationale
- `preference` — operating preferences ("I prefer short intros", "never send Monday morning")
- `knowledge` — domain knowledge worth preserving
- `open-loop` — things that need following up

Importance scoring: 1 (ephemeral) → 5 (permanent)

The assistant is trained (via system prompt) to:
- Proactively store decisions as `decision` category, importance 4
- Store client facts encountered in conversation as `client` category, importance 3–4
- Query memory before answering "do you remember" or "what did we decide about" questions

---

## Setup

### Step 1 — Enable pgvector in PostgreSQL

```sql
-- Run in your PostgreSQL instance (already in config/postgres/init.sql)
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE agent_memory (
  id SERIAL PRIMARY KEY,
  content TEXT NOT NULL,
  embedding vector(768),    -- nomic-embed-text dimension
  category VARCHAR(50),
  importance INTEGER DEFAULT 3,
  tags TEXT[],
  created_at TIMESTAMPTZ DEFAULT NOW(),
  last_accessed TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX ON agent_memory USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
```

### Step 2 — Pull the embedding model

```bash
ollama pull nomic-embed-text
```

### Step 3 — Configure .env

```
AGENT_MEMORY_DB_URL=postgresql://technomancer_user:password@postgres:5432/technomancer
AGENT_EMBEDDING_MODEL=nomic-embed-text
AGENT_EMBEDDING_ENDPOINT=http://ollama:11434
```

### Step 4 — Start the memory MCP server

```bash
# From agents/mcp-servers/memory/
npm install
node server.js
```

Or add to docker-compose (see `mcp-servers/README.md`).

---

## System Prompt Template

Every session should open with this system context loaded:

```
You are the personal AI assistant for [NAME], founder of [BUSINESS].

IDENTITY AND STANDARDS:
[Contents of brand-os/01-strategy/origin-stack.md]

YOUR TOOLS:
- memory_search: Search for stored facts, decisions, and context from previous work
- memory_add: Store important facts, decisions, or open loops for future sessions
- filesystem_read: Read documents, briefs, SOPs from the operator's brand-os
- n8n_trigger: Run automation workflows when explicitly instructed

RULES:
1. Always check memory before answering questions about past decisions or client facts.
2. Store any new decision made in this session to memory before the session ends.
3. Never send client data to external APIs. Use local models for sensitive content.
4. When uncertain, ask for clarification rather than inventing facts.
5. Flag when a request would require writing to filesystem or triggering a workflow — confirm before acting.
```

---

## OpenWebUI Integration

If you are using OpenWebUI (Docker service: `openwebui`), the MCP servers above can be connected as tool-use endpoints.

In OpenWebUI:
- Go to Settings → Tools
- Add each MCP server endpoint
- Assign them to the models you want to use them with

The `backend` Docker network allows OpenWebUI to reach MCP servers at their container names (e.g., `http://mcp-memory:3003`).
