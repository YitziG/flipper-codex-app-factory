# Codex Release Prompt

Prepare this Flipper app for private release or public catalog submission.

Checklist:

- Confirm `application.fam` version changed and uses `major.minor`.
- Run `ufbt lint` and `ufbt` for the app.
- Confirm `README.md` and `docs/changelog.md` describe the release.
- Confirm screenshots are present when preparing public Apps Catalog submission.
- Generate catalog manifest with `scripts/catalog_manifest.py` using the committed SHA.
- Confirm no hardware launch/flashing happens in CI.

For public Apps Catalog submission, prepare the `manifest.yml` path expected by the catalog repository: `applications/<category>/<appid>/manifest.yml`.
