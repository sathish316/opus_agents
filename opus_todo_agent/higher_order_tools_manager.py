import logging

from opus_todo_agent.higher_order_tools.calendar.clockwise_calendar_tools import (
    ClockwiseCalendarHOTools,
)
from opus_todo_agent.higher_order_tools.calendar.google_calendar_tools import (
    GoogleCalendarHOTools,
)
from opus_todo_agent.higher_order_tools.chat.slack_tools import SlackHOTools

logger = logging.getLogger(__name__)


class HigherOrderToolsManager:
    """
    Manager for higher order tools
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
        if self._is_mcp_enabled("productivity", "calendar", "google_calendar"):
            await GoogleCalendarHOTools().initialize_tools(
                self.agent, self.fastmcp_client_context
            )
            logger.info("Google calendar HigherOrderTools initialized")

        if self._is_mcp_enabled("productivity", "calendar", "clockwise"):
            await ClockwiseCalendarHOTools().initialize_tools(
                self.agent, self.fastmcp_client_context
            )
            logger.info("Clockwise HigherOrderTools initialized")

        if self._is_mcp_enabled("productivity", "chat", "slack"):
            await SlackHOTools(
                config_manager=self.config_manager,
                instructions_manager=self.instructions_manager,
                model_manager=self.model_manager,
            ).initialize_tools(self.agent, self.fastmcp_client_context)
            logger.info("Slack HigherOrderTools initialized")

        logger.info("Higher order MCP tools initialized")

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
