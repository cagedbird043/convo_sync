#!/usr/bin/env python3
"""测试代码块智能检测"""

import sys
from pathlib import Path

# 添加父目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.cleaners import JSONCleaner

# 测试用例
test_cases = [
    # Case 1: 纯文本总结（应该保留）
    (
        "这是一段讨论：\n```\n这是ai总结\n```\n继续讨论",
        "这是一段讨论：\n这是ai总结\n继续讨论",
        "纯文本总结",
    ),
    # Case 2: Python 代码（应该移除）
    (
        "示例代码：\n```python\ndef hello():\n    print('world')\n```\n说明",
        "示例代码：\n[代码块已移除]\n说明",
        "Python代码",
    ),
    # Case 3: 带语言标识的代码（应该移除）
    ("```javascript\nconst x = 1;\n```", "[代码块已移除]", "JavaScript代码"),
    # Case 4: 无语言标识但明显是代码（应该移除）
    (
        "```\nfunction test() {\n  return true;\n}\n```",
        "[代码块已移除]",
        "无标识的JS代码",
    ),
    # Case 5: 中文描述（应该保留）
    (
        "```\n功能说明：\n1. 处理数据\n2. 生成报告\n3. 发送通知\n```",
        "功能说明：\n1. 处理数据\n2. 生成报告\n3. 发送通知",
        "中文功能描述",
    ),
    # Case 6: 紧凑格式（应该保留）
    ("````这是ai总结````", "这是ai总结", "紧凑格式总结"),
]


def test_code_detection():
    """测试代码块检测"""
    cleaner = JSONCleaner("", "", remove_code_blocks=True)

    print("🧪 代码块智能检测测试\n")
    print("=" * 80)

    passed = 0
    failed = 0

    for i, (input_text, expected, description) in enumerate(test_cases, 1):
        result = cleaner._remove_code_blocks(input_text)

        # 规范化比较（去除多余空白）
        result_normalized = " ".join(result.split())
        expected_normalized = " ".join(expected.split())

        if result_normalized == expected_normalized:
            print(f"✅ Test {i}: {description}")
            passed += 1
        else:
            print(f"❌ Test {i}: {description}")
            print(f"   输入: {input_text!r}")
            print(f"   期望: {expected!r}")
            print(f"   实际: {result!r}")
            failed += 1
        print()

    print("=" * 80)
    print(f"\n📊 结果: {passed} passed, {failed} failed\n")

    return failed == 0


if __name__ == "__main__":
    success = test_code_detection()
    sys.exit(0 if success else 1)
