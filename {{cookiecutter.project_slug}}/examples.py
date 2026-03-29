"""{{ cookiecutter.project_name }} examples."""

from dotenv import load_dotenv

load_dotenv()

from src.{{ cookiecutter.package_name }}.agent import create_agent_graph
from src.{{ cookiecutter.package_name }}.states import AgentState


def example_basic_usage():
    """Basic example of using the agent."""
    # Create the agent graph
    agent = create_agent_graph()

    # Create initial state (TypedDict — use a plain dict)
    initial_state: AgentState = {"query": "Your input here"}

    # Run the agent
    result = agent.invoke(initial_state)

    # Print results
    if result.get("error"):
        print(f"Error: {result['error']}")
    else:
        print("\nResult:")
        print(result.get("summary"))


if __name__ == "__main__":
    print("Example: Basic agent usage")
    print("-" * 50)
    # Uncomment to run (requires .env with API key):
    # example_basic_usage()
