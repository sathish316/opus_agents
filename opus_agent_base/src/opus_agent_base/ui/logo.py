"""
ASCII art logo display for Opus Agents.
"""

from rich.console import Console


def display_logo(console: Console) -> None:
    """
    Display the Opus Agents ASCII art logo with aqua blue and grey colors.
    
    Args:
        console: Rich console instance for colored output
    """
    logo = """
[light_sky_blue1]╔══════════════════════════════════════════════════════════════════════════════════════════════════╗[/light_sky_blue1]
[light_sky_blue1]║                                                                                                  ║[/light_sky_blue1]
[light_sky_blue1]║   [bold]  ██████╗ ██████╗ ██╗   ██╗███████╗[/bold]    [light_sky_blue1][bold] █████╗  ██████╗ ███████╗███╗   ██╗████████╗███████╗[/bold][/light_sky_blue1]    ║[/light_sky_blue1]
[light_sky_blue1]║   [bold] ██╔═══██╗██╔══██╗██║   ██║██╔════╝[/bold]    [light_sky_blue1][bold]██╔══██╗██╔════╝ ██╔════╝████╗  ██║╚══██╔══╝██╔════╝[/bold][/light_sky_blue1]    ║[/light_sky_blue1]
[light_sky_blue1]║   [bold] ██║   ██║██████╔╝██║   ██║███████╗[/bold]    [light_sky_blue1][bold]███████║██║  ███╗█████╗  ██╔██╗ ██║   ██║   ███████╗[/bold][/light_sky_blue1]    ║[/light_sky_blue1]
[light_sky_blue1]║   [bold] ██║   ██║██╔═══╝ ██║   ██║╚════██║[/bold]    [light_sky_blue1][bold]██╔══██║██║   ██║██╔══╝  ██║╚██╗██║   ██║   ╚════██║[/bold][/light_sky_blue1]    ║[/light_sky_blue1]
[light_sky_blue1]║   [bold] ╚██████╔╝██║     ╚██████╔╝███████║[/bold]    [light_sky_blue1][bold]██║  ██║╚██████╔╝███████╗██║ ╚████║   ██║   ███████║[/bold][/light_sky_blue1]    ║[/light_sky_blue1]
[light_sky_blue1]║   [bold]  ╚═════╝ ╚═╝      ╚═════╝ ╚══════╝[/bold]    [light_sky_blue1][bold]╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝[/bold][/light_sky_blue1]    ║[/light_sky_blue1]
[light_sky_blue1]║                                                                                                  ║[/light_sky_blue1]
[light_sky_blue1]╚══════════════════════════════════════════════════════════════════════════════════════════════════╝[/light_sky_blue1]
"""
    
    console.print(logo)
