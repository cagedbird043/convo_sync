#!/usr/bin/env python3
"""
Unit tests for ConvoSync toolkit
"""

import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

import pytest

# Ensure the parent directory is in the path
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from src.cleaners import JSONCleaner
from src.converters import MarkdownConverter


@pytest.fixture
def temp_dir():
    """Create temporary directory for test files"""
    temp = tempfile.mkdtemp()
    yield temp
    shutil.rmtree(temp)


@pytest.fixture
def create_test_json(temp_dir):
    """Fixture to create test JSON files"""

    def _create_json(filename, data):
        filepath = os.path.join(temp_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return filepath

    return _create_json


# JSONCleaner Tests


def test_clean_fragmented_chunks(temp_dir, create_test_json):
    """Test cleaning fragmented chunkedPrompt.chunks structure"""
    test_data = {
        "chunkedPrompt": {
            "chunks": [
                {"role": "user", "parts": [{"text": "Hello"}]},
                {"role": "user", "parts": [{"text": " "}]},
                {"role": "user", "parts": [{"text": "World"}]},
            ]
        }
    }

    input_file = create_test_json("test_input.json", test_data)
    output_file = os.path.join(temp_dir, "test_output.json")

    cleaner = JSONCleaner(input_file, output_file)
    cleaner.clean()

    with open(output_file, encoding="utf-8") as f:
        result = json.load(f)

    assert "chunkedPrompt" in result
    assert len(result["chunkedPrompt"]["chunks"]) == 3
    # Parts are processed and consolidated


def test_clean_direct_text(temp_dir, create_test_json):
    """Test cleaning direct text field"""
    test_data = {
        "chunkedPrompt": {
            "chunks": [
                {"role": "user", "text": "Direct text message"},
                {"role": "model", "text": "Model response"},
            ]
        }
    }

    input_file = create_test_json("test_input.json", test_data)
    output_file = os.path.join(temp_dir, "test_output.json")

    cleaner = JSONCleaner(input_file, output_file)
    cleaner.clean()

    with open(output_file, encoding="utf-8") as f:
        result = json.load(f)

    assert len(result["chunkedPrompt"]["chunks"]) == 2
    chunk0_text = result["chunkedPrompt"]["chunks"][0]["text"]
    chunk1_text = result["chunkedPrompt"]["chunks"][1]["text"]
    assert chunk0_text == "Direct text message"
    assert chunk1_text == "Model response"


def test_cleaner_get_stats(temp_dir, create_test_json):
    """Test statistics gathering for JSONCleaner"""
    test_data = {
        "chunkedPrompt": {
            "chunks": [
                {"role": "user", "text": "msg1"},
                {"role": "model", "text": "resp1"},
                {"role": "user", "text": "msg2"},
            ]
        }
    }

    input_file = create_test_json("test_input.json", test_data)
    output_file = os.path.join(temp_dir, "test_output.json")

    cleaner = JSONCleaner(input_file, output_file)
    cleaner.clean()
    stats = cleaner.get_stats()

    assert stats["total"] == 3
    assert stats["users"] == 2
    assert stats["models"] == 1


# MarkdownConverter Tests


def test_convert_to_markdown(temp_dir, create_test_json):
    """Test conversion to Markdown format"""
    test_data = {
        "chunkedPrompt": {
            "chunks": [
                {"role": "user", "text": "Hello"},
                {"role": "model", "text": "Hi there!"},
            ]
        }
    }

    input_file = create_test_json("test_input.json", test_data)
    output_file = os.path.join(temp_dir, "test_output.md")

    converter = MarkdownConverter(input_file, output_file)
    converter.convert()

    with open(output_file, encoding="utf-8") as f:
        content = f.read()

    assert "**Human:**" in content
    assert "**Assistant:**" in content
    assert "Hello" in content
    assert "Hi there!" in content


def test_markdown_structure(temp_dir, create_test_json):
    """Test Markdown structure and formatting"""
    test_data = {
        "chunkedPrompt": {
            "chunks": [
                {"role": "user", "text": "Test user message"},
                {"role": "model", "text": "Test model response"},
            ]
        }
    }

    input_file = create_test_json("test_input.json", test_data)
    output_file = os.path.join(temp_dir, "test_output.md")

    converter = MarkdownConverter(input_file, output_file)
    converter.convert()

    with open(output_file, encoding="utf-8") as f:
        lines = f.readlines()

    # Check for header
    assert any("Conversation Log" in line for line in lines)
    # Check for separators
    assert any(line.strip().startswith("---") for line in lines)


def test_converter_get_stats(temp_dir, create_test_json):
    """Test statistics gathering for MarkdownConverter"""
    test_data = {
        "chunkedPrompt": {
            "chunks": [
                {"role": "user", "text": "msg1"},
                {"role": "model", "text": "resp1"},
                {"role": "user", "text": "msg2"},
            ]
        }
    }

    input_file = create_test_json("test_input.json", test_data)
    output_file = os.path.join(temp_dir, "test_output.md")

    converter = MarkdownConverter(input_file, output_file)
    converter.convert()
    stats = converter.get_stats()

    assert stats["users"] == 2
    assert stats["models"] == 1


# Integration Tests


def test_full_pipeline(temp_dir, create_test_json):
    """Test complete clean + convert pipeline"""
    test_data = {
        "chunkedPrompt": {
            "chunks": [
                {
                    "role": "user",
                    "parts": [
                        {"text": "How"},
                        {"text": " are"},
                        {"text": " you?"},
                    ],
                },
                {"role": "model", "text": "I'm fine, thank you!"},
            ]
        }
    }

    input_file = os.path.join(temp_dir, "input.json")
    with open(input_file, "w", encoding="utf-8") as f:
        json.dump(test_data, f, ensure_ascii=False)

    # Step 1: Clean
    clean_file = os.path.join(temp_dir, "clean.json")
    cleaner = JSONCleaner(input_file, clean_file)
    cleaner.clean()

    # Step 2: Convert
    md_file = os.path.join(temp_dir, "output.md")
    converter = MarkdownConverter(clean_file, md_file)
    converter.convert()

    # Verify outputs
    with open(clean_file, encoding="utf-8") as f:
        clean_data = json.load(f)

    assert "chunkedPrompt" in clean_data
    assert len(clean_data["chunkedPrompt"]["chunks"]) >= 1

    with open(md_file, encoding="utf-8") as f:
        md_content = f.read()

    assert "**Human:**" in md_content
    assert "**Assistant:**" in md_content
