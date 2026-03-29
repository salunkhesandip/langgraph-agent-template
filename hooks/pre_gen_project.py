"""Pre-generation hook: validate cookiecutter inputs."""

import re
import sys

slug = "{{ cookiecutter.project_slug }}"
package = "{{ cookiecutter.package_name }}"
python_version = "{{ cookiecutter.python_version }}"
temperature = "{{ cookiecutter.default_temperature }}"

# -- Slug must be a valid Python identifier / directory name ----------------
if not re.match(r"^[a-z][a-z0-9_]*$", slug):
    print(
        f"ERROR: project_slug '{slug}' is not a valid identifier. "
        "Use only lowercase letters, digits, and underscores."
    )
    sys.exit(1)

if not re.match(r"^[a-z][a-z0-9_]*$", package):
    print(
        f"ERROR: package_name '{package}' is not a valid Python package name. "
        "Use only lowercase letters, digits, and underscores."
    )
    sys.exit(1)

# -- Python version should look like X.Y ------------------------------------
if not re.match(r"^\d+\.\d+$", python_version):
    print(
        f"ERROR: python_version '{python_version}' is not valid. "
        "Expected format: 3.12"
    )
    sys.exit(1)

# -- Temperature should be a float 0-2 --------------------------------------
try:
    temp = float(temperature)
    if not 0.0 <= temp <= 2.0:
        raise ValueError
except ValueError:
    print(
        f"ERROR: default_temperature '{temperature}' must be a number between 0 and 2."
    )
    sys.exit(1)
