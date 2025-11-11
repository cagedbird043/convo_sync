# ConvoSync

[![CI](https://github.com/cagedbird043/convo_sync/actions/workflows/ci.yml/badge.svg)](https://github.com/cagedbird043/convo_sync/actions/workflows/ci.yml)
[![Documentation](https://github.com/cagedbird043/convo_sync/actions/workflows/docs.yml/badge.svg)](https://github.com/cagedbird043/convo_sync/actions/workflows/docs.yml)
[![codecov](https://codecov.io/gh/cagedbird043/convo_sync/branch/main/graph/badge.svg)](https://codecov.io/gh/cagedbird043/convo_sync)
[![Python 3.12-3.14](https://img.shields.io/badge/python-3.12%20|%203.13%20|%203.14-blue.svg)](https://www.python.org/downloads/)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

🚀 **AI Conversation Data Processing Toolkit**

一个专业的 AI 对话数据清理、转换和管理工具集。

## 特点

- ✅ **JSON 清理**：去除碎片化结构，标准化对话数据
- ✅ **Markdown 转换**：生成清晰、易渲染的 Markdown 格式
- ✅ **思维链过滤**：自动删除 AI 思维过程，保留核心对话
- ✅ **数据统计**：自动统计用户和助手消息数量
- ✅ **完整工作流**：支持 clean → convert 完整管道
- ✅ **专业 CLI**：易用的命令行界面

## 安装

```bash
# Clone the repository
git clone <repo-url>
cd convo_sync

# No external dependencies required!
# 无需任何外部依赖！
```

## 使用

### 基本命令

**1. 清理 JSON 数据**

```bash
python convo_sync.py clean input.json -o output.json
```

**2. 转换为 Markdown**

```bash
python convo_sync.py convert input.json -o output.md
```

**3. 完整工作流（推荐）**

```bash
python convo_sync.py pipeline input.json --stats
```

### 高级选项

```bash
# 查看统计信息
python convo_sync.py clean input.json --stats
python convo_sync.py convert input.json --stats

# 保留 AI 思维过程（默认会删除）
python convo_sync.py convert input.json --no-thinking
python convo_sync.py pipeline input.json --no-thinking

# 自定义输出路径
python convo_sync.py pipeline input.json \
  -c cleaned.json \
  -m output.md \
  --stats
```

## 输出格式

### JSON 格式

清理后的 JSON 采用标准格式：

```json
{
  "conversations": [
    { "role": "user", "text": "用户消息..." },
    { "role": "model", "text": "助手回复..." }
  ]
}
```

### Markdown 格式

转换后的 Markdown 采用清晰的分类格式：

```markdown
# 对话记录

> 总计 601 条对话记录

---

## 👤 用户

用户消息内容...

---

## 🤖 助手

助手回复内容...

---
```

## 性能

处理 600+ 条对话数据的性能指标：

| 指标          | 值          |
| ------------- | ----------- |
| 原始文件大小  | 3.9 MB      |
| 清理后大小    | 1.9 MB      |
| 最终 Markdown | 1.8 MB      |
| **总压缩率**  | **53.8%** ↓ |

## 项目结构

```
convo_sync/
├── src/
│   ├── __init__.py          # Package initialization
│   ├── cleaners.py          # JSON cleaning module
│   └── converters.py        # Markdown conversion module
├── tests/                   # Unit tests (coming soon)
├── examples/                # Usage examples
├── convo_sync.py            # CLI entry point
├── README.md                # This file
├── setup.py                 # Installation configuration
└── .gitignore              # Git ignore rules
```

## 开发

### 运行测试

```bash
python -m pytest tests/
```

### 添加新功能

1. 在 `src/` 中创建新模块
2. 在 `tests/` 中添加测试
3. 在 `convo_sync.py` 中添加 CLI 命令

## 许可证

MIT License

## 作者

Cagedbird

## 贡献

欢迎提交 Issue 和 Pull Request！

---

**💡 提示**：查看 `examples/` 目录了解更多用法示例。
