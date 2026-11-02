"""anonymize / restore. The mapping holds real values: this module never logs or stores it."""

from __future__ import annotations

import re
from collections.abc import Iterable
from collections.abc import Mapping as AbstractMapping
from dataclasses import dataclass, replace

from .detectors import DETECTORS

LANGS = frozenset({"de", "fr", "it", "en"})

# Tolerant on restore: models sometimes change case or add spaces inside the brackets.
_TOKEN = re.compile(r"\[\s*([A-Za-z]+)\s*_\s*(\d+)\s*\]")


@dataclass(frozen=True, slots=True)
class Finding:
    """One hit for the audit log. Positions refer to the original text; the value is not kept."""

    kind: str
    start: int
    end: int
    confidence: float
    detector: str
    checksum_ok: bool | None = None
    placeholder: str = ""


class Mapping(dict[str, str]):
    """placeholder -> real value, plus the findings. repr() hides the values."""

    findings: list[Finding]

    def __init__(self) -> None:
        super().__init__()
        self.findings = []

    def __repr__(self) -> str:
        return f"Mapping(<{len(self)} placeholders, values hidden>)"


def _check_lang(lang: str | None) -> None:
    # shortcut: lang has no effect yet (the checksum recognisers are language-neutral);
    # it selects context words once names and addresses arrive.
    if lang is not None and lang.lower().split("-")[0] not in LANGS:
        raise ValueError(f"unsupported lang {lang!r}, expected one of {sorted(LANGS)}")


def detect(text: str, lang: str | None = None, *, keep: Iterable[str] = ()) -> list[Finding]:
    """Find personal data. Overlaps go to the higher confidence, then the longer match.

    ``keep``: exact values (case-insensitive) that must stay in the text.
    """
    _check_lang(lang)
    kept = {k.casefold() for k in keep}
    found = sorted(
        (c for d in DETECTORS for c in d(text) if text[c.start : c.end].casefold() not in kept),
        key=lambda c: (-c.confidence, c.start - c.end, c.start),
    )
    taken: list[tuple[int, int]] = []
    out: list[Finding] = []
    for c in found:
        if all(c.end <= s or c.start >= e for s, e in taken):
            taken.append((c.start, c.end))
            out.append(Finding(c.kind, c.start, c.end, c.confidence, c.detector, c.checksum_ok))
    return sorted(out, key=lambda f: f.start)


def anonymize(
    text: str, lang: str | None = None, *, keep: Iterable[str] = ()
) -> tuple[str, Mapping]:
    """Replace personal data by placeholders like ``[AHV_1]``.

    Identical values get the same placeholder. Returns ``(text, mapping)``; the mapping has
    the real values and a ``findings`` list. Storing the mapping is up to the caller.
    """
    # Never reuse a placeholder that already stands in the text.
    in_text = {_name(m) for m in _TOKEN.finditer(text)}
    mapping = Mapping()
    by_value: dict[tuple[str, str], str] = {}
    counters: dict[str, int] = {}
    parts: list[str] = []
    pos = 0
    for f in detect(text, lang, keep=keep):
        value = text[f.start : f.end]
        ph = by_value.get((f.kind, value))
        if ph is None:
            n = counters.get(f.kind, 0)
            while True:
                n += 1
                ph = f"[{f.kind}_{n}]"
                if ph not in in_text:
                    break
            counters[f.kind] = n
            by_value[(f.kind, value)] = ph
            mapping[ph] = value
        mapping.findings.append(replace(f, placeholder=ph))
        parts += (text[pos : f.start], ph)
        pos = f.end
    parts.append(text[pos:])
    return "".join(parts), mapping


def _name(m: re.Match[str]) -> str:
    return f"[{m[1].upper()}_{int(m[2])}]"


def restore(text: str, mapping: AbstractMapping[str, str]) -> str:
    """Put the real values back. Single pass, so restored values are never rescanned.

    Unknown placeholders stay unchanged.
    """
    return _TOKEN.sub(lambda m: mapping.get(_name(m), m[0]), text)
