"""Shared data contracts for the SuperSub agency."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class Intent(StrEnum):
    """Kinds of work the small coordinator can route."""

    COMMERCE = "commerce"
    FINANCE = "finance"
    LOGISTICS = "logistics"
    CONTENT = "content"
    OPERATIONS = "operations"
    GENERAL = "general"


class RiskLevel(StrEnum):
    """Safety posture for a proposed action."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass(frozen=True)
class TaskRequest:
    """User request passed into the agency."""

    text: str
    budget_usd: float | None = None
    allow_real_money: bool = False
    approval_token: str | None = None


@dataclass(frozen=True)
class ToolResult:
    """Structured result from a tool."""

    tool_name: str
    summary: str
    next_steps: list[str] = field(default_factory=list)
    requires_approval: bool = False


@dataclass(frozen=True)
class AgencyResponse:
    """Complete agency response for one request."""

    intent: Intent
    specialist: str
    model_route: str
    risk_level: RiskLevel
    summary: str
    tool_results: list[ToolResult]
    gated_actions: list[str] = field(default_factory=list)

    def as_markdown(self) -> str:
        """Render a human-friendly response."""

        lines = [
            f"# SuperSub Agency Response",
            f"- Intent: `{self.intent.value}`",
            f"- Specialist: `{self.specialist}`",
            f"- Model route: `{self.model_route}`",
            f"- Risk level: `{self.risk_level.value}`",
            "",
            self.summary,
            "",
            "## Tool output",
        ]

        for result in self.tool_results:
            approval = " (approval required)" if result.requires_approval else ""
            lines.append(f"### {result.tool_name}{approval}")
            lines.append(result.summary)
            if result.next_steps:
                lines.append("")
                lines.append("Next steps:")
                lines.extend(f"- {step}" for step in result.next_steps)
            lines.append("")

        if self.gated_actions:
            lines.append("## Human approval gates")
            lines.extend(f"- {action}" for action in self.gated_actions)

        return "\n".join(lines).strip()
