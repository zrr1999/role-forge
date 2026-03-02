# agent-caster

Cross-platform AI coding agent definition caster. Write once, deploy everywhere.

## Why

AI coding agent 平台（Claude Code、OpenCode、Cursor、Codex、Windsurf、Aider...）各有自己的 agent 配置格式。团队维护多平台 agent 定义面临配置碎片化、平台锁定和安全配置重复维护等问题。

**agent-caster** 让你只写一份平台无关的 canonical agent 定义（`.agents/roles/*.md`），然后编译为各平台的具体配置。

| 能力 | 支持 |
|------|:---:|
| 单一事实来源 | ✅ |
| 多平台输出（Claude Code / OpenCode / ...） | ✅ |
| Model tier 抽象（reasoning / coding） | ✅ |
| Capability group 展开 | ✅ |
| 权限 / 委派建模 | ✅ |

## Installation

```bash
uv tool install agent-caster
```

## Quick Start

```bash
# 初始化项目，生成 .agents/roles/ 目录和 refit.toml
agent-caster init

# 编译 agent 定义到所有启用的平台
agent-caster cast

# 仅编译到指定平台
agent-caster cast --target claude

# 预览输出（不写入文件）
agent-caster cast --dry-run

# 列出当前所有 agent 定义
agent-caster list
```

## Canonical Agent Definition

在 `.agents/roles/` 下使用 YAML frontmatter + Markdown 编写 agent 定义：

```markdown
---
name: explorer
description: Code Explorer. Reads and analyzes source code.
role: subagent

model:
  tier: reasoning
  temperature: 0.05

skills:
  - repomix-explorer

capabilities:
  - read-code
  - write-report
  - web-read
  - bash:
      - "npx repomix@latest*"
---

# Explorer

Read-only code exploration agent. Traces execution paths and produces reports.
```

## Configuration

项目根目录的 `refit.toml` 配置编译目标和模型映射：

```toml
agents_dir = ".agents/roles"

[targets.opencode]
enabled = true
output_dir = ".opencode/agents"

[targets.opencode.model_map]
reasoning = "anthropic:claude-sonnet-4-20250514"
coding = "anthropic:claude-sonnet-4-20250514"

[targets.claude]
enabled = true
output_dir = ".claude/agents"

[targets.claude.model_map]
reasoning = "claude-sonnet-4-20250514"
coding = "claude-sonnet-4-20250514"
```

## Supported Platforms

| Platform | Adapter | Output |
|----------|---------|--------|
| Claude Code | `claude` | `.claude/agents/*.md` |
| OpenCode | `opencode` | `.opencode/agents/*.md` |

更多平台适配器开发中。

## Development

```bash
# 安装依赖
just install

# 格式化
just format

# Lint
just lint

# 类型检查
just check

# 测试
just test

# 测试 + 覆盖率
just cov

# 完整 CI 流程
just ci
```

## License

MIT
