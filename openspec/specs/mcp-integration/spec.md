# MCP Integration Specification

## Purpose
Connect the agent to external tools through MCP servers, registering each enabled integration with the right transport, credentials, and tool prefix.

## Requirements

### Requirement: Config-Driven Server Registry
The system SHALL register MCP servers per enabled integration, keyed by domain/category/server in configuration, each with a tool prefix to namespace its tools. Supported transports SHALL include stdio (local servers) and streamable-http (remote servers).

#### Scenario: Enabled server registered
- **WHEN** an integration is enabled in configuration
- **THEN** its MCP server is registered with the configured transport and tool prefix

### Requirement: Per-Agent Server Registries
Each agent package SHALL declare its MCP servers in its own server registry. The todo agent registry SHALL provide Todoist, Obsidian, Google Calendar (local stdio server from `GOOGLE_WORKSPACE_MCP_PATH`, authenticated via Google OAuth client credentials), Clockwise (remote streamable-http with OAuth), Slack (local stdio server), and a datetime utility server. The SDE agent registry SHALL provide GitHub, Jira, Linear, Docker, Kubernetes, and observability servers (Prometheus, with Loki/Grafana/Tempo definitions).

#### Scenario: Google Calendar server setup
- **WHEN** Google Calendar is enabled and `GOOGLE_OAUTH_CLIENT_ID`/`GOOGLE_OAUTH_CLIENT_SECRET` are set
- **THEN** the Google workspace MCP server is registered over stdio from `GOOGLE_WORKSPACE_MCP_PATH`

### Requirement: FastMCP Client Tools As Agent Tools
The system SHALL expose tools discovered from FastMCP client servers as native agent tools by wrapping each MCP tool's schema and routing calls through the FastMCP client. This allows servers that only work over a FastMCP client (e.g. Docker, whose schema is rejected by the direct toolset path) to still contribute tools.

#### Scenario: Client tool wrapped
- **WHEN** an enabled FastMCP server advertises a tool
- **THEN** the agent registers a native tool with the same name, description, and JSON schema that proxies calls to that server

### Requirement: Tool Allowlist Filtering
The system SHALL filter which FastMCP client tools are exposed: when a tool's prefix appears in `mcp_config.allowed_tool_prefixes`, only tools listed under `mcp_config.allowed_tools.<prefix>` are registered; tools with unlisted prefixes pass through unfiltered.

#### Scenario: Tool outside the allowlist
- **WHEN** a server's prefix is in `allowed_tool_prefixes` and one of its tools is not in that prefix's `allowed_tools` list
- **THEN** that tool is not registered on the agent

### Requirement: Slack Auth Method Selection
The system SHALL select Slack MCP credentials based on the explicitly configured `auth_method` setting (e.g. `xoxp` user token), passing the matching token environment variables to the server.

#### Scenario: xoxp auth configured
- **WHEN** `mcp_config.productivity.chat.slack.auth_method` is `xoxp`
- **THEN** the Slack MCP server is started with the `SLACK_MCP_XOXP_TOKEN` environment variable
