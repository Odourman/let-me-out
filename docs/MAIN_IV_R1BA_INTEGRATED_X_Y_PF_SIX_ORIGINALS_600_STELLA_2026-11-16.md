# LET ME OUT! – MAIN IV R1ba: integrated six-original 8×9 NPC masks, runtime X/Y and mirrored brown PF

**Date: 2026-11-16. STATUS: LOCAL RESEARCH PASS 600/600 authentic Stella frames. This is NOT a full R1, full R1–R4, or independent VERIFICATION.**

## Reproducible evidence and file integrity

- GitHub Actions **run #43884511590**, job `integrated-source-exact-X-Y-PF` **SUCCESS** after fixing a *research build-script matcher* (not any source sprite bitmap). [Run](https://github.com/Odourman/let-me-out/actions/runs/43884511590).
- Research branch `research/main-iv-r1ba-integrated-xyz-pf-20261116`, work product under `rom/v018/experiments/main_iv_r1ba_combined/`. Do not merge this into production.
- One **16,384-byte standard F6/NTSC ROM** (four identical 4 KiB banks). **ROM SHA-256:** `41fdb87969a20d40fee8cde5673792201663860c2d1e08c8d93f9172ede82361`.
- [Complete original Actions evidence ZIP](https://github.com/Odourman/let-me-out/actions/runs/43884511590/artifacts/14233733448): **622 archive entries**, includes 600 consecutive actual Stella PNG frames, the exact executable ROM, generated DASM `r1ba.asm`, symbol table/listing, builder, strict pixel analyzer, CSV and JSON evidence, source SHA and manifest. Original ZIP checked by MAIN via Python `ZipFile.testzip()`: **no damaged entry**. Internal ROM bytes: **16,384**, SHA agrees with both provided manifest and independent Python hash. **ZIP SHA-256:** `f8dd41e62939aa1699d80f70df0c5b5081b87441a1e2c740ff2786139908f325`. ZIP size **3,930,298 bytes**.
- [Verified Google Drive copy in dedicated Let Me Out! folder](https://drive.google.com/file/d/1c2Sd68dvQsmb_MJcQOLU8dbiMc5YgbsJ/view?usp=drivesdk) uploaded with the same 3,930,298-byte ZIP; not a renamed document, no unrelated project modified.

## Actual 600-frame local pixel audit

| Check | Result |
|---|---|
| Six full **original** 8×9 source masks on same 9-line raster band: M,M,F,F,SM,SF | **600/600** |
| One intact yellow P0 player and one static yellow M0 test shot | **600/600** |
| Three different actual X-layouts observed **in the same ROM at runtime** | **Yes**, all >=100 frames |
| Three different source-exact small-NPC Y offset profiles **in the same ROM at runtime** | **Yes**, all >=100 frames |
| Two mirrored brown PF side walls with empty center region on all sprite lines | **600/600** |
| Scanline HUD, exactly 262 NTSC rows and correct monotonic frame counter | **600/600** |
| Missing / extra WHITE source-mask pixels | **0 / 0** |
| Fail-closed CI result | **SUCCESS** |

Actual Stella screenshot-crop X starts (not standalone TIA color-clock X):

| Linked mode | X: large male ×2; large female ×2; SM; SF | SM Y delta | SF Y delta | Frames |
|---|---|---:|---:|---:|
| A | `75;107;147;179;243;303` | +1 | −1 | 297 |
| B | `75;107;159;191;243;303` | −1 | +1 | 151 |
| C | `87;119;159;191;243;303` | −2 | −1 | 152 |

**IMPORTANT:** The X/Y profiles are paired A+A, B+B, C+C. This does **not** prove nine independent cross-combinations or per-Android free X/Y; each large-person pair is still NUSIZ-coupled at fixed spacing.

## How it was implemented

1. Build the pinned **R1at runtime-three-X** original 16 KiB F6 ROM from its original scripts, demand SHA `486dca4b574d9a394075788bc974232d3b7452282f282e46c7dd3fca454d2c0a`.
2. In each of the three *already source-perfect* 9-scanline kernels A/B/C, change **only the source-immediate SM and SF 8×9 bitmap row bytes** according to the three R1ay-proven vertical profiles; retain original source tables unchanged, with transparent-zero padding so no white original pixel is clipped.
3. Reuse [R1ax corrected mirrored-brown PF experiment](https://github.com/Odourman/let-me-out/actions/runs/43883269341) once, outside critical visible raster rows: `COLUPF=$26`, `CTRLPF=$01`, `PF0=$F0`. All three original modes' P1 `RESP1` and `GRP1` *opcode schedule* preserved; original M/F/SM/SF and yellow P0/M0 source bitmap tables preserved.
4. The critical line CPU `RESP1` end-cycle schedules **from source planning**, not an independently measured Stella T07 trace: A c28/40/56/66, B c28/42/56/66, C c30/42/56/66. The end of each row's static instruction sequence is within nominal 76 cycles, but **full B02/T07 real debugger CPU-/TIA-write log is still missing**.
5. Single ROM selects the A/B/C full unrolled source kernel via `FRAMELO & $18` before critical sprite-band raster, so no new mid-row branches are added.
6. Pixel audit excludes the dark brown playfield from the yellow sprite/projectile mask, separately validates all nine brown side-band rows, and verifies all source masks and three observed X/Y profiles. This fixes a documented prior R1ax **auditor error**, not a graphics waiver.

## What is NOT delivered or approved

- **No six independently free X coordinates** despite six source-perfect simultaneous masks. Both large pair groups are hardware-copy-coupled. Small NPC X fixed. This is major R1/C01/LM-D10 risk and cannot be declared resolved or silently accepted as a design waiver.
- **No six independently free Y coordinates**. Only SM/SF move between precompiled Y profiles, coupled to which X mode is chosen. No actual Y physics, independent arbitrary X/Y combinations, close/crossing stress or verified collision responses.
- **No R2 five+gold key+P0+M0 and O1** logical key coordinate unchanged through long occlusion and return. The static missile is diagnostic, not moving projectile mechanics.
- **No R3 right-only unlock, orange door or black keyhole**. The proven `CTRLPF=$01` has *mirrored* sidewalls. A right-only opening requires a separately tested asymmetric playfield update or distinct rendering approach.
- **No independently reproduced clean rebuild by Verification**, no full R1–R4 16-case accepted matrix, no signed VERIFICATION report. 600 debugger screenshots and 262-scanline HUD are genuine local evidence but do not alone replace the required **TIA register-write CPU cycle trace** or manual visual review.
- F6 bank switching is not actually exercised as four distinct executing banks: this prototype repeats one 4K program four times.

## MAIN IV decision and next authorized diagnostic research

**Keep complete v0.18 = BLOCKED / NOT ACCEPTED, no merge, no production code changes, no PAL/full game.**

Priority within already authorized NTSC R1/R4 research: test whether X and Y profiles can be selected *independently*, not as 3 linked fixed layouts, with exactly six original masks and same P0/M0/PF in all states. In parallel or next, isolate a genuine R3 right-side-only open/closed PF test from one of the currently source-chosen A01/B01/C02/D01 maps; track brown baseline, orange gate, and black keyhole as separate outcomes. R2 gold key and O1 occlusion remain blockers. Reserve independent VERIFICATION for a fixed, complete developer deliverable; do not reuse Issue #8 frozen older commit.

## Main checkpoint and records

[MAIN IV current source/authority/status checkpoint in main](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_IV_CHECKPOINT_2026-11-16.md), also in [MAIN IV Google Doc](https://docs.google.com/document/d/1F3vKB3tK0VZ-KSLoHeKRopRoFdYNsAuqkpSFareN-1s/edit).

**Research only, scoped only to this Atari project.**
