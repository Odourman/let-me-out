# LET ME OUT! – FEM FIENDER, SPELDESIGN OCH KARTOR / V8

**Project Sources V8, MAIN XI, 2026-11-20.** Daterad navigationskopia, **inte** självständig projektcanon, en ny implementationsorder, emulator-PASS eller oberoende Verification. Följ alltid aktuell [GitHub-status](https://github.com/Odourman/let-me-out/blob/main/docs/CURRENT_AUTHORITY_STATUS_AND_WORK_QUEUE.md), [AGENTS.md](https://github.com/Odourman/let-me-out/blob/main/AGENTS.md), [G5-spärren](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5_AUTHORIZATION_BOUNDARY_AND_USER_CHOICE_2026-11-17.md), faktisk Issue, fryst commit och originalbeslut i [Google Drive](https://drive.google.com/drive/folders/1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u). Om ny leverans publicerats senare än denna daterade källa ska den granskas innan nuläget anges.

## Senast användargodkänd framtida fem-NPC-design

[Nyare uttryckligt beslut 20 november](https://github.com/Odourman/let-me-out/blob/main/docs/gates/MAIN_XI_USER_DECISION_FUTURE_RANDOM_NPC_FORMS_TOP_BOTTOM_EXIT_2026-11-20.md) **ersätter** den äldre tvingande visuella kombinationen **M,M,F,SM,SF**, men **inte** antalet fem, fiendernas individualitet eller någon av de fyra ursprungliga **TOP-DOWN 8×9 maskfilerna**. Varje individ får vid varje rumsstart ett **oberoende slumpat** utseende ur:
- stor man `large_male`
- stor kvinna `large_female`
- liten man `small_male`
- liten kvinna `small_female`

En naturlig framtida implementerings-/testtolkning är fyra lika sannolika former **1/4 per individ**, fem oberoende val. Därför är fem män, fem kvinnor och fem identiska maskformer tillåtna. Formen hålls stabil hela rummet. **Inga nya maskpixlar eller skiftande maskform för en levande individ vid varje bildruta.**

Varje av de **fem individerna** har fortfarande fri logisk X/Y, jakt i fyra riktningar och trovärdig fara, kollisions- och dödsregler. Oavsett utseende har var och en **1/5 chans att bära nyckeln**, oberoende av formen. Key faller på faktiskt logisk dödsplats efter dödsanimation, pickup synlig/fungerande. Fem olika giltiga spawns per rum enligt äldre [G5S](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5S_MAIN_VII_C1_D1_E1_USER_APPROVAL_DECISION_RECORD_2026-11-17.md). Poäng för framtida fem-NPC: **-30 per kill, lägsta 0; +50 pickup; +100 exit; +15 per överlevande**, extraliv 500,1500,2500... enligt original.

## Dörr- och kartdelta

Användaren har uttryckligen ersatt den obligatoriska **högra** dörrsidan: framtida karta kan ha sin **enda** orange låsta dörr med svart bakgrunds-utskuret nyckelhål i **övre eller nedre ytterväggen**. Dörren försvinner vid korrekt upplåsning, synlig svart passage och fysisk utgång; övriga outer-väggar ska vara stängda, innerväggar bruna, svart bakgrund.

[De tidigare fyra valda kart-ID:na](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5X_MAIN_VII_APPROVED_FUTURE_FOUR_MAPS_SOURCE_MANIFEST_2026-11-17.json) A_OPEN_01/B_OPEN_02/C_OPEN_01/D_OPEN_01 (40×22) är **historiskt exakt godkända framtida original** med höger D-cell, men framtida topp-/bottenutgång ger **ny geometri och behöver nya versionssatta varianter/hashar**. Inga original-ID:n/fingerprints ska återanvändas för ändrat grid. **Användaren har inte valt** vilken av de fyra som ska ha över-/underdörr, exakt öppnings-X/bredd eller ny R3-bitmapp. Ingen automatisk flerrums-cutover.

## Vad som är implementerat?

[MAIN-mottagen 8177c-V02](https://github.com/Odourman/let-me-out/issues/31#issuecomment-7036737753) är en körbar **enrums**-ROM med gammal fast M,M,F,SM,SF och **gammal högerdörr**; de nya designändringarna är **ännu inte** implementerade. 600×262 och 210 poäng/3 liv i utvecklarens kallstart, men rendering fortsatt FAIL (595/600 standard alla fem; same-Y 2/5; key/player samma Y 0/14; svart nyckelhål saknas). [Tekniskt topp-/bottenprov](https://github.com/Odourman/let-me-out/issues/31#issuecomment-7036700643) är **beställt men inte mottaget som resultat**.

Designbeslut ger inte automatiskt ett nytt gameplaysteg. **G5_FORMAL_OPEN, INDEPENDENT_VERIFICATION=NOT_RUN.**
