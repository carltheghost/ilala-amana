"""JSON serialization for agency API responses."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any

from supersub_agency.contracts import AgencyResponse, Intent, RiskLevel, ToolResult
from supersub_agency.providers import ProviderAdapter, ProviderMixer


def tool_result_to_dict(result: ToolResult) -> dict[str, Any]:
    return asdict(result)


def agency_response_to_dict(response: AgencyResponse) -> dict[str, Any]:
    payload = asdict(response)
    payload["intent"] = response.intent.value
    payload["risk_level"] = response.risk_level.value
    payload["tool_results"] = [tool_result_to_dict(r) for r in response.tool_results]
    return payload


def provider_to_dict(provider: ProviderAdapter) -> dict[str, Any]:
    return {
        "name": provider.name,
        "role": provider.role,
        "strengths": list(provider.strengths),
        "intents": [intent.value for intent in provider.intents],
        "description": provider.describe(),
    }


def capabilities_payload() -> list[dict[str, Any]]:
    return [provider_to_dict(p) for p in ProviderMixer().providers]
