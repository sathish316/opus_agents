from pydantic_ai.mcp import MCPServerStdio

from opus_agent_base.tools.mcp_server_config import MCPServerConfig
from opus_agent_base.tools.fastmcp_server_config import FastMCPServerConfig


class MCPServerRegistry:
    """
    Registry for MCP servers
    """

    def __init__(self):
        pass

    def register_server(self, mcp_server_config: MCPServerConfig):
        pass

    def get_filesystem_mcp_server(self) -> MCPServerConfig:
        return MCPServerConfig(
            "desktop_commander",
            "general.filesystem",
            "stdio",
            MCPServerStdio(
                command="npx",
                args=["-y", "@wonderwhy-er/desktop-commander"],
                tool_prefix="desktop_commander",
            )
        )

    def get_search_mcp_server(self) -> MCPServerConfig:
        return MCPServerConfig(
            "duckduckgo-mcp-server",
            "general.search",
            "stdio",
            MCPServerStdio(command="uvx", args=["duckduckgo-mcp-server"])
        )

    def get_code_execution_mcp_server(self) -> MCPServerConfig:
        return MCPServerConfig(
            "run_python",
            "general.code_execution",
            "stdio",
            MCPServerStdio(
                "deno",
                args=[
                    "run",
                    "-N",
                    "-R=node_modules",
                    "-W=node_modules",
                    "--node-modules-dir=auto",
                    "jsr:@pydantic/mcp-run-python",
                    "stdio",
                ],
            )
        )

    def get_datetime_mcp_server(self) -> MCPServerConfig:
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

