# LET ME OUT! – ROM DEVELOPMENT II till MAIN V
## R1-F2 Independent X Feasibility: samlad slutrapport

**Datum:** 2026-11-16
**G1-status:** **F2_GEOMETRY_LOCAL_PASS** (en mellanfigur, två små förkompilerade offsets, fem andra fixerade).
**G2-status:** **F2_LIMITED_RUNTIME_SINGLE_X_PASS** (EN 16 KiB F6-ROM, EN oförgrenad tidskritisk huvudkernel, RAM-styrd en-cykels variation i EN figurs RESP1-tid, 32/32 källkorrekta visuella rutor efter korrigerad read-only audit).
**Inte F2_PROFILE_SWITCH_ONLY:** ingen komplett formationskernel växlas, ingen bytekod behöver byggas om när X-läget ändras.
**Full R1:** **BLOCKED / NOT ACCEPTED**; sex individuellt fria X/Y-originalmasker har fortfarande **inte** visats. All evidens är DEVELOPMENT/CI-egenkontroll, **inte** oberoende VERIFICATION.

### 1. Auktorisation, källfrysning och isolering

Aktiv scope endast [MAIN V:s bindande R1-F2-order](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_V_TO_ROM_DEV_II_R1_F2_INDEPENDENT_X_FEASIBILITY_AUTHORIZED_2026-11-16.md), under tidigare diagnostik NTSC v0.18 Issue #6.

- F1-bascommit **ea1c09f865c6ec5e3ecd984138a9631a0fb7c82a** och föregående frysta R1 **b02ee3fe9e1ffe4bd77460ff43263a35e1f544e0** är **oförändrade**.
- Alla nya textfiler och CI-recept är isolerade på branch **rom-dev/v018-r1-f2-independent-x-20261116**. Varken main, PR #7, R3 eller andra faser har ändrats.
- Kontrollen är tidigare dokumenterat fungerande **6B** med sex originalsilhuetter vid fast X. Bas-ROM SHA-256 **36e588b7211be9dfe6afc534117823f6540aa6d3b753c2816a22c5828d0b60b4**. Ursprunglig assemblertext har sha256 **e268cf68c19543083e59b63b65087699ef281ec04c170a3cf624eab90c579012**, vilken F2-byggen hårdkontrollerar efter byteexakt generering från frysta källor. Original-6B, canons maskbytes och F1-evidens har inte korrigerats retroaktivt.
- Canon: design/NPC_REFERENCE_8x9_masks.json (original Git-blob **058800a4c1904d1ff289e7e61b3902aa111ba16d**), typer per explicit index **0=large_male, 1=large_male, 2=large_female, 3=large_female, 4=small_male, 5=small_female**. Fem statiska jämförelsefigurer är index 0,1,3,4,5.
- GitHub Actions Ubuntu 24.04, **DASM 2.20.14.1** (paket 2.20.15~20201109+really2.20.14.1-2), **Stella 6.7.1** (paket 6.7.1+dfsg-1build2), Xvfb, ImageMagick, xdotool, PIL 10.2.0. Standard F6 16 384 byte = fyra identiska 4 KiB-bankkopior; renderer använder bank 0, inga extra TIA-objekt.
- R3:s P1-dörr har **inte** kombinerats med denna kernel.

### 2. F2-G0: 6B-bas och trovärdig automatisk pixelkontroll

Ny äkta Stella-råkontroll från bas-ROM gav **16/16** med:
- sex visuellt separata, källkorrekta originalmasker på samma nio-radershöjd, exakta alla nio rader per index;
- gula P0-spelaren, synligt M0-skott och bruna playfield-väggar;
- Stella debugger **262 scanlines/NTSC** för varje råbild, kontrollerat mot originalets oförändrade debugger-HUD;
- oförändrad y0/rasterhöjd, inga vita ghostgrupper.

