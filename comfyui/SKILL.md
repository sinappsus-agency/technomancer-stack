# SKILL: Local ComfyUI — Image and Video Generation

## What This Skill Is For

This skill teaches GitHub Copilot (or any VS Code agent) how to work with a locally running ComfyUI instance using its REST API. Use this when you want to:

- Draft and optimize generation prompts for specific ComfyUI models
- Construct or modify ComfyUI workflow JSON files (API format)
- Submit workflows to the local ComfyUI server and retrieve outputs
- Route generated images to MinIO storage in the Technomancer Stack
- Understand model capabilities and choose the right model for a task

---

## Environment Assumptions

- ComfyUI Desktop (Windows) is running locally
- API available at: `http://127.0.0.1:8000`
- Model checkpoints are in the ComfyUI user data directory
- MinIO is running at `http://localhost:9000`, bucket: `technomancer-content`
- n8n is available at `http://localhost:5678` for workflow automation triggers

---

## ComfyUI API Basics

ComfyUI exposes a REST API on port 8000 (Desktop) or 8188 (Portable/Docker). The primary endpoint for running a workflow is:

```
POST http://127.0.0.1:8000/prompt
Content-Type: application/json

{
  "prompt": { ...workflow_api_json... },
  "client_id": "technomancer"
}
```

**Get available models:**
```
GET http://127.0.0.1:8000/object_info
```

**Get queue status:**
```
GET http://127.0.0.1:8000/queue
```

**Get history (completed outputs):**
```
GET http://127.0.0.1:8000/history
```

**Download an output file:**
```
GET http://127.0.0.1:8000/view?filename=ComfyUI_00001_.png&subfolder=&type=output
```

---

## Workflow JSON Format (API Format)

ComfyUI workflows exist in two formats:
- **Graph format** (.json from the Save button in the UI) — human-readable, contains layout info
- **API format** (.json from API > Save (API Format)) — what the REST API accepts, no layout info

Always use **API format** when calling the REST API or constructing workflows programmatically.

### Minimal SDXL Text-to-Image Workflow (API Format)

```json
{
  "4": {
    "class_type": "CheckpointLoaderSimple",
    "inputs": { "ckpt_name": "sd_xl_base_1.0.safetensors" }
  },
  "5": {
    "class_type": "EmptyLatentImage",
    "inputs": { "width": 1024, "height": 1024, "batch_size": 1 }
  },
  "6": {
    "class_type": "CLIPTextEncode",
    "inputs": {
      "text": "YOUR_POSITIVE_PROMPT_HERE",
      "clip": ["4", 1]
    }
  },
  "7": {
    "class_type": "CLIPTextEncode",
    "inputs": {
      "text": "YOUR_NEGATIVE_PROMPT_HERE",
      "clip": ["4", 1]
    }
  },
  "8": {
    "class_type": "KSampler",
    "inputs": {
      "seed": 42,
      "steps": 30,
      "cfg": 7.0,
      "sampler_name": "dpmpp_2m",
      "scheduler": "karras",
      "denoise": 1.0,
      "model": ["4", 0],
      "positive": ["6", 0],
      "negative": ["7", 0],
      "latent_image": ["5", 0]
    }
  },
  "9": {
    "class_type": "VAEDecode",
    "inputs": {
      "samples": ["8", 0],
      "vae": ["4", 2]
    }
  },
  "10": {
    "class_type": "SaveImage",
    "inputs": {
      "filename_prefix": "ComfyUI",
      "images": ["9", 0]
    }
  }
}
```

Node references use the format `["node_id", output_index]`.

---

## Model Capabilities

### SDXL (sd_xl_base_1.0.safetensors)
- **Best for:** General high-quality imagery, portraits, landscapes, product visuals
- **Resolution:** 1024×1024 native; use multiples of 64 for other sizes
- **KSampler settings:** steps 25–35, cfg 6–8, sampler: dpmpp_2m, scheduler: karras
- **Negative prompts:** Use extensively — SDXL responds well to negative guidance
- **Refiner:** Pair with `sd_xl_refiner_1.0.safetensors` at 80% base, 20% refiner for best quality

