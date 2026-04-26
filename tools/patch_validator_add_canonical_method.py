from pathlib import Path

p = Path("app/services/validator.py")
text = p.read_text()

anchor = """    def _contains_any(self, text: str, terms: list[str]) -> bool:
        return any(term in text for term in terms)
"""

insert = """    def _contains_any(self, text: str, terms: list[str]) -> bool:
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
            "setup": (
                self._is_specified(canonical.get("system"))
                and all(self._is_specified(flow.get(k)) for k in ["source", "sink", "gradient", "path"])
                and all(self._is_specified(constraints.get(k)) for k in ["barrier", "loss"])
            ),
            "maintenance": self._is_specified(constraints.get("maintenance")),
            "control": self._is_specified(constraints.get("control")),
            "fragility": self._is_specified(constraints.get("fragility")),
            "asymmetry": self._is_specified(commitments.get("asymmetry")),
            "pressure": self._is_specified(commitments.get("pressure_point")),
            "tradeoff": self._is_specified(commitments.get("tradeoff")),
            "specificity": (
                self._is_specified(canonical.get("system"))
                and any(self._is_specified(flow.get(k)) for k in ["source", "sink", "path"])
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
            "moralizing_only": False,
            "metaphoric_energy_only": False,
            "missing_setup": not gates["setup"],
            "generic_template": False,
            "missing_asymmetry": not gates["asymmetry"],
            "missing_pressure": not gates["pressure"],
            "missing_tradeoff": not gates["tradeoff"],
            "low_concreteness": not gates["concreteness"],
            "generic_language": False,
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
"""

if anchor not in text:
    raise SystemExit("anchor not found")

if "def validate_canonical(self, canonical: Dict[str, Any])" in text:
    raise SystemExit("validate_canonical already present")

text = text.replace(anchor, insert, 1)
p.write_text(text)
print("patched", p)
