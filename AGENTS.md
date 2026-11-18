# Let Me Out! — Codex working guide

Scope: **only** the Atari 2600 game in `Odourman/let-me-out`. This file is a short workflow guide, **not** an implementation authorization, game canon, test acceptance, or replacement for original project sources.

## Read current authority before acting

1. [Live project status and work queue](docs/CURRENT_AUTHORITY_STATUS_AND_WORK_QUEUE.md)
2. [G5 authorization boundary](docs/gates/G5_AUTHORIZATION_BOUNDARY_AND_USER_CHOICE_2026-11-17.md)
3. The **specific GitHub Issue / user-approved work order** for this task; its explicit scope, budgets, negative controls and stop criteria govern this task.
4. Relevant frozen source, acceptance/test matrix and actual ROM/emulator evidence. Original Master Spec and 57 decisions are in the [official project Drive folder](https://drive.google.com/drive/folders/1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u), with later **explicit** user decisions superseding originals *only within their stated scope*.

Dated handoffs and `docs/project_sources/` are navigation, not living authority. Do not use ChatGPT Memory or Library as project truth. Confirm live GitHub refs/sha and source version when needed; preserve historical failures.

## Roles and approval

- **MAIN** prioritizes, issues bounded work orders, checks developer receipts, records decisions and coordinates the user.
- **ROM DEVELOPMENT IV / Codex** does source analysis, 6507/DASM/TIA code, builds, debugging and **developer self-tests only inside explicitly approved scope**.
- **RESEARCH** advises; **GRAPHICS** supplies studies within its own design order.
- **VERIFICATION II** independently checks frozen deliverables; a developer's PASS never substitutes for it.
- A general "continue", a plan, an Issue's existence, or this `AGENTS.md` does **not** approve a new ROM build, emulator run, implementation step, design waiver, verification, PR merge or new gate.
- An authorized test may use only its stated **ROM/hash**, emulator/version, process/run limits, input controls and criteria. When a stop condition fires, stop; don't retry, broaden the run or change the goal without a new authorization.

## Efficient Codex workflow

1. Read the scoped order and only the originals necessary for that task. Distinguish **design target**, **source-only hypothesis**, **developer observation**, **independent verification**, and **not run**.
2. Work on an isolated specialist branch/worktree only if the order permits changes. Do not mutate frozen original ROMs, negative evidence or historical decision records; do not merge PRs.
3. For approved technical runs: record exact Git commit, versions, command lines, exit status, ROM/asset SHA-256, raw stdout/stderr, emulator TX/RX if relevant, bounded test matrix, actual observed results and failures. Keep claims at their proven evidence level; synthetic-fixture PASS is not emulator PASS.
4. Publish a compact `TO_MAIN` report with reproducible files/logs or unchanged raw log text in the **same authorized GitHub Issue**, and identify what remains unproven. Use the official Drive folder for durable evidence only when the specific workflow requires it.
5. Stop when the approved scope is complete. MAIN decides the next step; do not automatically start the proposed follow-up. Ask only when a real approval, missing primary source or blocker requires it.

## Debugger baseline

Keep **stock Stella 6.7.1** as the historical raster/TIA comparison target. **Gopher2600 v0.57.2** is a *candidate* for programmatic debugger control, **not** a proven replacement. Respect [G5AV's no-ROM startup blocker and synthetic-only PTY result](https://github.com/Odourman/let-me-out/issues/21) and [G5AL/G5AJ's failed debugger-stop attempts](docs/CURRENT_AUTHORITY_STATUS_AND_WORK_QUEUE.md). Do not silently replace versions, mislabel `GOPHER_OBSERVED` as `STELLA_OBSERVED`, or claim CPU→TIA START→pixel proof without real correlated evidence.

As of 2026-11-18 `G5_FORMAL_OPEN`; check the live status for subsequent decisions.
