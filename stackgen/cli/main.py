"""
Stackgen CLI - Entry Point

Author: Minhaz Alam
Created: 2026-03
"""

import typer
from stackgen.cli.commands import init_project

app = typer.Typer(help="Stackgen CLI")


@app.callback()
def main():
    """
    Stackgen CLI root.
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