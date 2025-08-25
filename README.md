# Opus CLI - Feature-Rich CLI Library

A feature-rich CLI library in Python, similar to Cobra in Go, built with Typer and managed with uv.

## Installation

### Option 1: Global Installation (Recommended)

To install Opus CLI globally so you can use the `opus` command from anywhere:

```bash
# Clone or navigate to the project directory
cd /path/to/opus-cli

# Install globally using uv
uv tool install .

# Or if you prefer pip
pip install .
```

After global installation, you can use `opus` from any directory:

```bash
opus --help
opus flow list
opus agent run myagent
```

### Option 2: Development Installation

For development or local testing:

```bash
# Navigate to the project directory
cd /path/to/opus-cli

# Install in development mode
uv pip install -e .

# Activate the virtual environment if needed
source .venv/bin/activate

# Now you can use opus
opus --help
```

### Option 3: Using uv run (No Installation Required)

You can run the CLI directly without installation:

```bash
# From the project directory
uv run python -m opus_cli.cli --help

# Or using the main.py entry point
uv run python main.py --help
```

## Usage

The CLI supports multiple command groups with various subcommands:

### Global Commands
- `opus help` - Show help information
- `opus quit` - Quit the application  
- `opus exit` - Exit the application

### Flow Commands
- `opus flow run <name>` - Run a flow by name
  - `--foo` - Example foo flag
- `opus flow list` - List all available flows
- `opus flow info <name>` - Show information about a specific flow
- `opus flow add <name> --path <path>` - Add a new flow

### Plugin Commands
- `opus plugin list` - List all available plugins
- `opus plugin info <name>` - Show information about a specific plugin
- `opus plugin add --core` - Add a core plugin
- `opus plugin add --community` - Add a community plugin

### Agent Commands
- `opus agent info <name>` - Show information about a specific agent
- `opus agent list` - List all available agents
- `opus agent run <name>` - Run an agent by name

## Examples

```bash
# Run a flow with the foo flag
opus flow run myflow --foo bar

# Add a flow with a specific path
opus flow add myflow --path /path/to/flow

# Add a core plugin
opus plugin add --core

# List all agents
opus agent list

# Get help for any command
opus flow --help
opus plugin add --help
```

## Verification

After installation, verify that Opus CLI is working:

```bash
# Check if opus command is available
opus --version

# View help
opus --help

# Test a command
opus flow list
```

## Troubleshooting

### Command Not Found
If you get "command not found" after global installation:

1. **For uv tool install**: Make sure `~/.local/bin` is in your PATH:
   ```bash
   export PATH="$HOME/.local/bin:$PATH"
   # Add this to your ~/.bashrc or ~/.zshrc for persistence
   ```

2. **For pip install**: The location depends on your Python installation:
   ```bash
   # Find where pip installs scripts
   python -m site --user-base
   # Add /bin to that path in your PATH environment variable
   ```

3. **Check installation**: 
   ```bash
   # For uv
   uv tool list
   
   # For pip
   pip list | grep opus-cli
   ```

## Development

This project uses:
- **uv** for package management
- **Typer** for CLI framework (similar to Cobra in Go)
- **Rich** for beautiful terminal output

### Project Structure

```
opus_cli/
├── __init__.py
├── cli.py           # Main CLI application
└── commands/
    ├── __init__.py
    ├── flow.py      # Flow command implementations
    ├── plugin.py    # Plugin command implementations
    └── agent.py     # Agent command implementations
```

Each command's business logic is separated into its own function in the respective command modules.

### Adding New Commands

1. Add the business logic function in the appropriate command module
2. Register the command in `opus_cli/cli.py`
3. Test the command with `opus <your-command>`

### Building for Distribution

```bash
# Build the package
uv build

# The built package will be in dist/
ls dist/
```