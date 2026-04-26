from pathlib import Path

p = Path("app/services/epra.py")
s = p.read_text()

old = """        distilled = getattr(runtime, "distilled_corpus", []) or []

        if routing.get("task_type") == "ATTRIBUTION":
"""

new = """        distilled = getattr(runtime, "distilled_corpus", []) or []

        answer_shape = (routing.get("control") or {}).get("answer_shape")
        target = routing.get("target_system") or task

        if answer_shape == "clarify_first":
            payload = {
                "compact_ep_setup": {
                    "system": target,
                    "active_forms": ["effective_force", "maintenance_load", "control_burden"],
                    "source": "underspecified user prompt",
                    "sink": "a clarified target and answerable scope",
                    "gradient": "pressure to answer quickly despite missing scope",
                    "path": "ask for the specific conflict, timeframe, or angle before analysis",
                    "barrier": "prompt is too short or ambiguous to support a stable reading",
                    "loss": "premature answering causes target drift and false specificity",
                    "maintenance": "hold the target steady until scope is clarified",
                    "control": "require clarification before committing to a full analysis",
                    "fragility": "short prompts can be overread into the wrong conflict or frame",
                },
                "analysis": {
                    "core_reading": f"Direct answer: the prompt '{target}' is too underspecified for a stable answer.",
                    "how_the_system_works": "The safe path is to clarify what exact system, conflict, period, or angle is intended before producing a full EP reading.",
                    "maintenance_control_fragility": "Maintenance requires delaying commitment. Control requires asking a clarifying question instead of inventing scope. Fragility appears when a short prompt is expanded into the wrong target."
                },
            }
            payload = _normalize_payload(payload, runtime=runtime)
            validation_text = _render_validation_text(payload)
            provisional = self.validator.validate_text(validation_text + "\\nValidity Label: Weak EP")
            final_text = validation_text + f"\\nValidity Label: {provisional['label']}"
            validity = self.validator.validate_text(final_text)

            s0 = payload["compact_ep_setup"]
            compact_setup = (
                f"system={s0['system']}; active_forms={', '.join(s0['active_forms'])}; "
                f"source={s0['source']}; sink={s0['sink']}; gradient={s0['gradient']}; "
                f"path={s0['path']}; barrier={s0['barrier']}; loss={s0['loss']}; "
                f"maintenance={s0['maintenance']}; control={s0['control']}; fragility={s0['fragility']}"
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

        if answer_shape == "direct_only":
            payload = {
                "compact_ep_setup": {
                    "system": target,
                    "active_forms": ["effective_force", "maintenance_load", "control_burden"],
                    "source": "the named target system",
                    "sink": "one bounded direct answer",
                    "gradient": "pressure to answer the yes/no or factual question directly",
                    "path": "give the shortest bounded answer supported by the target as asked",
                    "barrier": "do not drift into a full EP essay",
                    "loss": "over-expansion weakens answer precision",
                    "maintenance": "keep the answer short and target-bound",
                    "control": "answer directly before any supporting analysis",
                    "fragility": "generic expansion can obscure the actual answer",
                },
                "analysis": {
                    "core_reading": f"Direct answer: respond directly about {target}, not with a full EP essay.",
                    "how_the_system_works": "This route is for a bounded direct answer. Keep the target fixed and answer the question concisely.",
                    "maintenance_control_fragility": "Maintenance requires brevity. Control blocks drift into unnecessary structure. Fragility appears when the system over-explains instead of answering."
                },
            }
            payload = _normalize_payload(payload, runtime=runtime)
            validation_text = _render_validation_text(payload)
            provisional = self.validator.validate_text(validation_text + "\\nValidity Label: Weak EP")
            final_text = validation_text + f"\\nValidity Label: {provisional['label']}"
            validity = self.validator.validate_text(final_text)

            s0 = payload["compact_ep_setup"]
            compact_setup = (
                f"system={s0['system']}; active_forms={', '.join(s0['active_forms'])}; "
                f"source={s0['source']}; sink={s0['sink']}; gradient={s0['gradient']}; "
                f"path={s0['path']}; barrier={s0['barrier']}; loss={s0['loss']}; "
                f"maintenance={s0['maintenance']}; control={s0['control']}; fragility={s0['fragility']}"
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

        if answer_shape == "direct_then_ep":
            runtime.task_system = target

        if routing.get("task_type") == "ATTRIBUTION":
"""

if old not in s:
    raise SystemExit("target insertion point not found")

s = s.replace(old, new, 1)

old2 = """        routed_task = (
            f"TASK: {task}\\n"
            f"ROUTING_MODE: {routing.get('mode')}\\n"
            f"TASK_TYPE: {routing.get('task_type')}\\n"
            f"TARGET_SYSTEM: {routing.get('target_system')}\\n"
            f"NEEDS_CLARIFICATION: {routing.get('needs_clarification')}\\n"
            f"CONTROL_POLICY: {routing.get('control')}\\n"
            f"ANSWER_SHAPE: {answer_shape}\\n"
            f"HARD_RULE: Do not change the target system.\\n"
            f"HARD_RULE: Follow the routed task type.\\n"
            f"HARD_RULE: If TASK_TYPE is ATTRIBUTION, identify supported attribution if present; otherwise explicitly state attribution is indeterminate, unsupported, or contested.\\n"
            f"HARD_RULE: If TASK_TYPE is ATTRIBUTION, do not replace attribution with a general conceptual explanation.\\n"
            f"HARD_RULE: If ANSWER_SHAPE is direct, answer concisely and directly.\\n"
        )
"""

new2 = """        routed_task = (
            f"TASK: {task}\\n"
            f"ROUTING_MODE: {routing.get('mode')}\\n"
            f"TASK_TYPE: {routing.get('task_type')}\\n"
            f"TARGET_SYSTEM: {routing.get('target_system')}\\n"
            f"NEEDS_CLARIFICATION: {routing.get('needs_clarification')}\\n"
            f"CONTROL_POLICY: {routing.get('control')}\\n"
            f"ANSWER_SHAPE: {answer_shape}\\n"
            f"HARD_RULE: Do not change the target system.\\n"
            f"HARD_RULE: Follow the routed task type.\\n"
            f"HARD_RULE: If TASK_TYPE is ATTRIBUTION, identify supported attribution if present; otherwise explicitly state attribution is indeterminate, unsupported, or contested.\\n"
            f"HARD_RULE: If TASK_TYPE is ATTRIBUTION, do not replace attribution with a general conceptual explanation.\\n"
            f"HARD_RULE: If ANSWER_SHAPE is direct_only, answer directly and briefly.\\n"
            f"HARD_RULE: If ANSWER_SHAPE is direct_then_ep, give a direct answer first, then EP support.\\n"
            f"HARD_RULE: If ANSWER_SHAPE is full_ep, produce a full structured EP analysis.\\n"
        )
"""

if old2 not in s:
    raise SystemExit("routed_task block not found")

s = s.replace(old2, new2, 1)

p.write_text(s)
print("patched epra answer shapes")
