# ConvoSync

🚀 **AI Conversation Data Processing Toolkit**

一个专业的 AI 对话数据清理、转换和管理工具集。

## ✨ 特性

- ✅ **JSON 清理**：去除碎片化结构,标准化对话数据
- ✅ **Markdown 转换**：生成清晰、易渲染的 Markdown 格式
- ✅ **思维链过滤**：自动删除 AI 思维过程,保留核心对话
- ✅ **数据统计**：自动统计用户和助手消息数量
- ✅ **完整工作流**：支持 clean → convert 完整管道
- ✅ **专业 CLI**：易用的命令行界面
- ✅ **零依赖**：纯 Python 标准库实现

## 快速开始

### 安装

使用 Pixi (推荐):

```bash
# 克隆仓库
git clone https://github.com/cagedbird043/convo_sync.git
cd convo_sync

# 使用 Pixi 安装依赖
pixi install

# 激活环境
pixi shell
```

传统方式:

```bash
pip install convo-sync
```

### 基本使用

```bash
# 清理 JSON 数据
pixi run run-clean input.json -o output.json

# 转换为 Markdown
pixi run run-convert input.json -o output.md

# 完整工作流
pixi run run-pipeline input.json --stats
```

## 文档

- [安装指南](getting-started/installation.md)
- [快速开始](getting-started/quickstart.md)
- [CLI 使用](guide/cli.md)
- [API 参考](api/cleaners.md)

## 开发

本项目使用现代化的 Python 开发工具链:

- **Pixi**: 跨平台环境管理
- **Ruff**: 快速的 linting 和 formatting
- **MyPy**: 类型检查
- **pytest**: 测试框架
- **pre-commit**: Git hooks

查看 [贡献指南](contributing.md) 了解更多信息。

## 许可

MIT License
