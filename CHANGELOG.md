# Changelog

## 0.4.0

- Known names: `isomorphism.known.known_detector(names)` always replaces names the caller already knows, such as the clients of an office. Full names in any case and order (`KRASNIQI, Arben`) share one placeholder; single capitalised words of a name are found too, except surnames that are ordinary words (`Keller`, `Koch` …). Companies with and without legal form. Nothing is kept between calls.
- A recogniser can give hits a `key`: hits with the same kind and key share one placeholder although their text differs. `restore()` then gives back the first form seen.
- Acceptance: a second table shows tier 2 with known clients (set C names 51 % → 76 %, companies 54 % → 100 %) and that 500 unrelated names cost no precision.

## 0.3.1

- A postcode at the start of a line is no longer taken for postcode and place when the line next to it and at least one more of the two lines before and the two after start with a number and a word: a chart of accounts (`1000 Kasse`, `6570 Informatikaufwand`) or a price list stays in the text. A postcode line with one such neighbour (`2025 Steuererklärung`, a phone number) is still an address. Known gap: a numbered client list with `PLZ Ort` on its own line between the entries (`1001 Muster Hans\n8000 Zürich\n1002 …`), or three or more lines of `PLZ Ort` in a row, loses the place. The acceptance table is unchanged.

## 0.3.0

Persons, companies and addresses are measured against an acceptance on three blind, invented Swiss test sets (README "Acceptance"). 0.3.0 finds every name with a title, every company with a legal form and every full address in all three sets, where 0.2.0 found 27 to 50 % of those names. It does not reach the tier-2 minimum on the last blind set for any of the three kinds: names 51 % (0.2.0: 4 %), companies 54 % (0 %), addresses 63 % (47 %).

- Persons: names after a title with any first name (`Frau Dr. Patrizia Caflisch`), more titles (`Me`, `Fam.`, `Familie`, `Notar`, `avv.`, `Dr. med. dent.`), initials (`B. Bürgi`, `J.-P. Chappuis`), particles (`Dos Santos`, `van der Meer`), names after context words (`Mieter:`, `Gutschrift`, `Zahlbar durch`, `my wife`, `Lieber`, `CC:`) and under a closing formula, `X und Y`, surname first (`Krasniqi Arben,`). Double first names with one known half (`Rose-Marie`). Every name word of a found person is found again later. More first names of many origins and Swiss short forms (`Dani`, `Vreni`).
- Companies: legal form in front (`Verein …`, `…genossenschaft …`), trade and name (`Bäckerei Lüthi`, `Notariat Zumstein & Partner`, `Gashi Gipserei`), particles and `& Co.` inside names.
- Addresses: any words with number when postcode and place follow (`Im Grund 11, 8952 Schlieren`), `Postfach`, canton after the place (`Wil SG`), `Bahnhofpl.`, `Pl.`, `V.`, `Via S. Gottardo`, `Via ai Ronchi`, `V.le`, house number ranges (`140-142`), `|`, `/`, `;` or tab as separator, a postcode after `Wohnsitz:`.
- Text in capitals (bank bookings, payment slips) and chats without capitals are read as if written normally.
- Authorities: `Gemeinde X`, `Kanton X`, `Commune de X` and similar are not replaced.
- `tests/acceptance.py` with three blind sets and the agreed thresholds; the README shows the result.
- More is replaced than in 0.2.0. Overlap checks no longer grow with the square of the hits, and a word never starts inside a hyphen chain: 200,000 characters take up to about 2 s, also for adversarial input.
- Words of an authority are never reused as a name elsewhere in the text.

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
