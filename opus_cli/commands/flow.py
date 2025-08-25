"""Flow commands for the CLI."""

import typer
from typing import Optional


def flow_run(name: str, foo: Optional[str] = typer.Option(None, help="Example foo flag")):
    """Run a flow by name."""
    if foo:
        typer.echo(f"Running flow '{name}' with foo='{foo}'")
    else:
        typer.echo(f"Running flow '{name}'")


def flow_list():
    """List all available flows."""
    typer.echo("Listing all flows...")


def flow_info(name: str):
    """Show information about a specific flow."""
    typer.echo(f"Showing info for flow '{name}'")


def flow_add(name: str, path: str = typer.Option(..., help="Path to the flow")):
    """Add a new flow."""
    typer.echo(f"Adding flow '{name}' from path '{path}'")