from __future__ import annotations

import os
from typing import Any, Dict
from openai import OpenAI


class OpenAIResponsesGateway:
    def __init__(self) -> None:
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = os.getenv("OPENAI_MODEL")
        if not self.model:
            raise ValueError("OPENAI_MODEL is not set.")
        self.temperature = float(os.getenv("OPENAI_TEMPERATURE", "0"))
        self.top_p = float(os.getenv("OPENAI_TOP_P", "1"))

    def generate(self, system_prompt: str, runtime_state: Dict[str, Any], task: str) -> str:
        prompt = (
            f"SYSTEM RUNTIME RULES:\n{system_prompt}\n\n"
            f"EPRA RUNTIME STATE:\n{runtime_state}\n\n"
            f"USER TASK:\n{task}\n"
        )
        response = self.client.responses.create(
            model=self.model,
            input=prompt,
            temperature=self.temperature,
            top_p=self.top_p,
        )
        return response.output_text
