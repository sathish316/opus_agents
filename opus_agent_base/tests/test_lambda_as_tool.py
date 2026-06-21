import pytest
import yaml
from pydantic_ai import Agent
from pydantic_ai.models.test import TestModel
from unittest.mock import MagicMock

from opus_agent_base.agent.agent_builder import AgentBuilder
from opus_agent_base.config.config_manager import ConfigManager
from opus_agent_base.tools.custom_tools_manager import CustomToolsManager
from opus_agent_base.tools.lambda_as_tool import LambdaAsTool, lambda_as_tool


@pytest.fixture
def test_config(tmp_path) -> ConfigManager:
    config_dir = tmp_path / ".opusai"
    config_dir.mkdir()
    config_file = config_dir / "opus-config.yml"
    config_file.write_text(
        yaml.dump(
            {
                "model_config": [
                    {
                        "provider": "ollama",
                        "model": "qwen3:1.7b-q8_0",
                        "enabled": True,
                        "is_local": True,
                        "base_url": "http://127.0.0.1:8080/v1",
                    }
                ],
                "mcp_config": {
                    "framework": {
                        "lambda": {
                            "enabled": True,
                        }
                    }
                },
                "debug": {"log_level": "ERROR"},
            }
        )
    )
    return ConfigManager(str(config_dir), "opus-config.yml")


def add_numbers(a: int, b: int) -> int:
    """Add two integers."""
    return a + b


def multiply_numbers(a: int, b: int) -> int:
    """Multiply two integers."""
    return a * b


def test_lambda_as_tool_requires_at_least_one_function():
    with pytest.raises(ValueError, match="at least one function"):
        LambdaAsTool("calculator", "framework.lambda")


def test_lambda_as_tool_factory_requires_at_least_one_function():
    with pytest.raises(ValueError, match="at least one function"):
        lambda_as_tool()


def test_lambda_as_tool_registers_functions():
    lambda_tool = LambdaAsTool(
        "calculator",
        "framework.lambda",
        add_numbers,
        multiply_numbers,
        always_enabled=True,
    )
    agent = Agent(model=TestModel(), tools=[])
    lambda_tool.initialize_tools(agent)

    tool_names = {tool.name for tool in agent._function_toolset.tools.values()}
    assert tool_names == {"add_numbers", "multiply_numbers"}


def test_lambda_as_tool_factory_uses_function_name():
    tool = lambda_as_tool(add_numbers, always_enabled=True)
    assert tool.name == "add_numbers"


def test_custom_tools_manager_respects_always_enabled(test_config):
    agent = Agent(model=TestModel(), tools=[])
    manager = CustomToolsManager(
        test_config,
        instructions_manager=None,
        model_manager=None,
        agent=agent,
    )
    lambda_tool = LambdaAsTool(
        "calculator",
        "framework.lambda.disabled",
        add_numbers,
        always_enabled=True,
    )

    manager.initialize_tools([lambda_tool])

    assert "add_numbers" in {tool.name for tool in agent._function_toolset.tools.values()}


def test_custom_tools_manager_uses_config_flag(test_config):
    agent = Agent(model=TestModel(), tools=[])
    manager = CustomToolsManager(
        test_config,
        instructions_manager=None,
        model_manager=None,
        agent=agent,
    )
    enabled_tool = LambdaAsTool("calculator", "framework.lambda", add_numbers)
    disabled_tool = LambdaAsTool(
        "disabled",
        "framework.lambda.disabled",
        multiply_numbers,
    )

    manager.initialize_tools([enabled_tool, disabled_tool])

    tool_names = {tool.name for tool in agent._function_toolset.tools.values()}
    assert tool_names == {"add_numbers"}


def test_agent_builder_lambda_tool_registers_functions(test_config, tmp_path):
    instructions_file = tmp_path / "instructions.md"
    instructions_file.write_text("You are a helpful calculator assistant.")

    builder = (
        AgentBuilder(test_config)
        .set_system_prompt_keys(["instructions"])
        .add_instructions_manager()
        .instruction("instructions", str(instructions_file))
    )
    builder.model_manager = MagicMock()
    builder.model_manager.get_model.return_value = TestModel()
    builder.lambda_tool(add_numbers, multiply_numbers, name="calculator")
    agent = builder.build_agent()

    tool_names = {tool.name for tool in agent._function_toolset.tools.values()}
    assert tool_names == {"add_numbers", "multiply_numbers"}


def test_lambda_as_tool_example_exports_tools():
    from opus_agent_base.examples.lambda_as_tool_example import (
        celsius_to_fahrenheit,
        get_lambda_tools,
        greet,
    )

    tools = get_lambda_tools()
    assert len(tools) == 2
    assert celsius_to_fahrenheit(0) == 32.0
    assert greet("Opus") == "Hello, Opus!"
