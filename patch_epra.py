from pathlib import Path

p = Path("app/services/epra.py")
s = p.read_text()

old = """        runtime = self.runtime_builder.build(task=task, context=context)
        distilled = getattr(runtime, "distilled_corpus", []) or []

        raw = self.gateway.generate(
            system_prompt=self.system_prompt,
            runtime_state={
                "task_system": runtime.task_system,
                "active_forms": runtime.active_forms,
                "kernel": runtime.kernel,
                "selected_rules": runtime.selected_rules,
                "distilled_corpus": distilled,
                "examples": runtime.examples,
            },
            task=task,
        )
"""

new = """        routing = (context or {}).get("routing", {})
        runtime = self.runtime_builder.build(task=task, context=context)
        distilled = getattr(runtime, "distilled_corpus", []) or []

        routed_task = (
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

        raw = self.gateway.generate(
            system_prompt=self.system_prompt,
            runtime_state={
                "task_system": runtime.task_system,
                "active_forms": runtime.active_forms,
                "kernel": runtime.kernel,
                "selected_rules": runtime.selected_rules,
                "distilled_corpus": distilled,
                "examples": runtime.examples,
                "routing_mode": routing.get("mode"),
                "task_type": routing.get("task_type"),
                "target_system": routing.get("target_system"),
                "needs_clarification": routing.get("needs_clarification"),
                "control_policy": routing.get("control"),
            },
            task=routed_task,
        )
"""

if old not in s:
    raise SystemExit("❌ target block not found — stop here")

p.write_text(s.replace(old, new, 1))
print("✅ patched epra.py")
