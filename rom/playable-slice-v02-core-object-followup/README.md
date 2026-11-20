# Let Me Out! V02 objektkonflikter och skott

Två separata spelbara F6/NTSC-test från de frysta bruna dörrvarianterna. Piltangenter och mellanslag motsvarar vänster joystick i Stella.

## Bygg och prova

Kör från denna katalog med G5AR ENV-01, Python och Pillow. Bygg botten sist för samma genererade filer som i manifestet.

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
    python trace_shot.py "$edge" >"$out/$edge/shot-trace.jsonl"
    python phase.py "$rom" --transition wall-x71 >"$out/$edge/wall-x71.jsonl"
    python trial_audit.py "$out/$edge" "$edge"
done
bash stella_play.sh let-me-out-v02-brown-door-top.bin "$out/stella-top" 611 record
STELLA_BIN=/workspace/work/g5bb/stella7/usr/bin/stella \
    bash stella_play.sh let-me-out-v02-brown-door-bottom.bin "$out/stella-bottom" 612 record
```

De isolerade prototypernas tar-arkiv byggs i egna kataloger under `rom/` med `python build.py --edge top`. Kör `crowd.py` med `--key-cases` för BOLL-provet och utan flaggan för P1-omstarten.

[Rapport](TO_MAIN_V02_CORE_OBJECT_CONFLICT_FOLLOWUP.md)
