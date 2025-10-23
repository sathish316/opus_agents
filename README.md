# Opus Agents

Opus Agents is an open-source agentic AI framework, featuring a suite of AI agents and custom tools designed to enhance your productivity across multiple domains including productivity apps, collaboration tools, and software development.

Opus Agents is an attempt to make the tools we use everyday for Productivity, Collaboration, Software development etc feel almost like Jarvis. Key features are:
* Productivity tools
   * Todo lists - Ask your Todo lists what you did yesterday, last week, help you plan your day and prioritize Tasks according to your custom workflows
   * Notetaking - Ask questions to your notes
* Collaboration software
   * Google Calendar or Clockwise - Find out where your time is spent in meetings
   * Slack - Catch up on team-specific and project-specific Slack channels
   * Gmail - Catch up on important emails, categorize emails and achieve Inbox Zero
   * Zoom or Loom - Ask follow-up questions to your meeting transcripts
* Software development
   * More powers coming soon...
* Security
   * Built-in data security ensures you can only authenticate and authorize tools through workplace-approved methods, Remote MCP servers, or OAuth
   * Your data remains on your local machine, and sensitive tools/features can be configured to run exclusively with Local LLMs such as gpt-oss, Qwen3, Ollama3.

Opus Agents provides capabilities beyond simply integrating MCP tools into Cursor. As an extensible and hackable framework, it allows you to add and customize your frequently-used software and tools to match your unique daily workflows. It is built using [PydanticAI](https://ai.pydantic.dev/) and [FastMCP](https://gofastmcp.com/).

Check out Setup and User guide in [Installation and User Guide](USER_GUIDE.md)

Check out [Contributing Guide](CONTRIBUTING_GUIDE.md)

## Core Features

Opus Agents comes with the following generic features that work across all tools:
* Framework for AI Agents for managing orchestration, Models, MCP servers, Custom tools, Higher order tools, Prompts etc 
* CLI for Agents, CLI for Slash commands like Config
* Model management using Frontier models by OpenAI, Anthropic. Model management using Local models like gpt-oss, Qwen3, Ollama3
* MCP server integrations
* Custom tools and Higher order tools that enhance MCP servers
* Config management to enable/disable any category or MCP server or custom tool
* Prompt library to customize your workflows
* Coming soon - Plugins, Integration with existing AI tools, Local modeld end-to-end and more

## Installation and User Guide

[Installation and User Guide](USER_GUIDE.md)

## Development and Contributing Guide

[Contributing Guide](CONTRIBUTING_GUIDE.md)

If your favourite software or custom workflow is not present here, please see the [Contributing Guide](CONTRIBUTING_GUIDE.md) and raise a Pull request

## License

Opus Agents is designed as a highly customizable and hackable framework.
The project will remain open source under the [MIT LICENSE](LICENSE.md)

## About / Inspiration

The world is filled with polarized opinions on AI that either "AI will replace all humans" or "AI or LLM in its current state is next token prediction and not intelligence". This project draws inspiration from Neil DeGrasse Tyson's balanced perspective on AI from his podcast "Why AI is overrated" (https://www.youtube.com/watch?v=BYizgB2FcAQ). He suggests that society is already living on an exponential curve from Industrial Revolution to Automobiles to Internet to Modern computing systems and AI will drive the next wave of human creativity, productivity, and exponential growth. For this to become possible, AI has to be like Jarvis for most knowledge work. This project aims to fill the gaps of current AI tools to make them feel almost like Jarvis.

The name is inspired by the latin phrase "magnum opus" that means "great work". 


