from __future__ import annotations

from typing import Any, Dict, List


DEFINITIONS: Dict[str, Dict[str, Any]] = {
    "epra": {
        "answer": "EPRA is the runtime and wrapper implementation used to operationalize Energetic Paradigm.",
        "explanation": (
            "It takes prompts, routes them by task type, builds structured representations for system-analysis tasks, "
            "validates those structures, and returns readable answers."
        ),
        "aliases": ["epra", "epra api", "epra framework"],
    },
    "energetic paradigm": {
        "answer": "Energetic Paradigm is a structure-first analytical framework for studying flow, control, burden, maintenance, asymmetry, and system fragility.",
        "explanation": (
            "In this project, it is implemented operationally through EPRA as a governed runtime rather than remaining only a conceptual framework."
        ),
        "aliases": ["energetic paradigm", "ep"],
    },
    "canonical_setup": {
        "answer": "canonical_setup is the normalized structural object used inside EPRA.",
        "explanation": (
            "It contains system, flow_objects, constraint_objects, and structural_commitments, and serves as the source of validation and rendering."
        ),
        "aliases": ["canonical setup", "canonical_setup"],
    },
    "structural_commitments": {
        "answer": "structural_commitments are the explicit higher-order EP fields that make analysis validity legible.",
        "explanation": (
            "They include asymmetry, pressure_point, tradeoff, actors, cost_bearer, and fracture_condition."
        ),
        "aliases": ["structural commitments", "structural_commitments"],
    },
}


ATTRIBUTIONS: Dict[str, Dict[str, Any]] = {
    "energetic paradigm": {
        "direct": "Energetic Paradigm was developed by Wesley Shu.",
        "basis": (
            "This answer is based on the current project framing and the way Energetic Paradigm is named and organized in the EP Model workspace."
        ),
        "uncertainty": (
            "If you want a formal public-origin statement, that should be frozen in release documentation and repeated consistently across product surfaces."
        ),
        "aliases": ["energetic paradigm", "ep"],
    },
    "epra": {
        "direct": "EPRA was built as the operational runtime and wrapper layer for Energetic Paradigm inside this project.",
        "basis": (
            "This answer is based on the current wrapper structure, release organization, and project naming conventions."
        ),
        "uncertainty": (
            "The exact distinction between framework, runtime, wrapper, and release label should still be standardized in official documentation."
        ),
        "aliases": ["epra", "epra api", "epra framework"],
    },
}


FORECAST_PRESETS: Dict[str, Dict[str, Any]] = {
    "us_occupy_iran": {
        "match_terms": ["us", "iran", "occupy"],
        "bottom_line": "Probably not in the near term.",
        "confidence": "Low to medium confidence.",
        "drivers": [
            "The military, political, and economic costs of occupation would be extremely high.",
            "Regional escalation risk would likely exceed any stable gain from occupation.",
            "Domestic and allied tolerance for a long occupation is likely weak.",
        ],
        "watch_conditions": [
            "direct regime-collapse scenarios",
            "major interstate escalation",
            "sustained deployment and occupation signaling",
        ],
    },
}


CLARIFICATION_HINTS: List[Dict[str, str]] = [
    {
        "match": "analyze",
        "missing": "the target system is unspecified",
        "question": "What exact system or process do you want analyzed?",
    },
    {
        "match": "will",
        "missing": "the forecast scope is underspecified",
        "question": "What time horizon and what exact outcome do you want forecasted?",
    },
]


def _normalize(text: str) -> str:
    return text.strip().lower()


def lookup_definition(target: str) -> Dict[str, Any] | None:
    t = _normalize(target)
    for item in DEFINITIONS.values():
        aliases = [_normalize(x) for x in item.get("aliases", [])]
        if t in aliases:
            return item
    return None


def lookup_attribution(target: str) -> Dict[str, Any] | None:
    t = _normalize(target)
    for item in ATTRIBUTIONS.values():
        aliases = [_normalize(x) for x in item.get("aliases", [])]
        if t in aliases:
            return item
    return None


def lookup_forecast(target: str) -> Dict[str, Any] | None:
    t = _normalize(target)
    for item in FORECAST_PRESETS.values():
        terms = [_normalize(x) for x in item.get("match_terms", [])]
        if all(term in t for term in terms):
            return item
    return None


def lookup_clarification_hint(task: str) -> Dict[str, str] | None:
    t = _normalize(task)
    for item in CLARIFICATION_HINTS:
        if item["match"] in t:
            return item
    return None
