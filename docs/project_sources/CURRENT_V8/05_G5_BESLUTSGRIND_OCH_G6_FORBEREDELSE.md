# LET ME OUT! – G5, IMPLEMENTATION OCH SNABBARE TAKT / V8

**Project Sources V8, MAIN XI, 2026-11-20.** Daterad navigationskopia, **inte** självständig projektcanon, en ny implementationsorder, emulator-PASS eller oberoende Verification. Följ alltid aktuell [GitHub-status](https://github.com/Odourman/let-me-out/blob/main/docs/CURRENT_AUTHORITY_STATUS_AND_WORK_QUEUE.md), [AGENTS.md](https://github.com/Odourman/let-me-out/blob/main/AGENTS.md), [G5-spärren](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5_AUTHORIZATION_BOUNDARY_AND_USER_CHOICE_2026-11-17.md), faktisk Issue, fryst commit och originalbeslut i [Google Drive](https://drive.google.com/drive/folders/1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u). Om ny leverans publicerats senare än denna daterade källa ska den granskas innan nuläget anges.

## Formell status

**`G5_FORMAL_OPEN`; `INDEPENDENT_VERIFICATION=NOT_RUN` för den aktuella spelbara V02-checkpointen.** Inget G6/F12, senare gameplay-implementation, produktionsflerrums-cutover, PAL-/mapperbyte, PR-merge, release eller formell Verification är automatiskt auktoriserat.

[Senaste MAIN-mottagna V02-leverans](https://github.com/Odourman/let-me-out/issues/31#issuecomment-7036737753) fryst `8177c09368721988debb5407d8ffc2ed4bf4d94e`, ROM SHA-256 `f4ec909d57c583bc4cd58caa8550e6ff3f7a261a9f74f00156303c478fdd5b31` MAIN-verifierad från originalbinär. Utvecklarobserverat **600/600 ×262 scanlines**, **595/600 fem kompletta NPC i standardtest** och **80/96** utökade riktade vägg/NPC-fixturer (48 gamla +32 nya; 16 Y160 med 2 felpixlar). Joystick/nyckel/210 poäng/tre liv/utgång i kallstart. Fortsatta blockerare: nyckel och gul spelare i samma Y-band **0/14**, fem NPC samma Y **2/5**, svart R3-hål inte renderat, dynamiska PF missing closed/open/cold-key **36/58/16**, M(1)-grafik. F6 NTSC, ≤76 c/scanline och 128 RIOT inkl stack redovisade av utvecklaren, **inte** verifierade genom MAIN:s egen emulatoromkörning eller Verification II.

## Designbeslut vs implementation

[Senare uttryckligt godkänd framtida design](https://github.com/Odourman/let-me-out/blob/main/docs/gates/MAIN_XI_USER_DECISION_FUTURE_RANDOM_NPC_FORMS_TOP_BOTTOM_EXIT_2026-11-20.md) tillåter oberoende slumpade fyra originalutseenden per individuell NPC och en orange **över-/underdörr per framtida karta** med svart negativt nyckelhål. Detta ersätter tidigare fast M,M,F,SM,SF och obligatorisk högerdörr **endast som framtida designmål**. Fyra ursprungskartors grider/hashes oförändrade; exakt framtida top/bottom per karta ej låst. **Inget** i detta designbeslut auktoriserar att tyst ändra äldre fryst V02-checkpoint eller öppna ett senare implementationssteg.

## Aktuellt tekniskt V02-uppdrag: invänta ROM DEVELOPMENT

MAIN XI har i [samma Issue #31](https://github.com/Odourman/let-me-out/issues/31#issuecomment-7036700643) delegerat **två reella test-only F6/NTSC dörrvarianter** (centrerad övervägg resp undervägg) med orange dörr och svart cutout, fem NPC, key/player, raster/CPU/RAM och riktiga pixel-orakel. [Efterföljande MAIN-mottagning](https://github.com/Odourman/let-me-out/issues/31#issuecomment-7036737753) uppgraderar primär teknisk start från X71 till **8177c**, med X71 bevarad regression. **Användaren vill nu invänta ROM DEVELOPMENT IV:s svar.** Skriv inte ny ROM eller ny kommentar som om specialistarbete redan startats/levererats. Undvik att beställa upprepning av redan publicerat objektarbete.

## Arbetsregler och bevisnivå

LM-D29/D30 tillåter friska utvecklariterationer, riktig DASM-/Gopher-/Stella-testning och ny körbar ROM vid substantiellt framsteg inom en **verklig** avgränsad befintlig order utan mikro-Issues. MAIN granskar väsentliga rapporter proportionerligt. Teknisk test-only != ny gameplayetapp; rådgivande research != implementation; utvecklar-PASS != fristående Verification.

Leveranser ska ha fryst commit, byggbar 6507-kod, F6 16KiB ROM, SHA-256, reproduktion, riktiga originalemulatorbilder och positiva/negativa CPU/RAM/scanline/pixel-/RBG-resultat. Ingen tyst sänkning av fem individer, originalmasker, fri XY, färger, skyddsregler, nyckelsynlighet eller flimmeracceptans. För separat Codex-chatt: MAIN lämnar komplett kopierbar prompt med verklig startcommit, scope, frihet, regressionskriterier, stopp och publicering; en Issue-länk är inte att starta Codex.

## Projektkällors funktion

V8 är en **daterad snapshot**, inte en ny levande authority. Kontrollera alltid GitHub-status, nyare Issue-kommentarer, original Drive, beslut och frysta artefakter. Äldre V6/V7-källor arkiveras och ska inte vara parallellt aktiva.
