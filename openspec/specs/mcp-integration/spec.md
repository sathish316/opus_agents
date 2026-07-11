# MCP Integration Specification

## Purpose
Connect the agent to external tools through MCP servers, registering each enabled integration with the right transport, credentials, and tool prefix.

## Requirements

### Requirement: Config-Driven Server Registry
The system SHALL register MCP servers per enabled integration, keyed by domain/category/server in configuration, each with a tool prefix to namespace its tools. Supported transports SHALL include stdio (local servers) and streamable-http (remote servers).

#### Scenario: Enabled server registered
- **WHEN** an integration is enabled in configuration
- **THEN** its MCP server is registered with the configured transport and tool prefix

### Requirement: Integration Catalog
The system SHALL provide MCP server definitions for the built-in integrations: Todoist, Obsidian, Google Calendar (local stdio server from `GOOGLE_WORKSPACE_MCP_PATH`, authenticated via Google OAuth client credentials), Clockwise (remote streamable-http with OAuth), Slack (local stdio server), and a datetime utility server.

#### Scenario: Google Calendar server setup
- **WHEN** Google Calendar is enabled and `GOOGLE_OAUTH_CLIENT_ID`/`GOOGLE_OAUTH_CLIENT_SECRET` are set
- **THEN** the Google workspace MCP server is registered over stdio from `GOOGLE_WORKSPACE_MCP_PATH`

### Requirement: Slack Auth Method Selection
The system SHALL select Slack MCP credentials based on the explicitly configured `auth_method` setting (e.g. `xoxp` user token), passing the matching token environment variables to the server.

#### Scenario: xoxp auth configured
- **WHEN** `mcp_config.productivity.chat.slack.auth_method` is `xoxp`
- **THEN** the Slack MCP server is started with the `SLACK_MCP_XOXP_TOKEN` environment variable
