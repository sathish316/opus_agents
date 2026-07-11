# Tool Management Specification

## Purpose
Define the kinds of tools an agent can carry beyond raw MCP servers — hand-written custom tools, agent-backed higher-order tools, and spec-generated meta tools — and how each is registered.

## Requirements

### Requirement: Custom Tools
The system SHALL support custom tools: hand-written Python functions registered on the agent per configuration, used when an integration needs bespoke logic (e.g. Todoist completed-task queries, Obsidian RAG).

#### Scenario: Custom tool registered
- **WHEN** a custom tool's integration is enabled in configuration
- **THEN** the tool is registered on the agent and callable in the session

### Requirement: Higher-Order Tools
The system SHALL support higher-order tools: tools backed by their own inner agent with dedicated instructions and model, typically wrapping an MCP server to perform a multi-step task (e.g. calendar review, Slack catch-up).

#### Scenario: Higher-order tool invoked
- **WHEN** the user's request matches a higher-order tool
- **THEN** the tool's inner agent orchestrates its MCP tools and returns the result

### Requirement: Meta Tools
The system SHALL support meta tools that dynamically generate agent tools from a machine-readable specification — such as an OpenAPI spec — so an API can be integrated without custom code or an MCP server.

#### Scenario: Tools from an OpenAPI spec
- **WHEN** a meta tool is configured with an API's OpenAPI spec (e.g. HackerNews)
- **THEN** agent tools for that API's operations are generated and registered
