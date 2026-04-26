from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from typing import Any, Dict, List


@dataclass
class RouteDecision:
    task_type: str
    answer_shape: str
    target_system: str
    confidence: float
    reasons: List[str]


SYSTEM_ANALYSIS_PATTERNS = [
    r"\banalyze\b",
    r"\bsystem\b",
    r"\bprocess\b",
    r"\bworkflow\b",
    r"\bapproval\b",
    r"\ballocation\b",
    r"\bintake\b",
    r"\breview\b",
    r"\btriage\b",
    r"\branking\b",
    r"\benforcement\b",
    r"\bdispatch\b",
    r"\bscheduler\b",
    r"\bunderwriting\b",
    r"\bmoderation\b",
    r"\bwaitlist\b",
]

PROJECT_ATTRIBUTION_PATTERNS = [
    r"^who invented energetic paradigm\b",
    r"^who created energetic paradigm\b",
    r"^who invented ep\b",
    r"^who invented epra\b",
    r"^who created epra\b",
]

GENERIC_ATTRIBUTION_PATTERNS = [
    r"^who invented\b",
    r"^who created\b",
    r"^who wrote\b",
    r"^who founded\b",
    r"^who developed\b",
    r"\binvented\b",
    r"\bcreator\b",
    r"\boriginated\b",
]

FORECAST_PATTERNS = [
    r"^will\b",
    r"^when will\b",
    r"^when would\b",
    r"^when is .* going to\b",
    r"^how long will\b",
    r"^when will\b",
    r"^when would\b",
    r"^when is .* going to\b",
    r"^how long will\b",
    r"^when will\b",
    r"^when would\b",
    r"^when is .* going to\b",
    r"^how long will\b",
    r"^would\b",
    r"^is .* going to\b",
    r"\blikely\b",
    r"\bforecast\b",
    r"\bprediction\b",
    r"\bchance\b",
    r"\bprobability\b",
]

PROJECT_FACT_PATTERNS = [
    r"^what is epra\b",
    r"^what is energetic paradigm\b",
    r"^what is ep\b",
    r"^what is canonical setup\b",
    r"^what is canonical_setup\b",
    r"^what are structural commitments\b",
    r"^what is structural commitments\b",
]

HOW_TO_PATTERNS = [
    r"^how to\b",
    r"^how do i\b",
    r"^how can i\b",
    r"^how should i\b",
]

DIRECT_FACT_PATTERNS = [
    r"^what is\b",
    r"^what are\b",
    r"^when was\b",
    r"^where is\b",
    r"^who is\b",
    r"^who was\b",
    r"^define\b",
    r"^explain\b",
]

AMBIGUOUS_SHORT_PATTERNS = [
    r"^analyze this$",
    r"^explain this$",
    r"^what about this$",
    r"^what about it$",
    r"^analyze it$",
    r"^explain it$",
]

PROJECT_TERMS = {
    "energetic paradigm",
    "epra",
    "epra api",
    "ep",
    "canonical setup",
    "canonical_setup",
    "structural commitments",
    "structural_commitments",
}


def _matches_any(text: str, patterns: List[str]) -> bool:
    return any(re.search(pattern, text, flags=re.I) for pattern in patterns)


def _extract_target_system(prompt: str) -> str:
    text = prompt.strip()

    patterns = [
        r"analyze\s+the\s+(.+?)\s+with\s+energetic paradigm",
        r"analyze\s+the\s+(.+)$",
        r"^who invented\s+(.+?)[\?]?$",
        r"^who created\s+(.+?)[\?]?$",
        r"^who wrote\s+(.+?)[\?]?$",
        r"^who founded\s+(.+?)[\?]?$",
        r"^who developed\s+(.+?)[\?]?$",
        r"^who is\s+(.+?)[\?]?$",
        r"^who was\s+(.+?)[\?]?$",
        r"^what is\s+(.+?)[\?]?$",
        r"^what are\s+(.+?)[\?]?$",
        r"^when was\s+(.+?)[\?]?$",
        r"^where is\s+(.+?)[\?]?$",
        r"^will\s+(.+?)[\?]?$",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, flags=re.I)
        if match:
            return match.group(1).strip()

    return text


