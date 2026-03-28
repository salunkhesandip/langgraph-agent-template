"""Agent state definitions."""

from typing import Optional
from pydantic import BaseModel


class AgentState(BaseModel):
    """State for the {{ cookiecutter.project_name }} agent.

    Customize this state class to hold all the data your agent needs
    as it flows through the graph nodes.
    """

    query: str = ""
    """Input query or parameter for the agent"""

    data: list[dict] = []
    """List of data items fetched from the external source"""

    raw_text: Optional[str] = None
    """Formatted text representation of the data for LLM processing"""

    summary: Optional[str] = None
    """Generated summary or output from LLM processing"""

    error: Optional[str] = None
    """Error message if any step fails"""
