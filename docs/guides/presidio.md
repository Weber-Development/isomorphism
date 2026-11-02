---
title: Names with Presidio
description: Add names in running text from Microsoft Presidio, locally and optional.
---

The built-in recognisers find names after a title (`Hr. Keller`), as first name plus surname from a list of common first names, and a surname again later in the same text. For other names in running text you can add [Presidio](https://microsoft.github.io/presidio/) (MIT, runs locally). It is not a dependency of Isomorphism and nothing is downloaded by this package.

```sh
pip install presidio-analyzer
python -m spacy download en_core_web_lg    # or the model for your language
```

```python
from presidio_analyzer import AnalyzerEngine
from isomorphism import anonymize
from isomorphism.presidio import presidio_detector

detector = presidio_detector(AnalyzerEngine(), language="en")
safe, mapping = anonymize(text, detectors=[detector])
```

Presidio hits show up as `PERSON` or `ORG` findings with `detector == "presidio"`. A hit that overlaps a better hit loses against it, and names of authorities are still protected. For German, French or Italian texts configure the `AnalyzerEngine` with the spaCy model of that language and pass the matching `language`.

The quality of the names depends on the model: small models (`*_sm`) confuse persons and companies. Large models do better. The tests of Isomorphism use a fake analyzer; the adapter was also run once against Presidio with `en_core_web_sm`.
