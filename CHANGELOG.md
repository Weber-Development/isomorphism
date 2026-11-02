# Changelog

## 0.2.0

- New recognisers: persons (titles, first-name list, surname again later in the text, first name alone), companies by legal form, addresses (street with number, postcode and place), dates of birth after context words, card numbers (Luhn) and accounts (PostFinance mod 10, or digits after `Konto`, `compte`, `conto`, `account`).
- Streaming: `Restorer` and `restore_stream` restore an answer that arrives in pieces, also when a placeholder is split.
- Authorities (`Steueramt St. Gallen`, `Handelsregisteramt Zürich`, …) are not replaced; `protect_authorities=False` switches it off.
- `keep` also accepts compiled patterns.
- `detectors=[…]` adds recognisers; `isomorphism.presidio.presidio_detector` wraps a Presidio `AnalyzerEngine` (optional, not a dependency, nothing downloaded).
- More invented test texts (card, account, birth date, address, name, look-alikes) and measurement for every kind in the README.

## 0.1.0

First release.

- Recognisers for AHV numbers (EAN-13), IBANs of Switzerland and Liechtenstein (mod 97), UID numbers (mod 11), Swiss phone numbers and email addresses.
- `anonymize(text, lang=None, keep=())` returns the text with placeholders and a mapping; `restore(text, mapping)` reverses it; `detect(text)` returns the hits only.
- Same value, same placeholder. Findings carry kind, position, confidence, recogniser and checksum result, never the value.
- Invented test texts in German, French, Italian and English with hit rate and false alarms per kind.
