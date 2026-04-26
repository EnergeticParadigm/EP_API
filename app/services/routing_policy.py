from __future__ import annotations

import re
from typing import Any, Dict


def _clean_bound_target(text: str) -> str:
    s = str(text or "").strip()
    s = re.sub(r'\b(?:with|using|through|via|in)\s+Energetic\s+Paradigm\b', '', s, flags=re.I)
    s = re.sub(r'\bEnergetic\s+Paradigm\b', '', s, flags=re.I)
    s = re.sub(r'\bEPRA\b', '', s, flags=re.I)
    s = re.sub(r'\bthe\s+', '', s, flags=re.I)
    s = re.sub(r'\s+', ' ', s).strip(" .,:;-")
    return s



CAT_ATTRIBUTION = "ATTRIBUTION"
CAT_DIRECT_ONLY = "DIRECT_ONLY"
CAT_DIRECT_PLUS_EP = "DIRECT_PLUS_EP"
CAT_FULL_EP = "FULL_EP"
CAT_CLARIFY_FIRST = "CLARIFY_FIRST"
CAT_VALIDATION = "VALIDATION"
CAT_RECONSTRUCTION = "RECONSTRUCTION"


def normalize_input(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip())


def detect_language(text: str) -> str:
    if re.search(r"[\u4e00-\u9fff]", text):
        return "zh"
    return "en"


def classify_question(text: str) -> str:
    t = text.lower().strip()

    if not t:
        return CAT_CLARIFY_FIRST

    if any(k in t for k in ["validate", "validation", "validity check", "is this valid ep"]):
        return CAT_VALIDATION

    if any(k in t for k in ["reconstruct", "reconstruction"]):
        return CAT_RECONSTRUCTION

    if re.match(r"^(who|who is|who invented|who created|who developed|who wrote)\b", t):
        return CAT_ATTRIBUTION

    if any(k in t for k in [
        "invented", "created", "developed", "authorship", "origin of", "who wrote"
    ]):
        return CAT_ATTRIBUTION

    if any(k in t for k in [
        "analyze", "analysis", "in ep terms", "use ep", "map", "model", "compare", "trace"
    ]):
        return CAT_FULL_EP

    if re.match(r"^(what is|what are|what does|define|explain)\b", t):
        if "ep" in t or "energetic paradigm" in t:
            return CAT_DIRECT_PLUS_EP
        return CAT_DIRECT_ONLY

    if re.match(r"^(is|are|can|does|did|will|should|could|would|when|where|which|what)\b", t):
        return CAT_DIRECT_ONLY

    if len(t.split()) <= 3:
        return CAT_CLARIFY_FIRST

    return CAT_FULL_EP


def _clean_target(x: str) -> str:
    return x.strip(" .?\"'").strip()


def bind_target(text: str, category: str) -> str:
    raw = text.strip()

    if category == CAT_ATTRIBUTION:
        patterns = [
            r"who invented (.+?)\??$",
            r"who created (.+?)\??$",
            r"who developed (.+?)\??$",
            r"who wrote (.+?)\??$",
            r"origin of (.+?)\??$",
        ]
        for p in patterns:
            m = re.search(p, raw, flags=re.IGNORECASE)
            if m:
                return _clean_target(m.group(1))

    if category == CAT_FULL_EP:
        patterns = [
            r"analyze (.+?) in ep terms\.?$",
            r"analyze (.+?)\.?$",
            r"map (.+?) in ep terms\.?$",
            r"model (.+?) in ep terms\.?$",
            r"compare (.+?) in ep terms\.?$",
            r"trace (.+?) in ep terms\.?$",
        ]
        for p in patterns:
            m = re.search(p, raw, flags=re.IGNORECASE)
            if m:
                return _clean_target(m.group(1))

    if category == CAT_DIRECT_PLUS_EP:
        patterns = [
            r"what is (.+?)\??$",
            r"define (.+?)\??$",
            r"explain (.+?)\??$",
        ]
        for p in patterns:
            m = re.search(p, raw, flags=re.IGNORECASE)
            if m:
                return _clean_target(m.group(1))

    if category == CAT_DIRECT_ONLY:
        patterns = [
            r"is (.+?) a [^.?\n]+\??$",
            r"is (.+?) an [^.?\n]+\??$",
            r"are (.+?) [^.?\n]+\??$",
            r"what is (.+?)\??$",
            r"what are (.+?)\??$",
            r"does (.+?) [^.?\n]+\??$",
            r"did (.+?) [^.?\n]+\??$",
        ]
        for p in patterns:
            m = re.search(p, raw, flags=re.IGNORECASE)
            if m:
                return _clean_target(m.group(1))

    return raw


def select_mode(category: str) -> str:
    if category == CAT_ATTRIBUTION:
        return "ep_attribution"
    if category == CAT_FULL_EP:
        return "ep_system_analysis"
    if category == CAT_CLARIFY_FIRST:
        return "ep_clarify"
    if category == CAT_VALIDATION:
        return "ep_validate"
    if category == CAT_RECONSTRUCTION:
        return "ep_reconstruct"
    if category in {CAT_DIRECT_ONLY, CAT_DIRECT_PLUS_EP}:
        return "ep_direct_constrained"
    return "ep_system_analysis"


def build_control(category: str, target_system: str) -> Dict[str, Any]:
    answer_shape = {
        CAT_ATTRIBUTION: "direct_first_then_ep",
        CAT_DIRECT_ONLY: "direct_only",
        CAT_DIRECT_PLUS_EP: "direct_then_ep",
        CAT_FULL_EP: "full_ep",
        CAT_CLARIFY_FIRST: "clarify_first",
        CAT_VALIDATION: "validation",
        CAT_RECONSTRUCTION: "reconstruction",
    }[category]

    return {
        "must_bind_target": bool(target_system),
        "must_not_change_target": True,
        "must_not_invent_attribution": category == CAT_ATTRIBUTION,
        "allow_clarification": category == CAT_CLARIFY_FIRST,
        "answer_shape": answer_shape,
    }


def route_task(raw_input: str) -> Dict[str, Any]:
    normalized_input = normalize_input(raw_input)
    language = detect_language(normalized_input)
    question_category = classify_question(normalized_input)
    target_system = _clean_bound_target(bind_target(normalized_input, question_category))
    mode = select_mode(question_category)
    control = build_control(question_category, target_system)

    return {
        "raw_input": raw_input,
        "normalized_input": normalized_input,
        "language": language,
        "question_category": question_category,
        "task_type": question_category,
        "target_system": _clean_bound_target(target_system),
        "mode": mode,
        "needs_clarification": question_category == CAT_CLARIFY_FIRST,
        "control": control,
    }
