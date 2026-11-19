# Let Me Out! – Playable Slice V02, fortsatt rasterreparation

Spelbar 16 KiB F6/NTSC-ROM för det enda rummet A_OPEN_01. Ladda `let-me-out-v02-raster-continuation.bin` i stock Stella eller Gopher2600 med NTSC och F6. Joystick i vänster port, eller piltangenter och mellanslag i Stella.

[Läs utvecklarresultat och kvarvarande grafikfel](TO_MAIN_V02_RASTER_REPAIR_CONTINUATION.md) · [Issue #31](https://github.com/Odourman/let-me-out/issues/31)

## Bygg och återkör

Kör från katalogen med G5AR-prefixet `/workspace/.g5ar-env01/bin`, Python och Pillow. DASM:s blad och symbolfiler genereras tillsammans med ROM:en.

```bash
export PYTHONDONTWRITEBYTECODE=1
python build.py
sha256sum -c SHA256SUMS
out=$(mktemp -d)
rom=let-me-out-v02-raster-continuation.bin
python replay.py "$rom" "$out/basic" >"$out/basic.jsonl"
for case in patrol controls npc-obstacles wall touch priority key-door door-locked door-held-open; do
    python scenarios.py "$rom" "$out/$case" "$case" >"$out/$case.jsonl"
done
python scenarios.py "$rom" "$out/soak" soak --pixel-stride 1 >"$out/soak.jsonl"
python scenarios.py "$rom" "$out/unseeded" unseeded --key-lifetime >"$out/unseeded.jsonl"
python phase.py "$rom" >"$out/stage.jsonl"
python phase.py "$rom" --max-x >"$out/max-x.jsonl"
for mode in assist bridge key-assist cap cap-player wall-bridge; do
    python phase.py "$rom" --transition "$mode" >"$out/$mode.jsonl"
done
python phase.py "$rom" --raster >"$out/raster.jsonl"
python calibrate.py "$rom" "$out/calibration" >"$out/calibration.jsonl"
python calibrate.py "$rom" "$out/missile" --door-missile >"$out/missile.jsonl"
python crowd.py "$rom" "$out/crowd" >"$out/crowd.jsonl"
python crowd.py "$rom" "$out/key-crowd" --key-cases >"$out/key-crowd.jsonl"
python calibrate.py "$rom" "$out/wall-domain" --wall-domain >"$out/wall-domain.jsonl"
python audit.py "$out"
bash stella_play.sh "$rom" "$out/stella671" 597 record
STELLA_BIN=/workspace/work/g5bb/stella7/usr/bin/stella \
    bash stella_play.sh "$rom" "$out/stella70" 598
```

Jämför alla 600 bilder med den frysta start-ROM:en i Gopher2600:

```bash
ref=$(mktemp -d)
python scenarios.py ../playable-slice-v02-raster-repair-next/let-me-out-v02-raster-repair-bridge.bin \
    "$ref/soak" soak --pixel-stride 1 >"$ref/soak.jsonl"
python audit.py "$out" --compare-rgb "$ref"
python audit.py "$out" --compare-player "$ref"
```

`evidence/brief` innehåller protokoll per bildruta och `evidence/raw.tar.gz` innehåller de 600 originalbilderna och Gophers PTY-svar.
