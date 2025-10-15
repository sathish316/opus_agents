## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `uv run pytest`
5. Submit a pull request

## Development

**Adding New Custom Tools:**

Check custom_tools_manager.py for steps to add your own custom tools

**Adding New Higher order Tools:**

Higher order tools are a special type of custom tools that add functionalities to existing MCP tools.
Check higher_order_tools_manager.py for steps to add your own custom tools

**Adding Sub-Agents:**

Check zoom_tools.py and zoom_assistant.py for patterns to add Sub-Agent with its own model, prompts etc.
Similar patterns are used in multiple places

