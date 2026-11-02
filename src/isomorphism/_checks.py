"""Check-digit algorithms. Pure functions on digit strings, no I/O."""

from __future__ import annotations


def ahv_ok(digits: str) -> bool:
    """AHV number: 13 digits, prefix 756, EAN-13 check digit."""
    if len(digits) != 13 or not digits.startswith("756"):
        return False
    total = sum(int(c) * (3 if i % 2 else 1) for i, c in enumerate(digits[:12]))
    return (10 - total % 10) % 10 == int(digits[12])


def iban_ok(compact: str) -> bool:
    """ISO 13616 mod-97 on an IBAN without spaces."""
    if len(compact) < 5 or not compact.isalnum():
        return False
    rearranged = compact[4:] + compact[:4]
    return int("".join(str(int(c, 36)) for c in rearranged)) % 97 == 1


def uid_ok(digits: str) -> bool:
    """UID (CHE) number: 9 digits, mod-11 check digit with weights 5,4,3,2,7,6,5,4."""
    if len(digits) != 9:
        return False
    check = (
        11 - sum(int(c) * w for c, w in zip(digits[:8], (5, 4, 3, 2, 7, 6, 5, 4), strict=True)) % 11
    )
    return check != 10 and check % 11 == int(digits[8])
