# Let Me Out! — isolated R1 research/developer evidence package, 2026-11-16

## Authority

Scope **R1 original six individually positionable X/Y ANDROIDS in v0.18 NTSC**. Full gate not passed; USER CANON NOT CHANGED. No R2, R4, R1+R3 integration, no independent VERIFICATION, no merge.

## Directory layout

- `TO_MAIN_R1.md`: authoritative developer handoff: positives, fail cases, true measured TIA CPU cycles, scope and decisions.
- `TEST_MATRIX_R1_DELTA.csv`: scoped developer test results (INCONCLUSIVE, FAIL, NOT_RUN or DEVELOPER_LOCAL_PASS).
- `source/`: real 6502/assembler, original reference JSON, Python DASM generators and Stella capture + image-analysis scripts.
- `ROM/`: all compiled 16 KB standard F6 ROMs, some 4 KiB bank files, DASM listings/symbol tables, source build metadata.
- `evidence/`: all 600 consecutive Stella two-X screenshots, 48 original two-XY screenshots, 16 per 3–6 NPC and 16 per six-variant, six genuine Stella register-write trap GUI images, raw analysis summaries/CSV.
- `LetMeOut_R1_Stella_Positive_vs_Six_FAIL.png`: convenience contact sheet from **cropped real Stella GUI images**. Not original unedited evidence; the source PNGs are unchanged.
- `SHA256_MANIFEST.txt`: SHA-256 for **all** files except manifest itself. Every hash checked locally; main ZIP CRC checked.

## Quick build

Checkout GitHub `rom-dev/v018-r1-independent-xy-20261116` at the frozen source commit in the handoff; install `dasm`, `stella`, `python3-pil`, `xvfb`, `xdotool`, `imagemagick` on Ubuntu 24.04.

```bash
cd rom/v018/experiments/r1_free_xy
python3 build_two.py
python3 build_two_xy.py
python3 build_scaling.py
python3 build_six_sweep.py
```

Each emits built ROM plus SHA metadata. Actual Stella requires the respective `capture_*` script and real screenshots; Python mask comparisons are analyses of genuine screenshots, **not a substitute for the emulator**. `analyze_six_sweep.py` has a documented final print-format defect; its JSON/CSV pixel results are valid, and the test should be marked FAIL, never PASS on generic CI success.

**All raw sprites remain source-exact.** No original commercial Atari ROMs or unauthorized disassembly distributed.
