# ilala-amana

This folder is now a starter kit for a **SuperSub Agency Agent**: a small,
cheap coordinator that routes missions to specialist sub-agents and larger
model/tool backends.

## What is in this folder

- `README.md` - project overview and setup notes.
- `pyproject.toml` - Python package metadata and the `supersub` CLI command.
- `supersub_agency/` - the runnable agent scaffold.
  - `agency.py` - the top-level coordinator and specialist agents.
  - `model_router.py` - the small-model style router that chooses the right lane.
  - `tools.py` - tool stubs for markets, paper trading, sales, shipping, ops,
    and creative work.
  - `safety.py` - approval gates for money, customer, and shipping actions.
  - `contracts.py` - shared request/response data structures.
  - `cli.py` - command-line entry point.
- `tests/` - unit tests for the routing and safety behavior.

## The idea

The small agent does not try to be the smartest model in the room. It acts like
an agency director:

1. Read the mission.
2. Classify the intent: finance, commerce, logistics, content, operations, or
   general work.
3. Route the hard reasoning to a bigger model lane.
4. Call focused tools.
5. Stop at approval gates before doing anything with real money, customer data,
   shipping labels, ads, or brokerage accounts.

That gives you the shape of a personal AI agency without pretending a demo can
guarantee profit or safely trade/spend on its own.

## Run it

```bash
python3 -m supersub_agency "help me sell a product online and ship it" --budget 250
```

Structured JSON output:

```bash
python3 -m supersub_agency "research stocks and simulate a plan" --budget 1000 --json
```

Run tests:

```bash
python3 -m unittest discover -s tests
```

## How to make it powerful

Replace the tool stubs with real integrations:

- **Big models:** OpenAI, Anthropic, Gemini, local Ollama, image/video/audio
  generators.
- **Markets:** read-only market data first, then paper trading, then a broker
  integration only after strict approvals.
- **Selling:** Shopify, Stripe, Gumroad, Amazon/eBay/Etsy APIs, CRM, email.
- **Shipping:** Shippo, EasyPost, USPS, UPS, FedEx, DHL.
- **Automation:** browser control, calendars, files, databases, webhooks, queues.

Recommended rule: the agent can research, draft, simulate, and prepare. A human
must approve actions that place trades, spend money, publish listings, contact
customers, buy ads, or ship packages.