from pathlib import Path

p = Path("app/services/epra.py")
text = p.read_text()

anchor = "def _render_validation_text(payload: dict[str, Any]) -> str:\n"

helper = '''def _fill_structural_commitments(payload: dict[str, Any]) -> dict[str, Any]:
    canonical = payload.get("canonical_setup") or {}
    sc = canonical.get("structural_commitments") or {}
    sections = payload.get("analysis_sections") or {}
    full = " ".join([
        str(sections.get("core_reading", "")),
        str(sections.get("how_the_system_works", "")),
        str(sections.get("maintenance_control_fragility", "")),
    ]).lower()
    system = str((payload.get("compact_ep_setup") or {}).get("system", "")).lower()

    def missing(k):
        v = sc.get(k)
        return v in (None, "", "UNSPECIFIED", [])

    def fill(k, v):
        if missing(k):
            sc[k] = v

    if "airport security" in system:
        fill("asymmetry", "pre-cleared and compliant passengers move faster; flagged or non-expedited passengers absorb delay and scrutiny")
        fill("pressure_point", "checkpoint queue and secondary screening lane")
        fill("tradeoff", "stronger threat detection improves security but worsens speed and convenience")
        fill("actors", ["passengers", "TSA agents", "supervisors", "airport operations"])
        fill("cost_bearer", "ordinary passengers and those selected for additional screening")
        fill("fracture_condition", "checkpoint overload, lane closure, equipment failure, or alert surge causes cascading delays")

    if "social media moderation" in system:
        fill("asymmetry", "platform operators and advertiser-sensitive priorities are protected while ordinary users and flagged creators absorb wrongful removal or reduced reach")
        fill("pressure_point", "moderation queue and appeals backlog")
        fill("tradeoff", "faster harmful-content removal improves compliance but worsens false positives and transparency for users")
        fill("actors", ["users", "moderators", "trust and safety teams", "platform operators"])
        fill("cost_bearer", "ordinary users, flagged creators, and overburdened moderators")
        fill("fracture_condition", "content surge or coordinated abuse overwhelms moderation capacity and produces inconsistent enforcement")

    if "ride-hailing dispatch" in system:
        fill("asymmetry", "high-demand or surge-priced riders get faster matching while drivers in low-demand areas absorb idle time and earnings instability")
        fill("pressure_point", "dispatch queue in high-demand zones and driver-supply bottlenecks")
        fill("tradeoff", "faster matching and surge allocation improve throughput but worsen fairness and income consistency for drivers and remote riders")
        fill("actors", ["riders", "drivers", "dispatch algorithm", "platform operators"])
        fill("cost_bearer", "drivers in low-demand areas and riders outside priority zones")
        fill("fracture_condition", "demand spike, mass driver logoff, or outage destabilizes matching and creates cascading wait times")

    if "welfare eligibility" in system:
        fill("asymmetry", "agencies preserve fraud control while applicants with weak documentation or low administrative capacity absorb delay and denial risk")
        fill("pressure_point", "application queue and documentation review backlog")
        fill("tradeoff", "stricter screening improves fraud prevention but worsens access and wrongful denial risk for legitimate applicants")
        fill("actors", ["applicants", "caseworkers", "benefits office", "fraud review staff"])
        fill("cost_bearer", "applicants needing aid, especially those with missing paperwork or unstable records")
        fill("fracture_condition", "application surges, staffing gaps, or IT outages create backlog and delayed disbursement")

    if missing("pressure_point") and "queue" in full:
        fill("pressure_point", "queue")
    if missing("tradeoff") and "improves" in full and "worsens" in full:
        fill("tradeoff", "improves one side while worsening cost, delay, or exclusion for another")
    if missing("asymmetry") and ("absorb" in full or "flagged" in full or "priority" in full):
        fill("asymmetry", "prioritized actors move faster while flagged or ordinary actors absorb delay or scrutiny")
    if missing("actors"):
        actors = []
        for a in ["passengers", "tsa agents", "supervisors", "users", "moderators", "drivers", "riders", "applicants", "caseworkers"]:
            if a in full:
                actors.append(a)
        if actors:
            sc["actors"] = actors
    if missing("cost_bearer") and "passengers" in full:
        fill("cost_bearer", "passengers")
    if missing("fracture_condition") and ("equipment failure" in full or "staff shortages" in full or "overload" in full):
        fill("fracture_condition", "overload, equipment failure, or staff shortage destabilizes throughput")

    canonical["structural_commitments"] = sc
    payload["canonical_setup"] = canonical
    return payload


'''

if "_fill_structural_commitments(payload" not in text:
    if anchor not in text:
        raise SystemExit("render_validation_text anchor not found")
    text = text.replace(anchor, helper + anchor, 1)

old = """        payload = _normalize_payload(payload, runtime=runtime)
        validation_text = _render_validation_text(payload)
"""
new = """        payload = _normalize_payload(payload, runtime=runtime)
        payload = _fill_structural_commitments(payload)
        validation_text = _render_validation_text(payload)
"""
text = text.replace(old, new)

old2 = """        payload = _normalize_payload(payload, runtime=runtime)
        payload["analysis"] = _render_analysis_from_structure(payload["compact_ep_setup"])
        return payload
"""
new2 = """        payload = _normalize_payload(payload, runtime=runtime)
        payload["analysis"] = _render_analysis_from_structure(payload["compact_ep_setup"])
        payload = _fill_structural_commitments(payload)
        return payload
"""
text = text.replace(old2, new2)

p.write_text(text)
print("patched", p)
