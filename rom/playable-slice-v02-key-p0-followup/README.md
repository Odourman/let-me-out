# V02 key/P0 and PF integrated follow-up

Run from this directory in the let-me-out Codex environment. The wall bridge stays enabled while the key is carried because there is no floor-key sprite in that state. The floor-key and shot paths retain their original qualification. The ROM uses the existing late HMOVE phase and adds no RAM.

```bash
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1
out=$(mktemp -d)
for edge in top bottom; do
    mkdir "$out/$edge"
    d="$out/$edge"
    python build.py --edge "$edge"
    rom="let-me-out-v02-brown-door-$edge.bin"
    python scenarios.py "$rom" "$d/soak" soak --pixel-stride 1 >"$d/soak.jsonl"
    python door_trial.py "$rom" "$d/door" "$edge" >"$d/door.jsonl"
    python door_trial.py "$rom" "$d/cold" "$edge" --cold >"$d/cold.jsonl"
    python crowd.py "$rom" "$d/key-crowd" --key-cases >"$d/key-crowd.jsonl"
    python crowd.py "$rom" "$d/same-y" --same-y-only >"$d/same-y.jsonl"
    python calibrate.py "$rom" "$d/missile" --door-missile >"$d/missile.jsonl"
    python trial_audit.py "$d" "$edge"
done
python phase.py let-me-out-v02-brown-door-top.bin --transition wall-x60-held
python phase.py let-me-out-v02-brown-door-bottom.bin --stack-only
python trace_key.py let-me-out-v02-brown-door-top.bin 24 151
python trace_key.py let-me-out-v02-brown-door-top.bin 60 151
python trace_key.py let-me-out-v02-brown-door-top.bin 60 159
bash stella_play.sh let-me-out-v02-brown-door-top.bin "$out/top/stella" 623
STELLA_BIN=/workspace/work/g5bb/stella7/usr/bin/stella bash stella_play.sh let-me-out-v02-brown-door-bottom.bin "$out/bottom/stella" 624
sha256sum -c SHA256SUMS
```

For the rejected probes, start from a scratch copy of the frozen inner-render-conflict-repair directory under `rom/`. Overlay the single original-named `.inc` file from the negative evidence folder, then build TOP and run `crowd.py --key-cases` with the required ROM and output-directory arguments. The separate guarded-key-bridge source is a follow-up probe built with the carried-key PF gate also enabled.

The Gopher cold-joystick route starts at boot and issues controller input without RAM edits. The others use controlled diagnostic RAM positions. Stella captures are UI smoke runs.

## ITER6 domain control

Extract the historical diagnostic files into a scratch directory with
`git archive c70be450f5e270e795a4f908ac9ecc549c35573c experiments/g5be_iter6`.
From that diagnostic directory run the stored `evidence/iter6-domain-probe.py`
with an absolute path to a new output directory. This tests the frozen
diagnostic ROM and its dispatch domain separately from V02.

For the five M(1) overlap pixels, run `python mask_occlusion.py "$out/top"`
and repeat for BOTTOM.
