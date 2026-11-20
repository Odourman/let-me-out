# Multirow yellow-key diagnostic

Run from this directory in the pinned DASM/Gopher environment. Build and measure the indexed control:

    out=$(mktemp -d)
    python build_multirow.py "$out" --player 60 --first-cycle 30 --second-cycle 41 --shift-first 1 --sm-x 51 --shot-x 32 --p1-key --shot --indexed
    python measure_multirow.py "$out/probe.bin" >"$out/raw.jsonl"
    python check_band.py "$out/raw.jsonl" 60 51 32

Add --pf-dynamic to reproduce the negative raster result. The fixed P1 cases omit --indexed. For PX24 and PX104 use --first-cycle 32 --shift-first -1 --sm-x 59. Each evidence snapshot contains its generated assembler. Assemble multirow.asm in that snapshot with -f3, and concatenate the 4 KiB output four times. For historical snapshots use -DFIRST_X=24, 60 or 85 for the P0 cases as appropriate, or 24, 60 or 104 for the P1 cases. When the snapshot references SM_X or SHOT_X, use the fixture values in the report. Then run measure_multirow.py on the resulting probe.bin with its matching probe.sym.

Replay the failure with:

    for mode in 0 8; do
      rom="../playable-slice-v02-yellow-blink/roms/$mode/let-me-out-v02-brown-door-top.bin"
      python route_diff.py "$rom" evidence/route/original-input.jsonl
      python route_diff.py "$rom" evidence/route/original-input.jsonl --trace
    done

The replay forwards only the archived controller and frame-step commands. The trace stops in frame 386 before the first failing frame. The frozen 8/4 TOP and 6/6 BOTTOM cold checks are ordinary joystick tests from the preceding R2 driver. The short gameplay clips contain consecutive native Gopher images. Stella was used for an independent emulator view of the diagnostic band.
