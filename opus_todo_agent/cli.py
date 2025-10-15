"""
CLI module for Opus TODO Agent with pydantic AI integration and admin mode.
"""

import asyncio
import logging
import os
import sys
from pathlib import Path

import typer
from agent_runner import run_agent
from common.config_command_manager import ConfigCommandManager
from common.config_manager import ConfigManager
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory
from prompt_toolkit.styles import Style
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Setup CLI app
app = typer.Typer(
    name="opus-todo-agent",
    help="Opus TODO Agent - AI-powered productivity assistant with MCP integrations",
    rich_markup_mode="rich",
)

# Setup rich console for pretty output
console = Console()
logger = logging.getLogger(__name__)

config_manager = ConfigManager()
config_command_manager = ConfigCommandManager(config_manager, console)


def run_cli_mode(run_agent_on_startup: bool = False):
    """Run the admin mode with slash commands."""
    console.print(
        Panel.fit(
            "[bold green]Opus TODO Agent - Admin Mode[/bold green]\n"
            "Use slash commands to configure the agent.\n"
            "Type [bold]/help[/bold] for available commands or [bold]/exit[/bold] to quit.\n"
            "[dim]💡 Tip: Use ↑/↓ arrows to navigate command history, Tab for completion[/dim]",
            border_style="green",
        )
    )

    # Set up command history file
    history_dir = Path.home() / ".opusai"
    history_dir.mkdir(exist_ok=True)
    history_file = history_dir / ".admin_history"

    # Set up command completion for all available commands and subcommands
    command_completer = WordCompleter(
        [
            "/help",
            "/agent",
            "/config",
            "/config init",
            "/config list",
            "/config get",
            "/config set",
            "/config delete",
            "/status",
            "/clear",
            "/exit",
            "/quit",
        ],
        ignore_case=True,
        sentence=True,
    )

    # Create custom style for prompt
    prompt_style = Style.from_dict(
        {
            "prompt": "bold ansiblue",
        }
    )

    # Create prompt session with history, auto-suggestions, and completion
    session = PromptSession(
        history=FileHistory(str(history_file)),
        auto_suggest=AutoSuggestFromHistory(),
        completer=command_completer,
        complete_while_typing=True,
        style=prompt_style,
    )

    # Run agent on startup if requested
    if run_agent_on_startup:
        try:
            asyncio.run(run_agent())
        except KeyboardInterrupt:
            console.print("\n[dim]Agent interrupted. Returning to CLI...[/dim]")
        except Exception as e:
            console.print(f"[red]Agent error: {e}[/red]")

    while True:
        try:
            # Use prompt_toolkit for input with command history support
            command = session.prompt([("class:prompt", "\nopus> ")]).strip()

            if not command:
                continue

            if not command.startswith("/"):
                console.print(
                    "[yellow]Commands must start with '/'. Type /help for available commands.[/yellow]"
                )
                continue

            # Parse command
            parts = command[1:].split()
            if not parts:
                continue

            cmd = parts[0].lower()
            args = parts[1:] if len(parts) > 1 else []

            # Handle commands
            if cmd == "exit" or cmd == "quit":
                console.print("[green]Goodbye![/green]")
                break
            elif cmd == "help":
                show_admin_help()
            elif cmd == "agent":
                asyncio.run(run_agent())
            elif cmd == "config":
                config_command_manager.handle_config_command(args)
            elif cmd == "status":
                show_status()
            elif cmd == "clear":
                os.system("clear" if os.name == "posix" else "cls")
            else:
                console.print(f"[red]Unknown command: /{cmd}[/red]")
                console.print("Type [bold]/help[/bold] for available commands.")

        except KeyboardInterrupt:
            console.print("\n[green]Goodbye![/green]")
            break
        except EOFError:
            console.print("\n[green]Goodbye![/green]")
            break
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            sys.exit(1)


def show_admin_help():
    """Show help for admin commands."""
    table = Table(title="Admin Mode Commands")
    table.add_column("Command", style="cyan", no_wrap=True)
    table.add_column("Description", style="white")

    commands = [
        ("/help", "Show this help message"),
        ("/agent", "Run Agent mode"),
        ("/config init", "Initialize config file from sample template"),
        ("/config list", "List all configuration settings"),
        ("/config get <key>", "Get a specific configuration setting"),
        ("/config set <key> <value>", "Set a configuration setting"),
        ("/config delete <key>", "Delete a configuration setting"),
        ("/status", "Show agent status and configuration"),
        ("/clear", "Clear the screen"),
        ("/exit, /quit", "Exit admin mode"),
    ]

    for cmd, desc in commands:
        table.add_row(cmd, desc)

    console.print(table)

    # Add helpful tips
    console.print("\n[bold cyan]💡 Navigation & Editing Tips:[/bold cyan]")
    tips_table = Table(show_header=False, box=None, padding=(0, 2))
    tips_table.add_column("Key", style="yellow")
    tips_table.add_column("Action", style="dim white")

    tips = [
        ("↑/↓", "Navigate command history"),
        ("Tab", "Auto-complete commands"),
        ("→", "Accept auto-suggestion"),
        ("Ctrl+C", "Cancel / Exit"),
        ("Ctrl+L", "Clear screen"),
        ("Ctrl+A/E", "Jump to start/end of line"),
    ]

    for key, action in tips:
        tips_table.add_row(key, action)

    console.print(tips_table)
    console.print(
        "\n[dim]Config keys support dot notation (e.g., todoist.api_key, calendar.google.client_id)[/dim]"
    )


def show_status():
    """Show agent status and configuration."""
    table = Table(title="Agent Status")
    table.add_column("Component", style="cyan")
    table.add_column("Status", style="white")

    # Check environment variables
    required_env_vars = [
        "OPENAI_API_KEY",
        "ANTHROPIC_API_KEY",
        "GOOGLE_OAUTH_CLIENT_ID",
        "GOOGLE_OAUTH_CLIENT_SECRET",
        "SLACK_MCP_XOXC_TOKEN",
        "SLACK_MCP_XOXD_TOKEN",
        "SLACK_MCP_XOXP_TOKEN",
    ]

    for var in required_env_vars:
        value = os.getenv(var)
        status = "[green]Set[/green]" if value else "[red]Not Set[/red]"
        table.add_row(var, status)

    # Configuration file status
    config_exists = config_manager.config_file.exists()
    config_status = (
        "[green]Exists[/green]" if config_exists else "[yellow]Not Found[/yellow]"
    )
    table.add_row("Config File", config_status)
    table.add_row("Config Path", str(config_manager.config_file))

    if config_exists:
        config = config_manager.load_config()
        table.add_row("Config Settings", str(len(config)))

    console.print(table)


@app.command()
def main(
    agent: bool = typer.Option(
        False,
        "--agent",
        "-ai",
        help="Start in Agent mode with slash commands for configuration",
    ),
    admin: bool = typer.Option(
        False,
        "--admin",
        "-a",
        help="Start in admin mode with slash commands for configuration",
    ),
    version: bool = typer.Option(
        False, "--version", "-v", help="Show version information"
    ),
):
    """
    Opus TODO Agent - AI-powered productivity assistant.

    Use --admin to enter configuration mode with slash commands.
    """
    if version:
        console.print("[bold blue]Opus TODO Agent[/bold blue] v0.1.0")
        console.print("AI-powered productivity assistant with MCP integrations")
        return

    if admin:
        run_cli_mode(run_agent_on_startup=False)
    elif agent:
        run_cli_mode(run_agent_on_startup=True)
    else:
        run_cli_mode(run_agent_on_startup=True)


if __name__ == "__main__":
    app()
