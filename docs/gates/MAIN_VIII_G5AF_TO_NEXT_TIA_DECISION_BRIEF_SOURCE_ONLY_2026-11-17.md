# LET ME OUT! – MAIN VIII: beslutsläge efter G5AF, före eventuellt nytt TIA-mikroprov

**Datum:** 2026-11-17. **Klass:** `SOURCE_ONLY_DECISION_PREPARATION` (MAIN VIII). **Status:** `NEXT_TIA_EXPERIMENT_NOT_AUTHORIZED`.

Detta dokument är ett uppdaterat beslutsunderlag, **inte** ett nytt LM-D-beslut, implementeringssteg, GitHub Issue, specialistuppdrag, ny ROM eller en beställning av oberoende VERIFICATION II. Det följer på en kontroll av aktuellt GitHub-main, den officiella Drive-mappen och sex CURRENT_V5 Project Sources. Användarens allmänna "fortsätt" avser här fortsatt källgranskning/beslutsberedning, **inte** en ny programmeringsfullmakt.

## 1. Befintliga original och statusordning

1. [Aktuellt auktoritetsindex](https://github.com/Odourman/let-me-out/blob/main/docs/CURRENT_AUTHORITY_STATUS_AND_WORK_QUEUE.md) och [G5:s bindande spärr](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5_AUTHORIZATION_BOUNDARY_AND_USER_CHOICE_2026-11-17.md).
2. [MAIN VIII G5AG mottagning](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AG_MAIN_VIII_G5AF_F9_INSTRUMENTATION_RECEIPT_2026-11-17.md) av [ROM DEVELOPMENT III:s frysta G5AF-resultat](https://github.com/Odourman/let-me-out/blob/c56b52284e7322fdf1c41812ae407429d8fb0f20/rom/g5af_f9_instrumentation_2026-11-17/TO_MAIN_G5AF_F9_INSTRUMENTATION.md) och [rå-CSV](https://github.com/Odourman/let-me-out/blob/c56b52284e7322fdf1c41812ae407429d8fb0f20/rom/g5af_f9_instrumentation_2026-11-17/G5AF_INSTRUMENTATION_EVIDENCE.csv).
3. Historiskt [LM-D21/G5AD: EN villkorad TIA-ROM-order](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AD_MAIN_VII_ONE_TIA_PHASE_CALIBRATION_ROM_EXPLICIT_USER_AUTHORIZATION_2026-11-17.md), [dess förregistrerade C0–C4/N1-matris](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AD_MAIN_VII_TIA_CALIBRATION_PREREGISTERED_CASES_2026-11-17.csv) och [G5AE NO-BUILD-mottagning](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AE_MAIN_VII_G5AD_NO_BUILD_INSTRUMENTATION_BLOCKER_RECEIPT_AND_STELLA_SAVESES_SOURCE_REVIEW_2026-11-17.md). Dessa är frysta historiska dokument, **inte** en återaktiverad order.
4. [G5AC ursprungligt beslutskoncept](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AC_MAIN_VII_TIA_PHASE_CALIBRATION_DECISION_READY_NOT_AUTHORIZED_2026-11-17.md), [G5AA H4-ONE G0 inconclusive](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AA_MAIN_VII_G5Z_G0_INCONCLUSIVE_SOURCE_ONLY_RECEIPT_AND_NEXT_DECISION_2026-11-17.md) och [CURRENT_V5](https://github.com/Odourman/let-me-out/tree/main/docs/project_sources/CURRENT_V5).
5. [Officiell Drive-status](https://docs.google.com/document/d/13ROb1ZXjPjQh7g6xDSGfxIrquhD6xtWI-LCloF9BMPA/edit) och [G5AF arkivkopia](https://docs.google.com/document/d/1MvpvQEAwQRlPr_CH2VVy-gY5LYjebzkPxcUDh0Rk71g/edit). Native Google Docs är navigerings-/arkivkopior och inte byteidentiska med GitHub-original.

**Aktuella grindar:** `G5Z_G0=INCONCLUSIVE_NO_ROM`; `G5AD=NO_BUILD_INSTRUMENTATION_BLOCKER`; `G5AF=INSTRUMENTATION_READY_BOUNDED` efter högst två utförda CI-mätkörningar på **samma gamla frysta F9**; `G5_FORMAL_OPEN`. Issue #14 är stängd för endast instrumentation; PR #7 fortsatt draft; Issue #8 uppskjuten. Ingen full H4, G1/G6/F12, S05, fem-NPC-ROM eller oberoende verifiering har följt.

## 2. Exakt vad G5AF förbättrade – och vad det inte mätte

| Beviskedja | Positivt observerat eller källrapporterat | Fortfarande saknat |
|---|---|---|
| Instrumentering | Interaktiv `saveSes` efter promptinitiering; faktisk Stella 6.7.1-text för PC, frame, scanline, `_sCycles`, bank och `tia`; två nativa 320×228-bilder och specialistkontrollerade hashar | Interna TIA-START-/latchfaser är inte loggade som råa händelser |
| F9 två `RESP1`-fällor | Enligt fryst CSV: PC `$F1F0` / cykel 21 och `$F1F8` / cykel 32, frame 136, scanline 123; sessionsstorlekar 1709/1707 byte | `trapWriteIf`-paus-PC/scanline kan inte automatiskt likställas med exakt `STA RESP1`-slutcykel; native PNG är frusen framebuffer, inte per-colorclock skrivhändelselogg |
| Testartegritet | Andra Actions-körningen och separat artifact-readback-jobb i **samma run** är lyckade enligt GitHub; ROM SHA oförändrad enligt specialist | MAIN har inte egenkört Stella eller oberoende omhashat hela artifact-ZIP; ingen VERIFICATION II eller originalhårdvarukontroll |
| Separat historiskt fel | G5AD:s `saveSes`-ordningshypotes är förenlig med fungerande G5AF-utdata; Python-indenteringen korrigerades i **ny** verifierad harness | Promptens interna `_promptStartPos` mättes inte separat; gammalt G5AD-resultat förblir NO_BUILD |

## 3. Oförändrade mätluckor i G5AD:s sex förregistrerade fall

| Fall | Originalets specifika fråga | Krav som ännu inte uppfyllts av G5AF |
|---|---|---|
| `TIA-C0` | En P0-originalmask, numeriska X=40/104; fysisk pixel-CC och stabil START | Förankra faktisk registerskrivfas till synlig colorclock och rättvända nio maskrader; inte enbart emulatorfönstrets 320-pixelbredd |
| `TIA-C1` | `RESP0` under pågående P0, gul→vit och vit→gul, närliggande X-kontroll | Rått skrivtillfälle kontra faktisk klippning/ghost/START för BÅDA ordningarna |
| `TIA-C2` | `NUSIZ0=$00` jämfört med `$02` och **en** aktiv M0 i samma nio Y-rader | Varje verklig P0-/M0-kopias antal, width och pixel-CC, inte en M0 på tidigare Y |
| `TIA-C3` | C2 med endast skilda `ENAM0`-fönster | CPU-write-/enable-fas korrelerad till en/inga/flera synliga M0-kopior |
| `TIA-C4` | `GRP0/GRP1` före och nära START | Verklig latch-/fördröjningsverkan med `VDELP0/1` explicit, sourceinstruktion + pixelrader |
| `TIA-N1` | Vit P0 + separat begärd gul M0 på samma färgklocka | Faktiskt spårad `COLUP0`-delning i den negativa kontrollen; bara denna allokering, inte generell H4-NO-GO |

G5AF körde **inte** dessa sex fall; inga historiska `AUTHORIZED_NOT_RUN`-markeringar i fryst G5AD-CSV får tolkas som levande order. Här ges **inte** ett universellt genomförbarhetsbesked för fem fritt rörliga NPC.

## 4. MAIN VIII:s nästa tekniska rekommendation – endast om användaren väljer den separat

**Rekommenderad beslutskandidat:** en **enda ny, isolerad standard-F6/NTSC TIA-kalibreringsfamilj** hos ROM DEVELOPMENT III, **inte** återstart av LM-D21/G5AD eller LM-D22/G5AF. Återanvänd den *tekniska idén*, inte de förbrukade mandaten, från G5AD:s frysta C0–C4/N1-kontroller. En gemensam fryst ROM och tydligt dokumenterade separata scenlägen är bättre än växande osammanhängande varianter. Ingen H4-ONE-/fem-NPC-/S05-implementation.

**Den kritiska förbättringen mot gamla G5AD:** före slutlig ROM-mätning måste utvecklaren visa att metoden faktiskt kan korrelera **disassembler/source-PC och avslut av registerskrivning → _sCycles och scanline → TIA-statet → oförändrad nativ bild och råa synliga pixel-colorclocks**, med explicit 320 bildpixel till 160 synliga TIA-CC mapping och rätt bildfas. Om en tillräckligt exakt write-/CC-kedja inte kan styrkas ska den hårda förgrinden åter stanna vid `NO_BUILD` eller ett enskilt fall märkas `NOT_DETERMINABLE`, aldrig fyllas med uppskattade tider.

**Arbetsordning om framtida mandat uttryckligen ges:** C0-baslinjen ska bli mätbar före tolkning av beroende C1–C4; samma-X/Y och färgkontroller i varje relevant par ska vara frysta innan mätning. C2–C3 jämförs endast när samma-Y M0 går att följa. N1 är en avsedd negativ kontroll. Inga nya mask-, kart-, poäng-, spawn-, Y-lane- eller key-synlighetskompromisser tillåts.

**Separat uttrycklig användarauktorisation fordras för:** beställning till ROM DEVELOPMENT III, nya workflow-/Python-/ASM-ändringar som ingår i testet, nytt DASM-bygge, ny ROM, Stella/Actions-mätningar och eventuellt oberoende Verification II. Detta dokument ger inte den auktorisationen.

## 5. Stopp- och mottagningsregler för en eventuellt senare order

- Förregistrera kontrollscener, mätmetod, tillåtna negativa utfall och tids-/resursgräns innan en ny gren eller ny CI-körning startas.
- Behåll G5AD `SESSION_FILE_BYTES=0`, separat Python `IndentationError`, första G5AF FAIL och alla äldre negativa F11/G5H-observationer som historiskt korrekta.
- Skillnad mellan `STELLA_OBSERVED`, specialistens utvecklaregenkontroll och separat `VERIFICATION II` måste redovisas även vid lyckad kalibrering.
- Ingen automatisk H4/G1/G6/F12/S05/fem-NPC-fortsättning, ingen PR-merge, inget byte av aktiv spelcanon eller sex Project Sources genom att ett nytt beslut diskuteras.

**Beslut som återstår hos användaren:** Välj uttryckligen om en ny så avgränsad mätorder ska auktoriseras, eller om allt tekniskt fortsatt ska stå stilla medan MAIN/RESEARCH fortsätter källstudier. Till dess: `NEXT_TIA_EXPERIMENT_NOT_AUTHORIZED`.
