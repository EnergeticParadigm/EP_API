import ast
import inspect
import json
from typing import Any

from app.services.routing_policy import route_task


class RouteEngine:
    def __init__(self, service):
        self.service = service

    def detect_mode(self, prompt: str) -> str:
        return route_task(prompt)["mode"]

    async def dispatch(self, prompt: str, mode: str) -> Any:
        fn = getattr(self.service, "analyze", None)
        if not callable(fn):
            raise AttributeError("EPRAService.analyze() not found.")

        routing = route_task(prompt)
        result = fn(
            routing["normalized_input"],
            context={"routing": routing},
        )

        if inspect.isawaitable(result):
            return await result
        return result

    def coerce_payload(self, raw: Any, mode: str) -> dict:
        if isinstance(raw, dict):
            return raw
        if hasattr(raw, "model_dump") and callable(raw.model_dump):
            return raw.model_dump()
        if hasattr(raw, "dict") and callable(raw.dict):
            return raw.dict()
        if isinstance(raw, str):
            s = raw.strip()
            try:
                parsed = json.loads(s)
                if isinstance(parsed, dict):
                    return parsed
            except Exception:
                pass
            try:
                parsed = ast.literal_eval(s)
                if isinstance(parsed, dict):
                    return parsed
            except Exception:
                pass
            return {"mode": mode, "analysis": s}
        return {"mode": mode, "analysis": str(raw)}

    async def handle(self, prompt: str) -> dict:
        mode = self.detect_mode(prompt)
        raw = await self.dispatch(prompt, mode)
        return self.coerce_payload(raw, mode)
