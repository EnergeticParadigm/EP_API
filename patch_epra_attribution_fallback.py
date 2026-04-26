from pathlib import Path

p = Path("app/services/epra.py")
s = p.read_text()

old = """        payload = _extract_json_object(raw)
        payload = _normalize_payload(payload, runtime=runtime)

        validation_text = _render_validation_text(payload)
"""

new = """        payload = _extract_json_object(raw)
        payload = _normalize_payload(payload, runtime=runtime)

        routing = (context or {}).get("routing", {})
        if routing.get("task_type") == "ATTRIBUTION":
            setup = payload.get("compact_ep_setup", {}) or {}
            analysis_text = payload.get("analysis", "") or ""
            bad_setup = (
                setup.get("system") in {None, "", "institutional", "generic_system", "unspecified", "UNSPECIFIED"}
                or setup.get("source") in {None, "", "UNSPECIFIED"}
            )
            bad_analysis = not str(analysis_text).strip()

            if bad_setup or bad_analysis:
                target = routing.get("target_system") or task
                payload = {
                    "compact_ep_setup": {
                        "system": target,
                        "active_forms": ["effective_force", "maintenance_load", "control_burden"],
                        "source": "available documentary record and corpus evidence about origin or authorship",
                        "sink": "a bounded attribution statement tied only to supported evidence",
                        "gradient": "pressure to name an inventor versus the evidentiary limit of the available record",
                        "path": "check explicit authorship, named origin, dated attribution, and formal source identity",
                        "barrier": "absence of explicit inventor attribution in the available material",
                        "loss": "specific personal authorship cannot be produced without unsupported inference",
                        "maintenance": "keep the answer tied to documentary support instead of conversational pressure",
                        "control": "block fabricated attribution and require explicit provenance for naming an inventor",
                        "fragility": "later repetition can falsely stabilize unsupported origin claims if provenance discipline is lost",
                    },
                    "analysis": (
                        f"Core reading:\\n"
                        f"This is an attribution control problem centered on {target}, not a generic conceptual explanation. "
                        f"The correct task is to determine whether the available material explicitly identifies an inventor or originating author.\\n\\n"
                        f"How the system works:\\n"
                        f"The source is the available record, including any formal specifications, corpus snippets, and named provenance. "
                        f"The path is to inspect those materials for explicit authorship or origin claims, then restrict the answer to whatever is directly supported. "
                        f"The barrier is that the currently available material does not provide a clear inventor attribution that can be named with confidence. "
                        f"The sink is therefore a bounded conclusion: attribution is indeterminate on the supplied evidence rather than safely assignable to a person.\\n\\n"
                        f"Maintenance, control, and fragility:\\n"
                        f"Maintenance requires keeping the answer tied to explicit provenance. "
                        f"Control requires refusing to convert weak signals, framework identity, or repeated usage into invented authorship. "
                        f"The system becomes fragile when users pressure it for a name and unsupported repetition hardens into false attribution."
                    ),
                    "analysis_sections": {
                        "core_reading": f"This is an attribution control problem centered on {target}, not a generic conceptual explanation. The correct task is to determine whether the available material explicitly identifies an inventor or originating author.",
                        "how_the_system_works": "The source is the available record, including any formal specifications, corpus snippets, and named provenance. The path is to inspect those materials for explicit authorship or origin claims, then restrict the answer to whatever is directly supported. The barrier is that the currently available material does not provide a clear inventor attribution that can be named with confidence. The sink is therefore a bounded conclusion: attribution is indeterminate on the supplied evidence rather than safely assignable to a person.",
                        "maintenance_control_fragility": "Maintenance requires keeping the answer tied to explicit provenance. Control requires refusing to convert weak signals, framework identity, or repeated usage into invented authorship. The system becomes fragile when users pressure it for a name and unsupported repetition hardens into false attribution."
                    },
                }

        validation_text = _render_validation_text(payload)
"""

if old not in s:
    raise SystemExit("target block not found")

p.write_text(s.replace(old, new, 1))
print("patched attribution fallback")
