# H4 → FEM NPC OCH S05: KVARVARANDE GAP
**ROM DEVELOPMENT III, 2026-11-17.** Appendix till [G5Z G0 H4-ONE-rapport](TO_MAIN_G5Z_G0_H4_ONE.md). **Klass:** source-only konsekvens, inget nytt researchspår eller kodmandat. Slutklass: `G0_INCONCLUSIVE_NO_ROM`.

## 1. Vad full H4 skulle ha bevisat om det varit PLAUSIBLE
G4 H4-ONE innehåller **fyra** fulla 8x9-bitmapaktörer totalt: en gul diagnostisk P0-spelare, en vit original-M också på P0, två vita original-F/SM på P1, ett M0-skott i samma band och brown PF. Den historiskt positiva R1f-kopplingsmodellen och F9 finns på **olika** ROM-grenar och går inte att förena som redan exekverbar kernel. Även en framtida H4-mikro-PASS skulle visa **bara tre vita NPC**, inte fem; ingen nuvarande sådan mikro finns.

## 2. Framtida femfiendersbas, beslut skilda från teknikbevis
- **LM-D12/13:** fri individuell *logisk* NPC X/Y och igenkännbara synliga hot; ingen Y-lane, generell osynlighets- eller 10Hz-flimmerwaiver. [G5Q](../../docs/gates/G5Q_MAIN_VII_A1_B1_USER_APPROVAL_DECISION_RECORD_2026-11-17.md).
- **LM-D14/15/16:** framtida roster **M,M,F,SM,SF**, framtida `-30` per dödad NPC, fem validerade separata spawn, slumpad individuell bärare 1/5. Dessa beslut ersätter **inte retroaktivt** historisk v0.18 med R1 sex och R2 fem+key. [G5S](../../docs/gates/G5S_MAIN_VII_C1_D1_E1_USER_APPROVAL_DECISION_RECORD_2026-11-17.md).
- **LM-D17/19:** framtida exakta gridmål `A_OPEN_01/B_OPEN_02/C_OPEN_01/D_OPEN_01` är godkända. [G5X-urvalsmanifest](../../docs/gates/G5X_MAIN_VII_APPROVED_FUTURE_FOUR_MAPS_SOURCE_MANIFEST_2026-11-17.json). Geometri är **inte** 6507-PF-, väggkollision- eller spawnpass.
- **G5 FORMAL fortfarande OPEN**; H4/G5Z ändrar ingen speldesign eller teknisk acceptance.

## 3. Oförändrade konkreta hårdvaruluckor
1. **5 vita + 1 gul samma Y:** sex 8-bitars silhuetter måste renderas med två P0/P1-players, medan M0-skott och PF är upptagna. En hypotetisk H4-evenemangsscheduler med P0 2+P1 2 skalar inte utan vidare till fem vita + gul och korsande X/Y. G5H:s rad6 `79/76` för A och `74/76`/ `79/76` för B vid olika ordningar gäller just den äldre direkta fem-NPC/door-arkitekturen och dess begränsningar; det är inte H4-specifik universell maxkapacitet.
2. **X-rankbyte, tät X, shifted Y:** P0/P1 återutlösning, fulla fyra TOP-DOWN-originaltyper, event reorder, 76c/START/GRP-deadlines och faktisk synlighet vid överlapp saknar en källsatt helhet. Tre SM-nollrader löser inte critical row6 eller när tre/fyra NPC har samma färg men olika maskbytes.
3. **40x22 riktiga kartor och högerdörr:** Godkända nya 40-bits-rader kan behöva PF-uppdatering mitt i raster; R3/C02 hade sex PF-skrivningar vid c7/15/22/37/45/52 och P1 orange door c62 i en **separat ROM** med ca74/76 worst source row. H4:s edge-only PF-preload på ett identiskt band är ingen full-map eller orange-door-integration.
4. **S05 skild resurskonflikt:** På dörrens Y äger P1 orange dörr (svart nyckelhål = genomskinlig del i dörrbitmapen). P0 kan behöva gul player, vit original-NPC och guldkey på samma höjd, medan M0 delar `COLUP0` och bruna PF måste vara kvar. En H4 med **två vita P1** ger inte tre P0-ägare eller P1-orange-vitt på samma rad. G5Y särskiljer `S05-NO-OVERLAP` (key **måste** synas) från `S05-OVERLAP` (O1 medger *tillfällig* skymning endast vid faktisk bitpixelöverlapp; logisk position bevaras). Låst högerdörr och svart transparent keyhole får inte försvinna genom optisk genväg.
5. **Logiska spel- och verifieringsgrindar:** key efter dödsanimation, K1/E1 pickupordning, faktisk skymning/reappearance, 1/5 key-bärare och validerade 8x9-start-/väggträffar är inte implementerade av H4. Inga integrerade R1/R2/R3/R4 262-scanline-, 600-frame-, ROM-hash- eller oberoende Verification II-bevis finns för framtida femfiendersspelet.

## 4. Stopp
Denna text föreslår **inte** ett nytt G0/G1/N0/fem-NPC/S05-experiment, ingen ROM, ny mapper, Y-kompromiss eller PR-merge. **MAIN VII är ensam mottagare** av G5Z-rapporten och får efter egen källkontroll avgöra hur ett *framtida separat användarbeslut* bör formuleras. `G5_FORMAL=OPEN; G1/G6/F12/ROM/VERIFICATION=NOT_AUTHORIZED`.
