# LET ME OUT! – MAIN IV R1ay: same-frame original six-NPC masks at adjacent Y offsets

**Date:** 2026-11-16. **LOCAL RESEARCH PASS: 1,800/1,800 authentic Stella 6.7.1 frames.** NOT full R1/R4, not independent VERIFICATION, not production.

## Summary

Rebuilt from pinned [R1aq six-original-mask original](https://github.com/Odourman/let-me-out/actions/runs/43866445424), SHA256 `09e262958e9452ec3f61c3d93f2eea19ad03cda7ac52767ae72608e2f7b3a94b`, then shifted only the **precomputed per-scanline SM/SF 8x9 original bitmap immediate bytes** with transparent-zero padding.

- Canonical source registry `design/NPC_REFERENCE_8x9_masks.json`; original MaleRows/FemaleRows/SmallMaleRows/SmallFemaleRows/PlayerRows/ShotEnable tables are byte-identical.
- All four P1 `RESP1` cycle deadlines (28/40/56/66) and P0/M0 register schedules unchanged. No new raster instructions were inserted.
- Six complete full masks, two large male, two large female, one small male, one small female. Three physical Y-band variants; 600 consecutive actual Stella debugger PNG per variant, checked for exact per-mask pixel sets (at required Y offset), one yellow full P0 player, one two-pixel static M0 shot, and exactly 262 NTSC scanlines per frame.
- No white ghost pixels, no missing source-mask pixels, and correct per-frame HUD progression.

| Batch | SM delta Y in scanlines | SF delta Y in scanlines | Strict 600-frame pixel audit | ROM SHA256 |
|---:|---:|---:|---|---|
| 0 | +1 | −1 | **600/600 PASS**, 0 missing/extra | `f3d509e1c46b432bcc33a518647378c1332b4ff2564224a2ff36a62b90356633` |
| 1 | −1 | +1 | **600/600 PASS**, 0 missing/extra | `1abd8ab43c89ab5f95b446fb9172e0e83c96aff212cb9f7d761150271ffaf71a` |
| 2 | −2 | −1 | **600/600 PASS**, 0 missing/extra | `b5b75b5027692b8e8055901c79d462423eefa9ba6e0811db5b739e31a9bc7849` |

CI: [GitHub Actions run 43871126664](https://github.com/Odourman/let-me-out/actions/runs/43871126664), three parallel SUCCESS jobs.

Raw reproducibility packages including source, per-frame CSV and 600 PNG each: [batch 0](https://github.com/Odourman/let-me-out/actions/runs/43871126664/artifacts/14228136711), [batch 1](https://github.com/Odourman/let-me-out/actions/runs/43871126664/artifacts/14227613296), [batch 2](https://github.com/Odourman/let-me-out/actions/runs/43871126664/artifacts/14228336513).

## Interpretation and boundaries

**A major subset of authorized v0.18 acceptance C04 is technically demonstrated:** six fully intact original NPC silhouettes need not share a single source Y when two short NPC masks use their transparent top/bottom rows to shift ±1/±2 scanlines. This requires no extra per-row CPU cycles and retains yellow P0 and M0. It does NOT prove arbitrary free Y, continuous runtime Y motion, overlap/occlusion with players, PF walls, collisions, or independent six-NPC X motion.

All tested Y changes are static in separate ROM variants, while the original three runtime X layouts have previously been demonstrated in R1at. There is no yet verified **single** combined ROM with both runtime X changes AND shifted Y, and no brown PF wall/door/key in these Y variants.

## Next integration research

First validate [R1ax brown reflected-PF walls research branch](https://github.com/Odourman/let-me-out/tree/research/main-iv-r1ax-reflected-brown-pf-walls-20261116) in real Stella. Then assemble a single restricted R1/R4 research proof combining six masks, one or two static Y-offset profiles, the prior three runtime X modes, full P0+M0, and a brown PF border. Must re-run strict 600-frame audit across every state. Do not claim full R1 until independent six-X, wall collision and authorized full test gates; do not silently accept visual compromises.

Integrity: only research branches modified; no changes to main or blocked draft PR #7, no unapproved gameplay or mapper change; independent VERIFICATION is separate.