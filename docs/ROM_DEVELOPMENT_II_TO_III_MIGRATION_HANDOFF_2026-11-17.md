# LET ME OUT! – ROM DEVELOPMENT II → ROM DEVELOPMENT III

**Datum:** 2026-11-17. **Typ:** dokumentär migrering av en dedikerad utvecklarchatt, INTE en ny implementation eller auktorisation. **Mottagare:** ROM DEVELOPMENT III. **MAIN:** MAIN V. **Projekt:** enbart Atari 2600-spelet "Let Me Out!".

## 1. Mål och auktoritet

Den tidigare chatten är lång. Den nya chatten ska ta över roll, exakt fryst status, källor, arbetsmetod, blockerare och stoppgränser **utan att upprepa historiska ROM-experiment, förlita sig på ChatGPT Memory eller själv auktorisera F12**. Den kan inte bokstavligen flytta tidigare chatthistorik; den ska i stället läsa beständiga källor.

**Beslutsordning:** användarens direkta krav och MAIN V:s senaste uttryckliga arbetsorder > MAIN:s senaste faktiska mottagnings-/statusbeslut > frysta exakta commits, verkliga ROM/.lst/.sym, ZIP-hashade Stella-original och Actions > forskningsdokument, de 30 Atari-tricken och migration > chattminnen. Äldre historiska sektioner i CURRENT_PROJECT_STATE kan finnas kvar; utgå inte från att en titel daterad 15 november speglar rubrikens senaste faktiska innehåll. Nyare/högre auktoritet slår en gammal migration.

**Källor att öppna LIVE:**
- GitHub: https://github.com/Odourman/let-me-out
- Drive-projektmapp: https://drive.google.com/drive/folders/1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u
- MAIN-status: https://github.com/Odourman/let-me-out/blob/main/docs/CURRENT_PROJECT_STATE_2026-11-15.md
- Autorisation, scope, acceptance: `docs/ROM_GATE_V018_AUTHORIZATION_2026-11-15.md`, `docs/ROM_GATE_V018_SCOPE.md`, `docs/ROM_GATE_V018_ACCEPTANCE.md`, `docs/MAIN_SIX_INDEPENDENT_X_V018_2026-11-15.md`
- Utvecklarrollens ursprungliga arbetsordning: `docs/MAIN_V_ROM_DEVELOPMENT_STARTPROMPT_2026-11-16.md`.
- GitHub Issue #6: https://github.com/Odourman/let-me-out/issues/6
- PR #7: https://github.com/Odourman/let-me-out/pull/7 – vid denna kontroll OPEN/DRAFT/UNMERGED, HEAD `82667dae033f70570dce903f8e1d4866528be02a`
- VERIFICATION Issue #8: https://github.com/Odourman/let-me-out/issues/8 – OPEN men fristående Verification för F11 **inte** startad.
- KANON original M/F/SM/SF: `design/NPC_REFERENCE_8x9_masks.json`, Git blob `058800a4c1904d1ff289e7e61b3902aa111ba16d`.

## 2. Exakt frysta utvecklarresultat och deras bevisgränser

### F9 – MAIN V accepterad diagnostisk lokal PASS
- Fryst commit `c36982aef770af6cd3f68c2da37b8ed14aee2393`; rapport: https://github.com/Odourman/let-me-out/blob/c36982aef770af6cd3f68c2da37b8ed14aee2393/rom/v018/experiments/r1_free_xy/TO_MAIN_R1_F9.md
- Klass: `F9_THREE_BINARY_RUNTIME_SELECTORS_LOCAL_PASS`. EN standard-F6/NTSC-ROM, 16 384 byte, ROM SHA256 `6c2585148eb082fb8bc794d664edc4869b18849fcfabb9cada23373d1dc1318b`.
- Tre TOP-DOWN originalmasker (stor man, stor kvinna, liten man), TRE separata **BINÄRA** RAM-X-väljare i samma ROM, alla 8 kombinationer, 12/12 ortogonala X-kontraster, **144/144** autentiska Stella-bilder, 48 registertraps + 8 WSYNC-traps. MAIN kontrollerade ursprungligt ZIP och alla 499 filhashar. **Ingen numeriskt fri X/Y** och ingen fjärde/sjätte NPC.
- Ursprungs-ZIP i Drive: https://drive.google.com/file/d/15NquSf1pXcLnSKBzU1fjypDl7RASFR6b/view ; ZIP SHA256 `fd0127ecba3997a624a74dd1d357f6b2638543f9fc31de120d4968067213c4da`; 499/499 hashkontroll. Bygg inte om F9 enbart för migrationen.

