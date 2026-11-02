# isomorphism

Reversible anonymisation of Swiss personal data for Python. It replaces AHV numbers, IBANs, UID numbers, phone numbers and email addresses with placeholders before a text goes to a language model, and puts the real values back into the answer.

- **Local only.** No network calls, no telemetry, no dependencies, nothing downloaded at runtime.
- **Reversible.** `anonymize(text)` returns the text with placeholders and a mapping, `restore(text, mapping)` undoes it.
- **Same value, same placeholder.** The model can follow that `[AHV_1]` appears three times.
- **Checksums.** AHV (EAN-13), IBAN (mod 97) and UID (mod 11) are verified. Numbers that look right but fail the check are reported anyway, with lower confidence.
- **Audit-friendly.** Every hit comes back as kind, position, confidence and recogniser, without the value.

Python 3.12 or newer. MIT license.

```sh
pip install isomorphism
```

```python
from isomorphism import anonymize, restore

text = "Anna Muster, AHV 756.1234.5678.97, IBAN CH93 0076 2011 6238 5295 7, Tel. 071 123 45 67"
safe, mapping = anonymize(text, lang="de")
# 'Anna Muster, AHV [AHV_1], IBAN [IBAN_1], Tel. [PHONE_1]'

answer = call_your_model(safe)  # the model only sees placeholders
print(restore(answer, mapping))  # real values are back
```

The mapping holds the real values. This package never logs or stores it; keeping it (in memory, per request) is up to you. `repr(mapping)` shows only the number of placeholders.

## What it finds

| Kind | Placeholder | Formats | Check |
|---|---|---|---|
| AHV number | `[AHV_n]` | `756.1234.5678.97`, with spaces or without separators | prefix 756, EAN-13 |
| IBAN (CH, LI) | `[IBAN_n]` | with or without spaces, upper or lower case | mod 97 |
| UID number | `[UID_n]` | `CHE-123.456.788`, `CHE123456788`; `MWST`/`TVA`/`IVA`/`HR` stay in the text | mod 11 |
| Phone (Switzerland) | `[PHONE_n]` | `+41 71 123 45 67`, `0041 …`, `+41 (0)71 …`, `071 123 45 67`, `071/123 45 67`, `(071) …`, `0711234567` | format |
| Email | `[EMAIL_n]` | | format |

`detect(text)` returns the hits without changing the text. Passing `keep=["info@gemeinde.example"]` leaves exact values untouched (case-insensitive), for example the address of an authority.

## Measured on the test cases

`tests/cases.py` holds invented Swiss texts (payslip extract, client email, receipt, tax query, French and Italian letters, written-out variants, numbers with wrong check digits, and a text full of look-alikes that must not match). The numbers below come from `python -m tests.measure`, and a test fails if they are out of date or if a listed value slips through.

<!-- measure:start -->
| Kind | Expected | Found | Missed | False alarms |
|---|---|---|---|---|
| AHV | 10 | 10 | 0 | 0 |
| IBAN | 10 | 10 | 0 | 0 |
| UID | 9 | 9 | 0 | 0 |
| PHONE | 15 | 15 | 0 | 0 |
| EMAIL | 6 | 6 | 0 | 0 |
<!-- measure:end -->

This is a small invented set, not a benchmark on real documents. Read it as a regression guard, and test with your own (invented) samples before you rely on it.

## Not in this version

Personal names, postal addresses, company names, dates of birth, account and card numbers, and restoring a streamed answer arrive in the next version. Until then names and addresses stay in the text. `lang` ("de", "fr", "it", "en") is accepted and checked already but has no effect yet. Foreign IBANs and the old 11-digit AHV format are not recognised.

No tool finds all personal data. Treat the result as one protective layer, not as a guarantee of anonymity.

## Development

```sh
uv venv && uv pip install -e . pytest ruff mypy
ruff check . && ruff format --check . && mypy && pytest
```

Docs: <https://packages.sweber.dev/isomorphism/docs>
