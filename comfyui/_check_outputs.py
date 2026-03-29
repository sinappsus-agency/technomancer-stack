"""Inspect LTX video generation output to find the video."""
import json, urllib.request

COMFY = "http://127.0.0.1:8000"
prompt_id = "26c35a29-c9a6-41a3-96c7-16b27cba30e1"

resp = urllib.request.urlopen(f"{COMFY}/api/history/{prompt_id}")
history = json.loads(resp.read())
entry = history.get(prompt_id, {})

outputs = entry.get("outputs", {})
print(f"Output nodes: {len(outputs)}")
for nid, out in outputs.items():
    print(f"\n  Node {nid}: keys={list(out.keys())}")
    for k, v in out.items():
        if isinstance(v, list):
            for item in v[:3]:
                print(f"    {k}: {json.dumps(item)}")
        else:
            print(f"    {k}: {str(v)[:200]}")
