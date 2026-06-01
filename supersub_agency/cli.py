"""Command-line interface for the SuperSub agency demo."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict

from supersub_agency.agency import AgencyAgent
from supersub_agency.contracts import TaskRequest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run the SuperSub agency coordinator against a mission prompt."
    )
    parser.add_argument("mission", help="What you want the agency to plan.")
    parser.add_argument(
        "--budget",
        type=float,
        default=None,
        help="Optional budget cap in USD. Spending still requires approval.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print structured JSON instead of Markdown.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    response = AgencyAgent().handle(
        TaskRequest(text=args.mission, budget_usd=args.budget)
    )
    if args.json:
        print(json.dumps(asdict(response), indent=2))
    else:
        print(response.as_markdown())


if __name__ == "__main__":
    main()
