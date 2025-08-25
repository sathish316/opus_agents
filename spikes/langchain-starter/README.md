### Setup

Install dependencies in pyproject.toml
$ uv sync

$ source .venv/bin/activate

### Start jupyter notebook

$ uv run jupyter lab

or

$ uv run jupyter lab --app-dir /opt/homebrew/share/jupyter/lab

### LangChain - Agent framework primitives explored

1. Pass input in system prompt - String interpolation

langchain_system_and_user_prompt_input.ipynb

2. Pass input in user prompt - String interpolation

langchain_system_and_user_prompt_input.ipynb

3. Model and API key configuration

$ python langchain/langchain_openai_starter.py

4. Agent with Prompt and Tools (Search tool Tavily needs a test API key)

langchain_agent_with_tool_and_memory.ipynb

5. Agent with conversational-memory

langchain_agent_with_tool_and_memory.ipynb

6. Agent with Local MCP server tools

python langchain_mcp_starter.py

7. Conversational memory

langchain_langgraph_chatbot_starter.ipynb

8. ML classification

langchain_classification.ipynb

9. ML Extraction - Structured output extraction

langchain_extraction.ipynb

### Contribute

Clear jupyter output before check-in:

$ jupyter nbconvert --clear-output --inplace *.ipynb