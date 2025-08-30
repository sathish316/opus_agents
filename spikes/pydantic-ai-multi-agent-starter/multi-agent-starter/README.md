### Overview

Demo of Agent delegation pattern.
Agent delegates work to another agent using a tool.
When the delegate agent finishes, the original agent takes control.

Another pattern is for the agent and delegate agent to have the same set of dependencies.


### Setup

$ uv sync

TravelPlannerAgent -> Tool:TripAdvisor -> TripAdvisorAgent


### Run agent

$ uv run travel_agent_delegate_pattern.py


