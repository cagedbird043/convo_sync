"""
Markdown Converter Module - Markdown 转换模块
"""

import json


class MarkdownConverter:
    """Convert cleaned JSON to clean, renderable Markdown format."""

    def __init__(self, input_json_file, output_md_file=None):
        """
        Initialize the Markdown converter.

        Args:
            input_json_file: Path to input JSON file (cleaned format)
            output_md_file: Path to output Markdown file
        """
        self.input_json_file = input_json_file
        self.output_md_file = output_md_file or input_json_file.replace(".json", ".md")

    def convert(self):
        """
        Convert cleaned JSON to Markdown format with:
        - Auto-categorization by role (👤 User / 🤖 Assistant)
        - Clear headers and separators
        - Professional rendering
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
        model_count = content.count("## 🤖")

        return {
            "users": user_count,
            "models": model_count,
            "total": user_count + model_count,
        }
