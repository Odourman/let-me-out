# LET ME OUT! – G5AH / LM-D23: ett snävt C0-baslinjeprov, separat auktoriserat

**Datum:** 2026-11-17. **Beslutande:** användaren via MAIN VIII. **Utförare:** ROM DEVELOPMENT III efter manuell överlämning. **Typ:** ny, avgränsad teknisk auktorisation, inte ändring av spelcanon eller godkänd spelmotor.

## 1. Exakt användarbeslut och tolkning

MAIN VIII rekommenderade: "Begränsa nästa eventuella ROM-prov till att först bevisa mätbarheten hos C0 och därefter, endast om den lyckas, undersöka C1–C4/N1 inom en separat godkänd testorder. Vi ska inte återstarta hela H4 eller försöka bygga femfiendersmotorn ännu."

Användaren svarade därefter **"Ok, fortsätt med det du rekommenderar. Använd dig av GitHub, Google Drive och Project sources"**. MAIN VIII registrerar detta som uttryckligt godkännande att **beställa enbart det första, avgränsade C0-mätprovet** till ROM DEVELOPMENT III. Formuleringen "inom en separat godkänd testorder" betyder att ett faktiskt C1–C4/N1-uppdrag **inte** ingår i LM-D23, även om C0 skulle lyckas. Ingen automatisk G1/H4, G6/F12, S05, fem-NPC-implementation, oberoende Verification eller PR-merge.

**Nytt beslut-ID:** `LM-D23`. **Ensam tillåten ny teknisk familj:** `G5AH_C0_ONLY`. **Initialt statusläge:** `G5AH_C0_AUTHORIZED_NOT_YET_EXECUTED`. Detta återupplivar **inte** G5AD/LM-D21 eller G5AF/LM-D22.

## 2. Bindande original att läsa före arbete

