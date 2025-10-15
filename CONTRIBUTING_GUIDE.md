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