# Let Me Out! v0.18 – SEX_X_FREE, full real Stella measurements

Developer-owned evidence ONLY. Not a final game; R1 graphics BLOCKED. Original project baseline and independent verification preserved.

- Full Swedish MAIN report: `report/TO_MAIN_SIX_INDEPENDENT_X_STELLA_2026-11-15.md`
- Test deltas T01–T16: `report/TEST_MATRIX_V018_SIX_X_DELTA.csv`
- Compiled 16 KiB F6 ROMs: `rom/six_x_free_a_F6_16KB.bin` and `rom/six_x_free_b_F6_16KB.bin`
- Source and local DASM build: `src/six_x_free_a.asm`, `src/six_x_free_b.asm`, `src/build.sh`
- Original ROM bank binaries, DASM listing and symbol files: `build/`
- External pixel analysis: `analysis/analyze_six_x_stella.py`
- Every-frame results with exact 600 rows each: `evidence/frames_600_a.csv`, `evidence/frames_600_b.csv` and `evidence/summary_a.json`, `evidence/summary_b.json`
- 1,200 **unedited Stella X11 PNG screenshots** in *original* GitHub Actions artifact nested as `evidence/ORIGINAL_GITHUB_ACTIONS_ARTIFACT_1200_FRAMES.zip` (do not confuse with schematic images)
- Original emulator screenshots for sample frame indices 1/300/600 are also extracted to `evidence/Stella_..._RAW.png`. `Stella_16_sample_frames_contact_sheet_CROPPED.png` is an explicitly labeled collage of crops of those unedited screenshots.

## Rebuild

Ubuntu 24.04 packages `dasm stella xvfb xdotool imagemagick`. Run `bash src/build.sh` from a temporary directory with the source files and `dist` directory. The shell build script assumes its original repository position next to the original `.asm` files; for the packaged layout, copy `src/*` into the same temp folder and run `bash build.sh`. The resulting ROM SHA-256 must equal SHA256SUMS entries below and in `build/DASM_SHA256SUMS.txt`.

## Reanalyse full images

Unzip `evidence/ORIGINAL_GITHUB_ACTIONS_ARTIFACT_1200_FRAMES.zip` into an empty directory. For each variant:

`python3 analysis/analyze_six_x_stella.py --raw rom/v018/experiments/six_x_free/evidence_walk_a/raw --asm src/six_x_free_a.asm --out output --variant a --count 600`

`python3 analysis/analyze_six_x_stella.py --raw rom/v018/experiments/six_x_free/evidence_walk_b/raw --asm src/six_x_free_b.asm --out output --variant b --count 600`

Requires Pillow. The analyzer reads actual recorded screenshot pixels and refuses to assert 262 for unexpected HUD pixel patterns; its calibration is limited to Stella 6.7.1's captured GUI layout. 600 images per variant are REQUIRED; no simulated data or inferred visibility is substituted. No full TIA register-write trace is present.

## Evidence integrity

`SHA256SUMS.txt` lists every delivery file except itself. Nested GitHub artifact SHA256 `ea3eabff506964ba49c92019ffb18bdf14b138c6e512267df72ddce33e95a4c7`. Both delivered F6 ROMs reproduced in actual GitHub Actions run 43759690033. CI success alone does not imply R1 PASS.
