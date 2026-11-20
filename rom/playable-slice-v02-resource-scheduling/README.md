# V02 key/P0 resource-scheduling probes

The playable checkpoint remains `efe23bde3a1b6c6edbfc4fbf9f96c3f95dddd66a`,
`rom/playable-slice-v02-key-p0-followup/`. The binary files under `evidence/`
are developer probes and failed candidates.

For each probe, copy the frozen directory to a new scratch directory under
`rom/`. From that copy, apply the matching `evidence/<probe>/source.patch`
with `patch -p1`, then run `python build.py --edge top` (also `--edge bottom`
for postsync). Use fresh output folders in these commands from the scratch copy.

```bash
rom=let-me-out-v02-brown-door-top.bin
out=$(mktemp -d)
python crowd.py "$rom" "$out/key" --key-cases
python door_trial.py "$rom" "$out/door" top
python phase.py "$rom" --max-x
python calibrate.py "$rom" "$out/wall" --wall-domain
python scenarios.py "$rom" "$out/soak" soak --pixel-stride 1
```

Run the key fixture for VDEL, the wall and max-X fixtures for nofine, the key,
door, wall and soak fixtures for postsync, and only the soak for each isolation
ROM. The isolation patches stop after 101 frames. For the VDEL beam trace,
copy `trace_bridge_writes.py` into the scratch copy and run it with the built
TOP ROM as its sole argument. Non-probe cold runs use the frozen build,
`door_trial.py ROM OUT top --cold` or `bottom --cold`; this route never pokes RAM.
The short excerpts and native captures live in `evidence/`.