### F10 – MAIN V accepterad SOURCE ONLY
- Fryst commit `ef854d7436f1e1650827e2e19cc1b3d33a17f054`; rapport: https://github.com/Odourman/let-me-out/blob/ef854d7436f1e1650827e2e19cc1b3d33a17f054/docs/ROM_DEV_R1_F10_SIX_FREE_XY_ARCHITECTURE_SOURCE_ONLY_TO_MAIN_2026-11-17.md
- Klass `F10_NO_CURRENT_F6_SIX_FREE_XY_ARCHITECTURE_PROVEN`. Samtliga 30 Atari-trick återlästa, tre arkitekturfamiljer: A dynamisk P1-retriggering, B bankfördelade standard-F6-kernlar, C adaptiv NUSIZ/Y-multiplex. Ingen hel sex fritt numerisk X/Y-lösning styrkt; det är **inte** ett universellt omöjlighetsbevis.
- Endast en Markdown-rapport skapades, inga ASM/ROM/DASM/Stella/CI.

### F11 – SENASTE leverans, G0 FAIL och absolut INGEN F11-ROM
- Bindande historiska MAIN V-order: https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_V_TO_ROM_DEV_II_R1_F11_FOUR_NUMERIC_X_P1_DIAGNOSTIC_ONE_ROM_AUTHORIZED_2026-11-17.md
- Fryst **F11** commit `dfe21c80b7cbdcdd20138ebf5eadf4b89dbf0cc4`, branch `rom-dev/v018-r1-f11-g0-hard-stop-source-only-20261117`; rapport: https://github.com/Odourman/let-me-out/blob/dfe21c80b7cbdcdd20138ebf5eadf4b89dbf0cc4/rom/v018/experiments/r1_free_xy/TO_MAIN_R1_F11.md
- Klass `F11_SOURCE_ONLY_INFEASIBLE`: G0 kunde inte fastställa en säker källstyrkt **NUMERISK** P1-fyrkopie-/START-/GRP-plan för fyra olika TOP-DOWN original M,F,SM,SF och exakt förregistrerad A `[16,36,56,76]` respektive B `[19,36,56,76]` **fysiska TIA colorclocks** (+3 CC bara för första NPC). Den tidigare F9-cropkalibreringen föreslog A `[41,81,121,161]` och B `[47,81,121,161]` men **detta har aldrig mätts för F11**.
- Fysisk risk: nästa P1-RESP1-reset kan behöva inträffa medan föregående kopia fortfarande ritas; Stella 6.7.1 Player har **en** rendering/sample-räknare. Exakt START-fas för dessa fyra positioner och generell numerisk RAM→deadline-scheduler kunde inte styrkas. En förprogrammerad A/B-formationskernel hade brutit mot beställningens numeric-X-kriterium. 76-cykel- och RAM/F6-kalkyler är inte ett generellt bevis på omöjlighet.
- **HÅRD STOPP: G0 FAIL, G1 NOT RUN.** Exakt **0 nya F11-ROM, 0 DASM, 0 Stella, 0 CI**, en enda Markdown-rapport. Påstå inte F11 ROM_FAIL eller fjärde-NPC Stella-PASS.
- F11:s formella Issue #6-handoff: https://github.com/Odourman/let-me-out/issues/6#issuecomment-6946394788
- **MAIN V:s separata F11-mottagning har inte kunnat verifieras i repo-main vid denna migration.** Kontrollera LIVE om något nyare MAIN-beslut/arbetsorder tillkommit. Anta INTE F12-auktorisation.

**Full R1/v0.18: `BLOCKED / NOT ACCEPTED`.** Äldre isolerad R3/C02 har developer local PASS men ingen R1+R3-integration; R2 key/O1, full sexmask C01/C04, grafikkraven och fristående E02 Verification är inte slutgodkända. Tidigare R1ba 600-frame forskning har MAIN-oberoende konstaterad felvänd orientering för stora masker och kopplade profiler; använd inte R1ba som källrättvänd produktionskernel. Tidigare låsta positiva/negativa ROM-/Actions-serier ska inte startas om vid byte av chatt.