### Flux.1 Dev
- **Best for:** Exceptional prompt adherence, text rendering in images, photorealistic detail
- **Architecture difference:** Flux uses a diffusion transformer (DiT) — different node setup than SDXL
- **KSampler settings:** steps 20–30, cfg 1.0–3.5 (Flux needs low CFG), scheduler: simple
- **Guidance:** Flux uses a dual-text-encoder setup (CLIP + T5) — both must be loaded
- **Note:** Requires accepted HuggingFace terms of service to download. Available quantized as GGUF.

### Wan2.1 (Text-to-Video)
- **Best for:** Short video generation from text prompts, 4–6 second clips
- **Model size:** 14B parameters — requires significant VRAM (24GB+ recommended) or CPU offload
- **Output:** MP4 video, typically 16–24 frames at configurable FPS
- **Node:** Uses ComfyUI-Wan2.1 custom node package (install via ComfyUI Manager)
- **Prompt style:** More descriptive of motion and camera than still image prompts

### AnimateDiff (Image Animation)
- **Best for:** Animating SDXL outputs into short GIF/video clips
- **Workflow:** Standard SDXL text-to-image pipeline + AnimateDiff motion module
- **Custom node:** AnimateDiff-Evolved (install via ComfyUI Manager)

---

## Prompt Engineering for ComfyUI

### Positive Prompt Structure (SDXL)

```
[quality terms], [subject], [environment], [lighting], [camera/style], [additional detail]

Example:
masterpiece, best quality, ultra-detailed, 
a lone technomancer in a neon-lit server room, 
holographic displays reflected in their visor, 
dramatic side lighting, cinematic, 8k resolution, 
sharp focus, professional photography
```

**Effective quality terms:** `masterpiece`, `best quality`, `ultra-detailed`, `sharp focus`, `8k`, `cinematic`, `professional`

### Negative Prompt (SDXL)

```
worst quality, low quality, blurry, jpeg artifacts, 
extra limbs, malformed hands, mutated, ugly, duplicate, 
watermark, text, signature, cropped, out of frame
```

### Flux Prompts

Flux handles natural language prompts well — you do not need keyword stacking. Write a detailed description in plain language:

```
A lone figure silhouetted against a wall of glowing server racks 
in a darkened data centre, soft blue light from the screens 
illuminating their face from below, cinematic atmosphere, 
photorealistic, high detail
```

---

## Python: Submitting a Workflow via API

```python
import json
import urllib.request
import uuid

def submit_workflow(workflow: dict, server_url: str = "http://127.0.0.1:8000") -> str:
    """Submit a ComfyUI API-format workflow. Returns the prompt_id."""
    payload = json.dumps({
        "prompt": workflow,
        "client_id": str(uuid.uuid4())
    }).encode("utf-8")
    
    req = urllib.request.Request(
        f"{server_url}/prompt",
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read())
    return result["prompt_id"]


def get_output_files(prompt_id: str, server_url: str = "http://127.0.0.1:8000") -> list[str]:
    """Poll history for completed output filenames."""
    import time
    for _ in range(60):  # up to 60 seconds
        with urllib.request.urlopen(f"{server_url}/history/{prompt_id}") as response:
            history = json.loads(response.read())
        if prompt_id in history:
            outputs = history[prompt_id]["outputs"]
            files = []
            for node_output in outputs.values():
                if "images" in node_output:
                    files.extend(img["filename"] for img in node_output["images"])
            return files
        time.sleep(1)
    return []
```

---

## n8n Integration: Calling ComfyUI from a Workflow

Use an n8n **HTTP Request** node to submit a workflow and a **Wait** + second **HTTP Request** node to poll for results.

