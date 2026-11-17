# Let Me Out! – MAIN:s kompletterande beslutsregister och aktuell auktoritet

## MAIN VII – LM-D22 nytt precist användarmandat: F9-instrumentering en gång (2026-11-17)

**Uttryckligt användarbeslut:** Efter MAIN VII:s konkret föreslagna, mycket lilla rättning/återkontroll av Stella-instrumenteringen med den **redan frysta F9-ROM:en**, svarade användaren **"Ok, fortsätt med din rekommendation"**. **LM-D22** är **ett eget nytt avgränsat tillstånd för ROM DEVELOPMENT III:s testharness**, INTE återöppning av förbrukat LM-D21/G5AD och inte ett nytt spel-/graphics-/TIAscope. [Bindande G5AF-arbetsorder](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AF_MAIN_VII_LM_D22_F9_INSTRUMENTATION_ONLY_REPAIR_RETEST_AUTHORIZED_2026-11-17.md) · [Issue #14](https://github.com/Odourman/let-me-out/issues/14) · [Drive-kopia](https://docs.google.com/document/d/1qRX0t1RRn2bZG3dS4-9NAnrnbHZbd1wRVfeAorEbVAc/edit).

**Enbart tillåtet:** på isolerad gren justera arbetsflöde/Python/loggning och återköra oförändrad **F9** ROM (SHA-256 `6c2585148eb082fb8bc794d664edc4869b18849fcfabb9cada23373d1dc1318b`) i Stella, dokumentera två faktiska numeriska CPU/PC/scanline/registerstopp tillsammans med native pixelbild och filhashar; **högst två mätkörningar**. Slutstatus en av `G5AF_INSTRUMENTATION_READY_BOUNDED`, `G5AF_PARTIAL_INSTRUMENTATION_NOT_READY`, `G5AF_INSTRUMENTATION_BLOCKED` och sedan STOPP.

**Ej tillåtet:** ny `.asm/.bin`, DASM-build/F9-ändring, G5AD C0–C4/N1, full H4/G1/G6/F12/S05/fem-NPC, ny oberoende Verification eller merge, ny canon. G5Z/G5AD historiska tekniska utfall förblir oändrade; **G5 formellt OPEN**. G5AF är ännu **inte** utförd.


## MAIN VII – LM-D21 avrapporterat: G5AD instrumenteringsspärr, NO BUILD (2026-11-17)

**LM-D21** godkände en villkorad enda TIA-kalibrerings-ROM men **är nu förbrukat och avslutat vid den förregistrerade hårda förbyggsgrinden**. [G5AE MAIN-mottagning](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AE_MAIN_VII_G5AD_NO_BUILD_INSTRUMENTATION_BLOCKER_RECEIPT_AND_STELLA_SAVESES_SOURCE_REVIEW_2026-11-17.md) · [Drive](https://docs.google.com/document/d/1hJZJa11HB5pKV1k1nBn9YACnmEJHlNLj9klyXUV-usE/edit) · [fryst specialistresultat](https://github.com/Odourman/let-me-out/blob/1fe92438c3aa0d9f41cca0066f0a95e6c0335acc/rom/g5ad_tia_calibration_2026-11-17/TO_MAIN_G5AD_TIA_CALIBRATION.md) · [Issue #13](https://github.com/Odourman/let-me-out/issues/13). **Verkligt resultat `G5AD_NO_BUILD_INSTRUMENTATION_BLOCKER`: ingen ny ROM, ingen TIA-C0/C1/C2/C3/C4/N1-mätning**. Sex `NOT_DETERMINABLE` betyder **NOT_RUN_NO_NEW_ROM**, inte "TIA omöjlig". Loggarna visar tools PASS, gammal F9 PNG 320×228, `saveSes` 0 byte och separat Python `IndentationError`. Main har sedan läst Stella 6.7.1-kod och funnit stark orsakshypotes om `saveSes` inuti `autoexec` före färdig promptbuffer; ingen ny CI-körning eller kodändring gjord.

**Inget nytt användarbeslut finns efter LM-D21**, och ett senare instrumenteringsprov kräver **nytt separat uttryckligt godkännande**, ej "fortsätt". `G5_FORMAL_OPEN`, `G5Z_G0=INCONCLUSIVE_NO_ROM`, `FULL_H4/G1/G6/F12/S05/FIVE_NPC_IMPL/VERIFICATION/PR_MERGE=NOT_AUTHORIZED`. Äldre "G5AD auktoriserad, ännu ej körd" nedan är historisk tidssnapshot, inte gällande arbetsstatus.


## MAIN VII – LM-D21: EN instrumenterad TIA-kalibrerings-ROM godkänd (2026-11-17)

**Direkt uttryckligt användarbeslut:** Användaren citerade MAIN:s rekommendation om **ett enda begränsat TIA-mätprov** av RESP, GRP, NUSIZ0, M0, ENAM0 och instruerade **"Gör så"**. [G5AD bindande ROM DEVELOPMENT III-arbetsorder](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AD_MAIN_VII_ONE_TIA_PHASE_CALIBRATION_ROM_EXPLICIT_USER_AUTHORIZATION_2026-11-17.md) · [sex preregistrerade scenarier](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AD_MAIN_VII_TIA_CALIBRATION_PREREGISTERED_CASES_2026-11-17.csv) · [Issue #13](https://github.com/Odourman/let-me-out/issues/13) · [Drive](https://docs.google.com/document/d/163Xtt4ygxQD7eM4AfPwZgAN6JktF8DcEQjKK43JNF-g/edit).

**LM-D21 – avgränsad ny ROM-auktorisation:** EN källa+slutlig fryst standard-F6 NTSC 16 384-byte diagnos-ROM med egna DASM/Stella/Debugger-instrumenterade mätningar av `TIA-C0/C1/C2/C3/C4/N1`. Ingen fullspels-H4, ingen allmän G1/F12/G6, ingen S05/goldkey/orange door eller femfienders-implementation. **G5Z G0-resultat `INCONCLUSIVE_NO_ROM` gäller fortsatt** som historiskt uttömd order. Endast framtida MÄTNING för C0–C4/N1 får nu utföras av ROM DEVELOPMENT III och därefter STOPP; inte oberoende Verification II. Inga senare spelregler/waivers godkända.


> **STATUS: KRONOLOGISKT BESLUTSREGISTER MED HISTORISKA TIDSSNITT.** För exakt aktuellt nuläge använd [CURRENT_AUTHORITY_STATUS_AND_WORK_QUEUE.md](https://github.com/Odourman/let-me-out/blob/main/docs/CURRENT_AUTHORITY_STATUS_AND_WORK_QUEUE.md). Äldre "NOT APPROVED", "NOT ORDERED" eller "CURRENT" längre ned refererar till respektive beslutsdatum; de supersederas endast i motsvarande ämne av senare uttryckliga beslut LM-D12..20. G5Z G0 = COMPLETED INCONCLUSIVE; ingen ny ROM/G6.


## MAIN VII – LM-D20:s auktoriserade G0 är nu levererad INCONCLUSIVE, INGET NYTT ANVÄNDARBESLUT (2026-11-17)

[MAIN:s separat kontrollerade G5AA-avslutsmottagning](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AA_MAIN_VII_G5Z_G0_INCONCLUSIVE_SOURCE_ONLY_RECEIPT_AND_NEXT_DECISION_2026-11-17.md) · [officiell Drive-kopia](https://docs.google.com/document/d/1OTIdsk8JX0K3GDOkFQSKHCgFWNKoWaz4iRklItxUqSQ/edit) · [ROM DEVELOPMENT III källrapport](https://github.com/Odourman/let-me-out/blob/8c7cef622ebaa6543a3f044ddf50d21024b1b978/rom/g5z_g0_h4_one/TO_MAIN_G5Z_G0_H4_ONE.md) · [Issue #12](https://github.com/Odourman/let-me-out/issues/12). **BESLUT LM-D20 var tillåtelse för EN source-only H4-ONE G0; denna enda order är nu fullföljd och avslutad med `G0_INCONCLUSIVE_NO_ROM`.** Fyra frysta specialisttexter/CSV, korrekt 72 testfall×rader = 8 × 9, ingen ASM/BIN/Stella/CI/PR-merge. MAIN har kontrollerat originalmask-/nominell CC-data och nominella opcodekostnader, **inte** hardware timing. Ingen `G0_SOURCE_PLAUSIBLE` och inget globalt `G0_FAIL` har bevisats. **G5_FORMAL_OPEN, G1/G6/F12/ROM/NY_VERIFICATION/PR_MERGE_NOT_AUTHORIZED**. Eventuellt nästa instrumenterat registerfas-mikroprov skulle kräva ett **nytt uttryckligt användarbeslut**, inte ett återanvändande av redan förbrukad LM-D20-order. Äldre LM-D20-status `AUTHORIZED_NOT_STARTED` nedan är historik från innan leverans, inte aktuell status.


## MAIN VII – LM-D20: endast G0 H4-ONE källgranskning auktoriserad till ROM DEVELOPMENT III (2026-11-17)

**Senare, avgränsat användargodkännande:** Omedelbart efter MAIN VII:s tydliga förslag *"Auktorisera enbart G0-källgranskningen av H4-ONE till ROM DEVELOPMENT III, med ovanstående tre utfall och hård stoppgräns"* svarade användaren **"Ok, fortsätt. Följ dina rekommendationer"**. Detta är uttryckligt **LM-D20** om exakt **EN source-only G0-preflight**. [G5Z komplett auktoriserad order](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5Z_MAIN_VII_ROM_DEVELOPMENT_III_G0_H4_ONE_SOURCE_PREFLIGHT_AUTHORIZED_2026-11-17.md) · [öppet G0 specialistissue #12](https://github.com/Odourman/let-me-out/issues/12) · [officiell Drive-kopia](https://docs.google.com/document/d/15cWPUaLAzo-LP131WjTNCmHNsCrOWY9Ii9EAZ2hbmz0/edit).

**GÄLLANDE:** `G0_H4_ONE_SOURCE_ONLY_AUTHORIZED_NOT_YET_EXECUTED`; ROM DEVELOPMENT III får läsa originalkällor och skapa en källbaserad full H4-ONE 6507/cycle/CC/RESP/GRP/NUSIZ/M0/PF/RIOT/F6-plan för alla nio originalmaskrader, båda datastyrda P0 X-ordningarna, två P1 vita originalmasker och **EN M0 på samma Y**, med 76c/rad; N0 bara intern hjälp. Specialist ska leverera **ett** av `G0_SOURCE_PLAUSIBLE`, `G0_FAIL_NO_ROM` eller `G0_INCONCLUSIVE_NO_ROM` och STOPP. Eventuella luckor för fem fritt rörliga NPC samt S05 key+door ska redovisas kort, inte ny forskning.

**EJ GODKÄNT:** ny `.asm`, `.bin`, DASM-/Stella-test, G1/fysisk ROM, G6/F12/later-step, nya fiende-/flicker-/kartregler, PR-merge eller oberoende VERIFICATION II. G5 FORMAL fortsatt ÖPPEN. Äldre G5Y-frasen "G0 inte auktoriserad" är historiskt korrekt **före LM-D20** men supersederas nu **endast för source-only G0**; alla andra stopp kvarstår. Issue #12 är formellt beställt, **men annan chatt körs inte automatiskt av en GitHub-issue**.


## MAIN VII – LM-D19: B_OPEN_02 exakt framtida rum B godkänd; framtida fyrkartdesign komplett (2026-11-17)

**Senare användarbeslut:** Direkt efter frågan "Godkänner du B_OPEN_02 som exakt framtida rum B?" svarade användaren **"Är bra ut. Följ dina rekommendationer"**. Därför är **LM-D19 = B_OPEN_02 GODKÄND SOM EXAKT FRAMTIDA 40×22-KARTLAYOUT**. [Bindande snävt beslutsprotokoll](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5X_MAIN_VII_B_OPEN_02_EXACT_USER_APPROVAL_AND_FOUR_MAP_BASELINE_DECISION_2026-11-17.md) · [källpinnat fyrkartsmanifest](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5X_MAIN_VII_APPROVED_FUTURE_FOUR_MAPS_SOURCE_MANIFEST_2026-11-17.json) · [Drive](https://docs.google.com/document/d/1nRG3gmoP1Y8VRy5mu6xk3nRRGLVHntf4tRzWHzYOClQ/edit). Beslutet supersederar historiska formuleringar "B_OPEN_02 är ej godkänd" **endast för framtida kartgeometrins status**, utan att radera själva forsknings-/studiehistoriken.

| Framtida rum | Godkänd exakt layout | Beslut | Pin |
|---|---|---|---|
| **A** | `A_OPEN_01` | LM-D17 | `design/OPEN_ROOMS_V019_40x22_CANDIDATES.json` blob `0e449f97f87bd9b403476fd1435398042eaee285` |
| **B** | `B_OPEN_02` | **LM-D19** | `studies/graphics/G5V_B_OPEN_02_2026-11-17/B_OPEN_02.json` graphics-commit `2991a94a4d92a0ee75a5de8e8c5302d549734e1e`, blob `c32fc656fb5c60d16a5b73e4cea75f86df3e9621` |
| **C** | `C_OPEN_01` | LM-D17 | Samma A/C/D blob |
| **D** | `D_OPEN_01` | LM-D17 | Samma A/C/D blob |

**Den fullständiga fyrkartans exakta framtida DESIGNBAS är vald; ingen ROM-/PF-/G6-cutover har genomförts.** Original v0.11 A01/B01/C02/D01, äldre beslut/ROM-bevis och metadata `NOT APPROVED` i gamla studie-JSON bevaras oförändrade. G5:s 8×9-spawnkollisioner, fri fem-NPC-jakt, key-drop och S05 TIA-kanalkonflikt är olösta. **G5 FORMAL OPEN; G0/G6/F12/ROM/VERIFICATION/PR MERGE INTE AUKTORISERADE.**


## MAIN VII – LM-D17/LM-D18: exakt A/C/D-kartbeslut och G5V B-grafikuppdrag GODKÄNDA (2026-11-17)

**Direkt senare användarsvar:** MAIN frågade om användaren godkänner **exakt `A_OPEN_01`, `C_OPEN_01`, `D_OPEN_01` som framtida kartbaser** och ett **separat begränsat GRAPHICS II-uppdrag att förbättra B till `B_OPEN_02`**. Svaret var **"Ser bra ut"**, ett direkt avgränsat godkännande av dessa två delar. [Fullt G5V-beslutsprotokoll](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5V_MAIN_VII_A_C_D_EXACT_OPEN_MAPS_USER_APPROVAL_AND_B_OPEN_02_GRAPHICS_ORDER_2026-11-17.md) · [Drive](https://docs.google.com/document/d/11BAB8skxf1EJH7PFXo1mdlZ7MDGMevmRS_eDlhPYikw/edit) · [GRAPHICS II-uppdrag Issue #11](https://github.com/Odourman/let-me-out/issues/11).

| Beslut | Godkänd omfattning | Utesluter |
|---|---|---|
| **LM-D17** | De exakta 40×22-geometrierna för `A_OPEN_01`, `C_OPEN_01`, `D_OPEN_01` i original `design/OPEN_ROOMS_V019_40x22_CANDIDATES.json` är godkända **framtida kartlayoutmål**. | Inte komplett fyra-rums-cutover; ingen käll-JSON-ändring, ROM/avläst Stella, spawn-/kollisions-/raster-PASS. `B_OPEN_01` är inte godkänd. |
| **LM-D18** | MAIN får ge GRAPHICS II ett separat, snävt **source-only-studieuppdrag** att skapa `B_OPEN_02` som luftig, mer varierad 40×22-kandidat. | Ingen B-karta ännu skapad eller godkänd, ingen ROM, G0/G6/F12, godkända spawns eller PR-merge. |

**A1/B1/C1/D1/E1 (LM-D12..D16)** är redan godkända inom tidigare exakt scope. Historiska v0.11-layout-/ROM-prover är frysta. All äldre text om att *alla fyra* v0.19 OPEN-kartor ännu är obeslutade är en historisk tidssnapshot **före LM-D17** och supersederas endast för A/C/D. **G5_FORMAL_OPEN, G6/F12_NOT_AUTHORIZED**.


## MAIN VII – LM-D14, LM-D15 och LM-D16: nya G5S-beslut GODKÄNDA (2026-11-17)

**Senare direkt användarsvar:** Efter MAIN:s uttryckliga fråga "Godkänner du uttryckligen C1, D1 och E1 som framtida spel- och testregler?" svarade användaren "Fortsätt Följ dina egna rekommendationer". I just detta sammanhang gäller **C1+D1+E1 som framtida krav**. [Fullständigt exakt beslutsprotokoll](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5S_MAIN_VII_C1_D1_E1_USER_APPROVAL_DECISION_RECORD_2026-11-17.md) · [Drive](https://docs.google.com/document/d/1UboARrqu3sFHQgeV1y5C0IWoRkSlvAY_6b6RMLWwbnE/edit). Äldre G5R-texter om "fortfarande endast förslag" beskriver tiden **före** detta användarsvar och supersederas endast för dessa tre rekommendationer.

| ID | Godkänt beslut | Exakt giltighet och gräns |
|---|---|---|
| **LM-D14 / G5R C1** | Framtida versionerat R1-mål med **5 NPC M,M,F,SM,SF**, R2 med **4 kvarvarande + synlig key** efter dödsanimation. | **Testmål godkänt, INTE ett nytt ROM-PASS.** Originalmasker bevaras och v0.18 R1=6/R2=5+key förblir historiskt frysta. Ingen omedelbar teknisk cutover/implementation. |
| **LM-D15 / G5R D1** | För **framtida fem-NPC-spelversion**: **-30 poäng per dödad NPC**, ursprunglig +50 pickup, +100 exit, +15 per överlevande, 0-golv per kill och extralivströsklar oförändrade. | **Framtida spelregel godkänd**; originalets sex-NPC/-25 historiskt oförändrad. För k=5 och ingen poänggolvseffekt blir netto 0 per rum. Ingen ROM-kod ändrad. |
| **LM-D16 / G5R E1** | **5 distinkta, förhandsvaliderade NPC-spawnpositioner** per framtida rum och **uniform sannolikhet 1/5 för key-bärare bland de fem individuella NPC**, inte fyra masktyper. | **Policy godkänd**, men inga specifika startkoordinater/kartor, PRNG-implementation eller faktiska tester godkända. Key faller efter dödsanimation på fysisk/logisk fallplats; K1/O1/E1 fortsatt styrande. |

**A1/B1 LM-D12/13 godkända sedan tidigare.** Fortfarande ÖPPET: exakt v0.19 kartbyte, framtida G0-S05/renderingskernel och uttrycklig G6/F12-arbetsorder. **G5 FORMAL OPEN, G6/F12 NOT AUTHORIZED, NO NEW ROM, NO VERIFICATION, NO PR MERGE.**


## MAIN VII – LM-D12 och LM-D13: godkända G5Q-designmål, 2026-11-17

**Direkt användargodkännande via uttrycklig hänvisning:** På MAIN VII:s omedelbara fråga "Godkänner du G5Q:s rekommendation A1 + B1 som våra fortsatta designmål?" svarade användaren **"Följ dina egna rekommendationer"**. I just denna samtalskontext innebär det godkännande av A1+B1 som **mål**, inte av övriga förslag. [Fullständig spårbar beslutsregistrering](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5Q_MAIN_VII_A1_B1_USER_APPROVAL_DECISION_RECORD_2026-11-17.md) · [Drive](https://docs.google.com/document/d/1Yh5XfKZ8f9rm97sG7jY8tAjuGiV-0o9O-d9oy-BkP2s/edit).

| ID | Senare giltigt användarbeslut | Avgränsning |
|---|---|---|
| **LM-D12 (G5Q A1)** | Fem framtida NPC M,M,F,SM,SF ska **logiskt kunna röra sig individuellt fritt i X/Y**, fyrvägs-jakt och NPC/NPC-kollision bevaras som spelmål. | **Designmål godkänt.** Ingen permanent tyst Y-lane, ingen accepterad renderer eller generell synlighets-/AI-waiver. Framtida v0.18 R1/R2-cutover fortfarande obeslutad. |
| **LM-D13 (G5Q B1)** | Fem fiender ska vara igenkännbara, farliga närliggande fiender får inte systematiskt försvinna; key ska synas när ingen NPC faktiskt pixelöverlappas. | **Kvalitetsmål godkänt.** Ingen numerisk flimmergräns, 10Hz-acceptans eller ny key-hide. **LM-D06/O1** fortsatt giltig enbart vid faktisk pixelöverlappning. |

**Läsordning och auktoritet:** LM-D12/13 gäller senare **designmål** för den framtida femfiendersinriktningen; den äldre LM-D01 med sex fiender och frysta historiska R1/R2-romtester ska inte raderas eller retroaktivt märkas om. Övriga 57 beslut, Master Spec, K1/E1, originalmasker och tillämpliga restriktioner kvarstår. **C/D/E (test-baslinje, poäng -30 kontra -25, 1/5 key-bärare/femspawn, exakta v0.19-kartor) inte godkända; G5 formellt ÖPPEN och G6/F12 inte auktoriserade.**


**Datum:** 2026-11-15  
**Projekt:** enbart `Odourman/let-me-out` / Google Drive-mappen `Atari 2600 - Let Me Out!`.  
**Syfte:** bevara nyare användarbeslut, precisera vad som *inte* är godkänt och ge nya MAIN-/ROM DEVELOPMENT-/VERIFICATION-chattar en entydig ingång.  
**Registerstatus:** komplement till den ursprungliga **57-posters beslutshistoriken** i `LET_ME_OUT_MAIN_HANDOFF_2026-11-15.zip`; ersätter eller skriver inte om det originalet. Konkreta användarbeslut gäller före rådgivande studier. Tidigare daterade dokument med formuleringen "ROM DEVELOPMENT pausad" beskriver sitt **historiska läge** och får inte användas för att upphäva det senare uttryckliga v0.18-tillståndet.

## 1. Aktuella direkta användarbeslut och visuella mål

| ID | Beslut eller preferens | Status och avgränsning | Auktoritativt underlag |
|---|---|---|---|
| LM-D01 | Sex vita, människoliknande androider: 2 stora män, 2 stora kvinnor, 1 liten man och 1 liten kvinna; fyra igenkännbara figurtyper. | **Fastställt spelupplägg.** Inga tysta förenklingar till block, färre NPC:er eller sammanlänkad rörelse. | Ursprunglig 57-beslutshandoff och [exakta ursprungsmasker](https://github.com/Odourman/let-me-out/blob/main/design/NPC_REFERENCE_8x9_masks.json). |
| LM-D02 | Gul spelare med hatt och vapen; **lika stor på skärmen som de stora androiderna**. De små är visuellt mindre. | **Godkänt visuellt mål.** Fortsätt utvärdera 8×9 för spelaren/stora och 8×9 matris med sex synliga rader för de små. Spelarens slutliga bitmap är inte låst. Användaren vill att figurerna ska kännas något mindre än Berzerks och inte dominera rummet; exakt jämförelseskala mot Berzerk är inte mätt. | [MAIN spelarskala](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_PLAYER_SCALE_V018_2026-11-15.md), originalmaskerna, användarens förtydligande i chatten. |
| LM-D03 | **Spelaren ska inte framstå som större än dörröppningen.** | **Visuellt/rumsligt mål**, inte nytt numeriskt kollisionsbeslut. Nuvarande skiss med högerdörr y9–12 ger 4×8 = 32 skärmlinjer hög öppning i offline-visualiseringen; faktisk TIA-rendering är inte färdig. | Användarens storleksförtydligande och [v0.19 kartstudie](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_OPEN_ROOMS_V019_2026-11-15.md). |
| LM-D04 | **Rummen ska vara luftiga**: få bruna väggpartier som antyder små rum eller avdelningar, men inte bildar en tät labyrint; stor fri mitt-/rörelseyta och breda öppningar. Inspirationskälla: Berzerks enkla rumsformationer, inte kopierade nivåer. | **Godkänd designriktning.** De fyra schematiska öppna rumstyperna har fått positivt användarsvar. Det betyder inte automatiskt att de exakt genererade 40×22-rutmatriserna har godkänts som ny slutgiltig canon. | Användarens direkta beskrivning och godkännande av skisserna; [v0.19-rapport](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_OPEN_ROOMS_V019_2026-11-15.md). |
| LM-D05 | Fyra rum, endast utgång på **högra** väggen. Stängd vänstervägg. Orange dörrmarkör med svart nyckelhål; guldgul nyckel med runt hål och kort tandat skaft. | **Beslutad spelmekanik/visuell riktning**; exakta TIA-färger, bitmapmasker och teknisk lösning inte verifierade. Dörren och nyckelhålet försvinner tillsammans vid upplåsning, verklig utgång krävs för bonus. | [Godkänt visuellt mål v0.13](https://github.com/Odourman/let-me-out/blob/main/docs/KEY_AND_DOOR_VISUAL_TARGET_V013.md). |
| LM-D06 | **O1:** android får visuellt skymma nyckeln tillfälligt men nyckelns logiska läge ändras inte; den blir synlig på samma plats efter skymning. | **Godkänt**. Lite, kortvarigt flimmer accepterat, men inte långvarigt oläsbara farliga figurer. | [MAIN-beslut O1](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_STATUS_NEXT_10_2026-11-15.md). |
| LM-D07 | **K1:** nyckel som skapas under stillastående spelare kan plockas tidigast nästa logiska uppdatering. **E1:** dödlig kontakt vid verklig högerutgång prioriteras före utgångsbonus, förutsatt överlevande android; skottträff på den androiden behandlas först. | **Godkända spelregler**, inte implementerade/verifierade i ROM. | [K1/E1-besluten](https://github.com/Odourman/let-me-out/blob/main/docs/APPROVED_EDGE_CASE_DECISIONS_K1_E1_2026-11-15.md). |
| LM-D08 | Ingen separat startskärm; efter GAME OVER en Berzerk-inspirerad presentation i samma spelplan. **Endast konsolens RESET** startar om efter GAME OVER, med tre liv och noll poäng; FIRE startar inte om. | **Beslutat grundflöde.** Exakta färgeffekter och tidsintervall är öppna. | [Game Over/RESET-beslut](https://github.com/Odourman/let-me-out/blob/main/docs/GAME_OVER_RESET_ONLY_DECISION_2026-11-15.md). |
| LM-D09 | **Kodauktorisation: endast Atari 2600 NTSC-diagnostik v0.18 R1–R4**, F6 16 KB om tekniskt motiverat, under ROM DEVELOPMENT och separat VERIFICATION. | **Uttryckligen godkänt.** Fullspel, PAL, senare ROM-faser, AI, poängkod, ljudkod, gameplaykartcutover m.m. är **inte** därmed auktoriserade. | [Issue #6](https://github.com/Odourman/let-me-out/issues/6), [autorisationsdokument](https://github.com/Odourman/let-me-out/blob/main/docs/ROM_GATE_V018_AUTHORIZATION_2026-11-15.md). |
| LM-D10 | **Omedelbar prioritet inom v0.18:** lös sex androiders individuella X-positionering och läsbarhet med fullstor gul spelare och testsymbolskott. | **Uppgiftsprioritering inom redan auktoriserad R1**, inte nytt fristående utvecklingssteg. Tvåsilhuettsprovet fungerade endast vid NUSIZ-fasta 32/64-avstånd; sex oberoende sprites har ännu inte klarat ROM-test. | [MAIN sex-X-rapport](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_SIX_INDEPENDENT_X_V018_2026-11-15.md), [PR #7](https://github.com/Odourman/let-me-out/pull/7). |
| LM-D11 | Let Me Out! hålls isolerat från **The Cabin** och **I Love a Fish**; **Linear används inte**. | **Projektregel.** Endast detta GitHub-repo och dess dedikerade Google Drive-mapp får ändras inom uppdraget. | Projektets aktuella MAIN-dokument och användarens tidigare direktiv. |

## 2. Fyra nya exakta kartor – resultat, men inte automatiskt godkänd ersättning

Användaren godkände den **öppna rummens designriktning**, och bad därefter MAIN skapa och kontrollera exakta 40×22-matriser. Det uppdraget är utfört som **v0.19 design-/offline-studie**. De exakta rutplaceringarna nedan är dock ännu **förslag**; det finns inget uttryckligt separat beslut som byter ut den tidigare, källvalda kartbasen **A01/B01/C02/D01** (inklusive det tidigare explicita valet av C02).

| Kandidat | Beskrivning | Nya innerväggar / 760 innerrutor | Reachable 2×2-ankare (offline) | Tidigare karta |
|---|---|---:|---:|---|
| `A_OPEN_01` | Fyra L-formade hörn, fri mittarena | 36 = 4,74 % | 623/623 | A01 |
| `B_OPEN_01` | Fyra dubbla väggstumpar, öppet mittparti | 48 = 6,32 % | 619/619 | B01 |
| `C_OPEN_01` | Hörn som antyder små rum, stora öppningar | 64 = 8,42 % | 579/579 | C02 |
| `D_OPEN_01` | Väggarmar och fri mittarena | 60 = 7,89 % | 591/591 | D01 |

**Gemensam bevarad geometri:** 40×22; inre väggar speglas; brun vägg, svart spelplan; vänster gräns stängd; dörr på **x39, y9–12**; spelarstartankare x2/y10. En kartcell är 4 horisontella TIA-färgklockor × 8 vertikala förhandsvisnings-scanlines i offline-skissen. Dessa pixel-/färgdetaljer är inte ännu godkänd ROM-rendering.

**Reproducerbara filer:** [v0.19 JSON](https://github.com/Odourman/let-me-out/blob/main/design/OPEN_ROOMS_V019_40x22_CANDIDATES.json), [MAIN-rapport](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_OPEN_ROOMS_V019_2026-11-15.md), [Drive ZIP](https://drive.google.com/file/d/1kO38zm26fFSwu0cAnwQYAZ56D52HrJvK/view), [mobilrapport](https://drive.google.com/file/d/197ssAX79Zqdmwl0V5W3xLhDVKMwgYYw3/view). **Historisk originalbas:** [v0.11](https://github.com/Odourman/let-me-out/blob/main/design/PLANERADE_RUMSKARTOR_V011.json).

**Offlinebevis och gränser:** Alla lagliga 2×2-fotankare i varje rum var nåbara, en öppen väg till högerdörren fanns och minst sex separata startankare fanns. Dessutom gjordes 100 deterministiska, förenklade dynamiska trafiktester per rum (400 totalt); spelaren nådde dörren inom 180 modellsteg i 400/400. Ingen faktisk P2/J2-jakt, 8×9-spritekollision, full diagonalförflyttning, 2600-ROM eller Stella-test ingick. Testerna bevisar **inte** att ingen någonsin fastnar i spel.

## 3. Öppna val – får inte omtolkas till beslut

- **Slutlig uppsättning kartor:** de exakta `A_OPEN_01`–`D_OPEN_01` är *kandidater*. Bevarade v0.11-kartor är tills vidare känt källval. Byte kräver användarens explicita val efter fortsatt granskning.
- **Kollisionsrektangel:** 6×6 för spelaren/androiderna har diskuterats som en **möjlig framtida testkandidat**, inte ett godkänt byte från existerande logik. Stor och liten android ska fortsatt ha **samma logiska kollisionsyta** enligt det gamla beslutet.
- **Diagonalt väggglid:** rekommendation för smidig spelkontroll, **inte** implementerat eller uttryckligt godkänt som konkret rörelseregel.
- **Minimala korridorbredder och väggtjocklekar:** tidigare MAIN-förslag (t.ex. 12 färgklockor fritt vågrätt, 16–24 scanlines vertikalt) är **riktvärden**, inte låsta dimensioner och inte testad hardware-acceptans.
- **Slutlig spelarbitmap, exakt Berzerk-skaljämförelse, guldnyckelmask och färgkoder** kräver speltest och/eller uttrycklig senare formbedömning. AI-genererade jämförelsebilder är *skisser*, inte Stella-skärmbilder.
- **S0/S1 spawnjusteringar, P2/J2 AI, hastighet C-1, HUD och fullspelsstart** är tidigare förstudier där annat inte uttryckligen har godkänts.

## 4. Oavslutad ROM-diagnostik och verifieringsspärr

- Utvecklargren `rom-dev/v018-ntsc-diagnostic`, [draft PR #7](https://github.com/Odourman/let-me-out/pull/7). Senast kontrollerad utvecklar-HEAD: `f5c06f352ba8653f3ce65bbc3e5e392c892beec5`; PR ska **inte** mergas innan oberoende verifiering och MAIN:s mottagning.
- Fryst originalbaseline: `561d3baf00c6c4c4bd9bc46599a91dc693abdeba`, med [separat VERIFICATION Issue #8](https://github.com/Odourman/let-me-out/issues/8). Nya commits behöver egen oberoende bedömning, inte ärvd PASS.
- Faktiskt bevisat i Stella: 2 olika originalmasker (stor man/stor kvinna) med **fasta** NUSIZ-kopieavstånd 32/64 färgklockor, plus synlig gul spelarkandidat och skott. **Sex oberoende androider är fortfarande inte godkända**, och 600-frame scanlineloggar saknas. Allt nytt här ovan om kartor hör till **design/offline**, inte den redan godkända v0.18 ROM-implementationen.
- Ingen senare cutover, PAL, fullspel, nya AI-/poäng-/ljudimplementationer eller kartbyte får ske tyst eller bara genom att en ny rapport publiceras.

## 5. Vart nästa arbetschat ska börja

1. Läs denna beslutslogg och [aktuellt projektläge](https://github.com/Odourman/let-me-out/blob/main/docs/CURRENT_PROJECT_STATE_2026-11-15.md). Kontrollera sedan originalbesluten i handoffen och senaste källor som är relevanta för uppgiften.
2. Skilj **GODKÄNT BESLUT**, **VISUELL RIKTNING**, **KANDIDAT**, **OFFLINE-MODELL**, **KÖRBAR STELLA/ROM** och **OBEROENDE VERIFICATION** i varje rapport.
3. Kontrollera alltid faktisk PR-head och Issue #8 i GitHub, och respektive källmaterial i Drive; anta inte att HEAD/hash aldrig ändras efter detta dokument.
4. Bevara historiska beslut och filer. Vid senare godkännande: lägg till ett **daterat delta eller uttrycklig supersession** i stället för att tyst radera äldre beslut. Ingen automatisk överflyttning från designspår till ROM-spår.

**Arkivering:** samma text lagras i GitHub och Google Drive. Detta register är ett tillägg, inte en ny generell rätt att implementera.
