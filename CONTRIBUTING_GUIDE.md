## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `uv run pytest`
5. Submit a pull request

## Tech stacks

Tech stacks used are:
1. Language - Python
2. uv
3. Agent orchestration - PydanticAI
4. CLI - PydanticAI CLI and Typer
5. Vector store - Chromadb
6. MCP servers and clients - FastMCP

## Development

**Adding New Custom Tools:**

[GUIDE_ADD_CUSTOM_TOOL.md](docs/GUIDE_ADD_CUSTOM_TOOL.md)

**Adding New Higher order Tools:**

[GUIDE_ADD_HIGHER_ORDER_TOOL.md](docs/GUIDE_ADD_HIGHER_ORDER_TOOL.md)

**Adding Sub-Agents:**

Check zoom_tools.py and zoom_assistant.py in opus_todo_agent for patterns to add Sub-Agent with its own model, prompts etc.
Similar patterns are used in multiple places

**Adding New Agent:**

[GUIDE_BUILD_AN_AGENT.md](docs/GUIDE_BUILD_AN_AGENT.md)
