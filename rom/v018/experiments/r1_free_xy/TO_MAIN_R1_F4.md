# LET ME OUT! – ROM DEVELOPMENT II till MAIN V
## R1-F4 – Early-Copy Phase Geometry: samlad slutrapport (DEVELOPER_LOCAL)

**Datum:** 2026-11-16  
**Slutstatus:** **F4_INDEX0_PHASE_GEOMETRY_LOCAL_FAIL**, avgränsat till de två uttryckligen auktoriserade första-P1-RESP1-faserna c18 och c21. Båda är **F4_NO_SECOND_X_PHASE_RESPONSE**.  
**Två oberoende RAM-styrda runtime-X-lägen:** **NOT_RUN**, ej auktoriserade i F4.  
**Fullt R1:** **BLOCKED / NOT ACCEPTED**.  
**Bevisnivå:** ROM DEVELOPMENT II:s DASM/Stella/CI-egenkontroll (**DEVELOPER_LOCAL**), ej oberoende VERIFICATION och ej ROM-/speldesignacceptans.

### 1. Auktoritet, exakt branch och frysta beroenden

Bindande [MAIN V:s R1-F4-order](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_V_TO_ROM_DEV_II_R1_F4_EARLY_COPY_PHASE_GEOMETRY_AUTHORIZED_2026-11-16.md), Issue #6. MAIN:s [F3-mottagning](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_V_R1_F3_RECEIPT_AND_PHASE_BLOCKER_2026-11-16.md) har lästs innan kodändringar. Endast en smal R1/NTSC v0.18-diagnostik har utförts.

