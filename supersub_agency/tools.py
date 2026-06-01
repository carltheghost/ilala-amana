"""Tool stubs that a SuperSub agent can call.

The tools return plans and simulations today. Replace the internals with real
APIs (brokerage, marketplace, carrier, CRM) once credentials and approval
policies are configured.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from supersub_agency.contracts import TaskRequest, ToolResult


class Tool(ABC):
    """Base class for callable agency capabilities."""

    name: str

    @abstractmethod
    def run(self, request: TaskRequest) -> ToolResult:
        """Execute the tool."""


class MarketResearchTool(Tool):
    name = "market-research"

    def run(self, request: TaskRequest) -> ToolResult:
        return ToolResult(
            tool_name=self.name,
            summary=(
                "Prepared a research-first market workflow: define thesis, collect price/news/fundamental "
                "signals, compare risks, and produce a paper-trade recommendation instead of placing orders."
            ),
            next_steps=[
                "Connect read-only market data such as Polygon, Alpha Vantage, IEX, or broker research.",
                "Add a paper-trading ledger before any live broker integration.",
                "Require a human approval token for every real order.",
            ],
            requires_approval=True,
        )


class PaperTradingTool(Tool):
    name = "paper-trading"

    def run(self, request: TaskRequest) -> ToolResult:
        budget = request.budget_usd or 1_000.0
        return ToolResult(
            tool_name=self.name,
            summary=(
                f"Created a simulated capital plan with ${budget:,.2f}: cap one idea at 5% risk, log the thesis, "
                "entry, exit, stop condition, and post-trade review."
            ),
            next_steps=[
                "Store simulated positions in a local database.",
                "Backtest simple rules before connecting live accounts.",
                "Track maximum drawdown and stop automation if the limit is hit.",
            ],
        )


class SalesPlannerTool(Tool):
    name = "sales-planner"

    def run(self, request: TaskRequest) -> ToolResult:
        return ToolResult(
            tool_name=self.name,
            summary=(
                "Drafted a sellable offer workflow: pick a niche, validate demand, create a simple landing page, "
                "collect leads, draft outreach, and measure conversion."
            ),
            next_steps=[
                "Connect Shopify, Stripe, or a marketplace only after products and policies are approved.",
                "Generate product descriptions, images, and ad variants through creative model routes.",
                "Send test traffic to a waitlist before buying inventory.",
            ],
            requires_approval=True,
        )


class ShippingPlannerTool(Tool):
    name = "shipping-planner"

    def run(self, request: TaskRequest) -> ToolResult:
        return ToolResult(
            tool_name=self.name,
            summary=(
                "Mapped a fulfillment workflow: capture package dimensions, compare carriers, choose service "
                "levels, print labels only after approval, and notify customers with tracking."
            ),
            next_steps=[
                "Connect Shippo, EasyPost, or carrier APIs for live rates.",
                "Keep customer addresses encrypted and avoid exposing them to general-purpose models.",
                "Add return-label and lost-package procedures.",
            ],
            requires_approval=True,
        )


class OperationsPlannerTool(Tool):
    name = "operations-planner"

    def run(self, request: TaskRequest) -> ToolResult:
        return ToolResult(
            tool_name=self.name,
            summary=(
                "Built the agency operating loop: intake -> route -> specialist plan -> tool execution -> "
                "approval gate -> result logging -> improvement notes."
            ),
            next_steps=[
                "Add calendar, email, browser, database, and file-system tools one by one.",
                "Give each sub-agent a narrow job and measurable output.",
                "Log every action so the agency can be audited.",
            ],
        )


class CreativePlannerTool(Tool):
    name = "creative-planner"

    def run(self, request: TaskRequest) -> ToolResult:
        return ToolResult(
            tool_name=self.name,
            summary=(
                "Prepared a creative production loop: brief, audience, message, draft copy, generate visuals, "
                "run variants, and hand the best assets to the sales agent."
            ),
            next_steps=[
                "Connect large text, image, audio, and video models behind this tool.",
                "Keep brand rules in a reusable style guide.",
                "Review claims before publishing ads or product pages.",
            ],
        )
