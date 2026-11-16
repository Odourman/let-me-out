# Let Me Out! – MAIN IV R1aj / R1ai / R1ah / R1ag, independently auditable research handoff

**2026-11-16. Scope: research-only isolated Stella experiments.** NOT full v0.18 R1, NOT six independent NPCs, NOT production implementation or organizational independent VERIFICATION.

## Major advance: four DIFFERENT original 8x9 NPCs via P1, plus full yellow P0 player and one M0

- Four canonical source shapes on the **same nine physical raster rows**, all white through P1 and measured in real Stella 6.7.1 screenshots: LARGE MALE, LARGE FEMALE, SMALL MALE, SMALL FEMALE.
- Player P0 and one visible static M0 symbol retained simultaneously. No original 8x9 mask byte changed. Small-male/small-female masks are pinned to exact main design reference blob SHA `058800a4c1904d1ff289e7e61b3902aa111ba16d`.
- [R1aj Actions run #43863021994](https://github.com/Odourman/let-me-out/actions/runs/43863021994): batch 0 **600/600 strict PASS**, correct original masks, P0, M0, 262 NTSC scanlines, zero extra or missing white pixels. Actual 16,384-byte F6/NTSC ROM SHA256 `ff0f1c64ffff1915cef934f224b3f3d780bc2de6cc52038d62666904c1f0f263`.
- Four measured GUI-crop-mask-coordinate groups in the successful batch, NOT 160-CC general freedom: C `(75,135,195,255)`, D `(87,135,207,267)`, E `(75,147,207,267)`, F `(87,147,219,279)`. Positions given in 900x300 GUI screenshot crop, not TIA color-clock coordinates.
- [R1aj batch 0 full evidence](https://github.com/Odourman/let-me-out/actions/runs/43863021994/artifacts/14224576761) includes 600 authentic consecutive PNGs, exact source, DASM listing and sym, 600-frame CSV, audit summary, ROM and SHA256.

## R1aj second variant FAIL: precise limit

- Batch 1 attempts a fourth `RESP1` **two CPU cycles later**; ROM SHA256 `4d2f143b5a59c0110d5e22bfc6e1fd9c8955f6f17fc8bc33bc770c233c61748f`.
- **450/600 strict PASS**, remaining **150 FAIL**. All **600** still retain all four white original masks without lost or extra white pixels; **150/600** have incorrect 262-scanline HUD signature and **10 yellow non-player pixels rather than exactly 2**, causing static M0 test to fail. The failing mode is late F at third X219, fourth X291. Do NOT call the run a full PASS or infer a hardware-level invariant.
- This shows the raster timing/shot side needs a tighter budget even when all four white masks remain intact. It does NOT prove a fifth NPC impossible.
- [R1aj batch 1 failed-but-preserved evidence](https://github.com/Odourman/let-me-out/actions/runs/43863021994/artifacts/14224696960).

## Prerequisite R1ag: separate X/mask-order

- [R1ag report](https://github.com/Odourman/let-me-out/blob/research/main-iv-r1ag-mask-order-close-x-20261116/docs/MAIN_IV_R1AG_MASK_ORDER_24_PAIRS_3600_STELLA_2026-11-16.md) / [Actions](https://github.com/Odourman/let-me-out/actions/runs/43861230291): **six jobs x 600=3,600/3,600 strict PASS**.
- Full original large male/female P1 masks work in **either left/right draw order** within measured discrete pairs, including minimum tested eight-cycle RESP1 separation. No real mask overlap or live universal X sorting proven.

## Prerequisite R1ah: third original NPC

- [R1ah report](https://github.com/Odourman/let-me-out/blob/research/main-iv-r1ah-three-full-original-p1-20261116/docs/MAIN_IV_R1AH_THREE_ORIGINAL_P1_2_PASS_2_FAIL_2026-11-16.md) / [Actions](https://github.com/Odourman/let-me-out/actions/runs/43862062578): **two 600/600 strict PASS**, two 150/600 FAIL.
- Failed pictures showed missing WHITE third-P1 pixels when third small-male screen position intersected fixed yellow P0 player, but all 600 yellow players/M0 were intact and ghosts zero.

## Prerequisite R1ai: P0 overlap isolation

- [R1ai report](https://github.com/Odourman/let-me-out/blob/research/main-iv-r1ai-player-p0-separation-20261116/docs/MAIN_IV_R1AI_P0_OVERLAP_ISOLATION_1200_STELLA_2026-11-16.md) / [Actions](https://github.com/Odourman/let-me-out/actions/runs/43862530097): **two 600/600 strict PASS**.
- Only player initial P0 RESP0 positioning delay changed, from `LDX #12` to `LDX #9`; exact three-NPC source masks and all P1 timing maintained. Previously lost 5,700+4,200 white pixels became ZERO. This strongly supports P0 masking P1 white pixels during visual overlap as the R1ah failure, not a universal P1 rendering time ceiling.
- Static yellow M0 test shot no longer necessarily sits beside the moved player's hand; never call this working gameplay shooting.

## What is still NOT solved

1. Full six NPC instances: second large male and second large female still missing in a SAME-frame, same-Y full-pixel proof.
2. Independent free X movement/crossing, close/overlap stress, Y movement, 14-row R1s technique compatibility and P0/P1 ownership transition.
3. Game PF left wall/right door orange and black keyhole, R2 gold key and O1, R3/R4 complete integration, moving shot and real enemy identification, 128-byte RAM/data lists, PAL and full game.
4. No independent VERIFICATION, no permission to merge production draft PR #7. F6 has not been demonstrated as four actually different banks; the proof ROMs repeat one 4KB bank four times.

## Recommended next RESEARCH (not a new implementation authorization)

R1ak cycle/visual feasibility: investigate whether NUSIZ automatic copy plus selective GRP updates can add the **second large male and female** as full original mask instances without additional per-row writes. Start with a fifth NPC, do not assume full free X from copies. Fallbacks to evaluate separately: P0 post-player reuse and specialized two-line sections, all while preserving shot and exact source bitmap rows. First make a static register-deadline table and fail-closed 600-frame Stella test. Preserve research/implementation/verification boundaries; no gameplay, mapper, or design waiver.

## Integrity

Main SHA was independently checked unchanged at `f6b3fc76c59161e04e583dc8c0787332d2f261c7`; draft PR #7 HEAD unchanged at `82667dae033f70570dce903f8e1d4866528be02a`. The above experiment branches are separate research lineage only.
