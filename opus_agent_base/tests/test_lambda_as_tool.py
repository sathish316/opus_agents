from unittest.mock import MagicMock

import pytest
from opus_agent_base.agent.agent_builder import AgentBuilder
from opus_agent_base.tools.lambda_as_tool import lambda_as_tool
from pydantic_ai.models.test import TestModel


def test_lambda_as_tool_registers_lambda_name_description_and_schema():
    model = TestModel()
    agent = AgentBuilder(MagicMock())
    agent.system_prompt_keys = []
    agent.instructions_manager = MagicMock()
    agent.model_manager = MagicMock()
    agent.model_manager.get_model.return_value = model

    built_agent = agent.lambda_tool(
        lambda name: f"Hello, {name}!",
        name="greet",
        description="Return a friendly greeting for a name.",
    ).build_agent()
    built_agent.run_sync("Greet someone.")

    tool = model.last_model_request_parameters.function_tools[0]
    assert tool.name == "greet"
    assert tool.description == "Return a friendly greeting for a name."
    assert tool.parameters_json_schema["required"] == ["name"]
    agent.config_manager.get_setting.assert_not_called()


def test_lambda_as_tool_uses_named_function_metadata():
    def add(a: int, b: int) -> int:
        """Add two integers."""
        return a + b

    tool = lambda_as_tool(add)

    assert tool.name == "add"
    assert tool.description == "Add two integers."


def test_lambda_as_tool_requires_lambda_metadata():
    with pytest.raises(ValueError, match="name is required"):
        lambda_as_tool(lambda value: value)

    with pytest.raises(ValueError, match="description is required"):
        lambda_as_tool(lambda value: value, name="identity")
