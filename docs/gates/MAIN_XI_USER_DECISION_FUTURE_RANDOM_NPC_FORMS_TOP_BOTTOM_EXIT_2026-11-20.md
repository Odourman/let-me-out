# LET ME OUT! – MAIN XI: uttryckligt användarbeslut om slumpade NPC-former och dörr i över-/undervägg

**Datum:** 2026-11-20  
**Beslutsstatus:** `APPROVED_FUTURE_DESIGN_TARGETS_ONLY`  
**Typ:** Senare, direkt uttryckligt användarbeslut som ersätter äldre designkrav **endast** i de två nedan angivna delarna.  
**Gäller:** framtida fem-NPC-version och framtida kart-/dörrutformning; **inte** en automatisk V02-kodändring, multiroom-cutover, ny implementation gate eller verifierings-PASS.

## 1. Direkt användarbeslut och exakt tolkning

Användaren beslutade i MAIN XI:

> "Ja, låt oss **ändrar det framtida spelkravet till fem individuella fiender vars utseenden väljs oberoende och slumpmässigt bland de fyra originalmaskerna, så att även fem män eller fem kvinnor kan förekomma.**"
>
> "Och vi ändrar på dörren och dörröppningen också. Dörr placering kan variera mellan upppe och nere beroende på karta. Det borde vara lättare än att ha dörren till höger?"

Första stycket är ett uttryckligt godkännande av en **ny framtida spritefördelning**. Andra stycket är ett uttryckligt godkännande av **övre respektive nedre ytterväggen som alternativ dörrplacering efter karta** och av att framtida utgången inte längre behöver vara på höger yttervägg. Den sista meningen är en teknisk hypotes/fråga, **inte** ett bevis på förenkling eller en implementation-/emulator-PASS.

## 2. Fem individuella NPC; visuellt utseende väljs per individ vid rumsstart

- Alltid exakt **fem logiskt individuella** fiender per rum. Var och en väljer **oberoende** en av fyra oförändrade original `TOP-DOWN` **8×9-masker**: `large_male`, `large_female`, `small_male`, `small_female` i [originalmaskfilen](../../design/NPC_REFERENCE_8x9_masks.json).
- Kombinationer med fem manliga, fem kvinnliga, fem av samma mask och blandningar av varje slag ska vara tillåtna. Den tidigare **fixa** visuella instanssammansättningen **M, M, F, SM, SF** enligt [G5S LM-D14/C1](G5S_MAIN_VII_C1_D1_E1_USER_APPROVAL_DECISION_RECORD_2026-11-17.md) och [G5Q LM-D12/13](G5Q_MAIN_VII_A1_B1_USER_APPROVAL_DECISION_RECORD_2026-11-17.md) ersätts **endast** för framtida rummens fördelning av visuella former.
- Naturlig implementationstolkning av "slumpmässigt bland de fyra" är lika chans för varje mask (1/4 per individ), med fem oberoende val; detta är en explicit teknisk standardtolkning för testplanering, inte en annan av användaren separat uttalad sannolikhetskvot. Ingen fast kvot mellan kön/storlekar per rum. Nytt urval sker vid faktisk ny rumsstart; individuellt utseende **förblir stabilt under samma rum**. Kontrollera RNG-utdelning och oberoende i implementation, inte bara `random % 4` utan källgranskning.
- Varje individ behåller sina egna logiska X/Y, jakt/riktnings-AI, NPC-kollision, skjut-/död-/livs-/poängmekanik. **Samma logiska kollisionsruta oavsett grafisk mask**, enligt ursprunglig Master Spec. Ingen ny mask, rotering eller visuell maskändring har godkänts.
- [LM-D16/E1](G5S_MAIN_VII_C1_D1_E1_USER_APPROVAL_DECISION_RECORD_2026-11-17.md): exakt en av de **fem individerna** får nyckeln med **1/5 sannolikhet per individ**, oberoende av vilket utseende hen råkat få; nyckelbärardöd och nyckelfall regleras oförändrat. [LM-D15/D1] -30/kill och övriga poängregler oförändrade.
- Rendering ska prövas mot *vald originalmask per individ*, inklusive fembandiga/same-Y-, täta-X-, spelare-, key-, dörr- och skottfall. Att omfördela små/stora masker för att förbättra renderingsbudget får inte ske på bekostnad av individernas verkligt slumpade utseenden.

## 3. En enda orange utgång i övre eller nedre ytterväggen per karta

