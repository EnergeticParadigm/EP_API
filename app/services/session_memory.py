from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional
from uuid import uuid4


@dataclass
class TurnState:
    last_user_message: str = ""
    last_effective_message: str = ""
    last_mode: str = ""
    last_target: str = ""
    last_answer: str = ""


SESSIONS: Dict[str, TurnState] = {}


def get_or_create_session(session_id: Optional[str]) -> tuple[str, TurnState]:
    sid = session_id or str(uuid4())
    if sid not in SESSIONS:
        SESSIONS[sid] = TurnState()
    return sid, SESSIONS[sid]


def looks_like_followup(message: str) -> bool:
    t = str(message or "").strip().lower()
    if len(t.split()) <= 6:
        return True
    if t.startswith((
        "it ",
        "that ",
        "this ",
        "then",
        "therefore",
        "so ",
        "your answer",
        "the answer",
        "i only",
        "only ",
        "make it ",
        "give me ",
        "explain ",
        "why",
        "continue",
        "what about",
        "how about",
        "in computer science",
        "in religion",
        "in politics",
        "in economics",
    )):
        return True
    return False


def build_effective_message(message: str, state: TurnState) -> str:
    if state.last_effective_message and looks_like_followup(message):
        return (
            f"Previous user request:\n{state.last_effective_message}\n\n"
            f"Previous answer mode: {state.last_mode}\n"
            f"Previous target: {state.last_target}\n\n"
            f"Previous answer:\n{state.last_answer}\n\n"
            f"Follow-up instruction:\n{message}"
        )
    return message


def update_session(state: TurnState, user_message: str, effective_message: str, response: Any) -> None:
    metadata = getattr(response, "metadata", {}) or {}
    routing = metadata.get("routing", {}) or {}
    mode = metadata.get("mode") or routing.get("task_type", "")
    answer = str(getattr(response, "analysis", ""))[:4000]

    # Do not let clarification overwrite useful prior memory.
    if mode == "CLARIFICATION_REQUIRED" and state.last_effective_message:
        state.last_user_message = user_message
        return

    state.last_user_message = user_message
    state.last_effective_message = effective_message
    state.last_mode = mode

    target = metadata.get("task_system", "") or routing.get("target_system", "")

    msg = str(user_message or "").lower()
    ans = answer.lower()

    # Follow-up domain-shift repair.
    if "computer science" in msg and "canonical" in ans:
        target = "canonical in computer science"
    elif "religion" in msg and "canonical" in ans:
        target = "canonical in religion"
    elif "economics" in msg and "canonical" in ans:
        target = "canonical in economics"
    elif "politics" in msg and "canonical" in ans:
        target = "canonical in politics"

    state.last_target = target
    state.last_answer = answer

def session_payload(session_id: str, state: TurnState) -> Dict[str, Any]:
    data = asdict(state)
    data["session_id"] = session_id
    return data
