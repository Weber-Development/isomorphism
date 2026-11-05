---
title: Recognisers
description: Formats, checks and confidence per kind.
---

| Kind | Confidence | Notes |
|---|---|---|
| `AHV` | 0.99 valid, 0.60 wrong check digit | Dotted form. Without dots: 0.90 and 0.40 |
| `IBAN` | 0.99 valid, 0.60 wrong check digit | `CH` and `LI`, 21 characters |
| `UID` | 0.98 valid, 0.60 wrong check digit | `CHE` and nine digits. `MWST`, `TVA`, `IVA`, `HR` are not part of the match |
| `PHONE` | 0.95 with `+41` or `0041`, 0.85 with separators, 0.60 for ten bare digits | Area code 2 to 9 |
| `EMAIL` | 0.95 | |
| `PERSON` | 0.90 after a title (`Hr.`, `Frau`, `Dr.`, `Dr. med. dent.`, `M.`, `Mme`, `Me`, `Fam.`, `Notar`, `signora`, `avv.` …), 0.80 first name plus surname, 0.70 `Muster, Anna` or an initial (`B. Bürgi`), 0.65 after a context word (`Mieter:`, `Gutschrift`, `Zahlbar durch`, `CC:`, `Lieber` …) or under a closing formula, 0.60 `X und Y`, surname first at the end of an entry, or a name word of a found person again, 0.45 a first name alone | A list of common first names of many origins and Swiss short forms. Up to two name words after a title (three with a known first name). Lines in capitals and chats without capitals are read as if written normally |
| `ORG` | 0.85 legal form after the name, 0.75 legal form in front (`Verein …`, `…genossenschaft …`), 0.60 a trade or institution and a name (`Bäckerei Lüthi`, `Bank Emmental`, `Gashi Gipserei`) | Up to four words before AG, GmbH, SA, Sàrl, Sagl, KlG, KG, Ltd, Inc, LLC, Genossenschaft, Stiftung, `& Cie`; particles and `& Co.` inside. Leading articles and labels are trimmed |
| `ADDRESS` | 0.95 street and postcode together, 0.80 street with number, 0.75 postcode and place with `CH-` or `PLZ`, 0.55 postcode and place alone | Street words in German, French, Italian and English, abbreviations (`Bahnhofstr.`, `Bahnhofpl.`, `Rte`, `Ch.`, `Pl.`, `V.`), `Postfach`. Any words with a number count when postcode and place follow (`Im Grund 11, 8952 Schlieren`). A canton after the place (`Wil SG`) belongs to it. Alone, a postcode needs a line start, comma, preposition or legal form before it (or a line in capitals), and 1900 to 2099 is read as a year unless marked |
| `DOB` | 0.90 | Only a date after `geb.`, `Geburtsdatum`, `né le`, `nata il`, `date of birth` and similar. A date without such a word is not touched |
| `CARD` | 0.95 valid, 0.50 wrong check digit | 16 digits in groups of four, 19 digits, or Amex 4-6-5, Luhn |
| `ACCOUNT` | 0.90 valid, 0.40 wrong check digit (PostFinance `80-12345-6`), 0.80 digits after `Konto`, `compte`, `conto`, `account` | The context form needs at least six digits |

Known names (`isomorphism.known.known_detector`, see the guide): 0.99 for a full name in any case or order, 0.6 for a single capitalised word of it.

Wrong check digits are reported on purpose: a typo in a document is still personal data.

When two hits overlap, the higher confidence wins, then the longer match. This is why the digits inside an IBAN do not also come out as a phone number.

Authorities (`Steueramt …`, `Handelsregisteramt …`, `Bundesamt …`, `Gemeinde …`, `Kanton …`, `Commune de …`, `Tax Office …`, …) are never replaced as person, company or address.

Not recognised: foreign IBANs, the old 11-digit AHV format, service numbers such as `0800 …`.
