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
import unicodedata
from collections.abc import Callable, Iterable, Iterator

from ._names import FIRST_NAMES
from .detectors import Candidate
from .entities import (
    _KEEP_UPPER,
    _LEADING,
    _LEGAL,
    _NOT_SURNAME,
    _ORG_FIRST,
    _ORG_TRADE,
    _ORG_TRADE_AFTER,
    _PARTICLE,
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
_LEADING_GROUP = re.compile(rf"^(?:{_GROUP}[ ]+)+", re.IGNORECASE)
_LEGAL_END = re.compile(rf"[ ,]+{_LEGAL}$", re.IGNORECASE)
_LEGAL_END_AS_WRITTEN = re.compile(rf"[ ,]+{_LEGAL}$")  # "Anna Sa" is a person
_TRADE_WORD = re.compile(rf"{_TRADE}$")
# Words of a business name without legal form: "Muster Immobilien", "Muster & Söhne".
_BUSINESS = re.compile(
    r"(?i:immobilien|transporte?|söhne|soehne|partner|consulting|holding|services?|bau|"
    r"architekten|treuhand|praxis|beratung|handel|import|export|elektro|sanitär|gipser|maler)$"
)
_PARTICLE_WORD = re.compile(rf"{_PARTICLE}$")
# Surnames that are also ordinary words or places: alone they are not replaced (the full name
# and a title before them still are). Best effort: German writes every noun with a capital.
_COMMON = frozenset(
    """
    Keller Koch Kaufmann Richter Meister Sommer Winter Herbst Frei Gross Klein Lang Kurz Stein
    Berg Wolf Vogel Fischer Weber Bauer Schneider Müller Schmid Schmied Becker Wagner Zimmermann
    Gerber Hofer Huber Graf König Kaiser Fuchs Hahn Bach Brunner Wirth Wirz Jäger Schütz Engel
    Hase Weiss Schwarz Braun Roth Ernst Jung Wild Gut Frisch Stark Reich Stutz Boss Freitag
    Sonntag Montag Schweizer Zürcher Berner Basler Luzerner Walliser Bündner Appenzeller
    Thurgauer Aargauer Glarner Zuger Baden Glarus Zug Wil Thun Chur Olten Sion Pierre Marine
    Christian Grace Mark Bill Rose Rosa Can Jan Max Mai August Mars Martin Blanc Petit Grand
    Fontaine Noël Natale Felice Franco Marina Alba Costa Claire Pascal Fleur Chiara Serena Pia
    Bella Regina Luna Stella Domenica Rossi Bianchi Neri Santo Monte Ferrari Sole Long White
    Black Brown Green Young King Baker Smith Miller Wood Hill Bell Rich Fortune Bank Post
    Treuhand
    """.split()
)
_ONE_LETTER = re.compile(r"^[^\W\d_]\.?$")  # an initial
# A word as the name patterns see it: letters with inner apostrophes and hyphens.
_TOKEN = re.compile(r"(?<![\w'’-])[^\W_][\w'’]*(?:-[^\W_][\w'’]*)*")
_QUOTES = re.compile(r"[«»\"“”„‹›]")
_FOLD = str.maketrans({"ä": "ae", "ö": "oe", "ü": "ue", "Ä": "Ae", "Ö": "Oe", "Ü": "Ue", "ß": "ss"})


def _kind(value: str) -> str:
    words = value.split()
    if (
        (_LEGAL_END_AS_WRITTEN.search(value) or (value.isupper() and _LEGAL_END.search(value)))
        or _ORG_FIRST.match(value)
        or _ORG_TRADE.match(value)
        or _ORG_TRADE_AFTER.search(value)
        or "&" in words
        or "+" in words
        or any(_TRADE_WORD.match(w) or _BUSINESS.match(w) for w in words)
    ):
        return "ORG"
    return "PERSON"


def _words(value: str) -> list[str]:
    """The words of a name with the case it has in a sentence ("KRASNIQI" -> "Krasniqi");
    legal forms stay as written."""
    return [
        _capitalised(w) if w.isupper() and len(w) > 1 and w not in _KEEP_UPPER else w
        for w in value.split()
    ]


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


def _variants(text: str) -> set[str]:
    """The text, with umlauts as ae/oe/ue and without accents, as bank statements write it."""
    decomposed = unicodedata.normalize("NFKD", text)
    plain = "".join(c for c in decomposed if not unicodedata.combining(c))
    return {text, text.translate(_FOLD), plain}


def _single(word: str) -> bool:
    letters = sum(c.isalpha() for c in word)
    return (
        (letters >= 4 or (letters == 3 and word in FIRST_NAMES))
        and word[:1].isupper()
        and word not in _COMMON
        and word not in _NOT_SURNAME
        and word not in _LEADING
        and not _BUSINESS.match(word)
        and not _TRADE_WORD.match(word)
        and not re.fullmatch(_GROUP, word)
        and not re.fullmatch(_LEGAL, word, re.IGNORECASE)
        and not _ONE_LETTER.match(word)
    )


def _person_split(words: list[str]) -> tuple[list[str], list[str]]:
    """First names and surname: the surname starts at the first particle after the first word
    ("Maria | da Silva", "Hans | von Arx"), otherwise it is the last word."""
    for i in range(1, len(words)):
        if _PARTICLE_WORD.match(words[i]) and i < len(words) - 1:
            return words[:i], words[i:]
    return words[:-1], words[-1:]


def _forms(kind: str, value: str) -> tuple[list[list[str]], list[str], str]:
    """The full forms of a name (lists of words; a "," word marks the comma form), the single
    words that are found alone, and the key its full forms share."""
    value = " ".join(_QUOTES.sub("", value).split())
    full: list[list[str]] = []
    single: list[str] = []
    if kind == "ORG":
        bare = _LEGAL_END.sub("", value)
        for v in dict.fromkeys((value, bare)):
            if len(v.split()) >= 2:
                full.append(_words(v))
        rest = [w for w in _words(bare) if not _TRADE_WORD.match(w) and not _BUSINESS.match(w)]
        if len(rest) == 1 and _single(rest[0]):
            single.append(rest[0])
        return full, single, " ".join(_words(value))
    if value.count(",") == 1:  # "Krasniqi, Arben", as offices export their clients
        last, first = (_LEADING_GROUP.sub("", part.strip()) for part in value.split(","))
        value = f"{first} {last}"
    name = _LEADING_GROUP.sub("", value)
    words = _words(name)
    if len(_words(value)) >= 2:
        full.append(_words(value))
    if len(words) >= 2:
        # "Arben Krasniqi", "Krasniqi Arben", "Krasniqi, Arben", also with the split the other
        # way round for a name given surname first. A title before it stays in the text: the
        # model may see "Herr", and it is not part of the value that comes back.
        firsts, surname = _person_split(words)
        full += [words, [*surname, *firsts], [*surname, ",", *firsts]]
        full += [[words[0], ",", *words[1:]], [*words[1:], words[0]]]
    for w in words:
        if _single(w):
            single.append(w)
        if "-" in w:  # "Muster-Keller": "Frau Muster" and "Frau Keller" are both written
            single += [h for h in w.split("-") if _single(h)]
    return full, single, " ".join(words)


def _pattern(words: list[str]) -> str:
    out = ""
    for w in words:
        if w == ",":
            out += _COMMA
        else:
            out += (_GAP if out and not out.endswith(_COMMA) else "") + re.escape(w)
    return out


def known_detector(
    entries: Iterable[str | tuple[str, str]],
) -> Callable[[str], Iterator[Candidate]]:
    """A detector for ``anonymize(detectors=[...])`` that always finds the given names.

    ``entries``: names as strings, or ``(kind, name)`` with kind ``"PERSON"`` or ``"ORG"``.
    A string with a legal form ("… GmbH"), "Verein …" or a trade ("Bäckerei …") is a company,
    any other a person. At most ``MAX_ENTRIES`` names.
    """
    by_kind: dict[str, tuple[dict[str, str | None], dict[str, str]]] = {}
    for count, entry in enumerate(entries, 1):
        kind, value = entry if isinstance(entry, tuple) else (_kind(entry), entry)
        if kind not in ("PERSON", "ORG"):
            raise ValueError(f"unsupported kind {kind!r}, expected PERSON or ORG")
        if count > MAX_ENTRIES:
            raise ValueError(f"more than {MAX_ENTRIES} known names")
        full, single, key = _forms(kind, value)
        fulls, singles = by_kind.setdefault(kind, ({}, {}))
        for words in full:
            for variant in _variants(" ".join(words)):
                f = _pattern(variant.split(" "))
                # A form two names share ("Martin Thomas", "Thomas Martin" reversed) gets no
                # key: each spelling keeps its own placeholder and restore() stays right.
                known = fulls.setdefault(f, key)
                if known is not None and known.casefold() != key.casefold():
                    fulls[f] = None
        for w in single:
            for variant in _variants(w):
                singles.setdefault(variant, w)

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
        compiled.append((kind, starts, keys, singles))

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
                    if (word_key := words.get(m[0])) is not None:
                        yield Candidate(kind, m.start(), m.end(), WORD, "known-word", key=word_key)

    return detect
