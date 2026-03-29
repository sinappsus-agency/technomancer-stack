"""Trace which nodes depend on the upscaler (340:313)."""
import json

with open("_ltx_api.json", "r") as f:
    api = json.load(f)

# Find all nodes that reference 340:313
target = "340:313"
dependents = []
for nid, nd in api.items():
    for k, v in nd.get("inputs", {}).items():
        if isinstance(v, list) and len(v) == 2 and v[0] == target:
            dependents.append(f"  {nid} ({nd['class_type']}).{k} <- [{target}, {v[1]}]")

print(f"Nodes depending on {target}:")
for d in dependents:
    print(d)

# Now trace the chain from those dependents
for nid, nd in api.items():
    for k, v in nd.get("inputs", {}).items():
        if isinstance(v, list) and len(v) == 2:
            for dep_line in dependents:
                dep_nid = dep_line.strip().split(" ")[0]
                if v[0] == dep_nid:
                    print(f"  -> {nid} ({nd['class_type']}).{k} <- [{dep_nid}, {v[1]}]")
