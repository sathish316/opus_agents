"""Plugin commands for the CLI."""

import typer
from typing import Optional


def plugin_list():
    """List all available plugins."""
    typer.echo("Listing all plugins...")


def plugin_info(name: str):
    """Show information about a specific plugin."""
    typer.echo(f"Showing info for plugin '{name}'")


def plugin_add_core():
    """Add a core plugin."""
    typer.echo("Adding core plugin...")


def plugin_add_community():
    """Add a community plugin."""
    typer.echo("Adding community plugin...")