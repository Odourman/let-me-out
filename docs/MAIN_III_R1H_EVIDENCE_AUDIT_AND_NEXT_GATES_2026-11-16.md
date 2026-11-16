# LET ME OUT! – MAIN III:s R1h-evidensgranskning och nästa forskningsgrind

**Datum:** 2026-11-16  
**Roll:** MAIN III – teknisk forskningsgranskning och projektkoordination  
**Status:** R1h `LOCAL_PASS` inom begränsat test; full R1 fortfarande `FAIL/BLOCKED`. **Inte oberoende VERIFICATION, inte ett nytt ROM-implementationsmandat och inte en designwaiver.**

## 1. Kontrollerad källidentitet

- Projekt: [Odourman/let-me-out](https://github.com/Odourman/let-me-out).
- Godkänd kodgrind: [v0.18 NTSC/R1–R4](https://github.com/Odourman/let-me-out/blob/main/docs/ROM_GATE_V018_AUTHORIZATION_2026-11-15.md), standard-F6 16 KiB vid tekniskt behov.
- Forskningsgren: `research/main-ii-r1h-ball-left-asym-pf-four-x-20261116`.
- Faktiskt testad GitHub Actions-commit: `3e5b79fd0409a7ed9f9ae381ade6ac1e66d51b32`.
- [GitHub Actions-körning #43821560463](https://github.com/Odourman/let-me-out/actions/runs/43821560463): avslutad SUCCESS; DASM, Stella 6.7.1 och 600-fotografier av riktiga emulatorbilder.
- Evidensartefakt: GitHub Actions artifact-ID `14204881614`, `main-ii-r1h-integrated-4NPC-BALL-PF-rightdoor-600-evidence`, 624 arkivfiler.
- ROM: 16 384 byte, fyra identiska 4 096-byte-banker enligt testarkitekturen; SHA-256 `2a6fc522b139eaebbec6731df8cab1f1c9297f2266ed44a38a9cc2f29b453a39`.
- Nedladdat ZIP-evidensarkiv: SHA-256 `a6329a4fc16e3c7093dfab45bd4f385c77f9d3c7268a597601b69c875a9fa922`.

**Projektgräns:** Forskningen ändrar inte `main`, den separata ROM DEVELOPMENT-grenen `rom-dev/v018-ntsc-diagnostic`, [draft PR #7](https://github.com/Odourman/let-me-out/pull/7) eller [VERIFICATION Issue #8](https://github.com/Odourman/let-me-out/issues/8) för fryst äldre baseline `561d3baf00c6c4c4bd9bc46599a91dc693abdeba`.

## 2. Den faktiska R1h-utvecklargrinden

GitHub Actions-loggen och `evidence_600/summary.json` redovisar följande **lokala utvecklartest**, inte självständig slutverifiering:

| Kontroll | Uppmätt |
|---|---:|
| Sammanhängande Stella-frame-ID 11–610 | 600/600 |
| NTSC 262 rasterlinjer enligt testets HUD-kontroll | 600/600 |
| Fyra **olika** oförändrade 8×9-originalmasker, gul tillfällig spelarfigur och exakt en M0-symbol | 600/600 |
| BALL-vänstervägg x0 enligt testets rastermask | 600/600 |
| Högerdörrens 32-linjers PF-öppning enligt rastermask | 600/600 |
| Oönskade vita/gula GUI-pixlar i NPC-bandet | 0/0 |
| Fyra lägen för fjärde NPC | GUI-X 330, 348, 360, 378 |
| Dörrtillstånd | låst 310, öppen 290 |
| Alla åtta kombinationer X-läge × dörrtillstånd | observerade minst 64 gånger vardera |
| Testskriptets slutstatus | `LOCAL_PASS_R1H_FOUR_NPC_X_BALL_LEFT_PF_RIGHT_DOOR_600` |

**Teknisk mekanism:** BALL ritar den vänstra ytterväggen (förbrukar BL); `PF0` skapar/öppnar högra kanten. Door-toggling och BALL-förberedelse sker utanför de nio tidskritiska NPC-raderna. Fyra specialiserade rasterkärnor används för fyra diskreta X-lägen hos endast den fjärde androiden. De tre P1-androidernas X och den gula spelarens X är fortfarande statiska.

## 3. MAIN III:s separata kontroll av nedladdat evidenspaket

Det ursprungliga GitHub Actions ZIP-arkivet hämtades och öppnades, inte bara metadata lästes.

1. `ZipFile.testzip()` gav inget fel. Innehållet räknades till **624 filer**, varav **600 PNG-bildrutor**.
2. ROM-bytes lästes från arkivet: **16 384 byte**; beräknad SHA-256 matchade både den inlagda `ROM_SHA256.txt` och loggen.
3. `frames_600.csv` öppnades och dess **600 rader** kontrollerades mot index och angivna Stella-frame-ID 11–610. Samtliga `local_pass=True`; inga luckor i CSV eller bildrutefilnamn.
4. Alla **600** bildrutefiler avkodades separat som **900×300 RGB**. En separat pixelhash beräknades på exakt samma spelområdesrektangel `(0,18,321,210)` i varje bild, utan att köra projektets `analyze_600.py`.
5. Gruppering efter rapporterat X-läge och öppet/stängt dörrläge gav **precis en identisk spelområdesbitmap inom varje av de åtta kombinationerna** och **åtta distinkta bitmappar totalt**. Detta stödjer en stabil, deterministisk åttalägesbild utan ny visuell regression över de 600 fångade rutorna.

**Bevisgräns:** Punkt 4–5 är en självständig *bildhash-/arkivkonsistenskontroll*, inte en ny oberoende emulator-rebuild eller oberoende acceptans av varje originalmask mot canon. Att varje av de åtta bildlägena upprepas pixelidentiskt innebär heller inte fri rörelse; provet är en fasstyrd, deterministisk diagnostik.

## 4. Varför detta ännu inte är R1 eller R2 PASS

- **Inte sex androidfigurer:** Endast fyra olika original-NPC visas.
- **Inte sex fria X:** Tre P1-androids står stilla. Fjärde androiden kan bara välja fyra välkalibrerade X-lägen över **24 TIA-färgklockors spann**, inte godtyckliga koordinater över 160.
- **Spelaren är orörlig och använder en tillfällig, ej slutgodkänd 8×9-bitmap.** P0 används dessutom för den fjärde vita NPC:n genom färg-/grafikbyte; när spelaren eller fiender överlappar kan dessa registerdeadlines kollidera.
- **M0-skottet ligger på raden ovanför NPC-bandet.** Skott i samma nio rasterrader är fortfarande obevisat. `NUSIZ0` kan påverka M0-kopior och kräver särskild mätning.
- **Inte komplett rumskarta:** Endast enkel vänstergräns med BL och PF-högerkant; inte alla väggpartier ur 40×22-rummen.
- **Ingen orange port/svart nyckelhål**, inget R2 med fem NPC + guldnyckel/O1, ingen full R3/R4, ingen PAL, inga konsoltester.
- **Ingen oberoende VERIFICATION.** Gamla Issue #8 gäller en annan commit och får inte ärvas.

## 5. MAIN III:s prioriterade fortsatta forskning – inga nya kodordrar

### Grind A – räckvidd och registerdeadlines för X

Undersök vilka **faktiska X-intervall, ordningar och minimiavstånd** som var och en av R1h:s `RESP0`-/`RESP1`-retriggers kan stödja på samma nio originalrader. Bygg en offline-constraint-tabell per rasterrad med `GRP0/1`, `COLUP0/1`, `NUSIZ0/1`, `RESP0/1`, `M0`, `PF0/1/2`, `BL`, `WSYNC` och möjliga page-crossings. Redovisa instruktionscykel **och** pixeldedline, inte bara slutsumman mindre än 76 CPU-cykler.

Pröva minst vänsterkant/centrum/högerkant, nära och långt mellanrum, spelaren mellan två NPC, ändrad NPC-sorteringsordning och simultan ändring av spelare och flera NPC. En uppsättning fyra fasta lägen får inte kallas generell fri X.

### Grind B – minsta verkliga fria-X-delbevis

Ett framtida, separat godkänt kodprov bör visa **minst två olika original-NPC som båda flyttas oberoende mellan bildrutor**, medan gul spelare också kan flytta sig, inom samma nio höjdrader. Om någon originalmask tappar rader eller får spökpixlar: FAIL. Lås inte andra figurens position till spelaren, kopieavstånd eller första NPC. Säkra bruna väggar och M0-konflikten i testkontraktet.

### Grind C – sjunde bitmapbelastningen och full R1/R2

För sex NPC + gul spelare krävs totalt **sju separata humanoida bitmapinstanser** i det hårdaste höjdfallet (plus skott och väggar). R1h visar bara fem sådana instanser: fyra vita + en gul. Räkna explicit om fjärde/femte P1- eller tredje P0-utlösningen kan ske med **olika data och rätt färg** innan respektive kopias pixlar börjar. Framgång med en extra vit figur statiskt får inte tolkas som sex dynamiskt fria X.

R2 med fem NPC + guldnyckel/O1 och full högerdörr får inte skjutas undan av fortsatt R1-experimenterande utan ny scopekontroll.

### Grind D – slutkriterier

Håll `R1=FAIL/BLOCKED` tills användarens C01/C02-krav faktiskt klarats i riktig Stella med minst 600 sammanhängande bildrutor, både same-Y och nära positioner, alla originalmasker oförändrade, relevant M0-/PF-belastning och oberoende VERIFICATION på exakt kandidatcommit/ROM-hash. Inga egna numeriska flimmerwaivers. Inga nya mapperformat, fullspelsfas, PAL, v0.19-kartcutover eller tyst maskförenkling.

## 6. Externa tekniska referenser

- Andrew Towers: [TIA Hardware Notes – re-triggering, copy-start och timingfas](https://www.retroisle.com/atari/vcs/Technical/Hardware/TIAnotes.php). En `RESP`-reset startar inte automatiskt huvudkopian på samma rad; `NUSIZ`-extra-kopior kan triggas senare på samma rad. Ovanliga resetavstånd kan påverka latching/fas.
- Andrew Davie: [Atari 2600 Programming for Newbies, Session 21](https://www.randomterrain.com/atari-2600-memories-tutorial-andrew-davie-21.html): 76 CPU-cykler per scanline, positioneringsarbete och typiska svårigheter vid horisontell multi-sprite-överlappning.

**MAIN III:s beslut:** R1h är en positiv och reproducerbar *lokal forskningsbaseline* för fyra original-NPC + BL-vänstervägg + PF-högeröppning med fyra diskreta lägen för en NPC. Den ska sparas som evidens men **inte mergas eller förvandlas till full R1 PASS**. Nästa aktiva MAIN-arbete är forskningsanalys av oberoende X och faktiska rasterdeadlines; nytt implementationsscope kräver uttrycklig separat auktorisation.
