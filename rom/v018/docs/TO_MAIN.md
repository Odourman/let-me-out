# ROM DEVELOPMENT → MAIN: Let Me Out! v0.18 technical handoff

**Date:** 2026-11-15  
**Source authority:** `Odourman/let-me-out` Issue #6, `docs/ROM_GATE_V018_AUTHORIZATION_2026-11-15.md`, R1–R4 scope and acceptance.  
**Status:** RUNNABLE 6502 BINARY + OFFLINE CPU PREFLIGHT; STELLA AND INDEPENDENT VERIFICATION STILL PENDING.  
**No full game or later phase authorized.**

## What exists

- A 16,384-byte F6/NTSC-oriented Atari 2600 binary with four bank-isolated test scenes.
- Complete original 6502 assembler source for each 4 KiB bank.
- A source generator, build instructions, deterministic MOS 6502 assembler subset,
  CPU instruction/cycle test harness, SHA-256 checks and schematic source previews.
- R1 six PF-drawn humanlike silhouette candidates + P0 player + PF shot symbol,
  all sharing the same vertical stress band. No animal/robot replacement or removed android.
- R2 five surviving PF-silhouette androids, static K11/K09 gold key candidate at
  X=27/Y=80, yellow P0 player, PF shot symbol. At phase1/2 the fifth android
  overlaps that static key. P1's graphic mask is blanked only during the overlap;
  the logical RAM key never moves or disappears.
- R3 **C02** map transcribed from `design/PLANERADE_RUMSKARTOR_V011.json`.
  Left outermost PF cell remains set on every logical row; source door x=39,y=9..12
  is omitted in the *open* PF baseline; P1 overlays brown/orange when logically locked.
  Transparent P1 pixels attempt the approved black round/wedge keyhole motif.
  Unlocked stage makes P1 background color (black), revealing the right opening.
- R4 four phase profiles, moving both android PF masks and PF test shot with
  offsets up to one raster line, plus repeated key occlusion and recovery.

## Test result – what actually ran

A self-contained 6502 instruction/cycle model (`tools/cpu_trace.py`) executed
**7,287,927 instructions over 2,403 completed visible frames**, with 600 stable
consecutive 262-line frame deltas for each R1–R4 interval. The initial bootstrap
frame is intentionally excluded: its duration differs before regular framing.
The simulation reports the key RAM triplet (27,80,1) unchanged throughout.
All four scene transitions and F6 bank switches are observed in the model.

Critical PF writes in modeled steady visible scanlines (both full/band kernels):

| TIA register | Left write cycle | Right rewrite cycle |
| --- | ---: | ---: |
| PF0 `$0D` | 7 | 36 |
| PF1 `$0E` | 14 | 43 |
| PF2 `$0F` | 21 | 50 |
| GRP0 `$1B` | new row prepared by cycle 59 | n/a |
| GRP1 `$1C` | new row prepared by cycle 66 | n/a |

Those numbers come from a local 6502 instruction/cycle model, not Stella.
They are **provisional** until the TIA's display latch behavior, actual color clocks,
object positioning, and display stability are measured with Stella Debugger.

**Build:** Python 3.13.5, bundled `as6502.py` v0.18a, no third-party dependencies
for `.bin` generation. Clean rebuilt `.bin` SHA-256 agrees exactly (isolated rebuild using only the two bundled builder files; see `evidence/clean_build_check.json`).
**ROM:** 16 KiB F6, four 4 KiB banks; 8 RIOT-RAM bytes explicitly assigned,
128 B stock RAM unchanged; PF0/1/2 + P0/P1, no missiles/ball. Neither full
projectile mechanics nor AI exist.

## Important unresolved design risks and blockers

1. **PF silhouette quality (HIGH):** Four original diagnostic masks are only
   4 PF cells / 16 color clocks wide; the local schematics show very chunky
   humanoids. The *approved* 8×9-sized image quality is **not yet demonstrated**.
   Even a perfectly timed frame might fail C03/C04. Changing sprite design or
   silently reducing six androids is forbidden.
2. **PF shot and hazards (HIGH):** The shot is the same playfield color as the
   androids, so visual differentiation needs a manual emulator review.
3. **Right P1 overlay (HIGH):** An 8-pixel P1 can create a narrow orange door and
   transparent black hole candidate, but there is no Stella confirmation of exact
   placement, perceived keyhole shape, or full combined contention.
4. **Key visibility (MEDIUM):** Logical key position is preserved; the O1
   occlusion is explicitly handled by a blank P1 mask only when the PF android
   is over it. This must be observed visually; a permanently hidden key is
   not accepted by the actual game design.
5. **Color artifact (MEDIUM):** PF rendering ties the white android and boundary
   color within the same raster band. This diagnostic compromise is not an
   approved final visual treatment; changing design requires MAIN/user input.

**Do not interpret the CPU model's stable 262-line output as Stella pass.**
T01/T02/T03/T04/T05/T06/T07/T08/T09/T10/T11/T12/T13 all remain INCONCLUSIVE
until emulator/evidence and explicit gate review. T15 needs an *independent*
VERIFICATION actor. T14 is a reproducible-build local PASS, T16 is a scope
isolation local PASS after contents review.

A TIA control flag error discovered in source review was corrected: `CTRLPF` reflection is disabled for all right-half PF data, whose explicit PF0/PF1/PF2 rewrites already encode orientation. This change was rebuilt and locally re-tested. No claim of confirmed on-screen map fidelity is made.

## Remaining work for independent VERIFICATION

- Test the SHA in Stella, map type F6, NTSC mode, reset vector and register writes.
- Save real Stella `.png`/video for R1, R2 and R3 closed/open, with 600-frame
  traces per scene. Check horizontal coordinates, sprites and key legibility.
- Inspect `_scan` and `_sCycles` over worst-case contiguous frames.
- Confirm R2 key visible/hidden/recovered at exactly same display coordinates.
- Confirm R3 orange door disappears *only* at right and black keyhole can be read.
- Produce an independent verdict. No waiver is implied by the preflight data.

**Scope isolation:** No Berzerk data, The Cabin files, I Love a Fish files,
PAL, sound, scoring, AI, or full game screens were created.