**Negativa MUTANT-tester på separata KOPIOR av en autentisk 6B-bild:**
1. En verklig vit pixel från index 2 togs bort i testkopian. Checkern avvisade bilden; maskkostnader **[0,0,1,0,0,0]**.
2. Två extra vita ghostpixlar skapades vid x=1–2 i testkopian. Checkern avvisade bilden; antal grupper steg till **7**.
Båda manipulerade bilderna är uttryckligen märkta **NOT_STELLA**, förvarade endast under MUTANT_NEGATIVE_ONLY i evidensarkivet. De är INTE emulatorbevis. För G0/G1/G2 har ingen syntetisk bild används som positivt resultat.

Reproducerbar strikt per-index/per-rad-kontroll: [r1_f2_checker.py](r1_f2_checker.py). Korrigerad F1-audit [r1_f1_archive_reaudit.py](r1_f1_archive_reaudit.py) har återanvänts som basreferens; dess ursprungliga R1-feltyp len(groups)==sträng har INTE återinförts.

### 3. F2-G1: isolerad individuellt flyttbar X-geometri

Vald enda mellanfigur är **index 2**, den första stora kvinnan. Båda ändringarna gäller **samtliga nio originalrader** och ändrar exakt endast schemat runt hennes tredje RESP1; de andra fem avsedda RESP1-klockorna är oförändrade. Deras observerade sprite-start-X är också **identiska i alla 16 riktiga bildrutor per försök**. Ingen extra indexfamilj/svep startades efter framgången.

| ROM / prov | Planerad tredje RESP1 | Alla sex requested_X i Stella-crop | Alla sex rendered_X i 16/16 råbilder | Status |
|---|---|---|---|---|
| Fryst 6B kontroll | c37 | 43,75,129,183,243,303 | 43,75,129,183,243,303 | **16/16 PASS** |
| G1_M2, -2 CPU-cykler | **c35** | 43,75,117,183,243,303 | 43,75,117,183,243,303 | **16/16 PASS** |
| G1_P1, +1 CPU-cykel | **c38** | 43,75,135,183,243,303 | 43,75,135,183,243,303 | **16/16 PASS** |

X är **900×300-Debugger-cropens pixlar**, två sådana pixlar per Atari TIA-color-clock. Från 6B:s x129 ger -2 CPU-cykler **-6 color-clocks=-12 crop-pixlar** (x117), och +1 CPU-cykel **+3 color-clocks=+6 crop-pixlar** (x135). Y-raderna, masktyp, samtliga vita pixlar, de fem andras X och P0/M0/PF är oförändrade.

Generatorkälla [r1_f2_build_g1.py](r1_f2_build_g1.py); råbildcapture [r1_f2_capture_g1.sh](r1_f2_capture_g1.sh). Byteexakta DASM-byggen:

- G1_M2 F6-ROM 16384 bytes, SHA-256 **6ad0ac15acfb159f1412ca186545e7f9ab684847025dc3b467f82f81ca4792b1**.
- G1_P1 F6-ROM 16384 bytes, SHA-256 **39be11a80342d9881db90054b32717b1f128ffd1040f57e4e1dc918ceeeb38d2**.

De två separata G1-binärerna visar **en begränsad lokalt möjlig positionsgeometri**, men **inte** runtime-variabel eller generell fri-X.

### 4. Verklig registermätning: vald kritisk källrad 05

Precis som F1 är källmaskrad 05 = **Stella scanline 123**, bank 0. Samtliga målvärden nedan ligger under 76-cykelgränsen, men **statiska cykelberäkningar** respektive **faktiskt uppmätta Stella traps** hålls isär.

