# Opus Agents

## Overview

Opus Agents is an open-source agentic AI framework/toolkit. Its goal is to make the tools we use everyday for Productivity, Collaboration, Software development etc feel almost like Jarvis and more predictable/reliable/secure than using an LLM with MCP servers.

It is a combination of a framework for building Multi-agent systems/tools and a collection of AI agents and custom/higher-order tools for specific domains like Productivity and Software Engineering. The USP of Opus Agents is the capabilities it provides beyond adding MCP servers to Claude Desktop, Cursor etc.

The framework is extensible/hackable and allows you to add and customize your frequently-used software and tools to match your unique workflows. It is built using [PydanticAI](https://ai.pydantic.dev/) and [FastMCP](https://gofastmcp.com/).

## Getting started

Check out Setup and User guide in [Installation and User Guide](USER_GUIDE.md)

Check out [Contributing Guide](CONTRIBUTING_GUIDE.md) for development and contributing features to the framework or domains

## Framework - Features

Opus Agents framework has the following Key features:
* Manage AI Agents orchestration, Models, MCP servers, Custom tools, Higher order tools, Prompts
* CLI for Agents, CLI for Slash commands
* Config management
* Prompt management
* Model management using Frontier models and Local LLMs like gpt-oss, Qwen3, Ollama3
* MCP server integrations
* Custom tools and Higher order tools that enhance MCP servers
* Coming soon - Plugins, Integration with existing AI tools like Cur, Local models end-to-end

## Productivity Agents - Features

Key features for Productivity & Collaboration tools are:
* Productivity
   * Todo lists - Prioritize Tasks according to your custom workflows. Daily/Weekly review of completed or pending tasks
   * Notetaking - Index and query your personal notes
* Collaboration
   * Google Calendar or Clockwise - Optimize your calendar based on your preferences
   * Slack - Catch up on team-specific and project-specific Slack channels
   * Gmail - Apply your own personal workflows to achieve Inbox Zero
   * Zoom or Loom - Ask follow-up questions to meeting transcripts
* Security
   * Built-in data security ensures you can only authenticate and authorize tools through workplace-approved methods and OAuth
   * Sensitive data can be configured to run exclusively on Local LLMs such as gpt-oss, Qwen3, Ollama3.

## Software Engineering Agents - Features

Coming Soon

## Installation and User Guide

[Installation and User Guide](USER_GUIDE.md)

## Development and Contributing Guide

[Contributing Guide](CONTRIBUTING_GUIDE.md)

If your favourite software or custom workflow is not present here, please see the [Contributing Guide](CONTRIBUTING_GUIDE.md) and raise a Pull request

### Guide to Add Custom tools

### Guide to Add Higher-order tools

## License

Opus Agents is designed to be a customizable and hackable framework.
The project will remain open source under the [MIT LICENSE](LICENSE.md)

## About / Inspiration

Opinions on AI range from extremes that "AI will replace humans" or "AI in its current state is next token prediction and not intelligence". This project draws inspiration from Neil DeGrasse Tyson's balanced perspective on AI from his podcast (https://www.youtube.com/watch?v=BYizgB2FcAQ). He suggests that society is already living on an exponential curve, since the days of Industrial Revolution to Automobiles to Internet to Modern computing systems and AI will drive the next wave of human productivity and exponential growth. For this to become possible, AI has to be a Jarvis-like companion for most knowledge workers. Opus Agents is an attempt to make the interactions between AI tools (LLMs, Claude Desktop, Cursor, Coding CLIs) and Software/Tools used by knowledge workers as seamless, customizable and Jarvis-like as possible.

The name is inspired by the latin phrase "magnum opus" that means "great work". 


