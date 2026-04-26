from __future__ import annotations

import os
from typing import Any, Dict, Protocol

from app.services.openai_client import OpenAIResponsesGateway


class ModelGateway(Protocol):
    def generate(self, system_prompt: str, runtime_state: Dict[str, Any], task: str) -> str:
        ...


class OpenAIModelGateway:
    def __init__(self) -> None:
        self.client = OpenAIResponsesGateway()

    def generate(self, system_prompt: str, runtime_state: Dict[str, Any], task: str) -> str:
        return self.client.generate(
            system_prompt=system_prompt,
            runtime_state=runtime_state,
            task=task,
        )


class PlaceholderModelGateway:
    def __init__(self, provider: str) -> None:
        self.provider = provider

    def generate(self, system_prompt: str, runtime_state: Dict[str, Any], task: str) -> str:
        raise RuntimeError(
            f"Model provider '{self.provider}' is not implemented yet. "
            "Implement this provider behind the ModelGateway interface."
        )


def get_model_gateway() -> ModelGateway:
    provider = os.getenv("EPRA_MODEL_PROVIDER", "openai").strip().lower()

    if provider == "openai":
        return OpenAIModelGateway()

    if provider in {"gemini", "claude", "gemma", "qwen", "deepseek", "chinese_llm"}:
        return PlaceholderModelGateway(provider)

    raise RuntimeError(f"Unknown EPRA_MODEL_PROVIDER: {provider}")
