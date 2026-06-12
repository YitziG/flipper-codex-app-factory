# Codex Scaffold Prompt

You are adding a new Flipper Zero FAP app to this factory.

Inputs to confirm from the user or issue:

- `appid`: lowercase, numbers and underscores only.
- `name`: display name.
- `category`: one Flipper Apps Catalog category.
- `author`: app author.
- `short_description`: one concise sentence.

Use `make scaffold APPID=... NAME=... CATEGORY=... AUTHOR=... DESCRIPTION=...`.

After scaffolding:

- Keep `application.fam` metadata complete and consistent.
- Keep first-pass generated code safe: no radio, NFC, Sub-GHz, RFID, iButton, GPIO, USB HID, BadUSB, storage mutation, credential handling, or destructive device behavior unless explicitly requested.
- Run `python3 scripts/validate_app.py apps/<appid> --skip-ufbt`.
- If uFBT is available, run `make validate APP=apps/<appid>`.
- Summarize changed files and verification.
