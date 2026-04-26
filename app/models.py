from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    task: str = Field(..., description="User task or prompt")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Optional structured context")


class ValidateRequest(BaseModel):
    task: str
    output_text: str


class ReconstructRequest(BaseModel):
    fragments: List[str]


class EPRAResponse(BaseModel):
    compact_setup: str
    analysis: str
    validity_status: str
    repair_note: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
