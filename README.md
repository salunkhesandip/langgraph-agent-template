# LangGraph Agent Template

A [Cookiecutter](https://cookiecutter.readthedocs.io/) template for creating LangGraph-based AI agents.

This template provides a production-ready structure for building AI agents with:

- **LangGraph** workflow (fetch → format → process pipeline)
- **LLM integration** (Google Gemini or OpenAI)
- **Async support** with parallel task execution
- **Chunking & merging** for large inputs
- **Caching & retry logic** for resilient API calls

## Usage

### Install Cookiecutter

**Recommended (Linux):**

```bash
# using a virtual environment:
python3 -m venv .venv
source .venv/bin/activate
uv pip install cookiecutter
```

**Other platforms:**

```bash
uv pip install cookiecutter
```

### Generate a New Agent Project

```bash
cookiecutter path/to/langgraph-agent-template
```

You'll be prompted for:

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `project_name` | Human-readable name for your agent | My AI Agent | "Document Analyzer", "Research Assistant" |
| `project_slug` | Directory name for your project (auto-generated, just press Enter to accept default) | my_ai_agent | document_analyzer, research_assistant |
| `package_name` | Python package name (auto-generated, just press Enter to accept default) | my_ai_agent | document_analyzer, research_assistant |
| `description` | One-line summary of what your agent does | A LangGraph AI agent | "Analyzes PDFs and extracts key insights" |
| `author_name` | Your name or organization | Your Name | "John Doe", "Acme Corp" |
| `python_version` | Minimum Python version required | 3.12 | 3.10, 3.11, 3.12 |
| `llm_provider` | Which LLM service to use | google_gemini | google_gemini, openai |
| `llm_model` | Model identifier for your LLM provider | models/gemini-2.5-flash | gpt-4 (openai), models/gemini-2.0-flash (google) |
| `default_temperature` | LLM creativity level (0=deterministic, 1=exploratory, default 0.7; just press Enter to accept default) | 0.7 | 0.3 (factual), 0.7 (balanced), 0.9 (creative) |

### After Generation

1. `cd your_project_slug`
2. `cp .env.example .env` and fill in your API keys
3. `uv sync` to install dependencies
4. Edit `src/<package>/tools/data_source.py` — replace the stub with your data source
5. Edit `src/<package>/prompts/prompts.py` — customize prompts for your domain
6. Edit `src/<package>/states/state.py` — add fields specific to your agent
7. `python main.py` to run

## Generated Project Structure

```
your_project_slug/
├── main.py                          # Entry point
├── examples.py                      # Usage examples
├── pyproject.toml                   # Dependencies & build config
├── langgraph.json                   # LangGraph configuration
├── .env.example                     # Environment variable template
├── .gitignore
├── README.md
└── src/
    └── your_package_name/
        ├── __init__.py
        ├── config.py                # Logging, constants, settings
        ├── agent/
        │   ├── __init__.py
        │   └── graph.py             # LangGraph workflow & nodes
        ├── prompts/
        │   ├── __init__.py
        │   └── prompts.py           # LLM prompt templates
        ├── states/
        │   ├── __init__.py
        │   └── state.py             # Pydantic state definitions
        ├── tools/
        │   ├── __init__.py
        │   └── data_source.py       # Data fetching (TODO: customize)
        ├── utils/
        │   ├── __init__.py
        │   ├── credentials.py       # API key management
        │   └── ...                  # Your custom utilities
        └── tests/
            ├── __init__.py
            └── test_agent.py        # Unit tests
```

## License

This template is provided as-is for creating AI agent projects.
