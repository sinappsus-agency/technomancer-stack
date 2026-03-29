"""Check available TTS/speech nodes in ComfyUI."""
import urllib.request, json

req = urllib.request.Request("http://127.0.0.1:8000/api/object_info")
with urllib.request.urlopen(req) as r:
    data = json.loads(r.read())

keywords = ["tts", "speech", "elevenlabs", "voice", "speak", "kokoro", "piper", "bark", "xtts", "parler"]
tts_nodes = {k: v for k, v in data.items() if any(w in k.lower() for w in keywords)}

if not tts_nodes:
    print("No TTS/speech nodes found!")
else:
    for name in sorted(tts_nodes):
        inputs = tts_nodes[name].get("input", {}).get("required", {})
        optional = tts_nodes[name].get("input", {}).get("optional", {})
        print(f"\n=== {name} ===")
        for k, v in inputs.items():
            print(f"  REQ  {k}: {v[0] if isinstance(v, list) and len(v) == 1 else v}")
        for k, v in (optional or {}).items():
            print(f"  OPT  {k}: {v[0] if isinstance(v, list) and len(v) == 1 else v}")
