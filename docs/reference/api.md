---
title: API
description: anonymize, restore, detect, Finding and Mapping.
---

## `anonymize(text, lang=None, *, keep=())`

Returns `(text_with_placeholders, mapping)`.

- `lang`: `"de"`, `"fr"`, `"it"`, `"en"` or `None` (a region such as `"de-CH"` is accepted). Anything else raises `ValueError`. It has no effect yet; it will select context words for names and addresses.
- `keep`: values that stay in the text. Matching is exact and case-insensitive.

Identical values get the same placeholder inside one call. A placeholder that already stands in the input text, like a literal `[AHV_1]`, is never reused.

## `restore(text, mapping)`

Replaces placeholders with the real values in one pass. Models sometimes change the case or add spaces inside the brackets (`[ahv_1]`, `[ AHV_1 ]`); both still match. Placeholders that are not in the mapping stay unchanged. `mapping` can be any `dict[str, str]`, for example one you loaded from your own storage.

## `detect(text, lang=None, *, keep=())`

Returns `list[Finding]` without changing the text.

## `Finding`

| Field | Meaning |
|---|---|
| `kind` | `AHV`, `IBAN`, `UID`, `PHONE`, `EMAIL` |
| `start`, `end` | Position in the original text |
| `confidence` | 0 to 1 |
| `detector` | Name of the recogniser, for example `ahv-ean13` |
| `checksum_ok` | `True` or `False` for AHV, IBAN and UID, `None` for the others |
| `placeholder` | The placeholder used (empty from `detect`) |

A `Finding` holds no value.

## `Mapping`

A `dict` from placeholder to real value with a `findings` list. `repr()` and `str()` show only the number of placeholders, so the values do not end up in logs by accident. The package does not log anything.
