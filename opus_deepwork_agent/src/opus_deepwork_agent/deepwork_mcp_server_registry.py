from opus_agent_base.tools.fastmcp_server_config import FastMCPServerConfig


class DeepWorkMCPServerRegistry:
    """Registry for DeepWork agent MCP servers"""

    def __init__(self, config_manager):
        self.config_manager = config_manager

    def get_clockwise_fastmcp_server(self) -> FastMCPServerConfig:
        """
        Configure Clockwise MCP server
        """
        return FastMCPServerConfig(
            "clockwise",
            "deepwork.calendar.clockwise",
            {
                "transport": "streamable-http",
                "url": "https://mcp.getclockwise.com/mcp",
                "tool_prefix": "clockwise",
                "auth": "oauth",
            }
        )