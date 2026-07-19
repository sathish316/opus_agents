# AgentApps

AgentApps are focused, standalone practice and utility apps built alongside Opus Agents. Each app is a self-contained web experience for a specific hobby or workflow—independent of the agent CLI, but versioned in this monorepo so agents and humans can extend them together.

## Conventions

- One app per folder under `agent_apps/`
- Prefer a small Vite + React + TypeScript frontend
- Keep domain data (lessons, tabs, media IDs) in plain modules so agents can add content without rewriting UI
- Document how to run the app in each package’s README

## Apps

| App | Description |
|-----|-------------|
| [Scales](./scales) | Guitar major-scale practice routines with tabs, fingerings, video, and a synced metronome |
