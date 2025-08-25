# MyCLI - Feature-Rich CLI Library

A feature-rich CLI library in Python, similar to Cobra in Go, built with Typer and managed with uv.

## Installation

```bash
# Install dependencies and the CLI in development mode
uv pip install -e .
```

## Usage

The CLI supports multiple command groups with various subcommands:

### Global Commands
- `mycli help` - Show help information
- `mycli quit` - Quit the application  
- `mycli exit` - Exit the application

### Flow Commands
- `mycli flow run <name>` - Run a flow by name
  - `--foo` - Example foo flag
- `mycli flow list` - List all available flows
- `mycli flow info <name>` - Show information about a specific flow
- `mycli flow add <name> --path <path>` - Add a new flow

### Plugin Commands
- `mycli plugin list` - List all available plugins
- `mycli plugin info <name>` - Show information about a specific plugin
- `mycli plugin add --core` - Add a core plugin
- `mycli plugin add --community` - Add a community plugin

### Agent Commands
- `mycli agent info <name>` - Show information about a specific agent
- `mycli agent list` - List all available agents
- `mycli agent run <name>` - Run an agent by name

## Examples

```bash
# Run a flow with the foo flag
mycli flow run myflow --foo bar

# Add a flow with a specific path
mycli flow add myflow --path /path/to/flow

# Add a core plugin
mycli plugin add --core

# List all agents
mycli agent list

# Get help for any command
mycli flow --help
mycli plugin add --help
```

## Development

This project uses:
- **uv** for package management
- **Typer** for CLI framework (similar to Cobra in Go)
- **Rich** for beautiful terminal output

### Project Structure

```
mycli/
├── __init__.py
├── cli.py           # Main CLI application
└── commands/
    ├── __init__.py
    ├── flow.py      # Flow command implementations
    ├── plugin.py    # Plugin command implementations
    └── agent.py     # Agent command implementations
```

Each command's business logic is separated into its own function in the respective command modules.