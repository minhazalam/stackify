"""
Stackify CLI Commands

This module contains implementations of CLI commands
such as project initialization.

Author: Minhaz Alam
Created: 2026-03
"""

from stackify.core.generator import create_project_structure


def init_project(project_name: str) -> None:
    """
    Initialize a new data engineering project.

    Args:
        project_name (str): Name of the project directory to create.

    Returns:
        None
    """
    print(f"🚀 Initializing project: {project_name}")

    create_project_structure(project_name)

    print("✅ Project structure created successfully!")