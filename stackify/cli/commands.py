"""
Stackify CLI Commands

This module contains implementations of CLI commands
such as project initialization.

Author: Minhaz Alam
Created: 2026-03
"""

import typer
from stackify.core.generator import create_project_structure
import questionary


def init_project(project_name: str) -> None:
    """
    Initialize a new data engineering project.

    Args:
        project_name (str): Name of the project directory to create.

    Returns:
        None
    """
    typer.echo(f"\n🚀 Initializing project: {project_name}\n")

    mode = questionary.select(
        "Select pipeline type:",
        choices=[
            "Batch",
            "Streaming",
            "Full",
        ],
    ).ask()

    if not mode:
        typer.echo("❌ No mode selected. Exiting.")
        raise typer.Exit()

    typer.echo(f"\n⚙️ Selected mode: {mode}\n")

    # Pass mode to generator
    create_project_structure(project_name, mode)

    typer.echo("✅ Project structure created successfully!\n")