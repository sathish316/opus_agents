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

**File:** `<agent-src>/todo_mcp_server_registry.py` or `<agent-src>/deepwork_mcp_server_registry.py`

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

**File:** `<agent-src>/todo_agent_builder.py` or `<agent-src>/deepwork_agent_builder.py`

```python
    def _add_mcp_servers_config(self):
        mcp_server_registry = MCPServerRegistry()
        todo_mcp_server_registry = TodoMCPServerRegistry(self.config_manager)
        mcp_servers_config = [
            todo_mcp_server_registry.get_clockwise_fastmcp_server(),
        ]
        self.add_mcp_servers_config(mcp_servers_config)
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

Optionally, you can use [MCP inspector](https://github.com/modelcontextprotocol/inspector) to test or to understand the contract of Tools provided by MCP servers.

Now create the higher order tool that wraps the MCP server with custom logic.

**File:** `<agent-src>/higher_order_tools/calendar/clockwise_higher_order_tool.py`

```python

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
```


---

## Step 3: Register Higher Order Tool

Add higher order tool to an existing or new agent. If you're extending an existing Agent, make these changes in `todo_agent_builder.py`. If you're building a new agent by following [GUIDE_BUILD_AN_AGENT.md](GUIDE_BUILD_AN_AGENT.md), make these changes in `deepwork_agent_builder.py`

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
# Test prompts:
> Schedule a deep work session today
> Schedule a focus session today
> Schedule a deep work meeting at 2 PM today for 90 minutes
```

## Next Steps

- Check out [Guide to Build a new deepwork agent](./GUIDE_BUILD_NEW_DEEPWORK_AGENT.md)

---