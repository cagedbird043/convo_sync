"""
Markdown Converter Module - Markdown 转换模块
"""

import json
import re


class MarkdownConverter:
    """Convert cleaned JSON to clean, renderable Markdown format."""

    def __init__(self, input_json_file, output_md_file=None, remove_thinking=True):
        """
        Initialize the Markdown converter.

        Args:
            input_json_file: Path to input JSON file (cleaned format)
            output_md_file: Path to output Markdown file
            remove_thinking: Whether to remove AI thinking process
                sections (default: True)
        """
        self.input_json_file = input_json_file
        self.output_md_file = output_md_file or input_json_file.replace(".json", ".md")
        self.remove_thinking = remove_thinking

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
        - Auto-categorization by role (👤 User / 🤖 Assistant)
        - Clear headers and separators
        - Professional rendering
        - Optional thinking process removal
        """
        try:
            with open(self.input_json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON file: {e}")
        except FileNotFoundError:
            raise FileNotFoundError(f"Input file not found: {self.input_json_file}")

        if "conversations" not in data:
            raise ValueError(
                "JSON file format incorrect: 'conversations' field not found"
            )

        conversations = data["conversations"]

        with open(self.output_md_file, "w", encoding="utf-8") as f:
            # Write header
            f.write("# 对话记录\n\n")
            f.write(f"> 总计 {len(conversations)} 条对话记录\n\n")
            f.write("---\n\n")

            # Process each conversation
            for idx, conv in enumerate(conversations, 1):
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

                # Determine emoji and label
                if role == "user":
                    emoji = "👤"
                    label = "用户"
                elif role == "model":
                    emoji = "🤖"
                    label = "助手"
                else:
                    emoji = "💬"
                    label = "其他"

                # Write conversation
                f.write(f"## {emoji} {label}\n\n")
                f.write(text)
                f.write("\n\n")
                f.write("---\n\n")

        return self.output_md_file

    def get_stats(self):
        """Get statistics about the conversion."""
        with open(self.output_md_file, "r", encoding="utf-8") as f:
            content = f.read()

        user_count = content.count("## 👤")
        assistant_count = content.count("## 🤖")

        return {
            "users": user_count,
            "models": assistant_count,
            "total": user_count + assistant_count,
        }
