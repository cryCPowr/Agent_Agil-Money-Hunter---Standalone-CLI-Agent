"""CLI Main Entry Point — Agent_Agil command line interface."""

import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from agent_agil.core.agent import get_agent, AgentAgil
from agent_agil.skills.registry import get_skill_registry


console = Console()


def print_banner() -> None:
    """Print the Agent_Agil banner."""
    banner = r"""
    ░█▀▀░█▀█░█▀█░█▀▀░█▀▄░█▀█░█▀▀░█▀▀
    ░█░░░█▀█░█░█░█▀▀░█▀▄░█░█░█▀▀░▀▀█
    ░▀▀▀░▀░▀░▀░▀░▀▀▀░▀░▀░▀▀▀░▀▀▀░▀▀▀
    
    Agent_Agil (Money-Hunter) v0.1.0
    Autonomous Money-Making Agent Framework
    """
    console.print(Panel(banner, style="bold cyan"))


@click.group(invoke_without_command=True)
@click.option("--personality", "-p", help="Set personality mode")
@click.option("--verbose", "-v", is_flag=True, help="Verbose output")
@click.pass_context
def cli(ctx: click.Context, personality: Optional[str], verbose: bool) -> None:
    """Agent_Agil — Autonomous money-making agent."""
    print_banner()
    
    agent = get_agent()
    
    if personality:
        try:
            msg = agent.switch_personality(personality)
            console.print(f"[green]✓[/green] {msg}")
        except ValueError as e:
            console.print(f"[red]✗[/red] {e}")
            sys.exit(1)
    
    if ctx.invoked_subcommand is None:
        # Show system prompt preview
        console.print("\n[bold]System Prompt Preview:[/bold]")
        prompt = agent.get_system_prompt()
        # Show first 1000 chars
        console.print(prompt[:1000] + "..." if len(prompt) > 1000 else prompt)
        
        console.print("\n[dim]Use subcommands to interact with the agent.[/dim]")
        console.print("[dim]Run 'agent-agil --help' for available commands.[/dim]")


@cli.command()
@click.argument("niche")
def research(niche: str) -> None:
    """Research a niche for viability."""
    agent = get_agent()
    agent.set_niche(niche)
    console.print(f"[green]✓[/green] Researching niche: [bold]{niche}[/bold]")
    
    # Show market-research skill
    registry = get_skill_registry()
    skill = registry.get("market-research")
    if skill:
        console.print(f"\n[bold]Using skill:[/bold] {skill.name}")
        console.print(f"[dim]{skill.description}[/dim]")
        console.print("\n[bold]Steps:[/bold]")
        for i, step in enumerate(skill.steps, 1):
            console.print(f"  {i}. {step}")
    else:
        console.print("[yellow]⚠[/yellow] market-research skill not found")


@cli.command()
@click.option("--detailed", "-d", is_flag=True, help="Show detailed personality info")
def personalities(detailed: bool) -> None:
    """List available personalities."""
    agent = get_agent()
    personalities = agent.personality_manager.personalities.get("personalities", {})
    
    table = Table(title="Available Personalities")
    table.add_column("Name", style="cyan")
    table.add_column("Description", style="white")
    if detailed:
        table.add_column("Tone", style="yellow")
        table.add_column("Focus", style="green")
    
    for name, config in personalities.items():
        if detailed:
            table.add_row(
                name,
                config.get("description", ""),
                config.get("tone", ""),
                config.get("focus", "")
            )
        else:
            table.add_row(name, config.get("description", ""))
    
    console.print(table)


@cli.command()
def wallet() -> None:
    """Check wallet balance."""
    agent = get_agent()
    balance = agent.get_wallet_balance()
    configured = agent.wallet.is_configured()
    
    console.print(f"\n[bold]Wallet Status:[/bold]")
    console.print(f"  Configured: {'[green]Yes[/green]' if configured else '[red]No[/red]'}")
    console.print(f"  Balance: [cyan]${balance:.4f}[/cyan]")
    console.print(f"  Daily Limit: [cyan]${agent.state.spend_limit_daily:.2f}[/cyan]")
    console.print(f"  Per-Tx Limit: [cyan]${agent.state.spend_limit_per_transaction:.2f}[/cyan]")
    
    if not configured:
        console.print("\n[yellow]⚠[/yellow] Wallet not configured. Add PK_WALLET to config/.env")


