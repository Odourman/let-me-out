# LET ME OUT! – LÄS FÖRST / V8

**Project Sources V8, MAIN XI, 2026-11-20.** Daterad navigationskopia, **inte** självständig projektcanon, en ny implementationsorder, emulator-PASS eller oberoende Verification. Följ alltid aktuell [GitHub-status](https://github.com/Odourman/let-me-out/blob/main/docs/CURRENT_AUTHORITY_STATUS_AND_WORK_QUEUE.md), [AGENTS.md](https://github.com/Odourman/let-me-out/blob/main/AGENTS.md), [G5-spärren](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5_AUTHORIZATION_BOUNDARY_AND_USER_CHOICE_2026-11-17.md), faktisk Issue, fryst commit och originalbeslut i [Google Drive](https://drive.google.com/drive/folders/1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u). Om ny leverans publicerats senare än denna daterade källa ska den granskas innan nuläget anges.

## Faktiskt senaste MAIN-mottagna spel-ROM (20 november)

**MAIN XI mottog** [TO_MAIN_V02_OBJECT_CONFLICT_REPAIR](https://github.com/Odourman/let-me-out/issues/31#issuecomment-7036737753), fryst commit `8177c09368721988debb5407d8ffc2ed4bf4d94e`, standard-F6/NTSC 16 KiB, SHA-256 `f4ec909d57c583bc4cd58caa8550e6ff3f7a261a9f74f00156303c478fdd5b31` (MAIN XI omräknad från GitHub-binär). Den körbara **enrumsprototypen** har utvecklarobserverad joystick-/skott-/nyckel-/utgångsrunda med **210 poäng och tre liv** och 600/600 bilder med 262 NTSC-rader. Fyra sprite-/grafikbankdelar har uppdaterats utan byteändring av spellogikbank 1 sedan X71 ([50, 0, 50, 58] byteändringar per 4KiB-bank).

**Förbättrat:** de 48 tidigare riktade vägg/NPC-proven består, ytterligare 32/32 Y40/130 klarar exakt grafik, totalt 80/96 i större familj. **Grafik är fortfarande FAIL:** fem kompletta fiendemasker i 595/600 standardrutor; golvnyckel med spelare samma rasterband även vid skilda X: 0/14; fem NPC på samma Y86: endast 2/5 kompletta; svart ursprungligt utskuret nyckelhål saknas; locked/open/cold-key-PF har kvar 36/58/16 saknade brunpixlar. Y160 saknar två väggpixlar i 16/16 riktade fall. Källa: [mottagningsbeslut med fysiska mätningar och negativa tester](https://github.com/Odourman/let-me-out/issues/31#issuecomment-7036737753). **G5_FORMAL_OPEN, INDEPENDENT_VERIFICATION=NOT_RUN.**

## Nya, uttryckliga framtida designbeslut

[MAIN XI:s originalspårbara beslut](https://github.com/Odourman/let-me-out/blob/main/docs/gates/MAIN_XI_USER_DECISION_FUTURE_RANDOM_NPC_FORMS_TOP_BOTTOM_EXIT_2026-11-20.md):
- **Exakt fem individuella NPC** kvar. Varje individ får vid ny rumsstart oberoende slumpat utseende bland de fyra **oförändrade TOP-DOWN 8×9-originalmaskerna**, även fem av samma form/manliga/kvinnliga får förekomma. Tidigare fasta visuella sammansättningen M,M,F,SM,SF gäller **inte** som framtida tvång.
- **Exakt en orange låst utgång med svart utskuret nyckelhål** ligger i **övervägg eller undervägg beroende på kartan**, inte längre obligatoriskt till höger. Svart bakgrund, brun PF, faktiskt synlig låsning/öppning/passage kvarstår. Exakta dörr-X/öppningsbredder och top/bottom-fördelning per A/B/C/D är **inte beslutade**. De fyra ursprungliga kartfilerna bevaras och får inte tyst redigeras.

Detta är framtida designmål, **inte** påstående om att 8177c-ROM:en redan innehåller dem.

## Just nu

MAIN XI har utfärdat ett [tekniskt test-only-uppdrag för en centrerad överdörr och en centrerad underdörr i samma Issue #31](https://github.com/Odourman/let-me-out/issues/31#issuecomment-7036700643), med **8177c som ny start** enligt [senare MAIN-mottagning](https://github.com/Odourman/let-me-out/issues/31#issuecomment-7036737753). Den tidigare högerdörren i fryst ROM är endast historisk regressionbas. **Användaren vill invänta ROM DEVELOPMENT IV:s svar.** Starta inte ytterligare Codex-uppdrag, ROM-jobb, V03 eller release bara därför att denna källversion installeras. Bevaka inte asynkront utan uttryckligt uppdrag.

## Arbetssätt

Prioritera fungerande ROM-framsteg framför administration. ROM DEVELOPMENT IV får iterera inom faktiskt auktoriserat V02-scope med DASM/Gopher/Stella utan mikrogrind per test. MAIN granskar väsentliga leveranser; RESEARCH II ger råd, GRAPHICS II studier, VERIFICATION II är fristående. Ingen självsignerad verification, icke-auktoriserad full flerrumscutover, ändrad grafikkvalitet/flimmer, PAL-/mappercutover, PR-merge, release eller senare implementation utan separat godkännande.
