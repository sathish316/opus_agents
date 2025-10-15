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

2.2 Run one of these Local LLMs using llama.cpp

```bash
# run gpt-oss
llama-server -hf ggml-org/gpt-oss-20b-GGUF -c 32768

# run Qwen3
llama-server -hf Qwen/Qwen3-1.7B-GGUF:Q8_0 -c 32768

# run Phi3
llama-server -hf microsoft/Phi-3-mini-4k-instruct-gguf -c 32768
```

3. Install or Sync dependencies 

```bash
uv venv
source .venv/bin/activate
```

```bash
uv sync
source .venv/bin/activate
```

4. Initialize config

```bash
mkdir -p ~/.opusai
cp opus_todo_agent/common/opus-config.sample.yaml ~/.opusai/opus-config.yaml
```

5. Start Opus CLI

```bash
$ uv run opus_todo_agent/main.py
```

6. Install Opus CLI globally and start it - FIXME

```bash
uv tool install .
```

Test installation:

```bash
which opus-todo-agent

# Run from any directory
opus-todo-agent

# Test with a simple command
> Find open tasks in my todoist project Test
```

## Usage

### Global Usage (After Installation)

Once installed globally, you can use the agent from any directory:

```bash
# Start the interactive CLI from any project directory
opus-todo-agent
```

### Local Usage

If running from the Git repo

```bash
# Using uv
uv run opus_todo_agent/main.py
```

## Productivity tools Usage - Todo, Notetaking

### Todoist
1. Enable Todoist in ~/.opusai/opus-config.yaml
```
mcp_config.productivity.todo.todoist.enabled=true
```

2. Add your todoist API key to env variables
```
TODOIST_API_KEY="your-api-key"
```

3. Test Todoist from OpusCLI

OpusCLI> Find open tasks in Test project (in Todoist)

(Restart OpusCLI if required)

4. The power of OpusCLI is in the advanced workflows that it supports to suit your needs. For custom tools and workflows possible with Todoist, check Custom Tools and Prompt library section

### Obsidian
Obsidian is a notetaking tool.
Opus Agents support indexing your notes one-time or periodically and asking questions to your notes

1. Enable Obsidian in ~/.opusai/opus-config.yaml
```
mcp_config.productivity.notes.obsidian.enabled=true
```

2. Configure your vault name and location in ~/.opusai/opus-config.yaml
```
notes:
  obsidian:
    default_vault_name: "personal_notes"
    vault_configurations:
      - vault_name: "personal_notes"
        vault_path: "/path/to/personal_notes"
        vector_db_collection: "personal_notes"
        vector_db_path: "/tmp/data/chroma/personal_notes"
        exclude_dirs: ["ignore"]
        exclude_files: ["ignore.md"]
        num_results: 3
```

3. Install chromadb (vector database) to index and chat with your notes
https://docs.trychroma.com/docs/overview/getting-started

4. Index your notes. Opus updates only the changes every time you do this operation. It uses a local embedding model that comes by default in Chromadb and your notes are kept secure

```
 uv run opus_todo_agent/background_jobs/notes/obsidian_indexer.py sathish316_personal
```

5. Test Obsidian from OpusCLI

OpusCLI> Ask notes - what is X?

6. For advanced tools and workflows possible with Obsidian, check Custom Tools and Prompt library section

## Collaboration tools Usage - Mail, Calendar, Chat, Meetings

### Calendar - Google Calendar

1. Enable Google Calendar in ~/.opusai/opus-config.yaml
A higher order tool is a special type of custom tool that uses the MCP server to build advanced functionalities.

```
mcp_config.productivity.calendar.google_calendar.enabled=true
mcp_config.productivity.calendar.google_calendar.higher_order_tools.enabled=true
```

2. Google calendar works only with your personal Gmail account or if your workplace admin supports installation of custom apps. Perform the following steps to get the Auth config required for next step
https://lobehub.com/mcp/199-mcp-mcp-google#setup

3. Set the following ENV variables for Google calendar:
```
GOOGLE_OAUTH_CLIENT_ID="<your-key>"
GOOGLE_OAUTH_CLIENT_SECRET="<your-key>"
GOOGLE_USER_EMAIL="<your-email>"
```

### Configure Google calendar
TODO: Steps for Google calendar oauth client key and client secret from 

Configure the following env variables for Google calendar MCP to work
GOOGLE_OAUTH_CLIENT_ID=*
GOOGLE_OAUTH_CLIENT_SECRET=*
GOOGLE_WORKSPACE_MCP_PATH="/path/to/google_workspace_mcp"
OAUTHLIB_INSECURE_TRANSPORT=1


### Calendar - Clockwise

### Chat - Slack

### Meetings Recording and Transcript - Zoom

### Meetings Recording and Transcript - Zoom

## Custom Tools and Prompt Library

### Todo > Todoist

### Notes > Obsidian

### Calendar > Google Calendar

### Calendar > Clockwise

### Chat > Slack

### Meeting recorder > Zoom

### Meeting recorder > Loom

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

## Troubleshooting

