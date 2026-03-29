# ComfyUI — Visual Stack

The visual production layer of the Technomancer Stack. This directory gives you everything you need to generate images and video from VS Code using a locally running ComfyUI instance — no cloud subscriptions, no API keys.

**Book Reference:** Chapter 11 — The Visual Stack: ComfyUI, Stable Diffusion, and Generative Media

---

## Directory Structure

```
comfyui/
├── README.md               ← You are here
├── SKILL.md                ← Agent skill file — model reference, prompt engineering, API docs
├── mcp/
│   ├── README.md           ← MCP server setup guide
│   └── server.py           ← 15-tool MCP server (ComfyUI ↔ VS Code bridge)
├── workflows/              ← Parameterized workflow templates (ready to run)
│   ├── sdxl-basic-t2i.json
│   └── ltx23-img-audio-to-video.json
└── exports/                ← Staging area — drop raw ComfyUI exports here for import
    └── README.md           ← How to use the export → import pipeline
```

---

## How It Works

1. **ComfyUI Desktop** runs locally on your machine (port 8000)
2. The **MCP server** (`mcp/server.py`) wraps ComfyUI's REST API into 15 tools
3. **VS Code + GitHub Copilot** (Agent mode) can call those tools to generate images and video
4. **Workflow templates** in `workflows/` are parameterized — swap prompts, models, and settings without editing raw JSON
5. The **exports/** folder is a drop zone — export workflows from ComfyUI's UI, then use the MCP server's `import_workflow()` tool to auto-convert and parameterize them

---

## Quick Start

### Prerequisites

- ComfyUI Desktop installed and running (`http://127.0.0.1:8000`)
- Python 3.11+ with `uv` (`pip install uv`)
- VS Code 1.99+ with GitHub Copilot extension

### 1. Start the MCP Server

```bash
uv run comfyui/mcp/server.py
```

The server is pre-configured in `.vscode/settings.json` — after reloading VS Code, it appears automatically in Copilot's tool list.

### 2. Generate an Image (from Copilot Agent mode)

```
Generate a cinematic portrait of a technomancer in a neon-lit server room using SDXL.
```

Copilot calls `generate_image` → submits a workflow → polls for completion → returns the image URL.

### 3. Add Your Own Workflows

**From ComfyUI UI:**
1. Build or load a workflow in ComfyUI
2. Save it (Ctrl+S) or export as API format
3. In Copilot Agent mode: `Import my latest saved workflow as "my-template"`
4. The MCP server auto-detects format, converts if needed, and saves a parameterized template

**See also:** [exports/README.md](exports/README.md) for the full import/export pipeline.

---

## What's in SKILL.md

The `SKILL.md` file is an agent skill document — it teaches GitHub Copilot (or any VS Code agent) how to work with ComfyUI. It contains:

- ComfyUI API endpoint reference
- Model capabilities (SDXL, Flux.1 Dev, Wan2.1, AnimateDiff)
- Prompt engineering guidelines per model
- Python code for submitting workflows programmatically
- n8n integration patterns (HTTP Request → ComfyUI → MinIO)
- Custom node recommendations

You don't need to read SKILL.md yourself — it's automatically loaded by the agent when the ComfyUI skill is invoked.

---

## Available MCP Tools (15)

| Category | Tools |
|----------|-------|
| **Generation** | `generate_image`, `run_workflow`, `submit_workflow`, `get_history`, `get_queue` |
| **Models** | `list_models`, `get_node_info`, `upload_file` |
| **Templates** | `list_workflow_templates`, `load_workflow_template`, `inspect_workflow` |
| **Import** | `list_saved_workflows`, `import_workflow`, `scan_exports` |

Full tool documentation: [mcp/README.md](mcp/README.md)

---

## Workbook Integration

The companion workbook includes a ComfyUI planning template:

- **`workbook/stack/comfyui-workflows.md`** — Plan which workflows you need for your brand's visual production pipeline

---

## Extending the Stack

ComfyUI connects to the rest of the Technomancer Stack through n8n:

- **Content Machine** → n8n triggers ComfyUI to generate social media visuals for each post
- **MinIO** → Generated assets are stored in `technomancer-content` bucket for reuse
- **Brand LoRA** → Fine-tune a LoRA on your brand imagery for consistent visual identity across all generated content

These integration patterns are covered in Chapter 11 and the n8n workflow templates in `n8n-templates/`.
