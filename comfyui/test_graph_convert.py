"""Test graph-to-API conversion and list_saved_workflows against real ComfyUI data."""
import json
import sys
import os
import types
from pathlib import Path

# Mock the mcp package before importing server
mock_mcp = types.ModuleType("mcp")
mock_server = types.ModuleType("mcp.server")
mock_fastmcp = types.ModuleType("mcp.server.fastmcp")

class FakeMCP:
    def __init__(self, name): self.name = name
    def tool(self): return lambda f: f
    def run(self): pass

mock_fastmcp.FastMCP = FakeMCP
mock_mcp.server = mock_server
mock_server.fastmcp = mock_fastmcp
sys.modules["mcp"] = mock_mcp
sys.modules["mcp.server"] = mock_server
sys.modules["mcp.server.fastmcp"] = mock_fastmcp

# Add the mcp directory so we can import server components
sys.path.insert(0, str(Path(__file__).parent / "mcp"))

import urllib.request
import urllib.error

COMFYUI_URL = "http://127.0.0.1:8000"

# Now import server
import server

# Patch _get to use correct URL
def _get(path, timeout=10):
    with urllib.request.urlopen(f"{COMFYUI_URL}{path}", timeout=timeout) as r:
        return json.loads(r.read())

server._get = _get
server.COMFYUI_URL = COMFYUI_URL

passed = 0
failed = 0

def test(name, condition, detail=""):
    global passed, failed
    if condition:
        passed += 1
        print(f"  PASS  {name}")
    else:
        failed += 1
        print(f"  FAIL  {name} — {detail}")


# ── Test 1: _get_widget_names for known types ──
print("\n=== Test 1: _get_widget_names ===")

server._object_info_cache.clear()

wn = server._get_widget_names("KSampler")
test("KSampler has widget names", wn is not None)
if wn:
    test("KSampler includes seed", "seed" in wn, f"got: {wn}")
    test("KSampler does NOT include control_after_generate (hidden)", "control_after_generate" not in wn, f"got: {wn}")
    test("KSampler includes steps", "steps" in wn, f"got: {wn}")
    test("KSampler does NOT include model (connection type)", "model" not in wn, f"got: {wn}")

wn2 = server._get_widget_names("SaveImage")
test("SaveImage has widget names", wn2 is not None)
if wn2:
    test("SaveImage includes filename_prefix", "filename_prefix" in wn2, f"got: {wn2}")

wn3 = server._get_widget_names("CLIPTextEncode")
test("CLIPTextEncode has widget names", wn3 is not None)
if wn3:
    test("CLIPTextEncode includes text", "text" in wn3, f"got: {wn3}")
    test("CLIPTextEncode does NOT include clip (connection)", "clip" not in wn3, f"got: {wn3}")


# ── Discover saved workflow files ──
SAVED_DIR = Path(r"C:\ComfyUI\user\default\workflows")
saved_files = sorted(SAVED_DIR.glob("*.json")) if SAVED_DIR.exists() else []

# Find image and video workflows by content pattern
image_wf_path = None
video_wf_path = None
for sf in saved_files:
    try:
        d = json.loads(sf.read_text(encoding="utf-8"))
        nodes = d.get("nodes", [])
        # Image workflow: has SaveImage outer node
        for n in nodes:
            if n.get("type") == "SaveImage":
                image_wf_path = sf
                break
            if n.get("type") == "SaveVideo":
                video_wf_path = sf
                break
    except Exception:
        pass

print(f"  Image workflow: {image_wf_path.name if image_wf_path else 'not found'}")
print(f"  Video workflow: {video_wf_path.name if video_wf_path else 'not found'}")


# ── Test 2: _graph_to_api with image workflow ──
print("\n=== Test 2: Graph-to-API — image workflow ===")

