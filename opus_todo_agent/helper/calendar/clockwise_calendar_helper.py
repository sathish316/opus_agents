import json
import logging

from opus_todo_agent.helper.datetime_helper import DatetimeHelper
from opus_todo_agent.helper.fastmcp_client_helper import FastMCPClientHelper
from opus_todo_agent.models.calendar.clockwise_calendar_models import ClockwiseMeeting

logger = logging.getLogger(__name__)


class ClockwiseCalendarHelper:
    """Clockwise calendar helper"""

    def __init__(self):
        self.fastmcp_client_helper = FastMCPClientHelper()
        self.datetime_helper = DatetimeHelper()

    async def get_clockwise_meetings_for_date_range(
        self, fastmcp_client_context, from_datetime: str, to_datetime: str
    ) -> list[ClockwiseMeeting]:
        """
        Get meetings for a given date range from Clockwise

        Args:
            from_datetime: Start datetime in YYYY-MM-DDTHH:MM:SSZ format
            to_datetime: End datetime in YYYY-MM-DDTHH:MM:SSZ format

        Returns:
            List of ClockwiseMeeting objects.
            Each ClockwiseMeeting object contains the eventJson dictionary.
            EventJson dictionary contains the following fields - title, startTime, endTime.

        Format events as a list.
        Group events by date.
        Order events by start time. Understand that events in AM come before events in PM.
        """
        logger.info(
            f"[Tool call] Fetching Clockwise Meetings for date range: {from_datetime} to {to_datetime}"
        )
        mcp_tool_name = "clockwise_search_events"
        # mcp_tool_name = "search_events"
        result = await self.fastmcp_client_helper.call_fastmcp_tool(
            fastmcp_client_context,
            mcp_tool_name,
            {
                "query": {
                    "timeRangeSearch": {
                        "includeRanges": [
                            {
                                "startTime": self.datetime_helper.format_datetime(
                                    from_datetime
                                ),
                                "endTime": self.datetime_helper.format_datetime(
                                    to_datetime
                                ),
                            }
                        ]
                    }
                }
            },
            parse_json=False,
        )
        logger.debug(f"{result['data'][0]}")
        events_json_str = result["data"][0]
        events_list = json.loads(events_json_str)["events"]
        logger.info(f"Received {len(events_list)} Events from Clockwise")
        meetings = [ClockwiseMeeting(eventJson=event) for event in events_list]
        if len(meetings) > 0:
            logger.debug(f"Parsed sample event {meetings[0]}")
        else:
            logger.info("No events found in Clockwise")
        return meetings

    async def get_clockwise_meetings_for_predefined_date_range(
        self,
        fastmcp_client_context,
        predefined_daterange_key: str,
    ) -> list[ClockwiseMeeting]:
        """
        Get meetings for a predefined date range
        Values of predefined date ranges are:
        1. last_week
        2. today
        3. tomorrow
        4. yesterday
        5. current_week
        6. next_week
        """
        logger.info(
            f"[Tool call] Fetching Clockwise Meetings for predefined date range: {predefined_daterange_key}"
        )
        if predefined_daterange_key == "last_week":
            since, until = self.datetime_helper.get_last_week_datetime_range()
        elif predefined_daterange_key == "current_week":
            since, until = self.datetime_helper.get_current_week_datetime_range()
        elif predefined_daterange_key == "today":
            since, until = self.datetime_helper.get_today_datetime_range()
        elif predefined_daterange_key == "yesterday":
            since, until = self.datetime_helper.get_yesterday_datetime_range()
        elif predefined_daterange_key == "tomorrow":
            since, until = self.datetime_helper.get_tomorrow_datetime_range()
        elif predefined_daterange_key == "next_week":
            since, until = self.datetime_helper.get_next_week_datetime_range()
        else:
            raise ValueError(
                f"Invalid predefined date range key: {predefined_daterange_key}"
            )
        return await self.get_clockwise_meetings_for_date_range(
            fastmcp_client_context, since, until
        )
