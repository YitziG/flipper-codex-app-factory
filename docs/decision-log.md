# Decision Log

## 2026-06-12: Bootstrap Factory Agent Policy

Created a repo-level `AGENTS.md` for the Flipper Codex App Factory.

Operational delta:

- Codex agents must preserve FAP metadata in `application.fam`.
- Generated device-facing code defaults to safe, low-side-effect behavior.
- Hardware-facing launch/flash commands require explicit human approval per run.
- uFBT build and lint are the default verification path.
- OpenAI credentials for automation belong only in GitHub Secrets.

CI-enforced behavior:

- `.github/workflows/flipper-build.yml` runs uFBT build/lint for the sample app and script smoke checks.
- There is no custom policy-gate script in this newly bootstrapped template repo yet.
