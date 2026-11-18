# Let Me Out! — Codex working guide

Scope: **only** the Atari 2600 game in `Odourman/let-me-out`. This file is a short workflow guide, **not** an implementation authorization, game canon, test acceptance, or replacement for original project sources.

## Read current authority before acting

1. [Live project status and work queue](docs/CURRENT_AUTHORITY_STATUS_AND_WORK_QUEUE.md)
2. [G5 authorization boundary](docs/gates/G5_AUTHORIZATION_BOUNDARY_AND_USER_CHOICE_2026-11-17.md)
3. The **specific MAIN-issued work order**, under LM-D29's standing user permission for technical tests or an explicitly approved implementation scope; its budgets, negative controls and stop criteria govern that particular task.
4. Relevant frozen source, acceptance/test matrix and actual ROM/emulator evidence. Original Master Spec and 57 decisions are in the [official project Drive folder](https://drive.google.com/drive/folders/1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u), with later **explicit** user decisions superseding originals *only within their stated scope*.

Dated handoffs and `docs/project_sources/` are navigation, not living authority. Do not use ChatGPT Memory or Library as project truth. Confirm live GitHub refs/sha and source version when needed; preserve historical failures.

## Roles and approval

## Standing authorization for technical testing — user decision LM-D29, 2026-11-18

The user explicitly corrected MAIN: **"Du behöver inte fråga om godkännande hela tiden. ... Du får så klart göra tester. Om du vill ändra något kreativt så kan du fråga om godkännande."** This later express decision **supersedes older per-test user-approval requirements** for routine technical investigation and diagnostics, **not** past results or the frozen scope of already-issued test orders.

- MAIN may proactively commission and iterate **technical tests** without further user approval: source analysis, diagnostic builds/test-only ROMs, DASM/rebuild checks, emulator/debugger runs, TIA/raster timing, automated regression/negative tests, capture/trace experiments and tooling fixes **that do not change the approved game design**. Record a reasonable bounded test plan, safety/timeout limits, versions, hashes, raw evidence and negative outcomes. Do not create one approval gate per process, run, step or diagnostic family.
- ROM DEVELOPMENT / Codex may execute those tests when a **concrete MAIN task** delegates them, including troubleshooting and bounded follow-up tests within its technical diagnostic scope; no need to return to the user for another test-only authorization. Preserve specialist-role ownership; an Issue itself does not automatically start a Codex task.
- **Request user approval for creative/game-design changes**: rules, enemy count/appearance, sprites or graphical direction, map selection/geometry, story, sounds or intended gameplay. Don't silently turn research workarounds or technical compromises into canon.
- **Still do not automatically start separately gated gameplay implementation stages, major cutovers, change frozen accepted source/ROM, merge PRs, release, or grant independent VERIFICATION acceptance.** A disposable test-only ROM is not a gameplay implementation authorization.
- **Existing test orders keep their specific per-run safety/budget rules for those particular tests** (e.g. G5AX / Issue #23). When one order finishes, MAIN may authorize a **new bounded technical test** under this standing user permission, rather than asking the user again. Historical FAIL/NOT_RUN and G5_FORMAL_OPEN are not retroactively changed.

- **MAIN** prioritizes, issues bounded work orders, checks developer receipts, records decisions and coordinates the user.
- **ROM DEVELOPMENT IV / Codex** does source analysis, 6507/DASM/TIA code, builds, debugging and **developer self-tests inside concretely delegated MAIN scope**. LM-D29 removes repeated personal approval for technical tests, not the separate scope boundary for gameplay implementation.
- **RESEARCH** advises; **GRAPHICS** supplies studies within its own design order.
- **VERIFICATION II** independently checks frozen deliverables; a developer's PASS never substitutes for it.
- A general "continue", a plan, an Issue's existence or this `AGENTS.md` does **not** by itself start a Codex task, approve a gameplay implementation step, design waiver, independent verification, PR merge or release. **MAIN may commission bounded diagnostic ROM builds and emulator tests under LM-D29 without asking the user again.**
- Each specific diagnostic test must respect its stated **ROM/hash**, emulator/version, process/run limits, input controls and criteria. When a stop condition fires, stop that run; MAIN can delegate a **new, separately bounded test-only task** under the standing LM-D29 permission without seeking another personal approval. No unlimited silent retries.

## Faster technical execution — user decision LM-D30, 2026-11-18

The user expressly requested **more courage, speed and actual development progress**: "Och du är för försiktig. All försiktighet bromsar utvecklingen. Var mer modig och kör på..." This is a **workflow and initiative decision**, not an authorization to alter the game vision or merge/ship.

- **Default to doing the technical work**, not issuing serial source-only briefs, micro-gates and permission questions. When a MAIN-delegated *technical test problem* is blocked, ROM DEVELOPMENT should try multiple sensible, reproducible technical approaches **inside the delegated diagnostic goal**, including a disposable ROM or alternate emulator/debugger strategy as technically justified. Do not require one new Issue or user approval for every attempt.
- **Use practical risk budgets**, not arbitrary one-RUN/one-STEP rules for all future tests. Make run limits appropriate to the actual risk and available tools. Stop for material hazards, unverifiable evidence or scope boundaries, **not simply because an exploratory hypothesis failed**. Preserve real negative tests, avoid infinite retries and do not relabel partial observations as gameplay success.
- **Optimize for the game, not the test infrastructure.** After the already-authorized G5AX / Issue #23 (whose exact local limits still bind that run), prioritize decisive raster evidence and the feasibility of the approved **five independent NPC + player + shot + walls** scene. Move to integration only with its separately approved implementation scope. Avoid repetitive PTY/Gopher feasibility exercises once the transport mechanism is demonstrated unless necessary for actual graphics measurements.
- **Deliver working evidence quickly**: one coherent specialist report with source/ROM/hash, worst-case GUI/raster measurements, exact successes and failures; avoid sprawling administrative packages. MAIN should review substance and delegate the next technical **test-only** task without pinging the user. Independent VERIFICATION remains separate.
- **Creative choices still go to the user**: enemy design/count, appearance, maps, rules, story, audio and any compromise that changes the intended game. Do not disguise implementation or design concessions as a diagnostic experiment. Previous frozen ROMs, negative evidence, accepted sources and existing Issue #23 limits remain intact.

## Efficient Codex workflow

1. Read the scoped order and only the originals necessary for that task. Distinguish **design target**, **source-only hypothesis**, **developer observation**, **independent verification**, and **not run**.
2. Work on an isolated specialist branch/worktree only if the order permits changes. Do not mutate frozen original ROMs, negative evidence or historical decision records; do not merge PRs.
3. For approved technical runs: record exact Git commit, versions, command lines, exit status, ROM/asset SHA-256, raw stdout/stderr, emulator TX/RX if relevant, bounded test matrix, actual observed results and failures. Keep claims at their proven evidence level; synthetic-fixture PASS is not emulator PASS.
4. Publish a compact `TO_MAIN` report with reproducible files/logs or unchanged raw log text in the **same authorized GitHub Issue**, and identify what remains unproven. Use the official Drive folder for durable evidence only when the specific workflow requires it.
5. Stop when the approved scope is complete. MAIN decides the next step; do not automatically start the proposed follow-up. Ask only when a real approval, missing primary source or blocker requires it.

## Debugger baseline

Keep **stock Stella 6.7.1** as the historical raster/TIA comparison target. **Gopher2600 v0.57.2** now has **one real, bounded PTY command-ACK plus bank-neutral F9 pre-`STA RESP1` PC-stop observation**, [G5AW / Issue #22](https://github.com/Odourman/let-me-out/issues/22#issuecomment-6978952351) with [MAIN IX log review](https://github.com/Odourman/let-me-out/issues/22#issuecomment-6979047165): PC `$F1EE`, bank 0, `FR=0001 SL=122 CL=-14`, one process/one `RUN`. **It is not proven as a replacement for Stella/TIA pixel/colorclock verification or post-STA state inspection**. G5AW had SIGTERM→SIGKILL on cleanup, which must be retained. Respect [G5AV's no-ROM startup blocker](https://github.com/Odourman/let-me-out/issues/21) and [G5AL/G5AJ's failed earlier stops](docs/CURRENT_AUTHORITY_STATUS_AND_WORK_QUEUE.md). Do not silently replace versions, mislabel `GOPHER_OBSERVED` as `STELLA_OBSERVED`, or claim CPU→TIA START→pixel proof without real correlated evidence. **G5AW is closed; MAIN may commission new independently bounded technical tests under LM-D29/LM-D30 without a new personal approval.**

As of 2026-11-18 `G5_FORMAL_OPEN`; check the live status for subsequent decisions.
