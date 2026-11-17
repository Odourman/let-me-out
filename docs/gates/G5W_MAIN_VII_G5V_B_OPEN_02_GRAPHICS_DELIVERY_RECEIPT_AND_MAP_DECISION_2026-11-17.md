# LET ME OUT! – MAIN VII G5W: G5V/GRAPHICS II B_OPEN_02 mottagen och offline-reproducerad

> **HISTORISKT BESLUTSLÄGE – B-KARTVAL ÄR INTE LÄNGRE ÖPPET.** Vid G5W-mottagningen var B_OPEN_02 en icke-godkänd studie; **efterföljande användarbeslut LM-D19 har godkänt exakt B_OPEN_02 som framtida designlayout för rum B**. Ingen ROM/PF/8×9-acceptans följer. Se [G5X-beslutet](G5X_MAIN_VII_B_OPEN_02_EXACT_USER_APPROVAL_AND_FOUR_MAP_BASELINE_DECISION_2026-11-17.md) och [aktuell status](https://github.com/Odourman/let-me-out/blob/main/docs/CURRENT_AUTHORITY_STATUS_AND_WORK_QUEUE.md).

**Datum:** 2026-11-17. **Status:** `G5V_GRAPHICS_SOURCE_ONLY_DELIVERED_MAIN_RECEIPT_PASS_B_OPEN_02_USER_DECISION_PENDING`. **Inte:** B-kartgodkännande, grafik- eller ROM/Stella-pass, ny PR-merge, G0/G6/F12, oberoende VERIFICATION.

## 1. Leveransens provenance, gränser och original
- [GRAPHICS II:s Issue #11 och fullständig överlämning](https://github.com/Odourman/let-me-out/issues/11#issuecomment-6956473211).
- [Fryst graphics-commit `2991a94a4d92a0ee75a5de8e8c5302d549734e1e`](https://github.com/Odourman/let-me-out/tree/2991a94a4d92a0ee75a5de8e8c5302d549734e1e/studies/graphics/G5V_B_OPEN_02_2026-11-17). **12 studie-filer** på isolerad branch `graphics/g5v-b-open-02-20261117` (GitHub compare vid mottagning: 2 commits före main, 0 bakom, inga ändringar i original-JSON, ingen merge). En del av dessa 12 är SVG, en maskinläsbar ny kandidat-JSON, renderer, report och VALIDERING.
- [Ny exakt *kandidat*-JSON för B_OPEN_02](https://github.com/Odourman/let-me-out/blob/2991a94a4d92a0ee75a5de8e8c5302d549734e1e/studies/graphics/G5V_B_OPEN_02_2026-11-17/B_OPEN_02.json), Git-blob `c32fc656fb5c60d16a5b73e4cea75f86df3e9621`.
- Underlaget härleds enbart från källcommit `80bf072ee0e8a9a84905a29d70771a7cc6be7820`, v0.11 käll-blob `820a74e5fb77c818ffb1286c5b23698d4374e771`, v0.19 käll-blob `0e449f97f87bd9b403476fd1435398042eaee285`. Dessa exakta originalmatriser och historiska ROM-referenser är oförändrade.
- [Full ZIP från officiella Drive](https://drive.google.com/file/d/15-krJ-7Ga_Lyd_LrwEJnao_-637LCYP_/view), **82 809 byte**, SHA-256 `0db3d7325c9b08eb0197b1782a32d2f6b40722ef2e39e8eca7269594a7777a2d`; **18 arkivmedlemmar**, ZIP CRC PASS, **17/17 SHA256SUMS.txt värden PASS**. [Drive-presentation](https://drive.google.com/file/d/13oExBXBhFpwkMJDzKgQOww1Wwh02KoD3/view) och [rapport](https://drive.google.com/file/d/1Uw1hOzxTmmBQVf8KCDsRKhs_lMYcRzXz/view) ligger i officiell projektmapp `1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u`.

## 2. MAIN VII separat mottagnings- och reproduktionskontroll, endast offline
**Kontrollerna har faktiskt körts:**
1. MAIN öppnade ZIP lokalt, godkände ZIP CRC och verifierade 17/17 SHA256SUMS.txt-poster mot arkivbytes.
2. `build_g5v.py` granskades översiktligt, kördes i en ny isolerad temporär utmatningsmapp med källutdragen från samma ZIP. **12/12 genererade filer inklusive B-kartor, triptyk-PNG, ankare-overlay, deltakarta, B_OPEN_02.json och VALIDATION.json blev byteidentiska** med leveransens motsvarande filer.
3. Utan att använda GRAPHICS II:s egen räknare skrev MAIN en egen fyra-grannars BFS över alla tillåtna 2×2-ankare direkt från aktuell GitHub-JSON för historisk B01, tidigare B_OPEN_01 och nya B_OPEN_02. Resultat:
   - B01: **156** innerväggsceller, **439/439** ankarpositioner nåbara från start `(2,10)`, **0** artikulationsankare.
   - B_OPEN_01: **48**, **619/619**, **0** artikulationsankare.
   - B_OPEN_02: **72**, **565/565**, **0** artikulationsankare.
   - Samtliga B-kartor har högerdörrmarkörer endast `x=39, y=9..12`; B_OPEN_02 har samma vänster-/övre-/nedre stängda kontur och fri mittpassage över `y=9..12`.
4. Alla **13 historiska B01-startankare** ligger i fria 2×2-områden i B_OPEN_02; kontrollen bevisar **inte** att någon vald fempunktssamling fungerar med verkliga NPC 8×9, key-drop, aktiv fiende-AI eller spelarkollision.
5. MAIN har öppnat och visuellt bedömt den **faktiska** G5V-trippeljämförelsebilden från Drive: B_OPEN_02 erbjuder varierade stag-/väggarmar och små mittöar utan att återgå till B01:s täta labyrint.

**Rätt nivå på godkännande:** detta är `MAIN_RECEIPT_PASS_SOURCE_ONLY`, *inte* oberoende Verification II, TIA/6507/PF-register-/colorclock-kontroll, verklig sprite/rendering, rumsintegration eller spelcanon.

## 3. Kartbedömning och rekommenderat exakt användarbeslut
B_OPEN_02 (`studies/graphics/G5V_B_OPEN_02_2026-11-17/B_OPEN_02.json`, Git SHA `c32fc656fb5c60d16a5b73e4cea75f86df3e9621`) **rekommenderas som framtida exakt rum-B-layout**. I källrutnätet har B_OPEN_02 90,5 % öppen interiör mot B_OPEN_01:s 93,7 % och historiska B01:s 79,5 %. Den tillför bättre rumslig variation än B_OPEN_01 och undviker uppenbara 2×2-blockeringar. Det finns en visuell kvalitetsbedömning, inte ett bevis på att spelet med fem fiender kan köras.

**Separat, fortfarande efterfrågat användarval:**
> Godkänner du exakt `B_OPEN_02` som **framtida rum B** enligt den frysta G5V-JSON-filen, tillsammans med redan **exakt godkända** `A_OPEN_01`, `C_OPEN_01`, `D_OPEN_01`?

**Godkännande av B i framtiden skulle endast fastslå den nya framtida fyrkartdesignen**. Det är inte ett tillstånd att ändra original-JSON, starta ROM-arbete eller hävda full teknisk pass. Om användaren väljer en annan B-version krävs ett nytt exakt kartbeslut.

## 4. Håll hårt isär beslut och implementation
- **Redan godkänt LM-D17:** `A_OPEN_01/C_OPEN_01/D_OPEN_01` som framtida exakta kartlayoutmål. **Redan godkänt LM-D18:** grafikstudie för B_OPEN_02. Det innebär inte att B öppnas automatiskt efter lyckat offlinegrafikuppdrag.
- **G5V/B-kandidaten status:** `B_OPEN_02_NOT_APPROVED_AS_MAP`; `B_OPEN_01_NOT_APPROVED`. v0.11 `B01` förblir historisk källa. A/C/D i v0.19-kandidatoriginalet är godkända i senare separat beslutsprotokoll men original-JSON är oförändrad.
- **Kvar:** faktisk 8×9-/fem-NPC-spawnvalidering och navigations-/key-/door-logik; S05 samma raster-Y för player+white NPC+key+orange locked right door+M0+PF och fri X/Y-kernel; mätbar kvalitet i verklig Atari 2600 NTSC/Stella. G5 formellt OPEN, G0/G6/F12 och senare implementation EJ auktoriserade, ingen PR-merge eller ny oberoende Verification.
- **Issue #11 kan stängas** som levererad **source-only grafikstudie**, men kartvalet för B förblir ett nytt användarbeslut.

## 5. Nästa MAIN-åtgärd
Stäng #11 efter mottagningskommentar, uppdatera `CURRENT_PROJECT_STATE` och G5-gate som **mottagen icke-canon studie**. Förelägg sedan det exakta B_OPEN_02-valet för användaren. **Inget arbete som kräver ROM-specialist, G0/G6 eller ny grafikstudie ska startas automatiskt.**
