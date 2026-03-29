"""Read workflows from disk and extract their node structure."""
import json, os

BASE = r"C:\ComfyUI\user\default\workflows"
BUILTIN = r"C:\ComfyUI\.venv\Lib\site-packages"

# 1. ACE Step workflow
ace_path = os.path.join(BASE, "textToaudio_ace_step_1_5_split_4b.json")
with open(ace_path) as f:
    ace = json.load(f)
print("=== ACE STEP WORKFLOW ===")
print(f"Nodes: {len(ace.get('nodes', []))}")
for n in ace.get("nodes", []):
    t = n.get("type", "?")
    nid = n.get("id", "?")
    wv = n.get("widgets_values", [])
    print(f"  [{nid}] {t}")
    if wv:
        # Print only first few meaningful values
        vals = [str(v)[:80] for v in wv[:8] if v is not None and str(v).strip()]
        if vals:
            print(f"       vals: {vals}")

sgs = ace.get("definitions", {}).get("subgraphs", [])
if sgs:
    print(f"\nSubgraphs: {len(sgs)}")
    for sg in sgs:
        print(f"  '{sg.get('name', '?')}' — {len(sg.get('nodes', []))} inner nodes")
        for n in sg.get("nodes", []):
            t = n.get("type", "?")
            nid = n.get("id", "?")
            wv = n.get("widgets_values", [])
            print(f"    [{nid}] {t}")
            if wv:
                vals = [str(v)[:80] for v in wv[:8] if v is not None and str(v).strip()]
                if vals:
                    print(f"           vals: {vals}")

# 2. LTX Image+Audio to Video workflow
ltx_path = os.path.join(BASE, "LTXimageAndAudioToVideo.json")
with open(ltx_path) as f:
    ltx = json.load(f)
print("\n\n=== LTX IMAGE+AUDIO TO VIDEO ===")
print(f"Nodes: {len(ltx.get('nodes', []))}")
for n in ltx.get("nodes", []):
    t = n.get("type", "?")
    nid = n.get("id", "?")
    wv = n.get("widgets_values", [])
    print(f"  [{nid}] {t}")
    if wv:
        vals = [str(v)[:80] for v in wv[:8] if v is not None and str(v).strip()]
        if vals:
            print(f"       vals: {vals}")

sgs = ltx.get("definitions", {}).get("subgraphs", [])
if sgs:
    print(f"\nSubgraphs: {len(sgs)}")
    for sg in sgs:
        print(f"  '{sg.get('name', '?')}' — {len(sg.get('nodes', []))} inner nodes")
        for n in sg.get("nodes", []):
            t = n.get("type", "?")
            nid = n.get("id", "?")
            wv = n.get("widgets_values", [])
            print(f"    [{nid}] {t}")
            if wv:
                vals = [str(v)[:80] for v in wv[:8] if v is not None and str(v).strip()]
                if vals:
                    print(f"           vals: {vals}")

# 3. Also check the built-in ia2v template
import glob
for t_path in glob.glob(os.path.join(BUILTIN, "comfyui_workflow_templates*", "templates", "video_ltx2_3_ia2v.json")):
    with open(t_path) as f:
        ia2v = json.load(f)
    print(f"\n\n=== BUILT-IN LTX IA2V TEMPLATE ===")
    print(f"Nodes: {len(ia2v.get('nodes', []))}")
    for n in ia2v.get("nodes", []):
        t = n.get("type", "?")
        nid = n.get("id", "?")
        wv = n.get("widgets_values", [])
        print(f"  [{nid}] {t}")
        if wv:
            vals = [str(v)[:80] for v in wv[:8] if v is not None and str(v).strip()]
            if vals:
                print(f"       vals: {vals}")
    sgs2 = ia2v.get("definitions", {}).get("subgraphs", [])
    if sgs2:
        print(f"\nSubgraphs: {len(sgs2)}")
        for sg in sgs2:
            print(f"  '{sg.get('name', '?')}' — {len(sg.get('nodes', []))} inner nodes")
            for n in sg.get("nodes", []):
                t2 = n.get("type", "?")
                nid2 = n.get("id", "?")
                wv2 = n.get("widgets_values", [])
                print(f"    [{nid2}] {t2}")
                if wv2:
                    vals = [str(v)[:80] for v in wv2[:8] if v is not None and str(v).strip()]
                    if vals:
                        print(f"           vals: {vals}")
