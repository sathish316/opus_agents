# Opus Agents

## Overview

Opus Agents is an open-source Agentic AI framework and toolkit, that helps you build AI Agents and configure Tools easily.

The goal of the framework is to build Agents and Tools that can be used in a more predictable and reliable way, compared to just adding MCP servers to Agents or other AI tools like Claude Desktop, Cursor etc. It reduces Context pollution from multiple MCP servers/tools and improves Tool selection accuracy using abstractions like Custom tool, Higher order tool, Meta tool etc.

Example of an Agent built with OpusAgents framework:
```python
    # Build DeepWork Scheduling Agent
    config_manager = ConfigManager()
    deepwork_agent = (
        DeepWorkAgentBuilder(config_manager)
        .name("deepwork-agent")
        .set_system_prompt_keys(["opus_agent_instruction", "deepwork_agent_instruction"])
        .add_instructions_manager()
        .add_model_manager()
        .custom_tool(TodoistTools())
        .higher_order_tool(ClockwiseHigherOrderTool())
        .build()
    )

    # Run DeepWork Scheduling Agent
    agent_runner = AgentRunner(deepwork_agent)
    await agent_runner.run_agent()
```

OpusAgents has bundled AI Agents and Tools for specific domains. OpusTodoAgent is a bundled Agent that focuses on Productivity & Collaboration software using Google Calendar, Slack, Zoom, Todo lists, Notes etc

The goal of OpusTodoAgent is to make the software we use everyday for Productivity, Collaboration, Software development etc more seamless and predictable/reliable - almost like having your own Jarvis. To see how OpusTodoAgent is more seamless than using Cursor or ClaudeDesktop with MCP servers for certain use cases, refer to [docs/COMPARE_CURSOR_MCP_VS_OPUS.md](docs/COMPARE_CURSOR_MCP_VS_OPUS.md). 

Both the framework and bundled Agents are extensible/hackable, making it easy to extend them to suit your unique workflows and frequently used software. 

## OpusAgents Framework - Getting started

OpusAgents framework can be used to build your own Tools or build your own Agent. Refer to the following guides to get started:
* **[Build a custom tool](docs/GUIDE_ADD_CUSTOM_TOOL.md)** - Custom tools extend the capability of Agent, similar to function tools
* **[Build a higher order tool](docs/GUIDE_ADD_HIGHER_ORDER_TOOL.md)** - Higher order tools are capabilities on top of one or more existing MCP servers/tools, to make them easier to use for the Agent.
* TODO:Meta tool - Meta tools are re-usable tools on top of existing patterns like OpenAPI specs, Bash scripts, Scraping tools etc
* **[Build an agent](docs/GUIDE_BUILD_AN_AGENT.md)** - 

The framework is built on top of [PydanticAI](https://ai.pydantic.dev/) and [FastMCP](https://gofastmcp.com/)

## OpusTodoAgent - Getting started

Read Setup and User guide in [Installation and User Guide](docs/USER_GUIDE.md) to use OpusAgents with Productivity/Collaboration software like Google Calendar, Slack, Todoist, Obsidian, Zoom etc.

Read [Contributing Guide](CONTRIBUTING_GUIDE.md) for development and contributing features to the framework or bundled tools.

## OpusAgents Framework - Features

* Manage AI Agents orchestration, Models, MCP servers, Custom tools, Higher order tools, Prompts
* CLI for Agents, CLI for Slash commands
* Config management
* Prompt management
* Model management using Frontier models and Local LLMs like gpt-oss, Qwen3, Ollama3
* MCP server integrations
* Custom tools and Higher order tools that enhance MCP servers
* Coming soon - Plugins, Integration with existing AI tools like Cursor/ClaudeDesktop, Local models end-to-end

## OpusTodoAgent - Features

Key features for Productivity & Collaboration tools are:
* Productivity
   * Todo lists - Daily & weekly reviews, Your custom GTD or task prioritization framework
   * Notetaking - Index and Ask questions to your notes
* Collaboration
   * Google Calendar or Clockwise - Get meeting briefings, schedule deep work, optimize your calendar
   * Slack - Catch up on team/project specific channels
   * Zoom or Loom - Ask follow-up questions to meeting transcripts
   * Gmail (Coming soon) - Apply your own personal workflows to achieve Inbox Zero
* Security
   * Built-in data security ensures you can only authenticate and authorize tools through workplace-approved methods and OAuth
   * Sensitive data can be configured to run exclusively on Local LLMs such as gpt-oss, Qwen3, Ollama3.

## Installation and User Guide

[Installation and User Guide](docs/USER_GUIDE.md)

## Development and Contributing Guide

[Contributing Guide](CONTRIBUTING_GUIDE.md)

If your favourite software or custom workflow is not present here, please see the [Contributing Guide](CONTRIBUTING_GUIDE.md) and raise a Pull request

## License

Opus Agents is designed to be a customizable and hackable framework.
The project will remain open source under the [MIT LICENSE](LICENSE.md)

## About / Inspiration

Opinions on AI range from extremes that "AI will replace humans" or "AI in its current state is next token prediction and not intelligence". This project draws inspiration from Neil DeGrasse Tyson's balanced perspective on AI from his podcast (https://www.youtube.com/watch?v=BYizgB2FcAQ). He suggests that society is already living on an exponential curve, since the days of Industrial Revolution to Automobiles to Internet and AI will drive the next wave of exponential growth through human productivity. We are already seeing glimpses of this in AI Coding tools like Cursor and Coding CLIs. For this vision to become possible in all areas, AI has to be a Jarvis-like companion for most knowledge-workers. OpusAgents is an attempt to make the interactions between AI and Software/Tools used by knowledge workers as seamless, customizable, predictable/reliable and Jarvis-like as possible.

The name is inspired by the latin phrase "magnum opus" that means "great work". 