## 3. Roll, spelkrav och förändringsförbud

**MAIN V** äger prioritering, mottagningar, grindar och separat **uttrycklig auktorisation** av varje nytt Step/F12, liksom beslut när en fryst batch ska gå till VERIFICATION.

**ROM DEVELOPMENT III** är teknisk utvecklare: får skriva assembler, bygga, felsöka och självkontrollera **ENDAST inom en aktuell ny bindande MAIN-arbetsorder**. Ska då arbeta självständigt och följa orderns max ROM, förkontroller och hard stop utan att behöva "fortsätt" för varje mikroiteration. Resultatet ska vara en enda reproducerbar fryst rapport och, endast om beställt, bevisarkiv. Research är rådgivande, SOURCE_ONLY är inte kört, developer-local PASS är inte independent PASS.

**VERIFICATION** ska **inte** automatiskt kallas på grund av en handoff. Issue #8 är separat; MAIN beslutar vid en större fryst evidensbatch. **GRAPHICS** är stängt/pausat. Oförändrade top-down-originalmasker, gul P0-spelare, aktiv M0-projektil, brun PF, 262 NTSC, 76 CPU-cykler och standard-F6 är låsta för den nuvarande v0.18-diagnostiken. R2 har guldnyckel och O1, R3 asymmetrisk högersidig dörr med orange/svart komponent, men inget nytt arbete på dessa steg är tillåtet här.

**Inget vid migrationen auktoriserar:** F12, fjärde alternativ F11-ROM, ny registerfassvep, femte/sjätte test-NPC, R1+R3-integrationsbygge, R2–R4/PAL/fullspel, F6SC/DPC/ARM/ny mapper, ändrat antal androider, ändrade masker/färger/nyckel/dörr, självinitierad research/CI eller PR #7-merge. `main` och alla tidigare frysta F2–F11-filer får inte modifieras för att migrationsrapporten ska se mer "aktuell" ut.

## 4. Den nya chattens uppstart – exakt arbetssekvens

1. Läs detta **hela** handoff direkt från GitHub (alternativt Drive-spegeln). Kolla GitHub och Google Drive live. Om en plugin inte är ansluten, säg tydligt det; hitta inte på en läst fil.
2. Kontrollera MAIN:s senaste verkliga order och receipt, den låsta originalmasken, exakt F9/F10/F11 och F11 Issue #6; kontrollera PR #7 samt Issue #8. Om ett nyare beslut faktiskt finns gäller det framför denna migration.
3. Läs de relevanta roll- och acceptance-filerna. Förstå **fysiskt TIA CC vs 900×300-crop**, CPU-write vs intern P1 START/latch vs WSYNC efter skrivning och att 4×4KiB F6 inte ger fler 8-bitars players.
4. Skicka MAIN V en **kort mottagningsrapport** med vilka anslutningar som faktiskt fungerar, frysta SHA/status, sista F11-hard-stop och öppna blockerare samt eventuella källkonflikter. Högst två korta möjliga framtida **beslutsalternativ**, inga nya tester.
5. Stanna. Status: `ROM DEVELOPMENT III: MIGRATION READY – F11 G0 SOURCE-ONLY STOP; F9 LIMITED LOCAL PASS; FULL R1 BLOCKED; AWAIT MAIN V.`

## 5. Kopierbar startprompt till helt ny chatt

**LET ME OUT! – ROM DEVELOPMENT III / REN NY UTVECKLARCHATT**

Du är den NYA dedikerade **ROM DEVELOPMENT III-chatten** för Atari 2600-spelet **"Let Me Out!"**. Du ersätter ROM DEVELOPMENT II. Du är inte MAIN V, inte GRAPHICS, inte RESEARCH och inte oberoende VERIFICATION.

**Detta är en MIGRERING, inte en ny implementationorder.** Gör inga nya ROM-byggen, inga DASM-/Stella-/CI-körningar, inga källändringar eller grafikförändringar vid uppstart. MAIN V ensam ger separat uttrycklig auktorisation för ett senare F12 eller annat nytt scope.

