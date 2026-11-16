# MAIN II – akut teknisk överlämning: fjärde NPC:s X frikopplad från spelaren, 600/600 i FYRA lägen

**Datum 2026-11-16. Typ: RESEARCH. Ingen full R1 PASS, ingen oberoende VERIFICATION och inget produktionsgodkännande.**

## Varför MAIN bör känna till detta före fortsatt sex-NPC-planering

Den förra bästa standard-F6/NTSC-proven R1e fick fyra olika originalmasker korrekta samtidigt, men den fjärde masken kom från P0:s automatiska wide-kopia med **fast +64 TIA CC avstånd till gul spelare**.

**Den spärren är nu bruten i en ny cykelexakt rasterarkitektur.** `NUSIZ0=$02` plus två olika `STA RESP0` per renderad NPC-rad gör att gul spelare och vit liten kvinnlig original-NPC kan ha skilda positioneringshändelser. Fyra lika långa ordningar på P0:s färg-/bitmap-/reset-skrivningar ger fyra frikopplade X-lägen, utan per-rad kostnad utöver samma TIA-instansschema.

- Positivt **två separata statiska R1f-ROM**: [Actions #43815070386](https://github.com/Odourman/let-me-out/actions/runs/43815070386), X330/348 medan P0 X216, originalmasker exakta.
- Positivt **EN R1f tvåläges-ROM med 600/600 dynamiska frames**: [Actions #43815510141](https://github.com/Odourman/let-me-out/actions/runs/43815510141), SHA `795dd4d0b8e6255facdb528a1fd4008b38047a5e84c4883d34e2f82f73c5bbb3`.
- Positivt **FYRA statiska R1g-ROM med fyra X**: [Actions #43816935556](https://github.com/Odourman/let-me-out/actions/runs/43816935556).
- **NY BÄSTA REPRODUCERBARA ROM:** [Actions #43817440347 – R1g 600/600 SUCCESS](https://github.com/Odourman/let-me-out/actions/runs/43817440347). En enda NTSC standard F6 16 384-byte ROM, SHA **`a2cef3a6cf63bd1f0139f041d08e71c1a70e6569b298082aeb23e94b1776802b`**, väljer cykelexakt kernel genom `FRAMELO & $30` i blanktid, byter vit fjärde NPC X330/348/360/378 under 600 autentiska sammanhängande Stella debugger-frame-ID 11–610. Antal vid respektive X: **150/160/146/144**.
- Full teknisk käll- och testuppföljning [R1g 600-PASS](https://github.com/Odourman/let-me-out/blob/research/main-ii-r1g-four-X-dynamic-600-20261116/docs/MAIN_II_R1G_FOUR_X_DYNAMIC_600_STELLA_LOCAL_PASS_2026-11-16.md). Evidensartifact **14202444990**, 622 filer inkl. alla 600 verkliga bilder och `frames_600.csv`. Fysisk ROM-hash efter nedladdning, ZIP-integritet och summary.json omkontrollerade.

### Kontrollmatris i sista R1g-ROM

| Resultat | Mätt värde |
|---|---|
| Fyra olika fulla 8×9-original-NPC, gul spelare, exakt en M0 | **600/600**, utan maskfel |
| 262 NTSC rasterlinjer | **600/600** |
| Stray vita eller gula pixlar i nio-radersbandet | **0** |
| Spelarens rå Stella-GUI X | **216 i varje ruta** |
| Tre P1-original-NPC-X | **oförändrade i varje ruta** |
| Fjärde kvinnliga NPC:s rå GUI X | **330, 348, 360, 378 i cykliska 16-rutorsblock** |
| Pixelavståndets spännvidd fjärde X | **24 TIA-färgklockor** |

**Detta är inte godtyckligt fri X över hela 160 CC.** Fyra diskreta lägen i högra halvan räcker inte som rörlig NPC-design. Den tidigare R1e automatkopia kan inte fortfarande beskrivas som en *obrytbar hårdvaruspärr*, men godtycklig fjärde X samt fyra och sex fullt fria NPC saknar bevis.

## Övriga utförda trick i 26-posterplanen

- **#07 Asymmetric Playfield:** [Actions #43816293703](https://github.com/Odourman/let-me-out/actions/runs/43816293703) **lokalt PASS**, vänster brun PF0-vägg står kvar 48/48 rasterrader, höger vägg låst 48/48, upplåst 16/48 med 32-raders öppning endast till höger; 262 NTSC. Denna ROM är en **separat R3-geometriprob**, INTE väggar/dörr på R1g:s kritiska NPC-rader, ingen orange port/svart nyckelhål.
- **#25 Stack-Based TIA Register Tricks:** [Actions #43816526765](https://github.com/Odourman/let-me-out/actions/runs/43816526765) **lokalt PASS** i kontrollerad speglingsprob: `PHA` med SP=$08 skriver `$0108` → speglade `COLUPF=$08`; två låst/öppet Stella-vyer har 0 skillnader i TIA-pixlar mot `STA COLUPF` och 262 NTSC, SP återställd. **Ingen CPU-besparing** påvisad, PHA och STA zp tar båda tre cykler. Inget BRK-produktionstrick.
- Tidigare **#10 HMOVE**: 4/4 P0-parets finflytt PASS men P0-wide-kopian förblir kopplad till spelare; R1f är en annan mekanism. **#08 Two-Line** enkel dubbel-WSYNC tappar normal 9-radershöjd (negativ variant), **#05 Dynamic PF** 4/4 extra grov PF i SEPARAT höjdband (inte godkänd same-Y-humanoid).
- Samtliga 26 och positiva/negativa klassificeringar i [levande trickregister](MAIN_II_26_F6_TRICKS_TEST_REGISTER_2026-11-16.md). **27–30 exkluderade** enligt användaren.

## Vad MAIN inte får dra för slutsats

1. Inga påståenden om sex oberoende humanoider på samma rasterband. De tre P1 står still i R1g:s 600-rutorsprov; R1c visade endast ett litet separat X-steg.
2. `M0` är ett enkelt gult provskott på fysisk rasterrad **före NPC-bandet**. Inte kontinuerlig gameplay-projektil och inte på samma nio raders kritiska belastning.
3. Inga bruna PF-väggar/högerdörr i **samma rader** som de fyra original-NPC, trots positiv separat dörr-prob. PF0/1/2 och COLUPF kräver verklig 76-cykel- och latchanalys.
4. Ingen nyckel/O1, femte/sjätte NPC, näraöverlapptest, PAL, konsolhårdvara, fullspel, AI eller oberoende VERIFICATION. En användarwaiver förlorade bitar/flimmer finns inte.
5. Framgång i en forskningsgren får inte mergas eller automatiskt ersätta `main`/draft PR #7/Issue #8:s frysta baseline.

**Nästa forskningsgrind:** mät hur den frigjorda P0-kopiemekanismen klarar vänster/centrum, näraöver­lapp och flera samtidigt förflyttade P1. Bygg därefter en separat *integrerad PF+R1g rasterbudgetprobe* med vägg- och dörrskrivningar. Behåll originalmasker exakta, NTSC 262, 76 CPU-cykler per fysisk scanline, och utför oberoende Verification först på en faktiskt auktoriserad implementation. Detta är förslag inom RESEARCH, inte kodorder.

**Repositorydisciplin:** `main`, draft PR #7 och oberoende VERIFICATION Issue #8 orörda; enbart separata `research/*`-grenar använda.
