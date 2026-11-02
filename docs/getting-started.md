---
title: Getting started
description: Install Isomorphism, anonymise a text, call a model and restore the answer.
---

```sh
pip install isomorphism
```

Python 3.12 or newer.

## Anonymise and restore

```python
from isomorphism import anonymize, restore

text = "Hr. Keller, AHV 756.1234.5678.97, IBAN CH93 0076 2011 6238 5295 7, UID CHE-123.456.788 MWST"
safe, mapping = anonymize(text)
print(safe)  # [PERSON_1], AHV [AHV_1], IBAN [IBAN_1], UID [UID_1] MWST

answer = call_your_model(safe)
print(restore(answer, mapping))
```

Keep the mapping for as long as the request runs, for example in a variable or your request context. If you need to keep it longer, `dict(mapping)` gives you a plain dictionary to store. The package never writes it anywhere.

## Keep some values

```python
safe, mapping = anonymize(text, keep=["info@gemeinde.example"])  # strings or compiled patterns
```

## Audit log

```python
for f in mapping.findings:
    print(f.kind, f.start, f.end, f.confidence, f.detector, f.checksum_ok)
```

Positions refer to the original text. The findings contain no values, so they are safe to log.
