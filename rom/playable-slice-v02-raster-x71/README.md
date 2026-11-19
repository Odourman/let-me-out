# Let Me Out! V02 X71

Spelbar standard-F6/NTSC-ROM för A_OPEN_01. Piltangenter och mellanslag motsvarar vänster joystick i Stella. [Mätrapport](TO_MAIN_V02_RASTER_X71.md)

## Bygg och upprepa proven

Kör med G5AR ENV-01, Python och Pillow från denna katalog.

```bash
export PYTHONDONTWRITEBYTECODE=1
python build.py
sha256sum -c SHA256SUMS
out=$(mktemp -d)
rom=let-me-out-v02-raster-x71.bin
python scenarios.py "$rom" "$out/soak" soak --pixel-stride 1 >"$out/soak.jsonl"
python scenarios.py "$rom" "$out/unseeded" unseeded --key-lifetime >"$out/unseeded.jsonl"
for case in door-locked door-held-open key-door; do
    python scenarios.py "$rom" "$out/$case" "$case" >"$out/$case.jsonl"
done
python calibrate.py "$rom" "$out/wall-domain" --wall-domain >"$out/wall-domain.jsonl"
python calibrate.py "$rom" "$out/calibration" >"$out/calibration.jsonl"
python calibrate.py "$rom" "$out/missile" --door-missile >"$out/missile.jsonl"
python crowd.py "$rom" "$out/crowd" >"$out/crowd.jsonl"
python crowd.py "$rom" "$out/key-crowd" --key-cases >"$out/key-crowd.jsonl"
python phase.py "$rom" >"$out/stage.jsonl"
python phase.py "$rom" --transition wall-bridge >"$out/wall-bridge.jsonl"
python phase.py "$rom" --transition wall-x71 >"$out/wall-x71.jsonl"
python audit.py "$out"
python raster_budget.py
bash stella_play.sh "$rom" "$out/stella" 599 record
```

Provkällor i `evidence/negative` kan packas upp i varsin separat katalog direkt under `rom` och byggas med samma kommando. Kör sedan respektive `crowd.py` med `--key-cases` för P0-nyckeln, utan flaggan för P0-dörren. För öppna vägglägen kör `scenarios.py` med `door-held-open`.