if image_wf_path and image_wf_path.exists():
    graph = json.loads(image_wf_path.read_text(encoding="utf-8"))
    api, err = server._graph_to_api(graph)
    
    test("Conversion succeeded", err is None, f"error: {err}")
    test("API dict is not empty", len(api) > 0, f"got {len(api)} nodes")
    
    # Expected nodes: SaveImage(9) outer + inner nodes with 57: prefix
    expected_nodes = {"9", "57:30", "57:29", "57:33", "57:8", "57:28", "57:27", "57:13", "57:11", "57:3"}
    actual_nodes = set(api.keys())
    test("All expected nodes present", expected_nodes.issubset(actual_nodes),
         f"missing: {expected_nodes - actual_nodes}, got: {actual_nodes}")
    
    # SaveImage should reference VAEDecode(8) output
    if "9" in api:
        si = api["9"]["inputs"]
        test("SaveImage.images links to VAEDecode", 
             si.get("images") == ["57:8", 0],
             f"got: {si.get('images')}")
        test("SaveImage.filename_prefix is string",
             isinstance(si.get("filename_prefix"), str),
             f"got: {si.get('filename_prefix')}")
    
    # KSampler(57:3) should have correct links and values
    if "57:3" in api:
        ks = api["57:3"]["inputs"]
        test("KSampler.model links to ModelSamplingAuraFlow(57:11)",
             ks.get("model") == ["57:11", 0], f"got: {ks.get('model')}")
        test("KSampler.positive links to CLIPTextEncode(57:27)",
             ks.get("positive") == ["57:27", 0], f"got: {ks.get('positive')}")
        test("KSampler.seed is int value",
             isinstance(ks.get("seed"), (int, float)), f"got: {ks.get('seed')}")
        test("KSampler.steps is int value (8)",
             ks.get("steps") == 8, f"got: {ks.get('steps')}")
        test("KSampler.sampler_name is string",
             isinstance(ks.get("sampler_name"), str), f"got: {ks.get('sampler_name')}")
        test("No control_after_generate in KSampler",
             "control_after_generate" not in ks, f"keys: {list(ks.keys())}")
    
    # CLIPTextEncode(57:27) should have inline text
    if "57:27" in api:
        ct = api["57:27"]["inputs"]
        test("CLIPTextEncode has text value",
             isinstance(ct.get("text"), str) and len(ct["text"]) > 10,
             f"got: {str(ct.get('text'))[:50]}")
        test("CLIPTextEncode.clip links to CLIPLoader(57:30)",
             ct.get("clip") == ["57:30", 0], f"got: {ct.get('clip')}")
    
    # EmptySD3LatentImage(57:13) should have dimensions
    if "57:13" in api:
        li = api["57:13"]["inputs"]
        test("EmptySD3LatentImage.width is 1024",
             li.get("width") == 1024, f"got: {li.get('width')}")
        test("EmptySD3LatentImage.height is 1024",
             li.get("height") == 1024, f"got: {li.get('height')}")
else:
    print("  SKIP  Image workflow not found on disk")


# ── Test 3: _graph_to_api with video workflow ──
print("\n=== Test 3: Graph-to-API — video workflow ===")

if video_wf_path and video_wf_path.exists():
    graph = json.loads(video_wf_path.read_text(encoding="utf-8"))
    api, err = server._graph_to_api(graph)
    
    test("Conversion succeeded", err is None, f"error: {err}")
    test("Has many nodes (>15)", len(api) > 15, f"got {len(api)} nodes")
    
    # Outer nodes that should survive: LoadImage(269), LoadAudio(276), SaveVideo(341)
    test("LoadImage(269) present", "269" in api)
    test("LoadAudio(276) present", "276" in api)
    test("SaveVideo(341) present", "341" in api)
    
    # MarkdownNote(103) and RecordAudio(339) should be skipped
    test("MarkdownNote(103) skipped", "103" not in api and "340:103" not in api)
    test("RecordAudio(339) skipped (mode=4)", "339" not in api and "340:339" not in api)
    
    # SaveVideo should NOT reference subgraph node 340 — should reference inner node
    if "341" in api:
        sv = api["341"]["inputs"]
        video_ref = sv.get("video")
        test("SaveVideo.video does NOT reference subgraph(340)",
             not (isinstance(video_ref, list) and video_ref[0] == "340"),
             f"got: {video_ref}")
        # It should reference CreateVideo(340:312) output 0
        test("SaveVideo.video references CreateVideo(340:312)",
             video_ref == ["340:312", 0], f"got: {video_ref}")
    
    # Inner nodes should have 340: prefix
    inner_key_nodes = ["340:317", "340:293", "340:306", "340:307", "340:291", "340:310", "340:312", "340:316"]
    for nid in inner_key_nodes:
        test(f"Inner node {nid} present", nid in api)
    
    # LoadImage(269) → ResizeImageMaskNode(340:297): check connection through subgraph
    if "340:297" in api:
        ri = api["340:297"]["inputs"]
        # The first input should come from LoadImage(269) via subgraph expansion
        input_ref = ri.get("input")
        test("ResizeImageMaskNode gets input from LoadImage(269)",
             input_ref == ["269", 0], f"got: {input_ref}")
    
    # Check that inner Reroute(300) is eliminated
    test("Reroute(300) not in API", "300" not in api and "340:300" not in api)
    
    # Nodes that fed from Reroute(300) should reference CheckpointLoader(340:317) slot 2
    if "340:295" in api:
        vae_ref = api["340:295"]["inputs"].get("vae")
        test("LTXVLatentUpsampler.vae resolved through Reroute to 340:317",
             vae_ref == ["340:317", 2], f"got: {vae_ref}")

    # Check a prompt value survived conversion
    if "340:319" in api:
        pv = api["340:319"]["inputs"].get("value")
        test("Prompt primitive retained text value",
             isinstance(pv, str) and "buddha" in pv.lower(),
             f"got: {str(pv)[:50] if pv else None}")

    # No subgraph wrapper as plain '340' key in output (inner nodes use '340:X' format)
    test("Subgraph wrapper(340) not in API", "340" not in api)
    
    # Dump summary
    class_types = [v.get("class_type", "?") for v in api.values()]
    print(f"\n  Node count: {len(api)}")
    print(f"  Class types: {sorted(set(class_types))}")
