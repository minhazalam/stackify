"""
Stackify CLI Commands

This module contains implementations of CLI commands
such as project initialization.

Author: Minhaz Alam
Created: 2026-03
"""

import typer
from stackify.core.generator import create_project_structure


def init_project(project_name: str) -> None:
    """
    Initialize a new data engineering project.

    Args:
        project_name (str): Name of the project directory to create.

    Returns:
        None
    """
    typer.echo(f"\n🚀 Initializing project: {project_name}\n")

    # Prompt user
    typer.echo("Select pipeline type:")
    typer.echo("1. Batch")
    typer.echo("2. Streaming")
    typer.echo("3. Full")

    choice = typer.prompt("Enter choice (1/2/3)", default="3")

    mode_map = {
        "1": "batch",
        "2": "streaming",
        "3": "full",
    }

    mode = mode_map.get(choice, "full")

    typer.echo(f"\n⚙️ Selected mode: {mode}\n")

    # Pass mode to generator
    create_project_structure(project_name, mode)

    typer.echo("✅ Project structure created successfully!\n")