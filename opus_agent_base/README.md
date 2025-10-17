# Opus Agent Base

Generic infrastructure for building AI agents with pydantic-ai and MCP integrations.

## Overview

`opus_agent_base` is a reusable framework that provides the core infrastructure for building domain-specific AI agents. It handles agent lifecycle, model management, MCP server integration, configuration, logging, and CLI scaffolding.

## Features

- **Agent Management**: Core agent lifecycle and initialization
- **Model Support**: OpenAI, Anthropic, Ollama, Bedrock providers
- **MCP Integration**: MCP server management and FastMCP client
- **Configuration**: YAML-based config with nested key support
- **CLI Framework**: Admin mode with command history and auto-completion
- **Extensible**: Base classes for custom tools and higher-order tools
- **Logging**: Structured logging with file and console output

## Package Structure

```
opus_agent_base/
├── managers/              # Core management components
│   ├── agent_manager.py   # Agent lifecycle
│   ├── model_manager.py   # Model initialization
│   ├── mcp_manager.py     # MCP server management
│   ├── instructions_manager.py  # Base instructions
│   ├── custom_tools_manager.py  # Custom tools framework
│   └── higher_order_tools_manager.py  # Higher-order tools framework
├── common/                # Configuration and logging
│   ├── config_manager.py
│   ├── nested_config_manager.py
│   ├── config_command_manager.py
│   └── logging_config.py
├── helpers/               # Utility functions
│   ├── datetime_helper.py
│   └── fastmcp_client_helper.py
└── cli/                   # CLI infrastructure
    ├── agent_runner.py
    ├── cli.py
    └── main.py
```

## Usage

### Creating a New Agent

1. **Extend Base Managers**

```python
from opus_agent_base.managers.custom_tools_manager import BaseCustomToolsManager

class MyCustomToolsManager(BaseCustomToolsManager):
    def initialize_tools(self):
        # Register your domain-specific tools
        MyTool().initialize_tools(self.agent)
        logger.info("My custom tools initialized")
```

2. **Use Agent Runner**

```python
from opus_agent_base.cli.agent_runner import AgentInstance
from my_agent.custom_tools_manager import MyCustomToolsManager

# Initialize your agent with domain-specific managers
agent_instance = AgentInstance()
await agent_instance.initialize()
```

3. **Configure Your Agent**

Create `~/.opusai/opus-config.yaml`:
```yaml
model_config:
  - provider: "anthropic"
    model: "claude-sonnet-4-20250514"
    enabled: true

mcp_config:
  general:
    filesystem:
      enabled: true
```

## Components

### Agent Manager
Handles agent initialization, tool inspection, and lifecycle.

### Model Manager
Supports multiple AI providers:
- OpenAI (GPT-4, etc.)
- Anthropic (Claude)
- Ollama (local models)
- AWS Bedrock

### MCP Manager
Manages Model Context Protocol servers:
- Stdio-based MCP servers
- Remote MCP servers
- FastMCP client integration

### Configuration Manager
- YAML-based configuration
- Nested key support (e.g., `mcp_config.general.filesystem.enabled`)
- CLI commands for config management

### CLI Framework
- Admin mode with slash commands
- Command history and auto-completion
- Rich formatted output
- Agent mode for running agents

## Example: Domain-Specific Agent

```python
# my_agent/agent_runner.py
from opus_agent_base.cli.agent_runner import AgentInstance
from opus_agent_base.managers.agent_manager import AgentManager
from my_agent.custom_tools_manager import MyCustomToolsManager
from my_agent.instructions_manager import MyInstructionsManager

class MyAgentInstance(AgentInstance):
    async def initialize(self):
        # Use base initialization with your managers
        self.config_manager = ConfigManager()
        self.model_manager = ModelManager(self.config_manager)
        self.instructions_manager = MyInstructionsManager()
        self.mcp_manager = MCPManager(self.config_manager)
        
        self.agent_manager = AgentManager(
            self.model_manager,
            self.instructions_manager,
            self.mcp_manager,
            self.config_manager,
        )
        self.agent_manager = await self.agent_manager.async_init()
        self.agent = self.agent_manager.get_agent()
        
        # Register your custom tools
        self.custom_tools_manager = MyCustomToolsManager(
            self.config_manager,
            self.instructions_manager,
            self.model_manager,
            self.agent,
        )
        
        return self
```

## Dependencies

- `pydantic-ai>=0.8.1`
- `pydantic-ai-slim[anthropic,openai,retries]>=0.8.1`
- `fastmcp>=2.12.4`
- `typer>=0.19.2`
- `boto3>=1.40.21`
- `tenacity>=8.2.0`
- `httpx>=0.24.0`
- `singleton-decorator>=1.0.0`

## CLI Commands

```bash
# Start agent in interactive mode
opus-agent --agent

# Start in admin mode
opus-agent --admin

# Available admin commands:
/help              # Show help
/agent             # Run agent mode
/config init       # Initialize config
/config list       # List all settings
/config get <key>  # Get setting
/config set <key> <value>  # Set setting
/status            # Show status
/exit              # Exit
```

## Logging

Logs are written to:
- `/var/log/opus_agent_<timestamp>.log` (if writable)
- `~/logs/opus_agent_<timestamp>.log` (fallback)

## License

MIT

## Related Projects

- `opus_todo_agent`: Productivity agent built with opus_agent_base
