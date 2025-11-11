# 安装

## 使用 Pixi (推荐)

Pixi 是一个快速、跨平台的包管理器,提供完全可复现的开发环境。

### 1. 安装 Pixi

=== "Linux / macOS"

    ```bash
    curl -fsSL https://pixi.sh/install.sh | bash
    ```

=== "Windows"

    ```powershell
    iwr -useb https://pixi.sh/install.ps1 | iex
    ```

### 2. 克隆并设置项目

```bash
# 克隆仓库
git clone https://github.com/cagedbird043/convo_sync.git
cd convo_sync

# 使用 Pixi 安装所有依赖
pixi install

# 激活开发环境
pixi shell
```

就这么简单!所有依赖(包括 Python 本身)都会自动安装。

## 使用 pip

如果你更喜欢传统方式:

```bash
# 确保你有 Python 3.11+
python --version

# 从源码安装
git clone https://github.com/cagedbird043/convo_sync.git
cd convo_sync
pip install -e .

# 或从 PyPI 安装 (如果已发布)
pip install convo-sync
```

## 开发安装

如果你想参与开发:

```bash
# 使用 Pixi (推荐)
pixi install
pixi run hooks-install  # 安装 pre-commit hooks

# 或使用 pip
pip install -e ".[dev]"
pre-commit install
```

## 验证安装

```bash
# 测试 CLI
python convo_sync.py --help

# 使用 Pixi
pixi run test
```

## 下一步

- [快速开始](quickstart.md): 学习基本用法
- [CLI 使用](../guide/cli.md): 详细的命令行选项
