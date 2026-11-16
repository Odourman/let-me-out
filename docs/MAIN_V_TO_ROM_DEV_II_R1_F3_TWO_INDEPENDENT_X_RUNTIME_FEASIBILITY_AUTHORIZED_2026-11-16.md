# LET ME OUT! – MAIN V → ROM DEVELOPMENT II
## R1-F3 – Two Independent Runtime X Controls (bounded feasibility)

**Datum:** 2026-11-16. **Status:** SEPARAT NY MAIN V-ARBETORDER inom redan användarauktoriserad v0.18 NTSC R1-diagnostik (GitHub Issue #6 och `docs/ROM_GATE_V018_AUTHORIZATION_2026-11-15.md`). R1-F2 avslutades som `F2_GEOMETRY_LOCAL_PASS / F2_LIMITED_RUNTIME_SINGLE_X_PASS / DEVELOPER_LOCAL` på fryst commit `485a6c10047fb9b41e589ac3df724c1bc70f0283`. **Det här är inte fullspelsarbete, R1-PASS, R2/R4/integration eller verifieringsorder.**

### 1. Den ENDA nya frågan

**Går två DISTINKTA originalandroider att välja mellan var sitt par små X-lägen under samma sammanhängande körning av EN standard-F6/NTSC-ROM, med individuellt styrbara runtime-tillstånd, utan att de fyra övriga flyttas eller att någon av de sex ursprungliga 8×9-maskerna deformeras?**

Att bara visa två förkompilerade hela formationer, att koppla ihop de två figurernas X-lägen, eller att ändra bytes i ROM mellan lägen är **inte** bevis för individuell X-rörelse. Fyra kombinationer av de två individernas två lägen måste kunna visas med den **samma** kerneln, varav transitionsgrannar kräver att EN figur ändras medan den andra hålls oförändrad. Ett RAM-register kan hålla flera bitar, men de två logiska positionstillstånden måste vara oberoende skrivbara/väljbara; ett enda gemensamt 0/1-tillstånd räcker inte.

### 2. Exakta frysta källor, klassningar, fysisk begränsning

- Starta EN NY isolerad F3-gren från **fryst F2 HEAD `485a6c10047fb9b41e589ac3df724c1bc70f0283`**. Ändra inte huvudgren, PR #7, R1, R1-F1, R1-F2, R3, Issue #8 eller andra projekt.
- [F2 slutrapport](https://github.com/Odourman/let-me-out/blob/485a6c10047fb9b41e589ac3df724c1bc70f0283/rom/v018/experiments/r1_free_xy/TO_MAIN_R1_F2.md), och [MAIN:s F2-mottagning](MAIN_V_R1_F2_RECEIPT_AND_R1_F3_DECISION_2026-11-16.md).
- Bas-ROM 6B fast sexfigur `36e588b7211be9dfe6afc534117823f6540aa6d3b753c2816a22c5828d0b60b4`, F2 runtime 16 384 B SHA256 **`941c943e9000ca062cc5430cf28bcd34ca92beb70257f4dd84109c487b7c3e2b`**.
- Verkliga källmasker i `design/NPC_REFERENCE_8x9_masks.json` Git blob `058800a4c1904d1ff289e7e61b3902aa111ba16d`. Figurindex 0/1 stora män, 2/3 stora kvinnor, 4 liten man, 5 liten kvinna; F2 flyttar **index2** large_female mellan debuggercrop-X 129 ↔ 135. Övriga X enligt [43,75,129|135,183,243,303]. Alla sex maskerna måste fortsatt matcha på alla nio rasterrader.
- F2:s individuella timing använder `CPX #0; BNE *+2` före tredje `RESP1` och kompenserande `BEQ *+2` före fjärde; **bevarad c46 fjärde position**. F2 rapporterar sista `GRP1` c69, `WSYNC` c72 och statisk marginal 4/76 cykler. Nya tester måste mäta faktiska värden på relevanta scanlines, inte anta att c72 alltid håller.
- TIA-registerförbrukning: P0 gul spelare, M0 skott, P1 sex originalandrider, PF bruna väggar; NUSIZ1=$01 source-styrd, upprepade RESP1 och GRP1. Inget annat objekt borttas för att få testet att se bra ut. R3:s P1-dörr ligger i annan isolerad ROM och **får inte** läggas till.

### 3. Snäv plan och härlett första testspår

**F3-G0 – skrivskyddad kapacitetsanalys FÖRST.** Kontrollera F2-samma-kernelinstruktioner för en **ytterligare** liten X-tidsvariation, registerliveness och senast möjliga pixeldeadlines för samtliga nio rader. Prioritera **android index0** (den första stora mannen), därför att F2:s exakta nio-raderskedja innehåller en tidig `LDA bitmap; NOP; NOP; STA RESP1; STA GRP1; BIT FRAMELO; STA RESP1`, där tidsparet 4+3=7 CPU-cykler principiellt kan jämföras med F2:s `CPY / BNE / BEQ`-kompensationsmönster. Detta är en **teoretisk hypotes**, inte bevis: testa om Y-registret/flaggar, NUSIZ-kopior och den andra startens tidsposition överlever. **Ingen blind omorganisation** av senare GRP/deadlines och ingen påstådd "4 fria cykler" för allmän logik.

Välj en första minimal ±1-CPU-cykels kompilerad kontroll för **index0**, om den ryms i en rimlig registerplan. Index2 ska finnas kvar i sitt första fasta F2-läge. **Högst två** förkompilerade kontrollvarianter för index0. Vid misslyckande får en **enda** annan tidig individindexkandidat granskas offline, men **ingen ytterligare kodfamilj** startas utan separat MAIN-order. Skadade/ghostmasker eller kopplad flyttning innebär FAIL för G1. Resultat: `F3_SECOND_INDEX_GEOMETRY_PASS/FAIL/INCONCLUSIVE`, aldrig runtime-PASS.

**F3-G1 – en enda tvåindividers runtime-ROM, endast om G0/G1-geometrin faktiskt klarar riktiga Stella-bilder.**
- Bevara F2:s RAM-styrda index2-läge. Lägg till **en självständigt styrbar** 0/1-selektor för index0; ett separerat RIOT-RAM-tillstånd eller explicit separat skrivbara bitar är tillåtet. Om `FRAMELO` driver diagnossekvensen ska den kunna generera fyra **oberoende kombinationer**, inte bara två synkroniserade rörelseprofiler.
- Under TopBlank/VBLANK/overscan förbered respektive läge. I synlig kärna använder du som första hypotes **två balanserade branch-par** med separata register/tillstånd, så varje mask får sin egna lilla X-offset med nästa maskposition konstant. Du får välja en annan mikroimplementation av samma sak om mätning visar att den första inte fungerar, **utan** att byta till ny grafikarkitektur. Standard F6, oförändrade originalmasker, P0/M0/PF. Självmodifierande ROM-kod är inte möjlig i vanlig F6.
- Kör en deterministisk 4-stegssekvens av **alla fyra kombinationer `(index0_mode,index2_mode)` = 00, 01, 11, 10** med enbitsövergångar (Gray-ordning) samt upprepningar, där bytes/bitflaggor på RIOT-RAM kan sättas separat. Dokumentera RAM-varje före visuell bild, inte enbart emulatorns efterföljande frame-label; tidigare G2 hade en verklig fas-rapportbugg. Mät alla fyra med **samma körbara ROM** och minst 4 avlästa bildrutor per kombination.
- **Högst 64 sammanhängande verkliga Stella-bildrutor** i enda riktade G1-runtime-testet, samt korta måltraps för två kritiska rasterrader/states. **Ingen 600-frame-kampanj**. Godtag inte att bitmönster bara följer ROM-profilväxling eller enstaka oberoende fixed-ROMs.
- Pixlar: alla sex originalmasker exakt i samtliga nio rader, de andra **fyra** X oförändrade. När index0 ändras står index2 stilla; när index2 ändras står index0 stilla. Skillnader i begärd och faktiskt visad X måste förklaras; överlapp, ghost och vägg-/P0-/M0-destruktion är FAIL.
- Riktiga TIA-debuggertraps för ändrade `RESP1/GRP1`, den omedelbart följande ompositioneringen, scanline/PC/bank/cykel/värde, NUSIZ och HMOVE där relevant. Separera mätta och statiska cykler, page-crossing, init före frame och 76-cykelgräns. Ifall branchkompensation bara ger två lägen på bekostnad av nästa figur: FAIL.

**Kontroll av testverktyg – obligatoriskt på grund av två tidigare felaktiga audits:** bevara de orörda Stella-råbilderna och deras per-frame SHA256; använd korrigerad F2-checker plus helst en **andra, oberoende kodväg** för bitmapmatchning och negativa mutationer, som ska upptäcka felaktig mask, felaktig stå-still-X, extra ghostpixel och **fel frame/RAM-fas**. `requested_X` måste grundas på faktiskt loggat tillstånd under RENDERAD frame, inte härledas av `observed_X`. `FRAMELO`-sekvens i debugger är inte nödvändigtvis samma som redan färdigritad bildruta. En grön read-only re-audit efter en röd bildtestkörning ska redovisas som read-only, **inte** en ny grön Stella-exekvering.

### 4. Stopp, klassning och en enda leverans

**Stanna** när G0:s timingenvelope är tydligt omöjlig, när initial riktad G1-geometri ger reproducerbart byte- eller pixel-Fail, eller efter EN begränsad dynamisk testkandidat och högst en lokal tekniskt motiverad rättning. Ingen ändlös serie tricks, inga nya sexfigurs-sweeps, inga stora nybankade kernels. Om brist på Stella/CI-åtkomst hindrar mätning: `F3-INCONCLUSIVE` med konkret blockerare och underlag, inte PASS.

Leverera **en** `rom/v018/experiments/r1_free_xy/TO_MAIN_R1_F3.md` med käll- och commit-SHA, reproducerbara DASM-/Stella-versioner och byggen, full 16 KiB runtime ROM/SHA, Drive-evidens-ZIP hash + raw PNGs + pixel/auditnegativ och TIA-traps, RAM-karta samt **fyra-kombinationsmatris** och minst 4 bilder per tillstånd; logga både gröna och röda CI-runs. Skilj:
1. `F3_SECOND_INDEX_GEOMETRY_PASS/FAIL/INCONCLUSIVE`,
2. `F3_TWO_INDEPENDENT_RUNTIME_X_LOCAL_PASS/FAIL/INCONCLUSIVE`, där PASS endast gäller **två valbara binära X-lägen per två individer**, **inte** fri X för sex,
3. **full R1 = BLOCKED/NOT ACCEPTED**, sex fria Y ej testade, R2/R4/nyckel och R1+R3-integration ej utförda.

**Rollgränser:** ROM DEVELOPMENT II bygger och egenkontrollerar, MAIN mottar. VERIFICATION är fortfarande **STANDBY** tills stor fryst batch. Inga nya versioner, PAL, fullspel, ändrade figurer/antal/masker, designwaiver, PR #7-merge, produktionskod på main, eller andra projekt.

**Mål:** Ett enda falsifierbart nästa steg från EN till TVÅ verkligt oberoende små runtime-X-styrningar, eller ett ärligt tekniskt stopp. Blanda inte ihop detta med en komplett sexfiende-renderer.
