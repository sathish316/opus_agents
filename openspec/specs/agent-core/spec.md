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

### Requirement: Multi-Agent Framework
The system SHALL separate a reusable agent framework package (`opus_agent_base`) from concrete agent packages (e.g. the todo agent). The framework SHALL provide a generic `AgentBuilder` that assembles an agent from instructions, prompt templates, MCP servers, custom tools, higher-order tools, and meta tools; each agent package extends it with its own MCP server registry and tools. An example agent package SHALL demonstrate the pattern alongside guides for adding custom and higher-order tools.

#### Scenario: New agent built on the framework
- **WHEN** an agent package defines its builder and MCP server registry
- **THEN** the framework runs it with the shared CLI, config, model, and tool infrastructure

### Requirement: Agent Builder API
The `AgentBuilder` SHALL provide a `build_agent` method that assembles a full agent, and a `build_simple_agent` method for agents without tools, with configurable dependency and output types.

#### Scenario: Simple agent without tools
- **WHEN** a caller builds an agent via `build_simple_agent`
- **THEN** the agent is created without tool or MCP initialization

#### Scenario: Agent without MCP servers
- **WHEN** an agent is built with no MCP server configuration
- **THEN** the build succeeds and MCP initialization is skipped

### Requirement: Manager-Based Orchestration
The agent SHALL be assembled from dedicated managers for models, MCP servers, custom tools, higher-order tools, and instructions, so each concern can be configured independently.

#### Scenario: Startup orchestration
- **WHEN** the agent starts
- **THEN** each manager initializes from configuration before the session accepts prompts
