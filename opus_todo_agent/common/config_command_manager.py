from common.config_manager import ConfigManager
from rich.table import Table
from rich.console import Console
from rich.syntax import Syntax
import json
import yaml
import shutil
from pathlib import Path


class ConfigCommandManager:
    """
    Manager for config commands
    """

    def __init__(self, config_manager: ConfigManager, console: Console):
        self.config_manager = config_manager
        self.console = console

    def handle_config_command(self, args: list):
        """Handle configuration commands."""
        if not args:
            self.console.print(
                "[yellow]Usage: /config [init|list|get|set|delete] [args...][/yellow]"
            )
            self.console.print(
                "[dim]Note: Keys support dot notation for nested values (e.g., todoist.api_key)[/dim]"
            )
            return

        subcommand = args[0].lower()

        if subcommand == "init":
            self._handle_init_command(args)

        elif subcommand == "list":
            self._handle_list_command()

        elif subcommand == "get":
            if len(args) < 2:
                self.console.print("[yellow]Usage: /config get <key>[/yellow]")
                self.console.print("[dim]Example: /config get todoist.api_key[/dim]")
                return

            key = args[1]
            self._handle_get_command(key)

        elif subcommand == "set":
            if len(args) < 3:
                self.console.print("[yellow]Usage: /config set <key> <value>[/yellow]")
                self.console.print("[dim]Example: /config set todoist.api_key abc123[/dim]")
                return

            key = args[1]
            value = " ".join(args[2:])  # Join remaining args as value
            self._handle_set_command(key, value)

        elif subcommand == "delete":
            if len(args) < 2:
                self.console.print("[yellow]Usage: /config delete <key>[/yellow]")
                self.console.print("[dim]Example: /config delete todoist.api_key[/dim]")
                return

            key = args[1]
            self._handle_delete_command(key)

        else:
            self.console.print(f"[red]Unknown config subcommand: {subcommand}[/red]")
            self.console.print(
                "[yellow]Available: init, list, get, set, delete[/yellow]"
            )

    def _handle_init_command(self, args: list):
        """Handle the init command to copy sample config file."""
        config_file = self.config_manager.config_file

        # Check if config file already exists
        if config_file.exists():
            self.console.print(
                f"[yellow]Config file already exists at: {config_file}[/yellow]"
            )
            return

        # Find the sample config file (it's in the same directory as this file)
        current_dir = Path(__file__).parent
        sample_file = current_dir / "opus-config-productivity.sample.yaml"

        if not sample_file.exists():
            self.console.print(
                f"[red]Sample config file not found at: {sample_file}[/red]"
            )
            return

        try:
            # Ensure config directory exists
            config_file.parent.mkdir(parents=True, exist_ok=True)

            # Copy sample file to config location
            shutil.copy2(sample_file, config_file)

            self.console.print(
                f"[green]✓ Initialized config file at: {config_file}[/green]"
            )
            self.console.print(
                "\n[white]You can now edit the config file or use '/config set' commands[/white]"
            )

        except (IOError, OSError) as e:
            self.console.print(f"[red]Failed to initialize config file: {e}[/red]")

    def _handle_list_command(self):
        flat_config = self.config_manager.get_all_settings_flat()
        if not flat_config:
            self.console.print("[yellow]No configuration settings found.[/yellow]")
            return

        table = Table(title="Configuration Settings")
        table.add_column("Key", style="cyan")
        table.add_column("Value", style="white")

        # Sort keys for better readability
        for key in sorted(flat_config.keys()):
            value = flat_config[key]
            # Mask sensitive values
            if any(
                sensitive in key.lower()
                for sensitive in ["key", "token", "secret", "password"]
            ):
                display_value = "***" if value else ""
            else:
                display_value = str(value)
            table.add_row(key, display_value)

        self.console.print(table)

    def _handle_get_command(self, key: str):
        value = self.config_manager.get_setting(key)

        if value is None:
            self.console.print(f"[yellow]Configuration key '{key}' not found.[/yellow]")
        else:
            # Mask sensitive values
            if any(
                sensitive in key.lower()
                for sensitive in ["key", "token", "secret", "password"]
            ):
                display_value = "***" if value else ""
                self.console.print(f"[cyan]{key}[/cyan]: {display_value}")
            elif isinstance(value, dict):
                # Pretty print nested dictionaries
                self.console.print(f"[cyan]{key}[/cyan]:")
                yaml_str = yaml.safe_dump(value, default_flow_style=False, sort_keys=False)
                syntax = Syntax(yaml_str, "yaml", theme="monokai", padding=1)
                self.console.print(syntax)
            elif isinstance(value, list):
                # Pretty print lists
                self.console.print(f"[cyan]{key}[/cyan]:")
                yaml_str = yaml.safe_dump(value, default_flow_style=False)
                syntax = Syntax(yaml_str, "yaml", theme="monokai", padding=1)
                self.console.print(syntax)
            else:
                display_value = str(value)
                self.console.print(f"[cyan]{key}[/cyan]: {display_value}")

    def _handle_set_command(self, key: str, value: str):
        # Try to parse as JSON for complex values
        try:
            parsed_value = json.loads(value)
            value = parsed_value
        except json.JSONDecodeError:
            # Keep as string if not valid JSON
            pass

        if self.config_manager.set_setting(key, value):
            # Mask sensitive values in success message
            if any(
                sensitive in key.lower()
                for sensitive in ["key", "token", "secret", "password"]
            ):
                display_value = "***"
            else:
                display_value = json.dumps(value) if isinstance(value, (dict, list)) else str(value)
            self.console.print(f"[green]✓ Set {key} = {display_value}[/green]")
        else:
            self.console.print(f"[red]Failed to set configuration.[/red]")

    def _handle_delete_command(self, key: str):
        if self.config_manager.delete_setting(key):
            self.console.print(f"[green]Deleted configuration key: {key}[/green]")
        else:
            self.console.print(f"[yellow]Configuration key '{key}' not found.[/yellow]")
