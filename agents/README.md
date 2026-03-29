# Agents

This directory contains all agent configurations, MCP server definitions, and multi-agent workflows used in the Technomancer Stack.

---

## What "Agents" Means Here

In this stack, an agent is any process that:

1. **Perceives context** — reads files, queries a database, receives a webhook, reads a CRM record
2. **Reasons** — routes through an LLM (local via Ollama or remote via OpenRouter)
3. **Acts** — calls a tool, triggers an n8n workflow, writes a file, sends a message

Agents are not magic. They are composed of prompts, tools, and routing logic. Every agent in this directory can be fully audited and modified.

---

## Directory Structure

```
agents/
├── content-machine/            # Multi-agent content production pipeline
├── mcp-servers/                # Model Context Protocol server configs
├── personal-ai-infrastructure/  # Personal AI memory + context layer
└── call-center/                # AI-powered automated call handling
```

---

## Integration Map

```
                    ┌─────────────────────────────────────┐
                    │           Ollama (local LLM)          │
                    │  llama3.2, mistral, phi3, nomic-embed │
                    └──────────────┬──────────────────────┘
                                   │ inference
              ┌────────────────────┴────────────────────────┐
              │                                              │
    ┌─────────▼──────────┐                     ┌────────────▼──────────┐
    │    MCP Servers      │                     │      n8n Workflows     │
    │  (tool layer for    │◄───────────────────►│  (orchestration + I/O) │
    │   LLM agents)       │                     │                        │
    └─────────────────────┘                     └────────────────────────┘
              │                                              │
    ┌─────────▼──────────┐                     ┌────────────▼──────────┐
    │  content-machine/   │                     │  personal-ai-infra/   │
    │  (produce content)  │                     │  (memory + context)   │
    └─────────────────────┘                     └────────────────────────┘
```

---

## Choosing: Ollama Local vs OpenRouter

| Scenario | Use Ollama (Local) | Use OpenRouter (Remote) |
|---|---|---|
| Client data in prompt | ✅ Always | ❌ Never |
| Proprietary methodology in prompt | ✅ Always | ❌ Never |
| Long-running batch jobs (cost) | ✅ Preferred | Use for small bursts |
| Highest reasoning quality needed | ❌ | ✅ (GPT-4o, Claude 3.5) |
| Voice/realtime latency | ❌ | ✅ |
| Air-gapped / no internet | ✅ | ❌ |

Set `AGENT_LLM_BACKEND` in `.env` to `ollama` or `openrouter` to switch. Most workflows support both via the `local-ai-processor.json` abstraction layer.

---

## Security Posture

All agent-to-agent and agent-to-tool communication inside this stack:

- Stays on the internal Docker network (`backend`) unless explicitly publishing
- Uses bearer token authentication for all n8n webhook triggers
- Never logs full prompt content to disk by default (configurable)
- Never sends client data or proprietary prompts to external APIs (Ollama local models only for sensitive work)

See `../docker/security-checklist.md` for full verification steps.
