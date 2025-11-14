# Guide: Adding a Higher Order Tool

## What is a Higher Order Tool?

Higher order tools are specialized tools that leverage MCP servers and tools to provide enhanced functionality. They wrap and extend MCP server tools with custom business logic, making complex workflows for agents possible.

Higher order tools are ideal when:
- An MCP server exists but needs additional logic for an AI agent to consume to solve your problem
- You need to add validation, formatting, enrichment, transformation

**Key Difference from Custom Tools:**
- **Custom Tools**: Direct API integration, no MCP server needed
- **Higher Order Tools**: Build on top of existing MCP servers, add orchestration layer

---

## Example: Schedule Clockwise Events for DeepWork with Smart Defaults

This guide will walk you through creating a higher order tool that schedules events using Clockwise MCP server, with preferences that are specific to scheduling DeepWork tasks

### Prerequisites

- Clockwise Account for OAuth integration
- Clockwise MCP server configuration

---

## Step 1: Set Up Clockwise MCP Server

First, ensure the Clockwise MCP server is available. Higher order tools build on top of MCP servers.

### 1. Add Clockwise MCP Server to MCP Registry

Add Clockwise MCP server to your Agent's MCP registry. This is similar to adding MCP servers in mcp.json in other AI tools. The additional config here lets you contol which MCP servers/tools are enabled for the Agent.

**File:** `opus_todo_agent/todo_mcp_server_registry.py`

```python
class TodoMCPServerRegistry(MCPServerRegistry):
    """Registry for TODO agent MCP servers"""

    def get_clockwise_mcp_server(self) -> FastMCPServerConfig:
        # MCP server (remote): https://mcp.getclockwise.com/mcp
        return FastMCPServerConfig(
            "clockwise",
            "productivity.calendar.clockwise",
            {
                "transport": "streamable-http",
                "url": "https://mcp.getclockwise.com/mcp",
                "tool_prefix": "clockwise",
                "auth": "oauth",
            }
        )

```

### 2. Add Clockwise MCP Server to the Agent

MCP servers added to the agent are loaded on startup and are made available as tools

**File:** `opus_todo_agent/todo_agent_builder.py`

```python
    def _add_fastmcp_servers(self):
        mcp_server_registry = MCPServerRegistry()
        todo_mcp_server_registry = TodoMCPServerRegistry(self.config_manager)
        fastmcp_servers_config = [
            todo_mcp_server_registry.get_clockwise_fastmcp_server(),
        ]
        self.mcp_manager.add_fastmcp_servers(fastmcp_servers_config)
```

### 3. Enable Clockwise MCP server and tools

**File:** `opus-config.yaml`

```yaml
mcp_config:
  productivity:
    calendar:
      clockwise:
        enabled: true
        higher_order_tools_enabled: true
```

---

## Step 2: Implement Higher Order Tool

Analyze MCP tools to find the capability that will be useful to you:

TODO: Add section on MCP inspector

Now create the higher order tool that wraps the MCP server with custom logic.

**File:** `opus_todo_agent/higher_order_tools/calendar/clockwise_higher_order_tool.py`

