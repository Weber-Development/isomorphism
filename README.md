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
| Person | `[PERSON_n]` | `Hr. Keller`, `Frau Dr. Patrizia Caflisch`, `Mme Aurélie Dos Santos`, `Fam. Gashi`, `B. Bürgi`, `Anna Muster`, `Muster, Anna`; names after `Mieter:`, `Gutschrift`, `CC:`, `Lieber`, under `Freundliche Grüsse`; every name word again later in the text | titles, initials, context words, first-name list |
| Company | `[ORG_n]` | name before AG, GmbH, SA, Sàrl, Sagl, KlG, KG, Ltd, Inc, LLC …; `Verein …`, `Wohnbaugenossenschaft …`; a trade and a name (`Bäckerei Lüthi`, `Notariat Zumstein & Partner`) | legal form, trade words |
| Address | `[ADDRESS_n]` | `Musterstrasse 12, 9000 St. Gallen`, `Bahnhofstr. 3, 9500 Wil SG`, `Im Grund 11, 8952 Schlieren`, `Rue de Lausanne 12, 1003 Lausanne`, `Via S. Gottardo 14`, `Postfach 248, 9001 St. Gallen`, `12 Baker Street`, `CH-9000 St. Gallen` | street words, postcode |
| Date of birth | `[DOB_n]` | a date after `geb.`, `Geburtsdatum`, `né le`, `nata il`, `date of birth` … | context word |
| Card number | `[CARD_n]` | 16 digits (`4111 1111 1111 1111`), Amex | Luhn |
| Account | `[ACCOUNT_n]` | PostFinance `80-12345-6`; digits after `Konto`, `compte`, `conto`, `account` | mod 10 / context word |

Lines in capitals (`HANS-PETER AEBERSOLD`, bank bookings, payment slips) and chat messages without capitals (`hoi sandra, frau meier-huber fragt …`) are read as if written normally, at the same positions.

`detect(text)` returns the hits without changing the text.

- **Exceptions:** `keep=["info@gemeinde.example", re.compile(r".*@gemeinde\.example")]` leaves exact values (case-insensitive) or values matching a pattern untouched.
- **Authorities:** names such as "Steueramt St. Gallen", "Handelsregisteramt Zürich", "Gemeinde Wil" or "Kanton St. Gallen" are not replaced (`protect_authorities=True`, the default).
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
- Names, companies and addresses are heuristics (titles, initials, context words, a list of common first names of many origins, legal forms, trade and street words). They find less than a language model would and can over-report. A person written two ways (`Anna Muster`, then `Muster`) gets two placeholders.
- This is a small invented set, not a benchmark on real documents. Test with your own (invented) samples before you rely on it.

## Acceptance

Names, companies and addresses are heuristics, so they get their own acceptance, agreed before the recognisers were changed. Test texts are written blind by a reviewer who has not read the code, the word lists or the earlier sets, the way a fiduciary office writes: emails, payslips, bank bookings in capitals, chats in lower case, notes, signatures. Everything is invented.

- **Protected** means every letter and digit of the value lies inside a placeholder of any kind. A partial hit that leaves `Muster` visible counts as missed.
- **Tier 1, never missed (100 %):** a name with a salutation or title, a company with its legal form, street and number with postcode and place.
- **Tier 2, everything else:** at least 80 % of names, 80 % of companies and 90 % of addresses.
- **Precision:** at least 80 % of the hits of each kind touch a marked value. A false alarm costs the model some context; a miss leaks a value.
- **Authorities:** never replaced.

Set A was used for the first round of changes. Set B, written blind, showed what that round did not generalise, and the second round fixed the structural classes from B. Set C was then written blind by a fresh reviewer and decided the acceptance.

**Result: 0.3.0 does not pass the whole acceptance.** On set C as counted, tier 1 held for persons and companies (100 %) and reached 86 % for addresses; tier 2 reached 45 % of names, 54 % of companies and 53 % of addresses. Afterwards only the three tier-1 address layouts from C (`/` or tab before the postcode, a house number range `140-142`) and two structural classes (double first names with one known half, `V.le`) were fixed, so C is no longer blind. Tier 1 is now complete on all three sets. Tier 2 stays below the minimum on C for all three kinds (names 51 %, companies 54 %, addresses 63 %): names without a title or context word are found only when the first name is on the list, companies without legal form only after a known trade word. Until a recogniser with a language model is added, use 0.3.0 as one layer, not as the only protection for real documents.

