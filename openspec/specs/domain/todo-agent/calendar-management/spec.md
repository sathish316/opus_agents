# Calendar Management Specification

## Purpose
Help the user understand and reclaim their meeting time by asking questions about their Google Calendar and Clockwise schedules.

## Requirements

### Requirement: Calendar Providers
The system SHALL support Google Calendar and Clockwise as calendar sources, each integrated through its MCP server and exposed through higher-order calendar tools.

#### Scenario: Provider enabled
- **WHEN** a calendar provider is enabled in configuration
- **THEN** its meetings become queryable in the agent session

### Requirement: Meeting Queries
The system SHALL list the user's meetings for a given date.

#### Scenario: Meetings on a date
- **WHEN** the user asks "list all my meetings for date 1-Sep-2025"
- **THEN** the system returns that day's meetings from the enabled calendar

### Requirement: Reviews From Accepted Meetings
The system SHALL generate daily and weekly reviews from the user's accepted meetings, so past time spent in meetings can be analyzed.

#### Scenario: Daily review of meetings
- **WHEN** the user asks for a daily review of their meetings
- **THEN** the system summarizes that day's accepted meetings
