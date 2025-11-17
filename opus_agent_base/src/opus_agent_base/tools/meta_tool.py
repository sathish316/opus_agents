import logging
from abc import abstractmethod
from typing import Any, Dict

from opus_agent_base.config.config_manager import ConfigManager
from pydantic_ai.tools import Tool

logger = logging.getLogger(__name__)


class MetaTool:
    """
    Base class for Meta tools that can dynamically create tools
    for standard usecases like OpenAPI specs, Scrapers, Bash/Python scripts etc

    Meta tools are ideal when you want to integrate APIs without writing custom code
    or using an MCP server for a specific API.
    """

    def __init__(
        self,
        name: str,
        config_manager: ConfigManager,
        config_key: str,
        spec_properties: Dict[str, Any],
    ):
        """
        Initialize the MetaTool.

        Args:
            name: The name of the meta tool
            config_manager: The configuration manager instance
            config_key: The configuration key path for this tool
            spec_properties: The properties of the specification (URL, file path, etc.)
        """
        self.name = name
        self.config_manager = config_manager
        self.config_key = config_key
        self.spec_properties = spec_properties

    @abstractmethod
    async def setup_tool(self) -> list[str]:
        """
        Setup the tool for use by the Agent.
        """
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    async def load_spec(self) -> Dict[str, Any]:
        """
        Load the specification from the source.

        Returns:
            The loaded specification as a dictionary
        """
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    async def create_mcp_server(self):
        """
        Create an MCP server from the loaded specification.
        This method should return a configured MCP server instance.

        Returns:
            An MCP server instance
        """
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    async def create_mcp_client_and_initialize_tools(self):
        """
        Create an MCP client and initialize tools from the loaded specification.
        This method should return a configured MCP client and initialized tools.

        Returns:
            A tuple of (MCP client, initialized tools)
        """
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    async def initialize_tools(self, agent):
        """
        Initialize the tool for use by the Agent.
        """
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    async def build_agent_tool(self) -> Tool:
        """
        Build an agent tool from the loaded specification.
        This method should return an agent tool instance.
        """
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    async def call_dynamic_tool(self, tool_name: str, kwargs: dict):
        """
        Call a dynamic tool from the loaded specification.
        This method should call a tool from the loaded specification.
        """
        raise NotImplementedError("Subclasses must implement this method")

