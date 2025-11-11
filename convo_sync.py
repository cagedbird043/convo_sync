#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ConvoSync CLI - Command-line interface for conversation data processing
"""

import argparse
import sys

from src.cleaners import JSONCleaner
from src.converters import MarkdownConverter


def main():
    # Check if first arg is a subcommand or a file
    # This allows both "python convo_sync.py file.json" and
    # "python convo_sync.py clean file.json"
    has_subcommand = len(sys.argv) > 1 and sys.argv[1] in [
        "clean",
        "convert",
        "pipeline",
    ]

    parser = argparse.ArgumentParser(
        description="ConvoSync - AI Conversation Data Processing Toolkit",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
            Examples:
            # Default: Full pipeline (clean + convert with thinking removed)
            python convo_sync.py input.json

            # Keep AI thinking process
            python convo_sync.py input.json --no-thinking

            # Show statistics
            python convo_sync.py input.json --stats

            # Advanced: Individual commands
            python convo_sync.py clean input.json -o output.json
            python convo_sync.py convert input.json -o output.md
            python convo_sync.py pipeline input.json
        """,
    )

    if not has_subcommand:
        # Default pipeline mode arguments
        parser.add_argument("input", help="Input JSON file")
        parser.add_argument(
            "--no-thinking",
            action="store_true",
            help="Keep AI thinking process (default: remove)",
        )
        parser.add_argument("--stats", action="store_true", help="Show statistics")
        parser.add_argument("-c", "--clean-output", help="Clean JSON output file")
        parser.add_argument("-m", "--md-output", help="Markdown output file")

        args = parser.parse_args()
        handle_default_pipeline(args)
        return

    # Subcommand mode
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Clean command
    clean_parser = subparsers.add_parser("clean", help="Clean and normalize JSON data")
    clean_parser.add_argument("input", help="Input JSON file")
    clean_parser.add_argument("-o", "--output", help="Output JSON file")
    clean_parser.add_argument("--stats", action="store_true", help="Show statistics")

    # Convert command
    convert_parser = subparsers.add_parser("convert", help="Convert JSON to Markdown")
    convert_parser.add_argument("input", help="Input JSON file (cleaned format)")
    convert_parser.add_argument("-o", "--output", help="Output Markdown file")
    convert_parser.add_argument(
        "--no-thinking",
        action="store_true",
        help="Keep AI thinking process (default: remove)",
    )
    convert_parser.add_argument("--stats", action="store_true", help="Show statistics")

    # Pipeline command
    pipeline_parser = subparsers.add_parser("pipeline", help="Run full clean->convert pipeline")
    pipeline_parser.add_argument("input", help="Input JSON file")
    pipeline_parser.add_argument("-c", "--clean-output", help="Clean JSON output file")
    pipeline_parser.add_argument("-m", "--md-output", help="Markdown output file")
    pipeline_parser.add_argument(
        "--no-thinking",
        action="store_true",
        help="Keep AI thinking process (default: remove)",
    )
    pipeline_parser.add_argument("--stats", action="store_true", help="Show statistics")

    args = parser.parse_args()

    # Default behavior: if no command specified but input provided,
    # run full pipeline
    try:
        if not args.command:
            if args.input:
                # Run default pipeline
                handle_default_pipeline(args)
            else:
                parser.print_help()
                sys.exit(1)
        else:
            if args.command == "clean":
                handle_clean(args)
            elif args.command == "convert":
                handle_convert(args)
            elif args.command == "pipeline":
                handle_pipeline(args)
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


def handle_default_pipeline(args):
    """
    Handle default pipeline: clean + convert with thinking removed.
    This is the simplified, most common use case.
    """
    input_file = args.input

    print("🚀 Running ConvoSync Pipeline...")
    print(f"📄 Input: {input_file}")

    # Step 1: Clean
    print("\n📋 Step 1: Cleaning JSON...")
    clean_output = args.clean_output or input_file.replace(".json", ".cleaned.json")
    cleaner = JSONCleaner(input_file, clean_output)
    cleaner.clean()
    print(f"✅ Cleaned: {clean_output}")

    # Step 2: Convert to Markdown
    print("\n📋 Step 2: Converting to Markdown...")
    md_output = args.md_output or input_file.replace(".json", ".md")
    remove_thinking = not args.no_thinking
    converter = MarkdownConverter(clean_output, md_output, remove_thinking)
    converter.convert()
    print(f"✅ Markdown: {md_output}")
    if remove_thinking:
        print("   (AI thinking process removed)")

    # Statistics
    if args.stats:
        print("\n📊 Statistics:")
        clean_stats = cleaner.get_stats()
        print(f"  Cleaned conversations: {clean_stats['total']}")
        print(f"    - 👤 Users: {clean_stats['users']}")
        print(f"    - 🤖 Models: {clean_stats['models']}")

        md_stats = converter.get_stats()
        print(f"  Markdown output: {md_stats['total']} entries")
        print(f"    - 👤 Users: {md_stats['users']}")
        print(f"    - 🤖 Models: {md_stats['models']}")

    print("\n✨ Done! Your conversation is ready.")


def handle_clean(args):
    """Handle clean command."""
    print(f"🔄 Cleaning JSON file: {args.input}")

    cleaner = JSONCleaner(args.input, args.output)
    cleaner.clean()

    print(f"✅ Cleaned JSON saved to: {cleaner.output_file}")

    if args.stats:
        stats = cleaner.get_stats()
        print("\n📊 Statistics:")
        print(f"  Total conversations: {stats['total']}")
        print(f"  User messages: {stats['users']}")
        print(f"  Model messages: {stats['models']}")


def handle_convert(args):
    """Handle convert command."""
    print(f"🔄 Converting to Markdown: {args.input}")

    # Default is to remove thinking (unless --no-thinking is set)
    remove_thinking = not args.no_thinking
    converter = MarkdownConverter(args.input, args.output, remove_thinking)
    output_file = converter.convert()

    print(f"✅ Markdown saved to: {output_file}")
    if remove_thinking:
        print("   (AI thinking process removed)")

    if args.stats:
        stats = converter.get_stats()
        print("\n📊 Statistics:")
        print(f"  Total conversations: {stats['total']}")
        print(f"  👤 User messages: {stats['users']}")
        print(f"  🤖 Model messages: {stats['models']}")


def handle_pipeline(args):
    """Handle full pipeline command."""
    input_file = args.input

    # Step 1: Clean
    print("📋 Step 1: Cleaning JSON...")
    clean_output = args.clean_output or input_file.replace(".json", ".cleaned.json")
    cleaner = JSONCleaner(input_file, clean_output)
    cleaner.clean()
    print(f"✅ Cleaned: {clean_output}")

    # Step 2: Convert
    print("\n📋 Step 2: Converting to Markdown...")
    md_output = args.md_output or input_file.replace(".json", ".md")
    remove_thinking = not args.no_thinking
    converter = MarkdownConverter(clean_output, md_output, remove_thinking)
    converter.convert()
    print(f"✅ Converted: {md_output}")
    if remove_thinking:
        print("   (AI thinking process removed)")

    if args.stats:
        print("\n📊 Pipeline Statistics:")
        clean_stats = cleaner.get_stats()
        print(f"  Cleaned conversations: {clean_stats['total']}")
        print(f"    - Users: {clean_stats['users']}")
        print(f"    - Models: {clean_stats['models']}")

        md_stats = converter.get_stats()
        print(f"  Markdown output: {md_stats['total']} entries")
        print(f"    - 👤 Users: {md_stats['users']}")
        print(f"    - 🤖 Models: {md_stats['models']}")


if __name__ == "__main__":
    main()
