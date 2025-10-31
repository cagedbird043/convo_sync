# ConvoSync 使用示例

## 示例 1: 基本使用 - 清理 JSON

```bash
python convo_sync.py clean /path/to/input.json -o cleaned.json
```

**输入文件示例** (`input.json`):

```json
{
  "conversations": [
    {
      "role": "user",
      "chunkedPrompt": {
        "chunks": [
          { "parts": [{ "text": "你好" }] },
          { "parts": [{ "text": "，" }] },
          { "parts": [{ "text": "今天天气" }] },
          { "parts": [{ "text": "如何？" }] }
        ]
      }
    },
    {
      "role": "model",
      "text": "今天天气很好。"
    }
  ]
}
```

**输出文件示例** (`cleaned.json`):

```json
{
  "conversations": [
    { "role": "user", "text": "你好，今天天气如何？" },
    { "role": "model", "text": "今天天气很好。" }
  ]
}
```

---

## 示例 2: 转换为 Markdown

```bash
python convo_sync.py convert cleaned.json -o output.md
```

**生成的 Markdown 文件** (`output.md`):

```markdown
# 对话记录

> 总计 2 条对话记录

---

## 👤 用户

你好，今天天气如何？

---

## 🤖 助手

今天天气很好。

---
```

---

## 示例 3: 完整工作流 (推荐)

一步完成清理 + 转换：

```bash
python convo_sync.py pipeline input.json -c output/cleaned.json -m output/conversations.md --stats
```

**输出**:

```
✓ JSON cleaning completed: output/cleaned.json
✓ Markdown conversion completed: output/conversations.md

Statistics:
  Total conversations: 601
  User messages: 257
  Assistant messages: 305
```

---

## 示例 4: 查看统计信息

**清理时查看统计**:

```bash
python convo_sync.py clean input.json -o output.json --stats
```

**转换时查看统计**:

```bash
python convo_sync.py convert input.json -o output.md --stats
```

**完整工作流统计**:

```bash
python convo_sync.py pipeline input.json --stats
```

---

## 示例 5: 在 Python 中使用 (编程方式)

```python
from src.cleaners import JSONCleaner
from src.converters import MarkdownConverter

# Step 1: Clean the JSON
cleaner = JSONCleaner('input.json', 'cleaned.json')
cleaner.clean()
stats = cleaner.get_stats()
print(f"Cleaned: {stats['total']} conversations")
print(f"  - Users: {stats['users']}")
print(f"  - Models: {stats['models']}")

# Step 2: Convert to Markdown
converter = MarkdownConverter('cleaned.json', 'output.md')
converter.convert()
conversion_stats = converter.get_stats()
print(f"Users in Markdown: {conversion_stats['users']}")
print(f"Assistants in Markdown: {conversion_stats['assistants']}")
```

---

## 示例 6: 实际应用场景

### 场景 A: 数据预处理管道

```bash
#!/bin/bash
# 处理多个 JSON 文件

for file in data/*.json; do
  echo "Processing $file..."
  python convo_sync.py pipeline "$file" \
    -c "cleaned/${file%.json}_cleaned.json" \
    -m "markdown/${file%.json}.md" \
    --stats
done
```

### 场景 B: 数据分析与可视化

```python
import json
from src.cleaners import JSONCleaner

# 清理数据
cleaner = JSONCleaner('raw_data.json', 'processed.json')
cleaner.clean()

# 加载处理后的数据
with open('processed.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 分析
conversations = data['conversations']
user_count = sum(1 for c in conversations if c['role'] == 'user')
model_count = sum(1 for c in conversations if c['role'] == 'model')

print(f"总对话数: {len(conversations)}")
print(f"用户消息: {user_count}")
print(f"模型回复: {model_count}")
print(f"用户比例: {user_count/len(conversations)*100:.1f}%")
```

### 场景 C: 文本搜索与索引

```python
import json
from src.cleaners import JSONCleaner

cleaner = JSONCleaner('data.json', 'clean.json')
cleaner.clean()

with open('clean.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 关键词搜索
keyword = "天气"
results = [
    c for c in data['conversations']
    if keyword in c['text']
]

print(f"包含 '{keyword}' 的对话: {len(results)}")
for r in results:
    print(f"  [{r['role'].upper()}]: {r['text'][:50]}...")
```

---

## 命令行参考

### Clean 命令

```bash
python convo_sync.py clean <input_json> -o <output_json> [--stats]

参数:
  input_json    输入 JSON 文件路径 (必需)
  -o, --output  输出 JSON 文件路径 (默认: cleaned.json)
  --stats       显示处理统计信息
```

### Convert 命令

```bash
python convo_sync.py convert <input_json> -o <output_md> [--stats]

参数:
  input_json    输入 JSON 文件路径 (必需)
  -o, --output  输出 Markdown 文件路径 (默认: output.md)
  --stats       显示转换统计信息
```

### Pipeline 命令

```bash
python convo_sync.py pipeline <input_json> [-c <clean_json>] [-m <output_md>] [--stats]

参数:
  input_json    原始 JSON 文件路径 (必需)
  -c, --clean   清理后的 JSON 输出路径 (默认: cleaned.json)
  -m, --markdown 最终 Markdown 输出路径 (默认: output.md)
  --stats       显示全过程统计信息
```

---

## 常见问题

### Q: 我的 JSON 文件格式与示例不同怎么办?

**A:** ConvoSync 支持多种 JSON 格式:

- `chunkedPrompt.chunks` 中的 `parts` 数组
- 直接的 `text` 字段
- 混合格式

如果您的格式不同，请参考 `src/cleaners.py` 中的 `_process_chunks()` 方法进行定制。

### Q: 输出的 Markdown 文件很大怎么办?

**A:** 您可以:

1. 使用文本编辑器打开 (VS Code, Sublime 等可处理大文件)
2. 使用命令行工具分割: `split -l 1000 output.md`
3. 转换为 PDF 进行存档

### Q: 如何集成到自动化工作流?

**A:** 使用 Python API:

```python
from src.cleaners import JSONCleaner
from src.converters import MarkdownConverter

cleaner = JSONCleaner('input.json', 'clean.json')
cleaner.clean()

converter = MarkdownConverter('clean.json', 'output.md')
converter.convert()
```

---

## 更多信息

查看 [README.md](../README.md) 了解项目概览。
