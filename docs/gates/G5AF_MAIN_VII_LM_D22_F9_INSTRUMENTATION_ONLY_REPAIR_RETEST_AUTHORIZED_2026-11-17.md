# LET ME OUT! – MAIN VII G5AF: EN begränsad F9-instrumenteringsreparation och återkontroll
**Datum:** 2026-11-17.
**Beslut:** `LM-D22` – uttryckligt användargodkännande, **endast ett instrumenteringsuppdrag**.
**Status vid utfärdandet:** `G5AF_F9_INSTRUMENTATION_REPAIR_RETEST_AUTHORIZED_NOT_YET_EXECUTED`.
**Utförare:** ROM DEVELOPMENT III. **Mottagare:** MAIN VII. **Oberoende VERIFICATION II:** ej beställd.
**Får göras:** begränsad korrigering av testharness / CI-workflow / logginsamling och körning av **redan fryst F9-binär** i Stella 6.7.1. **Får inte göras:** ny `.asm`, ny `.bin`, DASM-rebuild av F9, G5AD-C0/C1/C2/C3/C4/N1-mätningar, full H4-ONE, G1/G6/F12, S05, femfiender, designändring, sammanslagning eller Verification.

## 1. Spårbart mandat
MAIN VII:s senast uttryckliga rekommendation efter [G5AE mottagning](G5AE_MAIN_VII_G5AD_NO_BUILD_INSTRUMENTATION_BLOCKER_RECEIPT_AND_STELLA_SAVESES_SOURCE_REVIEW_2026-11-17.md):
> "Nästa rimliga insats ... en mycket liten korrigering och återkontroll av instrumenteringen på den befintliga F9-ROM:en. Målet är att först få en icke-tom, reproducerbar logg som går att koppla till CPU- och pixeldata. Det kräver en ny, separat auktorisation."

**Användaren svarade direkt:** "Ok, fortsätt med din rekommendation". Det godkänner **exakt denna begränsade instrumenteringsreparation** i ROM DEVELOPMENT III. Det återaktiverar **inte** det förbrukade `LM-D21/G5AD`-mandatet och är **inte** en ny diagnostisk TIA-ROM-order.

