# Let Me Out! – MAIN IV R1au: six source-perfect Androids with ONE GROUP moving per runtime transition

**2026-11-16. Status: `LOCAL_RESEARCH_ONE_GROUP_PER_TRANSITION_RUNTIME_THREE_LAYOUTS_600_PASS`. NOT full v0.18 R1/R4; NOT independent VERIFICATION.**

## Primary reproducible evidence

- [GitHub Actions #43869049214](https://github.com/Odourman/let-me-out/actions/runs/43869049214): **SUCCESS** on exact tested source commit `25b0268ca2ef487508df6be1d792755c76069124`.
- [Full artifact #14226324427](https://github.com/Odourman/let-me-out/actions/runs/43869049214/artifacts/14226324427): 16,384-byte F6/NTSC ROM, exact original source and Python build chain, DASM listing/symbol file, 600 consecutive genuine Stella 6.7.1/X11 screenshot PNGs, 600-frame CSV, fail-closed JSON pixel/raster audit, SHA256.
- Exact R1au ROM SHA256: `e55f193b3ab13862e6dfaa21ae37ce1575afa8eb5de87681649e53ff17bb6c10`.
- Pin to previous source-perfect **one-ROM 3-layout R1at** original ROM SHA256: `486dca4b574d9a394075788bc974232d3b7452282f282e46c7dd3fca454d2c0a` ([R1at full report](https://github.com/Odourman/let-me-out/blob/research/main-iv-r1at-runtime-three-six-npc-x-20261116/docs/MAIN_IV_R1AT_ONE_ROM_THREE_RUNTIME_SIX_ANDROID_LAYOUTS_600_STELLA_2026-11-16.md)).

## Exact 600-frame Stella audit

| Test requirement | Measured result |
|---|---:|
| Original 2 M + 2 F + 1 SM + 1 SF full exact 8x9 white masks on same 9 physical scanlines | **600 / 600** |
| Source mask missing white pixels | **0** |
| Unexpected white pixels / ghost clusters | **0** |
| Full original yellow P0 + one M0 two-pixel diagnostic shot | **600 / 600** |
| Exact NTSC 262 scanlines and consecutive debugger frame IDs | **600 / 600** |
| Runtime layouts A/B/C in one BIN | **3**, all genuinely observed |
| Actual consecutive-frame transitions between source-perfect layouts | **75** |
| Transitions moving exactly one full large NPC copy pair by 12 GUI crop pixels | **75 / 75** |
| Multi-pair simultaneous jumps, illegal transitions | **0** |
| Full deterministic A→B→C→B→A phase proof, allowing one global frame-offset | **PASS**; offset **30** |

Stella coordinates refer to the measured 900×300 debugger image crop, NOT individual independent TIA color-clock coordinates:

| Stage | Actual source-perfect X positions M1/M2/F1/F2/SM/SF | Frames |
|---|---|---:|
| A | `75;107;147;179;243;303` | **145** |
| B | `75;107;159;191;243;303` | **303** |
| C | `87;119;159;191;243;303` | **152** |

## Minimal exact modification from prior approved R1at baseline

- All existing 9 physical scanline unrolled display kernels, all four original 8x9 source bitmap tables, yellow P0 player bitmap, M0 test-shot logic, NUSIZ1=$03 and cycle-perfect P1 resets are UNCHANGED.
- Only the 4th eight-frame slot's **pre-visible-line** dispatch changes from `JMP R1atA` to `JMP R1atB`, so frame phases A→B→C→B→A instead of A→B→C→A. No per-visible-scanline timing change.
- Selection uses `FRAMELO & $18`, each phase persists for eight frames. Measured transitions change only one duplicate pair's group X at a time. Difference uses the exact preverified P1 cycle schedules A=(28,40,56,66), B=(28,42,56,66), C=(30,42,56,66).
- The first R1au Actions run [43868724119](https://github.com/Odourman/let-me-out/actions/runs/43868724119) failed **only audit-manifest key mismatch** (`NUSIZ1` versus `NUSIZ1_value`), not an observed ROM graphics failure. The source metadata key was corrected; the rerun tested full 600 frames and passed.

## Source architecture & non-negotiable limitations

- This is now a reproducible **one-ROM runtime cycling demonstration** with six original Android sprite instances simultaneously visible and group-by-group movement, without flicker in tested original white masks. This does NOT prove individual independent X for all six: the duplicate big male and female copies remain separated by NUSIZ automatic-copy fixed relative spacing. Positions can only be switched among **three precompiled X layouts**, not general motion across all 160 active TIA color clocks.
- Only **one common nine-row Y band** was tested; C04 adjacent shifted-Y and actual close overlap/crossing were NOT tested. Also not integrated: brown PF walls, orange right exit/black keyhole, R2 gold key/O1 occlusion, R3/R4 scene switching, active moving gameplay shot, collision identity, audio/AI, PAL or all four F6 banks with differing code.
- P0 player was prepositioned away from white Android copy groups as an occlusion-control measure; the static M0 testsymbol is NOT proven attached to the player's hand or controlled by gameplay.
- No production `main`, draft PR #7, map cutover, AI/score/audio/gameplay rules, new mapper, design waiver, implementation step or independent VERIFICATION was authorized by this research.

## Project/verification gate check

- Live GitHub `docs/ROM_GATE_V018_AUTHORIZATION_2026-11-15.md`, `docs/ROM_GATE_V018_SCOPE.md` and `docs/ROM_GATE_V018_ACCEPTANCE.md` enforce full R1–R4 and independent VERIFICATION. A six-NPC common-Y research kernel addresses **part of C01**, but C04 requires adjacent Y bands and R2/R3/R4 remain.
- When this report was written, production main SHA was `f6b3fc76c59161e04e583dc8c0787332d2f261c7`. PR #7 remained **open draft, unmerged**, head `82667dae033f70570dce903f8e1d4866528be02a`. Neither was modified by MAIN IV research.

## MAIN IV recommended next RESEARCH (not implementation authorization)

1. Measure constrained X envelopes/actual pixel spacing for all six and formulate a **runtime slot scheduler** that never uses the demonstrated invalid first-M-to-F gap (30,40). Establish minimum safe spacing, crossings and missing sprites before declaring usability.
2. Separate **C04 staggered-Y** feasibility: same six original mask instances with neighboring scanline bands, worst-case per-scanline 76 CPU cycles, partial visibility/mask loss/flicker and user-approved silhouettes unchanged. Preserve fail-closed 600-frame evidence.
3. Assess PF walls/door raster writes and R2 key/O1 **only as separate feasibility budgets**. Integration belongs to explicitly authorized ROM DEVELOPMENT v0.18 and downstream independent VERIFICATION, not automatic research cutover.
