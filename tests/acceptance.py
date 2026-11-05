"""Acceptance for persons, companies and addresses, on texts written blind.

`tests/acceptance_a.py` and `tests/acceptance_b.py` were written by a second reviewer who did not
read the recognisers, as a fiduciary office would write: emails, payslips, bank booking texts,
notes. Everything is invented. `python -m tests.acceptance` prints the README table.

A marked value counts as protected when every letter and digit of it lies inside some placeholder
(of any kind): what the model must not see is the value, not the label. A partial hit that leaves
"Muster" visible counts as missed. A false alarm is a hit that touches no marked value.
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from dataclasses import dataclass

from isomorphism import detect
from isomorphism.known import known_detector

from . import acceptance_a, acceptance_b, acceptance_c
from .cases import Case, _parse

KINDS = ("PERSON", "ORG", "ADDRESS")

# Agreed before the recognisers were changed (Claude and a second reviewer, see README
# "Acceptance"). Tier 1 is what a recogniser must never miss: a name with a salutation or
# title, a company with its legal form, street and number with postcode and place. Tier 2 is
# everything else (a first name alone, lowercase chat, a company without legal form ...).
TIER1 = {
    "PERSON": re.compile(
        r"(?:Herrn?|Frau|Hr\.|Fr\.|Dr\.|Prof\.|M\.|Mme|Me|Monsieur|Madame|Signora?|avv\.|"
        r"Fam\.|Familie|Notar|Mrs?\.?|Ms\.?)\s"
    ),
    "ORG": re.compile(r".*\s(?:AG|GmbH|SA|Sàrl|Sagl|KlG|KG|Ltd|Inc|LLC)$"),
    "ADDRESS": re.compile(r".*\d+\s?[a-zA-Z]?,?\s+(?:CH-)?\d{4}\s+\S"),
}
MIN_PROTECTED = {
    1: {"PERSON": 1.0, "ORG": 1.0, "ADDRESS": 1.0},
    2: {"PERSON": 0.80, "ORG": 0.80, "ADDRESS": 0.90},
}
# Share of hits of a kind that touch a marked value. A false alarm costs the model some
# context, a miss leaks a value, so this is looser than the protection above.
MIN_PRECISION = 0.80
# No hit may touch an authority: the model needs to know who is asking.
AUTHORITY = re.compile(
    r"Steuer(?:amt|verwaltung)|Gemeinde|Kanton|Ausgleichskasse|ESTV|Commune|Canton|"
    r"Administration|Revisionsstelle"
)

SETS = {
    "A": [_parse(*row) for row in acceptance_a.RAW],
    "B": [_parse(*row) for row in acceptance_b.RAW],
    "C": [_parse(*row) for row in acceptance_c.RAW],
}


def tier(kind: str, value: str) -> int:
    return 1 if TIER1[kind].match(value) else 2


@dataclass
class Miss:
    case: str
    kind: str
    value: str
    visible: str  # what stays in the text


def _covered(case: Case, spans: list[tuple[int, int]], start: int, end: int) -> str:
    """The letters and digits of text[start:end] that no span covers."""
    return "".join(
        c
        for i, c in enumerate(case.text[start:end], start)
        if c.isalnum() and not any(s <= i < e for s, e in spans)
    )


Stats = dict[tuple[str, int], Counter[str]]


# Known names: the office passes its clients. "clients" simulates the best case, every person
# and company whose full name is marked in a text is a client; "strangers" passes 500 invented
# names that appear in no text, to show that a long client list costs no precision.
_SYL1 = "Hin Wal Brun Tschan Mor Zur Kel Lin Sut Rüe".split()
_SYL2 = "egger mattli wiler bühler matter".split()
_FIRST = "Ottilia Fridolin Arbnora Severin Livia Ramun Dragana Jolanda Ueli Mirela".split()
STRANGERS = [f"{f} {a}{b}" for f in _FIRST for a in _SYL1 for b in _SYL2]
_STRANGERS = known_detector(STRANGERS)


def _detectors(case: Case, known: str | None) -> list:  # type: ignore[type-arg]
    if known == "clients":
        # A client list holds full names: only marked values of two words or more are passed,
        # so a surname or first name alone in the text is measured, not handed over.
        values = [
            (k, case.text[s:e])
            for k, s, e in case.expected
            if k in ("PERSON", "ORG") and len(case.text[s:e].split()) >= 2
        ]
        return [known_detector(values)] if values else []
    if known == "strangers":
        return [_STRANGERS]
    return []


def score(
    cases: list[Case], known: str | None = None
) -> tuple[Stats, Counter[str], list[Miss], list[str]]:
    """Per (kind, tier): expected, protected. Per kind: hits and false hits. Misses, and the
    false hits on authorities. ``known``: None, "clients" or "strangers" (see above)."""
    stats: Stats = {(k, t): Counter() for k in KINDS for t in (1, 2)}
    hits: Counter[str] = Counter()
    misses: list[Miss] = []
    on_authority: list[str] = []
    for case in cases:
        findings = detect(case.text, case.lang, detectors=_detectors(case, known))
        spans = [(f.start, f.end) for f in findings]
        for kind, start, end in case.expected:
            if kind not in KINDS:
                continue
            value = case.text[start:end]
            c = stats[(kind, tier(kind, value))]
            c["expected"] += 1
            visible = _covered(case, spans, start, end)
            if visible:
                misses.append(Miss(case.name, kind, value, visible))
            else:
                c["protected"] += 1
        for f in findings:
            if f.kind not in KINDS:
                continue
            hits[f.kind] += 1
            if not any(s < f.end and f.start < e for _, s, e in case.expected):
                hits[f.kind + "_false"] += 1
                line_start = case.text.rfind("\n", 0, f.start) + 1
                context = case.text[line_start : f.end + 40]
                if AUTHORITY.search(case.text[f.start : f.end]) or AUTHORITY.search(
                    case.text[max(line_start, f.start - 25) : f.end]
                ):
                    on_authority.append(f"{case.name}: {context!r}")
    return stats, hits, misses, on_authority


def failures(
    cases: list[Case], tiers: tuple[int, ...] = (1, 2), known: str | None = None
) -> list[str]:
    stats, hits, _, on_authority = score(cases, known)
    out = [f"authority replaced in {a}" for a in on_authority]
    for (kind, t), c in stats.items():
        if t in tiers and c["expected"] and c["protected"] / c["expected"] < MIN_PROTECTED[t][kind]:
            out.append(f"{kind} tier {t}: {c['protected']}/{c['expected']} protected")
    for kind in KINDS:
        if hits[kind] and 1 - hits[kind + "_false"] / hits[kind] < MIN_PRECISION:
            out.append(f"{kind}: {hits[kind + '_false']} of {hits[kind]} hits are false")
    return out


def known_table() -> str:
    """Tier 2 and false alarms with known names, next to the patterns alone."""
    rows = [
        "| Set | Kind | Tier 2, patterns | Tier 2, clients known | False alarms, 500 strangers |",
        "|---|---|---|---|---|",
    ]
    for name, cases in SETS.items():
        runs = [score(cases, k) for k in (None, "clients", "strangers")]
        for kind in KINDS:
            if kind == "ADDRESS":
                continue
            cells = []
            for stats, *_ in runs[:2]:
                c = stats[(kind, 2)]
                n = c["expected"]
                cells.append(f"{c['protected']}/{n} ({c['protected'] / (n or 1):.0%})")
            hits = runs[2][1]
            false = f"{hits[kind + '_false']} of {hits[kind]} hits"
            rows.append(f"| {name} | {kind} | {cells[0]} | {cells[1]} | {false} |")
    return "\n".join(rows)


def table() -> str:
    rows = [
        "| Set | Kind | Tier 1 protected | Tier 2 protected | False alarms |",
        "|---|---|---|---|---|",
    ]
    for name, cases in SETS.items():
        stats, hits, _, _ = score(cases)
        for kind in KINDS:
            cells = []
            for t in (1, 2):
                c = stats[(kind, t)]
                n = c["expected"]
                cells.append(f"{c['protected']}/{n} ({c['protected'] / (n or 1):.0%})")
            false = f"{hits[kind + '_false']} of {hits[kind]} hits"
            rows.append(f"| {name} | {kind} | {cells[0]} | {cells[1]} | {false} |")
    return "\n".join(rows)


if __name__ == "__main__":
    print(table())
    print()
    print(known_table())
    if "-v" in sys.argv:
        for name, cases in SETS.items():
            result = score(cases)
            for m in result[2]:
                t = tier(m.kind, m.value)
                print(f"{name} {m.case}: T{t} {m.kind} {m.value!r} shows {m.visible!r}")
            for case in cases:
                for f in detect(case.text, case.lang):
                    if f.kind in KINDS and not any(
                        s < f.end and f.start < e for _, s, e in case.expected
                    ):
                        print(f"{name} {case.name}: false {f.kind} {case.text[f.start : f.end]!r}")
            for a in result[3]:
                print(f"{name} AUTHORITY {a}")
