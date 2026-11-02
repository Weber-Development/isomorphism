# Release checklist (package-launch)

| Item | Status |
|---|---|
| Repo `Weber-Development/isomorphism` | see GitHub for visibility; docs render only when public |
| PyPI `isomorphism` | 0.1.0 published; later versions: tag `v<version>` on `main` (trusted publishing, environment `pypi`) |
| packages.sweber.dev | page, demo, blog post: sxwxbxr/portfoliov3 (wheel in `public/demos/isomorphism/` must match the release) |
| Pro | none planned; core is MIT |
| Polar | not needed (free only) |
| Trademark check "Isomorphism" | open (Seya) |

## Per release

1. Bump `version` in `pyproject.toml`, update `CHANGELOG.md` and the README table (`python -m tests.measure`).
2. PR, CI green, merge, then tag `v<version>`.
3. portfoliov3: new wheel in `public/demos/isomorphism/`, `content/packages/isomorphism.json`, blog post.
