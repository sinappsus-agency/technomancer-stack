"""Download and inspect the ACE Step and LTX saved workflows."""
import json, urllib.request

COMFY = "http://127.0.0.1:8000"

for name in ["textToaudio_ace_step_1_5_split_4b.json", "LTXimageAndAudioToVideo.json"]:
    url = f"{COMFY}/api/userdata/workflows/{name}"
    resp = urllib.request.urlopen(url)
    data = json.loads(resp.read())
    out = f"_wf_{name}"
    with open(out, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Saved {out} ({len(data.get('nodes', []))} top-level nodes)")

# Also check for built-in LTX ia2v template
import glob, os
for t in glob.glob(r"C:\ComfyUI\.venv\Lib\site-packages\comfyui_workflow_templates*\templates\video_ltx2_3_ia2v.json"):
    print(f"\nFound built-in ia2v template: {t}")
    with open(t) as f:
        d = json.load(f)
    print(f"  Nodes: {len(d.get('nodes', []))}")
    with open("_wf_ltx_ia2v_builtin.json", "w") as f:
        json.dump(d, f, indent=2)
    print(f"  Saved _wf_ltx_ia2v_builtin.json")