| Test / RAM-läge | RESP1 för sex kopior (käll-/DASM-cykler) | GRP1 för fyra byten (käll-/DASM-cykler) | F2 verkligt fångad avvikande P1-register |
|---|---|---|---|
| 6B, F1-kontroll | 19,28,37,46,56,66 | 22,40,59,69 | Verkliga sex RESP1 + fyra GRP1 tidigare fångade i F1, frame12/source-row05 |
| G1_M2 | 19,28,**35**,46,56,66 | 22,**38**,59,69 | **RESP1 c35, GRP1 c38, nästa RESP1 c46** |
| G1_P1 | 19,28,**38**,46,56,66 | 22,**41**,59,69 | **RESP1 c38, GRP1 c41, nästa RESP1 c46** |
| G2 runtime, FRAMELO bit2=0 | 19,28,**37**,46,56,66 | 22,**40**,59,69 | **RESP1 c37, GRP1 c40** |
| G2 runtime, FRAMELO bit2=4 | 19,28,**38**,46,56,66 | 22,**41**,59,69 | **RESP1 c38, GRP1 c41, nästa RESP1 c46** |

**Autentiska Stella Debugger-registertraps på samma rad:**
- G1_M2: frame12, scanline123, **RESP1 c35**, bank0, A=$7E, PC efter STA **$F1C2**.
- G1_P1: frame12, scanline123, **RESP1 c38**, bank0, A=$7E, PC efter STA **$F1C4**.
- G2 mode 0: **frame10**, scanline123, **RESP1 c37**, bank0, **X=$00**, A=$7E, PC efter STA **$F1D4**, TIA color clock111.
- G2 mode 4: **frame14**, scanline123, **RESP1 c38**, bank0, **X=$04**, A=$7E, PC efter STA **$F1D4**, TIA color clock114.
- G2 mode 4, fjärde kopian: frame14, scanline123, **RESP1 c46**, bank0, X=$04, PC efter STA **$F1DA**, TIA color clock138.
- GRP1-traps har autentiska skärmar för mellanfigurens **c38/c41** (G1) och **c40/c41** (G2), motsvarande source-byte $7E på rad 05. Registret visas explicit som Dest/STA och cycle i Stella Debugger.
- De övriga fem RESP1-cyklerna och oförändrade P0/M0/PF-writes är bytehärledda från ett isolerat ändrings-delta mot den i F1 redan fullständigt trappade 6B-kontrollen. Ingen falsk uppgift om att alla återtrappats i varje ny ROM.

P0 GRP0 c5 och M0 ENAM0 c10 var autentiskt mätta i F1 och ligger källbyte-oförändrade här. **NUSIZ1=$01** vid Reset är käll-/DASM-kontrollerat, inte felaktigt beskrivet som fångat på en senare frame. HMOVE sker fortsatt under blankning, med tidigare riktig F1-kontroll. PF-väggar och färgregistrering är källmässigt oförändrade; inget nytt PF-write inom maskrad05.

**Pixeldeadline:** sista GRP1 c69, följande WSYNC-skrivinstruktion avslutas statiskt vid **c72/76**, alltså 4 CPU-cykler till fysisk maxgräns i detta schemalagda fall. Det är inte fritt utrymme för sex generella valfria X/Y och ger inte bevis för andra rasterkombinationer. F2:s ändrade tredje/fjärde kopior ryms i samma c72-envelope och har äkta exakta maskpixlar i Stella. ROM- och RAM-praktiken, inte bara teoretisk TIA-budget, är därmed provad för just ett index och två närliggande X.

### 5. F2-G2: EN körbar 6B-ROM med databeroende individuellt X

**En enda kernel**, inte två uppsättningar helt förkompilerade formationer:

