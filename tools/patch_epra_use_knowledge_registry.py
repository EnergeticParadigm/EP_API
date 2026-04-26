from pathlib import Path

p = Path("app/services/epra.py")
text = p.read_text()

import_anchor = "from typing import Any, Dict"
import_add = """from typing import Any, Dict
from app.services.knowledge_registry import (
    lookup_attribution,
    lookup_clarification_hint,
    lookup_definition,
    lookup_forecast,
)"""

if "from app.services.knowledge_registry import (" not in text:
    if import_anchor not in text:
        raise SystemExit("typing import anchor not found")
    text = text.replace(import_anchor, import_add, 1)

old_attr = """    def _handle_attribution(self, task: str, routing: Dict[str, Any]) -> EPRAResponse:
        target = routing.get("target_system") or task
        t = str(target).strip().lower()

        if t in {"energetic paradigm", "ep"}:
            direct = "Energetic Paradigm was developed by Wesley Shu."
            basis = "This answer is based on the current project framing and the way EP is defined inside the EPRA runtime and project materials."
            uncertainty = "If you want a formal public-origin statement, that should be frozen in release documentation."
        elif t in {"epra", "epra api", "epra framework"}:
            direct = "EPRA is the runtime and wrapper implementation built to operationalize Energetic Paradigm."
            basis = "This answer is based on the current wrapper and release structure in the project."
            uncertainty = "The exact naming boundary between framework, runtime, and wrapper should still be standardized in release documents."
        else:
            direct = f"I do not have a grounded attribution record for '{target}' in the current runtime."
            basis = "This mode should answer origin or authorship directly, but it should not invent provenance that is not explicitly grounded."
            uncertainty = "Attribution should remain unresolved unless the project corpus or release documentation names a clear origin."

        answer = (
            f"Direct answer: {direct}\\n\\n"
            f"Basis: {basis}\\n\\n"
            f"Uncertainty: {uncertainty}"
        )
"""

new_attr = """    def _handle_attribution(self, task: str, routing: Dict[str, Any]) -> EPRAResponse:
        target = routing.get("target_system") or task
        hit = lookup_attribution(str(target))

        if hit:
            direct = hit["direct"]
            basis = hit["basis"]
            uncertainty = hit["uncertainty"]
        else:
            direct = f"I do not have a grounded attribution record for '{target}' in the current runtime."
            basis = "This mode should answer origin or authorship directly, but it should not invent provenance that is not explicitly grounded."
            uncertainty = "Attribution should remain unresolved unless the project corpus or release documentation names a clear origin."

        answer = (
            f"Direct answer: {direct}\\n\\n"
            f"Basis: {basis}\\n\\n"
            f"Uncertainty: {uncertainty}"
        )
"""

old_fore = """    def _handle_forecast(self, task: str, routing: Dict[str, Any]) -> EPRAResponse:
        target = routing.get("target_system") or task
        t = str(target).strip().lower()

        if "occupy iran" in t or ("us" in t and "iran" in t):
            bottom_line = "Probably not in the near term."
            confidence = "Low to medium confidence."
            drivers = [
                "The military, political, and economic costs of occupation would be extremely high.",
                "Regional escalation risk would likely exceed any stable gain from occupation.",
                "Domestic and allied tolerance for a long occupation is likely weak.",
            ]
            watch = [
                "direct regime-collapse scenarios",
                "major interstate escalation",
                "sustained deployment and occupation signaling",
            ]
        else:
            bottom_line = f"I cannot make a confident forecast about '{target}' without a more specific scope."
            confidence = "Low confidence."
            drivers = [
                "The forecast target is underspecified.",
                "The time horizon is unclear.",
                "The key structural drivers are not yet bounded.",
            ]
            watch = [
                "clear timeframe",
                "clear actors",
                "clear decision threshold",
            ]

        answer = (
            f"Bottom line: {bottom_line}\\n\\n"
            f"Confidence: {confidence}\\n\\n"
            f"Main drivers:\\n- " + "\\n- ".join(drivers) + "\\n\\n"
            f"What could change the forecast:\\n- " + "\\n- ".join(watch)
        )
"""

