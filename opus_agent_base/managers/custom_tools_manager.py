import logging

logger = logging.getLogger(__name__)


class BaseCustomToolsManager:
    """
    Base Manager for custom tools.
    
    This class should be extended by domain-specific implementations
    to register custom tools for the agent.
    """

    def __init__(self, config_manager, instructions_manager, model_manager, agent):
        self.config_manager = config_manager
        self.agent = agent
        self.instructions_manager = instructions_manager
        self.model_manager = model_manager
        self.initialize_tools()

    def initialize_tools(self):
        """
        Initialize custom tools. Override this method in subclasses
        to register domain-specific tools.
        """
        logger.info("Base custom tools initialized")

    def _is_mcp_enabled(self, domain, category, mcp):
        """
        Check if the MCP server is enabled in a given domain and category.
        Examples of domain are: general, productivity
        Examples of category are: todo, calendar etc.
        Examples of mcp are: todoist, google_calendar, slack etc.
        """
        return self.config_manager.get_setting(f"mcp_config.{domain}.{category}.{mcp}.enabled")
