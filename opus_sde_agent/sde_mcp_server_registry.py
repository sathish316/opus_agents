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
    
    def get_github_fastmcp_server(self) -> FastMCPServerConfig:
        # Official GitHub MCP server - https://github.com/github/github-mcp-server/tree/main
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
                "env": self._get_github_auth_env(),
                "tool_prefix": "github",
            }
        )

    def get_docker_fastmcp_server(self) -> FastMCPServerConfig:
        # Docker MCP server - https://github.com/ckreiling/mcp-server-docker
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

    def get_k8s_fastmcp_server(self) -> FastMCPServerConfig:
        # k8s MCP server - https://github.com/strowk/mcp-k8s-go
        return FastMCPServerConfig(
            "k8s",
            "sde.container.k8s",
            {
                "command": "npx",
                "args": [
                    "@strowk/mcp-k8s"
                ],
                "tool_prefix": "k8s",
            }
        )

    def get_jira_fastmcp_server(self) -> FastMCPServerConfig:
        # Official Jira MCP server - https://mcp.atlassian.com/v1/sse
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

    def get_linear_fastmcp_server(self) -> FastMCPServerConfig:
        # Official Linear MCP server - https://mcp.linear.app/sse
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

