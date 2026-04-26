from pathlib import Path

p = Path("app/services/runtime.py")
s = p.read_text()

old = """    def build(self, task: str, context: Dict[str, Any] | None = None) -> RuntimeState:
        task_system = self.classify_system(task)
        active_forms = self.infer_active_forms(task_system)
        retrieved = self.retriever.retrieve(
            task=task,
            context=context,
            top_k=self.config["corpus"]["max_retrieved_items"],
        )
"""

new = """    def build(self, task: str, context: Dict[str, Any] | None = None) -> RuntimeState:
        routing = (context or {}).get("routing", {})

        if routing.get("target_system"):
            task_system = routing["target_system"]
        else:
            task_system = self.classify_system(task)

        if routing.get("mode") == "ep_system_analysis":
            active_forms = ["effective_force", "maintenance_load", "control_burden"]
        elif routing.get("mode") == "ep_attribution":
            active_forms = ["effective_force", "maintenance_load", "control_burden"]
        else:
            active_forms = self.infer_active_forms(task_system)

        retrieved = self.retriever.retrieve(
            task=task,
            context=context,
            top_k=self.config["corpus"]["max_retrieved_items"],
        )
"""

if old not in s:
    raise SystemExit("target block not found in runtime.py")

s = s.replace(old, new, 1)

old2 = """        selected_rules = {
            "require_compact_setup": True,
            "require_validity_label": True,
            "allowed_labels": self.config["runtime"]["allowed_labels"],
            "required_setup_fields": self.config["runtime"]["required_setup_fields"],
        }
"""

new2 = """        selected_rules = {
            "require_compact_setup": True,
            "require_validity_label": True,
            "allowed_labels": self.config["runtime"]["allowed_labels"],
            "required_setup_fields": self.config["runtime"]["required_setup_fields"],
            "hard_constraints": {
                "must_bind_target": True,
                "must_not_change_target": True,
            },
        }
"""

if old2 not in s:
    raise SystemExit("selected_rules block not found in runtime.py")

s = s.replace(old2, new2, 1)

p.write_text(s)
print("patched runtime.py")
