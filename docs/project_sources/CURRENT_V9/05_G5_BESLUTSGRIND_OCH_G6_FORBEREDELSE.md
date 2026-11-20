# LET ME OUT! – G5, IMPLEMENTATION OCH SNABBARE TAKT / V9

Project Sources V9, MAIN XI, 2026-11-20. Daterad navigation, INTE levande canon, implementationsauktorisation eller oberoende ROM-verifiering. Kontrollera alltid [levande projektstatus](https://github.com/Odourman/let-me-out/blob/main/docs/CURRENT_AUTHORITY_STATUS_AND_WORK_QUEUE.md), [AGENTS.md](https://github.com/Odourman/let-me-out/blob/main/AGENTS.md), [G5-spärren](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5_AUTHORIZATION_BOUNDARY_AND_USER_CHOICE_2026-11-17.md), relevant Issue, fryst källkod/ROM och [originalen i Drive](https://drive.google.com/drive/folders/1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u). Senare uttryckliga användarbeslut ändrar endast den angivna delen av äldre original. Minnet och dessa daterade Project Sources är inte projektauktoritet.

## Formella gränser

**G5_FORMAL_OPEN; INDEPENDENT_VERIFICATION=NOT_RUN.** MAIN granskar tekniska specialistleveranser, men det är bara oberoende VERIFICATION II som får bedöma formell status. Ingen ny V03, G6/F12, skarp fyrarumsproduktion, PAL-/mapperbyte, originella sprite-/fiende-/AI-/poäng-/flickerwaivers, PR merge eller release utan separat uttrycklig auktorisation.

LM-D29/D30: fortlöpande snabb faktisk 6507/DASM-spel-ROM-iteration inom redan godkänt **V02** tekniskt scope; verkliga Gopher2600/Stella-/pixelfixturer och positiva/negativa bevis. ROM DEVELOPMENT IV får prova seriöst olika metoder och leverera substantiella checkpoints utan mikro-Issue per prov. En publicerad Issue-order startar **inte** den separata Codex-chatten, som behöver användarens konkreta överlämning. Bevara frysta ursprungs-ROM, hash och negativa resultat.

## Senaste mottagna faktiska spel-/testnivå

**Allmän enrumsspelbar V02:** `8177c09368721988debb5407d8ffc2ed4bf4d94e`, ROM SHA256 `f4ec909d57c583bc4cd58caa8550e6ff3f7a261a9f74f00156303c478fdd5b31`, MAIN-omräknad. Utvecklar-Gopher: 600×262, 595/600 fem kompletta masker, 80/96 riktade brown PF/NPC, cold-key 65/65, key+shot 14/14, 210p/3 liv verklig joystickutgång; key/player 0/14, fem same-Y 2/5, M(1) och dynamiska PF kvar FAIL. [MAIN XI:s mottagning av allmän V02-8177c](https://github.com/Odourman/let-me-out/issues/31#issuecomment-7036737753).

**Separat senaste mottagna TOP/BOTTOM-testfamilj:** `4c4fc5b7c5545217b2321a38d9db6db5dac7db2f`, TOP `let-me-out-v02-door-top.bin` SHA256 `8b95313f8a02d7ba6bd1ab04a792a542c25ccaf7ff415c8f827e52f071e61891`, BOTTOM `let-me-out-v02-door-bottom.bin` SHA256 `cd351628b8432263462944da0d832381b5efc56ce3c7c6689d024cbcbc4a7dfb`; MAIN har omräknat båda från originalbinär. 16KiB F6/NTSC, 600×262, 595/600 standard NPC, max c76, 128 RIOT incl stack, riktig locked/key/unlocked joystickpassage i både TOP/BOTTOM; historiska orange PF-kontur: 80 spillpixel, TOP 256/256 öppning svart, BOTTOM 254/256, shot 9/10. Ingen allmän render-PASS. [MAIN XI:s mottagning av topp-/bottenproven](https://github.com/Odourman/let-me-out/issues/31#issuecomment-7037903760).

## Ändrad framtida design och aktuell delegering

[Fem självständigt slumpade originalmasker och dörrens över-/underplacering](https://github.com/Odourman/let-me-out/blob/main/docs/gates/MAIN_XI_USER_DECISION_FUTURE_RANDOM_NPC_FORMS_TOP_BOTTOM_EXIT_2026-11-20.md) med fem oberoende slumpade originalmasker och enda ytterdörr i TOP eller BOTTOM per framtida karta; senare [Brun dörr, svart negativ kontur och nyckelhål](https://github.com/Odourman/let-me-out/blob/main/docs/gates/MAIN_XI_USER_DECISION_BROWN_PF_DOOR_BLACK_OUTLINE_KEYHOLE_2026-11-20.md) supersederar orange framtida dörr: samma BRUNA `COLUPF` som vägg, synlig SVART NEGATIV dörrkontur och igenkännbart negativt nyckelhål. Exakt per-karta variant/geometri ännu inte godkänd. Nya former/dörrdesign **inte** byggda i fryst 8177c/4c4fc5b7.

[Nu gällande V02-testorder, brun dörr](https://github.com/Odourman/let-me-out/issues/31#issuecomment-7038233205) är nu **enda aktuella V02-test-only-ordern**: utgå från fryst `4c4fc5b7`, prova brun PF-dörr med svart kontur/hål först TOP sedan BOTTOM, låst/öppen/joystickexit, fem NPC/guldkey/spelare/skott och faktisk 262/76/128-/pixelregression. Orange P1-först-order #7038148323 är uttryckligen ERSATT; användaren har INTE skickat den tidigare prompten. Ny ersättningsprompt måste skickas manuellt till separat ROM DEVELOPMENT IV, och den har **inte** startats endast genom GitHub-dokumentation.

## Leveransnivå

V02-specialist: fryst commit, byggbar assembler, spelbar 16KiB F6-ROM, SHA256 post-push, DASM-build, Gopher/Stella-bilder, CPU/RAM/scanline/colorclock/RGB/pixelprover, riktiga joystickkörningar och dokumenterade negativa testresultat. Märk `SOURCE_ONLY`, `SYNTHETIC`, `DEVELOPER_OBSERVED`, `MAIN_REVIEWED` och `INDEPENDENT_VERIFICATION` korrekt; solver-SAT är inte TIA-PASS. Skilj test-ROM från faktisk ny gameplay/canon-implementation. Projekt Sources V9 är daterad navigation, inte gate eller replikerad GitHub-källa.
