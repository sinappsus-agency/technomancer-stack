#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["mcp>=1.0"]
# ///
"""
ComfyUI Local MCP Server — Technomancer Stack
==============================================
Wraps the ComfyUI REST API as MCP tools for GitHub Copilot Agent mode
in VS Code and other MCP-compatible AI clients.

No accounts. No cloud. No API keys. Just your local ComfyUI instance.

Usage:
    uv run server.py           (auto-installs mcp, runs server)
    python server.py           (requires: pip install mcp)

Environment variables:
    COMFYUI_URL    Base URL of your ComfyUI instance (default: http://127.0.0.1:8000)
    COMFYUI_PATH   ComfyUI installation path for reading saved workflows (default: C:\\ComfyUI)

ComfyUI must be running before any tool calls will succeed.

Tools:
    generate_image        Text-to-image with any SDXL-compatible checkpoint
    run_workflow          Load a template, fill PARAM placeholders, submit, poll, return outputs
    submit_workflow       Submit raw API-format JSON (fire-and-forget)
    get_history           Poll a prompt_id for output URLs
    get_queue             Check running/pending jobs
    upload_file           Upload image/audio to ComfyUI input directory
    list_models           List installed models by type (28 categories via /api/models)
    get_node_info         Query what inputs a ComfyUI node type accepts
    inspect_workflow      Show a template's PARAM placeholders and defaults
    list_workflow_templates  List available workflow templates
    load_workflow_template   Load raw template JSON for manual editing
    import_workflow       Import a workflow (API or graph format) and auto-detect PARAMs
    scan_exports          List unimported API-format exports in the exports/ drop folder
    list_saved_workflows  List workflows saved in ComfyUI's user data directory
"""

import json
import os
import random
import time
import uuid
from pathlib import Path

import urllib.error
import urllib.request

from mcp.server.fastmcp import FastMCP

# ── Configuration ──────────────────────────────────────────────────────────────

COMFYUI_URL = os.getenv("COMFYUI_URL", "http://127.0.0.1:8000").rstrip("/")

# Workflow templates directory relative to this file: comfyui/workflows/
WORKFLOW_DIR = Path(__file__).parent.parent / "workflows"

# Exports drop folder: users place raw API-format exports here for import
EXPORTS_DIR = Path(__file__).parent.parent / "exports"

# ComfyUI installation path (for reading saved workflows directly from disk)
COMFYUI_PATH = Path(os.getenv("COMFYUI_PATH", r"C:\ComfyUI"))
COMFYUI_SAVED_DIR = COMFYUI_PATH / "user" / "default" / "workflows"

mcp = FastMCP("comfyui-local")

# ── PARAM placeholder convention ───────────────────────────────────────────────
# Templates use string values starting with "PARAM_" to mark user-configurable
# inputs.  The _meta.params dict maps each PARAM_* key to the node/key/type it
# controls.  _fill_params() substitutes values and casts types automatically.

_PARAM_TYPE_CASTERS = {
    "int": int,
    "float": float,
    "string": str,
    "bool": lambda v: v if isinstance(v, bool) else str(v).lower() in ("true", "1", "yes"),
    "combo": str,
    "file": str,
}


def _fill_params(workflow: dict, params: dict[str, object]) -> dict:
    """Replace PARAM_* placeholders in a workflow with actual values.

    `params` maps PARAM names (e.g. "PARAM_POSITIVE_PROMPT") to their values.
    Type casting is driven by _meta.params[name].type when available.
    """
    meta = workflow.get("_meta", {})
    param_specs = meta.get("params", {})

    for param_name, value in params.items():
        spec = param_specs.get(param_name, {})
        node_id = spec.get("node")
        key = spec.get("key")
        ptype = spec.get("type", "string")

        # Cast value to the expected type
        caster = _PARAM_TYPE_CASTERS.get(ptype, str)
        try:
            typed_value = caster(value)
        except (ValueError, TypeError):
            typed_value = value

        if node_id and key:
            # Direct patch via spec
            if node_id in workflow and "inputs" in workflow[node_id]:
                workflow[node_id]["inputs"][key] = typed_value
        else:
            # Fallback: scan all nodes for the placeholder string
            for nid, node in workflow.items():
                if nid == "_meta":
                    continue
                inputs = node.get("inputs", {})
                for k, v in inputs.items():
                    if v == param_name:
                        inputs[k] = typed_value

    return workflow


# ── Internal helpers ───────────────────────────────────────────────────────────

def _get(path: str, timeout: int = 10) -> dict:
    """GET request to the ComfyUI API."""
    with urllib.request.urlopen(f"{COMFYUI_URL}{path}", timeout=timeout) as r:
        return json.loads(r.read())


