import logging

from opus_agent_base.managers.higher_order_tools_manager import BaseHigherOrderToolsManager
from opus_todo_agent.higher_order_tools.calendar.clockwise_calendar_tools import (
    ClockwiseCalendarHOTools,
)
from opus_todo_agent.higher_order_tools.calendar.google_calendar_tools import (
    GoogleCalendarHOTools,
)
from opus_todo_agent.higher_order_tools.chat.slack_tools import SlackHOTools

logger = logging.getLogger(__name__)


class HigherOrderToolsManager(BaseHigherOrderToolsManager):
    """
    Domain-specific manager for higher order tools in opus_todo_agent.
    
    Extends BaseHigherOrderToolsManager to register productivity-specific higher order tools.
    """

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
