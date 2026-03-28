"""LangGraph agent workflow for {{ cookiecutter.project_name }}."""

import asyncio
import os
from typing import Any, Dict, Optional

from langchain_core.messages import HumanMessage
{%- if cookiecutter.llm_provider == "google_gemini" %}
from langchain_google_genai import ChatGoogleGenerativeAI
{%- elif cookiecutter.llm_provider == "openai" %}
from langchain_openai import ChatOpenAI
{%- endif %}
from langgraph.graph import END, StateGraph

from src.{{ cookiecutter.package_name }}.config import CHUNK_SIZE, logger
from src.{{ cookiecutter.package_name }}.prompts import get_summary_prompt, get_chunk_merge_prompt
from src.{{ cookiecutter.package_name }}.states import AgentState
from src.{{ cookiecutter.package_name }}.tools import fetch_data, format_data_for_llm
from src.{{ cookiecutter.package_name }}.utils import get_api_key

# ── Constants ──────────────────────────────────────────────────────────
DEFAULT_ITEM_LIMIT = 50
SEPARATOR_THRESHOLD = 10

# Response keys
RESP_DATA = "data"
RESP_RAW_TEXT = "raw_text"
RESP_SUMMARY = "summary"
RESP_ERROR = "error"


# ── Helper: LLM singleton ───────────────────────────────────────────────
{%- if cookiecutter.llm_provider == "google_gemini" %}
_llm_instance: ChatGoogleGenerativeAI | None = None


def _get_llm() -> ChatGoogleGenerativeAI:
    """Return a cached LLM instance."""
    global _llm_instance
    if _llm_instance is None:
        api_key = get_api_key()
        _llm_instance = ChatGoogleGenerativeAI(
            model="{{ cookiecutter.llm_model }}",
            temperature={{ cookiecutter.default_temperature }},
            google_api_key=api_key,
        )
    return _llm_instance
{%- elif cookiecutter.llm_provider == "openai" %}
_llm_instance: ChatOpenAI | None = None


def _get_llm() -> ChatOpenAI:
    """Return a cached LLM instance."""
    global _llm_instance
    if _llm_instance is None:
        api_key = get_api_key()
        _llm_instance = ChatOpenAI(
            model="{{ cookiecutter.llm_model }}",
            temperature={{ cookiecutter.default_temperature }},
            openai_api_key=api_key,
        )
    return _llm_instance
{%- endif %}


# ── Graph nodes ──────────────────────────────────────────────────────────

def fetch_data_node(state: AgentState) -> AgentState:
    """Fetch data from external source.

    TODO: Implement your data fetching logic here.
    """
    try:
        try:
            limit = int(os.getenv("ITEM_LIMIT", str(DEFAULT_ITEM_LIMIT)))
        except ValueError:
            logger.warning("Invalid ITEM_LIMIT, using default %d", DEFAULT_ITEM_LIMIT)
            limit = DEFAULT_ITEM_LIMIT

        data = fetch_data(query=state.query, limit=limit)
        state.data = data
        logger.info("fetch_data_node: %d items loaded", len(data))
        return state

    except Exception as e:
        logger.error("fetch_data_node failed: %s", e)
        state.error = f"Failed to fetch data: {e}"
        return state


def format_data_node(state: AgentState) -> AgentState:
    """Format data for LLM processing."""
    try:
        state.raw_text = format_data_for_llm(state.data)
        # Drop raw data after formatting
        state.data = []
        logger.info(
            "format_data_node: formatted text length = %d chars",
            len(state.raw_text),
        )
        return state
    except Exception as e:
        logger.error("format_data_node failed: %s", e)
        state.error = f"Failed to format data: {e}"
        return state


def process_node(state: AgentState) -> AgentState:
    """Process data with LLM (summarize, analyze, etc.), with chunking for large inputs."""
    try:
        if not state.raw_text:
            state.error = "No content to process"
            return state

        llm = _get_llm()

        # ── Chunking: split long inputs into batches ─────────────────
        lines = state.raw_text.split("\n")
        blocks: list[str] = []
        current: list[str] = []
        for line in lines:
            current.append(line)
            if line.startswith("-" * SEPARATOR_THRESHOLD):
                blocks.append("\n".join(current))
                current = []
        if current:
            blocks.append("\n".join(current))

        if len(blocks) <= CHUNK_SIZE:
            # Single-shot processing
            prompt = get_summary_prompt(state.raw_text)
            response = llm.invoke([HumanMessage(content=prompt)])
            state.summary = response.content
        else:
            # Chunk → process each → merge
            logger.info(
                "Large input (%d blocks) – chunking into batches of %d",
                len(blocks),
                CHUNK_SIZE,
            )
            partial_summaries: list[str] = []
            for start in range(0, len(blocks), CHUNK_SIZE):
                chunk_text = "\n".join(blocks[start : start + CHUNK_SIZE])
                prompt = get_summary_prompt(chunk_text)
                resp = llm.invoke([HumanMessage(content=prompt)])
                partial_summaries.append(resp.content)

            merge_prompt = get_chunk_merge_prompt(partial_summaries)
            merged = llm.invoke([HumanMessage(content=merge_prompt)])
            state.summary = merged.content

        # Drop raw text after processing
        state.raw_text = None
        logger.info("process_node: summary generated (%d chars)", len(state.summary))
        return state

    except Exception as e:
        logger.error("process_node failed: %s", e)
        state.error = f"Failed to process data: {e}"
        return state


def error_handler_node(state: AgentState) -> AgentState:
    """Log the error and pass state through."""
    logger.error("Pipeline error: %s", state.error)
    return state


def should_process(state: AgentState) -> str:
    """Determine if processing should proceed."""
    if state.error or not state.data:
        return "error_handler"
    return "format_data"


# ── Graph construction ───────────────────────────────────────────────────

def create_agent_graph() -> StateGraph:
    """Create the LangGraph workflow."""
    graph = StateGraph(AgentState)

    graph.add_node("fetch_data", fetch_data_node)
    graph.add_node("format_data", format_data_node)
    graph.add_node("process", process_node)
    graph.add_node("error_handler", error_handler_node)

    graph.set_entry_point("fetch_data")
    graph.add_conditional_edges("fetch_data", should_process)
    graph.add_edge("format_data", "process")
    graph.add_edge("process", END)
    graph.add_edge("error_handler", END)

    return graph.compile()


# ── Async runner ─────────────────────────────────────────────────────────

async def run_agent(
    query: Optional[str] = None,
) -> dict:
    """Run the agent pipeline.

    Args:
        query: Optional input query or parameter

    Returns:
        Dictionary with data, raw text, summary, and error
    """
    agent = create_agent_graph()

    initial_state = AgentState(query=query or "")

    result = agent.invoke(initial_state)
    logger.info("Agent graph execution completed")

    response: Dict[str, Any] = _build_response(result)

    return response


def _build_response(result: Any) -> Dict[str, Any]:
    """Build response dictionary from agent result."""
    if isinstance(result, dict):
        return {
            RESP_DATA: result.get("data"),
            RESP_RAW_TEXT: result.get("raw_text"),
            RESP_SUMMARY: result.get("summary"),
            RESP_ERROR: result.get("error"),
        }
    else:
        return {
            RESP_DATA: result.data,
            RESP_RAW_TEXT: result.raw_text,
            RESP_SUMMARY: result.summary,
            RESP_ERROR: result.error,
        }