- Redan existerande RIOT-RAM **FRAMELO vid $80** ökas varje frame av den ursprungliga programloopen. Under slutet av det oförändrade TopBlank-höjdbandet görs **LDA FRAMELO; AND #$04; TAX** (7 CPU-cykler utanför den kritiska nio-raderskerneln). X blir **$00** eller **$04** för samtliga nio på varandra följande rasterrader i samma frame.
- Direkt efter LDA av den tredje figurens oförändrade originalmaskbyte: **CPX #0** (2 cykler), **BNE *+2** (2 cykler om X=0, annars 3), **STA RESP1** (3), **STA GRP1** (3), **BEQ *+2** (3 cykler om X=0, annars 2), **STA RESP1** för fjärde figuren (3). Branch-target är samma nästa instruktion i båda fallen; en-cykelsskillnaden beror på *verklig 6502 branch taken/not taken*-timing, inte duplicerad ROM-grafik.
- De två komplementära branchcyklerna summerar till **5 i båda lägena**. Tillsammans med CPX blir de **7 cykler**, exakt samma cykelsumma som den tidigare 6B-uppställningens två NOP (4) plus BIT FRAMELO (3). Den tredje RESP1 blir c37 **eller** c38, den fjärde stannar c46, och efterföljande fem kontrollpositioner förändras inte. Samma branchinstruktioner återanvänds på alla nio rasterrader.
- **Ingen ny RIOT-RAM-cell** används. En redan existerande FRAMELO-byte plus X-register räcker för det här begränsade tvålägesprovet. Y-banor/positionsarray för sex figurer finns inte. Kodsekvensen kostar cirka **+23 bytes i 4 KiB-bankens assemblerkod** jämfört med ursprunglig 6B (18 byte branchinstruktioner över nio rader och 5 byte RAM-lägesladdning); ingen andra kernel, ingen ny bankswitch-familj eller extra cart-RAM.

Byggfil [r1_f2_build_runtime.py](r1_f2_build_runtime.py), 32-frame capture [r1_f2_capture_runtime.sh](r1_f2_capture_runtime.sh). **En 16 384 byte F6-ROM, SHA-256 941c943e9000ca062cc5430cf28bcd34ca92beb70257f4dd84109c487b7c3e2b**. Byggd med riktig DASM och körd i Stella 6.7.1. Samtliga 32 bevarade skärmbilder kommer från **samma ROM-exekvering**; ingen reassembly vid byte från X=129 till X=135.

**32/32 korrigerat read-only pixelbevis**:
- Alla sex ursprungliga 8×9-masker, var och en på **alla nio källrader**, pixelkorrekta i **32 av 32** riktiga Stella-bilder: **0 saknade och 0 extra vita masker/ghostpixlar**.
- Index **0,1,3,4,5** står alltid på X=**43,75,183,243,303**. Bara index **2** växlar X=**129** ↔ **135** under runtime.
- Minst **åtta separata fasbyten i samma ROM** genom debuggerns 32 steg; 16 bilder från vardera X-läget, och oförändrad gul P0, aktivt M0, bruna PF-väggar och 262 NTSC scanlines.
- Full **per-frame** tabell över **requested_X[0..5], rendered_X[0..5], typ per index, nio rader, PNG SHA256 och FRAMELO-fas** finns i det korrigerade CI-arkivet/CSV under evidens.
- Tillämpad read-only frameidentifiering: efter Stella Debuggers **frame #10; sedan ctrl+f** visar varje screenshot det **senast färdigrenderade fältet**, medan debuggerns stoppunkt är i nästa frames VSYNC. Den synliga bildens FRAMELO=debugger-frame-label **minus 2**; bekräftat av verkliga RAM/PC/X-skärmar och pixelväxlingsgränser.

Representativa visuella rader (de fem övriga X identiska i samtliga):

| Debugger-framelabel vid screenshot | Antal rutor | Requested och rendered X för index 2 | Sex maskkostnader |
|---|---:|---:|---|
| 11–13 | 3 | 129 → 129 | 0 per mask, nio rader |
| 14–17 | 4 | 135 → 135 | 0 |
| 18–21 | 4 | 129 → 129 | 0 |
| 22–25 | 4 | 135 → 135 | 0 |
| 26–29 | 4 | 129 → 129 | 0 |
| 30–33 | 4 | 135 → 135 | 0 |
| 34–37 | 4 | 129 → 129 | 0 |
| 38–41 | 4 | 135 → 135 | 0 |
| 42 | 1 | 129 → 129 | 0 |

