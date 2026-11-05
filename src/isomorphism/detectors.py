"""Swiss recognisers. Each yields candidates; overlaps are resolved in core."""

from __future__ import annotations

import re
from collections.abc import Callable, Iterator
from dataclasses import dataclass, replace

from ._checks import ahv_ok, iban_ok, uid_ok


@dataclass(frozen=True, slots=True)
class Candidate:
    kind: str
    start: int
    end: int
    confidence: float
    detector: str
    checksum_ok: bool | None = None
    # The spelling a hit stands for: hits of one kind with the same key share a placeholder
    # even when their text differs ("KRASNIQI, Arben" with key "Arben Krasniqi" and the text
    # "Arben Krasniqi"). None: the text itself is the key.
    key: str | None = None


def _digits(s: str) -> str:
    return "".join(c for c in s if c.isdigit())


def _checked(
    kind: str,
    detector: str,
    pattern: re.Pattern[str],
    ok: Callable[[str], bool],
    clean: Callable[[str], str],
    text: str,
    valid: float,
    invalid: float,
) -> Iterator[Candidate]:
    # Invalid check digits are still reported, with lower confidence (better too many than too few).
    for m in pattern.finditer(text):
        good = ok(clean(m[0]))
        yield Candidate(kind, m.start(), m.end(), valid if good else invalid, detector, good)


_AHV = re.compile(r"(?<!\d)756[ .\-]?\d{4}[ .\-]?\d{4}[ .\-]?\d{2}(?!\d)")
_IBAN = re.compile(r"(?<![A-Za-z0-9])(?:CH|LI)\d{2}(?: ?[0-9A-Z]){17}(?![A-Za-z0-9])", re.I)
_UID = re.compile(r"(?<![A-Za-z0-9])CHE[- ]?\d{3}[. ]?\d{3}[. ]?\d{3}(?!\d)", re.I)
_EMAIL = re.compile(r"(?<![\w.+\-])[\w.+\-]+@[\w\-]+(?:\.[\w\-]+)*\.[^\W\d_]{2,}")
_PHONE = re.compile(
    r"""(?<![\w+])(?<!\d[ .\-/])
    (?:(?:\+|00)41[ .\-]?(?:\(0\)[ .\-]?)?|\(?0)
    [1-9]\d\)?
    [ .\-/]?\d{3}[ .\-]?\d{2}[ .\-]?\d{2}(?!\d)""",
    re.X,
)


def ahv(text: str) -> Iterator[Candidate]:
    for c in _checked("AHV", "ahv-ean13", _AHV, ahv_ok, _digits, text, 0.99, 0.6):
        if "." not in text[c.start : c.end]:  # bare digits are weaker evidence than the dotted form
            c = replace(c, confidence=0.9 if c.checksum_ok else 0.4)
        yield c


def iban(text: str) -> Iterator[Candidate]:
    yield from _checked(
        "IBAN", "iban-mod97", _IBAN, iban_ok, lambda s: s.replace(" ", "").upper(), text, 0.99, 0.6
    )


def uid(text: str) -> Iterator[Candidate]:
    yield from _checked("UID", "uid-mod11", _UID, uid_ok, _digits, text, 0.98, 0.6)


def email(text: str) -> Iterator[Candidate]:
    for m in _EMAIL.finditer(text):
        yield Candidate("EMAIL", m.start(), m.end(), 0.95, "email-regex")


def phone(text: str) -> Iterator[Candidate]:
    for m in _PHONE.finditer(text):
        s = m[0]
        international = s.startswith(("+", "00"))
        confidence = 0.95 if international else 0.85 if not s.isdigit() else 0.6
        yield Candidate("PHONE", m.start(), m.end(), confidence, "phone-ch")


DETECTORS: tuple[Callable[[str], Iterator[Candidate]], ...] = (ahv, iban, uid, email, phone)
