"""Provider mixer for model, sensor, and tool backends.

Names like OpenClaw, Hermes, and AgentClaw are adapter slots. The scaffold keeps
them offline and deterministic until real APIs or local models are wired in.
"""

from __future__ import annotations

from dataclasses import dataclass

from supersub_agency.contracts import Intent


@dataclass(frozen=True)
class ProviderAdapter:
    """A model/tool backend the agency can route work toward."""

    name: str
    role: str
    strengths: tuple[str, ...]
    intents: tuple[Intent, ...]

    def describe(self) -> str:
        strengths = ", ".join(self.strengths)
        return f"{self.name}: {self.role} ({strengths})"


DEFAULT_PROVIDERS: tuple[ProviderAdapter, ...] = (
    ProviderAdapter(
        name="OpenClaw",
        role="tool-use and web/API action planner",
        strengths=("API planning", "browser workflows", "code execution plans"),
        intents=(Intent.OPERATIONS, Intent.COMMERCE, Intent.LOGISTICS, Intent.GENERAL),
    ),
    ProviderAdapter(
        name="Hermes",
        role="reasoning, memory synthesis, and long-form writing",
        strengths=("strategy", "summaries", "creative briefs", "analysis"),
        intents=(Intent.CONTENT, Intent.MEDIA, Intent.FINANCE, Intent.GENERAL),
    ),
    ProviderAdapter(
        name="AgentClaw",
        role="multi-agent supervisor and task decomposer",
        strengths=("delegation", "checklists", "tool orchestration", "auditing"),
        intents=tuple(Intent),
    ),
    ProviderAdapter(
        name="VisionScout",
        role="image and video understanding lane",
        strengths=("object detection", "scene analysis", "visual QA", "watch mode"),
        intents=(Intent.MEDIA, Intent.CONTENT, Intent.OPERATIONS),
    ),
    ProviderAdapter(
        name="AudioEar",
        role="audio and speech understanding lane",
        strengths=("transcription", "sound classification", "voice notes", "meeting review"),
        intents=(Intent.MEDIA, Intent.CONTENT, Intent.OPERATIONS),
    ),
    ProviderAdapter(
        name="ToonForge",
        role="cartoon and character generation lane",
        strengths=("storyboards", "character sheets", "shot lists", "style prompts"),
        intents=(Intent.MEDIA, Intent.CONTENT, Intent.COMMERCE),
    ),
    ProviderAdapter(
        name="VideoForge",
        role="video production and editing lane",
        strengths=("scripts", "b-roll plans", "edit decisions", "render queues"),
        intents=(Intent.MEDIA, Intent.CONTENT, Intent.COMMERCE),
    ),
)


class ProviderMixer:
    """Selects model/tool lanes for a requested intent."""

    def __init__(self, providers: tuple[ProviderAdapter, ...] = DEFAULT_PROVIDERS) -> None:
        self.providers = providers

    def capabilities_for(self, intent: Intent) -> list[str]:
        selected = [
            provider.describe()
            for provider in self.providers
            if intent in provider.intents
        ]
        if intent != Intent.GENERAL:
            selected.extend(
                provider.describe()
                for provider in self.providers
                if Intent.GENERAL in provider.intents and intent not in provider.intents
            )
        return selected

    def names_for(self, intent: Intent) -> str:
        names = [provider.name for provider in self.providers if intent in provider.intents]
        return " + ".join(names)
