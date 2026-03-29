"""Show key nodes from the converted LTX API workflow."""
import json

with open("_ltx_api.json", "r") as f:
    api = json.load(f)

# Show nodes we need to patch
keys = ["269", "276", "340:319", "340:342", "340:306", "340:314", 
        "340:323", "340:324", "340:330", "340:331", "340:305",
        "340:317", "340:318", "340:293", "340:344", "341",
        "340:312", "340:335"]
for k in keys:
    if k in api:
        print(f"\n=== Node {k} ({api[k].get('class_type','?')}) ===")
        print(json.dumps(api[k]["inputs"], indent=2))
