"""
JSON Cleaning Module - 数据清理模块
"""

import json


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
        data = self._load_json_file()
        conversations = self._extract_conversations(data)
        cleaned_conversations = self._process_conversations(conversations)
        cleaned_data = {"conversations": cleaned_conversations}
        self._save_json_file(cleaned_data)
        return cleaned_data

    def _load_json_file(self):
        """Load and parse JSON file."""
        try:
            with open(self.input_file, encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON file: {e}") from e
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Input file not found: {self.input_file}") from e

    def _extract_conversations(self, data):
        """Extract conversations from data structure."""
        conversations = data.get("conversations", [])
        if not conversations:
            # Check for chunkedPrompt structure
            chunked_prompt = data.get("chunkedPrompt", {})
            chunks = chunked_prompt.get("chunks", [])
            if chunks:
                conversations = chunks
        return conversations

    def _process_conversations(self, conversations):
        """Process and clean all conversations."""
        cleaned_conversations = []
        for conv in conversations:
            cleaned_conv = self._process_single_conversation(conv)
            if cleaned_conv.get("text"):  # Only add if has text
                cleaned_conversations.append(cleaned_conv)
        return cleaned_conversations

    def _process_single_conversation(self, conv):
        """Process a single conversation entry."""
        cleaned_conv = {}

        # Copy role if exists
        if "role" in conv:
            cleaned_conv["role"] = conv["role"]

        # Extract text from various formats
        cleaned_conv["text"] = self._extract_text(conv)

        return cleaned_conv

    def _extract_text(self, conv):
        """Extract text from conversation in various formats."""
        # Handle chunkedPrompt structure (nested chunks with parts)
        if "chunkedPrompt" in conv:
            return self._extract_from_chunked_prompt(conv["chunkedPrompt"])

        # Handle parts structure (for chunks with fragmented text)
        if "parts" in conv:
            return self._extract_from_parts(conv["parts"])

        # Handle direct text field
        return conv.get("text", "")

    def _extract_from_chunked_prompt(self, chunked_prompt):
        """Extract text from chunkedPrompt structure."""
        chunks = chunked_prompt.get("chunks", [])
        text_parts = []
        for chunk in chunks:
            if "parts" in chunk:
                text_parts.append(self._extract_from_parts(chunk["parts"]))
        return "".join(text_parts)

    def _extract_from_parts(self, parts):
        """Extract text from parts list."""
        text_parts = []
        for part in parts:
            if isinstance(part, dict) and "text" in part:
                text_parts.append(part["text"])
        return "".join(text_parts)

    def _save_json_file(self, data):
        """Save cleaned data to JSON file."""
        with open(self.output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

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
        with open(self.output_file, encoding="utf-8") as f:
            data = json.load(f)

        conversations = data.get("conversations", [])
        user_count = sum(1 for c in conversations if c.get("role") == "user")
        model_count = sum(1 for c in conversations if c.get("role") == "model")

        return {
            "total": len(conversations),
            "users": user_count,
            "models": model_count,
        }
