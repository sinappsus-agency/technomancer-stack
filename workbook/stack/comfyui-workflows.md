# ComfyUI Workflow Management Guide

**Purpose:** How to export workflows from ComfyUI, import them into the Technomancer Stack's MCP server, and share them with others.

---

## Overview

The Technomancer Stack includes an MCP server that wraps ComfyUI's REST API. This lets AI agents (GitHub Copilot, Claude, etc.) generate images and video using your local ComfyUI installation — no cloud, no API keys.

Workflows are the core of ComfyUI. This guide covers the full lifecycle:

1. **Create** a workflow in ComfyUI (or download one from the community)
2. **Save or export** it (both graph format and API format are supported)
3. **Import** it into the MCP server with auto-detected parameters
4. **Run** it through the AI agent with custom inputs
5. **Share** it with others who can import your templates

---

## Part 1: Understanding Workflow Formats

ComfyUI uses two JSON formats. You need to know the difference.

### Graph Format (UI Format)

- Created by: **Save** or **Export** in ComfyUI
- Contains: Node positions, colours, group boxes, UI layout, connections
- Used by: The ComfyUI canvas (drag-and-drop to load)
- **Cannot** be submitted to the REST API directly

### API Format

- Created by: **Export (API Format)** in ComfyUI
- Contains: Only execution data — node types, inputs, and connections
- Used by: The REST API, the MCP server, automation scripts
- **This is what we use for templates**

### How to tell which format you have

Open the `.json` file. If the top-level keys are numbers (`"1"`, `"2"`, etc.) and each contains a `"class_type"` field — it's API format. If you see `"nodes"`, `"links"`, and `"groups"` at the top level — it's graph format.

**API format example:**
```json
{
  "4": {
    "class_type": "CheckpointLoaderSimple",
    "inputs": { "ckpt_name": "model.safetensors" }
  }
}
```

**Graph format example:**
```json
{
  "nodes": [...],
  "links": [...],
  "groups": [...]
}
```

---

## Part 2: Exporting from ComfyUI

The MCP server's `import_workflow` tool accepts **both** ComfyUI workflow formats. You can use whichever is most convenient.

### Option A: Use your ComfyUI saves directly (easiest)

Every time you press **Ctrl+S** or choose **Save** in ComfyUI, the workflow is saved to ComfyUI's user data directory on disk. The MCP server can read these files directly:

```
> list_saved_workflows()
> import_workflow("MyWorkflow.json", "my-template")
```

No manual copying needed.

### Option B: Export API Format (traditional)

1. Open ComfyUI and load or build your workflow
2. Make sure it runs successfully at least once (verify outputs look correct)
3. Click the **hamburger menu** (☰) in the top-left corner
4. Select **Export (API Format)**
5. Save the `.json` file to: `technomancer-stack/comfyui/exports/`

### Option C: Drop any JSON file

You can also pass an absolute file path to `import_workflow` — it works with any `.json` workflow file on your system, in either format.

> **Note:** In previous versions, only API-format exports were supported. The server now auto-detects graph-format files and converts them during import — handling subgraph expansion, Reroute node elimination, and widget value mapping automatically.

### Tips for clean exports

- **Name your nodes:** Before exporting, give meaningful titles to key nodes (right-click → Title). The import tool uses these titles to detect parameters. A node titled "Positive Prompt" will be auto-detected; "CLIP Text Encode" might not.
- **Test first:** Always verify the workflow produces correct output before exporting. The MCP server submits workflows as-is, so broken workflows will fail.
- **Keep defaults reasonable:** The values in your export become the defaults in the template. Set seed to something memorable, use good prompt text, and pick sensible dimensions.

---

## Part 3: Importing into the MCP Server

### Directory layout

```
comfyui/
  exports/        ← Drop API-format or graph-format exports here
  workflows/      ← Parameterized templates (auto-generated)
  mcp/
    server.py     ← The MCP server (15 tools)
```

### Fastest path: import from ComfyUI saves

If you saved the workflow in ComfyUI (Ctrl+S), you can import directly:

```
> list_saved_workflows()

Saved workflows in C:\ComfyUI\user\default\workflows:
  1. ImageZimageGeneration.json  (42 KB)
  2. LTXimageAndAudioToVideo.json  (37 KB)
  3. textToaudio_ace_step_1_5_split_4b.json  (18 KB)

> import_workflow("LTXimageAndAudioToVideo.json", "ltx23-video")
```

The server resolves bare filenames by checking: `exports/` → ComfyUI saved directory → current directory.

### Using scan_exports

If you prefer to use the `exports/` drop folder:

```
> scan_exports()

Found 2 export(s) in: .../comfyui/exports

Ready to import:
  → video_ltx2_3_ia2v.json (53 nodes, 14 KB) — ready to import

Already imported:
  ✓ sdxl-basic-t2i.json (10 nodes, 4 KB) — already imported
```

### Using import_workflow

```
> import_workflow("video_ltx2_3_ia2v.json", "ltx23-video")
```

This does four things automatically:

1. **Reads** the JSON from any supported source (exports folder, ComfyUI saves, or absolute path)
2. **Converts** graph-format files to API format (if needed) — handles subgraph expansion, Reroute elimination, and widget value mapping
3. **Detects** configurable inputs: prompts, seeds, models, dimensions, LoRAs, etc.
4. **Saves** a parameterized template to `workflows/ltx23-video.json`

### What gets auto-detected

The import tool scans for these node types and creates `PARAM_*` placeholders:

