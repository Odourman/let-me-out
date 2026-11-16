# Let Me Out! MAIN IV – R1af 32 independent cycle pairs, Stella research

**Date:** 2026-11-16. **Status:** LOCAL RESEARCH PASS only; full R1 and independent VERIFICATION remain blocked.

The R1ae-derived isolated test kernel has been run in eight independent DASM/Stella 6.7.1 jobs using standard F6/NTSC, unchanged original 8x9 large-male and large-female P1 masks, one intact yellow original P0 player, and one static yellow M0 test shot.

- [Jobs batches 0–3](https://github.com/Odourman/let-me-out/actions/runs/43858971838): SUCCESS, 2400/2400 correct frames; code commit 0a05af256379c06aed0999973e409729f949ed8b.
- [Jobs batches 4–7](https://github.com/Odourman/let-me-out/actions/runs/43859411670): SUCCESS, 2400/2400 correct frames; code commit 79ac52868b03e1be1fd740206c6cc4f3082e14cb.
- **32 distinct tested X-pairs**; 8 distinct actual X positions for each P1 figure. X values are screenshots' 900x300 GUI crop pixels, not TIA color clocks.
- Original male observed X: 75, 87, 99, 111, 123, 135, 147, 159.
- Original female observed X: 147, 159, 171, 183, 195, 207, 219, 231.
- Largest tested start-point gap: 156 GUI pixels (78 TIA color clocks on this scale), with full per-frame pixel accuracy.
- **4,800/4,800** authentic consecutive screenshot frames correct, 262 scanlines/frame, 0 missing original white pixels, 0 extra white ghost pixels, unchanged yellow P0 and exactly one M0 per frame. Four modes per batch, with correctly measured mode phase.
- Original R1ae parent 16K ROM SHA256: 05606a5fd7426df00941be5621ca46c113df794c4ac3fa0f00f0e15cca66a993.

## What is not solved

This demonstrates only **two** P1 figures, not six independent androids. The first figure is always left of the second. There is no crossing or overlap; in this exact microkernel the RESP1 operations require at least eight CPU cycles between them (about 24 TIA color clocks), and the actual tested minimum gap is 10 cycles. R1ae/R1af use nine source raster rows while the separate five-android R1s uses a fourteen-row presentation and a different resource allocation, including P1 register writes near cycles 45/66, P0 writes near 53/56, and M0 handling at 48. No direct merge is proven.

No door, key, O1 occlusion, full playfield, mobile bullet, gameplay collision, AI, PAL, different cartridge, or verified R1/R2/R3/R4 is included. Research branch only: main and production draft PR #7 were not changed.

## Next proof needed

1. **R1ag**: dynamic P1-mask ordering (male/female may switch left/right) and close-X geometry.
2. **R1ah**: a third complete original same-Y NPC with P0 player and M0 test bullet conserved.
3. Only then examine technical integration against R1s and all 6 NPC plus PF/door and R2 key. No further implementation step is authorized by this report.

## Source and artifacts

Source: rom/v018/experiments/main_iv_r1af_xmatrix on this branch. Each GitHub Actions run has eight jobs total across two runs, one artifact per batch (all 600 raw screenshot PNGs, assembler source and listing/symbols, SHA256 and fail-closed frame audit). This is not independent VERIFICATION; artifact and commit need separate downstream review.
