from pathlib import Path

p = Path("app/services/epra.py")
s = p.read_text()

old_prompt = """Routing priority rules:
- The routed TARGET_SYSTEM is binding.
- Do not replace the target with Energetic Paradigm, EP methodology, EPRA, graph representation, blueprint, ontology, primitive layer, node-edge language, or any meta-framework object unless the routed target explicitly is one of those.
- If TASK_TYPE is SYSTEM_ANALYSIS, analyze the bound target system itself, not EP as a theory.
- If TASK_TYPE is ATTRIBUTION, answer as a provenance / authorship control problem and do not convert it into a generic system-analysis essay.
- If TASK_TYPE is AMBIGUOUS, stay close to the bound target and minimize speculative expansion.
- Corpus snippets are support material, not permission to change the target.
- The compact_ep_setup.system field must describe the bound target system directly.
- If the target is "a university admissions system", the answer must stay on admissions selection, eligibility, ranking, offers, enrollment, review, quotas, appeals, and administrative load.
- Do not discuss energetic graphs, representation layers, blueprint ontology, or EP formal architecture unless the user explicitly asked about those objects.
"""

new_prompt = """Routing priority rules:
- The routed TARGET_SYSTEM is binding.
- Do not replace the target with Energetic Paradigm, EP methodology, EPRA, graph representation, blueprint, ontology, primitive layer, node-edge language, or any meta-framework object unless the routed target explicitly is one of those.
- If TASK_TYPE is SYSTEM_ANALYSIS, analyze the bound target system itself, not EP as a theory.
- If TASK_TYPE is ATTRIBUTION, answer as a provenance / authorship control problem.
- If TASK_TYPE is ATTRIBUTION, you MUST identify a specific attributed origin if it exists in the provided corpus.
- If TASK_TYPE is ATTRIBUTION, you MUST NOT invent authorship.
- If TASK_TYPE is ATTRIBUTION and no reliable attribution exists, you MUST explicitly state that attribution is indeterminate, unsupported, or contested.
- If TASK_TYPE is ATTRIBUTION, you MUST NOT replace attribution with a general conceptual explanation.
- If TASK_TYPE is AMBIGUOUS, stay close to the bound target and minimize speculative expansion.
- Corpus snippets are support material, not permission to change the target.
- The compact_ep_setup.system field must describe the bound target system directly.
- If the target is "a university admissions system", the answer must stay on admissions selection, eligibility, ranking, offers, enrollment, review, quotas, appeals, and administrative load.
- Do not discuss energetic graphs, representation layers, blueprint ontology, or EP formal architecture unless the user explicitly asked about those objects.
- Answer must follow the required answer shape.
- If answer_shape is "direct", respond as one concise bounded answer, not a generic essay.
"""

if old_prompt not in s:
    raise SystemExit("prompt block not found")
s = s.replace(old_prompt, new_prompt, 1)

old_block = """        routing = (context or {}).get("routing", {})
        runtime = self.runtime_builder.build(task=task, context=context)
        distilled = getattr(runtime, "distilled_corpus", []) or []
"""

new_block = """        routing = (context or {}).get("routing", {})
        runtime = self.runtime_builder.build(task=task, context=context)

        if routing.get("target_system"):
            runtime.task_system = routing["target_system"]

        if routing.get("task_type") in {"SYSTEM_ANALYSIS", "ATTRIBUTION"}:
            runtime.active_forms = ["effective_force", "maintenance_load", "control_burden"]

        distilled = getattr(runtime, "distilled_corpus", []) or []
"""

if old_block not in s:
    raise SystemExit("runtime block not found")
s = s.replace(old_block, new_block, 1)

old_task = """        routed_task = (
            f"TASK: {task}\\n"
            f"ROUTING_MODE: {routing.get('mode')}\\n"
            f"TASK_TYPE: {routing.get('task_type')}\\n"
            f"TARGET_SYSTEM: {routing.get('target_system')}\\n"
            f"NEEDS_CLARIFICATION: {routing.get('needs_clarification')}\\n"
            f"CONTROL_POLICY: {routing.get('control')}\\n"
            f"HARD_RULE: Do not change the target system.\\n"
            f"HARD_RULE: Follow the routed task type.\\n"
            f"HARD_RULE: If task type is ATTRIBUTION, do not invent authorship.\\n"
        )
"""

new_task = """        answer_shape = (routing.get("control") or {}).get("answer_shape")

        routed_task = (
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

if old_task not in s:
    raise SystemExit("routed_task block not found")
s = s.replace(old_task, new_task, 1)

p.write_text(s)
print("patched epra control v2")
