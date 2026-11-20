# V02 R2 reachability and yellow-key rescue

The playable control is `efe23bde3a1b6c6edbfc4fbf9f96c3f95dddd66a`.
The six 16 KiB control/8/4/6/6 reference builds are independently reproduced
here from the test sources at `058e3e67a40e3e0b72985a814f19520ea39a910f`.
The only new ROMs are isolated same-line P0 diagnostics.

From this directory in the pinned DASM/Gopher2600 environment:

```bash
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1
out=$(mktemp -d)
for mode in 0 8 6; do
    for edge in top bottom; do
        python build.py --edge "$edge" --blink "$mode"
        file="let-me-out-v02-brown-door-$edge.bin"
        cmp "$file" "../playable-slice-v02-yellow-blink/roms/$mode/$file"
        python r2_matrix.py "$file" "$out/$mode-$edge" "$mode" >"$out/$mode-$edge.jsonl"
    done
done
python door_trial.py ../playable-slice-v02-yellow-blink/roms/8/let-me-out-v02-brown-door-top.bin "$out/top-real" top --cold --blink 8 --pickup off
python door_trial.py ../playable-slice-v02-yellow-blink/roms/6/let-me-out-v02-brown-door-bottom.bin "$out/bottom-real" bottom --cold --blink 6 --pickup off
python door_trial.py ../playable-slice-v02-yellow-blink/roms/8/let-me-out-v02-brown-door-top.bin "$out/top-lure" top --cold --blink 8 --pickup off --visit 24 --lure
python door_trial.py ../playable-slice-v02-yellow-blink/roms/6/let-me-out-v02-brown-door-bottom.bin "$out/bottom-lure" bottom --cold --blink 6 --pickup off --visit 60 --lure
```

The TOP lure is expected to report a failure on the later exit route. Its
entire 24-frame field visit completes before that failure. Neither real
route uses RAM POKE. For seeded geometry, `RoomDone` freezes the world
while leaving the renderer live. Seeded carrier identities other than SF
test the rendering contract, independent of carrier selection in the game.
Repeat without `--lure` for the other recorded routes.

Build the one-scanline diagnostic with `python build_p0_line.py OUT`
and measure each generated ROM with `python measure_p0_line.py ROM PNG`.
The three historical variants take `--variant resp-first`,
`--variant grp-first`, or `--variant timed-copy-unshifted`. The injected
probe has a hardcoded yellow glyph and a white SM row. It does not
implement an entire player/key frame or an M0 integration. The ordinary
V02 beam path can be traced with `python trace_r2.py TOP_ROM 24` and repeated
for 60 or 104. Use the 8/4 TOP reference with its sibling symbol file.
