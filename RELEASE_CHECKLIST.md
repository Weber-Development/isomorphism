# Release checklist (package-launch)

| Item | Status |
|---|---|
| Repo `Weber-Development/isomorphism` | private; make it public before docs can render (read from GitHub) |
| PyPI `isomorphism` 0.1.0 | waits for the PyPI account and a trusted publisher (see below) |
| packages.sweber.dev | entry, docs config, demo, blog post: sxwxbxr/portfoliov3 PR |
| Pro | not planned for 0.1; core is MIT |
| Polar | not needed (free only) |

## Publishing (Seya)

1. Create the PyPI account (2FA on) if there is none.
2. On pypi.org: Your projects, Publishing, **Add a new pending publisher**: project `isomorphism`,
   owner `Weber-Development`, repository `isomorphism`, workflow `release.yml`, environment `pypi`.
3. In GitHub, repo Settings, Environments: create `pypi`.
4. Tag `v0.1.0` on `main` (the Release workflow builds, tests and publishes). No token is stored anywhere.

## Next version (0.2.0)

Names, addresses, company names, dates of birth, account and card numbers, streaming `restore`,
optional Presidio backend for names in running text.