def _is_project_target(target: str) -> bool:
    t = target.strip().lower()
    return t in PROJECT_TERMS


def route_prompt_v4(prompt: str) -> Dict[str, Any]:
    text = prompt.strip()
    lower = text.lower()
    reasons: List[str] = []
    target = _extract_target_system(text)

    if not text or len(text) < 8 or _matches_any(lower, AMBIGUOUS_SHORT_PATTERNS):
        reasons.append("prompt_too_short_or_ambiguous")
        return asdict(RouteDecision(
            task_type="CLARIFICATION_REQUIRED",
            answer_shape="clarify_first",
            target_system=text or "unspecified target",
            confidence=0.95,
            reasons=reasons,
        ))

    if _matches_any(lower, PROJECT_ATTRIBUTION_PATTERNS):
        reasons.append("project_attribution_pattern_match")
        return asdict(RouteDecision(
            task_type="PROJECT_ATTRIBUTION",
            answer_shape="direct_answer",
            target_system=target,
            confidence=0.98,
            reasons=reasons,
        ))

    if _matches_any(lower, GENERIC_ATTRIBUTION_PATTERNS):
        if _is_project_target(target):
            reasons.append("project_attribution_target_match")
            return asdict(RouteDecision(
                task_type="PROJECT_ATTRIBUTION",
                answer_shape="direct_answer",
                target_system=target,
                confidence=0.95,
                reasons=reasons,
            ))
        reasons.append("world_attribution_pattern_match")
        return asdict(RouteDecision(
            task_type="WORLD_ATTRIBUTION",
            answer_shape="direct_answer",
            target_system=target,
            confidence=0.92,
            reasons=reasons,
        ))

    if _matches_any(lower, FORECAST_PATTERNS):
        reasons.append("forecast_pattern_match")
        return asdict(RouteDecision(
            task_type="FORECAST",
            answer_shape="bounded_forecast",
            target_system=target,
            confidence=0.90,
            reasons=reasons,
        ))


    if _matches_any(lower, HOW_TO_PATTERNS):
        reasons.append("how_to_pattern_match")
        return asdict(RouteDecision(
            task_type="HOW_TO",
            answer_shape="instructional_answer",
            target_system=target,
            confidence=0.88,
            reasons=reasons,
        ))

    if _matches_any(lower, PROJECT_FACT_PATTERNS):
        reasons.append("project_fact_pattern_match")
        return asdict(RouteDecision(
            task_type="PROJECT_FACT",
            answer_shape="direct_answer",
            target_system=target,
            confidence=0.95,
            reasons=reasons,
        ))

    if _matches_any(lower, DIRECT_FACT_PATTERNS) and "system" not in lower:
        if _is_project_target(target):
            reasons.append("project_fact_target_match")
            return asdict(RouteDecision(
                task_type="PROJECT_FACT",
                answer_shape="direct_answer",
                target_system=target,
                confidence=0.90,
                reasons=reasons,
            ))
        reasons.append("world_fact_pattern_match")
        return asdict(RouteDecision(
            task_type="WORLD_FACT",
            answer_shape="direct_answer",
            target_system=target,
            confidence=0.85,
            reasons=reasons,
        ))

    if _matches_any(lower, SYSTEM_ANALYSIS_PATTERNS):
        reasons.append("system_analysis_pattern_match")
        return asdict(RouteDecision(
            task_type="SYSTEM_ANALYSIS",
            answer_shape="full_ep",
            target_system=target,
            confidence=0.90,
            reasons=reasons,
        ))

    reasons.append("fallback_to_clarification")
    return asdict(RouteDecision(
        task_type="CLARIFICATION_REQUIRED",
        answer_shape="clarify_first",
        target_system=target,
        confidence=0.60,
        reasons=reasons,
    ))
