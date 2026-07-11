# Config Management Specification

## Purpose
Give users a single YAML configuration to control which domains, tool categories, MCP servers, and models the agent runs with, plus CLI commands to manage it.

## Requirements

### Requirement: User Config File
The system SHALL read its configuration from `~/.opusai/opus-config.yml` by default, seeded from a sample config shipped with the project, and SHALL accept a custom config directory and file path.

#### Scenario: Config loaded at startup
- **WHEN** the agent starts and `~/.opusai/opus-config.yml` exists
- **THEN** managers initialize from its settings

#### Scenario: Custom config path
- **WHEN** a custom config directory and file are provided to the config manager
- **THEN** configuration is read from that path instead of the default

### Requirement: Typed Settings Access
The config manager SHALL expose settings by dot-notation key, including retrieving a config section as a typed Pydantic model.

#### Scenario: Section as model
- **WHEN** a caller requests a config section with a model class
- **THEN** the section is returned as a validated instance of that model

### Requirement: Hierarchical Enablement
Configuration SHALL support enabling or disabling integrations at domain, category, and individual MCP-server level (e.g. `mcp_config.productivity.chat.slack`), and the agent SHALL only initialize what is enabled.

#### Scenario: Disabled integration is skipped
- **WHEN** an MCP server is disabled at any level of its hierarchy
- **THEN** the agent does not register that server or its tools

### Requirement: Configurable Logging
Logging SHALL default to ERROR level and be configurable via the config file, keeping normal sessions quiet.

#### Scenario: Raise log verbosity
- **WHEN** the user sets a more verbose log level in `opus-config.yml`
- **THEN** the agent logs at that level

### Requirement: Config Commands
The CLI SHALL provide config slash commands to view and manage settings without editing the YAML file by hand.

#### Scenario: View settings from the CLI
- **WHEN** the user invokes a config command
- **THEN** the CLI displays the requested configuration values
