import logging
import os
from pathlib import Path
from typing import Annotated

import typer

from confluence_markdown_exporter import __version__
from confluence_markdown_exporter.utils.app_data_store import get_settings
from confluence_markdown_exporter.utils.app_data_store import set_setting
from confluence_markdown_exporter.utils.config_interactive import main_config_menu_loop
from confluence_markdown_exporter.utils.logging_config import setup_logging
from confluence_markdown_exporter.utils.measure_time import measure
from confluence_markdown_exporter.utils.type_converter import str_to_bool

DEBUG: bool = str_to_bool(os.getenv("DEBUG", "False"))

logger = logging.getLogger(__name__)

app = typer.Typer()


def override_output_path_config(value: Path | None) -> None:
    """Override the default output path if provided."""
    if value is not None:
        set_setting("export.output_path", value)


@app.command(help="Export one or more Confluence pages by ID or URL to Markdown.")
def pages(
    pages: Annotated[list[str], typer.Argument(help="Page ID(s) or URL(s)")],
    output_path: Annotated[
        Path | None,
        typer.Option(
            help="Directory to write exported Markdown files to. Overrides config if set."
        ),
    ] = None,
    verbose: Annotated[
        bool,
        typer.Option(
            "--verbose", "-v",
            help="Enable verbose logging output to console"
        ),
    ] = False,
) -> None:
    from confluence_markdown_exporter.confluence import Page

    setup_logging(verbose)
    logger.info(f"Starting export for pages: {', '.join(pages)}")
    
    with measure(f"Export pages {', '.join(pages)}"):
        for page in pages:
            override_output_path_config(output_path)
            logger.info(f"Processing page: {page}")
            _page = Page.from_id(int(page)) if page.isdigit() else Page.from_url(page)
            _page.export()
            logger.info(f"Completed export for page: {page}")


@app.command(help="Export Confluence pages and their descendant pages by ID or URL to Markdown.")
def pages_with_descendants(
    pages: Annotated[list[str], typer.Argument(help="Page ID(s) or URL(s)")],
    output_path: Annotated[
        Path | None,
        typer.Option(
            help="Directory to write exported Markdown files to. Overrides config if set."
        ),
    ] = None,
    verbose: Annotated[
        bool,
        typer.Option(
            "--verbose", "-v",
            help="Enable verbose logging output to console"
        ),
    ] = False,
) -> None:
    from confluence_markdown_exporter.confluence import Page

    setup_logging(verbose)
    logger.info(f"Starting export for pages with descendants: {', '.join(pages)}")
    
    with measure(f"Export pages {', '.join(pages)} with descendants"):
        for page in pages:
            override_output_path_config(output_path)
            logger.info(f"Processing page with descendants: {page}")
            _page = Page.from_id(int(page)) if page.isdigit() else Page.from_url(page)
            _page.export_with_descendants()
            logger.info(f"Completed export for page with descendants: {page}")


@app.command(help="Export all Confluence pages of one or more spaces to Markdown.")
def spaces(
    space_keys: Annotated[list[str], typer.Argument()],
    output_path: Annotated[
        Path | None,
        typer.Option(
            help="Directory to write exported Markdown files to. Overrides config if set."
        ),
    ] = None,
    verbose: Annotated[
        bool,
        typer.Option(
            "--verbose", "-v",
            help="Enable verbose logging output to console"
        ),
    ] = False,
) -> None:
    from confluence_markdown_exporter.confluence import Space

    setup_logging(verbose)
    logger.info(f"Starting export for spaces: {', '.join(space_keys)}")
    
    with measure(f"Export spaces {', '.join(space_keys)}"):
        for space_key in space_keys:
            override_output_path_config(output_path)
            logger.info(f"Processing space: {space_key}")
            space = Space.from_key(space_key)
            space.export()
            logger.info(f"Completed export for space: {space_key}")


@app.command(help="Export all Confluence pages across all spaces to Markdown.")
def all_spaces(
    output_path: Annotated[
        Path | None,
        typer.Option(
            help="Directory to write exported Markdown files to. Overrides config if set."
        ),
    ] = None,
    verbose: Annotated[
        bool,
        typer.Option(
            "--verbose", "-v",
            help="Enable verbose logging output to console"
        ),
    ] = False,
) -> None:
    from confluence_markdown_exporter.confluence import Organization

    setup_logging(verbose)
    logger.info("Starting export for all spaces")
    
    with measure("Export all spaces"):
        override_output_path_config(output_path)
        org = Organization.from_api()
        org.export()
        logger.info("Completed export for all spaces")


@app.command(help="Open the interactive configuration menu or display current configuration.")
def config(
    jump_to: Annotated[
        str | None,
        typer.Option(help="Jump directly to a config submenu, e.g. 'auth.confluence'"),
    ] = None,
    *,
    show: Annotated[
        bool,
        typer.Option(
            "--show",
            help="Display current configuration as YAML instead of opening the interactive menu",
        ),
    ] = False,
) -> None:
    """Interactive configuration menu or display current configuration."""
    if show:
        current_settings = get_settings()
        json_output = current_settings.model_dump_json(indent=2)
        typer.echo(f"```json\n{json_output}\n```")
    else:
        main_config_menu_loop(jump_to)


@app.command(help="Show the current version of confluence-markdown-exporter.")
def version() -> None:
    """Display the current version."""
    typer.echo(f"confluence-markdown-exporter {__version__}")


if __name__ == "__main__":
    app()
