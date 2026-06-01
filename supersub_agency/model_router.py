"""Small-model router that decides when to involve bigger model backends."""

from __future__ import annotations

from dataclasses import dataclass

from supersub_agency.contracts import Intent


KEYWORDS: dict[Intent, tuple[str, ...]] = {
    Intent.FINANCE: (
        "stock",
        "stocks",
        "trade",
        "trading",
        "invest",
        "portfolio",
        "market",
        "money",
    ),
    Intent.LOGISTICS: (
        "ship",
        "shipping",
        "warehouse",
        "fulfillment",
        "delivery",
        "freight",
    ),
    Intent.COMMERCE: (
        "sell",
        "selling",
        "store",
        "shop",
        "product",
        "customer",
        "revenue",
    ),
    Intent.MEDIA: (
        "cartoon",
        "animation",
        "animate",
        "video",
        "movie",
        "see",
        "hear",
        "listen",
        "look",
        "detect",
        "watch",
        "camera",
        "microphone",
        "vision",
        "audio",
        "multimodal",
        "analysis",
        "analyze",
    ),
    Intent.CONTENT: (
        "ad",
        "copy",
        "post",
        "email",
        "landing page",
        "content",
    ),
    Intent.OPERATIONS: (
        "automate",
        "workflow",
        "schedule",
        "agent",
        "agency",
        "delegate",
    ),
}


MODEL_ROUTES: dict[Intent, str] = {
    Intent.FINANCE: "finance-big-model + market-data tools",
    Intent.LOGISTICS: "logistics-big-model + carrier/rate tools",
    Intent.COMMERCE: "commerce-big-model + marketplace/CRM tools",
    Intent.MEDIA: "multimodal mixer: vision/audio/video + creative generators",
    Intent.CONTENT: "creative-big-model + image/video/copy tools",
    Intent.OPERATIONS: "operations-big-model + browser/API tools",
    Intent.GENERAL: "general-big-model",
}


@dataclass(frozen=True)
class RouteDecision:
    """Result of the small coordinator's routing pass."""

    intent: Intent
    model_route: str
    confidence: float


class SmallModelRouter:
    """A deterministic stand-in for a cheap local/small model.

    This keeps the repo runnable without API keys. Later, this class can call a
    compact local LLM and keep the same public interface.
    """

    def classify(self, text: str) -> RouteDecision:
        normalized = text.lower()
        scores = {
            intent: sum(1 for keyword in keywords if keyword in normalized)
            for intent, keywords in KEYWORDS.items()
        }
        intent = max(scores, key=scores.get)
        if scores[intent] == 0:
            intent = Intent.GENERAL

        confidence = min(0.95, 0.45 + (scores.get(intent, 0) * 0.15))
        return RouteDecision(
            intent=intent,
            model_route=MODEL_ROUTES[intent],
            confidence=confidence,
        )
