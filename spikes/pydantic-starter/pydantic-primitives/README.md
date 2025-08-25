### Setup

Install uv dependencies in pyproject.toml
$ uv sync
$ source .venv/bin/activate

### Primitives explored:

The following Agent framework primitives are explored in this spike:
1. Agent with Prompt
$ python hello_world.py

2. Agent with function tools
$ python dice_tool_agent.py

3. Agent with tools to connect to Database
$ python banksupport_database_agent.py

4. Agent with tools to call HTTP APIs
$ python weather_http_agent.py

5. Agent with Primitive TypedInput and TypedOutput
$ python roulette_agent.py

6. Structured Output extraction
$ python structured_output_agent.py

7. Dynamic system prompt
$ python dynamic_system_prompt_agent.py

8. Dynamic instructions
$ python dynamic_instruction_agent.py

9. Conversational memory (In-memory)
$ python conversational_memory_agent.py





