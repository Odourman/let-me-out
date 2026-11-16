# MAIN II R1e – empirisk RESP0/P0 coarse-X-kalibrering

**Datum:** 2026-11-16. **Roll:** endast forsknings-/diagnostikbevis, inte ny full-R1 PASS eller oberoende VERIFICATION.

## Reproducerbar körning

- [GitHub Actions run #43811638502 – SUCCESS](https://github.com/Odourman/let-me-out/actions/runs/43811638502).
- Gren `research/main-ii-r1e-p0-position-calibration-20261116`, testad commit `86be1adad703af1a37463f4313b01e135a9ae169`.
- DASM 2.20.14.1, Stella 6.7.1, åtta separata standard-F6 16KB diagnostik-ROM:er och **åtta verkliga råa Stella GUI-skärmbilder** med samma tre original-P1-androidmasker.
- Underlag i Actions-artifact `main-ii-r1e-p0-position-calibration-evidence`, `rom/v018/experiments/main_ii_p0_position/calibration.json` och varje `delay_XX/evidence/stella_full.png`.
- Pixelmätning i **rå debugger-GUI X**, inte Atari TIA x. Ingen visuell rekonstruktion.

| P0Delay-loopen (#) | Faktisk observerad gul P0-position X GUI | Stella HUD rasterlinjer | Exakt P0 originalmask i förväntat y162–170 |
|---:|---:|---:|---|
| 4 | 186 | **261** | Förskjuten till y161–169; 44 mismatch mot y162–170 |
| 6 | 246 | **261** | Förskjuten till y161–169; 44 mismatch |
| 8 | 306 | **261** | Förskjuten till y161–169; 44 mismatch |
| 10 | 366 | **261** | Förskjuten till y161–169; 44 mismatch |
| 12 | 108 | 262 | 72/72 exakt |
| 13 | 110 | 262 | 72/72 exakt |
| 14 | 110 | 262 | 72/72 exakt |
| 15 | 110 | 262 | 72/72 exakt |

I de korta d4/d6/d8/d10-proverna är den högra P0-positionen verklig. Bilderna visar att programmet avviker med en rasterrad, vilket gör att den tidiga kodens pixel-audit på fasta y-koordinater inte kan klassas som PASS. Det är **inte** att P0-bitmapens ursprungliga databytes ändrats. `P0Delay` kan passera en rastergräns och effekten är då icke-monoton.

## Rekommenderat nästa snäva test

För P0 fjärde originalmask-kandidaten: använd `P0Delay=4` och lägg till en enda tom `WSYNC` under VBLANK, så att 262 NTSC-linjer och normal y-band återställs. Vänstra gula P0-kopian hamnar då kring rå GUI-X186 och den automatiska `NUSIZ0=$04`-wide-kopian kring X314, lämpligt separerade från tre P1-masker. Detta är **ett kalibrerat testval**, inte en bekräftad fjärde figur eller full-R1-lösning. Provet måste mäta både P0 originalmask, P0 egen fjärde originalmask samt exakt ett M0-skott och 262 linjer. För fyra originalmasker gäller 72/72 bitpositioner var och **inga extrakopior**.

## Oförändrade grindar

`main`, utvecklings-PR #7, fryst oberoende Verification och godkända sex-NPC-krav har inte ändrats. Endast rådgivande standard-F6-forskning.
