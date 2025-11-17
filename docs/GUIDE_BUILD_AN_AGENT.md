# Guide: Build a DeepWork Scheduling Agent

## Overview

This guide walks you through creating a complete DeepWork Scheduling Agent that helps you manage and schedule focused work sessions. The agent combines:
- **Todoist Custom Tool**: Query tasks tagged with "deepwork"
- **Clockwise Higher Order Tool**: Schedule deep work sessions on your calendar

By the end of this guide, you'll have a fully functional agent that can:
- Find your deep work tasks from Todoist
- Schedule them on your calendar using Clockwise
- Provide intelligent scheduling recommendations

---

## Prerequisites

Before starting, ensure you have:
- Completed the [Installation and User Guide](../USER_GUIDE.md)
- Todoist API key (set as `TODOIST_API_KEY` environment variable)
- Clockwise account
- Familiarity with:
  - [Guide: Adding a Custom Tool](./GUIDE_ADD_CUSTOM_TOOL.md)
  - [Guide: Adding a Higher Order Tool](./GUIDE_ADD_HIGHER_ORDER_TOOL.md)

---

## Create an Opus Agent

The DeepWork Agent consists of:
* opus_deepwork_agent/deepwork_agent_builder.py
* opus_deepwork_agent/deepwork_agent_runner.py
* opus_deepwork_agent/deepwork_mcp_server_registry.py

System prompts are specified in `prompts/agent/DEEPWORK_AGENT_INSTRUCTIONS.md`
Configuration is in `opus-config.yaml`

---

## Step 1: Initialize Agent package

```bash
mkdir -p opus_deepwork_agent/src/opus_deepwork_agent
cd opus_deepwork_agent
uv init .
```

```pyproject.toml
[project]
name = "opus-deepwork-agent"
version = "0.1.0"
description = "DeepWork Agent for managing and scheduling focused work sessions"
requires-python = ">=3.12"
dependencies = [
    "opus-agent-base",
]

[project.scripts]
opus-deepwork-agent = "opus_deepwork_agent:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/opus_deepwork_agent"]
```

---

## Step 2: Add MCP servers

For the DeepWork agent, add Clockwise MCP server

**File:** `<agent-src>/deepwork_mcp_server_registry.py`

```python
class DeepWorkMCPServerRegistry:
    """Registry for DeepWork agent MCP servers"""

    def __init__(self, config_manager):
        self.config_manager = config_manager

    def get_clockwise_fastmcp_server(self) -> FastMCPServerConfig:
        """
        Configure Clockwise MCP server
        """
        return FastMCPServerConfig(
            "clockwise",
            "deepwork.calendar.clockwise",
            {
                "transport": "streamable-http",
                "url": "https://mcp.getclockwise.com/mcp",
                "tool_prefix": "clockwise",
                "auth": "oauth",
            }
        )
```

## Step 3: Add custom tools

Follow Custom tool guides to add Todoist tool and Clockwise tool to your Agent
* [GUIDE_ADD_CUSTOM_TOOL.md](GUIDE_ADD_CUSTOM_TOOL.md)
* [GUIDE_ADD_HIGHER_ORDER_TOOL.md](GUIDE_ADD_HIGHER_ORDER_TOOL.md)

---

## Step 4: Agent System Prompt

Define the agent's system prompt and instructions

**File:** `prompts/agent/DEEPWORK_AGENT_INSTRUCTIONS.md`

```markdown
# DeepWork Agent Instructions

You are a DeepWork Agent, specialized in helping users manage and schedule focused work sessions.

## Your Core Capabilities

1. **Task Management**
   - Query deep work tasks from Todoist
   - Filter tasks by project or tag
   - Provide task summaries and priorities

2. **Calendar Scheduling**
   - Schedule deep work sessions on Clockwise calendar
   - Find optimal time slots for focused work
   - Respect working hours and preferences

## Interaction Guidelines

- Be proactive in suggesting when to schedule deep work tasks
- Always confirm before scheduling events on the calendar
- Provide clear summaries of tasks and scheduled sessions

## Deep Work Philosophy

Deep work requires uninterrupted focus. When scheduling:
- Prefer slots as per User preferences
- Suggest minimum 60-90 minute blocks
- Avoid back-to-back meetings
- Respect user's working hours and timezone
```

---

## Step 5: Define DeepWork Agent using AgentBuilder and AgentRunner

AgentBuilder configures all components: prompts, MCP servers, custom tools, and higher order tools.
Extend AgentBuilder to create a DeepWorkAgentBuilder

**File:** `<agent-src>/deepwork_agent_builder.py`

