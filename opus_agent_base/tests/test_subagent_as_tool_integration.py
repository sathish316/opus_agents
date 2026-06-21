import pytest
from opus_agent_base.tools.subagent_as_tool import SubagentAsTool
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.test import TestModel


@pytest.mark.integration
class TestSubagentAsToolIntegration:
    @pytest.mark.asyncio
    async def test_parent_agent_calls_subagent_via_register_prompt_tool(self):
        """
        Example: a parent coordinator delegates open-ended work to a specialist
        subagent through a prompt-only tool registered by SubagentAsTool.
        """
        research_subagent = SubagentAsTool.from_instructions(
            name="research_assistant",
            instructions="Summarize research findings as concise bullet points.",
            model=TestModel(
                custom_output_text="- Finding A\n- Finding B\n- Finding C",
            ),
        )

        parent = Agent(
            model=TestModel(),
            instructions=(
                "You coordinate tasks. When the user asks for research, "
                "call the research assistant tool with a focused prompt."
            ),
        )
        research_subagent.register_prompt_tool(parent)

        result = await parent.run("Research the latest updates on SubagentAsTool.")

        assert "Finding A" in result.output
        assert "run_research_assistant" in result.output or "Finding B" in result.output

    def test_parent_can_register_multiple_named_subagent_tools(self):
        """Example: one parent exposes separate specialist subagents as tools."""
        summarizer = SubagentAsTool.from_instructions(
            name="summarizer",
            instructions="Summarize long content.",
            model=TestModel(custom_output_text="Short summary."),
        )
        classifier = SubagentAsTool.from_instructions(
            name="classifier",
            instructions="Classify incoming content.",
            model=TestModel(custom_output_text="bug_report"),
        )
        parent = Agent(
            model=TestModel(),
            instructions="Choose the right specialist for each request.",
        )

        summarizer.register_prompt_tool(parent)
        classifier.register_prompt_tool(parent)

        assert "run_summarizer" in parent._function_toolset.tools
        assert "run_classifier" in parent._function_toolset.tools

    @pytest.mark.asyncio
    async def test_custom_tool_pattern_with_context_prompt(self):
        """
        Example: parent tool prepares context (like meeting transcripts or notes)
        and forwards a formatted prompt to the subagent.
        """
        document = (
            "Alice: We should ship SubagentAsTool this week.\n"
            "Bob: Add unit and integration tests before merging."
        )

        summarizer = SubagentAsTool.from_instructions(
            name="meeting_summarizer",
            instructions="Summarize meeting transcripts.",
            model=TestModel(custom_output_text="Ship SubagentAsTool with tests."),
        )

        parent = Agent(
            model=TestModel(),
            instructions="You help users understand meeting transcripts.",
        )

        @parent.tool
        async def summarize_meeting(ctx: RunContext[None], meeting_id: str) -> str:
            """Summarize a meeting transcript by meeting id."""
            prompt = SubagentAsTool.format_prompt(
                "Meeting id: {meeting_id}\nTranscript:\n{transcript}\n"
                "Provide a one-line summary.",
                meeting_id=meeting_id,
                transcript=document,
            )
            return await summarizer.run(prompt)

        tool = parent._function_toolset.tools["summarize_meeting"]
        ctx = RunContext(
            deps=None,
            model=parent.model,
            usage=None,
            prompt=None,
            messages=[],
        )
        summary = await tool.function(ctx, meeting_id="M-42")

        assert summary == "Ship SubagentAsTool with tests."

    def test_sync_subagent_tool_registration(self):
        """Example: register a synchronous subagent tool for blocking workflows."""
        classifier = SubagentAsTool.from_instructions(
            name="priority_classifier",
            instructions="Classify task priority.",
            model=TestModel(custom_output_text="P2"),
        )

        parent = Agent(
            model=TestModel(),
            instructions="Classify incoming tasks.",
        )
        classifier.register_prompt_tool(parent, sync=True)

        tool_names = list(parent._function_toolset.tools.keys())
        assert "run_priority_classifier" in tool_names

        output = parent.run_sync("Classify: write docs for SubagentAsTool.")
        assert output.output