@cli.command()
def skills() -> None:
    """List available skills."""
    registry = get_skill_registry()
    skills = registry.list_all()
    
    table = Table(title="Available Skills")
    table.add_column("Name", style="cyan")
    table.add_column("Category", style="yellow")
    table.add_column("Description", style="white")
    table.add_column("Trigger", style="dim")
    
    for skill in skills:
        table.add_row(
            skill.name,
            skill.category,
            skill.description[:60] + "..." if len(skill.description) > 60 else skill.description,
            skill.trigger[:50] + "..." if len(skill.trigger) > 50 else skill.trigger
        )
    
    console.print(table)


@cli.command()
@click.argument("name")
def skill(name: str) -> None:
    """Show details for a specific skill."""
    registry = get_skill_registry()
    skill_obj = registry.get(name)
    
    if not skill_obj:
        console.print(f"[red]✗[/red] Skill '{name}' not found")
        sys.exit(1)
    
    console.print(f"\n[bold]{skill_obj.name}[/bold] ({skill_obj.category})")
    console.print(f"\n[bold]Description:[/bold] {skill_obj.description}")
    console.print(f"\n[bold]Trigger:[/bold] {skill_obj.trigger}")
    
    if skill_obj.steps:
        console.print("\n[bold]Steps:[/bold]")
        for i, step in enumerate(skill_obj.steps, 1):
            console.print(f"  {i}. {step}")
    
    if skill_obj.output_format:
        console.print(f"\n[bold]Output Format:[/bold]")
        console.print(skill_obj.output_format)
    
    if skill_obj.ponytail:
        console.print(f"\n[bold]Notes:[/bold] {skill_obj.ponytail}")


@cli.command()
def prompt() -> None:
    """Show the full system prompt."""
    agent = get_agent()
    console.print(agent.get_system_prompt())


@cli.command()
@click.argument("name")
def switch(name: str) -> None:
    """Switch personality."""
    agent = get_agent()
    try:
        msg = agent.switch_personality(name)
        console.print(f"[green]✓[/green] {msg}")
    except ValueError as e:
        console.print(f"[red]✗[/red] {e}")
        sys.exit(1)


@cli.command()
def state() -> None:
    """Show current agent state."""
    agent = get_agent()
    
    console.print("\n[bold]Current State:[/bold]")
    console.print(f"  Mode: [cyan]{agent.state.mode.value}[/cyan]")
    console.print(f"  Personality: [cyan]{agent.state.personality}[/cyan]")
    console.print(f"  Current Niche: [cyan]{agent.state.current_niche or 'None'}[/cyan]")
    console.print(f"  Current Project: [cyan]{agent.state.current_project or 'None'}[/cyan]")
    console.print(f"  Daily Spend Limit: [cyan]${agent.state.spend_limit_daily:.2f}[/cyan]")
    console.print(f"  Per-Tx Limit: [cyan]${agent.state.spend_limit_per_transaction:.2f}[/cyan]")
    console.print(f"  Wallet Balance: [cyan]${agent.get_wallet_balance():.4f}[/cyan]")


@cli.command()
def config() -> None:
    """Show configuration summary."""
    agent = get_agent()
    
    console.print("\n[bold]Configuration Summary:[/bold]")
    console.print(f"  Config Dir: [cyan]{agent.soul[:50]}...[/cyan]")
    
    # Show loaded files
    from agent_agil.core.agent import ConfigLoader
    config_dir = ConfigLoader.CONFIG_DIR
    for file in sorted(config_dir.glob("*")):
        if file.is_file():
            size = file.stat().st_size
            console.print(f"  ✓ {file.name} ({size} bytes)")


def cli_entry() -> None:
    """Entry point for setuptools."""
    cli()


if __name__ == "__main__":
    cli_entry()