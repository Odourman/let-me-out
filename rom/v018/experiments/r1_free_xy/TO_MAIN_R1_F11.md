# LET ME OUT! – ROM DEVELOPMENT II → MAIN V
## R1-F11: FOUR ORIGINAL MASKS / NUMERIC RAM-X P1 START GATE

**Fryst slutrapport:** 2026-11-17  
**Exakt en slutklass:** `F11_SOURCE_ONLY_INFEASIBLE`  
**G0:** **FAIL / HARD STOP BEFORE ANY ROM BUILD**  
**G1:** **NOT RUN**. Ingen ny F11-ROM, ingen DASM, ingen Stella, ingen GitHub Actions/CI, ingen PNG, ingen ZIP, inga ändrade ASM-/buildskript.  
**Full R1:** `BLOCKED / NOT ACCEPTED`.

### 1. Beslutets räckvidd – vad FAIL betyder och inte betyder

En källbaserad, tids- och positionsregistrerad plan som **samtidigt** klarar fyra separata **numeriska** RAM-X, de förregistrerade **exakta fysiska** A/B-positionerna, fyra rättvända hela originalmasker, oförstörd P1-START/GRP1-pipeline och standard-F6 har **inte kunnat etableras vid obligatoriska G0**. Därför förbjuder MAIN V:s uttryckliga stoppregel ett ROM-bygge.

Det är **inte** ett universellt bevis för att ingen Atari-2600-kernel någonsin skulle kunna rita dessa fyra startpositioner. Särskilt visar varken F9 eller den existerande TIA-källläsningen vilka alternativa interna phase-/copy-/HMOVE-raceutfall en *ny* kandidat skulle ge på en verklig Stella-frame. Men ett spekulativt fassvep eller en ROM som bara provar de två förregistrerade formationerna är uttryckligen otillåtet i F11. Ingen av de tillgängliga tekniskt preciserade vägarna ger **en i förväg källstyrkt, numeriskt datadriven 4-START-tidtabell** för A/B. Detta räcker för **G0 FAIL** inom det aktuella uppdraget.

