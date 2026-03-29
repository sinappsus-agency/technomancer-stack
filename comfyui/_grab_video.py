"""Download the already-generated LTX video from ComfyUI output."""
import urllib.request, os

COMFY = "http://127.0.0.1:8000"
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "test", "damabiah")

fn = "damabiah_video_00001_.mp4"
url = f"{COMFY}/api/view?filename={fn}&subfolder=&type=output"
dest = os.path.join(OUTPUT_DIR, "damabiah_video.mp4")

resp = urllib.request.urlopen(url)
with open(dest, "wb") as f:
    f.write(resp.read())

size_mb = os.path.getsize(dest) / 1024 / 1024
print(f"Saved: {dest} ({size_mb:.1f} MB)")
