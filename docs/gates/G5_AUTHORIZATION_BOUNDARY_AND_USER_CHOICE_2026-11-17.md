# LET ME OUT! – G5: bindande beslutsspärr och framtida scope (ingen canon-ändring)

## MAIN VIII G5AH / LM-D23 – SENARE AVGRÄNSAT C0-UNDANTAG (2026-11-17)

**SENARE DIREKT ANVÄNDARBESLUT:** På MAIN VIII:s specifika förslag att först bevisa **C0-mätbarheten** och behandla C1–C4/N1 i en **separat, senare godkänd testorder**, svarade användaren "Ok, fortsätt med det du rekommenderar. Använd dig av GitHub, Google Drive och Project sources". MAIN VIII har därmed utfärdat **LM-D23/G5AH** **endast för C0-baslinjen**, med hård instrumenterbarhetsgrind och högst **en** minimal 16KiB F6/NTSC C0-ROM efter godkänd grind samt högst två Actions-mätkörningar. [Bindande fullorder](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AH_MAIN_VIII_LM_D23_C0_ONLY_TIA_MEASUREMENT_EXPLICIT_USER_AUTHORIZATION_2026-11-17.md) · [Issue #15](https://github.com/Odourman/let-me-out/issues/15). **`G5AH_C0_AUTHORIZED_NOT_YET_EXECUTED`** – inte redan mätt eller byggt.

**Den generella äldre spärren "ingen ny ROM" har ett ENDA senare uttryckligt undantag: detta G5AH-C0-prov.** G5Z/LM-D20, G5AD/LM-D21 och G5AF/LM-D22 är fortfarande avslutade; G5AF får ingen tredje körning; G5AD:s sexfallsmatris öppnas inte på nytt. **C1/C2/C3/C4/N1 kräver ett NYTT separat användarbeslut**, liksom H4/G1, G6/F12, S05, full fem-NPC/spelimplementation, independent Verification II och PR-merge. **`G5_FORMAL_OPEN`**. Det nya C0-undantaget är *inte* ett tekniskt PASS.

## MAIN VIII G5AG – AKTUELL SENARE BINDANDE STOPPSPÄRR (2026-11-17)

**SENARE ÄN G5AF-ORDERTEXTEN NEDAN:** [MAIN VIII:s G5AG mottagningsrapport](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AG_MAIN_VIII_G5AF_F9_INSTRUMENTATION_RECEIPT_2026-11-17.md) visar att LM-D22/G5AF är **LEVERERAD OCH AVSLUTAD**, endast utvecklarverifierad fryst F9/Stella-instrumentering `G5AF_INSTRUMENTATION_READY_BOUNDED`. [Issue #14](https://github.com/Odourman/let-me-out/issues/14) är CLOSED/COMPLETED endast för instrumenteringen. Det tidigare `G5AF_AUTHORIZED_NOT_EXECUTED` nedan är status **vid orderns utfärdande**, inte aktivt mandat. De två tillåtna Actions-mätkörningarna har förbrukats. **Ingen tredje körning.**

**Historiskt oförändrat:** G5Z/LM-D20 H4-ONE G0 slutade `INCONCLUSIVE_NO_ROM`. G5AD/LM-D21 villkorad TIA-kalibrering slutade `NO_BUILD_INSTRUMENTATION_BLOCKER`; ingen ny G5AD-ROM och inga C0–C4/N1-tester. G5AF bevisar inte internt RESP/GRP/START eller full kernel. **`G5_FORMAL_OPEN`**, ingen ny ROM, H4/G1, G6/F12, S05, femfiendersimplementering, oberoende VERIFICATION II eller PR-merge auktoriserad. Nytt tekniskt steg fordrar separat uttrycklig användarauktorisation. [Levande aktuellt index](https://github.com/Odourman/let-me-out/blob/main/docs/CURRENT_AUTHORITY_STATUS_AND_WORK_QUEUE.md).

**ALLT UNDER NEDANSTÅENDE HISTORISKA G5AF/G5AE/G5AD-AVSNITT MÅSTE LÄSAS MED DESS TIDPUNKT OCH OVANSTÅENDE LATER STATUS.** Ursprungligt mandat och negativa provresultat ändras inte retroaktivt.

## MAIN VII G5AF – LM-D22 specifikt godkänd F9 instrumenteringsreparation, utan ROM-bygge (2026-11-17)

**Efter G5AE:s stängda G5AD-förkontroll:** MAIN föreslog enbart en mycket liten korrigering och ommätning av loggning med redan existerande fryst F9, och användaren svarade **"Ok, fortsätt med din rekommendation"**. Detta är **separat LM-D22**. [G5AF bindande arbetsomfattning och stopp](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AF_MAIN_VII_LM_D22_F9_INSTRUMENTATION_ONLY_REPAIR_RETEST_AUTHORIZED_2026-11-17.md) · [Issue #14 beställt enbart till ROM DEVELOPMENT III](https://github.com/Odourman/let-me-out/issues/14) · [Drive](https://docs.google.com/document/d/1qRX0t1RRn2bZG3dS4-9NAnrnbHZbd1wRVfeAorEbVAc/edit). **`G5AF_AUTHORIZED_NOT_EXECUTED`**, G5AD förblir `COMPLETED_NO_BUILD_INSTRUMENTATION_BLOCKER`.

**Tillåtet:** en enda F9-instrument-harnessfamilj, högst två nya Actions-körningar efter korrigering, rätta `saveSes` i autoexec-startfas och Pythonindentering, mät och spara två verkliga F9 CPU/PC/register/scanline-stopp med native TIA-bild och hashad sessions- och artefaktkedja. **Inte** en ny G5AD-ROM och inte C0–C4/N1-test. Även framgång vore bara `INSTRUMENTATION_READY_BOUNDED`, inte H4-/G5-/S05-PASS.

**Kvarvarande verkliga spärrar:** `G5_FORMAL_OPEN`, `NEW_ROM/H4/G1/G6/F12/S05/FIVE_NPC_IMPL/NEW_INDEPENDENT_VERIFICATION/PR_MERGE_NOT_AUTHORIZED`. Historiska textavsnitt om "inga nya testtillstånd" nedan gäller tiden före det specifika LM-D22-beslutet. Det nya tillståndet gäller **inte** ROM DEVELOPMENT III:s möjlighet att utfärda egen fortsättning.


## MAIN VII G5AE – senast giltiga status: G5AD NO-BUILD, ingen aktiv ROM-order (2026-11-17)

[G5AE MAIN VII originalkontrollerad G5AD-mottagning](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AE_MAIN_VII_G5AD_NO_BUILD_INSTRUMENTATION_BLOCKER_RECEIPT_AND_STELLA_SAVESES_SOURCE_REVIEW_2026-11-17.md) · [Drive](https://docs.google.com/document/d/1hJZJa11HB5pKV1k1nBn9YACnmEJHlNLj9klyXUV-usE/edit) · [fryst specialist-TO_MAIN](https://github.com/Odourman/let-me-out/blob/1fe92438c3aa0d9f41cca0066f0a95e6c0335acc/rom/g5ad_tia_calibration_2026-11-17/TO_MAIN_G5AD_TIA_CALIBRATION.md) · [Issue #13](https://github.com/Odourman/let-me-out/issues/13). **LM-D21:s enda särskilt godkända diagnos-ROM nådde `G5AD_NO_BUILD_INSTRUMENTATION_BLOCKER` i hård förkontroll, och är avslutad utan att någon G5AD-ROM byggdes**. Inget C0–C4/N1 scenario exekverades. DASM/Stella 6.7.1 fanns; fryst F9 gav native bild, men 0-byte `saveSes`, separat Python-indenteringsfel och saknad PC/STA/register/CC/råpixelkorrelation förhindrade verklig mätning. MAIN VII kontrollerade körloggar och Stella-källor; källa visar stark ordningsförklaring `saveSes` från `autoexec` före promptens färdigställning. Det bevisar inte generellt Stella-bug eller Atari-omöjlighet.

**Äldre aktiva formuleringar för G5AD nedan gäller enbart tidsögonblick före leverans.** **`G5_FORMAL_OPEN`, `G5Z_G0_INCONCLUSIVE_NO_ROM`, `G5AD_STOPPED_NO_ROM`, `FULL_H4/G1/G6/F12/S05/FIVE_NPC_IMPL/NEW_VERIFICATION/PR_MERGE_NOT_AUTHORIZED`**. Ingen automatisk återstart av LM-D21 och inget nytt specialistuppdrag. En ny *enbart instrumenteringsreparation* på gammal F9 eller annan verifierbar mätmetod förutsätter separat uttrycklig användarauktorisation.


## MAIN VII G5AD – ny begränsad användarauktorisation LM-D21 för exakt EN TIA-mät-ROM (2026-11-17)

**SENARE och specifikt mandat:** Användaren citerade rekommendationen om ett enda begränsat TIA-mätprov av RESP/GRP/NUSIZ0/M0/ENAM0 och svarade **"Gör så"**. [G5AD ordalydelse/acceptans/stopp](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AD_MAIN_VII_ONE_TIA_PHASE_CALIBRATION_ROM_EXPLICIT_USER_AUTHORIZATION_2026-11-17.md) · [G5AD fryst kontrollmatris](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AD_MAIN_VII_TIA_CALIBRATION_PREREGISTERED_CASES_2026-11-17.csv) · [aktivt Issue #13](https://github.com/Odourman/let-me-out/issues/13) · [Drive](https://docs.google.com/document/d/163Xtt4ygxQD7eM4AfPwZgAN6JktF8DcEQjKK43JNF-g/edit). Detta **supersederar bara det föregående generella `NEW_ROM/G1_NOT_AUTHORIZED`-förbudet för just detta instrumenterade NTSC F6-kalibreringsprov**. `G5AD_SINGLE_TIA_MEASUREMENT_ROM=AUTHORIZED_NOT_YET_EXECUTED`; ROM DEVELOPMENT III får DASM-bygga, köra Stella/Debugger och leverera EN ROM med sex separata kontrollmoder (C0–C4/N1). Raw timing/register/colorclock/pixel plus SHA256 obligatoriskt; om mätning ej kan avgöras ska utfallet märkas `NOT_DETERMINABLE`, inte PASS.

**Kvarstående bindande grindar:** full H4-ONE/R1/R2, G6/F12, S05 key+door, fem-NPC fullspel, ny independent Verification II, PR #7-merge och nya bild/AI/poäng/y-lane/flicker-waivers **INTE godkända**; G5 FORMAL OPEN. Äldre text nedan om `G0/G1/ROM_NOT_AUTHORIZED` är tidsbunden före LM-D21; G5Z G0 var korrekt avslutad `INCONCLUSIVE_NO_ROM`. Detta öppnar **inte** någon G6 cutover family.


> **STATUS: HISTORIKBEVARANDE G5-GRINDLOGG; AKTUELL ORDERSTATUS HÄMTAS FRÅN** [CURRENT_AUTHORITY_STATUS_AND_WORK_QUEUE.md](https://github.com/Odourman/let-me-out/blob/main/docs/CURRENT_AUTHORITY_STATUS_AND_WORK_QUEUE.md). G0 LM-D20 är redan avslutad INCONCLUSIVE, inte väntande; G5 fortsatt OPEN. G1/G6/F12/ny ROM/S05/fem-NPC-implementation/Verification/merge är INTE auktoriserade. Äldre avsnitt nedan visar vad som gällde före senare användarbeslut och ska **inte återaktivera** en order.


## MAIN VII G5AA – senare avslutsstatus för godkänd G0; ingen ny ROM-/G6-order (2026-11-17)

[MAIN G5AA mottagning och begränsat INCONCLUSIVE-resultat](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AA_MAIN_VII_G5Z_G0_INCONCLUSIVE_SOURCE_ONLY_RECEIPT_AND_NEXT_DECISION_2026-11-17.md) · [Drive](https://docs.google.com/document/d/1OTIdsk8JX0K3GDOkFQSKHCgFWNKoWaz4iRklItxUqSQ/edit) · [ROM DEVELOPMENT III:s frysta G5Z leverans](https://github.com/Odourman/let-me-out/blob/8c7cef622ebaa6543a3f044ddf50d21024b1b978/rom/g5z_g0_h4_one/TO_MAIN_G5Z_G0_H4_ONE.md) · [Issue #12 G0](https://github.com/Odourman/let-me-out/issues/12). **LM-D20:s ENDA source-only G0 av H4-ONE har utförts och avslutats `G0_INCONCLUSIVE_NO_ROM`**, mottaget som scope-korrekt efter MAIN:s käll-/72-raders-kontroll. 58/68c är nominell ofullständig direkt-opcodekostnad, 74/79c en villkorlig *append-only* variant, inte en säker körbar RESP/GRP/ENAM/NUSIZ/M0/PF-schema. R1f/R1g och F9 från olika kärnor, tidigare F11 G0 FAIL och G5H 79/76 bevaras som separat negativa/positiva historik. **H4 EJ SOURCE-PLAUSIBLE/EJ FYSISK-PASS**, **inte** universellt bevisad omöjlig.

**Inga följdmandat:** `G5_FORMAL_OPEN`, `G0_COMPLETE_INCONCLUSIVE`, `G1/G6/F12/ROM/ASM/DASM/STELLA/S05/FIVE_NPC_NEW_VERIFICATION/PR_MERGE=NOT_AUTHORIZED`. Tidigare avsnitt längre ned som säger "G0 fortfarande ej utförd" gäller äldre tidssnapshot. Framtida kort *separat* instrumenterad TIA-fas-/kopie-kalibrering kan endast bli ny arbetsorder efter **ny exakt användarauktorisation**; den kan inte kallas H4-fulltest eller göra N0 till H4-PASS och måste ha egen falsifierbar testplan.


## MAIN VII G5Z – särskilt användargodkänd ENDAST G0 H4-ONE source-only preflight (2026-11-17)

**Senare LM-D20 upphäver endast den tidigare spärren mot *källbaserad G0-granskning*.** På MAIN VII:s specifika fråga om endast G0 H4-ONE och tre möjliga utfall svarade användaren **"Ok, fortsätt. Följ dina rekommendationer"**. [G5Z tekniskt avgränsad auktoriserad specialistorder](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5Z_MAIN_VII_ROM_DEVELOPMENT_III_G0_H4_ONE_SOURCE_PREFLIGHT_AUTHORIZED_2026-11-17.md) · [Issue #12 ROM DEVELOPMENT III](https://github.com/Odourman/let-me-out/issues/12) · [Google Drive-kopia](https://docs.google.com/document/d/15cWPUaLAzo-LP131WjTNCmHNsCrOWY9Ii9EAZ2hbmz0/edit). **`G0_AUTHORIZED_NOT_YET_EXECUTED`**. Ingen actually verifierad timing, kernel eller teknisk G0-PASS finns ännu; G5Y 17-falls testmatris har inte körts som fysisk ROM.

Tillåtet en gång: full G4 H4-ONE source-only 6507/76c/START/GRP/RESP/NUSIZ/M0/PF-analys inklusive P0 gul/vit X-sort, två rättvända vita P1 F/SM originalmasker, numeriska separata RAM-X och en M0 på **samma rasterband**, och kort kvarvarande fem-NPC/S05-gap. Utfallet ska vara precis `G0_SOURCE_PLAUSIBLE`, `G0_FAIL_NO_ROM` eller `G0_INCONCLUSIVE_NO_ROM`. **STOPP efter leverans oavsett utfall.** G5P:s smalare N0 får aldrig ersätta H4. Historiska F11 negativ kvarstår.

**Fortfarande bindande stopp:** `G5_FORMAL_OPEN`, `G1/G6/F12/ROM/ASM/DASM/STELLA/NEW_VERIFICATION/PR_MERGE_NOT_AUTHORIZED`. Inga nya flicker-/osynlighets-/X/Y-/AI-kompromisser eller nya kartlayouter, 5-NPC R1/R2 tekniskt fortfarande obevisat. Äldre "G0 inte auktoriserad" längre ned i denna historiska fil är tiden före LM-D20, medan alla andra spärrar gäller.


## MAIN VII G5Y – förregistrerad testordning upprättad, faktiskt G0/G6 fortfarande spärrade (2026-11-17)

[MAIN:s fullständiga G5Y source-only testordning](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5Y_MAIN_VII_FALSIFIABLE_HARDWARE_TEST_PLAN_H4_ONE_S05_FIVE_NPC_NOT_AUTHORIZED_2026-11-17.md) · [17 `NOT_RUN` testfall](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5Y_MAIN_VII_PREREGISTERED_TECHNICAL_TEST_MATRIX_NOT_AUTHORIZED_2026-11-17.csv) · [Drive-kopia](https://docs.google.com/document/d/1Un1kOcd4XqC0drnt3bJaHiS7BINw6YnpRTZuZ53ce-4/edit). **Framtida valda exakta kartlayout A_OPEN_01/B_OPEN_02/C_OPEN_01/D_OPEN_01** är redan godkända som designmål via G5X; inga fysiska spelkartor/collision/ROM har ändå implementerats. G4:s fulla `H4-ONE` (P0 gul+vit, **två P1 vita**, M0 EXAKT EN på samma Y, PF verkligt brunt, bägge X-ordningar och numeriskt RAM-X) har inte G0-PASS. G5P:s smalare två-P0-aktörsdiagnostik kan ej ersätta full H4. Historiska F11 `G0 FAIL`, G5H naiv 79/76 och S05 key+orange door risk förblir giltiga blockerare/negativa referenser.

**G5Y plan är klar men varken SOURCE G0, G1 ROM/Stella, S05 integration eller fem-NPC fulltest är orderlagda.** Rekommenderad framtida **separat uttryckligt beslutad** förstainsats: EN source-only G0 H4-ONE preflight med hård `G0_FAIL_NO_ROM` om förregistrerade CPU/CC/START/GRP/color/RIOT/F6-kriterier fallerar. Om källpreflight mot förmodan plausibel, behövs ett NYTT separat beslut före en enda fysisk mikro-ROm. Inga nya flicker-/AI-/key-/grafikcompromiser godkända. **G5_FORMAL_OPEN, G6/F12_NOT_AUTHORIZED, NO_ROM, NO_INDEPENDENT_VERIFICATION, NO_PR_MERGE.**


## MAIN VII G5X – fyra exakta framtida kartlayouter godkända, teknisk grind kvar (2026-11-17)

[LM-D19 B02 användarbeslut och nu komplett framtida fyrkartsurval](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5X_MAIN_VII_B_OPEN_02_EXACT_USER_APPROVAL_AND_FOUR_MAP_BASELINE_DECISION_2026-11-17.md) · [machine-readable källpinnat urvalsmanifest](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5X_MAIN_VII_APPROVED_FUTURE_FOUR_MAPS_SOURCE_MANIFEST_2026-11-17.json) · [Drive](https://docs.google.com/document/d/1nRG3gmoP1Y8VRy5mu6xk3nRRGLVHntf4tRzWHzYOClQ/edit). **B_OPEN_02 är GODKÄND som exakt framtida 40×22-rum B** genom användarsvaret "Är bra ut. Följ dina rekommendationer" direkt efter MAIN:s specifika fråga; **A_OPEN_01, C_OPEN_01, D_OPEN_01** redan godkända via LM-D17. De fyra exakta framtida designlayouterna är således beslutade, **men ingen kart-JSON har retroaktivt skrivits om och inget spel/ROM har bytt kartbas**. Tidigare "B ej godkänd" nedan är historisk tidsstatus före detta specifika godkännande.

**Fortfarande öppet G5:** prövbar fem-NPC 8×9-kollision och spawn-/key-/door-åtkomst, fri logisk X/Y-implementering med rättvis synlighet, S05 integrerad TIA-reg-/timing-konflikt player+white+gold key+orange P1 door+M0/PF, samt teknisk acceptansordning med oberoende Verification II efter separat uttrycklig ROM-auktorisation. **G5_FORMAL_OPEN; G0/G6/F12/ROM/VERIFICATION/PR_MERGE ej auktoriserade**, inga nya flicker-/osynlighetswaivers.


## MAIN VII G5W – B_OPEN_02 grafikstudie mottagen och offline-reproducerad; B-exakt kartval väntar (2026-11-17)

[Fullständig MAIN-G5W-käll-/reproduktionskontroll](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5W_MAIN_VII_G5V_B_OPEN_02_GRAPHICS_DELIVERY_RECEIPT_AND_MAP_DECISION_2026-11-17.md) · [Drive-kopia](https://docs.google.com/document/d/12cGLvJpFkHUl0jMu2blZIoKSksyo2o1dDeYwGgJq0X4/edit) · [G5V GRAPHICS II Issue #11](https://github.com/Odourman/let-me-out/issues/11). **GRAPHICS II har nu levererat B_OPEN_02-kandidaten**, MAIN har verifierat 18-fils-ZIP CRC + **17/17** SHA, kört om renderer **12/12 byteidentiska filer**, och separat BFS/2×2-geometri visade **565/565** nåbara ankare och **13/13** återanvändbara gamla geometriska B01-spawnankare. Detta är **endast source-only grafik-/geometribevis**, INTE riktig fem-NPC 8×9-hårdkollision, AI, key-/dörrintegration eller TIA-kernel. **LM-D17 godkänner sedan tidigare A_OPEN_01/C_OPEN_01/D_OPEN_01 som framtida exakta kartmål. B_OPEN_02 är ännu INTE användarbeslutad. B_OPEN_01 är inte godkänd.** Nästa användarval är exakt B_OPEN_02 med fryst JSON-blob `c32fc656fb5c60d16a5b73e4cea75f86df3e9621`. Ingen kartsource-/ROM-implementation eller fyrkartscutover följer av MAIN-mottagningen. **G5 formellt OPEN; G0/G6/F12/ROM, oberoende Verification och PR-merge INTE auktoriserade.**


## MAIN VII G5V – senare användargodkännande A/C/D exakta kartmål, B_OPEN_02 studiebeställning (2026-11-17)

[LM-D17/LM-D18 G5V:s exakta beslut](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5V_MAIN_VII_A_C_D_EXACT_OPEN_MAPS_USER_APPROVAL_AND_B_OPEN_02_GRAPHICS_ORDER_2026-11-17.md) · [Drive](https://docs.google.com/document/d/11BAB8skxf1EJH7PFXo1mdlZ7MDGMevmRS_eDlhPYikw/edit) · [Issue #11 GRAPHICS II B_OPEN_02, source-only](https://github.com/Odourman/let-me-out/issues/11). På MAIN:s uttryckliga tvådelade fråga svarade användaren **"Ser bra ut"**; **exakta framtida 40×22-kartgeometrier `A_OPEN_01/C_OPEN_01/D_OPEN_01` GODKÄNDA** inom senare versionens designmål, **inte genomförd fyrkartscutover eller ROM-pass**. **B_OPEN_01 ej godkänd**; separat GRAPHICS II **B_OPEN_02** studie är auktoriserad, men ny B-layout varken framtagen eller godkänd. Ursprungsfilernas grid, historiska tester och Git-blobbar bibehålls oförändrade. Tidigare "inga exakta v0.19-kartor godkända" gäller enbart tidigare tidssnapshot och supersederas specifikt för A/C/D.

**G5 fortsatt öppet:** B-kartexakt val, framtida fem 8×9-validerade spawnkoordinater, fysisk S05/TIA-rendering och separat teknisk arbetsorder. **G0/G6/F12/ROM/Verification/PR-merge inte auktoriserade.** Inga nya flimmer-/osynlighetswaivers eller R1/R2/PRNG-bevis.


## MAIN VII G5U – G5T grafikleverans PASS som offline-studie; exakt kartval förblir användarägt (2026-11-17)

[MAIN:s G5U-mottagning](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5U_MAIN_VII_G5T_GRAPHICS_DELIVERY_INTAKE_AND_MAP_CHOICE_RECOMMENDATION_2026-11-17.md) · [Drive-kopia](https://docs.google.com/document/d/1EO3QxZDqnQ9tnU4NMXoMTVUjbaRnx0parMdNfHInpOw/edit) · [GRAPHICS II:s issue #10](https://github.com/Odourman/let-me-out/issues/10). GRAPHICS II:s grafikstudie levererad på separat branch, MAIN har separat återkört **18/18 PNG byteidentiska**, validerat **7 040/7 040** kartceller och 8/8 GitHub-gridvärden. Gäller bara **reproducerbar visualisering**, inte oberoende ROM/VERIFICATION. MAIN rekommenderar nu **A_OPEN_01, C_OPEN_01, D_OPEN_01 som kandidater att erbjuda användaren**, men **B_OPEN_01 bör inte tyst låsas**; B01 historisk bas och eventuell B_OPEN_02 endast via nytt uttryckligt GRAPHICS-uppdrag. Exakta v0.19-kartor har **inte** godkänts, v0.11 ursprungsbasen oförändrad. G5S LM-D14/15/16 gäller framtida femfiendersmål men bestämmer inga startkoordinater/kartor. **G5_FORMAL_OPEN, G6/F12_NOT_AUTHORIZED, NO_ROM, NO_PR_MERGE, NO_NEW_VERIFICATION.**


## MAIN VII G5S – uttryckligt godkännande C1+D1+E1, övriga spärrar kvar (2026-11-17)

[Fullt senare användarbeslut LM-D14/15/16](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5S_MAIN_VII_C1_D1_E1_USER_APPROVAL_DECISION_RECORD_2026-11-17.md) · [Drive](https://docs.google.com/document/d/1UboARrqu3sFHQgeV1y5C0IWoRkSlvAY_6b6RMLWwbnE/edit). Användaren svarade **"Fortsätt Följ dina egna rekommendationer"** omedelbart efter MAIN VII:s uttryckliga fråga om att godkänna **C1, D1 och E1 som framtida spel- och testregler**. Dessa tre är därför **GODKÄNDA inom sina exakta framtida scopes**: framtida R1 fem/R2 fyra+nyckel med fryst historisk v0.18 R1 sex/R2 fem+key; -30 poäng per kill i fem-NPC-version med oförändrat event-nollgolv; fem distinkta förhandsvaliderade starter + uniform 1/5 key-bärare per instans. **LM-D12/A1 och LM-D13/B1** redan godkända. Tidigare sektioner "C/D/E väntar" är historiska och gäller inte efter detta beslut.

**Fortfarande obeslutade och därför SPÄRRADE:** specifika v0.19 OPEN-kartor; exakta spawn-koordinater/PRNG; nya generella flimmer-/osynlighetswaivers; S05 och G0 TIA-resurskonflikten samt en versionssatt teknisk acceptance. **G5 formellt OPEN. Inget G6/F12/ROM, ingen ny oberoende Verification eller PR-merge får påbörjas utan egen uttrycklig auktorisation.**


## MAIN VII G5R – score/nollgolv validerade source-only, designregler väntar (2026-11-17)

[G5R-underlag direkt från Master Spec+57 beslut](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5R_MAIN_VII_FIVE_NPC_REBASELINE_SCORE_SPAWN_DECISION_READINESS_2026-11-17.md) · [210 poängfall](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5R_FIVE_NPC_SCORE_FLOOR_210_CASES_SOURCE_ONLY_2026-11-17.csv) · [Drive-kopia](https://docs.google.com/document/d/12qJI35fQIdvHQHJi5LbXMvNMmCOxNHaceKzI5GpxALM/edit). **A1+B1 är redan användargodkända.** Nytt aritmetiskt källfynd (inte spel-ROM): fem fiender och -25 original ger repeterbar +25 all-kill-farming; föreslaget -30/kill ger fem all-kill-rum från noll `150,150,150,150,150` och behåller originalets avsiktliga nollgolv. **-30 ännu INTE beslutat:** ursprungliga 043 står kvar tills uttryckligt användargodkännande. Samma krav gäller framtida testbas C1 (R1 5, R2 4+key; gamla ROM-acceptanser frysta), fem-start/1/5-bärare E1 och exakt kartval. Allmänt "fortsätt, följ rekommendationer" användes bara till G5 source-only-beredning, inte till tyst canonändring. Ingen automatisk implementeringsauktorisation, inga nya G0/G6/F12, ROM, Verification eller PR-merge; S05 kvarstår.


## MAIN VII G5Q A1+B1 – godkända mål men G5 tekniska/övriga grindar fortfarande öppna (2026-11-17)

[Användarbeslut LM-D12/13](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5Q_MAIN_VII_A1_B1_USER_APPROVAL_DECISION_RECORD_2026-11-17.md) · [Drive-kopia](https://docs.google.com/document/d/1Yh5XfKZ8f9rm97sG7jY8tAjuGiV-0o9O-d9oy-BkP2s/edit). Användaren godkände genom omedelbart svar "Följ dina egna rekommendationer" **endast G5Q A1+B1 som fortsatta designmål**. **A1:** fri **logisk** fem-NPC X/Y och trovärdig fyrvägs-jakt utan tyst permanent Y-lane. **B1:** identifierbara NPC, rättvist synliga hot, synlig key när ingen verklig pixelöverlapp föreligger. O1/LM-D06:s begränsade giltiga tillfälliga pixelöverlapp står kvar. **Ingen** generell flicker-/occlusion-waiver, 10Hz, ny faktisk TIA-kernel eller full 2600-feasibility påstås här.

G5Q:s nedanstående tidigare avsnitt "förslag, inget godkännande" beskriver läget **före detta direkta användarsvar** och får inte användas för att förneka A1+B1. **Separata C/D/E-punkter är fortsatt obeslutade** (framtida R1/R2-rebaseline, score, spawn/key-bärare och karta). S05 och G4/G5P:s G0-inkonsistens återstår. **G5_FORMAL_OPEN, G6/F12_NOT_AUTHORIZED, NO_ROM, NO_VERIFICATION, NO_PR_MERGE.**


## MAIN VII G5Q – uttryckligt G5-designmål krävs; förslag är inte canon (2026-11-17)

[G5Q-beslutsförslag](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5Q_MAIN_VII_DECISION_READY_DESIGN_TARGET_AND_PRE_G6_BOUNDARY_2026-11-17.md) · [officiell Drive-kopia](https://docs.google.com/document/d/1_bB-F6pvwEehRP09F1jdfyYnUtKo4c6mie4QD3c9YGw/edit). **G5Q är en användarbeslutsberedning, inget nytt godkännande.** MAIN rekommenderar A1 (fri logisk NPC-X/Y med ursprunglig jakt och utan hård permanent Y-lane) och B1 (kvalitetsmål: fem ursprungliga NPC läsbara, farliga NPC ej systematiskt dolda, key aldrig dold enbart för same-Y utan faktisk bitpixelöverlapp). G5P:s mjuka/fri-modellers ~498,6/900 bortprioritering är **syntetisk köbelastning, inte fysisk flicker** och ger ingen generell waiver. O1/LM-D06 redan godkänt men begränsat. Separata userbeslut återstår om formell fem-NPC R1/R2-bas, -30 kontra -25, 1/5 bärare/femspawn och exakta v0.19-kartor. G4 H4-ONE och G5P:s snävare G0-proposal är ännu inte samma definierade testorder. **Ingen G5-PASS, inga ändrade spelregler, ingen G6/F12/ROM/VERIFICATION/PR-merge.**


## MAIN VII G5P-mottagning – source-only reproduktion PASS, formell G5 ÖPPEN (2026-11-17)

[MAIN VII:s mottagnings-/reproduktionsrapport](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5P_MAIN_VII_RESEARCH_DELIVERY_INTAKE_AND_REPRODUCTION_2026-11-17.md) · [Drive](https://docs.google.com/document/d/1HzRq0wJlX8iZPZsxeDRWpQenMI5eveAr9lIgfTNICSA/edit) · [RESEARCH II:s underlag](https://github.com/Odourman/let-me-out/blob/research/g5p-adaptive-y-offline-20261117/docs/research/G5P_RESEARCH_II_FULL_REPORT_2026-11-17.md). Råfiler 672 huvudfall + 168 globalfall + 12 historiska replay verifierades; Pythonkörning gav **sex byteidentiska CSV** och ZIP-manifest/CRC PASS. Källkartornas grid 8/8 matchar live GitHub. **Detta accepterar endast reproducerbarheten hos rådgivande offlineforskning, INTE en TIA-kernel eller oberoende Verification.** G5P visar fortsatt svagheter med hård Y-lane, och mjuk Y ger förbättrad AI men stor syntetisk same-Y-synlighetsbelastning. Fri logisk X/Y med situationsberoende visuell planering är en **kandidat**, inte godkänd policy. S05 och kvantifierade synlighetsgarantier olösta; O1 endast godkänt vid faktisk NPC/key-pixelöverlapp. `-30`/kill, 1/5-key/spawn, framtida R1/R2-bas och exakta v0.19-kartor fortfarande användarägda beslut. **G5 formal ej avslutad; G6/F12/ROM, oberoende Verification och PR-merge ej auktoriserade.**


## MAIN VII G5P – source-only RESEARCH II-order, formell G5 fortsatt spärrad (2026-11-17)

[Preciserad G5P-instruktion](https://github.com/Odourman/let-me-out/blob/main/docs/research/G5P_MAIN_VII_TO_RESEARCH_II_ADAPTIVE_Y_POLICY_STUDY_ORDER_2026-11-17.md) · [öppen specialistuppgift #9](https://github.com/Odourman/let-me-out/issues/9) · [Drive](https://docs.google.com/document/d/1NHYV4EVnJyce19DCyFHFA_bEk5UMKHlN9okugkeyDxc/edit). MAIN har **bara** beställt en rådgivande jämförelse, inte fått RESEARCH II:s rapport. Nya testmått kräver kollisionskorrekt jämförelse; G5O:s <=1 av 5 nära spelarankare är delvis inneboende i en två-gridraders Y-separation och ingen självständig design-NO-GO. Bevara faktiskt negativa B01-stallfall och rådata. Inga nya rendering-/Y-/AI-/flickerregler, score -30, femspawn, R1/R2-rebaseline, kartbyte, G0/G6/F12 eller ROM får antas från denna order. O1 begränsat godkänt, S05 kvarstår tekniskt olöst. **G5 formell användargrind fortfarande ÖPPEN.**


## MAIN VII G5O – negativt source-only-strikt-lane-dynamikprov (2026-11-17)

[G5O/MAIN:s 12-scenariers test](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5O_MAIN_VII_STRICT_S1_Y_LANE_DYNAMIC_CHASE_NEGATIVE_SCREEN_2026-11-17.md) · [CSV](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5O_HARD_LANE_GREEDY_CHASE_12_CASES_SOURCE_ONLY_2026-11-17.csv) · [Drive](https://docs.google.com/document/d/12RG0YNpimCiY64gVTFYpaPzrjTYDXnLMfUONPYjLDqQ/edit). Den hårda S1-regeln `abs(grid_y_i-grid_y_j)>=2` för fem 9-raders NPC ger vid en enkel 2×2/BFS-girig modell högst en nära stillastående spelaren efter 180 ticks i 12/12 v0.11-kart-/målscenarier, B01 startspelarankare 0/5. **Det är en negativ MODEL SCREEN, inte allmängiltig S1-NO-GO, inte spelets riktiga AI/ROM/Stella.** En stabil femstart (G5N) räcker inte för spelbar jakt. MAIN rekommenderar att ingen hård S1-Y-restriktion canoniseras förrän RESEARCH II rådgivande bedömt adaptiv Y-planering och/eller synligt specificerad temporär multiplex/flimmer. Originalbeslut 008/019–025/032–034 får inte tyst ändras. **Formell G5 och score/spawn kvar; G6/F12 ej auktoriserade.**


## MAIN VII G5N – nya initiala start-/spelsystemfynd, utan auktorisation (2026-11-17)

[Full G5N source-only-rapport](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5N_MAIN_VII_S1_FIVE_NPC_LANE_START_AUDIT_AND_SCORE_PROPOSAL_2026-11-17.md) · [Drive-kopia](https://docs.google.com/document/d/1oVeMuwiwUrvzQrNBBd-aMUVHxnj5HiGgDWBPesy1CTQ/edit). **G5-S1 prövas som rekommenderad huvudkandidat**, inte som beslutad Y-lane gameplay. En deterministisk 2×2-grid-/BFS-enumerering av *endast v0.11:s historiska A01/B01/C02/D01* visar 2 208/48/1 248/420 möjligheter till fem startpunkter med parvis skilda 9-raders grafikband. Ingen dynamisk jakt, nyckelåtkomst, 8×9-hårdvarugeometri eller 2600-kernel är därmed verifierad. G5N föreslår -30 per kill för att undvika framtida +25 all-kill-farming, och fem validerade spawns/1/5 key-bärare; allt väntar på särskilt användarbeslut. **O1:s godkända faktiska överlappningsscope och alla G5/G6-spärrar oförändrade.**


## MAIN VII RÄTTELSE TILL G5:s O1-FORMULERINGAR, 2026-11-17

**Det senare uttryckliga användarbeslutet O1 är redan giltigt**, trots att några nedanstående MAIN VI/G5L-avsnitt felaktigt benämner det preliminärt. Se [O1-beslutet med ordagrant användarsvar](../MAIN_STATUS_NEXT_10_2026-11-15.md), [LM-D06 GODKÄNT](../MAIN_DECISION_LEDGER_SUPPLEMENT_2026-11-15.md) och [korrigendum](../project_sources/PROJECT_SOURCES_MAIN_VII_CORRIGENDUM_2026-11-17.md).

O1 tillåter tillfällig skymning av nyckel **vid verkligt android/nyckelöverlapp** utan ändrad logisk position/upptagning. Mindre, tillfälligt flimmer är acceptabelt kvalitativt; **inte** kvantifierad 10Hz, systematisk same-Y-occlusion eller dold nyckel när ingen verklig överlappning finns. Godkänd O1 får **inte** användas som ersättning för den fortfarande olösta G5-S0/G5-S1/G5-S2-kernelpolicyn.

**Övriga G5-spärrar fortsätter oförändrat:** formellt val av Y-rörelse/synlighetsgarantier utöver O1 och femfiendersscore/spawn saknas. Ingen G6/F12/ROM/ny verifiering/PR-merge är auktoriserad av denna rättelse.

**2026-11-17 · MAIN VI. Status: `G5_USER_DECISION_PENDING_NO_CANON_CHANGE`.**

Detta är en styrning av vad *inte* får påbörjas till följd av teknisk feasibility-granskning. [Fullständiga käll-/risk- och vägvalsbedömningen](G5_CANDID_FEASIBILITY_ASSESSMENT_AND_DECISION_BRIEF_2026-11-17.md) är separat och normativ som **MAIN:s rekommendation**, men **inte ett nytt användarbeslut**.

## 0H. G5M ny fem-fienders följdkonsekvens: score och nyckelbärarslump kräver eget uttryckligt beslut

[**G5M full källbaserad analys av 57 beslutsrader**](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5M_FIVE_NPC_GAMEPLAY_SCORE_KEY_CARRIER_AND_SPAWN_DEPENDENCIES_SOURCE_ONLY_2026-11-17.md) · [Project Sources-revisionspaket index](https://github.com/Odourman/let-me-out/blob/main/docs/project_sources/PROJECT_SOURCES_REVIEW_PACK_2026-11-17.md) · [officiell Drive ZIP](https://drive.google.com/file/d/1Pv0TUKoN3QVu-Yy8UZFOhlv7OgoGOQit/view). Efter uttryckt arbetsmål **5** i stället för originalets **6** visar originalpoängreglerna 042–047 en **ny potentiellt blockerande spelbalansändring**: normalt långsiktigt all-kill `-25*6 + 50+100=0`; fem blir `-25*5 +50+100=+25` per rum om nollgolv inte ingriper. Beslut 047 hade avsikten att all-kill inte gav långsiktig highscore-tillväxt. Vid första rum/nyckelupptagning före sista kills gäller nollgolv och händelseordning, inte dessa nettoformler automatiskt. Original 021 sex slumpade prevalidated spawn och 022 1/6 uniform bärare behöver framtida, **inte tyst gjord**, omprövning till fem positioner och 1/5 uniform sannolikhet.

**G5 FORMAL** har nu TVÅ separata användarägda beslutsklasser: (i) Y-/synlighets-/grafik-kernelpolicy (G5L), (ii) fem-NPC-poängbalans, bärar- och spawn-revision (G5M). Båda måste senare skrivas in i nytt versionerat scope/acceptance om användaren godkänner dem. **Inget av dem följer av "fortsätt"**, och ingen G6/F12-kodorder, ny VERIFICATION eller PR-merge får utges. Sourcepaket är navigation-only.

## 0G. G5L TEKNISKT EXIT-PAKET – sista kvarvarande USER-valet, INTE nästa G6 (2026-11-17)

[GitHub: avslutande G5L source-only 30 tricks/3 arkitekturer/10 nyckel-dörr stressfall](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5L_FINAL_TECHNICAL_EXIT_30_TRICKS_R1_R2_DOOR_KEY_AND_USER_DECISION_2026-11-17.md) · [fullständig Drive-kopia i officiella projektmappen](https://docs.google.com/document/d/1zbusyasMrLlO4zIp3iq8iplr8cvjvlAvbcgkDATOi38/edit) · [10-scene CSV](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5L_SAME_Y_KEY_DOOR_ENEMY_RENDERING_STRESS_2026-11-17.csv). **G5 technical source-only research COMPLETE, G5 formal decision PENDING**. Ingen ny generell five-NPC same-Y+key/door G0 kernel. Berzerk Y-lane och vår P0/P1 door-hybrid är lovande *enbart som villkorad designförändring*; när key och vit robot är på samma door-Y fordras P0=player+robot+key om P1=door och den föreslagna fasta 1-P1-policyn upprätthålls. Även O1 nyckelskymning är dokumenterad som **preliminär MAIN-policy, inte användarcanon**, så kan inte användas för att dölja icke-pixelöverlappande key.

**En enda återstående G5-designfråga:** tillåter användaren Y-arbitrering så att fem fienders 9-fysiska-radersband inte överlappar, med konsekvenser för rörelse/AI; eller skall de kunna röra sig helt fritt i Y utan automatisk flicker? Det finns ingen implicit waiver. **G6/ROM DEVELOPMENT III/independent VERIFICATION II behöver separata explicita arbetsorder oberoende av detta val.**

## 0F. G5J/G5K verklig Berzerk-källa och förberedd dynamisk kanal-arkitektur, Y-policy EJ GODKÄND

[Den kommenterade historiska källan analyserad, G5J](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5J_BERZERK_PRIMARY_SOURCE_LANE_KERNEL_AND_FIVE_NPC_SCOPE_OPTIONS_SOURCE_ONLY_2026-11-17.md) · [dynamisk P0 player/robot ↔ P1 orange door, G5K](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5K_BERZERK_LANE_DYNAMIC_P0_P1_DOOR_R1_R2_SOURCE_ONLY_2026-11-17.md). Berzerks 8 robotar använder Y-start med gap och rörelsekontroller, inte 8 same-Y 8bitars originalsprites. En **fram­tida** möjlig Atari 2600-renderer kan ha fem logiska NPC i Y-lanes, och per dörrband låta P0 hålla player+vit NPC medan P1 förblir R3-orange/black-hole. Offline 176 scanlines max P0 två/P1 ett, men **inte** ROM-pass. En sådan *Y-begränsning* av fienders frihet/AI är en uttrycklig användarägd canonändring; VARKEN den, key-O1, flimmer-/occlusionpolicy eller G6/F12 har blivit godkända genom användarens "fortsätt". Historiska v0.18 six-R1/5+key-R2 oförändrade. **Slutsats:** G5 källforskning konkret förbättrad och avslutad inom nytt G5J/K scope; FORMAL G5 fortfarande PENDING, G6 spärrad.

## 0E. G5I plan-/auktoritetsavstämning – felaktigt G5→G6 förhindrat (2026-11-17)

[Versionsstyrd G5I avstämning och framtida femfienders R1/R2 acceptance-delta](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5I_PLAN_RECONCILIATION_FIVE_NPC_DECISION_READY_NOT_G6_2026-11-17.md) · [fullständig officiell Google Drive-kopia](https://docs.google.com/document/d/1Zc-n5K-RHRZ5YriInxyQBqmb99siXl44547cVteT1YI/edit). G1–G4 avslutade som read-only/source-only underlag, G5:s tekniska feasibility-analys och G5F/G5G/G5H-delstudier utförda och dokumenterade. **G5 FORMELLT beslut om testkrav/visuell policy och eventuell 6→5 cutover fortfarande PENDING**; gammal R1 sex / R2 fem+nyckel gäller tills en riktig userauktoriserad rebaseline. Användaren har redan uttryckt Atari 2600, fem (M,M,F,SM,SF), svart bakgrund och nyckelhål som del av orange port – fråga inte om dessa preferenser på nytt. Utan explicit waiver för flicker/occlusion skall gamla synlighetskrav inte försämras i smyg. **"Fortsätt om klar" är villkorat, inte en separat specificerad G6 ROM-uppdragsorder.** Inga G6/F12/Gameplay/Verification eller nya masker inledda.

## 0D. G5H 24/36 ordningar, gräns för direkt-GRP/RESP-kernel (2026-11-17)

[GitHub G5H käll-/registeranalys](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5H_START_GRP_RESP_NUSIZ_SAME_Y_SOURCE_ONLY_DECISION_2026-11-17.md) · [Google Drive fulltext plus CSV](https://docs.google.com/document/d/1rsRlR4BOjXnY9Wtsp1N3Oq_02yGVMiAKD6Z3UhFa4Q4/edit). Vid fem fiender med originalmasker och orange P1-port räcker source-only direkt `GRP/RESP`-sekvens inte i fria worst-case-X: originalrad6 A 79/76 i alla 24 P1-ordningar, B bästa 74/76 bara om samma M-M intill, B 79/76 när player mellan två M, upp till 89/76 i uttryckligt hypotetiskt gult M0-stressfall. Ingen fysisk G0/ROM-pass, inga ROM-ändringar. Varken tidigare R1 sex, R2 fem + key eller G5 användarens slutliga designval har reviderats. Ytterligare experiment/implementation G6/F12 kräver separat uttrycklig auktorisation; RESEARCH II kan enligt MAIN studera NY kernelfamilj source-only.

## 0C. G5G ny teknikforskningskandidat; källmässigt naiv 6507-direktsekvens FAIL

[GitHub hela G5G-rapporten](../gates/G5G_BALL_LEFT_WALL_AND_FIVE_NPC_OPCODE_CENSUS_SOURCE_ONLY_2026-11-17.md) · [maskinläsbar 9-scenario CSV](../gates/G5G_DIRECT_EVENT_CPU_CYCLE_CENSUS_2026-11-17.csv) · [Google Drive-kopia i projektmappen](https://docs.google.com/document/d/14sNkAi8gdLqz2wo6OtR9jrpTggrcXB0cv-BCO3onaWY/edit). Teknik: reflektions-PF plus `Ball` 4CC i brunt vid x0 **endast på dörrbandet** när PF0=0, P1 samma orange bitmask med negativt svart keyhole, COLUBK svart. PF+BL 3520/3520 logiska kartceller PASS **endast offline**; BL-positionering, door P1+vit NPC same-Y, M0 och X/Y START-tider INTE mätta.

A/B:s enkla direkta 6507-instruktionsmodell på stadig dörrrad **79/76** (PF0-right toggle tidigare **89/76**); själva Ball/PF-radövergången ökar modellen till **89/76**. **NAIVE PLAN FAIL**, inte 2600 hardware NO-GO; full fysisk G0 ej godkänd och ROM IMPLEMENTATION EJ AUKTORISERAD. Befintlig användarcanon för historiska R1/R2 testantal samt övriga G5-val förblir spärrad i avvaktan på separat explicit användarbeslut.

## 0B. G5F source-only fem-NPC/REF PF baserad på faktisk källanalys, INTE en kodorder

Efter användarens "Ok, fortsätt" färdigställde MAIN VI [G5F source-only arkitekturrevision](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5F_FIVE_ANDROID_REFLECTED_PF_DOOR_SOURCE_ONLY_ARCHITECTURE_2026-11-17.md) och [Drive fullständigt underlag](https://docs.google.com/document/d/1PAELvVABaDAVuhZILC1Czo5kEIiRGQV2IaZ1bdtKRNw/edit). Alla fyra kartor speglar vänsterhalvan på 18/22 rader, endast dörr x39/y9–12 avviker. Förslaget är `CTRLPF.REF`, latched återbruk av väggdata, eventuellt PF0-only högersidig override på dörrlinjerna samt befintligt P1-dörrmotiv med svart utskuret nyckelhål. 5-NPC-maskradlast 3/3/5/5/5/5/5/5/3; F11 och P0/M0-färgkonflikter kvarstår. **Ingen G6/ROM-implementationsorder, ändrad v0.18-acceptans eller ny teknisk PASS följer av denna dokumentation.** Formellt G5-beslut, fem-NPC cutover av historisk R1/R2 och eventuella visuella waivers är fortfarande användarägt.

## 0A. Ny användarinitierad fem-NPC- och Video Chess-forskningskandidat (2026-11-17)

[GitHub dokument med användarens femandroidsförslag, Berzerk-jämförelse, och Video Chess/Venetian Blinds för guldnyckel + högerdörr](../MAIN_VI_FIVE_ANDROID_BERZERK_VIDEO_CHESS_RESEARCH_DIRECTION_2026-11-17.md) · [arkiverad Google Drive-kopia](https://docs.google.com/document/d/1Iv9XrYt3CvkPNhiCGxSgEQSe0M91SHa4CHIjqP6YAA8/edit). Exakt kandidat: **2 large M + 1 large F + 1 small M + 1 small F = 5** (mot frysta 2M+2F+SM+SF=6). R2 blir hypotetiskt 4 kvarvarande NPC + nyckel om antalet ändras. Kandidat för nyckel/dörr: pröva omväxlande scanlines NÄR de ligger på samma höjd; jämför först med enkel Y-separerad spriteåteranvändning och PF-buren dörr. Tidigare android-Venetian-negativfall är inte automatiskt key/door-negativfall.

**Auktoritet:** användaren bad att minnas och arkivera förslagen, **INTE** uttryckligen att fastställa ny canon eller utfärda kodorder. Originalantal 6, R1/R2 acceptans, fyra 8×9 TOP-DOWN-masker och G5 PENDING USER kvarstår. Varken G6 eller någon annan implementation är beslutad.

## 1. De två möjliga framtida produktbesluten
**A – Atari 2600, ny visuell renderingspolicy.** Behåll sex logiska individuell X/Y NPC, fyra typers originalidentiteter, gul spelare, en projektil, fyra rum, högernyckeldörr, O1/K1/E1, poäng, liv, RESET-only och spelkänsla **som mål**. Användaren måste *se och uttryckligen godkänna* den föreslagna policyn för hur många NPC som får saknas/flickra/occluderas på överbelastad same-Y-rad och exakt vad original8×9-krav ska betyda för en överlagrad grafisk framställning. Varken ändrade exakta rumsrutor, begränsad NPC Y-mobilitet, annan dörrfärg eller reducerat antal NPC följer automatiskt.

**B – originalambition bibehålls, plattformsbyte till Atari 7800/MARIA.** Användaren behöver uttryckligen bestämma att Atari 2600-målmaskinen överges som leveransplattform. Exakta originalmasker, sex fria X/Y, fullfärgsguldkey och orange/black dörr blir då vidareförda designmål; 7800-renderingen och ROM/gameplay måste nyutvecklas separat och är inte verifierad ännu. Standard-F6-DASM/2600 TIA-resultat är forskningshistoria, **inte** en färdig 7800 implementation.

Den tidigare G4-"villkorad GO" för EN mikrofysik-uppgift är en **alternativ forskningsmetod om användaren önskar testa originalspecen lite till**, inte ett tredje automatiskt produktbeslut. Ett lyckat mikroprov har INTE visat sex NPC eller guldkey/door samtidigt; inte heller ska ett misslyckande automatiskt ändra canon.

## 2. Frågor som kräver uttrycklig framtida användarformulering
- Vilket är absolut viktigast: **Atari 2600 som hårdvara** eller **alla nuvarande samtidiga originalgrafikregler**?
- Om A väljs: exakt **flicker-/occlusion-policy** och vilken minsta läsbarhet som krävs, särskilt sex same-Y och gameplay-/collision-invariant, baserat på synliga testklipp innan godkännande.
- Om B väljs: uttryckligt målmaskins- och scopebyte; nytt ROM- och oberoende verification-upplägg.
- Om användaren vill fortsätta exakt 2600-forskning: explicit separat mikro-G6-order enligt [G4 DRAFT_NOT_AUTHORIZED](G4_FUTURE_SINGLE_MICROPROBE_ORDER_DRAFT_NOT_AUTHORIZED_2026-11-17.md), med **G0 före bygg**, bounded exit och ett förhandsgodkänt kostnadsstopp.

**Nej till tysta antaganden** om "lite flimmer" = 10 Hz för en NPC, F6SC/ARM löser sprites, ändring 6→4 NPC, att nyckeln får vara brun eller att den vänstra väggen får öppnas.

## 3. Aktuell auktorisation och tekniskt tillstånd efter G5-analysen
| Del | Nuvarande faktiska status |
|---|---|
| **G1–G4** | Dokumentation/evidens/source-only analyser färdiga, ej ROM-PASS |
| **G5 feasibility-analys** | COMPLETE – ärlig 2600 produktplan bedöms **NO_GO med samtliga exakta krav samtidigt** (ingen universell omöjlighetssats) |
| **G5 val av canon/teknisk väg** | **PENDING USER DECISION** – inte godkänt/inte färdigt |
| **G6 nytt ROM-mikroprov/F12** | **NOT AUTHORIZED / NOT ORDERED** |
| **Full R1 och R2–R4** | BLOCKED / NOT ACCEPTED |
| **PR #7** | DRAFT, UNMERGED |
| **Issue #8** | Oberoende äldre fryst E02-baslinje, ej ny G5/future-ROM |
| **Andra projekt eller annan cartridge-mapper/PAL/fullspel** | INTE auktoriserade inom detta steg |

## 4. MAIN:s styrrekommendation
**Gör inget flerförgrenat F9–F12-probe-svep.** Pausa ytterligare grafikkernel-forskning tills användaren har valt vilken kompromiss de föredrar, eller har uttryckligen avgränsat att de vill lägga **EN sista** forskningsmikro på bevisning trots att det inte garanterar ett spel. Inga fullspelsfunktioner skall byggas i förtid mot en oföränderlig icke bevisad spritekernel.

**Bevara hela originalet.** Originalets 57 beslut och skisser, senare LM-D/Issue6, alla frysta ROMs, G1–G4 underlag och G5-bedömningen kvarstår oförändrade. Ingen gamla positiva/negativa bevis raderas. Huvudchattens nästa verkliga uppgift efter ett användarbeslut är ny, uttryckligen begränsad roadmap och separat rollordrade prov.

*Dokumentattest: MAIN VI, rådgivande produkt-/feasibility- och authority-gräns, inte användarsignerad canon.*
