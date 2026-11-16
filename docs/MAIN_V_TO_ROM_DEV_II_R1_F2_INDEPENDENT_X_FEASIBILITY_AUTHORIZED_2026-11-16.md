# LET ME OUT! – MAIN V till ROM DEVELOPMENT II
## R1-F2 – Independent X Feasibility: en android flyttas medan fem står stilla

**Datum:** 2026-11-16  
**Status:** **NY SEPARAT, UTTRYCKLIGT AVGRÄNSAD ARBETSORDER FRÅN MAIN V** efter användarens "ok, fortsätt" för den rekommenderade R1-uppföljningen. Gäller enbart redan användarauktoriserad **v0.18 NTSC R1-diagnostik** enligt `docs/ROM_GATE_V018_AUTHORIZATION_2026-11-15.md` och GitHub Issue #6. Detta är **inte** fullspelsauktorisation, generell fri-X/Y-implementering, grafisk waiver eller beställning av oberoende VERIFICATION.

### 1. Grund för MAIN:s teknikbeslut

**Huvudfråga:** Går en av sex kompletta ursprungsandroider att flytta i X, **medan fem andra verkligen står kvar**, utan att någon av de sex 8×9-maskerna klipps, får vita ghost-pixlar eller ersätts av en annan grafisk form, och kan den förflyttningen i ett senare delprov ske i **en och samma körbara ROM** utan ny assemblerbuild mellan lägen?

**Originalkrav är oförändrade**: två stora män, två stora kvinnor, liten man och liten kvinna, sex individuellt representerbara X/Y i slutligt R1, gul fullstor P0-spelare, M0-skott och bruna PF-väggar på samma/överlappande nio rasterhöjder. Ett fixed-X-bevis är inte fri X, ett tvålägesbevis är inte sex fria X och en RAM-tabell med förändrade siffror är inte bevis för synliga positioner.