new_fore = """    def _handle_forecast(self, task: str, routing: Dict[str, Any]) -> EPRAResponse:
        target = routing.get("target_system") or task
        hit = lookup_forecast(str(target))

        if hit:
            bottom_line = hit["bottom_line"]
            confidence = hit["confidence"]
            drivers = hit["drivers"]
            watch = hit["watch_conditions"]
        else:
            bottom_line = f"I cannot make a confident forecast about '{target}' without a more specific scope."
            confidence = "Low confidence."
            drivers = [
                "The forecast target is underspecified.",
                "The time horizon is unclear.",
                "The key structural drivers are not yet bounded.",
            ]
            watch = [
                "clear timeframe",
                "clear actors",
                "clear decision threshold",
            ]

        answer = (
            f"Bottom line: {bottom_line}\\n\\n"
            f"Confidence: {confidence}\\n\\n"
            f"Main drivers:\\n- " + "\\n- ".join(drivers) + "\\n\\n"
            f"What could change the forecast:\\n- " + "\\n- ".join(watch)
        )
"""

old_fact = """    def _handle_direct_fact(self, task: str, routing: Dict[str, Any]) -> EPRAResponse:
        target = routing.get("target_system") or task
        t = str(target).strip().lower()

        if t == "epra":
            answer = (
                "EPRA is the runtime and wrapper implementation used to operationalize Energetic Paradigm.\\n\\n"
                "It takes prompts, builds structured representations, validates them, and returns readable analysis."
            )
        elif t in {"energetic paradigm", "ep"}:
            answer = (
                "Energetic Paradigm is a structure-first analytical framework focused on flow, control, burden, maintenance, asymmetry, and system fragility.\\n\\n"
                "In the current project, EP is implemented operationally through EPRA."
            )
        else:
            answer = (
                f"{target}\\n\\n"
                "This was routed as a direct factual request, so it should be answered plainly rather than forced into full EP system-analysis form."
            )
"""

new_fact = """    def _handle_direct_fact(self, task: str, routing: Dict[str, Any]) -> EPRAResponse:
        target = routing.get("target_system") or task
        hit = lookup_definition(str(target))

        if hit:
            answer = f"{hit['answer']}\\n\\n{hit['explanation']}"
        else:
            answer = (
                f"{target}\\n\\n"
                "This was routed as a direct factual request, so it should be answered plainly rather than forced into full EP system-analysis form."
            )
"""

old_clar = """    def _handle_clarification(self, task: str, routing: Dict[str, Any]) -> EPRAResponse:
        target = routing.get("target_system") or task
        answer = (
            f"I need one missing detail before answering well: the prompt '{target}' does not yet specify a stable target or scope.\\n\\n"
            f"Question: do you want a system analysis, a direct fact, an attribution answer, or a forecast?"
        )
"""

new_clar = """    def _handle_clarification(self, task: str, routing: Dict[str, Any]) -> EPRAResponse:
        target = routing.get("target_system") or task
        hint = lookup_clarification_hint(str(task))

        if hint:
            answer = (
                f"I need one missing detail before answering well: {hint['missing']}.\\n\\n"
                f"Question: {hint['question']}"
            )
        else:
            answer = (
                f"I need one missing detail before answering well: the prompt '{target}' does not yet specify a stable target or scope.\\n\\n"
                f"Question: do you want a system analysis, a direct fact, an attribution answer, or a forecast?"
            )
"""

repls = [
    (old_attr, new_attr, "attribution"),
    (old_fore, new_fore, "forecast"),
    (old_fact, new_fact, "direct_fact"),
    (old_clar, new_clar, "clarification"),
]

for old, new, name in repls:
    if old not in text:
        raise SystemExit(f"{name} block not found")
    text = text.replace(old, new, 1)

p.write_text(text)
print("patched", p)
