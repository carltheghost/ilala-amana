"""Coordinator and specialist agents for the SuperSub agency."""

from __future__ import annotations

from dataclasses import dataclass

from supersub_agency.contracts import AgencyResponse, Intent, TaskRequest, ToolResult
from supersub_agency.model_router import SmallModelRouter
from supersub_agency.safety import approval_gates, assess_risk
from supersub_agency.tools import (
    CreativePlannerTool,
    MarketResearchTool,
    OperationsPlannerTool,
    PaperTradingTool,
    SalesPlannerTool,
    ShippingPlannerTool,
    Tool,
)


@dataclass(frozen=True)
class SpecialistAgent:
    """A focused worker that owns a small set of tools."""

    name: str
    tools: tuple[Tool, ...]

    def run(self, request: TaskRequest) -> list[ToolResult]:
        return [tool.run(request) for tool in self.tools]


class AgencyAgent:
    """Small coordinator that delegates to specialist agents and big-model routes."""

    def __init__(self, router: SmallModelRouter | None = None) -> None:
        self.router = router or SmallModelRouter()
        self.specialists: dict[Intent, SpecialistAgent] = {
            Intent.FINANCE: SpecialistAgent(
                name="Money Scout",
                tools=(MarketResearchTool(), PaperTradingTool()),
            ),
            Intent.LOGISTICS: SpecialistAgent(
                name="Shipping Runner",
                tools=(ShippingPlannerTool(),),
            ),
            Intent.COMMERCE: SpecialistAgent(
                name="Sales Builder",
                tools=(SalesPlannerTool(), CreativePlannerTool(), ShippingPlannerTool()),
            ),
            Intent.CONTENT: SpecialistAgent(
                name="Creative Engine",
                tools=(CreativePlannerTool(), SalesPlannerTool()),
            ),
            Intent.OPERATIONS: SpecialistAgent(
                name="Ops Commander",
                tools=(OperationsPlannerTool(),),
            ),
            Intent.GENERAL: SpecialistAgent(
                name="General Operator",
                tools=(OperationsPlannerTool(), CreativePlannerTool()),
            ),
        }

    def handle(self, request: TaskRequest) -> AgencyResponse:
        decision = self.router.classify(request.text)
        specialist = self.specialists[decision.intent]
        tool_results = specialist.run(request)
        gates = approval_gates(request, decision.intent)
        risk = assess_risk(request, decision.intent)

        summary = (
            "The small coordinator understood the request, chose the right specialist, "
            "and routed the heavy reasoning to the matching big-model/tool lane. "
            "This scaffold plans and simulates first; real-world money, customer, and shipping actions "
            "stay behind explicit approval gates."
        )

        return AgencyResponse(
            intent=decision.intent,
            specialist=specialist.name,
            model_route=decision.model_route,
            risk_level=risk,
            summary=summary,
            tool_results=tool_results,
            gated_actions=gates,
        )
