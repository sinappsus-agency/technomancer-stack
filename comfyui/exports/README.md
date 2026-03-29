# ComfyUI Workflow Exports — Drop Zone

Place your ComfyUI workflow exports in this folder. Both **graph format** (Save/Ctrl+S) and **API format** (Export API Format) are accepted.

## How to get workflows here

### Option A: Export from ComfyUI

1. Open or build a workflow in ComfyUI
2. Click the **menu** (☰ or right-click the canvas)
3. Select **Export (API Format)** — or regular **Export** / **Save** (both work)
4. Save the `.json` file into **this folder** (`comfyui/exports/`)

### Option B: Import directly from ComfyUI saves

You don't need to copy files here at all. The MCP server can read your saved workflows directly:

```
> list_saved_workflows()
> import_workflow("MyWorkflow.json", "my-template")
```

The server checks: `exports/` → ComfyUI saved workflows dir → current directory.

## What happens next

The MCP server has tools that work with this folder:

- **`scan_exports()`** — Lists all `.json` files here that haven't been imported yet
- **`import_workflow(filename)`** — Auto-detects format (graph or API), converts if needed, detects configurable inputs (prompts, seeds, models, dimensions) and saves a parameterized template to `comfyui/workflows/`

After import, use:
- `inspect_workflow("template-name")` — Review detected parameters
- `run_workflow("template-name", '{"PARAM_PROMPT": "your prompt"}')` — Execute with custom values

## Folder relationship

```
comfyui/
  exports/        ← YOU PUT FILES HERE (raw API exports)
  workflows/      ← TEMPLATES LIVE HERE (auto-parameterized, ready to run)
```

## Can I import our templates back into ComfyUI?

Yes. The templates in `workflows/` are valid API-format JSON. In ComfyUI:

1. Open ComfyUI
2. Click **Load** (or drag-and-drop the `.json` file onto the canvas)
3. ComfyUI will load the workflow — `PARAM_*` placeholder values will appear as literal strings in the input fields, which you can replace manually

For the cleanest experience, keep the original export in `exports/` (no PARAM placeholders) alongside the parameterized version in `workflows/`.
