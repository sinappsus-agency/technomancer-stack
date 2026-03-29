# Content Machine

A multi-agent pipeline for producing brand-consistent content at volume without grinding yourself into a content treadmill.

---

## The Problem This Solves

A solo operator's content bottleneck is almost never ideation. It is the conversion gap between "I have 40 good ideas" and "40 pieces are drafted, edited, formatted, and queued across five channels."

This pipeline closes that gap by decomposing content production into discrete agent roles, each with a specific prompt, specific tools, and specific handoff criteria.

---

## Agent Roles

### 1. Researcher
**Input:** Topic, audience stage, content angle
**Task:** Semantic search via `web-search` MCP + internal `memory` MCP for existing coverage
**Output:** Research brief (3–5 bullet claims with sources, gap analysis, hooks worth using)
**Model:** Local (Ollama / llama3.2) — no external data exposure needed for most research

### 2. Outliner
**Input:** Research brief + brand voice config (`prompts/brand/origin-stack-refinement.md`) + content format spec
**Task:** Produce a structured outline with section headers and a clear argument arc
**Output:** Numbered outline with estimated word counts per section
**Model:** Local preferred; remote (OpenRouter / Claude Haiku) for formats with strict structural requirements

### 3. Writer
**Input:** Outline + research brief + brand voice config + existing examples from memory store
**Task:** Write full draft, maintaining POV, voice, and argument thread from the outline
**Output:** Raw draft in Markdown
**Model:** Remote (Claude 3.5 Sonnet or GPT-4o) recommended for first-pass quality — OR local if content does not contain client/proprietary data

### 4. Editor
**Input:** Raw draft + brand standards (from voice config)
**Task:** Tighten sentences, flag off-brand language, verify factual claims match research brief, suggest hook rewrites
**Output:** Edited draft with inline comments for human review
**Model:** Local (Ollama) — this is a pass/fail check, not generative work

### 5. Formatter
**Input:** Edited draft + target channel spec
**Task:** Reformat for each channel (LinkedIn post, email, Twitter thread, video script, blog post)
**Output:** One file per format, following channel templates in `prompts/workflow/channel-formats.md`
**Model:** Local — formatting is deterministic enough for smaller models

### 6. Distributor
**Input:** Formatted content files
**Task:** Trigger the appropriate n8n distribution workflow via `n8n-trigger` MCP
**Output:** Queued post entries in n8n (confirmed via response payload)
**No model needed** — pure workflow trigger

---

## Pipeline Execution

### Option A — n8n Orchestrated (recommended)

The master content pipeline is defined in `../../n8n-templates/content-machine-pipeline.json` (to be imported).

Each node in n8n corresponds to an agent role above. The pipeline:
1. Accepts a brief via webhook (form submission, Telegram command, or direct n8n trigger)
2. Runs Researcher + Outliner in parallel for independent topics
3. Sequences Writer → Editor → Formatter with a human-review pause between Editor and Formatter
4. Routes to Distributor only after human approval

### Option B — CLI Orchestrated (dev/local)

```bash
# From this directory
python run_pipeline.py \
  --topic "Why most operators stall before they scale" \
  --audience "problem-aware" \
  --formats "linkedin,email,twitter" \
  --model "local"
```

Requires: Python 3.11+, `ollama` CLI accessible, `.env` populated

---

## Configuration

Create `config.yml` in this directory:

```yaml
brand_voice_file: ../../prompts/brand/origin-stack-refinement.md
memory_endpoint: http://localhost:3003/mcp    # memory MCP server
n8n_trigger_endpoint: http://localhost:3004/mcp  # n8n MCP server
default_llm_backend: ollama                   # ollama | openrouter
ollama_model: llama3.2
openrouter_model: anthropic/claude-3.5-haiku

output_dir: ~/brand-os/03-content-published
draft_dir: ~/brand-os/02-content-source

human_review_required: true                   # pause before Formatter step
auto_distribute: false                         # require explicit approval before posting
```

---

## Content Object Schema

Every piece of content tracked in this pipeline has a consistent object structure:

```json
{
  "id": "cma-2024-q1-001",
  "topic": "Why most operators stall before they scale",
  "audience_stage": "problem-aware",
  "research_brief": "...",
  "outline": "...",
  "draft_raw": "...",
  "draft_edited": "...",
  "formats": {
    "linkedin": "...",
    "email": "...",
    "twitter_thread": "..."
  },
  "status": "pending_human_review",
  "tags": ["positioning", "operations", "book-companion"],
  "created_at": "2024-01-15T09:00:00Z",
  "published_at": null
}
```

These objects are stored in PostgreSQL (`content_objects` table) and indexed in the memory MCP store for the Writer agent to reference when checking for topic duplication.

---

## Anti-Patterns to Avoid

- **Do not skip human review.** The Editor agent catches obvious problems; it does not catch subtle brand misalignment, factual overreach, or manufactured authority.
- **Do not run Writer with client data in the context.** If the research brief or outline contains client work, route to the local Ollama backend.
- **Do not let Distributor auto-post without approval.** The `auto_distribute: false` default exists for this reason.
