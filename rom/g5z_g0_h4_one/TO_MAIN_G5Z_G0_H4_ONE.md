# LET ME OUT! – ROM DEVELOPMENT III → MAIN VII
## G5Z / G0 H4-ONE: fryst SOURCE-ONLY preflight

**Datum:** 2026-11-17. **Bindande order:** [GitHub Issue #12](https://github.com/Odourman/let-me-out/issues/12) och [MAIN VII:s fullständiga G5Z-order](../../docs/gates/G5Z_MAIN_VII_ROM_DEVELOPMENT_III_G0_H4_ONE_SOURCE_PREFLIGHT_AUTHORIZED_2026-11-17.md). **Enda slututfall: `G0_INCONCLUSIVE_NO_ROM`.**

**STOPP:** `G1=NOT_AUTHORIZED`, `G6/F12=NOT_AUTHORIZED`, `ROM/DASM/Stella/CI=NOT_RUN`, `FULL_H4_SOURCE_PLAUSIBILITY=NOT_ESTABLISHED`, `G5_FORMAL=OPEN`. Detta är EN avslutad källgranskning, inte ett förslag att utföra fler experiment under samma order. Inget nytt .asm/.bin/.lst/.sym, inga byggen, emulatorer, GitHub Actions, grafikändringar eller PR-merge har producerats.

### 1. Granskningens omfattning och primärbevis
- Förregistrerad **hel H4-ONE**: P0 gul diagnostisk full 8x9-spelare **och** vit original-large_male M, i båda horisontella identitetsordningarna; P1 med **två** olika rättvända original-large_female F och small_male SM; ett enda synligt M0 på **en aktiv rad inuti samma 9-radersband**; bruna riktiga PF-väggar i båda kanter, svart BK; separata numeriska RAM-X, standard-F6, NTSC/76c/128B. Inte bara G5P:s N0.
- Historisk R1f bygggenerator [pinnad](https://github.com/Odourman/let-me-out/blob/552a085d0c1ce0ec47d4f3342173658a25fd0e87/rom/v018/experiments/main_ii_r1f_resp0/build.py) byter `NUSIZ0=$04` mot `$02`, lägger två `STA RESP0` och ändrar två statiska källordningar. Historisk [R1g](https://github.com/Odourman/let-me-out/blob/d1d16758c549ecd657aba3b0aa4d6d7559e19264/rom/v018/experiments/main_ii_r1g_dynamic/build_dynamic.py) väljer fyra **förbyggda** rasterrutiner via `FRAMELO & $30` före raster. Båda hade M0 på **föregående** rad och bevisar inte omvänd P0-identitet, generell numerisk X, samtidiga PF eller H4.
- [F9](https://github.com/Odourman/let-me-out/blob/c36982aef770af6cd3f68c2da37b8ed14aee2393/rom/v018/experiments/r1_free_xy/TO_MAIN_R1_F9.md): tre P1-original, men bara **binära** RAM-X och annan ROM. [F11](../../docs/MAIN_V_R1_F11_G0_FAIL_SOURCE_ONLY_RECEIPT_2026-11-17.md): fyra fria numeriska P1-X stoppade redan G0; **0 F11-ROM**, inget generellt omöjlighetsbevis. [G5H](../../docs/gates/G5H_START_GRP_RESP_NUSIZ_SAME_Y_SOURCE_ONLY_DECISION_2026-11-17.md): **79/76** för en fem-NPC/door-direktsekvens och **74/76** för ett specialfall; **annan större belastning** än H4, inte överförbar som H4-FAIL eller H4-PASS.
- [Stella 6.7.1 Player.cxx](https://github.com/stella-emu/stella/blob/6.7.1/src/emucore/tia/Player.cxx) `resp()` har branch för pågående rendering; `nusiz()` kan ändra decode/aktiv rendering. [TIA.cxx](https://github.com/stella-emu/stella/blob/6.7.1/src/emucore/tia/TIA.cxx) skickar `NUSIZ0` till **både** Player0 och Missile0; `GRP0/GRP1` och `ENAM0` köas med intern fördröjning men `RESP0/1` hanteras separat. [Missile.cxx](https://github.com/stella-emu/stella/blob/6.7.1/src/emucore/tia/Missile.cxx) använder NUSIZ-decode och `ENAM0`-gate. [DrawCounterDecodes.cxx](https://github.com/stella-emu/stella/blob/6.7.1/src/emucore/tia/DrawCounterDecodes.cxx) ger `NUSIZ=$02` nominell auto-kopia +32 CC. CPU-strobe är **inte** bekräftad intern START/GRP-latch.
- [Exakt käll-/blobregister](G5Z_SOURCE_PROVENANCE.md) anger vad som faktiskt hämtats. Google Drive-anslutningen verifierades genom läsning av den faktiska G5Z native Doc i officiella projektmappen.

### 2. Exakta nio TOP-DOWN rader och verkliga identiteter
`P` är **tillfällig diagnostisk spelare** i fryst historisk [R1e-källa](https://github.com/Odourman/let-me-out/blob/552a085d0c1ce0ec47d4f3342173658a25fd0e87/rom/v018/experiments/main_ii_p0_four/r1e_four_originals.asm), inte slutgodkänd spelarsprite. `M/F/SM` är oförändrade från originalblob `058800a4c1904d1ff289e7e61b3902aa111ba16d`.

| Top-down rad r | Gul P | Vit M | Vit F | Vit SM | M0 |
|---:|:---:|:---:|:---:|:---:|---|
|0|3C|3C|3C|00|off|
|1|7E|3C|3C|00|off|
|2|18|18|18|3C|off|
|**3**|**7E**|**FF**|**FF**|**3C**|**en enda 1CC-shot vid X=24 i positiva fall**|
|4|1E|18|3C|18|off|
|5|3C|24|7E|7E|off|
|6|18|24|7E|18|off|
|7|24|42|24|24|off|
|8|42|42|24|00|off|

SM:s nollrader 0/1/8 ingår i alla nio genomgångar och får inte kortas bort; om `GRP1` inte nollställs kan en tidigare bitmap synas som ghost. H4 innehåller **tre vita** NPC M/F/SM, inte de framtida fem.

### 3. Positions-/colorclock-kontrakt – inte CPU-STA- eller START-mätningar
NTSC normalrad = 228 TIA CC = 76 CPU-cykler. HBLANK = nominal 68 CC. **Synligt objekt-X = relativ fysisk colorclock 0..159**. Ideal synlig start inträffar vid **absolut CC = 68+X** (motsvarande bråktalet `(68+X)/3` i CPU-cykler som *pixelögonblick*, INTE ett verkligt `STA RESP`-klockslag). R1f/F9 är andra kompilerade kernels; deras fasta c-värden kan inte stoppas in här.

| Test | Skott X / absolut CC / pixel-c | P0 vänster identitet och X / abs CC | P1 F X / abs CC | P0 höger identitet och X / abs CC | P1 SM X / abs CC |
|---|---|---|---|---|---|
|G4-A1|24 / 92 / 30⅔|gul 40 /108|68 /136|vit M 104 /172|132 /200|
|G4-A2|24 / 92 / 30⅔|gul 48 /116|72 /140|vit M 96 /164|128 /196|
|G4-B1|24 / 92 / 30⅔|vit M 40 /108|68 /136|gul 104 /172|132 /200|
|G4-B2|24 / 92 / 30⅔|vit M 48 /116|72 /140|gul 96 /164|128 /196|

Varje 8-bitars START-fönster ligger nominellt på `X..X+7` CC även om raden innehåller nollbitar. Senaste SM START = abs CC196/200 (pixel c65⅓/66⅔), SM bitmap måste överleva åtminstone till CC203/207. Ingen rad i tabellen sätter `STA RESP0/1` lika med dessa pixelögonblick.

**På shot-raden r3:** M mask `FF`, P mask `7E`; det räcker inte att visa objektens geometriska start, färg och mask måste också vara rätt vid varje tänd pixel. Med `M0 width=1` som **villkorligt** testspecifik antagande går shot vid X24 före P0-vänster:
- A1/A2: `COLUP0` gul vid X24 och den första gula P0, därefter vit före M:s första pixel X104/X96.
- B1/B2: `COLUP0` gul vid shot X24, måste byta till **vit** före M:s första pixel X40/X48, sedan till **gul** före senare spelarens första tända pixel (ungefär X105/X97 på P-rad3). För B1 är det efter skottets nominella X24 och före X40 ett synligt fönster om **16 CC = 5⅓ CPU-cykler**; en enkel `LDA #white` 2c + `STA COLUP0` 3c använder 5c, innan internt färg-latch, övriga instruktioner och konkurrerande P1-/M0-skrivningar beaktats. Med antaget noll-latent register gäller CPU-**slut** `c31..35` (absolute 93..105 CC), **inte uppmätt och INTE garanterat giltigt**. B2 har till X48 24 CC. Någon komplett register-och-START-ordning som uppfyller fönstren och resten av H4 är inte källstyrkt.
- **G4-X1:** shot X43 tillsammans med M rad3 `FF` X40..47 kräver olika vit/gul färg under **samma X43** på P0 och M0, vilket är motsägelse för delat `COLUP0`. Ett förväntat negativt **kanalvittne**; inte ett positivt test och inte universellt Atari-NO-GO.
- **G4-X2:** M X40 och player X44 överlappar geometrierna X44..47, samtidigt som en andra `RESP0` kan avbryta den första. O1 gäller key under verklig NPC, inte godkänd maskförlust mellan P0-aktörer. Här finns varken källsäker originalmaskvisning eller fysikmätning.

### 4. Opcode-/cykelinventering på var och en av nio rader
Den **enda** analyskonstruktionen är en konservativ *direkt-event-mall för kostnad*, **inte en genomförbar 6507-listning**. En riktig programcounter, `STA`-slutcykel, grensekvens och fysisk latch kan inte uppges utan faktisk validerad och adresserad H4-källa; att fylla celler med exakta siffror vore påhitt. All numerisk sortering, val av färg-/maskidentitet, eventtid och dataadresser måste beräknas från RAM **före** aktiv rad och kontrolleras mot dess verkliga tidsfönster.

| Opcodekategori | Antal/rad | Cykler | Operand / källa och villkor |
|---|---:|---:|---|
|`LDA abs,Y` ($B9)|4|16|Riktiga P-left/P-right/F/SM radbytes ur ROM; 4c om ingen page-cross, annars 5c; adress/PC ännu okänd|
|`STA GRP0/GRP1` ($85)|4|12|Två till vardera, 3c, intern `GRP`-fördröjning **ej** inräknad|
|`STA RESP0/RESP1` ($85)|4|12|Två till vardera, 3c, **inte** likvärdigt START|
|`LDA #color` ($A9) + `STA COLUP0` ($85)|2|10|Två P0-färgskrivningar; ordning A gul→vit, B vit→gul; shot-rad B kräver gul vid shot innan vit|
|`DEY` ($88) + `BPL` ($10)|1|5 / 4|5c på tagna rad0..7 om ingen branch page-cross; 4c på sista rad8; eventuellt page-cross ger +1c|
|`STA WSYNC` ($85)|1|3|CPU skriver sedan WSYNC; intern väntan utgör inte gratis aktiv render-tid|
|**Direkt-kärna exkl. M0-enable**| |**58c rad0..7, 57c rad8**|Inga idle-slot, inga NUSIZ-ändringar, ingen maskclear, ingen per-rad X-sort, ingen extra PF-write|
|**Shot-rad r3: ytterligare två `LDA #/STA ENAM0`**|2|**+10c → 68c**|Teoretiskt on/off i samma rad; `ENAM0` är fördröjd, och faktisk x24-pixel/ghost-cutoff saknar tidsbevis|
|**Villkorliga två zero-preloaded `STX GRP0/GRP1` clear**|2|**+6c → 64c normal / 74c shot**|Endast om X hålls noll och `GRP`-clear verkligen kan schemaläggas utan att klippa sist ritad kopia|
|**En extra `LDA #NUSIZ;STA NUSIZ0`**|1|**+5c → 79c shot med båda clears**|Den **specifika append-only-mallen** spräcker 76c; en annan ordning/prefetch kan inte uteslutas|

**Begränsning:** 58/68 är exakta kostnadssummor för **dessa valda opcodes**, varken ett universellt lower bound eller cykelplacerade körbara rutiner. `LDA abs,Y` page-cross, branch page-cross, 2c/3c branchväg, förladdningar, M0 `RESM0`, aktörs-/fasdispatch, dynamiskt X och säker `NUSIZ`-policy kan öka kostnaden. Det finns inget påvisat giltigt `c_start/c_end`-schema som placerar dessa opcodepar i fyra sceners verkliga horisontella START-fönster. Alla sådana fält är `UNKNOWN_NOT_A_MEASUREMENT` i [36-raderskalkylen](G5Z_H4_ONE_ROW_CYCLE_CC_MATRIX.csv).

**Radbudget under exakt den här mallen:** r0=58, r1=58, r2=58, **r3=68**, r4=58, r5=58, r6=58, r7=58, r8=57; identiskt rent opcodeantal för A1/A2/B1/B2, men **olika färg- och fysisk deadlineordning**. Villkorliga clear-värden: 64,64,64,**74**,64,64,64,64,63. +1 per korsad tabellsida, +1 för tagen branch över sida. Numeriskt event-/WAIT-schema är **inte** inräknat; det kan inte gömmas i blankning om det styr kritiska `STA`-tider.

### 5. Registretablering, timing och varför kompletta H4-schemat inte kan tecknas
**I VBLANK/bandförberedelse, villkorlig kontrollfördelning:** fem olika `X`-bytes och associerade Y; `CMP`/villkorlig branch för P0 sort med maskpointer och färg-ID, P1 F/SM sort, prefetch/beräkning av CC-deadlines per originalrad och avsedd M0-position; statiskt PF-mönster endast om källa anger samma väggdata på ALLA nio linjer. `NUSIZ0/1`, `RESP0/1`, `GRP0/1`, `COLUP0/1`, `COLUPF`, `COLUBK`, `ENAM0/RESM0`, `PF0/1/2`, `CTRLPF`, `WSYNC` måste ha entydig ansvarig; `RESMP0` får inte oavsiktligt låsa M0 till P0.

**En källspårbar, begränsad PF-preload finns åtminstone som geometrisk kandidat:** alla fyra av MAIN VII godkända framtida 40x22-grid-originalen (A_OPEN_01, B_OPEN_02, C_OPEN_01, D_OPEN_01) har **både rad1 och rad2 exakt `#......................................#`**. Om 8 scanlines per gridrad och room-relativt y8..16 används blir vänster-/höger ytterkant konstant under nio rasterrader. En **villkorlig** TIA-kodningshypotes är speglad PF (`CTRLPF` reflect-bit), `PF0=$10`, `PF1=$00`, `PF2=$00` och `COLUPF` brun, `COLUBK` svart, med faktisk bitordning/crop och 40x22→TIA-Y-offset fortfarande att bekräfta fysiskt. PF kan då förladdas före bandet, inte utelämnas. Detta är **inte** bevis för hela kartan. G4:s exempel room-y96..104 korsar kart-rad12/13 där höger `D`→`#`; för den exakta kartgeometrin får detta band **inte** hävdas helt PF-statiskt. [De fyra pinade källorna och ID:n](../../docs/gates/G5X_MAIN_VII_APPROVED_FUTURE_FOUR_MAPS_SOURCE_MANIFEST_2026-11-17.json).

**NUSIZ0/M0 avgörande osäkerhet:** R1f/R1g:s `NUSIZ0=$02` ger en MEDIUM-autokopia också för missilen, nominellt **Xshot+32 = X56** om missile-decode/fas har startats för X24. En enda M0 kräver därför antingen tidsbegränsad `ENAM0`-gate (på vid X24 och **säkert av före extra decode**) eller en annan noga prövad `NUSIZ0`-/`RESM0`-policy. `ENAM0` går via `Delay::enam`, medan `NUSIZ0` påverkar **P0 och M0 samtidigt** och kan avbryta pågående P0 decode. R1f visade shot på **y−1** med `NUSIZ0=0`, sedan byte till `$02/$04`; detta är exakt varför historien inte ger same-Y-START-bevis. `NUSIZ0=0` under band skulle undvika auto-M0-kopia, men P0:s historiskt fungerande medium-retrigger-START-fas kan då inte ärvas utan en ny källsäker modell.

**RESP/GRP avgörande osäkerhet:** `Player::resp` justerar en **pågående** renderCounter när `myIsRendering` och render counter relativ offset är <4; `Player::nusiz` har en separat decode/rendergren. `GRP` skrivs dessutom via TIA:s fördröjningskö med P0/P1-patterndelning. R1f:s PC-stop före `STA RESP0` är inte ett mätt post-write/START-event. Ingen hämtad källversion levererar en komplett **per numeriskt X** omräkning `RAM_X→STA RESP0/1→intern START→verklig 8CC-pixel` för **samtliga 4 scenlägen**, särskilt för att växla M↔gul och samtidigt hålla F/SM och M0 korrekt. En fast c-tabell för A1/B1 vore förbjuden profilerad rendering.

### 6. 128-byte RIOT, bank och VBLANK
**Räkneexempel på RAM-utrymme, EJ fungerande allocation/high-water:** fem X + fem Y =10; P0/P1-ordning/ägare 4; fem eventfaser 5; fyra 16-bitars maskadresser 8; fyra rullande raddata 4; sex PF-latchbyte 6; shot-position/state/width 3; frame/rad-räknare 4; scratch/färgbuffert 10. **Summa 54 byte**. Om stacken reserveras 32 byte (på 6507:s RIOT-speglade hårdvarustack) återstår hypotetiskt `128−54−32=42` byte. Faktiska adresser, stackdjup, användning i blankning, banktrampolin, tids- och shader/eventbuffer **är inte bevisade**. Det vore fel att hävda RAM PASS.

Fyra F6-banker à 4096 byte ger 16 384 byte ROM men **endast 4096 aktivt åt gången**; R1f/R1g och F9 är separata profiler/banker. Fyra original-/diagnostikmasker kostar 4×9=36 källdatabyte; inklusive övrig originalmask vid behov, PF och faktisk eventkod återstår att allokera. Inget H4 `.lst`/`.sym` eller faktisk körbar event-scheduler finns, alltså inget mätt per-bank bytes-PASS. VBLANK medger begränsad sort/prefetch, inte oändlig tid eller fri 6507-självmodifiering av ROM.

### 7. Preregistererade scenutfall (endast SOURCE, ingen emulator)
| Fall | G0-slutsats | Vad återstår |
|---|---|---|
|G4-A1|**INCONCLUSIVE**|Gul→vit, F/SM samt PF möjliga som separata primitiva delar, men fulla 4x START och M0-single på samma rad ej schedule|
|G4-A2|**INCONCLUSIVE**|Numeriska avstånd 48→96 och F72/SM128 saknar källsäkrad CC-fas-/dataeventmekanism|
|G4-B1|**INCONCLUSIVE**|Vit→gul P0 kräver *tidig* gul shot X24 och vit M X40 inom 16CC samt senare färgbyte; aldrig kört i historiken|
|G4-B2|**INCONCLUSIVE**|Som B1 med M48 och player96, annan fysisk fas och otestad omvänd START|
|G4-X1|**EXPECTED NEGATIVE / COLOR CONTRADICTION**|M0 gul och M vit i exakt X43 kan inte få olika `COLUP0` samtidigt; inte globalt NO-GO|
|G4-X2|**NEGATIVE / INCONCLUSIVE PHYSICAL CLIP**|P0 M40 och gul44 överlappar; rättvänd full bitmap för båda och reset under aktiv rendering ej garanterad|
|G4-M1|**INCONCLUSIVE**|Exakt en aktiv M0 på shot-rad3; `NUSIZ0=$02` och `ENAM0`-delay/clone vid ca +32 CC behöver source-safe fasschema|
|G4-P1|**INCONCLUSIVE**|F och SM nio rättvända källrader finns, men inget integrerat numeriskt P1 GRP/RESP-schema för båda och samtidig P0/M0/PF|
|G5Y hidden x2|**NOT_RUN / ingen certifierad domän**|Två framtida MAIN-valda numeriska X-par inom i förväg deklarerad hållbar domän förutsätter först godkänd scheduler, inte åtta profillägen|

### 8. Slutdom, exakt gräns och STOPP
**`G0_INCONCLUSIVE_NO_ROM`**. Det finns konkreta historiska positiva P0/P1-delfynd och ett källspårbart PF-väggband. Men **inte ett sammanhängande, fullständigt, 6507-instruktions- och intern-TIA-START-fassatt källschema** för H4-A1/A2/B1/B2 med bytekorrekt M/F/SM, omvänd P0-sort, exakt en same-Y-M0, reella bruna PF-kanter, dynamiska numeriska RAM-X och alla 76c-deadlines. Inget brett `G0_FAIL_NO_ROM` kan styrkas utan att göra den smala append-only- eller färg/överlapp-analysen till ett otillåtet universellt omöjlighetsbevis. Inget `G0_SOURCE_PLAUSIBLE` får lämnas när de kritiska effekterna är okända.

**För att en senare, NY och uttryckligen auktoriserad teknisk grind ens ska kunna skilja PASS/FAIL behövs exakta `RESP0/1`-effektklockor, `NUSIZ0` kopie-/missilfas, `GRP0/1` fördröjda latch, `ENAM0` on/off-deadlines, full dynamisk X→händelse-scheduler, cycle/PC/stack/bank och autentiska originalpixlar.** Denna rapport **beställer inte** en sådan grind och tillåter inga nya experiment. [Återstående fem-NPC/S05-gap](H4_TO_FIVE_NPC_AND_S05_REMAINING_GAPS.md).

**MOTTAGARE: MAIN VII.** ROM DEVELOPMENT III avvaktar separat beslut.