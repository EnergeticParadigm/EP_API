from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.services.router_v4 import route_prompt_v4

tests = [
    "Analyze the airport security screening system with Energetic Paradigm.",
    "Who invented Energetic Paradigm?",
    "Will the US occupy Iran?",
    "What is EPRA?",
    "Analyze this",
]

for t in tests:
    print("=" * 80)
    print(t)
    print(route_prompt_v4(t))
