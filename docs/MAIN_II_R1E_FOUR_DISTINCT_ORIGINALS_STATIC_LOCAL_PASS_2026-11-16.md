# MAIN II – R1e: fyra olika original-8×9-masker på samma Y via P1 tre + P0 wide-copy

**Datum:** 2026-11-16. **Bevisklass:** körbar originalskriven 6502/DASM NTSC standard-F6 i GitHub Actions + faktisk Stella 6.7.1 X11-pixelkontroll. **Lokalt statiskt PASS, ej R1 full PASS och ej oberoende VERIFICATION.**

## Reproducerbart försök

- **GitHub Actions SUCCESS:** https://github.com/Odourman/let-me-out/actions/runs/43811912249
- Testad commit `46811f6badec42fe20497aea9a5399f8184b10db`, gren `research/main-ii-r1e-four-originals-p0wide-calibrated-20261116`.
- Exakt byggd NTSC **16 384-byte** F6 (fyra identiska 4K källbanker), ROM SHA256 `84083e1c01de7ab0347ac18e85bdf36f37a6a7a201dd060f1f5248020459e24a`.
- Evidence-artifact ID `14201175454`, `main-ii-r1e-four-originals-calibrated-evidence`: körbar ROM, DASM .asm/.sym/.lst, faktisk Stella-frame X11 PNG, fem `runToPc`-skärmbilder och `evidence/audit.json`.
- Alla fyra oförändrade maskdata från `main/design/NPC_REFERENCE_8x9_masks.json` i källan: stor man, stor kvinna, liten man, liten kvinna; källjämförelse och pixlarna har samma maskvärden. Ingen förenklad teckenersättning.

## Resultat för en verklig statisk Stella-bild

| Objekt | TIA-objekt/teknik | Rå GUI-X | Exakt originalmatch |
|---|---|---:|---|
| Stor man, vit | P1 retrigger #1 | 154 | 72/72 |
| Stor kvinna, vit | P1 retrigger #2 | 268 | 72/72 |
| Liten kvinna, vit | **P0 NUSIZ0=$04 fjärrkopia**, ny GRP0-rad och `COLUP0` vit | **316** | **72/72** |
| Liten man, vit | P1 retrigger #3 | 400 | 72/72 |
| P0 gul spelare | P0 första kopian, dess tidigare `GRP0`-rad | 188 | 72/72 |
| Testskott M0 | enda gula missile vid GUI-X240–241, y160 | 240 | 2 GUI-pixlar, **ingen extra kopia** |

- **262 NTSC rasterlinjer**, kontrollerat via Stellas HUD.
- **0 extra vita och 0 extra gula pixlar** i figurernas validerade 9-raders rasterband.
- `audit.py` status **`LOCAL_PASS_STATIC_FOUR_DISTINCT_ORIGINALS`**, alla sex separata checks är True.
- `P0Delay=4` kalibrerat från verkliga `P0Delay` 4–15-svepet i [Actions #43811638502](https://github.com/Odourman/let-me-out/actions/runs/43811638502). En extra blank VBLANK-rad återställde 262 och normal y=162–170. P0:s wide-kopia börjar 64 TIA-color-clocks efter den första (128 GUI-pixlar).
- `GRP0` laddas om med lilla kvinnans exakta 8×9-rad först **efter** att gula spelarens kopia ritats. `COLUP0` skrivs vit innan fjärrkopian ritas. P1:s tre originalmasker är samtidigt pixelkorrekta, genom `RESP1`-strober med cirka 57–66 color clocks mellan utlösningarna i detta schema.
- För M0-kontrollen sätts `NUSIZ0=0` under en **separat föregående rasterrad** och återställs till 4 för NPC-raderna, så den automatiska wide-kopian inte dubblerar projektilen.

## Absolut viktig begränsning

**Detta är inte ett spelbevis för sex fria androider.** Endast fyra statiska X-positioner i en scen har testats. Originalspelaren är en temporär grafikkandidat, M0-renderingen är avsiktligt förlagd en rad ovanför NPC-banden, och inga PF-väggar/dörrar, R2-nyckel/O1, kollisions-AI, independent X eller 600 konsekutiva frames ingår i just den här action-körningen. Inte heller någon verklig Atari 2600-hårdvarukörning. **Inget godkännande kan ärvas till andra scenlägen/andra maskgrupper.**

Main-branch, ROM DEVELOPMENT draft PR #7 och Verification Issue #8 oförändrade. Research-grenen är separat. Nästa lokala grind: 600 sammanhängande verkliga Stella-debuggerbilder av oförändrad exakt binär med fyra originalmasker och ett M0.
