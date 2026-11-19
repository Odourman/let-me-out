# Let Me Out! – Playable Slice V02, fortsättning

Spelbar 16 KiB F6/NTSC-ROM för det enda rummet A_OPEN_01. Ladda `let-me-out-v02-continuation.bin` i stock Stella eller Gopher2600 med NTSC och F6. Joystick i vänster port, eller piltangenter och mellanslag i Stella.

[Läs utvecklarresultat och kvarvarande grafikfel](TO_MAIN_PLAYABLE_SLICE_V02_CONTINUATION.md) · [Issue #31](https://github.com/Odourman/let-me-out/issues/31)

## Bygg och återkör

Kör från katalogen med G5AR-prefixet `/workspace/.g5ar-env01/bin`, Python och Pillow. DASM:s blad och symbolfiler genereras tillsammans med ROM:en.

```bash
export PYTHONDONTWRITEBYTECODE=1
python build.py
sha256sum -c SHA256SUMS
out=$(mktemp -d)
rom=let-me-out-v02-continuation.bin
python replay.py "$rom" "$out/basic" >"$out/basic.jsonl"
for case in patrol controls npc-obstacles wall touch priority key-door door-locked door-held-open; do
    python scenarios.py "$rom" "$out/$case" "$case" >"$out/$case.jsonl"
done
python scenarios.py "$rom" "$out/soak" soak --pixel-stride 1 >"$out/soak.jsonl"
python scenarios.py "$rom" "$out/unseeded" unseeded --key-lifetime >"$out/unseeded.jsonl"
python phase.py "$rom" >"$out/stage.jsonl"
python phase.py "$rom" --max-x >"$out/max-x.jsonl"
for mode in assist bridge; do
    python phase.py "$rom" --transition "$mode" >"$out/$mode.jsonl"
done
python phase.py "$rom" --raster >"$out/raster.jsonl"
python calibrate.py "$rom" "$out/calibration" >"$out/calibration.jsonl"
python calibrate.py "$rom" "$out/missile" --door-missile >"$out/missile.jsonl"
python crowd.py "$rom" "$out/crowd" >"$out/crowd.jsonl"
python audit.py "$out"
bash stella_play.sh "$rom" "$out/stella671" 587 record
STELLA_BIN=/workspace/work/g5bb/stella7/usr/bin/stella \
    bash stella_play.sh "$rom" "$out/stella70" 588
```

För direkt pixeljämförelse kör även `scenarios.py ../playable-slice-v02/let-me-out-v02.bin "$out/v02" soak --pixel-stride 1`. `evidence/brief` har läsbara utdrag. Råarkivet innehåller ursprungsbilderna och Gophers PTY-svar.
