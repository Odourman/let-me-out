# LET ME OUT! – MAIN IV R1aq–R1as technical research handoff

**Date:** 2026-11-16. **Authority:** research evidence only. Not an R1 or R4 full-scene PASS, not independent VERIFICATION, not a production merge.

## Proven same-Y six-original graphic feasibility (R1aq)

[GitHub Actions run 43866445424](https://github.com/Odourman/let-me-out/actions/runs/43866445424) is **SUCCESS** in both batches. Each source-pinned NTSC/F6 diagnostic draws all six white 8x9 original NPC instances simultaneously on the same nine raster rows using P1:

- large male ×2, large female ×2, small male ×1, small female ×1;
- complete original yellow player on P0 and exactly one static yellow M0 test shot;
- 600/600 consecutive genuine Stella 6.7.1 GUI screenshots in each batch, or 1,200/1,200;
- **zero missing white original-mask pixels and zero extra white pixels**, every frame 262 NTSC lines;
- six masks originate from exactly the four canonical original source tables, not six different masks.

R1aq batch 0 SHA256: `09e262958e9452ec3f61c3d93f2eea19ad03cda7ac52767ae72608e2f7b3a94b`.
R1aq batch 1 SHA256: `eb91ddcf197c6f16dbea6e54a806b6b41f6c5d642eab74baa22fa6e9de9e4461`.
Evidence: [batch 0](https://github.com/Odourman/let-me-out/actions/runs/43866445424/artifacts/14225747192), [batch 1](https://github.com/Odourman/let-me-out/actions/runs/43866445424/artifacts/14225557646).

## More than one six-mask coordinate layout (R1ar)

[GitHub Actions run 43866982533](https://github.com/Odourman/let-me-out/actions/runs/43866982533) is overall FAILURE by design because the strict audit rejects one of its three cases:

- **batch 0: PASS 600/600**, with female duplicated P1 group shifted while the male group remains unchanged; ROM SHA `55b5c8b0a85d657a23b00eacc3ce0738ce0defff725e3e630c96c5f0eb59852d`.
- **batch 1: PASS 600/600**, male and female reset time both +2 CPU cycles; ROM SHA `b6d454e53769f1ad17c4441f4784c4f2a8936712e61faf500d51f666dae77080`.
- **batch 2: FAIL strict six**, only five exact masks (`M,F,F,SM,SF`), although all five and the yellow P0/M0 are intact. This is a negative boundary result: moving the first male P1 reset later without allowing enough time before the female reset loses the automatic extra male copy.

Full genuine 600-frame artifacts: [batch 0](https://github.com/Odourman/let-me-out/actions/runs/43866982533/artifacts/14225682782), [batch 1](https://github.com/Odourman/let-me-out/actions/runs/43866982533/artifacts/14226381539), [batch 2 FAIL](https://github.com/Odourman/let-me-out/actions/runs/43866982533/artifacts/14226196876).

## First single-ROM runtime switching (R1as)

[GitHub Actions run 43867538154](https://github.com/Odourman/let-me-out/actions/runs/43867538154) is SUCCESS for **600/600 real frames**.

- **One** 16,384-byte standard F6/NTSC ROM (four identical 4096-byte banks), SHA256 `fcac441cc076ce4af415bcbc7322b84dcb1d1d77810a885b87c6063ad0791ffd`.
- Two *separate unrolled nine-row scanline kernels* stored in that same ROM, selected at runtime via `FRAMELO & $08` (nominal eight-frame hold).
- Two screenshot-crop coordinate signatures actually observed by strict pixel audit:
  - `75;107;147;179;243;303`: 297 of 600 frames.
  - `75;107;159;191;243;303`: 303 of 600 frames.
- This is **real runtime X movement of the doubled large-female P1 group only**, within fixed discrete alternatives. The two large-male positions and the two small-mask positions are unchanged.
- All 600 frames: the exact `2M,2F,SM,SF` source mask counts; each distinct 8x9 original intact, no white ghost/missing pixels, one complete yellow P0 player, exactly one static M0 test shot; 262 NTSC lines/frame.

[Full R1as artifact](https://github.com/Odourman/let-me-out/actions/runs/43867538154/artifacts/14225728463) contains the ROM, source, DASM listing/symbols, full raw consecutive Stella PNGs, per-frame CSV, and JSON audit.

## Crucial limitations / next gate

This is not six independent 160-color-clock X coordinates. In the successful kernel each duplicated male pair and female pair is separated by NUSIZ-defined fixed geometry (cannot freely overlap/cross), and each available layout is precompiled. Moving the male reset +2 while holding the female reset fixed (R1ar batch 2) does not retain the second male mask.

The live two-layout test also does **not** show wall playfield, right-door PF asymmetry, R2 gold key or O1 occlusion, actual moving hand-fired M0, collision identification per NPC, free Y, close/overlap stress, six-NPC independent arbitrary positions, or full R1–R4 diagnostics. 600 consecutively advanced debugger frames are a reproducible graphics proof, **not independent VERIFICATION**.

Next research test **R1at** independently advances the duplicated male pair earlier by moving only its `RESP1` call, while holding its original `GRP1` deadline and all female/small reset cycles fixed. It must pass 600 real Stella frames before any runtime integration. If infeasible, investigate segmented specialized kernels, measured register trace, and precomputed constrained but gameplay-useful NPC movement; report hard independent-X limitation rather than silently accepting a waiver.

**Production boundary:** no merge to main, no change to blocked draft PR #7, no extension beyond authorized v0.18 R1–R4 diagnostic, no PAL/cutover/new mapper; independent VERIFICATION remains separate.
