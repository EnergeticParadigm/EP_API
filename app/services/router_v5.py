from __future__ import annotations

import json
import re
from typing import Any, Dict

from app.services.model_gateway import get_model_gateway


ROUTER_SYSTEM_PROMPT = """
You are EPRA Semantic Router v5.

Classify the user request by meaning, not exact wording.

Return ONLY valid JSON.

Allowed task_type:
SYSTEM_ANALYSIS
FORECAST
FORECAST_THESIS
WORLD_FACT
WORLD_ATTRIBUTION
PROJECT_FACT
PROJECT_ATTRIBUTION
HOW_TO
FOLLOW_UP_REWRITE
CLARIFICATION_REQUIRED

Rules:

Critical target-binding rules:
- For "what is X in Y?" or "what does X mean in Y?", the target_system must be "X in Y", not just "Y".
- Example: "what is canonical in religion?" => WORLD_FACT, target_system="canonical in religion".
- Example: "what does canonical mean in computer science?" => WORLD_FACT, target_system="canonical in computer science".
- Do not classify "what is X" as attribution unless the user asks who invented, who created, who founded, who wrote, or who developed X.

- If previous_context.has_previous_answer is true and the user prompt starts with then, so, what about, how about, what does it mean, or uses it/this/that without a clear standalone noun, classify as FOLLOW_UP_REWRITE.
- For follow-ups like "then, what does it mean in computer science?", inherit the prior concept from previous_context.last_user_message and change only the requested domain.

- War, armed conflict, military escalation, geopolitical crisis, election, market, current event, or policy forecast should usually be FORECAST_THESIS and MUST set needs_current_source=true.
- Any question about when a war/conflict/crisis will end MUST set needs_current_source=true.
- If the answer depends on events after the model's training data, set needs_current_source=true.
- Forecast means future timing, likelihood, end-state, probability, prediction, scenario, or "when will X end".
- Forecast thesis means deep forecast, thesis request, war, armed conflict, military escalation, geopolitical crisis, institutional future, strategic uncertainty, or any forecast about the end/timing/outcome of a war or conflict.
- If the user asks when a war, conflict, crisis, escalation, blockade, strike campaign, or military confrontation will end, classify as FORECAST_THESIS, not FORECAST.
- System analysis means analyzing an institution, system, process, platform, market, workflow, or control/allocation mechanism.
- Follow-up rewrite means user modifies previous answer: shorter, longer, one sentence, expand, continue, why, compare, too long, unclear.
- Project terms include EP, EPRA, Energetic Paradigm, canonical setup, structural commitments.
- Project attribution means who invented/created EP, EPRA, or Energetic Paradigm.
- Do not fall back to clarification merely because wording is unusual.

Return:
{
  "task_type": "...",
  "answer_shape": "...",
  "target_system": "...",
  "confidence": 0.0,
  "reasons": ["..."],
  "needs_current_source": false,
  "scope_assumption": ""
}
"""


ALLOWED = {
    "SYSTEM_ANALYSIS",
    "FORECAST",
    "FORECAST_THESIS",
    "WORLD_FACT",
    "WORLD_ATTRIBUTION",
    "PROJECT_FACT",
    "PROJECT_ATTRIBUTION",
    "HOW_TO",
    "FOLLOW_UP_REWRITE",
    "CLARIFICATION_REQUIRED",
}


def _extract_json(raw: str) -> Dict[str, Any]:
    text = str(raw or "").strip()
    try:
        return json.loads(text)
    except Exception:
        pass

    m = re.search(r"\{.*\}", text, flags=re.S)
    if not m:
        return {}
    try:
        return json.loads(m.group(0))
    except Exception:
        return {}


def _shape(task_type: str) -> str:
    return {
        "SYSTEM_ANALYSIS": "full_ep",
        "FORECAST": "bounded_forecast",
        "FORECAST_THESIS": "thesis_forecast",
        "WORLD_FACT": "direct_answer",
        "WORLD_ATTRIBUTION": "direct_answer",
        "PROJECT_FACT": "direct_answer",
        "PROJECT_ATTRIBUTION": "direct_answer",
        "HOW_TO": "instructional_answer",
        "FOLLOW_UP_REWRITE": "rewrite_previous",
        "CLARIFICATION_REQUIRED": "clarify_first",
    }.get(task_type, "direct_answer")


def route_prompt_v5(prompt: str, previous_context: Dict[str, Any] | None = None) -> Dict[str, Any]:
    previous_context = previous_context or {}

    gateway = get_model_gateway()
    raw = gateway.generate(
        system_prompt=ROUTER_SYSTEM_PROMPT,
        runtime_state={},
        task=json.dumps(
            {
                "user_prompt": prompt,
                "previous_context": previous_context,
            },
            ensure_ascii=False,
        ),
    )

    payload = _extract_json(raw)
    task_type = str(payload.get("task_type") or "CLARIFICATION_REQUIRED").strip().upper()

    if task_type not in ALLOWED:
        task_type = "CLARIFICATION_REQUIRED"

    target = str(payload.get("target_system") or prompt).strip()

    try:
        confidence = float(payload.get("confidence", 0.7))
    except Exception:
        confidence = 0.7

    reasons = payload.get("reasons")
    if not isinstance(reasons, list):
        reasons = ["semantic_router_v5"]

    prompt_l = str(prompt or "").strip().lower()

    # Generic target-binding invariant:
    # "what is X in Y" is a definition request, not attribution, and the target is the whole X-in-Y phrase.
    attribution_words = ("who invented", "who created", "who founded", "who wrote", "who developed")
    if (prompt_l.startswith("what is ") or prompt_l.startswith("what does ")) and not prompt_l.startswith(attribution_words):
        if task_type == "WORLD_ATTRIBUTION":
            task_type = "WORLD_FACT"
            reasons.append("definition_not_attribution_guard")
        if " in " in prompt_l and ("what is " in prompt_l or "what does " in prompt_l):
            cleaned = prompt_l
            cleaned = cleaned.replace("what is ", "", 1)
            cleaned = cleaned.replace("what does ", "", 1)
            cleaned = cleaned.replace(" mean", "", 1)
            cleaned = cleaned.strip(" ?.")
            target = cleaned
            reasons.append("x_in_y_target_binding_guard")

    return {
        "task_type": task_type,
        "answer_shape": payload.get("answer_shape") or _shape(task_type),
        "target_system": target,
        "confidence": max(0.0, min(1.0, confidence)),
        "reasons": reasons,
        "needs_current_source": bool(payload.get("needs_current_source", False)),
        "scope_assumption": str(payload.get("scope_assumption") or ""),
    }
