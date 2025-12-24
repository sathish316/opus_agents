import logging

from fastmcp import Client
from singleton_decorator import singleton
from opus_agent_base.common.logging_config import console_log
from opus_agent_base.tools.fastmcp_server_config import FastMCPServerConfig

logger = logging.getLogger(__name__)


@singleton
class MCPManager:
    """
    Manager for MCP servers
    """

    def __init__(self, config_manager):
        self.config = {}
        self.config["mcpServers"] = {}
        self.config_manager = config_manager
        self.fastmcp_client_context = None
        self.fastmcp_client_instance = None
        self.fastmcp_client_instance_initialized = False
        self.enabled_servers = []

    def add_mcp_server(self, mcp_server_config: FastMCPServerConfig) -> bool:
        if self._is_mcp_enabled(mcp_server_config.config_key) or self._is_higher_order_tools_enabled(mcp_server_config.config_key):
            logger.info(f"Adding MCP server: {mcp_server_config.name}")
            self.config["mcpServers"][mcp_server_config.name] = mcp_server_config.mcp_server_config
            return True
        else:
            logger.info(f"MCP server {mcp_server_config.name} not enabled")
            return False

    def add_mcp_servers(self, mcp_servers_config: list[FastMCPServerConfig]) -> bool:
        for mcp_server_config in mcp_servers_config:
            result = self.add_mcp_server(mcp_server_config)
            if result:
                self.enabled_servers.append(mcp_server_config.name)
        console_log(f"Added {len(self.enabled_servers)} MCP servers - {self.enabled_servers}")
        logger.info("MCP servers added")

    async def initialize_fastmcp_client_context(self):
        if self.config["mcpServers"] is None or len(self.config["mcpServers"]) == 0:
            console_log("No MCP servers configured")
            return None

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
        logger.info("FastMCP Client initialized")
        return self.fastmcp_client_context

    async def inspect_fastmcp_client_tools(self):
        if self.fastmcp_client_context is None:
            return

        inspect_tools_enabled = self.config_manager.get_setting("debug.inspect_tools", False)
        inspect_tool_schema_enabled = self.config_manager.get_setting("debug.inspect_tool_schema", False)
        if inspect_tools_enabled:
            async def inspect_tools(client):
                await client.ping()
                self.fastmcp_client = client
                tools = await client.list_tools()
                logger.info("FastMCP Client - Available tools:")
                for tool in tools:
                    logger.debug(f"Tool attributes: {list(tool.__dict__.keys())}")
                    logger.info(f"Name - {tool.name}")
                    logger.debug(f"Title - {tool.title}")
                    logger.debug(f"Description - {tool.description}")
                    import json
                    if inspect_tool_schema_enabled:
                        logger.info(f"inputSchema - {json.dumps(tool.inputSchema, indent=2)}")
                    else:
                        logger.debug(f"inputSchema - {json.dumps(tool.inputSchema, indent=2)}")
                    logger.debug(f"outputSchema - {tool.outputSchema}")
                    logger.debug(f"annotations - {tool.annotations}")
            await self.fastmcp_client_context(inspect_tools)

    def _is_mcp_enabled(self, config_key):
        """
        Check if the MCP server is enabled in a given config key.
        config_key is of the format "domain.category.tool" or "domain.category"
        Examples of domain are: general, productivity
        Examples of category are: todo, calendar etc.
        Examples of tool are: todoist, google_calendar, slack etc.
        """
        # logger.info(f"Checking if MCP server is enabled - {config_key}")
        return self.config_manager.get_setting(f"mcp_config.{config_key}.enabled")

    def _is_higher_order_tools_enabled(self, config_key):
        """
        Check if the MCP server or higher order tools is enabled in a given config key.
        config_key is of the format "domain.category.tool" or "domain.category"
        Examples of domain are: general, productivity
        Examples of category are: todo, calendar etc.
        Examples of tool are: todoist, google_calendar, slack etc.
        """
        # logger.info(f"Checking if MCP server or higher order tools is enabled - {config_key}")
        return self.config_manager.get_setting(f"mcp_config.{config_key}.higher_order_tools_enabled")