"""Check that all models needed for the LTX i+a2v workflow exist on disk."""
import os, json

MODEL_DIRS = [
    r"C:\ComfyUI\models",
    os.path.join(os.environ.get("LOCALAPPDATA", ""), "Programs", "ComfyUI", "resources", "ComfyUI", "models"),
]

NEEDED = {
    "checkpoints": ["ltx-2.3-22b-dev-fp8.safetensors"],
    "text_encoders": ["gemma_3_12B_it_fp4_mixed.safetensors"],
    "loras": ["ltx-2.3-22b-distilled-lora-384.safetensors", "gemma-3-12b-it-abliterated_lora_rank64_bf16.safetensors"],
    "upscale_models": ["ltx-2.3-spatial-upscaler-x2-1.1.safetensors"],
}

for category, files in NEEDED.items():
    for fn in files:
        found = False
        for base in MODEL_DIRS:
            path = os.path.join(base, category, fn)
            if os.path.exists(path):
                size_mb = os.path.getsize(path) / 1024 / 1024
                print(f"  OK  {category}/{fn}  ({size_mb:.0f} MB)")
                found = True
                break
        if not found:
            # Also check subdirectories
            for base in MODEL_DIRS:
                cat_dir = os.path.join(base, category)
                if os.path.isdir(cat_dir):
                    for root, dirs, fnames in os.walk(cat_dir):
                        if fn in fnames:
                            full = os.path.join(root, fn)
                            size_mb = os.path.getsize(full) / 1024 / 1024
                            print(f"  OK  {os.path.relpath(full, base)}  ({size_mb:.0f} MB)")
                            found = True
                            break
                if found:
                    break
            if not found:
                print(f"  MISSING  {category}/{fn}")
