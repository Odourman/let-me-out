# Let Me Out! V02 bruna PF-dörrar

Två separata enrumstest med brun dörr i över- respektive underväggen vid X64–95. Spela med vänster joystick. Stella använder piltangenter och mellanslag.

## Bygg och prova

Kör från katalogen med DASM/Gopher i G5AR ENV-01, Python och Pillow. Bygg botten sist så att de gemensamma genererade filerna motsvarar manifestet.

```bash
export PYTHONDONTWRITEBYTECODE=1
python build.py --edge top
python build.py --edge bottom
sha256sum -c SHA256SUMS
out=$(mktemp -d)
for edge in top bottom; do
    rom=let-me-out-v02-brown-door-$edge.bin
    mkdir -p "$out/$edge"
    python door_trial.py "$rom" "$out/$edge/door" "$edge" >"$out/$edge/door.jsonl"
    python door_trial.py "$rom" "$out/$edge/cold" "$edge" --cold >"$out/$edge/cold.jsonl"
    python scenarios.py "$rom" "$out/$edge/soak" soak --pixel-stride 1 >"$out/$edge/soak.jsonl"
    python crowd.py "$rom" "$out/$edge/crowd" >"$out/$edge/crowd.jsonl"
    python crowd.py "$rom" "$out/$edge/key-crowd" --key-cases >"$out/$edge/key-crowd.jsonl"
    python calibrate.py "$rom" "$out/$edge/missile" --door-missile >"$out/$edge/missile.jsonl"
    python trace_door.py "$edge" >"$out/$edge/trace.jsonl"
    python trace_door.py "$edge" --open >"$out/$edge/open-trace.jsonl"
    python phase.py "$rom" --transition wall-x71 >"$out/$edge/wall-x71.jsonl"
    python trial_audit.py "$out/$edge" "$edge"
done
bash stella_play.sh let-me-out-v02-brown-door-top.bin "$out/stella-top" 609 record
STELLA_BIN=/workspace/work/g5bb/stella7/usr/bin/stella \
    bash stella_play.sh let-me-out-v02-brown-door-bottom.bin "$out/stella-bottom" 610 record
```

[Mätrapport](TO_MAIN_V02_BROWN_PF_DOOR_BLACK_OUTLINE_TRIAL.md)
