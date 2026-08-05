"""Retrieval boundary and the prompt-stuffing implementation used in phase 1."""

from __future__ import annotations

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class PatternCard:
    """One authored architecture-pattern card."""

    card_id: str
    title: str
    content: str
    source: Path


@dataclass(frozen=True)
class RetrievedContext:
    """Cards selected for synthesis and their concatenated prompt text."""

    cards: tuple[PatternCard, ...]
    stuffed_text: str


class Retriever(ABC):
    """Boundary that lets retrieval change without rewiring the pipeline."""

    @abstractmethod
    def retrieve(self, profile: dict[str, Any]) -> RetrievedContext:
        """Return architecture knowledge relevant to a profile."""


class StuffEverythingRetriever(Retriever):
    """Load every card and concatenate it into one synthesis context."""

    def __init__(self, cards_dir: Path):
        self._cards_dir = cards_dir

    def retrieve(self, profile: dict[str, Any]) -> RetrievedContext:
        del profile  # This phase deliberately does no relevance filtering.
        cards = tuple(_load_card(path) for path in sorted(self._cards_dir.glob("*.md")))
        if not cards:
            raise ValueError(f"No pattern cards found in {self._cards_dir}")

        stuffed_text = "\n\n---\n\n".join(card.content for card in cards)
        return RetrievedContext(cards=cards, stuffed_text=stuffed_text)


def _load_card(path: Path) -> PatternCard:
    content = path.read_text(encoding="utf-8").strip()
    title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    id_match = re.search(r"^\*\*Card ID:\*\*\s+([A-Z0-9-]+)$", content, re.MULTILINE)
    if not title_match or not id_match:
        raise ValueError(f"Pattern card lacks a title or Card ID: {path}")
    return PatternCard(
        card_id=id_match.group(1),
        title=title_match.group(1),
        content=content,
        source=path,
    )