**AUKTORISERAD BAS:** [F11-order](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_V_TO_ROM_DEV_II_R1_F11_FOUR_NUMERIC_X_P1_DIAGNOSTIC_ONE_ROM_AUTHORIZED_2026-11-17.md), innehållsblob `40c0e2be89b148dc3507d8e8b82c7b6e669492d5`; [MAIN:s formella F10-mottagning och F11-beslut](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_V_R1_F10_SOURCE_ONLY_RECEIPT_AND_F11_DECISION_2026-11-17.md), blob `f8bdbe0f3ce9daa01333fbb9d746cd2eaa9cb90d`; [aktuell MAIN-status](https://github.com/Odourman/let-me-out/blob/main/docs/CURRENT_PROJECT_STATE_2026-11-15.md), blob `fc8a6aacb57a62b44b20db9087ff8a28a54f5792`.

**Fryst förälder:** accepterad [F10 SOURCE ONLY](https://github.com/Odourman/let-me-out/blob/ef854d7436f1e1650827e2e19cc1b3d33a17f054/docs/ROM_DEV_R1_F10_SIX_FREE_XY_ARCHITECTURE_SOURCE_ONLY_TO_MAIN_2026-11-17.md), commit `ef854d7436f1e1650827e2e19cc1b3d33a17f054`, rapportblob `4a8c3cc9cf6893699a1fda48152f155d076bd242`. Ny och endast isolerad F11-gren `rom-dev/v018-r1-f11-g0-hard-stop-source-only-20261117`, skapad **exakt** från F10, inte från PR#7 eller main.

**Bevisad primärbas:** [F9 fryst rapport](https://github.com/Odourman/let-me-out/blob/c36982aef770af6cd3f68c2da37b8ed14aee2393/rom/v018/experiments/r1_free_xy/TO_MAIN_R1_F9.md), commit `c36982aef770af6cd3f68c2da37b8ed14aee2393`, innehållsblob `fd54ed338a0b067ee9551b57bc4cadb28c62c842`; det verkliga historiska scriptet [`r1_f9_build.py`](https://github.com/Odourman/let-me-out/blob/c36982aef770af6cd3f68c2da37b8ed14aee2393/rom/v018/experiments/r1_free_xy/r1_f9_build.py) och dess [G0-källpreflight](https://github.com/Odourman/let-me-out/blob/c36982aef770af6cd3f68c2da37b8ed14aee2393/rom/v018/experiments/r1_free_xy/r1_f9_preflight.py), **lästa som text – inte exekverade i F11**. F9 accepterad av MAIN som lokal diagnostik: enda ROM 16 384 byte SHA-256 `6c2585148eb082fb8bc794d664edc4869b18849fcfabb9cada23373d1dc1318b`; 144/144 äkta Stella-råbilder, 12/12 binära X-kontraster. **Tre BINÄRA X** för M/F/SM, inte ens tre fria numeriska X.

**Hårdvaruprovledande källor:** faktiskt lästa, versionspinnade Stella 6.7.1 [`Player.cxx`](https://github.com/stella-emu/stella/blob/6.7.1/src/emucore/tia/Player.cxx), [`Player.hxx`](https://github.com/stella-emu/stella/blob/6.7.1/src/emucore/tia/Player.hxx), [`DrawCounterDecodes.cxx`](https://github.com/stella-emu/stella/blob/6.7.1/src/emucore/tia/DrawCounterDecodes.cxx), [`TIA.cxx`](https://github.com/stella-emu/stella/blob/6.7.1/src/emucore/tia/TIA.cxx) och [`CartF6.cxx`](https://github.com/stella-emu/stella/blob/6.7.1/src/emucore/CartF6.cxx); [Andrew Towers, TIA Hardware Notes](https://www.retroisle.com/atari/vcs/Technical/Hardware/TIAnotes.php); [original 30 Atari-trick](https://github.com/Odourman/let-me-out/blob/main/docs/RESEARCH_30_ORIGINAL_ATARI_TRICKS_2026-11-16.md) och [F5-korrigering av START/RESP-kausalitet](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_V_F5_SOURCE_ONLY_CROSSCHECK_HBLANK_R1BA_AND_30_TRICKS_2026-11-16.md). Ingen av källorna är en ny F11-G1-mätning.

### 2. Förregistrering: fyra EXAKTA originalmasker, nio rättvända rader

Oförändrad `design/NPC_REFERENCE_8x9_masks.json`, Git blob `058800a4c1904d1ff289e7e61b3902aa111ba16d`. **Var och en exakt en gång**, på gemensamt rasterband, oberoende av RAM-läge:

| Top-down rasterrad | Stor man M | Stor kvinna F | Liten man SM | Liten kvinna SF | Gul P0, historisk F9-referens | M0 historisk F9-referens |
|---:|:---:|:---:|:---:|:---:|:---:|---:|
| 0 | 3C | 3C | 00 | 00 | 3C | 0 |
| 1 | 3C | 3C | 00 | 00 | 7E | 0 |
| 2 | 18 | 18 | 3C | 3C | 18 | 0 |
| 3 | FF | FF | 3C | 3C | 7E | 0 |
| 4 | 18 | 3C | 18 | 18 | 1E | 2 |
| 5 | 24 | 7E | 7E | 7E | 3C | 0 |
| **6, fyra olika GRP-värden** | **24** | **7E** | **18** | **3C** | 18 | 0 |
| 7 | 42 | 24 | 24 | 24 | 24 | 0 |
| 8 | 42 | 24 | 00 | 00 | 42 | 0 |

**SM/SF rader 0,1,8 är faktiskt tomma; en tom rad är fortfarande del av den nio-raderskorrekta masken.** Ingen R1ba-felvänd stor figur, ingen vertikal dubblering eller 5/4 Venetian-interleave. M0 och P0-rader är historiskt F9-underlag, inte nya sprites eller nya bilder. Bruna **speglade PF-väggar** i F9 räknas bara som bevarandekrav i F11, inte R3:s högerdörr.

### 3. Fyra NUMERISKA RAM-X och förregistrerad fysisk pixelprediktion

En **korrekt framtida implementering** måste ha t.ex. fyra **hela 8-bitars numeriska** RIOT-positioner `NPC_X0=$A0`, `NPC_X1=$A1`, `NPC_X2=$A2`, `NPC_X3=$A3` på en **ny isolerad** F11-ROM-källa (i F9 var $A2/$A3 gamla frame-/hold-räknare och får inte ärvas som nya X!). Därutöver separata frame-/event-/mask-index. A och B är bara värden i samma framtida ROM, inte separata ROM-profiler.

| Stimulus | Fysiskt begärt X_CC M,F,SM,SF relativt aktiv 160-CC-bild | Förregistrerad screenshot-crop-start vid historisk kalibrering `crop_x=9+2*X_CC` | Förväntad synlig pixeländring |
|---|---|---|---|
| **A** | **[16,36,56,76]** | **[41,81,121,161]** | 4 kompletta M/F/SM/SF top-down-masker |
| **B** | **[19,36,56,76]** | **[47,81,121,161]** | Bara M +3 fysiska CC = **+6 screenshotpixlar**, de andra tre oförändrade |

**Kalibreringen är arv från projektets tidigare F4/F9 screenshotgeometri och måste normalt prövas mot riktig F11-Stella**, men G0 får **inte** justera den efteråt. F9:s första autentiskt observerade faser var `RESP1 c21→crop x39` (motsvarar 15 synliga CC) och `c23→crop x45` (18 CC); **ingen historisk F9-mätning bekräftar 16 CC (crop x41) eller att `c22` skulle ge det**. För F9:s senare kopior var `c32→crop x99` (45 CC), `c33→105` (48 CC), `c48→x195` (93 CC), `c50→207` (99 CC). F11 kräver en ANNAN exakt geometri, inte bara att en tidigare binär väljer två lägen.

En ROM där `$A0..$A3` råkar innehålla A/B men rasterrutinen bara väljer mellan två inbyggda fasta tillstånd **uppfyller inte** orderns datastyrda `NUMERIC_X`. Det hade krävts en konkret generell `X_CC→RESP-cycle/phase/scheduler` med minst fyra individuella tabellerade/förberedda deadlines i RAM eller annat dataflöde och utan att ROM används som skrivbar kod.

### 4. HBLANK- och kopie-START-schemat: exakt varför den enkla modellen faller G0

En NTSC-rad är **228 TIA CC = 76 CPU-cykler**, normalt 68 CC HBLANK +160 aktiva CC. En CPU-cykel motsvarar **3 CC**. För den *F9-beprövade* nära-kopian `NUSIZ1=$01` kan den nominella färdiga bildkopian börja cirka **17 CC efter en effektiv RESP1-räknereset**, men den interna reset-/decode-/START/latch-övergången har kända fasberoenden. `Player::resp()` och `Player::tick()` i Stella 6.7.1 är **separata** operationer: en `RESP1`-CPU-skrivning är inte en bekräftad START. Stella `DrawCounterDecodes` tabell-index 12/28/60 för automatiska close/medium/far-kopior, medan huvudkopian har separat index 156.

**Fysisk källmodell om endast samma close-type används:** för ett önskat synligt start-X blir en idealiserad RESP1-skrivklocka `CC_write≈68+X_CC−17=51+X_CC`. Den kommer bara på CPU:s heltalsmultiplar av 3 CC. Exakt förregistrerade mål ger:

| NPC | Mål-A `X_CC` | Mål-B `X_CC` | Absolut ideal RESP1-CC vid 17-CC close-fördröjning | Ideal CPU-cykel | Krav vid illustrativt heltalsval A/B `c22/23,29,36,42` |
|---|---:|---:|---:|---:|---|
| M | 16 | 19 | A 67 / B 70 | A **22⅓** / B **23⅓** | A c22 ger 66 CC → kräver **18 CC** effektiv latens; B c23 ger 69 CC → **18 CC** |
| F | 36 | 36 | 87 | **29** | c29 ger 87 CC → **17 CC** |
| SM | 56 | 56 | 107 | **35⅔** | c36 ger 108 CC → kräver **16 CC** |
| SF | 76 | 76 | 127 | **42⅓** | c42 ger 126 CC → kräver **18 CC** |

**Källmässig följd:** med **samma close-type, samma konstanta latens ~17 CC och en gemensam HMOVE-förskjutning** kan inte alla fyra fysiska mål ligga på samma CPU-write-gitter. Deras synliga X-rester modulo 3 är `[1,0,2,1]`; en gemensam P1-finjustering ändrar alla rester lika och kan inte göra dem identiska. Den **illustrativa** c22/23,29,36,42-planen skulle kräva *olika* effektiva interna close-latenser `[18,17,16,18]`; F9 har INTE visat en per-kopia datadriven mekanism som väljer dessa latensvärden. Även de tidiga c22/c23 ligger vid/kring HBLANK. Varken Towers eller den lästa Stella-koden ger en trygg förregistrerad enkel linjär transform där dessa fyra individuella fasrester kan garanteras. **Detta är ett källstyrkt hinder för JUST denna F9-baserade same-close-modell, inte ett generellt fysikteorem mot alla NUSIZ-/HMOVE-hybrider.**

**Separat allvarligare renderkonflikt även om ovanstående faser *kunde* kalibreras:** för två 8-breda masker med startavstånd `d` skriver nästa när-kopias `RESP1` nominellt `17 CC` före dess START. Föregående kopia ritar under sina **8 CC**. En *tillräckligt säker* icke-överlappande writepolicy kräver därför inter-start-avstånd `d ≥ 17+8 = 25 CC` om själva RESP1 inte får inträffa medan föregående originalpixel läses. Detta är ett **tillräcklighetsvillkor för okomplicerad pipeline, inte en universell nödvändig gräns för TIA**.

| Övergång | Föregående kopias synliga datafönster | Nästa RESP1 nominellt vid synligt X | Konflikt |
|---|---|---:|---|
| A M→F, d20 | M pixlar **16..23** | **F-RESP x≈19** | Registerreset medan M:s pixel≈3 ritas |
| **B M→F, d17** | M pixlar **19..26** | **F-RESP x≈19** | Reset vid M:s allra första pixel |
| F→SM, d20 | F pixlar **36..43** | **SM-RESP x≈39** | Reset medan F:s pixel≈3 ritas |
| SM→SF, d20 | SM pixlar **56..63** | **SF-RESP x≈59** | Reset medan SM:s pixel≈3 ritas |

I **faktiska** Stella 6.7.1 `Player::resp()`: när `myIsRendering` redan är sant och `(myRenderCounter - Count::renderCounterOffset) < 4`, justeras **det pågående render-countertillståndet** av reset. `Player::tick()` använder ett **enda** `myIsRendering`, `myRenderCounter`, `mySampleCounter` och nollställer dessa när en ny kopie-decode träffas. Det finns inga fyra simultant oberoende 8-bitars P1-grafikklockor. **Alltså är B framför allt en verklig maskförvrängningsrisk och ingen källa bevisar att alla fyra kompletta originalmaskerna överlever.** En senare intern reset efter CPU-write, phase decode eller ett annat NUSIZ-läge *skulle kunna* ändra utfallet, men här saknas den källstyrkta garantin och någon F11-ROM får inte byggas för att gissa räddningsfaser.

**Alternativ kontrollerade men EJ godkända som G0-räddning:** `NUSIZ1=$03` auto-close/medium ger fasta 16/32-CC separationsmöjligheter, inte de begärda individuellt numeriska 20/20/20 (B 17/20/20). Mid-line `NUSIZ1`-byten kan påverka redan aktiv kopia enligt `Player::nusiz()` och kräver egna verkliga exakta register-/START-deadlines. En `HMOVE`-strobe mitt i bandet påverkar alla aktiverade objekts rörelsemaskineri inkl P0/M0 och kan skapa HBLANK-/utdataeffekter; en enda förinställd `HMP1` justerar P1-gruppen, inte individuellt varje copy. VDEL är en datapipeline, inte en fjärde P1-renderingsräknare. Äldre R1ba har fyra stora felvända originalmasker och kopplade X/Y och får inte kopieras. Inget av dessa är en **färdig source-only alternativkandidat** med A/B exakta fyra X, numerisk runtime scheduler och fulla oförändrade masker inom här auktoriserat EN enda ROM.

### 5. CPU-, GRP1- och efterföljande scanline-budget: **cyklerna ensamma är inte fatal FAIL**

För att särskilja timing och faktiskt objekt renderförmåga redovisas en **ILLUSTRATIV, statisk, icke numerisk och EJ GODKÄND** opcodeplan för det **svåraste row6-fallet med fyra olika bitmapbytes**. Den visar varför vi *inte* påstår falskt att fyra `RESP1/GRP1` är omöjligt enbart på grund av summan 76 CPU-cykler.

Anta att `GRP0/ENAM0` uppdateras enligt F9 c5/c10; förladda M till A, F till X, SM till Y. Illustrativa `STA RESP1` 3 cykler, speglade absolutadresserade TIA-RESP-skrivningar 4 cykler, `STA/STX/STY GRP1` 3 cykler och separat `LDA #SF` 2 cykler. Om 4-cykelregisteraccessen korrekt riktas mot RESP1 genom en TIA-mirror, skulle följande *källschema* kunna ge denna **fasta** tabell (inget DASM/Stella har provat spegeladressen i F11):

| CPU-slutcykel efter WSYNC | A | B | Datalatch / källhändelse |
|---:|---|---|---|
| c5 | lika | lika | `STA GRP0` P0 gul |
| c10 | lika | lika | `STA ENAM0` aktiv M0 |
| c12,14,16 | lika | lika | Förladdning `A=M, X=F, Y=SM` med **omedelbara** raddata |
| c19 | lika | lika | 3-cykel paus `BIT ZP` |
| **c22 / c23** | M RESP1 A c22 | M RESP1 B c23 | 3-/4-cykels writevarianten, ej runtime numeric |
| c25 / c26 | M GRP1 A c25 | M GRP1 B c26 | A-registret |
| **c29** | F RESP1 | F RESP1 | 4-/3-cykels registerwriteväg |
| c32 | F GRP1 | F GRP1 | X-registret |
| **c36** | SM RESP1 | SM RESP1 | 4-cykel registerwrite |
| c39 | SM GRP1 | SM GRP1 | Y-registret |
| **c42** | SF RESP1 | SF RESP1 | 3-cykel registerwrite |
| c44 | lika | lika | `LDA #SF`, separat fjärde radbyte |
| c47 | SF GRP1 | SF GRP1 | A-registret |
| **c50** | `STA WSYNC` | `STA WSYNC` | rad0–7, **26 CPU-cykler teoretiskt kvar** |
| **c53** | `JMP + WSYNC` | `JMP + WSYNC` | rad8, **23 CPU-cykler teoretiskt kvar** |

**Kritiskt:** tabellen är **inte** en genomförbar F11-lösning. Den kräver **två prekompilerade fasta instruktionsvarianter** för olika RESP-writeinstruktionslängder och en manuellt vald spegeladress, och **läser ingen av fyra numeriska X för att själv beräkna faserna**. Den uppfyller därför INTE ens ensam F11:s `NUMERIC_X`-grind. Den förutsätter dessutom att c22/23/c36/c42 ger mål-fysiska X och att den inuti föregående aktiva sprite gjorda resetten inte förvränger tidigare GRP-utdata; båda är okontrollerade antaganden. De 26/23 lediga cyklerna **efter sista kopian** kan inte magiskt flyttas bakåt till de låsta **c22→c29 (7 CPU-cykler), c29→c36 (7), c36→c42 (6)**-intervallen. I 6 cykler kan man exempelvis endast göra två zero-page STA; en RAM-numeric lookup, beslut och variabel vänttid kan inte placeras där utan ny före-raster-scheduling. Genom att koda dessa snäva mellanrum som fasta instruktioner får man **åter just en förprogrammerad formation**, förbjuden som `NUMERIC_X`-bevis.

**GRP-pixeldeadline mot de förregistrerade synliga kopiestarterna, enbart i detta illustrativa schema:**

| NPC | A/B `GRP1`-write CPU | Absolut skriven CC (3c) | Förregistrerad START-CC = 68+X | Marginal mellan write och start |
|---|---:|---:|---:|---:|
| M A / B | c25 / c26 | 75 / 78 | 84 / 87 | 9 / 9 CC |
| F | c32 | 96 | 104 | 8 CC |
| SM | c39 | 117 | 124 | 7 CC |
| SF | c47 | 141 | 144 | **3 CC** |

Alla skriver nominellt `GRP1` före nästa start, men en `GRP1`-CPU-trap är **inte** den interna delay-queue-latchens gällande bitvärde vid START. Den sena SF med 3 CC marginal och det föregående RESET-/render-counter-racet är **inte säkert validerade**. Efter WSYNC måste föregående huvudkopia/spökstart inte ritas på nästa rasterrad. F9 hade autentiska pixelbilder som bevisade avsaknad av vit spökbild för **sina tre relativt åtskilda kopior**, inte för den här hypotetiska fjärde kopian.

**Varför ett generellt numeriskt schema också faller G0:** fyra 8-bitars RAM-positioner och en `X→eventtimes`-beräkning i VBLANK är logiskt tänkbar, men ingen framtagen sourceplan visar hur en **resident oföränderlig ROM-instruktionsström** vid c22..c47 kan läsa fyra beräknade vänt-/fasvärden och respektera de snäva 6/7-cykelsintervallen och fyra olika raddata. Det finns varken fyra direkta phase-kontroller i TIA eller källa för en exakt dynamisk zero-overhead per-event-branch. Självmodifierad ROM-kod får inte antas. En full A/B-baserad unrolled profil skulle möjligen rendera två bilder men *strider uttryckligen mot F11:s arkitektur- och NUMERIC_X-villkor*. Att skriva en faktisk kodplan för generella X-värden och låta den valideras före en ny separat ROM-order skulle krävas; en ny F11-variant får inte uppfinnas under detta stopp.

### 6. RIOT och standard-F6: **rymden är inte konstaterat hårt blockerande**, men ger inget START-bevis

- Standard-F6: 16 384 ROM-byte, fyra 4 096-byte-banker, **EN resident bank i taget**, F6-hotspots `$FFF6..$FFF9`, 6-byte reset/interrupt-vektorer `$FFFA..$FFFF`; **128 byte RIOT-RAM** och 76 CPU-cykler/rasterrad. Ingen bankväxling genom P1-raden får antas gratis.
- **Verkligt F9-konto**, i **en** exekverande bank: **3019 program +115 tabeller +6 vektorer =3140/4096**. Aritmetiskt 956 byte kvar (952 om de fyra bank-hotspotadresserna räknas bort för säker layout enligt F10). F9 använde åtta **förkompilerade tre-mask-kernlar** och fyra **byteidentiska** banker. Att bara lägga en fjärde figur plus numeric scheduler ovanpå F9:s 3019 programbytes är **inte visat möjligt** och hade inte uppfyllt ny arkitektur.
- En NY föreslagen uniform 9-raderskernel skulle däremot kunna **ersätta** alla åtta gamla rutiner och ta plats i en enda 4KiB-bank. De cirka 50 källcyklerna i §5 är ett grovt positivt *tidsschema för fasta faser*, **inte** en faktisk ny assemblerbytebudget, eftersom inga F11-källfiler, .lst/.sym eller konkret numerisk scheduler har framtagits. Inget här ger en legitim G0 `BANK_PASS` för den saknade algoritmen.
- **Teoretiskt RAM-schema, inte allokerat:** `$A0..$A3`=fyra individuella numeriska X (4 byte), `$A4`=frame-counter (1), `$A5`=A/B teststeg (1), `$A6..$A9`=fyra planerade RESP-writes (4), `$AA..$AD`=fyra planerade GRP/phase-deadlines (4), `$AE..$B1`=fyra maskindex (4), `$B2..$B5`=FYRA rowmask-stagingbytes (4), `$B6..$B7`=P0/M0 state (2), `$B8..$BB`=PF/WSYNC/diagnos-scratch (4), `$BC..$C3`=8-byte ytterligare arbetsreserv. **32 byte** allokerade i ett **hypotetiskt** intervall `$A0..$C3` är egentligen **36 byte** (inklusive hål), därför betraktas hela `$A0..$C3` som **36 byte reserverat** i en eventuell framtida faktisk layout. `$C4..$FF` kan inte deklareras fritt utan stack- och andra systembehov; att allokera t.ex. 24-byte stack och P0/objektinit lämnar ändå relativt mycket av 128 kvar. RAM är alltså **inte** här bevisat omöjligt; fysiska START-/datafönster förblir huvudspärren.
- **Observera:** 4×4KiB ROM-kopior ger ingen extra P1-graphics-scan-unit eller TIA-fas. Inget F6SC/ARM/DPC, alternativ mapper eller PAL har använts eller auktoriserats.

### 7. Hårda G0-grindar och beslut

| F11 G0-grind i bindande order | Utfall – endast read-only källkontroll | Beslut |
|---|---|---|
| Proveniens, exakt fryst F10/F9, fyra TOP-DOWN-maskar | Alla specificerade källor lästa. M/F/SM/SF-byte rätt, inkl nollrader. Inga ändrade masker. | **PASS (source)** |
| Fyra separata **8-bitars NUMERISKA** RIOT-X, inte F9:s 1-bit modeID | Fyra RAM-adresser kan reserveras, men ingen faktisk sourcealgoritm finns som läser ALLA fyra och översätter dem till registerfaser i de trånga 6/7-cykelsfönstren. Fasta A/B-opcodes skulle strida mot ordern. | **FAIL / NO_NUMERIC_SCHEDULER** |
| A/B exakta **fysiska** X_CC och +3 CC endast M | Mod3/close-copy-gitter kräver flera obestyrkta 16/18-CC START-latenser eller ny NUSIZ-/HMOVE-arkitektur. Första x16 saknar historisk F9-kalibrering, x36/56/76 ryms inte i en konstantfas-modell. | **FAIL / NO_PREREGISTERED_FOUR_X_MAP** |
| Fyra hela originalmasker på nio samma-Y-rader utan latch/wrap/ghost | Tre-mask F9 PASS gäller gles geometri. A:s 20-CC, B:s **17-CC** första gap kräver RESP under aktiva föregående P1-pixlar; Stella 6.7.1 har EN aktiv render-counter som RESP/START kan ändra. Ingen säker TIA-kopiestartskedja är källbevisad. | **FAIL / P1_COPY_START_COLLISION_UNRESOLVED** |
| GRP1 deadlines | En statisk, **icke numerisk** c25/26,32,39,47 tabell kan skrivas på papper, men SF endast 3 CC före START och delayed GRP latch samt retrigger-race är obevisade. | **INCONCLUSIVE / INSUFFICIENT** |
| CPU ≤76, P0 c5/M0 c10, PF brun, WSYNC och nästa rad | Villkorad fixed-timing source-rad c50/c53 **under 76**; däremot inkluderar den **ingen** verklig numeric scheduler eller verifierad P1-latch. | **CONDITIONAL ONLY / NOT G0 PASS** |
| RIOT 128 byte / standard-F6 4KiB resident / ingen bank switch i raster | Källmässigt **möjligt i princip**, men **ingen färdig byte- eller numerisk schedulerlayout** som ärligt kunde valideras. F9:s 8 kodedubbleringar är inte en framtida layout. | **NO HARD RAM IMPOSSIBILITY; NO COMPLETE BANK PROOF** |
| G0 slutbeslut och rätt att gå till G1 | Flera bindande hårda source-/fysikgrindar saknar valid plan. MAIN-order kräver då STOPP. | **G0 FAIL → G1 NOT AUTHORIZED BY THIS RESULT** |

### 8. Formellt RESULTAT, bevisgräns och vad MAIN skulle behöva besluta separat

**`F11_SOURCE_ONLY_INFEASIBLE`** = F11:s auktoriserade *exakt prövade* F10-A-fyra-maskersnumeric-P1-kandidat har ingen uppställd **förregistrerad, sourcefeasible och 76-cykelkompatibel** plan för A/B där fyra kompletta olika originalmasker och P0/M0/PF klarar kopieSTART/GRP-timing. **Ingen ny körbar ROM är byggd.**

Ingen får läsa detta som att tre-F9-binär X-PASS omprövats eller fallerat: F9 är fortsatt fryst och accepterad av MAIN inom sitt begränsade scope. Inte heller får det rubriceras `FOUR_ARBITRARY_X_PROVEN` eller `F11_FOUR_MASK_NUMERIC_X_LOCAL_FAIL` eftersom en verklig F11-ROM **aldrig byggdes eller Stella-testades**. Full R1 är fortsatt `BLOCKED / NOT ACCEPTED`.

**Nödvändigt, men inte auktoriserat, nytt framtida MAIN-val:** antingen (a) beställ ett *separat nytt SOURCE-ONLY* förarbete som härleder en verklig generell numerisk vänt-/phase-scheduler plus fyra originalkopiors interna START-fönster med bevisat input-domain inklusive 16/19,36,56,76 CC, eller (b) om en framtida hårdvarumätning visar att detta kräver objektprioritet, X-separationskrav, ändrat antal/silhuett, annan TIA-kanal eller cartridgeformat: inhämta explicit **användarbeslut** om **den exakta** nya kompromissen. F11 ger **ingen** auktorisation till något av detta. Det enda senare tillåtna "testförslag" i F10 är inte ett undantag från detta stopp.

**HÅRT STOPP EFTER DENNA FRYSTA RAPPORT OCH [Issue #6](https://github.com/Odourman/let-me-out/issues/6)-handoff:** Ingen F11-ROM-variant, inget efterföljande G1, F12, femte/sjätte NPC, annan fas, ROM-/DASM-/Stella-/CI-körning, ändrade F2–F10-källor, grafik, R1ba-fix, ny mapper, PAL, R2/R3/R4, spelkod, PR #7-merge eller E02 oberoende Verification.

**Full R1: `BLOCKED / NOT ACCEPTED`.**
