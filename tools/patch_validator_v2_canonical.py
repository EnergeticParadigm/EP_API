from pathlib import Path

p = Path("app/services/validator.py")
text = p.read_text()

anchor = "from typing import Any, Dict"
if anchor in text and "_score_canonical_setup" not in text:
    text = text.replace(
        anchor,
        anchor + '''

def _is_specified(v):
    if v is None:
        return False
    if isinstance(v, str):
        s = v.strip().upper()
        return s != "" and s != "UNSPECIFIED"
    if isinstance(v, (list, dict, tuple, set)):
        return len(v) > 0
    return True

def _score_canonical_setup(canonical: Dict[str, Any]) -> Dict[str, Any]:
    flow = canonical.get("flow_objects", {}) or {}
    cons = canonical.get("constraint_objects", {}) or {}
    sc = canonical.get("structural_commitments", {}) or {}

    gates = {
        "setup": _is_specified(canonical.get("system")),
        "maintenance": _is_specified(cons.get("maintenance")),
        "control": _is_specified(cons.get("control")),
        "fragility": _is_specified(cons.get("fragility")),
        "asymmetry": _is_specified(sc.get("asymmetry")),
        "pressure": _is_specified(sc.get("pressure_point")),
        "tradeoff": _is_specified(sc.get("tradeoff")),
        "specificity": any(_is_specified(flow.get(k)) for k in ("source","sink","path")),
        "concreteness": any(_is_specified(cons.get(k)) for k in ("barrier","loss")),
    }

    weights = {
        "setup": 0.18,
        "maintenance": 0.10,
        "control": 0.10,
        "fragility": 0.10,
        "asymmetry": 0.12,
        "pressure": 0.10,
        "tradeoff": 0.12,
        "specificity": 0.08,
        "concreteness": 0.10,
    }

    score = round(sum(weights[k] for k,v in gates.items() if v), 2)
    mandatory_pass = all(gates[k] for k in ["setup","maintenance","control","fragility"])

    if mandatory_pass and score >= 0.85:
        label = "Valid EP"
    elif score >= 0.60:
        label = "Drifted EP"
    else:
        label = "Weak EP"

    return {
        "label": label,
        "score": score,
        "gates": gates,
        "mandatory_pass": mandatory_pass,
        "source": "canonical_setup",
    }
'''
    )

old = """def validate_ep_response(payload: Dict[str, Any]) -> Dict[str, Any]:
"""
new = """def validate_ep_response(payload: Dict[str, Any]) -> Dict[str, Any]:
    canonical = payload.get("canonical_setup")
    if isinstance(canonical, dict) and canonical:
        return _score_canonical_setup(canonical)

"""
if old in text:
    text = text.replace(old, new, 1)
else:
    raise SystemExit("validate_ep_response function not found")

p.write_text(text)
print("patched", p)
