# Agent Notes

Operate as an execution-first engineering partner for Flipper Zero app work.

## Flipper Safety Rules

- Preserve FAP metadata in `application.fam`: `appid`, `apptype`, `entry_point`, `stack_size`, `fap_version`, `fap_category`, `fap_description`, `fap_author`, and `fap_icon`.
- Keep generated device-facing code simple and reviewable.
- Do not add radio, NFC, Sub-GHz, RFID, iButton, GPIO, USB HID, BadUSB, storage mutation, credential handling, or destructive device behavior unless the user explicitly asks and the safety implications are documented.
- Never run `ufbt launch`, `./fbt launch`, flashing, or hardware-facing commands without explicit human approval for that run.
- Prefer uFBT for standalone app work. Use full `./fbt` only when working inside the official firmware repository.

## Verification

- For each changed app, run `ufbt lint` and `ufbt` from that app directory.
- For factory scripts, run the script-level smoke tests shown in `README.md`.
- Before public catalog submission, verify the generated Apps Catalog manifest against the catalog repository tooling when available.

## Codex Workflow

- Use Codex to scaffold and review code, but keep all generated device-facing code subject to human review before launch.
- Keep network access disabled by default; allow it only for explicit dependency installation, documentation lookup, or CI.
- Store OpenAI credentials only in GitHub Secrets for workflows. Do not commit keys or local `.env` files.
