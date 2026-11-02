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
| `PERSON` | 0.90 after a title (`Hr.`, `Frau`, `Dr.`, `M.`, `Mme`, `signora` …), 0.80 first name plus surname, 0.70 `Muster, Anna`, 0.60 the surname again, 0.45 a first name alone | About 440 common first names, no names of other origins. Needs a capital letter |
| `ORG` | 0.85 | Up to four capitalised words before AG, GmbH, SA, Sàrl, Sagl, KlG, KG, Ltd, Inc, LLC, Genossenschaft, Stiftung. Leading articles and labels are trimmed |
| `ADDRESS` | 0.95 street and postcode together, 0.80 street with number, 0.75 postcode and place with `CH-` or `PLZ`, 0.55 postcode and place alone | Street words in German, French, Italian and English. Alone, a postcode needs a line start, comma or preposition before it, and 1900 to 2099 is read as a year unless marked |
| `DOB` | 0.90 | Only a date after `geb.`, `Geburtsdatum`, `né le`, `nata il`, `date of birth` and similar. A date without such a word is not touched |
| `CARD` | 0.95 valid, 0.50 wrong check digit | 16 digits in groups of four, 19 digits, or Amex 4-6-5, Luhn |
| `ACCOUNT` | 0.90 valid, 0.40 wrong check digit (PostFinance `80-12345-6`), 0.80 digits after `Konto`, `compte`, `conto`, `account` | The context form needs at least six digits |

Wrong check digits are reported on purpose: a typo in a document is still personal data.

When two hits overlap, the higher confidence wins, then the longer match. This is why the digits inside an IBAN do not also come out as a phone number.

Authorities (`Steueramt …`, `Handelsregisteramt …`, `Bundesamt …`, `Tax Office …`, …) are never replaced as person, company or address.

Not recognised: foreign IBANs, the old 11-digit AHV format, service numbers such as `0800 …`.
