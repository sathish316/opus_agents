import logging
from typing import List

from opus_agent_base.common.datetime_helper import DatetimeHelper
from pydantic_ai import RunContext

from opus_agent_base.tools.higher_order_tool import HigherOrderTool
from opus_todo_agent.helper.calendar.google_calendar_helper import GoogleCalendarHelper
from opus_todo_agent.models.calendar.google_calendar_models import GCalMeeting
from opus_agent_base.common.logging_config import console_log

logger = logging.getLogger(__name__)


class GoogleCalendarHigherOrderTool(HigherOrderTool):
    """
    Google calendar tools on top of Google calendar MCP that can be added to the agent
    """

    def __init__(self, config_manager=None, instructions_manager=None, model_manager=None):
        super().__init__("google_calendar", "productivity.calendar.google_calendar", config_manager, instructions_manager, model_manager)
        self.datetime_helper = DatetimeHelper()
        self.google_calendar_helper = GoogleCalendarHelper()

    async def initialize_tools(self, agent, fastmcp_client_context):
        @agent.tool
        async def daily_or_weekly_review_of_meetings(
            ctx: RunContext[str],
            predefined_daterange_key: str = "today",
            from_date: str = "",
            to_date: str = "",
            summarize: bool = True,
        ) -> List[GCalMeeting]:
            """
            Return daily or weekly review of meetings.
            Supported filters for predefined_daterange_key are:
            1. today
            2. yesterday
            3. tomorrow
            4. last_week
            5. current_week
            6. next_week
            7. Default is today if no option is specified
            8. Default to current_week if user asks for weekly review and does not specify a week

            Instead of predefined_daterange_key, the user can also provide a from_date and to_date to specify the date range explicitly.
            Instead of predefined_daterange_key, the user can also provide a specific date in yyyy-mm-dd format.

            This method returns a list of meetings.

            Generate daily or weekly review summary by grouping meetings.

            If the user asks to summarize, return a summary of the meetings the user has accepted.
            If the user asks to not summarize, return the list of meetings.

            By default, summarize meetings.
            """
            try:
                if from_date and to_date:
                    logging.info(f"[CustomToolCall] Generating review of meetings for the date range: {from_date} to {to_date}")
                    console_log(f"[CustomToolCall] Generating review of meetings for the date range: {from_date} to {to_date}")
                    meetings = await self.google_calendar_helper.get_meetings_for_date_range(
                        fastmcp_client_context, from_date, to_date
                    )
                elif predefined_daterange_key in list(["today","yesterday","tomorrow","current_week","last_week","next_week"]):
                    logging.info(f"[CustomToolCall] Generating review of meetings for {predefined_daterange_key}")
                    console_log(f"[CustomToolCall] Generating review of meetings for {predefined_daterange_key}")
                    meetings = await self.google_calendar_helper.get_meetings_for_predefined_date_range(
                        fastmcp_client_context, predefined_daterange_key
                    )
                elif predefined_daterange_key:
                    logging.info(f"Generating review of meetings for date: {predefined_daterange_key}")
                    console_log(f"[CustomToolCall] Generating review of meetings for date: {predefined_daterange_key}")
                    meetings = (
                        await self.google_calendar_helper.get_meetings_for_date_range(
                            fastmcp_client_context,
                            predefined_daterange_key,
                            self.datetime_helper.get_next_date(
                                predefined_daterange_key
                            ),
                        )
                    )
            except Exception as e:
                logging.error(f"Error fetching meetings: {e}")
                import traceback
                logging.error(traceback.format_exc())
                return

            return meetings