**LÄS FÖRST HELA GITHUB-HANDOFFEN:** https://github.com/Odourman/let-me-out/blob/handoff/rom-development-ii-to-iii-20261117/docs/ROM_DEVELOPMENT_II_TO_III_MIGRATION_HANDOFF_2026-11-17.md

**GÅ DÄREFTER TILL VERKLIGA KÄLLOR, INTE MEMORY:** GitHub https://github.com/Odourman/let-me-out, projektets Drive https://drive.google.com/drive/folders/1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u, MAIN-status och senaste receipts/orders, ROM_GATE v0.18 authorization/scope/acceptance, `design/NPC_REFERENCE_8x9_masks.json`, Issue #6, PR #7 och Issue #8. Läs och kontrollera exakta frysta F9-, F10- och F11-rapporter och deras commit-SHA. Använd anslutna **GitHub- och Google Drive-verktyg direkt** och verifiera faktisk åtkomst och eventuella senare auktoritativa ändringar. Låt aldrig ett äldre handoff övertrumfa MAIN:s nyare order.

**STATUS DU MÅSTE FÖRSTÅ:**
- **F9** = `F9_THREE_BINARY_RUNTIME_SELECTORS_LOCAL_PASS`, fryst `c36982aef770af6cd3f68c2da37b8ed14aee2393`, accepterad developer-local 16KiB F6-ROM med tre rättvända originalmasker, tre **BINÄRA** RAM-X, 144 äkta Stella-bilder, alla 8 lägen och 12/12 oberoende X-kontraster. **Inte tre numeriskt fria X/Y.**
- **F10** = `F10_NO_CURRENT_F6_SIX_FREE_XY_ARCHITECTURE_PROVEN`, fryst `ef854d7436f1e1650827e2e19cc1b3d33a17f054`, accepterad SOURCE_ONLY: A dynamisk P1-retrigger, B F6-bankfördelning och C adaptiv NUSIZ analyserades mot alla 30 Atari-trick; ingen full sex fri X/Y bevisad.
- **F11** = `F11_SOURCE_ONLY_INFEASIBLE`, fryst `dfe21c80b7cbdcdd20138ebf5eadf4b89dbf0cc4`, efter obligatorisk **G0 FAIL och HÅRD STOPP FÖRE G1**. Fysiska A `[16,36,56,76]` och B `[19,36,56,76]` CC för M/F/SM/SF saknar säker datadriven NUMERIC-RAM-X/P1-START-och-GRP-deadline-plan. **F11 byggde INGEN ROM och körde INGEN DASM, Stella eller CI.** Kontrolleras i frysta TO_MAIN_R1_F11.md och Issue #6. F11 har levererats till MAIN; kontrollera själv om MAIN därefter har mottagit det och auktoriserat något nytt. Anta aldrig att F12 är beslutad.
- **Full R1/v0.18 är BLOCKED / NOT ACCEPTED.** PR #7 är vid denna snapshot draft/omerget; VERIFICATION Issue #8 standby; inga grafikändringar eller R1+R3/fullspel är auktoriserade.

**ROLL OCH BESLUT:** Du ska kunna använda DASM, Stella, debugger, GitHub Actions och Drive **när en framtida explicit MAIN-order tillåter detta**. Då följer du dess G0/G1-grindar och ROM-tak, bygger inte en reserv-ROM efter FAIL, skiljer CPU-registerskrivning från intern TIA-START, behåller top-down originalgrafiken och levererar riktiga hashade bevis. Du arbetar självständigt inom scope men börjar aldrig följande fas själv. Developer-local PASS är inte oberoende Verification. Ingen ny mapper, F6SC/ARM, R2–R4, PAL, grafik, PR-merge eller designwaiver utan separat uttrycklig behörighet.

**GÖR NU ENDAST FÖLJANDE:** verifiera verktygsåtkomst och källor live; redovisa fryst F9/F10/F11 status, F11:s blockerare och eventuell nyare auktoritativ ändring i en kort mottagningsrapport till MAIN V. **Bygg ingenting, ändra ingenting, kör inga nya experiment.** Stanna sedan med exakt status:

`ROM DEVELOPMENT III: MIGRATION READY – F11 G0 SOURCE-ONLY STOP; F9 LIMITED LOCAL PASS; FULL R1 BLOCKED; AWAIT MAIN V.`

Invänta en NY separat MAIN V-arbetsorder. Denna startprompt är inte sådan en order.
