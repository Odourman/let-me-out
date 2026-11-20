# V02 R2 P1/PF och separat overscanreparation

## Återskapa från repositoryts rot

DASM 2.20.14.1, Gopher2600 v0.57.2 och stock Stella 6.7.1 från
`/workspace/.g5ar-env01/bin`. Python och Pillow används för pixeloraklet.

```bash
A=rom/playable-slice-v02-p1-pf-integration
B=rom/playable-slice-v02-overscan-fix
python "$A/reproduce.py" /tmp/v02-p1-pf
python "$B/build.py" --edge top --blink 8
python "$B/build.py" --edge bottom --blink 6
python "$B/route_diff.py" "$B/roms/8/let-me-out-v02-brown-door-top.bin" \
  rom/playable-slice-v02-multirow-key/evidence/route/original-input.jsonl
python "$B/door_trial.py" "$B/roms/8/let-me-out-v02-brown-door-top.bin" /tmp/v02-top-cold top \
  --cold --blink 8 --pickup off
python "$B/calibrate.py" "$B/roms/8/let-me-out-v02-brown-door-top.bin" /tmp/v02-top-shot --door-missile
python "$B/phase.py" "$B/roms/8/let-me-out-v02-brown-door-top.bin" --transition wall-x60-held
python "$B/phase.py" "$B/roms/8/let-me-out-v02-brown-door-top.bin" --stack-only
bash "$B/stella_play.sh" "$A/evidence/wall120trace/probe.bin" /tmp/v02-pf-stella 194
```

Bygg om för båda kanterna med `--blink 0`, `--blink 8` och `--blink 6`.
Använd en egen oanvänd målkatalog för varje emulatorprov. Extrahera de tre
`run-*.tar.gz` till samma tomma katalog för att återskapa
`python "$B/summarize.py" <katalog>`. `paired_soak.py ROM UT REFERENSBILDER`
jämför en ny körning mot en tidigare 600-bildskörning på motsvarande kant.
`plan.json` innehåller generatorns parametrar. De genererade ASM-filerna,
DASM-listningarna, ROM, symboler, Gopher-bilder och råloggar ligger tillsammans.
Timer-ROM:arna och deras symboler ligger i `roms/` under timerkatalogen.
