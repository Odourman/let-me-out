# LET ME OUT! – MAIN IV R1as, one real-time-switching ROM with all six source-perfect NPC masks

**Date:** 2026-11-16. **Status:** `LOCAL_RESEARCH_RUNTIME_TWO_SIX_MASK_X_LAYOUTS_600_PASS`; not full v0.18 R1, not production integration, no independent VERIFICATION.

## Reproducible evidence

- GitHub Actions [run 43867538154](https://github.com/Odourman/let-me-out/actions/runs/43867538154): **SUCCESS**. Tested source commit `f48c908cd821293420e321641d1f4748ab0b9cb9`.
- Artifact [14225728463](https://github.com/Odourman/let-me-out/actions/runs/43867538154/artifacts/14225728463): 16KB ROM, source, build script, DASM listing, 600 actual consecutive Stella 6.7.1 X11 PNG screenshots, frame-by-frame CSV audit, summary, SHA256.
- Actual R1as 16,384-byte standard F6/NTSC ROM SHA256: `fcac441cc076ce4af415bcbc7322b84dcb1d1d77810a885b87c6063ad0791ffd`.
- Both subkernels rebuilt from pinned previous **600/600 static perfect** ROMs: original R1aq batch0 SHA `09e262958e9452ec3f61c3d93f2eea19ad03cda7ac52767ae72608e2f7b3a94b` and R1ar batch0 SHA `55b5c8b0a85d657a23b00eacc3ce0738ce0defff725e3e630c96c5f0eb59852d`.

## NEW: actual runtime selection inside ONE ROM

- A kernel-selecting branch is executed **BEFORE first nine-row-band WSYNC**, `FRAMELO & $08`, toggling every eight frames. The per-row raster instructions are unchanged, cycle-exact in the tested two variants.
- Both display kernels render **exactly six** source-perfect original 8x9 white NPC mask instances: `M;M;F;F;SM;SF`. The duplicate M/M and F/F relative spacing is constrained by NUSIZ1=$03; not individually free X.
- Two confirmed and **different white X signatures in 900x300 Stella crop pixels**: `75;107;147;179;243;303` appeared **297 frames**; `75;107;159;191;243;303` appeared **303 frames**. Difference is a shift of large female group; all other positions unchanged.
- Strict **600/600** original six mask pixel-PASS, zero missing/extra white mask pixels, **600/600** correct NTSC 262, **600/600** intact original full yellow P0 and precisely one M0 two-pixel test shot, **600/600** consecutive debugger frame IDs.
- Both layout signatures repeated across many frames; these are actual different screen states from the same running BIN, not static scenes independently compiled into distinct cartridges.

## Scope boundaries and evidence quality

1. This is a substantial local technical advance: **one running ROM can switch a female group position without degrading any of six canonical mask shapes**. It does NOT prove six individually movable enemies, full horizontal movement, crossing, valid visual overlap, AI or any playability.
2. Nine exact physical raster rows are used. No 14-row waiver; the yellow M0 shot is a static diagnostic symbol and is NOT guaranteed to remain beside the repositioned player's hand.
3. The demonstration bank structure is four identical 4KB bank copies; no actual four-bank F6 switching has been implemented. No additional RAM or hardware mapper.
4. Full R1 remains BLOCKED pending C04 staggered Y stress, independent usable X coverage, integration with brown PF walls and door. R2 gold key/O1, R3 one-sided orange door+black keyhole, R4 moving/collision stress remain not done here.
5. No approval to merge research into main/draft PR #7, no new gameplay step and no independent organizational Verification signoff.

## Next isolated research

R1at: one ROM with **three** preverified six-mask kernels selected each eight frames: first static baseline, then female group shifted 2 CPU cycles, then male group shifted 2 cycles. Require three **different** measured X signatures, >100 frames each and full 600/600 pixel/NTSC/P0/M0 proof. Compare ROM and raster footprint. Still not a general X positioning routine.