- Varje rum ska fortfarande ha **exakt en giltig ytterutgång**, med **orange låst dörr och svart utskuret nyckelhål mot svart bakgrund**. Ingen ytterligare öppning som kan användas som utgång eller sidodörr införs.
- För den **framtida** fyra-rumsdesignen kan dörren och dess öppning ligga i **övre eller nedre ytterväggen**, med placering beroende på vilken karta som används. Den tidigare bindande **högerdörren** i ursprunglig [Master Spec](https://drive.google.com/drive/folders/1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u) och beslutsregistret (särskilt originalbeslut **016, 017, 018**) samt senare "höger orange dörr"-mål är genom detta uttryckliga användarbeslut **supersederade enbart vad gäller framtida dörrsida och nödvändig placering av utgångsöppningen**.
- Vägg/öppning/dörr måste fortfarande faktiskt visa den **enda** orange dörren låst, ett synligt svart nyckelhål som **frånvaro av orange grafik**, dörrens försvinnande vid upplåsning och en synlig, navigerbar öppning som spelaren **fysiskt måste passera** för rumsexit. Androider kan blockera men får inte lämna rummet; utan nyckel ingen passage. Bakgrund fortsatt svart; playfield-väggar bruna, spelaren gul, NPC vita, nyckeln guld.
- En **centrerad** öppning på övre eller nedre väggen är **rekommenderad testhypotes**, eftersom TIA:s `CTRLPF` speglar vänster/höger, men användaren har inte här bestämt exakt X, öppningsbredd, dörrformat, per-karta-top/bottom-fördelning eller nya kartfingeravtryck. Dessa måste specificeras i versionssatta framtida kartvarianter och kontrolleras mot faktisk kollision, tillgänglighet och design innan produktionscutover. Dörrens placering är **kartberoende, inte slumpad varje besök** utan nytt beslut.
- De fyra tidigare godkända framtida kartidentiteterna **A_OPEN_01, B_OPEN_02, C_OPEN_01, D_OPEN_01** och deras interiöra väggprinciper är fortfarande designbas; deras frysta exakta tidigare **högerdörrs-grids** är historiska, inte automatiskt geometriskt identiska med nya topp-/bottenvarianter. **Modifiera inte originalfilerna eller ge nya koordinater samma gamla hash/ID.** Framtida kartvarianter behöver tydligt versionssättas och få exakt geometri/acceptans.
- Startpunkt på vänster sida och övriga originalregler ändras **inte** av detta beslut. Möjliga behov av nya rutt-/spawn-/utgångskollisionskontroller är implementation och får mätas i tekniska prov.

## 4. Teknisk rekommendation, inte påstått hårdvaru-PASS

Den faktiska V02 X71-ROM:en `a1b4449fe92fb8045f6f88f040c7f94be03e2ffb` använder `CTRLPF=$01` och speglad playfield. En centrerad topp-/bottenöppning kan formas med symmetriskt avstängda PF-bitar, som blottar svart `COLUBK`, och kan därför minska den **asymmetriska sidodörrens** krav. Det betyder **inte** att ett pixel-exakt litet nyckelhål (4 colorclocks per PF-bit) eller orange dörr medan resterande PF är brun redan fungerar. Horizontal PF-kolorering med `COLUPF` och eventuella P0/P1/M0/M1/BL-resurskonflikter kräver faktisk 6507/TIA-register-/cykel-/färgmätning. Topp/botten eliminerar inte automatiskt key+player eller fem-NPC-same-Y-FAIL.

**Föreslagen nästa tekniska åtgärd under redan stående LM-D29/LM-D30 testtillstånd:** parallella **test-only** F6/NTSC-varianter i befintligt Issue #31, en centrerad övre och en centrerad nedre dörr, jämförda mot fryst X71 med original orange/svart cutout, full fem-NPC-, nyckel-/spelar-, dynamisk PF- och riktig rumsutgångskontroll. Dokumentera marginaler och negativa utfall, välj inte cutover utifrån teori. Håll varje tidigare fryst ROM och exakta väggfixturers historiska orakel intakta; test av ändrad dörrgeometri måste ha nya explicit definierade pixel-/kollisionsorakel och kan inte krävas att matcha gamla högerdörrspixlar.

## 5. Auktoritetsgräns och pågående arbete

- **Godkänt nu:** framtida **designkrav** enligt avsnitt 2–3. MAIN får beställa tekniktester/test-ROM:ar av övre/nedre dörr inom LM-D29/LM-D30 utan ny personlig testauktorisation.
- **Inte automatiskt godkänt:** att tyst överföra nya designregler till befintlig fryst spel-ROM eller ändra en redan mottagen checkpoint; att ändra **fler** gameplayregler eller öppna en **senare implementationetapp/V03, G6/F12, fyra rum i skarp ROM, PAL-/mappercutover, PR-merge, release eller oberoende Verification**. Nytt versionssatt implementationsscope måste uttryckligen hållas inom den befintliga V02-gränsen eller få separat tillstånd för senare steg.
- Tidigare avgränsade V02-arbetsorder i [Issue #31](https://github.com/Odourman/let-me-out/issues/31) och X71-granskningen bevaras. Det nya designbeslutet innebär att framtida **högerdörr inte längre är ett bindande slutmål**, men den oförändrade gamla höger-implementationen är en viktig reproducerbar regressionreferens fram till uttryckligen auktoriserad ändring i spel-ROM.
- **`G5_FORMAL_OPEN`, `INDEPENDENT_VERIFICATION=NOT_RUN`**; ingen emulator-/rom-/grafik-PASS följer av detta dokument.
