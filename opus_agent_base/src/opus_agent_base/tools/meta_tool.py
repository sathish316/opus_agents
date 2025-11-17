import logging
from abc import abstractmethod
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class MetaTool:
    """
    Base class for Meta tools that can dynamically create tools from specifications
    without writing code.

    Meta tools are ideal when:
    - You want to integrate APIs without writing custom code
    - You have an API specification (like OpenAPI)
    - You need to quickly prototype integrations
    - You want to expose external APIs directly to the agent

    Examples of Meta tools:
    - OpenAPI spec-based tools
    - GraphQL schema-based tools
    - gRPC proto-based tools
    """

    def __init__(
        self,
        name: str,
        config_key: str,
        spec_source: str,
        config_manager=None,
        instructions_manager=None,
        model_manager=None,
    ):
        """
        Initialize the MetaTool.

        Args:
            name: The name of the meta tool
            config_key: The configuration key path for this tool
            spec_source: The source of the specification (URL, file path, etc.)
            config_manager: Configuration manager instance
            instructions_manager: Instructions manager instance
            model_manager: Model manager instance
        """
        self.name = name
        self.config_key = config_key
        self.spec_source = spec_source
        self.config_manager = config_manager
        self.instructions_manager = instructions_manager
        self.model_manager = model_manager
        self.spec: Optional[Dict[str, Any]] = None

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
    async def initialize_tools(self, fastmcp_client_context):
        """
        Initialize tools from the specification and register them with the agent.

        Args:
            fastmcp_client_context: The FastMCP client context for tool integration
        """
        raise NotImplementedError("Subclasses must implement this method")

    def is_enabled(self) -> bool:
        """
        Check if this meta tool is enabled in the configuration.

        Returns:
            True if enabled, False otherwise
        """
        if self.config_manager:
            return self.config_manager.get_setting(
                f"mcp_config.{self.config_key}.enabled", False
            )
        return False
