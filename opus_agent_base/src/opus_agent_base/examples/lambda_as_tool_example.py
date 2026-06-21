"""
Example: creating tools from plain functions with LambdaAsTool.

Run with:
    python -m opus_agent_base.examples.lambda_as_tool_example
"""

from pathlib import Path

from opus_agent_base.agent.agent_builder import AgentBuilder
from opus_agent_base.config.config_manager import ConfigManager
from opus_agent_base.tools.lambda_as_tool import lambda_as_tool

EXAMPLE_DIR = Path(__file__).parent


def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert a temperature from Celsius to Fahrenheit."""
    return (celsius * 9 / 5) + 32


def greet(name: str) -> str:
    """Return a friendly greeting for the given name."""
    return f"Hello, {name}!"


def build_example_agent(config_manager: ConfigManager):
    """Build an agent with lambda-based tools."""
    return (
        AgentBuilder(config_manager)
        .name("lambda-tool-example")
        .set_system_prompt_keys(["lambda_tool_example_instructions"])
        .add_instructions_manager()
        .instruction(
            "lambda_tool_example_instructions",
            str(EXAMPLE_DIR / "lambda_tool_example_instructions.md"),
        )
        .add_model_manager()
        .lambda_tool(celsius_to_fahrenheit, greet, name="utility_tools")
        .build_agent()
    )


def get_lambda_tools():
    """Return standalone LambdaAsTool instances for direct registration."""
    return [
        lambda_as_tool(celsius_to_fahrenheit, name="temperature"),
        lambda_as_tool(greet, name="greeting"),
    ]


if __name__ == "__main__":
    config_manager = ConfigManager()
    agent = build_example_agent(config_manager)
    print("Example agent created with lambda tools:")
    for tool in agent._function_toolset.tools.values():
        print(f"  - {tool.name}: {tool.description}")
