# Opus Agents

Opus Agents is an Open-source Agentic AI framework that comes with a collection of AI agents and Custom/Personalized tools to supercharge your productivity in different areas like Productivity tools, Collaboration tools, Software development etc.

It is inspired by the views of Neil DeGrasse Tyson in his Podcast "Why AI is overrated" - https://www.youtube.com/watch?v=BYizgB2FcAQ. TLDR - AI is expected to bring exponential growth and superpowers similar to Humanity's transition from Horses to Cars. Humanity has always been in exponential growth phase ever since the start of Industrial revolution and Internet or AI is no different. The current viewpoints on AI fall either on the spectrum that "AI will replace humans" or on the other end of the spectrum that "AI is a stochastic parrot". Neil DeGrasse Tyson takes a balanced view that AI will bring the superpowers of Jarvis to every human and trigger the next phase of Exponential growth.

Opus Agents is an attempt to make the tools we use everyday for Productivity, Collaboration, Software development etc feel almost like Jarvis. It's features are:
* Productivity tools
   * Todo lists - Asking your Todo lists what you did yesterday, last week, help you plan your day and to help you do Task prioritization according to your custom workflows
   * Notetaking - Ask questions to your notes
* Collaboration software
   * Google Calendar - Find out where your time is going and optimize your meetings
   * Slack - Catch up on team-specific and project-specific Slack channels without being in a deluge by Slack messages
   * Gmail - Catch up on important emails quickly, categorize emails and don't get bogged down by Inbox Zero
   * Clockwise - Same as Google Calendar, but more powerful
   * Zoom / Loom - Skip that meeting and ask follow-up questions to your meeting transcripts directly
* Software development
   * More powers coming soon...
* Security
   * All of this comes with Data security built in. You can only Authenticate and Authorize tools that are approved by your Workplace admin or by Remote MCP servers or by yourself using OAuth
   * The data does not leave your laptop and some of the sensitive tools/features can run only using Local LLMs like gpt-oss, Qwen3, Ollama3 etc

If you don't find a software or tool that you use everyday, It is meant to be a hackable framework to add customizations that suit your day-to-day workflows.

The name is inspired by the latin phrase "magnum opus" that means "great work". 

Check out Setup and User guide in TOLINK.
Check out Contribution guide in TOLINK

## Features

Opus Agents comes with the following generic features that work across all tools:
* Framework for AI Agents for managing orchestration, Models, MCP servers, Custom tools, Higher order tools, Prompts etc 
* CLI for Agents
* CLI for Admin features and Slash commands like Config
* Model management using Frontier models by OpenAI, Anthropic
* Model management using Local models like gpt-oss, Qwen3, Ollama3 for protecting secure data
* MCP server integrations
* Config management to enable/disable any category or MCP server or custom tool
* Prompt library to help you optimize your workflows in Productivity, Collaboration, Software development etc.
* Custom tools and Higher order tools for Productivity, Collaboration, Software development etc.
* Coming soon - Plugins to build and add tools that suit your custom workflows
* Coming soon - Integration with your existing AI tools like Cursor, Claude code etc
* Coming soon - Using Local LLMs end-to-end

Opus Agents enhances Productivity software to do the following:
- **✅ Todo Lists (Todoist)**: Daily/Weekly review of completed tasks, Plan your day using Task prioritization techniques
- **📝 Notetaking (Obsidian)**: Index your notes, Ask questions to your notes

Opus Agents enhances Collaboration software to do the following:
- **📧 Gmail**: Coming soon
- **📅 Calendar (Google calendar, Clockwise)**: Ask questions about your past meetings (yesterday or last week) to find out where your time is going, Optimize your future meetings to spend more time doing Deep work
- **💬 Chat (Slack)**: Catch up on Slack channels for a team for any duration (last one day, one week, x days/weeks), Convert Slack mentions for important messages to Todo list action items
- **🎥 Meeting recorders (Zoom/Loom)**: Ask follow-up questions to meeting transcripts to find out what was decided.

For Setup and User guide, check out TOLINK.

If your favourite software or custom workflow is not present here, please see the Contributing guide TOLINK and raise a Pull request


## Installation and User Guide

TOLINK

## Development and Contributing Guide

TOLINK

## Tech stacks

Tech stacks used are:
1. Language - Python
2. Agent orchestration - PydanticAI
3. CLI - PydanticAI CLI
4. Admin CLI - Typer
5. Vector store - Chromadb
6. MCP servers and clients - PydanticAI and FastMCP

## LICENSE

TOLINK

