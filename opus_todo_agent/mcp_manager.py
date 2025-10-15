import logging
import os

from fastmcp import Client
from pydantic_ai.mcp import MCPServerStdio
from singleton_decorator import singleton

logger = logging.getLogger(__name__)


@singleton
class MCPManager:
    """
    Manager for MCP servers
    """

    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.servers = []
        self.initialize_config()
        self.initialize_mcp_servers()
        self.fastmcp_client_instance = None
        self.fastmcp_client_instance_initialized = False

    async def async_init(self):
        self.fastmcp_client = await self.initialize_higher_order_mcp_servers()
        return self

    def initialize_config(self):
        self.config = {
            "filesystem": {"enabled": True},
            "search": {"enabled": True},
            "code_execution": {"enabled": True},
            "todo": {
                "todoist": {"enabled": True},
            },
            "calendar": {
                "google_calendar": {"enabled": False, "higher_order_tools_enabled": False},
                "clockwise": {"enabled": False, "higher_order_tools_enabled": True},
            },
            "chat": {
                "slack": {"enabled": True, "auth_method": "xoxp", "higher_order_tools_enabled": True},
            },
            "notes": {
                "obsidian": {"enabled": False},
            },
            "meeting_transcript": {
                "loom": {"enabled": False},
                "zoom": {"enabled": False},
            }
        }

    def _is_mcp_enabled(self, domain, category, mcp):
        """
        Check if the MCP server is enabled in a given domain and category.
        Examples of domain are: general, productivity
        Examples of category are: todo, calendar etc.
        Examples of mcp are: todoist, google_calendar, slack etc.
        """
        return self.config_manager.get_setting(f"mcp_config.{domain}.{category}.{mcp}.enabled")

    def _is_mcp_category_enabled(self, domain, category):
        """
        Check if MCP server is enabled in a given domain and category.
        The choice of MCP server is not customizable.
        Examples of domain are: general, productivity
        Examples of category are: todo, calendar etc.
        """
        return self.config_manager.get_setting(f"mcp_config.{domain}.{category}.enabled")

    def initialize_mcp_servers(self):
        self.init_filesystem_servers()
        self.init_search_servers()
        self.init_code_execution_servers()
        self.init_todo_servers()
        self.init_calendar_servers()
        self.init_chat_servers()

    async def initialize_higher_order_mcp_servers(self):
        self.config["mcpServers"] = {}
        # Add a dummy MCP server to ensure there are always multiple servers
        self.config["mcpServers"]["mcp-datetime"] = {
            "transport": "stdio",
            "command": "uvx",
            "args": ["mcp-datetime"],
            "tool_prefix": "mcp-datetime",
        }
        if self._is_mcp_enabled("productivity", "calendar", "google_calendar"):
            # Google calendar is run as stdio local mcp server using https://github.com/taylorwilsdon/google_workspace_mcp
            self.config["mcpServers"]["google_calendar"] = {
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
        if self._is_mcp_enabled("productivity", "calendar", "clockwise"):
            # Clockwise is run as Remote mcp server using https://mcp.getclockwise.com/mcp
            self.config["mcpServers"]["clockwise"] = {
                "transport": "streamable-http",
                "url": "https://mcp.getclockwise.com/mcp",
                "tool_prefix": "clockwise",
                "auth": "oauth",
            }
        if self._is_mcp_enabled("productivity", "chat", "slack"):
            # Slack is run as stdio local mcp server using https://github.com/korotovsky/slack-mcp-server
            self.config["mcpServers"]["slack"] = {
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
        logger.info("Higher order tools and FastMCP config initialized")
        async def fastmcp_client_context(func):
            if self.fastmcp_client_instance is None:
                self.fastmcp_client_instance = Client(self.config)
            async with self.fastmcp_client_instance as client:
                if not self.fastmcp_client_instance_initialized:
                    await client.ping()
                    self.fastmcp_client_instance_initialized = True
                logger.debug("Calling function with FastMCP client context")
                return await func(client)

        self.fastmcp_client_context = fastmcp_client_context
        await self.inspect_fastmcp_client_tools()
        logger.info("Higher order tools and FastMCP client initialized")

    def init_filesystem_servers(self):
        if self._is_mcp_category_enabled("general", "filesystem"):
            # MCP server - filesystem server and desktop commander for file system search and diffing capabilities
            toolset_name = "desktop_commander"
            desktop_commander = MCPServerStdio(
                command="npx",
                args=["-y", "@wonderwhy-er/desktop-commander"],
                tool_prefix="desktop_commander",
            )
            logger.info(f"Initialized MCP server - {toolset_name}")
            self.servers.append(desktop_commander)

    def init_search_servers(self):
        if self._is_mcp_category_enabled("general", "search"):
            # MCP server - internet search
            toolset_name = "duckduckgo-mcp-server"
            internet_search = MCPServerStdio(command="uvx", args=["duckduckgo-mcp-server"])
            logger.info(f"Initialized MCP server - {toolset_name}")
            self.servers.append(internet_search)

    def init_code_execution_servers(self):
        if self._is_mcp_category_enabled("general", "code_execution"):
            # MCP server - run_python
            toolset_name = "run_python"
            run_python = MCPServerStdio(
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
            logger.info(f"Initialized MCP server - {toolset_name}")
            self.servers.append(run_python)

    def init_todo_servers(self):
        if self._is_mcp_enabled("productivity", "todo", "todoist"):
            # MCP server - todoist
            toolset_name = "todoist"
            todoist = MCPServerStdio(
                command="npx",
                args=["-y", "@abhiz123/todoist-mcp-server"],
                env={"TODOIST_API_TOKEN": os.getenv("TODOIST_API_TOKEN")},
                tool_prefix="todoist",
            )
            logger.info(f"Initialized MCP server - {toolset_name}")
            self.servers.append(todoist)

    def init_calendar_servers(self):
        # MCP server - google calendar
        if self._is_mcp_enabled("productivity", "calendar", "google_calendar"):
            toolset_name = "google_calendar"
            google_calendar = MCPServerStdio(
                command="uv",
                args=[
                    "run",
                    "--directory",
                    f"{os.getenv('GOOGLE_WORKSPACE_MCP_PATH')}",
                    "python",
                    "main.py",
                    "--tools",
                    "calendar",
                ],
                env=self._get_google_calendar_auth_env(),
                tool_prefix="google_calendar",
            )
            logger.info(f"Initialized MCP server - {toolset_name}")
            self.servers.append(google_calendar)

        if self.config["calendar"]["clockwise"]["enabled"]:
            pass # clockwise with oauth can only be configured as FastMCP client

    def init_chat_servers(self):
        # MCP server - Slack
        if self._is_mcp_enabled("productivity", "chat", "slack"):
            toolset_name = "slack"
            slack = MCPServerStdio(
                command="npx",
                args=[
                    "-y",
                    "slack-mcp-server@latest",
                    "--transport",
                    "stdio"
                ],
                env=self._get_slack_auth_env(),
                tool_prefix="slack",
            )
            logger.info(f"Initialized MCP server - {toolset_name}")
            self.servers.append(slack)

    async def inspect_fastmcp_client_tools(self):
        inspect_fastmcp_client_tools_enabled = self.config_manager.get_setting("debug.inspect_tools", False)
        if inspect_fastmcp_client_tools_enabled:
            async with Client(self.config) as client:
                await client.ping()
                self.fastmcp_client = client
                tools = await client.list_tools()
                logger.info("FastMCP Client - Available tools:")
                for tool in tools:
                    logger.debug(f"Tool attributes: {list(tool.__dict__.keys())}")
                    logger.info(f"Name - {tool.name}")
                    logger.debug(f"Title - {tool.title}")
                    logger.debug(f"Description - {tool.description}")
                    logger.debug(f"inputSchema - {tool.inputSchema}")
                    logger.debug(f"outputSchema - {tool.outputSchema}")
                    logger.debug(f"annotations - {tool.annotations}")

    def _get_slack_auth_env(self):
        # setup slack tokens based on the auth method
        auth_method = self.config["chat"]["slack"].get("auth_method")
        if not auth_method or auth_method == "xoxp":
            slack_auth_env = {
                "SLACK_MCP_XOXP_TOKEN": os.getenv("SLACK_MCP_XOXP_TOKEN"),
            }
        elif auth_method == "xoxc":
            slack_auth_env = {
                "SLACK_MCP_XOXC_TOKEN": os.getenv("SLACK_MCP_XOXC_TOKEN"),
                "SLACK_MCP_XOXD_TOKEN": os.getenv("SLACK_MCP_XOXD_TOKEN"),
            }
        return slack_auth_env

    def _get_google_calendar_auth_env(self):
        auth_env = {
            "GOOGLE_OAUTH_CLIENT_ID": os.getenv("GOOGLE_OAUTH_CLIENT_ID"),
            "GOOGLE_OAUTH_CLIENT_SECRET": os.getenv("GOOGLE_OAUTH_CLIENT_SECRET"),
        }
        return auth_env