**HTTP Request node — Submit workflow:**
- Method: POST  
- URL: `http://127.0.0.1:8000/prompt`
- Body: JSON — paste your API-format workflow JSON with `prompt` and `client_id` keys
- Output: capture `body.prompt_id`

**HTTP Request node — Poll history:**
- Method: GET  
- URL: `http://127.0.0.1:8000/history/{{ $json.prompt_id }}`
- Run in a loop with a Wait node between polls

**Download image:**
- URL: `http://127.0.0.1:8000/view?filename={{ $json.filename }}&type=output`
- Method: GET, response as binary

---

## Routing Outputs to MinIO

After downloading the generated image as binary in n8n, upload to MinIO using the **S3** node or HTTP Request:

```
PUT http://localhost:9000/technomancer-content/generated/{filename}
Authorization: AWS-format signature (or use n8n's built-in S3 credentials)
Content-Type: image/png
Body: [binary image data]
```

Store the MinIO object URL (`http://localhost:9000/technomancer-content/generated/{filename}`) for further use in your workflow.

---

## Custom Nodes (Install via ComfyUI Manager)

| Node Pack | Purpose |
|-----------|---------|
| ComfyUI-Manager | GUI for installing/updating all other custom nodes |
| WAS Node Suite | Extended image processing, text, and utility nodes |
| ComfyUI-Impact-Pack | Face detection, segmentation, detailing (ADetailer equivalent) |
| AnimateDiff-Evolved | Video generation from SDXL checkpoints |
| ComfyUI_IPAdapter_plus | Image reference for style/character/face consistency |
| ComfyUI-Wan2.1 | Wan2.1 text-to-video integration |
| ComfyUI-API-Nodes | Extended API connection and HTTP nodes |
| rgthree-comfy | Better reroute nodes, bookmark nodes, power prompter |
| ComfyUI-Custom-Scripts | Additional utilities and quality-of-life nodes |

---

## Workflow Templates in This Repository

| File | Description |
|------|-------------|
| `workflows/sdxl-basic-t2i.json` | SDXL text-to-image, API format, parameterised prompts |
| `workflows/ltx23-img-audio-to-video.json` | LTX-Video 2.3 image+audio-to-video, 53 nodes |
| `workflows/sdxl-with-refiner.json` | SDXL base + refiner pipeline for highest quality |
| `workflows/flux-dev-t2i.json` | Flux.1 Dev text-to-image |
| `workflows/animatediff-t2v.json` | SDXL + AnimateDiff motion module, outputs MP4 |
| `workflows/wan21-t2v.json` | Wan2.1 text-to-video (requires 24GB+ VRAM) |
| `workflows/img2img-sdxl.json` | SDXL image-to-image with strength parameter |

Templates are auto-generated from workflow imports. To add new ones, see the workflow import section below.

---

## Workflow Import / Export Pipeline

### Directory structure

```
comfyui/
  exports/        ← Drop API-format exports here (staging area)
  workflows/      ← Parameterized templates (auto-generated by import_workflow)
  mcp/
    server.py     ← MCP server (15 tools)
```

ComfyUI's saved-workflows directory (default `C:\ComfyUI\user\default\workflows\`) is also readable by the MCP server. Set the `COMFYUI_PATH` environment variable if ComfyUI is installed elsewhere.

### Adding new workflows

There are three ways to import a workflow:

**Option A — Direct from ComfyUI saves (recommended):**
1. Save your workflow in ComfyUI (Ctrl+S or File → Save)
2. Use `list_saved_workflows()` to see what's available
3. Use `import_workflow("filename.json", "template-name")` — graph format is auto-converted

**Option B — API-format export (classic):**
1. In ComfyUI, click **menu → Export (API Format)**
2. Save the `.json` to `comfyui/exports/`
3. Use `scan_exports()` to see what's ready to import
4. Use `import_workflow("filename.json", "template-name")`

