from pathlib import Path

p = Path("app/services/epra.py")
text = p.read_text()

old = '''def _render_analysis_from_structure(s):
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

new = '''def _render_analysis_from_structure(s):
    if "flow_objects" in s or "constraint_objects" in s or "structural_commitments" in s:
        system = s.get("system", "the target system")
        flow = s.get("flow_objects", {}) or {}
        constraints = s.get("constraint_objects", {}) or {}
        commitments = s.get("structural_commitments", {}) or {}

        source = flow.get("source", "inputs")
        sink = flow.get("sink", "outputs")
        gradient = flow.get("gradient", "selection pressure")
        path = flow.get("path", "processing route")

        barrier = constraints.get("barrier", "gates")
        loss = constraints.get("loss", "drop-off")
        maintenance = constraints.get("maintenance", "upkeep")
        control = constraints.get("control", "enforcement")
        fragility = constraints.get("fragility", "breakdown pressure")

        asymmetry = commitments.get("asymmetry", "the system advantages some actors while others absorb delay or exclusion")
        pressure_point = commitments.get("pressure_point", "a bottleneck in the flow")
        tradeoff = commitments.get("tradeoff", "stability for some comes at a cost to others")
        cost_bearer = commitments.get("cost_bearer", "the actors pushed to absorb delay, burden, or exclusion")
        fracture_condition = commitments.get("fracture_condition", fragility)

        actors = commitments.get("actors", []) or []
        actor_text = ", ".join(actors) if actors else "the actors inside the system"

        return {
            "core_reading": (
                f"The {system} converts {source} into {sink}, but it does so by forcing movement through "
                f"{gradient} rather than by neutral processing. What looks administrative is actually selective: "
                f"{asymmetry}."
            ),
            "how_the_system_works": (
                f"Pressure enters through {source} and is routed along {path}. The choke point sits at {barrier}, "
                f"with pressure accumulating at {pressure_point}. Loss is not accidental here: {loss}. "
                f"The main actors are {actor_text}, and the system keeps legibility by making {cost_bearer} absorb the burden."
            ),
            "maintenance_control_fragility": (
                f"The system stays upright through {maintenance}, while {control} supplies the authority to escalate, "
                f"screen out, or override. Its tradeoff is explicit: {tradeoff}. "
                f"It fractures when {fracture_condition}, at which point the hidden bargain fails and the burden becomes visible."
            ),
        }

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

if old not in text:
    raise SystemExit("renderer block not found")

text = text.replace(old, new, 1)

old2 = '''        payload = _normalize_payload(payload, runtime=runtime)
        payload["analysis"] = _render_analysis_from_structure(payload["compact_ep_setup"])
        payload = _fill_structural_commitments(payload)
        return payload
'''

new2 = '''        payload = _normalize_payload(payload, runtime=runtime)
        payload = _fill_structural_commitments(payload)
        payload["analysis"] = _render_analysis_from_structure(payload["canonical_setup"])
        return payload
'''

if old2 not in text:
    raise SystemExit("structure extraction render block not found")

text = text.replace(old2, new2, 1)

p.write_text(text)
print("patched", p)
