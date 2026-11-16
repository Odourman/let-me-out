# LET ME OUT! – MAIN IV R1ag: mask order reversal and close P1 timing

Date: 2026-11-16. **LOCAL RESEARCH PASS**; NOT full six-android R1 and NOT independent VERIFICATION.

## Reproducible evidence

- [GitHub Actions run 43861230291](https://github.com/Odourman/let-me-out/actions/runs/43861230291): **SUCCESS** for all six parallel jobs, commit `882248822dc9cec3b5b75d6130f953bdb5afcb63`.
- 3,600 authentic consecutive Stella 6.7.1 screenshot frames across six jobs, each 600 in a 16 KiB standard F6/NTSC proof ROM.
- Every job has 600/600 strict per-pixel PASS, 262 NTSC scanlines, zero missing original white mask pixels, zero extra white ghost pixels, entire original yellow player P0 and one exact two-pixel M0 shot in all frames.
- Existing original MaleRows and FemaleRows 8x9 data retained byte-for-byte; only load order altered. Separate analysis expects the actual programmed mask order (not swapped identities).

## Six scenarios and observed local screenshot crop X positions

| Job | First original P1 mask | Second original P1 mask | Tested X pairs (GUI crop, not TIA color clocks) | 600-frame result | ROM SHA256 |
|---:|---|---|---|---|---|
| 0 | large female | large male | (75,147), (87,147), (75,159), (87,159) | PASS | `bb2b7c6d0901608633a784c2980f2846127bf28938e30b27170c6da53c1eb140` |
| 1 | large female | large male | (75,135), (87,135), (75,147), (87,147) | PASS | `28e1b7e1c9f1be1630bc9d809886024ab109c8b54d19dbaeed1df87dd85e3340` |
| 2 | large male | large female | (75,135), (87,135), (75,147), (87,147) | PASS | `4188d0c22a2c9b908de37af1f257e8a4c25799038c938976323204cedd46dbcd` |
| 3 | large female | large male | (123,183), (135,183), (123,195), (135,195) | PASS | `fd1a313cedbffdd92161cf86d1389ad6feb9712f35b58b1e6820a13c017d5392` |
| 4 | large male | large female | (123,183), (135,183), (123,195), (135,195) | PASS | `1ed0d3994de45bf08b8ed8b592a63bf8c5379b5b0171f8b6e4cde68d1e2439e9` |
| 5 | large female | large male | (75,219), (87,219), (75,231), (87,231) | PASS | `ddf1928866384ab1d9475ea1cdecdd8fbd0d77bf587300fa5f7d1a5e53dd469b` |

The minimum sampled RESP1 interval is **8 CPU cycles** (24 TIA color clocks). This is an instruction spacing limit in the CURRENT MICROKERNEL, not a demonstrated minimum NPC spacing for every Atari 2600 implementation. No actual overlap is verified. The roles can be inverted in separate compiled test variants, but no universal live X-sorter or one-ROM dynamic mask swap has been built.

## Remaining blocker

Only two full original NPC masks + P0 player + M0 test shot on nine physical rows are demonstrated. Six distinct NPC, movement freedom throughout 160 TIA color clocks, overlap/occlusion, use of 14-row R1s, PF wall, key, orange right door, collision identity and integrated R1–R4 remain unverified and blocked. Do not modify the game specification, introduce mapper changes, assert full R1 PASS or merge production PR #7.

## Evidence artifacts

- [Batch 0](https://github.com/Odourman/let-me-out/actions/runs/43861230291/artifacts/14222774880)
- [Batch 1](https://github.com/Odourman/let-me-out/actions/runs/43861230291/artifacts/14223382589)
- [Batch 2](https://github.com/Odourman/let-me-out/actions/runs/43861230291/artifacts/14223222764)
- [Batch 3](https://github.com/Odourman/let-me-out/actions/runs/43861230291/artifacts/14222999124)
- [Batch 4](https://github.com/Odourman/let-me-out/actions/runs/43861230291/artifacts/14223417399)
- [Batch 5](https://github.com/Odourman/let-me-out/actions/runs/43861230291/artifacts/14224000348)

## Next

R1ah: inspect the possibility of a third **different complete original** NPC mask on all nine raster rows, alongside both current P1 NPC, full P0 player, and one M0. Preserve canonical source mask bytes and independent fail-closed Stella pixel audit. Research only; no independent VERIFICATION.
