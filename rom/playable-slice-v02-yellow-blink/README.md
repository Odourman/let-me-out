# V02 yellow blinking key, test only

Frozen start `efe23bde3a1b6c6edbfc4fbf9f96c3f95dddd66a`. Build from this
directory with the pinned DASM in the project Cloud environment. The output
basename is shared by the modes, so copy each build to a distinct directory
before building the next variant.

```bash
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1
out=$(mktemp -d)
for mode in 0 8 6; do
    mkdir "$out/$mode"
    for edge in top bottom; do
        python build.py --edge "$edge" --blink "$mode"
        file="let-me-out-v02-brown-door-$edge.bin"
        cp "$file" "$edge-video.sym" "$edge-logic.sym" "$out/$mode/"
        rom="$out/$mode/$file"
        d="$out/$mode/$edge"
        python blink_probe.py "$rom" "$d-blink" "$mode" >"$d-blink.jsonl"
        python trace_color.py "$rom" "$edge" >"$d-color.jsonl"
        python phase.py "$rom" --stack-only >"$d-stack.jsonl"
        python phase.py "$rom" --transition wall-x60-held >"$d-phase.jsonl"
        python door_trial.py "$rom" "$d-door" "$edge" >"$d-door.jsonl"
        if [[ $mode == 0 ]]; then
            python door_trial.py "$rom" "$d-cold-on" "$edge" --cold >"$d-cold-on.jsonl"
        else
            for pickup in on off; do
                python door_trial.py "$rom" "$d-route-$pickup" "$edge" --cold --blink "$mode" --pickup "$pickup" >"$d-route-$pickup.jsonl"
            done
            python scenarios.py "$rom" "$d-soak" soak --pixel-stride 1 >"$d-soak.jsonl"
            python calibrate.py "$rom" "$d-missile" --door-missile >"$d-missile.jsonl"
        fi
    done
done
python bench_summary.py "$out"
```

Control GOLD and trial YELLOW use the same bitmap and coordinates, with
separate player, key-window and shot oracles. The matrix POKEs deliberately
freeze fixture coordinates. The cold routes use controller input only,
waiting without movement at X77 for the intended pickup phase, and the
same exit and score assertions as the original cold route. Gopher PNG
sequences retain consecutive native frames. The H.264 previews scale by
nearest-neighbor and replay two whole periods at 60 frames/s, repeatedly.
Stella screenshots are separate real-input smoke captures.

A rejected prototype did both gate and phase work inside the VBLANK planner.
The preserved log and source show its active-shot raster failure.

For exact comparisons across Gopher screenshot apertures, run
`aperture_audit.py LOG PNG_DIRECTORY MODE --apertures BOUNDS.json` on the raw
PTY log before feeding the resulting directory to `bench_summary.py`.
Keep original PNGs as captured. To run the full no-key RGB regression,
extract the frozen TOP/BOTTOM evidence archives from the start commit and
run `paired_soak.py ROM OUT FROZEN_EDGE_SOAK_DIRECTORY` for each blink build.
