"""
Markdown Converter Module - Markdown 转换模块
"""

import json
import re


class MarkdownConverter:
    """Convert cleaned JSON to clean, renderable Markdown format."""

    def __init__(
        self,
        input_json_file,
        output_md_file=None,
        remove_thinking=True,
    ):
        """
        Initialize the Markdown converter.

        Args:
            input_json_file: Path to input JSON file (cleaned format)
            output_md_file: Path to output Markdown file
            remove_thinking: Whether to remove AI thinking process
                sections (default: True)
        """
        self.input_json_file = input_json_file
        default_output = input_json_file.replace(".json", ".md")
        self.output_md_file = output_md_file or default_output
        self.remove_thinking = remove_thinking
        self.message_counter = {"user": 0, "model": 0}

    def _normalize_code_blocks(self, text):
        """
        Normalize code block backticks to use proper markdown syntax.

        Ensures code blocks use appropriate number of backticks:
        - Single backticks for inline code
        - Triple backticks (minimum) for code blocks
        - Uses language specifier when available

        Args:
            text: Input text with code blocks

        Returns:
            Text with normalized code blocks
        """

        # First pass: normalize code blocks with any number of backticks
        # Match opening backticks (3+), optional language, content,
        # closing backticks
        def normalize_block(match):
            language = match.group(2).lower().strip()
            content = match.group(3)

            # Always use triple backticks
            return f"```{language}\n{content.strip()}\n```"

        # Pattern: (3+ backticks)(optional language)(content)(same backticks)
        text = re.sub(
            r"^(`{3,})([a-z0-9]*)\s*\n(.*?)\n\1$",
            normalize_block,
            text,
            flags=re.MULTILINE | re.DOTALL,
        )

        # Second pass: normalize consecutive triple backticks (merge them)
        # This handles cases where code blocks got duplicated
        text = re.sub(r"\n```\n```\n", "\n```\n", text)
        text = re.sub(r"```+", "```", text)

        return text

    def _remove_thinking_sections(self, text):
        """
        Remove AI thinking process sections from text.

        Removes content between thinking markers like:
        - **Title**\n\nThinking content\n\n\n
        - Multiple consecutive sections separated by \n\n\n

        Args:
            text: Input text possibly containing thinking sections

        Returns:
            Text with thinking sections removed
        """
        # Pattern: Match **Bold Title** followed by paragraph(s)
        # The thinking section ends with triple newlines (\n\n\n)
        # or another **Bold Title**

        # This regex matches:
        # - **any text** (bold title)
        # - \n\n (double newline after title)
        # - .*? (non-greedy match for content, including newlines)
        # - \n\n\n (triple newline marking end of section)
        pattern = r"\*\*[^*]+\*\*\n\n.*?\n\n\n"
        text = re.sub(pattern, "", text, flags=re.DOTALL)

        # Also remove remaining **Title**\n\n...content at the end
        # (in case there's no triple newline at the very end)
        pattern_end = r"\*\*[^*]+\*\*\n\n.*?(?=\n\n[^\n]|$)"
        text = re.sub(pattern_end, "", text, flags=re.DOTALL)

        # Clean up excessive newlines (more than 2 consecutive)
        text = re.sub(r"\n{3,}", "\n\n", text)

        return text.strip()

    def convert(self):
        """
        Convert cleaned JSON to Markdown format with:
        - Clear role-based sections (Human / Assistant)
        - Proper formatting to avoid AI learning confusion
        - Code block normalization
        - Optional thinking process removal
        """
        try:
            with open(self.input_json_file, encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON file: {e}") from e
        except FileNotFoundError as e:
            msg = f"Input file not found: {self.input_json_file}"
            raise FileNotFoundError(msg) from e

        if "conversations" not in data:
            raise ValueError("JSON file format incorrect: 'conversations' field not found")

        conversations = data["conversations"]
        self.message_counter = {"user": 0, "model": 0}

        with open(self.output_md_file, "w", encoding="utf-8") as f:
            # Write header
            f.write("# Conversation Log\n\n")
            f.write(f"> Total {len(conversations)} messages\n\n")
            f.write("---\n\n")

            # Process each conversation
            for conv in conversations:
                role = conv.get("role", "unknown").lower()
                text = conv.get("text", "").strip()

                # Skip empty conversations
                if not text:
                    continue

                # Remove thinking sections if enabled
                if self.remove_thinking and role == "model":
                    text = self._remove_thinking_sections(text)

                # Skip if text is empty after thinking removal
                if not text.strip():
                    continue

                # Normalize code blocks
                text = self._normalize_code_blocks(text)

                # Increment counter
                if role in self.message_counter:
                    self.message_counter[role] += 1

                # Format output based on role
                if role == "user":
                    self._write_user_message(f, text)
                elif role == "model":
                    self._write_assistant_message(f, text)
                else:
                    self._write_other_message(f, role, text)

        return self.output_md_file

    def _write_user_message(self, f, text):
        """Write user message in standard format."""
        f.write("**Human:**\n\n")
        f.write(text)
        f.write("\n\n")
        f.write("---\n---\n\n")

    def _write_assistant_message(self, f, text):
        """Write assistant message in standard format."""
        f.write("**Assistant:**\n\n")
        f.write(text)
        f.write("\n\n")
        f.write("---\n---\n\n")

    def _write_other_message(self, f, role, text):
        """Write other role message in standard format."""
        f.write(f"**{role.capitalize()}:**\n\n")
        f.write(text)
        f.write("\n\n")
        f.write("---\n---\n\n")

    def get_stats(self):
        """Get statistics about the conversion."""
        return {
            "users": self.message_counter.get("user", 0),
            "models": self.message_counter.get("model", 0),
            "total": sum(self.message_counter.values()),
        }
