import logging
import os

from fastmcp import Client
from mcp.client.session import ClientSession
from pydantic_ai.tools import Tool
from singleton_decorator import singleton
from pydantic_ai.mcp import MCPServer


logger = logging.getLogger(__name__)


@singleton
class MCPManager:
    """
    Manager for MCP servers
    """

    def __init__(self, config_manager):
        self.config = {}
        self.config_manager = config_manager
        self.servers = []
        self.fastmcp_client_instance = None
        self.fastmcp_client_instance_initialized = False

    async def async_init(self):
        self.fastmcp_client = await self.initialize_higher_order_mcp_servers()
        return self

    def add_servers(self, mcp_servers_config):
        self.servers = []
        for mcp_server_config in mcp_servers_config:
            if self._is_mcp_enabled(mcp_server_config.config_key):
                logger.info(f"Adding MCP server: {mcp_server_config.name}")
                self.servers.append(mcp_server_config.mcp_server)
            else:
                logger.info(f"MCP server {mcp_server_config.name} not enabled")
        logger.info("MCP servers added")

    def add_fastmcp_servers(self, fastmcp_servers_config):
        self.config["mcpServers"] = {}
        for fastmcp_server_config in fastmcp_servers_config:
            if self._is_mcp_enabled(fastmcp_server_config.config_key) or self._is_higher_order_tools_enabled(fastmcp_server_config.config_key):
                logger.info(f"Adding FastMCP server: {fastmcp_server_config.name}")
                self.config["mcpServers"][fastmcp_server_config.name] = fastmcp_server_config.mcp_server_config
            else:
                logger.info(f"FastMCP server {fastmcp_server_config.name} not enabled")
        logger.info("FastMCP servers added")

    async def initialize_fastmcp_client_context(self):
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
        await self._inspect_fastmcp_client_tools()
        logger.info("Client for FastMCP servers initialized")
        return self.fastmcp_client_context

    def _is_mcp_enabled(self, config_key):
        """
        Check if the MCP server is enabled in a given config key.
        config_key is of the format "domain.category.tool" or "domain.category"
        Examples of domain are: general, productivity
        Examples of category are: todo, calendar etc.
        Examples of tool are: todoist, google_calendar, slack etc.
        """
        #logger.info(f"Checking if MCP server is enabled - {config_key}")
        return self.config_manager.get_setting(f"mcp_config.{config_key}.enabled")

    def _is_higher_order_tools_enabled(self, config_key):
        """
        Check if the MCP server or higher order tools is enabled in a given config key.
        config_key is of the format "domain.category.tool" or "domain.category"
        Examples of domain are: general, productivity
        Examples of category are: todo, calendar etc.
        Examples of tool are: todoist, google_calendar, slack etc.
        """
        #logger.info(f"Checking if MCP server is enabled - {config_key}")
        return self.config_manager.get_setting(f"mcp_config.{config_key}.higher_order_tools_enabled")

    async def _inspect_fastmcp_client_tools(self):
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