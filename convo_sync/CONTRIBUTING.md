# 贡献指南

感谢您对 ConvoSync 项目感兴趣！本指南将帮助您贡献代码。

## 开发环境设置

### 1. Clone 项目

```bash
git clone https://github.com/cagedbird/convo_sync.git
cd convo_sync
```

### 2. 创建虚拟环境

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 运行测试

```bash
python -m unittest tests.test_main -v
```

---

## 代码标准

### 风格指南

遵循 PEP 8:

- 使用 4 个空格缩进
- 最大行长度 100 字符
- 使用描述性变量名

### 文档标准

```python
def example_function(param1, param2):
    """
    简短的描述.

    更详细的描述 (如需要).

    Args:
        param1: 参数1 说明
        param2: 参数2 说明

    Returns:
        返回值说明

    Raises:
        ValueError: 异常说明
    """
    pass
```

### 提交消息标准

遵循 Conventional Commits:

```
<type>: <subject>

<body>

<footer>
```

**类型**:

- `feat`: 新功能
- `fix`: 修复 bug
- `test`: 添加测试
- `docs`: 文档更新
- `refactor`: 代码重构
- `perf`: 性能优化
- `chore`: 构建工具更新

**例子**:

```
feat: add CSV export support

- Implement CSVConverter class
- Add --csv option to CLI
- Update documentation

Closes #123
```

---

## 添加新功能

### 1. 创建特性分支

```bash
git checkout -b feature/my-feature
```

### 2. 实现功能

如果添加新的转换器:

```python
# src/converters.py 中添加新类
class CSVConverter:
    """转换为 CSV 格式"""

    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

    def convert(self):
        # 实现转换逻辑
        pass

    def get_stats(self):
        # 返回统计信息
        pass
```

### 3. 添加测试

```python
# tests/test_main.py 中添加
class TestCSVConverter(unittest.TestCase):
    def test_convert_to_csv(self):
        # 测试代码
        pass
```

### 4. 更新 CLI

```python
# convo_sync.py 中添加
def handle_csv(args):
    from src.converters import CSVConverter
    converter = CSVConverter(args.input, args.output)
    converter.convert()

# 在 main() 中添加子命令
subparsers.add_parser('csv', help='Convert to CSV')
```

### 5. 运行测试

```bash
python -m unittest tests.test_main -v
```

### 6. 提交 PR

```bash
git push origin feature/my-feature
# 在 GitHub 上创建 Pull Request
```

---

## 修复 Bug

### 1. 搜索现有 Issue

```bash
# 检查是否已有人报告
```

### 2. 创建修复分支

```bash
git checkout -b fix/bug-name
```

### 3. 编写复现测试

```python
def test_bug_reproduction(self):
    # 复现 bug 的测试
    pass
```

### 4. 修复 bug

修改源代码

### 5. 验证修复

```bash
python -m unittest tests.test_main -v
```

### 6. 提交 PR

指向原始 Issue

---

## 文档贡献

### 更新 README

- 保持清晰简洁
- 更新目录
- 添加示例

### 更新示例

```markdown
### 场景 X: 新场景

代码示例...

输出...
```

### 更新 API 文档

- 保持文档字符串最新
- 更新类型提示

---

## 测试要求

### 添加新功能时:

- 编写至少 2 个测试用例
- 测试成功路径
- 测试异常情况
- 覆盖率 ≥ 80%

### 修复 Bug 时:

- 编写复现 bug 的测试
- 验证修复有效
- 确保不引入新 bug

### 运行覆盖率检查

```bash
python -m pytest tests/ --cov=src
```

---

## 代码审查

### PR 检查清单

在提交 PR 前，确保:

- [ ] 代码遵循 PEP 8
- [ ] 添加或更新了测试
- [ ] 所有测试通过 ✅
- [ ] 更新了文档
- [ ] 提交消息清晰有意义
- [ ] 没有合并冲突
- [ ] 没有 Debug 代码

### 审查反馈

- 保持评论建设性
- 讨论设计决策
- 请求澄清
- 建议改进

---

## 发布新版本

仅项目维护者:

### 1. 更新版本

```python
# src/__init__.py
__version__ = "1.1.0"
```

### 2. 更新 CHANGELOG

```markdown
## [1.1.0] - 2024-XX-XX

### Added

- 新功能...

### Fixed

- Bug 修复...
```

### 3. 创建 Tag

```bash
git tag v1.1.0
git push origin v1.1.0
```

### 4. 发布到 PyPI

```bash
python setup.py sdist bdist_wheel
twine upload dist/*
```

---

## 常见问题

### Q: 我应该从哪个分支创建特性分支?

**A**: 从 `main` 分支创建

### Q: 如何处理 merge 冲突?

**A**:

```bash
git fetch origin
git rebase origin/main
# 解决冲突
git rebase --continue
```

### Q: 我可以编辑文档吗?

**A**: 可以！只需遵循 Markdown 格式

### Q: 我的 PR 被拒绝了怎么办?

**A**: 这很正常。查看反馈，进行改进，重新提交

---

## 行为准则

### 我们的价值观

- **尊重**: 尊重所有贡献者
- **包容**: 欢迎不同的观点
- **合作**: 一起创造更好的东西

### 不可接受的行为

- 骚扰或歧视
- 人身攻击
- 发布私人信息

任何不当行为将导致禁用账户

---

## 帮助与支持

- 📖 查看 [README.md](README.md)
- 📚 查看 [EXAMPLES.md](examples/EXAMPLES.md)
- 💬 开启 GitHub Discussions
- 🐛 报告 Bug 在 GitHub Issues

---

## 许可证

所有贡献均按 MIT License 许可

---

感谢您的贡献！🎉
