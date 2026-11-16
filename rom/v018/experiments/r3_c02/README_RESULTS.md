# Let Me Out! — NTSC v0.18, isolated R3 C02 right-door diagnostic

**Only ROM DEVELOPMENT developer self-tests.** Not R1/R2/R4/full-game proof and not independent VERIFICATION.

## Main outputs

- `TO_MAIN_R3.md`: technical handoff and result boundaries.
- `TEST_MATRIX_R3_DELTA.csv`: fresh developer status T01–T16; don't borrow earlier PASSES.
- `R3_REAL_TIA_REGISTER_TIMING.csv`: actual Stella 6.7.1 TIA write trap captures at sample scanline 134, plus pixel deadlines derived from TIA timing.
- `R3_PIXEL_AUDIT.json`: exact original-map and door mask matches in real Stella GUI images.
- `R3_FRAMES_600.csv` / `R3_FRAMES_600_SUMMARY.json`: 600 original Stella Ctrl+F debugger frames (11–610) and pixel-evidenced 262 HUD.
- `source/rom/v018/experiments/r3_c02/`: actual 6502 source, DASM build, source C02 table generator, source-map hash and compiled F6 ROM. Also 600 raw image crops, complete full debugger images for critical states/negative controls, and original six-source historical comparison frames.
- `source/rom/v018/experiments/r3_c02/dist/`: `LetMeOut_v018_R3_C02_F6_NTSC.bin` 16384 byte standard F6 (4 identical 4096-byte banks), historical original 16384-byte v018 baseline, `r3_c02.lst`, `r3_c02.sym`, generated `r3_tables.inc`, `source_geometry.json`.
- `SHA256_MANIFEST.txt`: per-file exact SHA256 digest excluding itself, plus full archive SHA reported in `DELIVERY_POINTERS.md`.

## Reproduce

```bash
# Clone the actual repository and switch to the pinned R3 development commit
# (see delivery pointers for exact commit, not a floating branch).
git clone https://github.com/Odourman/let-me-out.git
cd let-me-out
git checkout <commit-listed-in-DELIVERY_POINTERS.md>
sudo apt-get update
sudo apt-get install -y dasm stella xvfb xdotool imagemagick
bash rom/v018/experiments/r3_c02/baseline_build.sh
bash rom/v018/experiments/r3_c02/build.sh
bash rom/v018/experiments/r3_c02/capture.sh
bash rom/v018/experiments/r3_c02/capture_600.sh
bash rom/v018/experiments/r3_c02/trace_tia.sh
# Run the local Python analyzers with Pillow against real Stella screenshot directories.
```

The map generator **asserts** original `design/PLANERADE_RUMSKARTOR_V011.json` C02 room geometry. No v0.19 candidate substituted. The baseline build uses the existing historical source for comparison, and the new R3 build is isolated under its own subtree.

**Visual evidence:** Full original raw Stella debugger screenshots are not edited. Cropped/increased-scale preview images in this package are explicitly labeled as such; authoritative pixel-matches use the original screenshots.

**Limitations:** A diagnostic port-overlap and a four-case logical passage check do not implement actual player collision, player/key progression, enemy AI or sound; full R1/R2/R4 remain blocked. TIA write-cycle captures cover a defined critical scanline and are not a complete cycle audit over all code paths. Developer test claims are not independent verifier verdicts.
