# Let Me Out! – Playable Slice V02

Spelbar F6/NTSC-prototyp för det enda rummet A_OPEN_01. Kör `let-me-out-v02.bin` i Gopher2600 eller stock Stella med NTSC och F6. Joystick i vänster port, åtta riktningar och eld. Gå åt höger i utgångszonen efter nyckelupptagning.

[Specialistrapport och kända grafikfel](TO_MAIN_PLAYABLE_SLICE_V02.md) · [Issue #31](https://github.com/Odourman/let-me-out/issues/31)

## Bygg och återkör

Kör från denna katalog med G5AR-verktygen i `/workspace/.g5ar-env01/bin` och Python med Pillow. `build.py` använder de frysta kart- och maskfilerna i repots `design/`. DASM:s bygglistor och symboltabeller behövs för debuggerproven.

```bash
export PYTHONDONTWRITEBYTECODE=1
python build.py
sha256sum -c SHA256SUMS
rom=let-me-out-v02.bin
out=$(mktemp -d)
python replay.py "$rom" "$out/basic" >"$out/basic.jsonl"
for case in patrol controls npc-obstacles wall touch priority key-door door-locked door-held-open; do
    python scenarios.py "$rom" "$out/$case" "$case" >"$out/$case.jsonl"
done
python scenarios.py "$rom" "$out/soak" soak --pixel-probe >"$out/soak.jsonl"
python scenarios.py "$rom" "$out/unseeded" unseeded --key-lifetime >"$out/unseeded.jsonl"
python phase.py "$rom" >"$out/phase.jsonl"
python phase.py "$rom" --max-x >"$out/max-x.jsonl"
python phase.py "$rom" --raster >"$out/raster.jsonl"
python calibrate.py "$rom" "$out/calibration" >"$out/calibration.jsonl"
python calibrate.py "$rom" "$out/missile" --door-missile >"$out/missile.jsonl"
python audit.py "$out"
bash stella_play.sh "$rom" "$out/stella671" 585 record
STELLA_BIN=/workspace/work/g5bb/stella7/usr/bin/stella \
    bash stella_play.sh "$rom" "$out/stella70" 586
```

Loggarna för Gopher innehåller oförändrade PTY-transaktioner. `evidence/brief/` har läsbara utdrag, `evidence/images/` har originalbilder och `evidence/raw.tar.gz` har PTY-transaktionerna och de kompletta bildserierna.
