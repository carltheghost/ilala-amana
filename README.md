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
  - `providers.py` - the model/tool mixer for OpenClaw, Hermes, AgentClaw,
    VisionScout, AudioEar, ToonForge, and VideoForge adapter slots.
  - `tools.py` - tool stubs for markets, paper trading, sales, shipping, ops,
    multimodal analysis, detection/watch mode, cartoons, video, and creative work.
  - `safety.py` - approval gates for money, customer, and shipping actions.
  - `contracts.py` - shared request/response data structures.
  - `cli.py` - command-line entry point.
- `tests/` - unit tests for the routing and safety behavior.

## The idea

The small agent does not try to be the smartest model in the room. It acts like
an agency director:

1. Read the mission.
2. Classify the intent: finance, commerce, logistics, media, content,
   operations, or general work.
3. Mix model/tool lanes such as OpenClaw, Hermes, AgentClaw, VisionScout,
   AudioEar, ToonForge, and VideoForge.
4. Route the hard reasoning to a bigger model lane.
5. Call focused tools.
6. Stop at approval gates before doing anything with real money, customer data,
   shipping labels, ads, brokerage accounts, cameras, microphones, live watch
   mode, or generated media publishing.

That gives you the shape of a personal AI agency without pretending a demo can
guarantee profit or safely trade/spend on its own.

## Run it

### Visual 4D command deck (browser)

A Cursor Cloud–style spatial desktop: hyperspace WebGL, glass panels, dock, and live
routing into the same agency backend as the CLI.

```bash
python3 -m supersub_agency --desktop
# or: supersub --desktop --port 8765
```

Then open **http://127.0.0.1:8765/** — compose missions, browse provider lanes, and
read specialist output in floating panels with parallax depth.

### CLI

```bash
python3 -m supersub_agency "help me sell a product online and ship it" --budget 250
```

Structured JSON output:

```bash
python3 -m supersub_agency "research stocks and simulate a plan" --budget 1000 --json
```

List the available model/tool lanes:

```bash
python3 -m supersub_agency --capabilities
```

Multimodal studio example:

```bash
python3 -m supersub_agency "make a cartoon video and analyze screenshots, audio, and scenes"
```

Run tests:

```bash
python3 -m unittest discover -s tests
```

## How to make it powerful

Replace the tool stubs with real integrations:

- **Big models:** OpenAI, Anthropic, Gemini, local Ollama, image/video/audio
  generators, or your own OpenClaw/Hermes/AgentClaw-compatible adapters.
- **Multimodal sensing:** OCR, object detection, image QA, audio transcription,
  sound classification, video frame sampling, timeline summaries, and live watch
  mode for owned/consented sources.
- **Creative studio:** character sheets, storyboards, shot lists, voiceover
  direction, captions, edit decision lists, text-to-video, animation, music, and
  publishing workflows.
- **Markets:** read-only market data first, then paper trading, then a broker
  integration only after strict approvals.
- **Selling:** Shopify, Stripe, Gumroad, Amazon/eBay/Etsy APIs, CRM, email.
- **Shipping:** Shippo, EasyPost, USPS, UPS, FedEx, DHL.
- **Automation:** browser control, calendars, files, databases, webhooks, queues.

Recommended rule: the agent can research, draft, simulate, analyze provided
media, and prepare assets. A human must approve actions that place trades, spend
money, publish listings, contact customers, buy ads, ship packages, record from
camera/microphone, run live watch mode, or publish generated media.