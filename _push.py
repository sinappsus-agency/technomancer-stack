import subprocess, os
os.chdir(r"C:\Users\artgr\OneDrive\BACKUP\HTH\technomancer-stack")
# Remove the commit helper scripts
for f in ["_commit.py", "_clean_comfyui.py"]:
    if os.path.exists(f):
        os.remove(f)
        print(f"Removed {f}")
subprocess.run(["git", "add", "-A"], check=True)
r = subprocess.run(["git", "commit", "-m", "Remove temporary helper scripts"], capture_output=True, text=True)
print(r.stdout)
print(r.stderr)
# Push
r2 = subprocess.run(["git", "push"], capture_output=True, text=True)
print(r2.stdout)
print(r2.stderr)
