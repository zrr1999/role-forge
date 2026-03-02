# Toolchain Upgrade Design

Date: 2026-03-02
Status: Approved

## Goal

全面升级 agent-caster 的工具链配置，对齐 marrow-core 最佳实践并增强质量保障。

## Changes

### 1. pyproject.toml

- **dev 依赖组**: 显式加入 `prek>=0.3.4`, `ruff>=0.11`, `ty>=0.0.19`
- **ruff required-imports**: 强制 `from __future__ import annotations`
- **ruff isort per-file-ignores**: `__init__.py` 加 `I002`, `tests/**` 加 `I002`
- **ruff lint ignore**: 加入 `PGH003`（无类型注释 ignore）, `B008`（typer 函数调用默认值）
- **ruff exclude**: 排除 `src/agent_caster/_version.py`
- **project.urls**: 添加 Homepage / Repository

### 2. CI Workflows

- **ci-static-checks.yml**: 添加 `permissions: contents: read`，添加 `Install uv` + `setup-python` 步骤
- **ci-tests.yml**: 添加 `permissions: contents: read`，`uv sync --dev` → `uv sync --group test`
- **新增 publish.yml**: tag-triggered PyPI publish workflow

### 3. Justfile

- `install`: `uv sync --dev` → `uv sync --all-groups`
- `check`: `uvx ty check` → `uvx ty check src/`

### 4. Lint Fix

- 修复现有 3 个 F401 告警（tests 中未使用的 import）
- 修复 required-imports 引入的 I002 告警（tests 中缺少 future annotations）
