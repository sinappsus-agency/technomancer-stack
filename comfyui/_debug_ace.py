"""Debug the ACE Step submission - see what ComfyUI says."""
import json, urllib.request, urllib.error, random

COMFY = "http://127.0.0.1:8000"

tags = (
    "Ritual ambient, chamber sacred, occult devotional, "
    "clear, visionary, spacious, intelligent, "
    "numinous, emotionally precise, archetypal, "
    "close-mic lead with restrained choir on refrains, "
    "felt piano, frame drum pulse, warm strings, bell or chime accents, low drone, "
    "60 BPM"
)
lyrics = (
    "[Invocation]\n"
    "Damabiah of clear blessing, enter the breath and steady the heart.\n\n"
    "[Verse 1]\n"
    "The sign is Aquarius, the stage is Return with the Elixir.\n"
    "What once felt fated can become chosen.\n\n"
    "[Chorus]\n"
    "DAMABIAH, DRAW ME INTO THE TRUE CENTER.\n"
    "LET THIS CURRENT BECOME PRACTICE.\n\n"
    "[Benediction]\n"
    "By this hymn, the current of Damabiah is welcomed."
)

seed = random.randint(0, 2**63)

wf = {
    "104": {
        "class_type": "UNETLoader",
        "inputs": {"unet_name": "acestep_v1.5_turbo.safetensors", "weight_dtype": "default"}
    },
    "106": {
        "class_type": "VAELoader",
        "inputs": {"vae_name": "ace_1.5_vae.safetensors"}
    },
    "105": {
        "class_type": "DualCLIPLoader",
        "inputs": {
            "clip_name1": "qwen_0.6b_ace15.safetensors",
            "clip_name2": "qwen_4b_ace15.safetensors",
            "type": "ace",
            "device": "default"
        }
    },
    "94": {
        "class_type": "TextEncodeAceStepAudio1.5",
        "inputs": {
            "tags": tags,
            "lyrics": lyrics,
            "seed": seed,
            "control_after_generate": "fixed",
            "bpm": 62,
            "duration": 120,
            "instr_num": 4,
            "language": "en",
            "clip": ["105", 0]
        }
    },
    "98": {
        "class_type": "EmptyAceStep1.5LatentAudio",
        "inputs": {"seconds": 120, "batch_size": 1}
    },
    "47": {
        "class_type": "ConditioningZeroOut",
        "inputs": {"conditioning": ["94", 0]}
    },
    "78": {
        "class_type": "ModelSamplingAuraFlow",
        "inputs": {"shift": 3, "model": ["104", 0]}
    },
    "3": {
        "class_type": "KSampler",
        "inputs": {
            "seed": seed,
            "control_after_generate": "fixed",
            "steps": 8,
            "cfg": 1,
            "sampler_name": "euler",
            "scheduler": "simple",
            "denoise": 1,
            "model": ["78", 0],
            "positive": ["94", 0],
            "negative": ["47", 0],
            "latent_image": ["98", 0]
        }
    },
    "18": {
        "class_type": "VAEDecodeAudio",
        "inputs": {"samples": ["3", 0], "vae": ["106", 0]}
    },
    "107": {
        "class_type": "SaveAudioMP3",
        "inputs": {"filename_prefix": "damabiah_hymn", "quality": "V0", "audio": ["18", 0]}
    }
}

# Check node info for TextEncodeAceStepAudio1.5 and SaveAudioMP3
print("=== Checking node signatures ===")
resp = urllib.request.urlopen(f"{COMFY}/api/object_info/TextEncodeAceStepAudio1.5")
info = json.loads(resp.read())
node = info.get("TextEncodeAceStepAudio1.5", {})
req_inputs = node.get("input", {}).get("required", {})
opt_inputs = node.get("input", {}).get("optional", {})
print("TextEncodeAceStepAudio1.5 required:")
for k, v in req_inputs.items():
    print(f"  {k}: {v}")
print("TextEncodeAceStepAudio1.5 optional:")
for k, v in opt_inputs.items():
    print(f"  {k}: {v}")

print("\n=== Checking SaveAudioMP3 ===")
resp2 = urllib.request.urlopen(f"{COMFY}/api/object_info/SaveAudioMP3")
info2 = json.loads(resp2.read())
node2 = info2.get("SaveAudioMP3", {})
req2 = node2.get("input", {}).get("required", {})
print("SaveAudioMP3 required:")
for k, v in req2.items():
    print(f"  {k}: {v}")

# Now try submitting and capturing the error
print("\n=== Submitting ===")
payload = json.dumps({"prompt": wf}).encode()
req = urllib.request.Request(
    f"{COMFY}/api/prompt",
    data=payload,
    headers={"Content-Type": "application/json"},
)
try:
    resp = urllib.request.urlopen(req)
    data = json.loads(resp.read())
    print(f"OK: {data}")
except urllib.error.HTTPError as e:
    body = e.read().decode()
    print(f"HTTP {e.code}: {body[:2000]}")