```python

@dataclass
class DeepWorkPreferences:
    duration_minutes: int = 60,
    working_hours_start: int = 9,
    working_hours_end: int = 17,
    timezone: str = "Asia/Kolkata",
    visibility: str = "private",
    preferred_window: str = "start", # change to literal, possible values are start/middle/end of day, morning/afternoon/evening


class ClockwiseHigherOrderTool(HigherOrderTool):
    """
    Higher order tools for Clockwise calendar that add smart scheduling
    capabilities on top of the basic MCP server.
    """

    def __init__(self, config_manager=None, instructions_manager=None, model_manager=None):
        super().__init__(
            "clockwise",
            "deepwork.calendar.clockwise",
            config_manager,
            instructions_manager,
            model_manager
        )

    async def initialize_tools(self, agent, fastmcp_client_context):
        @agent.tool
        async def schedule_deepwork_event_today(
            ctx: RunContext[str],
            event_title: str,
            deepwork_preferences: DeepWorkPreferences
        ) -> str:
            """
            Schedule a deepwork event today in the first available free slot.
            
            This tool intelligently finds free time in your calendar today and
            schedules an event. It respects your working hours and finds gaps
            between existing meetings.
            
            Args:
                event_title: Title/name of the event to schedule
                deepwork_preferences: Captures details of DeeepWork scheduling preferences in `DeepWorkPreferences` format
            
            Returns:
                Success message with event details and link, or error message
            
            Example usage:
                - "Schedule a focus session today"
                - "Book 2 hours for deep work today in the morning"
                - "Schedule a 30 minute review meeting today"
                - "Create a 90 minute coding block today, prefer morning"
            """
            logger.info(
                f"[HigherOrderToolCall] Scheduling '{event_title}' today "
                f"({duration_minutes}m, {timezone})"
            )

            try:
                # Get today's date
                tz = pytz.timezone(timezone)
                today = datetime.now(tz).date().isoformat()
                
                logger.info(f"Finding free slots for {today}")

                # Find free slots #TODO: replace with helper
                free_slots = await self.clockwise_helper.find_free_slots(
                    fastmcp_client_context,
                    date=today,
                    working_hours_start=working_hours_start,
                    working_hours_end=working_hours_end,
                    duration_minutes=duration_minutes,
                    timezone=timezone
                )

                if not free_slots:
                    logger.warning(f"No free slots found for {duration_minutes} minutes")
                    return (
                        f"❌ Could not find any free {duration_minutes}-minute slots today "
                        f"between {working_hours_start}:00 and {working_hours_end}:00. "
                        f"Your calendar might be fully booked."
                    )

                # Select slot based on preference #TODO: replace with helper
                if prefer_morning:
                    # Take the earliest slot
                    selected_slot = free_slots[0]
                    slot_type = "morning"
                else:
                    # Take the first available (might be morning or afternoon)
                    selected_slot = free_slots[0]
                    slot_start_hour = datetime.fromisoformat(selected_slot[0]).hour
                    slot_type = "morning" if slot_start_hour < 12 else "afternoon"

                start_time, end_time = selected_slot

                # Create event request #TODO: doc on how to find tool input using mcp inspector
                request = EventSchedulingRequest(
                    title=event_title,
                    start_time=start_time,
                    end_time=end_time,
                    timezone=timezone,
                    visibility=visibility,
                    description=description
                )

                # Schedule the event #TODO: keep in tool
                event_id = await self.clockwise_helper.schedule_event(
                    fastmcp_client_context,
                    request
                )

                if event_id:
                    # Format time for display
                    start_dt = datetime.fromisoformat(start_time)
                    end_dt = datetime.fromisoformat(end_time)
                    
                    time_str = f"{start_dt.strftime('%I:%M %p')} - {end_dt.strftime('%I:%M %p')}"
                    
                    return (
                        f"✅ Event scheduled successfully!\n\n"
                        f"📅 **{event_title}**\n"
                        f"🕐 {time_str} ({timezone})\n"
                        f"⏱️  Duration: {duration_minutes} minutes\n"
                        f"🔒 Visibility: {visibility}\n"
                        f"🌅 Slot type: {slot_type}\n\n"
                        f"Found {len(free_slots)} available slot(s) today. "
                        f"Booked the {'earliest' if prefer_morning else 'first available'} one."
                    )
                else:
                    return "❌ Failed to schedule event. Please check logs for details."

            except Exception as e:
                logger.error(f"Error scheduling event: {e}")
                import traceback
                logger.error(f"Stacktrace: {traceback.format_exc()}")
                return f"❌ Error: {str(e)}"

        @agent.tool
        async def find_free_time_today(
            ctx: RunContext[str],
            duration_minutes: int = 60,
            working_hours_start: int = 9,
            working_hours_end: int = 17,
            timezone: str = "Asia/Kolkata",
        ) -> str:
            """
            Find all free time slots today without scheduling anything.
            
            Use this when the user wants to see available time before
            committing to schedule an event.
            
            Args:
                duration_minutes: Minimum duration needed (default: 60)
                working_hours_start: Start of working day (default: 9)
                working_hours_end: End of working day (default: 17)
                timezone: Timezone for the search (default: "Asia/Kolkata")
            
            Returns:
                Formatted list of free time slots
            
            Example usage:
                - "When am I free today?"
                - "Show me my available time slots today"
                - "Do I have any 2-hour blocks free today?"
            """
            logger.info(
                f"[HigherOrderToolCall] Finding free slots today "
                f"(min {duration_minutes}m)"
            )

            try:
                tz = pytz.timezone(timezone)
                today = datetime.now(tz).date().isoformat()

                free_slots = await self.clockwise_helper.find_free_slots(
                    fastmcp_client_context,
                    date=today,
                    working_hours_start=working_hours_start,
                    working_hours_end=working_hours_end,
                    duration_minutes=duration_minutes,
                    timezone=timezone
                )

                if not free_slots:
                    return (
                        f"📅 No free slots found today that are at least "
                        f"{duration_minutes} minutes long.\n"
                        f"Your calendar is fully booked between "
                        f"{working_hours_start}:00 and {working_hours_end}:00."
                    )

                # Format output
                output = [
                    f"📅 Free time today (minimum {duration_minutes} minutes):\n"
                ]

                for i, (start, end) in enumerate(free_slots, 1):
                    start_dt = datetime.fromisoformat(start)
                    end_dt = datetime.fromisoformat(end)
                    
                    duration = int((end_dt - start_dt).total_seconds() / 60)
                    time_range = f"{start_dt.strftime('%I:%M %p')} - {end_dt.strftime('%I:%M %p')}"
                    
                    # Add morning/afternoon indicator
                    period = "🌅 Morning" if start_dt.hour < 12 else "🌆 Afternoon"
                    
                    output.append(
                        f"{i}. {time_range} ({duration} min) {period}"
                    )

                return "\n".join(output)

            except Exception as e:
                logger.error(f"Error finding free time: {e}")
                return f"❌ Error: {str(e)}"
```


---

## Step 3: Register Higher Order Tool

Add higher order tool to an existing or new agent. If you're extending an existing Agent, make these changes in `todo_agent_builder.py`. If you're building a new agent by following the GUIDE_BUILD_AN_AGENT.md, make these changes in `deepwork_agent_builder.py`

```python
    def _add_higher_order_tools(self):
        self.higher_order_tools: list[HigherOrderTool] = [
            ClockwiseHigherOrderTool(),
        ]
```

Another option to add custom tools is to add tools to the AgentBuilder in `todo_agent_runner.py` or `deepwork_agent_runner.py`

```python
    DeepWorkAgentBuilder(config_manager)
        .name("deepwork-agent")
        .higher_order_tool(ClockwiseHigherOrderTool())
```

---

## Step 4: Test Your Higher Order Tool

```bash
# Start the agent
uv run main.py
```

```bash
# Test various scenarios:
> Schedule a deep work session today
> Schedule a focus session today
> Schedule a deep work meeting at 2 PM today for 90 minutes
> I need 2 hours to work on the report, prefer morning
```