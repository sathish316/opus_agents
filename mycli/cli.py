"""Main CLI application with all commands and subcommands."""

import typer
from typing import Optional
import sys

from mycli.commands.flow import flow_run, flow_list, flow_info, flow_add
from mycli.commands.plugin import plugin_list, plugin_info, plugin_add_core, plugin_add_community
from mycli.commands.agent import agent_info, agent_list, agent_run

# Create the main app
app = typer.Typer(
    name="mycli",
    help="A feature-rich CLI library similar to Cobra in Go",
    add_completion=False,
    rich_markup_mode="rich",
)

# Create subcommand groups
flow_app = typer.Typer(name="flow", help="Flow management commands")
plugin_app = typer.Typer(name="plugin", help="Plugin management commands")
agent_app = typer.Typer(name="agent", help="Agent management commands")

# Add subcommand groups to main app
app.add_typer(flow_app, name="flow")
app.add_typer(plugin_app, name="plugin")
app.add_typer(agent_app, name="agent")


# Global commands
@app.command("help")
def help_command(ctx: typer.Context):
    """Show help information."""
    typer.echo(ctx.get_help())


@app.command("quit")
def quit_command():
    """Quit the application."""
    typer.echo("Goodbye!")
    sys.exit(0)


@app.command("exit")
def exit_command():
    """Exit the application."""
    typer.echo("Goodbye!")
    sys.exit(0)


# Flow commands
@flow_app.command("run")
def flow_run_cmd(
    name: str = typer.Argument(..., help="Name of the flow to run"),
    foo: Optional[str] = typer.Option(None, "--foo", help="Example foo flag")
):
    """Run a flow by name."""
    flow_run(name, foo)


@flow_app.command("list")
def flow_list_cmd():
    """List all available flows."""
    flow_list()


@flow_app.command("info")
def flow_info_cmd(name: str = typer.Argument(..., help="Name of the flow")):
    """Show information about a specific flow."""
    flow_info(name)


@flow_app.command("add")
def flow_add_cmd(
    name: str = typer.Argument(..., help="Name of the flow to add"),
    path: str = typer.Option(..., "--path", help="Path to the flow")
):
    """Add a new flow."""
    flow_add(name, path)


# Plugin commands
@plugin_app.command("list")
def plugin_list_cmd():
    """List all available plugins."""
    plugin_list()


@plugin_app.command("info")
def plugin_info_cmd(name: str = typer.Argument(..., help="Name of the plugin")):
    """Show information about a specific plugin."""
    plugin_info(name)


@plugin_app.command("add")
def plugin_add_cmd(
    core: bool = typer.Option(False, "--core", help="Add a core plugin"),
    community: bool = typer.Option(False, "--community", help="Add a community plugin")
):
    """Add a plugin."""
    if core and community:
        typer.echo("Error: Cannot specify both --core and --community flags", err=True)
        raise typer.Exit(1)
    elif core:
        plugin_add_core()
    elif community:
        plugin_add_community()
    else:
        typer.echo("Error: Must specify either --core or --community flag", err=True)
        raise typer.Exit(1)


# Agent commands
@agent_app.command("info")
def agent_info_cmd(name: str = typer.Argument(..., help="Name of the agent")):
    """Show information about a specific agent."""
    agent_info(name)


@agent_app.command("list")
def agent_list_cmd():
    """List all available agents."""
    agent_list()


@agent_app.command("run")
def agent_run_cmd(name: str = typer.Argument(..., help="Name of the agent to run")):
    """Run an agent by name."""
    agent_run(name)


def main():
    """Main entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()