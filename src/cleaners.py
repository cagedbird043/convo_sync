"""
JSON Cleaning Module - 数据清理模块
"""

import json
import sys


class JSONCleaner:
    """Clean and normalize fragmented JSON conversation data."""

    def __init__(self, input_file, output_file=None):
        """
        Initialize the JSON cleaner.

        Args:
            input_file: Path to input JSON file
            output_file: Path to output JSON file (if None, uses .cleaned.json)
        """
        self.input_file = input_file
        self.output_file = output_file or input_file.replace(".json", ".cleaned.json")

    def clean(self):
        """
        Clean JSON file by:
        1. Removing duplicate/fragmented text parts
        2. Keeping only 'role' and reconstructed 'text' fields
        3. Creating a cleaner, more compact format
        """
        try:
            with open(self.input_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON file: {e}")
        except FileNotFoundError:
            raise FileNotFoundError(f"Input file not found: {self.input_file}")

        # Process the conversations
        conversations = data.get("conversations", [])
        if not conversations:
            # Check for chunkedPrompt structure
            chunked_prompt = data.get("chunkedPrompt", {})
            chunks = chunked_prompt.get("chunks", [])
            if chunks:
                conversations = chunks

        cleaned_conversations = []

        for conv in conversations:
            cleaned_conv = {}

            # Copy role if exists
            if "role" in conv:
                cleaned_conv["role"] = conv["role"]

            # Handle parts structure (for chunks with fragmented text)
            if "parts" in conv:
                text_parts = []
                for part in conv["parts"]:
                    if isinstance(part, dict) and "text" in part:
                        text_parts.append(part["text"])
                cleaned_conv["text"] = "".join(text_parts)
            # Handle direct text field
            elif "text" in conv:
                cleaned_conv["text"] = conv["text"]
            else:
                cleaned_conv["text"] = ""

            if cleaned_conv.get("text"):  # Only add if has text
                cleaned_conversations.append(cleaned_conv)

        cleaned_data = {"conversations": cleaned_conversations}

        # Save to output file
        with open(self.output_file, "w", encoding="utf-8") as f:
            json.dump(cleaned_data, f, ensure_ascii=False, indent=2)

        return cleaned_data

    def _process_chunks(self, chunks):
        """Process and clean individual chunks."""
        cleaned_chunks = []

        for chunk in chunks:
            cleaned_chunk = {}

            # Copy role
            if "role" in chunk:
                cleaned_chunk["role"] = chunk["role"]

            # Reconstruct text from parts if fragmented
            if "parts" in chunk:
                text_parts = []
                for part in chunk["parts"]:
                    if "text" in part:
                        text_parts.append(part["text"])
                cleaned_chunk["text"] = "".join(text_parts)
            elif "text" in chunk:
                cleaned_chunk["text"] = chunk["text"]
            else:
                cleaned_chunk["text"] = ""

            cleaned_chunks.append(cleaned_chunk)

        return cleaned_chunks

    def get_stats(self):
        """Get statistics about the cleaned data."""
        with open(self.output_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        conversations = data.get("conversations", [])
        user_count = sum(1 for c in conversations if c.get("role") == "user")
        model_count = sum(1 for c in conversations if c.get("role") == "model")

        return {
            "total": len(conversations),
            "users": user_count,
            "models": model_count,
        }
