"""Agent commands for the CLI."""

import typer


def agent_info(name: str):
    """Show information about a specific agent."""
    typer.echo(f"Showing info for agent '{name}'")


def agent_list():
    """List all available agents."""
    typer.echo("Listing all agents...")


def agent_run(name: str):
    """Run an agent by name."""
    typer.echo(f"Running agent '{name}'")