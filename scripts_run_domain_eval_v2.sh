#!/bin/zsh
set -euo pipefail

cd "/Users/wesleyshu/Library/CloudStorage/OneDrive-Personal/Energetic Paradigm/EP Model/Building EP on GPT/EPRA_API_Wrapper_v2"

python3 - <<'PY'
import json
import subprocess
from pathlib import Path
from datetime import datetime

bench_root = Path("/Users/wesleyshu/Library/CloudStorage/OneDrive-Personal/Energetic Paradigm/EP Model/EP Structure/Benchmarks_v2")
prompts_file = bench_root / "domain_eval_suite_50_draft.txt"
runs_root = bench_root / "runs"
runs_root.mkdir(parents=True, exist_ok=True)

prompts = [x.strip() for x in prompts_file.read_text().splitlines() if x.strip()]

stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
run_dir = runs_root / f"run_{stamp}"
run_dir.mkdir(parents=True, exist_ok=True)

results = []
for i, prompt in enumerate(prompts, 1):
    cmd = [
        "curl", "-s", "-X", "POST", "http://127.0.0.1:8000/chat",
        "-H", "Content-Type: application/json",
        "-d", json.dumps({"message": prompt})
    ]
    raw = subprocess.check_output(cmd, text=True)
    try:
        data = json.loads(raw)
        validity = data.get("metadata", {}).get("validity", {})
        row = {
            "id": i,
            "prompt": prompt,
            "status": data.get("validity_status"),
            "repair_note": data.get("repair_note"),
            "score": validity.get("score"),
            "mandatory_pass": validity.get("mandatory_pass"),
            "validation_source": validity.get("validation_source"),
            "gates": validity.get("gates", {}),
        }
    except Exception as e:
        row = {
            "id": i,
            "prompt": prompt,
            "status": "ERROR",
            "repair_note": str(e),
            "score": None,
            "mandatory_pass": False,
            "validation_source": None,
            "gates": {},
            "raw": raw[:1000],
        }
    results.append(row)

summary = {
    "total": len(results),
    "valid_ep": sum(1 for r in results if r.get("status") == "Valid EP"),
    "drifted_ep": sum(1 for r in results if r.get("status") == "Drifted EP"),
    "weak_ep": sum(1 for r in results if r.get("status") == "Weak EP"),
    "pseudo_ep": sum(1 for r in results if r.get("status") == "Pseudo-EP"),
    "errors": sum(1 for r in results if r.get("status") == "ERROR"),
    "canonical_validation": sum(1 for r in results if r.get("validation_source") == "canonical"),
}

(run_dir / "results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False))
(run_dir / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False))

print(json.dumps(summary, indent=2))
PY