- [Aktuell arbetskö och auktoritet](https://github.com/Odourman/let-me-out/blob/main/docs/CURRENT_AUTHORITY_STATUS_AND_WORK_QUEUE.md) och [G5 spärr](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5_AUTHORIZATION_BOUNDARY_AND_USER_CHOICE_2026-11-17.md).
- [MAIN VIII Stella 6.7.1 source-audit](https://github.com/Odourman/let-me-out/blob/main/docs/gates/MAIN_VIII_STELLA_671_TIA_MEASUREMENT_CAPABILITY_SOURCE_AUDIT_2026-11-17.md) och [beslutsbrief](https://github.com/Odourman/let-me-out/blob/main/docs/gates/MAIN_VIII_G5AF_TO_NEXT_TIA_DECISION_BRIEF_SOURCE_ONLY_2026-11-17.md).
- [G5AD fryst C0–C4/N1-matris](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AD_MAIN_VII_TIA_CALIBRATION_PREREGISTERED_CASES_2026-11-17.csv), **enbart raden TIA-C0 får användas för ny experimentexecution**; resten är historiskt designunderlag.
- [G5AE gamla NO_BUILD](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AE_MAIN_VII_G5AD_NO_BUILD_INSTRUMENTATION_BLOCKER_RECEIPT_AND_STELLA_SAVESES_SOURCE_REVIEW_2026-11-17.md); [G5AG MAIN VIII mottagen instrumentering](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AG_MAIN_VIII_G5AF_F9_INSTRUMENTATION_RECEIPT_2026-11-17.md) och [G5AF fryst reproduktionsmetod](https://github.com/Odourman/let-me-out/blob/c56b52284e7322fdf1c41812ae407429d8fb0f20/rom/g5af_f9_instrumentation_2026-11-17/REPRODUCE_AND_RAW_EVIDENCE.md).
- [8×9 TOP-DOWN-originalmasker](https://github.com/Odourman/let-me-out/blob/main/design/NPC_REFERENCE_8x9_masks.json) och [sex aktuella Project Sources V5](https://github.com/Odourman/let-me-out/tree/main/docs/project_sources/CURRENT_V5). GitHub-originalen, inte källsammanfattningar eller Memory, avgör.

## 3. Exakt tillåtet experiment: endast TIA-C0

**Fas A – hård instrumenterings-/källförgrind, före nytt ROM-bygge:** ROM DEVELOPMENT III kontrollerar versionstroget om Stella **6.7.1** med tillgänglig `step`, `disAsm`, `trapWriteIf`, interaktiv `saveSes`, fryst binär- och source/list/sym-korrelation samt nativ TIA-bild kan skilja:

- värdet vid **numerisk RAM-X** från instruktionens `STA RESP0`-skrivfas, faktisk `_sCycles`, frame och scanline;
- TIA-modellens **härledda** hblank/START-effekter från det som faktiskt **observerats** i samma Stella-build;
- verkliga synliga **0–159 colorclock-X** från nativ bild (320 PNG-kolumner får inte räknas som 320 TIA-colorclocks utan bevisad pixelpar-/offsetmappning);
- exakt **nio TOP-DOWN-maskrader** och att före/efter-/source- och pixeldata hör till samma frame, mode, seed och frysta ROM.

**Om denna beviskedja inte går att reproducerbart instrumentera i förgrinden: STOPPA, bygg INGEN ny ROM** och rapportera `G5AH_C0_NO_BUILD_INSTRUMENTATION_BLOCKER`. Ingen ändring av Stella-källkod, ingen annan emulator/metodfamilj eller oregistrerad loggfunktion (`logTrace` är inte registrerad i Stella 6.7.1).

**Fas B – EN enda minimal diagnos-ROM endast om Fas A PASS:** Standard-F6/NTSC, **16 384 byte**, en enda fryst slutlig `.bin` och `SHA-256`; egna `.asm/.lst/.sym` på isolerad specialistbranch, reproducibelt DASM-bygge. Minst **två kontrollmoder i samma ROM**, med **samma original M 8×9 TOP-DOWN-mask**, fast Y, P0 i isolation och numeriskt RAM-X = **40 respektive 104**; P1, M0, M1, BL och PF av så att de inte är konfunderande. Dokumentera bank, mask- och linjeordning, registerinitiering, `RESP0`-writefas (skilj *source-infererad* från direkt uppmätt), första/sista synliga CC och fulla nio rader för bägge lägen. Förvandla inte off-target-X till en tyst PASS. Färg/visuella kontrollval får inte ändra spelcanon.

Inga nya C1/C2/C3/C4/N1-kontroller, ingen P0/M0 same-Y-kopiekalibrering, ingen H4-kernel, inga framtida fem fiender eller fulla kartor under LM-D23. **C0-PASS kan aldrig vara G5-PASS.**

## 4. Körgräns och leverans

- **Högst två nya GitHub Actions-mätkörningar totalt** inom denna enda C0-familj (initialt försök och högst en riktad korrigering). Om en tredje skulle krävas, STOPP och återrapportera. Ingen ombyggnation till nya ROM-familjer för att dölja negativa resultat.
- Om förgrinden passerar får den enda diagnostiska ROM:en byggas och testas med Stella 6.7.1. Alla slutliga två C0-lägen måste dela **exakt samma ROM-SHA**. Om ett läge är oavgörbart, redovisa det utan att fabricera exakta colorclocks.
- Bevara rå `debugger_session.txt`, full commandsekvens, `autoexec.script`, native 320×228 TIA-PNG, numerisk data-CSV (mode, RAM-X, originalmaskrad, frame/scanline, start/slut-CC, PC, opcode/STA-referens, `_sCycles`, bank), alla relevanta `.lst/.sym`, körloggar och SHA256SUMS i ett reproducerbart Actions-arkiv. Kontrollera arkivets samtliga hashade filer. En GUI-skärmbild är inte native TIA-pixelbevis.
- **Tillåtna per-mode-resultat:** `STELLA_OBSERVED_EXPECTED`, `STELLA_OBSERVED_UNEXPECTED` eller `NOT_DETERMINABLE`, med separata fält för source-/modellhärledda faser. **Global leveransstatus:** `G5AH_C0_MEASUREMENT_COMPLETE_BOUNDED`, `G5AH_C0_PARTIAL_NOT_DETERMINABLE` eller `G5AH_C0_NO_BUILD_INSTRUMENTATION_BLOCKER`.
- Leverera fryst branch/commit, index över nya filer, metod, rå evidens, reproduktionssteg, jämförelse mot kontrollens krav och TO_MAIN till MAIN VIII. **Stanna efter leverans.** MAIN granskar källor och scope, men ersätter inte oberoende VERIFICATION II.
- Historiska G5AD-0-byte-sessionen, Python `IndentationError`, G5AF:s första FAIL, G5Z G0 inconclusive och andra negativa tester bevaras utan redigering och utan omklassificering.

## 5. Status- och rollspärrar

**G5_FORMAL_OPEN.** Ingen ny spelregel, mapperändring, Y-lane- eller flickerwaiver, originalmask- eller kartändring, fem-NPC/AI/kollision/score-/door-S05-implementation, G6/F12, sammanfogning av PR #7 eller beställning av oberoende VERIFICATION II. ROM DEVELOPMENT III arbetar endast efter att MAIN:s order och länkar faktiskt överlämnats i specialistchatten. **GitHub-Issue startar inte en annan chatt eller en CI-körning av sig självt.**

**Villkorat nästa beslut efter färdig C0:** MAIN får analysera och föreslå en **separat** framtida C1–C4/N1-order. Det kräver nytt uttryckligt användargodkännande; ingen automatisk exekvering vid C0-PASS.
