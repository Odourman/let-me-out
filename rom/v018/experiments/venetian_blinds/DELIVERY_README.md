# Let Me Out! v0.18 – Venetian Blinds experiment – reproducible delivery

This is a self-contained **scoped Atari 2600 technical experiment**, not a full game or an R1 PASS. No third-party commercial code/ROM is included.

All assembler source, build tooling, three F6 NTSC .bin, DASM .lst/.sym, unmodified Stella screenshots and debugger instrumentation logs, analysis code/CSV, exact static cycle budget and MAIN report are provided here. SHA256 manifest verifies included files (except manifest itself). Historical frozen independent VERIFICATION baseline not altered.

## Build

From this directory on Ubuntu 24.04, `sudo apt-get update && sudo apt-get install -y dasm stella xvfb xdotool imagemagick`, then `bash build.sh`, then `(cd dist && sha256sum -c SHA256SUMS.txt)`. Stella GUI screenshots: `bash ci_capture.sh` (Xvfb available). `python3 analyze_venetian_pixels.py .` requires Pillow+numpy; it reads only source Stella screenshots and compares the actual HUD ROI for 262, not guessed via OCR.

For review see `TO_MAIN_VENETIAN_BLINDS_2026-11-15.md`, `TEST_MATRIX_V018_VENETIAN_DELTA.csv`, `VENETIAN_MEASUREMENTS.json`, `CYCLE_PLAN.csv`. Every `evidence/.../stella_full.png` is a full unedited emulator GUI screenshot. `STELLA_CONTACT_SHEET_CROPPED.png` is only an enlarged excerpt. The six screenshots are two phases (13 and 18) for three ROM variants, not 600 continuous frames. The older 600+600 six-X results belong to a different failed experiment.

Caution: GitHub `ci_pc_cycle_probe.sh`, `ci_trace_probe.sh`, `ci_tia_traps.sh` are **unsuccessful instrumentation attempts**: their execution alone does not constitute a verified TIA register-write trace.
