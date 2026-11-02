---
title: Recognisers
description: Formats, checks and confidence per kind.
---

| Kind | Confidence | Notes |
|---|---|---|
| `AHV` | 0.99 valid, 0.60 wrong check digit | Dotted form. Without dots: 0.90 and 0.40 |
| `IBAN` | 0.99 valid, 0.60 wrong check digit | `CH` and `LI`, 21 characters |
| `UID` | 0.98 valid, 0.60 wrong check digit | `CHE` and nine digits. `MWST`, `TVA`, `IVA`, `HR` are not part of the match |
| `PHONE` | 0.95 with `+41` or `0041`, 0.85 with separators, 0.60 for ten bare digits | Area code 2 to 9 |
| `EMAIL` | 0.95 | |

Wrong check digits are reported on purpose: a typo in a document is still personal data.

When two hits overlap, the higher confidence wins, then the longer match. This is why the digits inside an IBAN do not also come out as a phone number.

Not recognised: foreign IBANs, the old 11-digit AHV format, service numbers such as `0800 …`.
