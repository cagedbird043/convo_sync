"""
Markdown Converter Module - Markdown 转换模块
"""

import json
import re


class MarkdownConverter:
    """Convert cleaned JSON conversations to readable Markdown format.

    This class transforms Google AI Studio conversation JSON into clean,
    human-readable Markdown documents with proper formatting and structure.

    The converter provides:
        - Structured conversation layout with user and assistant markers
        - Normalized code block rendering (prevents excessive backticks)
        - Optional removal of thinking process sections
        - Statistics tracking for message counts
        - Clean separator lines between messages

    Attributes:
        input_json_file (str): Path to the input cleaned JSON file.
        output_md_file (str): Path to the output Markdown file.
        remove_thinking (bool): Whether to filter out thinking process content.
        message_counter (dict): Tracks count of user and model messages.

    Example:
        >>> converter = MarkdownConverter("cleaned.json", "output.md")
        >>> converter.convert()
        >>> stats = converter.get_stats()
        >>> print(f"Converted {stats['total']} messages to Markdown")

    Note:
        The input should be a cleaned JSON file (ideally processed by JSONCleaner)
        to ensure optimal results and formatting.
    """

    def __init__(
        self,
        input_json_file: str,
        output_md_file: str | None = None,
        remove_thinking: bool = True,
    ) -> None:
        """Initialize the Markdown converter with file paths and options.

        Args:
            input_json_file: Path to input JSON file in Google AI Studio format.
                Should be a cleaned JSON (processed by JSONCleaner) for best results.
            output_md_file: Path for the Markdown output file. If None, automatically
                generates filename by replacing '.json' extension with '.md'.
            remove_thinking: If True, excludes parts marked as thinking process
                (thought: true flag) from the output. Default is True to produce
                cleaner conversation records.

        Raises:
            FileNotFoundError: If input_json_file does not exist.
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

    def _load_conversations(self, data):
        """
        Load conversations from JSON data.

        Supports both formats:
        - Standard format with 'conversations' field
        - Google AI Studio format with 'chunkedPrompt.chunks' field

        Args:
            data: Parsed JSON data

        Returns:
            List of conversation dicts with 'role' and 'text' fields

        Raises:
            ValueError: If data format is not recognized
        """
        if "conversations" in data:
            return data["conversations"]

        if "chunkedPrompt" in data and "chunks" in data["chunkedPrompt"]:
            # Convert Google AI Studio format to standard format
            conversations = []
            for chunk in data["chunkedPrompt"]["chunks"]:
                role = chunk.get("role", "unknown")
                # Try to get text, or merge from parts
                if "text" in chunk:
                    text = chunk["text"]
                elif "parts" in chunk:
                    # Merge parts into text
                    text = "".join(part.get("text", "") for part in chunk["parts"])
                else:
                    text = ""
                conversations.append({"role": role, "text": text})
            return conversations

        msg = "JSON file format incorrect: neither 'conversations' nor 'chunkedPrompt.chunks' found"
        raise ValueError(msg)

    def convert(self) -> str:
        """Convert JSON conversation data to formatted Markdown document.

        This method processes the input JSON and generates a clean Markdown file
        with proper structure, role markers, and normalized code blocks.

        The conversion process includes:
            - Extracting conversations from Google AI Studio format
            - Creating role-based sections (👤 User / 🤖 Assistant)
            - Normalizing code block backticks for consistent rendering
            - Filtering thinking process sections (if enabled)
            - Adding visual separators between messages
            - Generating summary header with message count

        Returns:
            str: Path to the generated Markdown file.

        Raises:
            FileNotFoundError: If the input JSON file does not exist.
            json.JSONDecodeError: If the input file contains invalid JSON.
            IOError: If unable to write to the output file.

        Example:
            >>> converter = MarkdownConverter("input.json", "output.md")
            >>> output_path = converter.convert()
            >>> print(f"Markdown generated at: {output_path}")
            Markdown generated at: output.md

        Note:
            The method automatically detects and handles both standard conversation
            format and Google AI Studio's chunkedPrompt format.
        """
        try:
            with open(self.input_json_file, encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON file: {e}") from e
        except FileNotFoundError as e:
            msg = f"Input file not found: {self.input_json_file}"
            raise FileNotFoundError(msg) from e

        conversations = self._load_conversations(data)
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

    def get_stats(self) -> dict[str, int]:
        """Retrieve statistics from the conversion process.

        Provides a summary of messages converted to Markdown, broken down by
        role (user vs model/assistant).

        Returns:
            dict: A dictionary containing:
                - users (int): Number of user messages converted
                - models (int): Number of model/assistant messages converted
                - total (int): Total number of messages in the Markdown output

        Example:
            >>> converter = MarkdownConverter("input.json")
            >>> converter.convert()
            >>> stats = converter.get_stats()
            >>> print(f"Converted {stats['users']} user and {stats['models']} model messages")
            Converted 76 user and 74 model messages

        Note:
            This method should be called after convert() to get accurate statistics.
            The counter is reset each time convert() is called.
        """
        return {
            "users": self.message_counter.get("user", 0),
            "models": self.message_counter.get("model", 0),
            "total": sum(self.message_counter.values()),
        }
