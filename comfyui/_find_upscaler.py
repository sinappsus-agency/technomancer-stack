"""Find which LTX API nodes reference the upscaler model."""
import json

with open("_ltx_api.json", "r") as f:
    api = json.load(f)

for nid, nd in api.items():
    ct = nd.get("class_type", "")
    inputs = nd.get("inputs", {})
    for k, v in inputs.items():
        if isinstance(v, str) and "upscal" in v.lower():
            print(f"  Node {nid} ({ct}): {k} = {v}")
    if "upscal" in ct.lower():
        print(f"  Node {nid} ({ct}): {json.dumps(inputs, indent=2)}")
