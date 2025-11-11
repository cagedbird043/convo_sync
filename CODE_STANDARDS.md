# 代码规范与质量标准

## 1. 概览

本项目遵循完整的 Python 代码规范和最佳实践。所有代码通过自动化工具链进行检查和格式化，确保代码质量和一致性。

## 2. 代码风格规范

### 2.1 行长度

- **最大行长度**: 120 字符
- **理由**: 平衡可读性和现代宽屏显示
- **工具**: Black, Flake8, Pylint

### 2.2 代码格式化

- **工具**: Black (v25.1.0)
- **命令**: `black --line-length=120 .`
- **特点**:
  - 自动格式化，减少争议
  - 确保一致的代码风格
  - 与 Flake8 和 isort 完全兼容

### 2.3 导入排序

- **工具**: isort (v5.13.2)
- **命令**: `isort --profile black --line-length 120 .`
- **规则**:
  - 标准库导入
  - 第三方库导入
  - 本地导入
  - 字母顺序排列

### 2.4 命名规范

- **模块名**: `snake_case` (例: `converters.py`)
- **函数名**: `snake_case` (例: `def get_stats()`)
- **类名**: `PascalCase` (例: `class MarkdownConverter`)
- **常量名**: `UPPER_CASE` (例: `MAX_LINE_LENGTH = 120`)
- **变量名**: `snake_case` (例: `user_count`)

### 2.5 缩进

- **制表符**: 4 个空格
- **禁止**: 混合制表符和空格
- **工具**: pre-commit hooks 自动检查

## 3. 代码检查工具

### 3.1 Flake8 (v7.1.2)

- **用途**: PEP 8 风格检查和代码质量
- **配置文件**: `.flake8`
- **忽略规则**:
  - `E203`: 冒号前空格 (Black 兼容)
  - `E266`: 行注释与代码间隔
  - `E501`: 行过长 (由 Black 处理)
  - `W503`: 断行时的二进制运算符
  - Docstring 检查 (D\*) - 过度严格

### 3.2 Pylint (v3.3.9)

- **用途**: 深度代码分析和质量评分
- **配置文件**: `.pylintrc`
- **最低评分**: 无硬性要求，持续改进
- **关键指标**:
  - 无未定义变量
  - 无未使用导入
  - 无悬挂异常

### 3.3 MyPy (v1.7.1)

- **用途**: 静态类型检查
- **配置**: `pyproject.toml`
- **模式**: 非强制类型检查 (allow untyped)
- **目标**: 逐步增加类型注解覆盖率

### 3.4 Pre-commit Hooks

完整的检查清单：

1. **Black** - 代码格式化
2. **isort** - 导入排序
3. **Flake8** - 风格和质量
4. **Pylint** - 深度分析
5. **MyPy** - 类型检查
6. **Pre-commit-hooks**:
   - 末尾空格去除
   - 文件末尾修复
   - YAML 检查
   - 大文件检测 (>1MB)
   - JSON 格式检查
   - 合并冲突检查
   - 私钥检测
   - 行终止符统一 (LF)

## 4. 注释规范

### 4.1 代码注释

```python
# 好的注释：清晰说明意图
if role in self.message_counter:
    self.message_counter[role] += 1

# 避免：重复代码含义
x = x + 1  # 增加 x
```

### 4.2 文档字符串

- **格式**: Google 风格
- **位置**: 模块、类、函数顶部
- **内容**: 描述、参数、返回值、异常

```python
def _normalize_code_blocks(self, text):
    """Normalize code block backticks to proper markdown syntax.

    Ensures code blocks use appropriate number of backticks:
    - Single backticks for inline code
    - Triple backticks (minimum) for code blocks
    - Uses language specifier when available

    Args:
        text: Input text with code blocks

    Returns:
        Text with normalized code blocks
    """
```

## 5. 异常处理规范

### 5.1 异常捕获

```python
# 好的做法：明确指出异常类型
except FileNotFoundError as e:
    raise FileNotFoundError(f"Input file not found: {e}") from e

# 避免：捕获过宽的异常
except Exception:  # 太宽泛
    pass
```

### 5.2 异常链

