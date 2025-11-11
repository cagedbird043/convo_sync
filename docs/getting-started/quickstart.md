# 快速开始

本指南将帮助你在 5 分钟内开始使用 ConvoSync。

## 基本工作流

### 1. 清理 JSON 数据

如果你有一个包含 AI 对话的 JSON 文件:

```bash
pixi run run-clean input.json -o cleaned.json
```

这会:

- 移除思维链 (`<think>` 标签)
- 标准化消息结构
- 去除冗余数据

### 2. 转换为 Markdown

将清理后的 JSON 转换为易读的 Markdown:

```bash
pixi run run-convert cleaned.json -o output.md
```

### 3. 一键完成(推荐)

使用 pipeline 命令一次完成所有操作:

```bash
pixi run run-pipeline input.json --stats
```

这会:

1. 清理 JSON 数据
2. 转换为 Markdown
3. 显示统计信息

## 示例

假设你有这样的输入 JSON:

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Hello, how are you?"
    },
    {
      "role": "assistant",
      "content": "<think>Let me think...</think>I'm doing great!"
    }
  ]
}
```

运行:

```bash
pixi run run-pipeline input.json -o output.md --stats
```

输出 `output.md`:

```markdown
# Conversation

**User:**
Hello, how are you?

**Assistant:**
I'm doing great!

---

📊 Statistics:

- User messages: 1
- Assistant messages: 1
- Total messages: 2
```

## 高级选项

### 自定义思维链标签

```bash
pixi run run-clean input.json -o output.json --think-tag "reasoning"
```

### 保留思维链

```bash
pixi run run-convert input.json -o output.md --keep-think
```

### 详细输出

```bash
pixi run run-pipeline input.json --verbose
```

## 下一步

- 查看 [CLI 使用指南](../guide/cli.md) 了解所有选项
- 阅读 [示例](../guide/examples.md) 查看更多用例
- 探索 [API 文档](../api/cleaners.md) 在代码中使用
