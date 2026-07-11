# Agent Core Specification

## Purpose
Provide the core agent runtime: an interactive CLI that assembles a PydanticAI-based agent from its managers (model, MCP servers, custom tools, higher-order tools, instructions) and runs user conversations.

## Requirements

### Requirement: Interactive Agent CLI
The system SHALL provide an interactive CLI (`opus-todo-agent`, or `uv run main.py` locally) that starts an agent session with all configured tools available.

#### Scenario: Start a session
- **WHEN** the user runs `opus-todo-agent`
- **THEN** an interactive session starts with the configured model, MCP servers, and tools initialized

### Requirement: Admin Commands
The CLI SHALL provide admin commands, including help and status, alongside the conversational interface.

#### Scenario: Inspect agent status
- **WHEN** the user invokes the status command
- **THEN** the CLI reports the current agent configuration state

### Requirement: Manager-Based Orchestration
The agent SHALL be assembled from dedicated managers for models, MCP servers, custom tools, higher-order tools, and instructions, so each concern can be configured independently.

#### Scenario: Startup orchestration
- **WHEN** the agent starts
- **THEN** each manager initializes from configuration before the session accepts prompts
