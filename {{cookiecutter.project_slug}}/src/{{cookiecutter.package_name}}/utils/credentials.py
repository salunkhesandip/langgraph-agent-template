"""Credential utilities for the agent."""

import os


def get_api_key() -> str:
    """Get the LLM API key from environment.

    Returns:
        API key string

    Raises:
        ValueError: If API key is not set
    """
{%- if cookiecutter.llm_provider == "google_gemini" %}
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("Please set GOOGLE_API_KEY environment variable")
{%- elif cookiecutter.llm_provider == "openai" %}
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Please set OPENAI_API_KEY environment variable")
{%- endif %}
    return api_key
