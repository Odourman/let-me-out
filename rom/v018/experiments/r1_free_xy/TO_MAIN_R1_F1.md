# LET ME OUT! – ROM DEVELOPMENT II till MAIN V
## R1-F1 – Six-Mask Timing Forensics: slutrapport

**Datum:** 2026-11-16  
**Forensikstatus:** **F1-CAUSE_IDENTIFIED** för 6B:s falska FAIL-klassificering och den avgränsade fysiska bildkantskadan i 6C.  
**Full R1:** **FAIL/BLOCKED** för sex androider med **individuellt fria X/Y**.  
**Evidens:** DEVELOPER_LOCAL, inte oberoende VERIFICATION.

### 1. Auktorisation, frysta källor och miljö

Enbart MAIN V:s [R1-F1-order](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_V_TO_ROM_DEV_II_R1_F1_SIX_MASK_TIMING_FORENSICS_AUTHORIZED_2026-11-16.md), alltså exakt 6B och 6C med N5-kontroll samt **en** möjlig falsifierande fasändring.

- Fryst oförändrad R1-bas: rom-dev/v018-r1-independent-xy-20261116, commit **b02ee3fe9e1ffe4bd77460ff43263a35e1f544e0**.
- Separat F1-gren: **rom-dev/v018-r1-f1-sixmask-forensics-20261116**, avgrenad exakt därifrån. F1-filer enbart i rom/v018/experiments/r1_free_xy/ och .github/workflows/. Ingen ändring av main, original R1, PR #7, R3, R2 eller R4.
- [Originalets R1-evidensarkiv i Drive](https://drive.google.com/file/d/1j8r7vzgKmx_XiRRzvZKGFZWlJ776t3F1/view): 5 541 354 byte, SHA-256 **68e538758fd4b452f493242a5fb8e86f527cee18b004483825fc3c05cadbc124**, CRC och 925/925 interna SHA-manifestposter godkända.
- Oförändrad canonical maskkälla: design/NPC_REFERENCE_8x9_masks.json, Git blob **058800a4c1904d1ff289e7e61b3902aa111ba16d**. Sex originalmasker: två stora män, två stora kvinnor, liten man, liten kvinna.
- Autentisk GitHub Actions-miljö: Ubuntu 24.04, DASM-paket 2.20.15~20201109+really2.20.14.1-2 (motor 2.20.14.1), Stella **6.7.1**, Xvfb, xdotool, ImageMagick, Pillow. Standard **16 384-byte F6**, fyra byte-identiska 4 KiB-bankkopior, körd bank 0. F6 skapar inga nya TIA-kanaler.

### 2. Pinning av binärer, källa och clean rebuild

| Variant | SHA-256 av 16 384-byte F6-ROM | F1-bevis |
|---|---|---|
| N5, fast X | 5368d88474187604284c8348054dc6f68cdaeec8492a2ad0d5cd659e4e48a506 | Original 16 PNG och byteidentisk DASM-ombyggnad |
| 6B, fast X | 36e588b7211be9dfe6afc534117823f6540aa6d3b753c2816a22c5828d0b60b4 | Original 16 PNG, ny byteidentisk ombyggnad, riktiga traps |
| 6C, fast X | c9c71fb9c41cee3d1c5bb4839c7d4bbea759151e4e49510b98d4ed3ad2f03c58 | Original 16 PNG, ny byteidentisk ombyggnad, riktiga traps |
| 6C-F1AB, den enda mikrovarianten | d07387b4da66a4fd41dd782cc86252d36282eea0805cb8899e59cb189f1eabdb | Nytt DASM-bygge och exakt 16 nya riktiga Stella-rutor |

Frysta .asm/.lst/.sym och de tre originalbinärerna matchar ursprungliga R1-arkivet. Nya GitHub Actions-byggen jämfördes mot ovanstående SHA med sha256sum -c. Byte-identiska **utvecklarbyggen** är inte samma som en separat beställd oberoende clean rebuild.

### 3. Grundfynd: den gamla 6B-FAIL är falsk

Det frysta ursprungliga auditprogrammet analyze_six_sweep.py beräknar bland annat **len(groups) == n**, där n är en **sträng** som "6B", "6C" etc., inte det heltal som behövs för antalet masker. Därmed blir exact_masks=False för dessa namngivna varianter **även när samtliga sex faktiska maskgrupper är rätt**. Dessutom kraschar senare rapportutskrift när samma text används med numeriskt format.

Ny, separat, läsande, per-pixelrevision av samtliga **48 autentiska original-Stella-PNG** för de tre auktoriserade varianterna:

| Prov | Pixelkorrekta råbilder | Maskgrupper | Korrekt tolkning |
|---|---:|---:|---|
| N5 | **16/16** | 5 | Positiv kontroll med fasta X |
| **6B** | **16/16** | 6 | Sex kompletta originalmasker med fasta X; tidigare FAIL berodde på auditbugg |
| **6C** | **0/16** | 7 | Sex avsedda masker plus bildkants-ghost; verklig avvikelse |

Faktiskt observerade maskstart i Stella 900×300 debugger-crop: N5 **39,93,159,225,297**; 6B **43,75,129,183,243,303**; 6C:s sex avsedda **39,81,135,189,249,309**. Detta är **dubbelupplösta screenshot-pixlar**, inte fritt positionerbara logiska spelkoordinater.

**Viktig korrigering till MAIN:** R1:s historiska generella formulering "0/80 exakta sexmaskbilder i 6A–6E" är otillförlitlig. Minst 16 av de rapporterade 80 bilderna (6B) är objektivt korrekta vid **fast X**. Varianterna 6A, 6D och 6E har **inte** granskats här och får inte automatiskt tilldelas PASS. Originalrapport och fryst arkiv bevaras; detta är ett spårbart delta, inte en retroaktiv ändring av ursprungsdata.

[Reproducerbar forensisk auditkod på F1-grenen](r1_f1_archive_reaudit.py) och [48-raders revision i Drive](https://drive.google.com/file/d/1JGyo8csbTS3cwbTKbk1jDvYK5LzIBlMP/view), CSV SHA-256 **d97654fd9296c47ad26ab9b94b3d4e832fe579d7ceb1ba9f95e2511429d7faf8**. CSV innehåller varje rå-PNG:s SHA och faktiskt bildutfall.

### 4. Precis var 6C:s källmask bryts visuellt

Alla 16 gamla 6C-bilder ger samma avvikelse. De första **fem** maskerna är pixelkorrekta. Sjätte, **small_female**, börjar vid crop-x **309**:

| Källrad | Oförändrad 8-bitars mask | Förväntad/observerad pixel |
|---|---|---|
| 04, bild-y 100 | 00011000 | Vita x315–318 förväntas. x317–318 är faktiskt **gula** M0-skottpixlar RGB (253,253,72). Det är visuell övertäckning, **inte** maskbyteförlust. |
| 05, bild-y 101 | 01111110 | Vitt förväntas vid x311–322. x321–322 ligger **utanför högra synliga bildgränsen**, bara x311–320 syns. |
| 06, bild-y 102 | 00111100 | Rätt vita x313–320 **plus två extra vita pixlar x1–2 till vänster** på följande rasterrad. |

De fyra saknade vita pixlar som den gamla programmodellen flaggar hos sista masken består alltså av **två M0-övertäckta** och **två utanför högerkant**. Extra x1–2 nästa rad är ett **separat autentiskt wrap-/bildkantsfenomen**, inte ytterligare en individ. Vid 6B:s sista start-x303 ses varken denna klippning eller dessa spökpixlar.

### 5. Verkliga debugger-traps – exakt skadad källrad 05

Två inledande riktade trace-serier mätte source-row 06 (Stella scanline 124) respektive source-row 04 (scanline 122). Att de träffade fel rad upptäcktes genom kontroll av **PC mot verkliga DASM-rowlabels**. De räknas därför inte som bevis för själva skadade rad 05.

Korrigerad mätning fångade med Stella Debugger **frame 12, bank 0, scanline 123 = källrad 05**. Traps är villkorade på faktiskt TIA-register och CPU-cykel, och stannar **efter STA-instruktionen**. Alla nedanstående källberäknade cykler har matchats till riktiga debuggerfångster på rätt rad:

| Register | N5, statisk = verklig cykel | 6B, statisk = verklig cykel | 6C, statisk = verklig cykel |
|---|---|---|---|
| RESP1 (ordnade strober) | 21,31,42,53,65 | **19,28,37,46,56,66** | **20,29,38,47,57,67** |
| GRP1 (fyra byteskrivningar) | 24,45,56,68 | **22,40,59,69** | **23,41,60,70** |
| GRP0 | c5, A=$3C | c5, A=$3C | c5, A=$3C |
| ENAM0 | c10, A=$00 | c10, A=$00 | c10, A=$00 |

**Verifierad återtagning av sista saknade 6B-trap:** De automatiska allra första 6B/c19-bilderna blev svarta vid Xvfb-start, och användes aldrig som evidens. Sista **endast läsande** riktade försök fångade **RESP1, frame 12, scanline 123, CPU cycle 19, PC efter STA $F1B7, bank 0, A=$24**. Nu finns verklig GUI-trap för **var och en av de sex RESP1-stroberna** hos både 6B och 6C.

Övrig detalj: 6C:s sista RESP1 är faktiskt **c67**, PC efter STA **$F1DD**, A=$7E, bank 0. Efterföljande GRP1 skrivs **c70** med A=$7E. 6B:s sista par är **c66/c69**. Detta förklaras **inte** av att exekveringen överstiger 76 cykler: båda ligger under gränsen, men fysiska sprite-kopior och pixeldeadlines påverkas av när under scanline skrivningen sker.

- Initieringsvärdet **NUSIZ1=$01** är bekräftat i källkod/DASM; dess tidiga Reset-STA kunde **inte** fångas efter frame12, och ska **inte** kallas mätt sexmasktrap. NUSIZ1 ger close-kopior, inga nya oberoende playerobjekt.
- HMOVE har en riktig tidigare 6B-trap på blankningsscanline 7, c3. Färger source-only vid init: COLUP0=$1E (gul), COLUP1=$0E (vit), COLUPF=$26 (brun), CTRLPF=$01. PF-väggarna finns synligt kvar. Ingen kritisk PF-färgskrivning sker inom valda rasterrad 05.
- GRP0/P0 och ENAM0/M0 finns i samma verkliga registerrad; P0, M0, PF syns i råbilderna. Bytekorrekt ROM-mask är **inte** automatiskt renderad pixelkorrekt mask.

### 6. Exakt EN falsifierande 6C A/B-mikroprob

**Mätgrundad hypotes:** sista 6C-RESP1 på c67 placerar sjätte källmasken för nära höger bildgräns, så att delar försvinner och pixlar dyker upp längst till vänster på följande scanline.

**Enda registerfasändring:** ta bort en **2-cykel NOP direkt före SJÄTTE STA RESP1** i samma unrolled kodmönster på nio ursprungliga bitmaprader. Alla originalmaskbytes, sex NPC, de första fem RESP1-stroberna, P0, M0, PF, NUSIZ1, färger och F6-format behölls. En och samma fasändring upprepas för hela 9-radersmasken, **inte** nio olika varianter.

- Sjätte RESP1 **c67 → c65**, sjätte relaterade GRP1 **c70 → c68**.
- Ny verklig 16 KiB DASM-ROM SHA-256 **d07387b4da66a4fd41dd782cc86252d36282eea0805cb8899e59cb189f1eabdb**.
- **16/16** riktiga Stella 6.7.1-framecrops: sex **pixelkorrekta ursprungliga masker**, 0 extra/saknade vita pixlar, 262-scanline HUD; P0/M0 och PF synliga.
- Fem första maskerna behöll sina exakta start-X. **Endast sjätte start flyttades x309 → x297**, dvs. **12 screenshot-pixlar = 6 TIA-color-clocks = 2 CPU-cykler**. Ingen vänster-ghost eller högerklippning.
- M0-skottet är oförändrat men överlappar inte längre sjätte maskens vita pixlar.

Den enda A/B-mikroproben **falsifierar påståendet att sex fasta originalmasker i detta schema alltid klipps**, och bekräftar **orsakssambandet mellan sen sista P1-reset och just den visade 6C-bildkantskadan**. Det säger inte att sex individer har fria X/Y-positioner.

### 7. Äkta evidens, integritet och reproduktion

Samtliga följande ZIP hämtades ned efter Actions, CRC- och SHA-kontrollerades och lades i **rätt dedikerad Drive-mapp**. De innehåller råa oförändrade Stella-debuggerskärmar, config/autoexec, logs eller 16-rutors A/B-bilder. Felaktiga svarta startupbilder räknas inte som registerbevis.

1. [Scanline 123, source-row05, riktig sex/N5-trace i Drive](https://drive.google.com/file/d/1x28N_KJr9M3NOLkyk6NC5dETABW4l9-o/view) – ZIP SHA **53f7f80c9800259c13e9ab4886d14e1472ce7be26b41e40b726bdb4e18c50f3d**. [Grön Actions 43921122338](https://github.com/Odourman/let-me-out/actions/runs/43921122338).
2. [Sista saknade 6B/RESP1/c19, autentisk GUI-trap](https://drive.google.com/file/d/1PpCAcMFcX9Bjg5rV68ezc8GUTpLFj5t1/view) – ZIP SHA **a1a9e0981b1d66e49bb0e50e59e69d9dac0c9e520d5411376ee9eb4ce89230c8**. [Grön Actions 43921910809](https://github.com/Odourman/let-me-out/actions/runs/43921910809).
3. [Scanline 122-traps och **ENDA** A/B med 16 nya autentiska bilder](https://drive.google.com/file/d/1grjbAdO4eBBh9m0l6cHTzoma9UNNej4s/view) – ZIP SHA **7d7d78421f42ade98a147c9e1aae8875d75a967083ae0cb095071551cb3e03e6**. [Grön Actions 43920307403](https://github.com/Odourman/let-me-out/actions/runs/43920307403).
4. [Scanline 124-traps, inklusive HMOVE-kontroll](https://drive.google.com/file/d/11dLnRMuM-eqSZsk1D0Ce266-s9VafbWB/view) – ZIP SHA **20c92758368ab692a6e4f4bae4502745fe8f25c7bca42eec3d436ff17db02adb**. [Grön Actions 43919329143](https://github.com/Odourman/let-me-out/actions/runs/43919329143).

Återskapa i Ubuntu 24.04 från F1-grenen: installera dasm/stella/xvfb/xdotool/imagemagick/python3-pil, kör python3 build_scaling.py och python3 build_six_sweep.py från rom/v018/experiments/r1_free_xy, jämför ROM mot tabellens SHA, kör sedan python3 r1_f1_archive_reaudit.py på original-Drive-ZIP. För riktade riktiga registerfångster används bash r1_f1_trace_actual_row05.sh, för c19 bara bash r1_f1_first_6b_resp.sh, för enda A/B bash r1_f1_ab_one_phase.sh. Kör inte ytterligare svep/600-rutorsprov under detta avslutade F1. CI-recept under .github/workflows är bevarade.

### 8. Beslut, stopp och möjliga separata nästa beslut

**F1-CAUSE_IDENTIFIED:** 6B:s gamla FAIL är en **auditbugg**, 6C:s verkliga bildfel är **sen c67/c70-placering vid högra skärmgränsen**, med M0-övertäckning och nästa-scaneline-ghost; endast en 2-cyklers fasändring gav 16/16 korrekta sexmaskbilder.

**Fortfarande ej bevisat:** sex individuellt fria X/Y över hela spelplanen, nära positioner/korsning, sammanfallande X, Y-rörelse i sexfigursformat, full sexmask-TIA-rymd-/tidsprofil, 600 efterföljande sexfigursframes, integration med R3:s P1-dörr, oberoende clean rebuild och oberoende VERIFICATION. T02/T04 **INTE godkända för full R1**; T01/T07 **INCONCLUSIVE för globalt krav**; T14 byte-identisk egenbyggning men oberoende del saknas; T15 NOT_RUN; T16 isolering bevarad. Den äldre generiska Actions **43913227299 är fortfarande RÖD** och rättas inte retroaktivt av F1:s gröna riktade jobb.

**Högst två möjliga nya, ej auktoriserade, huvuduppdrag:**
1. **Rekommenderat:** ett dokumenterat MAIN-/validator-rättelsedelta med 6B=16/16 **endast fast X**, historisk supersession av påståendet 0/80 och tydliga T01–T16-statusar, utan ändring av original-ROM eller fryst evidens. Stopp när källor och testetiketter är entydiga.
2. Efter separat MAIN-order: en **mycket snäv** sex-X/Y-falsifiering med 6B som fast-position-kontroll: flytta en individ i taget, håll övriga fasta, avsluta direkt om NUSIZ-/RESP-avstånd eller maskintegritet kräver kopplade positioner. Inga nya breda optimeringssvep.

**R1-F1 är avslutad och levererad. Full R1 förblir FAIL/BLOCKED. Ingen R2, R4, R1+R3-integration, designwaiver, PR-merge eller VERIFICATION är utförd eller tillåten av denna leverans.**
