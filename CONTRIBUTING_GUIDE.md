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

Use `SubagentAsTool` from `opus_agent_base.tools.subagent_as_tool` to wrap a PydanticAI subagent and call it from a parent agent tool. See existing usages in `zoom_meeting_assistant.py`, `slack_assistant.py`, and `obsidian_rag.py`.

**Adding New Agent:**

[GUIDE_BUILD_AN_AGENT.md](docs/GUIDE_BUILD_AN_AGENT.md)
