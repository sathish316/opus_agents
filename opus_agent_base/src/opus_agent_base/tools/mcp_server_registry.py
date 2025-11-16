from opus_agent_base.tools.fastmcp_server_config import FastMCPServerConfig


class MCPServerRegistry:
    """
    Registry for MCP servers
    """
    def get_filesystem_mcp_server(self) -> FastMCPServerConfig:
        return FastMCPServerConfig(
            "desktop_commander",
            "general.filesystem",
            {
                "command": "npx",
                "args": [
                    "-y",
                    "@wonderwhy-er/desktop-commander@latest"
                ]
            })

    def get_search_mcp_server(self) -> FastMCPServerConfig:
        return FastMCPServerConfig(
            "duckduckgo-mcp-server",
            "general.search",
            {
                "command": "uvx",
                "args": ["duckduckgo-mcp-server"]
            })

    def get_python_code_execution_mcp_server(self) -> FastMCPServerConfig:
        return FastMCPServerConfig(
            "run_python",
            "general.code_execution",
            {
                "command": "uvx",
                "args": ["-y", "mcp-run-python"]
            })

    def get_datetime_mcp_server(self) -> FastMCPServerConfig:
        return FastMCPServerConfig(
            "mcp-datetime",
            "general.datetime",
            {
                "transport": "stdio",
                "command": "uvx",
                "args": ["mcp-datetime"],
                "tool_prefix": "mcp-datetime",
            }
        )

