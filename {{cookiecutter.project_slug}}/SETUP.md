# Setup Guide for {{ cookiecutter.project_name }}

This guide covers local setup, environment configuration, running the agent, and the first files you will likely customize.

## Prerequisites

- Python {{ cookiecutter.python_version }} or newer
- `pip` available in your shell
- `uv` installed

Install `uv` if needed:

### Windows PowerShell

```powershell
py -m pip install --upgrade pip
py -m pip install uv
```

### macOS or Linux

```bash
python3 -m pip install --upgrade pip
python3 -m pip install uv
```

## Install Dependencies

From the project root:

```bash
uv sync
```

If you want development tools such as `pytest`, `black`, `isort`, and `mypy`:

```bash
uv sync --extra dev
```

## Configure Environment Variables

Create a local `.env` file from `.env.example`.

### Windows PowerShell

```powershell
Copy-Item .env.example .env
```

### macOS or Linux

```bash
cp .env.example .env
```

Then edit `.env` and set the provider-specific API key:

{% if cookiecutter.llm_provider == "google_gemini" %}- `GOOGLE_API_KEY` for Google Gemini
{% elif cookiecutter.llm_provider == "openai" %}- `OPENAI_API_KEY` for OpenAI
{% endif %}

Optional:

- set `LOG_FILE=logs/agent.log` to also write logs to disk

## Run the Agent

Run the default workflow:

```bash
uv run python main.py
```

Run with a query:

```bash
uv run python main.py --query "your input here"
```

## Run Tests

```bash
uv run pytest src/{{ cookiecutter.package_name }}/tests -v
```

## First Customization Steps

This generated project is a scaffold. In most cases you should update these areas first:

1. `src/{{ cookiecutter.package_name }}/tools/data_source.py`
2. `src/{{ cookiecutter.package_name }}/states/state.py`
3. `src/{{ cookiecutter.package_name }}/prompts/prompts.py`
4. `src/{{ cookiecutter.package_name }}/agent/graph.py`
5. `src/{{ cookiecutter.package_name }}/config.py`

## Troubleshooting

### `uv` command not found

Reinstall `uv` with the Python interpreter used by your shell, then reopen the terminal.

### Missing API key error

Make sure your `.env` file exists and includes the correct provider-specific key.

### Dependency installation issues

Try refreshing the lock and reinstalling:

```bash
uv sync --refresh
```

### Test command cannot find the package

Check that you are running commands from the project root and that `src/{{ cookiecutter.package_name }}` matches the generated package name.