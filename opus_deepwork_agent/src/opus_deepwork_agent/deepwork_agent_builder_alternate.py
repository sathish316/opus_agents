from opus_agent_base.agent.agent_builder import AgentBuilder
from opus_agent_base.tools.mcp_server_registry import MCPServerRegistry

from opus_deepwork_agent.deepwork_mcp_server_registry import DeepWorkMCPServerRegistry


class DeepWorkAgentBuilderAlternate(AgentBuilder):
    """Builder for DeepWork Agent"""

    def __init__(
        self, config_manager, instructions_manager, model_manager, mcp_manager
    ):
        super().__init__(config_manager)
        self.name = "deepwork-agent"
        self.system_prompt_keys = [
            "opus_agent_instruction",
            "deepwork_agent_instruction",
        ]

    def build(self) -> AgentBuilder:
        """Build the DeepWork agent with all components"""
        self._add_instructions()
        self._add_mcp_servers()
        self._add_custom_tools()
        self._add_higher_order_tools()
        return self

    def _add_instructions(self):
        """Load agent instructions from markdown files"""
        # System prompt
        self.instructions_manager.put_from_file(
            "opus_agent_instruction", "prompts/agent/OPUS_AGENT_INSTRUCTIONS.md"
        )
        self.instructions_manager.put_from_file(
            "deepwork_agent_instruction", "prompts/agent/DEEPWORK_AGENT_INSTRUCTIONS.md"
        )

    def _add_mcp_servers(self):
        """Add FastMCP servers (Clockwise for calendar)"""
        mcp_server_registry = MCPServerRegistry()
        deepwork_mcp_server_registry = DeepWorkMCPServerRegistry(self.config_manager)
        mcp_servers_config = [
            mcp_server_registry.get_datetime_mcp_server(),
            deepwork_mcp_server_registry.get_clockwise_fastmcp_server(),
        ]
        self.mcp_manager.add_fastmcp_servers(mcp_servers_config)

    def _add_custom_tools(self):
        """Add custom tools (Todoist for task management)"""
        self.custom_tools: list[CustomTool] = [
            TodoistTools(),
        ]

    def _add_higher_order_tools(self):
        """Add higher order tools (Clockwise for smart scheduling)"""
        self.higher_order_tools: list[HigherOrderTool] = [
            ClockwiseHigherOrderTool(),
        ]
