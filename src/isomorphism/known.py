"""Names you already know, for example the clients of an office, are always replaced.

Patterns miss a name without title or context when the first name is not on the list. When the
caller knows the names that may appear (its clients), it can pass them::

    from isomorphism import anonymize
    from isomorphism.known import known_detector

    clients = known_detector(["Arben Krasniqi", "Familie Muster", "Reinigung Blitzblank GmbH"])
    safe, mapping = anonymize(text, detectors=[clients])

Build the detector once and keep it while the names do not change; this module keeps nothing
between calls. The full name is found in any case and order ("KRASNIQI, Arben", "Herr Arben
Krasniqi") and every form of it gets the same placeholder; ``restore`` gives back the first
form seen in the text. A single word of the name ("Krasniqi")
is found when it is capitalised, with its own placeholder, except for surnames that are also
ordinary words (Keller, Koch, Weber ...), which the patterns find after a title instead.
"""

from __future__ import annotations

import re
from collections.abc import Callable, Iterable, Iterator

from .detectors import Candidate
from .entities import (
    _LEADING,
    _LEGAL,
    _NOT_SURNAME,
    _ORG_FIRST,
    _ORG_TRADE,
    _TITLE,
    _TRADE,
    _capitalised,
    normalise,
)

MAX_ENTRIES = 5000
FULL = 0.99  # wins over every pattern, so the whole name is one hit
WORD = 0.6  # like a surname found again: loses to a pattern hit that covers the whole name

# Group words in front of a surname: "Familie Muster", "Erben Muster", "Ehepaar Muster".
_GROUP = rf"(?:{_TITLE}|Erben|Erbengemeinschaft|Ehepaar|Eheleute|Geschwister|Héritiers|Eredi|Firma)"
_LEADING_GROUP = re.compile(rf"^(?:{_GROUP}[ ]+)+")
_LEGAL_END = re.compile(rf"[ ,]+{_LEGAL}$")
_TRADE_WORD = re.compile(rf"{_TRADE}$")
# Surnames that are also ordinary words in German, French, Italian or English: alone they are
# not replaced, the full name and a title before them still are.
_COMMON = frozenset(
    """
    Keller Koch Kaufmann Richter Meister Sommer Winter Frei Gross Klein Lang Stein Berg Wolf
    Vogel Fischer Weber Bauer Schneider Müller Schmid Schmied Becker Wagner Zimmermann Gerber
    Hofer Huber Graf König Kaiser Fuchs Hahn Bach Brunner Wirth Wirz Jäger Schütz Engel Hase
    Pierre Marine Christian Grace Mark Bill Rose Can Jan Max Mai August Mars Martin Blanc
    Petit Grand Fontaine Rossi Bianchi Neri Santo Monte Ferrari Sole Long White Black Brown
    Green Young King Baker Smith Miller Wood Hill Bell Rich Fortune Bank Post Treuhand
    """.split()
)
_INITIAL = re.compile(r"^[^\W\d_]\.?$")
# A word as the name patterns see it: letters with inner apostrophes and hyphens.
_TOKEN = re.compile(r"(?<![\w'’-])[^\W_][\w'’]*(?:-[^\W_][\w'’]*)*")


def _kind(value: str) -> str:
    if _LEGAL_END.search(value) or _ORG_FIRST.match(value) or _ORG_TRADE.match(value):
        return "ORG"
    return "PERSON"


def _words(value: str) -> list[str]:
    """The words of a name with the case it has in a sentence ("KRASNIQI" -> "Krasniqi")."""
    return [_capitalised(w) if w.isupper() and len(w) > 1 else w for w in value.split()]


_GAP = r"[ \t]+"
_COMMA = r"[ \t]*,[ \t]*"


def _phrase(words: list[str]) -> str:
    return _GAP.join(re.escape(w) for w in words)


def _unescape(form: str) -> str:
    """A form pattern back as text: "Krasniqi[ \\t]*,[ \\t]*Arben" -> "Krasniqi, Arben"."""
    form = form.replace(_COMMA, ", ").replace(_GAP, " ")
    return re.sub(r"\\(.)", r"\1", form)


def _spelling(text: str) -> str:
    """One spelling for the forms of a name: case, spaces and the comma do not count."""
    return " ".join(text.replace(",", " , ").split()).casefold()


def _single(word: str) -> bool:
    letters = sum(c.isalpha() for c in word)
    return (
        letters >= 3
        and word[:1].isupper()
        and word not in _COMMON
        and word not in _NOT_SURNAME
        and word not in _LEADING
        and not re.fullmatch(_GROUP, word)
        and not _INITIAL.match(word)
    )


