# LET ME OUT! — MAIN VI: senaste 10 tekniska steg, nuläge och nästa 10
Datum: 2026-11-17 (Sverige). Projekt: endast Odourman/let-me-out.
Dokumentklass: källgranskad MAIN-plan, EJ genomförandeorder, EJ ny ROM-/PAL-/mapper-/gameplay-/VERIFICATION-auktorisation. Ingen F12 utfärdas.

## 1. Aktuell auktoritet och läge
Vid genomgången: main HEAD 3ccb10f50ef31e2fd4cd781bd66d0fb61995dad3. Issue #6 OPEN (endast v0.18/NTSC R1–R4 diagnostik), PR #7 OPEN/DRAFT/UNMERGED head 82667dae033f70570dce903f8e1d4866528be02a, Issue #8 OPEN (äldre E02-baseline), ingen genomförd full E02 för F9–F11. Dedikerad Google Drive-mapp har nuvarande MAIN VI audit och de äldre frysta F6/F7/F9-arkiven; 17 november har tillfört migrationsdokumentation, inte nya spel- eller ROM-testresultat efter F11.

Full R1 = BLOCKED / NOT ACCEPTED. F11 = F11_SOURCE_ONLY_INFEASIBLE, G0 FAIL, G1 NOT RUN, 0 nya F11-ROM/DASM/Stella. R3 är separat lokal diagnostik, inte integrerad med R1; R2 nyckel/O1 och R4 stress inte integrerat/oberoende verifierat. Ingen fullspels-ROM.

57 ursprungliga beslut, tre originalskisser, de fyra låsta rättvända 8×9-maskerna (Git blob 058800a4c1904d1ff289e7e61b3902aa111ba16d) och kompletterande användarbeslut är designauktoritet. Sex vita androider med numeriskt egna X/Y, gul spelare med hatt/vapen, M0-skott, bruna väggar, enda orange högra dörren med svart nyckelhål, nyckel/O1, poäng/liv/RESET är oförändrade mål.

## 2. De senaste tio avslutade tekniska arbetsstegen: R1-F2–F11
1. F2 — En av sex originalandroider växlar begränsat X i samma ROM, övriga fem fasta. DEVELOPER_LOCAL begränsat PASS; inga sex fria X/Y.
2. F3 — Försök med en andra individstyrd X; verifierad registerwrite men oförändrat pixel-X, F3 position FAIL. Andra runtime-ROM NOT RUN.
3. F4 — c18/c21-fasändringar inom tidig HBLANK gav ingen fysisk X-förflyttning, lokal FAIL.
4. F5 — SOURCE-ONLY HBLANK/START-kausalanalys; separat MAIN-audit påvisade R1ba:s fyra stora vertikalt omvända masker (600/600 gamla sex-original-PASS ogiltigförklarad).
5. F6 — Två olika rättvända originalmasker vid kalibrerade c21/c23 och c32; två ROM-varianter, 32/32 pixelkorrekta Stella-bilder, lokal PASS.
6. F7 — Två separata binära RAM-väljare, fyra diskreta kombinationer i EN ROM och 160 äkta Stella-bilder, lokal PASS.
7. F8 — SOURCE-ONLY tredje binära RAM-X möjlighets- och 4KiB-analys; ingen ny ROM.
8. F9 — En standard-F6/NTSC ROM med tre rättvända olika originalmasker och tre BINÄRA RAM-X, åtta kombinationer, 144/144 Stella-bilder, 12/12 ortogonala kontraster, lokal + MAIN egen råbildsaudit. INTE tre godtyckligt numeriska X.
9. F10 — SOURCE-ONLY analys av tre arkitekturfamiljer, S1–S5 och 30 Atari-trick; ingen styrkt sex numeriskt fri X/Y i standard-F6.
10. F11 — Fyrmaskers numeriskt datadriven X-kandidat [16,36,56,76]→[19,36,56,76] stoppad G0 av oklar fysisk copy START/GRP och scheduler; ingen ny ROM, ej universellt omöjlighetsbevis.
Migration MAIN V→VI, ROM DEVELOPMENT II→III, GRAPHICS II, RESEARCH II, VERIFICATION II och ART är organisatoriska steg efter F11, ej ytterligare ROM-evidens.

