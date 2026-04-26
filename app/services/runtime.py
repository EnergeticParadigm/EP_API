from __future__ import annotations

import re


from dataclasses import dataclass
from typing import Any, Dict


def _clean_task_system(text: str) -> str:
    s = str(text or "").strip()
    s = re.sub(r'\b(?:with|using|through|via|in)\s+Energetic\s+Paradigm\b', '', s, flags=re.I)
    s = re.sub(r'\bEnergetic\s+Paradigm\b', '', s, flags=re.I)
    s = re.sub(r'\bEPRA\b', '', s, flags=re.I)
    s = re.sub(r'\s+', ' ', s).strip(" .,:;-")
    return s

import os
import yaml

from app.services.corpus import PrivateCorpusRetrieverDistiller


@dataclass
class RuntimeState:
    task_system: str
    active_forms: list[str]
    kernel: dict[str, str]
    selected_rules: dict[str, Any]
    examples: list[dict[str, Any]]
    distilled_corpus: list[dict[str, Any]]


class RuntimeBuilder:
    def __init__(self) -> None:
        config_path = os.getenv("EPRA_RUNTIME_CONFIG", "./config/epra_runtime_policy.yaml")
        with open(config_path, "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)
        self.retriever = PrivateCorpusRetrieverDistiller()

    def classify_system(self, task: str) -> str:
        text = task.lower()
        if any(k in text for k in ["policy", "institution", "government", "law", "court", "university"]):
            return "institutional"
        if any(k in text for k in ["ai", "model", "inference", "deployment", "llm", "agent"]):
            return "computational"
        if any(k in text for k in ["logistics", "supply", "command", "military", "transport"]):
            return "logistical"
        return "generic_system"

    def infer_active_forms(self, task_system: str) -> list[str]:
        mapping = {
            "institutional": ["authority", "compliance_capacity", "legitimacy_pressure", "maintenance_load"],
            "computational": ["compute", "memory_bandwidth", "routing_load", "maintenance_load"],
            "logistical": ["supply_throughput", "command_bandwidth", "reserve_depth", "maintenance_load"],
            "generic_system": ["effective_force", "maintenance_load", "control_burden"],
        }
        return mapping.get(task_system, mapping["generic_system"])

    def build(self, task: str, context: Dict[str, Any] | None = None) -> RuntimeState:
        routing = (context or {}).get("routing", {})

        if routing.get("target_system"):
            task_system = _clean_task_system(routing["target_system"])
        else:
            task_system = _clean_task_system(self.classify_system(task))

        if routing.get("mode") == "ep_system_analysis":
            active_forms = ["effective_force", "maintenance_load", "control_burden"]
        elif routing.get("mode") == "ep_attribution":
            active_forms = ["effective_force", "maintenance_load", "control_burden"]
        else:
            active_forms = self.infer_active_forms(task_system)

        retrieved = self.retriever.retrieve(
            task=task,
            context=context,
            top_k=self.config["corpus"]["max_retrieved_items"],
        )
        distilled_corpus = self.retriever.distill(
            retrieved,
            max_items=self.config["corpus"]["max_distilled_items"],
            max_chars=self.config["corpus"]["distill_max_chars_per_snippet"],
        )

        task_type = routing.get("task_type")
        target_system = (routing.get("target_system") or "").strip().lower()

        if task_type == "SYSTEM_ANALYSIS":
            distilled_corpus = [
                x for x in distilled_corpus
                if x.get("entry_id") not in {"ep_methodology_full", "ep_fcs_v0"}
            ]

        elif task_type == "AMBIGUOUS":
            distilled_corpus = []

        elif task_type == "ATTRIBUTION":
            distilled_corpus = [
                x for x in distilled_corpus
                if x.get("entry_id") in {"ep_fcs_v0", "ep_methodology_full"}
            ]

        if not distilled_corpus and task_type == "SYSTEM_ANALYSIS":
            distilled_corpus = [{
                "entry_id": "runtime_target_anchor",
                "title": "Runtime Target Anchor",
                "role": "target_anchor",
                "signal": f"The bound system for analysis is: {routing.get('target_system')}. Do not replace it with a generic EP object.",
                "score": 10.0,
            }]
        kernel = {
            "system": task_system,
            "active_forms": ", ".join(active_forms),
            "source": "identify effective input or origin",
            "sink": "identify effective destination or consumption point",
            "gradient": "identify directional pressure or asymmetry",
            "path": "identify admissible route or transfer chain",
            "barrier": "identify obstruction or gating",
            "loss": "identify degradation, leakage, or dissipation",
        }
        selected_rules = {
            "require_compact_setup": True,
            "require_validity_label": True,
            "allowed_labels": self.config["runtime"]["allowed_labels"],
            "required_setup_fields": self.config["runtime"]["required_setup_fields"],
            "hard_constraints": {
                "must_bind_target": True,
                "must_not_change_target": True,
            },
        }
        examples = []
        return RuntimeState(
            task_system=task_system,
            active_forms=active_forms,
            kernel=kernel,
            selected_rules=selected_rules,
            examples=examples,
            distilled_corpus=distilled_corpus,
        )
