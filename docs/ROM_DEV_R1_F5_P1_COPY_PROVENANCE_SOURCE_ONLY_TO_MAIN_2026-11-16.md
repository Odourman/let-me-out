# LET ME OUT! – ROM DEVELOPMENT II → MAIN V
## R1-F5 P1 COPY PROVENANCE – KÄLLANALYS, UTAN NY ROM

**Datum:** 2026-11-16  
**Överlämningsklass:** SOURCE_ONLY, teknisk forensik; INGEN ny DASM, Stella, Actions, ROM, binär-/assembler-/Pythonkod eller fristående VERIFICATION.  
**Huvudklassning:** **SOURCE_ONLY_CAUSAL_HYPOTHESIS_WITH_PREDICTION**, med explicit kvarstående **EXACT_COPY_START_PROVENANCE_NOT_ISOLATED** och **NO_INDEPENDENT_SECOND_X_GEOMETRY**.  
**FULL R1:** **BLOCKED / NOT ACCEPTED**. R1ba är **RESEARCH_LOCAL**, F2 begränsad enindividers runtime-X är **DEVELOPER_LOCAL**, ingen sex fri-X/Y eller två-fri-X-runtime har därmed visats.

### 1. Bindande scope och lästa, pin:ade källor

**Bindande F5-order**, [MAIN_V_TO_ROM_DEV_II_R1_F5_P1_COPY_PROVENANCE_SOURCE_ONLY_2026-11-16.md](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_V_TO_ROM_DEV_II_R1_F5_P1_COPY_PROVENANCE_SOURCE_ONLY_2026-11-16.md), Git blob **0eaf069d4a49ec41b934ef937f77e091f6f40d44**. Nytt rådgivande komplement, [MAIN V F5 HBLANK/R1ba/30-trick](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_V_F5_SOURCE_ONLY_CROSSCHECK_HBLANK_R1BA_AND_30_TRICKS_2026-11-16.md), blob **ba0a39032753f54cb9562d5a83802c35995a44b8**. [CURRENT_PROJECT_STATE](https://github.com/Odourman/let-me-out/blob/main/docs/CURRENT_PROJECT_STATE_2026-11-15.md), läst senaste överordnade F5-sektion. Auktoritetsordningen behandlar gamla researchslutsatser som hypoteser, inte acceptans.

Fryst **F4 HEAD och denna enda analysgrens exakta bas**: **2218e583f4a6f9c60adc3e4bb850b05a7176f1b4**; [F4 TO_MAIN](https://github.com/Odourman/let-me-out/blob/2218e583f4a6f9c60adc3e4bb850b05a7176f1b4/rom/v018/experiments/r1_free_xy/TO_MAIN_R1_F4.md), source [r1_f4_build.py](https://github.com/Odourman/let-me-out/blob/2218e583f4a6f9c60adc3e4bb850b05a7176f1b4/rom/v018/experiments/r1_free_xy/r1_f4_build.py), [F2-föregångaren](https://github.com/Odourman/let-me-out/blob/485a6c10047fb9b41e589ac3df724c1bc70f0283/rom/v018/experiments/r1_free_xy/r1_f2_build_runtime.py), [MAIN:s F4-mottagning](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_V_R1_F4_RECEIPT_AND_NEXT_DIAGNOSTIC_DECISION_2026-11-16.md). F4:s redan levererade [Drive-original](https://drive.google.com/file/d/1ELlpy5rlXrgtW-flmKT7sUpZXKGj3LMJ/view), 1 306 370 bytes, SHA256 **c8585485eeb78cf3fb7c17dd1dbddbc77d17118485232161d9b1c16736dd8c50**; endast läst arkiv-/textinnehåll, ingen ny emulator.

Separat R1ba research-HEAD **788e2b2764b367f880d78d2caa779da58c281281**, [forskningsrapport](https://github.com/Odourman/let-me-out/blob/788e2b2764b367f880d78d2caa779da58c281281/docs/MAIN_IV_R1BA_INTEGRATED_X_Y_PF_SIX_ORIGINALS_600_STELLA_2026-11-16.md), [builder](https://github.com/Odourman/let-me-out/blob/788e2b2764b367f880d78d2caa779da58c281281/rom/v018/experiments/main_iv_r1ba_combined/build_r1ba.py) Git blob **f943d18841058a8a741787ddf19ad6a79dec9797**, [research-granskare](https://github.com/Odourman/let-me-out/blob/788e2b2764b367f880d78d2caa779da58c281281/rom/v018/experiments/main_iv_r1ba_combined/analyze_600.py) blob **5aee0170ee5cad7f096b9f28b0f22896d18f7a8a**. Verkligt existerande, redan levererat [Drive-researcharkiv](https://drive.google.com/file/d/1c2Sd68dvQsmb_MJcQOLU8dbiMc5YgbsJ/view), **3 930 298 bytes**, SHA256 **f8dd41e62939aa1699d80f70df0c5b5081b87441a1e2c740ff2786139908f325**, 622 ZIP-poster CRC PASS: original **r1ba.asm, r1ba.lst, r1ba.sym, proof.bin** och **600 historiskt producerade rå-Stella-PNG** samt historiskt CSV. ROM 16 384 B SHA256 **41fdb87969a20d40fee8cde5673792201663860c2d1e08c8d93f9172ede82361**. SOURCE-ONLY läsning av redan befintlig assembler/listning och auditorkod, **ingen omkörning av 600 bilder**. Forskarens 600/600-påståenden förblir lokala och begränsas ytterligare i avsnitt 8.

Låst [original-NPC-canon](https://github.com/Odourman/let-me-out/blob/main/design/NPC_REFERENCE_8x9_masks.json), Git blob **058800a4c1904d1ff289e7e61b3902aa111ba16d**. Indexordning: **M,M,F,F,SM,SF**, 8 kolumner × 9 ursprungligen definierade top-down-rader, små har transparens i rad 0,1,8. Inga kanondata får ändras. B02 CPU/TIA/cykeltraps, C01/C04 same-Y och E02 fristående [ROM_GATE_V018_ACCEPTANCE](https://github.com/Odourman/let-me-out/blob/main/docs/ROM_GATE_V018_ACCEPTANCE.md) kvarstår blockerande.

**Externa källor, alla lästa SOURCE ONLY:**
- Andrew Towers, [TIA Hardware Notes: horizontal counters, The Re-trigger Trick, CPU Clock to Player Pixel Table](https://www.retroisle.com/atari/vcs/Technical/Hardware/TIAnotes.php) (gate-/signalmodell, inte vår interna TIA-trace).
- Faktisk [Stella 6.7.1 / TIA.cxx](https://github.com/stella-emu/stella/blob/6.7.1/src/emucore/tia/TIA.cxx), [Player.hxx](https://github.com/stella-emu/stella/blob/6.7.1/src/emucore/tia/Player.hxx), [Player.cxx](https://github.com/stella-emu/stella/blob/6.7.1/src/emucore/tia/Player.cxx) och [DrawCounterDecodes.cxx](https://github.com/stella-emu/stella/blob/6.7.1/src/emucore/tia/DrawCounterDecodes.cxx). Här läser vi implementation, men gör **ingen** modifierad emulator-/hårdvarukörning. Stella-kommentarerna erkänner särskilt att RESP under aktiv decode fortfarande kan behöva trimmas.

### 2. Source-only: exakt rasterbudget, nio rader och föregående/nästa scanline

Alla följande c-värden är **CPU-cykler efter aktuell rad-WSYNC**, angivna **efter registerskrivande STA/STX**. De kommer ur de frysta källprogrammen, deras befintliga DASM-listningar och registrerade F4-statiska schema. **SOURCE_ONLY/STATIC** gäller hela 9-radsmatrisen: en särskild äldre Stella-trap vid source-rad05 ger bara punktmätning, inte en egen uppmätt nio-radersmatris.

**F4 $01**, var och en av de nio raderna: **P0 GRP0 c5**, **M0 ENAM0 c10**, första P1 \`RESP1 c18 / GRP1 c21\` för c18-proben eller \`RESP1 c21 / GRP1 c24\` för c21-proben; andra till sjätte RESP **c28, c37, c46, c56, c66**. Övriga uppdateringar av de fyra ursprungliga P1-typmaskerna via GRP1 nära **c40, c59, c69**. Sista GRP1 **c69**, följande WSYNC-skrivning **c72 STATIC**, 4 CPU-cykler beräknad marginal mot 76. F2:s tillåtna index2-motion är alternativ tredje **c38** (andra kompensationsgrenen håller fjärde c46), F4 använder tredje **c37**. Inga PF-skrivningar inom dessa nio rader; PF0/CTRLPF/COLUPF förbereds vid Reset. NUSIZ1=$01. HMOVE under äldre VBLANK, inte som per-rad X-val. Inget nytt VDEL1-steg.

**R1ba $03**, per profilerad nio-raderskernel:
- Cykler **c3 STX GRP1 (föregående P1-radsrest nollas), c10 STA GRP0 gul P0, c15 STA ENAM0 skott**.
- Profil **A**: \`RESP1 c28 → GRP1(M) c33 → RESP1(F) c40 → GRP1(F) c43 → RESP1(SM) c56 → GRP1(SM) c59 → RESP1(SF) c66 → GRP1(SF) c69\`.
- Profil **B**: samma men andra reset **c42 → GRP1(F) c45**.
- Profil **C**: första reset **c30 → GRP1(M) c35**, kvinnors c42/c45 som B.
- Alla tre profiler har källbaserad **WSYNC c72** i normal fortlöpande synlig rad, inte ny real debuggertrap; deras sista rad går genom \`JMP R1acAfterRows\` och följande avslutande WSYNC/GRP-shutdown och måste bedömas som randfall, inte som oinspekterad identisk tidsplan.

**Exakt nio-raders källa-/cykelöversikt; "F4 c18|c21" innebär två separata, tidigare befintliga ROM:er, "R1ba A/B/C" tre förkompilerade nio-radersprofiler i en äldre research-ROM:**

| Bitmaprad (uppifrån 0–8) | F4 P0/M0 | F4 RESP1[0–5] c18-prob / c21-prob | F4 GRP1 första / sista; WSYNC | R1ba P0/M0 | R1ba RESP1[0–3] A / B / C | R1ba GRP1 typ M,F,SM,SF | Nästa WSYNC |
|---:|---|---|---|---|---|---|---|
| 0 | 5/10 | 18,28,37,46,56,66 / 21,28,37,46,56,66 | 21/69 eller 24/69; 72 | 10/15 | 28,40,56,66 / 28,42,56,66 / 30,42,56,66 | A 33,43,59,69; B 33,45,59,69; C 35,45,59,69 | 72* |
| 1 | 5/10 | samma | samma | 10/15 | samma | samma | 72 |
| 2 | 5/10 | samma | samma | 10/15 | samma | samma | 72 |
| 3 | 5/10 | samma | samma | 10/15 | samma | samma | 72 |
| 4 | 5/10 | samma | samma | 10/15 | samma | samma | 72 |
| 5 | 5/10 | samma | samma | 10/15 | samma | samma | 72 |
| 6 | 5/10 | samma | samma | 10/15 | samma | samma | 72 |
| 7 | 5/10 | samma | samma | 10/15 | samma | samma | 72 |
| 8 | 5/10 | samma, följt av BottomBlank | samma + shutdown | 10/15 | samma, följt av R1acAfterRows | samma + shutdown | 72* |

\`*\` betyder att 9-radersproveniens vid första/efter sista raden inkluderar föregående TopBlank och följande BottomBlank/branch; **c72 är endast statisk beräkning i normalt internt radflöde, inte en ny R1ba TIA-trace**. På rad0 är P1:s initiala tillstånd före WSYNC särskilt beroende av preload/TopBlank; på rad1–8 sätts R1ba GRP1 initialt till 0 vid c3, men de **interna render-/positionsräknarna lever vidare** från föregående rad. Under hela 9-bandet kommer den sista föregående radens RESP1 c66 på colorclock 198; till nästa radens första F4-resp c18 = CC54 passerar (228-198)+54 = **84 CC** och R1ba:s första c28 = CC84 ger **114 CC**. Båda är mindre än 160 synliga P1-räknarsteg för en hel main-copy-omgång. Det är ett *källbaserat argument mot* fristående huvudkopiestart mellan upprepade resetter i de **inre** bitmapraderna, inte ett bevis för exakt första START-ursprung på rad0. Endast giltigt utan ytterligare intern TIA retrigger-/pipelineeffekt.

**Bitmapdata-/deadlinekontroll:** R1ba:s c33 GRP1(M) ligger vid nominell cc99, före A:s första close-start omkring cc101, endast cirka **2 CC marginal före start**. R1ba c43 GRP1(F) vid cc129, **efter** M:s medium-start cc117 och ungefär **efter** den åtta pixlar breda M-bildens slut cc125, samt **före** F:s close-start cc137. B/C förskjuter först/kvinna schematiskt men bibehåller smås c59/c69. Dessa nominella deadlines är **SOURCE_INFERENCE**, inte en intern GRP-latch-oscillogrammätning. M0/P0-färg och PF init kommer från verkliga äldre builders, inte ny pixelverifiering.

### 3. Verklig evidens: CPU/write/fysisk X – och vad den INTE mäter

| Familj / fryst material | NUSIZ1 | Första/annan RESP1 i en intern rasterrad | Faktisk mask-start X i 900×300 Stella-crop | Kontrollnivå |
|---|---|---|---|---|
| 6B/F1 | $01 | första c19, nästa c28 | index0 **43**, index1 **75** | tidigare 16 autentiska bilder och riktad trap |
| F3 G0 | $01 | första c20, nästa c28 | index0 **43** (begärt linjärt 49) | **16/16** sourcepixelkorrekta, geometri FAIL, faktisk c20 trap |
| F4 c18 | $01 | första **c18**, nästa c28 | index0 **43** (begärt linjärt 37) | **16/16** bilder, faktisk c18 trap scan123/bank0/PC efter $F1C3 |
| F4 c21 | $01 | första **c21**, nästa c28 | index0 **43** (begärt linjärt 55) | **16/16** bilder, faktisk c21 trap scan123/bank0/PC efter $F1BF |
| F2 i samma körbara ROM | $01 | tredje c37 **eller c38**, fjärde c46 | index2 **129 / 135**, övriga fem orörda | **32/32** från befintliga autentiska PNG, endast EN RAM-X |
| R1ba forskning A | $03 | M c28; F c40; SM c56; SF c66 | **75,107,147,179,243,303** | historisk lokalt egenkontrollerad profilerad research, 297 bilder |
| R1ba forskning B | $03 | M c28; F c42; SM c56; SF c66 | **75,107,159,191,243,303** | historisk lokal, 151 bilder |
| R1ba forskning C | $03 | M c30; F c42; SM c56; SF c66 | **87,119,159,191,243,303** | historisk lokal, 152 bilder |

**OBS:** R1ba:s forskningsaudit visade originalmasker med en **top-down-orienteringskonflikt** (punkt 8); räkna **inte** den sista tabellens 600 frame som ren originalmaskacceptans förrän orienteringen retts ut. Värdena i R1ba-rader är redan historiskt rapporterade faktiska X, inte F5-mätta om.

I F4 är faktiskt \`RESP1\` c18/21, nästa c28, tredje c37 och sista \`GRP1\` c69 mätta **på just source-rad05/scan123**, men **WSYNC c72 är en statisk källuppgift**: efter WSYNC-stoppet anger Stella nästa scanline124/c0. R1ba har ingen full individuell B02 CPU/TIA T07-debuggertrace på samma nio rader. CPU-cykel- och bankdata visar skrivinstruktionen, **inte interna reset/START-/pixel-latch-signaler**.

### 4. Stark kausal HBLANK-teori – ännu inte unik intern proveniens

En Atari scanline har **228 TIA-colorclocks** = 76 CPU-cykler; normalt HBLANK slutar kring **CC68** och aktiv video är 160 CC. För en P1-close-start beskriver Towers en ungefärlig väg **RESP-CPU-write → intern reset (~4 CC) → positionsräknardecode (offset 12) → START-latch (~1 CC)**, netto cirka **17 CC** efter tidigare skrivning när räknaren arbetar i aktiv bild. En medium-kopia ger analogt cirka **33 CC**. **Dessa fördröjningar är hårdvarumodell, inte interna signaler uppmätta i Let Me Out!**

Stella 6.7.1-kod **bekräftar nödvändig mekanik men inte identiteten för varje historisk puls**:
- \`TIA::poke\` tar \`RESP1\`, anropar \`myPlayer1.resp(resxCounter())\`; \`resxCounter()\` skiljer \`HState::blank\`/lateHblank/\`frame\`, alltså är en CPU-registerskrivning i HBLANK inte samma positionsläge som en under aktiv display.
- \`Player::resp\` sätter \`myCounter\` och särbehandlar reset nära \`myIsRendering\` och tidig \`myRenderCounter\`, med kommentaren att detaljerna behöver vidare tuning. Det betyder att redan startad kopia och inkommande RESP kan samverka; man får inte antaga momentan förlust/överlevnad av en START.
- \`DrawCounterDecodes.cxx\` använder \`myDecodes1[12]=2\` för $01, men \`myDecodes3[12]=2\` och \`myDecodes3[28]=3\` för $03. Därigenom är de två R1ba-stora maskparen separata **automatiska kopiestarter från samma countbase**, inte två oberoende TIA-P1-spelare.
- \`Player::tick\` kontrollerar \`myDecodes[myCounter]\`, sätter \`myIsRendering\`/\`mySampleCounter\` och går sedan genom åtta pixlar; ett nytt GRP1-registervärde är inte likställt med en ny positions-start.
- \`TIA::poke\` köar **GRP1** via \`myDelayQueue.push(GRP1,value,Delay::grp)\`; senare \`Player::grp\` uppdaterar \`myPatternNew\` och \`updatePattern()\` (om VDEL inte är aktiv). Därför är **CPU:s STA GRP1**, dess fördröjda effekt och en pixelkopias pågående dataläsning **tre separata tidpunkter**. VDEL1-skrivning finns inte som aktivt R1ba-kernelgrepp, och Stella reset initierar \`myIsDelaying=false\` – inte något nytt verifierat hardware VDEL-tillstånd.

**Empiriskt kalibrerad, snäv bildprediktionsmodell** från de FRYSTA bilderna (inte en TIA-kretsdefinition):

    write_CC = 3 * CPU_cycle
    active_start_CC ≈ 68
    close_start_visible_CC ≈ 17 + max(0, write_CC - 68)
    Stella_cropX ≈ 9 + 2 * close_start_visible_CC

\`+9\` är empirisk cropkalibrering; \`2\` är screenshotpixlar per TIA-colorclock, inte extra TIA-räknarsteg. Ger c18/19/20/21 → **43**; c28→**75**; c37/38→**129/135**; c40/42→**147/159**; c30→**87**; c56→**243**, c66→**303**; medium för R1ba c28/30 och c40/42 ger **close+32 screenshotpx**. Utfallen överensstämmer med redan rapporterade bilder, men återger samtidigt parametrar som är kalibrerade på **samma** datamängd; det är inte en oberoende prediktion av obesett beteende.

**Critical counterexample to a simplistic cancellation argument:** F4:s senare fasta \`RESP1 c28 = CC84\`, medan en idealiserad första HBLANK-baserad close-START ligger runt **CC85**. Den tidigare argumentationen \`"84 < 85, therefore first must vanish"\` är **inte giltig som slutlig hårdvaruslutsats**: internt CPU→counter-reset finns fördröjning, decoder->START-latch ytterligare timing, och både Stella och Towers beskriver specialfall vid åter-reset inom decode-window. Att index0 syns på x43 **bevisar ett riktigt bildstartutfall men inte vilken exakt START-latch som producerade det**. Möjlig proveniens är en redan framtagen close-START från den tidiga resetten, en fördröjd/latchad START nära konkurrerande c28 eller ett tidigare counter-tillstånd; förkasta ingenting utan intern timingtrace. Därav **EXACT_COPY_START_PROVENANCE_NOT_ISOLATED**.

### 5. R1ba: två automatiska kopior per stor-par är samma positioneringsfamilj, inte två fria sprites

R1ba använder \`NUSIZ1=$03\` för **close(+16)** och **medium(+32)** TIA-colorclocks från **samma första stora-par-reset**, inte två oberoende skrivbara indexpositioner. Typisk source-only-klockmodell för A:

| Register händelse | CPU / nominell CC | Nominell fysisk START | Historisk faktisk X och relation |
|---|---|---|---|
| P1 reset för stora M/M | c28 / CC84 | close CC101, medium CC117 | **x75 och x107**, fast Δ=32 croppixlar |
| P1 GRP1 stora M | c33 / CC99 | display nära CC101 och CC117 | Samma maskbyte används för båda automatiska kopiorna; F/M separeras med senare GRP |
| P1 reset för stora F/F | c40 / CC120 | close CC137, medium CC153 | **x147 och x179**, fast Δ=32 |
| P1 GRP1 stora F | c43 / CC129 | före CC137; efter M-bildens c117..125 | Om denna tidigareläggs kan M:s andra kopia muteras |
| P1 reset liten M | c56 / CC168 | close CC185; medium CC201 riskerar c66-reset | **x243**, nästa c66 åter-reset före medium-start (exakt race ej spårad) |
| P1 reset liten F | c66 / CC198 | close CC215; medium CC231 utanför normalt aktivt fönster | **x303**, inte ny fri X-kanal |

A→B ändrar **kvinnogruppens båda X tillsammans** +12 croppixlar, A/B→C ändrar **mansgruppens båda X tillsammans** +12 croppixlar. Samma c56/66 små X kvar. Exakt profilantal och rapporterat Y från äldre R1ba: **A 297** (SM +1, SF −1), **B 151** (SM −1, SF +1), **C 152** (SM −2, SF −1). Förvalda A/B/C-kernels väljs via \`FRAMELO & $18\` **före** nio-radersraster. Det är ett **tidsstyrt byte mellan tre fulla formationer**, inte två oberoende runtime-RAM-X-reglage och absolut inte sex X/Y.

Det finns ingen fyrkombinationsmatris där X för man1, man2, kvinna1, kvinna2 och små kunde ställas separat. Samma white mask kan kopieras två gånger men NUSIZ-decode har ofrånkomligen en **bestämd par-separation** tills ny reset/hårdvaruschema bevisat frigör individernas START. GRP1-byte förstår *maskdata*, inte *separat individ-X*.

### 6. 30 ursprungliga Atari-trick: faktisk teknisk avkastning, inte önskelista

[Exakt 30 ursprungliga tricks](https://github.com/Odourman/let-me-out/blob/main/docs/RESEARCH_30_ORIGINAL_ATARI_TRICKS_2026-11-16.md), [MAIN:s egen R1-tillämpning](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_V_R1_30_TRICKS_APPLICABILITY_REVIEW_2026-11-16.md), [senare HBLANK-korrigering](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_V_POST_F4_RESEARCH_30_TRICKS_HBLANK_COPY_CAUSE_2026-11-16.md). **Det verkliga, här källbevisade framsteget** är tillsammans **#15 NUSIZ-copy decode, #02 mid-rad GRP1, #01 P1-retrigger/multiplex, #24 cycle-exact förberedd nine-row kernel**: R1ba kan utnyttja två automatiska kopiestarter per man-/kvinnogrupp med fyra RESP per rad, men då är parets separata X just låsta till automatikens Δ16 TIA-colorclocks.

**#09 VDEL** kan inte antas ge fri X; R1ba-källan använder ingen aktiv VDEL1-write och gamla Venetian/VDEL tester var negativa. **#10 HMOVE** flyttar P1-counter/gruppens bild, inte oberoende kopior från samma reset. **#08 tvålinjekernel** skulle behöva ny höjd-/maskproof och är här INTE källbevisad. PF-asymmetri (R3), HUD/rasterfärger, scorefonts, alternativa mapper/fler bankbytes och CPU-tabeller ger inte två nya TIA P1-countbases. Äldre Venetian/flicker/fördela originalmasker i halvhöjder uppfyller inte nio-rader + same-Y; ny cartridgehårdvara är förbjuden och skulle inte öka TIA:s två Player-objekt. **Inget trick från listan ger på befintliga källor sex fria X/Y**.

### 7. EN falsifierbar framtida diagnostik på papper – EJ BESTÄLLD, EJ KÖRD

**Mekanism att skilja:** Är den tidigaste P1-kopian verkligen HBLANK-clampad till \`x43\` och fri att röra endast när dess **effektiva reset + START** faller efter HBLANK, eller är den första observerade bildkopian beroende av en redan lagrad/c28-nära START som gör även en sen första RESET visuellt verkningslös?

**En enda separat framtida två-originalmaskers källgeometri** skulle kunna jämföra två lägen i samma niolins-raster med **NUSIZ1=$01, första RESP1 vid c21 (före HBLANK-slut) respektive c23 (just efter), första GRP1 omedelbart efter, andra RESP1 HÅLLS vid c32 (inte c28), andra GRP1 före nästa close-START**, och en gång vardera index0=large_male, index1=large_female, båda samhöjd. De övriga fyra androiderna skulle **inte** omfattas av denna mycket smala hårdvaruorsaksdiagnostik. Den föreslagna c32-separationen avsätter tid för första START och 8 pixelclocks innan ny reset (i c23-läge ideal första START CC86, slut CC94; nästa CPU-write c32=CC96). Detta är **endast en feasibility-idé på papper**; verkliga TIA-pipeline- och registerdeadline samt 76-cykelbudget måste omprövas i separat uttryckligt uppdrag, inte antas PASS.

**Förregistrerade separerande möjliga pixelutfall**, i **Stella-crop-X (dubbelupplösning)** enligt snäva modellkalibreringen:
- **Hypotes HBLANK + independent first START:** \`(X0,X1) = (43,99)\` när första reset c21, och **\`(45,99)\`** när endast första reset byts till c23; båda maskernas nio rader orörda, och andra X99 är invariant. Skulle falsifiera en teori om att första alltid är låst till x43 oberoende av efter-HBLANK-fas.
- **Hypotes äldre/konkurrerande START-latch eller reset som dödar första:** \`(43,99)\` i båda lägena, **eller** förlust/fel i första masken efter c23, även om CPU-trap bekräftar c23 och c32. Detta skulle falsifiera den enkla två-oberoende-reset-modellen **för testat schema** men inte varje TIA-arkitektur.

Observera att **c23 är inte testad i F2–F4**, att crop-offset +9 är kalibrerad och exakt \`45\` kan påverkas av hardware +4CC-fas; en faktisk X≠43 med intakt andra X är huvudgrinden, inte en efterhandsjusterad framgångsetikett. Testet kräver **ny separat MAIN V ROM-order** med käll-/cykelpreflight, riktiga Stella-rawbilder, PC/scanline/CPU-traps, full nio-radersmaskjämförelse och mutantnegativer. **Även positivt 2-maskers svar är INTE sex fri-X/Y och auktoriserar INTE nästa utvecklingssteg.**

### 8. NYTT SOURCE-ONLY MOTBEVIS / KANONPROVENIENS: R1ba har vertikalt omvända rasterrader

Detta är **ett nytt konkret fynd från själva redan levererade R1ba ASM + egna auditorn**, inte ur MAIN:s rådgivande korsrapport. Har INTE rättats, byggts om eller Stella-testats.

**Låst mask för \`large_male\`, uppifrån/ned i canon JSON:** \`3C 3C 18 FF 18 24 24 42 42\`. Arkiverad R1ba \`r1ba.asm\` innehåller visserligen denna sekvens byte-exakt i \`MaleRows: BYTE $3C,$3C,$18,$FF,$18,$24,$24,$42,$42\`. MEN på faktiskt exekverat toppband \`R1atAScan0\` används **\`LDA #$42; ... STA GRP1\`** för mannen; på sista \`R1atAScan8\` används **\`LDA #$3C\`**. **Samma felriktning för stora kvinnan**: \`FemaleRows\` börjar top-down \`3C 3C 18 FF 3C 7E 7E 24 24\` men \`R1atAScan0\` laddar \`LDX #$24\` och första överföringen för kvinnomasken är \`STX GRP1\`. R1ba:s P0-proxy visar liknande omvänd ordning i jämförelse med tabellen.

**R1ba:s publicerade \`analyze_600.py\` innehåller uttryckligen \`return [ ... ][::-1]\` i funktionen \`mask(name)\`; därefter används dess **omvända** mönster för \`pts()\` och den rapporterade 600/600-maskmatchningen.** Dess inbyggda assert för man kräver \`[0x42,0x42,0x24,0x24,0x18,0xff,0x18,0x3c,0x3c]\`, **inte** låst uppifrån/ned-canon. Originaltabellerna är bytebevarade, men **deras nio top-down bildrader är inte bevisat bevarade** och källsekvensen visar tvärtom vertikal inversion i den genererade synliga rasterkerneln.

**Konsekvens:** Den historiska etiketten \`600/600 exakt originalmask\` är **inte ett tillförlitligt påstående om spelprojektets låsta TOP-DOWN pixelreferenser**. Den är ett positivt resultat för en **inverterad presentationsreferens**. Även om källornas format/bitmapvärden är intakta och forskningsbilderna/ROM:en är autentiska måste MAIN kontrollera originalorientering mot de nio faktiskt synliga rasterraderna före varje eventuell teknisk kanonacceptans eller vidare basval. Detta orienteringsmotbevis **ändrar inte** att den befintliga R1ba-code-path använder NUSIZ $03-kopior och att tre kopplade X-profiler rapporterats. Ingen ny pixel-/ROM-/CI-körning utfördes i F5 och detta är inte separat oberoende VERIFICATION.

### 9. Beslut till MAIN V och stopp

**Orsak till F4 X0-låsning:** Källor och faktiska bilder ger **stark, reproducerbar** HBLANK/counter-clamp-förklaring till att första RESP1 c18/19/20/21, alla före CC68, ger samma x43. Konsekvent med Stella 6.7.1:s HBLANK-specifika \`resxCounter()\` och Towers tvåstegiga START, men **exakt aktiv copy-start/latchproveniens vid c28-racet är ännu ej isolerad**. Därför klassas detta till \`SOURCE_ONLY_CAUSAL_HYPOTHESIS_WITH_PREDICTION\`, **inte** \`ROOT_CAUSE_FULLY_VERIFIED\`.

**Två oberoende X:** F2 har visat **en** dynamiskt valbar index2-X, R1ba har visat **positionsankare för par** i förberedda tre X/Y-lägen. **Ingenting i dessa källor visar två oberoende originalandroider med varsitt X i samma nio-radersband.** R1ba:s vertikala radinversion är dessutom en ny uttrycklig data-/visuell korrekthetsblockerare för att upphöja dess research-PASS till canon.

**Högst två framtida MAIN-beslut, inte utfärdade här:**
1. **Separat framtida minimal diagnosorder** endast om MAIN vill pröva den i §7 förregistrerade HBLANK/START-latch-prediktionen med två originalmasker på en **ny, isolerad** tekniksond och separat kontroll av top-down-orienteringen. Detta ger även om det fungerar bara delgeometri och skulle kräva ytterligare **nya** auktorisationer för sex-X/Y.
2. **Stanna vid aktuellt R1-schema**, förkasta antagandet att parvis NUSIZ eller blind RESP-cykelsvep löser C01/C04 och öppna istället en **separat MAIN-styrd arkitektur-/användar-waiver-diskussion**. Ingen designwaiver är given och ingen teknisk substitution av originalmasker/antal/planerade objekt får antas.

**STOPP här**. Denna rapport är det enda nya F5-repoartefaktet på en isolerad analysbranch från fryst F4. **Ingen** ny ROM, DASM, Stella, CI, kodändring, R1-F6 eller senare utveckling; **ingen** ändring i tidigare låsta brancher, \`main\`, draft PR #7, Issue #8, GRAPHICS, R2/R4, PAL, mapper eller fullspel. Oberoende VERIFICATION fortfarande STANDBY. **Fullständigt R1 fortsätter BLOCKED / NOT ACCEPTED.**