### 6. VIKTIG ärlig CI-korrigering

Första G2-körningen [GitHub Actions 43926447975](https://github.com/Odourman/let-me-out/actions/runs/43926447975) är **RÖD**. Detta **döljs inte**. ROM byggdes korrekt och **alla 32 autentiska rutor samlades in**, men dåvarande r1_f2_checker.py härledde förväntat positioneringsläge från **debuggerns NEXT-frame-label** utan att dra av två. Resultat: **alla 32 råa bitmap-kostnader var redan [0,0,0,0,0,0] och P0/M0/PF/262 True**, medan begärd-position-jämförelsen var **False** i cirka hälften av fallen.

En ren efterhandsanalys av **samma 32 byteriktiga ursprungliga PNG**, utan ny emulator, korrigerar kopplingen till **FRAMELO för den färdigrenderade bilden**. Analysen tar inte bort pixlar, ändrar ROM eller syntetiserar ramar.

- [Korrigerad återskapbar read-only-kod](r1_f2_runtime_reaudit.py), bygger på oförändrade original-PNG och strikt per-index r1_f2_checker.audit_image.
- [NY GRÖN read-only GitHub Actions 43927249076](https://github.com/Odourman/let-me-out/actions/runs/43927249076): laddade ned fryst artifact från **röda** run 43926447975, **verifierade SHA-256 för varenda en av dess 32 råbilder**, och reauditerade **32/32 PASS**, utan att installera/köra Stella eller DASM. Originalets röda status lämnas intakt.
- [Korrigerad per-frame CSV+JSON och SHA-manifest i Drive](https://drive.google.com/file/d/1DqAKKsKgjcF_es28QscTB9_b_YS0Psbf/view), SHA-256 för archivet **dcc2a52b661db1c39f550cc75b9620cff348b41f9eff4b1234fa7efe6ab1f541**. CSV SHA-256 **12de7cde6b9c2547b5497ce874367962fc608e362e1a8f3acba5b67ed2ad7484**, JSON SHA-256 **486306863d113e2783d7f273aa9ec0fb853b8ea82b8928d5c0ab439debc19a8d**.
- En separat oavsiktlig G1-omtrigger på [Actions 43926153813](https://github.com/Odourman/let-me-out/actions/runs/43926153813) slutade tidigt med **Stella GUI-startfel före användbar ny framecapture**. Ingen extra G1-variant eller evidens kommer från den; den genomförda G1-körningen [43926065656](https://github.com/Odourman/let-me-out/actions/runs/43926065656) är grön. Rapporten påstår INTE att alla workflow-runs är gröna.

### 7. Frysta empiriska artefakter, filhashar, reproducerbarhet

Alla GitHub Actions-artefakter nedan har hämtats ned efter körning, deras ZIP CRC kontrollerats, och deras storlek/SHA-256 beräknats lokalt. Överföring till projektets **dedikerade Drivefolder** har metadata-readback för storlek och parent-ID **1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u**.

| Drive-arkiv | Storlek | SHA-256 och innehåll |
|---|---:|---|
| [G0+G1 6B/offsets + mutant-negativer](https://drive.google.com/file/d/1sWmbMhqS2LrsZ-o7dj-B9M4yCEqyukgh/view) | **476 677 B** | **8c5d7a35d9fa5553fcf49c2a792e6f05c891c4e30f631640b56bd917e50bedca**. Genuine Stella 16+16+16, byggda ROM/.lst/.sym, pixel-JSON, mutantprover och PNG-SHA |
| [G2 samma ROM, 32 råbilder + elva verkliga debuggertraps](https://drive.google.com/file/d/1rG35l_rhdit-XfFmAvE3Xq5KOw-cf3So/view) | **531 840 B** | **6f41cbaa38206e86a3671667469bb11ad8c3878ed392ab05ef80c628ba702836**. G2 F6-ROM, assembler, .lst/.sym, 32 PNG, initial/final GUI, skärmbilder för PC/register/CPU |
| [Korrigerad audit-only CI-resultat](https://drive.google.com/file/d/1DqAKKsKgjcF_es28QscTB9_b_YS0Psbf/view) | **5 494 B** | **dcc2a52b661db1c39f550cc75b9620cff348b41f9eff4b1234fa7efe6ab1f541**. 32 per-frame-rader, fulla masker, X, P0/M0/PF/262, hashes |
| [Extra oberoende vitpixel-READONLY CSV](https://drive.google.com/file/d/14OqM9FPt1VSaGmHl37J4qIDiZR-Yh74M/view) | **11 079 B** | **87e7b965ba5f346f0a016add5035c38de461f091c4a387e85fcda4bd02f6b17c**. Separat unionskontroll av oförändrade originalmaskbytes |

Reproducerbart flöde: checkout F2-branchen; med DASM 2.20.14.1 kör build_six_sweep.py och kontrollera 6B-bas-ROM:s SHA, kör r1_f2_build_g1.py och r1_f2_build_runtime.py, jämför alla fyra SHA mot sektion 2/3/5. Ursprungliga autentiska Stella-bilder är arkiverade, och pixlarna kan efterkontrolleras utan emulator med:

    python3 r1_f2_runtime_reaudit.py <nedladdat_original_G2_Actions_zip> --csv audit.csv --json audit.json

För exakt CI-provning: se .github/workflows/v018-r1-f2-g1.yml, v018-r1-f2-g2.yml, v018-r1-f2-readonly-audit.yml. Det senare kör **ingen Stella**, men bekräftar samma faktiska rådata igen efter korrigerad fas.

### 8. Slutbeslut, vad som INTE bevisats, och rekommenderat stopp

**F2_GEOMETRY_LOCAL_PASS** – visat: en enda mellanfigurs 6B-index 2 har tre stabila källmaskkorrekta positioner x117/x129/x135 i separata små ROM; fem andra X orörda.

**F2_LIMITED_RUNTIME_SINGLE_X_PASS** – visat: EN 16 KiB F6-ROM, en enda 9-raderskernel och databeroende branch-timing väljer verkligen index2 mellan x129 och x135 under **samma** 32-frame exekvering med 32/32 originalmasker och fem statiska kontrollfigurer. **Inte F2_PROFILE_SWITCH_ONLY** eftersom samma kernelinstruktioner körs och endast deras branch-tid ändras.

**R1 FULLT = BLOCKED / NOT ACCEPTED.** Detta bevisar **inte** att alla sex androiders X kan styras individuellt i en tillräckligt stor mängd lägen, inte Y för sex, inte korsning/överlapp/samma X, inte 600 stabila frames, inte R3:s P1-dörr samtidigt, inte full T01–T16 och inte oberoende VERIFICATION. CPU-bandets endast 4 statiskt kvarvarande cykler och P1/RESP-kopplingen är mycket verkliga begränsningar. Den positiva mikrofria tredje X:n får inte omtolkas till en generell X-arkitektur.

**Ett möjligt separat nästa MAIN V-uppdrag (inte auktoriserat):** Testa om en **andra** enskild NPC kan ges en enda oberoende tvåläges-X-variabel med befintliga en-kernel-branches **samtidigt** som index2 kan växlas, max två lägen per individ, med samma pixeltest och hårt stopp om kvarvarande 76-cykelbudget eller kopieeffekter faller. Ingen implicit expansion från detta förslag.

**Inga R2, R4, Y-expansion, R1+R3-integration, designwaiver, PR merge, PAL, v0.19, ändrad originalmask eller oberoende VERIFICATION har utförts. R1-F2 avslutas här som en komplett separat utvecklaregenkontroll.**
