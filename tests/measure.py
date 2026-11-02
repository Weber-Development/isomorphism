"""Hit rate and false alarms per kind over tests/cases.py.

`python -m tests.measure` prints the README table.
"""

from __future__ import annotations

from collections import Counter

from isomorphism import detect

from .cases import CASES

KINDS = (
    "AHV",
    "IBAN",
    "UID",
    "PHONE",
    "EMAIL",
    "PERSON",
    "ORG",
    "ADDRESS",
    "DOB",
    "CARD",
    "ACCOUNT",
)


def measure() -> dict[str, Counter[str]]:
    stats: dict[str, Counter[str]] = {k: Counter() for k in KINDS}
    for case in CASES:
        found = {(f.kind, f.start, f.end) for f in detect(case.text, case.lang)}
        for hit in case.expected & found:
            stats[hit[0]]["tp"] += 1
        for miss in case.expected - found:
            stats[miss[0]]["fn"] += 1
        for extra in found - case.expected:
            stats[extra[0]]["fp"] += 1
    return stats


def table() -> str:
    rows = ["| Kind | Expected | Found | Missed | False alarms |", "|---|---|---|---|---|"]
    for kind, c in measure().items():
        rows.append(f"| {kind} | {c['tp'] + c['fn']} | {c['tp']} | {c['fn']} | {c['fp']} |")
    return "\n".join(rows)


if __name__ == "__main__":
    print(table())
