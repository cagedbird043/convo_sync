# ConvoSync

🚀 **AI Conversation Data Processing Toolkit**

专为 Google AI Studio 导出的对话数据设计的清理和转换工具，使用启发式算法智能识别代码块。

![Zero Dependencies](https://img.shields.io/badge/dependencies-zero-success.svg)
![No LLM Required](https://img.shields.io/badge/LLM-not%20required-brightgreen.svg)
![Compression Rate](https://img.shields.io/badge/compression-71.4%25-orange.svg)
![Processing Speed](https://img.shields.io/badge/speed-%3C%201s-blueviolet.svg)

## ✨ 核心特性

- ✅ **Google AI Studio 支持**：专门处理 GAS 导出的 JSON 格式
- ✅ **智能思维过滤**：自动删除 AI 思维过程（thinking process），保留核心对话
- ✅ **智能代码检测**：区分真实代码与文本描述，保留重要信息
- ✅ **保留模型设置**：完整保留 runSettings、systemInstruction 和文件引用
- ✅ **可重新导入**：清理后的 JSON 可以重新导入 Google AI Studio
- ✅ **高压缩率**：Token 使用量减少 70% 以上
- ✅ **Markdown 转换**：生成清晰、易渲染的 Markdown 格式
- ✅ **数据统计**：自动统计消息数量和文件引用
- ✅ **灵活控制**：通过参数控制保留或删除特定内容

## 🎯 为什么选择 ConvoSync？

### 不用 LLM 的智能检测

ConvoSync 使用**启发式算法**而非 LLM 来检测代码块：

| 方案          | 处理时间   | 成本   | 准确率   | 依赖     |
| ------------- | ---------- | ------ | -------- | -------- |
| **ConvoSync** | **< 0.1s** | **$0** | **100%** | **零**   |
| LLM API       | 23.4s      | $0.054 | 99%+     | 需要 API |

**速度提升 263 倍 · 完全免费 · 零依赖**

### 真实性能数据

测试文件：PIPA2025_11_11.json

- 📉 **压缩率**：71.4%（1108 KB → 317 KB）
- ⚡ **处理速度**：< 0.1 秒
- 🎯 **代码块识别**：78 个全部正确处理
- ✅ **测试准确率**：100%（6/6 通过）
- 🔓 **零依赖**：无需网络、API、外部服务

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

## 📚 文档导航

### 🚀 快速上手

- [安装指南](getting-started/installation.md) - 多种安装方式
- [快速开始](getting-started/quickstart.md) - 5 分钟入门教程

### 📖 使用指南

- [CLI 使用](guide/cli.md) - 命令行完整参考
- [使用示例](guide/examples.md) - 实际应用场景
- [Pre-commit 配置](guide/pre-commit.md) - 自动化工作流

### 🧠 技术深度

- [算法详解](algorithm.md) - 智能代码检测的启发式算法原理
- [性能对比](performance-comparison.md) - 启发式算法 vs LLM 的详细分析

### 🔧 API 参考

- [Cleaners API](api/cleaners.md) - JSON 清理模块
- [Converters API](api/converters.md) - Markdown 转换模块

### 🤝 参与贡献

- [贡献指南](contributing.md) - 如何参与项目开发

## 💡 核心理念

!!! success "工程智慧"
**ConvoSync 证明了：不是所有问题都需要 LLM 来解决**

    通过精心设计的启发式算法，我们实现了：

    - ⚡ **263 倍**的速度提升（0.089s vs 23.4s）
    - 💰 **完全免费**的处理成本（$0 vs $0.054/文件）
    - 🎯 **100%** 的测试准确率（6/6 测试通过）
    - 🔓 **零依赖**的独立运行（无需网络、API、外部服务）

!!! quote "设计哲学"
**工程的艺术在于选择合适的工具，而不是使用最强大的工具。** 🔨✨

## 🎨 智能代码检测原理

ConvoSync 使用多重启发式规则区分代码和文本：

```python
# 会被删除的代码块
def hello():
    print("world")
```

```text
# 会被保留的文本内容
这是 AI 的总结
```

**检测依据**（无需 LLM）：

- ✅ 编程关键词（def, class, import, function 等 28+ 个）
- ✅ 符号密度（{}、[]、()、=> 等特殊符号）
- ✅ 缩进模式（代码的一致性缩进）
- ✅ 函数调用模式（排除中文括号）
- ✅ 行数检查（超长内容更可能是代码）

详细了解：[算法详解](algorithm.md) | [性能对比](performance-comparison.md)

## 🔧 开发

本项目使用现代化的 Python 开发工具链:

- **Pixi**: 跨平台环境管理
- **Ruff**: 快速的 linting 和 formatting
- **MyPy**: 类型检查
- **pytest**: 测试框架
- **pre-commit**: Git hooks

查看 [贡献指南](contributing.md) 了解更多信息。

## 📄 许可

MIT License
