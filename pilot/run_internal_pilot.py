from __future__ import annotations

"""
Small internal pilot against a real model endpoint.

Prerequisites:
- OPENAI_API_KEY set in the environment.
- Optional OPENAI_MODEL override.
- Private corpus registry configured on the server.

This script is included as a ready-to-run pilot harness. It is not executed automatically here.
"""

import json
from pathlib import Path

from app.services.epra import EPRAService


TASKS = [
    "Set up a university admissions system in EP terms before answering.",
    "Analyze an AI inference deployment pipeline using EPRA and report the validity status.",
    "Compare two supply networks under pressure and identify maintenance, control, and fragility differences.",
]


def main() -> None:
    service = EPRAService()
    out_dir = Path("./pilot/out")
    out_dir.mkdir(parents=True, exist_ok=True)
    records = []
    for i, task in enumerate(TASKS, start=1):
        resp = service.analyze(task=task)
        record = {
            "id": f"pilot_{i:03d}",
            "task": task,
            "compact_setup": resp.compact_setup,
            "analysis": resp.analysis,
            "validity_status": resp.validity_status,
            "repair_note": resp.repair_note,
            "metadata": resp.metadata,
        }
        records.append(record)
    output_path = out_dir / "pilot_results.jsonl"
    output_path.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in records), encoding="utf-8")
    print(f"wrote {output_path}")


if __name__ == "__main__":
    main()
