"""Post-generation hook: remove optional utility files based on cookiecutter choices."""

import os

# Paths relative to the generated project root
REMOVE_PATHS = []

for path in REMOVE_PATHS:
    if os.path.isfile(path):
        os.remove(path)
