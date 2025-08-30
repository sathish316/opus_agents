### Setup

$ uv sync

### Overview

Demo of Multi-Agent patterns:
1. Agent delegates to another Agent (using a tool)
$ uv run travel_agent_delegate_pattern.py

2. Agent delegates to another Agent with same set of deps
$ uv run travel_agent_delegate_deps.py

3. Programatically invoke multiple agents using sequence of methods - one per Agent call
$ uv run travel_agent_programmatic_handoff.py

4. Agent using a Pandas/Numpy tool for numeric calculation
$ uv run financial_planner_agent_basic.py

5. Multi-agent orchestration
$ uv run financial_planner_multi_agent.py
