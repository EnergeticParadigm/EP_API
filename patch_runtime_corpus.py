from pathlib import Path

p = Path("app/services/runtime.py")
s = p.read_text()

old = """        distilled_corpus = self.retriever.distill(
            retrieved,
            max_items=self.config["corpus"]["max_distilled_items"],
            max_chars=self.config["corpus"]["distill_max_chars_per_snippet"],
        )
"""

new = """        distilled_corpus = self.retriever.distill(
            retrieved,
            max_items=self.config["corpus"]["max_distilled_items"],
            max_chars=self.config["corpus"]["distill_max_chars_per_snippet"],
        )

        task_type = routing.get("task_type")
        target_system = (routing.get("target_system") or "").strip().lower()

        if task_type == "SYSTEM_ANALYSIS":
            distilled_corpus = [
                x for x in distilled_corpus
                if x.get("entry_id") not in {"ep_methodology_full", "ep_fcs_v0"}
            ]

        elif task_type == "AMBIGUOUS":
            distilled_corpus = []

        elif task_type == "ATTRIBUTION":
            distilled_corpus = [
                x for x in distilled_corpus
                if x.get("entry_id") in {"ep_fcs_v0", "ep_methodology_full"}
            ]

        if not distilled_corpus and task_type == "SYSTEM_ANALYSIS":
            distilled_corpus = [{
                "entry_id": "runtime_target_anchor",
                "title": "Runtime Target Anchor",
                "role": "target_anchor",
                "signal": f"The bound system for analysis is: {routing.get('target_system')}. Do not replace it with a generic EP object.",
                "score": 10.0,
            }]
"""

if old not in s:
    raise SystemExit("distill block not found in runtime.py")

p.write_text(s.replace(old, new, 1))
print("patched runtime corpus policy")
