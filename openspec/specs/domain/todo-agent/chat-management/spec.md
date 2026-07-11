# Chat Management Specification

## Purpose
Let the user catch up on Slack without drowning in messages: summarize channels over a time window and turn important mentions into actionable todos.

## Requirements

### Requirement: Channel Catch-Up
The system SHALL summarize activity in team- or project-specific Slack channels over a user-specified duration (e.g. last day, last week, last N days).

#### Scenario: Catch up on a channel
- **WHEN** the user asks to catch up on a Slack channel for the last week
- **THEN** the system summarizes that channel's messages from the period

### Requirement: Mentions To Action Items
The system SHALL convert Slack mentions of the user in important messages into todo-list action items.

#### Scenario: Mention becomes a task
- **WHEN** the user asks to process their Slack mentions
- **THEN** important mentions are turned into tasks in their todo list
