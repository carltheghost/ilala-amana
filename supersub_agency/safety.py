"""Safety and approval gates for high-impact agency actions."""

from __future__ import annotations

from supersub_agency.contracts import Intent, RiskLevel, TaskRequest


MONEY_MOVING_TERMS = (
    "buy",
    "sell stock",
    "purchase",
    "place order",
    "wire",
    "transfer",
    "ship now",
    "charge",
    "refund",
)


def assess_risk(request: TaskRequest, intent: Intent) -> RiskLevel:
    """Estimate how much supervision the request needs."""

    text = request.text.lower()
    if intent == Intent.FINANCE:
        return RiskLevel.HIGH
    if any(term in text for term in MONEY_MOVING_TERMS):
        return RiskLevel.HIGH
    if request.budget_usd and request.budget_usd > 0:
        return RiskLevel.MEDIUM
    return RiskLevel.LOW


def approval_gates(request: TaskRequest, intent: Intent) -> list[str]:
    """List actions that should never happen silently."""

    gates: list[str] = []
    if intent == Intent.FINANCE:
        gates.append(
            "Real trades are blocked by default. Use paper trading or connect a broker only with explicit approval."
        )
    if "ship" in request.text.lower() or "shipping" in request.text.lower():
        gates.append(
            "Buying labels, booking freight, or sharing customer addresses requires approval."
        )
    if "sell" in request.text.lower() or "store" in request.text.lower():
        gates.append(
            "Publishing listings, charging customers, or sending outreach requires approval."
        )
    if request.budget_usd:
        gates.append(f"Budget cap: ${request.budget_usd:,.2f}. Spending requires approval.")
    return gates
