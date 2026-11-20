# Let Me Out! V02 topp- och bottendörrprov

Två isolerade enrumskassetter i standard F6/NTSC, byggda från den spelbara V02-basen. I provet är dörren centrerad vid X64–95 och den övriga kartan behåller sina ursprungliga kollisionsceller. Piltangenter och mellanslag motsvarar joystick i Stella.

## Reproducera

Kör i denna katalog med G5AR ENV-01, Python och Pillow. Kör 600-bildruteproven seriellt om PTY-gränsen uppnås. Byggkommandona skriver om genererade standardfiler, så bygg botten sist för identisk arbetskopia.

```bash
export PYTHONDONTWRITEBYTECODE=1
python build.py --edge top
python build.py --edge bottom
sha256sum -c SHA256SUMS
out=$(mktemp -d)
for edge in top bottom; do
    rom=let-me-out-v02-door-$edge.bin
    mkdir -p "$out/$edge"
    python scenarios.py "$rom" "$out/$edge/soak" soak --pixel-stride 1 >"$out/$edge/soak.jsonl"
    python door_trial.py "$rom" "$out/$edge/door" "$edge" >"$out/$edge/door.jsonl"
    python door_trial.py "$rom" "$out/$edge/cold" "$edge" --cold >"$out/$edge/cold.jsonl"
    python crowd.py "$rom" "$out/$edge/crowd" >"$out/$edge/crowd.jsonl"
    python crowd.py "$rom" "$out/$edge/key-crowd" --key-cases >"$out/$edge/key-crowd.jsonl"
    python trace_door.py "$edge" >"$out/$edge/trace.jsonl"
    python trial_audit.py "$out/$edge" "$edge"
done
python trace_mid.py >"$out/mid-band.jsonl"
bash stella_play.sh let-me-out-v02-door-top.bin "$out/stella-top" 607 record
STELLA_BIN=/workspace/work/g5bb/stella7/usr/bin/stella \
    bash stella_play.sh let-me-out-v02-door-bottom.bin "$out/stella-bottom" 608 record
```

[Mätrapport](TO_MAIN_V02_TOP_BOTTOM_DOOR_TRIAL.md) · [Framtida NPC-former](FUTURE_NPC_FORMS.md)
