import subprocess
import json
import os

# Get the list of changed Solidity files
print("📂 Collecting changed Solidity files...")
changed_files_str = subprocess.check_output(
    "git diff --name-only origin/main...HEAD -- '*.sol'",
    shell=True,
    text=True
).strip()

# If no .sol files were changed, exit gracefully
if not changed_files_str:
    print("No Solidity files changed. Skipping review.")
    with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
        f.write("has_changes=false\n")
    exit(0)

changed_files = changed_files_str.splitlines()
print(f"🔍 Files changed: {changed_files}")

codebase_before = {}
codebase_after = {}

for file_path in changed_files:
    # Get the state of the file AFTER changes from the local checkout
    print(f"📄 Reading 'after' state for {file_path}")
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            codebase_after[file_path] = f.read()
    else:
        # The file was deleted in the PR
        codebase_after[file_path] = ""

    # Get the state of the file BEFORE changes from the main branch
    print(f"📄 Reading 'before' state for {file_path}")
    try:
        # Use git show to get the file content from the base branch
        before_content = subprocess.check_output(
            f"git show origin/main:{file_path}",
            shell=True,
            text=True,
            stderr=subprocess.DEVNULL # Hide errors for new files
        )
        codebase_before[file_path] = before_content
    except subprocess.CalledProcessError:
        # This error means the file is new, so its 'before' state is empty
        print(f"'{file_path}' is a new file. 'Before' state is empty.")
        codebase_before[file_path] = ""

# Read the diff content from the file generated in the previous step
with open("diff.patch", "r") as f:
    diff_content = f.read()

# Assemble the final payload with the new structure
payload = {
    "diff": diff_content,
    "codebase_before": codebase_before,
    "codebase_after": codebase_after
}

# Write the payload to a file for the next step
with open("payload.json", "w") as f:
    json.dump(payload, f, indent=2)

print("✅ Payload prepared with 'before' and 'after' states:")
print(json.dumps(payload, indent=2))

# Set a step output to indicate that changes were found and processed
with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
    f.write("has_changes=true\n")
