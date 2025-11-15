import logging
from datetime import datetime

from opus_agent_base.common.logging_config import console_log
from opus_agent_base.tools.fastmcp_client_helper import FastMCPClientHelper
from opus_agent_base.tools.higher_order_tool import HigherOrderTool
from pydantic_ai import RunContext

logger = logging.getLogger(__name__)


class ClockwiseHigherOrderTool(HigherOrderTool):
    """
    Simple higher order tool for Clockwise calendar that schedules deepwork sessions.
    """

    def __init__(self, config_manager=None, instructions_manager=None, model_manager=None):
        super().__init__(
            "clockwise",
            "deepwork.calendar.clockwise",
            config_manager,
            instructions_manager,
            model_manager
        )
        self.fastmcp_client_helper = FastMCPClientHelper()

    async def initialize_tools(self, agent, fastmcp_client_context):
        @agent.tool
        async def schedule_deepwork_slot_in_calendar(
            ctx: RunContext[str],
            event_title: str,
            start_hour: int,
            end_hour: int,
            duration_minutes: int = 60,
        ) -> str:
            """
            Schedule a deepwork slot in the calendar today.
            If a proposal url is returned after scheduling, always show the proposal url to the user.
            Proposal url indicates that deep work slot is scheduled successfully.

            Args:
                event_title: Title of the deepwork session
                start_hour: Start of search window (e.g., 9 for 9am)
                end_hour: End of search window (e.g., 17 for 5pm)
                duration_minutes: How long the session should be (default: 60)
                timezone: Timezone (default: "America/Los_Angeles")

            Returns:
                Success message with scheduled time or error message

            Example: "Schedule a 90 minute coding session between 9am and 5pm"
            """
            logger.info(f"[CustomToolCall] Scheduling '{event_title}' ({duration_minutes}m, {start_hour}-{end_hour})")
            console_log(f"[CustomToolCall] Scheduling '{event_title}' ({duration_minutes}m, {start_hour}-{end_hour})")

            try:
                # Create time window for today
                today = datetime.now().date()
                search_start = datetime.combine(today, datetime.min.time().replace(hour=start_hour))
                search_end = datetime.combine(today, datetime.min.time().replace(hour=end_hour))

                # Create a proposal
                proposal_params = {
                        "newEvents": [{
                            "title": event_title,
                            "timeRanges": [{
                                "startTime": search_start.isoformat(),
                                "endTime": search_end.isoformat(),
                            }],
                            "duration": f"PT{duration_minutes}M",
                        }]
                    }
                logger.info(f"[CustomToolCall] Creating proposal: {proposal_params}")
                proposal_result = await self.fastmcp_client_helper.call_fastmcp_tool(
                    fastmcp_client_context,
                    "clockwise_create_proposal",
                    proposal_params,
                    parse_json=False,
                )

                if not proposal_result:
                    logger.error("Failed to create proposal")
                    return False

                return proposal_result

            except Exception as e:
                logger.error(f"Error scheduling: {e}")
                import traceback
                logger.error(f"Stacktrace: {traceback.format_exc()}")
                return f"❌ Error: {str(e)}"