## 3. Nytt strategiskt forskningsfynd från faktisk separat GitHub-research, ännu endast rådgivande
Den på 2026-11-16 separata MAIN II-researchen visar **ytterligare en byggsten som bör vägas mot F11:s P1-enda-kandidat**, men INTE en alternativ full R1-godkänd implementation:
- R1e: fyra olika låsta rättvända originalmasker med tre NPC via P1 och en vit NPC via P0:s andra kopia, samtidigt med gul spelare via P0; endast en statisk specialgeometri, M0 på föregående rasterrad och ingen PF-integration. Rapport: https://github.com/Odourman/let-me-out/blob/research/main-ii-r1e-four-originals-p0wide-calibrated-20261116/docs/MAIN_II_R1E_FOUR_DISTINCT_ORIGINALS_STATIC_LOCAL_PASS_2026-11-16.md
- R1f: två separata RESP0 per rad ger fjärde NPC två lägen utan att gula spelarens X flyttas, men separata statiska ROM och snäv geometri. Rapport: https://github.com/Odourman/let-me-out/blob/research/main-ii-r1f-resp0-independent-fourth-20261116/docs/MAIN_II_R1F_RESP0_BREAKS_FIXED_P0_COPY_X_STELLA_LOCAL_PASS_2026-11-16.md
- R1g: EN ROM växlar fjärde vita NPC:s fyra diskreta P0-X-lägen, 600/600 Stella-bilder, medan de tre vita P1-NPC och gul spelare står på fasta X. M0 ligger på annan rasterrad, PF-väggar/dörrar saknas, ingen sex-fri-X/Y eller E02. Rapport: https://github.com/Odourman/let-me-out/blob/research/main-ii-r1g-four-X-dynamic-600-20261116/docs/MAIN_II_R1G_FOUR_X_DYNAMIC_600_STELLA_LOCAL_PASS_2026-11-16.md

**Implikation:** Data/kopiestart per P0 och P1 är ett **källbelagt alternativt teknikspår** som bör analyseras SOURCE-ONLY; det tar inte bort 76 cykler, 128B RIOT, en resident F6 4KiB-bank eller behovet av P0 gul + vita NPC-färgbyten i värsta X/Y. Inget här bevisar sex fria, tätt överlappande eller korsande X/Y. F10/F11:s P1-only-kostnads- och kopieresultat får inte felaktigt upphöjas till omöjlighetsbevis mot en tvåkanalslösning, men R1g får inte heller upphöjas till generell fri-X.

## 4. Nästa tio ordnade milstolpar — strikt VILLKORLIG PLAN, inte arbetsorder
1. **Källbevisinventering:** Läs R1e/R1f/R1g:s verkliga arkiv, källor och mätningar mot frysta F9/F10/F11, inklusive spriteordning, spelare, testskott, PF och kopie-END. Markera alla saknade tester. MAIN/RESEARCH får analysera utan kodning.
2. **Alternativt objekt-/rasterkontrakt:** Skissa SOURCE-ONLY dynamisk tvåkanals P0/P1-schemaläggning med bevarad gul spelare, sex originalvita NPC, M0 och PF. Visa vilka objekt som ritas i vilken TIA-kanal på samma rasterrad, inklusive COLUP0/GRP0-färgbyten.
3. **Värsta-fall-budget och kollisionspolicy:** Utvärdera exakt 76 CPU-cykler, 128B RIOT, 4KiB aktiv F6-bank, START/latch/GRP-pixelfönster, logiskt numeriskt X/Y, sex same-Y, när-X, delvis skiftat Y, ordningsbyten och avsatt R2/R3-kostnad. Fysiska pixelöverlapp ska redovisas separat; ingen implicit waiver.
4. **Teknisk GO/NO-GO före kod:** Om ingen fullständig källgrundad väg finns, stoppa och dokumentera de återstående exakta design-/hårdvarubeslut som skulle krävas av användaren. Inget nytt experiment eller F12 på endast önsketänkande.
5. **Endast VID GO:** MAIN får överväga en separat, pre-registrerad avgränsad R1-kodorder inom Issue #6, med STOPP, reproducibla pixel-/cykelgrindar och begränsat antal ROM. *Denna plan utfärdar INTE den ordern*.
6. **Endast efter lokalt positivt test:** Reproducera sex rättvända oförändrade originalmasker med sex verkliga numeriska RAM-X/Y, gul spelare, M0 och PF i svåraste R1-fallen, utan kopplade förprogrammerade formationer/felvända bilder/otillåtet flimmer.
7. **R2-diagnostik, separat beslut:** Fem NPC + guldnyckel + gul spelare + aktivt skott på samma band, O1 logisk position bevarad och key-visible efter dödsanimation enligt beslutat gameplaymål (diagnostik behöver inte implementera full döds-/pickup-logik).
8. **R3 + R4 integrationsdiagnostik, med separata avgränsade order:** Höger endast öppningsbar orange port/svart keyhole med PF, därefter deterministisk rörelse/Y-/X-crossing och full rasterstress. Ingen falsk PASS från isolerad R3.
9. **Oberoende E02 och PR-beslut:** När ett fryst samlat R1–R4-diagnospaket faktiskt finns: oberoende DASM/Stella-verifiering mot rätt commit och 16 testfall. PR #7 förblir draft tills relevant godkännande.
10. **Spelbart första steg efter separat uttrycklig användarauktorisation:** Först efter godkänd teknikgrind får MAIN begära nytt mandat för gameplay-ROM med spelarrörelse/skott, NPC-patrull/jakt, hemlig nyckelbärare, nyckel/utgång, poäng/liv/GAME OVER. PAL, balans, ljud, manual och release är senare egna milstolpar och ingår inte automatiskt i v0.18.

**Aktuell och enda omedelbara handlingsprioritet:** nr 1–3 SOURCE-ONLY käll-/arkitekturkontroll av den redan befintliga dual P0/P1-forskningen. Nr 4 är beslutspunkt; nr 5–10 är villkorade och INTE beställda.
