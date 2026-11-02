---
title: FastAPI and streaming
description: Anonymise before the model call, restore the answer, also while it streams.
---

The usual flow per request: anonymise the incoming text, call the model with placeholders, restore the answer. The mapping lives only for the length of the request.

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from isomorphism import Restorer, anonymize, restore

app = FastAPI()


@app.post("/ask")
async def ask(question: str) -> dict:
    safe, mapping = anonymize(question)
    answer = await call_your_model(safe)  # placeholders only
    return {"answer": restore(answer, mapping)}


@app.post("/ask/stream")
async def ask_stream(question: str) -> StreamingResponse:
    safe, mapping = anonymize(question)

    async def pieces():
        r = Restorer(mapping)
        async for chunk in call_your_model_stream(safe):
            if out := r.feed(chunk):
                yield out
        if out := r.flush():
            yield out

    return StreamingResponse(pieces(), media_type="text/plain")
```

`Restorer` holds back the end of a piece when it could be the start of a placeholder (`[AHV_`), so a placeholder split between two pieces is still restored. `restore_stream(chunks, mapping)` does the same for a normal iterator. Call `flush()` at the end of the answer.

## Audit log

```python
for f in mapping.findings:
    audit.write(kind=f.kind, start=f.start, end=f.end, confidence=f.confidence, detector=f.detector)
```

The findings contain no values. Do not log the mapping itself.

## Keep what must stay

```python
safe, mapping = anonymize(text, keep=["info@gemeinde.example", re.compile(r"Steueramt .*")])
```

Names of authorities such as "Steueramt St. Gallen" are not replaced anyway.

## Filter by confidence

Heuristic hits (a first name alone, a postcode next to a capitalised word) have a low confidence. If you prefer fewer false alarms, drop them yourself from `detect(text)`; if you prefer to replace too much rather than too little, keep everything, which is the default.
