#!/usr/bin/env python3
"""Test code block detection"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.cleaners import JSONCleaner


def test_code_detection():
    """Test code block detection in cleaner"""
    cleaner = JSONCleaner("dummy.json", "dummy.json")

    # Test case 1: Pure text summary (should be kept)
    text1 = "Discussion:\n```\nAI summary\n```\nMore discussion"
    result1 = cleaner._remove_code_blocks(text1)
    assert "AI summary" in result1

    # Test case 2: Python code (should be removed)
    text2 = "Code:\n```python\ndef hello():\n    print('world')\n```\nNote"
    result2 = cleaner._remove_code_blocks(text2)
    assert "def hello" not in result2

    # Test case 3: JavaScript code (should be removed)
    text3 = "```javascript\nconst x = 1;\n```"
    result3 = cleaner._remove_code_blocks(text3)
    assert "const x" not in result3
