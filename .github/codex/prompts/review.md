# Codex Review Prompt

Review this Flipper app factory change for release readiness.

Focus on:

- FAP metadata correctness in every touched `application.fam`.
- Whether generated C code is simple, buildable, and free of unexpected hardware side effects.
- Whether `ufbt lint` and `ufbt` are wired for changed app directories.
- Whether catalog metadata points to committed source, README, changelog, and screenshots.
- Whether CI avoids hardware launch/flashing.
- Whether credentials are confined to GitHub Secrets and not printed.

Return only actionable findings. If there are no major issues, say that clearly and list any verification gaps.
