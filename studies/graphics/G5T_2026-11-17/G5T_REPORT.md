# LET ME OUT! — G5T GRAPHICS II report, 2026-11-17

**Status:** GRAPHICS SOURCE-ONLY, NOT APPROVED, NOT STELLA TESTED, NO ROM.

## Source provenance
- GitHub main source commit: `57a4f4954f5699b3d20893d12893f901fe767f7a`
- v0.11 grid blob: `820a74e5fb77c818ffb1286c5b23698d4374e771`; v0.19 grid blob: `0e449f97f87bd9b403476fd1435398042eaee285`
- MAIN VII authorization in Issue #10 and `docs/gates/G5T_MAIN_VII_V011_V019_ROOM_MAP_COMPARISON_AND_NEXT_USER_GATE_2026-11-17.md`.
- Future five-enemy decisions C1/D1/E1 in `docs/gates/G5S_MAIN_VII_C1_D1_E1_USER_APPROVAL_DECISION_RECORD_2026-11-17.md`. These approve **five distinct prevalidated spawns as a future policy, NOT any exact pool**.

## Grid comparisons (interior 38×20 = 760 cells)
| Pair | Old wall cells | v0.19 wall cells | Retained source candidates |
|---|---:|---:|---:|
| A01 / A_OPEN_01 | 64 | 36 | 20 -> 18 |
| B01 / B_OPEN_01 | 156 | 48 | 13 -> **9** |
| C02 / C_OPEN_01 | 124 | 64 | 18 -> 16 |
| D01 / D_OPEN_01 | 168 | 60 | 15 -> 15 |

**A:** old divided L corners and inner bars simplify to four clean corner arms; wider free arena. Historical anchor omissions: (9,6),(29,6).

**B:** old pillars and obstacles simplify to four long wall stubs. Very open, but risks visual sameness and insufficient interesting hunting obstructions. Historical omissions (9,3),(29,3),(9,15),(29,15). Nine retained source anchors are NOT five validated future spawnpoints.

**C:** old dense corner formations and inner crossbars become four angled partitions and clear openings. Visual character preserved most strongly relative to an airy room target. Historical omissions: (14,15),(24,15).

**D:** old central blocks and other pillars simplify to opposed short arms with broad central arena. All 15 historical anchor candidates remain listed, but none is gameplay verified.

## Validation and rendering limits
All eight source grids checked as exact 40×22 symbols. Each has x=0 closed and D at x=39,y=9..12 only, with no other right-side openings. Read the per-grid FNV32 and count in `VALIDATION.json`. SVG renderer reads original JSON and paints each wall/door run from its source characters, without geometric reinterpretation; all images have the same cell size and orientation. The orange D is a *source map marker*, not a claim about an implemented Atari keyhole or a validated 2600 palette.

Spawn overlays are a separate drawing layer: old `candidate_positions`, new `reusable_old_S0_candidates_for_geometry_only`; red crosses denote old positions absent in the new source candidate list. Neither layer changes the map grid. Overlay candidates are not technical proof of 8×9 collision, player reachability, AI pathfinding, key or exit access, real NTSC raster timing, PF/BL encoding or implemented ROM. None was independently verified in Stella.

**Advisory view:** A_OPEN_01, C_OPEN_01 and D_OPEN_01 are strongest visual matches for airy but visually distinct spaces; B_OPEN_01 may feel too empty. MAIN VII should request an exact, explicit user choice. Suggested question: "Godkänner du A_OPEN_01, B_OPEN_01, C_OPEN_01 och D_OPEN_01 i exakt nuvarande 40×22-form som planerad kartbas för en framtida separat godkänd version?" Include warning that B is simplistic and that all future spawns and S05 / ROM feasibility remain unverified. This study **does not select any map or start G6/F12**.
