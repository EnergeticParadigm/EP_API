from pathlib import Path

p = Path("app/services/epra.py")
text = p.read_text()

old = """    return {
        "compact_ep_setup": setup,
        "analysis": analysis_text,
        "analysis_sections": analysis_sections,
    }
"""

new = """    canonical = {
        "system": setup["system"],
        "flow_objects": {
            "source": setup["source"],
            "sink": setup["sink"],
            "gradient": setup["gradient"],
            "path": setup["path"],
        },
        "constraint_objects": {
            "barrier": setup["barrier"],
            "loss": setup["loss"],
            "maintenance": setup["maintenance"],
            "control": setup["control"],
            "fragility": setup["fragility"],
        },
        "structural_commitments": {
            "asymmetry": "UNSPECIFIED",
            "pressure_point": "UNSPECIFIED",
            "tradeoff": "UNSPECIFIED",
            "actors": [],
            "cost_bearer": "UNSPECIFIED",
            "fracture_condition": "UNSPECIFIED",
        },
    }

    return {
        "compact_ep_setup": setup,
        "canonical_setup": canonical,
        "analysis": analysis_text,
        "analysis_sections": analysis_sections,
    }
"""

if old not in text:
    raise SystemExit("target return block not found in _normalize_payload")

text = text.replace(old, new, 1)
p.write_text(text)
print("patched", p)
