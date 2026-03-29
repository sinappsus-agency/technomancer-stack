"""Discover all saved workflows and built-in templates for ACE Step and LTX."""
import json, urllib.request, glob, os

COMFY = "http://127.0.0.1:8000"

# 1. List saved user workflows
print("=== SAVED WORKFLOWS ===")
resp = urllib.request.urlopen(f"{COMFY}/api/userdata?dir=workflows&recurse=true")
wfs = json.loads(resp.read())
for w in wfs:
    name = w if isinstance(w, str) else w.get("path", w.get("name", str(w)))
    if any(k in name.lower() for k in ["ace", "ltx", "audio", "video", "speech", "tts"]):
        print(f"  * {name}")
    else:
        print(f"    {name}")

# 2. List built-in templates mentioning ace/ltx/audio/video
print("\n=== BUILT-IN TEMPLATES (ace/ltx/audio/video) ===")
template_dirs = glob.glob(r"C:\ComfyUI\.venv\Lib\site-packages\comfyui_workflow_templates*\templates\*.json")
for t in template_dirs:
    base = os.path.basename(t)
    if any(k in base.lower() for k in ["ace", "ltx", "audio", "video", "speech", "tts"]):
        print(f"  {base}")

# 3. Check object_info for ACE/LTX node types
print("\n=== NODE TYPES (ace/ltx/speech/tts) ===")
resp2 = urllib.request.urlopen(f"{COMFY}/api/object_info")
nodes = json.loads(resp2.read())
for name in sorted(nodes.keys()):
    if any(k in name.lower() for k in ["ace", "ltx", "speech", "tts", "cosyvoice"]):
        print(f"  {name}")
