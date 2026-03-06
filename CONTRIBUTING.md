# Contributing to agent-caster

感谢你的贡献！本文档面向人类贡献者，说明参与开发的基本流程。

## 开发环境

```bash
git clone https://github.com/zrr1999/agent-caster.git
cd agent-caster
just install   # 安装依赖
just ci        # 完整 CI 流程（format + lint + check + test）
```

## 提交与 PR 规范

见 [docs/conventions.md](docs/conventions.md)。

## 添加新适配器

1. 在 `src/agent_caster/adapters/` 下创建新模块，继承 `BaseAdapter`
2. 在 `adapters/__init__.py` 的 `_REGISTRY` 中注册
3. 在 `pyproject.toml` 的 `[project.entry-points."agent_caster.adapters"]` 中注册
4. 在 `tests/` 下添加对应的 snapshot 测试

## License

MIT
