# AGENTS

See `README.md`, `CONTRIBUTING_GUIDE.md`, and `docs/USER_GUIDE.md` for the full product overview.

## Cursor Cloud specific instructions

Opus Agents is a Python (uv) agent framework + CLI. It is a uv workspace with members
`opus_agent_base` and `opus_todo_agent`. Python is provided by `uv` (requires >= 3.12).
The startup update script runs `uv sync --extra dev`, so deps (incl. ruff/black/mypy/pytest)
are already installed.

Non-obvious caveats:

- **The `opus_agent_base` wheel is consumed by the sibling `codd_query_engine` repo.** The startup
  update script builds it into `opus_agent_base/dist/` with
  `uv build opus_agent_base --out-dir opus_agent_base/dist`. That `dist/` dir is gitignored; rebuild
  it if it goes missing. Build with `uv build` (not `python -m build`, which needs `python3.12-venv`
  / `ensurepip` that is not installed).
- **The CLI requires a config file before it will start.** Create it once with
  `mkdir -p ~/.opusai && cp opus-config.sample.yml ~/.opusai/opus-config.yml` (or run
  `opus-agents --admin` then `/config init`). This lives in `$HOME`, not the repo.
- **Agent modes need LLM credentials.** `--agent` / `--todo-agent` / `--sde-agent` make real LLM
  calls and require `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`. The `--admin` mode (config/status slash
  commands) works without keys and is the easiest smoke test.

Run the CLI: `uv run opus-agents --help` (or `--admin`).
Lint/format/types: `uv run ruff check`, `uv run black .`, `uv run mypy` (repo has pre-existing
ruff findings). Tests: `uv run pytest` (no test files exist yet, so 0 are collected).
