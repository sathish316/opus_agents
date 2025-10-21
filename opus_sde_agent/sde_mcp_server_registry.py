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
                },
                "tool_prefix": "github",
            }
        )

    def get_docker_mcp_server(self) -> MCPServerConfig:
        return MCPServerConfig(
            name="docker",
            config_key="sde.container.docker",
            type="stdio",
            mcp_server=MCPServerStdio(
                command="uvx",
                args=[
                    "mcp-server-docker"
                ],
                env={
                    "DOCKER_HOST": os.getenv("DOCKER_HOST")
                },
                tool_prefix="docker",
            )
        )

    def get_docker_fastmcp_server(self) -> FastMCPServerConfig:
        return FastMCPServerConfig(
            "docker",
            "sde.container.docker",
            {
                "command": "uvx",
                "args": [
                    "mcp-server-docker"
                ],
                "env": {
                    "DOCKER_HOST": os.getenv("DOCKER_HOST")
                },
                "tool_prefix": "docker",
            }
        )

    def get_jira_mcp_server(self) -> MCPServerConfig:
        pydantic_ai_mcp_oauth_support = False
        if not pydantic_ai_mcp_oauth_support:
            return None
        #FIXME: wrap selective jira tools
        return MCPServerConfig(
            name="jira",
            config_key="sde.project_management.jira",
            type="streamable-http",
            mcp_server=MCPServerSSE(
                url="https://mcp.atlassian.com/v1/sse"
            )
        )

    def get_jira_fastmcp_server(self) -> FastMCPServerConfig:
        return FastMCPServerConfig(
            "jira",
            "sde.project_management.jira",
            {
                "type": "http",
                "url": "https://mcp.atlassian.com/v1/sse",
                "transport": "streamable-http",
                "tool_prefix": "jira",
                "auth": "oauth",
            }
        )

    def get_linear_mcp_server(self) -> MCPServerConfig:
        pydantic_ai_mcp_oauth_support = False
        if not pydantic_ai_mcp_oauth_support:
            return None
        #FIXME: wrap selective linear tools
        return MCPServerConfig(
            name="linear",
            config_key="sde.project_management.linear",
            type="stdio",
            mcp_server=MCPServerStdio(
                command="npx",
                args=["-y", "mcp-remote", "https://mcp.linear.app/sse"],
                tool_prefix="linear",
            )
        )

    def get_linear_fastmcp_server(self) -> FastMCPServerConfig:
        return FastMCPServerConfig(
            "linear",
            "sde.project_management.linear",
            {
                "command": "npx",
                "args": ["-y", "mcp-remote", "https://mcp.linear.app/sse"],
                "tool_prefix": "linear",
            }
        )

    def _get_github_auth_env(self):
        auth_env = {
            "GITHUB_PERSONAL_ACCESS_TOKEN": os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN"),
        }
        return auth_env

