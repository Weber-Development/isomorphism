---
title: API
description: anonymize, restore, detect, Finding and Mapping.
---

## `anonymize(text, lang=None, *, keep=(), detectors=(), protect_authorities=True)`

Returns `(text_with_placeholders, mapping)`.

- `lang`: `"de"`, `"fr"`, `"it"`, `"en"` or `None` (a region such as `"de-CH"` is accepted). Anything else raises `ValueError`. It has no effect: all four languages are always active, because Swiss texts mix them.
- `keep`: values that stay in the text: exact strings (case-insensitive) or compiled patterns that must match the whole value.
- `detectors`: extra recognisers, for example `presidio_detector(...)` from `isomorphism.presidio`.
- `protect_authorities`: names such as "Steueramt St. Gallen" are not replaced (default `True`).

Identical values get the same placeholder inside one call. A placeholder that already stands in the input text, like a literal `[AHV_1]`, is never reused.

## `restore(text, mapping)`

Replaces placeholders with the real values in one pass. Models sometimes change the case or add spaces inside the brackets (`[ahv_1]`, `[ AHV_1 ]`); both still match. Placeholders that are not in the mapping stay unchanged. `mapping` can be any `dict[str, str]`, for example one you loaded from your own storage.

## `detect(text, lang=None, *, keep=(), detectors=(), protect_authorities=True)`

Returns `list[Finding]` without changing the text.

## `restore_stream(chunks, mapping)` and `Restorer(mapping)`

`restore_stream` takes an iterable of text pieces and yields restored pieces. `Restorer.feed(piece)` does the same step by step; call `Restorer.flush()` after the last piece. An end that could be the start of a placeholder (`[AHV_`) is held back until the next piece or the flush, so a placeholder split between two pieces is restored. At most 40 characters are held back.

## `Finding`

| Field | Meaning |
|---|---|
| `kind` | `AHV`, `IBAN`, `UID`, `PHONE`, `EMAIL`, `PERSON`, `ORG`, `ADDRESS`, `DOB`, `CARD`, `ACCOUNT` |
| `start`, `end` | Position in the original text |
| `confidence` | 0 to 1 |
| `detector` | Name of the recogniser, for example `ahv-ean13` |
| `checksum_ok` | `True` or `False` for AHV, IBAN, UID, CARD and PostFinance accounts, `None` for the others |
| `placeholder` | The placeholder used (empty from `detect`) |

A `Finding` holds no value.

## `Mapping`

A `dict` from placeholder to real value with a `findings` list. `repr()` and `str()` show only the number of placeholders, so the values do not end up in logs by accident. The package does not log anything.
