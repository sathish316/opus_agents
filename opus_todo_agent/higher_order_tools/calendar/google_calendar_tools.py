import logging
from typing import List

from pydantic_ai import RunContext

from opus_todo_agent.helper.calendar.google_calendar_helper import GoogleCalendarHelper
from opus_agent_base.helpers.datetime_helper import DatetimeHelper
from opus_todo_agent.models.calendar.google_calendar_models import GCalMeeting

logger = logging.getLogger(__name__)


class GoogleCalendarHOTools:
    """
    Google calendar tools on top of Google calendar MCP that can be added to the agent
    """

    def __init__(self):
        self.datetime_helper = DatetimeHelper()
        self.google_calendar_helper = GoogleCalendarHelper()

    async def initialize_tools(self, agent, fastmcp_client_context):
        @agent.tool
        async def generate_daily_review_of_meetings(
            ctx: RunContext[str],
            predefined_daterange_key: str = None,
            summarize: bool = True,
        ) -> List[GCalMeeting]:
            """
            Generate daily review of meetings.
            Supported filters for predefined_daterange_key are:
            1. today
            2. yesterday
            3. Specific date in yyyy-mm-dd format

            This method returns a list of meetings.

            Generate daily review summary by grouping meetings.

            If the user asks to summarize, return a summary of the attended meetings.
            If there are more than 5 meetings for a day, try to summarize them.

            If the user asks to not summarize, return the list of meetings.

            By default, summarize meetings.
            """
            try:
                if (
                    predefined_daterange_key == ""
                    or predefined_daterange_key == "today"
                ):
                    logging.info("[CustomToolCall] Generating Daily review of meetings for today")
                    meetings = await self.google_calendar_helper.get_meetings_for_predefined_date_range(
                        fastmcp_client_context, predefined_daterange_key
                    )
                elif predefined_daterange_key == "yesterday":
                    logging.info("[CustomToolCall]Generating Daily review of meetings for yesterday")
                    meetings = await self.google_calendar_helper.get_meetings_for_predefined_date_range(
                        fastmcp_client_context, predefined_daterange_key
                    )
                else:
                    logging.info(
                        f"Generating Daily review of meetings for date: {predefined_daterange_key}"
                    )
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
                return

            return meetings

        @agent.tool
        async def generate_weekly_review_of_meetings(
            ctx: RunContext[str],
            predefined_weekrange_key: str = "current_week",
            from_date: str = "",
            to_date: str = "",
            summarize: bool = True,
        ) -> List[GCalMeeting]:
            """
            Generate weekly review of meetings.
            Supported filters for predefined_weekrange_key are:
            1. last_week
            2. current_week
            3. Default is current_week if no option is specified

            Instead of predefined_weekrange_key, the user can also provide a from_date and to_date to specify the week range explicitly.

            This method returns a list of meetings.

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
                    meetings = await self.google_calendar_helper.get_meetings_for_date_range(
                        fastmcp_client_context, from_date, to_date
                    )
                elif predefined_weekrange_key == "current_week":
                    logging.info(
                        "[CustomToolCall] Generating weekly review of meetings for current week"
                    )
                    meetings = await self.google_calendar_helper.get_meetings_for_predefined_date_range(
                        fastmcp_client_context, "current_week"
                    )
                elif predefined_weekrange_key == "last_week":
                    logging.info("[CustomToolCall] Generating weekly review of meetings for last week")
                    meetings = await self.google_calendar_helper.get_meetings_for_predefined_date_range(
                        fastmcp_client_context, "last_week"
                    )
                else:
                    raise ValueError(
                        f"Invalid date range for weekly review: {predefined_weekrange_key}"
                    )
            except Exception as e:
                logging.error(f"Error fetching meetings: {e}")
                return

            return meetings
