import subprocess, os
os.chdir(r"C:\Users\artgr\OneDrive\BACKUP\HTH\technomancer-stack")
subprocess.run(["git", "add", "-A"], check=True)
msg = """Cleanup: remove dev artifacts, add missing documentation, fix SKILL.md

- Deleted 22 dev/debug scripts and staging JSONs from comfyui/
- Created comfyui/README.md with orientation, MCP tools, workbook integration
- Created n8n-templates/README.md with 10-workflow index and chapter mapping
- Created config/README.md with config directory orientation
- Fixed SKILL.md: removed 5 phantom workflow template references
- Updated root README: added comfyui/, iot/ to structure and chapter table
- Added Using the Workbook and Using ComfyUI sections to root README
- Updated .gitignore with comfyui dev artifact patterns"""
r = subprocess.run(["git", "commit", "-m", msg], capture_output=True, text=True)
print(r.stdout)
print(r.stderr)
