from __future__ import annotations

import json
from pathlib import Path

from app.services.epra import EPRAService


LABEL_ORDER = {"Pseudo-EP": 0, "Drifted EP": 1, "Weak EP": 2, "Valid EP": 3}


def main() -> None:
    service = EPRAService()
    cases_path = Path("./benchmarks/cases.jsonl")
    results_path = Path("./benchmarks/results.jsonl")
    rows = [json.loads(line) for line in cases_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    outputs = []
    pass_count = 0
    for row in rows:
        resp = service.analyze(task=row["task"], context={"benchmark_case": row["id"]})
        observed = resp.validity_status
        expected = row["expected_min_label"]
        passed = LABEL_ORDER.get(observed, -1) >= LABEL_ORDER.get(expected, -1)
        pass_count += int(passed)
        outputs.append(
            {
                "id": row["id"],
                "task": row["task"],
                "expected_min_label": expected,
                "observed_label": observed,
                "passed": passed,
                "repair_note": resp.repair_note,
                "metadata": resp.metadata,
            }
        )
    results_path.write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in outputs), encoding="utf-8")
    print(json.dumps({"total": len(outputs), "passed": pass_count, "results_path": str(results_path)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
