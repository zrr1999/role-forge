## 提交流程

- 小步提交，确保每个提交聚焦单一主题
- 提交前运行 `just ci` 确保格式、lint、类型检查和测试通过

## Commit message 规范

围绕项目功能模块来写 message，格式统一为：

`<emoji> <type>(<scope>): <subject>`

scope 为可选项，用于标注影响的模块。

### 推荐 type

- `✨ feat` 新增功能
- `🐛 fix` 修复 bug
- `♻️ refactor` 重构（不改变外部行为）
- `📝 docs` 文档调整
- `✅ test` 测试相关
- `🔧 chore` 构建、CI、依赖等杂项

### 示例

- `✨ feat(adapter): add Cursor adapter`
- `🐛 fix(claude): align output with official .claude/agents format`
- `♻️ refactor: rename compiler to caster`
- `📝 docs: add README and AGENTS.md`
- `✅ test(opencode): add snapshot tests for permission block`
- `🔧 chore: upgrade toolchain config`

## PR 标题规范

- 与提交规范保持一致
- 描述要更宏观，概括 PR 整体变更
- CI 会自动检查 PR 标题是否符合规范

### 示例

- `✨ feat(adapter): add Cursor adapter support`
- `🐛 fix(loader): handle missing frontmatter gracefully`
- `🔧 chore: upgrade CI to Python 3.14`

## 开发命令

```bash
just install       # 安装依赖
just format        # 格式化代码
just lint          # Lint 检查
just check         # 类型检查
just test          # 运行测试
just cov           # 测试 + 覆盖率
just ci            # 完整 CI 流程（format + lint + check + test）
just pre-commit    # 运行 pre-commit 钩子
```

## 项目结构

```
src/agent_caster/
├── cli.py          # CLI 入口（init / cast / list）
├── config.py       # refit.toml 解析
├── loader.py       # Agent 定义加载（YAML frontmatter + Markdown）
├── models.py       # Pydantic 数据模型
├── groups.py       # Capability group 和 bash policy 定义
├── caster.py       # Cast 编译管线
└── adapters/       # 平台适配器
    ├── base.py     # Adapter Protocol
    ├── claude.py   # Claude Code 适配器
    └── opencode.py # OpenCode 适配器
```

## 添加新适配器

1. 在 `src/agent_caster/adapters/` 下创建新模块，实现 `Adapter` Protocol
2. 在 `adapters/__init__.py` 的 `_REGISTRY` 中注册
3. 在 `pyproject.toml` 的 `[project.entry-points."agent_caster.adapters"]` 中注册
4. 在 `tests/` 下添加对应的 snapshot 测试
