"""Try different download paths for ComfyUI saved workflows."""
import json, urllib.request, urllib.parse

COMFY = "http://127.0.0.1:8000"
name = "textToaudio_ace_step_1_5_split_4b.json"

# Try various URL patterns
attempts = [
    f"{COMFY}/api/userdata/workflows/{name}",
    f"{COMFY}/api/userdata/workflows/{urllib.parse.quote(name)}",
    f"{COMFY}/userdata/workflows/{name}",
    f"{COMFY}/api/userdata/{name}?dir=workflows",
]

for url in attempts:
    try:
        req = urllib.request.Request(url)
        resp = urllib.request.urlopen(req)
        data = resp.read()
        print(f"OK: {url}  ({len(data)} bytes)")
        with open("_wf_ace_step.json", "wb") as f:
            f.write(data)
        break
    except Exception as e:
        print(f"FAIL: {url} -> {e}")
else:
    # Try GET with query param
    url2 = f"{COMFY}/api/userdata/workflows/{name}?dir=workflows"
    try:
        resp = urllib.request.urlopen(url2)
        data = resp.read()
        print(f"OK: {url2}")
    except:
        pass

    # Last resort: check if we can use the file= query approach
    url3 = f"{COMFY}/api/userdata?dir=workflows&file={urllib.parse.quote(name)}"
    try:
        resp = urllib.request.urlopen(url3)
        data = resp.read()
        print(f"OK: {url3}  ({len(data)} bytes)")
    except Exception as e:
        print(f"FAIL: {url3} -> {e}")
