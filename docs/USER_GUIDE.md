# Installation and User Guide

## Prerequisites
1. Install Python3 and uv
https://pypi.org/project/uv/

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
cp opus_todo_agent/common/opus-config.sample.yml ~/.opusai/opus-config.yml
```

5. Configure which model to use

Frontier models can be configured in ~/.opusai/config.yml
```
model_config.enabled=true (where provider="openai", model="gpt-5")
```

Local models can also be configured and enabled in ~/.opusai/config.yml
```
model_config.enabled=true (where provider="ollama", model="qwen3:1.7b-q8_0", is_local=true)
```

6. Start Opus CLI

```bash
$ uv run main.py
```

7. Test with a simple command
> Find open tasks in my todoist project Test

8. Install Opus CLI globally and start it - FIXME

```bash
uv tool install .
```

Test installation:

```bash
which opus-agents

# Run from any directory
opus-agents

# Run a specific agent
opus-agents -todo

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
uv run main.py
```

# Productivity tools Usage - Todo, Notetaking

## Todoist
1. Enable Todoist in ~/.opusai/opus-config.yml
```
mcp_config.productivity.todo.todoist.enabled=true
```

2. Add your todoist API key to env variables
```
TODOIST_API_KEY="your-api-key"
```

3. Start/Restart OpusCLI

```
uv run main.py
```

4. Test Todoist from OpusCLI

OpusCLI> Find open tasks in Test project (in Todoist)

> Generate daily review of Todoist tasks

> Generate weekly review of Todoist tasks

The power of OpusCLI is in the advanced workflows that it supports to suit your needs. For custom tools and workflows possible with Todoist, check Custom Tools and Prompt library section

<img src="demo/opus/opus_todoist_2025-11-15 17.20.27.gif">

## Obsidian
Obsidian is a notetaking tool.
Opus Agents support indexing your notes one-time or periodically and asking questions to your notes

1. Enable Obsidian in ~/.opusai/opus-config.yml
```
mcp_config.productivity.notes.obsidian.enabled=true
```

2. Configure your vault name and location in ~/.opusai/opus-config.yml
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
 uv run opus_todo_agent/src/opus_todo_agent/background_jobs/notes/obsidian_indexer.py my_personal_notes
```

5. Test Obsidian from OpusCLI

OpusCLI> Ask notes - what is X?

For advanced Obsidian workflows, check Custom Tools and Prompt library section

<img src="demo/opus/opus_obsidian_2025-11-15 17.53.32.gif">

# Collaboration tools Usage - Mail, Calendar, Chat, Meetings

## Calendar - Google Calendar

1. Enable Google Calendar in ~/.opusai/opus-config.yml
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
USER_GOOGLE_EMAIL="<your-email>"
```

4. Google workspace MCP requires an Stdio transport version of MCP to be configured.
Clone this repo and configure environment variables for Google workspace MCP to work.

http://github.com/taylorwilsdon/google_workspace_mcp

```
GOOGLE_WORKSPACE_MCP_PATH=/path/to/google_workspace_mcp
OAUTHLIB_INSECURE_TRANSPORT=1
```

5. Test Google Calendar from OpusCLI

OpusCLI> What meetings do i have tomorrow?

> Generate summary of my meetings this week

6. Complete the OAuth handshake flow in your browser

7. The power of OpusCLI is in the advanced Google Calendar workflows that it supports to suit your needs. For advanced tools and workflows possible with Google Calendar, check Custom Tools and Prompt library section

<img src="demo/opus/opus_calendar_1_success_2025-11-16 13.12.48.gif">

## Calendar - Clockwise

In case your Google workspace permission does not allow you to use Google calendar, Clockwise provides Remote MCP servers with access to your Calendar and more optimization tools.

1. Enable Calendar in ~/.opusai/opus-config.yml
A higher order tool is a special type of custom tool that uses the MCP server to build advanced functionalities.

```
mcp_config.productivity.calendar.clockwise.enabled=true
mcp_config.productivity.calendar.clockwise.higher_order_tools.enabled=true
```

2. Clockwise does not require any additional work other than OAuth handshake. Start OpusCLI and Complete the OAuth handshake flow in your browser

3. Test Clockwise from OpusCLI

OpusCLI> What meetings do i have tomorrow?

The power of OpusCLI is in the advanced and hackable Clockwise workflows that it supports to suit your needs. For advanced tools and workflows possible with Clockwise, check Custom Tools and Prompt library section

## Chat - Slack
1. Enable Slack in ~/.opusai/opus-config.yml
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

4. For advanced features, OpusCLI supports the following config to guide Opus about your specific teams and projects and their corresponding Slack channels:

```
chat.slack.project_to_channels.phoenix=["phoenix-dev","phoenix-product"]
chat.slack.team_to_channels.neo=["neo-dev","neo-alerts"]
```

5. OpusCLI supports Local LLMs to secure Slack data. In order to use Local LLM with Slack, configure:

```
chat.slack.use_local_model=true
```

6. Test Slack from OpusSLI

> Update me on the recent messages in Test slack channel

> Brief me about Test project's slack channels from last one week

> Brief me about Test team's slack channels from last one week

<img src="demo/opus/opus_slack_2025-11-16 13.34.44.gif">

## Meetings Recording and Transcript - Zoom and Loom

OpusCLI does not direcly integrate with Zoom or Loom APIs. It expects you to download the transcript in a specific location and uses a Local model to answer follow-up questions about the meeting

1. Enable Zoom or Loom in ~/.opusai/opus-config.yml
```
mcp_config.productivity.meeting_transcript.zoom.enabled=true
mcp_config.productivity.meeting_transcript.loom.enabled=true
```

2. Configure storage directory for meeting trancript
```
meeting_transcript:
  zoom:
    storage_dir: "~/tmp/opusai/data/zoom"
  loom:
    storage_dir: "~/tmp/opusai/data/loom"
