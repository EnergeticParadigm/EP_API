from pathlib import Path

p = Path("app/services/epra.py")
text = p.read_text()

start_marker = "def _render_analysis_from_structure(s):"
end_marker = "\ndef _extract_json_object"

start = text.find(start_marker)
if start == -1:
    raise SystemExit("start marker not found")

end = text.find(end_marker, start)
if end == -1:
    raise SystemExit("end marker not found")

replacement = '''def _render_analysis_from_structure(s):
    system = s.get("system", "the target system")
    source = s.get("source", "inputs")
    sink = s.get("sink", "outputs")
    gradient = s.get("gradient", "selection pressure")
    path = s.get("path", "processing route")
    barrier = s.get("barrier", "gates")
    loss = s.get("loss", "drop-off")
    maintenance = s.get("maintenance", "upkeep")
    control = s.get("control", "enforcement")
    fragility = s.get("fragility", "breakdown pressure")

    return {
        "core_reading": (
            f"The {system} converts {source} into {sink}, but it does so by forcing movement through "
            f"{gradient} rather than by neutral processing. What looks administrative is actually selective: "
            f"flow is narrowed, delayed, or expelled until only a controlled output reaches {sink}."
        ),
        "how_the_system_works": (
            f"Pressure enters through {source} and is routed along {path}. The choke point sits at {barrier}, "
            f"where the system decides who passes cleanly and who absorbs delay, rejection, or uncertainty. "
            f"Loss is not accidental here: {loss} is the price paid to keep throughput legible and controllable."
        ),
        "maintenance_control_fragility": (
            f"The system stays upright through {maintenance}, while {control} supplies the authority to escalate, "
            f"screen out, or override. Its fracture line appears when {fragility}: then the hidden bargain fails, "
            f"and the burden the system normally spreads quietly becomes visible as backlog, exclusion, or breakdown."
        ),
    }
'''

text2 = text[:start] + replacement + text[end:]
p.write_text(text2)
print("patched", p)
