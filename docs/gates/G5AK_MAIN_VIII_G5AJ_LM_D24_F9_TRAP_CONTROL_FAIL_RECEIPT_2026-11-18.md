# LET ME OUT! – MAIN VIII G5AK: mottagning och källgranskning av G5AJ / LM-D24

**Datum:** 2026-11-18. **Klass:** `MAIN_SOURCE_REVIEW_RECEIPT_ONLY` (inte oberoende Verification II, inte ny ROM-testorder). **Specialistens slututfall:** `G5AJ_F9_TRAP_CONTROL_FAIL`. **G5:** `G5_FORMAL_OPEN`. **LM-D24:** förbrukat 2/2 Actions-mätkörningar och avslutat.

## 1. Direkta originalkällor kontrollerade av MAIN VIII

- [LM-D24/G5AJ bindande äldre order](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AJ_MAIN_VIII_LM_D24_F9_DEBUGGER_STOP_METHOD_REPAIR_AUTHORIZED_2026-11-18.md) och [Issue #16 med fryst specialistöverlämning](https://github.com/Odourman/let-me-out/issues/16#issuecomment-6964138600). Fryst specialistcommit [`b0cda0c55b05fa8ceb9763731363fbaada822f0b`](https://github.com/Odourman/let-me-out/commit/b0cda0c55b05fa8ceb9763731363fbaada822f0b), branch `rom-dev-iii/g5aj-lm-d24-f9-debugger-method-20261118`.
- [Full fryst TO_MAIN-rapport](https://github.com/Odourman/let-me-out/blob/b0cda0c55b05fa8ceb9763731363fbaada822f0b/rom/g5aj_f9_method_2026-11-18/TO_MAIN_G5AJ_F9_METHOD.md), [bevis-CSV](https://github.com/Odourman/let-me-out/blob/b0cda0c55b05fa8ceb9763731363fbaada822f0b/rom/g5aj_f9_method_2026-11-18/G5AJ_F9_METHOD_EVIDENCE.csv), [fryst manifest](https://github.com/Odourman/let-me-out/blob/b0cda0c55b05fa8ceb9763731363fbaada822f0b/rom/g5aj_f9_method_2026-11-18/MANIFEST.txt), [förregistrering och riktad korrigering](https://github.com/Odourman/let-me-out/blob/b0cda0c55b05fa8ceb9763731363fbaada822f0b/rom/g5aj_f9_method_2026-11-18/TARGETED_CORRECTION_BEFORE_SECOND_FINAL_RUN.md).
- **Verklig GitHub-compare** från fryst MAIN-bas `25149240815dd04248d9fc5a5b395f1afb85d4d7` till specialistens slutcommit: **11 commits ahead, 0 behind; 9 nya filer**, ingen historisk originalfil ändrad och **ingen merge**.
- [Officiell Google Drive native slutrapport](https://docs.google.com/document/d/1u-cwDlbo1nWvlhFIG_zQ9jakGNAh_rJS9ituIQbwSDI/edit) och [original-ZIP försök 1](https://drive.google.com/file/d/1c9BkHlwZ8FFjK7qLX6iQSP2WftA6IJ-t/view) samt [original-ZIP försök 2](https://drive.google.com/file/d/1JsH3T0l_ngkZ8GtuvXj_Kr0rlHf2-2xP/view). Drive metadata läst direkt: alla tre har förälder **`1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u`**; ZIP-storlekar **29 280** respektive **26 363 byte**, överens med GitHub. Native Google Doc är läsbar textarkivkopia, inte byteidentisk ZIP.
- Historisk oförändrad F9 16 384-byte F6/NTSC-ROM SHA-256 `6c2585148eb082fb8bc794d664edc4869b18849fcfabb9cada23373d1dc1318b`. Fryst källkontroll visar **fyra identiska 4KiB bankbilder** och originala nio M-maskrader `3C 3C 18 FF 18 24 24 42 42`; ingen ny `.asm`/`.bin` och ingen DASM-/C0-körning.

## 2. Faktiskt mätutfall och kontrollernas nivå

| Del | Försök 1 | Försök 2 | Hela G5AJ |
|---|---|---|---|
| Original ROM, source, list, sym, mask | Käll-/hashkontroll PASS | Käll-/hashkontroll PASS | Original endast; ingen ny ROM |
| A förregistrerat F9 `trapWriteIf RESP1` | Verkligt Stella-debuggerfönster och session **1 688 B**, native TIA **320×228**, `PC=$F1F0`, frame 136, scan 123, `_sCycles=21`, **`_bank=3`**, inte föreskrivet **bank 0** = **STRICT FAIL** | `Debugger mode` syntes poll 2, men titeln/prompten försvann före första interaktiva `print pc`; ingen giltig session = FAIL | **`A_FAIL`** |
| B bankbunden pre-STA `break $F1EE` | NOT RUN | NOT RUN | **NOT_DETERMINABLE** |
| C `step` + pre/post native TIA | NOT RUN | NOT RUN | **NOT_DETERMINABLE** |
| D SHA256SUMS + separat archivreadback | **PASS, 27/27** | **PASS, 21/21** | **ARCHIVE_INTEGRITY_PASS_ONLY** |

**Försök 1:** [Actions run 44198377885](https://github.com/Odourman/let-me-out/actions/runs/44198377885), capture-job **134445741776 FAIL**, readback-job **134449813202 SUCCESS**. [Original artifact 14379688339](https://github.com/Odourman/let-me-out/actions/runs/44198377885/artifacts/14379688339), GitHub-rapporterad ZIP SHA-256 `65ec8db7f83275360ea27f3d180a2b955d2b13ada0cd17bbcccdb94c44b1e36c`. MAIN läste både faktiska jobb-loggar och rapporterad artifact-metadata; `sha256sum -c` visar PASS på 27 listade filer.

**Försök 2:** [Actions run 44199817228](https://github.com/Odourman/let-me-out/actions/runs/44199817228), capture-job **134450717591 FAIL**, readback-job **134450997161 SUCCESS**. [Original artifact 14379579815](https://github.com/Odourman/let-me-out/actions/runs/44199817228/artifacts/14379579815), GitHub-rapporterad ZIP SHA-256 `ca63b5dad68c382a1391d882e28124634e637aa4d68417d8d73910675313811c`. `sha256sum -c` PASS på 21 listade filer.

**MAIN:s gräns för granskningspåståendet:** Denna källgranskning verifierar i GitHubs verkliga CI-loggar att separata hash-readback-jobb rapporterade SUCCESS. Specialistens uppgift att dessutom själv ha räknat om nedladdade ZIP-original är **redovisad i rapporten**, men MAIN har inte i denna mottagning själv laddat ned och lokalt omhashat ZIP-bytes. Det är inte oberoende VERIFICATION II av emulerade TIA-effekter.

## 3. Ny viktig slutsats som inte ändrar specialistens FAIL

- F9-ROM:s **fyra 4KiB bankar innehåller identiska bytes** enligt kontrollerad källa. Därför är bank-3-observationen inte i sig belägg för felaktiga bildpixlar eller en misslyckad ROM: den visar **ett annat faktiskt emulatortillstånd** än förregistrerad bank-0-referens. G5AJ testade uttryckligen bank 0, så **försök 1 förblir strikt FAIL** och får aldrig tyst omklassas.
- G5AJ:s försök-1 native TIA SHA `078c9c1ce249cb8c9ef6a45dc322647db2e1a869b3f60635c9e27436f38c016a` är enligt specialistens egna källor **samma SHA som G5AF:s ursprungliga M-RESP1-bild**. Bildlikhet kan därför sammanfalla med olika banknummer i denna byteidentiska F9-referens. Det är **inte** ett bevis för C0, femfienders-PASS eller PC-breakpoint/pre/post-stegning.
- Försök 2 införde en förhandsdokumenterad källbaserad `dump $fff6 $fff6`-bank-fixture, men detta kunde inte bekräftas med faktisk `print _bank` eftersom debuggerprompten försvann före inmatning. **Ingen bevisad rotorsak**, inget bank0-runtime-PASS.
- De två återstående orsaksgrupperna att utreda separat, **utan ny körning**, är F6-bank-/test-fixture-semantik respektive debuggerns `autoexec`/`run`-livscykel och GUI-promptens övergång. Är det värt ett **nytt separat mandat** bör det framtida provet välja en stabil kontrollmekanism, isolera en parameter åt gången, och inte börja med C0-ROM. Inget nytt test beställt här.

## 4. Projektstatus och stoppgräns

**G5AJ / LM-D24 SLUTFÖRD VID FAIL enligt hårda stoppregler.** Högst 2/2 tillåtna mätkörningar förbrukade. **Inga nya Stella-/Actions-runs under LM-D24.** G5AH `C0_NO_BUILD_INSTRUMENTATION_BLOCKER` och dess ursprungliga hash-FAIL, G5AF `INSTRUMENTATION_READY_BOUNDED`, G5AD `NO_BUILD_INSTRUMENTATION_BLOCKER` och G5Z `INCONCLUSIVE_NO_ROM` bevaras. **G5 `G5_FORMAL_OPEN`; inget C0/X40/X104/H4/G6/S05/5-NPC.** Ingen PR-merge, ingen automatisk Verification II eller senare Step-order.

**Project Sources:** Statisk senaste GitHub-guide `CURRENT_V6`; redan uppladdade ChatGPT V5 kan behållas som navigering, inga nya source-filer eller byten behövs. Detta protokoll är en MAIN source-only mottagning, inte implementationsbeslut eller självständig sanningsstämpel för emulatorns osedda effekter.
