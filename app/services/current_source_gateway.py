from __future__ import annotations

import os
from typing import Any, Dict


class CurrentSourceGateway:
    def search(self, query: str) -> Dict[str, Any]:
        provider = os.getenv("EPRA_CURRENT_SOURCE_PROVIDER", "none").strip().lower()

        if provider == "none":
            return {
                "provider": "none",
                "available": False,
                "query": query,
                "sources": [],
                "note": "No current-source provider is connected. Do not claim live-event verification.",
            }

        raise RuntimeError(
            f"Current-source provider '{provider}' is not implemented yet. "
            "Implement it behind CurrentSourceGateway.search()."
        )
