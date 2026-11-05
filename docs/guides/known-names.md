---
title: Known names
description: Always replace the names you already know, such as the clients of an office.
---

The built-in recognisers find a name without title or context only when its first name is on the list. An application usually knows many of the names that can appear: an office knows its clients. Pass them, and they are always replaced.

```python
from isomorphism import anonymize
from isomorphism.known import known_detector

clients = known_detector(["Arben Krasniqi", "Familie Muster", "Reinigung Blitzblank GmbH"])
safe, mapping = anonymize(text, detectors=[clients])
```

- **Full names** are found in any case and order: `Arben Krasniqi`, `KRASNIQI ARBEN`, `Krasniqi, Arben`, also in a chat without capitals. An entry may be written `Krasniqi, Arben`, as offices export their clients. A particle starts the surname (`Maria da Silva`, `Hans von Arx`), so `da Silva Maria` is found too. Umlauts are also found as bank statements write them (`RUEEGG` and `Ruegg` for `Rüegg`), accents also without them. All forms of one name get the same placeholder, so the model can follow who is meant; `restore()` gives back the first form seen in the text, not each spelling as it was. A title before the name (`Herr`) stays visible. Confidence 0.99, `detector == "known"`.
- **A single word** of a name (`Krasniqi`, `Arben`) is found when it is capitalised or in a line in capitals, with a placeholder of its own that all its spellings share. An entry of one word (`Keller`) is only such a single word. Surnames that are also ordinary words or places (`Keller`, `Koch`, `Weber`, `Zug`, `Pierre` …) are not replaced alone; the patterns still find them after a title. This list is best effort: German writes every noun with a capital, so a client named like a noun can be replaced where the noun is meant. Confidence 0.6, `detector == "known-word"`.
- **Groups** such as `Familie Muster`, `Erben Muster` or `Ehepaar Muster` are found as written, and `Muster` alone as above. A double surname (`Zumsteg-Keller`) also gives its halves of four letters or more.
- **Companies** are found with and without the legal form, in any case (`Reinigung Blitzblank GmbH`, `REINIGUNG BLITZBLANK GMBH`, `Reinigung Blitzblank`), and by the remaining name alone when it is a single word of four letters or more (`Blitzblank`). Quotes in the entry do not count.
- A string with a legal form, `Verein …`, `…genossenschaft …`, a trade (`Bäckerei …`), a business word (`Muster Immobilien`, `Muster Treuhand`) or `&` is a company, any other a person. A sole proprietorship with a plain name (`Hans Muster`) cannot be told from a person: pass `("ORG", name)` or `("PERSON", name)` to say it yourself. At most 5,000 names.
- When two entries share a form (`Martin Thomas` and `Thomas Martin`), that form keeps its own placeholder per spelling, so `restore()` never swaps them.

Not found yet: a name broken over two lines, initials (`A. Krasniqi`), genitive and possessive forms (`Krasniqis`, `Krasniqi's`), and hyphen variants of a name entered without hyphen. `keep=` compares the text of each hit: keeping `Arben Krasniqi` does not keep `Krasniqi, Arben`.

Build the detector once and keep it while the names do not change. The package keeps nothing between calls: holding the detector (and with it the names) is up to you. Names of authorities stay protected as for every other recogniser.

The README section "Acceptance" shows what known names add on the blind test sets: with every full name of a text known, set C reaches 76 % of the names without a title (patterns alone: 51 %) and all companies, and neither the clients nor 500 unrelated names add a false alarm.