def _post(path: str, data: dict) -> dict:
    """POST request to the ComfyUI API."""
    payload = json.dumps(data).encode()
    req = urllib.request.Request(
        f"{COMFYUI_URL}{path}",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def _upload_multipart(filepath: str, subfolder: str = "", file_type: str = "input") -> dict:
    """Upload a file to ComfyUI via multipart POST to /upload/image."""
    boundary = uuid.uuid4().hex
    filename = Path(filepath).name

    with open(filepath, "rb") as f:
        file_data = f.read()

    parts = [
        f"--{boundary}".encode(),
        f'Content-Disposition: form-data; name="image"; filename="{filename}"'.encode(),
        b"Content-Type: application/octet-stream",
        b"",
        file_data,
    ]
    if subfolder:
        parts += [
            f"--{boundary}".encode(),
            b'Content-Disposition: form-data; name="subfolder"',
            b"",
            subfolder.encode(),
        ]
    parts += [
        f"--{boundary}".encode(),
        b'Content-Disposition: form-data; name="type"',
        b"",
        file_type.encode(),
        f"--{boundary}".encode(),
        b'Content-Disposition: form-data; name="overwrite"',
        b"",
        b"true",
        f"--{boundary}--".encode(),
    ]

    body = b"\r\n".join(parts)
    req = urllib.request.Request(
        f"{COMFYUI_URL}/upload/image",
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def _collect_output_urls(history_entry: dict) -> list[str]:
    """Extract all output URLs (images + videos) from a history entry."""
    urls = []
    for node_out in history_entry.get("outputs", {}).values():
        for img in node_out.get("images", []):
            fname = img["filename"]
            sub = img.get("subfolder", "")
            typ = img.get("type", "output")
            urls.append(
                f"{COMFYUI_URL}/view?filename={fname}&subfolder={sub}&type={typ}"
            )
        for vid in node_out.get("videos", []):
            fname = vid["filename"]
            sub = vid.get("subfolder", "")
            typ = vid.get("type", "output")
            urls.append(
                f"{COMFYUI_URL}/view?filename={fname}&subfolder={sub}&type={typ}"
            )
    return urls


def _collect_output_files(history_entry: dict) -> list[dict]:
    """Extract output file metadata from a history entry."""
    files = []
    for node_id, node_out in history_entry.get("outputs", {}).items():
        for img in node_out.get("images", []):
            files.append({
                "node": node_id, "type": "image",
                "filename": img["filename"],
                "subfolder": img.get("subfolder", ""),
                "url": f"{COMFYUI_URL}/view?filename={img['filename']}&subfolder={img.get('subfolder', '')}&type={img.get('type', 'output')}",
            })
        for vid in node_out.get("videos", []):
            files.append({
                "node": node_id, "type": "video",
                "filename": vid["filename"],
                "subfolder": vid.get("subfolder", ""),
                "url": f"{COMFYUI_URL}/view?filename={vid['filename']}&subfolder={vid.get('subfolder', '')}&type={vid.get('type', 'output')}",
            })
    return files


def _poll_history(prompt_id: str, timeout: int) -> dict:
    """Poll /history until the job completes or timeout expires.

    Returns dict with keys: status ("success"|"error"|"timeout"), outputs (list), error (str|None).
    """
    for _ in range(timeout):
        time.sleep(1)
        try:
            history = _get(f"/history/{prompt_id}")
        except urllib.error.URLError:
            continue
        if prompt_id in history:
            entry = history[prompt_id]
            status = entry.get("status", {})

            if status.get("status_str") == "error":
                msgs = status.get("messages", [])
                for m in msgs:
                    if isinstance(m, list) and len(m) >= 2:
                        detail = m[1] if isinstance(m[1], dict) else {}
                        if "exception_message" in detail:
                            return {"status": "error", "outputs": [], "error": detail["exception_message"]}
                return {"status": "error", "outputs": [], "error": "Job failed — check ComfyUI logs."}

            files = _collect_output_files(entry)
            if files:
                return {"status": "success", "outputs": files, "error": None}
            # Job exists but no outputs yet — keep polling (still rendering)
            continue

    return {"status": "timeout", "outputs": [], "error": f"Timed out after {timeout}s."}


def _submit(workflow: dict) -> tuple[str | None, str | None]:
    """Submit a workflow. Returns (prompt_id, error_message)."""
    # Strip _meta before submission (ComfyUI doesn't understand it)
    clean = {k: v for k, v in workflow.items() if k != "_meta"}
    try:
        resp = _post("/prompt", {"prompt": clean, "client_id": str(uuid.uuid4())})
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace") if hasattr(e, "read") else str(e)
        return None, f"ComfyUI rejected the workflow (HTTP {e.code}): {body[:500]}"
    except urllib.error.URLError as e:
        return None, f"Cannot reach ComfyUI at {COMFYUI_URL}. Is it running? Detail: {e.reason}"

    pid = resp.get("prompt_id")
    if not pid:
        return None, f"ComfyUI returned no prompt_id. Response: {json.dumps(resp)[:300]}"
    return pid, None


def _sdxl_workflow(
    positive: str, negative: str, model: str,
    width: int, height: int, steps: int, cfg: float, seed: int,
) -> dict:
    """Build a minimal SDXL API-format workflow dictionary."""
    return {
        "4": {
            "class_type": "CheckpointLoaderSimple",
            "inputs": {"ckpt_name": model},
        },
        "5": {
            "class_type": "EmptyLatentImage",
            "inputs": {"width": width, "height": height, "batch_size": 1},
        },
        "6": {
            "class_type": "CLIPTextEncode",
            "inputs": {"text": positive, "clip": ["4", 1]},
        },
        "7": {
            "class_type": "CLIPTextEncode",
            "inputs": {"text": negative, "clip": ["4", 1]},
        },
        "8": {
            "class_type": "KSampler",
            "inputs": {
                "seed": seed,
                "steps": steps,
                "cfg": cfg,
                "sampler_name": "dpmpp_2m",
                "scheduler": "karras",
                "denoise": 1.0,
                "model": ["4", 0],
                "positive": ["6", 0],
                "negative": ["7", 0],
                "latent_image": ["5", 0],
            },
        },
        "9": {
            "class_type": "VAEDecode",
            "inputs": {"samples": ["8", 0], "vae": ["4", 2]},
        },
        "10": {
            "class_type": "SaveImage",
            "inputs": {"filename_prefix": "mcp", "images": ["9", 0]},
        },
    }


def _load_template(name: str) -> tuple[dict | None, str | None]:
    """Load a workflow template by name. Returns (workflow_dict, error)."""
    fname = name if name.endswith(".json") else f"{name}.json"
    path = WORKFLOW_DIR / fname
    if not path.exists():
        available = [f.name for f in sorted(WORKFLOW_DIR.glob("*.json"))] if WORKFLOW_DIR.exists() else []
        return None, f"'{fname}' not found. Available: {available}"
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except json.JSONDecodeError as e:
        return None, f"Template '{fname}' has invalid JSON: {e}"


# ── MCP Tools ──────────────────────────────────────────────────────────────────

# ---------- Generation tools ----------

@mcp.tool()
def generate_image(
    prompt: str,
    model: str = "sd_xl_base_1.0.safetensors",
    negative_prompt: str = (
        "worst quality, low quality, blurry, watermark, text, signature, "
        "extra limbs, malformed hands, duplicate"
    ),
    width: int = 1024,
    height: int = 1024,
    steps: int = 30,
    cfg: float = 7.0,
    seed: int = -1,
    timeout_seconds: int = 180,
) -> str:
    """
    Generate an image using the local ComfyUI instance with an SDXL-compatible
    checkpoint model. Constructs the workflow, submits it, waits for completion,
    and returns the output image URL(s).

    Use list_models("checkpoints") first if you are unsure which model to specify.

    Args:
        prompt: Positive generation prompt describing the desired image.
        model: Checkpoint filename from ComfyUI's models/checkpoints directory.
        negative_prompt: Elements to exclude from the image.
        width: Image width in pixels (use multiples of 64; SDXL native = 1024).
        height: Image height in pixels.
        steps: Number of denoising steps (20-40 is a good range for SDXL).
        cfg: Classifier-free guidance scale (6-8 for SDXL; 1-3.5 for Flux).
        seed: Random seed (-1 for a random seed each run).
        timeout_seconds: Maximum time to wait for the job to complete.
    """
    if seed == -1:
        seed = random.randint(0, 2**31 - 1)

    workflow = _sdxl_workflow(
        positive=prompt, negative=negative_prompt, model=model,
        width=width, height=height, steps=steps, cfg=cfg, seed=seed,
    )

    pid, err = _submit(workflow)
    if err:
        return f"ERROR: {err}"

    result = _poll_history(pid, timeout_seconds)

    if result["status"] == "error":
        return f"ERROR: {result['error']}"
    if result["status"] == "timeout":
        return f"ERROR: {result['error']} prompt_id: {pid}"

    urls = [f["url"] for f in result["outputs"]]
    return f"Generated {len(urls)} image(s) — seed: {seed}\n" + "\n".join(urls)


@mcp.tool()
def run_workflow(
    template: str,
    params: str = "{}",
    timeout_seconds: int = 600,
) -> str:
    """
    Load a workflow template, fill PARAM_* placeholders, submit to ComfyUI,
    wait for completion, and return the output file URLs.

    This is the primary tool for running any workflow end-to-end. Use
    inspect_workflow() first to see what PARAM_* values a template expects.

    For file inputs (images, audio), upload them first with upload_file() and
    use the returned registered filename as the PARAM value.

    Args:
        template: Template filename (e.g. "sdxl-basic-t2i" or "ltx23-img-audio-to-video").
        params: JSON string mapping PARAM names to values, e.g.
                '{"PARAM_POSITIVE_PROMPT": "a cat in space", "PARAM_SEED": 42}'.
                Omitted PARAMs keep their placeholder strings (will likely error).
        timeout_seconds: Maximum wait time (default 600s = 10 min; use more for video).
    """
    wf, err = _load_template(template)
    if err:
        return f"ERROR: {err}"

    try:
        param_dict = json.loads(params)
    except json.JSONDecodeError as e:
        return f"ERROR: Invalid params JSON — {e}"

    # Handle random seed convention
    for k, v in param_dict.items():
        spec = wf.get("_meta", {}).get("params", {}).get(k, {})
        if spec.get("type") == "int" and v == -1 and "seed" in k.lower():
            param_dict[k] = random.randint(0, 2**53)

    wf = _fill_params(wf, param_dict)

    pid, err = _submit(wf)
    if err:
        return f"ERROR: {err}"

    result = _poll_history(pid, timeout_seconds)

    if result["status"] == "error":
        return f"ERROR: Job failed — {result['error']}\nprompt_id: {pid}"
    if result["status"] == "timeout":
        return (
            f"Job still running after {timeout_seconds}s. "
            f"Use get_history('{pid}') to check later.\nprompt_id: {pid}"
        )

    lines = [f"Completed — prompt_id: {pid}", f"Outputs ({len(result['outputs'])}):", ""]
    for f in result["outputs"]:
        lines.append(f"  [{f['type']}] {f['filename']}  →  {f['url']}")
    return "\n".join(lines)


# ---------- Low-level submission tools ----------

@mcp.tool()
def submit_workflow(workflow_json: str) -> str:
    """
    Submit a raw ComfyUI API-format workflow JSON string for execution.
    Returns the prompt_id. Use get_history(prompt_id) to retrieve output URLs.

    Use this when you have a complete API-format workflow to send as-is —
    for example, a workflow loaded with load_workflow_template() and then
    modified programmatically.

    Args:
        workflow_json: A ComfyUI API-format workflow as a JSON string.
    """
    try:
        workflow = json.loads(workflow_json)
    except json.JSONDecodeError as e:
        return f"ERROR: Invalid JSON — {e}"

    pid, err = _submit(workflow)
    if err:
        return f"ERROR: {err}"
    return f"Submitted. prompt_id: {pid}"


@mcp.tool()
def get_history(prompt_id: str) -> str:
    """
    Retrieve output URLs for a completed ComfyUI job.
    Returns output URLs and types if the job is done, or a status message.

    Args:
        prompt_id: The prompt_id returned by submit_workflow() or run_workflow().
    """
    try:
        history = _get(f"/history/{prompt_id}")
    except urllib.error.URLError as e:
        return f"ERROR: Cannot reach ComfyUI. Detail: {e.reason}"

    if prompt_id not in history:
        return f"Pending: job {prompt_id} is not yet in history (still queued or running)."

    entry = history[prompt_id]
    status = entry.get("status", {})
    if status.get("status_str") == "error":
        return f"Job {prompt_id} FAILED. Check ComfyUI logs for details."

    files = _collect_output_files(entry)
    if not files:
        return f"Job {prompt_id} complete, but no outputs found in response."

    lines = [f"Job {prompt_id} — {len(files)} output(s):"]
    for f in files:
        lines.append(f"  [{f['type']}] {f['filename']}  →  {f['url']}")
    return "\n".join(lines)


# ---------- Queue / status ----------

@mcp.tool()
def get_queue() -> str:
    """
    Check how many jobs are currently running and pending in the ComfyUI queue.
    Useful before submitting to understand current GPU load.
    """
    try:
        q = _get("/queue")
    except urllib.error.URLError as e:
        return f"ERROR: Cannot reach ComfyUI at {COMFYUI_URL}. Detail: {e.reason}"

    running = len(q.get("queue_running", []))
    pending = len(q.get("queue_pending", []))
    return f"Queue: {running} running, {pending} pending."


# ---------- File upload ----------

@mcp.tool()
def upload_file(filepath: str) -> str:
    """
    Upload a local image or audio file to ComfyUI's input directory so it can
    be referenced by name in workflow nodes (LoadImage, LoadAudio, etc.).

    Returns the registered filename to use in PARAM_IMAGE / PARAM_AUDIO values
    or directly in workflow JSON.

    Args:
        filepath: Absolute path to the file on your local filesystem.
    """
    p = Path(filepath)
    if not p.exists():
        return f"ERROR: File not found: {filepath}"

    try:
        result = _upload_multipart(str(p))
    except urllib.error.URLError as e:
        return f"ERROR: Cannot reach ComfyUI at {COMFYUI_URL}. Detail: {e.reason}"

    name = result.get("name", p.name)
    subfolder = result.get("subfolder", "")
    return (
        f"Uploaded '{p.name}' → registered as '{name}'"
        + (f" (subfolder: {subfolder})" if subfolder else "")
    )


# ---------- Model discovery ----------

@mcp.tool()
def list_models(model_type: str = "checkpoints") -> str:
    """
    List installed model files in ComfyUI by type.

    Use without arguments to see all available model categories.
    Use with a type to see installed files for that category.

    The return value lists exact filenames to use in workflow JSON or tool params.

    Args:
        model_type: The model category to list. Common values:
            checkpoints, loras, vae, text_encoders, diffusion_models,
            upscale_models, controlnet, clip_vision, embeddings, LLM.
            Pass "all" to list every category and its file count.
    """
    try:
        categories = _get("/api/models")
    except urllib.error.URLError as e:
        return f"ERROR: Cannot reach ComfyUI at {COMFYUI_URL}. Detail: {e.reason}"

    if not isinstance(categories, list):
        return f"ERROR: Unexpected response from /api/models: {str(categories)[:200]}"

    # Show all categories with file counts
    if model_type == "all":
        lines = [f"Model categories ({len(categories)}):"]
        for cat in sorted(categories):
            try:
                files = _get(f"/api/models/{cat}")
                count = len(files) if isinstance(files, list) else "?"
            except Exception:
                count = "?"
            lines.append(f"  {cat}: {count} file(s)")
        return "\n".join(lines)

    # List files for a specific category
    if model_type not in categories:
        # Fuzzy match: try case-insensitive, partial match
        matches = [c for c in categories if model_type.lower() in c.lower()]
        if len(matches) == 1:
            model_type = matches[0]
        elif matches:
            return f"Ambiguous type '{model_type}'. Did you mean one of: {matches}?"
        else:
            return (
                f"Unknown model type '{model_type}'.\n"
                f"Available: {', '.join(sorted(categories))}"
            )

    try:
        files = _get(f"/api/models/{model_type}")
    except urllib.error.URLError as e:
        return f"ERROR: Cannot reach ComfyUI. Detail: {e.reason}"

    if not isinstance(files, list) or not files:
        return f"No files found for '{model_type}'."

    return f"Installed {model_type} ({len(files)}):\n" + "\n".join(f"  {m}" for m in sorted(files))


# ---------- Node introspection ----------

@mcp.tool()
def get_node_info(node_type: str) -> str:
    """
    Query what inputs a specific ComfyUI node type accepts.
    Returns all required and optional inputs with their types, default values,
    and COMBO options (for dropdown selections like model names).

    Useful for understanding what a workflow node needs, or for debugging
    validation errors.

    Args:
        node_type: The exact class_type name (e.g. "KSampler", "CheckpointLoaderSimple",
                   "LoadImage", "LTXAVTextEncoderLoader"). Case-sensitive.
    """
    try:
        info = _get(f"/object_info/{node_type}")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return f"ERROR: Node type '{node_type}' not found. Check spelling (case-sensitive)."
        return f"ERROR: HTTP {e.code} querying node info."
    except urllib.error.URLError as e:
        return f"ERROR: Cannot reach ComfyUI. Detail: {e.reason}"

    if not info or node_type not in info:
        return f"ERROR: Node type '{node_type}' not found. Check spelling (case-sensitive)."

    node_data = info[node_type]
    lines = [f"Node: {node_type}"]

    desc = node_data.get("description", "")
    if desc:
        lines.append(f"Description: {desc}")

    cat = node_data.get("category", "")
    if cat:
        lines.append(f"Category: {cat}")

    outputs = node_data.get("output", [])
    output_names = node_data.get("output_name", [])
    if outputs:
        out_parts = []
        for i, otype in enumerate(outputs):
            oname = output_names[i] if i < len(output_names) else f"output_{i}"
            out_parts.append(f"  [{i}] {oname}: {otype}")
        lines.append("Outputs:")
        lines.extend(out_parts)

    for section in ("required", "optional"):
        inputs = node_data.get("input", {}).get(section, {})
        if not inputs:
            continue
        lines.append(f"\n{section.title()} Inputs:")
        for ikey, ispec in inputs.items():
            if isinstance(ispec, list) and len(ispec) >= 1:
                itype = ispec[0]
                extra = ispec[1] if len(ispec) > 1 else {}
                if isinstance(itype, list):
                    # COMBO — list of allowed values
                    preview = itype[:10]
                    suffix = f" ... (+{len(itype) - 10} more)" if len(itype) > 10 else ""
                    lines.append(f"  {ikey}: COMBO {preview}{suffix}")
                elif isinstance(extra, dict):
                    parts = [f"{ikey}: {itype}"]
                    if "default" in extra:
                        parts.append(f"default={extra['default']}")
                    if "min" in extra:
                        parts.append(f"min={extra['min']}")
                    if "max" in extra:
                        parts.append(f"max={extra['max']}")
                    lines.append(f"  {' | '.join(parts)}")
                else:
                    lines.append(f"  {ikey}: {itype}")
            else:
                lines.append(f"  {ikey}: {ispec}")

    return "\n".join(lines)


# ---------- Workflow introspection ----------

@mcp.tool()
def inspect_workflow(template: str) -> str:
    """
    Show what a workflow template needs: its PARAM_* placeholders, their types,
    descriptions, and the current default values in the template.

    Use this BEFORE run_workflow() to understand what values to supply.
    For file-type params, upload the file first with upload_file().

    Args:
        template: Template filename (e.g. "sdxl-basic-t2i" or "ltx23-img-audio-to-video").
    """
    wf, err = _load_template(template)
    if err:
        return f"ERROR: {err}"

    meta = wf.get("_meta", {})
    name = meta.get("name", template)
    desc = meta.get("description", "")
    param_specs = meta.get("params", {})

    lines = [f"Template: {name}"]
    if desc:
        lines.append(f"Description: {desc}")
    lines.append("")

    if not param_specs:
        # No _meta.params — scan for PARAM_ strings
        found = {}
        for nid, node in wf.items():
            if nid == "_meta":
                continue
            for k, v in node.get("inputs", {}).items():
                if isinstance(v, str) and v.startswith("PARAM_"):
                    found[v] = f"node {nid}, key '{k}'"
        if found:
            lines.append("Parameters (auto-detected, no _meta.params):")
            for pname, loc in sorted(found.items()):
                lines.append(f"  {pname}  →  {loc}")
        else:
            lines.append("No PARAM_* placeholders found in this template.")
        return "\n".join(lines)

    lines.append(f"Parameters ({len(param_specs)}):")
    lines.append("")
    for pname, spec in param_specs.items():
        node_id = spec.get("node", "?")
        key = spec.get("key", "?")
        ptype = spec.get("type", "string")
        pdesc = spec.get("description", "")

        # Get current value from the workflow
        current = "?"
        if node_id in wf and "inputs" in wf[node_id]:
            current = wf[node_id]["inputs"].get(key, "?")

        lines.append(f"  {pname}")
        lines.append(f"    Type: {ptype}")
        lines.append(f"    Node: {node_id} → {key}")
        if pdesc:
            lines.append(f"    Desc: {pdesc}")
        lines.append(f"    Default: {current}")
        lines.append("")

    # Count total nodes (excluding _meta)
    node_count = sum(1 for k in wf if k != "_meta")
    lines.append(f"Total nodes: {node_count}")

    return "\n".join(lines)


# ---------- Template listing / loading ----------

@mcp.tool()
def list_workflow_templates() -> str:
    """
    List pre-built ComfyUI API-format workflow templates in the companion
    repository (comfyui/workflows/*.json).

    Each template has PARAM_* placeholders for user-configurable values.
    Use inspect_workflow() to see what a template needs, then run_workflow()
    to execute it.
    """
    if not WORKFLOW_DIR.exists():
        return f"Workflows directory not found at: {WORKFLOW_DIR}"

    files = sorted(WORKFLOW_DIR.glob("*.json"))
    if not files:
        return "No templates found. Add API-format JSON files to comfyui/workflows/."

    lines = ["Workflow templates:", ""]
    for f in files:
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            meta = data.get("_meta", {})
            name = meta.get("name", f.stem)
            desc = meta.get("description", "")
            param_count = len(meta.get("params", {}))
            lines.append(f"  {f.name}")
            lines.append(f"    Name: {name}")
            if desc:
                lines.append(f"    Desc: {desc[:120]}{'...' if len(desc) > 120 else ''}")
            lines.append(f"    Params: {param_count}")
            lines.append("")
        except (json.JSONDecodeError, OSError):
            lines.append(f"  {f.name}  (cannot parse)")
            lines.append("")

    return "\n".join(lines)


@mcp.tool()
def load_workflow_template(name: str) -> str:
    """
    Load a workflow JSON template from comfyui/workflows/ by filename.
    Returns the raw API-format JSON for inspection, manual editing, or
    direct submission via submit_workflow().

    For the easier path, use inspect_workflow() + run_workflow() instead.

    Args:
        name: Template filename (e.g. "sdxl-basic-t2i" or "sdxl-basic-t2i.json").
    """
    wf, err = _load_template(name)
    if err:
        return f"ERROR: {err}"
    return json.dumps(wf, indent=2)


# ---------- Graph-to-API conversion ----------

# Cache for /object_info widget-name lookups (class_type → ordered widget names)
_object_info_cache: dict[str, list[str] | None] = {}

# Frontend-only widgets that should not appear in API-format output
_FRONTEND_ONLY_WIDGETS = frozenset({"control_after_generate", "audioUI"})

# Node types to skip during graph conversion (UI annotations, previews)
_GRAPH_SKIP_TYPES = frozenset({
    "MarkdownNote", "Note", "PreviewAny", "PreviewImage",
    "PreviewAudio", "RecordAudio",
})


def _get_widget_names(class_type: str) -> list[str] | None:
    """Get ordered widget input names for a node type from /object_info.

    Widget inputs are those with scalar types (INT, FLOAT, STRING, BOOLEAN)
    or COMBO (list of options).  Connection-only types (MODEL, CLIP, etc.)
    are excluded.

    Returns ordered list matching widgets_values positions, or None on failure.
    """
    if class_type in _object_info_cache:
        return _object_info_cache[class_type]
    try:
        info = _get(f"/object_info/{class_type}")
        node_info = info.get(class_type, {})
        names: list[str] = []
        for section in ("required", "optional"):
            section_inputs = node_info.get("input", {}).get(section, {})
            if not isinstance(section_inputs, dict):
                continue
            for key, spec in section_inputs.items():
                if not isinstance(spec, list) or len(spec) < 1:
                    continue
                type_info = spec[0]
                if isinstance(type_info, list):          # COMBO
                    names.append(key)
                elif isinstance(type_info, str) and type_info.upper() in (
                    "INT", "FLOAT", "STRING", "BOOLEAN",
                ):
                    names.append(key)
        _object_info_cache[class_type] = names
        return names
    except Exception:
        _object_info_cache[class_type] = None
        return None


def _graph_to_api(graph_data: dict) -> tuple[dict, str | None]:
    """Convert a ComfyUI graph-format (UI save) to API-format.

    Handles:
      - Standard nodes → flat API entries
      - Subgraph (component) nodes → expanded into inner nodes
      - Reroute nodes → eliminated, connections traced through
      - Widget values → mapped via /object_info for correct positional alignment

    Returns (api_dict, error_message).  api_dict is empty on error.
    """

    # ── Parse helper ──
    def _pl(ld):
        """Extract (link_id, origin_id, origin_slot, target_id, target_slot)."""
        if isinstance(ld, dict):
            return (ld["id"], ld["origin_id"], ld["origin_slot"],
                    ld["target_id"], ld["target_slot"])
        return tuple(ld[:5])

    # ── Phase 1: Parse outer graph structure ──
    outer_nodes = graph_data.get("nodes", [])

    outer_links: dict[int, tuple[int, int]] = {}
    for ld in graph_data.get("links", []):
        lid, oid, osl, _tid, _tsl = _pl(ld)
        outer_links[lid] = (oid, osl)

    sg_defs = {sg["id"]: sg for sg in
               graph_data.get("definitions", {}).get("subgraphs", [])}

    # ── Phase 2: Analyze subgraph instances ──
    # (sg_node_id, output_slot) → (inner_node_id, inner_output_slot)
    sg_output_map: dict[tuple[int, int], tuple[int, int]] = {}
    # sg_node_id → {input_slot: (outer_origin_id, outer_origin_slot)}
    sg_input_map: dict[int, dict[int, tuple[int, int]]] = {}
    # sg_node_id → {link_id: (origin_id, origin_slot)}
    sg_ilinks: dict[int, dict[int, tuple[int, int]]] = {}

    for node in outer_nodes:
        nt = node.get("type", "")
        nid = node["id"]
        if nt not in sg_defs:
            continue
        sg = sg_defs[nt]

        # Parse inner links
        ilinks: dict[int, tuple[int, int]] = {}
        for ld in sg.get("links", []):
            lid, oid, osl, _tid, _tsl = _pl(ld)
            ilinks[lid] = (oid, osl)
        sg_ilinks[nid] = ilinks

        # Output mapping: which inner node feeds each subgraph output?
        for i, sg_out in enumerate(sg.get("outputs", [])):
            for lid in sg_out.get("linkIds", []):
                if lid in ilinks:
                    sg_output_map[(nid, i)] = ilinks[lid]

        # Input mapping: outer link → subgraph input slot
        in_map: dict[int, tuple[int, int]] = {}
        outer_inputs = node.get("inputs", [])
        for i, _sg_in in enumerate(sg.get("inputs", [])):
            if i < len(outer_inputs):
                ol_id = outer_inputs[i].get("link")
                if ol_id is not None and ol_id in outer_links:
                    in_map[i] = outer_links[ol_id]
        sg_input_map[nid] = in_map

    # ── Phase 3: Build Reroute pass-through map ──
    reroute_src: dict[int, tuple[int, int]] = {}

    for node in outer_nodes:
        if node.get("type") == "Reroute":
            il = (node.get("inputs") or [{}])[0].get("link")
            if il is not None and il in outer_links:
                reroute_src[node["id"]] = outer_links[il]

    for sg_nid, ilinks in sg_ilinks.items():
        sg_type = next((n["type"] for n in outer_nodes if n["id"] == sg_nid), "")
        sg = sg_defs.get(sg_type, {})
        for inode in sg.get("nodes", []):
            if inode.get("type") == "Reroute" and inode.get("id", 0) > 0:
                il = (inode.get("inputs") or [{}])[0].get("link")
                if il is not None and il in ilinks:
                    reroute_src[inode["id"]] = ilinks[il]

    def _resolve(nid: int, slot: int) -> tuple[int, int]:
        """Trace through subgraph outputs and reroutes to the real source."""
        seen: set[tuple[int, int]] = set()
        while (nid, slot) not in seen:
            seen.add((nid, slot))
            if (nid, slot) in sg_output_map:
                nid, slot = sg_output_map[(nid, slot)]
            elif nid in reroute_src:
                nid, slot = reroute_src[nid]
            else:
                break
        return (nid, slot)

    # ── Phase 4: Convert each node to API format ──
    api: dict[str, dict] = {}

    def _convert(node: dict, link_tbl: dict, sg_nid: int | None = None):
        nid = node.get("id", 0)
        ct = node.get("type", "")
        if (nid <= 0 or ct in _GRAPH_SKIP_TYPES or ct == "Reroute"
                or ct in sg_defs or node.get("mode") == 4):
            return

        node_inputs = node.get("inputs", [])
        wv = node.get("widgets_values") or []

        # Map widgets_values → {name: value}
        # The graph's inputs array lists visible widget inputs; widgets_values
        # also contains hidden frontend-only values (e.g. control_after_generate
        # which follows seed/noise_seed/PrimitiveInt widgets).  We align by
        # detecting surplus entries: when widgets_values has more entries than
        # visible widgets, skip known control strings.
        _CONTROL = frozenset({
            "randomize", "fixed", "increment", "decrement",
            "increment and wrap", "decrement and wrap",
        })
        visible_widgets = [inp for inp in node_inputs if "widget" in inp]
        wv_dict: dict[str, object] = {}
        wi_idx = 0   # visible widget index
        wv_idx = 0   # widgets_values index
        surplus = len(wv) - len(visible_widgets)
        while wi_idx < len(visible_widgets) and wv_idx < len(wv):
            wn = visible_widgets[wi_idx]["widget"].get(
                "name", visible_widgets[wi_idx].get("name", ""))
            wv_dict[wn] = wv[wv_idx]
            wv_idx += 1
            wi_idx += 1
            # After assignment, check for hidden control_after_generate
            if surplus > 0 and wv_idx < len(wv):
                nv = wv[wv_idx]
                if isinstance(nv, str) and nv in _CONTROL:
                    wv_idx += 1
                    surplus -= 1

        # Build API inputs dict
        api_inputs: dict[str, object] = {}

        for inp in node_inputs:
            iname = inp.get("name", "")
            ilink = inp.get("link")
            has_w = "widget" in inp

            if ilink is not None:
                ol = link_tbl.get(ilink)
                if not ol:
                    continue
                orig_id, orig_sl = ol

                if orig_id == -10 and sg_nid is not None:
                    # From subgraph virtual input — check if outer provides it
                    sources = sg_input_map.get(sg_nid, {})
                    if orig_sl in sources:
                        rid, rsl = _resolve(*sources[orig_sl])
                        api_inputs[iname] = [str(rid), rsl]
                    else:
                        # Not externally linked — fall back to widget value
                        wn = inp.get("widget", {}).get("name", iname)
                        val = wv_dict.get(wn, wv_dict.get(iname))
                        if val is not None:
                            api_inputs[wn] = val
                else:
                    rid, rsl = _resolve(orig_id, orig_sl)
                    api_inputs[iname] = [str(rid), rsl]

            elif has_w:
                wn = inp.get("widget", {}).get("name", iname)
                val = wv_dict.get(wn, wv_dict.get(iname))
                if val is not None:
                    api_inputs[wn] = val

        # Strip frontend-only widgets
        for fw in _FRONTEND_ONLY_WIDGETS:
            api_inputs.pop(fw, None)
        for inp in node_inputs:
            if inp.get("type") in ("IMAGEUPLOAD", "AUDIOUPLOAD", "AUDIO_RECORD"):
                api_inputs.pop(inp.get("name", ""), None)

        api[str(nid)] = {
            "class_type": ct,
            "inputs": api_inputs,
            "_meta": {"title": node.get("title", ct)},
        }

    # Convert outer nodes (non-subgraph)
    for node in outer_nodes:
        _convert(node, outer_links)

    # Expand and convert subgraph inner nodes
    for node in outer_nodes:
        nt = node.get("type", "")
        if nt not in sg_defs:
            continue
        ilinks = sg_ilinks.get(node["id"], {})
        for inode in sg_defs[nt].get("nodes", []):
            _convert(inode, ilinks, sg_nid=node["id"])

    # Final pass: resolve any remaining references to subgraph/reroute nodes
    for nd in api.values():
        for key, val in nd.get("inputs", {}).items():
            if isinstance(val, list) and len(val) == 2:
                try:
                    ref_id = int(val[0])
                    rid, rsl = _resolve(ref_id, val[1])
                    if rid != ref_id or rsl != val[1]:
                        nd["inputs"][key] = [str(rid), rsl]
                except (ValueError, TypeError):
                    pass

    # ── Remap inner-node IDs to compound "outer:inner" format ──
    # Matches ComfyUI's own export format and prevents ID collisions.
    inner_ids: set[int] = set()
    sg_owner: dict[int, int] = {}          # inner_nid → parent subgraph nid
    for node in outer_nodes:
        nt = node.get("type", "")
        if nt not in sg_defs:
            continue
        for inode in sg_defs[nt].get("nodes", []):
            iid = inode.get("id", 0)
            if iid > 0:
                inner_ids.add(iid)
                sg_owner[iid] = node["id"]

    remap: dict[str, str] = {}
    for iid in inner_ids:
        old = str(iid)
        if old in api:
            remap[old] = f"{sg_owner[iid]}:{iid}"

    if remap:
        new_api: dict[str, dict] = {}
        for k, v in api.items():
            nk = remap.get(k, k)
            for iname, ival in v.get("inputs", {}).items():
                if isinstance(ival, list) and len(ival) == 2:
                    ref = str(ival[0])
                    if ref in remap:
                        v["inputs"][iname] = [remap[ref], ival[1]]
            new_api[nk] = v
        api = new_api

    if not api:
        return {}, "Conversion produced no nodes — workflow may be empty."
    return api, None


# ---------- Workflow import ----------

# Node types whose primary string input is user content (prompts, filenames)
_PARAMETERIZABLE_NODE_TYPES = {
    # Loaders: auto-detect model/file inputs
    "LoadImage": [("image", "file", "Input image filename")],
    "LoadAudio": [("audio", "file", "Input audio filename")],
    "CheckpointLoaderSimple": [("ckpt_name", "combo", "Checkpoint model")],
    "LoraLoader": [("lora_name", "combo", "LoRA adapter")],
    "LoraLoaderModelOnly": [("lora_name", "combo", "LoRA adapter")],
    # Seeds
    "RandomNoise": [("noise_seed", "int", "Random seed")],
    "KSampler": [("seed", "int", "Random seed")],
}

# Node _meta.title keywords that indicate user-configurable primitive values
_TITLE_PARAM_HINTS = {
    "prompt": ("string", "Text prompt"),
    "width": ("int", "Image/video width in pixels"),
    "height": ("int", "Image/video height in pixels"),
    "duration": ("float", "Duration in seconds"),
    "frame rate": ("int", "Frames per second"),
    "fps": ("int", "Frames per second"),
    "seed": ("int", "Random seed"),
    "steps": ("int", "Sampling steps"),
    "cfg": ("float", "CFG guidance scale"),
}


def _auto_parameterize(workflow: dict, name: str) -> dict:
    """Analyze a raw API-format workflow and add _meta.params for user-configurable values.

    Heuristic detection:
    1. Known node types (loaders, samplers) → parameterize their key inputs
    2. Primitive nodes (PrimitiveInt, PrimitiveFloat, PrimitiveStringMultiline) with
       descriptive _meta.title → parameterize their value
    3. CLIPTextEncode with inline text (not from another node) → parameterize prompt
    """
    params = {}
    counters: dict[str, int] = {}  # for deduplication

    def make_param_name(base: str) -> str:
        """Generate unique PARAM_* name."""
        key = base.upper()
        if key not in counters:
            counters[key] = 0
            return f"PARAM_{key}"
        counters[key] += 1
        return f"PARAM_{key}_{counters[key]}"

    for node_id, node in workflow.items():
        if node_id == "_meta":
            continue
        if not isinstance(node, dict):
            continue

        class_type = node.get("class_type", "")
        inputs = node.get("inputs", {})
        title = node.get("_meta", {}).get("title", "").lower()

        # 1. Known node types
        if class_type in _PARAMETERIZABLE_NODE_TYPES:
            for input_key, ptype, desc in _PARAMETERIZABLE_NODE_TYPES[class_type]:
                if input_key in inputs:
                    val = inputs[input_key]
                    # Skip if it's a link to another node
                    if isinstance(val, list):
                        continue
                    base = input_key.upper()
                    pname = make_param_name(base)
                    params[pname] = {
                        "node": node_id, "key": input_key,
                        "type": ptype, "description": desc,
                    }

        # 2. Primitive nodes with descriptive titles
        elif class_type.startswith("Primitive"):
            for hint_key, (hint_type, hint_desc) in _TITLE_PARAM_HINTS.items():
                if hint_key in title:
                    # Find the value key (usually "value")
                    for input_key, val in inputs.items():
                        if input_key == "value" and not isinstance(val, list):
                            pname = make_param_name(hint_key.upper().replace(" ", "_"))
                            params[pname] = {
                                "node": node_id, "key": input_key,
                                "type": hint_type, "description": hint_desc,
                            }
                    break

        # 3. CLIPTextEncode with inline text
        elif class_type == "CLIPTextEncode":
            text_val = inputs.get("text")
            if isinstance(text_val, str):
                # Check title and content to distinguish positive/negative
                neg_title_words = ("negative", "neg ", "exclude", "avoid")
                neg_content_words = ("worst quality", "low quality", "ugly", "blurry",
                                     "watermark", "deformed", "bad anatomy", "childish")
                is_negative = (
                    any(w in title for w in neg_title_words)
                    or sum(1 for w in neg_content_words if w in text_val.lower()) >= 2
                )
                if is_negative:
                    pname = make_param_name("NEGATIVE_PROMPT")
                    desc = "Negative prompt — elements to exclude"
                else:
                    pname = make_param_name("POSITIVE_PROMPT")
                    desc = "Positive text prompt"
                params[pname] = {
                    "node": node_id, "key": "text",
                    "type": "string", "description": desc,
                }

    # Build _meta block
    meta = {
        "name": name,
        "description": f"Auto-imported workflow with {len(params)} configurable parameters.",
        "params": params,
    }

    # Merge: put _meta at root level, preserve existing per-node _meta
    workflow["_meta"] = meta
    return workflow


@mcp.tool()
def import_workflow(
    filepath: str,
    template_name: str = "",
) -> str:
    """
    Import a ComfyUI workflow and register it as a reusable MCP template
    with auto-detected PARAM_* placeholders.

    Accepts BOTH workflow formats:
      - API format: from ComfyUI "Export (API Format)" menu option
      - Graph format: from ComfyUI "Save" or the saved-workflows directory
        (graph-format files are automatically converted to API format)

    File resolution for bare filenames (no path separators):
      1. exports/ drop folder
      2. ComfyUI saved-workflows directory (C:\\ComfyUI\\user\\default\\workflows\\)
      3. Current directory

    After import, use inspect_workflow() to review and run_workflow() to execute.

    Args:
        filepath: Path to the workflow JSON file. Can be an absolute path,
                  or just a filename to search exports/ and ComfyUI saved dir.
        template_name: Name for the template (e.g. "wan21-t2v"). If omitted,
                       derived from the filename.
    """
    p = Path(filepath)

    # Resolution order for bare filenames
    if not p.is_absolute() and p.parent == Path("."):
        exports_candidate = EXPORTS_DIR / p.name
        saved_candidate = COMFYUI_SAVED_DIR / p.name
        if exports_candidate.exists():
            p = exports_candidate
        elif saved_candidate.exists():
            p = saved_candidate

    if not p.exists():
        return f"ERROR: File not found: {filepath}"
    if not p.suffix.lower() == ".json":
        return f"ERROR: Expected a .json file, got: {p.name}"

    try:
        workflow = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return f"ERROR: Invalid JSON in {p.name}: {e}"

    if not isinstance(workflow, dict):
        return f"ERROR: Expected a JSON object (dict), got {type(workflow).__name__}"

    # Detect format: graph (has "nodes" array) vs API (has numbered keys with class_type)
    is_graph = isinstance(workflow.get("nodes"), list)
    api_nodes = [k for k, v in workflow.items()
                 if isinstance(v, dict) and "class_type" in v]

    format_note = ""
    if is_graph:
        # Convert graph format → API format
        api_workflow, conv_err = _graph_to_api(workflow)
        if conv_err:
            return f"ERROR converting graph to API format: {conv_err}"
        workflow = api_workflow
        api_nodes = [k for k, v in workflow.items()
                     if isinstance(v, dict) and "class_type" in v]
        format_note = f" (converted from graph format)"
    elif not api_nodes:
        return (
            "ERROR: Not a recognized ComfyUI workflow format. "
            "Expected either graph format (nodes/links) or API format (class_type entries)."
        )

    # Determine template name
    name = template_name or p.stem
    fname = name if name.endswith(".json") else f"{name}.json"

    # Check if template already exists
    dest = WORKFLOW_DIR / fname
    if dest.exists():
        return (
            f"ERROR: Template '{fname}' already exists. "
            f"Choose a different template_name or remove the existing file."
        )

    # Auto-parameterize
    workflow = _auto_parameterize(workflow, name)
    params = workflow.get("_meta", {}).get("params", {})

    # Ensure workflows directory exists
    WORKFLOW_DIR.mkdir(parents=True, exist_ok=True)

    # Save
    dest.write_text(json.dumps(workflow, indent=2), encoding="utf-8")

    # Report
    lines = [
        f"Imported '{p.name}'{format_note} → saved as template '{fname}'",
        f"Nodes: {len(api_nodes)}",
        f"Auto-detected {len(params)} configurable parameter(s):",
        "",
    ]
    for pname, spec in params.items():
        node_id = spec["node"]
        key = spec["key"]
        current = workflow.get(node_id, {}).get("inputs", {}).get(key, "?")
        lines.append(f"  {pname}")
        lines.append(f"    Type: {spec['type']} | Node: {node_id} → {key}")
        lines.append(f"    Desc: {spec['description']}")
        lines.append(f"    Default: {str(current)[:80]}")
        lines.append("")

    lines.append("Next steps:")
    lines.append(f"  1. inspect_workflow('{name}')  — review parameters")
    lines.append(f"  2. run_workflow('{name}', '{{...}}')  — execute with custom values")
    lines.append("")
    lines.append("To add/modify parameters, edit the _meta.params block in:")
    lines.append(f"  {dest}")

    return "\n".join(lines)


@mcp.tool()
def list_saved_workflows() -> str:
    """
    List workflows saved in ComfyUI's local user data directory on disk.

    These are graph-format workflows saved from the ComfyUI UI (via Save or
    Ctrl+S).  They can be imported as MCP templates using import_workflow()
    which automatically converts graph format to API format.

    The directory searched is controlled by the COMFYUI_PATH environment
    variable (default: C:\\ComfyUI).
    """
    if not COMFYUI_SAVED_DIR.exists():
        return (
            f"ComfyUI saved-workflows directory not found:\n  {COMFYUI_SAVED_DIR}\n\n"
            f"If ComfyUI is installed elsewhere, set COMFYUI_PATH environment variable.\n"
            f"Current COMFYUI_PATH: {COMFYUI_PATH}"
        )

    files = sorted(COMFYUI_SAVED_DIR.glob("*.json"))
    if not files:
        return f"No saved workflows found in:\n  {COMFYUI_SAVED_DIR}"

    # Check which have already been imported as templates
    existing = {f.stem for f in WORKFLOW_DIR.glob("*.json")} if WORKFLOW_DIR.exists() else set()

    lines = [f"Saved workflows in ComfyUI ({len(files)}):", ""]

    for f in files:
        size_kb = f.stat().st_size / 1024
        status = "already imported" if f.stem in existing else "ready to import"
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            nodes = data.get("nodes", [])
            real_nodes = [n for n in nodes
                          if n.get("type", "") not in _GRAPH_SKIP_TYPES]
            sgs = data.get("definitions", {}).get("subgraphs", [])
            total_inner = sum(len(sg.get("nodes", [])) for sg in sgs)

            parts = [f"{len(real_nodes)} nodes"]
            if sgs:
                parts.append(f"{len(sgs)} subgraph(s) expanding to {total_inner} inner nodes")
            parts.append(f"{size_kb:.0f} KB")

            lines.append(f"  {f.name}  [{status}]")
            lines.append(f"    {', '.join(parts)}")

            sg_names = [sg.get("name", "") for sg in sgs if sg.get("name")]
            if sg_names:
                lines.append(f"    Pipeline: {', '.join(sg_names)}")
        except Exception:
            lines.append(f"  {f.name} ({size_kb:.0f} KB) — cannot parse")
        lines.append("")

    lines.append("To import a saved workflow, run:")
    lines.append("  import_workflow('<filename>')")
    lines.append(
        "The graph format is auto-converted to API format during import."
    )

    return "\n".join(lines)


@mcp.tool()
def scan_exports() -> str:
    """
    List API-format JSON files in the exports/ drop folder that haven't been
    imported as workflow templates yet.

    The exports/ folder is where users place raw ComfyUI "Export (API Format)"
    files.  This tool shows which ones are available and which have already
    been imported to the workflows/ directory.

    Returns a summary with filenames, sizes, and import status.
    """
    if not EXPORTS_DIR.exists():
        EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
        return (
            "The exports/ folder was just created. It's empty.\n\n"
            "To add workflows:\n"
            "  1. In ComfyUI, open a workflow\n"
            "  2. Click menu → 'Export (API Format)'\n"
            f"  3. Save to: {EXPORTS_DIR}\n"
        )

    json_files = sorted(EXPORTS_DIR.glob("*.json"))
    if not json_files:
        return (
            "No .json files found in exports/ folder.\n\n"
            f"Drop API-format exports into:\n  {EXPORTS_DIR}\n"
        )

    # Check which have been imported already
    existing_templates = {f.stem for f in WORKFLOW_DIR.glob("*.json")} if WORKFLOW_DIR.exists() else set()

    lines = [f"Found {len(json_files)} export(s) in: {EXPORTS_DIR}", ""]

    ready = []
    already = []
    invalid = []

    for f in json_files:
        if f.name == "README.md":
            continue
        size_kb = f.stat().st_size / 1024
        stem = f.stem

        # Quick-validate: is it API format?
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            api_nodes = [k for k, v in data.items() if isinstance(v, dict) and "class_type" in v]
            is_valid = len(api_nodes) > 0
            node_count = len(api_nodes)
        except Exception:
            is_valid = False
            node_count = 0

        if not is_valid:
            invalid.append(f"  ✗ {f.name} ({size_kb:.0f} KB) — not valid API format")
        elif stem in existing_templates:
            already.append(f"  ✓ {f.name} ({node_count} nodes, {size_kb:.0f} KB) — already imported")
        else:
            ready.append(f"  → {f.name} ({node_count} nodes, {size_kb:.0f} KB) — ready to import")

    if ready:
        lines.append("Ready to import:")
        lines.extend(ready)
        lines.append("")

    if already:
        lines.append("Already imported:")
        lines.extend(already)
        lines.append("")

    if invalid:
        lines.append("Invalid (not API format — use 'Export (API Format)' in ComfyUI):")
        lines.extend(invalid)
        lines.append("")

    if ready:
        lines.append("To import, run:")
        for r in ready:
            fname = r.split(" ")[2]  # extract filename
            tname = Path(fname).stem
            lines.append(f"  import_workflow('{fname}', '{tname}')")

    return "\n".join(lines)


# ── Entry point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    mcp.run()
