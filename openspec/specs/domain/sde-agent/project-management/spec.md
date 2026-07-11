# Project Management Specification

## Purpose
Give software engineers conversational access to their project trackers — GitHub issues, Jira, and Linear — plus AI-assisted issue enrichment.

## Requirements

### Requirement: Tracker Integrations
The SDE agent SHALL integrate GitHub, Jira (Atlassian via npx), and Linear through MCP servers so issues can be queried and managed conversationally.

#### Scenario: Tracker enabled
- **WHEN** a tracker is enabled in configuration
- **THEN** its issues become queryable in the SDE agent session

### Requirement: Acceptance Criteria Generation
The SDE agent SHALL auto-generate acceptance criteria for a GitHub issue from the relevant code, using a dedicated higher-order tool driven by a prompt template.

#### Scenario: Enrich a GitHub issue
- **WHEN** the user asks to generate acceptance criteria for a GitHub issue
- **THEN** the tool produces acceptance criteria informed by the codebase and adds them to the issue

### Requirement: Jira Issue Classification
The SDE agent SHALL classify Jira issues via a higher-order tool that returns enriched, structured issue data.

#### Scenario: Classify an issue
- **WHEN** the user asks to classify a Jira issue
- **THEN** the tool returns the issue enriched with its classification