```python
class DeepWorkAgentBuilder(AgentBuilder):
    """Builder for DeepWork Agent"""

    def __init__(self, config_manager: ConfigManager):
        super().__init__(config_manager)

    def build(self) -> AgentBuilder:
        """Build the DeepWork agent with all components"""
        self._add_mcp_servers_config()
        return self

    def _add_mcp_servers_config(self):
        """Add FastMCP servers (Clockwise for calendar)"""
        mcp_server_registry = MCPServerRegistry()
        deepwork_mcp_server_registry = DeepWorkMCPServerRegistry(self.config_manager)
        mcp_servers_config = [
            mcp_server_registry.get_datetime_mcp_server(),
            deepwork_mcp_server_registry.get_clockwise_fastmcp_server(),
        ]
        self.add_mcp_servers_config(mcp_servers_config)
```

AgentRunner runs your Agent.

**File:** `<agent-src>/deepwork_agent_runner.py`

```python
async def run_deepwork_agent():
    """Run DeepWork Agent using AgentRunner"""
    logger.info("🎯 Starting DeepWork Agent")

    # Build DeepWork Agent
    config_manager = ConfigManager()
    deepwork_agent = (
        DeepWorkAgentBuilder(config_manager)
        .name("deepwork-agent")
        .set_system_prompt_keys(["opus_agent_instruction", "deepwork_agent_instruction"])
        .add_instructions_manager()
        .add_model_manager()
        .instruction(
            "opus_agent_instruction", "prompts/agent/OPUS_AGENT_INSTRUCTIONS.md"
        )
        .instruction(
            "deepwork_agent_instruction", "prompts/agent/DEEPWORK_AGENT_INSTRUCTIONS.md"
        )
        .custom_tool(TodoistTools())
        .higher_order_tool(ClockwiseHigherOrderTool())
        .build()
    )

    # Run DeepWork Agent
    agent_runner = AgentRunner(deepwork_agent)
    await agent_runner.run_agent()
```

If you need more control to define your Agent instead of the builder pattern, you can add all capabilities to the agent in build method

```python
class DeepWorkAgentBuilder:
    """Builder for DeepWork Agent"""

    def _add_mcp_servers(self):
        """Add FastMCP servers (Clockwise for calendar)"""
        mcp_server_registry = MCPServerRegistry()
        deepwork_mcp_server_registry = DeepWorkMCPServerRegistry(self.config_manager)
        mcp_servers_config = [
            mcp_server_registry.get_datetime_mcp_server(),
            deepwork_mcp_server_registry.get_clockwise_fastmcp_server(),
        ]
        self.mcp_manager.add_fastmcp_servers(mcp_servers_config)

    def _add_custom_tools(self):
        """Add custom tools (Todoist for task management)"""
        self.custom_tools: list[CustomTool] = [
            TodoistTools(),
        ]

    def _add_higher_order_tools(self):
        """Add higher order tools (Clockwise for smart scheduling)"""
        self.higher_order_tools: list[HigherOrderTool] = [
            ClockwiseHigherOrderTool(),
        ]
```

---

## Step 6: Configure the Agent

Add configuration for the DeepWork agent in your main config file.

**File:** `opus-config.yaml`

```yaml
# Agent Configuration
agent:
  name: "deepwork-agent"
  description: "DeepWork Agent for managing focused work sessions"

# Model Configuration
model_config:
  - provider: "openai"
    model: "gpt-5"
    enabled: true

# MCP Server Configuration
mcp_config:
  general:
    datetime:
      enabled: true
  deepwork:
    todo:
      todoist:
        enabled: true
    calendar:
      clockwise:
        enabled: true
        higher_order_tools_enabled: true

# Environment Variables (set these in your shell)
# export TODOIST_API_KEY="your_todoist_api_key"
# Clockwise uses OAuth, no API key needed
```

---

## Step 7: Create main to run DeepWorkAgent and run the agent

```python
def main():
    """Entry point for the Opus Agents CLI."""
    try:
        app = create_cli_app(
            agent_name="Opus Deepwork Agent",
            agent_description="Deepwork Scheduling Agent",
            agent_version="0.1.0",
            agent_runner=run_deepwork_agent,
        )
        app()
    except Exception as e:
        logger.error(f"Fatal error in main: {type(e).__name__}: {e}")
        logger.error(f"Full traceback:\n{traceback.format_exc()}")
        raise


if __name__ == "__main__":
    main()
```

Run the Agent


```bash
uv run main.py
```

Another option is to install DeepWork agent globally and run from anywhere
```bash
uv tool install .
opus-deepwork-agent
```

Test DeepWorkAgent with these prompts:

> What deep work tasks do I have today?

> Schedule my top priority deep work task for today on calendar

> Suggest timeslots between 9AM to 6PM for 90 minutes when i can do this task = "Foo". If a slot is available, schedule it on my calendar