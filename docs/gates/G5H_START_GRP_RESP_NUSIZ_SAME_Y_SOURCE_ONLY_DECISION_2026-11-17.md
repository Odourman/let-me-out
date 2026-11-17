# LET ME OUT! – MAIN VI G5H: RESP/GRP/NUSIZ RASTERFÖNSTER OCH FEM FIENDERS WORST CASE
**Datum:** 2026-11-17 · **Klassning:** `G5H_SOURCE_ONLY_DIRECT_KERNEL_FAIL_FOR_UNRESTRICTED_FIVE_NO_PHYSICAL_G0_PASS`.
**Uppdrag:** användaren: "Ok fortsätt" efter G5G Ball-left-wall och direktsekvens-budget. Denna fortsättning är en **källbaserad full genomgång av MASK-radruns, olika X-ordningar, GRP-/RESP-antal och NUSIZ/M1-trick**. **Ingen ny ROM, ASM, Stella-körning, designcanon, PAL, mapper, G6/F12 eller independent E02.** Varken R1 sex fiender eller R2 fem + key i historisk v0.18 ändras tyst. Den föreslagna fem-NPC-versionen är ny SOURCE-ONLY arbetsinriktning (2 stora M, 1 stor F, SM, SF).

## 1. Två väsentliga gränser från original-TIA-källor
- `GRP0/GRP1` styr 8-bitars playergrafik, `RESP0/RESP1` ompositionerar **en enda horisontell counter per player**, `NUSIZ0/1` ger fasta extra kopior vid ungefär **16/32/64 colorclock separationer**; `HMOVE` finjusterar men skapar inga nya individuella horisontella counter. `VDEL` ger lagrade maskvärden, ingen extra player-position. `NUSIZ0` påverkar M0-kopior, `NUSIZ1` M1-kopior. Alla påståenden om verklig START-effekt måste bevisas i Stella-DEBUGGER, inte bara av `STA RESP`-cykeln. [Original Stella Programmer's Guide](https://www.atariage.com/2600/programming/2600_101/docs/stella.html) · [Andrew Towers TIA notes](https://www.retroisle.com/atari/vcs/Technical/Hardware/TIAnotes.php).
- `Ball` är **EN** 1-bitars enhetsgrafik med `RESBL`-position, `ENABL`, bredd 1/2/4/8 CC via CTRLPF D4/D5, och normalt samma `COLUPF` som bruna väggar. Den **behåller sin horisontella position mellan scanlines** och kan därför i teorin rita en brun, 4CC bred x0-vänstervägg under 32 door-scanlines utan att CPU gör `RESBL` på varje rad. Detta är den nya G5G-hypotesen, fortfarande **inte faktiskt positionerad i Stella och inte E02-verifierad**. Bitmodellen 3520/3520 matchar originalrum A/B/C/D när `PF0` släcks i door-y9–12; portens orange P1-mask med inskuret transparent nyckelhål förblir oförändrat.

**Lås inte upp någon G6-fysikorder här.** Detta är nästa SOURCE-ONLY kontroll av om de sparade väggcyklerna kan omsättas i en godtagbar fem-NPC-kernel.

## 2. Ny bitmap-radanalys: sorterade identiska GRP-byte kan återanvändas (trick 02+24)
**Källa och källhash:** `design/NPC_REFERENCE_8x9_masks.json`, Git blob `058800a4c1904d1ff289e7e61b3902aa111ba16d`. En identisk byte behöver **inte** laddas/skrivas igen mellan två objekt om GRP-kanalen har samma bitmap och TIA-START kan startas om på rätt X. Detta kan spara den direkta opcode-parningen `LDA #imm` 2c + `STA GRP0/1` 3c = **5c per sammanhängande maskrun som undviks**. Om figurer med olika bitmap kommer emellan måste GRP ändå laddas igen.

**På originalrad 6 är alla fyra typer olika:**

| Originaltyp | 8bit rad6 | Same-Y påverkan |
|---|---|---|
| Large M | `00100100` | Identisk för våra två stora män |
| Large F | `01111110` | Annan mask |
| Small M | `00011000` | Annan mask |
| Small F | `00111100` | Annan mask |

### A: P0 = player + en stor M; P1 = M + F + SM + SF; orange port längst höger
Alla **24** horisontella P1-identitetsordningar (4!) har granskats mot ALLA nio originalrader. Rad 6 kräver **fyra olika P1-bitmaps i samtliga 24**; GRP-run-tricket kan inte spara en P1-laddning där. Med två P0 maskload/RESP, fyra P1 maskload/RESP, orange P1 door-mask/RESP, två P0-färgskrivningar, två P1-färgskrivningar och WSYNC blir det **79/76 CPU-cykler** på rad 6 i den dokumenterade *naiva direkta opcode-modellen* redan utan numerisk X/Y, M0-enable, PF-row-change, tabellindex eller verkliga START-deadlines. **Direktsekvens A FAIL i exakt den klassen; inte universellt TIA-omöjlighetsbevis.**

### B: P0 = player + BÅDA stora M; P1 = F + SM + SF; orange port längst höger
Alla **36** distinkta registerordningar (P0: 3! =6 med två etiketter M1/M2, P1:3! =6; 36 profiler) har analyserats:
- När P0 kan rita de två stora männen **intill varandra i X-ordningen**, kan båda använda samma `GRP0` under en viss rad. På kritisk originalrad6 minskar den optimistiska direktsumman från **79/76 till 74/76**; den nominella marginalen är bara **2c**, före RAM-maskfetch, X/Y, M0, NUSIZ och fysisk färg-START.
- När **gul player ligger horisontellt MELLAN de två vita männen**, måste P0 byta bitmap white→player→white, och vår direktsumma blir **79/76 FAIL** igen. Det förekommer i **12/36** registrerade ordningsprofiler (2/6 P0-ordningar × 6 P1-ordningar). Att bevara fri numerisk X gör denna ordning obligatorisk att stödja utan att flytta/ta bort aktörerna.
- Särskilt COLOR STRESS: om det aktiva **M0-skottet kräver gult** (såsom i G4:s uttalat hypotetiska testprofil) och befinner sig **till höger om de båda männen**, när player ligger mellan dem, behövs `COLUP0` white→yellow→white→yellow (skott)→white (nästa rasterrad) i stället för bara två P0-färgväxlingar. Det är **två ytterligare** direkta `LDA #; STA COLUP0`-par = **+10c**, dvs **89/76** i samma illustrativa modell. **Gult skott är ett villkorligt G4-stressantagande, inte en ny kanonisk fastställd skottfärg.** Fysisk P0/M0 färg vid samma colorclock är fortfarande en separat konflikt.

**Bästa radrun i B kan alltså förbättra den normala rastersumman, men den fria spelarens X-ordningskorsningar tar bort marginalen.**

## 3. Reproducerbar 24+36-kombinationsaudit av alla nio originalrader
Maskinläsbart: [G5H 9-raders mask-/cykeltabell](G5H_ROW_MASK_RUNS_AND_COLOR_STRESS_2026-11-17.csv).

| Originalrad | P1 vita aktiva A | A min/max GRP-runs i P1 | A min/max direktkostnad | B min/max direktkostnad |
|---:|---:|---:|---:|---:|
| 0 | 2 | 1/1 | 58/58 | 58/63 |
| 1 | 2 | 1/1 | 58/58 | 58/63 |
| 2 | 4 | 2/4 | 69/79 | 69/79 |
| 3 | 4 | 2/4 | 69/79 | 69/79 |
| 4 | 4 | 2/3 | 69/74 | 69/79 |
| 5 | 4 | 2/3 | 69/74 | 64/69 |
| **6** | **4** | **4/4** | **79/79** | **74/79** |
| 7 | 4 | 2/3 | 69/74 | 64/69 |
| 8 | 2 | 2/2 | 63/63 | 58/63 |

**Reproduktionsregel:** För varje `y in 0..8`, filtrera endast ut `00000000`-masker (originalraden bevaras). Sortera efter **faktiska olika X**, beräkna antal sammanhängande olika 8-bitarsmask-runs per P0/P1; P0 player antas ha en självständig fullstor GRP-bitmap under alla nio rader och alltid kräva en skild grafisk gruppering från vit male. P1 dörren antas vid far right och ha skild mask/färg (orange). Antal resp-events = antal aktiva figurer per kanal, även när GRP-byte återanvänds. `STA RESP` =3c per aktör, `LDA #bit`=2c+`STA GRP`3c per run; `LDA#`2+`STA COLUPx`3 c per färgväxling (P0=2, P1=2); `STA WSYNC`3c. De exakta identiteterna M/M/F/SM/SF behålls. I B enumereras P0-order M1/M2/P och P1-order F/SM/SF (36 etiketterade ordningar, två M visuellt identiska); i A P1 fyra typer (24).

**VIKTIG INTE-ÖVERTOLKNING:** Det är **instruktionskostnader i en given direktsekvens**, inte verklig PC-/bank- och START-fasordning. Eftersom full numerisk X/Y och bildrutvariabel vertikal bandstart inte kan ersättas med nio fasta förkompilerade profil-ROM, kan verkliga `LDA RAM zp` 3c eller `LDA ROM,Y` 4–5c behövas i stället för illustrationens omedelbara `LDA #imm` 2c, PLUS index-/tabellarbete. I B bästa kritiska rad6 med totalt sex GRP-runs skulle bara 1c dyrare RAM-lookup per mask lyfta **74→80/76** redan innan resten. Detta är ett **villkorligt bytestest**, inte ett bevis att alla framtida smarta kernels måste läsa RAM-masker just där.

## 4. Äkta X-stress och varför NUSIZ eller mellanrads-positionering inte löser worst case
Som en geometriskt möjlig **C02 y10/11-rumscen** är innerområdet öppet på de båda raderna. Välj fem vita NPC vid start-X (synliga colorclocks) **[16,36,56,76,96]** och gul player X124; en aktiv visuell testprojektil vid X140. Den orange dörren ligger längst höger och hela gruppen kan vara i samma nio-scanlinehöjd på den öppna delen av C02 y10–11. Detta är förregistrerade **kandidatkoordinater**, inte uppmätt eller godkänd ROM.

- White-NPC-skillnader i X är multipler av **20 CC** (20/40/60/80). `NUSIZ` hårdvarukopior med fasta 16/32/64 CC-avstånd kan **inte** användas för denna uppställnings naturliga pairings, och door-pixelx152 är inte heller i +16/+32/+64 från X96. Även om två stora M har identisk grafikraddata fungerar inte automatisk kopiering vid deras önskade avstånd 20 CC.
- `RESPx` register kan behålla en **ENDA** playerkanals senaste X när nästa scanline börjar, men efter att den kanalen ritat många **olika X på samma rad** är dess counter inställd på **sista** ompositioneringen, inte på första NPC:s tidigare X. En generell sourceplan kan INTE avskriva ett `RESP` per vit fiende genom att hävda att positionen "redan finns" på nästa rad. Att tidigarelägga reset till föregående rad kan flytta kostnad och hota föregående figur; det är INTE verifierat sparad nettotid.
- **Nominal 20-CC mellan två P1-starter motsvarar bara 6⅔ CPU-cykler.** Två separata `STA GRP1`+`STA RESP1` kostar 6c **UTAN** maskfetch och utan någon marginal för faktiskt START-latch/NR / PF. Om en ny mask måste hämtas **mellan** två figurer (`LDA #imm`2+`STA GRP1`3+`STA RESP1`3 = 8c), är den direkta sekvensen **för lång för just ett 20-CC mellanrum**. En data-prefetch före eller VDEL/NUSIZ kan möjligen hjälpa, men behöver faktisk opcode-/START-plan. Ännu tätare 12-CC gap ger bara 4c mot `STA GRP1`+`STA RESP1` = 6c, och är därmed ett starkt falsifierande delprov för just den direkta tvåskrivsmetoden. **Detta är INTE ett universellt motbevis mot alla 2600-renderingstekniker**, och det får inte användas som ett "minsta färgklockor"-bevis utan verklig START-kontroll.
- **M1 som vit maskrad-avlastning** analyserades mot de fyra orörda 8x9-originalmaskerna: M1 har bara en sammanhängande färgad bredd 1/2/4/8 CC. För rad5 är Large M `00100100` splittrad och F/SM/SF `01111110` är sex sammanhängande CC (ej direkt M1-bredd). För rad7 är ALLA fyra typer splittrade (M `01000010`; F/SM/SF `00100100`). Därför kan M1 INTE ersätta en hel original-8x9 aktör genom ett enda enable/width-objekt på alla nio rader. Den kan bara hjälpa vissa rader under separat exakt `RESM1`-/`NUSIZ1`-/färg-/latchbudget, och `COLUP1` följer P1:s vita/orange färg. **Ingen M1-ROM har byggts.**

## 5. Instruktionsinventering på svåraste raden – exakt vad som saknas för G0
B med M1 vit M vid x16, M2 vit M x36, gul player x124; P1 F x56, SM x76, SF x96, orange door x~152. Player ligger till höger om de båda M; de två identiska M-maskerna får alltså i teorin en sammanhängande P0-grupp. Relative TOPDOWN-rad6:

| Operation | Count × opcode cost | Cycles | Bevisstatus |
|---|---:|---:|---|
| P0: mask-run loads + STA GRP0 (M, player) | 2 × (2+3) | 10 | Endast om immediate-data kan vara källstatisk per rad och korrekt P0-START |
| P1: mask-run loads + STA GRP1 (F, SM, SF, door) | 4 × (2+3) | 20 | Alla olika på originalrad6; orange måste komma efter vit vid rätt CC |
| RESP0: M1, M2 och player | 3 × 3 | 9 | Ger inga bevis på verklig X-start utan korrekt TIA counterfas |
| RESP1: F, SM, SF och door | 4 × 3 | 12 | F11 fyra numeriska P1-X underkändes G0 tidigare |
| COLUP0: white/yellow/next row | 2 × (2+3) | 10 | Gult M0-skott vid fel CC ger ytterligare konflikt |
| COLUP1: white/orange/next row | 2 × (2+3) | 10 | Dörrens orange färg kontra vita NPC på samma Y |
| WSYNC | 1 × 3 | 3 | Skriver sista efter grafikhändelserna |
| **Direkt summering** | | **74/76** | **SOURCE COST ONLY, INGEN G0-START PASS** |

**Worst order** på exakt samma öppna C02-raster: M1 x16, **player x26**, M2 x36; P1 och dörr som ovan. Nu kräver P0 tre `GRP0`-maskruns, = **79/76** redan utan separat shot-color-ändring; om M0-skottet är gult på x140 efter andra vita M och detta behövs på varje rad blir det **89/76**, som förklarat §2. Det är ett faktiskt tillåtet logiskt X-korsningsfall som vi inte får ignorera med enkel spawnstatik.

**Extra blockeringar även om direktkostnaden sjunker under 76:** riktig `RESP`→START-fördröjning; GRP-latch/VDEL; NUSIZ/M0-kopior; `RESBL` x0/wall-id med korrekta pixlar; Y-korsning och datafetch; `COLUP0` white/yellow med faktiskt M0-skott; P1 orange/white near-right; CPU/Overscan/RIOT 128 B/F6 aktiv 4KiB; key-drop med R2 hypotetiskt 4 NPC+key och genomskinlig svart keyhole.

## 6. G5H beslut / stoppvillkor
**Verifierat med källdata + deterministisk enumerering:** 24 A-ordningar, 36 B-ordningar, nio 8×9-rader; rad6 A 79/76 för alla, B 74/76 om M-M intill och 79/76 när player mellan; M1 8bit full ersättning saknas på rad5 och rad7. Inget tyder på att NUSIZ fasta kopior kan ersätta godtyckliga 20CC-positioner.

**Inte uppnått:** konkret komplett 6507 .lst PC/bank/cycle, faktiskt TIA START/RESP/BL och originalmaskpixelträff, full numerisk RAM-X/Y, dörr/nyckel integration, Stella/ROM och E02-verification. **G0 = NOT PASSED**, ingen kod får byggas på detta. A/B:s **direkta opcode-sekvenser är underkända för det generella femfienderskravet** i värsta tillåtna X-ordning, men 6507/TIA kan fortfarande ha en ANNAN bevisad arkitektur. Det vore metodfel att kalla detta "Atari 2600 definitivt omöjligt".

**MAIN rekommenderar:** Spara Ball-left-wall-metoden och källanalysen; prioritera INTE flera kosmetiska opcode-besparingar på en direktsekvens som redan faller i row6 och player-middle-fallet. Nästa riktiga researchfråga är **en annan P0/P1-kernelarkitektur med register-/positionsevent som kan hantera täta och korsande numeriska X inklusive dörr utan ett GRP+RESP-par per aktör/rad**. Den frågan bör först granskas SOURCE-ONLY av RESEARCH II eller via specifikt separat MAIN-uppdrag. **Ingen ny G6 ROM-order**; om sådan source-arkitektur inte går att förregistrera med G0-scheman återstår explicit användarval om grafisk samtidighet/occlusion/flicker eller ett plattformsbyte, inte automatisk kompromiss.

## 7. Källor
- [G5G tidigare Ball x0 och 79/76](G5G_BALL_LEFT_WALL_AND_FIVE_NPC_OPCODE_CENSUS_SOURCE_ONLY_2026-11-17.md), [G5H CSV](G5H_ROW_MASK_RUNS_AND_COLOR_STRESS_2026-11-17.csv), [originala 8×9-masker](../../design/NPC_REFERENCE_8x9_masks.json), [C02 öppna y10–11](../../design/PLANERADE_RUMSKARTOR_V011.json).
- [F11 G0 negativa bevisspärrar](G2_NEGATIVE_TESTS_AND_NONREPEAT_RULES_2026-11-17.md), [G3 deadlines](G3_COLOR_CLOCK_DEADLINES_2026-11-17.csv), [G4 Player vs M0](G4_PREREGISTERED_PHYSICAL_HYPOTHESIS_2026-11-17.md), [Historical v0.18 R1/R2/D03 criteria](../ROM_GATE_V018_ACCEPTANCE.md).
- [Original Stella Programmer's Guide: player, ball, fixed NUSIZ copies, VDEL](https://www.atariage.com/2600/programming/2600_101/docs/stella.html), [Andrew Towers TIA notes: actual GRP, counters, missile and ball](https://www.retroisle.com/atari/vcs/Technical/Hardware/TIAnotes.php).
- [R3 frozen developer source](https://github.com/Odourman/let-me-out/blob/000b6f2a579e4aa96995229b2174884fb7c565e2/rom/v018/experiments/r3_c02/r3_door.asm): original standalone P1 orange door, COLUBK=0, CTRLPF=0, not integrated NPC.

**SLUTSTATUS:** Source-only G5H complete. **Direktsekvensfamiljen A/B har falsifierats i worst-case, inte all Atari 2600-teknik.** Historiska sex-NPC-v0.18-testcanon och G5 användarbeslut är fortfarande Pending; fem-NPC är användarens uttryckta tekniska riktning, inte retroaktivt implementerat. **MAIN VI beslutar ingen implementation eller verifierar ROM själv.**
