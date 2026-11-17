# LET ME OUT! – MAIN VII G5Y: falsifierbar teknisk testordning efter fastslagen framtida fyrkartsdesign

> **HISTORISK FÖRREGISTRERAD PLAN (G5Y).** Vid planens skapande var G0 inte auktoriserad; detta **har senare ändrats** genom LM-D20: endast G0 H4-ONE source-only beställdes och är redan **avslutad `G0_INCONCLUSIVE_NO_ROM` i G5AA**. Matrisen dokumenterar planerade scenarier, inte att 17 fall fysiskt utförts; ingen G1/G6/F12/ny ROM är auktoriserad. Se [aktuell status](https://github.com/Odourman/let-me-out/blob/main/docs/CURRENT_AUTHORITY_STATUS_AND_WORK_QUEUE.md).

**Datum:** 2026-11-17. **Status:** `G5Y_TECHNICAL_TEST_PLAN_READY_SOURCE_ONLY_NO_NEW_TEST_AUTHORIZATION`.
**Arbetets omfattning i denna MAIN-chatt:** söka och jämföra nuvarande original-/teknikkällor, välja en **testordning som förslag** och förregistrera tester med stoppvillkor. **Ingen** assembler, DASM-kompilering, ROM, Stella-fysiktest, G0 som faktiskt utfört experiment, G6/F12, PR-merge, nytt tillstånd till en specialist, nytt gameplaybeslut eller oberoende Verification har skett.

## 0. Autoritet: vad är beslutat och vad är bara historiska tester?
- [G5X senare användarbeslut LM-D19 + framtida 4 exakta rum](G5X_MAIN_VII_B_OPEN_02_EXACT_USER_APPROVAL_AND_FOUR_MAP_BASELINE_DECISION_2026-11-17.md), [källpinnat fyrkartsmanifest](G5X_MAIN_VII_APPROVED_FUTURE_FOUR_MAPS_SOURCE_MANIFEST_2026-11-17.json). **Framtida exakta kartlayouter**: `A_OPEN_01`, `B_OPEN_02`, `C_OPEN_01`, `D_OPEN_01` (giltiga layoutmål, inte ROM-byggen).
- [LM-D12/D13: G5Q fri X/Y, identifierbara synliga hot](G5Q_MAIN_VII_A1_B1_USER_APPROVAL_DECISION_RECORD_2026-11-17.md), [LM-D14/D15/D16: G5S fem NPC, −30/kill, fem validerade starter och 1/5 carrier](G5S_MAIN_VII_C1_D1_E1_USER_APPROVAL_DECISION_RECORD_2026-11-17.md). R1-fem `M,M,F,SM,SF`, R2-fyra+key **framtida scope**; historiska v0.18 sex/fem+key och tidigare negativa tester är frysta. Originala fyra TOP-DOWN 8×9-masker i `design/NPC_REFERENCE_8x9_masks.json`, blob `058800a4c1904d1ff289e7e61b3902aa111ba16d`.
- [K1/E1 händelseprioritet](../APPROVED_EDGE_CASE_DECISIONS_K1_E1_2026-11-15.md), [O1/LM-D06](../MAIN_STATUS_NEXT_10_2026-11-15.md): nyckel får skymmas tillfälligt **endast vid faktisk NPC/key-bitpixelöverlapp**, inte på grund av enbart samma Y; ingen generell 10Hz- eller osynlighetswaiver.
- [G3 samlat R1–R4-resurskontrakt](G3_RESOURCE_CONTRACT_COMPLETION_RECEIPT_2026-11-17.md), [G2 NEGATIVA teknikhistorik](G2_NEGATIVE_TESTS_AND_NONREPEAT_RULES_2026-11-17.md), [F11 fryst G0 FAIL](../MAIN_V_R1_F11_G0_FAIL_SOURCE_ONLY_RECEIPT_2026-11-17.md), [G4 H4-ONE original förregistrerade fysiska hypotes](G4_PREREGISTERED_PHYSICAL_HYPOTHESIS_2026-11-17.md), [G4 single-test draft, EJ beordrad](G4_FUTURE_SINGLE_MICROPROBE_ORDER_DRAFT_NOT_AUTHORIZED_2026-11-17.md), [G5H source-only 79/76 och 74/76 worst-case](G5H_START_GRP_RESP_NUSIZ_SAME_Y_SOURCE_ONLY_DECISION_2026-11-17.md), [G5L stress S05, door/key](G5L_FINAL_TECHNICAL_EXIT_30_TRICKS_R1_R2_DOOR_KEY_AND_USER_DECISION_2026-11-17.md), [G5P reproducerad rådgivande AI-test](G5P_MAIN_VII_RESEARCH_DELIVERY_INTAKE_AND_REPRODUCTION_2026-11-17.md).
- [Färdig 17-cases **ENDAST förregistrerad** testmatris](G5Y_MAIN_VII_PREREGISTERED_TECHNICAL_TEST_MATRIX_NOT_AUTHORIZED_2026-11-17.csv). Samtliga rader `NOT_RUN`, ingen falsk G0/G1 PASS.

## 1. Tekniskt dilemma som måste lösas före ny beställning
**Två tidigare konkurrerande försökidéer är INTE utbytbara.**

1. **G4 H4-ONE** (ursprungligt preflight-huvudspår): **samma** nio synliga rasterrader med `P0` gul fullstor diagnostisk player + vit original-M i **båda X-ordningarna**, `P1` vita original-F och SM, **EXAKT EN** aktiv M0 på SAMMA rad i icke-overlap positivfallet, **riktiga bruna PF-väggar**, samtliga positioner separat numeriskt RAM-X. NTSC standard F6, 76 CPU-cykler/scanline, 128-byte RIOT med stack, 4KB aktiv bank och nio korrekta maskrader. Förreg A1/A2/B1/B2, negativ X1/X2, M1/P1 och minst två hemliga efter-frysning numeriska X-par.
2. **G5P:s senare *snävare* idé** nämnde endast `P0 yellow player + P0 white NPC + M0 + PF` som första isolering. Det kan vara en diagnostisk **N0-kontroll** för retrigger-/M0-problem, men ett sådant `N0` kan inte räknas som `H4-ONE_PASS` eller bevisa två `P1` originalmasker. **Det får inte väljas i smyg som ersättning för H4-ONE** efter att användaren godkänt fem fiender/fri X/Y.

**MAIN VII:s lösning för framtida planering:** bevara H4-ONE som **en enda fullständig falsifierbar primitiv** för ett eventuellt senare uttryckligen beställt microprobe. Vid en framtida begränsad source-only G0 kan ROM DEVELOPMENT III använda N0 som **intern analytisk deldiagnostik**, men den får varken försena obestämt eller sänka H4 acceptance. Detta innebär **ingen ny faktisk implementation**. Ett fullständigt H4 G0-FAIL innebär `NO_ROM`; om N0 råkar fungera är det fortfarande inte H4-PASS. S05 är ett annat senare separat test, inte något H4-PASS magiskt täcker.

**Varför full H4 återstår som huvudprov:** F11 G0 FAIL avsåg **fyra numeriskt oberoende original-P1-X** i F10:s familj; det bevisar INTE att tvåfönsters P0+tvåfönsters P1 är möjligt eller omöjligt. G4 bygger på historiska R1f/R1g och F9 **från olika kernel-/ROM-familjer**, vilket inte gör en sammanfogning redan bevisad. Därför först källpreflight, sedan mycket avgränsad fysisk falsifiering.

## 2. Föreslagen teknisk ordning med separata faktiska tillstånd
| Etapp | Fråga och krav | Får påbörjas nu? | PASS-betydelse och stopp |
|---|---|---|---|
| **G5Y, MAIN planering** | Original- och riskavstämning, 17 preregistrerade fall, falsifieringskriterier | **Ja – utförd nu source-only** | `G5Y_PLAN_READY`, aldrig ROM PASS |
| **Föreslagen G0 source preflight** | H4-ONE komplett cycle/CC/GRP/RESP/PF/M0/numerisk-X-konstruktion på papper/källnivå, **ingen binär** | **NEJ – kräver egen senare uttrycklig auktorisation** | `G0_SOURCE_PLAUSIBLE` eller `G0_FAIL_NO_ROM`; ett litet N0-PASS får inte upphöjas till H4 |
| **Föreslagen G1 fysisk mikro** | **En** standard-F6/NTSC ROM om G0 är faktiskt rimligt, rätt P0/P1 mask+color+PF+M0 på samma Y med verklig Stella/raw-pixel/cykelspårning | **NEJ – kräver separat uttryckligt beslut även efter G0** | `H4_MICRO_PASS_BOUNDED` / `FAIL` / `INCONCLUSIVE`. Ingen full fem-NPC-arkitektur verifierad |
| **S05 separat integrationstest** | Gold key + white NPC + yellow player + orange P1-door + M0/PF samma rasterhöjd, både 13 bitpixelöverlapp och 0 bitpixelöverlapp | **NEJ – kräver egen scopeauktorisation senare** | O1 gäller bara verklig överlapp; ej kombinerbar med full H4/P1 vit på samma raster automatiskt |
| **Fem-NPC 8×9 och framtida fyra rum** | Fem fria logiska X/Y, dynamiska same/shifted-Y, kollisionsfri 8×9 spawn, 1/5 bärare, K1/E1, PF/map/door, femfiendersscore | **NEJ – separat ROM/gameplay-scope krävs** | Ingen G5/full R1/R2/R3/R4 PASS utan fungerande ROM och oberoende Verification II |

**G0 innebär inte automatiskt G1**, och G1 innebär inte automatiskt S05/G7, M8 eller en full ROM. Utan ny användarauktorisation ska inga av ovanstående tekniska etapper beställas till ROM DEVELOPMENT III via GitHub Issue, chatt eller PR.

## 3. G0 source-only gate: vilka underlag måste finnas före *ett enda* binärbygge?
En framtida ROM-specialist ska då (endast efter separat användarorder):
1. Pin frysta källor/utfall (F11 negative, R1f/R1g/F9/R3, G4-timeline, originalmask). Markera gamla `NOT CALCULATED` som öppna – aldrig byt till gissade värden.
2. För exakt H4-A1/A2/B1/B2 och nio TOP-DOWN-rader: instruktion-för-instruktion `PC/opcode/cycles/branch/page-cross/write end CPU c`; koppla till **faktisk TIA `START`/GRP-latch/colorclock-deadline**, inte bara `X≈3c`. Beräkna värsta rad **inklusive `WSYNC`** och förberedda/nödvändiga registerväxlingar. **Alla** rader `<=76c`; förväntat CC-utfall ska vara falsifierbart.
3. Dokumentera `NUSIZ0` och M0-replikationsinterferens: **bara en** M0 aktiverad på originalmaskbandets faktiska rasterrad, aldrig M0 på y−1 som falsk positiv. Kontrollera P0 retrigger vid **omvänd** X-ordning och vid kritisk aktiv bitmap.
4. Visa `P1` F/SM med alla nio originalrader inklusive SM:s nollrader, inga byte-speglingar, inga omritade masker, ingen duplicerad M0 via NUSIZ. Gul P0 diagnostisk spelare är fortsatt tillåten inom just den begränsade mikron.
5. Brunt PF måste vara **faktiskt närvarande på vänster och höger kant på samma Y**. Förladdat PF godtas endast om just **den valda** 9-raderszonens registrerade väggdata är konstant och originellt källspårbar; kan inte anta att historiska C02/R3-PF-skrivtider gäller A_OPEN_01/B_OPEN_02/C_OPEN_01/D_OPEN_01. **H4 kan använda isolerat verkligt PF-väggband som jämförbar G0-kontroll men får då inte kallas fullgodkänd ny rumskarta.** Översätt senare 40×22-grid till TIA:s 160 synliga CC, 40 PF-bits, ungefär 4CC/cell och 8 scanlines/cell som separat **kart-PF-hypotes**, inte genom att kalla en offlinebild fungerande ROM.
6. Specifik budget: 128B RIOT RAM inklusive stack, instruktions-/tabellplatser i aktiv 4KB F6-bank, bankbyte under en rad (om aktuellt), datastyrd X-sort av individers separata numeriska RAM-koordinater, tidsförberedelse före första pixel och reell färgkoppling `COLUP0` P0+M0, `COLUP1` P1+M1, `COLUPF` PF+BL.
7. Skilj fysisk testgeometri och logisk fem-NPC-kollision. Den mikro som har två P1-original är **FYRA bitmappaktörer totalt** (player, white M, white F, white SM), inte fem vita NPC. Den är ett nödvändigt eller nyttigt *delbevis*, **inte** tillräckligt fullspelsbevis.
8. **Hård stopp** om en fullständig plausibel schedule inte kan hittas utan att dra av PF/M0/P1, ersätta fri numerisk X med four-mode-LUT, felvända/komprimera maskerna, göra 8×18 2LK, överstiga 76c eller förutsätta dolda/försvunna fiender.

`G0_SOURCE_PLAUSIBLE` är en källbedömning, inte ett "physical PASS". `G0_FAIL_NO_ROM` ska leverera blockerarrapport, utan att försöka flera okända ROM-varianter i samma order.

## 4. H4:s förregistrerade positiva och negativa testfall
Se [testmatrisen](G5Y_MAIN_VII_PREREGISTERED_TECHNICAL_TEST_MATRIX_NOT_AUTHORIZED_2026-11-17.csv). **Identifiera alltid test-ID med prefix `G4-`** så `G4-A1` inte förväxlas med **LM-D12/G5Q A1**.

- **`G4-A1`**: `player=40, M=104, F=68, SM=132, M0=24` synliga TIA-CC-mål (P0 gul→vit).
- **`G4-A2`**: `48,96,72,128,24` (nytt numeriskt avstånd).
- **`G4-B1`**: `104,40,68,132,24` (P0 vit→gul).
- **`G4-B2`**: `96,48,72,128,24` (omvänd ordning, annat avstånd).
- **`G4-X1` NEGATIV**: M0 X43 mot original M rad3 `11111111` X40..47 med begärd **annan** testfärg. Under samma fysiska `COLUP0` ska två olika färger **inte** få hävdas som möjlig samtidig slutpixel. Detta är konkret kanal-/färgnegativ, inte generell omöjlighet för alla arkitekturer.
- **`G4-X2` NEGATIV/SKARP**: P0 white M vid X40, gul player vid X44; risk för `RESP` under aktiv rendering och bitmapklippning. Inget implicit synlighetsavsteg.
- **`G4-M1`** en M0 i faktiska samma Y och källdeklarerad `NUSIZ0`-kopiepolicy.
- **`G4-P1`** två separata TOP-DOWN P1 original-masker F och SM (inklusive nollrader), inte EN P1-only-profil.
- **Två efter-frysning numeriska RAM-X-par** väljs av MAIN/oberoende granskare **först efter binär-SHA** inom en på G0 före fryst stödbar och uttryckligt definierad domän. **Samma ROM, inga ombyggen**. Actor-identiteter, mönster och övrigas X måste bestå.
- Negativa historiska villkor F11: **fyra fria P1-X** kan inte rehabiliteras utan ny faktisk takt-/fasplan; fyra modeprofilers "pass" är inte numeriskt PASS; fusk med PF=0 eller M0 utanför bandet är inte PASS.

**Evidensmall per fysiskt scenario (om senare beställd):** test-ID, ROM-hash, källcommit, all RAM input, dokumenterad screenshot-crop↔synlig-CC-transform, 262 NTSC-lines där relevant, minst nio korrekt orienterade originalmaskrader, rå GUI/pixlar, debug PC, bank, scanline, `RESP/GRP/COLUP/NUSIZ/M0/PF/WSYNC` cykelposition, observerad startsignal och en genomförd `PASS/FAIL/INCONCLUSIVE` mot *förregistrerade* kriterier. Inte bara bilder från offline-visualisering.

## 5. S05: medvetet separat svart-på-vitt stopprov för full R2/key/door
**S05 har *annan kanalägarkonflikt* än H4**. I door-y äger `P1` orange låst högerdörr inklusive svart genomskinligt nyckelhål som del av samma bitmap. `P0` behöver då potentiellt **gul player, vit original-NPC och gold key** på samma rasterhöjd; `M0` delar `COLUP0`, PF ska fortsätta visa bruna väggar och left-wall/Ball är än så länge en hypotes. Även om H4 lyckas med två vita `P1` bevisar det **inte** denna P1-door + tre P0-ägare.

Två källförankrade **separata** uppställningar måste senare särskiljas:
- `G5Y-S05-NO-OVERLAP`: NPC och key är på samma Y men **0 gemensamma verkliga synliga bitpixlar** → **key måste synas**. Att dölja key för att slippa dyr `RESP0` bryter O1 och LM-D13.
- `G5Y-S05-OVERLAP`: NPC och key har **verklig** bitpixelöverlapp (G5P illustrativt 13). O1 tillåter **temporär lokal skymning**, men key får inte flyttas eller försvinna logiskt, efter skymning ska den synas igen, spelaren ska kunna ta den och +50 gäller K1-först-vid-pickup.

**Fysisk acceptans saknas** för båda; nya renderingsarkitektur-/flickerkoncessioner kräver uttryckligt framtida användarbeslut, inte "förväntade tekniska kompromisser". `S05` bör inte bakas in i det första H4-provet, eftersom det skulle ändra dess primitiva kanalägarschema och förstöra jämförbarheten. **S05 kräver nytt separat scope även efter ett H4-PASS.**

## 6. Fem-NPC och de fyra nya kartorna: vad längre fram *måste* bevisas
- **Frysta exakta source-grid-matriser** väljs i [G5X-manifestet](G5X_MAIN_VII_APPROVED_FUTURE_FOUR_MAPS_SOURCE_MANIFEST_2026-11-17.json): A_OPEN_01, B_OPEN_02, C_OPEN_01, D_OPEN_01. Ingen historisk v0.11-map/ROM-scen får omskrivas till ny version; B_OPEN_01 är uttryckligen ej vald.
- **Visning:** 5 vita TOPDOWN M,M,F,SM,SF tillsammans med gul fullstor player, M0 samt PF i x/Y-stress, fria X-ordningar inklusive player mellan två M, och scanline-maskar med många samtidiga bitar. G5H har source-only naiv A-ordning **79/76** och särskild B bäst **74/76** (före RAM-fetch, real M0, PF, START); detta är en kostnadsmodell, inte hårdvarupass eller ett universellt omöjlighetsbevis. Nekad tyst permanent Y-lane enligt LM-D12; större flimmer än godkänt kräver separat beslut.
- **Kartornas PF:** 40×22 är en källa/designlayout, inte färdig TIA-bitraster. Den faktiska x39 orange door och låst upplåst-visualisering med transparens måste kunna visas även när väggarna ändras scanline/fas. Gamla R3/C02 är isolerat separat bevis och gäller inte automagiskt den nu nya fyrkartsbasen.
- **Logik:** fem individuella rumsstartpositioner måste testas med riktiga 8×9-mask-/collision envelopes, inte enbart 2×2-ankare som G5P/G5V. Varje NPC-instans M1/M2/F/SM/SF har 1/5 sannolikhet att vara key-holder, efter dess dödsanimation key på faktisk fallplats; K1/E1 och scoring −30/kill med event-nollgolv; alla fem worst-case bärare och utgångar.
- **Oberoende validering:** ROM DEVELOPMENT III får senare utveckla inom sin **egen uttryckligen godkända** order. MAIN:s egen kontroll ≠ VERIFICATION II; senare verklig ROM-acceptans kräver separat oberoende granskningsunderlag. Ett H4-micro-pass ger bara `H4_MICRO_PASS_BOUNDED`, inte `G5/PASS`, `R1`, `R2`, `R3` eller `G6/PASS` för hela spelet.

## 7. Beslutsunderlag för användaren vid framtida auktorisation – INGEN ORDER NU
**MAIN rekommenderar att nästa *eventuellt* auktoriserade tekniska steg är ENBART en source-only `G0 H4-ONE` preflight med verklig cycle-/CC-/START-/RIOT-/F6-analys och en tydlig `G0_FAIL_NO_ROM`-möjlighet.**

Ett **senare** explicit beslut kan formulera `Jag auktoriserar enbart G5Y:s G0 source-only-preflight av H4-ONE till ROM DEVELOPMENT III. Ingen binär, ingen G1, inget G6/F12 utan nytt beslut.` Detta beslut är **INTE lämnat i aktuell användarreplik "Bra, fortsätt"**. Det bör utfärdas först efter att användaren fått detta fasta underlag. Vi ska INTE redan nu öppna Issue som ROM-specialistens order och vi ska INTE smygauktorisera en ny v0.18/F12-variation.

Vid `G0_SOURCE_PLAUSIBLE`: MAIN kontrollerar exakt plan och förelägger därefter **separat** användarförfrågan om en enda fysisk mikro. Vid `G0_FAIL_NO_ROM`: ingen ROM byggs; överlämna exakt blockerare och eventuellt framtida explicit gameplay- eller teknikbeslut. Vid `INCONCLUSIVE`: identifiera vad som saknas; ingen standardmässig "försök igen"-loop. **G5_FORMAL_OPEN**, **G6/F12_NOT_AUTHORIZED**, **ROM_NOT_STARTED**, **PR#7_NOT_MERGED**, **NO_NEW_INDEPENDENT_VERIFICATION** gäller efter publiceringen av G5Y.

**G5Y:s fullbordan betyder att vi slutat cirkulera i G5-designval och nu har en prövbar teknisk ordning; den betyder INTE att vi har visat att hela spelet är genomförbart.**
