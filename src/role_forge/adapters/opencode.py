"""OpenCode adapter — generates .opencode/agents/*.md.

Migrated from precision-alignment-agent/adapters/opencode/generate.py.
"""

from __future__ import annotations

from role_forge.adapters.base import BaseAdapter
from role_forge.groups import ALL_TOOL_IDS, BASH_POLICIES, TOOL_GROUPS
from role_forge.models import AgentDef, TargetConfig


class OpenCodeAdapter(BaseAdapter):
    name = "opencode"
    base_dir = ".opencode/agents"
    file_suffix = ".md"
    prompt_separator = "\n\n"

    def _expand_capabilities(
        self,
        capabilities: list[str | dict],
        capability_map: dict[str, dict[str, bool]],
    ) -> tuple[dict[str, bool], list[str], list[str]]:
        """Expand raw capabilities into OpenCode tools, bash patterns, delegates.

        Bash policy groups (safe-bash, readonly-bash) and explicit ``bash: [...]``
        entries are **merged** — the final whitelist is the union of all patterns.
        """
        tools: dict[str, bool] = {}
        bash_allowed: list[str] = []
        delegates: list[str] = []

        for cap in capabilities:
            if isinstance(cap, str):
                # Bash policy group
                if cap in BASH_POLICIES:
                    bash_allowed.extend(BASH_POLICIES[cap])
                    tools["bash"] = True
                elif cap == "all":
                    tools.update(dict.fromkeys(ALL_TOOL_IDS, True))
                # Built-in tool group
                elif cap in TOOL_GROUPS:
                    for tool_id in TOOL_GROUPS[cap]:
                        tools[tool_id] = True
                # User-defined capability_map from refit.toml
                elif cap in capability_map:
                    tools.update(capability_map[cap])
                else:
                    # Pass through as-is — the platform may support it natively
                    tools[cap] = True
            elif isinstance(cap, dict):
                if "bash" in cap:
                    bash_allowed.extend(cap["bash"] or [])
                    tools["bash"] = True
                if "delegate" in cap:
                    delegates = cap["delegate"] or []
                    if delegates:
                        tools["task"] = True

        # Deduplicate bash patterns while preserving order
        seen: set[str] = set()
        deduped: list[str] = []
        for p in bash_allowed:
            if p not in seen:
                seen.add(p)
                deduped.append(p)
        bash_allowed = deduped

        return {k: v for k, v in tools.items() if v}, bash_allowed, delegates

    def _resolve_temperature(self, agent: AgentDef) -> float:
        model = agent.model
        if model.temperature is not None:
            return model.temperature
        return 0.2 if agent.role == "primary" else 0.1

    def _build_permissions(
        self,
        bash_allowed: list[str],
        delegates: list[str],
        tools: dict[str, bool],
        role: str,
        *,
        full_access: bool = False,
    ) -> dict:
        if full_access:
            return {
                "bash": "allow",
                "task": "allow",
                "edit": "allow",
                "write": "allow",
                "read": "allow",
                "glob": "allow",
                "grep": "allow",
                "webfetch": "allow",
                "websearch": "allow",
                "question": "allow",
            }

        perm: dict = {}

        if bash_allowed:
            perm["bash"] = {"*": "deny"}
            for pattern in bash_allowed:
                perm["bash"][pattern] = "allow"

        if delegates:
            perm["task"] = {"*": "deny"}
            for d in delegates:
                perm["task"][d] = "allow"
        elif tools.get("task"):
            perm["task"] = "allow"

        if tools.get("bash") and not bash_allowed:
            perm["bash"] = "allow"

        if tools.get("edit"):
            perm["edit"] = "allow"
        if tools.get("write"):
            perm["write"] = "allow"

        if role == "primary":
            perm["question"] = "allow"
        return perm

    def _serialize_frontmatter(
        self,
        description: str,
        mode: str,
        model: str,
        temperature: float,
        skills: list[str],
        tools: dict[str, bool],
        permission: dict,
    ) -> str:
        """Custom YAML serializer matching OpenCode's expected format."""
        lines = ["---"]
        lines.append(f"description: {description}")
        lines.append(f"mode: {mode}")
        lines.append(f"model: {model}")
        lines.append(f"temperature: {temperature}")

        if skills:
            lines.append("skills:")
            for s in skills:
                lines.append(f"  - {s}")

        if tools:
            lines.append("tools:")
            for k, v in tools.items():
                lines.append(f'  "{k}": {str(v).lower()}')

        if permission:
            lines.append("permission:")
            for section, val in permission.items():
                if isinstance(val, dict):
                    lines.append(f'  "{section}":')
                    for pk, pv in val.items():
                        lines.append(f'    "{pk}": {pv}')
                else:
                    lines.append(f'  "{section}": {val}')

        lines.append("---")
        return "\n".join(lines)

    def render_agent(
        self,
        agent: AgentDef,
        config: TargetConfig,
        delegates: list[str],
    ) -> str:
        tools, bash_allowed, _ = self._expand_capabilities(
            agent.capabilities, config.capability_map
        )

        description = agent.description
        mode = agent.role
        model = self._resolve_model(agent.model, config.model_map)
        temperature = self._resolve_temperature(agent)
        skills = [s for s in agent.skills if s]
        permission = self._build_permissions(
            bash_allowed,
            delegates,
            tools,
            agent.role,
            full_access="all" in agent.capabilities,
        )

        fm = self._serialize_frontmatter(
            description, mode, model, temperature, skills, tools, permission
        )
        return self._compose_document(fm, agent.prompt_content)
