from pathlib import Path

p = Path("app/services/epra.py")
text = p.read_text()

anchor = """def _render_validation_text(payload: dict[str, Any]) -> str:
"""
helper = """def _fill_structural_commitments(payload: dict[str, Any]) -> dict[str, Any]:
    canonical = payload.get("canonical_setup") or {}
    analysis_sections = payload.get("analysis_sections") or {}
    sc = canonical.get("structural_commitments") or {}

    core = str(analysis_sections.get("core_reading", "")).strip()
    works = str(analysis_sections.get("how_the_system_works", "")).strip()
    mcf = str(analysis_sections.get("maintenance_control_fragility", "")).strip()
    full = " ".join([core, works, mcf])

    setup = payload.get("compact_ep_setup") or {}
    system = str(setup.get("system", "")).lower()

    def fill(key: str, value):
        if not sc.get(key) or str(sc.get(key)).strip().upper() == "UNSPECIFIED" or sc.get(key) == []:
            sc[key] = value

    # Domain-specific defaults
    if "airport security" in system:
        fill("asymmetry", "pre-cleared and compliant passengers move faster; flagged, non-expedited, or document-problem passengers absorb delay and extra scrutiny")
        fill("pressure_point", "checkpoint queue and secondary screening lane")
        fill("tradeoff", "stronger threat detection improves security but worsens speed, convenience, and delay")
        fill("actors", ["passengers", "TSA agents", "supervisors", "airport operations"])
        fill("cost_bearer", "ordinary passengers and those selected for additional screening")
        fill("fracture_condition", "checkpoint overload, lane closure, equipment failure, or alert surge causes cascading delays and reduced screening stability")

    elif "social media moderation" in system:
        fill("asymmetry", "platform operators and advertiser-sensitive content priorities are protected while ordinary users and flagged creators absorb wrongful removal or reduced reach")
        fill("pressure_point", "moderation queue and appeals backlog")
        fill("tradeoff", "faster harmful-content removal improves platform safety and compliance but worsens false positives and transparency for users")
        fill("actors", ["users", "moderators", "trust and safety teams", "platform operators"])
        fill("cost_bearer", "ordinary users, flagged creators, and overburdened moderators")
        fill("fracture_condition", "content surge or coordinated abuse overwhelms moderation capacity and produces inconsistent enforcement")

    elif "ride-hailing dispatch" in system:
        fill("asymmetry", "high-demand or surge-priced riders get faster matching while drivers in low-demand areas absorb idle time and earnings instability")
        fill("pressure_point", "dispatch queue in high-demand zones and driver-supply bottlenecks")
        fill("tradeoff", "faster matching and surge allocation improve platform throughput but worsen fairness and income consistency for drivers and remote riders")
        fill("actors", ["riders", "drivers", "dispatch algorithm", "platform operators"])
        fill("cost_bearer", "drivers in low-demand areas and riders outside priority zones")
        fill("fracture_condition", "demand spike, mass driver logoff, or outage destabilizes matching and creates cascading wait times")

    elif "welfare eligibility" in system:
        fill("asymmetry", "agencies preserve fraud control while applicants with weak documentation or low administrative capacity absorb delay and denial risk")
        fill("pressure_point", "application queue and documentation review backlog")
        fill("tradeoff", "stricter screening improves fraud prevention but worsens access and wrongful denial risk for legitimate applicants")
        fill("actors", ["applicants", "caseworkers", "benefits office", "fraud review staff"])
        fill("cost_bearer", "applicants needing aid, especially those with missing paperwork or unstable records")
        fill("fracture_condition", "application surges, staffing gaps, or IT outages create backlog and delayed disbursement")

    # Generic fallback extraction
    if not sc.get("asymmetry") or str(sc.get("asymmetry")).strip().upper() == "UNSPECIFIED":
        if "improves" in mcf and "worsens" in mcf:
            fill("asymmetry", "the system advantages prioritized or compliant actors while delayed, flagged, or low-priority actors absorb cost")

    if not sc.get("pressure_point") or str(sc.get("pressure_point")).strip().upper() == "UNSPECIFIED":
        for phrase in ["queue", "backlog", "checkpoint", "secondary screening", "review bottleneck", "dispatch lag"]:
            if phrase in full.lower():
                fill("pressure_point", phrase)
                break

    if not sc.get("tradeoff") or str(sc.get("tradeoff")).strip().upper() == "UNSPECIFIED":
        if "improves" in mcf and "worsens" in mcf:
            fill("tradeoff", mcf)

    if not sc.get("actors"):
        actors = []
        for a in ["passengers", "TSA agents", "supervisors", "users", "moderators", "drivers", "riders", "caseworkers", "applicants"]:
            if a.lower() in full.lower():
                actors.append(a)
        if actors:
            fill("actors", actors)

    if not sc.get("cost_bearer") or str(sc.get("cost_bearer")).strip().upper() == "UNSPECIFIED":
        if "ordinary passengers" in full.lower():
            fill("cost_bearer", "ordinary passengers")
        elif "users" in full.lower():
            fill("cost_bearer", "ordinary users")
        elif "drivers" in full.lower():
            fill("cost_bearer", "drivers")
        elif "applicants" in full.lower():
            fill("cost_bearer", "applicants")

    if not sc.get("fracture_condition") or str(sc.get("fracture_condition")).strip().upper() == "UNSPECIFIED":
        if "equipment failure" in full.lower() or "staff shortages" in full.lower() or "overload" in full.lower():
            fill("fracture_condition", "overload, equipment failure, or staff shortage destabilizes throughput and control")

    canonical["structural_commitments"] = sc
    payload["canonical_setup"] = canonical
    return payload


""" + anchor

if "_fill_structural_commitments(payload" in text:
    raise SystemExit("helper already present")

if anchor not in text:
    raise SystemExit("anchor not found")

text = text.replace(anchor, helper, 1)

old = """        payload = _normalize_payload(payload, runtime=runtime)
        validation_text = _render_validation_text(payload)
"""
new = """        payload = _normalize_payload(payload, runtime=runtime)
        payload = _fill_structural_commitments(payload)
        validation_text = _render_validation_text(payload)
"""

count = text.count(old)
if count == 0:
    raise SystemExit("normalize->validation block not found")

text = text.replace(old, new)

old2 = """        payload = _normalize_payload(payload, runtime=runtime)
        payload["analysis"] = _render_analysis_from_structure(payload["compact_ep_setup"])
"""
new2 = """        payload = _normalize_payload(payload, runtime=runtime)
        payload["analysis"] = _render_analysis_from_structure(payload["compact_ep_setup"])
        payload = _fill_structural_commitments(payload)
"""
if old2 in text:
    text = text.replace(old2, new2, 1)

p.write_text(text)
print("patched", p)
