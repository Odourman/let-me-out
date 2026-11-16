# LET ME OUT! – MAIN III R1i-A: två separata NPC-X-axlar, 600 Stella-bilder – lokal PASS

**Datum:** 2026-11-16.  
**Besluts-/evidensstatus:** `LOCAL_PASS_R1I_TWO_INDEPENDENT_X_AXES_600` för denna isolerade diagnostik. **Full R1 = FAIL/BLOCKED, full R2–R4 inte utförda, ingen independent VERIFICATION, ingen adoption/merge.**

## 1. Exakt reproducerbart resultat

**GitHub Actions [#43827883164](https://github.com/Odourman/let-me-out/actions/runs/43827883164)** är avslutad **SUCCESS**, körd på **exakt commit `190b6237906e21b7f3eff6377dbce7038a0ae1aa`** på forskningsgrenen `research/main-iii-r1i-p1-independent-x-20261116`.

- Standard Atari 2600 **NTSC/F6** med **16 384-byte ROM**, bestående av fyra identiska 4 096-byte kodbanker i det isolerade provet.
- ROM SHA-256: `34a7f515773c6991d0a7abff4d48f6f9d82dadcfb364fb8996d5ccb31539c55c`.
- [Evidensartefakt **#14207252012**](https://github.com/Odourman/let-me-out/actions/runs/43827883164/artifacts/14207252012), 622 ZIP-filer inklusive .asm/.lst/.sym, byggmanifest, binärfil, 600 original-PNG från Stella 6.7.1 X11 Debugger, samtliga CSV-mätningar och `evidence_600/summary.json`.
- Nedladdat verifierat evidensarkiv SHA-256 `cc53807b7cf24cdee1920e8f830cfdc1894bc517092fa8cfede261e9fb447751`; ZIP:s CRC-kontroll gav inga fel.
- Grundbas: R1h-testad ROM SHA-256 `2a6fc522b139eaebbec6731df8cab1f1c9297f2266ed44a38a9cc2f29b453a39` från [Actions #43821560463](https://github.com/Odourman/let-me-out/actions/runs/43821560463); R1i-generatorn kontrollerar exakt denna bas innan byggning.
- Godkända bitmasker från `main/design/NPC_REFERENCE_8x9_masks.json`, blob `058800a4c1904d1ff289e7e61b3902aa111ba16d`. Fyra masker för stor man, stor kvinna, liten man, liten kvinna är oförändrade, inklusive alla nio rader.

### Mätresultat i 600 konsekutiva faktiska Stella-bilder

| Kontroll | Lokal observation |
|---|---:|
| Stella-frame-ID från 11 till 610 utan luckor | **600/600** |
| 262 NTSC-rasterlinjer | **600/600** |
| Fyra distinkta godkända NPC-masker + gul temporär testspelare + exakt ett M0-testskott på föregående rasterrad | **600/600** |
| Inga extra vita eller gula bildpunkter i NPC-bandet | **0 / 0 totalt** |
| BALL-vänsterväggen exakt, inklusive öppet dörrläge | **600/600** |
| PF0-högerdörr: 32 rader, stängd ovanför/under öppningen | **600/600** |
| Stora kvinnans andra P1-strobe, **tidig/normal** | **256 / 344 frames** |
| Lilla kvinnans fjärde P0-strobe, **fyra positioner** | **150 / 160 / 146 / 144 frames** |
| Högerdörr låst/öppen | **310 / 290 frames** |
| Alla **16** olika kombinationer (P1:2 × P0:4 × dörr:2) | **16/16**, minst 32 frames per kombination |
| Oklara figurpositioner eller underkända frames | **0** |
| Actions slutstatus | **SUCCESS** |

### Faktiska positioner (Stella X11 GUI-koordinater, inte native Atari X)

- Gul testspelare: **x216**, temporär testmask, statisk.
- Stor vit man: **x166**, statisk.
- **Stor vit kvinna: x244 eller x280**, beroende på separat `FRAMELO` bit7.
- Liten vit man: **x406**, statisk.
- **Liten vit kvinna: x330, x348, x360 eller x378**, beroende på `FRAMELO & $30`.
- M0 testsymbolskott: **x240–241, y160**, en rasterrad ovanför alla NPC:s **y162–170**.
- 2 GUI-X-pixlar motsvarar 1 native TIA-färgklocka; kvinnans två lägen ligger **18 färgklockor** isär, den lilla kvinnans fyra lägen spänner **24 färgklockor**.

## 2. Vad som ändrades i registerkoden

R1h har en tidskritisk, inrullad nio-raders-kernel med P1 och P0 återutlösta flera gånger. Efter att den stora kvinnans originalbitmap skrivits till `GRP1` vid CPU-cykel 36 följer **två 3-cykels `BIT FRAMELO`**, och därefter `STA RESP1` vid cykel 45.

**R1i-A flyttar exakt samma `STA RESP1` före dessa två `BIT FRAMELO`** i fyra nya specialiserade rasterrutiner: strobe vid **CPU-cykel 39**, i stället för 45. Det är ett omordnande av identiska 3-cykelsinstruktioner, **utan någon ytterligare instruktion eller cykel inne i rasterbandet**.

- De fyra R1h-kärnorna A–D är bevarade; fyra förgrenade, dynamiskt utvalda kopior E–H används för tidig P1.
- P0:s fyra oberoende specialiseringar är identiska per par, utom P1-timing. Före nio-radersbandet väljs P1-läge med `FRAMELO & $80`, P0-läge med `FRAMELO & $30`. Högerdörren använder den fristående `FRAMELO & $40`.
- **Statiskt cykelräknade med verklig DASM-lista:** R1i A–D använder **74** CPU-cykler per tagen branchrad; E använder **75** på grund av 256-bytes sidgränskorsning; F–H använder **74**. Överskrider inte 76 cykler.
- P1 vid c39 är uppmätt som en helt korrekt **separat stor kvinnomask vid X244**, inte bara en ändrad RAM-variabel. P1 vid c45 motsvarar X280.
- Väggen/öppningen använder fortfarande BALL/PF0 och inga nya rasterwrites i figurbandet.
- **Ingen annan cart-arkitektur, flicker, PF-kroppsersättning eller originalmaskändring.**

## 3. Oberoende lokal granskning av evidensbyten (ej oberoende VERIFICATION)

Utöver Actions egen `analyze_600.py` laddade MAIN III ned det kompletta framgångsrika ZIP-arkivet och bekräftade:

1. **622 arkivposter**, inklusive **600** PNG-bilder av riktiga debugger-skärmar; `testzip()==None`.
2. Hämtad 16 384-byte ROM SHA-256 stämde med `ROM_SHA256.txt` och Actionsloggen.
3. En lokal replay av det identiska bildmaterialet från det första (filvägsmisslyckade) provet, med enda korrigeringen `SRC=r1i.asm` och masker explicit jämförda med både R1h och `main`, gav exakt samma 600/600 och 16/16 lägen. Första körningen [#43827595457](https://github.com/Odourman/let-me-out/actions/runs/43827595457) har därför **CI=FAIL på grund av FileNotFoundError i testhärvan**, inte påvisad grafik-Fail.
4. **Separat råbild-hashkontroll** av de 600 bildrutorna: per kombination (stor kvinna × liten kvinna × dörr) är spelområdet **pixelidentiskt över alla förekomster**. Det finns **16 olika hashbilder totalt**, en unik för var och en av de 16 kombinationerna. Minst 32 exemplar per kombination.

Den lokala kontrollen är en **teknisk dubbelkontroll**, inte en fristående verifieringsorganisation, och den visar deterministiska faser snarare än joystickstyrd spelrörelse.

## 4. Vad som återstår (absoluta blockerare)

1. **Bara fyra androidfigurer**, inte sex. Den andra stora mannen saknas, och det finns endast en stor kvinna synlig åt gången (den flyttar sig mellan två positioner).
2. X-positionerna är **diskreta, förkompilerade registertidslägen**, styrda av framecounterbitar. Detta bevisar separata valbara lägen i två maskgeneratorer, **inte** sex godtyckliga X över 160 färgklockor eller oberoende joystick-/spel-AI-styrd rörelse.
3. Stor man, liten man och gul spelare har fasta X. Spelarens figur är fortfarande en temporär icke-canon testbitmap. M0-skottet är en testsymbol **på raden före** humanoidbandet, inte samtidigt på samma nio rader.
4. Vänster yttre BALL-vägg och asymmetrisk brun PF0-högeröppning har bevisats i samma band. **Hela 40×22-kartan, orange port och svart nyckelhål saknas**. BALL är reserverad till vänsterväggen.
5. **R2 fem NPC + guldnyckel/O1** och full R3/R4 är fortfarande ej genomförda. Ingen PAL, riktig Atari-hårdvarusession eller independent VERIFICATION.
6. Framtida R1i-B-hypotes om en extra 18CC `RESP1`-strobe för två stora kvinnor är **inte testad** och får inte ärvas som PASS från detta prov.

## 5. MAIN III:s beslut

**Markera R1i-A = LOCAL_PASS** för **två distinkt valbara, diskreta NPC-X-axlar** under korrekt originalmaskteckning och samtidig BALL-/PF-dörrbelastning. Detta är en verklig förbättring från R1h, utan att rastercykelbudgeten överskrids.

**Behåll full R1 = FAIL/BLOCKED.** Ingen maskförenkling, ingen reducering av androidantal, ingen ny mapper, ingen framflyttad spel-/kartgrind. Forskningsgren och dess lokala CI ska förbli isolerade från `main`, `rom-dev/v018-ntsc-diagnostic` och draft PR #7. VERIFICATION Issue #8 avser en annan äldre commit och får inte automatiskt kvittera R1i.

**Nästa analytiska prioritering:** kontrollera det tredje möjliga P1-fönstret c42 och kombinatoriken för spelarkontrollerad X utan att skapa fler CPU-instruktioner i bandet; alternativ R1i-B med extra faktisk femte originalmask är **egen, separat testgrind** som kräver uttrycklig avgränsning. Målet om sex fria X kvarstår oförändrat.