```python
# 推荐：使用异常链
try:
    result = json.load(f)
except json.JSONDecodeError as e:
    raise ValueError(f"Invalid JSON file: {e}") from e
```

## 6. 类设计规范

### 6.1 类大小限制

- **最大方法数**: 建议 < 10
- **最大属性数**: 建议 < 7
- **最大参数数**: 函数参数 < 5

### 6.2 方法命名

- 私有方法: `_method_name()`
- 特殊方法: `__method_name__()`
- 公开 API: `method_name()`

## 7. 测试规范

### 7.1 测试文件位置

- **目录**: `tests/`
- **文件命名**: `test_*.py` 或 `*_test.py`
- **函数命名**: `test_*`

### 7.2 测试覆盖率

- **目标**: > 70%
- **关键路径**: 100%
- **工具**: pytest + coverage

### 7.3 运行测试

```bash
pytest -v --tb=short
pytest --cov=src tests/
```

## 8. Git 提交规范

### 8.1 Commit Message 格式

```
<type>: <subject>

<body>
```

### 8.2 Commit Types

- **feat**: 新功能
- **fix**: 修复 bug
- **refactor**: 重构（不改变功能）
- **chore**: 配置、依赖等
- **docs**: 文档更新
- **test**: 测试代码
- **style**: 代码风格（不改变逻辑）
- **perf**: 性能优化

### 8.3 Commit 检查

Pre-commit hooks 会自动在提交前检查：

- 代码格式
- 导入排序
- Flake8 风格
- Pylint 质量
- MyPy 类型
- 通用检查

## 9. 环境设置

### 9.1 虚拟环境

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### 9.2 Pre-commit 安装

```bash
pre-commit install
pre-commit run --all-files  # 首次运行
```

### 9.3 配置文件

- `pyproject.toml` - 工具配置和项目元数据
- `.flake8` - Flake8 配置
- `.pylintrc` - Pylint 配置
- `.pre-commit-config.yaml` - Pre-commit 钩子配置

## 10. 开发工作流

### 10.1 编写代码

```bash
# 激活虚拟环境
source .venv/bin/activate

# 编写代码
# ... 编辑文件 ...

# 自动格式化
black --line-length=120 .
isort --profile black --line-length 120 .
```

### 10.2 提交代码

```bash
git add .
git commit -m "feat: 新功能描述"
# Pre-commit hooks 会自动运行检查
```

### 10.3 推送前检查

```bash
pre-commit run --all-files
pytest -v
```

## 11. 常见问题

### 11.1 Black 和 Flake8 冲突？

- 不会冲突：已配置兼容
- Black 处理代码格式
- Flake8 检查逻辑问题

### 11.2 如何跳过某个检查？

```python
# 禁用单行
x = y  # noqa: E501

# 禁用整个文件
# flake8: noqa

# Pylint
# pylint: disable=broad-exception-caught
```

### 11.3 导入顺序不对？

```bash
isort --check-only src/  # 检查
isort src/  # 自动修复
```

## 12. 性能优化建议

### 12.1 代码审查要点

- 循环中避免重复计算
- 使用生成器处理大数据
- 缓存重复的昂贵操作

### 12.2 内存优化

- 及时释放大对象
- 使用流式处理大文件
- 避免全量加载不必要的数据

## 13. 安全最佳实践

### 13.1 输入验证

- 总是验证外部输入
- 使用类型注解
- 检查边界条件

### 13.2 错误处理

- 不要暴露敏感信息
- 记录足够的上下文
- 提供清晰的错误消息

## 14. 文档维护

### 14.1 README

- 项目描述
- 快速开始
- API 文档链接

### 14.2 代码注释

- 解释"为什么"，不是"是什么"
- 保持与代码同步
- 定期审查

## 15. CI/CD 流程

### 15.1 GitHub Actions

- 每次 PR 自动运行 pre-commit
- 运行完整的测试套件
- 生成覆盖率报告

### 15.2 保护分支

- 要求通过所有检查
- 需要至少 1 个审查者
- 自动删除合并后的分支

---

**维护者**: cagedbird043
**最后更新**: 2025 年 11 月 11 日
**版本**: 1.0
