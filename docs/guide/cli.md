# CLI 使用

ConvoSync 提供了强大的命令行界面。

## 命令概览

```bash
convo_sync <command> [options]
```

### 可用命令

- `clean`: 清理 JSON 数据
- `convert`: 转换为 Markdown
- `pipeline`: 完整工作流

## clean 命令

清理和标准化 JSON 对话数据。

```bash
pixi run run-clean <input> [options]
```

### 选项

- `-o, --output FILE`: 输出文件路径 (默认: 添加 `.cleaned` 后缀)
- `--think-tag TAG`: 自定义思维链标签 (默认: `think`)
- `--remove-empty`: 移除空消息
- `--verbose`: 详细输出

### 示例

```bash
# 基本用法
pixi run run-clean conversation.json

# 指定输出
pixi run run-clean input.json -o output.json

# 自定义思维链标签
pixi run run-clean input.json --think-tag "reasoning"

# 移除空消息并显示详细信息
pixi run run-clean input.json --remove-empty --verbose
```

## convert 命令

将 JSON 转换为 Markdown 格式。

```bash
pixi run run-convert <input> [options]
```

### 选项

- `-o, --output FILE`: 输出文件路径 (默认: 替换为 `.md` 扩展名)
- `--keep-think`: 保留思维链内容
- `--format FORMAT`: 输出格式 (`markdown`, `html`) (默认: `markdown`)
- `--title TITLE`: 自定义文档标题
- `--stats`: 在末尾添加统计信息

### 示例

```bash
# 基本转换
pixi run run-convert conversation.json

# 保留思维链
pixi run run-convert input.json --keep-think

# 添加统计信息
pixi run run-convert input.json -o output.md --stats

# 自定义标题
pixi run run-convert input.json --title "My Conversation"
```

## pipeline 命令

执行完整的清理和转换流程。

```bash
pixi run run-pipeline <input> [options]
```

### 选项

- `-o, --output FILE`: Markdown 输出路径
- `--cleaned FILE`: 保存清理后的 JSON
- `--stats`: 显示统计信息
- `--all-options`: 应用所有优化选项

### 示例

```bash
# 完整流程
pixi run run-pipeline conversation.json

# 指定所有输出
pixi run run-pipeline input.json \
  --cleaned cleaned.json \
  -o output.md \
  --stats

# 应用所有优化
pixi run run-pipeline input.json --all-options
```

## 使用 Pixi 任务

项目预定义了方便的任务:

```bash
# 查看所有可用任务
pixi task list

# 运行测试
pixi run test

# 代码检查
pixi run lint
pixi run typecheck
pixi run check  # 运行所有检查

# 格式化代码
pixi run format
```

## Python API

也可以在 Python 代码中使用:

```python
from src.cleaners import clean_conversation
from src.converters import convert_to_markdown

# 清理数据
cleaned = clean_conversation(data)

# 转换为 Markdown
markdown = convert_to_markdown(cleaned)
```

查看 [API 文档](../api/cleaners.md) 了解更多。
