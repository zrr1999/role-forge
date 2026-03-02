"""Source parsing and git operations for agent-caster registry."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ParsedSource:
    """A parsed source reference."""

    org: str | None = None
    repo: str | None = None
    ref: str | None = None
    local_path: str | None = None

    @property
    def is_local(self) -> bool:
        return self.local_path is not None

    @property
    def github_url(self) -> str:
        if self.is_local:
            raise ValueError("Local source has no GitHub URL")
        return f"https://github.com/{self.org}/{self.repo}"

    @property
    def cache_key(self) -> str:
        if self.is_local:
            raise ValueError("Local source has no cache key")
        return f"{self.org}/{self.repo}"


def parse_source(source: str) -> ParsedSource:
    """Parse a source string into a ParsedSource.

    Formats:
        org/repo            → GitHub repo
        org/repo@ref        → GitHub repo at ref
        ./path              → local relative path
        /path               → local absolute path
    """
    if not source:
        raise ValueError("Invalid source: empty string")

    if source.startswith("./") or source.startswith("/"):
        return ParsedSource(local_path=source)

    if "/" not in source:
        raise ValueError(f"Invalid source: {source!r}. Expected 'org/repo' or a local path.")

    # Split off @ref if present
    if "@" in source:
        repo_part, ref = source.rsplit("@", 1)
    else:
        repo_part, ref = source, None

    parts = repo_part.split("/", 1)
    return ParsedSource(org=parts[0], repo=parts[1], ref=ref)
