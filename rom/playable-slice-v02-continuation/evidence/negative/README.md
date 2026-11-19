# Kasserade ROM-försök

- `a-soak.err` registrerar 263-raders regression vid den första P0-banddelningen.
- `pre-alignment-soak.jsonl` tillhör P0-provet före sidgränskorrigeringen i Position. Köplatsen registrerades trots fysisk förskjutning.
- `e-key-door.err`, `h-key-door.err` och `j-key-door.err` är alternativa PF-vägar som gav 263 eller 264 scanlines.
- `late-clear-missile.jsonl` visar att fyra X-prov fortfarande gav en extra skottrad med senare ENAM0-nollställning.
- `m1-hole.bin` med Gopher-spår i `capture.jsonl` är den kasserade M1-stencilen. För att bygga den igen, lägg `m1-hole-game.asm` som `game.asm`, `m1-hole-build.py` som `build.py` och `hole.inc` i en kopia av fortsättningskatalogen under `rom/`. `probe.py` användes från den katalogen med projektet på Python-sökvägen. Det provet använder frysta koordinater. Dess 268 scanlines försköt den synliga rådatan och den godkända dörrbilden uppnåddes aldrig.