| Node Type | Detected Inputs |
|-----------|----------------|
| `CheckpointLoaderSimple` | Model checkpoint name |
| `LoraLoader` | LoRA adapter name |
| `LoadImage` | Input image file |
| `LoadAudio` | Input audio file |
| `RandomNoise` | Noise seed |
| `KSampler` | Random seed |
| `EmptyLatentImage` | Width, height |
| `CLIPTextEncode` | Positive/negative prompts |
| Primitive nodes | Width, height, prompt, seed, steps, CFG, denoise, duration, FPS |

Prompts are classified as positive or negative based on the node title and content analysis.

### After importing

Review the detected parameters:

```
> inspect_workflow("ltx23-video")
```

Run with custom values:

```
> run_workflow("ltx23-video", '{"PARAM_PROMPT": "a dragon flying over mountains", "PARAM_NOISE_SEED": 12345}')
```

---

## Part 4: The PARAM Placeholder System

### How it works

Templates use `PARAM_*` strings as placeholders for values that change between runs. The `_meta.params` block at the root of the JSON maps each placeholder to:

- **node**: Which node ID to patch
- **key**: Which input field to replace
- **type**: Expected data type (string, int, float, combo, file)
- **description**: Human-readable explanation

### Example _meta block

```json
{
  "_meta": {
    "name": "ltx23-video",
    "description": "Auto-imported workflow with 11 configurable parameters.",
    "params": {
      "PARAM_PROMPT": {
        "node": "340:319",
        "key": "value",
        "type": "string",
        "description": "Text prompt"
      },
      "PARAM_NOISE_SEED": {
        "node": "340:285",
        "key": "noise_seed",
        "type": "int",
        "description": "Random seed for noise generation"
      }
    }
  },
  "4": { "class_type": "...", "inputs": { ... } },
  ...
}
```

When you call `run_workflow("ltx23-video", '{"PARAM_PROMPT": "hello world"}')`, the server:

1. Loads the template
2. Finds `PARAM_PROMPT` in `_meta.params` → node `340:319`, key `value`
3. Sets `workflow["340:319"]["inputs"]["value"] = "hello world"`
4. Strips the `_meta` block
5. Submits to ComfyUI's `/prompt` endpoint

### Manual parameter editing

You can always edit the `_meta.params` block manually to:
- Add parameters the auto-detection missed
- Remove parameters you want to stay fixed
- Rename parameters for clarity
- Change types (e.g., `float` → `int`)

---

## Part 5: Sharing Workflows

### For other Technomancer Stack users

Share the files in `comfyui/exports/` and `comfyui/workflows/`:

- `exports/*.json` — The original API-format exports (can be re-imported, modified, or loaded into ComfyUI)
- `workflows/*.json` — Parameterized templates ready for the MCP server

Another user with the same models installed can:
1. Clone the repo
2. Start ComfyUI
3. Start the MCP server
4. Call `run_workflow("template-name", '{"PARAM_PROMPT": "their prompt"}')` immediately

### Loading templates back into ComfyUI

Templates in `workflows/` are valid API-format JSON (with an extra `_meta` block that ComfyUI ignores). To load one back into ComfyUI:

1. Open ComfyUI
2. Drag the `.json` file onto the canvas, OR click **Load** and select it
3. ComfyUI will render the workflow — `PARAM_*` placeholder values will appear as literal text in input fields
4. Replace the placeholder values with your actual inputs
5. Run the workflow normally

For the cleanest experience, load from `exports/` instead (which has real default values, no placeholders).

### For the wider ComfyUI community

If you want to share a workflow with someone who doesn't use the Technomancer Stack:

1. Open the workflow in ComfyUI
2. Use **Export** (the regular one, NOT API format) — this preserves the canvas layout
3. Share the resulting `.json` file — they can drag-and-drop it into their ComfyUI

---

## Part 6: Workflow Inventory

Current templates in this repository:

| Template | Description | Parameters | Notes |
|----------|------------|------------|-------|
| `sdxl-basic-t2i` | SDXL text-to-image | 8 | Requires SDXL checkpoint |
| `ltx23-img-audio-to-video` | LTX-Video 2.3 image+audio→video | 9 | 53 nodes, manually authored |

After importing your exports, run `list_workflow_templates()` to see the current full list.

---

## Part 7: Troubleshooting

### "This doesn't look like API-format JSON"

This error is from older versions. The current server auto-detects and converts graph-format workflows during import. If you see this, update your `server.py` to the latest version.

### "Template already exists"

A template with that name is already in `workflows/`. Either:
- Choose a different `template_name`
- Delete the existing file and re-import

### Parameters not detected

The auto-detection uses heuristics. If an important input wasn't detected:
1. Open the template in `workflows/`
2. Add the parameter manually to `_meta.params`
3. Follow the existing format: `{ "node": "ID", "key": "input_name", "type": "string", "description": "..." }`

### Compound node IDs (e.g., "57:27")

Workflows with subgraphs produce node IDs in the format `parent:inner`. This is normal — it matches ComfyUI's own convention. Parameters referencing these nodes will use compound IDs in the template's `_meta.params` block.

### Workflow fails when submitted

- Verify ComfyUI is running
- Check that all required models are installed (`list_models()`)
- Try running the original workflow in ComfyUI's canvas first

---

*See also:*
- `comfyui/SKILL.md` — Full ComfyUI skill reference for the AI agent
- `comfyui/exports/README.md` — Quick instructions for the exports drop folder
- `workbook/stack/minimum-effective-stack.md` — Stack planning guide
