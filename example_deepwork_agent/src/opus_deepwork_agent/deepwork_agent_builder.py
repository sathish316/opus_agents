from opus_agent_base.agent.agent_builder import AgentBuilder
from opus_agent_base.config.config_manager import ConfigManager
from opus_agent_base.tools.mcp_server_registry import MCPServerRegistry

from opus_deepwork_agent.deepwork_mcp_server_registry import DeepWorkMCPServerRegistry
from opus_deepwork_agent.meta_tools.hackernews_meta_tool import HackerNewsMetaTool


class DeepWorkAgentBuilder(AgentBuilder):
    """Builder for DeepWork Agent"""

    def __init__(self, config_manager: ConfigManager):
        super().__init__(config_manager)

    def build(self) -> AgentBuilder:
        """Build the DeepWork agent with all components"""
        self._add_mcp_servers_config()
        self._add_meta_tools()
        return self

    def _add_mcp_servers_config(self):
        """Add FastMCP servers (Clockwise for calendar)"""
        mcp_server_registry = MCPServerRegistry()
        deepwork_mcp_server_registry = DeepWorkMCPServerRegistry(self.config_manager)
        mcp_servers_config = [
            mcp_server_registry.get_datetime_mcp_server(),
            deepwork_mcp_server_registry.get_clockwise_fastmcp_server(),
        ]
        self.add_mcp_servers_config(mcp_servers_config)

    def _add_meta_tools(self):
        """Add meta tools (HackerNews API)"""
        self.meta_tools = [
            HackerNewsMetaTool(
                config_manager=self.config_manager,
            ),
        ]
