# Pre-commit Hooks 配置

## 设计理念

本项目采用 **Pixi + Pre-commit** 的混合策略，这是 2024-2025 年的最佳实践。

## 架构说明

### 🎯 两层架构

```
Pre-commit (轻量级触发器)
    ↓
Pixi Tasks (实际执行)
    ↓
统一的开发环境
```

### 为什么这样设计？

#### ✅ 优势

1. **环境一致性 100%**

   - 所有工具在同一个 pixi 环境中运行
   - CI/CD、本地开发、pre-commit 使用完全相同的工具版本
   - 避免 "在我机器上能运行" 问题

2. **速度优势**

   - Pre-commit 不需要为每个 hook 创建独立的 virtualenv
   - Pixi 的依赖解析和缓存机制更快
   - 首次运行后，后续几乎即时完成

3. **维护简单**

   - 只需在 `pixi.toml` 中管理依赖
   - 不需要在 `.pre-commit-config.yaml` 中重复声明工具版本
   - 工具升级只需更新一个地方

4. **完全可复现**
   - `pixi.lock` 锁定所有依赖（包括系统级）
   - 任何人、任何时间、任何机器都是相同的结果

#### ⚠️ 权衡

- 需要团队成员安装 Pixi（一次性成本）
- Pre-commit 的自动安装功能不适用于 pixi tasks

## 配置详解

### .pre-commit-config.yaml

```yaml
repos:
  # 轻量级检查（不依赖 Python）
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      # ... 其他文件检查

  # 所有 Python 工具通过 pixi 执行
  - repo: local
    hooks:
      - id: ruff-lint
        name: ruff lint
        entry: pixi run lint
        language: system
        types: [python]
        pass_filenames: false

      # ... 其他 hooks
```

### 关键配置说明

- **`repo: local`** - 使用本地 hooks 而非远程仓库
- **`language: system`** - 使用系统命令（pixi）
- **`entry: pixi run <task>`** - 直接调用 pixi 任务
- **`pass_filenames: false`** - 让 pixi task 自己决定检查哪些文件

## 使用方法

### 安装 hooks

```bash
pixi run hooks-install
```

### 手动运行所有 hooks

```bash
pixi run hooks-run
```

### 提交时自动运行

```bash
git add .
git commit -m "feat: add feature"
# hooks 自动运行
```

### 跳过 hooks（紧急情况）

```bash
git commit -m "fix: emergency fix" --no-verify
```

## 与 CI/CD 的关系

Pre-commit 和 CI/CD 使用**完全相同的命令**：

```yaml
# .github/workflows/ci.yml
- name: Run checks
  run: pixi run check-all
```

```bash
# Pre-commit
pixi run lint
pixi run typecheck
pixi run security
```

这保证了：

- ✅ 本地和 CI 结果一致
- ✅ 开发者提前发现问题
- ✅ 减少 CI 失败次数

## 故障排除

### 问题：Hook 运行失败

```bash
# 重新安装环境
pixi install

# 重新安装 hooks
pixi run hooks-install
```

### 问题：速度慢

首次运行会安装 pre-commit 环境，后续会很快：

```bash
# 预先安装所有环境
pixi run hooks-run
```

### 问题：检测到修改但不是我改的

这是 formatter 自动修复的，重新提交即可：

```bash
git add .
git commit -m "chore: apply formatter fixes"
```

## 对比传统方案

| 特性       | Pixi + Pre-commit | 传统 Pre-commit   | Poetry + Pre-commit |
| ---------- | ----------------- | ----------------- | ------------------- |
| 环境一致性 | ✅ 完美           | ❌ 每个 hook 独立 | ⚠️ Python 包一致    |
| 速度       | ⚡⚡⚡            | ⚡                | ⚡⚡                |
| 系统依赖   | ✅ 自动处理       | ❌ 手动安装       | ❌ 手动安装         |
| 维护成本   | ✅ 低             | ⚠️ 中             | ⚠️ 中               |
| CI/CD 一致 | ✅ 100%           | ❌ 需配置         | ⚠️ 部分一致         |
| 跨平台     | ✅ 完美           | ⚠️ 需配置         | ⚠️ 需配置           |

## 最佳实践建议

1. **团队协作**

   - 在 README 中说明需要安装 Pixi
   - 提供一键安装脚本

2. **性能优化**

   - 首次克隆后立即运行 `pixi install`
   - 定期运行 `pixi update` 更新依赖

3. **自定义 hooks**

   - 新增检查添加到 `pixi.toml` 的 `[tasks]`
   - 然后在 `.pre-commit-config.yaml` 中引用

4. **调试模式**

   ```bash
   # 详细输出
   SKIP=ruff-lint pixi run hooks-run

   # 跳过特定 hook
   SKIP=mypy git commit -m "wip"
   ```

## 总结

这个方案结合了：

- ✅ Pre-commit 的自动触发机制
- ✅ Pixi 的环境管理能力
- ✅ 现代 Rust 工具链的速度

这就是 2025 年 Python 项目的标准配置！🚀
