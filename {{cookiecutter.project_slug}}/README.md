# {{ cookiecutter.project_name }}

{{ cookiecutter.description }}

## Features

- **LangGraph Workflow**: Structured agent graph with fetch → format → process pipeline
- **LLM Integration**: {% if cookiecutter.llm_provider == "google_gemini" %}Google Gemini{% elif cookiecutter.llm_provider == "openai" %}OpenAI{% endif %} for intelligent processing
- **Async Support**: Non-blocking async operations for better performance
- **Chunking**: Automatic chunking and merging for large inputs
- **Caching**: In-memory cache to avoid redundant API calls
- **Retry Logic**: Exponential back-off for resilient API calls

For installation, environment configuration, and run commands, see [SETUP.md](SETUP.md).

## Project Structure

```
src/{{ cookiecutter.package_name }}/
├── agent/           # Main agent graph and workflow
├── tools/           # Data source client and utilities
├── states/          # State definitions for the agent
├── prompts/         # LLM prompt templates
├── utils/           # Helper utilities (credentials)
└── tests/           # Unit tests
```

## Customization Guide

This project was generated from the **langgraph-agent-template**. Here's how to customize it for your use case:

### 1. Data Source (`tools/data_source.py`)
Replace the `fetch_data()` stub with your actual data fetching logic (API calls, database queries, web scraping, etc.).

### 2. State (`states/state.py`)
Add or modify fields in `AgentState` to hold the data your agent needs.

### 3. Prompts (`prompts/prompts.py`)
Customize `SYSTEM_PROMPT` and `SUMMARY_PROMPT_TEMPLATE` for your specific domain.

### 4. Graph (`agent/graph.py`)
Add new nodes, modify the workflow, or add conditional edges to the LangGraph pipeline.

### 5. Configuration (`config.py`)
Adjust limits, timeouts, retry settings, and other constants.
