# 示例

## 场景 1: 清理 Claude 对话导出

假设你从 Claude 导出了对话数据:

```json
{
  "messages": [
    {
      "role": "user",
      "content": "What is Python?"
    },
    {
      "role": "assistant",
      "content": "<think>Let me explain...</think>Python is a programming language."
    }
  ]
}
```

清理并转换:

```bash
pixi run run-pipeline claude_export.json -o python_qa.md --stats
```

结果 `python_qa.md`:

```markdown
# Conversation

**User:**
What is Python?

**Assistant:**
Python is a programming language.

---

📊 Statistics:

- User messages: 1
- Assistant messages: 1
```

## 场景 2: 批量处理多个文件

```bash
#!/bin/bash
for file in conversations/*.json; do
  pixi run run-pipeline "$file" -o "output/$(basename $file .json).md"
done
```

## 场景 3: 保留思维过程用于分析

```bash
pixi run run-convert input.json --keep-think -o analysis.md
```

## 场景 4: 在 Python 脚本中使用

```python
from src.cleaners import clean_conversation
from src.converters import convert_to_markdown
import json

# 读取数据
with open('input.json') as f:
    data = json.load(f)

# 清理
cleaned = clean_conversation(data, remove_think=True)

# 转换
markdown = convert_to_markdown(
    cleaned,
    title="My Conversation",
    add_stats=True
)

# 保存
with open('output.md', 'w') as f:
    f.write(markdown)
```

## 场景 5: CI/CD 集成

在 GitHub Actions 中使用:

```yaml
- name: Process conversations
  run: |
    pixi install
    pixi run run-pipeline data/conversations.json -o docs/processed.md
```

更多示例请查看 [examples/](../../examples/) 目录。
