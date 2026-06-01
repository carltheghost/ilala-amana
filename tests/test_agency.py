"""Tests for the SuperSub agency coordinator."""

from __future__ import annotations

import unittest

from supersub_agency import AgencyAgent
from supersub_agency.contracts import Intent, RiskLevel, TaskRequest


class AgencyAgentTests(unittest.TestCase):
    def test_routes_stock_requests_to_finance_with_approval_gate(self) -> None:
        response = AgencyAgent().handle(
            TaskRequest(text="Research stocks and make money with paper trades", budget_usd=500)
        )

        self.assertEqual(response.intent, Intent.FINANCE)
        self.assertEqual(response.risk_level, RiskLevel.HIGH)
        self.assertTrue(response.gated_actions)
        self.assertIn("Money Scout", response.specialist)

    def test_routes_selling_and_shipping_to_commerce(self) -> None:
        response = AgencyAgent().handle(
            TaskRequest(text="Help me sell products online and handle shipping")
        )

        self.assertEqual(response.intent, Intent.LOGISTICS)
        self.assertIn("Shipping", response.specialist)
        self.assertTrue(any(result.requires_approval for result in response.tool_results))

    def test_general_agent_still_produces_tool_results(self) -> None:
        response = AgencyAgent().handle(TaskRequest(text="Build my personal agency"))

        self.assertEqual(response.intent, Intent.OPERATIONS)
        self.assertGreaterEqual(len(response.tool_results), 1)

    def test_routes_multimodal_cartoon_video_requests_to_media(self) -> None:
        response = AgencyAgent().handle(
            TaskRequest(text="Make a cartoon video and watch screenshots to detect objects")
        )

        self.assertEqual(response.intent, Intent.MEDIA)
        self.assertEqual(response.specialist, "OmniMedia Studio")
        self.assertEqual(response.risk_level, RiskLevel.HIGH)
        self.assertTrue(any("VisionScout" in capability for capability in response.capabilities))
        self.assertTrue(any(result.tool_name == "cartoon-studio" for result in response.tool_results))
        self.assertTrue(response.gated_actions)


if __name__ == "__main__":
    unittest.main()
