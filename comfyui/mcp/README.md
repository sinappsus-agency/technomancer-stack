# ComfyUI Local MCP Server

A local MCP (Model Context Protocol) server that wraps the ComfyUI REST API for use with **GitHub Copilot Agent mode in VS Code** and any other MCP-compatible AI client.

No accounts. No cloud subscriptions. No API keys. Just your local ComfyUI instance talking to your AI assistant over a stdio pipe.

---

## Prerequisites

| Requirement | How to get it |
|-------------|---------------|
| Python 3.11+ | Already installed if you followed the stack setup |
| `uv` (fast Python runner) | `pip install uv` or `winget install astral-sh.uv` |
| ComfyUI Desktop (Windows) | `https://download.comfy.org/windows/nsis/x64` |
| VS Code 1.99+ | code.visualstudio.com |
| GitHub Copilot extension | `code --install-extension GitHub.copilot-chat` |

---

## Quick Start

### 1. Verify the server runs standalone

With ComfyUI Desktop open and running:

```bash
# From the technomancer-stack root:
uv run comfyui/mcp/server.py
```

You should see the MCP server start up. Press `Ctrl+C` to stop. If ComfyUI is not running, the server starts fine but tool calls will return connection errors until you start ComfyUI.

`uv run` reads the PEP 723 inline script metadata at the top of `server.py` and automatically installs the `mcp` package into an isolated environment. No manual `pip install` needed.

**Without uv:**
```bash
pip install mcp
python comfyui/mcp/server.py
```

### 2. Register the server in VS Code

The technomancer-stack workspace includes `.vscode/settings.json` with the server pre-configured. If you need to add it manually, open your workspace or user `settings.json` and add:

```json
{
  "mcp": {
    "servers": {
      "comfyui-local": {
        "type": "stdio",
        "command": "uv",
        "args": ["run", "${workspaceFolder}/comfyui/mcp/server.py"],
        "env": {
          "COMFYUI_URL": "http://127.0.0.1:8000"
        }
      }
    }
  }
}
```

If you are not using `uv`, replace `"command": "uv"` and `"args": ["run", "..."]` with:
```json
"command": "python",
"args": ["${workspaceFolder}/comfyui/mcp/server.py"]
```

### 3. Reload and verify

`Ctrl+Shift+P → Reload Window`

Open Copilot Chat (`Ctrl+Alt+I`), switch to **Agent** mode, and click the tools icon (⚙). You should see `comfyui-local` listed with its tools.

---

## Available Tools (15)

### Generation & Execution

| Tool | Description |
|------|-------------|
| `generate_image` | Full SDXL pipeline: prompt → workflow → submit → poll → image URL |
| `run_workflow` | Load template → fill PARAM placeholders → submit → poll → outputs |
| `submit_workflow` | Submit raw API-format workflow JSON (fire-and-forget) |
| `get_history` | Poll a prompt_id for completed output URLs |
| `get_queue` | Check running/pending jobs |

### Models & Node Info

| Tool | Description |
|------|-------------|
| `list_models` | List installed models by type (28 categories via /api/models) |
| `get_node_info` | Query what inputs a ComfyUI node type accepts |
| `upload_file` | Upload image/audio to ComfyUI's input directory |

### Workflow Templates

| Tool | Description |
|------|-------------|
| `list_workflow_templates` | List available parameterized templates in `workflows/` |
| `load_workflow_template` | Load raw template JSON for inspection or editing |
| `inspect_workflow` | Show a template's PARAM placeholders and defaults |

### Import Pipeline

| Tool | Description |
|------|-------------|
| `list_saved_workflows` | List workflows saved in ComfyUI's user data directory on disk |
| `import_workflow` | Import graph or API format → auto-convert → auto-detect PARAMs → save template |
| `scan_exports` | List unimported API-format exports in the `exports/` drop folder |

### Import Workflow Formats

`import_workflow` accepts **both** ComfyUI workflow formats:

- **Graph format** (from ComfyUI's Save/Ctrl+S) — automatically converted to API format. Handles subgraph expansion, Reroute elimination, and widget value mapping.
- **API format** (from Export API Format) — used directly.

File resolution for bare filenames: `exports/` → ComfyUI saved dir → current directory.

---

## Example Copilot prompts (Agent mode)

```
List my saved workflows in ComfyUI and import the image generation one.
```

```
List my available models and generate an image of a rain-soaked 
Tokyo street at night, neon reflections, cinematic, SDXL quality.
```

```
Run the z-image-turbo template with the prompt 
"a lone figure in a brutalist server room, dramatic lighting".
```

```
Import the video workflow from my ComfyUI saves, then inspect 
its parameters so I can see what I need to fill in.
```

---

## Configuration

### Changing the ComfyUI URL

By default the server connects to `http://127.0.0.1:8000` (the ComfyUI Desktop default). Override with the `COMFYUI_URL` environment variable in your `settings.json`:

```json
"env": {
  "COMFYUI_URL": "http://your-vps-address:8188"  
}
```

This is useful if you want to route generation to a remote GPU server instead of your local machine.

### Custom workflow templates

Drop any ComfyUI workflow JSON into `comfyui/workflows/` or use `import_workflow` to auto-convert and save templates. Templates support both graph format (ComfyUI's native Save/Ctrl+S) and API format (Export API Format). Graph files are automatically converted during import.

You can also import directly from your ComfyUI saved workflows directory — use `list_saved_workflows` to see what's available, then `import_workflow` with the filename.

---

## How It Works

```
VS Code Copilot Agent
        │
        │  stdio (MCP protocol)
        ▼
comfyui/mcp/server.py  (this file, run by uv)
        │
        │  HTTP REST
        ▼
ComfyUI Desktop / Portable
http://127.0.0.1:8000
        │
        ▼
Your local GPU
```

The MCP server is a thin translation layer. It receives tool calls from Copilot, converts them to ComfyUI REST API calls, and returns the results. All computation happens in ComfyUI on your local hardware. Nothing leaves your machine.

---

## Troubleshooting

**Server not appearing in Copilot tool list:**
- Reload VS Code window after adding it to `settings.json`
- Confirm the path in `args` resolves correctly — use an absolute path if `${workspaceFolder}` is not substituting

**"Cannot reach ComfyUI" errors:**
- ComfyUI Desktop or Portable must be running *before* you invoke a tool
- Check `COMFYUI_URL` matches your actual ComfyUI port (default 8000 for Desktop, 8188 for Portable/Docker)
- If ComfyUI shows a different port in its terminal output, update the env var

**`uv` not found:**
- Install: `pip install uv` or `winget install astral-sh.uv`
- Or switch to `"command": "python"` in settings.json (requires `pip install mcp` first)

**Workflow node errors (from ComfyUI):**
- The `generate_image` tool uses SDXL node structure — if your checkpoint is Flux.1 or another architecture, it requires a different workflow structure
- Use `submit_workflow` with a Flux-compatible template from `comfyui/workflows/` instead
