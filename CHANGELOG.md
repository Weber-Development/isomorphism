# Changelog

## 0.1.0

First release.

- Recognisers for AHV numbers (EAN-13), IBANs of Switzerland and Liechtenstein (mod 97), UID numbers (mod 11), Swiss phone numbers and email addresses.
- `anonymize(text, lang=None, keep=())` returns the text with placeholders and a mapping; `restore(text, mapping)` reverses it; `detect(text)` returns the hits only.
- Same value, same placeholder. Findings carry kind, position, confidence, recogniser and checksum result, never the value.
- Invented test texts in German, French, Italian and English with hit rate and false alarms per kind.
