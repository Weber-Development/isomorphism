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

- **Full names** are found in any case and in both orders: `Arben Krasniqi`, `KRASNIQI ARBEN`, `Krasniqi, Arben`, also in a chat without capitals. All forms of one name get the same placeholder, so the model can follow who is meant; `restore()` gives back the first form seen in the text. A title before the name (`Herr`) stays visible. Confidence 0.99, `detector == "known"`.
- **A single word** of a name (`Krasniqi`, `Arben`) is found when it is capitalised or in a line in capitals, with a placeholder of its own. Surnames that are also ordinary words (`Keller`, `Koch`, `Weber`, `Pierre` …) are not replaced alone; the patterns still find them after a title. Confidence 0.6, `detector == "known-word"`.
- **Groups** such as `Familie Muster`, `Erben Muster` or `Ehepaar Muster` are found as written, and `Muster` alone as above. A double surname (`Zumsteg-Keller`) also gives its halves of four letters or more.
- **Companies** are found with and without the legal form (`Reinigung Blitzblank GmbH`, `Reinigung Blitzblank`), and by the remaining name alone when it is a single word of four letters or more (`Blitzblank`).
- A string with a legal form, `Verein …`, `…genossenschaft …` or a trade (`Bäckerei …`) is a company, any other a person. Pass `("PERSON", name)` or `("ORG", name)` to say it yourself. At most 5,000 names.

Build the detector once and keep it while the names do not change. The package keeps nothing between calls: holding the detector (and with it the names) is up to you. Names of authorities stay protected as for every other recogniser.

The README section "Acceptance" shows what known names add on the blind test sets: with every full name of a text known, set C reaches 76 % of the names without a title (patterns alone: 51 %) and all companies, and 500 unrelated names cost no precision.
