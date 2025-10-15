import logging
import os

from opus_todo_agent.helper.datetime_helper import DatetimeHelper
from opus_todo_agent.helper.fastmcp_client_helper import FastMCPClientHelper
from opus_todo_agent.models.calendar.google_calendar_models import GCalMeeting

logger = logging.getLogger(__name__)


class GoogleCalendarHelper:
    """Google calendar helper"""

    def __init__(self):
        self.fastmcp_client_helper = FastMCPClientHelper()
        self.datetime_helper = DatetimeHelper()

    async def get_meetings_for_date_range(
        self, fastmcp_client_context, from_datetime: str, to_datetime: str
    ) -> list[GCalMeeting]:
        """
        Get meetings for a given date range

        Args:
            from_datetime: Start datetime in YYYY-MM-DDTHH:MM:SSZ format
            to_datetime: End datetime in YYYY-MM-DDTHH:MM:SSZ format

        Returns:
            List of Meeting objects
        """
        logger.info(
            f"[Tool call] Fetching Google Calendar Meetings for date range: {from_datetime} to {to_datetime}"
        )
        mcp_tool_name = "google_calendar_get_events"
        # mcp_tool_name = "get_events"
        result = await self.fastmcp_client_helper.call_fastmcp_tool(
            fastmcp_client_context,
            mcp_tool_name,
            {
                "time_min": from_datetime,
                "time_max": to_datetime,
                "user_google_email": os.getenv("GOOGLE_USER_EMAIL"),
            },
            parse_json=False,
        )
        logger.info(f"{result['data'][0]}")
        meetings_text = result["data"][0]
        meeting_lines = meetings_text.split("\n")[1:]
        meetings = [GCalMeeting(line) for line in meeting_lines if line.strip()]
        return meetings

    async def get_meetings_for_predefined_date_range(
        self,
        fastmcp_client_context,
        predefined_daterange_key: str,
    ) -> list[GCalMeeting]:
        """
        Get meetings for a predefined date range
        Values of predefined date ranges are:
        1. last_week
        2. today
        3. yesterday
        4. current_week
        """
        logger.info(
            f"[Tool call] Fetching Google Calendar Meetings for predefined date range: {predefined_daterange_key}"
        )
        if predefined_daterange_key == "last_week":
            since, until = self.datetime_helper.get_last_week_datetime_range()
        elif predefined_daterange_key == "current_week":
            since, until = self.datetime_helper.get_current_week_datetime_range()
        elif predefined_daterange_key == "today":
            since, until = self.datetime_helper.get_today_datetime_range()
        elif predefined_daterange_key == "yesterday":
            since, until = self.datetime_helper.get_yesterday_datetime_range()
        else:
            raise ValueError(
                f"Invalid predefined date range key: {predefined_daterange_key}"
            )
        return await self.get_meetings_for_date_range(
            fastmcp_client_context, since, until
        )
