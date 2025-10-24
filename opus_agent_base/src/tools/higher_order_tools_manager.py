import logging

from opus_agent_base.tools.higher_order_tool import HigherOrderTool

logger = logging.getLogger(__name__)


class HigherOrderToolsManager:
    """
    Manager for higher order tools
    """

    def __init__(
        self,
        config_manager,
        agent,
        fastmcp_client_context,
    ):
        self.config_manager = config_manager
        self.agent = agent
        self.fastmcp_client_context = fastmcp_client_context

    async def initialize_tools(self, higher_order_tools: list[HigherOrderTool]):
        for tool in higher_order_tools:
            if self._is_mcp_enabled(tool.config_key):
                await tool.initialize_tools(self.agent, self.fastmcp_client_context)
                logger.info(f"{tool.name} Higher order tools initialized")
            else:
                logger.info(f"{tool.name} Higher order tools not enabled")
        logger.info("All Higher order tools initialized")

    def _is_mcp_enabled(self, config_key: str):
        """
        Check if the Higher order tool is enabled in a given config key.
        config_key is of the format "domain.category.tool"
        Examples of domain are: productivity
        Examples of category are: calendar, chat etc.
        Examples of tool are: google_calendar, slack etc.
        """
        return self.config_manager.get_setting(f"mcp_config.{config_key}.higher_order_tools_enabled")
