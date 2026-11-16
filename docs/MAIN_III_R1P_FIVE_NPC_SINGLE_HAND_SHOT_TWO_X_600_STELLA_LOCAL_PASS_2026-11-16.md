# LET ME OUT! – MAIN III R1p: fem originalandroider + EN M0-kula vid handen på 14 rader

**Datum 2026-11-16. Forskningsstatus: `LOCAL_PASS_R1P_SINGLE_M0_TWO_P0_X_600`**, strikt avgränsat till **två av fyra** diskreta P0-lägen. **Full R1 fortfarande FAIL/BLOCKED.** Inget i denna leverans är accepterad spelkod eller oberoende VERIFICATION.

## Exakt genomförd Stella-körning

- [GitHub Actions #43837774400](https://github.com/Odourman/let-me-out/actions/runs/43837774400): **SUCCESS** med DASM och 600 konsekutiva faktiska Stella 6.7.1/X11-bildrutor på testad commit **`9de77b325dee5010244752c9e01f68a5c557a90f`**.
- [Evidensartefakt #14211427332](https://github.com/Odourman/let-me-out/actions/runs/43837774400/artifacts/14211427332), 622 arkivposter, varav **600 autentiska PNG**, originalassembler, listing/symboler, ROM, full CSV och `summary.json`; nedladdad ZIP SHA256 **`4f20004636693f529b50e6d24141435c85b8af88d87d3ff549144aa47c21f50d`**, CRC PASS.
- Körbar standard **16 384 byte NTSC F6** med fyra identiska 4KB-banker; ROM SHA256 **`4b7d4ed1c0b039dea05a59fba4d4c4c5fbd512e7cec2c05a0b9875613ce848c6`**.
- Byggbas [R1o](https://github.com/Odourman/let-me-out/blob/research/main-iii-r1o-single-arm-shot-14rows-20261116/docs/MAIN_III_R1O_ARM_SHOT_FOUR_P0_MODES_PARTIAL_310_OF_600_FAIL_2026-11-16.md), verifierad SHA256 `41a1b55a4d413cca88eccd690d29b6af1a041e4a354e0f4838a832f10fd6c44d`, härledd från exakt R1n14 `eb52e6baf37a396acbbf424a7ba937d78ef662cce7a47aff0cda9d9c6cf25558`.
- **ENDA** förändringen från R1o är att selector före figurbandet väljer **A eller B** baserat på `FRAMELO & $10`, i stället för fyra positioner; R1o:s radkernlar och datatabeller är källidentiska. R1o:s C/D-misslyckanden finns alltså kvar som öppna forskningsproblem, inte bortförklarade.

## Direkt mätta godkända kontroller

| Kontroll i verkliga Stella-bilder | Utfall |
|---|---:|
| 600 löpande Stella-frame-ID utan luckor | **600/600** |
| NTSC 262 rasterlinjer | **600/600** |
| Fem kompletta vita NPC-instansmasker (en stor man, två stora kvinnor, en liten man, en liten kvinna) med ursprungliga 8×9-radbytes, vertikalt upprepade till 14 rader | **600/600** |
| Ursprunglig temporär gul spelarbitmap, nu visad i 14 rader | **600/600** |
| **Exakt en gul M0-projektil vid spelarens hand på GUI x232–233, y167** | **600/600** |
| Gammal M0 ovanför huvudet på GUI-y160 borta | **600/600** |
| Saknad oönskad automatisk M0-kopia vid x296 | **600/600** |
| BALL som vänstervägg och PF0 höger 32-raders dörröppning | **600/600** |
| Fjärde NPC GUI-x330 / x348 och dörr låst/öppen | **4/4 kombinationer** |
| Extra vita och gula bildpunkter totalt | **0 / 0** |
| Felslagna strikt granskade frames | **0** |

Kombinationsantal: x330/låst **150**, x348/låst **160**, x330/öppen **146**, x348/öppen **144**. Samtliga har godkända masker och exakt en synlig projektil. Den extra lokala, oberoende-från-CI-datahanteringen läste hela nedladdade ZIP-paketet (CRC PASS), samtliga **600** CSV- och PNG-par, och räknade hash på autentiska pixlar i aktiv 320×192-region. Resultat: **fyra** olika unika SHA-256-bildlägen, **exakt en stabil hash per P0-X × dörrtillstånd**, utan delad hash mellan lägen. Detta är **lokal dubbelkontroll**, inte separat organisatorisk VERIFICATION.

## Avgränsad spelteknik: varför det fungerar

R1n14:s temporära gula spelare står vid GUI-x216. Med 14 raders visning är spelarens hand nära GUI-y167 och högra ytterkant GUI-x229–230. R1p visar EN gul M0 vid GUI **x232–233/y167**, direkt utanför handen; alltså inte vid huvudet och ingen nödvändig skjutpose eller animation. M0:s ursprungliga x240 flyttades **4 TIA-färgklockor vänster** via `HMM0=$40` under blanknings-HMOVE.

R1o delade de 14 figurraderna i **5 översta + 1 specialiserad armrad + 8 nedersta**. På specialraden (Y=8, top-down index5) är `FemaleRows14,Y=$FF` (D1 satt), vilket gör att `STA ENAM0` kan ersätta en tidigare 3-cykels `BIT FRAMELO` och slå på kulan utan ökade cykler. Strax efter kulan körs **`STY ENAM0`** med Y=8 (D1 rensad) innan `NUSIZ0` hinner rita den extra missilkopian.

På exakt denna rad är de två små NPC-bitmapvärdena båda **$3C**. I stället för `LDA SmallMaleRows14,Y` (4 cykler) + `STA GRP1` (3) används **`STX.w GRP1`**: en tvingad absolut X-skrivning om **4 cykler**. Det sparar exakt **3 cykler** för den extra avstängningen utan att förskjuta andra NPC:ers render-tid. DASM:s `.w`-tillägg tvingar 6502-absolut adressering även för det nollsidesspeglade TIA-registert $001C. R1p använder standard-F6/NTSC, **inga extra RAM-kretsar/ARM/DPC**.

## Varför ursprungliga fyra P0-lägen ännu inte fungerar

I [R1o Actions #43837276975](https://github.com/Odourman/let-me-out/actions/runs/43837276975) klarade samma fullständiga fem-NPC/skottkernel **310/600** bilder med P0-fjärde x330/x348. Vid C/D (x360/x378), **290/600** bilder, kommer `STA RESP0` senare i samma rasterrad. Att stoppa in `STY ENAM0` innan detta strobe flyttar en enskild maskrad, och i den längst högra fasen kan den överlappa lilla mannen. Underkända C/D har separata bild-/källbevis och får inte anses lösta med denna tvåläges-ROM. Fyra-X-lösning ska få ett eget verifierat steg.

## Hårda begränsningar / project gate

- **En kula synlig i en statisk ögonblicksbild**; det är ännu **inte** en riktig avfyrning med rörlig position, skotthastighet, eldknapp, riktning, explosion eller skadelogik.
- **Falska kollisioner** är inte särskilt testade genom systematiska `CXM0P`/RAM-registerläsningar under stress och NPC-rörelse; påstå inte att hela kollisionssystemet är klart.
- Endast **två** av de fyra lilla kvinnans tidigare diskreta X-lägen; inte godkänd sex-NPC fri-X-interaktiv R1. Fem vita figurer (en kvinnomask syns två gånger), inte den saknade andra stora mannen.
- Vertikalt upprepade original-8×9-rader till 14 visade rader är **estetisk research**, inget godkännande att ändra designspecifikation.
- Ingen full karta, nyckel, orange dörr med svart nyckelhål, PAL, riktig rörelse eller oberoende verification; full R1–R4 fortfarande blockerade.

**Projektet rör inte `main`, ROM DEVELOPMENT:s öppna draft PR #7 eller oberoende VERIFICATION-issue #8.**

Nästa relevanta rådgivande steg: undersök en cykelneutral justering av de sena C/D-`RESP0`-fönstren för att förena **alla fyra** P0-X-lägen med **precis en** M0-kula. **Fördela inte resultatet från R1p som auktorisering för att införa fungerande skott i produktionsspel-PR.**
