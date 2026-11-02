# isomorphism

Reversible anonymisation of Swiss personal data for Python. It replaces AHV numbers, IBANs, UID numbers, phone numbers, emails, names, addresses, companies, dates of birth, card and account numbers with placeholders before a text goes to a language model, and puts the real values back into the answer.

- **Local only.** No network calls, no telemetry, no dependencies, nothing downloaded at runtime.
- **Reversible.** `anonymize(text)` returns the text with placeholders and a mapping, `restore(text, mapping)` undoes it, also for an answer that arrives in pieces.
- **Same value, same placeholder.** The model can follow that `[PERSON_1]` appears three times.
- **Checksums.** AHV (EAN-13), IBAN (mod 97), UID (mod 11), cards (Luhn) and PostFinance accounts (mod 10) are verified. Numbers that look right but fail the check are reported anyway, with lower confidence.
- **Audit-friendly.** Every hit comes back as kind, position, confidence and recogniser, without the value.
- **German, French, Italian and English** in one pass, including Swiss spellings.

Python 3.12 or newer. MIT license.

```sh
pip install isomorphism
```

```python
from isomorphism import anonymize, restore

text = "Hr. Keller, Musterstrasse 12, 9000 St. Gallen, AHV 756.1234.5678.97, Tel. 071 123 45 67"
safe, mapping = anonymize(text)
# '[PERSON_1], [ADDRESS_1], AHV [AHV_1], Tel. [PHONE_1]'

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
| Person | `[PERSON_n]` | `Hr. Keller`, `Frau Dr. Müller`, `M. Jean Dupont`, `signora Bianchi`, `Anna Muster`, `Muster, Anna`; the same surname or a first name alone later in the text | titles, first-name list |
| Company | `[ORG_n]` | name before AG, GmbH, SA, Sàrl, Sagl, KlG, KG, Ltd, Inc, LLC … | legal form |
| Address | `[ADDRESS_n]` | `Musterstrasse 12, 9000 St. Gallen`, `Rue de Lausanne 12, 1003 Lausanne`, `Via Nassa 8, 6900 Lugano`, `12 Baker Street`, `CH-9000 St. Gallen` | street words, postcode |
| Date of birth | `[DOB_n]` | a date after `geb.`, `Geburtsdatum`, `né le`, `nata il`, `date of birth` … | context word |
| Card number | `[CARD_n]` | 16 digits (`4111 1111 1111 1111`), Amex | Luhn |
| Account | `[ACCOUNT_n]` | PostFinance `80-12345-6`; digits after `Konto`, `compte`, `conto`, `account` | mod 10 / context word |

`detect(text)` returns the hits without changing the text.

- **Exceptions:** `keep=["info@gemeinde.example", re.compile(r".*@gemeinde\.example")]` leaves exact values (case-insensitive) or values matching a pattern untouched.
- **Authorities:** names such as "Steueramt St. Gallen" or "Handelsregisteramt Zürich" are not replaced (`protect_authorities=True`, the default).
- **Streaming:** `restore_stream(chunks, mapping)` or `Restorer(mapping)` restore an answer that arrives in pieces, also when a placeholder is split between two pieces.
- **Presidio (optional):** `anonymize(text, detectors=[presidio_detector(analyzer, language="de")])` adds names in running text from Microsoft Presidio. Presidio is not a dependency and runs locally.

## Measured on the test cases

`tests/cases.py` holds invented Swiss texts (payslip extract, client email, receipt, tax query, French and Italian letters, English mail, written-out variants, numbers with wrong check digits, and a text full of look-alikes that must not match). The numbers below come from `python -m tests.measure`. A test fails if the table is out of date, if a listed value slips through, or if the false alarms exceed what is listed here.

<!-- measure:start -->
| Kind | Expected | Found | Missed | False alarms |
|---|---|---|---|---|
| AHV | 10 | 10 | 0 | 0 |
| IBAN | 10 | 10 | 0 | 0 |
| UID | 9 | 9 | 0 | 0 |
| PHONE | 15 | 15 | 0 | 0 |
| EMAIL | 6 | 6 | 0 | 0 |
| PERSON | 10 | 10 | 0 | 0 |
| ORG | 4 | 4 | 0 | 0 |
| ADDRESS | 9 | 9 | 0 | 2 |
| DOB | 6 | 6 | 0 | 0 |
| CARD | 6 | 6 | 0 | 0 |
| ACCOUNT | 3 | 3 | 0 | 0 |
<!-- measure:end -->

Read it as follows:

- "Missed" is zero for every kind: no value in these texts gets through.
- The two address false alarms are `4500 Euro` and `1200 Meter` after a comma: a four-digit number followed by a capitalised word looks like a postcode and a place. They are reported with low confidence (0.55), so you can filter by confidence.
- Names, companies and addresses are heuristics (titles, a list of about 440 first names, legal forms, street words). They find less than a language model would and can over-report. A person written two ways (`Anna Muster`, then `Muster`) gets two placeholders.
- This is a small invented set, not a benchmark on real documents. Test with your own (invented) samples before you rely on it.

## Limits

`lang` ("de", "fr", "it", "en") is accepted and checked but has no effect: all four languages are always active, because Swiss texts mix them. Foreign IBANs, the old 11-digit AHV format and service numbers such as `0800 …` are not recognised. Names of other origins than the first-name list are found with a title or through Presidio.

No tool finds all personal data. Treat the result as one protective layer, not as a guarantee of anonymity.

## Development

```sh
uv venv && uv pip install -e . pytest ruff mypy
ruff check . && ruff format --check . && mypy && pytest
```

Docs: <https://packages.sweber.dev/isomorphism/docs>