**Historiska frysta fakta (återbygg från verkliga källor före varje slutsats):**
- Fryst föregående R1: `rom-dev/v018-r1-independent-xy-20261116`, commit `b02ee3fe9e1ffe4bd77460ff43263a35e1f544e0`.
- Avslutad R1-F1: `rom-dev/v018-r1-f1-sixmask-forensics-20261116`, commit `ea1c09f865c6ec5e3ecd984138a9631a0fb7c82a`. [Slutrapport](https://github.com/Odourman/let-me-out/blob/ea1c09f865c6ec5e3ecd984138a9631a0fb7c82a/rom/v018/experiments/r1_free_xy/TO_MAIN_R1_F1.md); [MAIN:s mottagning och supersession](MAIN_V_R1_F1_RECEIPT_AND_HISTORICAL_AUDIT_CORRECTION_2026-11-16.md).
- **6B** har enligt korrigerad utvecklaregenkontroll **16/16** källkorrekta sexmaskbildrutor vid **fasta X**, ROM SHA-256 `36e588b7211be9dfe6afc534117823f6540aa6d3b753c2816a22c5828d0b60b4`.
- **6C-F1AB** uppnådde enligt utvecklaren **16/16** fixed-X efter sista RESP1 **c67→c65**, ROM SHA-256 `d07387b4da66a4fd41dd782cc86252d36282eea0805cb8899e59cb189f1eabdb`. Använd som teknisk kontroll och gränsfall, inte automatisk kandidat för fri rörelse.
- Källor: `rom/v018/experiments/r1_free_xy/build_six_sweep.py` genererar nio **utrullade** rasterrader med fasta NOP-fördröjningar för varje `RESP1` och intermittent `GRP1`; 6B på scanline 123 hade verkliga `RESP1`-write-cykler **19,28,37,46,56,66**, `GRP1` **22,40,59,69**. Detta är en uppmätt fast formation, inte ett X-register som kan ändras fritt.
- Äldre `analyze_six_sweep.py` har `len(groups)==n` med `n='6B'` (sträng) och därmed falskt FAIL för 6B. **Använd korrigerad audit** `r1_f1_archive_reaudit.py` och skapad F1-CSV, behåll originalverktyget och 6B-ROM frysta. Testa auditens förmåga att DETEKTERA ett fel.
- R1ba:s 600/600-profil använder tre **kopplade** X/Y-uppställningar och är inte fri individuell rörelse.
- R3/C02 separat lokal PASS använder **P1 för den orange porten**, statiskt beräknad peak **74/76 CPU-cykler**, och är fortsatt en senare integrationskonflikt. **Ingen R1+R3-integration här.**

### 2. Inom R1-F2 tillåten självständig utvecklaraktivitet

Skapa **EN** isolerad ny F2-gren från fryst F1 commit, behåll original R1-, F1-, R3-, PR#7- och main-källor orörda. Använd rätt DASM/Stella 6.7.1 och Stella Debugger via befintlig Actions-miljö när lokala verktyg saknas. För denna begränsade uppgift får ROM DEVELOPMENT självständigt bygga minimala diagnostikfiler och köra riktade tester, utan att fråga MAIN mellan varje mikrofelsökning, men med hårda stopp och utan en ny teknikfamilj. Standard 16 KiB F6 får användas, men fyra identiska 4 KiB-bankkopior är inte fyra oberoende grafikkanaler.

**F2-G0 – fast kontroll och trovärdig audit (read-only och begränsad kod):**
- Läs F1:s sexmask-källor, rå-Stella-framebevis och 6B-rastercykler. Kontrollera 6B mot sex korrekta exakta originalmasker, fem orörliga när en annan testas; P0 gul, M0 aktiv, brun PF och **262 NTSC-scanlines**.
- Kör korrigerad re-audit och **minst två MUTANT-negativ** *endast på kopior av testdata*: ta bort/ändra minst en vit maskpixel och skapa en extra vit pixel/ghost eller rubba en hel maskgrupp. Den automatiska checker måste larma; ingen syntetisk bild får lämnas som emulatorbevis.
- Spåra screenshot-pixlar mot riktiga TIA-color-clocks och begärda X. Deklarera om visuell överlappning med M0 eller annan NPC innebär maskövertäckning snarare än förlorade P1-bitmapbitar.

**F2-G1 – isolerad EN-individ-X-geometri (förkompilerade små sonder, ännu INTE dynamik-PASS):**
- Utgå från **6B:s sex exakt hela maskbildningar på en och samma nio-radershöjd**, alla sex källmasker oförändrade. Välj först EN realistisk, horisontellt väl separerad mellanfigur där en **liten icke-noll X-förflyttning** är möjlig som hypotes utan sammanstötning. Behåll de andra fem apparenta start-X-pixlarna **exakt** lika i varje bildruta; håll P0/M0/PF intakta.
- Testa exakt vald liten förskjutning åt ett håll och, om rimlig, åt andra hållet. Rapportera begärd vs verklig X för VARJE person, inklusive identifierad masktyp och samtliga nio originalrader. Mät riktiga `RESP1`, `GRP1` och relevanta övriga TIA-register på hårdaste linjen.
- Efter en faktiskt positiv mellanfigursvariant är ytterligare högst **TVÅ** representativa indexfall tillåtna: en tidig P1-kopia och en sen, inklusive närhet till högerkanten. Sammanlagt **högst tre utvalda individindex, max två avsiktliga X-offsets per index**; inte något generellt positionssvep. Avbryt uppskalning om första relevanta position inte kan flyttas utan att andra fem glider, maskerna bryts eller tiderna blir otillåtna.
- Separata ROM-varianter med compile-time-NOP-inställningar kan högst ge **F2_GEOMETRY_LOCAL_PASS**, inte runtime-X och absolut inte full R1.

**F2-G2 – EN ROM med minst två synligt olika, runtimeskiftade individuella X-lägen, endast om G1 ger positivt pixelbevis:**
- Använd ett ENDA körbart NTSC/F6-program som under samma exekvering faktiskt **byter läge mellan två olika X för bara den valda androiden**, medan sex originalmasker, de andra fem observerade X, Y-höjdbandet, gul P0, aktiv M0 och bruna PF är oförändrade. Förprogrammerad deterministisk frame-toggling duger; inga AI- eller gameplayförändringar. Rapportera vilken ROM/RAM-variabel, vilket frame-ID, begärd X och vilken **faktiskt visad** X som gäller.
- Om hela sexmask-kerneln väljs mellan två separata *förkompilerade formationer* måste resultatet märkas **F2_PROFILE_SWITCH_ONLY**. Det är värdefullt men visar varken generell positionsdata eller oberoende fri X.
- Sök helst **en enda kärnalgoritm** där en förberedd tids-/X-parameter eller begränsad tabellväg för EN individuell mask styr `RESP1`/nödvändig `GRP1` med bibehållen cykeldeadline. Nå ett verkligt runtime-X-bevis för minst två valbara koordinater som den egna avsedda individen kan få, **utan reassemblering**. Märk detta **F2_LIMITED_RUNTIME_SINGLE_X_PASS**, inte generell sexfri-X.
- ROM är inte skrivbart RIOT-RAM: bygg inte på otillåten self-modifying code i standard F6. Förberäkning/tabellbyggning i VBLANK/overscan är tillåten inom diagnostikens scope; mät RAM- och cykelkostnad. Om det måste användas sex fulla duplicerade kernels eller en ny bankarkitektur, rapportera kostnad och varför metoden riskerar att inte skala, i stället för att kalla det generaliserbart.
- Om runtime-data-driven lösning faller, avsluta F2 med korrekt partial/FAIL. **Ingen tredje arkitektur, inget oavgränsat försök med full fri X.**

### 3. Hårda test-, stopp- och leveranskrav

**Mätbara tester:**
1. Minst ett äkta Stella-raw screenshot före/efter varje relevant X-ändring; ingen Pythonmodell räknas som fysisk grafik. Under G1 max **16 faktiska följande bildrutor per sond**. Under G2 max **32 följande bildrutor** med flera verkliga växlingar; ett litet riktat debugprov får komplettera. **Ingen 600-frame-kampanj** inom R1-F2.
2. Automatisk källkorrekt 8×9-per-individ-och-rad pixelkontroll plus optisk representation av masktypen. Fotorealistisk läsbarhet eller överlapp måste särskiljas från exakta maskpixlar. Platsargument får inte räddas genom att klippa mask, tappa en individ, flytta fem andra, dölja M0 eller lägga till ghost-graphics.
3. Exakt tabell över sex `requested_X[i]` och sex `rendered_X[i]`, per testad frame, **alla fem statiska kontrollfigurer oförändrade**; de kan ha identifieringskollision i samma masktyp så använd explicit källindex och masktyp. Att bara skriva olika RAM-X utan motsvarande bilddata är FAIL.
4. Riktiga `PC/bank/frame/scanline/_sCycles/register/value` från Stella Debugger på den hårdaste nio-raderssträckan; källberäknad deadline och 76-cykelgräns särredovisade. Kontrollera NUSIZ1-initvärde, HMOVE-artefakter och wrapper mot vänster/höger bildkant; uppmätt vs statiskt tydligt.
5. En faktiskt körbar ROM, reproducerbar DASM-build, versionspin, 16 384 B och ROM SHA-256, branch- och commit-SHA, käll-/audit-/loggfilindex och positiva såväl som negativa Stella-evidensbilder; spara arkiv i dedikerad Google Drive-mapp och länka GitHub Issue #6. Om verktyg/CI saknas: exakt `F2-INCONCLUSIVE`, inte hittepå-PASS.

**Stoppgrind:** Stoppa direkt efter ett klart och spårbart G1-FAIL för den initiala individen om ingen tekniskt rimlig position finns, eller efter G2:s första uttömmande begränsade runtimeförsök/tekniskt blockerande registerdeadline. Ingen omgjord "tio metoder"-kampanj. Lämna **en** samlad `TO_MAIN_R1_F2.md` med:
- `F2_GEOMETRY_LOCAL_PASS / FAIL / INCONCLUSIVE`;
- `F2_PROFILE_SWITCH_ONLY` eller `F2_LIMITED_RUNTIME_SINGLE_X_PASS / FAIL / INCONCLUSIVE`;
- bevarat **R1 FULLT = BLOCKED/NOT ACCEPTED** tills verkligt sex X/Y-fritt bevis, full T01–T16, integration och senare separat oberoende VERIFICATION;
- ett kort konkret förslag om vad nästa verkliga, separat auktoriserade test skulle behöva vara, eller besked om att den här P1-arkitekturen inte rimligen skalar.

**Fortsatt uttryckligen UTANFÖR R1-F2:** R2, R4, R3-kodändring, same-frame R1+R3 eller nyckel/dörr-integration, sex individuella Y-banor, full 600-frame integrerad R1, AI, annan mapper/extra cart-RAM, PAL, v0.19-kartcutover, flimmerwaiver, ändrad NPC-antal/mask/canon, produktionsmerge, ny PR som ändrar main, The Cabin eller I Love a Fish. OBEROENDE VERIFICATION förblir STANDBY tills MAIN beställer större fryst batch.

**Detta uppdrag ersätter inte användarens designmål. Det ska besvara om 6B-tekniken har någon faktisk individuell X-rörelsemarginal och någon utvecklingsbar runtime-styrning – med data, inte löften.**
