import os

from pydantic_ai.mcp import MCPServerStdio

from opus_agent_base.tools.mcp_server_config import MCPServerConfig
from opus_agent_base.tools.fastmcp_server_config import FastMCPServerConfig


class TodoMCPServerRegistry:
    """
    Registry for MCP servers
    """

    def __init__(self, config_manager):
        self.config_manager = config_manager
        pass

    def get_todoist_mcp_server(self) -> MCPServerConfig:
        # https://github.com/abhiz123/todoist-mcp-server
        return MCPServerConfig(
            "todoist",
            "productivity.todo.todoist",
            "stdio",
            MCPServerStdio(
                command="npx",
                args=["-y", "@abhiz123/todoist-mcp-server"],
                env={"TODOIST_API_TOKEN": os.getenv("TODOIST_API_TOKEN")},
                tool_prefix="todoist",
            )
        )

    def get_google_calendar_fastmcp_server(self) -> FastMCPServerConfig:
        # Google workspace is run as a stdio MCP server using https://github.com/taylorwilsdon/google_workspace_mcp
        return FastMCPServerConfig(
            "google_calendar",
            "productivity.calendar.google_calendar",
            {
                "transport": "stdio",
                "command": "uv",
                "args": [
                    "run",
                    "--directory",
                    f"{os.getenv('GOOGLE_WORKSPACE_MCP_PATH')}",
                    "python",
                    "main.py",
                    "--tools",
                    "calendar",
                ],
                "env": self._get_google_calendar_auth_env(),
                "cwd": f"{os.getenv('GOOGLE_WORKSPACE_MCP_PATH')}",
                "tool_prefix": "google_calendar",
            }
        )

    def _get_google_calendar_auth_env(self):
        auth_env = {
            "GOOGLE_OAUTH_CLIENT_ID": os.getenv("GOOGLE_OAUTH_CLIENT_ID"),
            "GOOGLE_OAUTH_CLIENT_SECRET": os.getenv("GOOGLE_OAUTH_CLIENT_SECRET"),
        }
        return auth_env

    def get_clockwise_fastmcp_server(self) -> FastMCPServerConfig:
        # MCP server (remote): https://mcp.getclockwise.com/mcp
        # https://support.getclockwise.com/article/238-connecting-to-clockwise-mcp
        return FastMCPServerConfig(
            "clockwise",
            "productivity.calendar.clockwise",
            {
                "transport": "streamable-http",
                "url": "https://mcp.getclockwise.com/mcp",
                "tool_prefix": "clockwise",
                "auth": "oauth",
            }
        )

    def get_slack_fastmcp_server(self) -> FastMCPServerConfig:
        # Slack is run as stdio local mcp server using https://github.com/korotovsky/slack-mcp-server
        return FastMCPServerConfig(
            "slack",
            "productivity.chat.slack",
            {
                "transport": "stdio",
                "command": "npx",
                "args": [
                    "-y",
                    "slack-mcp-server@latest",
                    "--transport",
                    "stdio"
                ],
                "env": self._get_slack_auth_env(),
                "tool_prefix": "slack",
            }
        )

    def _get_slack_auth_env(self):
        # setup slack tokens based on the auth method
        auth_method = self.config_manager.get_setting("mcp_config.productivity.chat.slack.auth_method")
        if auth_method == "xoxp":
            slack_auth_env = {
                "SLACK_MCP_XOXP_TOKEN": os.getenv("SLACK_MCP_XOXP_TOKEN"),
            }
        elif auth_method == "xoxc":
            slack_auth_env = {
                "SLACK_MCP_XOXC_TOKEN": os.getenv("SLACK_MCP_XOXC_TOKEN"),
                "SLACK_MCP_XOXD_TOKEN": os.getenv("SLACK_MCP_XOXD_TOKEN"),
            }
        return slack_auth_env


