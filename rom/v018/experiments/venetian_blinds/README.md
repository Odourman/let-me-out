# Let Me Out! v0.18 – Venetian Blinds, R1 isolated diagnostics

This directory contains **original** 6502/DASM code investigating the historical *Video Chess* line-interleaving principle. This is **only** the explicitly approved NTSC R1 graphics feasibility scope. It is not a game or a validated six-android renderer.

## Three real ROM variants

- `vb_9_interleave.asm`: one 9-scanline raster band; even lines feed the original large-male bitmap, odd lines feed the original large-female bitmap into P1; P0 has a yellow 9-line player candidate and M0 an active shot.
- `vb_18_doubled.asm`: 18 scanlines; one original-row contribution per android on alternate lines, **twice** the approved vertical scale and only a diagnostic comparison.
- `vb_9_vdel.asm`: 9-line variant with VDEL1 enabled and a corrected delayed-GRP1 latch clear.

**P1 is repositioned with `RESP1` on every visible row**, and two independently updated 16-frame delay/X tables drive its intended horizontal position. `NUSIZ1=0` (no fixed-distance copies). No outside game's code has been copied.

## Build requirements

Ubuntu 24.04 GitHub Actions package versions: DASM `2.20.15~20201109+really2.20.14.1-2`, Stella `6.7.1+dfsg-1build2`.

```bash
sudo apt-get update
sudo apt-get install -y dasm stella xvfb xdotool imagemagick
bash rom/v018/experiments/venetian_blinds/build.sh
bash rom/v018/experiments/venetian_blinds/ci_capture.sh
```

The build emits one DASM bank, `.lst`, `.sym`, and a 16,384-byte F6 test ROM for each variant. The F6 binaries are exactly 4 repeats of the same 4K program bank; no extra sprites/RAM or bank-specific effect is claimed. `dist/SHA256SUMS.txt` is checked.

Real Stella evidence comes from an Xvfb-backed GUI after debugger `frame #13` and `frame #18`. Original 1366×900 `stella_full.png` images are required. The separate `ci_trace_probe.sh`, `ci_tia_traps.sh` and `ci_pc_cycle_probe.sh` are **instrumentation attempts**, not automatically valid timing evidence. The trained auditor must check actual debugger PC/scanline/cycle, not only that the command ran.

## Interpretation

An interleaved 9-line picture can contain, at best, only 5 of 9 rows for the male and 4 of 9 for the female. It therefore cannot be called full preservation of either reference mask. The 18-line experiment may provide more rows but changes perceived height, which is not an approved solution.

The earlier 600+600 frame test with six logical X positions in `../six_x_free/` is a separate and unsuccessful R1 experiment. Do not transfer its frame PASS/FAIL statuses to these different new ROMs.

**Main gates:** six independently located NPCs with four human-like original types, correct full-size yellow player and shot, acceptable visibility, real per-TIA cycle/deadline trace, R2 key coexistence, 600 consecutive Stella frames, independent VERIFICATION. These are not shown to pass by either the 9-line or 18-line experiment.

The original frozen independent verification commit `561d3baf00c6c4c4bd9bc46599a91dc693abdeba` is not modified. PR #7 must remain DRAFT. No full game, PAL, special cart, or later step is authorized.
