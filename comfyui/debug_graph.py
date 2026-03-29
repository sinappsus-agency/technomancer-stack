"""Quick debug: check image workflow structure for embedded API data."""
import json
from pathlib import Path

p = Path(r"C:\ComfyUI\user\default\workflows\image_z_image_turbo.json")
d = json.loads(p.read_text(encoding="utf-8"))

print("Top-level keys:", list(d.keys()))
print()

extra = d.get("extra", {})
print("extra keys:", list(extra.keys()))

prompt = extra.get("prompt", {})
if prompt:
    print(f"extra.prompt has {len(prompt)} entries")
    for k, v in list(prompt.items())[:5]:
        ct = v.get("class_type", "?") if isinstance(v, dict) else type(v).__name__
        print(f"  '{k}': class_type={ct}")
else:
    print("No extra.prompt field")

# Check if any top-level key has class_type
for k, v in d.items():
    if isinstance(v, dict) and "class_type" in v:
        print(f"\nFOUND class_type at top-level key '{k}': {v.get('class_type')}")

# Check nodes
nodes = d.get("nodes", [])
print(f"\nnodes is a list: {isinstance(nodes, list)}")
print(f"nodes count: {len(nodes)}")

# Check if it has the weird colon IDs
for k in d.keys():
    if ":" in str(k):
        print(f"Key with colon: '{k}'")
