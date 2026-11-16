# LET ME OUT! MAIN IV – R1az: three runtime Y profiles, six original 8x9 NPCs

**Date: 2026-11-16. LOCAL RESEARCH PASS: 600/600 real Stella 6.7.1 screenshots.** This is not full R1/R4, not independent VERIFICATION, and not production implementation.

## Reproducible result

- [GitHub Actions success run #43871769128](https://github.com/Odourman/let-me-out/actions/runs/43871769128), strict six-original-mask/frame audit = **600/600**.
- A single 16,384-byte standard F6/NTSC ROM, SHA256 `8c87ded77195f7171d1649e73b6406b1526f727dd57b4951f44ea5766d84b840` (4 identical 4KB banks; no actual bank switching).
- Three precomputed nine-raster-row Y kernels for exact original large male ×2, large female ×2, small male ×1, small female ×1, full original yellow P0 and one static M0 test shot. No source original sprite mask byte altered; P1 RESP1 deadlines identical c28/40/56/66.
- The same ROM changes the small male / small female Y positions every nominal eight frames via `FRAMELO & $18` choosing A/B/C before the first sprite `WSYNC`.

| Runtime Y profile | Small male Y offset | Small female Y offset | Actual frames observed |
|---|---:|---:|---:|
| A | +1 physical raster row | −1 physical raster row | 297 |
| B | −1 physical raster row | +1 physical raster row | 151 |
| C | −2 physical raster rows | −1 physical raster row | 152 |

**All 600**: six full source-exact original 8×9 silhouettes; zero missing/extra white pixels; one complete yellow P0 player, exactly one static yellow M0 shot; every frame 262 NTSC scanlines and monotonic 600-frame debugger capture. Individual Y variants were first demonstrated independently in [R1ay 1800-frame source-verified run](https://github.com/Odourman/let-me-out/actions/runs/43871126664).

Three-profile audit is not fooled by a ROM containing three kernels but showing only one: it fits each observed white silhouette to all three specified canonical Y profiles independently, rejects a frame with any partial source mask, and demands each of the three distinct profiles be observed at least 100 times.

**Evidence:** [Complete R1az ROM, source, DASM listing/symbols, SHA256 manifest, 600 authentic PNGs, per-frame CSV, JSON](https://github.com/Odourman/let-me-out/actions/runs/43871769128/artifacts/14227502995).

## Boundaries and next research

This proves **runtime Y transitions for the two smaller original silhouettes as a group of static precomputed raster kernels**; it is not freely selectable independent Y for six NPC, dynamic Y physics, collision/occlusion, full moving projectile, different-Y overlapping playfield stress, gold key or right orange door. Large male/female pairs remain NUSIZ-coupled in X.

The separate R1at runtime-X proof shows three same-Y horizontal positions, but **no single ROM combines both runtime X movement AND runtime Y changes** yet. R1ax mirrored-brown-PF border remains separately under investigation. The next useful R1/R4 research step is integrate these two, then independently verify complete six originals, P0/M0, PF walls and 262 NTSC frames across transitions.

Keep `main` and production draft PR #7 unchanged; stop at research, do not claim full v0.18 R1–R4 or independent VERIFICATION without full authorized verification.