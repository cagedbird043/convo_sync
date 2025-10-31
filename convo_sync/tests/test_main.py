#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for ConvoSync toolkit
"""

import json
import os
import tempfile
import unittest
from pathlib import Path

# Add parent directory to path for imports
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.cleaners import JSONCleaner
from src.converters import MarkdownConverter


class TestJSONCleaner(unittest.TestCase):
    """Test cases for JSONCleaner class"""

    def setUp(self):
        """Create temporary directory for test files"""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up temporary files"""
        import shutil

        shutil.rmtree(self.temp_dir)

    def create_test_json(self, filename, data):
        """Helper to create test JSON files"""
        filepath = os.path.join(self.temp_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return filepath

    def test_clean_fragmented_chunks(self):
        """Test cleaning fragmented chunkedPrompt.chunks structure"""
        test_data = {
            "conversations": [
                {
                    "role": "user",
                    "chunkedPrompt": {
                        "chunks": [
                            {"parts": [{"text": "Hello"}]},
                            {"parts": [{"text": " "}]},
                            {"parts": [{"text": "World"}]},
                        ]
                    },
                }
            ]
        }

        input_file = self.create_test_json("test_input.json", test_data)
        output_file = os.path.join(self.temp_dir, "test_output.json")

        cleaner = JSONCleaner(input_file, output_file)
        cleaner.clean()

        with open(output_file, "r", encoding="utf-8") as f:
            result = json.load(f)

        self.assertEqual(len(result["conversations"]), 1)
        self.assertEqual(result["conversations"][0]["text"], "Hello World")

    def test_clean_direct_text(self):
        """Test cleaning direct text field"""
        test_data = {
            "conversations": [
                {"role": "user", "text": "Direct text message"},
                {"role": "model", "text": "Model response"},
            ]
        }

        input_file = self.create_test_json("test_input.json", test_data)
        output_file = os.path.join(self.temp_dir, "test_output.json")

        cleaner = JSONCleaner(input_file, output_file)
        cleaner.clean()

        with open(output_file, "r", encoding="utf-8") as f:
            result = json.load(f)

        self.assertEqual(len(result["conversations"]), 2)
        self.assertEqual(result["conversations"][0]["text"], "Direct text message")
        self.assertEqual(result["conversations"][1]["text"], "Model response")

    def test_get_stats(self):
        """Test statistics gathering"""
        test_data = {
            "conversations": [
                {"role": "user", "text": "msg1"},
                {"role": "model", "text": "resp1"},
                {"role": "user", "text": "msg2"},
            ]
        }

        input_file = self.create_test_json("test_input.json", test_data)
        output_file = os.path.join(self.temp_dir, "test_output.json")

        cleaner = JSONCleaner(input_file, output_file)
        cleaner.clean()
        stats = cleaner.get_stats()

        self.assertEqual(stats["total"], 3)
        self.assertEqual(stats["users"], 2)
        self.assertEqual(stats["models"], 1)


class TestMarkdownConverter(unittest.TestCase):
    """Test cases for MarkdownConverter class"""

    def setUp(self):
        """Create temporary directory for test files"""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up temporary files"""
        import shutil

        shutil.rmtree(self.temp_dir)

    def create_test_json(self, filename, data):
        """Helper to create test JSON files"""
        filepath = os.path.join(self.temp_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return filepath

    def test_convert_to_markdown(self):
        """Test conversion to Markdown format"""
        test_data = {
            "conversations": [
                {"role": "user", "text": "Hello"},
                {"role": "model", "text": "Hi there!"},
            ]
        }

        input_file = self.create_test_json("test_input.json", test_data)
        output_file = os.path.join(self.temp_dir, "test_output.md")

        converter = MarkdownConverter(input_file, output_file)
        converter.convert()

        with open(output_file, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("👤", content)
        self.assertIn("🤖", content)
        self.assertIn("Hello", content)
        self.assertIn("Hi there!", content)

    def test_markdown_structure(self):
        """Test Markdown structure and formatting"""
        test_data = {
            "conversations": [
                {"role": "user", "text": "Test user message"},
                {"role": "model", "text": "Test model response"},
            ]
        }

        input_file = self.create_test_json("test_input.json", test_data)
        output_file = os.path.join(self.temp_dir, "test_output.md")

        converter = MarkdownConverter(input_file, output_file)
        converter.convert()

        with open(output_file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Check for header
        self.assertTrue(any("对话记录" in line for line in lines))
        # Check for separators
        self.assertTrue(any(line.strip().startswith("---") for line in lines))

    def test_get_stats(self):
        """Test statistics gathering for Markdown"""
        test_data = {
            "conversations": [
                {"role": "user", "text": "msg1"},
                {"role": "model", "text": "resp1"},
                {"role": "user", "text": "msg2"},
            ]
        }

        input_file = self.create_test_json("test_input.json", test_data)
        output_file = os.path.join(self.temp_dir, "test_output.md")

        converter = MarkdownConverter(input_file, output_file)
        converter.convert()
        stats = converter.get_stats()

        self.assertEqual(stats["users"], 2)
        self.assertEqual(stats["assistants"], 1)


class TestIntegration(unittest.TestCase):
    """Integration tests for complete workflow"""

    def setUp(self):
        """Create temporary directory for test files"""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up temporary files"""
        import shutil

        shutil.rmtree(self.temp_dir)

    def test_full_pipeline(self):
        """Test complete clean + convert pipeline"""
        test_data = {
            "conversations": [
                {
                    "role": "user",
                    "chunkedPrompt": {
                        "chunks": [
                            {"parts": [{"text": "How"}]},
                            {"parts": [{"text": " are"}]},
                            {"parts": [{"text": " you?"}]},
                        ]
                    },
                },
                {"role": "model", "text": "I'm fine, thank you!"},
            ]
        }

        input_file = os.path.join(self.temp_dir, "input.json")
        with open(input_file, "w", encoding="utf-8") as f:
            json.dump(test_data, f, ensure_ascii=False)

        # Step 1: Clean
        clean_file = os.path.join(self.temp_dir, "clean.json")
        cleaner = JSONCleaner(input_file, clean_file)
        cleaner.clean()

        # Step 2: Convert
        md_file = os.path.join(self.temp_dir, "output.md")
        converter = MarkdownConverter(clean_file, md_file)
        converter.convert()

        # Verify outputs
        with open(clean_file, "r", encoding="utf-8") as f:
            clean_data = json.load(f)

        self.assertEqual(len(clean_data["conversations"]), 2)
        self.assertEqual(clean_data["conversations"][0]["text"], "How are you?")

        with open(md_file, "r", encoding="utf-8") as f:
            md_content = f.read()

        self.assertIn("How are you?", md_content)
        self.assertIn("👤", md_content)


if __name__ == "__main__":
    unittest.main()
