"""Command-line interface for the SuperSub agency demo."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict

from supersub_agency.agency import AgencyAgent
from supersub_agency.contracts import TaskRequest
from supersub_agency.providers import ProviderMixer


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run the SuperSub agency coordinator against a mission prompt."
    )
    parser.add_argument("mission", nargs="?", help="What you want the agency to plan.")
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
    parser.add_argument(
        "--capabilities",
        action="store_true",
        help="List all model/tool lanes in the provider mixer.",
    )
    parser.add_argument(
        "--desktop",
        action="store_true",
        help="Launch the 4D visual command deck in your browser.",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8765,
        help="Port for --desktop (default: 8765).",
    )
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="With --desktop, do not auto-open a browser tab.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.desktop:
        from supersub_agency.desktop import run_desktop

        run_desktop(port=args.port, open_browser=not args.no_browser)
        return

    if args.capabilities:
        mixer = ProviderMixer()
        for provider in mixer.providers:
            print(provider.describe())
        return

    if not args.mission:
        raise SystemExit("Provide a mission or use --capabilities.")

    response = AgencyAgent().handle(
        TaskRequest(text=args.mission, budget_usd=args.budget)
    )
    if args.json:
        print(json.dumps(asdict(response), indent=2))
    else:
        print(response.as_markdown())


if __name__ == "__main__":
    main()
