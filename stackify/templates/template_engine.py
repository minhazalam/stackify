"""
Template Engine Module

Handles rendering of Jinja2 templates.

Author: Minhaz Alam
Created: 2026-03
"""

import os
from jinja2 import Environment, FileSystemLoader


# Path to templates directory
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "..", "templates")


# Jinja environment
env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    trim_blocks=True,
    lstrip_blocks=True,
)


def render_template(template_path: str, output_path: str, context: dict) -> None:
    """
    Render a Jinja2 template to a file.

    Args:
        template_path (str): Path inside templates folder
        output_path (str): Output file path
        context (dict): Variables to inject
    """

    template = env.get_template(template_path)
    content = template.render(context)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w") as f:
        f.write(content)