# LET ME OUT! – GRAFIKARKITEKTUR OCH TESTFALL / V8

**Project Sources V8, MAIN XI, 2026-11-20.** Daterad navigationskopia, **inte** självständig projektcanon, en ny implementationsorder, emulator-PASS eller oberoende Verification. Följ alltid aktuell [GitHub-status](https://github.com/Odourman/let-me-out/blob/main/docs/CURRENT_AUTHORITY_STATUS_AND_WORK_QUEUE.md), [AGENTS.md](https://github.com/Odourman/let-me-out/blob/main/AGENTS.md), [G5-spärren](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5_AUTHORIZATION_BOUNDARY_AND_USER_CHOICE_2026-11-17.md), faktisk Issue, fryst commit och originalbeslut i [Google Drive](https://drive.google.com/drive/folders/1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u). Om ny leverans publicerats senare än denna daterade källa ska den granskas innan nuläget anges.

## Konkreta Atari-ramar

Standard F6 = **16 384 byte, fyra 4 KiB-banker**. **76 CPU-cykler/scanline** maximalt, mål **262 scanlines NTSC**, **128 RIOT-byte inklusive stack**. P0/M0 delar färg; P1 med komplex omkoppling till vita NPC/guldkey, PF brown och dörr måste synas på faktisk TIA-tid. Svart bakgrund, brun vägg, gul spelare, vit originalmaskfiende, guldkey. Korrekt sprite-multiplex bedöms genom fysiska pixel-/RGB-jämförelser, inte genom enbart abstrakta objekt eller korrekt emulator-frameantal.

## Fryst aktuell spel-ROM

[MAIN XI mottagen V02](https://github.com/Odourman/let-me-out/issues/31#issuecomment-7036737753): `8177c09368721988debb5407d8ffc2ed4bf4d94e`, SHA `f4ec909d57c583bc4cd58caa8550e6ff3f7a261a9f74f00156303c478fdd5b31`. 600 frames ×262 enligt utvecklarens Gopher; 595/600 exakta fem originalmasker, key-kallstart 65/65, key+shot 14/14, men player/key vid olika X och samma Y **0/14**; fem fiender samma Y86 **2/5**, M1 fem partiella standardbilder. Utökade väggfixtures: 48/48 gamla +32/32 nya Y40/130, 16 Y160 med vardera två missade bruna pixlar. Låst/open/cold-key missing **36/58/16**. Resursbudget kritisk c76, rapporterad stack SP=$F7 (128-byte-området helt disponerat). MAIN har inte själv återemulerat eller återbyggt.

## Dörrarkitektur efter nytt designbeslut

[Användaren har uttryckligen valt framtida **en enda** orange dörr i topp eller botten per karta](https://github.com/Odourman/let-me-out/blob/main/docs/gates/MAIN_XI_USER_DECISION_FUTURE_RANDOM_NPC_FORMS_TOP_BOTTOM_EXIT_2026-11-20.md); svart nyckelhål ska vara **borttagna orange pixlar som exponerar svart bakgrund**. Gammal orange högerdörr i X71 och 8177c är historiskt jämförelseobjekt, inte framtida placeringscanon.

Speglad `CTRLPF=$01` gör en **centrerad** topp-/bottenöppning plausibelt lättare i PF-bitmönstret, men PF har 4-colorclock horisontell bitupplösning och PF-färgen delas med bruna väggar. Undvik att påstå bevisat originaltrogna en-/två-colorclock-svarta R3-nyckelhål. [Beställd top/bottom F6-test-only](https://github.com/Odourman/let-me-out/issues/31#issuecomment-7036700643), starta efter senare receipt från **8177c**, inte X71; dörrläge låst/öppet/passage, färg, asymmetrifel, minsta pixel och P0/P1/M0/M1/BL-konflikter måste granskas på riktiga frames.

## Testmatris

- Regression: original X71 **48/48** väggfixturer, 8177c ytterligare **32/32**; bevara gamla original/ROM intakta, skapa **nya top/bottom-pixelorakel** för ändrad geometri. Y160 och dynamisk PF måste fortsatt granskas.
- Faktiska fem individer på samma Y och tät/omordnad X, olika storlek/mask, spelare ovanför/på band, gulmask/vitmask, skott och nyckel, dörrens låsta/orange/svart-utskurna och öppna tillstånd.
- Nyckel icke-ockluderad X-separated/Y-shared måste vara synlig; faktisk pixelöverlappning följer O1, ingen generell osynlighetstillåtelse. Ursprungliga fyra TOP-DOWN 8×9 maskbytes oförändrade.
- Riktig joystick-kallstart: skott, vägg/NPC-kollision, nyckelbärarens död och pickup, logiskt lås, fysisk exit, poäng/liv. **262/76/128** inklusive stack på dynamiska rasterfall.
- Ny slumpvisuell framtid kräver maskexakta testorakel efter individens faktisk valda sprite, även all-female/all-male/fem samma mask. Fördelning av formen är **inte ännu byggd**.

Behåll `G5_FORMAL_OPEN`, `INDEPENDENT_VERIFICATION=NOT_RUN`; `DEVELOPER_OBSERVED` ≠ oberoende PASS.
