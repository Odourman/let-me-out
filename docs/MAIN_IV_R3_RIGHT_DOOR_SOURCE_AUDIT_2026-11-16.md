# Let Me Out! – MAIN IV R3 källgranskning: endast högerdörr, orange port och svart nyckelhål

**2026-11-16. Roll:** MAIN:s källbaserade förstudie och teknisk blockeraranalys för redan auktoriserad v0.18 NTSC/R3. **Inte en ny kodauktorisation, inte ett nytt designbeslut och inte verifierad Stella-R3.**

## Originalbeslut och karta

- Källa: `design/PLANERADE_RUMSKARTOR_V011.json` på `main`, vald `C02` som v0.11 planerad kartbas. Det är inte en v0.19-kartcutover.
- Lokal separat kontroll av exakt källavskriven 40×22 C02-matris: alla 22 vänsterceller är `#`; högra `x=39` är `D` för `y=9,10,11,12` och `#` på samtliga andra rader; `x=38` är `.` i fyra dörrrader. **Statisk kartgeometri PASS**, inte grafisk ROM- eller kollisionstest.
- Direkt beslut: vänsterväggen stängd; endast högerutgången kan låsas upp; vid upplåsning ska **orange port och svart nyckelhål försvinna tillsammans**; faktisk passage sker separat, E1 kvarstår. Se [v0.12 dörrförstudie](https://github.com/Odourman/let-me-out/blob/main/docs/DOOR_VISUAL_RIGHT_ONLY_STUDY_V012.md), [v0.13 visuell riktning](https://github.com/Odourman/let-me-out/blob/main/docs/KEY_AND_DOOR_VISUAL_TARGET_V013.md) och [v0.18 acceptanskriterier D01-D03](https://github.com/Odourman/let-me-out/blob/main/docs/ROM_GATE_V018_ACCEPTANCE.md).

## Vad faktiskt finns i äldre draft PR #7, utan att godkänna den

Faktiskt lästa, frysta ROM DEVELOPMENT-källor på `rom-dev/v018-ntsc-diagnostic`:

1. `rom/v018/tools/build.py` innehåller källmatrisen `C02` och lämnar `D` öppen som PF i bank 2, samtidigt som en separat 8-bitars `P1`-bitmap försöker ge en synlig, skiftande dörrport. Det är en diagnostisk konstruktion, inte slutlig dörrgrafik.
2. `rom/v018/src/bank2.asm`: raden `STA CTRLPF` med `LDA #0` (omkring källrader 168–171) väljer **ospeglat PF** i fullbildskärnan. `FullLoop` (omkring källrader 290–315) uppdaterar `LEFT0/1/2` och `RIGHT0/1/2` separat på samma scanline. Till skillnad från R1ax:s speglade `CTRLPF=$01` innehåller den äldre R3-kärnan alltså en **avsiktlig asymmetrisk PF-implementation**.
3. `DOORCOLOR` sätts i `bank2.asm` till brun `$64` före cirka frame 85, orange `$3C` cirka frame 85–169, därefter färg `0`; `COLUP1` ges detta värde på VBLANK. Detta är en färgsekvens i koden, **inte bevis för synlig korrekt orange port eller funktionell upplåsning**.
4. `DOOR`-masken genereras med sammanhängande orangefält och mörka utsparingar (`.##..##.` för fyra source-rader, `.###.##.` för fyra). **Black-keyhole silhouette not yet independently established** from true Stella output, and the minimum width of one PF cell is 4 color clocks.
5. Draft PR #7 är **open/draft, unmerged**, och Issue #8:s frysta oberoende baseline är från annan tidigare commit. Ingen av de senare R1aq/R1ba-grafikforsknings-ROM:erna får tillskrivas verifierad R3-funktion på grund av denna äldre kod.

## Riskgrind och test som fortfarande måste utföras

| R3-kriterium | Källa finns | Faktisk verifierad Stella/R3 |
|---|---|---|
| D01: vänster ytterkant stängd, höger dörr låst/öppen | C02 40×22 original + ospeglad PF-kod | **NOT PROVEN** |
| D02: höger öppnas helt vid upplåsning, vänster lämnas stängd | Idé via `D`-celler i PF och P1 färg 0 | **NOT PROVEN**; logisk exit-/positionsgrind måste visas separat |
| D03-a: orange synlig port när låst | P1 DOORCOLOR `$3C` testsekvens | **NOT PROVEN** med färgbild och tidslogg |
| D03-b: svart igenkännbart nyckelhål (separat) | Grafisk utsparing i P1 förstudie, inte godkänd mask | **NOT PROVEN**; markera FAIL/BLOCKED om otillräckligt |
| B02/E01: faktisk register-/CPU-timing, reproducibel skärmbild, bildruta och ROM-hash | Kodskelett finns | **NOT PROVEN** för ny sammanhållen R3-leverans |

**Direkt nästa redan auktoriserade ROM DEVELOPMENT-diagnostik:** Gör en **isolerad R3-portaudit i Stella** av den frysta C02-källan (ingen kartändring): dokumentera samma fysiska skärmområde före/efter `SCENE=2` och dörrens color-/statefaser. Kräver pixelbevis att vänsterväggen är stängd och endast högra `x39/y9–12` är öppningsbar, separat orange port och utskärning svart, exakt 262 scanlines, och ett signerat eget förtest. Om aktiva ROM-code changes krävs: separat research-only gren, tydlig scope, ingen PR #7-merge eller produktionstyst cutover. Därefter riktig, **separat VERIFICATION**.

## Hårdvarukontext (extern forskning, endast rådgivande)

- [Stella Programmer's Guide](https://www.atariage.com/2600/programming/2600_101/docs/stella.html): 20 PF-bitar per halvskärm, 76 CPU-cykler per scanline.
- [2600 Cookbook – Asymmetrical Playfield](https://alienbill.com/2600/cookbook/playfield.html): PF0/PF1/PF2 måste laddas om med rätt tidpunkt för högerhalvan; `CTRLPF=0` upprepar bitordningen, `CTRLPF=1` speglar.
- Asymmetrisk PF på grund av R3 upphäver inte NUSIZ-kopplingen i sexandroid-ROM:en. Det finns ännu inget bevis för en sammanhållen R1+R2+R3+R4-produktions-ROM.

**MAIN IV ställningstagande:** R3 fortfarande **BLOCKED/NOT PROVEN**. Det är fel både att förkasta den befintliga asymmetriska källlösningen som oprövad hypotes och att beskriva den som godkänd bara för att koden finns. Ingen designwaiver utan användarbeslut.