def _forms(kind: str, value: str) -> tuple[list[str], list[str]]:
    """Patterns for the full name (in any case) and single words (capitalised)."""
    value = " ".join(value.split())
    full: list[str] = []
    single: list[str] = []
    if kind == "ORG":
        words = _words(value)
        full.append(_phrase(words))
        bare = _LEGAL_END.sub("", " ".join(words))
        if bare != " ".join(words):
            full.append(_phrase(bare.split()))
        rest = [w for w in bare.split() if not _TRADE_WORD.match(w)]
        if len(rest) == 1 and len(rest[0]) >= 4 and _single(rest[0]):
            single.append(re.escape(rest[0]))
        return full, single
    name = _LEADING_GROUP.sub("", value)
    words = _words(name)
    if not words:
        return full, single
    full.append(_phrase(_words(value)))
    if len(words) >= 2:
        # "Arben Krasniqi", "Krasniqi Arben", "Krasniqi, Arben". A title before it stays in the
        # text: the model may see "Herr", and it is not part of the value that comes back.
        last, rest = words[-1], words[:-1]
        for order in (words, [last, *rest]):
            full.append(_phrase(order))
        full.append(f"{re.escape(last)}{_COMMA}{_phrase(rest)}")
    for w in words:
        if _single(w):
            single.append(re.escape(w))
        if "-" in w:  # "Muster-Keller": "Frau Muster" and "Frau Keller" are both written
            single += [re.escape(h) for h in w.split("-") if len(h) >= 4 and _single(h)]
    return full, single


def known_detector(
    entries: Iterable[str | tuple[str, str]],
) -> Callable[[str], Iterator[Candidate]]:
    """A detector for ``anonymize(detectors=[...])`` that always finds the given names.

    ``entries``: names as strings, or ``(kind, name)`` with kind ``"PERSON"`` or ``"ORG"``.
    A string with a legal form ("… GmbH"), "Verein …" or a trade ("Bäckerei …") is a company,
    any other a person. At most ``MAX_ENTRIES`` names.
    """
    by_kind: dict[str, tuple[dict[str, str], set[str]]] = {}
    for count, entry in enumerate(entries, 1):
        kind, value = entry if isinstance(entry, tuple) else (_kind(entry), entry)
        if kind not in ("PERSON", "ORG"):
            raise ValueError(f"unsupported kind {kind!r}, expected PERSON or ORG")
        if count > MAX_ENTRIES:
            raise ValueError(f"more than {MAX_ENTRIES} known names")
        full, single = _forms(kind, value)
        key = " ".join(_words(value)).casefold()
        fulls, singles = by_kind.setdefault(kind, ({}, set()))
        for f in full:
            fulls.setdefault(f, key)
        singles.update(single)

    # A word index instead of one large alternation: with thousands of names the regex engine
    # would try every name at every position.
    compiled = []
    for kind, (fulls, singles) in by_kind.items():
        by_first: dict[str, list[str]] = {}
        for f in fulls:
            first = _TOKEN.search(_unescape(f))
            if first and first.start() == 0:
                by_first.setdefault(first[0].casefold(), []).append(f)
        starts = {
            first: re.compile(
                "(?:" + "|".join(sorted(forms, key=len, reverse=True)) + r")(?![\w'’-])",
                re.IGNORECASE,
            )
            for first, forms in by_first.items()
        }
        # The key of a hit is found again from its text.
        keys = {_spelling(_unescape(f)): k for f, k in fulls.items()}
        words = {_unescape(w) for w in singles}
        compiled.append((kind, starts, keys, words))

    def detect(text: str) -> Iterator[Candidate]:
        # Single words only as written in a sentence; normalise() reads capitals as such.
        normal = normalise(text) if any(words for *_, words in compiled) else text
        tokens = [(m.start(), m[0]) for m in _TOKEN.finditer(text)]
        for kind, starts, keys, words in compiled:
            end = 0  # left to right without overlaps, as re.finditer would
            for start, token in tokens:
                pattern = start >= end and starts.get(token.casefold())
                if pattern and (m := pattern.match(text, start)):
                    key = keys.get(_spelling(m[0]))
                    yield Candidate(kind, start, m.end(), FULL, "known", key=key)
                    end = m.end()
            if words:
                for m in _TOKEN.finditer(normal):
                    if m[0] in words:
                        yield Candidate(kind, m.start(), m.end(), WORD, "known-word")

    return detect