- **EN ny F4-branch**: rom-dev/v018-r1-f4-early-copy-phase-20261116, skapad **direkt från F3-fryst commit 65cdeb3cd9d6ab120043f8bd2f5a3d1106ff8190**.  
- **F4 kod- och evidensfrysning före denna rapport**: commit **383d0e2f0163270503d010f7f71f55cdc47aac56**. Den fullständiga **rapportcommiten framgår av Github-URL:n och Issue #6:s leveranskommentar** efter rapportskrivningen; ett dokument kan inte innehålla sin egen framtida SHA-256-commit på ett självreferentiellt vis.
- **F3 original kvar oförändrat**: [fryst slutrapport](https://github.com/Odourman/let-me-out/blob/65cdeb3cd9d6ab120043f8bd2f5a3d1106ff8190/rom/v018/experiments/r1_free_xy/TO_MAIN_R1_F3.md). F3 c20 ROM 16 384 B SHA-256 **1ed9cd9f735dcbf4cd2dc731da607d84a9c4f85f3c894a4dbd48d2d3fc50c286**; första RESP1 verkligt c20, renderat index0 x43.
- **F2 fryst oförändrat**: commit **485a6c10047fb9b41e589ac3df724c1bc70f0283**. Ursprunglig F2 runtime-16KiB-ROM **941c943e9000ca062cc5430cf28bcd34ca92beb70257f4dd84109c487b7c3e2b**. Endast F2:s index2 tvåläge x129↔135 har tidigare autentiskt **enindividigt runtime-PASS**.
- **6B ursprungskontroll**: 16KiB-ROM **36e588b7211be9dfe6afc534117823f6540aa6d3b753c2816a22c5828d0b60b4**, nio korrekta rader för sex masker, x **[43,75,129,183,243,303]**.
- **Maskcanon:** design/NPC_REFERENCE_8x9_masks.json, oförändrat Git-blob **058800a4c1904d1ff289e7e61b3902aa111ba16d**. Index0/1 large_male, index2/3 large_female, index4 small_male, index5 small_female. Ursprungsdata är låsta; små har sex synliga rader men exakt samma nio-radiga datablock.
- **F4 source-blobs:** r1_f4_source_preflight.py Git blob **8dda4877d7e3543e51bcd95269ebbe31dd991f62**; r1_f4_build.py blob **be0f55c4c347e915a9c1ad24746e52c7a98359c9**; r1_f4_audit.py blob **710949e90e99004b8a809d356257fd619775d33f**.
- GitHub compare F3→F4 före rapport visar **endast 10 NYA F4-filer** (sex scripts och fyra CI-workflows) i F4-branchen, **0 borttagna/ändrade ursprungliga F2/F3/R1/R3/canon-filer**. PR #7 är kontrollerat **draft, not merged**. Inget i main/Issue #8 ändrades.

### 2. G0 – nio rasterraders SOURCE-ONLY-kapacitetsanalys

**SOURCE_ONLY_FEASIBLE_C18_AND_C21_NOT_STELLA.** Den första source-only CI-provningen [43954048630](https://github.com/Odourman/let-me-out/actions/runs/43954048630) var röd på en felaktig escaped NUL i mitt Git-blob-hash-test; det var inte CPU-geometrins fel och ingen ROM byggdes. Korrigerat, helt **utan DASM eller Stella**, [43954134314](https://github.com/Odourman/let-me-out/actions/runs/43954134314) blev GRÖN. Alla nio rader återges mask- och instruktionsmässigt i filen r1_f4_source_preflight.json i evidens-ZIP.

Den ursprungliga fixed 6B-serien på varje rasterrad, och de två exakt prövade första-fasplanerna:

| Källrad (0-bas) | P0 GRP0 | M0 ENAM0 | C18: första RESP1 / första GRP1 | C21: första RESP1 / första GRP1 | Index1 RESP1 | Index2 RESP1 | Index3/4/5 RESP1 | Sista GRP1 | WSYNC source |
|---:|---:|---:|---|---|---:|---:|---|---:|---:|
| 0 | c5 | c10 | **18 / 21** | **21 / 24** | 28 | 37 | 46 / 56 / 66 | 69 | 72 |
| 1 | c5 | c10 | 18 / 21 | 21 / 24 | 28 | 37 | 46 / 56 / 66 | 69 | 72 |
| 2 | c5 | c10 | 18 / 21 | 21 / 24 | 28 | 37 | 46 / 56 / 66 | 69 | 72 |
| 3 | c5 | c10 | 18 / 21 | 21 / 24 | 28 | 37 | 46 / 56 / 66 | 69 | 72 |
| 4 | c5 | c10 | 18 / 21 | 21 / 24 | 28 | 37 | 46 / 56 / 66 | 69 | 72 |
| 5 | c5 | c10 | 18 / 21 | 21 / 24 | 28 | 37 | 46 / 56 / 66 | 69 | 72 |
| 6 | c5 | c10 | 18 / 21 | 21 / 24 | 28 | 37 | 46 / 56 / 66 | 69 | 72 |
| 7 | c5 | c10 | 18 / 21 | 21 / 24 | 28 | 37 | 46 / 56 / 66 | 69 | 72 |
| 8 | c5 | c10 | 18 / 21 | 21 / 24 | 28 | 37 | 46 / 56 / 66 | 69 | 72 |

**Viktigt:** Alla cykler i denna matris är **SOURCE_ONLY/STATIC**, inte nio separata Stella-traps. En verklig registertrap gjordes på **rad 5, scanline 123**, i vardera ROM, se punkt 5. Sista GRP1 c69 är även faktiskt mätt. WSYNC source-c72 är 4 CPU-cykler före 76-cykelgränsen, men **WSYNC-trappen visar PC efter skrivningen i scanline 124/c0**, så skrivtid c72 är inte direkt synlig som 72 i den ögonblicksbilden.

Detta är **två förkompilerade små instruktionstider i samma ursprungliga nio-raders 6B-schema**, inte två samtidigt aktiva ROM-formationer, två fri-X-kontroller eller en ny renderer.

- **C18:** efter LDA bitmap0 (c12) används BIT FRAMELO (3) i stället för två NOP (4); första STA RESP1 skrivs c18, STA GRP1 c21, två NOP (4) kompenserar före oförändrat andra STA RESP1 c28. F2-index2 sätts till X-reg=0 före kärnan och dess CPX/BNE/BEQ lämnas bytefunktionellt som tidigare, tredje RESP1 c37. Ingen ny branch i förstapartiet.
- **C21:** efter bitmap0 c12 läggs tre NOP (6), första STA RESP1 c21, STA GRP1 c24, därefter **STA RESP1,X på zero-page** (4 cykler) med X=0, för att återställningen av index1 fortsatt ska ligga **c28**. DASM-listan visar opkod **95 11** i exakt **nio** rasterrader. Det är verklig nollsidesindexerad write till samma TIA RESP1 ($11), inte en ny TIA-registeradress, och ingen page-crossing-tidsförskjutning finns i 6502:s zero-page-indexerade STA. Resten av F2:s kernel och P0/M0/PF/hårdvaru-init ligger kvar.
- NUSIZ1 **$01** och HMOVE under redan använd blankning är **källstyrda, nedärvda** från 6B/F2; de har inte separat mätts med nya F4-init-traps. Ingen ändring i originalmaskbytes, gula P0, aktiva M0, PF-väggar, färgdatablock, RAM-arkitektur eller F6-bankkopior.

Den externa [Andrew Towers – TIA Hardware Notes](https://www.retroisle.com/atari/vcs/Technical/Hardware/TIAnotes.php) är en rådgivande förklaring av retriggering och close-copy-start, **inte bevis för den exakta interna orsaken i vår körbara ROM**.

### 3. Exakt EN kompilerad F6-ROM per auktoriserad ny fas

DASM **2.20.14.1** (Ubuntu 24.04 paket 2.20.15~20201109+really2.20.14.1-2), Stella **6.7.1** (6.7.1+dfsg-1build2), Pillow **10.2.0** (10.2.0-1ubuntu1.5), Xvfb/xdotool/ImageMagick. ROM = 4 × 4 KiB byteidentiska standard-F6-bankkopior; kernel bank **0** och ingen ny mapper.

| Binär | 16 384 bytes SHA-256 | F4-fas | Efterföljande fem RESP1 |
|---|---|---:|---|
| r1_f4_6B_I0_C18_I2_FIXED_F6.bin | **d06fa761ddcc4756fbb2b9b2d72bbe49cc4ec5146a04c8e5e4ff8483dfd9f15d** | 18 | 28, 37, 46, 56, 66 |
| r1_f4_6B_I0_C21_I2_FIXED_F6.bin | **fc3e3622e155c3faded0d91e12f2889c24d0c9eb16822bbef58a4d7cdd6d704f** | 21 | 28, 37, 46, 56, 66 |

Båda F4-binärer och kompletta assembler-, DASM-list-, symbolfiler samt originala källskript finns i Drive-ZIP. **Endast dessa två nya 16KiB F4-geometrivarianter byggdes.** Tidiga röda CI-försök var källguard-/GUI-infrastrukturfel, eller samma byteidentiska variant, inte en tredje variant eller en dold annan kernel.

F4:s **förregistrerade linjära X-hypoteser** innan Stella-råbilderna analyserades:
- C18: **[37,75,129,183,243,303]** i 900×300 Stella-debuggercrop.
- C21: **[55,75,129,183,243,303]**.
Dessa härstammar från CPU-skrivfaser och 3 TIA color-clocks/cykel (×2 pixlar/cropcolor-clock). De är **hypoteser**, inte slutsatser om en faktisk fysisk spriteposition och inte framtagna från avläst rendered_X.

### 4. Verkliga 16+16 Stella-pixelbilder och två oberoende maskkontroller

Båda körningarna genererade **16 verkliga, konsekutiva Stella-bilder vardera**, märkta frame 11–26 efter stabil init. För VARJE frame har vi bevarat både:
- ursprunglig **900×300 pixelcrop** från Stella Debuggers spelplans- och HUD-område, helt orörd;
- ursprunglig **1366×900 full debugger screenshot** på samma frame;
- SHA-256 för var och en av de 16 cropfilerna och 16 fullscreenshotsna, samtliga återkontrollerade från faktiskt nedladdade ZIP-bytes.

**Pixelmetod A**, i r1_f4_audit.py: fullständig direkt XY-mängd av alla vita P1-pixlar mot OR-unionen av alla sex originalens 8×9-matriser, med kandidat för index0:s verkliga x0 insökt utan att anta i förväg att det blev x37 eller x55. **Pixelmetod B:** en helt annan kodväg per rasterrad, 336-bits occupancy-integer och xor-bit_count, utan att gruppera vita figurer med ett godtyckligt x-avstånd. Detta hanterar även geometriskt tätt placerade index0/index1 och avvisar white ghosts/klippning. En fysiskt flyttad mask får endast räknas som exakt om **alla nio rader** och hela vita unionen stämmer.

F2:s tidigare källstyrda separata färgkontroller granskar samtidigt gul P0, M0-skott, brun PF till vänster och höger samt Stella HUD **262 scanlines NTSC**. För varje legitim första cropbild gjordes en **separat tydligt märkt SYNTHETIC_NOT_STELLA-negativmutation**: en vit ursprungsmaskpixel togs bort på en KOPIA, och **båda oberoende kodvägarna underkände den**. Mutantbilden är aldrig godkänd som äkta Stella-evidens.

**Exakt matris, samtliga 16 bilder per rad:**

| ROM-kontroll | Förregistrerad modellbegäran X index0 | Verkligt renderade sex X | Exact original white union | 9 rasterrader per mask | P0/M0/PF/262 | Geometriskt resultat |
|---|---:|---|---|---|---|---|
| C18 / 16/16 | 37 | **[43,75,129,183,243,303]** | **16/16**; 348 vita bildpixlar/frame; 0 saknade, 0 ghost | **16/16** på samtliga sex | **16/16 alla** | **NO_RESPONSE** |
| C21 / 16/16 | 55 | **[43,75,129,183,243,303]** | **16/16**; 348 vita bildpixlar/frame; 0 saknade, 0 ghost | **16/16** på samtliga sex | **16/16 alla** | **NO_RESPONSE** |

Båda granskarna återger x0=43 **utan att härleda förväntad position från den verkliga bilden**. Hela den ursprungliga X-vektorn är intakt i båda faserna. Andra fem X står kvar **[75,129,183,243,303]**. Dessa är inte två fria runtime-positioner. Ingen position-PASS har påståtts för de 32 källkorrekta bilderna.

### 5. Autentiska Stella Debugger TIA-register- och 6502-cykelbevis

Varje ROM kördes också i **sex korta, riktade, riktiga Stella-traps**, allt på bank0, frame12, source-maskrad05/scanline123. De kompletterande skärmbilderna är autentiska, oförändrade 1366×900 PNG och har individuella SHA-256. Register A/X/Y och PC är avlästa i debug-HUD. Alla siffror nedan i CPU-cykelkolumnerna är **faktiskt mätta** där angivet, inte enbart statisk kalkyl:

| Registerhändelse | C18: TIA/CPU-skrivning, efter-STA PC | C21: TIA/CPU-skrivning, efter-STA PC | Data |
|---|---|---|---|
| index0 **RESP1** | **c18**, PC **$F1C3**, ColorClk **54** | **c21**, PC **$F1BF**, ColorClk **63** | A=$24, X=$00, Y=$00, bank0, scan123 |
| index0 **GRP1** | **c21**, PC **$F1C5**, ColorClk63 | **c24**, PC **$F1C1**, ColorClk72 | A=$24, X=$00 |
| index1 **RESP1** | **c28**, PC **$F1C9**, ColorClk84 | **c28**, PC **$F1C3**, ColorClk84 | A=$24, X=$00 |
| index2 **RESP1** | **c37**, PC **$F1D1**, ColorClk111 | **c37**, PC **$F1CB**, ColorClk111 | A=$7E, X=$00 |
| sista **GRP1** | **c69**, PC **$F1C7**, ColorClk207 | **c69**, PC **$F1C1**, ColorClk207 | A=$7E |
| **WSYNC** | Efter write PC **$F1C9**, nu **scan124 / c0** | Efter write PC **$F1C3**, nu **scan124 / c0** | Källa före WSYNC = c72, **STATIC_ONLY**; registertrap visar verklig synkronisering, inte c72 i HUD efter write |

F3:s verkliga c20/PC$F1D1-fångst förblir fryst i sin ursprungliga F3-branch/evidens och har INTE retuscherats. Den relevanta fyrpunktssamlingen för första RESP1 är nu 6B c19→x43 (tidigare F1), F3 c20→x43, F4 c18→x43 och F4 c21→x43. I F4 bekräftas dessutom att den närmast följande c28-ompositioneringen **faktiskt hålls konstant** och att slutet av rasterraden har c69 innan WSYNC.

**Avgränsad orsaksbedömning:** Tidig första RESP1 inom intervallet c18/c19/c20/c21 uppträder verkligt vid olika CPU-/TIA-color-clocks, men den pixelkorrekta första ursprungsandroidens mask står kvar vid x43 i just denna NUSIZ1=$01/upprepade RESP1/GRP1-schemakonfiguration. Endast första kopians positionering/rasterfas är därmed blockerad för DENNA enkla metod. **Det är inte bevisat** att alla andra P1-faser, andra index eller annan helt auktoriserad teknik är omöjliga. Exakta interna TIA-kopie-start/retimering har inte isolerats kausalt och får inte benämnas mätt rotorsak. P0/M0/PF och de övriga fem bevarades, snarare än att ett visuellt fel dolde en lyckad flytt.

### 6. Faktisk Drive-leverans, ZIP-integritet, filindex och kryptografiska hashvärden

Alla tre verkliga ZIP:ar är uppladdade till den befintliga dedikerade projektmappen (Drive parent ID **1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u**). Varje fil har lästs tillbaka via Drive-metadata och byteantalet överensstämmer med den faktiskt nedladdade filen; originalzipparna har kontrollerats med Python zipfile.testzip() = **CRC PASS**.

| Verklig ZIP | Byte | Verifierad hela ZIP SHA-256 | Vad den innehåller |
|---|---:|---|---|
| [C18 eget originalpaket](https://drive.google.com/file/d/19ymcYUpqPSGh79x7u3iR1I9DKQWdAxsF/view) | **638 459** | **740f2dee7fcf0f5483ed98b8b59d6b01a98e87480287c8335f28015b5ee3ec46** | 16 äkta crop-PNG, 16 äkta debugger-PNG, 6 äkta TIA-traps, C18 16KiB-ROM, ASM/list/sym, originala per-frame-SHA, oberoende pixelcheck + SYNTHETIC mutant |
| [C21 eget originalpaket](https://drive.google.com/file/d/1UVQxKxuPN3NrlSYOA1mX_tgyHyoXO0gb/view) | **635 922** | **642043a96e1940ec1e286e1b465f2f789874388c886a75ec7ad5e4ceecf9bb8c** | Samma fulla verkliga 16+16+6 evidens för C21, med andra ROM-SHA och separata listningar |
| **[KOMBINERAD slutlig F4-evidens-ZIP](https://drive.google.com/file/d/1ELlpy5rlXrgtW-flmKT7sUpZXKGj3LMJ/view)** | **1 306 370** | **c8585485eeb78cf3fb7c17dd1dbddbc77d17118485232161d9b1c16736dd8c50** | ALLA original från både c18 och c21, 32 riktiga crop + 32 fulla debugger + 12 riktiga traps, båda ROM, source+list+sym, reproduktionsskript, BUNDLE_VALIDATION.json, EVIDENCE_FILE_INDEX.json och MANIFEST_SHA256SUMS.txt |

Den kombinerade ZIP:n innehåller **149 ZIP-poster varav 147 ursprungliga/datafiler listade och SHA-kontrollerade i EVIDENCE_FILE_INDEX.json**. De två separat genererade index- och manifestfilerna är inte självreferentiellt upptagna i sitt eget manifest. **0 CRC-fel, 0 SHA-mismatch** på alla 147 listade filer i en ny fristående Python-kontroll av de faktiskt nedladdade ZIP-bytesen. Motsvarande samlade read-only GitHub Actions [43956223045](https://github.com/Odourman/let-me-out/actions/runs/43956223045) är **GRÖN**, men **hämtar endast redan infångade autentiska screenshots**; den startar ingen ny Stella och räknas aldrig som en separat emulatorverifiering.

### 7. Full CI-transparens – både röda och gröna runs

| GitHub Actions run | Typ | Status och exakt orsak |
|---|---|---|
| [43954048630](https://github.com/Odourman/let-me-out/actions/runs/43954048630) | F4 G0 SOURCE-ONLY | **RED**: eget felaktigt Git blob-NUL i källguard; ingen ROM/Stella |
| [43954134314](https://github.com/Odourman/let-me-out/actions/runs/43954134314) | F4 G0 SOURCE-ONLY | **GREEN**, 9/9 statiska radplaner, inga ROM/Stella |
| [43954442397](https://github.com/Odourman/let-me-out/actions/runs/43954442397) | Första c18-bygget | **RED**: strikt källguard felräknade extra shutdown GRP0/ENAM0 i BottomBlank efter rad08; ingen F4-ROM byggd |
| [43954663819](https://github.com/Odourman/let-me-out/actions/runs/43954663819) | c18-bygget | **RED**: källguard misstagit befintlig efter-kernel LDX #102 för ny X-skrivning; ingen F4-ROM byggd |
| [43954871755](https://github.com/Odourman/let-me-out/actions/runs/43954871755) | Verklig c18 Stella | **GREEN som diagnostisk exekvering**, 16/16 faktisk oförändrad position, mask/p0/m0/pf korrekt, 6 TIA-traps. **Geometri NO_RESPONSE** |
| [43955212331](https://github.com/Odourman/let-me-out/actions/runs/43955212331) | c21 första kompileringen | **RED**: DASM-listan har TAB mellan STA och RESP1,X, eget alltför strikt strängtest. Den VERKLIGA c21-binären kompilerades och har exakt SHA **fc3e...**, men **inga** Stella-bilder |
| [43955419787](https://github.com/Odourman/let-me-out/actions/runs/43955419787) | c21 samma binär | **RED**: Stella-fönstret hittades inte inom 4s vid Xvfb-start; inga nya riktiga PNG kunde fångas. Inget pixel-Fail klassat |
| [43955699139](https://github.com/Odourman/let-me-out/actions/runs/43955699139) | Verklig c21 Stella | **GREEN som diagnostisk exekvering**, samma c21 ROM-SHA som tidigare, 16/16 oförändrat x43, mask/p0/m0/pf korrekt, 6 TIA-traps. **Geometri NO_RESPONSE** |
| [43956223045](https://github.com/Odourman/let-me-out/actions/runs/43956223045) | Read-only evidence bundle | **GREEN**, laddade ner de två tidigare REAL Stella-artefakterna, kontrollerade deras SHA, bildantal, ROM-hash och paketerade; **ingen ny Stella** |

F3:s [äkta röda G0-pixelrun 43929134626](https://github.com/Odourman/let-me-out/actions/runs/43929134626) ligger fortfarande kvar oförändrad. Tidiga röda F4 CI-runs är inte fysiska mask-Fails och ingen är dolt omklassificerad till grönt. Ingen tredje ny ROM-variant eller annat geometritest har följt.

### 8. Reproduktion, utan ny arbetsauktorisation

Använd **exakt F4-kodfrysning 383d0e2f0163270503d010f7f71f55cdc47aac56** eller den senare rapportcommiten på F4-branchen. Ubuntu 24.04 och angivna DASM/Stella-versioner. Kör från projektroten eller cd till **rom/v018/experiments/r1_free_xy**.

    cd rom/v018/experiments/r1_free_xy
    /usr/bin/python3 r1_f4_source_preflight.py
    /usr/bin/python3 build_six_sweep.py
    printf '%s  %s\n' 36e588b7211be9dfe6afc534117823f6540aa6d3b753c2816a22c5828d0b60b4 dist/r1_individual_6B_F6.bin | sha256sum -c
    /usr/bin/python3 r1_f2_build_runtime.py
    printf '%s  %s\n' 941c943e9000ca062cc5430cf28bcd34ca92beb70257f4dd84109c487b7c3e2b dist/r1_f2_6B_I2_RUNTIME_F6.bin | sha256sum -c

    # Reproducera EN fryst F4-variant i taget. INGEN 2-X-runtime:
    /usr/bin/python3 r1_f4_build.py --phase 18
    sha256sum dist/r1_f4_6B_I0_C18_I2_FIXED_F6.bin
    bash r1_f4_capture.sh 18
    bash r1_f4_trace.sh 18

    # Den andra var endast tillåten efter oförstörande C18 NO_RESPONSE:
    /usr/bin/python3 r1_f4_build.py --phase 21
    sha256sum dist/r1_f4_6B_I0_C21_I2_FIXED_F6.bin
    bash r1_f4_capture.sh 21
    bash r1_f4_trace.sh 21

    # Verifiera raw-bilders SHA i respektive evidence/r1_f4_cXX
    # Pixelklassning finns i STRICT_16_FRAME_PIXEL_AUDIT.json
    # och source-kalkylen i r1_f4_source_preflight.json

**Viktigt:** Dessa är reproduktionsinstruktioner för de REDAN auktoriserade/frysta två diagnostiska F4-proberna, **inte** en ny licens att starta annan variant, två-RAM-runtime, fri X/Y, R2/R4 eller produktionsutveckling. En ny CI-success på återskapade foton är fortfarande DEVELOPER_LOCAL.

### 9. F4:s hårda stoppbeslut och högst två möjliga MAIN-val

**F4_INDEX0_PHASE_GEOMETRY_LOCAL_FAIL**, med **F4_NO_SECOND_X_PHASE_RESPONSE på både c18 och c21**, efter två och endast två nya förkompilerade 16KiB F6-prober. Det har fastställts med 32 originalmask-exakta riktiga Stella-bilder och tolv riktiga tids-/registertraps. En förändrad första CPU-RESP1-fas med bevarat index1 c28 ändrade **inte** en annan androids fysiska X. Detta kan inte kallas en lyckad second-individual geometry, och säger ingenting positivt om två oberoende valbara RAM-runtime-X.

**F4_TWO_INDEPENDENT_RUNTIME_X = NOT_RUN (ej auktoriserad)**. **FULLT R1 = BLOCKED / NOT ACCEPTED**. Sex dynamiska X/Y, andra Y-nivåer, R2/R4/nyckel, R1+R3/P1-portkonflikt, PAL och fullspelet är inte byggda; inget nytt designbeslut/waiver eller nytt testscopetillstånd har införts. Ingen oberoende VERIFICATION har kallats.

**Högst två möjliga separata framtida MAIN-beslut, enbart rådgivande:**
1. Godkänn, endast genom helt ny uttrycklig order, en *source-first* studie av vilken P1-kopia som faktiskt genererar den första synliga androiden när RESP1 c28 och NUSIZ1=$01 är aktiva. Vidare käll-/TIA-analyser får inte antas vara en fungerande lösning eller starta en ny assemblerfamilj utan särskild order.
2. Håll F4 stängd och R1 BLOCKED; be MAIN väga en större R1-arkitekturgranskning eller fortsatt separat research mot den faktiska sex X/Y-acceptansgrinden. Designwaiver är **EJ GODKÄND** utan direkt användarbeslut.

**ROM DEVELOPMENT II: R1-F4 är avslutat enligt den hårda stoppgrinden. Ingen F5 eller senare fas påbörjad.**
