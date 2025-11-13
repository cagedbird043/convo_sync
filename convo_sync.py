#!/usr/bin/env python3
"""
ConvoSync CLI - Command-line interface for conversation data processing
"""

from pathlib import Path
from typing import Optional

import typer
from typing_extensions import Annotated

from src.cleaners import JSONCleaner
from src.converters import MarkdownConverter

app = typer.Typer(
    name="convo_sync",
    help="🚀 AI Conversation Data Processing Toolkit - Clean and convert Google AI Studio conversation data",
    add_completion=False,
    rich_markup_mode="rich",
)


@app.command()
def clean(
    input_file: Annotated[Path, typer.Argument(help="Input JSON file to clean")],
    output: Annotated[
        Optional[Path],
        typer.Option("--output", "-o", help="Output JSON file (default: input.cleaned.json)"),
    ] = None,
    keep_thinking: Annotated[
        bool,
        typer.Option("--keep-thinking", help="Keep AI thinking process (default: remove)"),
    ] = False,
    keep_code: Annotated[
        bool,
        typer.Option("--keep-code", help="Keep code blocks (default: remove)"),
    ] = False,
    stats: Annotated[
        bool,
        typer.Option("--stats", help="Show statistics after cleaning"),
    ] = False,
) -> None:
    """
    🧹 Clean and normalize JSON data from Google AI Studio.

    Removes thinking process and code blocks by default to reduce token usage.
    """
    typer.echo(f"🔄 Cleaning JSON file: {input_file}")

    if not input_file.exists():
        typer.secho(f"❌ Error: File not found: {input_file}", fg=typer.colors.RED, err=True)
        raise typer.Exit(1)

    output_file = output or input_file.with_suffix(".cleaned.json")
    remove_thinking = not keep_thinking
    remove_code = not keep_code

    cleaner = JSONCleaner(
        str(input_file),
        str(output_file),
        remove_thinking=remove_thinking,
        remove_code_blocks=remove_code,
    )
    cleaner.clean()

    typer.secho(f"✅ Cleaned JSON saved to: {output_file}", fg=typer.colors.GREEN)
    if remove_thinking:
        typer.echo("   🧠 Thinking process removed")
    if remove_code:
        typer.echo("   💾 Code blocks removed")

    if stats:
        stats_data = cleaner.get_stats()
        typer.echo("\n📊 Statistics:")
        typer.echo(f"  Total chunks: {stats_data['total']}")
        typer.echo(f"  👤 User messages: {stats_data['users']}")
        typer.echo(f"  🤖 Model messages: {stats_data['models']}")
        typer.echo(f"  📎 File references: {stats_data['files']}")


@app.command()
def convert(
    input_file: Annotated[Path, typer.Argument(help="Input JSON file (cleaned format)")],
    output: Annotated[
        Optional[Path],
        typer.Option("--output", "-o", help="Output Markdown file (default: input.md)"),
    ] = None,
    keep_thinking: Annotated[
        bool,
        typer.Option("--keep-thinking", help="Keep AI thinking process (default: remove)"),
    ] = False,
    stats: Annotated[
        bool,
        typer.Option("--stats", help="Show statistics after conversion"),
    ] = False,
) -> None:
    """
    📝 Convert cleaned JSON to Markdown format.

    Generates human-readable conversation records.
    """
    typer.echo(f"🔄 Converting to Markdown: {input_file}")

    if not input_file.exists():
        typer.secho(f"❌ Error: File not found: {input_file}", fg=typer.colors.RED, err=True)
        raise typer.Exit(1)

    output_file = output or input_file.with_suffix(".md")
    remove_thinking = not keep_thinking

    converter = MarkdownConverter(str(input_file), str(output_file), remove_thinking)
    result_file = converter.convert()

    typer.secho(f"✅ Markdown saved to: {result_file}", fg=typer.colors.GREEN)
    if remove_thinking:
        typer.echo("   (AI thinking process removed)")

    if stats:
        stats_data = converter.get_stats()
        typer.echo("\n📊 Statistics:")
        typer.echo(f"  Total conversations: {stats_data['total']}")
        typer.echo(f"  👤 User messages: {stats_data['users']}")
        typer.echo(f"  🤖 Model messages: {stats_data['models']}")


@app.command()
def pipeline(
    input_file: Annotated[Path, typer.Argument(help="Input JSON file")],
    clean_output: Annotated[
        Optional[Path],
        typer.Option("--clean-output", "-c", help="Clean JSON output file (default: input.cleaned.json)"),
    ] = None,
    md_output: Annotated[
        Optional[Path],
        typer.Option("--md-output", "-m", help="Markdown output file (default: input.md)"),
    ] = None,
    keep_thinking: Annotated[
        bool,
        typer.Option("--keep-thinking", help="Keep AI thinking process (default: remove)"),
    ] = False,
    keep_code: Annotated[
        bool,
        typer.Option("--keep-code", help="Keep code blocks (default: remove)"),
    ] = False,
    stats: Annotated[
        bool,
        typer.Option("--stats", help="Show statistics after each step"),
    ] = False,
) -> None:
    """
    ⚡ Run full clean→convert pipeline.

    This is the recommended workflow for most users.
    """
    typer.secho("🚀 Running ConvoSync Pipeline...", fg=typer.colors.BLUE, bold=True)
    typer.echo(f"📄 Input: {input_file}")

    if not input_file.exists():
        typer.secho(f"❌ Error: File not found: {input_file}", fg=typer.colors.RED, err=True)
        raise typer.Exit(1)

    if input_file.is_dir():
        typer.secho(f"❌ Error: Input must be a file, not a directory: {input_file}", fg=typer.colors.RED, err=True)
        raise typer.Exit(1)

    remove_thinking = not keep_thinking
    remove_code = not keep_code

    # Step 1: Clean
    typer.echo("\n📋 Step 1: Cleaning JSON...")
    clean_out = clean_output or input_file.with_suffix(".cleaned.json")
    cleaner = JSONCleaner(
        str(input_file),
        str(clean_out),
        remove_thinking=remove_thinking,
        remove_code_blocks=remove_code,
    )
    cleaner.clean()
    typer.secho(f"✅ Cleaned: {clean_out}", fg=typer.colors.GREEN)
    if remove_thinking:
        typer.echo("   🧠 Thinking process removed")
    if remove_code:
        typer.echo("   💾 Code blocks removed")

    # Step 2: Convert
    typer.echo("\n📋 Step 2: Converting to Markdown...")
    md_out = md_output or input_file.with_suffix(".md")
    converter = MarkdownConverter(str(clean_out), str(md_out), False)  # Already removed in clean step
    converter.convert()
    typer.secho(f"✅ Converted: {md_out}", fg=typer.colors.GREEN)

    # Statistics
    if stats:
        typer.echo("\n📊 Pipeline Statistics:")
        clean_stats = cleaner.get_stats()
        typer.echo(f"  Cleaned chunks: {clean_stats['total']}")
        typer.echo(f"    - 👤 Users: {clean_stats['users']}")
        typer.echo(f"    - 🤖 Models: {clean_stats['models']}")
        typer.echo(f"    - 📎 Files: {clean_stats['files']}")

        md_stats = converter.get_stats()
        typer.echo(f"  Markdown output: {md_stats['total']} entries")
        typer.echo(f"    - 👤 Users: {md_stats['users']}")
        typer.echo(f"    - 🤖 Models: {md_stats['models']}")

    typer.secho("\n✨ Done! Your conversation is ready.", fg=typer.colors.GREEN, bold=True)


def main() -> None:
    """Entry point for the CLI application."""
    app()


if __name__ == "__main__":
    main()