**Option C — Absolute path:**
1. Use `import_workflow("/full/path/to/workflow.json", "template-name")`
2. Works with both graph format and API format files

### Graph-to-API conversion

`import_workflow()` automatically detects whether a file is graph format (has `nodes`/`links`) or API format (has `class_type` entries). Graph-format files are converted on the fly:

- Subgraph (component) nodes are expanded into their inner nodes
- Reroute nodes are eliminated — connections are traced to real sources
- Widget values are mapped using ComfyUI's `/object_info` API and surplus detection for hidden widgets
- Inner node IDs use compound format (`parent:inner`) matching ComfyUI's own export convention

### The PARAM placeholder system

Templates use `PARAM_*` strings as placeholders. The `_meta.params` dict maps each one to a specific node/input/type. When `run_workflow()` is called, placeholders are replaced with actual values and type-cast automatically.

Auto-detected parameters include: prompts (positive/negative), seeds, model checkpoints, LoRAs, dimensions, duration, FPS, input images, and audio files.

### Sharing with users

- `exports/` files are raw ComfyUI API-format — can be loaded back into ComfyUI via drag-and-drop
- `workflows/` files are parameterized templates — valid API JSON that ComfyUI can also load (PARAM_* values appear as literal strings the user replaces manually)
- For non-MCP users, export from ComfyUI using the regular **Export** button (graph format with layout) to share canvas-ready workflows

Full documentation: `workbook/stack/comfyui-workflows.md`

---

## MCP Server Tools (15 tools)

| Tool | Purpose |
|------|---------|
| `generate_image` | Text-to-image with any SDXL-compatible checkpoint |
| `run_workflow` | Load template → fill PARAMs → submit → poll → return outputs |
| `submit_workflow` | Fire-and-forget raw JSON submission |
| `get_history` | Poll a prompt_id for output URLs with rich metadata |
| `get_queue` | Check running/pending jobs |
| `upload_file` | Upload image/audio to ComfyUI input directory |
| `list_models` | List installed models by type (28 categories via /api/models) |
| `get_node_info` | Query what inputs a ComfyUI node type accepts |
| `inspect_workflow` | Show a template's PARAM placeholders and defaults |
| `list_workflow_templates` | List available workflow templates |
| `load_workflow_template` | Load raw template JSON for manual editing |
| `import_workflow` | Import a workflow (graph or API format), auto-convert and auto-detect PARAMs |
| `scan_exports` | List unimported API-format exports in the exports/ drop folder |
| `list_saved_workflows` | List workflows saved in ComfyUI's user data directory on disk |

---

## Agent Instructions

When assisting with ComfyUI tasks:

1. **Both formats accepted** — `import_workflow()` handles graph format (from ComfyUI Save) and API format (from Export API Format). Graph format is auto-converted. When constructing workflows programmatically, use API format.
2. **Check saved workflows first** — use `list_saved_workflows()` before asking the user to export or locate files. Most workflows they've built are already saved in ComfyUI's user data directory.
3. **Check the model** — ask which checkpoint is installed if the task requires a specific model capability
4. **Scale resolution to the model** — SDXL works at 1024×1024; Flux works well at 768–1024; use multiples of 64
5. **Adjust CFG for Flux** — if generating Flux workflows, set cfg to 1.0–3.5, not the SDXL default of 7
6. **Name nodes clearly** — when constructing complex multi-node workflows, use descriptive `title` fields in node metadata so the workflow is readable in the ComfyUI canvas
7. **Save workflows to the repo** — output any new workflow JSON to `comfyui/workflows/` with a descriptive filename
8. **Use scan_exports for API exports** — when the user has API-format exports in the drop folder
9. **Prefer import_workflow** — auto-detection handles most common node types; only manual editing needed for exotic custom nodes
10. **Compound node IDs** — workflows with subgraphs use `parent:inner` format IDs (e.g. `"340:319"`). This is normal and matches ComfyUI's own convention.
