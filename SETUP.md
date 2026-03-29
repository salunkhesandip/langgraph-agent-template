# LangGraph Agent Template Setup

This guide covers both:

- setting up the template itself so you can generate new projects
- setting up a generated project after Cookiecutter creates it

## Prerequisites

- Python 3.10+
- `pip` available in your shell
- `git` installed if you plan to clone the repository

## 1. Install Cookiecutter and uv

### Windows PowerShell

```powershell
py -m pip install --upgrade pip
py -m pip install cookiecutter uv
```

### macOS or Linux

```bash
python3 -m pip install --upgrade pip
python3 -m pip install cookiecutter uv
```

Verify the tools are available:

```bash
cookiecutter --version
uv --version
```

## 2. Generate a New Agent Project

From the parent directory of this template, run:

```bash
cookiecutter path/to/langgraph-agent-template
```

Example from this repository root:

```bash
cookiecutter langgraph-agent-template
```

Cookiecutter will prompt for project metadata such as the project name, package name, Python version, LLM provider, and model.

## 3. Enter the Generated Project

```bash
cd your_project_slug
```

The generated project already includes:

- `.env.example` for environment variables
- `pyproject.toml` for dependency management
- `main.py` as the local entry point
- `langgraph.json` for LangGraph tooling

## 4. Install Project Dependencies

Use `uv` from the generated project directory:

```bash
uv sync
```

If you want development dependencies too:

```bash
uv sync --extra dev
```

## 5. Configure Environment Variables

Create a local `.env` file from the example:

### Windows PowerShell

```powershell
Copy-Item .env.example .env
```

### macOS or Linux

```bash
cp .env.example .env
```

Then update `.env` with the correct API key for the provider you selected:

- `GOOGLE_API_KEY` for `google_gemini`
- `OPENAI_API_KEY` for `openai`

Optional:

- set `LOG_FILE=logs/agent.log` to enable file logging

## 6. Run the Generated Agent

Run the default flow:

```bash
uv run python main.py
```

Run with an explicit query:

```bash
uv run python main.py --query "your input here"
```

## 7. Run Tests

```bash
uv run pytest src/your_package_name/tests -v
```

## 8. Customize the Generated Project

Most generated projects need these edits before they are useful:

1. Replace the stub data fetcher in `src/<package>/tools/data_source.py`.
2. Adjust state fields in `src/<package>/states/state.py`.
3. Rewrite prompt templates in `src/<package>/prompts/prompts.py`.
4. Modify graph behavior in `src/<package>/agent/graph.py`.
5. Tune models, limits, retries, and timeouts in `src/<package>/config.py`.

## Troubleshooting

### `cookiecutter` or `uv` command not found

Install the packages again with the same Python interpreter you use in your shell, then restart the terminal.

### Missing API key error at startup

The generated agent validates provider-specific credentials. Make sure `.env` contains the right key for the provider chosen during project generation.

### Dependency install problems

Try:

```bash
uv sync --refresh
```

### Tests fail because the package path changed

Replace `your_package_name` in commands with the actual generated package name.