## 2. Faktiska original att kontrollera FÖRE någon kodändring
- [G5AE MAIN:s faktakontroller och stoppspärrar](G5AE_MAIN_VII_G5AD_NO_BUILD_INSTRUMENTATION_BLOCKER_RECEIPT_AND_STELLA_SAVESES_SOURCE_REVIEW_2026-11-17.md), [G5AD förbrukad beställning](G5AD_MAIN_VII_ONE_TIA_PHASE_CALIBRATION_ROM_EXPLICIT_USER_AUTHORIZATION_2026-11-17.md).
- [G5AD frysta stopprapporten](https://github.com/Odourman/let-me-out/blob/1fe92438c3aa0d9f41cca0066f0a95e6c0335acc/rom/g5ad_tia_calibration_2026-11-17/TO_MAIN_G5AD_TIA_CALIBRATION.md), [PREBUILD_REPRODUCTION](https://github.com/Odourman/let-me-out/blob/1fe92438c3aa0d9f41cca0066f0a95e6c0335acc/rom/g5ad_tia_calibration_2026-11-17/PREBUILD_REPRODUCTION.md), [original workflow](https://github.com/Odourman/let-me-out/blob/1fe92438c3aa0d9f41cca0066f0a95e6c0335acc/.github/workflows/g5ad_prebuild_instrument_check.yml) och [rå misslyckad Actions-jobblogg](https://github.com/Odourman/let-me-out/actions/runs/44159356697/job/134308674746). **Bevara G5AD:s 0-byte `saveSes`, `IndentationError` och skärmbildens begränsade bevisvärde som faktiska negativa resultat.**
- Fryst, existerande **F9 F6 NTSC 16 384-byte ROM** från ursprunglig Actions-run `44050126727`, artifact `LET_ME_OUT_R1_F9_ONE_ROM_AND_ACTUAL_STELLA_PARTIAL_OR_COMPLETE_G1`, historiskt SHA-256 **`6c2585148eb082fb8bc794d664edc4869b18849fcfabb9cada23373d1dc1318b`**. **Binären får bara laddas/läsas/köras, inte ändras.**
- Läs faktiskt Stella 6.7.1 i [`PromptWidget::loadConfig`](https://github.com/stella-emu/stella/blob/6.7.1/src/debugger/gui/PromptWidget.cxx#L369-L411), [`Debugger::autoExec`](https://github.com/stella-emu/stella/blob/6.7.1/src/debugger/Debugger.cxx#L175-L201), [`DebuggerParser::executeSaveSes`](https://github.com/stella-emu/stella/blob/6.7.1/src/debugger/DebuggerParser.cxx#L2027-L2057) och [`PromptWidget::saveBuffer`](https://github.com/stella-emu/stella/blob/6.7.1/src/debugger/gui/PromptWidget.cxx#L931-L957).

## 3. Diagnostisk hypotes att pröva, inte på förhand slå fast
`PromptWidget::loadConfig` utför autoexec **före** att `_promptStartPos` färdigställs. G5AD lät `saveSes` exekvera inuti `autoexec.script`. `saveBuffer` skriver bara promptens färdiga rader; denna ordning ger en **starkt underbyggd** förklaring till nollbyte-sessionen. Det är **inte** redan observerat att flyttad `saveSes` löser problemet eller att sparad prompttext utgör tillräcklig timingtrace.

**Åtgärd att utvärdera:** låt autoexec sätta baseline/breakpoint om det fungerar, men **flytta `saveSes` till en verifierat färdiginitialiserad debuggerprompt**; använd kontrollerad GUI-/keyboard-/prompt-automation enligt Stella 6.7.1 och logga exakt när kommandona kördes. Kontrollera kommandosyntax mot den installerade Stella-versionen. Alternativ loggmetod inom samma enda harnessfamilj får väljas om `saveSes` inte kan bära data, men inget ingrepp i Stellas emulator-källkod och ingen ny test-ROM. **Rätta också det separata Python-indenteringsfelet** och säkerställ att PNG och text faktiskt kopieras till Actions-artifakten.

## 4. Litet, falsifierbart kontrakt för *instrumentering*, inte TIA-rendering
- **F9-kontroll:** seed-binärens storlek **16 384 byte**, exakt ovan SHA-256 före och efter. Dokumentera den egna fulla commit-/workflow-/Stella-versionspinningen (Stella 6.7.1, Xvfb, DASM endast verktygsnärvaro).
- **Två olika, förregistrerade F9-stopp** i samma frysta ROM, med uppenbart skilda kända PC-/rasterlägen, härledda ur frysta F9-original och utan gissade adresser. För varje stopp: **namngivet kontroll-ID, PC, CPU-cykelposition, scanline, frame/bank, relevanta aktuella TIA-registervärden** och dokumenterad debugger-command/script-input. CPU-write-end-cykeln för en faktisk `STA` får bara hävdas om den verkligen kan spåras.
- **Verifierbart prompttranskript:** i minst två kontrollerade stopp sparas en *icke-tom*, maskinläsbar/hackbar TXT/CSV-logg som innehåller faktiska numeriska CPU-/TIA-/scanlinevärden. **Byteantal >0 utan spårade värden ger FAIL.** Spara sessionen **efter initiering** och visa i logg hur detta kontrollerades. Skräddarsy textparsing/GUI-automation till den verifierade faktiska utskriften.
- **Nativa bilddata:** producera och **arkivera faktiskt** original `saveSnap`-TIA-bild från samma F9-run/stopp med identifierad frame/scanline, dimensionskontroll och SHA-256; skilj native TIA-bild från helskärms-/GUI-capture. Dokumentera exakt nativ bild→synlig colorclock-transform **endast om käll-/bilddata stödjer den**. Bara PNG utan registerspår är FAIL.
- **Korrelation:** minst två olika stopp måste kunna jämföras reproducerbart mot samma frysta ROM SHA och dokumenterad step/order; granska i artefaktfilen att tillhörande text och PNG faktiskt finns och att `PC/_scan/_sCycles`-värden inte kommer från olika frames av misstag. **Målet är instrumentation READY, inte TIA-fysik mätt**.
- **Bunden försöksslinga:** samma enda reparerade harnessfamilj och **högst två Actions-mätkörningar efter korrigeringen** (ett verifieringsförsök och vid behov en kontrollerad felrättning/omkörning). Återanvänd inte flera olika experimentfamiljer. Vid fortsatt blockerare stoppa och redovisa, utan fler försök.

## 5. Tillåtna slututfall och stopp
- `G5AF_INSTRUMENTATION_READY_BOUNDED`: två källförankrade F9-stopp med reproducerbar faktisk numerisk debuggertext + bevarad/synkad native TIA-bild, båda hashade, och tydligt dokumenterade kvarvarande begränsningar. Detta är **INTE** H4/G5/G6 eller CPU→pixel full TIA proof.
- `G5AF_PARTIAL_INSTRUMENTATION_NOT_READY`: sessioner/bilder sparas men går inte att tidsmässigt eller källmässigt para eller saknar nödvändiga register-/CPU-värden.
- `G5AF_INSTRUMENTATION_BLOCKED`: samma eller annat konkret testharness-fel hindrar även själva spårningen.

**STOPP efter ett av dessa tre utfall.** Ingen automatisk övergång till G5AD-C0–C4/N1, ny ROM, H4, G6/F12, full implementation, ny Verification eller merge. F9:s äldre positiva/negativa rasterresultat ändras aldrig retroaktivt.

## 6. Specialistleverans
- Ny **isolerad ROM DEVELOPMENT III-branch** under t.ex. `rom/g5af_f9_instrumentation_2026-11-17/`, separata nya workflow/script/check-dokument; ändra INTE frysta G5AD-original eller `main` gameplay/kartor.
- `TO_MAIN_G5AF_F9_INSTRUMENTATION.md`: exakt verdict, försökslogg, påvisade `saveSes`-ordningseffekter och begränsningar, samtliga Actions-run-/job-länkar.
- `G5AF_INSTRUMENTATION_EVIDENCE.csv`: två kontrollerade stopp, PC, frame, scanline, CPU, bank, aktuell registerprint, loggfil+hash, native bild+hash, PASS/FAIL/NOT_DETERMINABLE per kontroll; inga påhittade tal.
- Rättad kod (endast workflow/postprocess/GUI-automation), körbara reproduktionssteg, original- och slutmanifest, **råa artefakter faktiskt bevarade och återlästa** från Actions. Om någon fil inte kunde bevaras, redovisa det istället för att hävda nedladdningsbarhet.
- Om möjligt kopia i officiell [Google Drive-projektmapp](https://drive.google.com/drive/folders/1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u) med exakta länkar och faktisk mappmedlemskap. **ROM DEVELOPMENT III egenkontrollerar; MAIN mottar; VERIFICATION II är separat.**

## 7. Nu-status
`G5Z_G0=COMPLETED_INCONCLUSIVE_NO_ROM`.
`G5AD=COMPLETED_NO_BUILD_INSTRUMENTATION_BLOCKER` (historiskt och stängt).
**`G5AF=AUTHORIZED_NOT_YET_EXECUTED` (enbart ny instrumenteringsreparation F9).**
`G5_FORMAL_OPEN`. `NEW_ROM/H4/G1/G6/F12/S05/FIVE_NPC/NEW_VERIFICATION/PR_MERGE=NOT_AUTHORIZED`.