All three sets stay as regression tests. `python -m tests.acceptance -v` prints the table below and every miss.

<!-- acceptance:start -->
| Set | Kind | Tier 1 protected | Tier 2 protected | False alarms |
|---|---|---|---|---|
| A | PERSON | 24/24 (100%) | 38/40 (95%) | 0 of 62 hits |
| A | ORG | 24/24 (100%) | 4/4 (100%) | 0 of 28 hits |
| A | ADDRESS | 27/27 (100%) | 7/7 (100%) | 0 of 31 hits |
| B | PERSON | 26/26 (100%) | 85/87 (98%) | 2 of 114 hits |
| B | ORG | 25/25 (100%) | 16/16 (100%) | 0 of 41 hits |
| B | ADDRESS | 24/24 (100%) | 20/21 (95%) | 0 of 36 hits |
| C | PERSON | 33/33 (100%) | 39/76 (51%) | 4 of 84 hits |
| C | ORG | 18/18 (100%) | 14/26 (54%) | 0 of 31 hits |
| C | ADDRESS | 21/21 (100%) | 12/19 (63%) | 0 of 34 hits |
<!-- acceptance:end -->

For comparison, 0.2.0 protected 42 %, 50 % and 27 % (A, B, C) of the tier-1 names, 70 %, 75 % and 71 % of the tier-1 addresses, and 4 % of the tier-2 names on C.

### Known names

An office knows its clients. Passed with `known_detector` (see `docs/guides/known-names.md`), their names are always replaced. The table simulates the best case: every person and company whose full name (two words or more) is marked in a text is passed as a client, so a surname or first name alone is still measured, not handed over. The false alarms compare the patterns alone, the clients run and a run with 500 invented names that appear in no text: neither adds a false alarm to those of the patterns.

<!-- known:start -->
| Set | Kind | Tier 2, patterns | Tier 2, clients known | False alarms: patterns / clients known / 500 strangers |
|---|---|---|---|---|
| A | PERSON | 38/40 (95%) | 39/40 (98%) | 0 of 62 / 0 of 63 / 0 of 62 |
| A | ORG | 4/4 (100%) | 4/4 (100%) | 0 of 28 / 0 of 28 / 0 of 28 |
| B | PERSON | 85/87 (98%) | 85/87 (98%) | 2 of 114 / 2 of 113 / 2 of 114 |
| B | ORG | 16/16 (100%) | 16/16 (100%) | 0 of 41 / 0 of 41 / 0 of 41 |
| C | PERSON | 39/76 (51%) | 58/76 (76%) | 4 of 84 / 4 of 95 / 4 of 84 |
| C | ORG | 14/26 (54%) | 26/26 (100%) | 0 of 31 / 0 of 44 / 0 of 31 |
<!-- known:end -->

With known clients, set C protects 76 % of the names without a title, still below the 80 % minimum: what remains are people whose full name never appears in the text (children, `Gion`, a surname in a member list) and lower-case chats, where only full names are matched. Companies reach 100 %. The 500 unrelated names add no false alarm.

What still gets through, by structure:

- **Names without any trigger** when the first name is not on the list (rarer names, many names of other origins), and table columns such as `Name;Vorname` without labels.
- **A surname or a first name alone** (a child, "Schreiner Bühler") when the full name does not appear earlier in the same text.
- **Lower-case chats** with names that are not on the list.
- **Companies without legal form** whose first word is not a known trade or institution (`Physio am Bach`, `Frauenchor Oberdorf`), and name parts around `&` or `+` outside the legal-form match (`Brunschwiler & Hossmann Architekten`).
- **Addresses** in table cells with `;` between postcode and place, and foreign formats.
- **False alarms:** a title before a brand (`Dr. Bohne`), a field after a job title (`Leiterin Finanzen`), the month `August` next to a name.

## Limits

`lang` ("de", "fr", "it", "en") is accepted and checked but has no effect: all four languages are always active, because Swiss texts mix them. Foreign IBANs, the old 11-digit AHV format and service numbers such as `0800 …` are not recognised. The first-name list covers common names of many origins in Switzerland, not all; other names are found with a title, an initial, a context word, as known names, or through Presidio.

No tool finds all personal data. Treat the result as one protective layer, not as a guarantee of anonymity.

## Development

```sh
uv venv && uv pip install -e . pytest ruff mypy
ruff check . && ruff format --check . && mypy && pytest
```

Docs: <https://packages.sweber.dev/isomorphism/docs>
