"""Download saved workflows - try URL-encoded paths and list first."""
import json, urllib.request, urllib.parse

COMFY = "http://127.0.0.1:8000"

# First list what's actually in the workflows dir
print("=== Listing workflows dir ===")
resp = urllib.request.urlopen(f"{COMFY}/api/userdata?dir=workflows&recurse=true")
items = json.loads(resp.read())
for item in items:
    print(f"  {item}")

# Try to download each workflow
print("\n=== Downloading workflows ===")
for item in items:
    name = item if isinstance(item, str) else item.get("path", str(item))
    encoded = urllib.parse.quote(name)
    url = f"{COMFY}/api/userdata/workflows/{encoded}"
    try:
        resp = urllib.request.urlopen(url)
        data = json.loads(resp.read())
        out = f"_wf_{name.replace('/', '_')}"
        with open(out, "w") as f:
            json.dump(data, f, indent=2)
        nodes = data.get("nodes", [])
        print(f"  OK: {name} -> {out} ({len(nodes)} nodes)")
    except Exception as e:
        print(f"  FAIL: {name} -> {e}")

# Also get built-in ia2v template
import glob
for t in glob.glob(r"C:\ComfyUI\.venv\Lib\site-packages\comfyui_workflow_templates*\templates\video_ltx2_3_ia2v.json"):
    with open(t) as f:
        d = json.load(f)
    with open("_wf_ltx_ia2v_builtin.json", "w") as f:
        json.dump(d, f, indent=2)
    print(f"\n  Built-in ia2v template saved ({len(d.get('nodes', []))} nodes)")
