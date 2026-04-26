from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable
import os
import re

import yaml


_WORD_RE = re.compile(r"[a-zA-Z0-9_\-]+")


@dataclass
class CorpusEntry:
    id: str
    title: str
    role: str
    tags: list[str]
    text_path: str
    priority: int


@dataclass
class RetrievedSnippet:
    entry_id: str
    title: str
    role: str
    score: float
    snippet: str
    source_path: str


class PrivateCorpusRetrieverDistiller:
    def __init__(self) -> None:
        registry_path = os.getenv(
            "EPRA_PRIVATE_CORPUS_REGISTRY",
            "./config/private_corpus_registry.yaml",
        )
        self.registry_path = Path(registry_path)
        self.entries = self._load_registry(self.registry_path)

    def _load_registry(self, path: Path) -> list[CorpusEntry]:
        if not path.exists():
            return []
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        entries = []
        for item in data.get("entries", []):
            entries.append(
                CorpusEntry(
                    id=item["id"],
                    title=item["title"],
                    role=item.get("role", "unknown"),
                    tags=item.get("tags", []),
                    text_path=item["text_path"],
                    priority=int(item.get("priority", 0)),
                )
            )
        return entries

    def _tokenize(self, text: str) -> set[str]:
        return {m.group(0).lower() for m in _WORD_RE.finditer(text)}

    def _split_chunks(self, text: str, max_chars: int = 1200) -> Iterable[str]:
        text = re.sub(r"\s+", " ", text).strip()
        if len(text) <= max_chars:
            yield text
            return
        start = 0
        while start < len(text):
            end = min(len(text), start + max_chars)
            chunk = text[start:end]
            if end < len(text):
                last_break = max(chunk.rfind(". "), chunk.rfind("; "), chunk.rfind(" ) "))
                if last_break > max_chars // 2:
                    end = start + last_break + 1
                    chunk = text[start:end]
            yield chunk.strip()
            start = end

    def retrieve(self, task: str, context: dict[str, Any] | None = None, top_k: int = 6) -> list[RetrievedSnippet]:
        query = task if not context else task + " " + " ".join(f"{k} {v}" for k, v in context.items())
        qtokens = self._tokenize(query)
        results: list[RetrievedSnippet] = []
        for entry in self.entries:
            p = Path(entry.text_path)
            if not p.exists():
                continue
            text = p.read_text(encoding="utf-8", errors="ignore")
            etokens = self._tokenize(entry.title + " " + " ".join(entry.tags) + " " + entry.role)
            base_overlap = len(qtokens & etokens)
            for chunk in self._split_chunks(text):
                ctokens = self._tokenize(chunk)
                overlap = len(qtokens & ctokens)
                if overlap == 0 and base_overlap == 0:
                    continue
                score = overlap + 0.5 * base_overlap + 0.1 * entry.priority
                results.append(
                    RetrievedSnippet(
                        entry_id=entry.id,
                        title=entry.title,
                        role=entry.role,
                        score=score,
                        snippet=chunk,
                        source_path=str(p),
                    )
                )
        results.sort(key=lambda r: r.score, reverse=True)
        return results[:top_k]

    def distill(self, retrieved: list[RetrievedSnippet], max_items: int = 4, max_chars: int = 900) -> list[dict[str, Any]]:
        distilled = []
        seen = set()
        for item in retrieved:
            if item.entry_id in seen:
                continue
            seen.add(item.entry_id)
            distilled.append(
                {
                    "entry_id": item.entry_id,
                    "title": item.title,
                    "role": item.role,
                    "signal": item.snippet[:max_chars],
                    "score": round(item.score, 3),
                }
            )
            if len(distilled) >= max_items:
                break
        return distilled
