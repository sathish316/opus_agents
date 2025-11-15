import logging
from datetime import datetime, timedelta
from opus_agent_base.tools.higher_order_tool import HigherOrderTool
from opus_agent_base.tools.fastmcp_client_helper import FastMCPClientHelper
from pydantic_ai import RunContext
import json

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
        async def schedule_deepwork_session(
            ctx: RunContext[str],
            event_title: str,
            start_hour: int,
            end_hour: int,
            duration_minutes: int = 60,
            timezone: str = "Asia/Kolkata"
        ) -> str:
            """
            Schedule a deepwork session today by finding a free slot.

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
            logger.info(f"Scheduling '{event_title}' ({duration_minutes}m, {start_hour}-{end_hour})")

            try:
                # Create time window for today
                today = datetime.now().date()
                search_start = datetime.combine(today, datetime.min.time().replace(hour=start_hour))
                search_end = datetime.combine(today, datetime.min.time().replace(hour=end_hour))

                # Step 1: Get calendar events
                events = await self.get_calendar_events(fastmcp_client_context, search_start, search_end)

                # Step 2: Find a free slot
                free_slot = self.find_free_slot(events, search_start, search_end, duration_minutes)

                if not free_slot:
                    return f"❌ No {duration_minutes}-minute slots available between {start_hour}:00 and {end_hour}:00"

                free_start, free_end = free_slot

                # Step 3: Schedule the event
                success = await self.schedule_event(fastmcp_client_context, event_title, free_start, free_end)

                if not success:
                    return "❌ Failed to schedule event"

                return (
                    f"✅ Scheduled: {event_title}\n"
                    f"📅 {free_start.strftime('%I:%M %p')} - {free_end.strftime('%I:%M %p')}\n"
                    f"⏱️  {duration_minutes} minutes"
                )

            except Exception as e:
                logger.error(f"Error scheduling: {e}")
                import traceback
                logger.error(f"Stacktrace: {traceback.format_exc()}")
                return f"❌ Error: {str(e)}"

    async def get_calendar_events(self, fastmcp_client_context, start_time: datetime, end_time: datetime):
        """
        Helper 1: Get calendar events from Clockwise MCP server

        Args:
            fastmcp_client_context: MCP client context
            start_time: Start of time range
            end_time: End of time range

        Returns:
            List of calendar events
        """
        logger.info(f"Fetching events between {start_time} and {end_time}")

        result = await self.fastmcp_client_helper.call_fastmcp_tool(
            fastmcp_client_context,
            "clockwise_search_events",
            {
                "query": {
                    "timeRangeSearch": {
                        "includeRanges": [{
                            "startTime": start_time.isoformat() + "Z",
                            "endTime": end_time.isoformat() + "Z",
                        }]
                    }
                }
            },
            parse_json=False,
        )

        events = json.loads(result["data"][0])["events"]
        logger.info(f"Found {len(events)} existing events")
        return events

    def find_free_slot(self, events, search_start: datetime, search_end: datetime, duration_minutes: int):
        """
        Helper 2: Find first free slot in calendar

        Args:
            events: List of calendar events
            search_start: Start of search window
            search_end: End of search window
            duration_minutes: Required duration in minutes

        Returns:
            Tuple of (start_time, end_time) for free slot, or None if no slot found
        """
        logger.info(f"Finding {duration_minutes}min slot between {search_start} and {search_end}")

        current_time = search_start

        # Sort events by start time
        sorted_events = sorted(events, key=lambda e: e["startTime"])

        for event in sorted_events:
            event_start = datetime.fromisoformat(event["startTime"].replace("Z", ""))

            # Check if there's a gap before this event
            if (event_start - current_time).total_seconds() >= duration_minutes * 60:
                free_start = current_time
                free_end = free_start + timedelta(minutes=duration_minutes)
                logger.info(f"Found free slot: {free_start} to {free_end}")
                return (free_start, free_end)

            event_end = datetime.fromisoformat(event["endTime"].replace("Z", ""))
            current_time = max(current_time, event_end)

        # Check if there's time after the last event
        if (search_end - current_time).total_seconds() >= duration_minutes * 60:
            free_start = current_time
            free_end = free_start + timedelta(minutes=duration_minutes)
            logger.info(f"Found free slot at end: {free_start} to {free_end}")
            return (free_start, free_end)

        logger.warning("No free slot found")
        return None

    async def schedule_event(self, fastmcp_client_context, title: str, start_time: datetime, end_time: datetime):
        """
        Helper 3: Schedule an event using Clockwise MCP server

        Args:
            fastmcp_client_context: MCP client context
            title: Event title
            start_time: Event start time
            end_time: Event end time

        Returns:
            True if successful, False otherwise
        """
        logger.info(f"Scheduling '{title}' from {start_time} to {end_time}")

        # Create a proposal
        proposal_result = await self.fastmcp_client_helper.call_fastmcp_tool(
            fastmcp_client_context,
            "clockwise_create_proposal",
            {
                "title": title,
                "startTime": start_time.isoformat() + "Z",
                "endTime": end_time.isoformat() + "Z",
            },
            parse_json=False,
        )

        proposal_data = json.loads(proposal_result["data"][0])
        proposal_id = proposal_data.get("id")

        if not proposal_id:
            logger.error("Failed to create proposal")
            return False

        # Confirm the proposal to create the event
        await self.fastmcp_client_helper.call_fastmcp_tool(
            fastmcp_client_context,
            "clockwise_confirm_proposal",
            {"proposalId": proposal_id},
            parse_json=False,
        )

        logger.info("Event scheduled successfully")
        return True

