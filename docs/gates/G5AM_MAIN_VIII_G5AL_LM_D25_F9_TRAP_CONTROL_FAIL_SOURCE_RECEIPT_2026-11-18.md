# LET ME OUT! – MAIN VIII / G5AM: G5AL LM-D25 fryst slutmottagning efter hård A-FAIL

**Datum:** 2026-11-18. **Klass:** `MAIN_SOURCE_REVIEW_RECEIPT_ONLY`. **Gällande specialistutfall:** `G5AL_F9_TRAP_CONTROL_FAIL`. **G5-status:** `G5_FORMAL_OPEN`. **LM-D25:** 2/2 nya Actions-mätkörningar förbrukade, avslutad. **Ingen ny ROM, inga nya mätningar och ingen oberoende VERIFICATION II utförd av MAIN.**

## 1. Originalkällor lästa och kontrollerade av MAIN VIII

- **Bindande LM-D25-scope:** [G5AL order](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AL_MAIN_VIII_LM_D25_F9_STABLE_PROMPT_BANK_NEUTRAL_METHOD_AUTHORIZATION_2026-11-18.md), [Issue #17](https://github.com/Odourman/let-me-out/issues/17), [förregistreringsoriginal](https://github.com/Odourman/let-me-out/blob/f16e1e4ac3736e3d6bb1bc0b959b0213e28f6431/rom/g5al_f9_method_2026-11-18/PREREGISTERED_F9_METHOD.md), [riktad ändring före försök 2](https://github.com/Odourman/let-me-out/blob/f16e1e4ac3736e3d6bb1bc0b959b0213e28f6431/rom/g5al_f9_method_2026-11-18/TARGETED_CORRECTION_BEFORE_SECOND_FINAL_RUN.md).
- **Fryst ROM DEVELOPMENT III-leverans:** commit [`f16e1e4ac3736e3d6bb1bc0b959b0213e28f6431`](https://github.com/Odourman/let-me-out/commit/f16e1e4ac3736e3d6bb1bc0b959b0213e28f6431), isolerad branch `rom-dev-iii/g5al-lm-d25-f9-stable-bank-neutral-20261118`, [TO_MAIN](https://github.com/Odourman/let-me-out/blob/f16e1e4ac3736e3d6bb1bc0b959b0213e28f6431/rom/g5al_f9_method_2026-11-18/TO_MAIN_G5AL_F9_METHOD.md), [CSV](https://github.com/Odourman/let-me-out/blob/f16e1e4ac3736e3d6bb1bc0b959b0213e28f6431/rom/g5al_f9_method_2026-11-18/G5AL_F9_METHOD_EVIDENCE.csv), [MANIFEST](https://github.com/Odourman/let-me-out/blob/f16e1e4ac3736e3d6bb1bc0b959b0213e28f6431/rom/g5al_f9_method_2026-11-18/MANIFEST.txt) och scripts. **Verklig GitHub compare** från fryst MAIN-bas `bef65b52556dab99d8eaac4270325704de81dbff`: **14 commits ahead, 0 behind; exakt 10 enbart ADDED-filer** (9 `rom/g5al_...` och 1 workflow), **0 historiska modifierade filer**, ingen merge.
- **Verkliga Actions-run metadata, jobb och loggar** för [run 44203795042](https://github.com/Odourman/let-me-out/actions/runs/44203795042) och [run 44204912620](https://github.com/Odourman/let-me-out/actions/runs/44204912620). Capture-jobb `134464417668` och `134468256971`: **FAIL**; **separata** arkivåterläsningsjobb `134467449687` och `134468721983`: **SUCCESS**, direkt dokumenterat via `sha256sum -c`.
- **Officiella Google Drive original:** [fryst Drive-textarkiv](https://docs.google.com/document/d/1HsGmRV72-HzNliP3UTsxSUnOwJXQOWcSxxoH7x8gvBM/edit), [försök 1 original ZIP](https://drive.google.com/file/d/1qwKIqIBlJ67mUP7b034J78KjgEJxQAQn/view), [försök 2 original ZIP](https://drive.google.com/file/d/1_dSFqTn_bIypBNrsmJiV5WPjgLORwetZ/view). MAIN läste Google Doc samt de tre filernas metadata och **verifierade föräldermappen `1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u`**, ZIP storlekar **35 625** och **32 818** byte, exakt samma som GitHub Actions artifact metadata. En native Google Doc är en textarkivkopia, **inte** byteidentisk ZIP.

## 2. Faktisk källa- och loggkontrollerad matris

| Kontroll | Försök 1, run 44203795042 | Försök 2, run 44204912620 | Bindande G5AL-utfall |
| --- | --- | --- | --- |
| F9 16 384 B ROM SHA/source/list/sym/mask | statisk PASS | statisk PASS | bara original utan nya ROM-byggen |
| A initial verklig debuggerprompt | PASS, `saveSes` 833 B, PC `$F000`, bank0 | PASS, samma typ av riktiga svar | positiv preliminär del |
| A interaktiv `frame #136` | PASS, 1280 B session, frame136, PC `$F063`, bank0 | PASS, frame136 och PC `$F063` | positiv preliminär del |
| A `trapWriteIf RESP1` | `added trap 0`-kvittens, PASS | `added trap 0`-kvittens, PASS | positiv preliminär del |
| A post-`run` komplett nytt RESP1-stopp | verklig `PC=$F1F0`, frame136, scan123, `_sCycles=21`, bank0, session 2893 B och native TIA; **`print pcprint _fCount` / `too many arguments`** ger saknad andra riktiga PC-avläsning => **STRICT FAIL** | nytillkommen debuggerfönstertitel men **`A_REENTRY_HANDSHAKE` `saveSes` skapade ingen giltig session**; inga post-run numeriska värden eller native => **STRICT FAIL** | **A FAIL** |
| A native 320×228 TIA vs G5AF | native PNG SHA `078c9c1ce249cb8c9ef6a45dc322647db2e1a869b3f60635c9e27436f38c016a`; specialistens jämförelse anger 0 pixlar avvikande och hash lika historiska G5AF | ingen native bild | endast positiv avgränsad referens, INTE metod-PASS |
| B bankbunden pre-`STA RESP1` set/PC | INTE KÖRD | INTE KÖRD | **NOT_DETERMINABLE** |
| C exakt en `step` och pre/post native | INTE KÖRD | INTE KÖRD | **NOT_DETERMINABLE** |
| D SHA efter Stella/Xvfb `wait` + separat raw readback | **SUCCESS 44/44 listade filer** | **SUCCESS 39/39 listade filer** | **D arkivintegritet PASS, INTE A–D metod-PASS** |

**Försök 1 original artifact:** [ID 14382688726](https://github.com/Odourman/let-me-out/actions/runs/44203795042/artifacts/14382688726), GitHub-rapporterat **35 625 B**, `sha256:b2edf5609eefb051885bc5eaa5b7cfb8a20e4b9fdeb3e0c9f8df9f389c8d69f7`. Logg från readback-jobb visar 44 `...: OK` och egen slutmarkör `G5AL_ORIGINAL_ARCHIVE_READBACK_SHA256_PASS_ONLY_NOT_METHOD_PASS`.

**Försök 2 original artifact:** [ID 14383206943](https://github.com/Odourman/let-me-out/actions/runs/44204912620/artifacts/14383206943), GitHub-rapporterat **32 818 B**, `sha256:a937861dc55c674abee68146c8e12026bd732e4b36116d55c80aa3b1d39668fe`. Separat jobb bekräftar 39 `...: OK` och samma PASS_ONLY-markör.

**Nivå på MAIN:s påstående:** MAIN har själv läst GitHub-jobbloggar, GitHub-artifact-digests och Drive-metadata. Specialisten redovisar dessutom lokal byte-för-byte omhashning av nedladdade ZIP. **MAIN har inte i denna mottagning själv laddat ned och räknat om råa ZIP-bytes**; inte heller utfört en egen emulator- eller pixeljämförelse. Därför räknas det som källgranskad audit av **separata Actions-readback-jobb** och specialistens rapporterade pixeljämförelse, **inte** oberoende Verification II.

## 3. Tekniskt bevarande och rimlig fortsättning – INGEN ny order

Det är **inte ett ROM-fel som är bevisat**. Det senare misslyckandet ligger **efter** fungerande initial prompt, verklig frame-frammatning och `trapWriteIf`-kvittens. Den nya källmodellen från G5AJ:s `lockHotspots`-analys har alltså gjort förgrinden bättre, men A:s **post-`run`-kommandotransport och sessionexport** är fortfarande otillförlitlig. Försök 1 visar explicit sammanfogade inmatningar i debuggerprompten; försök 2 saknar verifierbar outputfil från `saveSes`. Ingen ensam rotorsak för försök 2 är bevisad.

**MAIN-rekommendation, inte implementationstillstånd:** Stoppa upprepade rena `xdotool`-timingjusteringar utan bevis för att kommandon skickas till en initierad, *interaktivt mottaglig* prompt. En senare **källbaserad metodförstudie utan ny emulator-run** kan analysera inmatningskvittens och filsparningssemantik samt om en mer deterministisk styrmekanism än GUI-tangentbordsautomation finns i exakt Stella 6.7.1. Först efter sådan förstudie och separat nytt uttryckligt användarbeslut kan ett mycket snävt nytt instrumenteringsprov övervägas. Ingen ny C0-ROM, TIA-fysisk colorclock-, M0-/RESP0-/femfienders-verifikation påstås vara gjord.

## 4. Auktoritetsstatus och stopp

**G5AL / LM-D25 SLUTFÖRD VID `G5AL_F9_TRAP_CONTROL_FAIL` enligt dess hårda stoppregler.** **2/2** tillåtna Actions-mätkörningar är förbrukade; ingen tredje körning under LM-D25. G5AJ `G5AJ_F9_TRAP_CONTROL_FAIL` 2/2, G5AH `C0_NO_BUILD_INSTRUMENTATION_BLOCKER` med historiskt ursprungligt hash-FAIL, G5AF `G5AF_INSTRUMENTATION_READY_BOUNDED`, G5AD och G5Z negativa historik bevaras. `G5_FORMAL_OPEN`. **Ingen ny `.asm/.bin`, DASM, C0/X40/X104, C1–C4/N1, H4/G1/G6/F12, S05, fem NPC, spelcanon, Verification II, merge eller senare implementation.**

**Issue #17 avslutas vid uppdragets stoppgräns, aldrig som godkänd metod.** Detta är inte en G5AM-implementation eller en ny G5AM-testorder, utan ett MAIN-mottagningsprotokoll som katalogiserar G5AL-historik. **Project Sources V5/V6 kan behållas som index; ingen ny V7 och inget byte krävs.**
