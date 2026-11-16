# R1/v0.18 NTSC – actual developer handoff pointers (2026-11-16)

**Status: BLOCKED / NOT ACCEPTED for full R1.** These are *only* independently reproducible ROM DEVELOPMENT self-tests. Neither MAIN nor independent VERIFICATION has approved full R1. VERIFICATION stays STANDBY. Do not merge PR #7.

## Exact source and evidence

- GitHub report commit: `08f44e61d8da6cb864021bc205092ea3d925dbd7`. Source branch `rom-dev/v018-r1-independent-xy-20261116`, created from `82667dae033f70570dce903f8e1d4866528be02a`. Final source checkout must pin an actual commit from the branch, **not** floating PR #7.
- [Technical handoff to MAIN](TO_MAIN_R1.md) • [Scoped T01–T16 delta](TEST_MATRIX_R1_DELTA.csv) • [Reproducible readme](README_RESULTS_R1.md).
- **[Complete Google Drive evidence ZIP](https://drive.google.com/file/d/1j8r7vzgKmx_XiRRzvZKGFZWlJ776t3F1/view?usp=drivesdk)** under *Atari 2600 – Let Me Out!* project folder (ID `1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u`). Size **5,541,354 bytes**, SHA-256 **`68e538758fd4b452f493242a5fb8e86f527cee18b004483825fc3c05cadbc124`**. **926 files total**; 925 internal SHA-256 manifest rows checked, plus ZIP CRC. 600 genuine two-X, 48 genuine two-X/Y, 64 N3..6 and 64 six-sweep genuine raw Stella images; no software-generated images submitted as emulator proof.
- Original canon: `main/design/NPC_REFERENCE_8x9_masks.json` blob `058800a4c1904d1ff289e7e61b3902aa111ba16d`; on R1 branch available byte-identically as `canon_masks.json`. Four source types unchanged.

## Positive limited developer results

- [Actions #43911479618](https://github.com/Odourman/let-me-out/actions/runs/43911479618): **600/600** consecutive Stella 262-scanline frames with TWO upright source-exact M/F originals in four factorized, independent X pairs, P0/M0/brown PF. F6 ROM (16,384 B) SHA256 `affec8170c9e0dece70975b16702c227ec1546b2fb317564c996943169313538`.
- [Actions #43912321860](https://github.com/Odourman/let-me-out/actions/runs/43912321860): **48/48** source-exact two-NPC XY, **16/16** factorized combinations of independently selected 2×2 X and 2×2 Y, with 1-scanline Y offset range, P0/M0/PF intact. F6 ROM SHA256 `c668111c19f18de859631f18b95999571c867057455bb8060f34255a7ed9a6c6`. Stable RIOT-cache source `build_two_xy.py`; indirect-ROM-pointer variant retained separately as FAIL 24/48.
- [Actions #43909428292](https://github.com/Odourman/let-me-out/actions/runs/43909428292): three, four and five exact original mask instances **16/16 per N** at **fixed** X; they do not prove individual X/Y freedom.
- [Actions #43910212031](https://github.com/Odourman/let-me-out/actions/runs/43910212031): real Stella two-NPC raster write traps `RESP1 c30/c54, GRP1 c35/c57` at scanline124; `NUSIZ1=$01` and `HMOVE` also trapped separately in VBlank.

## R1 blocker

- Initial SIX unrolled P1-trigger schedule 0/16 source-exact; four additional schedules [Actions #43910212163](https://github.com/Odourman/let-me-out/actions/runs/43910212163) **0/16 each**. **0/80** test six-avatar frames successful, despite 262 NTSC, P0/M0 and PF intact 80/80. Fourteen or fewer P1 CPU cycles remaining cannot by itself guarantee all six complete original masks; raster copy interference remains. No proof of six independent X/Y.
- The older R1ba [fixed-NUSIZ research result](https://github.com/Odourman/let-me-out/blob/research/main-iv-r1ba-integrated-xyz-pf-20261116/docs/MAIN_IV_R1BA_INTEGRATED_X_Y_PF_SIX_ORIGINALS_600_STELLA_2026-11-16.md) renders all six with paired/coupled positions, not individually free.
- T01/T02/T04/T07: unresolved or FAIL at full R1 scope. T15 verification not activated; no R2/R4/R1+R3 integration or main changes.

Source baseline branch + full ZIP cover every negative and positive claim. MAIN V reviews R1 blocker and issues any next separate scoped work order. No design-waiver inferred.
