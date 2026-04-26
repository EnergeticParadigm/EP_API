from __future__ import annotations

from typing import Any, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.services import epra
from app.services.router_v5 import route_prompt_v5
from app.services.session_memory import get_or_create_session, build_effective_message, update_session, session_payload
from app.services.control_shell_v6 import normalize_control_class


class TextRequest(BaseModel):
    message: Optional[str] = None
    previous_message: Optional[str] = None
    session_id: Optional[str] = None
    prompt: Optional[str] = None



def _looks_like_followup_message(message: str) -> bool:
    t = str(message or "").strip().lower()
    markers = [
        "but i really want",
        "i really want an answer",
        "i need a thesis",
        "give me a thesis",
        "expand",
        "continue",
        "why",
        "explain more",
        "go deeper",
        "more detail",
        "what about",
        "then what",
    ]
    return t in {"why?", "why", "continue", "expand"} or any(x in t for x in markers)


def _effective_message(message: str, previous_message: str | None) -> str:
    if previous_message and _looks_like_followup_message(message):
        return f"{previous_message}\n\nFollow-up instruction: {message}"
    return message


app = FastAPI(title="EPRA API Wrapper v6")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


service = epra.EPRAService()


def _coerce_result(result: Any, routing: dict[str, Any]) -> Any:
    try:
        if hasattr(result, "metadata") and isinstance(result.metadata, dict):
            result.metadata["routing"] = dict(routing)
        elif isinstance(result, dict):
            result.setdefault("metadata", {})
            if isinstance(result["metadata"], dict):
                result["metadata"]["routing"] = dict(routing)
    except Exception:
        pass
    return result


@app.get("/")
def root() -> dict[str, str]:
    return {"status": "ok", "service": "EPRA API Wrapper v6"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}


@app.post("/chat")
def chat(req: TextRequest) -> Any:
    message = (req.message or req.prompt or "").strip()
    if not message:
        raise HTTPException(status_code=400, detail="No message or prompt provided.")

    session_id, memory_state = get_or_create_session(req.session_id)
    effective_message = build_effective_message(message, memory_state)

    if memory_state.last_effective_message and effective_message != message:
        routing = normalize_control_class({
            "task_type": "FOLLOW_UP_REWRITE",
            "answer_shape": "rewrite_previous",
            "target_system": memory_state.last_target or memory_state.last_effective_message,
            "confidence": 0.95,
            "reasons": ["session_memory_followup"],
        })
    else:
        routing = normalize_control_class(route_prompt_v5(
        effective_message,
        previous_context={
            "last_mode": memory_state.last_mode,
            "last_target": memory_state.last_target,
            "last_user_message": memory_state.last_user_message,
            "has_previous_answer": bool(memory_state.last_answer),
        },
    ))

    try:
        result = service.analyze(effective_message, context={"routing": routing,
            "previous_message": req.previous_message})
        result = _coerce_result(result, routing)
        update_session(memory_state, message, effective_message, result)
        result.metadata = result.metadata or {}
        result.metadata["session"] = session_payload(session_id, memory_state)
        return result
    except TypeError:
        result = service.analyze(message)
        return _coerce_result(result, routing)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
