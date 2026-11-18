# LET ME OUT! – ROM DEVELOPMENT III → MAIN VIII
## G5AP / OFF-01 – OFFLINE SYNTHETIC PARSER REGRESSION, FROZEN HANDOFF

**Date:** 2026-11-18. **Verdict:** `OFFLINE_ONLY_PASS` (developer's synthetic Python self-test only). **98/98 offline assertions PASS, two deterministic runs; 0 FAIL in the final run.** These are NOT 98 Stella emulator passes. Historic `G5AL_F9_TRAP_CONTROL_FAIL`, G5AJ FAIL, G5AH original hash FAIL, and `G5_FORMAL_OPEN` are unchanged. This is NOT independent Verification II.

### Authority and original source

- [Binding Issue #18 / G5AP OFF-01](https://github.com/Odourman/let-me-out/issues/18) and [MAIN VIII handoff comment 6965174994](https://github.com/Odourman/let-me-out/issues/18#issuecomment-6965174994).
- [G5AP MAIN VIII source-verified recommendation](https://github.com/Odourman/let-me-out/blob/103de29025fed4ec603b437f927ab874b0b9965e/docs/research/G5AP_MAIN_VIII_WEB_VERIFIED_DEBUGGER_ALTERNATIVES_AND_NEXT_OFFLINE_GATE_2026-11-18.md), [G5AO offline results 18/18](https://github.com/Odourman/let-me-out/blob/103de29025fed4ec603b437f927ab874b0b9965e/docs/research/G5AO_MAIN_VIII_EXACT_FROZEN_G5AL_PARSER_OFFLINE_FIXTURE_RESULTS_2026-11-18.md).
- [Actual frozen G5AL original](https://github.com/Odourman/let-me-out/blob/f16e1e4ac3736e3d6bb1bc0b959b0213e28f6431/rom/g5al_f9_method_2026-11-18/audit_g5al.py), **8426 bytes**, verified connected GitHub blob `f159c1f8668c1f504fd9538a8d1ef17b2ddefafa`. Original content copied **byte-identically** into NEW specialist branch as `audit_g5al_frozen_original_reference.py`; original historic path unchanged.
- Source branch base main commit: `103de29025fed4ec603b437f927ab874b0b9965e`. Specialist branch: `rom-dev-iii/g5ap-off01-offline-parser-regression-20261118`, no merge. Final frozen branch commit SHA is recorded in Issue #18 at final handoff.

**Unavailable attachment:** MAIN VIII's G5AO package `LET_ME_OUT_G5AO_OFFLINE_FIXTURES_2026-11-18.zip`, reported size 8959 B and SHA256 `c519555a974199a2c19e07583c179a2af32819af69d2b42ccdb00c4ba1aad633`, was **not present in this specialist conversation's accessible attachments**. I could NOT download/re-hash those original bytes. The original G5AO 18 expectations were reconstructed from the source-reviewed GitHub report and the frozen verified parser, not by falsely claiming to execute the absent ZIP. The supplied hash is **UNVERIFIED HERE**.

### Repairs in independent new copy `audit_g5ap_offline.py`

1. `session_path(root,stage)` is a **single canonical function** used by fixture writer, stage `--gate`, and `--fullaudit`. Only exact `A_TRAP/<STAGE>_debugger_session.txt` or `B_BREAK_STEP/<STAGE>_debugger_session.txt` is read. The historical bug `*_session.txt` is not reproduced.
2. Stage dispatch explicitly checks `A_REENTRY_HANDSHAKE` for actual parsed **PC `0xF1F0`** and `B_REENTRY_HANDSHAKE` for **PC `0xF1EE`**, with no accidental generic `endswith("HANDSHAKE")` early return. Initial handshakes are separate. Bad PC/bank (F6 only 0..3) are rejected.
3. Exact `> print X` transcript commands are paired with their own unique `#<decimal>` output. Missing, duplicated, joined `print pcprint _fCount`, malformed/unacknowledged `saveSes`, bad `break set` or `cleared`, trap or step textual ACK without actual matching command, wrong frame/scan/cycle/bank all fail closed.
4. Synthetics have an explicit **artificial capture registry** (`G5AP_CAPTURE_INDEX.json`) with source kind `OFFLINE_SYNTHETIC`, SHA256, canonical filename, archive ID, stage, debugger entry ID, monotone sequence and exact matching embedded synthetic marker. Old/stale mismatching file/hash/entry or wrong capture order is rejected. **This is a test contract, not a claim that Stella's saveSes records authentic entry IDs.** A future adapter must supply trusted real provenance under separately authorized scope.
5. A full A-pass with absent B/C returns `OFFLINE_SYNTHETIC_PARTIAL_NOT_DETERMINABLE`, with B=false and C=false. Full ABC positive fixture yields `OFFLINE_SYNTHETIC_A_B_C_CONTRACT_PASS`, NEVER `G5AL_F9_METHOD_READY_BOUNDED` or `STELLA_OBSERVED`. A method FAIL with `archive_sha_pass=true` stays a method FAIL.
6. B requires earlier A, C requires earlier B and exact one STEP with post - pre **+3 cycles**, same frame/scan/bank, plus native 320x228 RGB file/hash. Reference PNG in fixtures is deliberately synthetic, not the historical G5AF image. `--gate` also rejects incoherent entry/source ordering.

### Actual offline regression and reproducibility

- Command: `python3 run_g5ap_offline_fixtures.py > RAW_TEST_STDOUT.txt 2> RAW_TEST_STDERR.txt` (Python 3, Pillow). Actual `--gate` and `--fullaudit` CLI subprocess assertions are included; the numerous other assertions call exactly the same internal validation functions without interpreter-launch overhead.
- **Run 1:** 98/98 final positive/negative expectations, 0 failed. **Run 2:** identical 98/98, 0 failed. Byte-identical `G5AP_OFFLINE_TEST_RESULTS.json` SHA256 `477a86a280a054340b1fa339c2cafae63f9cc85a197179b466664b9fbebe90d0` and stdout SHA256 `41074505221bbf7269e7f5aff165d1a36cfc0d94091613f80cbd7de8c15d40a4`. Both stderr files empty (expected SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`). No failed assertions were hidden. A first **development self-check** found a test-audit classification bug (C-cycle mismatch incorrectly invalidated previously successful A), corrected in the new copy before these two final reproducible test passes. Its initial exploratory failure is noted; it is not an emulator-run failure.
- Positive: all 14 individual stage gates and synthetic full ABC; correct A/B PC reentry; exact step +3, 320x228 RGB synthetic reference equality, positive A-only PARTIAL.
- Negatives: wrong reentry PC A/B, bank4, wrong A/B frames, scans, cycles, missing/duplicated/joined print, missing bank, missing `saveSes`, bad path, missing file/index, tampered/stale hash, old archive and entry, duplicate sequence, wrong/cleared breakpoint, trap removal, missing trap/break/step command despite fake textual ACK, missing/bad native PNG, wrong dimensions/pixels, B/C without A/B, C only +2 cycles, changed entry at step, duplicate synthetic provenance markers and claimed archive integrity with false method PASS.
- `G5AP_OFFLINE_TEST_RESULTS.json` contains **all 98 individually named expected and observed outcomes**, classification `OFFLINE_SYNTHETIC`, counts, unchanged G5AL and G5 state, and original absent G5AO ZIP disclaimer. Raw stdout and stderr both runs are delivered, SHA manifest and reproducible sample synthetic specimen ZIP of 65 files. The test runner's temporary fixtures are generated afresh deterministically, never pulled from an emulator.

### Frozen evidence identity

- New parser `audit_g5ap_offline.py` SHA256 `8ade1878264ee9ef1d3c4badc2c5ef9a799477435a6af5e2e14ca7bec1943f8a`.
- Executed regression runner `run_g5ap_offline_fixtures.py` SHA256 `4ab9fee258138dbdd1114d8adc20209284eb24ae4615076a6b4574686c1ba0c5`.
- Synthetic example ZIP **31,148 B**, **65 file members**, SHA256 `e3fb349a5e3fbe2f010a5f60c95d43a53d6a80ff08bfd3b0ecfe604f0cc19dfd`. These specimens are fake text/PIL PNG, not an Atari ROM.
- Canonical raw data and code are recorded in `MANIFEST_SHA256SUMS.txt` (non-self-referential). The ZIP is a convenience snapshot, not a runtime archive. GitHub exact new-code blobs/commit will be checked before final Issue handoff; no historical files modified.

### Hard STOP / technical interpretation

This developer regression is **`OFFLINE_ONLY_PASS`**. The synthetic parser can reject described bad inputs and consistently classify described synthetic good inputs. It **does not** verify Stella 6.7.1 command transport, framebuffer, 6507 bus cycles, any future `RESP0`/C0/CC placement, Gopher2600, ROM gameplay or Atari hardware. `G5AL_F9_TRAP_CONTROL_FAIL`, G5AJ previous FAIL and G5AH historical negative archive SHA are permanent history; G5AF bounded earlier instrumentation remains bounded; **`G5_FORMAL_OPEN`**.

No Stella, Gopher2600, Actions, emulator code, assembly, DASM or ROM build, PR, merge, Step/G6/S05/5NPC or independent Verification II has been run or initiated. A future headless runtime, Stella adapter or next implementation requires a **new separate explicit user authorization**. Return to MAIN VIII for source-reviewed receipt only.
