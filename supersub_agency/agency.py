"""Coordinator and specialist agents for the SuperSub agency."""

from __future__ import annotations

from dataclasses import dataclass

from supersub_agency.contracts import AgencyResponse, Intent, TaskRequest, ToolResult
from supersub_agency.model_router import SmallModelRouter
from supersub_agency.providers import ProviderMixer
from supersub_agency.safety import approval_gates, assess_risk
from supersub_agency.tools import (
    CartoonStudioTool,
    CreativePlannerTool,
    DetectionWatchTool,
    MarketResearchTool,
    MultimodalSensorTool,
    OperationsPlannerTool,
    PaperTradingTool,
    SalesPlannerTool,
    ShippingPlannerTool,
    Tool,
    VideoStudioTool,
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

    def __init__(
        self,
        router: SmallModelRouter | None = None,
        provider_mixer: ProviderMixer | None = None,
    ) -> None:
        self.router = router or SmallModelRouter()
        self.provider_mixer = provider_mixer or ProviderMixer()
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
                tools=(
                    SalesPlannerTool(),
                    CreativePlannerTool(),
                    CartoonStudioTool(),
                    ShippingPlannerTool(),
                ),
            ),
            Intent.MEDIA: SpecialistAgent(
                name="OmniMedia Studio",
                tools=(
                    MultimodalSensorTool(),
                    DetectionWatchTool(),
                    CartoonStudioTool(),
                    VideoStudioTool(),
                    CreativePlannerTool(),
                ),
            ),
            Intent.CONTENT: SpecialistAgent(
                name="Creative Engine",
                tools=(CreativePlannerTool(), CartoonStudioTool(), VideoStudioTool(), SalesPlannerTool()),
            ),
            Intent.OPERATIONS: SpecialistAgent(
                name="Ops Commander",
                tools=(OperationsPlannerTool(), MultimodalSensorTool()),
            ),
            Intent.GENERAL: SpecialistAgent(
                name="General Operator",
                tools=(OperationsPlannerTool(), CreativePlannerTool(), MultimodalSensorTool()),
            ),
        }

    def handle(self, request: TaskRequest) -> AgencyResponse:
        decision = self.router.classify(request.text)
        specialist = self.specialists[decision.intent]
        tool_results = specialist.run(request)
        gates = approval_gates(request, decision.intent)
        risk = assess_risk(request, decision.intent)
        capabilities = self.provider_mixer.capabilities_for(decision.intent)
        model_route = f"{decision.model_route} via {self.provider_mixer.names_for(decision.intent)}"

        summary = (
            "The small coordinator understood the request, chose the right specialist, mixed the available "
            "model/tool lanes, and routed the heavy reasoning to the matching big-model/tool lane. "
            "This scaffold plans and simulates first; real-world money, customer, and shipping actions "
            "plus camera, microphone, live watch, and publishing actions stay behind explicit approval gates."
        )

        return AgencyResponse(
            intent=decision.intent,
            specialist=specialist.name,
            model_route=model_route,
            risk_level=risk,
            summary=summary,
            tool_results=tool_results,
            capabilities=capabilities,
            gated_actions=gates,
        )
