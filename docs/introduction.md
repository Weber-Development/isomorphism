---
title: Why Isomorphism
description: Replace Swiss personal data with placeholders before a model call and restore it afterwards, fully local.
---

A language model does not need to know a client's AHV number, IBAN or phone number to summarise a letter or answer a question about it. Isomorphism replaces such values with placeholders like `[AHV_1]` before the text leaves your system, and puts the real values back into the answer.

- **Swiss formats first.** AHV numbers, IBANs of Switzerland and Liechtenstein, UID numbers, Swiss phone numbers, email addresses, names, companies, addresses, dates of birth, card and account numbers, with the check digits that Swiss documents carry.
- **Four languages.** German (also Swiss spellings), French, Italian and English in one pass.
- **Reversible.** The same value always gets the same placeholder, so the model can follow who is meant. `restore` swaps the real values back in.
- **Local.** Pure Python, no dependencies, no network calls, no telemetry. The mapping with the real values never leaves your process unless you send it somewhere. [Streaming answers](guides/fastapi.md) are restored while they arrive.
- **Audit-friendly.** Each hit reports kind, position, confidence and recogniser, never the value.

## Limits

Isomorphism recognises patterns. It does not understand context, and it cannot promise that a text is free of personal data. Names, companies and addresses are found with patterns, a list of first names and context words, so they are less certain than the checksum kinds; [Presidio](guides/presidio.md) can be added for names in running text. See [Legal notes](legal.md).

## Packages

| Package | License | Content |
|---|---|---|
| `isomorphism` (PyPI) | MIT | Recognisers, `anonymize`, `restore`, `restore_stream`, `detect`, optional Presidio adapter |
