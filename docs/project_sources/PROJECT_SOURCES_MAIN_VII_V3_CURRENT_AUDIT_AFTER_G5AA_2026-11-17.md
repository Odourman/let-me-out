# LET ME OUT! – MAIN VII V3: samlad GitHub-, Google Drive- och Project Sources-revision

> **G5AB INVENTERINGS-/REVISIONSSNAPSHOT, INTE EN STÄNDIGT LEVANDE STATUSKÄLLA.** Kontroller 174 main-trädposter och 247 Drive-objekt gällde vid granskningstillfället, före senare dokumenttillägg. Aktuell ingång är [CURRENT_AUTHORITY_STATUS_AND_WORK_QUEUE.md](https://github.com/Odourman/let-me-out/blob/main/docs/CURRENT_AUTHORITY_STATUS_AND_WORK_QUEUE.md). Detta dokument behålls för metod/proveniens och går inte att läsa som ett nytt ROM-mandat.

**Datum:** 2026-11-17, efter MAIN:s mottagning av G5Z/G5AA.
**Klassning:** `MAIN_VII_G5AB_SOURCE_AUDIT_COMPLETED_SOURCE_ONLY`. **Ej** ny spelcanon, ROM-kod, testkörning, G1/G6/F12-auktorisation, merge eller oberoende Verification II.
**Fortsättning inom MAIN:s befintliga source-only-mandat:** [G5AC – förregistrerad framtida TIA-kalibreringsfråga, EJ AUKTORISERAD](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AC_MAIN_VII_TIA_PHASE_CALIBRATION_DECISION_READY_NOT_AUTHORIZED_2026-11-17.md). Inga nya ROM- eller specialistordrar.

## 1. Faktiskt granskade ytor och vad granskningen INTE är
- **GitHub:** https://github.com/Odourman/let-me-out. Trädet på main var **`ad84d142fcda58048ccef7418ff3e03b6bcad1ab`**, **174 tree-poster**, `truncated=false` vid inventeringen. Jag läste direkt relevanta original i `docs/gates`, `design`, historiska MAIN-källor, roller/överlämningar, grafik-/ljudstatus och PR/Issue-metadata. Källinnehåll och specialistresultat i frysta branches kontrollerades separat där de var avgörande för senaste läget. **Jag hävdar inte manuell djupgranskning av varje GitHub-dokument**.
- **Google Drive:** https://drive.google.com/drive/folders/1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u, **247 objekt** i faktisk folder-listning: 94 native Docs, 70 ZIP, 30 Markdown, 21 PNG, 9 GIF, 9 JSON, 8 PDF, 4 CSV, 2 text/plain. Jag verifierade live metadata/projektmapp för ursprunglig användarhandoff och senare original/källkopior, läste nyaste G5Z/G5AA-dokument och identifierade arkivens källvägar. **Detta är full inventering, inte ny bit-/CRC-kontroll av samtliga 247 filer**.
- **ChatGPT Project Sources:** `files.list` visade exakt **sex aktiva project-backed** källfiler med namn `00_LAS_FORST.md` … `05_G5_BESLUTSGRIND_OCH_G6_FORBEREDELSE.md`. **Alla sex texter lästes direkt** i detta projekt. Andra historiskt genererade `00..`-filer är inte aktuella `source_kind=project`.
- **Master Spec/57 ursprungsbeslut:** [ursprungliga Drive-handoff ZIP](https://drive.google.com/file/d/1mqU07Q7xTgU5t5lYQhCOyI7wRQl6vD7o/view) fortfarande i officiell mapp, 738586 B. [G1 auktoritets-/råarkivgranskning](../gates/G1_AUTHORITY_DIFF_2026-11-17.md) dokumenterar 21 arkivfiler, 57 beslut 001–057 och tidigare SHA-/CRC-kontroll. **Jag har inte påstått att jag i just denna revision extraherat hela original-ZIP på nytt**. Dessa original gäller tills senare uttryckligt användarbeslut ersätter exakt sakområde.

## 2. Faktiskt gällande framtida spel- och kartbeslut
[LM-D12/D13](../gates/G5Q_MAIN_VII_A1_B1_USER_APPROVAL_DECISION_RECORD_2026-11-17.md): fem individuell **fri logisk X/Y** (fyra riktningar, inte hårt begränsade Y-lanes) samt korrekt synliga hot/nyckel utan generellt same-Y-fusk.

[LM-D14–D16](../gates/G5S_MAIN_VII_C1_D1_E1_USER_APPROVAL_DECISION_RECORD_2026-11-17.md): framtida fem NPC **M,M,F,SM,SF**, R1 fem, R2 fyra+synlig key efter bärares dödsanimation, `-30`/kill (score floor per event), övriga +50 pickup/+100 exit/+15 per survivor, fem **ännu inte faktiskt 8×9-validerade** framtida spawnpositioner på varje rum, 1/5 likformigt per individuell keyholder. Vid startsaldo 0 kan fem kills före pickup klampas till score 0 och därefter ge +150 efter key+exit, trots att den oklandrade formeln för högt saldo ger 0/rum vid fem kills; skillnaden är avsiktlig score-floor-eventmatematik, inte bevisat gameplay i ROM.

[LM-D17/LM-D19 G5X](../gates/G5X_MAIN_VII_B_OPEN_02_EXACT_USER_APPROVAL_AND_FOUR_MAP_BASELINE_DECISION_2026-11-17.md), [källpinnat manifest](../gates/G5X_MAIN_VII_APPROVED_FUTURE_FOUR_MAPS_SOURCE_MANIFEST_2026-11-17.json): fyra framtida **exakta 40×22** layoutmål **`A_OPEN_01`, `B_OPEN_02`, `C_OPEN_01`, `D_OPEN_01`**. Historiska v0.11 A01/B01/C02/D01, test-ROM, originalblobbar och negativa tester bevaras. Source-only G5T/G5V-bilder och 2×2 BFS-ankare är inte riktig PF/8×9-collision/ROM-Stella proof. MAIN återkörde G5T med **18/18 byteidentiska PNG** och G5V med **12/12 byteidentiska genererade filer**, inklusive PNG och JSON.

[O1 LM-D06](../MAIN_STATUS_NEXT_10_2026-11-15.md) ger kortvarig key-skymning **endast vid faktiskt bitpixelöverlapp** med NPC; tillfälligt mindre flimmer kvalitativt accepterat, men ingen 10Hz-/same-Y-/systematisk NPC/key-osynlighet.

## 3. Tekniska sanningen efter G5Z
- [G5Z ROM DEVELOPMENT III:s fulla frysta originalrapport](https://github.com/Odourman/let-me-out/blob/8c7cef622ebaa6543a3f044ddf50d21024b1b978/rom/g5z_g0_h4_one/TO_MAIN_G5Z_G0_H4_ONE.md) på separat, **inte mergad** branch.
- [MAIN VII G5AA separat källmottagning](../gates/G5AA_MAIN_VII_G5Z_G0_INCONCLUSIVE_SOURCE_ONLY_RECEIPT_AND_NEXT_DECISION_2026-11-17.md): av användaren godkänd **enda** H4-ONE G0 är **fullföljd** med `G0_INCONCLUSIVE_NO_ROM`, INTE `G0_SOURCE_PLAUSIBLE` eller ny fysisk G1. 72/72 mask-/nominella CC-matrisrader stämmer. Den begränsade opcode-mallen 58/68c (+clear/NUSIZ villkorliga 74/79c) saknar dynamisk X-scheduler och TIA-effect START/RESP/GRP/NUSIZ0/M0-timing, är **inte** en exekverbar kernel.
- [G2 negativa och nonrepeat](../gates/G2_NEGATIVE_TESTS_AND_NONREPEAT_RULES_2026-11-17.md) gäller fortsatt: R1ba orienteringsfel trots 600/600, F11 source-only FAIL för sin fyra-P1-numeriska allokering, F9 **tre binära** korrekta NPC-mask-/X-val i en ROM men inte fri numerisk X; R1f/R1g historiskt M0 på föregående rasterrad. **Fysiska fullspelspåståenden är inte styrkta**.
- [G5H](../gates/G5H_START_GRP_RESP_NUSIZ_SAME_Y_SOURCE_ONLY_DECISION_2026-11-17.md): förenklad fem-NPC-direktsumma **79/76** i worst order och **74/76** i särskilt gynnsamt fall före övriga register/deadlines, **inte** universell omöjlighet eller en ROM-PASS.
- **S05** är fortfarande separat olöst: gul player, vit NPC, guldkey, orange P1-högerdörr med svart genomskinligt keyhole, en M0-projektil och bruna PF-väggar på samma rasterhöjd. **Noll faktisk key/NPC-pixelöverlapp får inte användas som skäl att gömma key**. H4, även om senare positivt, skulle inte automatiskt bevisa S05 eller fem NPC.
- **Source-only färdig design ≠ implementerat spel**. Ingen integrerad framtida R1/R2/R3/R4, inga validerade fem 8×9-actual spawns, ingen oberoende Verification II för nytt spel.

## 4. Andra delsystem som inte bör försvinna i rasterarbetet
| Område | Faktisk källa och gräns |
|---|---|
| Spelargrafik | [PLAYER v0.3 MAIN-mottagning](../MAIN_V_GRAPHICS_PLAYER_SPRITE_V03_RECEIPT_2026-11-16.md): `8x9 WEAPON READABILITY STILL FAILED`, `V03_B` bara jämförelsekandidat, inte full godkänd player-P0-mask |
| Androiders gång | [Walk Frame B](../MAIN_V_ANDROID_WALK_FRAME_B_V01_RECEIPT_2026-11-16.md): file/pixel trohet OK, särskilt små figurers gångillusion olöst, inte ROM-acceptans; Frame A behålls |
| HUD/poäng | [SCORE/LIVES HUD](../MAIN_V_SCORE_LIVES_HUD_VISUAL_V01_RECEIPT_AND_GRAPHICS_PAUSE_2026-11-16.md): H1 första offline-kandidat, H2 reserv, ingen fysisk kernel-/pixel-PASS |
| Ljud | [Sound Design v0.17](../SOUND_DESIGN_V017_2026-11-15.md): fyra ljudeffekter rådgivande (nyckelljud ursprungligt krav), ingen implementerad TIA-AUDC/AUDF/AUDV-styrning |
| ART/PACKAGING | [ART överlämning](../ART_PACKAGING_MANUAL_MIGRATION_2026-11-17.md): accepterade visuella riktningar för omslag och dörrscen, manual/story-utkast inte automatiskt godkänd spelcanon |
| VERIFICATION II | [Oberoende rollöverlämning](../VERIFICATION_II_MIGRATION_HANDOFF_2026-11-17.md): ingen ny faktisk ROM-verifikation. Tidigare batchpolicy kräver separat konkret beställning när underlag frysts |

## 5. Administrativa käll-/statusrisker som denna audit hittade
1. **De sex Project Sources är gamla V2-snapshots** från före senare LM-D12–20 och G5AA: särskilt `01` och `04` beskriver femfienders poäng-/spawnbeslut som väntande, `01/05` beskriver exakta v0.19-kartor som obestämda, och `00/05` saknar avslutad G0 INCONCLUSIVE. Äldre texter var korrekta vid sin egen skapelse men duger **inte** som oberoende källa för dagens status. **V3 ersättningspaket med samma sex namn har genererats lokalt i MAIN-chatten, ZIP + SHA256SUMS och CRC-kontroll**. **V3 är inte automatiskt infört i ChatGPT Project Sources**; användaren måste själv byta de sex filerna, inte lägga dubbla versioner.
2. Historiska GitHub README och `docs/project_sources/*` innehåller olika översta "ENDA SLUTLIGA"-rekommendationer för äldre **niofils FINAL** och senare **sexfilers V2**. Dessa är tidsbundna arbets-/arkivartefakter. **Detta aktuella G5AB-index** gäller som senaste navigationsstatus för V3, utan att ändra äldre revisionsbevis. Behåll historiken, tillskriv den inte aktuell auktoritet.
3. [Issue #6](https://github.com/Odourman/let-me-out/issues/6) är **open** och talar om äldre 2026-11-15 **v0.18 R1 6 / R2 5+key** NTSC-diagnostik. Detta är historisk order/leveranslogg, **inte** ett nytt tillstånd för framtida fem NPC. [Issue #3](https://github.com/Odourman/let-me-out/issues/3) gäller gammal v0.11 S0/S1 **sex-NPC-spawngräns**, inte dagens godkända nya kartmål.
4. [Issue #8](https://github.com/Odourman/let-me-out/issues/8) är fortsatt **open/deferred**, explicit batchpolicy av 16 november och ingen independent PASS; ingen automatic Verification II. [Issue #5](https://github.com/Odourman/let-me-out/issues/5) är framtida key/door verifieringsgrind utan ny kodauktorisation. [Issue #12](https://github.com/Odourman/let-me-out/issues/12) stängdes som genomfört endast **G0**.
5. [PR #7](https://github.com/Odourman/let-me-out/pull/7) fortsatt **draft/open/blockerad, ej mergad**. Där finns äldre tekniska experiment och negativa pixelresultat, som inte ska döljas eller förklaras PASS. GitHub `main` vid inventeringen innehöll design/docs/planning, men ingen ny integrerad `rom/`-kod från G5Z; dess specialistleverans ligger på isolerad branch.

## 6. Fortsatt arbete som MAIN redan får göra utan nytt kodmandat
- Lås en **source-only beslutsguide för EN framtida möjlig TIA-kalibrering**, knuten till G5AA:s verkliga bevisluckor: mät bara `RESP0` aktiv-rendering/START, `NUSIZ0=$02` P0/M0-kopieinterferens, `GRP`-latens och tidsstyrd `ENAM0`-gate, om ett isolerat test faktiskt kan differentiera utfallen. Detta är **förberedelse** och **inte** en ROM-order eller G6-plan med automatisk GO.
- Bevara separat H4-ONE fulla krav (två P1 original + P0 gul/vit + M0 samma Y + PF), S05 och fem-NPC/gameplay. Mätning av en liten delmekanism kan inte förvandlas till H4- eller G5-PASS.
- Fråga först efter **ett nytt uttryckligt användarbeslut** om specialistkod/ROM/DASM/Stella ska utföras. Eftersom tidigare G0 slutade `INCONCLUSIVE` har G5Y-villkoret för en full H4-G1 **inte** uppfyllts.
- Ingen automatisk ny graphics/audio/verification/cutover, ingen merge, inga waivers eller start av G6/F12.

## 7. Slutstatus vid G5AB
**`G5_FORMAL_OPEN` · `G0_H4_ONE=COMPLETED_INCONCLUSIVE_NO_ROM` · `G1/G6/F12/NEW_ROM/NEW_VERIFICATION/PR_MERGE=NOT_AUTHORIZED`.**

Det finns en framtida exakta fyra-rum+fem-NPC designriktning, men fortfarande **ingen tekniskt verifierad generell TIA-renderer** och inget försvarbart löfte om att hela spelet går att färdigställa utan separat accepterade avsteg. 
