# V02 Inner Render Conflict Repair

TOP and BOTTOM are playable F6/NTSC ROMs built from the brown-door checkpoint at `9acaeaf7aa65a3619c062b79f05780e9c5ca1867`. The late-HMOVE wall route now also covers the measured X60–62 band. It starts RESP1 four CPU cycles earlier with its own HMP1 values and rejoins the unchanged late-HMOVE timing. The earlier phase is admitted only when the first queue slot lies left of the ordinary phase's X63–78 band. This bounded check avoids an additional queue search during VBLANK. The change is confined to eligible, unlocked-state-zero, no-shot routing already selected by the wall scheduler. The wall, NPC and player oracles retain the same coordinates and RGB values.

## Reproduce

Run these commands from this directory in the let-me-out Codex environment with pinned DASM and Gopher2600, stock Stella, Xvfb, xdotool and Python with Pillow. The output directories for the Python captures must be new.

```bash
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1
out=$(mktemp -d)
for edge in top bottom; do
    python build.py --edge "$edge"
    rom="let-me-out-v02-brown-door-$edge.bin"
    mkdir "$out/$edge"
    python scenarios.py "$rom" "$out/$edge/soak" soak --pixel-stride 1 >"$out/$edge/soak.jsonl"
    python door_trial.py "$rom" "$out/$edge/door" "$edge" >"$out/$edge/door.jsonl"
    python door_trial.py "$rom" "$out/$edge/cold" "$edge" --cold >"$out/$edge/cold.jsonl"
    python crowd.py "$rom" "$out/$edge/crowd" >"$out/$edge/crowd.jsonl"
    python crowd.py "$rom" "$out/$edge/key-crowd" --key-cases >"$out/$edge/key-crowd.jsonl"
    python calibrate.py "$rom" "$out/$edge/missile" --door-missile >"$out/$edge/missile.jsonl"
    python calibrate.py "$rom" "$out/$edge/wall" --wall-domain >"$out/$edge/wall.jsonl"
    python trial_audit.py "$out/$edge" "$edge" >"$out/$edge/audit.json"
    base="../playable-slice-v02-core-object-followup/$rom"
    python calibrate.py "$base" "$out/$edge/base-wall" --wall-domain >"$out/$edge/base-wall.jsonl"
    python wall_delta.py "$out/$edge/base-wall" "$out/$edge/wall" "$edge" >"$out/$edge/wall-delta.jsonl"
done
python phase.py let-me-out-v02-brown-door-top.bin --transition wall-x60
python phase.py let-me-out-v02-brown-door-bottom.bin --stack-only
bash stella_play.sh let-me-out-v02-brown-door-top.bin "$out/top/stella" 621
STELLA_BIN=/workspace/work/g5bb/stella7/usr/bin/stella bash stella_play.sh let-me-out-v02-brown-door-bottom.bin "$out/bottom/stella" 622
sha256sum -c SHA256SUMS
```

Cold joystick input runs from boot with no RAM writes. The wall, missile, and crowd fixtures intentionally freeze logic and set RAM to known positions for pixel diagnosis. Stella runs are stock-UI cross-checks. The deterministic pixel and full cold-joystick assertions are Gopher2600 runs.

The isolated negative probes use source patches against the frozen core-object-followup directory. Make a scratch copy of that directory under `rom/`, apply the selected `source.patch` using `patch -p1`, then copy the sibling `.inc` into the scratch directory. Build with `python build.py --edge top`. Use the patched `crowd.py` with `--key-cases` for the BALL+M0 probe and without that flag for the M1 probe. Both report a single selected case.
