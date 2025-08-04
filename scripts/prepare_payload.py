import subprocess, json

files = subprocess.check_output(
    "git diff --name-only origin/main...HEAD '*.sol'",
    shell=True, text=True
).splitlines()

print("Changed files:", files)

codebase = {f: open(f).read() for f in files}
diff = subprocess.check_output(
    "git diff origin/main...HEAD", shell=True, text=True
)

with open("payload.json", "w") as f:
    json.dump({"diff": diff, "codebase": codebase}, f, indent=2)