```

3. This step is for additional security. Enable local models and token limit for Meeting transcripts. 
```
meeting_transcript:
  zoom:
    use_local_model: true
    max_transcript_size: 32000
  loom:
    use_local_model: true
    max_transcript_size: 32000
```

4. Go to zoom and download meeting transcript to ~/tmp/opusai/data/zoom. Zoom meetings have *.vtt extension. If your meeting is is abc13371337, the filename where the transcript should be stored is ~/tmp/opusai/data/zoom/abc13371337.vtt

To download transcript: Go to zoom.com > Sign-in > Recordings & Transcripts > Click on meeting id > Click on Audio transcript download

5. Go to loom and download meeting transcript to ~/tmp/opusai/data/loom. Loom meetings have *.srt extension. If your meeting is is abc13371337, the filename where the transcript should be stored is ~/tmp/opusai/data/loom/abc13371337.srt

To download transcript: Go to loom.com > Sign-in > Click on meeting > View Recording > Transcript > Download

6. Test Zoom or Loom on OpusAI

> Ask question about meeting id 123 - Summarize the meeting

# Custom Tools and Prompt Library

## Todo > Todoist

```
** Task management
> Create task 'Order Cake' in Birthday project

** Task search
> Find open tasks in Todoist project Birthday
> Find out all the tasks i completed last week / this week / today / yesterday

** Daily review
> Generate daily review of Todoist tasks
> Generate daily review, don't summarize
> Generate daily review for 6-Sep-2025

** Weekly review
> Generate weekly review of Todoist tasks
> Generate weekly review, don't summarize
> Generate weekly review from 1-Sep to 10-Sep / Sep 1st week

** Task recommendation and grouping
> Suggest/Recommend tasks from the project Orion
> Pick 5 random tasks from the project Orion that i can work on
> Suggest tasks with the tag deepwork

** Due, Deadline, Urgent, Important tasks
> TODO - find tasks due today
> TODO - find tasks with deadline today
> TODO - find tasks that are past deadline
> TODO - find tasks with the tag urgent | important | urgent and important
```

## Notes > Obsidian

```
** Chat with your notes
> Ask notes - what is X?
```

## Calendar > Google Calendar, Clockwise

```
** Meeting summary
> Brief me about meetings that I have today / I attended yesterday / are planned for tomorrow
> Brief me about meetings I have this week / I attended last week / I have next week / I have this week
> Brief me about meetings on 1-Sep-2025
> Brief me about meetings from 22-Sep-2025 to 26-Sep-2025

** Daily review of accepted meetings
> Show daily review of my meetings (Defaults to today)
> Show daily review of my meetings for today / yesterday / 1-Sep-2025

** Weekly review of accepted meetings
> Show weekly review of my meetings (Defaults to current week)
> Show weekly review of my meetings for this week / last week / from 1-Sep-2025 to 10-Sep-2025

** Deep work scheduler
> Brief me about my meetings tomorrow. Schedule a deepwork slot for 60 mins for the task - "<insert complex task here>"

** Meetings optimizer - batching, focus time etc
TODO

** Meetings metrics - percentage of time spent in meetings
TODO
```

## Chat > Slack

```
** Catchup on Slack channel
> List my slack channels
> List recent messages in slack channel foo and summarize them
> Brief me about slack channel foo from today / yesterday / custom date (and summarize them)

** Catchup on Project specific slack channels
> Brief me about Bar project's slack channels from last one day / one week / last x days

** Catchup on Team specific slack channels
> Brief me about Bar team's slack channels from last one day / last one week / last x days
```

## Meeting recorder > Zoom or Loom

```
> Ask question about meeting id 123 - what is the final decision on X from this meeting?
```

# Troubleshooting

