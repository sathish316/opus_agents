### Setup

Install dependencies in pyproject.toml
$ uv sync

$ source .venv/bin/activate

### Start jupyter notebook

$ uv run jupyter lab

or

$ uv run jupyter lab --app-dir /opt/homebrew/share/jupyter/lab


### LangGraph - Agent framework primitives explored

1. Agent with System prompt and String interpolation

langgraph_agent_with_system_prompt.ipynb

2. Agent with Function tool

$ source .venv/bin/activate
$ python langgraph_agent_with_weather_function_tool.py

3. Conversational memory

langchain_langgraph_chatbot_starter.ipynb

langgraph_conversational_memory.ipynb

4. Structured output

langgraph_structured_output.ipynb

6. Agent with Local MCP server tools

$ source .venv/bin/activate
$ python langgraph_mcp_starter.py

### Contribute

Clear jupyter output before check-in:

$ jupyter nbconvert --clear-output --inplace *.ipynb