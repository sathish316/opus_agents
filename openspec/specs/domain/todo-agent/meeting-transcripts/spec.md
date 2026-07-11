# Meeting Transcripts Specification

## Purpose
Let the user skip a meeting and still get the outcomes: ask follow-up questions directly to Zoom and Loom meeting transcripts.

## Requirements

### Requirement: Transcript Sources
The system SHALL support Zoom and Loom as meeting transcript sources through dedicated meeting-assistant tools.

#### Scenario: Source enabled
- **WHEN** a transcript source is enabled in configuration
- **THEN** its meeting transcripts become queryable in the agent session

### Requirement: Follow-Up Questions On Transcripts
The system SHALL answer follow-up questions about a meeting from its transcript, such as what was discussed or decided.

#### Scenario: Ask what was decided
- **WHEN** the user asks what was decided in a recorded meeting
- **THEN** the system answers from that meeting's transcript
