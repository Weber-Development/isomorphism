"""anonymize / restore. The mapping holds real values: this module never logs or stores it."""

from __future__ import annotations

import re
from collections.abc import Callable, Iterable, Iterator
from collections.abc import Mapping as AbstractMapping
from dataclasses import dataclass, replace

from . import entities
from .detectors import DETECTORS, Candidate

LANGS = frozenset({"de", "fr", "it", "en"})

Detector = Callable[[str], Iterator[Candidate]]
# Kinds that never replace what looks like the name of an authority ("Steueramt St. Gallen").
_PROTECTED = frozenset({"PERSON", "ORG", "ADDRESS"})

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
    # shortcut: lang is validated but changes nothing; all four languages are always active
    # because Swiss texts mix them.
    if lang is not None and lang.lower().split("-")[0] not in LANGS:
        raise ValueError(f"unsupported lang {lang!r}, expected one of {sorted(LANGS)}")


def _kept(value: str, keep: Iterable[str | re.Pattern[str]]) -> bool:
    folded = value.casefold()
    return any(
        k.fullmatch(value) if isinstance(k, re.Pattern) else k.casefold() == folded for k in keep
    )


def detect(
    text: str,
    lang: str | None = None,
    *,
    keep: Iterable[str | re.Pattern[str]] = (),
    detectors: Iterable[Detector] = (),
    protect_authorities: bool = True,
) -> list[Finding]:
    """Find personal data. Overlaps go to the higher confidence, then the longer match.

    ``keep``: values that must stay in the text, as exact strings (case-insensitive) or
    compiled patterns that must match the whole value.
    ``detectors``: extra recognisers, for example ``isomorphism.presidio.presidio_detector``.
    ``protect_authorities``: names of authorities such as "Steueramt St. Gallen" are not replaced.
    """
    _check_lang(lang)
    keep = tuple(keep)
    official = bytearray(len(text))  # 1 inside a name of an authority
    if protect_authorities:
        for m in entities.AUTHORITY.finditer(entities.normalise(text)):
            official[m.start() : m.end()] = b"\x01" * (m.end() - m.start())
    candidates = (
        c
        for d in (*DETECTORS, *entities.DETECTORS, *detectors)
        for c in d(text)
        if not _kept(text[c.start : c.end], keep)
        and not (c.kind in _PROTECTED and any(official[c.start : c.end]))
    )
    found = sorted(candidates, key=lambda c: (-c.confidence, c.start - c.end, c.start))
    taken = bytearray(len(text))  # 1 where a hit was kept
    out: list[Finding] = []
    for c in found:
        if not any(taken[c.start : c.end]):
            taken[c.start : c.end] = b"\x01" * (c.end - c.start)
            out.append(Finding(c.kind, c.start, c.end, c.confidence, c.detector, c.checksum_ok))
    return sorted(out, key=lambda f: f.start)


def anonymize(
    text: str,
    lang: str | None = None,
    *,
    keep: Iterable[str | re.Pattern[str]] = (),
    detectors: Iterable[Detector] = (),
    protect_authorities: bool = True,
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
    for f in detect(
        text, lang, keep=keep, detectors=detectors, protect_authorities=protect_authorities
    ):
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


# A placeholder with generous spaces stays well below this; longer tails are plain text.
_HOLD = 40


class Restorer:
    """``restore`` for an answer that arrives in pieces, also when a placeholder is split.

    >>> r = Restorer(mapping); out = "".join(r.feed(c) for c in chunks) + r.flush()
    """

    def __init__(self, mapping: AbstractMapping[str, str]) -> None:
        self._mapping = mapping
        self._tail = ""

    def feed(self, chunk: str) -> str:
        buf = self._tail + chunk
        i = buf.rfind("[")
        if i != -1 and "]" not in buf[i:] and len(buf) - i <= _HOLD:
            buf, self._tail = buf[:i], buf[i:]
        else:
            self._tail = ""
        return restore(buf, self._mapping)

    def flush(self) -> str:
        """The held-back end, once the answer is complete."""
        tail, self._tail = self._tail, ""
        return restore(tail, self._mapping)


def restore_stream(chunks: Iterable[str], mapping: AbstractMapping[str, str]) -> Iterator[str]:
    """Generator version of :class:`Restorer`."""
    r = Restorer(mapping)
    for chunk in chunks:
        if out := r.feed(chunk):
            yield out
    if out := r.flush():
        yield out
