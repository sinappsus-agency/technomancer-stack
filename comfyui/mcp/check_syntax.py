import ast, sys
with open("server.py", encoding="utf-8") as f:
    code = f.read()
try:
    ast.parse(code)
    print("SYNTAX OK")
    print(f"Lines: {len(code.splitlines())}")
except SyntaxError as e:
    print(f"SYNTAX ERROR: {e}")
    sys.exit(1)
