import logging
from typing import List

from pydantic_ai import RunContext

from opus_todo_agent.helper.calendar.clockwise_calendar_helper import (
    ClockwiseCalendarHelper,
)
from opus_agent_base.helpers.datetime_helper import DatetimeHelper
from opus_todo_agent.models.calendar.clockwise_calendar_models import ClockwiseMeeting

logger = logging.getLogger(__name__)


class ClockwiseCalendarHOTools:
    """
    Clockwise calendar tools on top of Clockwise MCP that can be added to the agent
    """

    def __init__(self):
        self.clockwise_calendar_helper = ClockwiseCalendarHelper()
        self.datetime_helper = DatetimeHelper()

    async def initialize_tools(self, agent, fastmcp_client_context):
        @agent.tool
        async def generate_review_of_past_or_future_daily_meetings(
            ctx: RunContext[str],
            predefined_daterange_key: str = "today",
            summarize: bool = True,
        ) -> List[ClockwiseMeeting]:
            """
            Generate daily review of Clockwise meetings.
            Supported filters for predefined_daterange_key are:
            1. today
            2. yesterday
            3. tomorrow
            4. Specific date in yyyy-mm-ddTHH:MM:SSZ format

            This method returns a list of meetings.

            Generate daily review summary by grouping meetings.

            If the user asks for a future date or a briefing of upcoming meetings, brief them about upcoming meetings.
            If the user asks for a past date or a review of past date, generate a review about past meetings.

            If the user asks to summarize, return a summary of the attended meetings.
            If there are more than 5 meetings for a day, try to summarize them.

            If the user asks to not summarize, return the list of meetings.

            By default, summarize meetings.
            """
            try:
                if (
                    predefined_daterange_key in list(["today","yesterday","tomorrow"])
                ):
                    logging.info(f"[CustomToolCall] Generating Daily review of meetings for {predefined_daterange_key}")
                    meetings = await self.clockwise_calendar_helper.get_clockwise_meetings_for_predefined_date_range(
                        fastmcp_client_context, predefined_daterange_key
                    )
                else:
                    logging.info(
                        f"[CustomToolCall]Generating Daily review of meetings for date: {predefined_daterange_key}"
                    )
                    meetings = (
                        await self.clockwise_calendar_helper.get_clockwise_meetings_for_date_range(
                            fastmcp_client_context,
                            predefined_daterange_key,
                            self.datetime_helper.get_next_datetime(
                                predefined_daterange_key
                            ),
                        )
                    )
            except Exception as e:
                import traceback
                logging.error(f"Stacktrace: {traceback.format_exc()}")
                logging.error(f"Error fetching meetings: {e}")
                return

            return meetings

        @agent.tool
        async def generate_review_of_past_or_future_weekly_meetings(
            ctx: RunContext[str],
            predefined_weekrange_key: str = "current_week",
            from_date: str = "",
            to_date: str = "",
            summarize: bool = True,
        ) -> List[ClockwiseMeeting]:
            """
            Generate weekly review of Clockwise meetings.
            Supported filters for predefined_weekrange_key are:
            1. last_week
            2. current_week
            3. next_week
            4. Default is current_week if no option is specified

            Instead of predefined_weekrange_key, the user can also provide a from_date and to_date to specify the week range explicitly.
            If from_date and to_date are provided, they should be in yyyy-mm-ddTHH:MM:SSZ format.

            This method returns a list of meetings. Group the meetings by date.

            If the user asks for a future week or a briefing of upcoming meetings, brief them about upcoming meetings.
            If the user asks for a past week or a review of past week, generate a review about past meetings.

            Generate weekly review summary by grouping meetings.

            If the user asks to summarize, return a summary of the meetings the user has accepted.
            If there are more than 10 meetings, try to summarize them.

            If the user asks to not summarize, return the list of meetings.

            By default, summarize meetings.
            """
            try:
                if from_date and to_date:
                    logging.info(
                        f"[CustomToolCall] Generating weekly review of meetings for the date range: {from_date} to {to_date}"
                    )
                    meetings = await self.clockwise_calendar_helper.get_clockwise_meetings_for_date_range(
                        fastmcp_client_context, from_date, to_date
                    )
                elif predefined_weekrange_key in list(["current_week","last_week","next_week"]):
                    logging.info(
                        f"[CustomToolCall] Generating weekly review of meetings for {predefined_weekrange_key}"
                    )
                    meetings = await self.clockwise_calendar_helper.get_clockwise_meetings_for_predefined_date_range(
                        fastmcp_client_context, predefined_weekrange_key
                    )
                else:
                    raise ValueError(
                        f"Invalid date range for weekly review: {predefined_weekrange_key}"
                    )
            except Exception as e:
                logging.error(f"Error fetching meetings: {e}")
                return

            return meetings