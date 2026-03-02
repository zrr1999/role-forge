"""Tests for registry.py — source parsing."""

from __future__ import annotations

import pytest

from agent_caster.registry import parse_source


def test_parse_org_repo():
    src = parse_source("PFCCLab/precision-agents")
    assert src.org == "PFCCLab"
    assert src.repo == "precision-agents"
    assert src.ref is None
    assert src.is_local is False
    assert src.github_url == "https://github.com/PFCCLab/precision-agents"


def test_parse_org_repo_with_ref():
    src = parse_source("PFCCLab/precision-agents@v1.0")
    assert src.org == "PFCCLab"
    assert src.repo == "precision-agents"
    assert src.ref == "v1.0"


def test_parse_org_repo_with_branch_ref():
    src = parse_source("PFCCLab/precision-agents@main")
    assert src.ref == "main"


def test_parse_local_relative():
    src = parse_source("./my/agents")
    assert src.is_local is True
    assert src.local_path == "./my/agents"
    assert src.org is None
    assert src.repo is None


def test_parse_local_absolute():
    src = parse_source("/tmp/my-agents")
    assert src.is_local is True
    assert src.local_path == "/tmp/my-agents"


def test_parse_invalid_no_slash():
    with pytest.raises(ValueError, match="Invalid source"):
        parse_source("just-a-name")


def test_parse_empty():
    with pytest.raises(ValueError, match="Invalid source"):
        parse_source("")
