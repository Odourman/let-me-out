# G5AF LM-D22 – F9-only instrumentation preregistration (before first new CI measurement)
**Date:** 2026-11-17. **Role:** ROM DEVELOPMENT III. **Main base:** `9063a5ad8f725093e57c1a6e5c6848e2a9d60518`.
**Active order:** [GitHub Issue #14](https://github.com/Odourman/let-me-out/issues/14), [G5AF original authorized order](https://github.com/Odourman/let-me-out/blob/9063a5ad8f725093e57c1a6e5c6848e2a9d60518/docs/gates/G5AF_MAIN_VII_LM_D22_F9_INSTRUMENTATION_ONLY_REPAIR_RETEST_AUTHORIZED_2026-11-17.md).
**Sources re-read:** [G5AE acceptance/source analysis](https://github.com/Odourman/let-me-out/blob/9063a5ad8f725093e57c1a6e5c6848e2a9d60518/docs/gates/G5AE_MAIN_VII_G5AD_NO_BUILD_INSTRUMENTATION_BLOCKER_RECEIPT_AND_STELLA_SAVESES_SOURCE_REVIEW_2026-11-17.md), G5AD [last failing run 44159356697/job 134308674746](https://github.com/Odourman/let-me-out/actions/runs/44159356697/job/134308674746), [frozen F9 trace source](https://github.com/Odourman/let-me-out/blob/8145a50607942202315439477bd378ba92fbdba1/rom/v018/experiments/r1_free_xy/r1_f9_trace.sh), F9 [build source](https://github.com/Odourman/let-me-out/blob/8145a50607942202315439477bd378ba92fbdba1/rom/v018/experiments/r1_free_xy/r1_f9_build.py). No original source modified.

## Exactly two F9 stop probes
Both are explicit original F9 `r1_f9_trace.sh` source entries for RAM mode **000**, the existing single F9 F6 ROM (16,384 B; **SHA256** `6c2585148eb082fb8bc794d664edc4869b18849fcfabb9cada23373d1dc1318b`), source/debugger frame **136**, `_scan == #123`.

| Probe ID | Pre-registered register write | `_sCycles` trap range exclusive | Earlier F9 source center only (NOT measured G5AF) | Distinction |
|---|---|---|---|---|
| `F9_000_M_RESP1` | `RESP1` | `> #19 && < #23` | 21 | First male bitmap reposition |
| `F9_000_F_RESP1` | `RESP1` | `> #30 && < #34` | 32 | Subsequent female bitmap reposition |

These **two distinct source timing windows** are preregistered, NOT two separately authored kernels. Actual stop PC, frame, scanline, cycle, bank and TIA state will be captured from Stella itself; if they do not match, mark `NOT_DETERMINABLE`. A `trapWriteIf` halt can occur **after** the relevant write; do not call the observed `_sCycles` the exact `STA` end-cycle without additional evidence.

## Sequence / stop logic
1. GitHub Actions ubuntu-24.04 installs **Stella 6.7.1** and Xvfb, no DASM compiler invocation; downloads **only** historical F9 artifact `LET_ME_OUT_R1_F9_ONE_ROM_AND_ACTUAL_STELLA_PARTIAL_OR_COMPLETE_G1` from run `44050126727`. Byte-length and SHA256 are checked before and after.
2. For each independent source-registered trap, `autoexec.script` contains **only** `base #10`, `frame #136`, `trapWriteIf {...} RESP1`, `run`. **No** `saveSes` in autoexec; source checks show that `autoExec()` is called inside the first-time prompt `loadConfig()` before `_promptStartPos` is set.
3. After debugger GUI becomes available, the X11 keyboard sends real interactive commands: `print pc`, `print _fCount`, `print _scan`, `print _sCycles`, `print _bank`, `tia`, `print pc`, `print _scan`, `saveSnap`, **then `saveSes`**. The latter must happen only after the prompt's startup pass is completed. See pinned [PromptWidget::loadConfig](https://github.com/stella-emu/stella/blob/6.7.1/src/debugger/gui/PromptWidget.cxx#L369-L411), [saveBuffer](https://github.com/stella-emu/stella/blob/6.7.1/src/debugger/gui/PromptWidget.cxx#L931-L957), [executeSaveSes](https://github.com/stella-emu/stella/blob/6.7.1/src/debugger/DebuggerParser.cxx#L2027-L2057).
4. Immediately copy native Stella `*_dbg_*.png` and `session_*.txt` from actual runner directory **into the Actions artifact directory**, plus keyboard command sequence, GUI screenshot (only auxiliary), workflow/stella stdout. Hash each copied file.
5. Audit must prove both actual numeric `PC, _fCount, _scan, _sCycles, _bank`, actual `tia` register state, unchanged duplicate `pc/_scan` sample, and saved native **320×228 RGB** image from same stopped F9 debugger. **Distinct PC** across the two traps. `TIADebug::toString` prints `COLUxx, P0/P1, M0`; note Stella source explicitly says it does **not** print `RESP0/1` strobes in TIA state dump.
6. Two runs MAX, a first corrected workflow then at most one targeted fix/rerun in same family. If it still cannot satisfy criteria, stop `PARTIAL` or `BLOCKED`. G5AD negatives remain archival and unchanged.

## Critical delimitations
- Instrumentation benchmark, **not** new gameplay or G5AD TIA-C0..N1 test; no new `.asm/.bin` or F9 rebuild; no Stella source patch. **No** H4, G6, F12, S05, five NPC, PR merge, independent Verification.
- Observed Stella pixels are emulator data. Even a fully correlated debugger session is **not** CPU→TIA physical START-latch proof or original Atari hardware verification.
- The separate old Python `IndentationError` (unindented `import shutil`) is eliminated by a fresh, indentation-checked standalone `audit_evidence.py`, not by modifying the historical G5AD workflow.
