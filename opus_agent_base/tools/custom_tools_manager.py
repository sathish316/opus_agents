import logging

from opus_agent_base.tools.custom_tool import CustomTool

logger = logging.getLogger(__name__)


class CustomToolsManager:
    """
    Manager for custom tools
    """

    def __init__(self, config_manager, instructions_manager, model_manager, agent):
        self.config_manager = config_manager
        self.agent = agent
        self.instructions_manager = instructions_manager
        self.model_manager = model_manager

    def initialize_tools(self, custom_tools: list[CustomTool]):
        for custom_tool in custom_tools:
            if self._is_mcp_enabled(custom_tool.config_key):
                custom_tool.initialize_tools(self.agent)
                logger.info(f"{custom_tool.name} Custom tools initialized")
            else:
                logger.info(f"{custom_tool.name} Custom tools not enabled")
        logger.info("All Custom tools initialized")

    def _is_mcp_enabled(self, config_key: str):
        """
        Check if the Custom tool is enabled in a given config key.
        config_key is of the format "domain.category.tool"
        Examples of domain are: productivity
        Examples of category are: todo, calendar etc.
        Examples of tool are: todoist, google_calendar, slack etc.
        """
        return self.config_manager.get_setting(f"mcp_config.{config_key}.enabled")
