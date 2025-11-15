from opus_agent_base.agent.agent_builder import AgentBuilder
from opus_agent_base.config.config_manager import ConfigManager
from opus_agent_base.tools.mcp_server_registry import MCPServerRegistry

from opus_deepwork_agent.deepwork_mcp_server_registry import DeepWorkMCPServerRegistry


class DeepWorkAgentBuilder(AgentBuilder):
    """Builder for DeepWork Agent"""

    def __init__(self, config_manager: ConfigManager):
        super().__init__(config_manager)

    def build(self) -> AgentBuilder:
        """Build the DeepWork agent with all components"""
        self._add_mcp_servers()
        return self

    def _add_mcp_servers(self):
        """Add FastMCP servers (Clockwise for calendar)"""
        mcp_server_registry = MCPServerRegistry()
        deepwork_mcp_server_registry = DeepWorkMCPServerRegistry(self.config_manager)
        mcp_servers_config = [
            mcp_server_registry.get_datetime_mcp_server(),
            deepwork_mcp_server_registry.get_clockwise_fastmcp_server(),
        ]
        self.mcp_manager.add_fastmcp_servers(mcp_servers_config)
