from __future__ import annotations

from typing import Dict, Any
import os
import re
import yaml


class ValidityEngine:
    def __init__(self) -> None:
        config_path = os.getenv("EPRA_RUNTIME_CONFIG", "./config/epra_runtime_policy.yaml")
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f)
        self.validity_cfg = cfg["validity"]
        self.runtime_cfg = cfg["runtime"]

    def _contains_any(self, text: str, terms: list[str]) -> bool:
        return any(term in text for term in terms)

    def _is_specified(self, value) -> bool:
        if value is None:
            return False
        if isinstance(value, str):
            s = value.strip().upper()
            return s != "" and s != "UNSPECIFIED"
        if isinstance(value, (list, tuple, set, dict)):
            return len(value) > 0
        return True

    def validate_canonical(self, canonical: Dict[str, Any]) -> Dict[str, Any]:
        flow = canonical.get("flow_objects", {}) or {}
        constraints = canonical.get("constraint_objects", {}) or {}
        commitments = canonical.get("structural_commitments", {}) or {}

        gates = {
            "setup": self._is_specified(canonical.get("system")) and all(
                self._is_specified(flow.get(k)) for k in ["source", "sink", "gradient", "path"]
            ) and all(
                self._is_specified(constraints.get(k)) for k in ["barrier", "loss"]
            ),
            "maintenance": self._is_specified(constraints.get("maintenance")),
            "control": self._is_specified(constraints.get("control")),
            "fragility": self._is_specified(constraints.get("fragility")),
            "asymmetry": self._is_specified(commitments.get("asymmetry")),
            "pressure": self._is_specified(commitments.get("pressure_point")),
            "tradeoff": self._is_specified(commitments.get("tradeoff")),
            "specificity": self._is_specified(canonical.get("system")) and any(
                self._is_specified(flow.get(k)) for k in ["source", "sink", "path"]
            ),
            "concreteness": (
                len(commitments.get("actors", []) or []) > 0
                or self._is_specified(commitments.get("cost_bearer"))
                or self._is_specified(commitments.get("fracture_condition"))
            ),
        }

        weighted = self.validity_cfg["weighted_checks"]
        score = 0.0
        for key, weight in weighted.items():
            score += (1.0 if gates.get(key, False) else 0.0) * float(weight)

        drift_flags = {
            "missing_setup": not gates["setup"],
            "missing_asymmetry": not gates["asymmetry"],
            "missing_pressure": not gates["pressure"],
            "missing_tradeoff": not gates["tradeoff"],
            "low_concreteness": not gates["concreteness"],
            "generic_template": False,
            "generic_language": False,
            "moralizing_only": False,
            "metaphoric_energy_only": False,
        }

        hard_drift_keys = [
            "missing_setup",
            "missing_asymmetry",
            "missing_pressure",
            "missing_tradeoff",
            "low_concreteness",
        ]
        soft_drift_keys = [
            "generic_template",
            "generic_language",
            "moralizing_only",
            "metaphoric_energy_only",
        ]

        hard_drift_count = sum(1 for k in hard_drift_keys if drift_flags.get(k))
        soft_drift_count = sum(1 for k in soft_drift_keys if drift_flags.get(k))
        mandatory_pass = all(gates[g] for g in self.validity_cfg["mandatory_gates"])

        if score >= self.validity_cfg["thresholds"]["valid_ep"] and hard_drift_count == 0 and mandatory_pass:
            label = "Valid EP"
        elif score >= self.validity_cfg["thresholds"]["weak_ep"]:
            label = "Weak EP" if hard_drift_count == 0 else "Drifted EP"
        else:
            label = "Pseudo-EP" if drift_flags["missing_setup"] else "Drifted EP"

        return {
            "label": label,
            "score": round(score, 3),
            "gates": gates,
            "drift_flags": drift_flags,
            "hard_drift_count": hard_drift_count,
            "soft_drift_count": soft_drift_count,
            "mandatory_pass": mandatory_pass,
            "validation_source": "canonical",
        }

    def validate_text(self, text: str) -> Dict[str, Any]:
        lower = text.lower()
        gates = {
            "setup": self._contains_any(lower, ["source", "sink", "gradient", "path", "barrier", "loss"]),
            "maintenance": self._contains_any(lower, ["maintenance"]),
            "control": self._contains_any(lower, ["control"]),
            "fragility": self._contains_any(lower, ["fragility", "fracture", "failure pathway", "legal challenge", "review error", "overload", "policy shock", "appeal", "gaming", "misclassification"]),
            "asymmetry": self._contains_any(lower, [
                "benefits", "benefit", "gains", "advantage", "favored",
                "filtered out", "excluded", "rejected", "absorbs cost", "bears cost",
                "who benefits", "who is filtered out",
                "gets priority", "prioritized", "priority for", "severely ill",
                "less urgent", "waits longer", "delays for", "underrepresented groups",
                "critical care for", "worsens outcomes for", "those with less obvious",
                "additional screening", "secondary screening", "flagged passengers",
                "ordinary passengers", "cleared passengers", "passengers subjected to",
                "high-risk", "heightened risk levels", "extra screening",
                "approved", "denied", "accepted", "screened out", "selected",
                "ranked higher", "ranked lower", "matched first", "left waiting",
                "drivers absorb", "riders wait", "creators lose reach", "flagged content",
                "eligible", "ineligible", "qualified", "disqualified", "priority cases",
                "low-priority", "fast-tracked", "deferred", "escalated", "ordinary users",
                "high-value customers", "low-value customers", "borrowers", "lenders",
                "couriers absorb", "drivers bear", "restaurants wait", "customers wait",
                "high-engagement content", "low-visibility users", "moderators escalate",
                "flagged users", "ordinary posts", "viral content", "shadowed", "demoted",
                "detainees wait", "new arrivals are classified", "high-risk inmates", "low-risk inmates",
                "segregated", "general population", "restricted movement", "disciplinary referral",
                "students removed", "suspended students", "expelled students", "compliant students",
                "targeted students", "repeat offenders", "students flagged", "students who comply",
                "some students", "other students", "higher-risk detainees", "lower-risk detainees",
                "new arrivals", "intake detainees", "classified inmates", "pretrial detainees",
                "violent offenders", "nonviolent detainees", "maximum security", "minimum security",
                "placed in segregation", "placed in general population", "those awaiting classification",
                "arrestees", "law enforcement agencies", "police holding cells", "rapid offload",
                "wrongful detention", "holding times", "flagged for medical or legal issues",
                "diverted for further review", "assigned to housing units", "security classification",
                "medical needs", "those who pass all checks", "those flagged",
                "pickers", "packers", "forklift operators", "warehouse supervisors",
                "priority shipments", "rush orders", "back-of-queue orders", "slow-moving inventory",
                "workers absorb", "retailers wait", "stores wait", "drivers wait",
                "expedited orders", "standard orders", "high-volume customers", "low-priority orders",
                "couriers wait", "restaurants absorb delays", "drivers absorb idle time",
                "customers in dense areas", "customers in remote areas", "high-value customers",
                "low-value customers", "priority restaurants", "small restaurants",
                "fast-delivery zones", "slow-delivery zones", "orders are delayed for",
                "drivers bear fuel cost", "restaurants bear platform dependence",
                "customers pay surge fees", "platform prioritizes", "those who pay more",
                "well-behaved students", "students subject to bias", "rule-abiding students",
                "disciplined students", "students with less parental advocacy", "marginalized backgrounds",
                "compliant students", "flagged students", "repeat offenders", "arbitrary sanctions",
                "teachers gain order", "students absorb delay", "students absorb sanctions",
                "ordinary users are filtered", "flagged users face extra review",
                "platform operators benefit", "users absorb wrongful removal",
                "creators lose reach", "high-risk content is escalated", "ordinary posts are suppressed",
                "engagement is preserved for the platform", "moderators absorb overload",
                "drivers wait for matches", "riders get faster pickups",
                "surge-priced riders get priority", "drivers absorb idle time",
                "drivers bear fuel cost", "platform takes commission",
                "high-demand zones get priority", "remote riders wait longer",
                "drivers in low-demand areas wait", "customers pay surge fees",
                "platform prioritizes dense routes", "drivers absorb cancellation risk"
            ]),
            "pressure": self._contains_any(lower, [
                "pressure", "bottleneck", "backlog", "queue", "overload", "capacity",
                "ranking threshold", "review capacity", "quota pressure", "accumulation",
                "checkpoint", "secondary screening", "lane capacity", "scanner throughput",
                "staffing gaps", "screening delays", "line buildup", "wait times",
                "review load", "processing delay", "case load", "matching lag", "approval delay",
                "moderation queue", "appeals backlog", "intake backlog", "dispatch lag",
                "inventory buildup", "warehouse congestion", "staff shortage", "surge demand",
                "peak periods", "throughput constraint", "service delay", "decision queue"
            ]),
            "tradeoff": (
                self._contains_any(lower, [
                    "tradeoff", "trade-off", "at the cost of", "improves", "worsens",
                    "increases", "reduces", "preserves", "sacrifices",
                    "enhance", "enhances", "improve", "improved",
                    "reduce", "reduces", "reduced",
                    "but could", "but may", "while reducing", "while weakening"
                ])
                and (" but " in lower or " while " in lower or "at the cost of" in lower)
            ),
            "specificity": (
                self._contains_any(lower, [
                    "applicant", "admissions", "enrollment", "offer", "quota", "ranking", "review",
                    "triage", "patient", "nurse", "emergency department", "critical care",
                    "treatment pathway", "medical staff", "hospital capacity", "assessment",
                    "claims adjuster", "claim", "policyholder", "reimbursement",
                    "courier", "restaurant", "customer order", "dispatch",
                    "housing unit", "eligibility interview", "visa officer", "consular",
                    "moderation queue", "flagged post", "account suspension",
                    "intake officer", "classification", "cell assignment",
                    "picker", "inventory", "fulfillment", "warehouse",
                    "recruiter", "candidate", "interview loop", "shortlist",
                    "disciplinary referral", "suspension", "loan officer", "credit score",
                    "underwriting", "driver", "rider", "match rate",
                    "tsa", "precheck", "checkpoint", "x-ray", "pat-down", "boarding gate",
                    "secondary inspection", "airside", "sterile zone",
                    "housing authority", "waitlist", "voucher", "eligibility file",
                    "placement officer", "unit assignment", "tenant screening",
                    "public housing", "housing allocation", "housing unit", "applicant file",
                    "priority category", "income verification", "eligibility interview",
                    "subsidized unit", "family size", "residency requirement",
                    "content moderation", "moderation queue", "flagged post", "flagged content",
                    "account suspension", "community guidelines", "appeal review", "trust and safety",
                    "content reviewer", "automated detection", "ranking demotion", "shadow ban",
                    "policy enforcement", "removed post", "repeat violator", "creator reach"
                ])
                and not self._contains_any(lower, [
                    "set criteria and standards", "defined sequence", "external pressures",
                    "various factors", "plays a role", "helps manage", "can be seen as"
                ])
            ),
            "concreteness": (
                self._contains_any(lower, [
                    "officers", "committee", "reviewers", "nurses", "supervisors", "agents",
                    "adjusters", "moderators", "drivers", "riders", "couriers", "recruiters",
                    "loan officers", "tsa", "screeners", "students", "applicants", "patients",
                    "passengers", "tenants", "detainees", "inmates", "teachers", "staff",
                    "customers", "claimants", "dispatchers", "restaurants",
                    "hiring managers", "candidates", "interviewers", "hr", "recruitment team",
                    "claims examiners", "fraud investigators", "policyholders",
                    "recruiters", "applicants", "sourcers", "panel interviewers",
                    "principals", "deans", "teachers", "counselors", "students",
                    "visa officers", "consular officers", "applicants", "review clerks",
                    "immigration staff", "security reviewers",
                    "caseworker", "caseworkers", "benefits office", "eligibility worker",
                    "intake clerk", "intake clerks", "fraud detection unit", "fraud investigators",
                    "application form", "forms", "supporting documents", "documentation review",
                    "eligibility verification", "income threshold", "income thresholds",
                    "residency", "family status", "appeals process", "denial notice",
                    "it infrastructure", "processing backlog", "payment delay", "staff burnout"
                ])
                and self._contains_any(lower, [
                    "queue", "backlog", "bottleneck", "appeals", "waitlist", "secondary screening",
                    "ranking", "quota", "deadline", "checkpoint", "dispatch", "classification",
                    "underwriting", "shortlist", "suspension", "cell assignment", "missed flights",
                    "overtime", "re-review", "surge", "line length", "case load",
                    "matches", "assignments", "rerouted", "outages", "surge pricing",
                    "demand spikes", "service degradation", "pickup lag", "cancellations",
                    "claims queue", "claims backlog", "documentation review", "fraud review",
                    "interview loop", "resume screening", "candidate pipeline", "job requisition",
                    "approval queue", "processing lag", "screening stage", "offer stage",
                    "reference check", "interview scheduling",
                    "disciplinary referral", "incident report", "hearing", "suspension", "expulsion",
                    "visa queue", "consular interview", "security check", "background screening",
                    "document review", "processing window", "appointment slot", "administrative processing",
                    "application queue", "processing backlog", "benefit delay", "payment delay",
                    "eligibility verification", "documentation review", "income verification",
                    "residency verification", "recertification", "administrative hold",
                    "interview slot", "missing documents", "denial review"
                ])
                and self._contains_any(lower, [
                    "absorbs", "bears", "waits", "delayed", "rejected", "denied", "missed",
                    "excluded", "flagged", "deferred", "screened out", "removed", "overtime",
                    "uncertainty", "intrusive", "reopened", "appeals burden",
                    "idle time", "wait times", "deactivation", "degraded", "rerouted",
                    "cancellations", "unmatched", "failed matches",
                    "claim denial", "claim delay", "unpaid", "ghosted", "passed over",
                    "withdraws", "drops out", "lost wages", "offer rescinded",
                    "payment delay", "benefit suspension", "benefit cutoff", "denied benefits",
                    "administrative hold", "missing paperwork", "wrongful denial", "delayed disbursement",
                    "candidate drop-off", "passed over", "left waiting",
                    "suspended", "expelled", "disciplined", "sanctioned",
                    "visa refusal", "administrative delay", "stuck abroad", "missed travel",
                    "missed enrollment", "missed job start", "left in limbo"
                ])
            ),
        }

        weighted = self.validity_cfg["weighted_checks"]
        score = 0.0
        for key, weight in weighted.items():
            score += (1.0 if gates.get(key, False) else 0.0) * float(weight)

        drift_flags = {
            "moralizing_only": ("should" in lower or "ought" in lower) and not self._contains_any(lower, ["source", "sink", "maintenance", "control"]),
            "metaphoric_energy_only": "energy" in lower and not self._contains_any(lower, ["source", "sink", "path", "barrier"]),
            "missing_setup": not gates["setup"],
            "generic_template": not gates["specificity"],
            "missing_asymmetry": not gates["asymmetry"],
            "missing_pressure": not gates["pressure"],
            "missing_tradeoff": not gates["tradeoff"],
            "low_concreteness": not gates["concreteness"],
            "generic_language": self._contains_any(lower, [
                "institutional goals", "resource constraints", "operates within",
                "plays a role", "helps manage", "various factors", "can be seen as",
                "ensuring efficiency", "maintaining safety", "decision-makers",
                "authorities", "users", "stakeholders", "appropriate resources"
            ]),
        }

        hard_drift_keys = [
            "missing_setup",
            "missing_asymmetry",
            "missing_pressure",
            "missing_tradeoff",
            "low_concreteness",
        ]
        soft_drift_keys = [
            "moralizing_only",
            "metaphoric_energy_only",
            "generic_template",
            "generic_language",
        ]

        hard_drift_count = sum(1 for k in hard_drift_keys if drift_flags.get(k))
        soft_drift_count = sum(1 for k in soft_drift_keys if drift_flags.get(k))

        if score >= self.validity_cfg["thresholds"]["valid_ep"] and hard_drift_count == 0 and all(gates[g] for g in self.validity_cfg["mandatory_gates"]):
            label = "Valid EP"
        elif score >= self.validity_cfg["thresholds"]["weak_ep"]:
            label = "Weak EP" if hard_drift_count == 0 else "Drifted EP"
        else:
            label = "Pseudo-EP" if drift_flags["missing_setup"] else "Drifted EP"

        return {
            "label": label,
            "score": round(score, 3),
            "gates": gates,
            "drift_flags": drift_flags,
            "hard_drift_count": hard_drift_count,
            "soft_drift_count": soft_drift_count,
            "mandatory_pass": all(gates[g] for g in self.validity_cfg["mandatory_gates"]),
        }
