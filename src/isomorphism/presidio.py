"""Optional backend: names in running text from Microsoft Presidio (MIT, runs locally).

Presidio is not a dependency. Install it yourself (``pip install presidio-analyzer`` and a spaCy
model for your language) and pass the detector to ``anonymize``::

    from presidio_analyzer import AnalyzerEngine
    from isomorphism import anonymize
    from isomorphism.presidio import presidio_detector

    detector = presidio_detector(AnalyzerEngine(), language="en")
    safe, mapping = anonymize(text, detectors=[detector])

Nothing is downloaded by this module. Any object with an ``analyze(text=..., language=...,
entities=...)`` method that returns results with ``entity_type``, ``start``, ``end`` and
``score`` works.
"""

from __future__ import annotations

from collections.abc import Callable, Iterator, Sequence
from typing import Any

from .detectors import Candidate

_KINDS = {"PERSON": "PERSON", "ORGANIZATION": "ORG", "ORG": "ORG"}


def presidio_detector(
    analyzer: Any,
    *,
    language: str = "en",
    entities: Sequence[str] = ("PERSON", "ORGANIZATION"),
    min_score: float = 0.5,
) -> Callable[[str], Iterator[Candidate]]:
    """Wrap a Presidio ``AnalyzerEngine`` as a detector for ``anonymize(detectors=[...])``."""

    def detect(text: str) -> Iterator[Candidate]:
        for r in analyzer.analyze(text=text, language=language, entities=list(entities)):
            kind = _KINDS.get(r.entity_type)
            if kind and r.score >= min_score:
                yield Candidate(kind, r.start, r.end, min(float(r.score), 0.85), "presidio")

    return detect
