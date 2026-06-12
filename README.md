# Flipper Codex App Factory

Repeatable factory for creating, validating, reviewing, and publishing Flipper Zero FAP apps with uFBT and Codex.

## Quick Start

```bash
make scaffold APPID=my_tool NAME="My Tool" CATEGORY=Tools AUTHOR="Your Name" DESCRIPTION="Short app description"
make validate APP=apps/my_tool
```

Build and lint a generated app:

```bash
make lint APP=apps/sample_tool
make build APP=apps/sample_tool
```

CI builds and lints every committed app under `apps/*/application.fam` for both the `release` and `dev` SDK channels. Tag releases attach release-channel `.fap` files for every committed app.

Launch to a locally connected Flipper only after reviewing the generated device-facing code:

```bash
make launch APP=apps/sample_tool
```

## What This Factory Provides

- `apps/sample_tool/`: a minimal generated C FAP app.
- `factory/templates/c-app/`: canonical template for new C apps.
- `scripts/new_app.py`: scaffold a new app from the template.
- `scripts/validate_app.py`: check required FAP metadata and run `ufbt lint` plus `ufbt`.
- `scripts/catalog_manifest.py`: emit an Apps Catalog-ready `manifest.yml`.
- GitHub Actions for uFBT build/lint, private release artifacts, and optional Codex readiness review.
- Codex prompt files for scaffold, review, and release workflows.

## Firmware Workspace Adapter

The default workflow uses uFBT from a standalone app directory. If you want to test inside the official firmware repository, copy a generated app into `applications_user/<appid>` and run:

```bash
./fbt build APPSRC=applications_user/<appid>
./fbt launch APPSRC=applications_user/<appid>
```

Use `./fbt launch` only when a human has reviewed the generated code and approved flashing/running it on a physical Flipper.

## Apps Catalog Flow

Public catalog publication still happens through a pull request to `flipperdevices/flipper-application-catalog`.

Generate catalog metadata after committing the app source:

```bash
python3 scripts/catalog_manifest.py apps/sample_tool \
  --origin https://github.com/<owner>/<repo>.git \
  --commit-sha "$(git rev-parse HEAD)"
```

The generated manifest is written to:

```text
dist/catalog/<category>/<appid>/manifest.yml
```

Before public submission, add qFlipper screenshots under the app's `screenshots/` directory and validate against the Apps Catalog repository if available.
