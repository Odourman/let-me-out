# LET ME OUT! – MAIN IV R1ak, NUSIZ1-only feasibility scan

**2026-11-16. Status: NEGATIVE full-six result, positive limited extra-original-copy evidence. Research only; not independent VERIFICATION.**

## Source and methodology

- [GitHub Actions #43864335638](https://github.com/Odourman/let-me-out/actions/runs/43864335638), commit `bfd7adc6a8fdf68e9ca46f5c664a135a73823a68`.
- From R1aj **600/600 fully successful four-canonical-P1-mask ROM**, SHA256 `ff0f1c64ffff1915cef934f224b3f3d780bc2de6cc52038d62666904c1f0f263`.
- Each of six candidate ROMs changes ONLY the `NUSIZ1` initialization immediate byte while leaving all source mask rows, four P1 `RESP1` strobe timestamps, yellow player P0, yellow M0 and 262-line NTSC scaffold untouched.
- Six modes tested: $00 (single), $01 (two close, original control), $02 (two medium), $03 (three close), $04 (two far), $06 (three medium). Every mode produces 600 actual consecutive Stella 6.7.1 screenshots, 600-frame CSV, strict original mask classification and complete evidence artifact, including on failed variants.
- A **strict six** result requires exactly two large male, two large female, one small male, one small female (all original 8x9 bitmap rows complete and individually distinguishable), plus full yellow original P0 player, exactly one M0 test projectile, and correct NTSC timing in all 600 frames. Merely counting 6 white groups is not a pass.

## Observations from actual Stella evidence

| NUSIZ1 | Strict 4 original-types frames | Strict required 6 frames | Screen outcome |
|---|---:|---:|---|
| $00 | 0/600 | 0/600 | Zero observed complete white groups under same close-copy retrigger routine |
| $01 control | **600/600** | 0/600 | Four original masks M,F,SM,SF, full no-ghost baseline |
| $02 | 0/600 | 0/600 | Distorted/missing original shapes in all four selector modes |
| $03 | **300/600** | 0/600 | 5 or 6 fully shaped groups in some selector modes but wrong types and/or incomplete masks in others |
| $04 | 0/600 | 0/600 | Original shapes not preserved; only one malformed detected group |
| $06 | 0/600 | 0/600 | Extra copies appear but white masks corrupted/merged |

**R1ak $03 diagnostic distribution:** 150 frames have 6 visible groups `M;M;F;SM;SF;SF`, all individually full source masks, but composition is **two M, one F, one SM, two SF**, not required 2M/2F/SM/SF. Another 150 frames have five complete `M;F;SM;SF;SF`, while other two modes have damaged or anomalous copies. This is why strict six is ZERO, even though a frame may contain six perfect source masks.

**Important:** The cluster classifier partitions at a >16 GUI-pixel separation and labels source-exact 8x9 silhouettes. Overlapping silhouettes are not disentangled and cannot be claimed as individual full masks from this evidence. The mode $03 cases are real measured patterns, not independently verified R1.

## CPU timing mechanism and recommended follow-up

Atari 2600 P1 `NUSIZ=011` offers close and medium automatic copy starts relative to each `RESP1` trigger. The documented +17 and +33 TIA color-clock offsets suggest that the first/second full copies could both start before a subsequent reset **only if enough time remains between `RESP1` strobes**.

The original R1aj proven C/D/E/F mode gaps are usually 8–10 CPU cycles, corresponding to only 24–30 TIA color clocks. To generate a second large male/female copy, a candidate cycle-fixed proof must give their strobes at least 12 CPU cycles separation without losing the two small masks or the P0/M0 shot.

Next isolated probe [R1al research branch](https://github.com/Odourman/let-me-out/tree/research/main-iv-r1al-six-original-p1-timing-20261116) tries all four mode loops at `RESP1` CPU cycles **28, 40, 52, 62**, using `$03`, with final CPU c73 before next WSYNC. This is a testable hypothesis, NOT an assumed solution.

Hardware references: [Retro Isle TIA notes](https://www.retroisle.com/atari/vcs/Technical/Hardware/TIAnotes.php); [batari Basic NUSIZ modes](https://www.randomterrain.com/atari-2600-memories-batari-basic-commands.html).

No changes authorized to game canon, production main branch, draft PR #7, 16KB F6 mapper or independent VERIFICATION gate.
