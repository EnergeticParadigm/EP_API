from __future__ import annotations

from typing import Any, Dict


CONTROL_CLASSES = {
    "FACT",
    "HOW_TO",
    "FORECAST",
    "EP_ANALYSIS",
    "LIVE_SOURCE_REQUIRED",
    "STRUCTURED_TASK",
    "FOLLOW_UP",
    "CLARIFY",
}


def normalize_control_class(route: Dict[str, Any]) -> Dict[str, Any]:
    task_type = str(route.get("task_type") or "").upper()
    needs_current = bool(route.get("needs_current_source", False))

    if needs_current:
        control_class = "LIVE_SOURCE_REQUIRED"
    elif task_type in {"WORLD_FACT", "PROJECT_FACT", "WORLD_ATTRIBUTION", "PROJECT_ATTRIBUTION", "ATTRIBUTION"}:
        control_class = "FACT"
    elif task_type == "HOW_TO":
        control_class = "HOW_TO"
    elif task_type in {"FORECAST", "FORECAST_THESIS"}:
        control_class = "FORECAST"
    elif task_type == "SYSTEM_ANALYSIS":
        control_class = "EP_ANALYSIS"
    elif task_type == "FOLLOW_UP_REWRITE":
        control_class = "FOLLOW_UP"
    elif task_type == "CLARIFICATION_REQUIRED":
        control_class = "CLARIFY"
    else:
        control_class = "STRUCTURED_TASK"

    route["control_class"] = control_class
    route["control_policy"] = policy_for(control_class, route)
    return route


def policy_for(control_class: str, route: Dict[str, Any]) -> Dict[str, Any]:
    policies = {
        "FACT": {
            "truth_condition": "answer directly; avoid unsupported certainty",
            "source_rule": "use model knowledge unless current-source flag is set",
            "answer_shape": "concise answer plus brief explanation",
        },
        "HOW_TO": {
            "truth_condition": "give practical steps; include safety caveats only when useful",
            "source_rule": "no live source needed unless availability/prices/schedules are involved",
            "answer_shape": "steps",
        },
        "FORECAST": {
            "truth_condition": "bounded uncertainty; no fake certainty",
            "source_rule": "current-source required for current events, geopolitics, markets, sports, law, schedules",
            "answer_shape": "bottom line, confidence, drivers, change conditions",
        },
        "EP_ANALYSIS": {
            "truth_condition": "must produce canonical EP structure and pass validation",
            "source_rule": "current-source optional unless user asks about live/current status",
            "answer_shape": "EP canonical analysis",
        },
        "LIVE_SOURCE_REQUIRED": {
            "truth_condition": "do not pretend live verification; either use connected source or state limitation",
            "source_rule": "must check current-source gateway before final answer",
            "answer_shape": "source status, answer if possible, uncertainty",
        },
        "STRUCTURED_TASK": {
            "truth_condition": "preserve requested structure",
            "source_rule": "depends on task",
            "answer_shape": "task-specific",
        },
        "FOLLOW_UP": {
            "truth_condition": "inherit prior target unless user clearly changes it",
            "source_rule": "inherit prior source requirement",
            "answer_shape": "follow user modification",
        },
        "CLARIFY": {
            "truth_condition": "ask one precise clarification",
            "source_rule": "do not invent missing target",
            "answer_shape": "single question",
        },
    }
    return policies.get(control_class, policies["STRUCTURED_TASK"])
