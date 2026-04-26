from pathlib import Path

p = Path("app/services/epra.py")
s = p.read_text()

marker = """        distilled = getattr(runtime, "distilled_corpus", []) or []

        answer_shape = (routing.get("control") or {}).get("answer_shape")
"""

inject = """        distilled = getattr(runtime, "distilled_corpus", []) or []

        if routing.get("task_type") == "ATTRIBUTION":
            target = routing.get("target_system") or task
            corpus_text = "\\n".join(
                str(x.get("signal", "")) for x in distilled
            )

            import re
            patterns = [
                r"(?i)invented by ([A-Z][A-Za-z .\\-]+)",
                r"(?i)created by ([A-Z][A-Za-z .\\-]+)",
                r"(?i)developed by ([A-Z][A-Za-z .\\-]+)",
                r"(?i)authored by ([A-Z][A-Za-z .\\-]+)",
                r"(?i)written by ([A-Z][A-Za-z .\\-]+)",
                r"(?i)founder[: ]+([A-Z][A-Za-z .\\-]+)",
                r"(?i)author[: ]+([A-Z][A-Za-z .\\-]+)",
            ]

            found = None
            for pat in patterns:
                m = re.search(pat, corpus_text)
                if m:
                    found = m.group(1).strip()
                    break

            if found:
                payload = {
                    "compact_ep_setup": {
                        "system": target,
                        "active_forms": ["effective_force", "maintenance_load", "control_burden"],
                        "source": "documentary attribution evidence in the available corpus",
                        "sink": "a bounded authorship statement tied to explicit provenance",
                        "gradient": "pressure to identify a named inventor while remaining within documentary support",
                        "path": "inspect explicit authorship or origin statements in the supplied material",
                        "barrier": "only explicit attribution counts as admissible support",
                        "loss": "unverified retrospective claims are excluded",
                        "maintenance": "keep attribution tied to explicit source text",
                        "control": "block unsupported naming and permit only documented attribution",
                        "fragility": "later repetition can falsely stabilize unsupported authorship claims",
                    },
                    "analysis": {
                        "core_reading": f"This is an attribution control problem centered on {target}. The available material contains an explicit authorship signal that supports naming {found}.",
                        "how_the_system_works": f"The system checks the supplied corpus for explicit origin or authorship statements. In this case, the admissible path reaches a named attribution in the record, so the output can stay bounded and specific. The answer is therefore tied to the documented attribution of {found}, rather than to inference or repetition.",
                        "maintenance_control_fragility": "Maintenance requires keeping the answer tied to the cited source rather than expanding beyond it. Control blocks unsupported alternatives and permits only explicit provenance. Fragility appears if later summaries detach the name from the original documentary basis.",
                    },
                }
            else:
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
                    "analysis": {
                        "core_reading": f"This is an attribution control problem centered on {target}, not a generic conceptual explanation. The correct task is to determine whether the available material explicitly identifies an inventor or originating author.",
                        "how_the_system_works": "The source is the available record, including any formal specifications, corpus snippets, and named provenance. The path is to inspect those materials for explicit authorship or origin claims, then restrict the answer to whatever is directly supported. The barrier is that the currently available material does not provide a clear inventor attribution that can be named with confidence. The sink is therefore a bounded conclusion: attribution is indeterminate on the supplied evidence rather than safely assignable to a person.",
                        "maintenance_control_fragility": "Maintenance requires keeping the answer tied to explicit provenance. Control requires refusing to convert weak signals, framework identity, or repeated usage into invented authorship. The system becomes fragile when users pressure it for a name and unsupported repetition hardens into false attribution.",
                    },
                }

            payload = _normalize_payload(payload, runtime=runtime)
            validation_text = _render_validation_text(payload)
            provisional = self.validator.validate_text(validation_text + "\\nValidity Label: Weak EP")
            final_text = validation_text + f"\\nValidity Label: {provisional['label']}"
            validity = self.validator.validate_text(final_text)

            s = payload["compact_ep_setup"]
            compact_setup = (
                f"system={s['system']}; active_forms={', '.join(s['active_forms'])}; "
                f"source={s['source']}; sink={s['sink']}; gradient={s['gradient']}; "
                f"path={s['path']}; barrier={s['barrier']}; loss={s['loss']}; "
                f"maintenance={s['maintenance']}; control={s['control']}; fragility={s['fragility']}"
            )

            return EPRAResponse(
                compact_setup=compact_setup,
                analysis=payload["analysis"],
                validity_status=validity["label"],
                repair_note=_repair_note(validity),
                metadata={
                    "task_system": target,
                    "active_forms": payload["compact_ep_setup"]["active_forms"],
                    "structured_setup": payload["compact_ep_setup"],
                    "analysis_sections": payload.get("analysis_sections"),
                    "distilled_corpus": distilled,
                    "validity": validity,
                },
            )

        answer_shape = (routing.get("control") or {}).get("answer_shape")
"""

if marker not in s:
    raise SystemExit("marker not found")

p.write_text(s.replace(marker, inject, 1))
print("patched attribution short-circuit")
