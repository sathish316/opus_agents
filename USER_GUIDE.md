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

5. Configure which model to use

Frontier models can be configured in ~/.opusai/config.yaml
```
model_config.enabled=true (where provider="openai", model="gpt-5")
```

Local models can also be configured and enabled in ~/.opusai/config.yaml
```
model_config.enabled=true (where provider="ollama", model="qwen3:1.7b-q8_0", is_local=true)
```

6. Start Opus CLI

```bash
$ uv run opus_todo_agent/main.py
```

# Test with a simple command
> Find open tasks in my todoist project Test

7. Install Opus CLI globally and start it - FIXME

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

The power of OpusCLI is in the advanced workflows that it supports to suit your needs. For custom tools and workflows possible with Todoist, check Custom Tools and Prompt library section

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

For advanced tools and workflows possible with Obsidian, check Custom Tools and Prompt library section

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

4. Google workspace MCP requires an Stdio transport version of MCP to be configured.
Clone this repo and configure an environment variable for Google workspace MCP to work.

http://github.com/taylorwilsdon/google_workspace_mcp

```
GOOGLE_WORKSPACE_MCP_PATH=/path/to/google_workspace_mcp
OAUTHLIB_INSECURE_TRANSPORT=1
```

5. Test Google Calendar from OpusCLI

OpusCLI> What meetings do i have tomorrow?

6. Complete the OAuth handshake flow in your browser

7. For advanced tools and workflows possible with Google Calendar, check Custom Tools and Prompt library section

### Calendar - Clockwise

### Chat - Slack
1. Enable Slack in ~/.opusai/opus-config.yaml
```
mcp_config.productivity.chat.slack.enabled=true
```

2. Slack supports 2 different auth methods. Follow the below guide to get XOXC and XOXD token:
https://github.com/korotovsky/slack-mcp-server/blob/master/docs/01-authentication-setup.md

Enable xoxc in config:
```
mcp_config.productivity.chat.slack.auth_method: "xoxc"
```

Configure tokens in ENV
```
SLACK_MCP_XOXC_TOKEN=<your-token>
SLACK_MCP_XOXD_TOKEN=<your-token>
```

The disadvantage of xoxc and xoxd is that they need to be frequently updated.

3. For other auth methods, Slack integration works only if your workplace admin supports installation of custom apps. Perform the following steps to get the Auth config required for XOXP token:
https://github.com/korotovsky/slack-mcp-server/blob/master/docs/01-authentication-setup.md

Enable xoxp in config:
```
mcp_config.productivity.chat.slack.auth_method: "xoxp"
```

Configure tokens in ENV:
```
SLACK_MCP_XOXP_TOKEN=<your-token>
```

4. For advanced features, OpusCLI supports the following config for Slack to tell Opus about your specific teams and projects and their corresponding Slack channels:

```
chat.slack.project_to_channels.phoenix=["phoenix-dev","phoenix-product"]
chat.slack.team_to_channels.neo=["neo-dev","neo-alerts"]
```

5. OpusCLI supports Local LLMs to secure Slack data. In order to use Local LLM with Slack, configure:

```
chat.slack.use_local_model=true
```

6. Test Slack from OpusSLI

OpusCLI> Update me on the recent messages in Test slack channel in last one week

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

