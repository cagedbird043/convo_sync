# 贡献指南

感谢你对 ConvoSync 的兴趣!

## 开发环境设置

### 1. 安装 Pixi

```bash
curl -fsSL https://pixi.sh/install.sh | bash
```

### 2. 克隆并设置项目

```bash
git clone https://github.com/cagedbird043/convo_sync.git
cd convo_sync
pixi install
pixi run hooks-install
```

### 3. 激活环境

```bash
pixi shell
```

## 开发工作流

### 运行测试

```bash
pixi run test
```

### 代码检查

```bash
# Linting
pixi run lint

# 类型检查
pixi run typecheck

# 安全检查
pixi run security

# 运行所有检查
pixi run check-all
```

### 格式化代码

```bash
pixi run format
```

### 运行 pre-commit

```bash
pixi run hooks-run
```

## 提交规范

我们使用 [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

### 类型

- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式
- `refactor`: 重构
- `test`: 测试
- `chore`: 构建/工具

### 示例

```
feat(cleaners): add support for custom think tags

- Added --think-tag option
- Updated documentation
- Added tests

Closes #123
```

## Pull Request 流程

1. Fork 仓库
2. 创建特性分支 (`git checkout -b feat/amazing-feature`)
3. 提交更改 (`git commit -m 'feat: add amazing feature'`)
4. 推送到分支 (`git push origin feat/amazing-feature`)
5. 开启 Pull Request

### PR 检查清单

- [ ] 代码通过所有测试 (`pixi run test`)
- [ ] 代码通过 linting (`pixi run lint`)
- [ ] 代码通过类型检查 (`pixi run typecheck`)
- [ ] 添加了必要的测试
- [ ] 更新了文档
- [ ] 遵循了提交规范

## 项目结构

```
convo_sync/
├── src/              # 源代码
│   ├── cleaners.py   # 清理逻辑
│   └── converters.py # 转换逻辑
├── tests/            # 测试
├── docs/             # 文档
├── examples/         # 示例
├── pixi.toml         # Pixi 配置
├── pyproject.toml    # Python 项目配置
└── mkdocs.yml        # 文档配置
```

## 测试指南

### 编写测试

```python
def test_clean_conversation():
    """Test conversation cleaning."""
    data = {"messages": [...]}
    result = clean_conversation(data)
    assert result is not None
```

### 运行特定测试

```bash
pixi run pytest tests/test_cleaners.py -v
```

### 覆盖率

```bash
pixi run test  # 自动生成覆盖率报告
```

## 文档

### 本地预览

```bash
pixi run -e docs docs-serve
```

访问 http://localhost:8000

### 构建文档

```bash
pixi run -e docs docs-build
```

## 发布流程

1. 更新版本号 (`pyproject.toml` 和 `pixi.toml`)
2. 更新 CHANGELOG
3. 提交: `git commit -m "chore: bump version to x.y.z"`
4. 创建标签: `git tag vx.y.z`
5. 推送: `git push && git push --tags`

GitHub Actions 会自动:

- 运行所有测试
- 构建包
- 发布到 PyPI
- 部署文档

## 获取帮助

- GitHub Issues: 报告 bug 或请求功能
- Discussions: 提问和讨论

## 行为准则

请保持友善和专业。我们欢迎所有贡献者!
