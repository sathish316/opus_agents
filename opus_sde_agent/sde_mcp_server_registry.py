from math import e
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
            # using streamable-http
            {
                "transport": "streamable-http",
                "url": "https://api.githubcopilot.com/mcp/",
                "tool_prefix": "github",
                "auth": "oauth",
                "headers": {
                    "Authorization": f"Bearer {os.getenv('GITHUB_PERSONAL_ACCESS_TOKEN')}"
                },
            },
            # using docker
            # {
            #     "command": "docker",
            #     "args": [
            #         "run",
            #         "-i",
            #         "--rm",
            #         "-e",
            #         "GITHUB_PERSONAL_ACCESS_TOKEN",
            #         "ghcr.io/github/github-mcp-server"
            #     ],
            #     "env": self._get_github_auth_env(),
            #     "tool_prefix": "github",
            # }
        )

    def get_docker_fastmcp_server(self) -> FastMCPServerConfig:
        # Docker MCP server - https://github.com/ckreiling/mcp-server-docker
        return FastMCPServerConfig(
            "docker",
            "sde.container.docker",
            {
                "command": "uvx",
                "args": ["mcp-server-docker"],
                "env": {"DOCKER_HOST": os.getenv("DOCKER_HOST")},
                "tool_prefix": "docker",
            },
        )

    def get_k8s_fastmcp_server(self) -> FastMCPServerConfig:
        # k8s MCP server - https://github.com/strowk/mcp-k8s-go
        return FastMCPServerConfig(
            "k8s",
            "sde.container.k8s",
            {
                "command": "npx",
                "args": ["@strowk/mcp-k8s"],
                "tool_prefix": "k8s",
            },
        )

    def get_jira_fastmcp_server(self) -> FastMCPServerConfig:
        # Official Jira MCP server - https://mcp.atlassian.com/v1/sse
        return FastMCPServerConfig(
            "jira",
            "sde.project_management.jira",
            # {
            #     "url": "https://mcp.atlassian.com/v1/sse",
            #     "transport": "streamable-http",
            #     "tool_prefix": "jira",
            #     "auth": "oauth",
            # }
            {
                "command": "npx",
                "args": ["-y", "mcp-remote", "https://mcp.atlassian.com/v1/sse"],
                "tool_prefix": "jira",
            },
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
            },
        )

    def get_prometheus_fastmcp_server(self) -> FastMCPServerConfig:
        # Prometheus MCP server - https://github.com/pab1it0/prometheus-mcp-server
        enabled = False
        if not enabled:
            return None
        return FastMCPServerConfig(
            "prometheus",
            "sde.monitoring.prometheus",
            {
                "command": "uvx",
                "args": ["-y", "@pab1it0/prometheus-mcp-server"],
                "tool_prefix": "prometheus",
            },
        )

    def get_loki_fastmcp_server(self) -> FastMCPServerConfig:
        # Loki MCP server - https://github.com/grafana/loki-mcp
        enabled = False
        if not enabled:
            return None
        return FastMCPServerConfig(
            "loki",
            "sde.monitoring.loki",
            {
                "command": "docker",
                "args": [
                    "run",
                    "--rm",
                    "-i",
                    "-e",
                    "LOKI_URL=http://host.docker.internal:3100",
                    "-e",
                    "LOKI_ORG_ID=your-default-org-id",
                    "-e",
                    "LOKI_USERNAME=your-username",
                    "-e",
                    "LOKI_PASSWORD=your-password",
                    "-e",
                    "LOKI_TOKEN=your-bearer-token",
                    "loki-mcp-server:latest",
                ],
                "tool_prefix": "loki",
            },
        )

    def get_grafana_fastmcp_server(self) -> FastMCPServerConfig:
        # Grafana MCP server - https://github.com/grafana/mcp-grafana
        enabled = False
        if not enabled:
            return None
        return FastMCPServerConfig(
            "grafana",
            "sde.monitoring.grafana",
            {
                "command": "docker",
                "args": [
                    "run",
                    "--rm",
                    "-i",
                    "-e",
                    "GRAFANA_URL",
                    "-e",
                    "GRAFANA_SERVICE_ACCOUNT_TOKEN",
                    "mcp/grafana",
                    "-t",
                    "stdio",
                ],
                "env": {
                    "GRAFANA_URL": "http://localhost:3000",  # Or "https://myinstance.grafana.net" for Grafana Cloud
                    "GRAFANA_SERVICE_ACCOUNT_TOKEN": "<your service account token>",
                    # If using username/password authentication
                    "GRAFANA_USERNAME": "<your username>",
                    "GRAFANA_PASSWORD": "<your password>",
                    # Optional: specify organization ID for multi-org support
                    "GRAFANA_ORG_ID": "1",
                },
                "tool_prefix": "grafana",
            },
        )

    def get_grafana_tempo_fastmcp_server(self) -> FastMCPServerConfig:
        enabled = False
        if not enabled:
            return None
        # Grafana Tempo MCP server - https://github.com/grafana/tempo-mcp-server
        return None

    def _get_github_auth_env(self):
        auth_env = {
            "GITHUB_PERSONAL_ACCESS_TOKEN": os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN"),
        }
        return auth_env
