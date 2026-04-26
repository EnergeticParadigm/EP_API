from pathlib import Path

p = Path("app/services/epra.py")
text = p.read_text()

anchor = """    def _handle_attribution(self, task: str, routing: Dict[str, Any]) -> EPRAResponse:
"""
helpers = '''
    def _handle_project_attribution(self, task: str, routing: Dict[str, Any]) -> EPRAResponse:
        return self._handle_attribution(task, routing)

    def _handle_project_fact(self, task: str, routing: Dict[str, Any]) -> EPRAResponse:
        return self._handle_direct_fact(task, routing)

    def _handle_world_attribution(self, task: str, routing: Dict[str, Any]) -> EPRAResponse:
        target = routing.get("target_system") or task
        prompt = f"""
Answer the following attribution question directly and briefly.

Question target: {target}

Requirements:
- Give the best direct answer first.
- If the answer is uncertain, say so explicitly.
- Add one short basis sentence.
- Do not force Energetic Paradigm system-analysis structure.
- Keep it under 120 words.
- Do not invent certainty.
"""
        raw = self.client.complete(prompt)
        answer = (raw or "").strip() or f"I cannot confidently attribute '{target}' from the current model output."

        return EPRAResponse(
            compact_setup=f"mode=WORLD_ATTRIBUTION; target={target}",
            analysis=answer,
            validity_status="Valid EP",
            repair_note=None,
            metadata={
                "task_system": target,
                "active_forms": [],
                "routing": routing,
                "mode": "WORLD_ATTRIBUTION",
                "validity": {
                    "label": "Valid EP",
                    "score": 1.0,
                    "gates": {"direct_answer": True},
                    "mandatory_pass": True,
                    "validation_source": "mode_contract",
                },
            },
        )

    def _handle_world_fact(self, task: str, routing: Dict[str, Any]) -> EPRAResponse:
        target = routing.get("target_system") or task
        prompt = f"""
Answer the following factual question directly and briefly.

Question target: {target}
Original question: {task}

Requirements:
- Give the best direct answer first.
- Add one short explanation sentence.
- If uncertain, say so clearly.
- Do not force Energetic Paradigm system-analysis structure.
- Keep it under 120 words.
"""
        raw = self.client.complete(prompt)
        answer = (raw or "").strip() or f"I cannot confidently answer the factual question about '{target}' from the current model output."

        return EPRAResponse(
            compact_setup=f"mode=WORLD_FACT; target={target}",
            analysis=answer,
            validity_status="Valid EP",
            repair_note=None,
            metadata={
                "task_system": target,
                "active_forms": [],
                "routing": routing,
                "mode": "WORLD_FACT",
                "validity": {
                    "label": "Valid EP",
                    "score": 1.0,
                    "gates": {"direct_fact": True},
                    "mandatory_pass": True,
                    "validation_source": "mode_contract",
                },
            },
        )
'''
if anchor not in text:
    raise SystemExit("helper anchor not found")

if "_handle_world_fact" not in text:
    text = text.replace(anchor, helpers + anchor, 1)

old = """        task_type = routing.get("task_type")
        if task_type == "ATTRIBUTION":
            return self._handle_attribution(task, routing)
        if task_type == "FORECAST":
            return self._handle_forecast(task, routing)
        if task_type == "DIRECT_FACT":
            return self._handle_direct_fact(task, routing)
        if task_type == "CLARIFICATION_REQUIRED":
            return self._handle_clarification(task, routing)
"""
new = """        task_type = routing.get("task_type")
        if task_type == "PROJECT_ATTRIBUTION":
            return self._handle_project_attribution(task, routing)
        if task_type == "WORLD_ATTRIBUTION":
            return self._handle_world_attribution(task, routing)
        if task_type == "FORECAST":
            return self._handle_forecast(task, routing)
        if task_type == "PROJECT_FACT":
            return self._handle_project_fact(task, routing)
        if task_type == "WORLD_FACT":
            return self._handle_world_fact(task, routing)
        if task_type == "CLARIFICATION_REQUIRED":
            return self._handle_clarification(task, routing)
"""
if old not in text:
    raise SystemExit("dispatch block not found")

text = text.replace(old, new, 1)
p.write_text(text)
print("patched", p)