else:
    print("  SKIP  Video workflow not found on disk")


# ── Test 4: Auto-parameterize the converted workflow ──
print("\n=== Test 4: Auto-parameterize converted image workflow ===")

if image_wf_path and image_wf_path.exists():
    graph = json.loads(image_wf_path.read_text(encoding="utf-8"))
    api, _ = server._graph_to_api(graph)
    parameterized = server._auto_parameterize(api, "z-image-turbo-test")
    params = parameterized.get("_meta", {}).get("params", {})
    
    test("Has parameters", len(params) > 0, f"got {len(params)}")
    
    param_names = list(params.keys())
    print(f"  Detected params: {param_names}")
    
    # Should detect the prompt in CLIPTextEncode(27)
    prompt_params = [p for p in params.values() if "prompt" in p.get("description", "").lower()]
    test("Detected prompt parameter", len(prompt_params) > 0)
    
    # Should detect seed in KSampler(3)
    seed_params = [p for p in params.values() if "seed" in p.get("description", "").lower()]
    test("Detected seed parameter", len(seed_params) > 0)


# ── Test 5: list_saved_workflows ──
print("\n=== Test 5: list_saved_workflows ===")

result = server.list_saved_workflows()
test("Returns string", isinstance(result, str))
image_name = image_wf_path.stem if image_wf_path else ""
video_name = video_wf_path.stem if video_wf_path else ""
test("Mentions image workflow", image_name in result if image_name else True, f"result: {result[:200]}")
test("Mentions video workflow", video_name in result if video_name else True)
test("Shows node info", "nodes" in result.lower())
test("Shows subgraph info", "subgraph" in result.lower())
print(f"\n  Output:\n{result}")


# ── Test 6: Full import pipeline (dry run — test but clean up) ──
print("\n=== Test 6: Full import pipeline ===")

if image_wf_path and image_wf_path.exists():
    # Import using explicit saved-workflows path to ensure graph conversion is tested
    # (bare filenames may resolve to pre-existing API exports in exports/)
    template_name = "z-image-turbo-test-pipeline"
    dest = server.WORKFLOW_DIR / f"{template_name}.json"
    # Clean up from any previous run
    if dest.exists():
        dest.unlink()
    result = server.import_workflow(str(image_wf_path), template_name)
    
    test("Import succeeded", "ERROR" not in result, f"result: {result[:300]}")
    test("Shows conversion note", "graph format" in result.lower(), f"result: {result[:300]}")
    test("Shows detected parameters", "PARAM_" in result)
    
    print(f"\n  Import output:\n{result}")
    
    # Clean up the test template
    dest = server.WORKFLOW_DIR / f"{template_name}.json"
    if dest.exists():
        dest.unlink()
        test("Cleaned up test template", not dest.exists())


# ── Summary ──
print(f"\n{'='*50}")
print(f"Results: {passed} passed, {failed} failed")
if failed:
    sys.exit(1)
