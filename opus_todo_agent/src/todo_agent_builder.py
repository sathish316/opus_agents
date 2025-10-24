from opus_agent_base.tools.mcp_server_registry import MCPServerRegistry

from opus_agent_base.agent.agent_runner import AgentInstance
from opus_agent_base.tools.custom_tool import CustomTool
from opus_agent_base.tools.higher_order_tool import HigherOrderTool
from opus_todo_agent.custom_tools.meeting_transcript.loom_tools import LoomTools
from opus_todo_agent.custom_tools.meeting_transcript.zoom_tools import ZoomTools
from opus_todo_agent.custom_tools.notes.obsidian_tools import ObsidianTools
from opus_todo_agent.custom_tools.todo.todoist_tools import TodoistTools
from opus_todo_agent.higher_order_tools.calendar.clockwise_higher_order_tool import (
    ClockwiseHigherOrderTool,
)
from opus_todo_agent.higher_order_tools.calendar.google_calendar_higher_order_tool import (
    GoogleCalendarHigherOrderTool,
)
from opus_todo_agent.higher_order_tools.chat.slack_higher_order_tool import (
    SlackHigherOrderTool,
)
from opus_todo_agent.todo_mcp_server_registry import TodoMCPServerRegistry


class TodoAgentBuilder:
    def __init__(
        self, config_manager, instructions_manager, model_manager, mcp_manager
    ):
        self.name = "todo-agent"
        self.agent_instruction_keys = [
            "opus_agent_instruction",
            "todo_agent_instruction",
        ]
        self.config_manager = config_manager
        self.instructions_manager = instructions_manager
        self.model_manager = model_manager
        self.mcp_manager = mcp_manager
        self.custom_tools: list[CustomTool] = []
        self.higher_order_tools: list[HigherOrderTool] = []

    def build(self) -> AgentInstance:
        """Build the todo agent"""
        self._add_instructions()
        self._add_prompt_templates()
        self._add_mcp_servers()
        self._add_fastmcp_servers()
        self._add_custom_tools()
        self._add_higher_order_tools()

    def _add_instructions(self):
        self.instructions_manager.put_from_file(
            "opus_agent_instruction", "prompts/agent/OPUS_AGENT_INSTRUCTIONS.md"
        )
        self.instructions_manager.put_from_file(
            "todo_agent_instruction", "prompts/agent/TODO_AGENT_INSTRUCTIONS.md"
        )
        self.instructions_manager.put_from_file(
            "obsidian_notes_instructions",
            "prompts/tools/productivity/OBSIDIAN_NOTES_INSTRUCTIONS.md",
        )
        self.instructions_manager.put_from_file(
            "loom_meeting_assistant_instructions",
            "prompts/tools/productivity/LOOM_MEETING_ASSISTANT_INSTRUCTIONS.md",
        )
        self.instructions_manager.put_from_file(
            "zoom_meeting_assistant_instructions",
            "prompts/tools/productivity/ZOOM_MEETING_ASSISTANT_INSTRUCTIONS.md",
        )
        self.instructions_manager.put_from_file(
            "slack_assistant_instructions",
            "prompts/tools/productivity/SLACK_ASSISTANT_INSTRUCTIONS.md",
        )

    def _add_prompt_templates(self):
        self.instructions_manager.put_from_file(
            "slack_assistant_prompt_template",
            "prompt_templates/tools/productivity/SLACK_ASSISTANT_PROMPT_TEMPLATE.md",
        )
        self.instructions_manager.put_from_file(
            "loom_meeting_assistant_prompt_template",
            "prompt_templates/tools/productivity/LOOM_MEETING_ASSISTANT_PROMPT_TEMPLATE.md",
        )
        self.instructions_manager.put_from_file(
            "zoom_meeting_assistant_prompt_template",
            "prompt_templates/tools/productivity/ZOOM_MEETING_ASSISTANT_PROMPT_TEMPLATE.md",
        )
        self.instructions_manager.put_from_file(
            "obsidian_notes_prompt_template",
            "prompt_templates/tools/productivity/OBSIDIAN_NOTES_PROMPT_TEMPLATE.md",
        )

    def _add_mcp_servers(self):
        mcp_server_registry = MCPServerRegistry()
        todo_mcp_server_registry = TodoMCPServerRegistry(self.config_manager)
        mcp_servers_config = [
            mcp_server_registry.get_filesystem_mcp_server(),
            mcp_server_registry.get_search_mcp_server(),
            mcp_server_registry.get_code_execution_mcp_server(),
            todo_mcp_server_registry.get_todoist_mcp_server(),
        ]
        self.mcp_manager.add_servers(mcp_servers_config)

    def _add_fastmcp_servers(self):
        mcp_server_registry = MCPServerRegistry()
        todo_mcp_server_registry = TodoMCPServerRegistry(self.config_manager)
        fastmcp_servers_config = [
            mcp_server_registry.get_datetime_mcp_server(),
            todo_mcp_server_registry.get_google_calendar_fastmcp_server(),
            todo_mcp_server_registry.get_clockwise_fastmcp_server(),
            todo_mcp_server_registry.get_slack_fastmcp_server(),
        ]
        self.mcp_manager.add_fastmcp_servers(fastmcp_servers_config)

    def _add_custom_tools(self):
        self.custom_tools: list[CustomTool] = [
            TodoistTools(),
            ObsidianTools(
                config_manager=self.config_manager,
                instructions_manager=self.instructions_manager,
                model_manager=self.model_manager,
            ),
            LoomTools(
                config_manager=self.config_manager,
                instructions_manager=self.instructions_manager,
                model_manager=self.model_manager,
            ),
            ZoomTools(
                config_manager=self.config_manager,
                instructions_manager=self.instructions_manager,
                model_manager=self.model_manager,
            ),
        ]

    def _add_higher_order_tools(self):
        self.higher_order_tools: list[HigherOrderTool] = [
            GoogleCalendarHigherOrderTool(),
            ClockwiseHigherOrderTool(),
            SlackHigherOrderTool(
                config_manager=self.config_manager,
                instructions_manager=self.instructions_manager,
                model_manager=self.model_manager,
            ),
        ]
