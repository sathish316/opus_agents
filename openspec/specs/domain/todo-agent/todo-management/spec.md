# Todo Management Specification

## Purpose
Supercharge Todoist with conversational task management: querying and creating tasks, reviewing completed work, and prioritizing what to do next.

## Requirements

### Requirement: Task Management via Todoist
The system SHALL let the user create and search Todoist tasks conversationally within their projects.

#### Scenario: Create a task in a project
- **WHEN** the user asks to create a task (e.g. "Create task 'Order Curtains' in Interior project")
- **THEN** the task is created in the named Todoist project

### Requirement: Completed Task Queries
The system SHALL answer queries about completed tasks over relative time periods — today, yesterday, this week, last week — using custom Todoist tools.

#### Scenario: Completed last week
- **WHEN** the user asks "Find out all the tasks I completed last week"
- **THEN** the system returns tasks completed in that period

### Requirement: Daily And Weekly Reviews
The system SHALL generate daily and weekly reviews of completed tasks, supporting an explicit date or date range and an option to skip summarization.

#### Scenario: Weekly review for a range
- **WHEN** the user asks "Generate weekly review from 1-Sep to 10-Sep"
- **THEN** the system produces a review covering completed tasks in that range

### Requirement: Task Recommendation And Organization
The system SHALL recommend tasks to work on from a project or tag (including picking N at random) and SHALL help organize an inbox by recommending project categories for its tasks.

#### Scenario: Suggest from a tag
- **WHEN** the user asks "Suggest tasks with the tag deepwork"
- **THEN** the system recommends matching open tasks
