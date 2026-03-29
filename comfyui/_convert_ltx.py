"""
Convert LTX i+a2v workflow from graph to API format using _graph_to_api from our MCP server.
Also tests ElevenLabs TTS availability.
"""
import json, sys, os, types

# ── Read the LTX workflow from disk ──
LTX_PATH = r"C:\ComfyUI\user\default\workflows\LTXimageAndAudioToVideo.json"
with open(LTX_PATH, "r") as f:
    ltx_graph = json.load(f)

print("=== LTX Workflow Structure ===")
print(f"  Top-level keys: {list(ltx_graph.keys())}")
print(f"  Nodes: {len(ltx_graph.get('nodes', []))}")
print(f"  Links: {len(ltx_graph.get('links', []))}")
defs = ltx_graph.get("definitions", {}).get("subgraphs", [])
for sg in defs:
    print(f"  Subgraph '{sg.get('id','')}': {len(sg.get('nodes',[]))} inner nodes, {len(sg.get('links',[]))} inner links")
print()

# List outer nodes
for n in ltx_graph.get("nodes", []):
    print(f"  Node {n['id']}: type={n.get('type','?')}, title={n.get('title','')}")
print()

# ── Import _graph_to_api by exec'ing server.py with mocked mcp ──
SERVER_PY = os.path.join(os.path.dirname(__file__), "mcp", "server.py")

# Create a mock mcp module structure
mock_fastmcp = types.ModuleType("mcp.server.fastmcp")
class FakeMCP:
    def __init__(self, *a, **kw): pass
    def tool(self, *a, **kw):
        return lambda fn: fn
mock_fastmcp.FastMCP = FakeMCP
sys.modules["mcp"] = types.ModuleType("mcp")
sys.modules["mcp.server"] = types.ModuleType("mcp.server")
sys.modules["mcp.server.fastmcp"] = mock_fastmcp

# Now we can import server.py
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "mcp"))
import importlib.util
spec = importlib.util.spec_from_file_location("server", SERVER_PY)
server = importlib.util.module_from_spec(spec)
spec.loader.exec_module(server)

print("=== Converting with _graph_to_api ===")
api_dict, err = server._graph_to_api(ltx_graph)
if err:
    print(f"  ERROR: {err}")
else:
    print(f"  Success! {len(api_dict)} API nodes")
    # Save to file for inspection
    out_path = os.path.join(os.path.dirname(__file__), "_ltx_api.json")
    with open(out_path, "w") as f:
        json.dump(api_dict, f, indent=2)
    print(f"  Saved API workflow to {out_path}")

    # Show node summary
    for nid, nd in sorted(api_dict.items(), key=lambda x: x[0]):
        ct = nd.get("class_type", "?")
        title = nd.get("_meta", {}).get("title", "")
        print(f"    {nid}: {ct} ({title})")

# ── Check for input nodes we need to patch ──
print("\n=== Input Nodes to Patch ===")
for nid, nd in api_dict.items():
    ct = nd.get("class_type", "")
    if ct in ("LoadImage", "LoadAudio"):
        print(f"  Node {nid} ({ct}): {json.dumps(nd.get('inputs', {}))}")
    if "prompt" in str(nd.get("inputs", {})).lower() or "text" in ct.lower():
        for k, v in nd.get("inputs", {}).items():
            if isinstance(v, str) and len(v) > 20:
                print(f"  Node {nid} ({ct}) .{k}: {v[:80]}...")
