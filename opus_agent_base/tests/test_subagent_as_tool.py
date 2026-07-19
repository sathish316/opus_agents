from unittest.mock import AsyncMock, MagicMock

import pytest
from opus_agent_base.tools.subagent_as_tool import SubagentAsTool
from pydantic_ai import Agent
from pydantic_ai.models.test import TestModel


class TestSubagentAsToolUnit:
    def test_format_prompt_example(self):
        """Example: build a subagent prompt from retrieved context."""
        prompt = SubagentAsTool.format_prompt(
            "Question: {question}\nNotes:\n{context}",
            question="What should we ship this week?",
            context="- SubagentAsTool wrapper\n- Unit tests",
        )
        assert "What should we ship this week?" in prompt
        assert "SubagentAsTool wrapper" in prompt

    def test_from_instructions_creates_named_wrapper(self):
        """Example: create a specialist subagent from instructions + test model."""
        tool = SubagentAsTool.from_instructions(
            name="release_notes_writer",
            instructions="Write concise release notes.",
            model=TestModel(custom_output_text="Added SubagentAsTool."),
        )

        assert tool.name == "release_notes_writer"
        assert tool.tool_name == "run_release_notes_writer"
        assert tool.subagent is not None

    def test_from_instructions_allows_explicit_tool_name(self):
        """Example: expose a short tool name for the parent agent."""
        tool = SubagentAsTool.from_instructions(
            name="release_notes_writer",
            tool_name="draft_release_notes",
            instructions="Write concise release notes.",
            model=TestModel(custom_output_text="Added SubagentAsTool."),
        )

        assert tool.tool_name == "draft_release_notes"

    def test_run_sync_returns_subagent_output(self):
        response = MagicMock()
        response.output = "subagent answer"
        subagent = MagicMock()
        subagent.run_sync.return_value = response

        tool = SubagentAsTool(subagent, name="test_subagent")
        result = tool.run_sync("hello")

        assert result == "subagent answer"
        subagent.run_sync.assert_called_once_with("hello")

    @pytest.mark.asyncio
    async def test_run_returns_subagent_output(self):
        response = MagicMock()
        response.output = "async answer"
        subagent = MagicMock()
        subagent.run = AsyncMock(return_value=response)

        tool = SubagentAsTool(subagent, name="test_subagent")
        result = await tool.run("hello")

        assert result == "async answer"
        subagent.run.assert_awaited_once_with("hello")

    def test_from_managers_uses_local_model_when_configured(self, monkeypatch):
        created_agents = []

        class FakeAgent:
            def __init__(self, **kwargs):
                created_agents.append(kwargs)

        monkeypatch.setattr(
            "opus_agent_base.tools.subagent_as_tool.Agent",
            FakeAgent,
        )

        config_manager = MagicMock()
        config_manager.get_setting.return_value = True
        instructions_manager = MagicMock()
        instructions_manager.get.return_value = "You are a helper."
        model_manager = MagicMock()
        model_manager.get_local_model.return_value = "local-model"
        model_manager.get_model.return_value = "cloud-model"

        tool = SubagentAsTool.from_managers(
            name="helper",
            instructions_key="helper_instructions",
            config_manager=config_manager,
            instructions_manager=instructions_manager,
            model_manager=model_manager,
            use_local_model_config_key="helper.use_local_model",
        )

        assert tool.name == "helper"
        assert created_agents == [
            {
                "instructions": "You are a helper.",
                "model": "local-model",
            }
        ]
        model_manager.get_local_model.assert_called_once_with()
        model_manager.get_model.assert_not_called()
        instructions_manager.get.assert_called_once_with("helper_instructions")

    def test_register_prompt_tool_adds_tool_to_parent_agent(self):
        subagent = Agent(
            model=TestModel(custom_output_text="done"),
            instructions="You are a helper.",
        )
        parent = Agent(
            model=TestModel(),
            instructions="You delegate to helpers.",
        )

        SubagentAsTool(subagent, name="helper").register_prompt_tool(parent)

        assert "run_helper" in parent._function_toolset.tools

    def test_register_prompt_tool_allows_tool_name_override(self):
        subagent = Agent(
            model=TestModel(custom_output_text="done"),
            instructions="You are a helper.",
        )
        parent = Agent(
            model=TestModel(),
            instructions="You delegate to helpers.",
        )

        SubagentAsTool(subagent, name="helper").register_prompt_tool(
            parent,
            tool_name="ask_helper",
        )

        assert "ask_helper" in parent._function_toolset.tools
