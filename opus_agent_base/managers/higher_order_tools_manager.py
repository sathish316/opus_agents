import logging

logger = logging.getLogger(__name__)


class BaseHigherOrderToolsManager:
    """
    Base Manager for higher order tools.
    
    This class should be extended by domain-specific implementations
    to register higher order tools for the agent.
    """

    def __init__(
        self,
        agent,
        fastmcp_client_context,
        config_manager,
        instructions_manager,
        model_manager,
    ):
        self.agent = agent
        self.fastmcp_client_context = fastmcp_client_context
        self.config_manager = config_manager
        self.instructions_manager = instructions_manager
        self.model_manager = model_manager

    async def initialize_tools(self):
        """
        Initialize higher order tools. Override this method in subclasses
        to register domain-specific higher order tools.
        """
        logger.info("Base higher order tools initialized")

    def _is_mcp_enabled(self, domain, category, mcp):
        """
        Check if the MCP server is enabled in a given domain and category.
        Examples of domain are: general, productivity
        Examples of category are: todo, calendar etc.
        Examples of mcp are: todoist, google_calendar, slack etc.
        """
        return self.config_manager.get_setting(
            f"mcp_config.{domain}.{category}.{mcp}.higher_order_tools_enabled"
        )
