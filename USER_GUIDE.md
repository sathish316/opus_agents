# Installation and User Guide

## Prerequisites
1. Install Python3 and uv
https://pypi.org/project/uv/
2. 

## Installation

1. Add API keys for any frontier model to environment
```bash
export OPENAI_API_KEY="your-openai-api-key"
export ANTHROPIC_API_KEY="your-anthropic-api-key"
```

2. To use local models, setup llama.cpp and install a local LLM like gpt-oss or Qwen3

2.1 Install llama.cpp
https://github.com/ggml-org/llama.cpp/blob/master/docs/install.md

2.2 Install 


Run opus_todo_agent for local development
1. **Create virtual environment**:
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   ```

2. **Make code changes and run opus_todo_agent**:
   ```bash
   uv run main.py
   ```

Setup dependencies and install Agent CLI globally:

```bash
# Clone and install everything
./scripts/install-mcp-deps.sh
uv tool install .
```

Test installation:

```bash
which opus-todo-agent

# Run from any directory
opus-todo-agent

# Test with a simple command
> Find open tasks in my todoist project TodoAI?
```

Troubleshooting:

Enable debug mode: `export FASTMCP_LOG_LEVEL=DEBUG` 


## Configuration

### Required Environment Variables

Create a `.env` file or set these environment variables:

```bash
# Required: Choose one or both models
export OPENAI_API_KEY="your-openai-api-key"
export ANTHROPIC_API_KEY="your-anthropic-api-key"
```

### Install MCP Server Dependencies

The agent uses several MCP servers that require additional dependencies:

```bash
./scripts/install-mcp-deps.sh
```

## Usage

### Global Usage (After Installation)

Once installed globally, you can use the agent from any directory:

```bash
# Start the interactive CLI from any project directory
opus-todo-agent
```

### Local Usage

If running locally in the project directory:

```bash
# Using uv
uv run python main.py
```

## Development

### Adding New Tools

To add custom tools to the agent:

```python
@agent.tool_plain
def your_custom_tool() -> str:
    """Description of what your tool does"""
    # Your tool implementation
    return "Tool result"
```

## Architecture and Project structure

## Sub-Agents and Tools

## Prompt Library
* Todoist
** Task management
> Create task 'Order Curtains' in Interior project
** Task search
> Find open tasks in Todoist project Interior
** Task search - custom tools
> Find out all the tasks i completed last week
> Find out all the tasks i completed this week
> Find out all the tasks i completed today
> Find out all the tasks i completed yesterday
** Daily review
> Generate daily review
> Generate daily review, don't summarize
> Generate daily review for 6-Sep-2025
** Weekly review
> Generate weekly review
> Generate weekly review, don't summarize
> Generate weekly review from 1-Sep to 10-Sep
> Generate weekly review for Sep 1st week
** Task recommendation and grouping
> Suggest tasks from the project Interior
> Recommend tasks from the project Interior
> Pick 5 random tasks from the project Interior
> Suggest tasks with the tag deepwork
** Task organizer
> Organize by Todoist Inbox
> Recommend project categories for 20 tasks in Todoist Inbox
** Due, Deadline, Urgent, Important tasks
> TODO - find tasks due today
> TODO - find tasks with deadline today
> TODO - find tasks that are past deadline
> TODO - find tasks with the tag urgent | important | urgent and important

* Google calendar
** Meetings management
> TODO - list all my meetings for today
> TODO - list all my meetings for tomorrow
> list all my meetings for date 1-Sep-2025
** Daily review from accepted meetings
** Weekly review from accepted meetings
** Meetings optimizer - batching, focus time etc
** Meetings metrics - percentage of time spent in meetings on a given day
```

## Configure integrations

### Configure Todoist
TODO: steps for Todoist API key

### Configure Google calendar
TODO: Steps for Google calendar oauth client key and client secret from https://lobehub.com/mcp/199-mcp-mcp-google#setup

Configure the following env variables for Google calendar MCP to work
GOOGLE_OAUTH_CLIENT_ID=*
GOOGLE_OAUTH_CLIENT_SECRET=*
GOOGLE_WORKSPACE_MCP_PATH="/path/to/google_workspace_mcp"
OAUTHLIB_INSECURE_TRANSPORT=1

## Troubleshooting
```bash
export FASTMCP_LOG_LEVEL=DEBUG
export PYDANTIC_AI_LOG_LEVEL=DEBUG
opus-todo-agent
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `uv run pytest`
5. Submit a pull request

## License

[Add your license here]