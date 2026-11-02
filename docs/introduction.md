---
title: Why Isomorphism
description: Replace Swiss personal data with placeholders before a model call and restore it afterwards, fully local.
---

A language model does not need to know a client's AHV number, IBAN or phone number to summarise a letter or answer a question about it. Isomorphism replaces such values with placeholders like `[AHV_1]` before the text leaves your system, and puts the real values back into the answer.

- **Swiss formats first.** AHV numbers, IBANs of Switzerland and Liechtenstein, UID numbers, Swiss phone numbers and email addresses, with the check digits that Swiss documents carry.
- **Reversible.** The same value always gets the same placeholder, so the model can follow who is meant. `restore` swaps the real values back in.
- **Local.** Pure Python, no dependencies, no network calls, no telemetry. The mapping with the real values never leaves your process unless you send it somewhere.
- **Audit-friendly.** Each hit reports kind, position, confidence and recogniser, never the value.

## Limits

Isomorphism recognises patterns. It does not understand context, and it cannot promise that a text is free of personal data. Names and postal addresses are not recognised in this version. See [Legal notes](legal.md).

## Packages

| Package | License | Content |
|---|---|---|
| `isomorphism` (PyPI) | MIT | Recognisers, `anonymize`, `restore`, `detect` |
