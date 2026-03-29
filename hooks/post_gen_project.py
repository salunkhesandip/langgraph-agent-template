"""Post-generation hook: initialise git and clean up optional files."""

import os
import subprocess

# Paths relative to the generated project root
REMOVE_PATHS = []

for path in REMOVE_PATHS:
    if os.path.isfile(path):
        os.remove(path)

# Initialize a git repository so users can start versioning immediately
try:
    subprocess.run(["git", "init"], check=True, capture_output=True)
    subprocess.run(["git", "add", "."], check=True, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", "Initial commit from langgraph-agent-template"],
        check=True,
        capture_output=True,
    )
except (FileNotFoundError, subprocess.CalledProcessError):
    # git not installed or init failed — not critical
    pass
