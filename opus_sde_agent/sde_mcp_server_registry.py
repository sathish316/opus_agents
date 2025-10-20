import os

from pydantic_ai.mcp import MCPServerSSE, MCPServerStdio, MCPServerHTTP

from opus_agent_base.tools.mcp_server_config import MCPServerConfig
from opus_agent_base.tools.fastmcp_server_config import FastMCPServerConfig


class SDEMCPServerRegistry:
    """
    Registry for SDE MCP servers
    """

    def __init__(self, config_manager):
        self.config_manager = config_manager
    
    def get_github_mcp_server(self) -> MCPServerConfig:
        return MCPServerConfig(
            name="github",
            config_key="sde.git.github",
            type="stdio",
            mcp_server=MCPServerStdio(
                command="docker",
                args=[
                    "run",
                    "-i",
                    "--rm",
                    "-e",
                    "GITHUB_PERSONAL_ACCESS_TOKEN",
                    "ghcr.io/github/github-mcp-server"
                ],
                env=self._get_github_auth_env(),
                tool_prefix="github",
            )
        )

    def get_github_fastmcp_server(self) -> FastMCPServerConfig:
        return FastMCPServerConfig(
            "github",
            "sde.git.github",
            {
                "command": "docker",
                "args": [
                    "run",
                    "-i",
                    "--rm",
                    "-e",
                    "GITHUB_PERSONAL_ACCESS_TOKEN",
                    "ghcr.io/github/github-mcp-server"
                ],
                "env": {
                    "GITHUB_PERSONAL_ACCESS_TOKEN": os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
                }
            }
        )

    def _get_github_auth_env(self):
        auth_env = {
            "GITHUB_PERSONAL_ACCESS_TOKEN": os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN"),
        }
        return auth_env

