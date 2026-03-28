"""{{ cookiecutter.project_name }} examples."""

import os
from src.{{ cookiecutter.package_name }}.agent import create_agent_graph
from src.{{ cookiecutter.package_name }}.states import AgentState


def example_basic_usage():
    """Basic example of using the agent."""
    # Set your API keys as environment variables
{%- if cookiecutter.llm_provider == "google_gemini" %}
    os.environ["GOOGLE_API_KEY"] = "your_google_api_key"
{%- elif cookiecutter.llm_provider == "openai" %}
    os.environ["OPENAI_API_KEY"] = "your_openai_api_key"
{%- endif %}

    # Create the agent graph
    agent = create_agent_graph()

    # Create initial state
    initial_state = AgentState(query="Your input here")

    # Run the agent
    result = agent.invoke(initial_state)

    # Print results
    if result.error:
        print(f"Error: {result.error}")
    else:
        print("\nResult:")
        print(result.summary)


if __name__ == "__main__":
    print("Example: Basic agent usage")
    print("-" * 50)
    # example_basic_usage()
    print("\nNote: Uncomment examples and add your credentials to run")
