"""
Stackify CLI - Entry Point

Author: Minhaz Alam
Created: 2026-03
"""

import typer
from stackify.cli.commands import init_project

app = typer.Typer(help="Stackify CLI")


@app.callback()
def main():
    """
    Stackify CLI root.
    """
    pass


@app.command()
def init(name: str):
    """
    Initialize a new data engineering project.

    Args:
        name (str): Project name
    """
    init_project(name)


if __name__ == "__main__":
    app()